"""Which recorded player's schedule we ship, in one place.

The path used to be written out longhand in 27 files -- 6 scripts and 21 tests -- so "which plan do
we play" was not a decision recorded anywhere, it was a string repeated until it looked like a fact.
Switching it meant 27 edits and any one of them missed left a harness measuring a plan the
submission does not run. That is exactly how a stale `--module` default spent a day measuring a
2026-08-09 agent.

**A schedule is a per-day target row, not a replay.** The agent plays all 30 days from these rows;
it does not replay anyone's actions. See `docs/architecture.md`.

**KAWASHIGI AND VICTOR ARE GONE FROM THIS BRANCH, 2026-08-26.** Alex: *"remove all kawa from the
whole fucking repo branch"*. The clone lineage pairs a per-arm TAPE with a per-arm SCHEDULE, and the
kawashigi branches overwrote that pairing at runtime -- `melon_branch.install()` replaced the entire
schedule with an embedded row set on a d3 opponent signal, so the agent played kawashigi's season
while being measured against the clone tape. The shipped `main_baseline.py` carried it and scored
1243.8 against the older artifact's 1630.6.

`data/` is gitignored, so these files are not recoverable from git. `scripts/extract_leader_schedule.py`
regenerates one from a downloaded replay.
"""
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent

#: **The plan the submission ships and every harness measures.** Change it here and nowhere else.
#: One of the three clone arms; `build_planner_submission.REPLAY_ARMS` picks per arm at the latch.
SHIPPED_PLAN = REPO / "data/seed_scripts/clone_open/schedule.json"

#: The three clone arms, reachable by name so an A/B has something to point `--schedule` at.
PLANS = {
    "clone_open": REPO / "data/seed_scripts/clone_open/schedule.json",
    "clone_yarn3": REPO / "data/seed_scripts/clone_yarn3/schedule.json",
    "clone_yarn6": REPO / "data/seed_scripts/clone_yarn6/schedule.json",
}

#: Keys a schedule row carries that describe what the RECORDING did rather than what the agent
#: should do, and which every consumer strips before handing the row to `make_agent`. Duplicated in
#: `scripts/build_planner_submission.py` and `scripts/breakdown.py` before this module existed.
#:
#: **`orders` was removed from this tuple on 2026-08-26.** It held the recording's turn-level action
#: stream, and stripping it made the HOUR on every SELL unreachable -- a module constant
#: (`LATE_SELL_BIAS` / `LATE_SELL_FROM_HOUR = 16`) decided the sell time instead, so across the
#: three clone arms 260 of `clone_open`'s 591 sell orders could never fire at the hour the row asks.
#: The row is the driver; the clock is not.
#:
#: **The "target sheet, not a tape" rule still binds and is now enforced where it belongs.** It is a
#: rule about what the AGENT does, not about which keys travel with a row -- roughly 150 scripts and
#: tests open-code this strip, so a key removed here reaches all of them and a key added here
#: reaches none. `sell_by_hour` below is the only view of `orders` the agent may take: SELL entries
#: only, no unit, no position, no HIRE, land or seed action. Pinned by
#: `tests/test_a_sell_is_offered_at_the_hour_the_row_asks_for_it.py`.
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns")


def sell_by_hour(row):
    """`{product: [[hour, qty], ...]}` -- WHEN the row's day totals are meant to be sold.

    **This is a target sheet, not a tape, and the distinction is the whole point.** `orders` is the
    recording's turn-level action stream and is stripped by `TAPE_ONLY` so no artifact ever replays
    his HIREs, land buys or seed purchases. Its SELL entries are different in kind: `sells` already
    ships the day total for each product, and this resolves that same total by hour. Nothing here
    says which unit acts or where it stands.

    It exists because the hour was previously unreachable. `LATE_SELL_BIAS` / `LATE_SELL_FROM_HOUR`
    held every offer to h16 from a module constant while the row carried an hour on every order, so
    the data was dead: across the three clone arms every one of 28 days carries sell orders spread
    over all 24 hours, and for `clone_open` **260 of 591 fall before h16**.

    Measured d12 of `clone_open`, seed 123641874, handover d12 -- the dawn shed is HIS shed exactly,
    because d0-d11 is his tape replayed verbatim:

        hour   our shed FERT   his shed FERT   row asks
           0        15              15
           1        15              15          SELL FERTILIZER 8
           2        15               6          SELL FERTILIZER 8, SELL FERTILIZER 1
           3        14               0          SELL FERTILIZER 3
          16        20               0          (our first offer of the day)

    He clears it from stock already sitting in the shed. Nothing had to be fetched, carried or
    dropped -- the day simply declined to sell, and banked $941 against his $4,178.

    Returns `None` when the row carries no `orders`, which is how a caller distinguishes "this
    schedule has no timing" from "this day sells nothing".
    """
    orders = (row or {}).get("orders")
    if not orders:
        return None
    out = {}
    for o in orders:
        if len(o) > 3 and o[1] == "SELL" and o[3]:
            out.setdefault(o[2], []).append([int(o[0]), int(o[3])])
    for v in out.values():
        v.sort()
    return out


def thin(row):
    """One row with `TAPE_ONLY` stripped, ready for `make_agent`.

    Prefer this to open-coding the comprehension. Roughly 150 scripts and tests still open-code it,
    which is why `TAPE_ONLY` may only ever SHRINK safely: removing a key reaches every call site,
    adding a derived one reaches none of them.
    """
    return {k: v for k, v in (row or {}).items() if k not in TAPE_ONLY}


def load(path=None, strip_tape_only=True):
    """The schedule as `{day: row}` with integer days, ready for `make_agent`."""
    import json

    raw = json.loads(pathlib.Path(path or SHIPPED_PLAN).read_text())
    rows = {int(day): row for day, row in raw.items()}
    if not strip_tape_only:
        return rows
    return {day: thin(row) for day, row in rows.items()}
