# Design Docs — gamblers-gambit

이 폴더는 `gamblers-gambit` 의 **설계·리서치 문서** 를 모은다. 당분간 레포의 커밋은 대부분 여기에 쌓일 예정이다.

## 읽는 순서

1. **[`01-game-concept.md`](./01-game-concept.md)** — 게임 컨셉, metric 선택, payout 공식 초안, 미결정 항목(Open Questions). **여기서 시작.**
2. **[`02-research-tasks.md`](./02-research-tasks.md)** — 초안의 가정을 검증하기 위한 리서치 과제 목록 (R1~R5). 앞으로의 커밋은 이 목록에서 하나씩 소화한다.
3. **[`03-glossary.md`](./03-glossary.md)** — cp, wp, pp, V, payout, α/β 등 반복되는 용어 정의. 다른 문서에서 용어가 등장하면 이 파일을 참조한다.

## 작업 규칙

- 설계 변경은 **관련 섹션의 in-place 업데이트** 를 원칙으로 한다 (히스토리는 git 이 기억한다).
- **새 용어가 등장하면 그 커밋에서 `03-glossary.md` 도 함께 업데이트** 한다.
- 리서치 과제(R*) 의 결과물은 `docs/research/` 하위에 별도 파일로 두고, 완료 시 `02-research-tasks.md` 에 산출물 링크를 건다.
- 코드/프로토타입은 설계가 충분히 안정화된 이후 별도 커밋에서 시작한다.

## 앞으로 추가될 예정 (예상)

- `04-betting-format.md` — Open Question #1 (베팅 대상의 형태) 에 대한 결정 문서.
- `docs/research/r1-v-distribution.md` 등 R1~R5 산출물.
- 이후 설계가 안정화되면 `05-architecture.md` 류 실구현 문서.

신규 문서가 들어오면 이 README 의 "읽는 순서" 도 함께 갱신한다.
