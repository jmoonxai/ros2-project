
import numpy as np
import rclpy as rp
from rclpy.node import Node
from rclpy.action import ActionClient
from my_project_package_msgs.action import DistTurtle




class DistTurtleClient(Node):
    def __init__(self):
        super().__init__('dist_turtle_action_client')
        self.action_client = ActionClient(
                self, DistTurtle,'dist_turtle')
            # Goal 목록 및 현재 인덱스
        self.goals = [
            {'linear_x': 1.0, 'angular_z': 0.0, 'dist': 2.0, "return_home": False},
            {'linear_x': 0.5, 'angular_z': 0.5, 'dist': 3.0, "return_home": False},
            {'linear_x': 0.8, 'angular_z': -0.3, 'dist': 2.5, "return_home": False},
        ]
        self.current_goal_index = 0



    def send_goal(self):
        
        if self.current_goal_index+1 > len(self.goals):
            #import ipdb; ipdb.set_trace()
            self.get_logger().info('✅ 모든 Goal 완료!')
            rp.shutdown()

        

        goals = self.goals[self.current_goal_index]

        # Goal 메시지 생성
        goal_msg = DistTurtle.Goal()
        goal_msg.linear_x = goals["linear_x"]
        goal_msg.angular_z = goals["angular_z"]
        goal_msg.dist = goals["dist"]
        goal_msg.return_home = goals["return_home"]

        # 서버 기다리기
        self.action_client.wait_for_server(timeout_sec=5.0)

        # Goal 보내기 (비동기)
        self._send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    # Goal 요청 결과 받기
    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('❌ Goal rejected')
            return

        self.get_logger().info('✅ Goal accepted')

        # 결과 요청
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self.result_callback)

    # 진행 상황 (Feedback)
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'📊 Feedback: {feedback.remained_dist}')

    # 최종 결과
    def result_callback(self, future):
        result = future.result().result
        
        self.get_logger().info(
            f'🏁 Goal {self.current_goal_index + 1} 완료\n'
            f'   최종 위치: x={result.pos_x:.2f}, y={result.pos_y:.2f}, '
            f'theta={result.pos_theta:.2f}\n'
            f'   총 이동 거리: {result.result_dist:.3f} m'
        )
       

        # 인덱스 증가 후 다음 Goal 전송
        self.current_goal_index += 1
        self.send_goal()

    




def main(args=None):
    rp.init()

    action_client = DistTurtleClient()
    
    # 서버가 준비될 때까지 대기
    action_client.get_logger().info('🔍 Action Server 연결 대기 중...')
    action_client.action_client.wait_for_server()
    action_client.get_logger().info('🔗 서버 연결 완료')
    
    action_client.send_goal()

    rp.spin(action_client)



if __name__ == '__main__':
    main()