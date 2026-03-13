# ros2-project-1-beginner



# 🟢 프로젝트 입문

> [!summary] 목표
> 섹션 1에서 배운 Publisher / Subscriber 패턴을 각각 독립 프로젝트로 완성한다.
> 새로운 개념 없이 배운 것만으로 끝낼 수 있는 프로젝트 2개.

---

## 프로젝트 A — 거북이 키보드 조종기

**▸ 한 줄 설명**

키보드 입력(`w a s d`)을 받아 `cmd_vel` 토픽을 발행하고 turtlesim 거북이를 실시간으로 조종한다.

---

**▸ 핵심 학습 포인트**

- `create_publisher()` + `create_timer()` 패턴 복습
- Python `input()` 또는 `sys.stdin`으로 키 입력 처리
- `Twist` 메시지의 `linear.x` / `angular.z` 필드 제어

---

**▸ 패키지 구조**

```
my_first_package/
└── my_first_package/
    ├── my_first_node.py
    ├── my_subscriber.py
    ├── my_publisher.py
    └── turtle_teleop.py      ← 새로 만들 파일
```

---

**▸ 구현 단계**

**Step 1. 키 입력 → Twist 변환 로직 설계**

| 키 | linear.x | angular.z | 동작 |
|----|----------|-----------|------|
| `w` | 2.0 | 0.0 | 앞으로 |
| `s` | -2.0 | 0.0 | 뒤로 |
| `a` | 0.0 | 2.0 | 좌회전 |
| `d` | 0.0 | -2.0 | 우회전 |
| 그 외 | 0.0 | 0.0 | 정지 |

**Step 2. 노드 코드 작성**

```python
import rclpy as rp
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

class TurtleTeleop(Node):
    def __init__(self):
        super().__init__('turtle_teleop')
        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.key = ''

    def get_key(self):
        # 논블로킹 키 입력
        settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = sys.stdin.read(1) if rlist else ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def timer_callback(self):
        self.key = self.get_key()
        msg = Twist()

        if   self.key == 'w': msg.linear.x =  2.0
        elif self.key == 's': msg.linear.x = -2.0
        elif self.key == 'a': msg.angular.z =  2.0
        elif self.key == 'd': msg.angular.z = -2.0

        self.publisher.publish(msg)
        self.get_logger().info(f'key: {self.key}')

def main(args=None):
    rp.init(args=args)
    node = TurtleTeleop()
    rp.spin(node)
    node.destroy_node()
    rp.shutdown()
```

**Step 3. `setup.py` entry_points 추가**

```python
'turtle_teleop = my_first_package.turtle_teleop:main',
```

**Step 4. 빌드 & 실행**

```bash
cd ~/ros2_study
colcon build
ros2_study

# 터미널 1
ros2 run turtlesim turtlesim_node

# 터미널 2
ros2 run my_first_package turtle_teleop
