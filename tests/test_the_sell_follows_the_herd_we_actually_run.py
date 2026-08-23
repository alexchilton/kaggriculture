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
