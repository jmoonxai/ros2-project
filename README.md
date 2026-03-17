# ROS2 Project

ROS2를 단계별로 학습하고 프로젝트를 정리하는 저장소입니다.

---

## Learning Progress

<!-- AUTO-PROGRESS-START -->
| Stage | Progress |
|------|---------|
| Beginner | 🟡 4 projects |
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
| [projectD](beginner/projectD) | 서비스로 대형 이름(`circle` / `triangle` / `grid`)과 마릿수를 요청하면 해당 모양으로 거북이들을 배치하는 시스템을 구현한다. 멀티 스폰 코드의 `calc_position()`을 대형별로 확장하는 프로젝트로, 수식 변경만으로 다양한 형태를 만들 수 있다. | Completed | ros2, beginner, pubsub |

<!-- AUTO-PROJECTS-END -->
