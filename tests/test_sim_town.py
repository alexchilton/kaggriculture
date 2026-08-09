"""Parity tests for batched town consumption.

Checked against `kagg.economics.market`, whose drain model is itself verified exact against live
episodes for every product at every step -- so this is transitively gated on the real environment
rather than on a second reading of the same source.
"""

import numpy as np

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.economics.market import inventory_path, observe_unlocks, town_drain
from kagg.sim.market import I0, PRODUCTS, PRODUCT_INDEX
from kagg.sim.town import (
    N_SHOPS,
    SHOP_INDEX,
    center_multiplier,
    drain_at,
    season_drain_table,
)

SEED = 11


def _mask_for(unlocks, day):
    """Open shop *instances* per shop, not a set of which shops are open.

    A bool mask was correct until 1.32.6 and is not now: the town draws with replacement, so
    `observe_unlocks(11)` has YARN_STORE on days 12, 15 *and* 21, and each instance consumes
    independently. Collapsing them reported 3 WOOL a tick against the economics model's 5.
    """
    counts = np.zeros((1, N_SHOPS), dtype=np.int64)
    for unlock_day, shops in unlocks.items():
        if unlock_day <= day:
            for shop in ([shops] if isinstance(shops, str) else shops):
                counts[0, SHOP_INDEX[shop]] += 1
    return counts


def test_center_multiplier_matches_the_schedule():
    """Against the INSTALLED env's schedule, never against a remembered one.

    This test used to hard-code 1, 1, 2, 2, 4, 4 -- the ramp as it stood through 1.32.5. The
    "Kaggriculture town rebalance" (merged 2026-08-07, shipped in 1.32.6) deleted
    `TOWN_CENTER_DEMAND_SCHEDULE` outright and took `townCenterSellInterval` from 12 to 24, so
    late-season drawdown fell 8x: 4-units-twice-daily became 1-unit-once-daily.

    Hard-coding the old numbers would have turned a rule change into a test failure that reads like
    our bug, which is the wrong signal entirely. Assert the SHAPE the env declares -- monotonic,
    non-decreasing, starting at the day-0 value -- so a future rebalance is caught by
    `test_drain_matches_the_validated_economics_model_at_every_step` as a real divergence rather
    than by this one as a stale literal.
    """
    from kagg.sim.town import CENTER_SCHEDULE

    assert CENTER_SCHEDULE == sorted(CENTER_SCHEDULE), CENTER_SCHEDULE
    assert CENTER_SCHEDULE[0][0] == 0, f"no day-0 entry: {CENTER_SCHEDULE}"
    for threshold, mult in CENTER_SCHEDULE:
        assert int(center_multiplier(threshold)) == mult, (threshold, mult, CENTER_SCHEDULE)
        if threshold:
            assert int(center_multiplier(threshold - 1)) <= mult, (threshold, CENTER_SCHEDULE)
    assert int(center_multiplier(29)) == CENTER_SCHEDULE[-1][1]


def test_drain_matches_the_validated_economics_model_at_every_step():
    """Every step of a full season, every product, no tolerance."""
    unlocks = observe_unlocks(SEED)

    for step in range(719):
        mask = _mask_for(unlocks, step // 24)
        ours = drain_at(step, mask)[0]
        theirs = town_drain(step, unlocks)

        for product in PRODUCTS:
            assert ours[PRODUCT_INDEX[product]] == theirs[product], (
                f"step {step}, {product}: {ours[PRODUCT_INDEX[product]]} != {theirs[product]}"
            )


def test_season_table_reproduces_the_live_inventory_path():
    """Accumulating the table must land on the same inventory a live episode ends with."""
    unlocks = observe_unlocks(SEED)
    table = season_drain_table(unlocks)

    for product in PRODUCTS:
        expected_path, _ = inventory_path(product, unlocks)
        ours = I0[PRODUCT_INDEX[product]] - table[:, PRODUCT_INDEX[product]].cumsum()

        assert list(ours) == expected_path, product


def test_a_batch_of_different_unlock_schedules_drains_independently():
    """Different games unlock different shops, so each row must use its own mask."""
    only_bakery = np.zeros((3, N_SHOPS), dtype=bool)
    only_bakery[0, SHOP_INDEX["BAKERY"]] = True
    only_bakery[1, SHOP_INDEX["YARN_STORE"]] = True
    # Row 2 stays empty: no shops unlocked at all.

    drain = drain_at(4, only_bakery)   # a shop tick, not a centre tick

    assert drain[0, PRODUCT_INDEX["WHEAT"]] == 1 and drain[0, PRODUCT_INDEX["EGG"]] == 1
    # YARN_STORE sells only wool, so it pulls double.
    assert drain[1, PRODUCT_INDEX["WOOL"]] == 2
    assert drain[1, PRODUCT_INDEX["WHEAT"]] == 0
    assert drain[2].sum() == 0


def test_fertilizer_is_never_drained():
    """The town centre pulls every product except fertilizer, and no shop demands it."""
    unlocks = observe_unlocks(SEED)
    table = season_drain_table(unlocks)

    assert table[:, PRODUCT_INDEX["FERTILIZER"]].sum() == 0
