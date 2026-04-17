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
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        move_uci="e2e4",
        note="Opening: main-line e4. Expect small positive V for white.",
    ),
    Round(
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        move_uci="a2a3",
        note="Opening: passive a3. Expect small V, mild direction.",
    ),
    Round(
        fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
        move_uci="c7c5",
        note="Sicilian reply. Mid-to-small V, direction subtle.",
    ),
    Round(
        fen="r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 2 3",
        move_uci="d1h5",
        note="Scholar's setup: Qh5. Sharp but not obviously winning to a novice.",
    ),
    Round(
        fen="rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq g3 0 2",
        move_uci="d8h4",
        note="Fool's mate: Qh4#. Obvious once spotted — big V, easy target.",
    ),
    Round(
        fen="8/8/8/3k4/8/3K4/8/8 w - - 0 1",
        move_uci="d3c3",
        note="K-only endgame, opposition move. Near-zero V, pure noise.",
    ),
    Round(
        fen="2K5/1P6/8/8/8/8/r7/4k3 w - - 0 1",
        move_uci="b7b8q",
        note="Pawn promotion in R+P vs R endgame. Large V winning-ward.",
    ),
    Round(
        fen="rnb1kbnr/ppp1pppp/8/3q4/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        move_uci="e2e3",
        note="Exposed Q on d5: any dev move is fine. Quiet, small V.",
    ),
    Round(
        fen="r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        move_uci="c4f7",
        note="Bxf7+ speculative sac. Dubious sacrifice — direction hard to read.",
    ),
    Round(
        fen="rnbqkb1r/ppp1pppp/5n2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 4",
        move_uci="h2h3",
        note="Prophylactic h3. Very small V — design target for 'subtle' rounds.",
    ),
)
