"""Seated second, the observation carries no `step`, and the whole season runs as day 0.

**The defect.** `kaggle_environments` puts `step` only in seat 0's observation. `state_from_obs`
reads `int(obs.get("step", 0))`, so for a seat-1 agent the clock is pinned at 0 for all 720 turns.
Measured 2026-08-22 on the four DAgger tapes, at true turn 100 (day 4):

    92498144.json    seat 0 -> step_index 100  day 4
    91907974.json    seat 0 -> step_index 100  day 4
    92466371.json    seat 0 -> step_index 100  day 4
    91906088.json    seat 1 -> step_index   0  day 0     <-- one of the four training tapes

**What it costs.** Every crop and animal rule is driven by `step_index // TURNS_PER_DAY`. The one
that bites hardest is HARVEST, whose mask is

    ripe = is_plant & (yield_units > 0) & ((day - planted_day) >= FIRST_YIELD_DAY[crop])

With `day` frozen at 0 and `planted_day` read from a real mid-season board, `day - planted_day` goes
negative and nothing is ever ripe. So HARVEST is masked illegal all season -- unemittable through
`_masked_logits` and zero-weighted in the loss by `bc.py:232`, the same double lock as the LOCKED
bugs. Measured across the four tapes over 719 turns: **300 of 1585 HARVEST labels forbidden, 301 of
the 307 total offenders on that one tape.**

`curriculum.py:114` already found this and wrote `_with_step_index` to work around it locally. The
workaround never reached `dagger_tape`, so a quarter of the imitation training data has a wrong
clock.

The fix is an explicit `step` argument. `state_from_obs` keeps defaulting to `obs["step"]` for the
callers that have it, and a caller that knows the turn says so rather than hoping.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")
kaggle_environments = pytest.importorskip("kaggle_environments")

from kagg.rl import adapter as AD
from kagg.rl import jax_masks
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

TURN = 100
DAY = TURN // J.TURNS_PER_DAY


def stepped_env(turns=TURN):
    env = kaggle_environments.make("kaggriculture", debug=False)
    env.reset(2)
    for _ in range(turns):
        env.step([{}, {}])
    return env


def state_for(env, seat, **kw):
    obs = env.state[seat].observation
    privates = [obs["private"] if p == seat else AD.agent_private_stub() for p in range(2)]
    return AD.state_from_obs(obs, privates, **kw)


def test_seat_one_really_has_no_step_in_its_observation():
    """The fixture for everything below. If this fails, the environment changed."""
    env = stepped_env()
    assert env.state[0].observation.get("step") == TURN
    assert env.state[1].observation.get("step") is None, (
        "seat 1 now carries a step; this whole class of bug is gone and the workaround below "
        "can be deleted")


def test_seated_second_the_clock_is_wrong_without_an_explicit_step():
    """Documents the trap itself, so nobody 'fixes' the default and is surprised."""
    env = stepped_env()
    st = state_for(env, seat=1)
    assert int(np.asarray(st.step_index).reshape(-1)[0]) == 0


def test_an_explicit_step_wins_for_seat_one():
    env = stepped_env()
    st = state_for(env, seat=1, step=TURN)
    got = int(np.asarray(st.step_index).reshape(-1)[0])
    assert got == TURN, (
        "seated second, an explicitly supplied step must reach step_index; got %d, wanted %d"
        % (got, TURN))
    assert got // J.TURNS_PER_DAY == DAY


def test_an_explicit_step_wins_for_seat_zero_too():
    """It must override, not merely fill a gap -- a caller that knows the turn is the authority."""
    env = stepped_env()
    st = state_for(env, seat=0, step=7)
    assert int(np.asarray(st.step_index).reshape(-1)[0]) == 7


def test_omitting_step_still_reads_the_observation():
    """The existing callers must not change behaviour."""
    env = stepped_env()
    st = state_for(env, seat=0)
    assert int(np.asarray(st.step_index).reshape(-1)[0]) == TURN


def test_the_wrong_clock_is_what_forbids_harvest():
    """The consequence, driven through the real mask rather than asserted about it.

    A ripe plant on a mid-season board is harvestable with the true clock and is not with a day-0
    one. This is the mechanism behind `HARVEST 300/1585 forbidden`.
    """
    env = stepped_env()
    obs = env.state[1].observation
    privates = [obs["private"] if p == 1 else AD.agent_private_stub() for p in range(2)]

    true_clock = AD.state_from_obs(obs, privates, step=TURN)
    day0_clock = AD.state_from_obs(obs, privates)

    # Put a ripe wheat under unit 0 of seat 1, planted early enough to be harvestable at DAY.
    def with_ripe_plant(st):
        pos = np.asarray(st.farm.unit_pos).copy()
        pos[0, 1, 0] = (2, 2)
        idx = 2 * J.BOARD + 2
        kind = np.asarray(st.tiles.kind).copy()
        crop = np.asarray(st.tiles.crop).copy()
        planted = np.asarray(st.tiles.planted_day).copy()
        yield_u = np.asarray(st.tiles.yield_units).copy()
        kind[0, 1, idx] = J.PLANT
        crop[0, 1, idx] = 0
        planted[0, 1, idx] = 0
        yield_u[0, 1, idx] = 3
        return st._replace(
            farm=st.farm._replace(unit_pos=jnp.asarray(pos, dtype=J._I)),
            tiles=st.tiles._replace(
                kind=jnp.asarray(kind, dtype=J._I),
                crop=jnp.asarray(crop, dtype=J._I),
                planted_day=jnp.asarray(planted, dtype=J._I),
                yield_units=jnp.asarray(yield_u, dtype=J._I)))

    ok = np.asarray(jax_masks.unit_op_mask(with_ripe_plant(true_clock)))[0, 1, 0]
    bad = np.asarray(jax_masks.unit_op_mask(with_ripe_plant(day0_clock)))[0, 1, 0]

    assert ok[O.HARVEST], (
        "a ripe wheat planted on day 0 is not harvestable at day %d even with the true clock; "
        "the fixture is wrong, not the code" % DAY)
    assert not bad[O.HARVEST], (
        "the day-0 clock did NOT forbid the harvest, so it is not the mechanism behind the 300 "
        "forbidden HARVEST labels and the diagnosis needs redoing")


def test_dagger_tape_passes_the_turn_it_already_knows():
    """A call-site test, because the unit tests above all pass with the caller left broken.

    This is the failure mode the carrot rule hit earlier the same day: eight green unit tests and
    the feature wired in at a point that never ran.
    """
    import inspect
    import pathlib
    import sys

    repo = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo / "scripts"))
    import dagger_tape as DT

    src = inspect.getsource(DT.run_episode)
    assert "state_from_obs(obs, privates, step=" in src, (
        "run_episode builds its state without passing the turn it is already iterating over, so "
        "the seat-1 tape trains on a day-0 clock. Found:\n%s"
        % "\n".join(l for l in src.splitlines() if "state_from_obs" in l))
