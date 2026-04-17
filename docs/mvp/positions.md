# MVP Positions — Curator Notes

MVP의 10개 포지션은 **"runtime Stockfish 평가가 실제로 의미를 갖는지"** 를 확인하기 위한 수동 큐레이팅 세트다. V 는 저장하지 않는다 — 매 세션 엔진이 계산한다.

## 분포 의도

| 카테고리 | 예상 V | 라운드 # | 의도 |
|---|---|---|---|
| 오프닝·쿼이엇 | 작음 (~0–5 pp) | 1, 2, 3, 8, 10 | 대부분의 MVP 라운드가 여기 속함. "subtle judgment" 감각 테스트용. |
| 중간 변동 | 중간 (~5–20 pp) | 4, 9 | 직관적으로 읽히지만 확신 어려움. |
| 큰 변동 | 큼 (20+ pp) | 5, 7 | 명백한 블런더 / 명백한 승리 수. payout 공식의 "쉬운 문제 = 짠 리워드" 감각 검증. |
| 평형 | ~0 pp | 6 | 엔드게임 opposition. payout이 0 근처에서 어떻게 동작하는지 관찰. |

## 목록 상세

1. **Opening e4** — `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`, `e2e4`. 메인 라인. 아주 작은 양의 V.
2. **Opening a3** — 같은 FEN, `a2a3`. 수동적 수. V ≈ 0 또는 미세하게 음.
3. **Sicilian reply** — `...c7c5`. 검정이 반격. 방향 판단 애매.
4. **Scholar Qh5** — `r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 2 3`, `Qh5`. 초보에겐 "승리 같지만" 엔진 관점에선 dubious.
5. **Fool's mate** — `rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq g3 0 2`, `Qh4#`. 체크메이트 → 큰 V. 찾기 쉬움 ("쉬운 문제" 예시).
6. **KK endgame opposition** — `8/8/8/3k4/8/3K4/8/8 w - - 0 1`, `Kc3`. 무승부 엔드게임의 opposition 수. V ≈ 0.
7. **Pawn promotion** — `2K5/1P6/8/8/8/8/r7/4k3 w - - 0 1`, `b8=Q`. 프로모션 → 큰 V 위쪽 방향.
8. **Exposed black queen** — `rnb1kbnr/ppp1pppp/8/3q4/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`, `e3`. 조용한 수. 작은 V.
9. **Bxf7+ sac** — `r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4`, `Bxf7+`. 의심스러운 희생. 초보에겐 "공격처럼 보이는" 반례 (design doc §난이도 가정 §반례 — sacrifice 케이스).
10. **Prophylactic h3** — `rnbqkb1r/ppp1pppp/5n2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 4`, `h3`. 아주 subtle. design doc의 "quiet move" 예시.

## 수정 시 체크

- 모든 FEN의 기보 legality는 `chess.Board(fen); chess.Move.from_uci(move) in board.legal_moves` 로 검증했다.
- 새 포지션 추가 시 위 테이블의 **분포**를 유지할 것. 블런더에 치우치면 payout의 "subtle 감각 훈련" 의도가 무너진다 (design doc §Design goals).

## 향후 확장

MVP 이후: PGN/puzzle DB 연동으로 이 하드코딩 리스트를 대체. `docs/design/research-tasks.md` **R1** (V 분포 실측) 이 이 세트를 교체할 데이터 기반 분포를 제공한다.
