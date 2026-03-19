
import time
import math
import numpy as np
import rclpy as rp
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor

from my_project_package_msgs.action import DistTurtle
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist




class TurtlesimSubscriber(Node):
    def __init__(self, ac_server):
        super().__init__('turtlesim_subscriber')
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.callback,
            10
        )
        self.ac_server = ac_server
        
    def callback(self, msg):
        self.ac_server.current_pose = msg

        

class DistTurtleServer(Node):
    def __init__(self):
        super().__init__("dist_turtle_action_server")
        
        self.action_server = ActionServer(
            self, DistTurtle, 'dist_turtle', self.execute_callback)
        self.publisher = self.create_publisher(
            Twist, '/turtle1/cmd_vel',10)
          
        self.current_pose = Pose()
        self.previous_pose = Pose()
        self.start_pose = Pose()
        self.is_first_time = True
        self.total_dist = 0.0
        


    def cal_diff_pose(self):
        # 거리 계산 하는 함수

        if self.is_first_time:
            self.previous_pose.x = self.current_pose.x
            self.previous_pose.y = self.current_pose.y
        
            self.is_first_time = False
        
        diff_pose = math.sqrt((self.current_pose.x - self.previous_pose.x)**2 + 
                              (self.current_pose.y - self.previous_pose.y)**2)

        self.previous_pose = self.current_pose

        return diff_pose

    def execute_callback(self, goal_handle):
        
        self.start_pose.x = self.current_pose.x
        self.start_pose.y = self.current_pose.y
        feedback_msg = DistTurtle.Feedback()
        
        # 요청 만큼 움직이기
        twist = Twist()
        twist.linear.x = goal_handle.request.linear_x
        twist.angular.z = goal_handle.request.angular_z

        # 움직이기
        while True :
            # 거리계산
            self.total_dist+= self.cal_diff_pose()
            self.remain_dist = goal_handle.request.dist - self.total_dist
            self.publisher.publish(twist)
            
            # feedback 
            feedback_msg.remained_dist = self.remain_dist
            goal_handle.publish_feedback(feedback_msg) # 피드백 메시지 주는거
            time.sleep(0.1)
            
            if self.remain_dist <= 0.2:
                    break
        
        # 원위치로 돌아가기
        if goal_handle.request.return_home == True:
            self.publisher.publish(Twist())
            time.sleep(0.5)
            
            # 제자리 회전
            twist.linear.x = 0.0
            

            # 처음 theta 값 구하기 
            angle_to_home = math.atan2(
                self.start_pose.y - self.current_pose.y,
                self.start_pose.x - self.current_pose.x
                )
            
            while True:
                diff_angle = angle_to_home - self.current_pose.theta
                twist.angular.z = diff_angle * 0.5  # 가까울수록 천천히 회전
                self.publisher.publish(twist)
                time.sleep(0.1)
                if abs(diff_angle) <=0.05:
                    break
            
            # 돌아가기(전진)
            # 초기화
            self.total_dist = 0.0
            self.is_first_time = True 

            home_dist = math.sqrt(
                (self.start_pose.x - self.current_pose.x) ** 2 +
                (self.start_pose.y - self.current_pose.y) ** 2
                )
            
            while True :
                self.total_dist+= self.cal_diff_pose()
                print(self.total_dist)
                self.remain_dist = home_dist - self.total_dist
                
                # 가까워질 수록 느리게
                twist.linear.x = max(0.1, self.remain_dist * 0.5)
                twist.angular.z = 0.0
                self.publisher.publish(twist)
            
                # feedback 
                feedback_msg.remained_dist = self.remain_dist
                goal_handle.publish_feedback(feedback_msg) # 피드백 메시지 주는거
                time.sleep(0.1)
                if self.remain_dist <= 0.2:
                        break
   

        
        # Result 반환
        goal_handle.succeed()
        result = DistTurtle.Result()
        result.pos_x = self.current_pose.x
        result.pos_y = self.current_pose.y
        result.pos_theta = self.current_pose.theta
        result.result_dist = self.total_dist
    
        # 초기화
        self.total_dist = 0.0
        self.is_first_time = True


        return result



def main(args=None):
    rp.init(args=args)
    dist_turtle = DistTurtleServer()
    sub_turtle = TurtlesimSubscriber(dist_turtle)

    executor = MultiThreadedExecutor()

    executor.add_node(dist_turtle)
    executor.add_node(sub_turtle)
    
    try:

        executor.spin()

    finally:

        executor.shutdown()
        sub_turtle.destroy_node()
        dist_turtle.destroy_node()
        rp.shutdown()



if __name__ == '__main__':
    main()