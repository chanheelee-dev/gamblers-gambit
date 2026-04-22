"""Stockfish UCI wrapper + cp→wp conversion.

Engine lookup order:
  1. `STOCKFISH_PATH` env var (explicit override)
  2. `shutil.which("stockfish")` — PATH
  3. `/usr/games/stockfish` (Debian/Ubuntu default — `/usr/games` is often
     missing from PATH for non-login shells).
"""

from __future__ import annotations

import math
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

import chess
import chess.engine

DEFAULT_DEPTH = 12

_REPO_ROOT = Path(__file__).parent.parent.parent
_SYSTEM_FALLBACKS = ("/usr/games/stockfish", "/usr/local/bin/stockfish")


def find_stockfish() -> str:
    override = os.environ.get("STOCKFISH_PATH")
    if override:
        return override
    found = shutil.which("stockfish")
    if found:
        return found
    # repo-local: scan <repo>/stockfish/ for any executable
    repo_stockfish_dir = _REPO_ROOT / "stockfish"
    if repo_stockfish_dir.is_dir():
        for candidate in sorted(repo_stockfish_dir.iterdir()):
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate)
    for candidate in _SYSTEM_FALLBACKS:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    raise FileNotFoundError(
        "Stockfish binary not found. Install it (`apt install stockfish` or "
        "`brew install stockfish`) or set STOCKFISH_PATH."
    )


def cp_to_wp(cp: int) -> float:
    """Lichess cp→winrate conversion (docs/design/game-concept.md line 52).

    Returns winrate as a percent in [0, 100] from the perspective of the
    side whose score was measured.
    """
    return 50.0 + 50.0 * (2.0 / (1.0 + math.exp(-0.00368208 * cp)) - 1.0)


@dataclass(frozen=True)
class Evaluation:
    wp_before: float
    wp_after: float
    v: float


class Engine:
    def __init__(self, path: str | None = None, depth: int = DEFAULT_DEPTH) -> None:
        self._path = path or find_stockfish()
        self._depth = depth
        self._engine = chess.engine.SimpleEngine.popen_uci(self._path)

    def __enter__(self) -> "Engine":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        self._engine.quit()

    def _score_pov(self, board: chess.Board, pov: chess.Color) -> int:
        info = self._engine.analyse(
            board, chess.engine.Limit(depth=self._depth)
        )
        score = info["score"].pov(pov)
        return score.score(mate_score=10000)

    def evaluate_move(self, board: chess.Board, move: chess.Move) -> Evaluation:
        """Compute V = |wp_after − wp_before|, both from the mover's POV.

        Convention: wp is always measured from the POV of the side that
        just moved (or is about to move, for wp_before). This keeps
        "Up/Down" intuitive for the player whose side is on move.
        """
        if move not in board.legal_moves:
            raise ValueError(f"Illegal move {move.uci()} in position {board.fen()}")

        mover = board.turn
        cp_before = self._score_pov(board, mover)
        wp_before = cp_to_wp(cp_before)

        after = board.copy(stack=False)
        after.push(move)
        cp_after = self._score_pov(after, mover)
        wp_after = cp_to_wp(cp_after)

        return Evaluation(
            wp_before=wp_before,
            wp_after=wp_after,
            v=abs(wp_after - wp_before),
        )
