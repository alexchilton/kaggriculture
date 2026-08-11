"""FERTILIZE is priced off the crop's window and never off the days the season has left.

Both gates in `crop_ops` count window days:

    # one-shot, router.py:617
    waters_left = info["max_day"] - age + 1

    # ongoing, router.py:685
    if (produces_tomorrow and not fertilized and have_fertilizer and room > 1
            and price > fert_price):

Neither is clipped to `R.SEASON_DAYS`. The rest of the file already knows how -- `_crop_remaining`
(:542, :550) and the window pricer (:869) all take `days_left = R.SEASON_DAYS - 1 - day` and
`window_end = min(info["max_day"], days_left)`.

So on the last day of the season a strawberry that "produces tomorrow" is fertilized for a
production day that never arrives, and a one-shot near the end is credited with waters the season
cannot afford to give it.

It is not merely a wasted turn. FERTILIZER is a PRODUCT -- it has a market row and a base price --
so every unit put in the ground at the end of the season is a unit not in the shed for the last
day's liquidation. Measured on the Victor grid, seed 11, `fertilize` ours/tape:

    d24 8/3   d25 1/0   d26 10/2   d27 3/0   d28 9/0   d29 0/0

The tape stops at d26. We are still burning nine units on d28, and d29 sells 27 against its 179.
The gate gets *keener* late, too: nothing eats fertilizer, so its book only ratchets and its price
falls to ~$20 by d26 (router.py:580), which makes `price > fert_price` easier to satisfy exactly
when the unit has least time to earn its doubling back.

STRAWBERRY is the discriminating case: `first_yield_day` 10, `interval` 2, so a tile planted on d18
has `produces_tomorrow` true on d29 -- production on d30, one day past the end.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import router as RT
from kagg.search import routines as R

LAST_DAY = R.SEASON_DAYS - 1        # 29


def _cell(crop, planted_day, **kw):
    cell = dict(kind="PLANT", crop=crop, planted_day=planted_day, yield_units=0,
                watered_today=False, consecutive_unwatered=0, fertilized_until_day=-1)
    cell.update(kw)
    return cell


def _ops(cell, day, price=20.0):
    """`crop_ops` with fertilizer cheap, which is what it actually costs at the end of a season."""
    return [op for op, _item, _prize in RT.crop_ops(cell, day, True, price)]


def test_the_premise_this_tile_would_produce_the_day_after_the_season_ends():
    """Guards the fixture. If STRAWBERRY's cadence moves, the case below stops discriminating."""
    info = RT.CROP["STRAWBERRY"]
    age = LAST_DAY - 18
    assert age + 1 >= info["first"] and (age + 1 - info["first"]) % info["interval"] == 0, (
        f"a STRAWBERRY planted on d18 no longer 'produces tomorrow' on d{LAST_DAY}; this file's "
        f"fixture is stale and the season-end case must be re-derived.")
    assert LAST_DAY + 1 >= R.SEASON_DAYS, "the production day is inside the season; nothing to test."


def test_an_ongoing_tile_is_not_fertilized_on_the_last_day_of_the_season():
    ops = _ops(_cell("STRAWBERRY", 18), LAST_DAY)
    assert "FERTILIZE" not in ops, (
        f"d{LAST_DAY} is the last day of a {R.SEASON_DAYS}-day season and a STRAWBERRY planted on "
        f"d18 was offered {ops}. The doubling it buys lands on d{LAST_DAY + 1}, which never "
        f"happens, and the FERTILIZER unit it spends could have been sold instead.")


def test_the_same_tile_is_still_fertilized_when_the_season_has_room():
    """The clip must be season-end specific. If this goes red the fix has disabled the op outright."""
    ops = _ops(_cell("STRAWBERRY", 10), 21)
    assert "FERTILIZE" in ops, (
        f"a STRAWBERRY producing on d22 was not offered FERTILIZE ({ops}). The season-end clip has "
        f"turned the op off generally instead of only where the season cannot pay it back.")


def test_a_one_shot_is_priced_off_the_waters_the_season_can_actually_give_it():
    """WHEAT planted d27: window d29-d31, of which the season affords exactly one day.

    Asserted on the PRIZE, not on the op. With one water left the doubling is still marginally
    worth having -- one unit of wheat at $25 against a $20 fertilizer -- so refusing the op outright
    would be wrong. What is wrong is pricing it as though three waters were coming:

        unclipped   gain = min(6, 3 * 2) - min(6, 3) = 3   ->  prize 75
        clipped     gain = min(6, 1 * 2) - min(6, 1) = 1   ->  prize 25

    A prize three times what the tile can deliver is what outranks the survival water on a tile that
    would otherwise weed, which is how the late season accumulates thirteen weeds against the
    tape's one.
    """
    got = [(op, prize) for op, _item, prize in
           RT.crop_ops(_cell("WHEAT", 27), LAST_DAY, True, 20.0) if op == "FERTILIZE"]
    assert got, "the fixture no longer offers FERTILIZE at all; re-derive the case."
    price = RT.BASE_PRICE["WHEAT"] if hasattr(RT, "BASE_PRICE") else 25
    assert got[0][1] == 1 * price, (
        f"a WHEAT planted on d27 is offered FERTILIZE at {got[0][1]}, which prices "
        f"{got[0][1] / price:.0f} extra units. The season ends on d{LAST_DAY}, so exactly one water "
        f"is available and the doubling can add exactly one unit.")
