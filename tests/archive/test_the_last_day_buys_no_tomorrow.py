"""Survival waters, rotation waters and weed digs buy a tomorrow the last day does not have.

The op families on a crop board and what each one buys, read off the reference:

  - an IN-WINDOW water on a one-shot adds a yield unit THE SAME DAY (`_apply_unit_action`), so it
    is real money on d29 exactly like a harvest, and the tape still emits 11 of them on its d29;
  - a SURVIVAL water (outside the window, `consecutive_unwatered >= 1`) buys the tile not weeding
    at tonight's rollover -- worth the crop's remaining production, which after d29's rollover
    is nothing;
  - a ROTATION water (`WATER_ROTATION`, the half-board alternation) is the same purchase spread
    over two days;
  - a DIG clears ground for a planting that must happen on a later day.

The d29 trace (`data/logs/fable_d29_trace.log`) shows the cost: u4 spends h17 and h20 DIGging
weeds at (1,0) and (3,0) and ends the season at (3,1) holding 3 units it had no turns left to
walk in. The grid shows `dig 5/0` and `water 18/11` on d29 -- the tape's eleven are the
yield-carrying kind, and it digs nothing.

Same master switch as the upkeep rule: `router.NO_UPKEEP_ON_THE_LAST_DAY`, asked through
`router.upkeep_buys_nothing(day)`, so one revert restores the whole family.
"""
import importlib

import pytest

RT = importlib.import_module("kagg.search.router")
SA = importlib.import_module("kagg.search.schedule_agent")
R = importlib.import_module("kagg.search.routines")

LAST_DAY = R.SEASON_DAYS - 1


def _wheat(planted_day, unwatered=0, units=0):
    return dict(kind="PLANT", crop="WHEAT", yield_units=units, planted_day=planted_day,
                watered_today=False, consecutive_unwatered=unwatered, fertilized_until_day=-1)


def test_no_survival_water_on_the_last_day():
    """Age 1 wheat is outside its window; at `consecutive_unwatered >= 1` it gets a survival
    water on any ordinary day. On d29 the weed it prevents costs nothing."""
    ops = RT.crop_ops(_wheat(planted_day=LAST_DAY - 1, unwatered=1), LAST_DAY, False, tile=(7, 0))
    assert not [o for o in ops if o[0] == "WATER"], (
        f"d{LAST_DAY} offered a survival water; the tile it saves is gone at the rollover: {ops}")


def test_no_rotation_water_on_the_last_day():
    """The half-board alternation exists to keep `consecutive_unwatered` below 2 across days."""
    ops = RT.crop_ops(_wheat(planted_day=LAST_DAY - 1, unwatered=0), LAST_DAY, False, tile=(7, 0))
    assert not [o for o in ops if o[0] == "WATER"], (
        f"d{LAST_DAY} offered a rotation top-up water: {ops}")


def test_the_yield_water_is_still_offered_on_the_last_day():
    """The other side. An in-window water IS the yield -- the tape emits 11 on its own d29."""
    ops = RT.crop_ops(_wheat(planted_day=LAST_DAY - 2, unwatered=0), LAST_DAY, False, tile=(7, 0))
    assert [o for o in ops if o[0] == "WATER"], (
        f"d{LAST_DAY} stopped offering the in-window water that adds a unit today: {ops}")


@pytest.mark.parametrize("day", [20, 25, 28])
def test_earlier_days_still_water_for_survival(day):
    ops = RT.crop_ops(_wheat(planted_day=day - 1, unwatered=1), day, False, tile=(7, 0))
    assert [o for o in ops if o[0] == "WATER"], (
        f"d{day} stopped survival-watering; only d{LAST_DAY} may: {ops}")


def test_the_executor_digs_no_weed_on_the_last_day():
    """`_live_ops` re-derives a DIG at any WEED tile a route visits, whatever the plan priced.
    That is how u4 dug twice on d29 while its load stranded."""
    ops = SA._live_ops((3, 0), {"kind": "WEED"}, LAST_DAY, {}, {}, {})
    assert not [o for o, _i in ops if o == "DIG"], (
        f"the executor still digs a weed on d{LAST_DAY}; the planting it unblocks never comes: "
        f"{ops}")


def test_the_executor_still_digs_on_d28():
    ops = SA._live_ops((3, 0), {"kind": "WEED"}, LAST_DAY - 1, {}, {}, {})
    assert [o for o, _i in ops if o == "DIG"], (
        f"d{LAST_DAY - 1} stopped digging weeds; only the last day may: {ops}")
