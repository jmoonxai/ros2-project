
import ipdb
import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class TurtlesimWallAvoid(Node):
    def __init__(self):
        super().__init__('turtle_wall_avoid')

        self.pose = Pose()
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.callback, 10
            )        
            
        self.publisher = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
            )
        
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

            
        

    def timer_callback(self):
        
        twist = Twist()
        
        # 가까운지 판단
        WALL_LIMIT = 1.0
        
        if self.pose.x > 11.0 - WALL_LIMIT and abs(self.pose.theta) < math.pi / 2:
            twist.angular.z = 1.0
            twist.linear.x = 1.0

        elif self.pose.x < WALL_LIMIT and abs(self.pose.theta) > math.pi / 2:
            twist.angular.z = 1.0
            twist.linear.x = 1.0

        elif self.pose.y < WALL_LIMIT and self.pose.theta < 0:  # ✅ 아래 향할 때
            twist.angular.z = 1.0
            twist.linear.x = 1.0

        elif self.pose.y > 11.0 - WALL_LIMIT and self.pose.theta > 0:  # ✅ 위 향할 때
            twist.angular.z = 1.0
            twist.linear.x = 1.0

        else:
            twist.linear.x = 2.0

        self.publisher.publish(twist)



    def callback(self, msg):
        self.pose = msg
        print("X:",self.pose.x, "Y:",self.pose.y, "theta:",self.pose.theta)


def main():
    rp.init()

    turtlesim_node = TurtlesimWallAvoid()
    rp.spin(turtlesim_node)
    
    turtlesim_node.destroy_node()
    rp.shutdown()




if __name__ == "__main__" :
 
    main()





