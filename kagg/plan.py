"""Which recorded player's schedule we ship, in one place.

The path used to be written out longhand in 27 files -- 6 scripts and 21 tests -- so "which plan do
we play" was not a decision recorded anywhere, it was a string repeated until it looked like a fact.
Switching it meant 27 edits and any one of them missed left a harness measuring a plan the
submission does not run. That is exactly how a stale `--module` default spent a day measuring a
2026-08-09 agent.

**A schedule is a per-day target row, not a replay.** The agent plays all 30 days from these rows;
it does not replay anyone's actions. See `docs/architecture.md`.

Measured 2026-08-13, our agent on each plan against each tape, seed 11, weeds off, shop draw
injected from the recording:

    tape        plan        our final bank
    Victor      Victor            $112,402
    Victor      カワシギ           $115,477     +$3,075
    カワシギ     Victor             $56,940
    カワシギ     カワシギ           $112,026    +$55,086

His plan wins on both boards, so this is not a board-specific result. On his own board Victor's plan
goes broke by d4, misses the d6 land purchase, plays the season on 25 tiles against 50 and loses ten
animals to starvation at d12 -- none of which is an agent defect, all of which is a plan that does
not fit that board.

`data/` is gitignored, so these files are not recoverable from git. `scripts/extract_leader_schedule.py`
regenerates one from a downloaded replay.
"""
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent

#: **The plan the submission ships and every harness measures.** Change it here and nowhere else.
#: **`cheap_mix` was pointed here on 2026-08-26 and MEASURED AS A LOSS; reverted.** That arm was
#: `kawashigi`'s schedule with the winning lineage's crop mix and nothing else -- carrot 8 -> 20 in
#: their d11/d26 blocks, melon 20 -> 11, their d24 wheat burst, wheat held at 134. Against the pool
#: it moved the win rate not at all (95.0% both) and money -$3,269; against the three clone tapes
#: both arms lost 0/6, and it made `clone_late` $9,815 worse. The generator is kept at
#: `scripts/make_the_cheap_arm.py` so the arm can be re-run rather than re-argued, but nothing
#: points at it. Composition alone is not the gap.
SHIPPED_PLAN = REPO / "data/seed_scripts/kawashigi/schedule.json"

#: Kept reachable by name so an A/B has something to point `--schedule` at, and so the losing arm
#: of the table above can be re-run rather than re-argued.
PLANS = {
    "kawashigi": REPO / "data/seed_scripts/kawashigi/schedule.json",
    "victor": REPO / "data/seed_scripts/victor/schedule.json",
    "cheap_mix": REPO / "data/seed_scripts/cheap_mix/schedule.json",
}

#: Keys a schedule row carries that describe what the RECORDING did rather than what the agent
#: should do, and which every consumer strips before handing the row to `make_agent`. Duplicated in
#: `scripts/build_planner_submission.py` and `scripts/breakdown.py` before this module existed.
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def load(path=None, strip_tape_only=True):
    """The schedule as `{day: row}` with integer days, ready for `make_agent`."""
    import json

    raw = json.loads(pathlib.Path(path or SHIPPED_PLAN).read_text())
    rows = {int(day): row for day, row in raw.items()}
    if not strip_tape_only:
        return rows
    return {day: {k: v for k, v in row.items() if k not in TAPE_ONLY}
            for day, row in rows.items()}
