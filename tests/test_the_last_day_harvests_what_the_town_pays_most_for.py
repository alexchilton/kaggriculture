"""The last-day harvest must be ranked by what the town is paying NOW, not by a base price.

Alex, 2026-08-24: *"the sheep in that game was the high value - sometimes it is milk - your job is
to find the shop values at the time and optimise the harvest or wool or milk based on that"*.

**The defect.** `router.animal_ops` prices its last-day HARVEST off `BASE_PRICE`
(`router.py:76`), which is a module constant: WOOL is 200 and MILK is 160 whatever the book
actually says. The two runs of ladder game 98335212 show how far that drifts, on the same seed:

    recorded submission     WOOL $183   MILK $1
    HEAD rematch            WOOL $5     MILK $214

Same game, opposite answer, because we sell into the book we ourselves flood. A route that ranks a
pen by `BASE_PRICE` walks to the wrong animal in one of those two worlds and cannot tell which.

In the recorded game that cost the match: 4 wool were left standing at $183 -- $732 -- and the game
was lost by $781, while the closing turns hauled MILK at $1 a unit.

`crop_ops` already takes `fertilizer_price=None` and falls back to `BASE_PRICE`
(`router.py:416,436`), so threading a live price is the pattern this module already uses rather
than a new idea.
"""

import pytest

R = pytest.importorskip("kagg.search.router")


def _pen(animal, units):
    """A stocked pen holding `units` of unpicked product, fed, on the last day."""
    return {"kind": "PASTURE", "animal": animal, "yield_units": units,
            "fed_today": True, "cared_today": True, "consecutive_unfed": 0,
            "fertilizer_available": False}


LAST_DAY = 29


def _harvest_prize(ops):
    for op, _item, prize in ops:
        if op == "HARVEST":
            return prize
    return None


def test_a_pen_is_priced_at_the_live_price_not_the_base_price():
    """The whole point. Wool at $5 and wool at $183 must not produce the same number."""
    cheap = _harvest_prize(R.animal_ops(_pen("SHEEP", 4), LAST_DAY, True,
                                        product_price=5.0))
    dear = _harvest_prize(R.animal_ops(_pen("SHEEP", 4), LAST_DAY, True,
                                       product_price=183.0))
    assert cheap is not None and dear is not None
    assert dear > cheap, (dear, cheap)


def test_the_town_decides_which_animal_is_worth_the_walk():
    """**The acceptance test.** In the recorded game wool beat milk 183 to 1; in our own rematch of
    the same seed milk beat wool 214 to 5. The ranking has to follow the book, not a constant."""
    wool_rich = _harvest_prize(R.animal_ops(_pen("SHEEP", 4), LAST_DAY, True, product_price=183.0))
    milk_poor = _harvest_prize(R.animal_ops(_pen("COW", 4), LAST_DAY, True, product_price=1.0))
    assert wool_rich > milk_poor

    wool_poor = _harvest_prize(R.animal_ops(_pen("SHEEP", 4), LAST_DAY, True, product_price=5.0))
    milk_rich = _harvest_prize(R.animal_ops(_pen("COW", 4), LAST_DAY, True, product_price=214.0))
    assert milk_rich > wool_poor


def test_more_units_of_the_same_product_are_worth_more():
    """Guard: the prize must still scale with what is actually standing there, so a pen holding one
    unit does not outrank a pen holding six of the same thing."""
    one = _harvest_prize(R.animal_ops(_pen("SHEEP", 1), LAST_DAY, True, product_price=100.0))
    six = _harvest_prize(R.animal_ops(_pen("SHEEP", 6), LAST_DAY, True, product_price=100.0))
    assert six > one


def test_omitting_the_price_falls_back_to_the_base_price():
    """**The compatibility guard, and it is the reason this is safe to land.** Every existing caller
    passes no price, so it must behave byte-identically to the constant it used before -- the same
    contract `crop_ops` gives `fertilizer_price`."""
    base = float(R.BASE_PRICE["WOOL"])
    assert (_harvest_prize(R.animal_ops(_pen("SHEEP", 4), LAST_DAY, True))
            == _harvest_prize(R.animal_ops(_pen("SHEEP", 4), LAST_DAY, True,
                                           product_price=base)))
