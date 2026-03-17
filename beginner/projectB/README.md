
## 프로젝트 B — 거북이 위치 로거

**▸ 한 줄 설명**

`turtle1/pose`를 구독해 x, y, 각도를 시간과 함께 CSV 파일로 저장한다. 나중에 matplotlib으로 이동 경로를 시각화할 수 있다.

---

**▸ 핵심 학습 포인트**

- `create_subscription()` 패턴 복습
- Python 파일 I/O (`csv` 모듈)와 ROS2 콜백 조합
- `self.get_clock().now()` 로 ROS2 타임스탬프 활용

---

**▸ 패키지 구조**

```
my_first_package/
└── my_first_package/
    └── turtle_logger.py      ← 새로 만들 파일

~/ros2_study/
└── turtle_log.csv            ← 저장될 로그 파일
```

---

**▸ 구현 단계**

**Step 1. CSV 저장 로직 설계**

```
timestamp, x, y, theta, linear_velocity, angular_velocity
```

**Step 2. 노드 코드 작성**



**Step 3. `setup.py` entry_points 추가**

```python
'turtle_logger = my_first_package.turtle_logger:main',
```

**Step 4. 빌드 & 실행**

```bash
cd ~/ros2_study
colcon build
ros2_study

# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: Publisher (거북이 움직이게)
ros2 run my_first_package my_publisher

# 터미널 3: 로거 실행
ros2 run my_first_package turtle_logger

# 저장된 파일 확인
cat ~/ros2_study/turtle_log.csv
```

---

**▸ 확장 아이디어**

- matplotlib으로 x, y 좌표를 플롯해 이동 경로 시각화
- 일정 줄 수마다 파일을 rotate하는 로직 추가
- 로그 파일 경로를 파라미터로 받도록 개선
