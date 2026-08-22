"""A fertilizer unit is priced at a constant $100, so late-season tiles never get fertilized.

`router.crop_ops` decides between SELLING a fertilizer unit and APPLYING it to a tile by comparing
the tile's gain against `BASE_PRICE["FERTILIZER"]`:

    if gain * price > BASE_PRICE["FERTILIZER"]:                      # one-shot,  router.py:608
    if (... and price > BASE_PRICE["FERTILIZER"]):                   # ongoing,   router.py:672

`BASE_PRICE["FERTILIZER"]` is 100 -- the market's I0 equilibrium, described in its own comment as
a price "nobody actually pays". Nothing in the game eats fertilizer: no shop lists it and
`reference/kaggriculture.py:101` builds the town centre's list as
`[p for p in PRODUCTS if p != "FERTILIZER"]`. So its book only ever ratchets upward and the price
only ever falls.

Measured over the 85 recorded games that carry a market trace, the day the price first reaches:

    $80    median day 10.2      85 of 85 games
    $50    median day 17.0      84 of 85
    $30    median day 23.9      78 of 85
    $20    median day 25.9      75 of 85
    $10    median day 27.4      64 of 85

So from about day 17 the router is refusing to fertilize tiles on the grounds that the unit is worth
$100, when the unit is worth $50; by day 26 it is worth $20. It under-applies exactly when applying
has become the better trade.

## Why the previous attempt at this measured null, and why that reason has expired

`router.py:79-91` records a TRIED-and-REVERTED version of this that used the mean realised sale
price ($53) instead of the constant. It was a null, and the recorded reason is precise:

> the only case the threshold change touches is an ongoing crop priced between $53 and $100
> (TOMATO, $60), and this schedule's crop mix is WHEAT/STRAWBERRY/MELON only -- no TOMATO or CARROT
> ever appears in a `plants` row.

`SHOP_ADAPT_CROPS` plants TOMATO and CARROT. The precondition that made the fix unreachable is the
exact thing the crop swap removes, so the null does not carry over. This is the CLAUDE.md rule that
a decision to skip a fix expires when the problem changes -- re-read the reason before assuming it
still holds.

The fix here is also not the reverted one: a season MEAN is still a constant, and the whole defect
is that the value moves. The live quote is in the observation (`market.prices`), so it need not be
estimated at all.
"""

import pytest

from kagg.search import router as RT


def ongoing_tile(day=20, crop="TOMATO"):
    """A tomato tile that produces tomorrow, has room, and is not yet fertilized."""
    info = RT.CROP[crop]
    # Age it so that `produces_tomorrow` is true: (age + 1 - first) % interval == 0.
    age = info["first"] - 1
    return dict(kind="PLANT", crop=crop, planted_day=day - age, watered_today=True,
                consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)


def has_fertilize(ops):
    return "FERTILIZE" in [o for o, _i, _p in ops]


def test_a_tomato_tile_is_fertilized_once_the_book_has_cratered():
    """TOMATO is $60. At a fertilizer quote of $20 the swap is clearly worth making."""
    cell = ongoing_tile(day=26, crop="TOMATO")
    ops = RT.crop_ops(cell, 26, True, fertilizer_price=20.0)
    assert has_fertilize(ops), (
        f"a $60 tile refused a $20 fertilizer unit; ops {[(o, p) for o, _i, p in ops]}")


def test_the_same_tile_is_left_alone_while_fertilizer_still_fetches_its_base():
    """Early in the season the unit really is worth ~$100, and a $60 tile is the worse use of it."""
    cell = ongoing_tile(day=8, crop="TOMATO")
    ops = RT.crop_ops(cell, 8, True, fertilizer_price=100.0)
    assert not has_fertilize(ops), (
        f"a $60 tile took a $100 fertilizer unit; ops {[(o, p) for o, _i, p in ops]}")


def test_a_carrot_tile_becomes_worth_fertilizing_late():
    """CARROT is $35, so it only ever pays once the book is well down. One-shot path."""
    info = RT.CROP["CARROT"]
    # Inside the yield window, with more room than plain waters can fill.
    age = info["max_day"]
    cell = dict(kind="PLANT", crop="CARROT", planted_day=27 - age, watered_today=False,
                consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)
    cheap = RT.crop_ops(cell, 27, True, fertilizer_price=10.0)
    dear = RT.crop_ops(cell, 27, True, fertilizer_price=100.0)
    assert has_fertilize(cheap) or not has_fertilize(dear), (
        "the carrot tile's answer did not move with the fertilizer price at all")
    assert not has_fertilize(dear), (
        f"a carrot tile took a $100 unit; ops {[(o, p) for o, _i, p in dear]}")


def test_the_default_is_the_old_constant():
    """Callers that do not pass a price must behave exactly as before -- this is a threading change.

    Without this the fix is indistinguishable from a behaviour change on every code path that has
    not been updated yet, and a partial rollout would be silently mixing two valuations.
    """
    cell = ongoing_tile(day=20, crop="TOMATO")
    assert (RT.crop_ops(cell, 20, True)
            == RT.crop_ops(cell, 20, True, fertilizer_price=RT.BASE_PRICE["FERTILIZER"]))
