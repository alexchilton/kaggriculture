"""The student must be able to see the turn, and which shops are trading.

Two features, both added 2026-08-22 on Fable's review (`docs/fable_dagger_review_2026-08-22.md`).

**The clock.** A tape-replaying teacher is a ~719-entry lookup keyed on the turn. It used to reach
the network as two smooth scalars, `day/30` and `hour/24`, and a net fits low frequencies first, so
that asks a 3-layer trunk to carve two smooth ramps into 719 bins. On-tape the board proxies for the
turn; off-tape -- where DAgger collects -- it does not.

**The open shops.** `q4_branch` picks which of four tapes gets replayed on "is the yarn store
unlocked" (`q4_branch.py:242`). That bit was not in the observation at all, and `adapter` stubbed the
unlock schedule to NEVER, so on the reference-environment path it read all-zero. On four fixed games
that is confounded with game identity: training looks fine, deployment fails invisibly.

Related: `tests/test_rehire_cost_feature.py`, which reads the END-relative afford offsets that these
features must not shift.
"""
import json
import pathlib
import sys

import numpy as np
import pytest

from kagg.rl import adapter as AD, jax_obs
from kagg.sim import jax_sim as J
from kagg.sim.town import SHOPS

REPO = pathlib.Path(__file__).resolve().parents[1]

#: Where the new block starts: money, opp_money, lead, day/30, hour/24.
_OFFSET = 3 + 2
_HOUR = slice(_OFFSET, _OFFSET + J.TURNS_PER_DAY)
_DAY = slice(_OFFSET + J.TURNS_PER_DAY, _OFFSET + J.TURNS_PER_DAY + jax_obs.N_DAYS)
_SHOPS = slice(_OFFSET + J.TURNS_PER_DAY + jax_obs.N_DAYS,
               _OFFSET + J.TURNS_PER_DAY + jax_obs.N_DAYS + J.N_SHOPS)


def test_the_global_vector_is_as_wide_as_the_constant_says():
    """A constant that lies about the width is how a checkpoint silently fails to load."""
    _t, _u, glob = jax_obs.encode(J.reset_with_shops(2, seed=0))
    assert glob.shape[-1] == jax_obs.GLOBAL_FEATURES


def test_the_turn_is_readable_as_a_one_hot():
    state = J.reset_with_shops(1, seed=0)
    for step in (0, 1, 25, 200, 718):
        st = state._replace(step_index=J.jnp.full_like(state.step_index, step))
        _t, _u, glob = jax_obs.encode(st)
        g = np.asarray(glob)[0, 0]
        hour, day = step % J.TURNS_PER_DAY, step // J.TURNS_PER_DAY
        assert g[_HOUR].sum() == pytest.approx(1.0), "hour is not exactly one-hot at step %d" % step
        assert int(np.argmax(g[_HOUR])) == hour
        assert g[_DAY].sum() == pytest.approx(1.0), "day is not exactly one-hot at step %d" % step
        assert int(np.argmax(g[_DAY])) == min(day, jax_obs.N_DAYS - 1)


def test_the_day_saturates_rather_than_wrapping_past_the_bell():
    """An index past the last day must read as the last day, not as day 0 and not as all-zero."""
    state = J.reset_with_shops(1, seed=0)
    st = state._replace(step_index=J.jnp.full_like(state.step_index, 40 * J.TURNS_PER_DAY))
    _t, _u, glob = jax_obs.encode(st)
    g = np.asarray(glob)[0, 0]
    assert g[_DAY].sum() == pytest.approx(1.0)
    assert int(np.argmax(g[_DAY])) == jax_obs.N_DAYS - 1


@pytest.mark.slow
def test_the_open_shops_match_the_observation_on_the_reference_path():
    """The bits must track `town.unlocked_shops`, through the adapter, in a real game.

    This is the one that was silently all-zero: `adapter.state_from_obs` stubbed the unlock schedule
    to NEVER, so the feature existed and meant nothing on the only path DAgger uses.
    """
    from kaggle_environments import make

    sys.path.insert(0, str(REPO / "scripts"))
    import breakdown as B

    from kagg.search import schedule_agent as SA

    tape_path, team = SA.REPLAY_OPENING_TAPE[(True, False)]
    doc = json.loads((REPO / tape_path).read_text())
    seat = doc["info"]["TeamNames"].index(team)
    cfg = B.env_config(REPO / tape_path)
    cfg.pop("steps", None)
    cfg["seed"] = int(doc["info"]["seed"])
    cfg["weedSpawnChance"] = 0.0
    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    mine = [((s[seat] or {}).get("action") or {}) for s in doc["steps"][1:]]
    opp = [((s[1 - seat] or {}).get("action") or {}) for s in doc["steps"][1:]]

    checked, saw_open = 0, False
    for turn in range(200):
        if env.done:
            break
        obs = env.state[seat].observation
        privates = [obs["private"] if p == seat else AD.agent_private_stub() for p in range(2)]
        _t, _u, glob = jax_obs.encode(AD.state_from_obs(obs, privates))
        bits = np.asarray(glob)[0, seat][_SHOPS]
        got = sorted(SHOPS[i] for i, v in enumerate(bits) if v > 0.5)
        want = sorted(set(n for n in ((obs.get("town") or {}).get("unlocked_shops") or [])
                          if n in SHOPS))
        assert got == want, "turn %d: bits %s, observation %s" % (turn, got, want)
        checked += 1
        saw_open = saw_open or bool(want)

        hands = [len((env.state[0].observation["farms"][i] or {}).get("hands") or [])
                 for i in (0, 1)]
        pair = [None, None]
        pair[seat] = {"farmer": mine[turn].get("farmer") or ["PASS"],
                      "hands": list(mine[turn].get("hands") or [])[:hands[seat]],
                      "market": mine[turn].get("market") or []}
        pair[1 - seat] = {"farmer": opp[turn].get("farmer") or ["PASS"],
                          "hands": list(opp[turn].get("hands") or [])[:hands[1 - seat]],
                          "market": opp[turn].get("market") or []}
        env.step(pair)

    assert checked > 100
    # Without this the test passes on an all-zero feature against an all-empty observation, which is
    # exactly the bug it exists to catch.
    assert saw_open, "no shop ever opened in 200 turns; the test proves nothing"
