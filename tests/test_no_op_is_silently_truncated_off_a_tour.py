"""A task counted as done must have all of its ops in the tape. `seq[:cap]` may never cut anything.

This is the worst failure shape in the project, because the report actively lies. `_assign` appends a
task's ops to `seq`, appends the task to `done`, and then at the end does

    seq = seq[:cap]

so if the tour overran the day the tail is discarded **after** the task was counted. `emit()` then
reports `tasks: 21, done: 21, refused: none` for a day where two of four pens were never fed or cared
for. Every op census taken off our own arrays agrees with the tape's total, and the farm is different.

Measured on day 0, at the tape's own schedule -- all four pens went to unit 0, whose tour needs more than
23 turns:

    u0: .. PICK:W PICK:C NORTH BUILD PLAC:C FEED CARE SOUTH PICK:S NORTH NORTH BUILD PLAC:S FEED CARE
        SOUTH SOUTH PICK:C WEST BUILD PLAC:C FEED            <- day ends here, the third CARE is gone
    u4: .. NORTH WEST WEST WEST WEST PL:WHE WATER NORTH PL:WHE WATER PASS PASS PASS ... <- idle 12 turns

CARE landed twice against the tape's six and FEED three times against four, while a hand sat idle for
half the day. Idle capacity and dropped work in the same hour is the assignment failure this module was
written to fix, and truncation is how it came back invisibly.

The immediate cause was a cost-model omission: animals are drawn on a detour back to the shed at their
own stop (so the PICKUP lands after the purchase settles), and `_cost` did not charge for that walk. The
packer therefore accepted a tour it could not finish. But the omission is not the defect -- the silent
cut is. Any future under-estimate has to surface as a refusal the caller can count, which is the same
contract `claim()` and the land gate already honour.
"""

import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")


@pytest.fixture(scope="module")
def report():
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    from kagg.search import dayplan

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    return rep


def test_no_op_is_silently_truncated_off_a_tour(report):
    """`emit()` must report every op it dropped. Zero is the only passing value.

    Asserted on a count the emitter publishes rather than reconstructed here, so the number cannot drift
    away from what the packer actually did.
    """
    cut = report.get("truncated")
    assert cut is not None, (
        "emit() does not report truncated ops at all; a dropped op is invisible by construction")
    assert not cut, ("ops cut off the end of a tour after being counted as done:\n  "
                     + "\n  ".join(f"day {d}: {n} ops" for d, n in sorted(cut.items()))[:1200])


def test_a_hand_does_not_idle_while_another_overruns(report):
    """The other half of the same failure: work piled onto one unit while a hand had turns spare.

    Day 0 put all four pens on unit 0 and left unit 4 idle for twelve turns. A tour that does not fit is
    only a problem because the work had somewhere else to go.
    """
    over = []
    for row in report.get("days") or []:
        spare = row.get("idle_turns")
        if spare is None:
            continue
        if row.get("truncated") and spare > 0:
            over.append(f"day {row['day']}: {row['truncated']} ops cut with {spare} turns idle")
    assert not over, "\n  " + "\n  ".join(over[:10])
