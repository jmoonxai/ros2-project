# ros2-project-1-beginner



# 🟢 프로젝트 입문

> 목표
> 섹션 1에서 배운 Publisher / Subscriber 패턴을 각각 독립 프로젝트로 완성한다.
> 새로운 개념 없이 배운 것만으로 끝낼 수 있는 프로젝트 2개.





## 프로젝트 A — 거북이 키보드 조종기

**▸ 한 줄 설명**

키보드 입력(`w a s d`)을 받아 `cmd_vel` 토픽을 발행하고 turtlesim 거북이를 실시간으로 조종한다.





**▸ 핵심 학습 포인트**

- `create_publisher()` + `create_timer()` 패턴 복습
- Python `input()` 또는 `sys.stdin`으로 키 입력 처리
- `Twist` 메시지의 `linear.x` / `angular.z` 필드 제어





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
