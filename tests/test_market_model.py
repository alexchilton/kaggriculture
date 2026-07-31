"""Tests for the offline market model.

The model exists so that pricing questions can be answered by arithmetic instead of by
simulation, which only works if the arithmetic is provably the same arithmetic the
environment does.
Hence the parity tests: they compare the model's inventory path against a live episode
step for step, and they are the reason any conclusion drawn from this module is
trustworthy.
"""

import pytest

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.economics.market import (
    BASE,
    I0,
    PRODUCTS,
    absorption,
    drain_per_day,
    inventory_path,
    observe_unlocks,
    price,
    sell_revenue,
)

SEEDS = [11, 23, 42]


@pytest.fixture(scope="module")
def episodes():
    """One `pass` vs `pass` episode per seed: unlock schedule plus recorded inventories.

    Both players idle, so every inventory change is town drain and the model has nothing
    to explain away.
    """
    from kaggle_environments import make

    out = {}
    for seed in SEEDS:
        env = make("kaggriculture", configuration={"seed": seed}, debug=False)
        env.run(["pass", "pass"])

        unlocks = {}
        for step in env.steps:
            obs = step[0]["observation"]
            for shop in obs.get("town", {}).get("unlocked_shops", []):
                unlocks.setdefault(shop, obs.get("day", 0))

        inventories = [s[0]["observation"]["market"]["inventory"] for s in env.steps]
        out[seed] = ({day: shop for shop, day in unlocks.items()}, inventories)
    return out


@pytest.mark.parametrize("seed", SEEDS)
def test_drain_model_reproduces_live_inventory_exactly(seed, episodes):
    """The whole module rests on this: every product, every step, no tolerance.

    If this fails, the drain model is wrong and every number derived from it is fiction.
    """
    unlocks, inventories = episodes[seed]
    recorded_steps = len(inventories) - 1

    for item in PRODUCTS:
        modelled, _ = inventory_path(item, unlocks, steps=recorded_steps)
        expected = [inv[item] for inv in inventories[1:]]

        assert modelled == expected, f"{item} diverges from the live episode on seed {seed}"


def test_observe_unlocks_matches_the_schedule_read_from_a_live_episode(episodes):
    unlocks, _ = episodes[SEEDS[0]]

    assert observe_unlocks(SEEDS[0]) == unlocks


def test_unlocks_land_every_third_day_until_all_eight_shops_are_open(episodes):
    unlocks, _ = episodes[SEEDS[0]]

    assert sorted(unlocks) == [3, 6, 9, 12, 15, 18, 21, 24]
    assert set(unlocks.values()) == set(kg.SHOPS)


def test_unlock_order_is_not_a_pure_function_of_the_seed():
    """Documents the trap: the unlock draw shares an RNG with weed spawning.

    `_spawn_weeds` consumes one draw per empty unlocked tile before `rng.choice` runs, so
    an opponent who plants differently shifts which shop opens. Anything that tries to
    predict the unlock order offline from the seed alone is wrong.
    """
    idle = observe_unlocks(7, "pass", "pass")
    farming = observe_unlocks(7, "starter", "starter")

    assert idle != farming


def test_price_falls_as_inventory_rises_and_is_floored_at_one():
    assert price("STRAWBERRY", I0["STRAWBERRY"]) == BASE["STRAWBERRY"]
    assert price("STRAWBERRY", I0["STRAWBERRY"] + 50) < BASE["STRAWBERRY"]
    assert price("STRAWBERRY", I0["STRAWBERRY"] + 100_000) == kg.PRICE_FLOOR


def test_scarcity_lifts_price_above_base():
    """The premium-timing thesis needs this to be true, so it is asserted rather than assumed."""
    assert price("STRAWBERRY", I0["STRAWBERRY"] - 100) > BASE["STRAWBERRY"]


def test_bulk_sale_walks_the_price_down_rather_than_clearing_at_one_price():
    """A naive `qty * price` revenue estimate overstates a bulk premium sale."""
    inventory = I0["STRAWBERRY"]
    revenue, _, unit_prices = sell_revenue("STRAWBERRY", inventory, 40)

    assert unit_prices[0] > unit_prices[-1]
    assert revenue < 40 * price("STRAWBERRY", inventory)


def test_units_sold_at_the_floor_do_not_deepen_the_glut():
    """Confirms `_commit_unit`'s "sales at $1 do not increase market supply" branch.

    This is why a crashed price recovers on town drain alone, and it bounds how much
    damage a price attack can do.
    """
    crashed = I0["STRAWBERRY"] + 100_000
    _, after, unit_prices = sell_revenue("STRAWBERRY", crashed, 500)

    assert set(unit_prices) == {kg.PRICE_FLOOR}
    assert after == crashed


def test_sell_revenue_matches_a_live_bulk_sale_of_wheat():
    """End-to-end check of the sell integral against the environment itself.

    Wheat is the only product buyable from the market, so it is the only one a probe can
    trade without farming. `market_price` and `_commit_unit` are shared by every product,
    so validating wheat validates the code path for all of them.
    """
    from kaggle_environments import make

    qty = 30

    def probe(obs, cfg):
        if obs["step"] == 0:
            return {"market": [["BUY_PRODUCT", "WHEAT", qty]]}
        if obs["step"] == 1:
            return {"market": [["SELL", "WHEAT", qty]]}
        return {}

    env = make("kaggriculture", configuration={"seed": 5}, debug=False)
    env.run([probe, "pass"])

    # steps[1] records the state after step 0 (the buy), steps[2] after step 1 (the sell).
    before = env.steps[1][0]["observation"]["market"]["inventory"]["WHEAT"]
    money_before = env.steps[1][0]["observation"]["farms"][0]["money"]
    money_after = env.steps[2][0]["observation"]["farms"][0]["money"]

    expected, _, _ = sell_revenue("WHEAT", before, qty)

    assert money_after - money_before == expected


def test_absorption_is_deep_for_wheat_and_shallow_for_melon():
    """The glut-tolerance split the strategy turns on, stated as a test."""
    wheat = absorption("WHEAT", I0["WHEAT"], floor_frac=0.8)
    melon = absorption("MELON", I0["MELON"], floor_frac=0.8)

    assert wheat > 10 * melon


def test_town_drain_accelerates_over_the_season(episodes):
    """Late demand must exceed early demand, or premium timing has nothing to exploit."""
    unlocks, _ = episodes[SEEDS[0]]
    per_day = drain_per_day(unlocks)["STRAWBERRY"]

    assert sum(per_day[25:30]) > 4 * sum(per_day[0:5])
