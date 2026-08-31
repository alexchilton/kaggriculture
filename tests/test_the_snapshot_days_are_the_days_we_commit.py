"""The carried opponent snapshot must describe the days the agent actually branches on.

    python -u -m pytest tests/test_the_snapshot_days_are_the_days_we_commit.py -q

`kagg.sim` must not import `kagg.search`, so `jax_sim.SNAPSHOT_DAYS` repeats the two decision days
that `melon_branch` and `q4_branch` own, and `jax_obs` repeats the melon threshold and the yarn shop
index on top of that. Four constants in three modules, describing one thing.

**A duplicated constant that drifts is the failure mode this project keeps paying for**, and it is
always silent: `SOLVED_DAYS` was patched while the code read `PRECOMPUTED_ROUTES`, and the A/B came
back byte-identical and was written up as a measured null. Move `melon_branch.DECIDE_BY_DAY` to 4
and nothing here raises -- the snapshot is simply taken on a day nobody decides on, `melon_armed`
answers a question no branch asks, and every downstream number stays plausible.

So the copies are pinned here. This test is the reason the duplication is allowed to exist.

There is also a real invariant, not just bookkeeping: the snapshot must be taken **on or before**
the day the branch reads it. A snapshot of day 5 cannot inform a decision taken on day 3.
"""
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def test_the_melon_decision_day_is_a_snapshot_day():
    from kagg.search import melon_branch
    from kagg.sim import jax_sim as J

    assert melon_branch.DECIDE_BY_DAY in J.SNAPSHOT_DAYS, (
        "melon_branch decides on day %d and the snapshot is taken on days %s. The opponent's melon "
        "count on the decision day is the whole input to that branch, and no other day's board "
        "carries it." % (melon_branch.DECIDE_BY_DAY, J.SNAPSHOT_DAYS))


def test_the_yarn_decision_day_is_a_snapshot_day():
    from kagg.search import q4_branch
    from kagg.sim import jax_sim as J

    assert q4_branch.DECIDE_BY_DAY in J.SNAPSHOT_DAYS, (
        "q4_branch decides on day %d and the snapshot is taken on days %s."
        % (q4_branch.DECIDE_BY_DAY, J.SNAPSHOT_DAYS))


def test_the_encoder_repeats_the_branch_constants_exactly():
    """`jax_obs` states both latches itself; its copies of the thresholds must be the real ones."""
    from kagg.search import melon_branch, q4_branch
    from kagg.sim.town import SHOPS

    from kagg.rl import jax_obs

    assert jax_obs.MELON_LATCH_DAY == melon_branch.DECIDE_BY_DAY
    assert jax_obs.OPPONENT_MELON == melon_branch.OPPONENT_MELON, (
        "jax_obs says the melon latch fires at %d tiles; melon_branch fires at %d."
        % (jax_obs.OPPONENT_MELON, melon_branch.OPPONENT_MELON))
    assert jax_obs.Q4_LATCH_DAY == q4_branch.DECIDE_BY_DAY
    assert list(SHOPS)[jax_obs.YARN_STORE_INDEX] == q4_branch.TRIGGER_SHOP, (
        "jax_obs reads shop index %d, which is %s; q4_branch triggers on %s."
        % (jax_obs.YARN_STORE_INDEX, list(SHOPS)[jax_obs.YARN_STORE_INDEX], q4_branch.TRIGGER_SHOP))


@pytest.mark.parametrize("module,attr", [("melon_branch", "DECIDE_BY_DAY"),
                                         ("q4_branch", "DECIDE_BY_DAY")])
def test_a_snapshot_is_never_taken_after_the_day_it_informs(module, attr):
    """The snapshot for a branch must exist by the time that branch reads it."""
    import importlib

    from kagg.sim import jax_sim as J

    decide = getattr(importlib.import_module(f"kagg.search.{module}"), attr)
    earlier = [d for d in J.SNAPSHOT_DAYS if d <= decide]
    assert earlier, (
        "%s decides on day %d and every snapshot day %s is later. The branch would be reading a "
        "board from its own future." % (module, decide, J.SNAPSHOT_DAYS))


def test_the_two_ways_a_board_becomes_a_snapshot_agree():
    """`jax_sim.seat_summary` and `adapter._seat_summary_from_obs` build the same 17 columns.

    Two implementations of one layout, one per path -- the same shape of pair as the two encoders,
    which had been silently disagreeing on 23 unit slots. The snapshot is worse if they drift: its
    whole value is being comparable with the LIVE opponent block, so a permuted column turns a
    subtraction into noise that still looks like a number.
    """
    import numpy as np
    from kaggle_environments import make

    from kagg.rl import adapter as AD

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    for _ in range(30):                      # let the boards stop being identical
        if env.done:
            break
        env.step([{}, {}])
    obs = env.state[0].observation
    privates = [obs["private"] if p == 0 else AD.agent_private_stub() for p in range(2)]

    from_obs = np.asarray(AD._seat_summary_from_obs(obs))[0]
    state = AD.state_from_obs(obs, privates, step=30)
    from_state = np.asarray(__import__("kagg.sim.jax_sim", fromlist=["x"]).seat_summary(
        state.tiles, state.farm))[0]

    bad = np.flatnonzero(np.abs(from_obs - from_state).max(axis=0) > 1e-4)
    assert bad.size == 0, (
        "columns %s differ.\n  from observation %s\n  from state       %s"
        % (bad.tolist(), from_obs[0][bad].tolist(), from_state[0][bad].tolist()))
