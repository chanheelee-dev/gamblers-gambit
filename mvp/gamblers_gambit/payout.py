"""Payout formulas from docs/design/game-concept.md §Payout.

All functions are pure and operate on V (volatility) in percent points (pp).
Defaults: λ=0.06, α=0.5, β=1.0 — design doc initial values.
"""

from __future__ import annotations

import math

DEFAULT_LAMBDA = 0.06
DEFAULT_ALPHA = 0.5
DEFAULT_BETA = 1.0


def p_correct(v: float, lam: float = DEFAULT_LAMBDA) -> float:
    return 0.5 + 0.5 * (1.0 - math.exp(-lam * v))


def easiness(v: float) -> float:
    return min(1.0, v / 100.0)


def win_payout(
    v: float,
    alpha: float = DEFAULT_ALPHA,
    lam: float = DEFAULT_LAMBDA,
) -> float:
    p = p_correct(v, lam)
    base_odds = (1.0 - p) / p
    return base_odds * (1.0 - alpha * easiness(v))


def loss_mult(v: float, beta: float = DEFAULT_BETA) -> float:
    return 1.0 * (1.0 + beta * easiness(v))
