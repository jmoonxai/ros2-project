
import rclpy as rp
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType





class TurtleParams(Node): 
    def __init__(self):
        super().__init__("turtle_my_param")

        # 파라미터
        self.colors = [
        {'background_r': 69,  'background_g': 86,  'background_b': 255},  # 파랑
        {'background_r': 69,  'background_g': 200, 'background_b': 69},   # 초록
        {'background_r': 200, 'background_g': 100, 'background_b': 200},  # 핑크
        ]
        
        self.index = 0

        
        # turtlesim에 파라미터 전달할 서비스 클라이언트
        self.client = self.create_client(
            SetParameters,
            '/turtlesim/set_parameters'
        )

        self.client.wait_for_service(timeout_sec=5.0)
        # 3초마다 색 변경하는 타이머
        self.timer = self.create_timer(3.0, self.cycle_color)
        

    def cycle_color(self):
        if self.index == 3:
            self.timer.cancel()
            self.get_logger().info('종료합니다!')
            raise SystemExit  # ← 노드 종료
            
        
        color = self.colors[self.index % len(self.colors)]
        self.get_logger().info(f'색 변경: {color}')

        for param_name, param_value in color.items():
            self.apply_background(param_name, param_value)
        self.index += 1


    def apply_background(self, param_name, param_value):
        # 3. 요청 데이터 만들기
        # 4. 비동기로 요청 전송
        request = SetParameters.Request()
        p = Parameter()
        p.name = param_name
        p.value = ParameterValue(
            type=ParameterType.PARAMETER_INTEGER,
            integer_value=param_value
        )
        request.parameters = [p]
        self.client.call_async(request)
        



def main(args=None):
    rp.init(args=args)
    dist_turtle = TurtleParams()
    rp.spin(dist_turtle)
    rp.shutdown()

if __name__ == '__main__':
    main()