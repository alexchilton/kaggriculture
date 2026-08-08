"""A book at the price floor must stop the offer, not open it wide.

Measured on episode 91122388 (`docs/we_oversell_into_a_contested_book_2026-08-09.md`): WOOL's book
reaches `d = 59` above `I0` on day 16 -- exactly where its curve `200 - 0.058*d^2` hits the floor --
and we then sell **another 140 units into it at $1 to $5 each**, all season, because the town drains
a few units and we refill them immediately. Selling 30% less lets the drain outrun our supply, the
book falls 51 -> 48 -> 39 -> 27 -> 16 -> 6, and the same goods realise $149/unit instead of $24.

`reservation_units` does the opposite by design. Its docstring argues that when supply exceeds the
town's remaining absorption the offer should WIDEN, "since there is no future in which that stock
clears at today's price". That is true about the stock and false about the money: a unit sold into a
floored book earns $1 and costs ~$150 on every unit sold after it, because it is what holds the book
at the floor.

The mechanism is one line. With the book floored, `market_price` returns `PRICE_FLOOR`, so
`floor_price` collapses to `(1 - slip) * PRICE_FLOOR` -- below the floor itself -- and the loop runs
to `supply`.
"""

import pytest

import kaggle_environments.envs.kaggriculture.kaggriculture as kg
from kagg.search import schedule_agent as SA

#: Day 16 of the measured episode: eight shops open, mid-season, plenty of drain still to come.
STEP = 16 * 24
SHOPS = ["FARMERS_MARKET", "BAKERY", "SMOOTHIE_SHOP", "PIZZA_SHOP",
         "YARN_STORE", "ICE_CREAM_SHOP", "PET_CAFE", "BRUNCH_SPOT"]


def floored_inventory(prod):
    """Lowest book level at which `prod` already quotes at the price floor."""
    i0 = kg.MARKET_PARAMS[prod]["I0"]
    d = 0
    while kg.market_price(prod, i0 + d) > kg.PRICE_FLOOR:
        d += 1
    return i0 + d


def test_the_wool_book_really_does_floor_where_the_replay_says_it_does():
    """Guards the premise: if the curve moves, the numbers below stop meaning anything."""
    i0 = kg.MARKET_PARAMS["WOOL"]["I0"]
    assert floored_inventory("WOOL") - i0 == pytest.approx(59, abs=2)


def recoverable_supply(prod):
    """A stock small enough that the town's remaining drain can still absorb it.

    Holding is only worth anything if the book can come back, and it comes back at `d_rem`. The
    rule guards on `d_rem >= supply` for that reason, so a test that holds more than the town can
    take is asserting the wrong contract -- which the first version of this file did.
    """
    return SA.town_drain_remaining(prod, STEP, SHOPS, 720)


@pytest.mark.parametrize("prod", ["WOOL", "MILK", "STRAWBERRY"])
def test_a_floored_book_does_not_take_the_whole_shed(prod):
    """Book already at the floor, stock the town could still absorb: do not offer all of it.

    The shipped behaviour the loss replays show is the opposite -- the offer is `supply`, in full,
    every turn, for the rest of the season.
    """
    supply = recoverable_supply(prod)
    n = SA.reservation_units(prod, floored_inventory(prod), STEP, SHOPS, supply)
    assert n < supply, (
        f"{prod}: the book is already at ${kg.PRICE_FLOOR} and the rule offered all {n} units. "
        "Every one of them earns the floor price and holds the book there, so the units sold "
        "after them earn the floor price too. Withholding is what lets the town's drain pull the "
        "book back under the crash point."
    )


def test_melon_is_deliberately_excluded_because_its_book_cannot_recover():
    """MELON must keep selling into a floored book, and that is not an oversight.

    No shop carries melon, so the town removes 30 units across a whole season while melon's curve
    crashes 158 units above `I0`. The price a hold waits for never arrives. Replaying this rule over
    24 real ladder losses without the `d_rem >= supply` guard: WOOL +$341,759, STRAWBERRY +$162,355,
    MILK +$153,871 and MELON **-$73,143** -- the stock stranded mid-season and the sales it refused
    were the profitable ones.
    """
    i0 = kg.MARKET_PARAMS["MELON"]["I0"]
    d_rem = SA.town_drain_remaining("MELON", STEP, SHOPS, 720)
    assert d_rem < floored_inventory("MELON") - i0, (
        "melon's remaining drain can now clear its own crash depth; the exclusion below is only "
        "correct while it cannot"
    )
    supply = 60
    assert SA.reservation_units("MELON", floored_inventory("MELON"), STEP, SHOPS, supply) == supply


@pytest.mark.parametrize("prod", ["WOOL", "MILK"])
def test_the_offer_shrinks_as_the_book_deepens(prod):
    """Monotonicity: a worse book must never produce a larger offer.

    The failure is not only at the floor. The whole approach to it is wrong -- the rule widens as
    the price falls -- so a book halfway to the floor must already be offering less than a healthy
    one. Measured before the fix, on a floored book: `MILK: 8 -> 5 -> 200`.
    """
    i0 = kg.MARKET_PARAMS[prod]["I0"]
    crash = floored_inventory(prod) - i0
    supply = recoverable_supply(prod)
    healthy = SA.reservation_units(prod, i0, STEP, SHOPS, supply)
    strained = SA.reservation_units(prod, i0 + crash // 2, STEP, SHOPS, supply)
    floored = SA.reservation_units(prod, i0 + crash, STEP, SHOPS, supply)
    assert healthy >= strained >= floored, (
        f"{prod}: offers went {healthy} -> {strained} -> {floored} as the book filled. "
        "The rule is opening up exactly as the price collapses."
    )
