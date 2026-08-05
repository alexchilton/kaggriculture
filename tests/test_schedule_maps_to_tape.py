"""Schedule in, tape out, asserted per day and per op. `schedule[day].x` must become `tape[day].y`.

Alex's framing, and it is the right unit: the season census in
`tests/test_the_emitter_reproduces_his_tape.py` says *that* we diverge, but a total of 115 PLANT
against his 131 does not say which day lost them. These assert the mapping itself, one row at a
time, so a failure names the day and the op.

The mapping the emitter owes, read straight off `data/seed_scripts/new_leader/schedule.json`:

    row["builds"] == n      ->  n BUILD_PASTURE ops on that day, and n PLACE ops
    row["plants"] == [...]  ->  one PLANT op per entry, of that crop, on that day
    row["land"]   == 1      ->  one BUY_LAND market order on that day
    row["hands"]  == n      ->  at most n HIRE orders at that day's dawn, and none after it

Nothing here is a threshold I chose; every right-hand side is a count off his replay.
"""

import collections
import json
import math
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TPD = R.TURNS_PER_DAY


@pytest.fixture(scope="module")
def sched():
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    return {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}


@pytest.fixture(scope="module")
def tape(sched):
    """`day -> Counter(op name)` for the tape our emitter produces from his schedule."""
    from kagg.search import dayplan

    script, report = dayplan.emit(sched)
    names = {v: k for k, v in R.OP.items()}
    per_day = collections.defaultdict(collections.Counter)
    crops_planted = collections.defaultdict(collections.Counter)
    op = np.asarray(script.unit_op)
    crop = np.asarray(script.unit_crop)
    for t in range(op.shape[0]):
        day = t // TPD
        for u in range(op.shape[1]):
            nm = names.get(int(op[t, u]), "PASS")
            if nm == "PASS":
                continue
            per_day[day][nm] += 1
            if nm == "PLANT":
                crops_planted[day][R.CROPS[int(crop[t, u])]] += 1
    return dict(script=script, report=report, per_day=per_day, crops=crops_planted)


# --------------------------------------------------------------------- one row, one assertion
def test_every_pen_he_builds_that_day_is_built_that_day(sched, tape):
    """`builds: 4` on day 0 means four BUILD_PASTURE ops on day 0, not four spread over four days.

    `ranch()` raised one pen per day per chain, so matching his day-0 herd took four chains and
    therefore four hands. A per-day assigner can put all four on one day; this is the test that says
    it did.
    """
    wrong = []
    for day, row in sorted(sched.items()):
        want = row.get("builds", 0)
        got = tape["per_day"][day]["BUILD_PASTURE"] + tape["per_day"][day]["BUILD_COOP"]
        if got != want:
            wrong.append(f"day {day}: {got} builds against his {want}")
    assert not wrong, "\n  " + "\n  ".join(wrong)


def test_every_animal_he_places_that_day_is_placed_that_day(sched, tape):
    """A pen with no animal in it is a turn spent and nothing earned."""
    wrong = []
    for day, row in sorted(sched.items()):
        want = len(row.get("places") or [])
        got = tape["per_day"][day]["PLACE"]
        if got < want:
            wrong.append(f"day {day}: {got} PLACE against his {want}")
    assert not wrong, "\n  " + "\n  ".join(wrong)


def test_every_tile_he_plants_that_day_is_planted_that_day(sched, tape):
    """131 plantings across 30 days, and the day matters: his day-26 wave is 31 tiles at once."""
    wrong = []
    for day, row in sorted(sched.items()):
        want = len(row.get("plants") or [])
        got = tape["per_day"][day]["PLANT"]
        if got < want:
            wrong.append(f"day {day}: {got} PLANT against his {want}")
    assert not wrong, "\n  " + "\n  ".join(wrong)


def test_he_plants_the_crop_the_schedule_names(sched, tape):
    """Not just the count -- the crop. Wheat and strawberry have different windows and prices, so
    planting the right number of the wrong thing is a different farm."""
    wrong = []
    for day, row in sorted(sched.items()):
        want = collections.Counter(row.get("plants") or [])
        got = tape["crops"][day]
        for crop, n in want.items():
            if got[crop] < n:
                wrong.append(f"day {day}: {got[crop]} {crop} against his {n}")
    assert not wrong, "\n  " + "\n  ".join(wrong[:12])


