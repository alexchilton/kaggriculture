"""19 pens, 15 wheat, and four animals unfed a day -- with 424 spare unit-turns on the field.

Measured on Seb's tape, seed 11, weeds off, seat 0 (`data/logs/why_animal_dies.log`). The FEED ops
that actually land track the WHEAT IN THE SHED almost exactly, never the pen count:

    day   pens   shed WHEAT   FEED ops landed
     16     18           18                14
     19     19           18                17
     22     19           15                15      <- an animal is gone by dawn on day 23
     25     18           19                19

So this was never a routing failure. `scripts/breakdown.py --tape seb --seed 11 --weeds 0.0` puts
`idle` at **+424 unit-turns** against the tape over the season and `work` at +192: we have hundreds of
spare turns and do more work than he does. What we do not have is wheat -- `buy_product` runs **-130**
against him for the season and `sh:wheat` -23.

The suspect is the order list. `maxMarketOrdersPerTurn` is 10 and the reference TRUNCATES the list
before parsing it, so this file guards every append with `len(orders) < 9`. The sell block runs
first and late season we hold many products at once, so on a turn with nine sells pending the feed
order is simply never appended -- silently, and only from the day the shed gets crowded, which is
exactly the day the feeds start falling short.

That is a theory about a mechanism, so it gets a test that fails before the fix and passes after.
`test_hire_survives_the_ten_order_market_cap` in `test_router.py` is the same shape for HIRE and was
written when this bit us the first time; feeding the herd has a better claim on a slot than any of
them.
"""
import collections

import pytest

from kagg.search import routines as R
from kagg.search import schedule_agent as SA

TPD = R.TURNS_PER_DAY
PRODUCTS = ["MELON", "WOOL", "MILK", "STRAWBERRY", "FERTILIZER", "EGG", "TOMATO", "CARROT"]


def _board(pens=19):
    """A 10x10 board, all four quadrants, `pens` hungry animals on it."""
    tiles = [[None for _ in range(10)] for _ in range(10)]
    placed = 0
    for y in range(10):
        for x in range(10):
            if placed >= pens or (x, y) in {(4, 4), (5, 4), (4, 5), (5, 5)}:
                continue
            tiles[y][x] = dict(kind="PASTURE", animal="COW", placed_day=0, fed_today=False,
                               cared_today=False, consecutive_unfed=1, yield_units=0,
                               fertilizer_available=False, pending_care_bonus=0)
            placed += 1
    return tiles


def _sched(days=30, **row):
    base = dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                seeds={}, buys={}, sells={}, hands=0)
    return {d: dict(base, **row) for d in range(days)}


def _day(sells, shed, pens=19, money=100_000, day=22):
    """Run one whole day and return every market order the agent emitted, by turn."""
    sched = _sched(sells=sells)
    agent = SA.make_agent(sched, 0, router=True)
    tiles = _board(pens)
    farm = {"tiles": tiles, "money": money, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW", "NE", "SW", "SE"]}
    priv = {"shed": dict(shed), "seeds": {}, "inventories": [{}]}
    market = {"prices": {p: 60 for p in SA.RT.BASE_PRICE}, "inventory": {p: 10_000 for p in SA.RT.BASE_PRICE}}
    out = []
    for hour in range(TPD):
        act = agent({"day": day, "hour": hour, "farms": [farm], "private": priv,
                     "market": market, "step": day * TPD + hour})
        out.append(list(act["market"] or []))
    return out


def test_a_full_sell_list_does_not_crowd_out_the_herds_feed():
    """Nine products to sell and nineteen hungry animals: the wheat order must still go out.

    This is the whole defect, as one day. The shed is stocked with every product the season produces,
    which is what a day-22 shed actually looks like, and the sell row asks for all of them.
    """
    shed = {p: 40 for p in PRODUCTS}
    shed["WHEAT"] = 0                       # nothing to feed 19 hungry animals with
    orders = _day(sells={p: 99 for p in PRODUCTS}, shed=shed)

    wheat = sum(o[2] for turn in orders for o in turn
                if o[:2] == ["BUY_PRODUCT", "WHEAT"])
    biggest = max(len(t) for t in orders)
    assert wheat >= 19, (
        f"nineteen hungry animals, an empty wheat shed and a $100,000 bank, and the day ordered "
        f"{wheat} wheat. Longest order list was {biggest} of the 10 the env accepts; the feed buy is "
        f"appended under `len(orders) < 9` and the sell block runs first, so on a crowded turn it is "
        f"dropped without a word. Turn 0 emitted: {orders[0]}")


def test_the_same_day_with_an_empty_shed_orders_the_feed_fine():
    """The control. With nothing to sell there is no competition for slots and the order goes out.

    Without this the test above could be failing for any reason at all -- no bank, no animals, a
    guard somewhere else -- and would not implicate the order list specifically.
    """
    orders = _day(sells={}, shed={"WHEAT": 0})
    wheat = sum(o[2] for turn in orders for o in turn if o[:2] == ["BUY_PRODUCT", "WHEAT"])
    assert wheat >= 19, (
        f"only {wheat} wheat ordered for nineteen hungry animals with an EMPTY order list, so the "
        f"shortfall is not the ten-order cap and this whole diagnosis is wrong: {orders[0]}")
