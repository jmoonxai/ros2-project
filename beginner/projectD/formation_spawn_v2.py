import rclpy
from rclpy.node import Node
import math
import time
from my_custom_interfaces.srv import FormationSpawn
from turtlesim.srv import Spawn
from turtlesim.srv import TeleportAbsolute
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from turtlesim.srv import Kill


class Formation_spawn(Node):

    def __init__(self):
        super().__init__('formation_spawn_jm')

        self.cb_group = ReentrantCallbackGroup()  # ✅ 재진입 허용

        self.srv = self.create_service(
            FormationSpawn,
            'Formation_JM',
            self.add_callback,
            callback_group=self.cb_group  # ✅ 적용
        )

        self.get_logger().info('Formation_JM Service Ready')


        self.spawn_client = self.create_client(
            Spawn,
            'spawn',
            callback_group=self.cb_group  # ✅ 적용
        )
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('spawn service not available, waiting...')
        
        self.kill_client = self.create_client(
            Kill, 'kill',
            callback_group=self.cb_group
        )
        while not self.kill_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('kill service not available, waiting...')
        


        self.request = Spawn.Request()

        self.center_x = 5.5
        self.center_y = 5.5

        self.turtle_names = ['turtle1']
        self.teleport_clients = {}



    def compute_formation(self, formation: str, num: int, scale: float):

        if num <= 0:
            return [], [], [], "invalid num"

        if scale <= 0.0:
            return [], [], [], "invalid scale"

        formation = formation.lower()
        
        if formation == "circle":
            
            return self.compute_circle(num, scale)
            
        elif formation == "triangle":
            return self.compute_triangle(num, scale)

        elif formation == "grid":
            return self.compute_grid(num, scale)

        else:
            return [], [], [], "unknown formation"

    def compute_circle(self, num: int, radius: float):

        x = []
        y = []
        theta = []

        for i in range(num):

            angle = 2.0 * math.pi * i / num

            px = self.center_x + radius * math.cos(angle)
            py = self.center_y + radius * math.sin(angle)

            # 원 중심 바라보기
            yaw = angle + math.pi

            x.append(px)
            y.append(py)
            theta.append(self.normalize_angle(yaw))

        return x, y, theta, "success"

    def compute_triangle(self, num: int, spacing: float):
        x = []
        y = []
        theta = []

        # 필요한 row 개수 계산
        rows = 0
        total = 0
        while total < num:
            rows += 1
            total += rows

        count = 0

        for row in range(rows):
            row_count = row + 1

            # 삼각형 전체 높이 기준 중앙 정렬
            local_y = ((rows - 1) / 2.0 - row) * spacing

            for col in range(row_count):
                if count >= num:
                    break

                # 각 row를 x축 중앙 정렬
                local_x = (col - row / 2.0) * spacing

                px = self.center_x + local_x
                py = self.center_y + local_y

                x.append(float(px))
                y.append(float(py))
                theta.append(0.0)

                count += 1

        return x, y, theta, "success"

    def compute_grid(self, num: int, spacing: float):

        x = []
        y = []
        theta = []

        cols = math.ceil(math.sqrt(num))
        rows = math.ceil(num / cols)

        count = 0

        for r in range(rows):

            for c in range(cols):

                if count >= num:
                    break

                local_x = (c - (cols - 1) / 2.0) * spacing
                local_y = -(r - (rows - 1) / 2.0) * spacing

                px = self.center_x + local_x
                py = self.center_y + local_y

                x.append(px)
                y.append(py)
                theta.append(0.0)

                count += 1

        return x, y, theta, "success"

    def normalize_angle(self, angle: float):

        while angle > math.pi:
            angle -= 2.0 * math.pi

        while angle < -math.pi:
            angle += 2.0 * math.pi

        return angle

    
    def get_active_turtles(self) -> list[str]:
        """현재 활성화된 turtle 이름 목록을 topic 목록으로 추론"""
        active = []
        # get_topic_names_and_types() 는 spin 불필요, 즉시 반환
        for topic, _ in self.get_topic_names_and_types():
            # /turtle1/pose, /turtle_2/pose ... 패턴으로 확인
            parts = topic.split('/')
            if len(parts) == 3 and parts[2] == 'pose':
                active.append(parts[1])
        return active
    

       
    def _get_teleport_client(self, turtle_name):  # ✅ 클라이언트 캐싱으로 중복 생성 방지
        if turtle_name not in self.teleport_clients:
            client = self.create_client(
                TeleportAbsolute,
                f'/{turtle_name}/teleport_absolute',
                callback_group=self.cb_group
            )
            self.teleport_clients[turtle_name] = client
        return self.teleport_clients[turtle_name]
    
        
    def _wait_future(self, future, timeout=5.0): # ✅ spin_until_future_complete 대신 폴링 대기
        start = time.time()
        while not future.done():
            if time.time() - start > timeout:
                self.get_logger().error('Future timeout')
                return False
            time.sleep(0.01)
        return True
    

    def add_callback(self, request, response):

        x, y, theta, result = self.compute_formation(
            request.formation,
            request.num,
            request.scale
        )

        response.x = x
        response.y = y
        response.theta = theta
        response.result = result

        if result != "success":
            return response

        # ── 1. 목표 turtle 이름 목록 ──────────────────────────────────
        target_names = ['turtle1']
        for i in range(1, int(request.num)):
            target_names.append(f'turtle_{i + 1}')

        # ── 2. 현재 살아있는 turtle 목록 파악 ─────────────────────────
        current_names = self.get_active_turtles()   # 아래 메서드 참고

        current_set = set(current_names)
        target_set  = set(target_names)

        
        # ── 3. 남는 turtle 제거 (turtle1 은 kill 불가이므로 제외) ──────
        to_kill = current_set - target_set
        for name in to_kill:
            if name == 'turtle1':
                continue
            kill_req = Kill.Request()
            kill_req.name = name
   
            self._wait_future(self.kill_client.call_async(kill_req))
            self.teleport_clients.pop(name, None)  # 캐시도 제거
            self.get_logger().info(f'Killed: {name}')

        # ── 4. 부족한 turtle 생성 ─────────────────────────────────────
        to_spawn = target_set - current_set
        for name in to_spawn:
            if name == 'turtle1':
                continue
            spawn_req = Spawn.Request()
            spawn_req.name  = name
            spawn_req.x     = self.center_x
            spawn_req.y     = self.center_y
            spawn_req.theta = 0.0
            #future = self.spawn_client.call_async(spawn_req)

            self._wait_future(self.spawn_client.call_async(spawn_req))
            self.get_logger().info(f'Spawned: {name}')

        
        # ── 5. 전체 대형 위치로 이동 ───────────────────────────────────
        for i, name in enumerate(target_names):

            teleport_client = self._get_teleport_client(name)
     
            if not teleport_client.wait_for_service(timeout_sec=1.0):
                self.get_logger().warn(f'{name} teleport service not available')
                continue

            teleport_req = TeleportAbsolute.Request()
            teleport_req.x     = float(response.x[i])
            teleport_req.y     = float(response.y[i])
            teleport_req.theta = float(response.theta[i])

            #future = teleport_client.call_async(teleport_req)
            self._wait_future(teleport_client.call_async(teleport_req))

        return response


    



def main(args=None):
    rclpy.init(args=args)
    node = Formation_spawn()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()

if __name__ == '__main__':
    main()
