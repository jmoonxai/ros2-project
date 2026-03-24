
import rclpy as rp
from rclpy.node import Node
from std_msgs.msg import String
from rcl_interfaces.msg import SetParametersResult

class ParamPublisher(Node):
    def __init__(self):
        super().__init__('param_publisher')
        # create_publisher(메시지타입, 토픽이름, queue_size)
        self.publisher_ = self.create_publisher(String, 'params', 10)
         
         # 1. 파라미터 선언
        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('message_prefix', "hello")

        # 2. 변수로 저장
        self.publish_rate = self.get_parameter('publish_rate').value
        self.message_prefix = self.get_parameter('message_prefix').value

        # 타이머 생성
        self.timer = self.create_timer(0.5, self.timer_callback)

        # 3. 변경 콜백 등록
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'[{self.message_prefix}] count: {self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(msg.data)
        self.count += 1
    
    def parameter_callback(self, params):
        for param in params:
            if param.name == 'publish_rate':
                self.publish_rate = param.value
                self.timer.cancel()
                timer_period = 1.0 / self.publish_rate
                self.timer = self.create_timer(timer_period, self.timer_callback)
            elif param.name == 'message_prefix':
                self.message_prefix = param.value
        return SetParametersResult(successful=True)     



def main():
    rp.init()

    turtlesim_publisher = ParamPublisher()
    rp.spin(turtlesim_publisher)
    
    turtlesim_publisher.destroy_node()
    rp.shutdown()




if __name__ == "__main__" :
 
    main()





