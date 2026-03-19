# 🐢 Project — 거북이 이동 완료 후 자동 복귀

## 프로젝트 목표

기존 `DistTurtleServer`를 확장해서, Goal에 `return_home: true`를 포함시키면
이동 완료 후 거북이가 **출발 위치로 자동 복귀**하도록 만든다.

완성 기준:
- `return_home: false` → 기존과 동일하게 동작
- `return_home: true` → 목표 거리 이동 후 출발 위치 근처로 복귀
- 복귀 중에도 남은 거리가 Feedback으로 출력됨
- 복귀 완료 후 Result 반환

---

## 사전 준비 체크리스트

- [ ] Chapter 03 전체 강의 수강 완료
- [ ] `dist_turtle_action_server.py` 정상 실행 확인
- [ ] `ros2 action send_goal`로 기본 이동 테스트 완료

---

## Step 1 — Action Definition 수정

### 파일 위치
```
~/ros2_study/src/my_first_pkg_msgs/action/dist_turtle.action
```

### 수정 내용
기존 파일에 `return_home` 필드 한 줄을 추가한다.

```
# Goal
float32 linear_x
float32 angular_z
float32 dist
bool return_home        ← 추가

---
# Result
float32 pos_x
float32 pos_y
float32 pos_theta
float32 ret_dist

---
# Feedback
float32 remain_dist
```

### 빌드 확인
```bash
cd ~/ros2_study
colcon build
source install/setup.bash
ros2 interface show my_first_pkg_msgs/action/DistTurtle
```

예상 출력에 `bool return_home` 줄이 보이면 성공이다.


## Step 2 — 출발 위치 저장 로직 추가


## Step 3 — 복귀 함수 구현


## Step 4 — execute_callback에 복귀 로직 연결


## Step 5 — 빌드 및 실행

```bash
# 빌드
cd ~/ros2_study
colcon build
source install/setup.bash

# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: Action Server 실행
ros2 run my_first_pkg dist_turtle_action_server

# 터미널 3-A: 복귀 없이 테스트
ros2 action send_goal --feedback /dist_turtle \
  my_first_pkg_msgs/action/DistTurtle \
  "{linear_x: 0.8, angular_z: 0.4, dist: 2.0, return_home: false}"

# 터미널 3-B: 복귀 있이 테스트
ros2 action send_goal --feedback /dist_turtle \
  my_first_pkg_msgs/action/DistTurtle \
  "{linear_x: 0.8, angular_z: 0.4, dist: 2.0, return_home: true}"
```

---

## 완성 확인 체크리스트

- [ ] `return_home: false` 시 기존과 동일하게 동작
- [ ] `return_home: true` 시 이동 완료 후 복귀 시작
- [ ] 복귀 중 Feedback의 `remain_dist` 값이 감소
- [ ] 복귀 완료 후 Result가 반환됨
- [ ] 두 번째 Goal 전송 시에도 정상 동작 (상태 초기화 확인)

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `return_home` 필드가 없다는 에러 | `.action` 파일 수정 후 빌드 안 함 | `colcon build` 후 소싱 재실행 |
| 복귀 시작 후 거북이가 제자리 회전만 함 | `linear.x`가 0 또는 너무 작음 | `msg.linear.x` 값 증가 |
| `current_pose`가 (0.0, 0.0)으로 저장됨 | pose 수신 전에 저장함 | `time.sleep(0.3)` 추가 |
| 복귀가 끝나지 않음 | tolerance가 너무 작음 | 0.3 → 0.5로 증가 |

---

## 도전 과제 (선택)

1. 복귀 시 단순 고정 속도 대신, 출발점까지 **거리에 비례한 속도**로 이동하도록 개선하라.
2. Feedback 메시지에 `is_returning: bool` 필드를 추가해서 이동 중인지 복귀 중인지 구분하라.
3. 복귀 완료 후 **출발 시 방향(theta)** 까지 원복하는 기능을 추가하라.
