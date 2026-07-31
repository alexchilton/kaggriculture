"""Parity tests for the batched market.

`CLAUDE.md` makes this a hard gate: **do not train on the fast sim until parity is exact.** A
divergent simulator makes every downstream result fiction, and the design doc predicted the market
settlement specifically would be where it breaks. So these tests come before the rest of the
simulator, not after.

Everything here compares against `kaggriculture` itself rather than against a remembered formula.
"""

import numpy as np
import pytest

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.sim.market import (
    I0,
    N_PRODUCTS,
    PRODUCTS,
    price,
    price_of,
    settle_sales,
)


@pytest.mark.parametrize("product", PRODUCTS)
def test_price_matches_the_reference_across_the_whole_curve(product):
    """Both sides of I0, the floor, and the extremes -- exactly, as integers.

    Rounding is the risk: the reference uses Python `round` (half to even) and this uses
    `np.rint` (also half to even). Asserting it here means a future change to either cannot
    silently drift.
    """
    i0 = kg.MARKET_PARAMS[product]["I0"]
    inventories = np.array(
        [0, 1, i0 - 5000, i0 - 400, i0 - 100, i0 - 1, i0, i0 + 1, i0 + 100,
         i0 + 400, i0 + 5000, i0 + 100_000],
        dtype=np.int64,
    )

    ours = price_of(product, inventories)
    theirs = [kg.market_price(product, int(inv)) for inv in inventories]

    assert list(ours) == theirs


def test_price_matches_the_reference_at_every_integer_near_the_kink():
    """Dense sweep either side of I0, where the branch changes and rounding is most fragile."""
    for product in PRODUCTS:
        i0 = kg.MARKET_PARAMS[product]["I0"]
        inventories = np.arange(i0 - 60, i0 + 60, dtype=np.int64)

        ours = price_of(product, inventories)
        theirs = [kg.market_price(product, int(inv)) for inv in inventories]

        assert list(ours) == theirs, product


def test_batched_price_over_all_products_at_once():
    """The [B, N_PRODUCTS] form must agree with the per-product form and with the reference."""
    rng = np.random.default_rng(0)
    grid = (I0 + rng.integers(-800, 800, size=(16, N_PRODUCTS))).astype(np.int64)

    ours = price(grid)

    assert ours.shape == (16, N_PRODUCTS)
    for j, product in enumerate(PRODUCTS):
        expected = [kg.market_price(product, int(inv)) for inv in grid[:, j]]
        assert list(ours[:, j]) == expected, product


def _reference_sale(product, inventory, qty, held):
    """What `_commit_unit` does for a single player's sell order, in plain Python."""
    money = 0
    for _ in range(qty):
        if held <= 0:
            break
        unit = kg.market_price(product, inventory)
        money += unit
        held -= 1
        if unit > kg.PRICE_FLOOR:
            inventory += 1
    return inventory, money, held


@pytest.mark.parametrize("product", ["WHEAT", "MELON", "STRAWBERRY"])
@pytest.mark.parametrize("qty", [1, 7, 60, 400])
def test_settlement_matches_a_unit_by_unit_reference_walk(product, qty):
    """A bulk sale walks the price down; it does not clear at one price."""
    start = int(kg.MARKET_PARAMS[product]["I0"])
    inv, money, held = settle_sales(
        product, np.array([start]), np.array([qty]), np.array([0.0]), np.array([qty])
    )
    exp_inv, exp_money, exp_held = _reference_sale(product, start, qty, qty)

    assert int(inv[0]) == exp_inv
    assert float(money[0]) == exp_money
    assert int(held[0]) == exp_held


def test_settlement_is_identical_across_a_batch_of_differing_games():
    """The point of the whole module: B games settle at once and each matches its own walk."""
    starts = np.array([9_000, 9_800, 10_000, 10_200, 12_000], dtype=np.int64)
    qtys = np.array([5, 40, 0, 120, 300], dtype=np.int64)

    inv, money, held = settle_sales(
        "MELON", starts, qtys, np.zeros(len(starts)), qtys.copy()
    )

    for k in range(len(starts)):
        e_inv, e_money, e_held = _reference_sale("MELON", int(starts[k]), int(qtys[k]), int(qtys[k]))
        assert int(inv[k]) == e_inv
        assert float(money[k]) == e_money
        assert int(held[k]) == e_held


