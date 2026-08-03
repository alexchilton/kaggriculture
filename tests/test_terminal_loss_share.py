"""The value-loss share carried by terminal rows -- item 1 of the critic-blindness doc.

**Why this number and not the row count.** `train_jax_rl.py` states in three places that terminal rows
are ~0.14% of a batch, one turn in 719, and infers from that that the critic trains on its own
bootstrap. The inference is about the *gradient*, and row count is not gradient. A terminal row
regresses onto the true outcome while every other row regresses onto a bootstrap, so its squared error
is typically much larger -- if 0.14% of rows carry 2% of the loss they already have 14x leverage, and
upweighting them is a far smaller intervention than the count implies.

The doc's own instruction is to take this measurement *before* adding a third mechanism to the value
loss. The measurement shipped as `terminal_loss_shares`; these are its unit tests, on arrays whose
answers are computable by hand, because in a real rollout no episode ends inside a short window and
every share reads zero -- which is exactly how a broken implementation would also look.
"""

import importlib.util
from pathlib import Path

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

TRAINER = Path(__file__).resolve().parents[1] / "scripts" / "train_jax_rl.py"


def _load_trainer():
    """Import the trainer by path; `scripts/` is not a package."""
    spec = importlib.util.spec_from_file_location("_train_jax_rl", TRAINER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T = _load_trainer()


def _grid(h, r, sq, done, trainable=None):
    """`[h, r]` arrays from nested lists, with everything trainable unless stated."""
    tr = np.ones((h, r), bool) if trainable is None else np.asarray(trainable, bool)
    return dict(sq_err=jnp.asarray(np.asarray(sq, np.float32)),
                done=jnp.asarray(np.asarray(done, bool)),
                trainable=jnp.asarray(tr))


def test_no_terminal_row_gives_a_zero_share_and_not_a_nan():
    """The common case in a short window, and the one that must not divide by zero."""
    got = T.terminal_loss_shares(**_grid(4, 2, np.ones((4, 2)), np.zeros((4, 2))), near_turns=2)
    assert float(got["term_loss_share"]) == pytest.approx(0.0)
    assert float(got["term_row_share"]) == pytest.approx(0.0)
    assert np.isfinite(float(got["term_leverage"]))


def test_one_terminal_row_carrying_all_the_error_reads_one_hundred_percent():
    """Eight rows, one terminal, and it is the only row with any error at all."""
    sq = np.zeros((4, 2)); sq[3, 0] = 5.0
    done = np.zeros((4, 2), bool); done[3, 0] = True
    got = T.terminal_loss_shares(**_grid(4, 2, sq, done), near_turns=1)
    assert float(got["term_loss_share"]) == pytest.approx(1.0)
    assert float(got["term_row_share"]) == pytest.approx(1 / 8)
    assert float(got["term_leverage"]) == pytest.approx(8.0)


def test_leverage_is_one_when_the_terminal_row_pulls_like_any_other():
    """**The reading that would justify upweighting.** Uniform error everywhere means a terminal row
    contributes exactly its share of the rows and no more."""
    got = T.terminal_loss_shares(
        **_grid(4, 2, np.full((4, 2), 3.0), np.eye(4, 2, dtype=bool)), near_turns=1)
    assert float(got["term_leverage"]) == pytest.approx(1.0)


def test_the_shares_are_measured_against_trainable_rows_only():
    """The opponent's seat is in the buffer and is not trained on, so it must not dilute the
    denominator -- the same mistake that made a per-opponent win rate meaningless."""
    sq = np.full((2, 2), 1.0)
    done = np.array([[False, False], [True, True]])
    trainable = np.array([[True, False], [True, False]])       # column 1 is the opponent
    got = T.terminal_loss_shares(**_grid(2, 2, sq, done, trainable), near_turns=1)
    # Two trainable rows, one of them terminal.
    assert float(got["term_row_share"]) == pytest.approx(0.5)
    assert float(got["term_loss_share"]) == pytest.approx(0.5)


def test_a_terminal_on_an_untrainable_row_is_not_counted():
    done = np.array([[False, False], [False, True]])
    trainable = np.array([[True, True], [True, False]])
    got = T.terminal_loss_shares(**_grid(2, 2, np.ones((2, 2)), done, trainable), near_turns=1)
    assert float(got["term_row_share"]) == pytest.approx(0.0)


# ---- the near-terminal window -----------------------------------------------------------------


def test_the_near_window_reaches_backwards_only():
    """A row is near-terminal if a terminal is at or *after* it within the window. Reaching forward
    would count rows the policy has already been paid for, which is not what a reverse curriculum or
    terminal upweighting touches."""
    done = np.zeros((6, 1), bool); done[3, 0] = True
    got = T.terminal_loss_shares(**_grid(6, 1, np.ones((6, 1)), done), near_turns=3)
    # Turns 1, 2 and 3 are within 3 of the terminal at turn 3; turns 0, 4 and 5 are not.
    assert float(got["near_row_share"]) == pytest.approx(3 / 6)


def test_the_near_window_does_not_wrap_around_the_horizon():
    """`jnp.roll` would make turn 0 adjacent to the last turn. A terminal at the very top of the
    window must leave the bottom untouched."""
    done = np.zeros((5, 1), bool); done[0, 0] = True
    got = T.terminal_loss_shares(**_grid(5, 1, np.ones((5, 1)), done), near_turns=4)
    assert float(got["near_row_share"]) == pytest.approx(1 / 5), (
        "only the terminal row itself is near; nothing precedes it in this window")


def test_a_window_of_one_is_exactly_the_terminal_rows():
    done = np.zeros((6, 2), bool); done[4, 1] = True
    a = T.terminal_loss_shares(**_grid(6, 2, np.arange(12).reshape(6, 2), done), near_turns=1)
    assert float(a["near_row_share"]) == pytest.approx(float(a["term_row_share"]))
    assert float(a["near_loss_share"]) == pytest.approx(float(a["term_loss_share"]))


def test_the_near_share_is_never_below_the_terminal_share():
    """Monotonicity, over a spread of windows -- the near set always contains the terminal set."""
    rng = np.random.default_rng(0)
    sq = rng.random((16, 4)).astype(np.float32)
    done = rng.random((16, 4)) < 0.1
    prev = 0.0
    for k in (1, 2, 4, 8):
        got = T.terminal_loss_shares(**_grid(16, 4, sq, done), near_turns=k)
        near = float(got["near_loss_share"])
        assert near >= float(got["term_loss_share"]) - 1e-6
        assert near >= prev - 1e-6, "widening the window cannot shrink the share"
        prev = near


def test_the_default_window_is_a_quarter_of_the_default_horizon():
    """A guard on the constant: `near8` in the log line has to mean something stable."""
    assert T.NEAR_TERMINAL_TURNS == 8
