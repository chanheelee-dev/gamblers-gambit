# 02. Research Tasks

`01-game-concept.md` 초안이 기반한 가정들을 검증하기 위한 리서치 과제 목록. 각 과제는 다음 3 필드로 기술한다:

- **질문**: 이 과제가 답하려는 것.
- **산출물**: 어떤 형태의 결과물을 레포에 남길 것인가 (보통 `docs/research/` 하위 문서 + 필요 시 데이터/노트북).
- **참고 자료**: 시작점으로 삼을 외부 리소스.

과제가 하나 끝날 때마다, 그 결과를 `01-game-concept.md` 의 관련 섹션에 반영한다. 새로운 용어가 생기면 `03-glossary.md` 에도 동시에 추가한다.

---

## R1. V 분포 관측

- **질문**: 실제 체스 게임에서 수당 변동폭 V(pp) 는 어떻게 분포하는가? 장르(오프닝/미들게임/엔드게임, 속기/장기)에 따라 다른가?
- **산출물**:
  - `docs/research/r1-v-distribution.md` — 히스토그램 이미지 + 구간별 %.
  - 가능하면 재현용 스크립트 (`scripts/r1_*`) 도 함께.
  - 결과를 바탕으로 `01-game-concept.md` 의 "예시 테이블" 구간을 실제 분포 기반으로 재선정.
- **참고 자료**: Lichess puzzle db, Lichess open database (pgn), Stockfish.

## R2. cp ↔ wp 변환식 검증

- **질문**: 우리가 쓸 cp → wp 변환식을 Lichess / Chess.com / 자체 로지스틱 중 무엇으로 확정할 것인가? 각 식의 차이는 V(pp) 값에 얼마나 영향을 주는가?
- **산출물**:
  - `docs/research/r2-cp-to-wp.md` — 후보 식 3~4개 비교 그래프 + 채택식과 그 근거.
  - 채택식을 `01-game-concept.md` §2 에 최종 확정식으로 반영.
- **참고 자료**: Lichess [accuracy blog post](https://lichess.org/page/accuracy), Chess.com CAPS / Elo 기반 공식들 (공개된 범위 내).

## R3. p(V) 실측

- **질문**: 가정 "V 클수록 p 커짐" 이 실제로 성립하는가? 성립한다면 λ 의 실측값은?
- **산출물**:
  - `docs/research/r3-p-of-v.md` — 작은 플레이테스트(50~100 라운드) 결과, 또는 공개 puzzle solve rate 데이터 기반 V vs p 산점도 / 적합 곡선.
  - λ 추정값을 `01-game-concept.md` §4 의 초기값으로 반영.
  - **모델 비교**: 현재 exponential saturation 외에 logistic sigmoid, power law, linear clamp 등 대안 후보를 같은 데이터에 fit 해서 잔차/AIC 비교. 더 나은 모델이 있으면 §4 교체.
- **참고 자료**: Lichess puzzle 난이도 (glicko rating → 추정 solve rate), 자체 플레이테스트 로그.

## R4. Tactical Obviousness 신호

- **질문**: V 외에 정답률을 예측할 수 있는 보조 신호는 무엇인가?
- **산출물**:
  - `docs/research/r4-obviousness-features.md` — 후보 신호 목록 + 각 신호를 엔진에서 얻는 방법 + 기대 효과.
  - 향후 `p(V, features)` 확장의 스펙 초안.
- **참고 자료**: Stockfish UCI `info` 출력(PV, multipv, depth), "only move" / "sacrifice" 판정 휴리스틱 관련 글.

후보 신호 (초안):
- PV 길이 (희생수일수록 긺)
- 2nd best move 와의 cp 차이 (작을수록 어려움)
- Only move 플래그
- 희생 플래그 (수 직후 material 손실 여부)
- 킹 근처 수인지 여부

## R5. Baseline 정답률

- **질문**: 베팅 형태(Open Question #1)가 확정된 후, 해당 형태의 "찍기 baseline" 은 얼마인가? 그 baseline 이 p(V) 모델의 하한을 어떻게 바꾸는가?
- **산출물**:
  - `docs/research/r5-baseline.md` — 형태별 baseline 표 + 최종 채택 형태의 p(V) 재정의.
  - `01-game-concept.md` §4 의 p(V) 식에서 `0.5` 상수를 baseline 으로 교체.
- **참고 자료**: 내부 결정 사항(Open Question #1 의 결론).

---

## 의존 그래프 (대략)

```
R1 ─┬─► 01 §4 예시 테이블 재선정
    └─► R3 의 V 구간 설계

R2 ───► 01 §2 최종 확정식

R3 ───► 01 §4 λ 초기값

R4 ───► 장기: p(V, features) 확장

(Open Q #1 결정) ──► R5 ──► 01 §4 p(V) 의 상수항
```

R1, R2 는 서로 독립이므로 병렬 진행 가능. R5 는 베팅 형태 결정(Open Q #1) 에 의존.
