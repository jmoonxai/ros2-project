
# 🤖 Project — Python Action Client로 순차 다중 이동

## 프로젝트 목표

터미널 명령(`ros2 action send_goal`) 없이 **Python 코드로 Action Client 노드**를 작성한다.
3개의 Goal을 **이전 Goal이 완료된 후 순서대로** 전송하고,
각 단계의 Feedback과 최종 Result를 터미널에 출력한다.

완성 기준:
- Python `ActionClient` 코드로 Goal 전송 가능
- 이전 Goal 완료 전까지 다음 Goal 미전송 (순차 실행)
- 각 Goal마다 Feedback(남은 거리) 실시간 출력
- 각 Goal 완료 시 Result(최종 위치, 총 이동 거리) 출력
- 3개 Goal 모두 완료 후 노드 자동 종료

--

## 사전 준비 체크리스트

- [ ] `dist_turtle_action_server.py` 정상 실행 확인
- [ ] `ActionServer` 코드 구조 완전 이해
- [ ] `rclpy.action` 모듈 문서 한 번 훑기

--

## Action Client 개념 이해

Action Client는 Action Server에 Goal을 보내고 Feedback/Result를 받는 노드다.
서버와 달리 **비동기(async)** 방식으로 동작한다. 핵심 흐름은 아래와 같다.

```
send_goal_async(goal)          ← Goal 전송 (비동기)
    ↓ Future 반환
goal_response_callback()       ← 서버가 Goal 수락/거부 시 호출
    ↓ get_result_async() 등록
feedback_callback()            ← 서버가 publish_feedback() 할 때마다 호출
    ↓
get_result_callback()          ← 서버가 succeed() 후 Result 반환 시 호출
    ↓ 다음 Goal 전송
```

> [!info] Future 패턴이란?
> `send_goal_async()`는 즉시 Future 객체를 반환한다. 결과가 아직 없지만,
> 나중에 완료되면 `add_done_callback()`으로 등록한 함수를 자동 호출한다.
> 이것이 ROS2 비동기 프로그래밍의 핵심 패턴이다.

---

## Step 1 — Goal 목록 설계

3개의 Goal을 리스트로 정의한다. 각 항목은 딕셔너리로 관리한다.

```python
GOALS = [
    {'linear_x': 1.0, 'angular_z': 0.0, 'dist': 2.0},   # 직선 이동
    {'linear_x': 0.5, 'angular_z': 0.5, 'dist': 3.0},   # 나선형 이동
    {'linear_x': 0.8, 'angular_z': -0.3, 'dist': 2.5},  # 반대 방향 나선
]
```

--

## Step 2 — Action Client 클래스 기본 구조

## Step 3 — 콜백 함수 3개 구현

### ① goal_response_callback: Goal 수락/거부 처리

### ② feedback_callback: 중간 상태 출력

### ③ get_result_callback: Result 처리 및 다음 Goal 전송

## Step 4 — main 함수 및 실행 진입점

## Step 5 — setup.py 등록 및 빌드

## Step 6 — 실행

```bash
# 터미널 1: turtlesim 실행
ros2 run turtlesim turtlesim_node

# 터미널 2: Action Server 실행
source ~/ros2_study/install/setup.bash
ros2 run my_first_pkg dist_turtle_action_server

# 터미널 3: Action Client 실행
source ~/ros2_study/install/setup.bash
ros2 run my_first_pkg dist_turtle_action_client
```

### 예상 터미널 출력 (클라이언트)
```
[INFO] 🔍 Action Server 연결 대기 중...
[INFO] 🔗 서버 연결 완료
[INFO] 📤 Goal 1/3 전송: dist=2.0
[INFO] ✔️  Goal 수락됨 — 실행 중...
[INFO]   📡 Feedback — 남은 거리: 1.953 m
[INFO]   📡 Feedback — 남은 거리: 1.821 m
...
[INFO] 🏁 Goal 1 완료
[INFO]    최종 위치: x=6.23, y=7.41, theta=1.23
[INFO]    총 이동 거리: 2.013 m
[INFO] 📤 Goal 2/3 전송: dist=3.0
...
[INFO] ✅ 모든 Goal 완료!
```

--

## 완성 확인 체크리스트

- [ ] Goal 1 완료 전까지 Goal 2가 전송되지 않음
- [ ] 각 Goal마다 Feedback이 출력됨
- [ ] 각 Goal마다 Result(위치, 거리)가 출력됨
- [ ] 3개 Goal 완료 후 노드가 자동 종료됨
- [ ] 서버가 없을 때 `wait_for_server()` 가 무한 대기함을 확인

---
