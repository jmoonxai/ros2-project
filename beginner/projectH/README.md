
# 🟡 ROS2 파라미터 실습 프로젝트

## 프로젝트 개요

**파라미터로 동작이 바뀌는 주기 퍼블리셔 노드**

- `publish_rate`와 `message_prefix` 두 파라미터를 가진 퍼블리셔 노드를 만든다. 
- `ros2 param set`으로 값을 바꾸면 퍼블리시 주기와 메시지 내용이 노드 재시작 없이 즉시 반영된다.
- `declare_parameter`, `get_parameter`, `add_on_set_parameters_callback` 세 API를 모두 실전 적용하는 프로젝트다.



## 목표

- 파라미터를 선언하고 변수로 가져오는 패턴을 익힌다.
- 파라미터 콜백에서 `self` 변수를 업데이트하는 구조를 직접 구현한다.
- `ros2 topic echo`로 변경 전후 메시지를 비교해 콜백이 정상 동작하는지 검증한다.



## 요구사항

**파라미터 사양**

| 파라미터 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `publish_rate` | float | 1.0 | 초당 퍼블리시 횟수 |
| `message_prefix` | string | `"hello"` | 메시지 앞에 붙는 텍스트 |

**출력 예시**
```
[hello] count: 0
[hello] count: 1
# ros2 param set /param_publisher message_prefix "ROS2" 실행 후
[ROS2] count: 2
[ROS2] count: 3
```



## 검증 순서

```bash
# 터미널 1: 노드 실행
ros2 run my_first_pkg param_publisher

# 터미널 2: 메시지 수신 확인
ros2 topic echo /param_topic

# 터미널 3: 파라미터 변경 테스트
ros2 param set /param_publisher message_prefix "ROS2"
ros2 param set /param_publisher publish_rate 5.0
```



## 확인 기준

- [ ] 노드 실행 후 `ros2 topic echo /param_topic`으로 `[hello] count: N` 메시지 수신
- [ ] `ros2 param set /param_publisher message_prefix "ROS2"` 후 메시지가 `[ROS2] count: N`으로 즉시 변경
- [ ] `ros2 param set /param_publisher publish_rate 5.0` 후 메시지 출력 속도가 빨라짐
- [ ] `ros2 param list`에서 두 파라미터 모두 확인
