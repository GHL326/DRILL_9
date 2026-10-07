# DRILL_9 — 상하좌우 이동 및 방향 바꾸기

제출 저장소: https://github.com/GHL326/DRILL_9.git

## 실행

Python과 pico2d가 설치된 환경에서 다음 명령으로 실행합니다.

```powershell
python -m pip install pico2d
python move_character.py
```

`move_character.py`는 다른 프로젝트 파이썬 파일을 가져오지 않는 독립 실행 파일입니다. 같은 폴더의 `animation_sheet.png`와 `TUK_GROUND.png`가 필요합니다.

## 조작과 제출 기능

- 방향키 ↑ ↓ ← →: 상하좌우 이동. 여러 키를 누르면 마지막으로 누른 한 방향으로 이동합니다.
- 위·아래 이동: 마지막으로 바라본 좌우 방향의 RUN 애니메이션을 유지합니다.
- 키를 놓거나 화면 경계에 막히면 해당 방향의 IDLE 애니메이션을 재생합니다.
- 100×100 캐릭터 프레임 전체가 화면 안에 있도록 네 경계를 제한합니다.
- 화면 크기는 배경 비율과 같은 1000×800입니다.
- ESC 또는 창 닫기: 종료.

## 파일

| 파일 | 용도 |
| --- | --- |
| `move_character.py` | 모든 제출 기능을 포함한 통합 실행 파일 |
| `move_character_with_key.py` | 같은 제출 기능을 갖춘 독립 키보드 예제 |
| `move_character_with_mouse.py` | 마우스 이동 예제. 공통 캐릭터 처리는 통합 파일 사용 |
| `character_runs_esc.py` | 오른쪽으로 자동 이동 후 경계에서 IDLE. ESC 종료 예제 |
| `IMPLEMENTATION_PLAN.md` | 확정 요구사항과 구현 계획 |
| `tests/test_character.py` | 이동, 방향, 경계, 입력 및 애니메이션 검증 |

## 검증

```powershell
python -m unittest discover -s tests -v
```
