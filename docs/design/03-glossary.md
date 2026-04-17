# 03. Glossary

이 프로젝트에서 반복적으로 쓰는 기술 용어를 한 곳에 모은다. 본 문서는 정책상 **한국어 본문 + 영어 기술 용어** 를 쓰기 때문에, 다른 문서에서는 용어의 재정의 없이 이 파일을 참조하는 것을 원칙으로 한다.

> **작업 규칙**: 새 용어가 설계·리서치 문서에 등장하면, 해당 커밋에서 이 파일도 함께 업데이트한다.

형식: **용어** / 정의 / 이 프로젝트에서의 의미 / 참고.

---

## 평가와 단위

Centipawn (cp) 의 일반 정의는 [Chess Primer](../background/chess-primer.md#centipawn-cp) 참조. 본 프로젝트에서는 내부 계산용이며 플레이어에게 직접 노출하지 않는다.

### Winrate / Win Probability (wp, %)

현재 포지션에서 한쪽(문맥에 따라 백 또는 "수를 둔 쪽")의 기대 승률. 0~100 %.

- **이 프로젝트**: 표면에 노출되는 평가 단위. cp → wp 변환식은 `01-game-concept.md` §2 참조. 확정 전 후보 비교는 R2.

### Percent Point (pp)

두 wp 값의 차이를 표현하는 단위. "30 % → 45 %" 는 15 **pp** 상승. ("% 포인트") 와 "% 가 상승" 은 다른 개념 — 혼동 주의.

### 변동폭 (V)

어떤 수(move) 전후의 wp 변화 절댓값.

```
V = |wp_after − wp_before|    (단위: pp)
```

- **이 프로젝트**: 본 게임의 난이도 proxy. 작업가설상 V 가 클수록 플레이어 정답률 p 가 크다.

---

## 배당과 베팅

### Payout / Win payout

베팅을 맞췄을 때 받는 **순이익 배수** (베팅액 1 기준). 즉 베팅 10 유닛에서 `win_payout = 0.5` 면 맞췄을 때 +5 유닛을 받는다 (원금 10 유닛은 그대로 반환).

### Loss multiplier

베팅을 틀렸을 때 잃는 양의 배수 (베팅액 1 기준). `loss_mult = 1.5` 면 10 유닛 베팅 시 실제 손실은 15 유닛.

### Skill tax (α, β)

[공정 배당](../background/gambling-primer.md#fair-odds--base-odds) 위에 얹는 난이도 비대칭 파라미터.

- **α ∈ [0, 1]**: 쉬운 문제(큰 V)의 win_payout 축소율.
- **β ∈ [0, 1]**: 쉬운 문제의 loss_mult 증폭율.
- α = β = 0 → 공정 배당. 값이 클수록 "쉬운 건 짜게, 실수는 혹독히".
- 이를 통해 [하우스 엣지](../background/gambling-primer.md#house-edge) 를 V 축에서 비균일하게 발생시키는 것이 설계 의도.

### Betting mode

플레이어가 한 라운드에서 **무엇에 대해 베팅하는가** 의 형식. 후보: up/down (승률 올림/내림), multi-choice (N개 후보 중 best), threshold (V ≥ X?), numeric range (V 값 예측). Mode 가 바뀌면 정답률 모델 `p(V)` 과 배당 공식을 **별도로 설계** 해야 한다 — baseline, 난이도 축, skill tax 크기가 전부 달라짐.

### Baseline 정답률

Betting mode 별 "찍기" 기대 정답률.

- binary up/down → 0.5
- N-choice → 1/N
- numeric range → 구간 넓이에 의존

p(V) 모델에서 V=0 일 때의 상수항으로 쓰인다 (R5 참조). **베팅 페이즈** (아래) 에 따라 값이 교체된다.

---

## 세션 구조

### Session arc (세션 아크)

한 게임 세션이 시작부터 뱅크롤 소진 / 종료까지 그리는 구조. 본 게임은 **뒤로 갈수록 버티기 힘든** 곡선을 의도 (§1.1, §5). 세 가지 메커니즘이 독립적으로 돌면서 서로 강화:

- **Ramping house edge** (아래 / §5.1)
- **Betting mode escalation** (아래 / §5.2)
- **Serendipity round** (아래 / §5.3)
- **Time pressure ramp** (아래 / §5.4)

### Ramping house edge

α, β 가 라운드 번호 `t` 의 증가 함수로 확장되는 메커니즘. `α(t) = min(α_max, α_0 + k_α · t)` 류. 초반 거의 공정 → 후반 치명타. §5.1.

### Betting phase (베팅 페이즈)

세션 아크 안에서 동일한 betting mode 가 유지되는 구간. 각 페이즈는 고유한 [baseline 정답률](#baseline-정답률) 을 가진다 (예: Phase 1 binary up/down → 0.5, Phase 2 multi-choice → 1/N). §5.2.

### Time pressure ramp

라운드당 판단 시간이 세션이 진행될수록 줄어드는 메커니즘. `time_limit(t) = max(T_min, T_0 − k_T · t)`. 초기 15~20초 → 최소 5초. 경제적 압박(ramping edge) 과 별개인 **인지적 압박** 축. §5.4.

### Serendipity round

매 라운드 확률적으로 발동하는 bonus 라운드. 플레이어 상태(뱅크롤, 승패)와 **무관** — 서바이벌에서의 "우연한 행운". 발동 후 `cooldown` 라운드 동안 잠기고, 갈수록 발동 확률이 올라감. "그럼 뭘 했어야 했지?" 형태, EV 가 플레이어 쪽으로 기울어 있는 **설계적 숨구멍**. §5.3.

---

## 난이도 신호

체스 수의 유형 (blunder, sacrifice, only move, quiet move, PV 등) 은 난이도를 추정하는 보조 신호로 쓰인다. 각 유형의 일반 정의는 [Chess Primer](../background/chess-primer.md#수의-유형) 참조.

### Tactical obviousness

"사람 눈에 그 수가 얼마나 뻔히 보이는가" 를 가리키는 비공식 용어. 본 프로젝트에서는 p(V, features) 확장의 축으로 등장. 이 용어 자체는 일반 체스 용어가 아닌 **프로젝트 고유 개념**.

---

## 모델·수식

### p(V)

변동폭 V 에서의 기대 정답률. 초안:

```
p(V) = baseline + (1 − baseline) * (1 − exp(−λ * V))
```

- `baseline` 은 betting mode 에 따라 0.5 또는 1/N (R5).
- `λ` 는 "V 한 단위당 난이도 감소 속도". 실측값은 R3.

---

## 관련 문서

- `01-game-concept.md` — 용어가 실제로 쓰이는 맥락.
- `02-research-tasks.md` — 용어 뒤의 값/식을 확정하기 위한 리서치 과제.
- [`../background/gambling-primer.md`](../background/gambling-primer.md) — EV, 하우스 엣지, 공정 배당 등 **일반 도박/확률 개념**.
- [`../background/chess-primer.md`](../background/chess-primer.md) — Elo, SAN/PGN/FEN, 수의 유형, 엔진 용어 등 **일반 체스 개념**.
