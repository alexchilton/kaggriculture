"""The dict-observation bridge, gated the same way the simulator is.

`kagg/rl/adapter.py` rebuilds a `jax_sim.State` from the reference environment's nested dicts so a
trained policy can play the real game. A bridge that is *nearly* right is the worst outcome
available: the policy would act on a subtly wrong board, play badly, and every metric would blame
the policy. So this compares the reconstruction against the simulator field by field, over a real
episode, rather than checking that it merely runs.

The comparison runs the reference environment and the simulator from the same actions, then rebuilds
a State from the environment's observation and asserts it matches the simulator's -- which is the
same shape of test as `tests/test_sim_parity.py`, for the same reason.
"""

import numpy as np
import pytest

from kagg.rl import adapter
from kagg.sim import jax_sim as J
from kagg.sim.parity import random_script, run_reference

jax = pytest.importorskip("jax")

TILE_FIELDS = ("kind", "crop", "planted_day", "yield_units", "animal", "placed_day",
               "consecutive_unfed", "fed_today", "cared_today", "pending_care_bonus")


def _obs_and_privates(env):
    obs = env.state[0].observation
    privates = [env.state[p].observation["private"] for p in range(2)]
    return obs, privates


def test_state_from_obs_matches_the_environment_it_was_built_from():
    """Rebuild a State mid-episode and check every field against the environment's own dicts.

    Driving a script that plants, builds, hires and places animals matters: a bridge tested on an
    empty board proves only that zeros survive the trip. The same mistake -- a gate that could not
    reach the thing it claimed to cover -- has already cost this project twice.
    """
    from kaggle_environments import make

    rng = np.random.default_rng(3)
    script = random_script(rng, steps=200, max_units=6, allow_hire=True, hire_rate=0.5)

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(num_agents=2)
    # Replay far enough in that farms hold crops, animals, seeds and a crew.
    ref, _unlocks = run_reference(script, seed=11)

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(num_agents=2)
    from kagg.sim.parity import CROPS, ITEM_OPS, OP_NAMES
    from kagg.sim import ops as O

    for entry in script:
        farms = env.state[0].observation["farms"]
        actions = []
        for p in range(2):
            ops, crops, items, qtys = entry["units"][p]

            def _as(op, crop, item, qty):
                if op == O.PLANT_OP:
                    return ["PLANT", CROPS[crop]]
                if op in ITEM_OPS:
                    from kagg.sim.market import ITEMS
                    return [ITEM_OPS[op], ITEMS[item], qty]
                return [OP_NAMES[op]]

            n_hands = len(farms[p].get("hands", []))
            farmer = _as(ops[0], crops[0], items[0], qtys[0])
            hands = [_as(o, c, i, q) for o, c, i, q in
                     zip(ops[1:], crops[1:], items[1:], qtys[1:])][:n_hands]
            market = []
            for item, n in entry["sell"][p].items():
                if n:
                    market.append(["SELL", item, n])
            for crop, n in entry["buy_seed"][p].items():
                if n:
                    market.append(["BUY_SEED", crop, n])
            if entry["hire"][p]:
                market.append(["HIRE"])
            actions.append({"farmer": farmer, "hands": hands, "market": market[:10]})
        env.step(actions)
        if env.done:
            break

    obs, privates = _obs_and_privates(env)
    state = adapter.state_from_obs(obs, privates)

    # Money, inventory and step come straight across and are the easiest to get wrong by an axis.
    assert float(np.asarray(state.farm.money)[0, 0]) == obs["farms"][0]["money"]
    assert float(np.asarray(state.farm.money)[0, 1]) == obs["farms"][1]["money"]
    assert int(np.asarray(state.step_index)[0]) == obs.get("step", 0)

    from kagg.sim.market import PRODUCTS
    for i, item in enumerate(PRODUCTS):
        assert int(np.asarray(state.inventory)[0, i]) == obs["market"]["inventory"][item]

    # Unit count and positions: the farmer plus every hired hand, in that order.
    for p in range(2):
        expected = [tuple(obs["farms"][p]["farmer"])] + [
            tuple(h) for h in obs["farms"][p].get("hands", [])]
        assert int(np.asarray(state.farm.n_units)[0, p]) == len(expected)
        for u, (x, y) in enumerate(expected):
            got = np.asarray(state.farm.unit_pos)[0, p, u]
            assert (int(got[0]), int(got[1])) == (x, y)

    # Seeds and shed, per player.
    from kagg.sim.market import ITEM_INDEX
    from kagg.sim.tiles import CROP_INDEX
    for p in range(2):
        for crop, ci in CROP_INDEX.items():
            assert int(np.asarray(state.farm.seeds)[0, p, ci]) == \
                privates[p]["seeds"].get(crop, 0)
        for item, ii in ITEM_INDEX.items():
            assert int(np.asarray(state.farm.shed)[0, p, ii]) == \
                privates[p]["shed"].get(item, 0)


def test_the_rebuilt_state_encodes_without_nans():
    """The encoder must accept a rebuilt State, since that is the only thing a submission feeds it."""
    from kaggle_environments import make
    from kagg.rl import jax_obs

    env = make("kaggriculture", configuration={"seed": 5, "weedSpawnChance": 0.0}, debug=False)
    env.reset(num_agents=2)
    env.step([{"farmer": ["PASS"], "hands": [], "market": []} for _ in range(2)])

    obs, privates = _obs_and_privates(env)
    tiles, units, glob = jax_obs.encode(adapter.state_from_obs(obs, privates))

    for name, arr in (("tiles", tiles), ("units", units), ("glob", glob)):
        a = np.asarray(arr)
        assert np.isfinite(a).all(), f"{name} has non-finite values"
        assert a.shape[0] == 1 and a.shape[1] == 2, f"{name} has shape {a.shape}"
