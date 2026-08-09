"""The four rules `kaggle-environments` 1.32.6 changed, one test each.

Parity was established against 1.32.2 and the ladder moved to 1.32.6 on 2026-08-08. Diffing the two
env sources gives an exact, closed list of behavioural changes -- everything else in the diff is
comments. Each one below is first *measured* against the installed environment, then asserted
against both simulators, because CLAUDE.md's rule is that a theory without a failing test is a guess.

The changes, in the order they appear in `_apply_unit_action` / `_commit_unit` / `_end_of_day`:

1. **Movement onto a LOCKED tile is allowed.** 1.32.2 returned early. The stated reason is that a
   hand can spawn on a locked shed-access tile and blocking movement would strand it there forever.
2. **Shed operations resolve before the LOCKED guard.** DROP, PICKUP and PLACE use the tile only as
   a standing position, and three of the four shed-access tiles start LOCKED. Tile operations
   (PLANT, WATER, DIG, ...) still no-op on LOCKED, so the guard did not go away -- it moved.
3. **BUY_PRODUCT and BUY_ANIMAL respect `shedCapacity`.** Bought goods land in the shed, which
   obeys the cap like every other deposit path. 1.32.2 let them overfill it.
4. **Shops unlock with replacement, capped at `MAX_SHOP_INSTANCES` total.** 1.32.2 drew from the
   shops *not yet* unlocked, so all eight were distinct. Each instance now consumes independently,
   so the same shop twice is double demand for its products.

The fourth is the one that cannot be waved through as an edge case: with eight instances drawn from
eight shops, all-distinct has probability 8!/8^8 = 0.24%, so a duplicate is the norm rather than the
exception, and a simulator holding `unlocked_shops` as a set of booleans under-drains every game.

Not in this file, because it is not a simulator bug: `tests/test_tape_parity.py` replays episode
89873723, whose own recorded configuration says `module_version 1.32.3` and
`townCenterSellInterval 12`. See `docs/parity_restored_on_1326_2026-08-09.md`.
"""

import numpy as np
import pytest

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.sim import ops as O
from kagg.sim.game import Actions, Game
from kagg.sim.market import ITEM_INDEX, PRODUCT_INDEX
from kagg.sim.town import SHOP_INDEX

NOOP_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}


def _env(**config):
    from kaggle_environments import make

    settings = {"seed": 1, "weedSpawnChance": 0.0}
    settings.update(config)
    env = make("kaggriculture", configuration=settings, debug=True)
    env.reset(num_agents=2)
    return env


# ---- 1. movement onto a LOCKED tile ------------------------------------------------------------


def test_a_unit_may_walk_onto_a_locked_tile():
    """The farmer spawns on (4,4); (5,4) is the NE quadrant's shed-access tile and starts LOCKED."""
    env = _env()
    env.step([{"farmer": ["EAST"], "hands": [], "market": []}, NOOP_ACTION])
    reference = list(env.state[0].observation["farms"][0]["farmer"])
    assert reference == [5, 4], "the installed env no longer allows the move this test is about"

    game = Game(1, weed_chance=0.0)
    actions = Actions(1)
    actions.unit_op[0, 0, 0] = O.EAST
    game.step(actions)
    ours = [int(v) for v in game.farms[0].unit_pos[0, 0]]

    assert ours == reference, (
        f"our farmer stopped at {ours} where the env walked to {reference}: "
        f"1.32.6 dropped the LOCKED guard on movement")


# ---- 2. shed operations from a LOCKED shed-access tile ------------------------------------------


def test_pickup_works_while_standing_on_a_locked_shed_access_tile():
    """BUY_ANIMAL banks a cow, the farmer steps onto the locked (5,4), and PICKUP still reaches it."""
    env = _env()
    env.step([{"farmer": ["EAST"], "hands": [], "market": [["BUY_ANIMAL", "COW", 1]]}, NOOP_ACTION])
    env.step([{"farmer": ["PICKUP", "COW", 1], "hands": [], "market": []}, NOOP_ACTION])
    private = env.state[0].observation.private
    reference_shed = {k: int(v) for k, v in private["shed"].items() if v}
    reference_carried = {k: int(v) for k, v in (private["inventories"][0] or {}).items() if v}
    assert reference_carried == {"COW": 1}, "the installed env no longer allows the pickup"

    game = Game(1, weed_chance=0.0)
    cow = ITEM_INDEX["COW"]

    move = Actions(1)
    move.unit_op[0, 0, 0] = O.EAST
    move.buy_animal[0, 0, list(kg.ANIMALS).index("COW")] = 1
    game.step(move)

    grab = Actions(1)
    grab.unit_op[0, 0, 0] = O.PICKUP
    grab.unit_item[0, 0, 0] = cow
    grab.unit_qty[0, 0, 0] = 1
    game.step(grab)

    ours_shed = {k: int(v) for k, v in zip(
        [n for n in kg.PRODUCTS] + list(kg.ANIMALS), game.farms[0].shed[0]) if v}
    ours_carried = int(game.farms[0].carried[0, 0, cow])

    assert (ours_carried, ours_shed) == (1, reference_shed), (
        f"we carried {ours_carried} and held shed {ours_shed} against the env's "
        f"{reference_carried} / {reference_shed}: 1.32.6 resolves shed ops before the LOCKED guard")


