
## 🐢 Project 2 — 거북이 대형 변경 서비스


> 프로젝트 개요
> 서비스로 대형 이름(`circle` / `triangle` / `grid`)과 마릿수를 요청하면 해당 모양으로 거북이들을 배치하는 시스템을 구현한다.
> 멀티 스폰 코드의 `calc_position()`을 대형별로 확장하는 프로젝트로, 수식 변경만으로 다양한 형태를 만들 수 있다.

---

## 🎯 목표

- [ ] 커스텀 서비스 정의 — 대형 이름 + 마릿수를 Request로 받기
- [ ] `circle`, `triangle`, `grid` 대형 좌표 계산 함수 구현
- [ ] 서비스 서버에서 대형에 따라 다른 함수 호출
- [ ] Jupyter에서 각 대형 시각화 검증 후 ROS2 이식

---

## 📐 시스템 설계

**서비스 정의 — FormationSpawn.srv**

```text
# srv/FormationSpawn.srv
string formation   # "circle" / "triangle" / "grid"
int64 num          # 마릿수
float64 scale      # 전체 크기 (반지름 or 간격)
---
float64[] x
float64[] y
float64[] theta
string result      # "success" / "unknown formation"
```

**데이터 흐름**

```
ros2 service call /formation_spawn ...
        │
        ▼
[formation_server_node]
        │
  formation 이름 분기
  ├── "circle"   → calc_circle()
  ├── "triangle" → calc_triangle()
  └── "grid"     → calc_grid()
        │
        ▼
  /spawn 서비스 반복 호출 (turtlesim)
```

---

## 🏗️ 구현 단계

**▸ Step 1 — 서비스 정의 파일 추가**

`my_first_package_msgs/srv/FormationSpawn.srv` 생성 후 `CMakeLists.txt`에 등록.

```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CmdPose.msg"
  "srv/MultiSpawn.srv"
  "srv/FormationSpawn.srv"   # 추가
)
```

---

**▸ Step 2 — 대형별 좌표 계산 함수 (Jupyter 검증 먼저)**


**▸ Step 3 — 서비스 서버 노드**


**▸ Step 4 — 실행**

---

## 🔧 개선 아이디어

- **대형 추가**: `line`(직선), `star`(별), `spiral`(나선) 등 수식만 추가하면 확장 가능
- **TeleportAbsolute 활용**: Spawn 대신 기존 거북이를 이동시키는 버전으로 변경
- **대형 전환 서비스**: 이미 배치된 거북이들을 다른 대형으로 재배치

---

## ✅ 완성 기준

- `circle`, `triangle`, `grid` 세 가지 대형이 모두 정상 동작한다
- 알 수 없는 대형 이름 요청 시 `"unknown formation"`을 응답한다
- Jupyter에서 각 대형의 좌표를 시각화로 검증한 결과가 있다