def test_units_clearing_at_the_floor_pay_out_but_do_not_deepen_the_glut():
    """`_commit_unit`'s floor branch, which is why a crashed price recovers on drain alone."""
    crashed = np.array([kg.MARKET_PARAMS["MELON"]["I0"] + 200_000], dtype=np.int64)

    inv, money, _ = settle_sales("MELON", crashed, np.array([50]), np.array([0.0]), np.array([50]))

    assert int(inv[0]) == int(crashed[0])       # inventory unchanged
    assert float(money[0]) == 50 * kg.PRICE_FLOOR


def test_a_seller_with_nothing_held_sells_nothing():
    inv, money, held = settle_sales(
        "WHEAT", np.array([10_000]), np.array([25]), np.array([500.0]), np.array([0])
    )

    assert int(inv[0]) == 10_000
    assert float(money[0]) == 500.0
    assert int(held[0]) == 0


def _reference_market(orders, shed, money=0.0):
    """Run the real `kaggriculture._process_market` over hand-built state.

    Stronger evidence than a walk written from reading the source, which is how the same-price
    rule below came to be asserted backwards: the old version of this test claimed seat 0 got the
    better price on a contested unit, and the reference pays both seats the same.
    """
    from types import SimpleNamespace as NS

    inv = {item: kg.MARKET_PARAMS[item]["I0"] for item in kg.PRODUCTS}
    market = {"inventory": dict(inv), "prices": {}}
    farms = [{"money": float(money), "hands": [], "farmer": [4, 4],
              "tiles": [[None] * 10 for _ in range(10)],
              "unlocked_quadrants": ["NW"], "hires_today": 0} for _ in range(2)]
    state = [
        NS(observation=NS(market=market, farms=farms, player=p,
                          private={"shed": dict(shed[p]), "seeds": {}, "inventories": [{}]}),
           action={"market": orders[p]})
        for p in range(2)
    ]
    env = NS(configuration={"boardSize": 10, "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1})

    kg._process_market(state, env)
    return [farms[p]["money"] for p in range(2)], market["inventory"]


def test_two_players_selling_the_same_product_are_paid_the_same_price():
    """`_process_market` quotes BOTH seats against the same pre-commit inventory for each unit.

    Both quotes are taken before either commit lands, so on a contested unit the two seats are paid
    identically and the inventory rises by two. Re-quoting between the seats -- which is what this
    simulator did -- shortchanges seat 1 on every contested unit, and in real play both agents sell
    the same staples every turn, so 'contested' is the normal case rather than the exotic one.
    """
    expected, _ = _reference_market(
        [[["SELL", "MELON", 10]], [["SELL", "MELON", 10]]],
        [{"MELON": 10}, {"MELON": 10}],
    )
    assert expected[0] == expected[1]           # the rule being pinned, straight from the reference

    inv, money, held = settle_sales(
        "MELON",
        np.array([10_000], dtype=np.int64),
        np.array([[10, 10]]),
        np.array([[0.0, 0.0]]),
        np.array([[10, 10]]),
    )

    assert [float(money[0, 0]), float(money[0, 1])] == expected
    assert int(held[0, 0]) == 0 and int(held[0, 1]) == 0
    assert int(inv[0]) == 10_020


@pytest.mark.parametrize("product,qty", [("MELON", 10), ("WHEAT", 40), ("STRAWBERRY", 25)])
def test_the_game_loop_settles_a_contested_sale_exactly_like_the_reference(product, qty):
    """`Game._process_market` keeps its own copy of the settlement, so gate it separately.

    The end-to-end parity gate does not reach this. Its random scripts almost never have both
    players holding stock of the same product on the same turn, so 300 full-length episodes passed
    while this branch was wrong -- reverting the fix leaves the entire non-JAX suite green. That is
    the `CLAUDE.md` lesson about gates testing only what they exercise, landing a third time.
    """
    from kagg.sim.game import Actions, Game

    idx = PRODUCTS.index(product)
    game = Game(1, starting_money=0.0, weed_chance=0.0)
    for p in range(2):
        game.farms[p].shed[:, idx] = qty

    actions = Actions(1)
    actions.sell[:, :, idx] = qty
    game._process_market(actions)

    expected, inventory = _reference_market(
        [[["SELL", product, qty]], [["SELL", product, qty]]],
        [{product: qty}, {product: qty}],
    )

    assert [float(game.farms[p].money[0]) for p in range(2)] == expected
    assert int(game.inventory[0, idx]) == inventory[product]
    assert expected[0] == expected[1] > 0        # the case is contested, not vacuous
