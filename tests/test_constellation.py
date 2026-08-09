"""Tests for `kagg.arena.constellation` -- forcing which shops the town unlocks.

Why this exists: the shop draw is not a function of the seed alone.
`_spawn_weeds` consumes draws from the same per-day rng *before* the unlock draw
(`reference/kaggriculture.py:856-878`), and weed spawning depends on which tiles are empty, so how
the agents play shifts the rng stream position the shop draw lands on. Measured, same seed 29:
PASS-vs-PASS play and real-agent play produced two different shop sequences. A seed -> constellation
catalogue is therefore agent-dependent and goes stale whenever the agent changes; the constellation
has to be imposed, not searched for.

All tests here are fast: with `turnsPerDay=1` and `townShopUnlockInterval=1`, all `MAX_SHOP_INSTANCES`
unlocks land inside 8 turns, well under the ~50-turn threshold for `@pytest.mark.slow`.
"""

import random

import pytest
from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.arena.constellation import (
    MAX_SHOP_INSTANCES,
    drain_vector,
    enumerate_constellations,
    forced_shops,
)

ALL_EIGHT = [
    "BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "YARN_STORE",
    "ICE_CREAM_SHOP", "PET_CAFE", "SMOOTHIE_SHOP", "FARMERS_MARKET",
]

FAST_CFG = {"turnsPerDay": 1, "townShopUnlockInterval": 1}

NO_OP = {"farmer": ["PASS"], "hands": [], "market": []}


def _play_out_unlocks(seed, n_steps=MAX_SHOP_INSTANCES):
    """Step a fresh env `n_steps` times with both players passing, return the
    town's unlocked_shops list. With FAST_CFG, one shop unlocks per step."""
    env = make("kaggriculture", configuration={"seed": seed, **FAST_CFG}, debug=False)
    env.reset(2)
    for _ in range(n_steps):
        env.step([dict(NO_OP), dict(NO_OP)])
    return list(env.state[0].observation.town["unlocked_shops"])


# -- 1. forcing a list yields exactly that list, in order --------------------------------------

def test_forced_list_yields_exact_order():
    with forced_shops(ALL_EIGHT):
        unlocked = _play_out_unlocks(seed=13)
    assert unlocked == ALL_EIGHT


# -- 2. env is restored exactly on a normal exit ------------------------------------------------

def test_restores_random_choice_on_normal_exit():
    before = random.Random.choice
    with forced_shops(ALL_EIGHT):
        assert random.Random.choice is not before, "patch should be installed inside the block"
    assert random.Random.choice is before, "patch must be removed after the block exits normally"


# -- 3. env is restored exactly when the body raises ---------------------------------------------

def test_restores_random_choice_on_exception():
    before = random.Random.choice
    with pytest.raises(RuntimeError):
        with forced_shops(ALL_EIGHT):
            assert random.Random.choice is not before
            raise RuntimeError("boom")
    assert random.Random.choice is before, "patch must be removed even when the body raises"


# -- 4. forcing is play-independent: identical under two different seeds ------------------------

def test_forcing_identical_under_two_seeds():
    with forced_shops(ALL_EIGHT):
        unlocked_a = _play_out_unlocks(seed=13)
    with forced_shops(ALL_EIGHT):
        unlocked_b = _play_out_unlocks(seed=97)
    assert unlocked_a == ALL_EIGHT
    assert unlocked_b == ALL_EIGHT
    assert unlocked_a == unlocked_b


# -- 5. the enumerator returns 285 distinct classes ----------------------------------------------

def test_enumerator_returns_285_distinct_classes():
    constellations = enumerate_constellations()
    assert len(constellations) == 285, (
        "6,435 multisets of 8 shops from 8 types collapse to 285 distinct drain vectors over "
        "(MILK, WOOL, STRAWBERRY, MELON) -- measured, must not drift silently."
    )
    for shops in constellations:
        assert len(shops) == MAX_SHOP_INSTANCES
        assert all(s in kg.SHOPS for s in shops)

    vectors = {drain_vector(shops) for shops in constellations}
    assert len(vectors) == 285, "representative constellations must be pairwise distinct"


def test_weeds_still_spawn_under_forced_shops():
    """Forcing shops must not silently also freeze weed spawning -- only the shop choice
    is overridden. weedSpawnChance=1.0 guarantees every empty tile weeds on day 1."""
    env = make(
        "kaggriculture",
        configuration={"seed": 5, "turnsPerDay": 1, "townShopUnlockInterval": 1,
                       "weedSpawnChance": 1.0},
        debug=False,
    )
    env.reset(2)
    with forced_shops(ALL_EIGHT):
        env.step([dict(NO_OP), dict(NO_OP)])
    tiles = env.state[0].observation.farms[0]["tiles"]
    flat = [t for row in tiles for t in row]
    weeds = [t for t in flat if isinstance(t, dict) and t.get("kind") == "WEED"]
    assert weeds, "weed spawning must be unaffected by forced_shops"
