"""Board assignment for *selection*: rival candidates must be ranked on the same markets.

`jax_sim.random_unlock_days` gives every batch element its own shop unlock order, and its docstring
is right about why -- "a batch cannot learn one market's timing and call it the market". That is the
correct choice for **training**, where batch elements are independent episodes.

It is the wrong choice for **selection**, where batch elements are rival candidates whose scores get
compared to each other. Measured (`tests/test_selection_boards_are_shared.py`): one identical tape
scored $107,661 to $152,867 across six batch positions -- a $45,206 spread, 27% of the score, from
batch index alone. `scripts/optimise_script.py` was taking an argmax over that, so it selected
whichever candidate drew the friendliest shop order. Its recorded +1.6% is smaller than the spread by
a factor of 16.

`kagg/search/rollout.py:114` already had the discipline this module restores -- "on every unlock
schedule", one schedule across all candidates, averaged -- and `cem.confirm` even re-draws schedules
as a winner's-curse check. The numpy search got it right; the JAX tape optimiser lost it.

The layout here matches what the optimiser's `_expand` already builds: a flat game index
``pair * batch + candidate``, where ``pair = opponent * n_boards + board``. Every candidate therefore
meets the identical set of (opponent, board) combinations, so a score difference between two
candidates is a difference between the candidates.
"""

import numpy as np

from kagg.sim import jax_sim as J


def board_schedules(n_boards, seed=0):
    """`[n_boards, N_SHOPS]` distinct unlock orders -- the set every candidate is scored on."""
    if n_boards < 1:
        raise ValueError(f"n_boards must be >= 1, got {n_boards}")
    return np.asarray(J.random_unlock_days(n_boards, seed=seed), dtype=np.int32)


def pair_count(n_opponents, n_boards):
    """Games per candidate: every opponent on every board."""
    return n_opponents * n_boards


def unlock_array(n_opponents, n_boards, batch, seed=0):
    """`[n_opponents*n_boards*batch, N_SHOPS]`, indexed as ``pair*batch + candidate``.

    The board depends only on `pair`, never on `candidate`, which is the whole point: candidate `c`
    and candidate `c'` face the same board in the same pair slot.
    """
    sched = board_schedules(n_boards, seed=seed)
    # Row `pair` must be `sched[pair % n_boards]`, so tile (not repeat) over the opponent axis...
    per_pair = np.tile(sched, (n_opponents, 1))
    # ...then repeat each pair `batch` times, giving flat index `pair*batch + candidate`.
    return np.repeat(per_pair, batch, axis=0)


def opponent_of_pair(n_boards, n_pairs):
    """Which opponent each pair slot belongs to, for stacking the opponent scripts."""
    return [p // n_boards for p in range(n_pairs)]