def test_land_is_bought_on_the_day_he_buys_it(sched, tape):
    """A PLANT on LOCKED ground is a silent no-op, so a parcel that arrives late costs the whole
    block its season and reports nothing."""
    buy_land = np.asarray(tape["script"].buy_land)
    wrong = []
    for day, row in sorted(sched.items()):
        want = row.get("land", 0)
        got = int(buy_land[day * TPD:(day + 1) * TPD].sum())
        if got != want:
            wrong.append(f"day {day}: {got} BUY_LAND against his {want}")
    assert not wrong, "\n  " + "\n  ".join(wrong)


def test_the_crew_is_hired_two_at_a_time_early_and_is_never_larger_than_his(sched, tape):
    """`hire[t]` is a COUNT of HIRE orders at turn `t`, and the ladder is walked once per order.

    Writing the crew size into all 24 turns of a day emitted 96 hires on day 0 instead of 4, climbed
    the Fibonacci ladder inside the day, and drained $3,000 to $76 before the farm existed -- the
    tape banked $0 with an empty crew all season. The hands are dismissed every night
    (`reference/kaggriculture.py:849`), so it must be re-issued each dawn.

    **This test used to demand "and only at dawn", and that half of it was wrong.** `_spawn_hand`
    (`kaggriculture.py:508`) picks the min-occupancy shed-access tile *at the moment the HIRE settles*,
    so a whole crew hired in one turn puts hand 3 on `(5,5)` -- SE, both neighbours locked, unable to
    move at all -- and every hand after it somewhere dead reckoning does not predict. Measured: every
    unit spent 139-505 turns on a tile the emitter did not believe in and 76 of 126 PLANT ops were
    silently refused. Two per turn is what makes the spawn tile predictable, and it is what the tape
    itself does: `[(1, 2), (2, 2), (3, 2)]` on day 1.

    So the assertion is now the cadence rather than the single turn: at most two orders in any turn, and
    all of them inside the first turns of the day, before the crew is needed.
    """
    hire = np.asarray(tape["script"].hire)
    wrong = []
    for day, row in sorted(sched.items()):
        dawn = int(hire[day * TPD]) if day * TPD < len(hire) else 0
        window = hire[day * TPD:(day + 1) * TPD]
        for h, n in enumerate(window):
            if int(n) > 2:
                wrong.append(f"day {day} hour {h}: {int(n)} HIRE orders in one turn; the third lands "
                             f"on (5,5) and cannot move")
        late = [h for h, n in enumerate(window) if int(n) and h > max(1, math.ceil(row.get("hires", 0) / 2))]
        if late:
            wrong.append(f"day {day}: HIRE at hours {late}, past the point the crew is needed")
        # Compared against HIRES ORDERED, not hands owned. On day 1 the tape issues 6 HIRE orders
        # and is only ever observed holding 4 hands: it is sitting on $42, and `_do_hire` returns
        # silently when `farm["money"] < cost`, so the last two no-op. Asserting `hires <= hands`
        # would forbid us from doing what the tape does -- over-order into a thin bank and let the
        # ladder truncate itself.
        if dawn > row.get("hires", 0):
            wrong.append(f"day {day}: hires {dawn} against the tape's {row.get('hires', 0)}")
    assert not wrong, "\n  " + "\n  ".join(wrong[:12])


def test_a_weeded_tile_is_dug_rather_than_abandoned(tape):
    """The farm was being eaten alive and nothing said so.

    Board census of our own tape in the real environment: WEED 9 on day 3, 17 on day 8, 20 on day 12,
    while PLANT fell 9 -> 2 -> 1 and the bank hit $8. A weed makes PLANT a silent no-op on that tile,
    so an un-dug tile is dead for the rest of the season and every op aimed at it is wasted. Neither
    `routines.py` nor the day planner has ever emitted a single DIG (open task #27); his tape emits
    25.
    """
    total = sum(c["DIG"] for c in tape["per_day"].values())
    assert total > 0, "not one DIG in 720 turns; a weeded tile is dead ground for the season"
