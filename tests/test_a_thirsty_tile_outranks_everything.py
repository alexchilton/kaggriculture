"""A tile that misses two waterings in a row BECOMES A WEED. That is the whole farm.

`reference/kaggriculture.py:752-753`, inside `_daily_refresh_plants`:

    if tile["consecutive_unwatered"] >= 2:
        farm["tiles"][y][x] = {"kind": "WEED"}

Not the random spawner -- `weedSpawnChance` is 0.005, which over 30 days and 60 tiles is a handful.
This is our own crops dying and being replaced by weeds, and a WEED tile makes PLANT a silent no-op,
so the ground is dead for the rest of the season too.

Measured on our own tape in the real environment before this test existed:

    day   PLANT  WEED  money
      5      16     2    208
      7       4    13     28
     13       1    18      6
     25       0    20  1,296

Sixteen crop tiles became four in two days. The farm never earned again, and every number downstream
-- the 74.69% op match, the eighteen refusals, the bank pinned under $700 all season -- was measured
on a board that had already died.

The cause is the packer's static priority. `RANK` put `crop` last, behind every pen upkeep task, so a
full day drops watering first; and the cadence waters at a gap of two, which means the tile is
*already* one dry day in. Dropping that one op kills the tile outright.

So the rule is not "water more". It is that a watering which is due is **unrecoverable if skipped**,
exactly like a pen that never gets built, and it has to be ranked that way. A CARE visit skipped
today can happen tomorrow; a tile left dry today is gone.
"""

import sys

import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R


def _tasks(farm, day):
    from kagg.search import dayplan
    return dayplan._tasks_for_day(farm, day, [], [], fertilize=False)


def test_a_tile_one_dry_day_from_death_outranks_pen_upkeep():
    """The contract. If this is not true, a busy day silently kills crop tiles."""
    from kagg.search import dayplan

    farm = dayplan.Farm()
    thirsty = (1, 1)
    farm.crops[thirsty] = dict(crop="STRAWBERRY", planted=0, last_water=0,
                               last_harvest=0, fert_until=-1)
    for i in range(6):
        farm.pens[(4 + i % 2, 4 + i // 2)] = dict(animal="COW", placed=0, last_feed=0)

    tasks = _tasks(farm, 2)          # gap of 2: one dry day already banked
    water = next(t for t in tasks if t["tile"] == thirsty)
    assert "WATER" in water["ops"], "the tile is due and no watering was generated at all"

    pens = [t for t in tasks if t["kind"] == "pen"]
    assert pens, "fixture is wrong; expected pen tasks to compete with"
    assert water["_rank"] < min(p["_rank"] for p in pens), (
        f"a tile one dry day from becoming a WEED ranks {water['_rank']}, behind pen upkeep at "
        f"{min(p['_rank'] for p in pens)} -- so a full day drops the watering and the tile dies")


def test_a_tile_with_slack_does_not_outrank_pen_upkeep():
    """The other half, so the fix cannot become 'crops always win'. A tile watered today is in no
    danger tomorrow, and its visit is genuinely deferrable."""
    from kagg.search import dayplan

    farm = dayplan.Farm()
    safe = (1, 1)
    farm.crops[safe] = dict(crop="STRAWBERRY", planted=0, last_water=2,
                            last_harvest=0, fert_until=-1)
    farm.pens[(4, 4)] = dict(animal="COW", placed=0, last_feed=0)
    tasks = _tasks(farm, 3)
    crop = [t for t in tasks if t["tile"] == safe]
    pens = [t for t in tasks if t["kind"] == "pen"]
    if crop and pens:
        assert crop[0]["_rank"] >= min(p["_rank"] for p in pens), (
            "a tile with a day of slack should not pre-empt the herd")


def test_the_death_rule_is_two_consecutive_dry_days():
    """Pinned against the reference so the margin above is not folklore."""
    src = open("reference/kaggriculture.py").read()
    assert 'tile["consecutive_unwatered"] >= 2' in src, (
        "the death threshold moved; the watering priority above is calibrated to it")
    assert '{"kind": "WEED"}' in src
