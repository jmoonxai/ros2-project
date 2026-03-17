# Standard Library
import time
from datetime import datetime

# Third-party
import ipdb
import pandas as pd
import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose



class TurtlesimSubscriber(Node):
    def __init__(self):
        super().__init__('turtle_sub_logger')
        self.subscription = self.create_subscription(
            
            Pose,
            '/turtle1/pose',
            self.callback,
            10
        )
        self.count = 0

    
    def save_realtime_to_csv(self, msg=None):
    # 첫 번째 실행 시 헤더 포함 저장
        
        path = r"/home/jaemoon/jm/pose_log.csv"
        first_write = True
        
        # 실시간 데이터 수집 (예시)
        new_data = {
            "timestamp": datetime.now(),
            "X": msg.x,  # 실제 데이터 함수로 교체
            "Y": msg.y,  # 실제 데이터 함수로 교체
            "Theta": msg.theta,  # 실제 데이터 함수로 교체
        }
        
        df = pd.DataFrame([new_data])
        
        # mode='a': append, header=first_write: 첫 번째만 헤더 쓰기
        if self.count == 0:
            self.count += 1
        else:
            first_write = False

        df.to_csv(path, mode='a', header=first_write, index=False)
        first_write = False
        

    def callback(self, msg):

        self.save_realtime_to_csv(msg=msg)        
        print("X:",msg.x, "Y:",msg.y, "theta:",msg.theta)


def main():
    rp.init()

    turtlesim_subscriber = TurtlesimSubscriber()
    rp.spin(turtlesim_subscriber)
    
    turtlesim_subscriber.destroy_node()
    rp.shutdown()




if __name__ == "__main__" :
 
    main()





