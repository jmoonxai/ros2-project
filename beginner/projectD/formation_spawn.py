from my_project_package_msgs.srv import FormationSpawn
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import Spawn


import time
import numpy as np
import rclpy as rp
from rclpy.node import Node
import math


class MulitiFormationSpawn(Node):
    def __init__(self):
        super().__init__("mul_fom_spawn")
        # 서비스 서버
        self.server = self.create_service(FormationSpawn, "mul_fom_spawn", self.add_callback)
        
        # Spawn 서비스 클라이언트
        self.client_spawn = self.create_client(Spawn, '/spawn')
        self.req_spawn = Spawn.Request()

        self.center = 5.54


    def get_triangle_positions(self, num, spacing=2.):
        positions_x = []
        positions_y = []
        positions_theta = []
        layer = 0
        
        while len(positions_x) < num:
            layer += 1
            for col in range(layer):
                x = (col - (layer - 1) / 2.0) * spacing
                y = -(layer - 1) * spacing * math.sqrt(3) / 2
                positions_x.append(x)
                positions_y.append(y)
                positions_theta.append(0.0)
                if len(positions_x) == num:
                    break

        return positions_x, positions_y, positions_theta
        
    def calc_position(self, n, r=3):
        gap_theta = 2*np.pi /n
        theta = [gap_theta*i for i in range(n)]
        x = [r*np.cos(th) for th in theta]
        y = [r*np.sin(th) for th in theta]

        return x, y, theta

    def add_callback(self, request, response):

        # ✅ 서버 준비 확인 추가
        if not self.client_spawn.wait_for_service(timeout_sec=2.0):
            self.get_logger().error('/spawn 서비스 없음!')
            return response
        
        # 배치 정하기
        if request.formation == "circle":
            x, y, theta = self.calc_position(request.num)
        elif request.formation == "triangle":
            x, y, theta = self.get_triangle_positions(request.num)
        
        for n in range(request.num):
            self.req_spawn.x = x[n] + self.center
            self.req_spawn.y = y[n] + self.center
            self.req_spawn.theta = theta[n] 

            self.client_spawn.call_async(self.req_spawn)
        
        # response 값 전달
        
        response.x = x
        response.y = y
        response.theta = theta
        
        return response


def main(args=None):
    rp.init(args=args)
    multi_spawn= MulitiFormationSpawn()
    rp.spin(multi_spawn)
    rp.shutdown()


if __name__ == '__main__':
    main()