"""CLI session loop for the MVP.

Single phase, binary Up/Down, fixed bet size. Session ends when bankroll
hits zero or all rounds are played.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field

import chess

from gamblers_gambit.engine import Engine, Evaluation
from gamblers_gambit.payout import loss_mult, win_payout
from gamblers_gambit.positions import MVP_ROUNDS, Round

STARTING_BANKROLL = 100.0
BET_SIZE = 10.0


@dataclass
class RoundResult:
    round_index: int
    guess: str
    evaluation: Evaluation
    correct: bool
    delta: float
    bankroll_after: float


@dataclass
class Session:
    bankroll: float = STARTING_BANKROLL
    history: list[RoundResult] = field(default_factory=list)

    @property
    def bankrupt(self) -> bool:
        return self.bankroll <= 0


def _prompt_guess(input_fn=input) -> str | None:
    while True:
        raw = input_fn("Up/Down [u/d] (q to quit): ").strip().lower()
        if raw in ("u", "up"):
            return "U"
        if raw in ("d", "down"):
            return "D"
        if raw in ("q", "quit", "exit"):
            return None
        print("  '?' — please enter u or d (or q to quit).")


_WHITE_SYMS = {
    chess.PAWN: "♟", chess.ROOK: "♜", chess.KNIGHT: "♞",
    chess.BISHOP: "♝", chess.QUEEN: "♛", chess.KING: "♚",
}
_BLACK_SYMS = {
    chess.PAWN: "♙", chess.ROOK: "♖", chess.KNIGHT: "♘",
    chess.BISHOP: "♗", chess.QUEEN: "♕", chess.KING: "♔",
}
_EMPTY_SYM = "⭘"
_HL = "\033[43;30m"   # black text on yellow background
_RST = "\033[0m"


def _board_with_highlights(board: chess.Board, highlight: set[int], flip: bool = False) -> str:
    ranks = range(8) if flip else range(7, -1, -1)
    files = range(7, -1, -1) if flip else range(8)
    file_label = "   h g f e d c b a" if flip else "   a b c d e f g h"
    lines = ["  -----------------"]
    for rank in ranks:
        row = f"{rank + 1} |"
        for file in files:
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)
            if piece:
                sym = (_WHITE_SYMS if piece.color == chess.WHITE else _BLACK_SYMS)[piece.piece_type]
            else:
                sym = _EMPTY_SYM
            row += (f"{_HL}{sym}{_RST}" if sq in highlight else sym) + "|"
        lines.append(row)
        lines.append("  -----------------")
    lines.append(file_label)
    return "\n".join(lines)


def _render_board(fen: str, move_uci: str) -> str:
    board = chess.Board(fen)
    move = chess.Move.from_uci(move_uci)
    side = "White" if board.turn == chess.WHITE else "Black"
    san = board.san(move)
    piece = board.piece_at(move.from_square)
    piece_name = chess.piece_name(piece.piece_type).capitalize() if piece else "?"
    from_sq = chess.square_name(move.from_square)
    to_sq = chess.square_name(move.to_square)

    board_after = board.copy(stack=False)
    board_after.push(move)
    flip = board.turn == chess.BLACK
    board_str = _board_with_highlights(board_after, {move.from_square, move.to_square}, flip=flip)

    return (
        f"{board_str}\n"
        f"  Side to move : {side}\n"
        f"  Moving piece : {piece_name} ({from_sq} → {to_sq})   [{san}]"
    )


def _settle(
    guess: str, evaluation: Evaluation, bet: float
) -> tuple[bool, float]:
    if evaluation.wp_after > evaluation.wp_before:
        truth = "U"
    elif evaluation.wp_after < evaluation.wp_before:
        truth = "D"
    else:
        truth = "FLAT"

    if truth == "FLAT":
        return guess == "U", 0.0

    correct = guess == truth
    if correct:
        return True, bet * win_payout(evaluation.v)
    return False, -bet * loss_mult(evaluation.v)


def play_round(
    engine: Engine,
    rnd: Round,
    round_index: int,
    session: Session,
    bet: float = BET_SIZE,
    input_fn=input,
) -> RoundResult | None:
    print(f"\n─── Round {round_index + 1} / {len(MVP_ROUNDS)} ───")
    print(f"Bankroll: {session.bankroll:.2f}    Bet: {bet:.2f}")
    print(_render_board(rnd.fen, rnd.move_uci))

    guess = _prompt_guess(input_fn)
    if guess is None:
        return None

    board = chess.Board(rnd.fen)
    move = chess.Move.from_uci(rnd.move_uci)
    ev = engine.evaluate_move(board, move)
    correct, delta = _settle(guess, ev, bet)
    session.bankroll += delta

    verdict = "CORRECT" if correct else "WRONG"
    print(
        f"\n  wp_before = {ev.wp_before:5.1f}%   "
        f"wp_after = {ev.wp_after:5.1f}%   V = {ev.v:5.2f} pp"
    )
    print(f"  {verdict}  →  {delta:+.2f}    bankroll = {session.bankroll:.2f}")

    return RoundResult(
        round_index=round_index,
        guess=guess,
        evaluation=ev,
        correct=correct,
        delta=delta,
        bankroll_after=session.bankroll,
    )


def run(input_fn=input) -> Session:
    print("=== Gambler's Gambit (MVP) ===")
    print("Guess whether the candidate move raises (u) or lowers (d) the")
    print("side-to-move's winrate. Fixed bet = 10. Starting bankroll = 100.\n")

    session = Session()
    with Engine() as engine:
        for i, rnd in enumerate(MVP_ROUNDS):
            if session.bankrupt:
                print("\n  Bankroll ≤ 0 — session over.")
                break
            result = play_round(engine, rnd, i, session, input_fn=input_fn)
            if result is None:
                print("\n  Quit requested.")
                break
            session.history.append(result)

    print("\n─── Session summary ───")
    rounds_played = len(session.history)
    correct_count = sum(1 for r in session.history if r.correct)
    print(f"Rounds played: {rounds_played}")
    print(f"Correct:       {correct_count}")
    print(f"Final bankroll: {session.bankroll:.2f}")
    if session.bankrupt:
        print("Result: BANKRUPT")
    elif rounds_played == len(MVP_ROUNDS):
        print("Result: SURVIVED")
    else:
        print("Result: QUIT")
    return session


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
