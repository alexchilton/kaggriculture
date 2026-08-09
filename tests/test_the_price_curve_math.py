"""Verify the market arithmetic every decision today rests on, against the env's own function.

`docs/the_book_is_shallow_2026-08-09.md` turns the whole market analysis on one inverted formula:
the surplus above `I0` at which each product reaches the `$1` floor -- WOOL 59, STRAWBERRY 63,
MILK 76, MELON 158, with WHEAT and EGG effectively unfloodable. Those numbers drove the conclusion
that production, not selling, is the binding constraint, and they were derived on paper.

`market_price` (`reference/kaggriculture.py:179`) is:

    price = base - (above_target * base / shape(above_func, T)) * shape(above_func, inventory - I0)

inverted here per shape. A sign slip or a mixed-up `T` would not crash anything -- it would quietly
produce a plausible table and send a week of work at the wrong problem. So check the inversion
against the function itself rather than against the algebra a second time.
"""
import math
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "reference"))
import kaggriculture as kg  # noqa: E402

HI = ("WOOL", "STRAWBERRY", "MILK", "MELON")
#: The table asserted in the doc, and used to argue melon is over-produced on every board.
PUBLISHED = {"WOOL": 59, "STRAWBERRY": 62, "MILK": 76, "MELON": 158}


def units_to_floor(item):
    """Invert `market_price` for the surplus above I0 that reaches PRICE_FLOOR."""
    p = kg.MARKET_PARAMS[item]
    amp = p["above_target"] * p["base"] / kg._shape(p["above_func"], p["T"])
    y = (p["base"] - kg.PRICE_FLOOR) / amp        # = shape(above_func, x)
    f = p["above_func"]
    if f == "linear":
        return y
    if f == "sq":
        return math.sqrt(y)
    if f == "sqrt":
        return y * y
    if f == "log":
        return math.exp(min(y, 700.0)) - 1.0      # clamp: EGG/WHEAT overflow a float otherwise
    raise AssertionError(f"unhandled above_func {f}")


@pytest.mark.parametrize("item", HI)
def test_the_inverted_formula_agrees_with_market_price(item):
    """At the derived surplus the price is the floor; one unit earlier it is not."""
    x = units_to_floor(item)
    at = kg.market_price(item, kg.MARKET_I0 + math.ceil(x), None)
    before = kg.market_price(item, kg.MARKET_I0 + max(0, math.floor(x) - 1), None)

    assert at == kg.PRICE_FLOOR, (
        f"{item}: the inversion says {x:.1f} units above I0 reaches the floor, but "
        f"market_price there is ${at}, not ${kg.PRICE_FLOOR}"
    )
    assert before > kg.PRICE_FLOOR, (
        f"{item}: the price is already at the floor {x:.1f}-1 units above I0, so the derived "
        f"figure is too LARGE and every 'units we can sell' number built on it is wrong"
    )


@pytest.mark.parametrize("item,published", sorted(PUBLISHED.items()))
def test_the_published_table_is_still_what_the_env_says(item, published):
    """Guard the doc itself: these four numbers are quoted as settled facts across the project."""
    x = units_to_floor(item)
    assert abs(x - published) <= 1.0, (
        f"{item}: docs/the_book_is_shallow_2026-08-09.md publishes {published} units to the floor, "
        f"the env now gives {x:.1f}. Either MARKET_PARAMS changed or the doc is wrong -- fix "
        f"whichever, but they must not disagree."
    )


@pytest.mark.parametrize("item", ("WHEAT", "EGG"))
def test_wheat_and_egg_really_are_unfloodable(item):
    """Both use `log`, which is why volume there behaves nothing like the premium products.

    This is load-bearing twice over: it is why the wheat feed churn is not the cost it appears to
    be, and why the goose's revenue is robust while the cow's is not.
    """
    assert kg.MARKET_PARAMS[item]["above_func"] == "log"
    # A whole season of production dumped at once barely moves either book.
    assert kg.market_price(item, kg.MARKET_I0 + 1000, None) > kg.MARKET_PARAMS[item]["base"] * 0.4


@pytest.mark.parametrize("item", HI + ("WHEAT", "EGG"))
def test_price_is_monotone_decreasing_in_inventory(item):
    """The reservation logic assumes this; without it, 'sell before the price falls' is meaningless."""
    prices = [kg.market_price(item, kg.MARKET_I0 + x, None) for x in range(0, 400, 7)]
    assert all(a >= b for a, b in zip(prices, prices[1:])), f"{item} is not monotone above I0"
    below = [kg.market_price(item, kg.MARKET_I0 - x, None) for x in range(0, 400, 7)]
    assert all(a <= b for a, b in zip(below, below[1:])), f"{item} is not monotone below I0"


def test_price_equals_base_exactly_at_I0():
    """`PRICE_AWARE_SELL_CAP` gates on `price >= base`, which is only a proxy for `inventory <= I0`
    if the two coincide exactly. The whole `DEPTH_RULE_BELOW_BASE` analysis assumed they do."""
    for item in kg.PRODUCTS:
        assert kg.market_price(item, kg.MARKET_I0, None) == kg.MARKET_PARAMS[item]["base"], item


def test_melon_has_no_shop_and_egg_and_wool_have_the_ones_we_think():
    """The production argument rests on these counts; a shop table edit must break this test."""
    sells = {p: sorted(s for s, prods in kg.SHOPS.items() if p in prods) for p in kg.PRODUCTS}
    assert sells["MELON"] == [], f"MELON now has shops: {sells['MELON']}"
    assert sells["WOOL"] == ["YARN_STORE"], sells["WOOL"]
    assert len(sells["MILK"]) == 3, sells["MILK"]
    assert len(sells["EGG"]) == 2, sells["EGG"]
    assert len(kg.SHOPS) == 8 and kg.MAX_SHOP_INSTANCES == 8
