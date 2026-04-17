"""Engine smoke tests. Skipped if Stockfish is not available."""

import pytest
import chess

from gamblers_gambit.engine import Engine, cp_to_wp, find_stockfish


def _stockfish_available() -> bool:
    try:
        find_stockfish()
    except FileNotFoundError:
        return False
    return True


requires_stockfish = pytest.mark.skipif(
    not _stockfish_available(), reason="Stockfish binary not available"
)


def test_cp_to_wp_zero_is_fifty() -> None:
    assert cp_to_wp(0) == pytest.approx(50.0)


def test_cp_to_wp_monotonic() -> None:
    assert cp_to_wp(-500) < cp_to_wp(-100) < cp_to_wp(0) < cp_to_wp(100) < cp_to_wp(500)


def test_cp_to_wp_bounded() -> None:
    assert 0.0 <= cp_to_wp(-10000) < 1.0
    assert 99.0 < cp_to_wp(10000) <= 100.0


@requires_stockfish
def test_engine_evaluates_starting_position() -> None:
    with Engine(depth=6) as e:
        board = chess.Board()
        ev = e.evaluate_move(board, chess.Move.from_uci("e2e4"))
    assert 0.0 <= ev.wp_before <= 100.0
    assert 0.0 <= ev.wp_after <= 100.0
    assert 0.0 <= ev.v <= 100.0


@requires_stockfish
def test_engine_detects_blunder() -> None:
    """Queen-hanging blunder from the starting position should yield large V."""
    with Engine(depth=8) as e:
        board = chess.Board(
            "rnbqkbnr/pppp1ppp/8/4p3/8/5N2/PPPPPPPP/RNBQKB1R w KQkq - 0 2"
        )
        legal = [m for m in board.legal_moves]
        assert chess.Move.from_uci("f3e5") in legal
        ev = e.evaluate_move(board, chess.Move.from_uci("f3g1"))
    assert ev.v >= 1.0
