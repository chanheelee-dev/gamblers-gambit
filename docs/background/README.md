# Background Docs

도박·확률·체스 일반 개념 등, **디자인 결정 자체는 아니지만** 디자인 문서(`docs/design/`) 이해에 필요한 공통 배경 지식.

## 파일

- **[`gambling-primer.md`](./gambling-primer.md)** — EV, 하우스 엣지, 공정 배당 등 도박 용어·개념.
- **[`chess-primer.md`](./chess-primer.md)** — Elo, SAN/PGN/FEN, 수의 유형(blunder, sacrifice, quiet move 등), 엔진 용어(Stockfish, PV, depth).

## `docs/design/` 와의 관계

| 위치 | 내용 | 예 |
|---|---|---|
| `docs/design/` | 이 게임의 **결정·가정·수식** | payout 공식, V 의 정의, skill tax α/β |
| `docs/design/03-glossary.md` | 이 게임의 **프로젝트 고유** 용어 | cp, wp, pp, V, win_payout, skill tax |
| `docs/background/` (여기) | 도박·확률·체스 **일반** 개념 (디자인에 종속되지 않음) | EV, 하우스 엣지, Elo, SAN, blunder |

## 편집 규칙

- 설명이 "이 게임이 아니었어도 존재하는 개념" 이면 여기로.
- "이 게임에서 이렇게 정의했다" 면 `03-glossary.md` 로.
- 두 성격이 겹치는 용어는 여기서 일반 정의 → 프로젝트 용례 블록으로 이어 쓰거나, glossary 엔 짧게 언급 + 여기로 링크.
