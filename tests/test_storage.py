"""Tests for the storage constraint, which bounds every sell-timing strategy.

The reason this file exists: an earlier version of `docs/economics_q5_findings.md` claimed a
1.75x gain from holding a whole quadrant's wheat harvest and selling it late.
That is impossible -- there is nowhere to put 700 units.
Storage is the constraint that decides whether *any* hold-and-sell-late plan is legal, so its
exact semantics are pinned here rather than reasoned about.

The overflow tests run with `shedCapacity` lowered to 10, because a $3000 start cannot buy its
way past the default 100 (each `BUY_PRODUCT` unit walks the price up, so the bank runs out at
about 95 wheat). The rule under test is capacity-parametric, so a small capacity exercises it
exactly; `test_default_shed_capacity_is_one_hundred` pins the real number separately.
"""

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as kg

SHED_CAP = 100
SMALL_CAP = 10
QTY = 20  # affordable, and comfortably over SMALL_CAP


def _run(agent, seed=5, **config):
    env = make("kaggriculture", configuration={"seed": seed, **config}, debug=False)
    env.run([agent, "pass"])
    return env


def _buy_then_pickup(qty):
    def agent(obs, cfg):
        if obs["step"] == 0:
            return {"market": [["BUY_PRODUCT", "WHEAT", qty]]}
        if obs["step"] == 1:
            return {"farmer": ["PICKUP", "WHEAT", qty]}
        return {}

    return agent


def test_default_shed_capacity_is_one_hundred():
    """The number every storage conclusion depends on."""
    env = make("kaggriculture", configuration={"seed": 5}, debug=False)

    assert int(env.configuration["shedCapacity"]) == SHED_CAP


def test_overnight_carry_is_capped_at_shed_capacity_and_the_excess_is_destroyed():
    """The binding constraint on holding product: capacity overnight, the rest ceases to exist.

    `_drop_inventories_to_shed` moves what fits and then `del inv[item]` unconditionally, so
    overflow is not left in inventory for tomorrow -- it is gone.
    """
    env = _run(_buy_then_pickup(QTY), shedCapacity=SMALL_CAP)

    # steps[2] is after step 1: everything picked up, shed emptied.
    assert env.steps[2][0]["observation"]["private"]["inventories"][0]["WHEAT"] == QTY
    assert env.steps[2][0]["observation"]["private"]["shed"]["WHEAT"] == 0

    # Day 0 ends after step 23, so steps[25] is the following morning.
    morning = env.steps[25][0]["observation"]["private"]
    assert morning["shed"]["WHEAT"] == SMALL_CAP
    assert sum(morning["inventories"][0].values()) == 0, "overflow must be destroyed, not held"


def test_carried_inventory_itself_has_no_cap_so_intraday_throughput_can_exceed_the_shed():
    """`_inv_add` never checks capacity, so a unit can hold arbitrarily much during a day.

    This is why the shed cap limits *overnight* storage rather than same-day selling: a large
    harvest can be dropped and sold in shed-sized instalments before nightfall, given the
    actions to do it.
    """
    env = _run(_buy_then_pickup(QTY), shedCapacity=SMALL_CAP)
    carried = env.steps[2][0]["observation"]["private"]["inventories"][0]

    assert carried["WHEAT"] == QTY > SMALL_CAP


def test_buying_product_bypasses_the_shed_cap_entirely():
    """`_commit_unit` BUY_PRODUCT writes straight to the shed with no capacity check.

    A genuine asymmetry: bought wheat stockpiles past capacity, harvested product cannot.
    Only WHEAT and FERTILIZER are buyable, so this is a wheat-and-fertilizer-only loophole.
    """
    def agent(obs, cfg):
        return {"market": [["BUY_PRODUCT", "WHEAT", QTY]]} if obs["step"] == 0 else {}

    env = _run(agent, shedCapacity=SMALL_CAP)

    assert env.steps[1][0]["observation"]["private"]["shed"]["WHEAT"] == QTY > SMALL_CAP
    # Nightfall does not trim an already-overfull shed; it only refuses to add more.
    assert env.steps[25][0]["observation"]["private"]["shed"]["WHEAT"] == QTY


def test_a_quadrant_of_wheat_cannot_be_stockpiled_for_a_late_dump():
    """The arithmetic that killed the original 1.75x claim.

    25 wheat tiles yield 28 units each over a season. Overnight storage is 100 items, so at
    most a seventh of that can ever be waiting to sell at the end.
    """
    from kagg.economics.production import TILE_YIELD_PER_SEASON

    season_output = TILE_YIELD_PER_SEASON["WHEAT"] * 25

    assert season_output == 700
    assert SHED_CAP / season_output < 0.15


def test_ongoing_crop_tiles_are_short_term_storage_only():
    """The "tile is the warehouse" idea has a hard limit: `max_yield` units, then decay.

    Once an ongoing crop has produced `max_yield`, `_daily_refresh_plants` sets
    `max_lifespan_step` and `_decay_plants` then removes a unit every other turn. A tile holds
    at most 4 units, for about a day -- nowhere near enough to bank a season.
    """
    cd = kg.CROPS["STRAWBERRY"]

    assert cd["ongoing"] and cd["max_yield"] == 4
    assert cd["max_yield"] < SHED_CAP
