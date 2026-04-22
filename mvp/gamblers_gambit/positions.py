"""Hardcoded MVP position set.

See docs/mvp/positions.md for curator notes. V is NOT pre-computed here —
it's calculated at runtime by the Stockfish wrapper so the engine is
actually exercised.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Round:
    fen: str
    move_uci: str
    note: str = ""


MVP_ROUNDS: tuple[Round, ...] = (
    Round(
        fen="6k1/ppp2ppp/8/8/8/8/PPP2PPP/4R1K1 w - - 0 1",
        move_uci="e1e8",
        note="Back-rank checkmate — Re8#. Black king trapped behind own pawns. Big V.",
    ),
    Round(
        fen="r4rk1/pp4pp/2p5/5p2/8/2NP4/PP3PPP/2R1R1K1 w - - 0 1",
        move_uci="e1e7",
        note="Rook infiltrates 7th rank, attacking Black pawns. Medium-large V.",
    ),
    Round(
        fen="r3k2r/pp3ppp/8/3Np3/8/8/PPP2PPP/R3K2R w KQkq - 0 1",
        move_uci="d5c7",
        note="Nc7+ forks Black king (e8) and rook (a8) simultaneously. Large V.",
    ),
    Round(
        fen="r3k2r/ppp2ppp/8/3R4/8/8/PPP2PPP/4K2R w Kkq - 0 1",
        move_uci="d5d8",
        note="Rd8+ — rook invades back rank with check, forcing king from castled safety. Large V.",
    ),
    Round(
        fen="2K5/1P6/8/8/8/8/r7/4k3 w - - 0 1",
        move_uci="b7b8q",
        note="Pawn promotion in R+P vs R endgame. Large V winning-ward.",
    ),
    Round(
        fen="r1bqk2r/ppp2ppp/2np1n2/4p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R w KQkq - 0 8",
        move_uci="d1a4",
        note="Qa4 pins Nc6 against uncastled king. Medium V.",
    ),
    Round(
        fen="r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        move_uci="c4f7",
        note="Bxf7+ speculative sac. Dubious sacrifice — direction hard to read.",
    ),
)
