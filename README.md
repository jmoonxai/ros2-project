# ROS2 Project

ROS2를 단계별로 학습하고 프로젝트를 정리하는 저장소입니다.

---

## Learning Progress

<!-- AUTO-PROGRESS-START -->
| Stage | Progress |
|------|---------|
| Beginner | 🟡 7 projects |
| Intermediate | ⚪ 0 projects |
| Advanced | ⚪ 0 projects |
<!-- AUTO-PROGRESS-END -->

---

## Project Structure

<!-- AUTO-STRUCTURE-START -->
```text
ros2-project/
└── beginner/
    └── projectA/
    └── projectB/
    └── projectC/
    └── projectD/
    └── projectE/
    └── projectF/
    └── projectG/
```
<!-- AUTO-STRUCTURE-END -->

---

## Projects

<!-- AUTO-PROJECTS-START -->
### Beginner

| Project | Description | Status | Tags |
|--------|-------------|-------|------|
| [projectA](beginner/projectA) | `키보드 입력(`w a s d`)을 받아 `cmd_vel` 토픽을 발행하고 turtlesim 거북이를 실시간으로 조종한다. | 🟢 Completed | ros2, beginner, pubsub |
| [projectB](beginner/projectB) | `turtle1/pose`를 구독해 x, y, 각도를 시간과 함께 CSV 파일로 저장한다. 나중에 matplotlib으로 이동 경로를 시각화할 수 있다. | 🟢 Completed | ros2, beginner, pubsub |
| [projectC](beginner/projectC) | pose 토픽으로 거북이의 현재 위치를 실시간으로 감지하고, 벽에 가까워지면 자동으로 방향을 전환하는 노드를 구현한다. "센서 → 판단 → 제어" 루프를 처음으로 직접 구현하는 프로젝트 | 🟢 Completed | ros2, beginner, pubsub |
| [projectD](beginner/projectD) | 서비스로 대형 이름(`circle` / `triangle` / `grid`)과 마릿수를 요청하면 해당 모양으로 거북이들을 배치하는 시스템을 구현한다. 멀티 스폰 코드의 `calc_position()`을 대형별로 확장하는 프로젝트로, 수식 변경만으로 다양한 형태를 만들 수 있다. | 🟢 Completed | ros2, beginner, pubsub |
| [projectE](beginner/projectE) | 기존 DistTurtleServer를 확장해서, Goal에 return_home: true를 포함시키면 이동 완료 후 거북이가 출발 위치로 자동 복귀하도록 만든다. | 🟢 Completed | ros2, beginner, pubsub |
| [projectF](beginner/projectF) | 터미널 명령(ros2 action send_goal) 없이 Python 코드로 Action Client 노드를 작성한다. 3개의 Goal을 이전 Goal이 완료된 후 순서대로 전송하고, 각 단계의 Feedback과 최종 Result를 터미널에 출력한다. | 🟢 Completed | ros2, beginner, pubsub |
| [projectG](beginner/projectG) | R터미널에서 `ros2 param set`을 손으로 치는 대신, Python 스크립트 하나가 3가지 색상을 3초 간격으로 자동 순환시킨다. 파라미터 CLI 명령어의 동작 방식을 코드로 자동화하는 연습이다. | 🟢 Completed | ros2, beginner, pubsub |

<!-- AUTO-PROJECTS-END -->
