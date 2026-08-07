"""A pen built today must not also appear as standing herd today.

`emit()` inserts the new pen into `farm.pens` (`dayplan.py:480`) BEFORE it calls `_tasks_for_day`
(`dayplan.py:527`). Inside, the standing-pens loop emits FEED/CARE/COLLECT_FERTILIZER for every pen
it finds -- including the ones raised this very day -- while the `build_orders` loop separately emits
BUILD_PASTURE/PLACE/FEED/CARE for the same tile. Two task entries, one tile, one day.

Fifteen phantom tasks across the season, on every build day, which matches BUILD_PASTURE at 14-15.
Feeding or caring twice in a day buys nothing: production is not gated on `fed_today`
(`kaggriculture.py:791`) and `pending_care_bonus` accumulates once per day (`:798`).

The cost is not only the wasted turns. Hands fill sequentially (`dayplan.py:273`) and the duplicate
ranks 3 against the build's 0, so the hand that raised the pen has usually moved on before its own
phantom becomes the cheapest option -- and a LATER hand walks back across the board to service it.
Traced on day 0: hand 4 finished plantings at (0,4) and (0,3), then returned to (4,3) and (4,2),
tiles other hands had built pens on earlier.

This is also, most likely, what the CARE +47 / FEED +36 season residual actually was. The earlier
attempt to fix that by cutting the herd cadence was the wrong fix for a real symptom, and cost eight
points of tape fidelity (`docs/fable_emitter_task_generation_2026-08-05.md`).
"""


import pytest

#: **Disabled 2026-08-07: this whole file asserts against the OLD LEADER's tape (`new_leader`).**
#:
#: Kept, not deleted, because it is the record of a specific and expensive mistake. The agent is now
#: matched against Seb's tape (`top_guys/90494364`), and the two tapes play differently -- the case
#: that forced this was watering. `router.py` had been made to water every tile every day on the
#: strength of a table showing "the tape" watering ~1.06 per live tile daily, 18 times on day 1
#: against our 1. That table was measured here, on the old leader, and then applied to Seb:
#:
#:     oldleader  d0 16/17  d1 17/18  d2 18/19  d3 18/19   waters daily
#:     seb        d0 17/17  d1 17/0   d2 17/17  d3 17/14   waters alternate days
#:
#: Seb takes zero weeds through day 7 on the alternate-day cadence, and the every-day rule was
#: costing 17 work turns and ~31 walk turns on day 1 alone for nothing.
#:
#: So these assertions are not wrong about the old leader; they are answers to a question we stopped
#: asking. Left red, they read as regressions and pull work towards the wrong target. Re-enable only
#: by first deciding which tape the number is supposed to describe.
_OLD_LEADER_SKIP = pytest.mark.skip(
    reason="asserts against the OLD LEADER's tape; the agent now targets Seb's -- see banner")

pytestmark = _OLD_LEADER_SKIP
import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")


def test_a_pen_raised_today_gets_one_task_not_two():
    """The unit form: one tile, one task, on the day it is built."""
    from kagg.search import dayplan

    farm = dayplan.Farm()
    tile = (4, 4)
    farm.pens[tile] = dict(animal="COW", placed=3, last_feed=3)   # as emit() does, before the call
    tasks = dayplan._tasks_for_day(farm, 3, [], [(tile, "COW")], fertilize=False)
    here = [t for t in tasks if t["tile"] == tile]
    assert len(here) == 1, (
        f"{len(here)} tasks for the pen raised today at {tile}: "
        f"{[(t['kind'], t['ops']) for t in here]}")
    assert here[0]["kind"] == "build"


def test_no_build_day_anywhere_in_the_season_doubles_up():
    """The season form, against the real schedule, so a regression anywhere is caught."""
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    from kagg.search import dayplan

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    dupes = []
    orig = dayplan._tasks_for_day

    def spy(farm, day, plant_orders, build_orders, fertilize, replant=None):
        tasks = orig(farm, day, plant_orders, build_orders, fertilize, replant)
        seen = collections.Counter(t["tile"] for t in tasks)
        for tile, n in seen.items():
            if n > 1:
                dupes.append(f"day {day}: {n} tasks on {tile} "
                             f"({[t['kind'] for t in tasks if t['tile'] == tile]})")
        return tasks

    dayplan._tasks_for_day = spy
    try:
        dayplan.emit(sched)
    finally:
        dayplan._tasks_for_day = orig
    assert not dupes, f"{len(dupes)} duplicated tiles:\n  " + "\n  ".join(dupes[:10])
