# MVP — Minimum Playable Slice

디자인 문서의 풀 스펙이 아직 확정되지 않은 단계에서, **엔드투엔드로 한 세션을 플레이해 볼 수 있는 가장 얇은 슬라이스**다.

## 범위

포함:
- CLI 터미널 인터페이스.
- python-chess + Stockfish UCI 연동 (런타임 V 계산).
- 바이너리 Up/Down 베팅 (design 문서 Phase 1만).
- 상수 α=0.5, β=1.0, λ=0.06 으로 payout 공식 적용 (`docs/design/game-concept.md` §Payout).
- 하드코딩된 10 라운드 (`mvp/gamblers_gambit/positions.py`, 큐레이팅 노트: [`positions.md`](./positions.md)).

제외 (design 장기 과제):
- 페이즈 전환 (multi-choice, numeric range).
- Serendipity round.
- Time pressure ramp.
- α(t), β(t) 라운드 의존 ramping.
- PGN/puzzle DB 연동.
- R1~R5 실측 튜닝.

## 실행법

```bash
apt install stockfish          # Debian/Ubuntu. brew install stockfish on macOS.
uv sync
uv run python -m gamblers_gambit
```

Stockfish 바이너리 위치를 명시적으로 지정하려면:

```bash
STOCKFISH_PATH=/custom/path/stockfish uv run python -m gamblers_gambit
```

(Debian 패키지는 `/usr/games/stockfish` 에 설치되며, `/usr/games` 가 PATH 에 없는 경우를 위해 `find_stockfish()` 가 자동 폴백한다.)

## 테스트

```bash
uv run pytest mvp/tests/
```

- `test_payout.py` — design 문서 §Payout 공식을 pin. `p(V)`, `win_payout`, `loss_mult` 의 수치 일관성과 단조성, 하우스 엣지 (EV<0) 를 검증.
- `test_engine.py` — Stockfish 가 설치되어 있을 때만 실행. cp→wp 변환의 경계/단조성, 그리고 실제 포지션에서 V 가 합리적 범위인지.

## 파일 구조

```
mvp/
├── gamblers_gambit/
│   ├── __init__.py
│   ├── __main__.py          # CLI 엔트리
│   ├── engine.py            # Stockfish UCI 래퍼 + cp→wp
│   ├── game.py              # 세션/라운드 루프
│   ├── payout.py            # 순수 payout 공식
│   └── positions.py         # 하드코딩 10 라운드
└── tests/
    ├── test_engine.py
    └── test_payout.py

docs/mvp/
├── README.md                # 이 파일
└── positions.md             # 10 라운드 큐레이팅 노트
```

## 다음 커밋에서 붙이기 좋은 것

MVP 바깥의 확장 — 이 구조가 그대로 발판이 된다:

1. **PGN/puzzle 로더** → `positions.py` 를 데이터 파일 기반으로 교체.
2. **α(t), β(t) ramping** → `payout.py` 함수 시그니처에 `t` 파라미터 추가.
3. **Time pressure** → `game.py` 의 `_prompt_guess` 에 타임아웃.
4. **Phase 2 (multi-choice)** → `game.py` 의 라운드 루프 분기.
5. **Serendipity round** → 세션 루프에 확률 트리거.
6. **R1~R5 실측** → 각 문서 산출물은 `docs/design/research-tasks.md` 참조.

관련 설계: [`docs/design/game-concept.md`](../design/game-concept.md) §Session arc, §Open Questions.