# ---- 3. shedCapacity bounds BUY_PRODUCT and BUY_ANIMAL ------------------------------------------


def test_buying_stops_at_shed_capacity():
    """One BUY_PRODUCT order for 150 wheat, with money to spare. The shed holds 100."""
    env = _env(startingMoney=100_000)
    env.step([{"farmer": ["PASS"], "hands": [], "market": [["BUY_PRODUCT", "WHEAT", 150]]},
              NOOP_ACTION])
    reference = sum(int(v) for v in env.state[0].observation.private["shed"].values())
    assert reference == 100, "the installed env no longer caps the shed at 100"

    game = Game(1, starting_money=100_000.0, weed_chance=0.0)
    actions = Actions(1)
    actions.buy_product[0, 0, PRODUCT_INDEX["WHEAT"]] = 150
    game.step(actions)
    ours = int(game.farms[0].shed[0].sum())

    assert ours == reference, (
        f"we banked {ours} items against the env's {reference}: 1.32.6 refuses BUY_PRODUCT and "
        f"BUY_ANIMAL once the shed is full")


# ---- 4. shops unlock with replacement, and each instance drains ---------------------------------


def test_the_same_shop_unlocking_twice_drains_twice():
    """`unlocked_shops` is a list, not a set. YARN_STORE twice is 4 WOOL a tick, not 2.

    YARN_STORE is the clean probe: it is single-product, so it pulls 2x WOOL and nothing else, and
    no other shop touches WOOL. A simulator holding unlocks as booleans reports half the drain.
    """
    wool = PRODUCT_INDEX["WOOL"]
    yarn = SHOP_INDEX["YARN_STORE"]
    assert kg.SHOPS["YARN_STORE"] == ["WOOL"], "YARN_STORE is no longer the single-product probe"

    once = Game(1, weed_chance=0.0, unlock_schedule={0: [yarn]})
    twice = Game(1, weed_chance=0.0, unlock_schedule={0: [yarn, yarn]})
    start = int(once.inventory[0, wool])

    # Four steps covers exactly one shop tick and one centre tick, both on step 0. So one
    # YARN_STORE is 2 (single-product, doubled) + 1 (the centre) = 3, and a second instance adds
    # 2 more. Anything that reads unlocks as a set reports 3 for both.
    for _ in range(4):
        once.step(Actions(1))
        twice.step(Actions(1))

    drained_once = start - int(once.inventory[0, wool])
    drained_twice = start - int(twice.inventory[0, wool])

    assert drained_once == 3, f"one YARN_STORE drained {drained_once} WOOL, expected 2 + 1 centre"
    assert drained_twice == 5, (
        f"two YARN_STORE instances drained {drained_twice} WOOL, not 5: "
        f"1.32.6 draws shops with replacement and each instance consumes independently")


def test_the_reference_really_does_unlock_the_same_shop_twice():
    """Pins the premise of the test above, so nobody dismisses duplicates as a contrived case.

    Replays the env's own unlock draw for the seeds the parity gate uses. All of them duplicate.
    """
    import random

    for seed in (700, 701, 800, 1500, 1501, 1502):
        shops = []
        for day in range(30):
            rng = random.Random((seed * 1_000_003) ^ day)
            if (day + 1) % 3 == 0 and len(shops) < kg.MAX_SHOP_INSTANCES:
                shops.append(rng.choice(sorted(kg.SHOPS)))
        assert len(shops) > len(set(shops)), (
            f"seed {seed} drew {shops}, all distinct -- if that is now typical this test is "
            f"obsolete rather than passing")
