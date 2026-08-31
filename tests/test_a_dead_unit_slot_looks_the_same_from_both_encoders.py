"""The two ways a board becomes features must produce the same features.

    python -u -m pytest tests/test_a_dead_unit_slot_looks_the_same_from_both_encoders.py -q

THE DEFECT
----------
There are two entry points into `jax_obs.encode`, and they are not the same function:

    training       jax_obs.encode(jax_sim.State)                   -- native, RL rollouts
    play / BC      adapter.state_from_obs(obs) -> jax_obs.encode   -- the shipped submission,
                                                                      and every imitation label

`jax_sim.reset` leaves the 23 unhired unit slots at the spawn tile, so their `x`, `y` and `on_shed`
features are non-zero; `adapter.state_from_obs` builds them from an observation that has no such
units and leaves them at zero. `live` is 0 in both, so the slots are correctly dead -- but the
transformer attends over every token, and three non-zero features on 23 dead tokens are not nothing.

Measured 2026-08-28 (`scripts/diff_the_two_ways_a_board_becomes_features.py`), one board, one set of
weights, turn 0:

    slots differing [1..23]   feats differing [1, 2, 3]
    op         from jax_sim [1 0 0 0]   from adapter [17 0 0 0]
    qty_sell   from jax_sim [8 6 0 2]   from adapter [3 6 0 8]

The LIVE farmer's op changes. So a checkpoint fitted through the adapter path and warm-started into
RL is, on its very first rollout, reading a different game -- and no learning rate, entropy
coefficient or KL setting repairs an observation mismatch.

**The 300/300 fast-sim parity gate does not cover this.** It tests the SIMULATOR against the
reference, op for op. It says nothing about the ENCODER, and this is the encoder.

WHICH DIRECTION IS CORRECT -- AND THIS FILE FIRST GOT IT WRONG
--------------------------------------------------------------
It said ZERO: a slot with `live == 0` is not a unit, so make `jax_obs` gate x/y/on_shed on `live`
and let training see what play sees. That reasoning is sound about the game and wrong about the
weights, and it cost a training run.

Gating those three columns is not an append -- **it changes the meaning of three features every
existing checkpoint was fitted on.** Dead slots were 0.444/0.444/1.0 when the weights were trained.
`jax_policy.migrate_params` zero-pads columns that are NEW; it has no way to repair a column whose
meaning moved, so the warm start's unit projection read a different feature than it was fitted on.
The run that followed put per-op agreement at exactly 0.000 across 12,844 WEST, 12,960 NORTH and
10,013 EAST labels -- not "learned badly", unreachable -- while the loss fell normally, which is
what a broken input looks like from the outside.

**The correct direction is SPAWN**, in `adapter.state_from_obs` and `numpy_obs.state_from_obs`:
park the unhired slots where `jax_sim.reset` parks them. The two paths agree, and not one trained
column changes.

The invariant is therefore AGREEMENT, not zero. A test that pins a specific value here is pinning a
weight convention, and it will send the next person to fix the encoder instead of the adapter --
which is exactly what happened.
"""
import pathlib
import sys

import numpy as np
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

LIVE = 0                    # feature 0 of the unit token
INTRINSIC = (1, 2, 3)       # x, y, on_shed -- properties of a UNIT, meaningless without one

# Features 4+ are `carried` and the `_target(...)` distances. Those are derived from the BOARD, and
# both encoders already agree on them for a dead slot -- the measured diff is exactly (1, 2, 3). So
# "a dead slot must be all zeros" is the wrong invariant and would fail after a correct fix.


def _both_encodings():
    """`(from_jax_sim, from_adapter)` unit features for the same fresh board."""
    from kagg.rl import adapter as AD, jax_obs
    from kagg.sim import jax_sim as J

    state = J.reset(1)
    _t, units_native, _g = jax_obs.encode(state)

    obs, privates = AD.obs_from_state(state, 0) if hasattr(AD, "obs_from_state") else (None, None)
    if obs is None:                                   # no state->obs helper; build it from the env
        from kaggle_environments import make
        env = make("kaggriculture", configuration={"seed": 11}, debug=False)
        env.reset(2)
        o = env.state[0].observation
        privates = [o["private"] if p == 0 else AD.agent_private_stub() for p in range(2)]
        adapted = AD.state_from_obs(o, privates, step=0)
    else:
        adapted = AD.state_from_obs(obs, privates, step=0)
    _t2, units_adapter, _g2 = jax_obs.encode(adapted)
    return np.asarray(units_native), np.asarray(units_adapter)


def test_a_dead_slot_sits_where_the_simulator_parks_it():
    """Both paths must put an unhired slot on the SPAWN tile -- not at the origin, and not at zero.

    Pinned to the value rather than left to the agreement test below, because agreement alone is
    also satisfied by both encoders being wrong together -- which is what gating these columns on
    `live` would have produced, silently and in a way that invalidates every checkpoint.
    """
    from kagg.sim import farm as F

    native, adapted = _both_encodings()
    sx, sy = (int(v) for v in F.default_spawn())
    want = np.array([sx / 9.0, sy / 9.0], dtype=np.float32)

    for name, u in (("jax_sim", native), ("adapter", adapted)):
        dead = u[..., LIVE] == 0
        if not dead.any():
            pytest.skip(f"{name}: no dead slots on this board")
        got = u[dead][0][list(INTRINSIC)]
        assert np.allclose(got[:2], want, atol=1e-6), (
            f"{name}: a dead unit slot reads x/y {got[:2]} against the spawn tile {want}. "
            "Every checkpoint was fitted with unhired slots parked at spawn; moving them "
            "re-points a trained column and `migrate_params` cannot repair it.")


def test_the_two_encoders_agree_on_the_dead_slots():
    """The head-to-head the RL warm start actually depends on."""
    native, adapted = _both_encodings()
    n = min(native.shape[-2], adapted.shape[-2])
    dead = (native[0, 0, :n, LIVE] == 0) & (adapted[0, 0, :n, LIVE] == 0)
    if not dead.any():
        pytest.skip("no commonly dead slots on this board")
    a, b = native[0, 0, :n][dead], adapted[0, 0, :n][dead]
    diff = np.flatnonzero(np.abs(a - b).sum(axis=0) > 1e-6)
    assert diff.size == 0, (
        f"the two encoders disagree on features {diff.tolist()} of the dead unit slots.\n"
        f"  jax_sim  {a[0]}\n  adapter  {b[0]}\n"
        "A checkpoint fitted through one and rolled out through the other is reading a "
        "different game.")
