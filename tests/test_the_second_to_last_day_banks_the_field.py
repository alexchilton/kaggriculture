"""d28 is the last day a harvest banks itself. Take everything the board is holding.

**Selling costs no unit-turns.** A SELL is a market order, handled in `_process_market`, not a unit
action -- so the only thing that decides how much the last day can sell is how much sits in
`private["shed"]` when it starts. The shed is filled for free by `_drop_inventories_to_shed`, which
runs inside `_end_of_day`. So produce harvested on d28 is banked overnight at zero turn cost and is
sellable all through d29; produce harvested ON d29 lands in a hand, and that drop comes after the
final turn (`tests/test_the_last_day_puts_its_load_in_the_shed.py`).

That used to cost us the last two days: an earlier grid showed d28 harvest at 27 against a 32-unit
tape, the shortfall carrying into d29 as 51 stranded, unsellable units (~$1,192).
That back-loading is now closed -- see `docs/the_last_two_days_2026-08-17.md`.
The live grid (2026-08-17) matches the tape on both days:

    closing week   harvest      ours/tape
    d28             32/32
    d29             19/19

This test now guards against a regression, not a live defect. It pins the pricing, not the
routing: a ripe tile on d28 must outrank ordinary work, because tomorrow that produce cannot be
banked. It does not say which hand goes where.
"""
import importlib

import pytest

RT = importlib.import_module("kagg.search.router")
R = importlib.import_module("kagg.search.routines")

LAST_FREE_DROP_DAY = R.SEASON_DAYS - 2          # d28


def _ripe_wheat(planted_day, units=4):
    return dict(kind="PLANT", crop="WHEAT", yield_units=units, planted_day=planted_day,
                watered_today=True, consecutive_unwatered=0, fertilized_until_day=-1)


def _pen(units=4):
    return {"animal": "COW", "placed_day": 0, "fed_today": True, "cared_today": True,
            "consecutive_unfed": 0, "yield_units": units}


def test_the_last_free_drop_day_is_twenty_eight():
    """The premise. d29's own drop lands after the final turn, so d28 is the last one that banks."""
    assert LAST_FREE_DROP_DAY == 28, f"SEASON_DAYS puts the last free drop on d{LAST_FREE_DROP_DAY}"


def test_a_ripe_crop_on_d28_outranks_ordinary_work():
    """The defect, priced. A tile holding produce on d28 is the last chance to bank it free."""
    ops = RT.crop_ops(_ripe_wheat(planted_day=24), LAST_FREE_DROP_DAY, True, tile=(7, 0))
    harvest = [o for o in ops if o[0] == "HARVEST"]
    assert harvest, f"no HARVEST offered on d{LAST_FREE_DROP_DAY} for a tile holding 4 units: {ops}"
    assert harvest[0][2] >= RT.CRITICAL, (
        f"d{LAST_FREE_DROP_DAY} HARVEST priced at {harvest[0][2]}, below CRITICAL={RT.CRITICAL}. "
        f"Tomorrow this produce cannot be banked, and the grid shows 48 idle unit-turns on d28 "
        f"while 51 units end the season stranded in hands.")


def test_a_ripe_pen_on_d28_outranks_ordinary_work():
    """Animals too -- milk and wool strand exactly like crops."""
    ops = RT.animal_ops(_pen(), LAST_FREE_DROP_DAY, have_wheat=True)
    harvest = [o for o in ops if o[0] == "HARVEST"]
    assert harvest, f"no HARVEST offered on d{LAST_FREE_DROP_DAY} for a pen holding 4 units: {ops}"
    assert harvest[0][2] >= RT.CRITICAL, (
        f"d{LAST_FREE_DROP_DAY} pen HARVEST priced at {harvest[0][2]}, below CRITICAL")


def test_an_empty_tile_is_not_promoted():
    """It is the produce that is urgent, not the day. A tile holding nothing must not jump."""
    ops = RT.crop_ops(_ripe_wheat(planted_day=24, units=0), LAST_FREE_DROP_DAY, True, tile=(7, 0))
    assert not [o for o in ops if o[0] == "HARVEST" and o[2] >= RT.CRITICAL], (
        f"an empty tile was priced CRITICAL on d{LAST_FREE_DROP_DAY}: {ops}")


@pytest.mark.parametrize("day", [20, 24, 26])
def test_earlier_days_are_untouched(day):
    """Only d28. Every earlier day banks itself overnight too, so nothing is urgent about them.

    A tile still inside its filling window must not be dragged forward -- harvesting a part-filled
    one-shot demolishes the tile for the units it has, which is the mistake this repo has already
    made once.
    """
    cell = _ripe_wheat(planted_day=day - 2)            # age 2, still filling
    ops = RT.crop_ops(cell, day, True, tile=(7, 0))
    assert not [o for o in ops if o[0] == "HARVEST" and o[2] >= RT.CRITICAL], (
        f"d{day} promoted a still-filling crop: {ops}")
