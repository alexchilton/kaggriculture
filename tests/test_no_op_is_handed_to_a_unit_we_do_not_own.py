"""No op may be handed to a unit slot the farm does not own that day.

An agent submits `{"farmer": op, "hands": [op, ...]}` and the harness truncates the hand list to the
hands the farm actually has (`build_script_submission.py`, and the reference simply indexes
`hands_actions` against `farm["hands"]`). So an op written into slot 5 on a day with four hands is
not refused, not logged, and not visible in any op census taken off our own arrays -- it is
**dropped before the environment ever sees it**, and our accounting still counts it as emitted.

Measured with `scripts/where_do_we_think_we_are.py`, driving the tape's own schedule:

    day  0:   7 ops on slot [5]                 -- 5 WEST, 1 PLANT, 1 WATER
    day  9:  20 ops on slot [6]
    day 11:  95 ops on slots [5, 6, 7, 8, 9]    -- 13 FEED, 13 CARE, 13 COLLECT_FERTILIZER
    day 12:  28 ops on slots [7, 8]
    day 14:   9 ops on slot [9]
    day 26:  68 ops on slots [10, 11, 12]

That day-0 PLANT is the whole of `plants day 1: 16 against the tape's 17`. The emitter's own
report says 126 of 126 tile-plantings emitted, and it is right -- the op exists in the array. It just
went to a hand that was never hired.

The cause is one slice. `_assign` does:

    usable_units = [u for u in units if _can_leave(u, parcels)]
    for unit in usable_units[:max_hands]:

`_can_leave` correctly drops unit 3 -- it spawns on `(5,5)` in SE with both neighbours locked -- but
dropping it *shifts the slice up*, so a crew of five becomes slots `[0, 1, 2, 4, 5]`. A unit that
cannot leave its spawn has to be skipped, leaving the crew a worker short, not backfilled from a slot
the farm has not hired.
"""

import collections
import json
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TPD = R.TURNS_PER_DAY


@pytest.fixture(scope="module")
def emitted():
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    from kagg.search import dayplan

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, report = dayplan.emit(sched)
    return sched, np.asarray(script.unit_op)


def test_no_op_is_handed_to_a_unit_we_do_not_own(emitted):
    """Slot `u` is the farmer at 0 and hand `u` after that, so `u` must be <= that day's hands.

    Asserted against hires ORDERED rather than hands observed, which is the generous reading: a HIRE
    on a thin bank is itself a silent no-op, so the real crew can be smaller than this. If we fail
    even the generous bound the op was never going to be executed.
    """
    sched, op = emitted
    pass_op = R.OP["PASS"]
    lost = collections.defaultdict(list)
    for t in range(op.shape[0]):
        day = t // TPD
        limit = (sched.get(day, {}).get("hands", 0) or 0)      # highest legal slot index
        for u in range(limit + 1, op.shape[1]):
            if int(op[t, u]) != pass_op:
                lost[day].append((t, u))
    assert not lost, "ops written to unhired slots:\n  " + "\n  ".join(
        f"day {day}: {len(v)} ops on slots {sorted({u for _, u in v})}"
        for day, v in sorted(lost.items()))
