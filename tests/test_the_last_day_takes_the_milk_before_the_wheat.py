"""On the last day the richest thing on the board must outrank the poorest, whatever it is.

Alex, 2026-08-24, on ladder game 98428765 (lost by $1,783 with $3,006 of milk and wool standing):
*"i would prefer in that case you take the milk and the wool before the wheat! when they are both
so high!"*

That game was played by `e2500_shopprice.py`, byte-identical to the built artifact, so the
shop-price fix WAS live. It still left three cows holding 3 milk at $270 and a sheep holding 4 wool
at $144, and spent the day hauling wheat the town paid $21 for.

The cause is an asymmetry introduced by that same fix:

    animal_ops, last day    prize = units * LIVE price          cow  = 3 * 270  =       810
    crop_ops,   last day    prize = units * BASE_PRICE + CRITICAL  wheat = 3 * 25 + 1e6 = 1,000,075

`CRITICAL` was removed from the pens and left on the crops, which made a pen strictly worse than
any crop on the last day -- worse than before the fix. Every wheat tile outranked every cow by
1,235x, so the tour filled with wheat and the pens were never reached.

`CRITICAL` earns its place on a NON-final day, where it means "this tile decays tomorrow and there
is a tomorrow to lose it in". On the last day nothing decays -- everything standing is discarded
whole -- so the deadline is identical for every tile and a term that is equal everywhere cannot
order anything. It only destroys the value comparison.

These tests pin the ordering Alex asked for, at the live prices from that game's final turn.
"""

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from kagg.search import router as RT                                     # noqa: E402

# The town's book at the close of game 98428765, seed 1236821574.
MILK, WOOL, WHEAT = 270.0, 144.0, 21.0
LAST_DAY = 29


def a_cow(units=3):
    """A pen holding `units` of milk, fed, with nothing else to offer."""
    return {"animal": "COW", "yield_units": units, "fed_today": True,
            "consecutive_unfed": 0, "fertilizer_available": False}


def a_sheep(units=4):
    return {"animal": "SHEEP", "yield_units": units, "fed_today": True,
            "consecutive_unfed": 0, "fertilizer_available": False}


def a_wheat_tile(units=3, planted_day=24):
    """A wheat tile holding `units`, old enough that its HARVEST is legal."""
    return {"kind": "PLANT", "crop": "WHEAT", "yield_units": units,
            "planted_day": planted_day, "fertilized_until_day": -1,
            "consecutive_unwatered": 0, "watered_today": True,
            "max_lifespan_step": -1, "production_count": 0}


def harvest_prize(ops):
    """The prize on the HARVEST in `ops`, or None if there is not one."""
    for op, _item, prize in ops:
        if op == "HARVEST":
            return prize
    return None


def test_a_cow_full_of_270_milk_outranks_a_wheat_tile_worth_21_a_unit():
    """$810 of milk must beat $63 of wheat. This is the exact d29 of game 98428765."""
    cow = harvest_prize(RT.animal_ops(a_cow(), LAST_DAY, True, product_price=MILK))
    wheat = harvest_prize(RT.crop_ops(a_wheat_tile(), LAST_DAY, False, None,
                                      tile=(9, 6), product_price=WHEAT))
    assert cow is not None and wheat is not None
    assert cow > wheat, (
        f"the cow prices {cow:,.0f} and the wheat {wheat:,.0f} -- the tour takes the wheat, "
        f"which is what left $3,006 standing in game 98428765")


def test_a_sheep_full_of_144_wool_outranks_the_same_wheat():
    """$576 of wool must beat $63 of wheat."""
    sheep = harvest_prize(RT.animal_ops(a_sheep(), LAST_DAY, True, product_price=WOOL))
    wheat = harvest_prize(RT.crop_ops(a_wheat_tile(), LAST_DAY, False, None,
                                      tile=(9, 6), product_price=WHEAT))
    assert sheep > wheat, f"wool prices {sheep:,.0f}, wheat {wheat:,.0f}"


def test_the_cow_outranks_the_sheep_because_the_milk_is_dearer():
    """Within the pens, value still decides -- $810 of milk over $576 of wool."""
    cow = harvest_prize(RT.animal_ops(a_cow(), LAST_DAY, True, product_price=MILK))
    sheep = harvest_prize(RT.animal_ops(a_sheep(), LAST_DAY, True, product_price=WOOL))
    assert cow > sheep


def test_no_last_day_harvest_prize_carries_the_constant():
    """Nothing on the last day may be priced with `CRITICAL`; it equalises what it touches."""
    for ops in (RT.animal_ops(a_cow(), LAST_DAY, True, product_price=MILK),
                RT.animal_ops(a_sheep(), LAST_DAY, True, product_price=WOOL),
                RT.crop_ops(a_wheat_tile(), LAST_DAY, False, None, tile=(9, 6),
                            product_price=WHEAT)):
        p = harvest_prize(ops)
        if p is not None:
            assert p < RT.CRITICAL, f"{p:,.0f} carries CRITICAL"


def test_the_last_day_crop_prize_is_the_live_price_not_the_constant():
    """3 wheat at a live $21 is worth $63, not 3 x BASE_PRICE."""
    prize = harvest_prize(RT.crop_ops(a_wheat_tile(units=3), LAST_DAY, False, None,
                                      tile=(9, 6), product_price=WHEAT))
    assert prize == pytest.approx(63.0)


def test_the_wheat_goes_first_when_the_animal_book_has_crashed():
    """The rule reversed, and this is the half that proves it is a rule and not a preference.

    Alex, 2026-08-24: *"so will it get the wheat in first if the cow and sheep have crashed to 1?"*

    We flood our own book, so the same board that pays $270 for milk in one game pays $1 in the next
    -- both measured on seed 34935263. Nothing here knows what a cow is; it multiplies units by
    what the town pays this turn. A pen holding 3 milk at $1 is worth $3 and must LOSE to a wheat
    tile worth $63.

    This is why the earlier rematch of game 98428765 leaving three cows standing was correct play
    rather than a failure: milk was $1 in that run.
    """
    cow = harvest_prize(RT.animal_ops(a_cow(), LAST_DAY, True, product_price=1.0))
    sheep = harvest_prize(RT.animal_ops(a_sheep(), LAST_DAY, True, product_price=1.0))
    wheat = harvest_prize(RT.crop_ops(a_wheat_tile(), LAST_DAY, False, None,
                                      tile=(9, 6), product_price=WHEAT))
    assert wheat > sheep > cow, (
        f"crashed book: wheat {wheat:,.0f}, wool {sheep:,.0f}, milk {cow:,.0f} -- "
        f"a constant anywhere in this chain breaks the reversed case first")


def test_a_crop_still_gets_the_deadline_promotion_before_the_last_day():
    """The `CRITICAL` deadline is real on a day that HAS a tomorrow. Do not remove it there.

    This is the guard that stops the fix above from being over-applied: on d29 nothing decays, but
    on d20 a tile past its last safe age is eaten overnight and must still be promoted.
    """
    cell = a_wheat_tile(units=3, planted_day=10)
    prize = harvest_prize(RT.crop_ops(cell, 20, False, None, tile=(9, 6), product_price=WHEAT))
    assert prize is not None and prize >= RT.CRITICAL, (
        "a mid-season tile past its last safe day must keep its deadline promotion")
