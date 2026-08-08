"""When the shed cannot take the day's harvest, the CHEAPEST stock must go, not the biggest pile.

`shedCapacity` is 100 slots shared by all nine products, and `_drop_inventories_to_shed` discards
whatever does not fit at the rollover -- silently, and without regard to what it is worth. The agent
gets one chance to choose: `SELL_TO_MAKE_ROOM` sells stock down during the day to leave space.

It chose by quantity:

    for p in sorted(SELLABLE, key=lambda p: -int(shed.get(p, 0))):

which is right today only by coincidence. Wheat is both the cheapest product and the biggest pile
(41-45 of 100 slots late season at base $25, against milk's 0-9 at base $160), so largest-first
happens to pick it. Nothing makes that hold: the moment an expensive product is the largest pile,
this rule sells it to protect a cheap one.

A slot is a slot. What it should hold is whatever is worth most per slot.
"""

import pytest

from kagg.search import schedule_agent as SA


def test_the_biggest_pile_is_not_automatically_the_one_to_sell():
    """Milk is the biggest pile and the most valuable; wheat is smaller and nearly worthless."""
    shed = {"MILK": 60, "WHEAT": 20, "WOOL": 5}
    order = SA.release_order(shed)
    assert order[0] != "MILK", (
        f"release order was {order}: the shed is crowded and the rule reaches for MILK first, at a "
        "base of $160, while WHEAT sits there at $25. Ordering by pile size sells the most valuable "
        "thing in the shed whenever it also happens to be the largest."
    )
    assert order.index("WHEAT") < order.index("MILK")


def test_the_cheapest_stock_goes_first():
    """Full ordering, cheapest base price first, over everything actually in the shed."""
    shed = {"MILK": 10, "WHEAT": 10, "WOOL": 10, "STRAWBERRY": 10, "MELON": 10}
    order = [p for p in SA.release_order(shed) if p in shed]
    assert order == ["WHEAT", "STRAWBERRY", "MILK", "WOOL", "MELON"], order


def test_an_empty_pile_is_never_chosen_over_a_stocked_one():
    """A product we do not hold frees no slot, however cheap it is."""
    shed = {"MILK": 40, "WHEAT": 0}
    order = [p for p in SA.release_order(shed) if shed.get(p)]
    assert order == ["MILK"], order


@pytest.mark.parametrize("shed", [{}, {"WHEAT": 0}])
def test_an_empty_shed_orders_without_raising(shed):
    assert isinstance(SA.release_order(shed), list)
