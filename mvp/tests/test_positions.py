import chess
import pytest

from gamblers_gambit.positions import MVP_ROUNDS


@pytest.mark.parametrize("rnd", MVP_ROUNDS, ids=[r.move_uci for r in MVP_ROUNDS])
def test_move_is_legal(rnd):
    board = chess.Board(rnd.fen)
    move = chess.Move.from_uci(rnd.move_uci)
    assert move in board.legal_moves, (
        f"{rnd.move_uci} is illegal in position {rnd.fen}"
    )
