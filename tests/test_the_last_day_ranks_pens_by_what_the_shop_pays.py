"""On the last day a pen is worth what the shop will pay for what is standing in it.

Alex, 2026-08-24: *"we are wanting to optimise based on the actual price in the shop not what you
set it"*, and *"it is not only wool - it should be shop dependent - if the shop for wool is only low
then it will be possibly milk etc"*.

**Two defects, and the second hides the first.**

1. `animal_ops` priced the last-day HARVEST off `BASE_PRICE` (`router.py`), a module constant. WOOL
   is 200 and MILK is 160 there whatever the town is actually paying. Both runs of ladder game
   98335212 on seed 34935263 show how far that drifts:

       recorded submission     WOOL $183   MILK $1
       our own rematch         WOOL $5     MILK $214

   Same seed, opposite ranking, because the price is set by what WE dumped into the book earlier.

2. The prize was `CRITICAL + units * price` with `CRITICAL = 1_000_000`, so:

       cow,   3 milk @ $214  ->  1,000,642
       sheep, 4 wool @ $5    ->  1,000,020

   A $642 pen and a $20 pen differ by 0.06%. Even with a correct price threaded in, the ranking is
   noise against the constant, and the route visits pens in whatever order the board offers.

Measured consequence, d29 of that game with the planner owning the last two days: four pens left
holding at the close -- two cows at 3 milk and two sheep at 4 wool -- $1,600 standing, of which
~$1,284 was the milk it walked past.
"""

import pytest

R = pytest.importorskip("kagg.search.router")

LAST_DAY = 29


def _pen(animal, units):
    return {"kind": "PASTURE", "animal": animal, "yield_units": units,
            "fed_today": True, "cared_today": True, "consecutive_unfed": 0,
            "fertilizer_available": False}


def _prize(animal, units, price=None):
    ops = R.animal_ops(_pen(animal, units), LAST_DAY, True, product_price=price)
    for op, _item, prize in ops:
        if op == "HARVEST":
            return prize
    return None


def test_the_shop_price_decides_which_pen_is_worth_more():
    """**The acceptance test.** The expensive pen must outrank the cheap one by the ratio of what
    they are worth, not by a rounding error on a constant."""
    cow = _prize("COW", 3, price=214.0)          # $642
    sheep = _prize("SHEEP", 4, price=5.0)        # $20
    assert cow > sheep
    # And by a margin that can actually order a route: the cheap pen must not be within 1% of it.
    assert sheep < 0.5 * cow, (cow, sheep)


def test_the_same_pen_flips_rank_when_the_book_flips():
    """The other half of Alex's point: it is not that wool is valuable, it is that the SHOP decides.
    In the recording wool beat milk 183 to 1; in our rematch of that same seed milk beat wool 214
    to 5. One ranking rule has to get both right."""
    assert _prize("SHEEP", 4, price=183.0) > _prize("COW", 3, price=1.0)
    assert _prize("COW", 3, price=214.0) > _prize("SHEEP", 4, price=5.0)


def test_the_prize_is_the_money_not_a_constant_plus_the_money():
    """`CRITICAL` swamps the price. On the last day the pen's whole worth IS its standing product,
    so the number must scale with the money and nothing else."""
    one = _prize("SHEEP", 1, price=100.0)
    two = _prize("SHEEP", 2, price=100.0)
    assert two == pytest.approx(2 * one), (one, two)


def test_omitting_the_price_still_falls_back_to_the_base_price():
    """Compatibility guard. Callers that pass nothing must behave as before, which is what keeps
    every day other than the last byte-identical."""
    assert _prize("SHEEP", 4) == _prize("SHEEP", 4, price=float(R.BASE_PRICE["WOOL"]))
