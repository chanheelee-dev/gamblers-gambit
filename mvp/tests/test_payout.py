"""Pin the Payout formulas from docs/design/game-concept.md §Payout.

λ=0.06, α=0.5, β=1.0. The design doc's example table (lines 126-132) has
minor hand-calc drift at small V (~0.5 units off at V=2); we keep a loose
sanity check against it, and a tight pin against the formula itself.
"""

import math

import pytest

from gamblers_gambit.payout import easiness, loss_mult, p_correct, win_payout


@pytest.mark.parametrize("v", [0, 2, 10, 25, 50, 80, 100, 150])
def test_p_correct_matches_closed_form(v: float) -> None:
    expected = 0.5 + 0.5 * (1.0 - math.exp(-0.06 * v))
    assert p_correct(v) == pytest.approx(expected)


@pytest.mark.parametrize(
    "v, doc_p",
    [(2, 0.553), (10, 0.725), (25, 0.888), (50, 0.975), (80, 0.996)],
)
def test_p_correct_matches_doc_table(v: float, doc_p: float) -> None:
    assert p_correct(v) == pytest.approx(doc_p, abs=0.005)


@pytest.mark.parametrize(
    "v, doc_loss_units",
    [(2, 10.2), (10, 11.0), (25, 12.5), (50, 15.0), (80, 18.0)],
)
def test_loss_mult_matches_doc_table(v: float, doc_loss_units: float) -> None:
    bet = 10.0
    assert bet * loss_mult(v) == pytest.approx(doc_loss_units, abs=0.05)


def test_p_v_zero_is_50_50() -> None:
    assert p_correct(0) == pytest.approx(0.5)


def test_win_payout_at_v_zero_is_fair_odds() -> None:
    assert win_payout(0) == pytest.approx(1.0)


def test_loss_mult_at_v_zero_is_one() -> None:
    assert loss_mult(0) == pytest.approx(1.0)


def test_easiness_clamped_above_100() -> None:
    assert easiness(150) == 1.0
    assert loss_mult(150) == loss_mult(100)


def test_win_payout_shrinks_as_v_grows() -> None:
    assert win_payout(2) > win_payout(10) > win_payout(25) > win_payout(50)


def test_loss_mult_grows_as_v_grows() -> None:
    assert loss_mult(2) < loss_mult(10) < loss_mult(25) < loss_mult(50)


def test_negative_ev_at_all_positive_v() -> None:
    for v in (2, 10, 25, 50, 80):
        p = p_correct(v)
        ev = p * win_payout(v) - (1 - p) * loss_mult(v)
        assert ev < 0, f"EV should be negative at V={v} (house edge), got {ev}"
