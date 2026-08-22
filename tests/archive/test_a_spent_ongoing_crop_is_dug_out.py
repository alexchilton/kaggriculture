"""An ongoing crop that has finished producing is ground, not a crop.

A one-shot HARVEST clears its tile (`kaggriculture.py:454-455`). An ongoing one does not -- it
collects. So a strawberry that has produced its lifetime maximum sits on its square forever,
occupying ground the season still wants, and nothing in `crop_ops` ever offers to remove it.

**The signal is exact and needs no estimate.** `_new_crop` starts an ongoing crop at
`max_lifespan_step = -1` (`:211`). `_daily_refresh_crops` sets it to `(next_day + 1) * turns_per_day`
the moment `production_count == cd["max_yield"]` (`:789`), and from that step the tile only rots --
`yield_units -= 1` every second step (`:746-752`). So `max_lifespan_step >= 0` on an ongoing crop
means "this tile will never produce again", read straight off the observation.

Victor plays exactly this. Of his 45 DIGs in the season, **30 clear spent STRAWBERRY plants**, every
one of them from d19 on and every one `planted_day: 3` -- the crop reaching the end of its life. Ten
more clear weeds and five hit empty tiles. Measured against our own d16-d29:

    day          d19    d20    d21    d22    d23    d24    d25    d26
    ours/tape    0/3    3/0    0/8    2/1   1/10   10/3    3/1   3/10
    plant        1/7  11/13  10/12    4/1   3/16  14/16  10/12   0/11
    sell        47/45 38/109 88/98 115/62  49/60  56/92  30/66  73/62

Our digs and his are different ops doing different jobs: ours clear WEEDS (16 of them by d29, every
one our own missed watering), his recycle producing ground. He digs, replants, harvests and sells;
we hold dead tiles, `plant` falls to 3/16 and 0/11, and `sell` collapses. We lead by $4,314 at d19
and trail by $20,372 at d29.

The assertion is on `crop_ops` -- that a spent ongoing tile is offered a DIG -- because the claim is
about which op exists, not about whether the planner has turns for it. It says nothing about a crop
still producing, which must NOT be dug, and nothing about one-shots, which clear themselves.
"""
import pytest

from kagg.search import router as R

DAY = 20
TPD = 24


def _strawberry(**over):
    """A STRAWBERRY planted on d3, as Victor's dug tiles all were."""
    cell = {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": 3, "yield_units": 0,
            "watered_today": False, "consecutive_unwatered": 0, "fertilized_until_day": -1,
            "max_lifespan_step": -1}
    cell.update(over)
    return cell


def _ops(cell, day=DAY):
    return R.crop_ops(cell, day, have_fertilizer=False)


def test_the_premise_an_ongoing_crop_marks_its_own_exhaustion():
    """Guard, straight off the reference: the field exists and -1 means 'still producing'."""
    assert R.CROP["STRAWBERRY"]["ongoing"], "STRAWBERRY is not ongoing; wrong fixture"
    assert _strawberry()["max_lifespan_step"] == -1


def test_a_producing_crop_is_never_offered_a_dig():
    """The dangerous direction. Digging a live tile destroys the rest of its season."""
    ops = _ops(_strawberry())
    assert not [o for o in ops if o[0] == "DIG"], (
        f"a STRAWBERRY still producing (max_lifespan_step -1) was offered {ops}")


def test_a_spent_ongoing_crop_is_offered_a_dig():
    spent = _strawberry(max_lifespan_step=(DAY - 1) * TPD)
    ops = _ops(spent)
    assert [o for o in ops if o[0] == "DIG"], (
        f"a STRAWBERRY that has produced its lifetime maximum -- max_lifespan_step "
        f"{spent['max_lifespan_step']}, set once and only once by _daily_refresh_crops -- was "
        f"offered {ops}. It will never produce again and it is holding ground the season wants.")


def test_the_dig_does_not_outrank_harvesting_what_is_left():
    """A spent tile may still hold units. Take them before demolishing it."""
    spent = _strawberry(max_lifespan_step=(DAY - 1) * TPD, yield_units=3)
    ops = _ops(spent)
    names = [o[0] for o in ops]
    if "DIG" not in names or "HARVEST" not in names:
        pytest.skip(f"need both ops to compare order; got {names}")
    assert names.index("HARVEST") < names.index("DIG"), (
        f"DIG is emitted before HARVEST on a tile still holding {spent['yield_units']} units: {ops}")
