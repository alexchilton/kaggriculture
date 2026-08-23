"""A WOOL sell offers whatever is in the shed. Nothing else changes.

Ladder game 97495667, lost by $1,991 while holding **38 WOOL at a price of 223** (~$8,474). The
tape's WOOL cadence is sized for the 4 sheep it recorded; `_herd_split` runs 6 when the town draws
a YARN_STORE, so the produce outruns the offers and the surplus is still in the shed at the bell,
where it is worth nothing.

The book takes whatever we send it -- same game, price against volume offered:

    day  WOOLprc  shed  offered
     13     227      8        8
     19     231     21       20
     28     227     44        8
     29     229     40        8

227-234 all season regardless, while MILK fell 185 -> 1 over the same days. So an unfilled wool
offer costs nothing and there is no price to protect.

**This file used to test a general herd-ratio scaler that also throttled MILK.** That shipped and
the pool gate measured it: roughly half the money against every opponent, including ones with no
animals in play, because it compared `state["bought"]` -- a RUNNING count -- against the tape's
whole-SEASON total. The wool half was correct (12 of 12 seasons ended with an empty shed), so the
milk half is deleted and these tests shrank to match.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent as SA                       # noqa: E402


def test_wool_offers_the_whole_shed():
    assert SA.sell_all_the_wool(["SELL", "WOOL", 4], {"WOOL": 38}) == ["SELL", "WOOL", 38]


def test_wool_is_never_reduced_below_the_tapes_own_cadence():
    """Only ever puts MORE on the book. A thin shed must not shrink the tape's order."""
    order = ["SELL", "WOOL", 9]
    assert SA.sell_all_the_wool(order, {"WOOL": 2}) is order
    assert SA.sell_all_the_wool(order, {"WOOL": 0}) is order


def test_carrot_offers_the_whole_shed():
    """`CARROT_SWAP_DAYS` is our own addition: we grow a crop the tape barely grew.

    Validation game 97523402, seed 0: **73 CARROT in the shed at the bell at a price of 90**
    (~$6,570) against 4 CARROT sell orders posted all season. Carrot ripens in 2-3 days
    (`first_yield_day: 2, max_yield_day: 3`), so planted d25-27 there is time to sell -- the orders
    were simply never posted. `reference/kaggriculture.py:1069` sells the whole carrot shed too.
    """
    assert SA.sell_all_the_wool(["SELL", "CARROT", 4], {"CARROT": 73}) == ["SELL", "CARROT", 73]


def test_carrot_is_never_reduced_below_the_tapes_own_cadence():
    order = ["SELL", "CARROT", 9]
    assert SA.sell_all_the_wool(order, {"CARROT": 2}) is order


def test_milk_is_untouched():
    """The regression that halved the money. MILK is the tape's cadence, always."""
    order = ["SELL", "MILK", 10]
    assert SA.sell_all_the_wool(order, {"MILK": 60}) is order


def test_crops_are_untouched():
    order = ["SELL", "WHEAT", 12]
    assert SA.sell_all_the_wool(order, {"WHEAT": 99}) is order


def test_a_non_sell_order_is_untouched():
    for order in (["BUY_ANIMAL", "SHEEP", 1], ["BUY_SEED", "WHEAT", 5], ["HIRE"]):
        assert SA.sell_all_the_wool(order, {"WOOL": 38}) is order


def test_an_equal_shed_returns_the_tapes_own_object():
    """Nothing moved, so the tape's order passes through unrebuilt."""
    order = ["SELL", "WOOL", 38]
    assert SA.sell_all_the_wool(order, {"WOOL": 38}) is order


# --- selling the moment it arrives, not only when the tape happens to post -------------------

def test_stock_with_no_tape_sell_still_gets_offered():
    """RED: resizing the tape's order cannot help on a turn the tape posts no sell at all.

    Measured after the resize fix, 9 seasons: 5 cleared, 4 still held 8-24 CARROT, because the only
    carrot sell after the crop lands is `t696 d29 h0` and one order cannot clear 54 units in the
    hours left. Offering on every turn stock exists removes the dependency on the tape's cadence.
    """
    out = SA.top_up_the_sell_orders([["BUY_SEED", "WHEAT", 3]], {"CARROT": 54, "WOOL": 12})
    assert ["SELL", "CARROT", 54] in out, "carrot in the shed must be offered: %r" % (out,)
    assert ["SELL", "WOOL", 12] in out, "wool in the shed must be offered: %r" % (out,)
    assert out[0] == ["BUY_SEED", "WHEAT", 3], "the tape's own orders keep their slots first"


def test_no_duplicate_when_the_tape_already_sells_it():
    """The resize already handled that order. Two sells of the same product waste a slot."""
    out = SA.top_up_the_sell_orders([["SELL", "CARROT", 54]], {"CARROT": 54, "WOOL": 0})
    assert out == [["SELL", "CARROT", 54]], "no second carrot order: %r" % (out,)


def test_an_empty_shed_adds_nothing():
    orders = [["SELL", "WHEAT", 5]]
    assert SA.top_up_the_sell_orders(orders, {"CARROT": 0, "WOOL": 0}) == orders


def test_a_full_turn_never_displaces_a_tape_order():
    """`maxMarketOrdersPerTurn` is 10 and the reference truncates with `q[:max_orders]`.

    Appending means OUR order is the one dropped, never the tape's. A turn already at the cap must
    come back untouched.
    """
    full = [["SELL", "WHEAT", 1]] * 10
    out = SA.top_up_the_sell_orders(list(full), {"CARROT": 54, "WOOL": 12})
    assert out == full, "a full turn must not grow past the cap: %r" % (len(out),)


def test_it_fills_only_the_slots_that_are_free():
    """Nine tape orders leaves exactly one slot: the bigger holding gets it."""
    nine = [["SELL", "WHEAT", 1]] * 9
    out = SA.top_up_the_sell_orders(list(nine), {"CARROT": 54, "WOOL": 12})
    assert len(out) == 10, "one slot free, one order added: %r" % (len(out),)
    assert out[9] == ["SELL", "CARROT", 54], "the larger holding takes the slot: %r" % (out[9],)
