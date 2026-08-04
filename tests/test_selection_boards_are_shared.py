"""Two candidates in one evaluation batch must be scored on the same markets.

`scripts/optimise_script.py` ranks candidates by argmax over one batch, and compares that argmax
against a best recorded in an earlier batch. Both comparisons are claims about scripts, and they are
only valid if a script's score does not depend on where it sat in the batch.

It did. Measured before the fix, with one tape replicated across six batch positions of
`reset_with_shops`:

    one script scored 107,661 to 152,867 across 6 batch positions (spread $45,206)

27% of the score from batch index alone, against a recorded "improvement" of 1.6%. So the optimiser's
argmax was selecting whichever candidate drew the friendliest shop unlock order.

The defect was in the caller, not in `jax_sim.random_unlock_days` -- per-game randomness is correct
for *training*, where batch elements are independent episodes, and these tests deliberately do not
touch it. What they pin is `kagg/search/boards.py`, which assigns boards for *selection*.

The final test is the end-to-end one and the only one that would have caught the original bug.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.search import boards as B
from kagg.sim import jax_sim as J

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")


def test_every_candidate_meets_the_same_set_of_boards():
    """**The invariant selection depends on.** Board is a function of pair, never of candidate."""
    n_opp, n_boards, batch = 3, 4, 5
    arr = B.unlock_array(n_opp, n_boards, batch, seed=0)
    pairs = B.pair_count(n_opp, n_boards)
    assert arr.shape == (pairs * batch, J.N_SHOPS)

    reshaped = arr.reshape(pairs, batch, J.N_SHOPS)
    for p in range(pairs):
        for c in range(1, batch):
            np.testing.assert_array_equal(
                reshaped[p, c], reshaped[p, 0],
                err_msg=f"pair {p}: candidate {c} plays a different board than candidate 0. "
                        "An argmax over this batch would rank boards, not scripts.")


def test_the_boards_are_actually_different_from_each_other():
    """The other half: sharing must not collapse to one board, or we are back to single-seed tuning."""
    arr = B.unlock_array(1, 6, 1, seed=0)
    distinct = {tuple(row) for row in np.asarray(arr)}
    assert len(distinct) > 1, (
        "all boards identical -- averaging over them adds nothing and the score is a single-market "
        "score wearing a mean")


def test_pair_slots_map_back_to_the_right_opponent():
    """`pair = opponent*n_boards + board`, so the opponent stack must be built to match."""
    n_boards = 3
    owners = B.opponent_of_pair(n_boards, B.pair_count(4, n_boards))
    assert owners == [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]


def test_one_script_scores_identically_at_every_batch_index():
    """End-to-end. This is the test whose absence let a 27% noise floor sit under every measurement."""
    tape = np.load("data/seed_scripts/replay_89873723_seat0.npz")
    mine = {}
    for f in FIELDS:
        v = np.asarray(tape[f]).astype(np.int64)
        mine[f] = v[:, 0] if v.ndim >= 2 and v.shape[1] == 2 else v

    batch, n_boards = 4, 1
    unlocks = B.unlock_array(1, n_boards, batch, seed=0)
    state = J.reset(len(unlocks), unlock_schedule=unlocks, seed=0)
    T = mine["unit_op"].shape[0]

    for t in range(T):
        acts = J.Actions(**{f: jnp.asarray(np.broadcast_to(
            mine[f][t][None, None], (len(unlocks), 2) + np.shape(mine[f][t]))) for f in FIELDS})
        state = J.step(state, acts, weed_chance=0.0)

    money = np.asarray(state.farm.money[:, 0])
    spread = float(money.max() - money.min())
    assert spread < 1.0, (
        f"one script scored {money.min():,.0f} to {money.max():,.0f} across {batch} batch positions "
        f"(spread ${spread:,.0f}) -- selection is still ranking boards")
