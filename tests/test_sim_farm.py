"""Parity tests for batched farm bookkeeping."""

import numpy as np

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.sim.farm import (
    HIRE_COST,
    LAND_PRICES,
    MAX_UNITS,
    N_LAND,
    SHED_CAP,
    FarmState,
    buy_land,
    buy_seeds,
    drop_to_shed,
    end_of_day,
    hire,
)
from kagg.sim.market import N_PRODUCTS, PRODUCT_INDEX
from kagg.sim.tiles import CROP_INDEX, EMPTY, LOCKED, TileState


def test_hire_costs_match_the_reference_fibonacci():
    """The cost curve that made 14 hands ruinous: it resets daily and is paid 30 times."""
    for n in range(MAX_UNITS):
        assert HIRE_COST[n] == kg._hire_cost(n), f"hire {n}"

    # The steepness is the point: hires 13 and 14 alone cost more than the first eight combined.
    assert HIRE_COST[:8].sum() < HIRE_COST[12] + HIRE_COST[13]


def test_hiring_stops_when_money_runs_out():
    state = FarmState(3, starting_money=10.0)
    got = []
    for _ in range(8):
        got.append(hire(state, np.array([True, True, True])).copy())

    # 1+1+2+3+5 = 12 > 10, so the fifth hire is unaffordable.
    assert state.n_units[0] == 5
    assert state.money[0] == 10.0 - (1 + 1 + 2 + 3)


def test_hiring_matches_the_reference_bank_exactly():
    state = FarmState(1, starting_money=3000.0)
    farm = kg._new_farm(10, 3000)
    private = kg._new_private()

    for _ in range(12):
        hire(state, np.array([True]))
        kg._do_hire(farm, private, 10)

    assert state.money[0] == farm["money"]
    assert state.n_units[0] == 1 + len(farm["hands"])


def test_buy_land_unlocks_quadrants_in_the_reference_order_and_price():
    state = FarmState(1, starting_money=10_000.0)
    tiles = TileState(1)
    # Everything outside NW starts locked.
    for t in range(100):
        x, y = t % 10, t // 10
        if not (x < 5 and y < 5):
            tiles.kind[0, t] = LOCKED

    farm = kg._new_farm(10, 10_000)
    for _ in range(N_LAND + 1):
        buy_land(state, tiles, np.array([True]))
        kg._do_buy_land(farm, 10)

    assert state.money[0] == farm["money"]
    assert state.n_land[0] == N_LAND
    reference_unlocked = sum(
        1 for row in farm["tiles"] for cell in row if cell != "LOCKED"
    )
    assert int((tiles.kind != LOCKED).sum()) == reference_unlocked == 100


def test_buy_land_is_refused_without_the_money():
    state = FarmState(1, starting_money=500.0)
    tiles = TileState(1)
    tiles.kind[0, :] = LOCKED

    buy_land(state, tiles, np.array([True]))

    assert state.n_land[0] == 0
    assert state.money[0] == 500.0


def test_buy_seeds_respects_the_bank():
    state = FarmState(2, starting_money=100.0)
    wheat = CROP_INDEX["WHEAT"]     # $10 each

    bought = buy_seeds(state, wheat, np.array([25, 3]))

    assert list(bought) == [10, 3]
    assert state.seeds[0, wheat] == 10 and state.money[0] == 0.0
    assert state.seeds[1, wheat] == 3 and state.money[1] == 70.0


def test_shed_overflow_is_destroyed_not_retained():
    """The constraint that bounds every hold-and-sell-late plan."""
    state = FarmState(1)
    state.carried[0, 0, PRODUCT_INDEX["WHEAT"]] = 150

    drop_to_shed(state)

    assert state.shed[0, PRODUCT_INDEX["WHEAT"]] == SHED_CAP
    assert state.carried[0, 0, PRODUCT_INDEX["WHEAT"]] == 0     # the other 50 are gone


def test_shed_cap_is_total_across_products_not_per_product():
    state = FarmState(1)
    state.carried[0, 0, PRODUCT_INDEX["WHEAT"]] = 80
    state.carried[0, 1, PRODUCT_INDEX["MELON"]] = 80

    drop_to_shed(state)

    assert state.shed[0].sum() == SHED_CAP
    assert state.shed[0, PRODUCT_INDEX["WHEAT"]] == 80
    assert state.shed[0, PRODUCT_INDEX["MELON"]] == 20


def test_drop_matches_the_reference_when_the_cap_binds():
    """Fill order matters once the shed is full, so it must walk units the same way."""
    state = FarmState(1)
    private = kg._new_private()
    for unit, (item, n) in enumerate([("WHEAT", 60), ("MELON", 70)]):
        state.carried[0, unit, PRODUCT_INDEX[item]] = n
        if unit >= len(private["inventories"]):
            private["inventories"].append({})
        private["inventories"][unit][item] = n

    drop_to_shed(state)
    kg._drop_inventories_to_shed(private, SHED_CAP)

    for product, idx in PRODUCT_INDEX.items():
        assert state.shed[0, idx] == private["shed"].get(product, 0), product


def test_end_of_day_dismisses_hands_and_resets_the_hire_counter():
    state = FarmState(1, starting_money=3000.0)
    for _ in range(6):
        hire(state, np.array([True]))
    state.carried[0, 0, PRODUCT_INDEX["WHEAT"]] = 5

    end_of_day(state)

    assert state.n_units[0] == 1
    assert state.hires_today[0] == 0
    assert state.shed[0, PRODUCT_INDEX["WHEAT"]] == 5
    assert state.carried.sum() == 0


def test_hiring_is_cheap_at_eight_and_ruinous_at_fourteen():
    """The measured claim in CLAUDE.md, asserted so it cannot rot."""
    season = 30
    assert HIRE_COST[:8].sum() * season < 2_000
    assert HIRE_COST[:14].sum() * season > 25_000
