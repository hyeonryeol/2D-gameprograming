# 2D Game Programming - LEC00 mission

수업 첫 미션(개발 환경 구성 + 샘플 프로그램 실행) 결과물입니다.

## 구성 완료 항목

| 항목 | 상태 |
| --- | --- |
| VSCode | 1.135.0 (winget, 사용자 범위 설치) |
| Python | 3.14.7 |
| pico2d | 1.5.1 (PySDL2 / PySDL2-DLL 자동 설치) |
| AI 에이전트 | Claude Code VSCode 확장 (`anthropic.claude-code`) |
| 샘플 프로그램 | `main.py` |

## 실행 방법

```
python main.py
```

VSCode 안에서는 `F5`(Run game) 또는 `Ctrl+Shift+B`(Run game task)로 실행합니다.

조작: 좌/우 방향키 이동, 스페이스 점프, ESC 종료.

키 입력 없이 환경만 확인하려면:

```
python tools/smoke_test.py
```

## 새 PC에서 다시 세팅할 때

```
pip install -r requirements.txt
python tools/make_assets.py
python main.py
```

리소스 이미지는 표준 라이브러리만으로 직접 생성하므로 별도 다운로드가 필요 없습니다.
