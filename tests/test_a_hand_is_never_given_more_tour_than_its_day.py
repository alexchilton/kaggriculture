"""A hand is never given more tour than its day can walk.

## The theory this test exists to prove

`cover.cover` returns early on any day in `PRECOMPUTED_ROUTES`, and `_apply_precomputed` seats the
solved stops **without pricing them** -- its own sibling docstring says so, at
`TRIM_HOME_DAYS`: "the reserve pricing cannot reach a precomputed day (`_apply_precomputed` seats
stops without pricing them)".

The greedy path cannot do this. `slot`/`claim` price every job against `budget[u]` before seating
it, and `_insert_leftovers` prices every insertion the same way. The solved path is the only one
that hands a unit a sequence nobody checked, and the day simply stops at turn 24 with the tail of
the tour unwalked.

**Nothing reports it.** `PRECOMPUTED_MISSES` records a stop the board could not FILL; it has no
entry for a stop that was seated and then never reached. So the day looks fully covered and is not.

## Why it is the strawberry defect

Measured on the gate's own season -- tape `kawashigi`, seed 11, `weedSpawnChance` 0.005, 30 days,
`data/logs/over_budget_kawashigi_s11.log` -- eleven WATER stops are planned past the turn budget,
and the tiles they name are the tiles that weed that night:

    d16  u6   budget 23  cost 28   WATER past the cut: (1,4) (0,4)   -> both weed at the end of d16
    d19  u12  budget 23  cost 25   WATER past the cut: (0,5)         -> weeds at the end of d19
    d26  u4   budget 23  cost 26   WATER past the cut: (6,2)         -> weeds at the end of d26
    d27  u10  budget 23  cost 25   WATER past the cut: (8,7)         -> weeds at the end of d27

STRAWBERRY is `ongoing: True`, so it must be watered every second day for the whole season or it
weeds (`reference/kaggriculture.py`, `_daily_refresh_plants`, `consecutive_unwatered >= 2`). A tile
at `consecutive_unwatered == 1` at dawn has no slack at all: the one water it is owed today is the
only thing between it and a WEED, and here that water is planned into turns the hand does not have.

`data/logs/who_overruns_s11.log` separates the two candidates. The cost of the SOLVED stops alone
is already over budget on every one of these days, before `_insert_leftovers` adds anything -- so
the insertion is innocent and the seating is the fault.

## What this test asserts, and what it deliberately does not

It asserts one thing: no unit is handed a tour costing more turns than it has. It says nothing
about which jobs should be dropped when the day is genuinely too full -- that is
`_insert_leftovers`' existing ordering (at-risk first, then required), and this test only makes
that ordering reachable.

    python -u -m pytest tests/test_a_hand_is_never_given_more_tour_than_its_day.py -q
"""
import importlib
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

SEED = 11
WEEDS = 0.005
DAYS = 30
TAPE = "kawashigi"
MODULE = "kagg.search.schedule_agent"


@pytest.fixture(scope="module")
def overruns():
    """`[(day, unit, budget, cost)]` for every tour planned longer than the unit's day.

    Built by wrapping `cover.plan`, so it observes the real season the acceptance gate runs rather
    than re-deriving any decision. Played ONCE for the module.
    """
    import breakdown as B

    from kagg.search import cover as C

    SA = importlib.import_module(MODULE)
    real_plan = C.plan
    rows, seen = [], set()

    def plan(units, jobs, budget, *a, **kw):
        out, left = real_plan(units, jobs, budget, *a, **kw)
        # One reading per (day, budget vector). `_router_acts` may call the planner more than once
        # in a day; the dawn plan is the one that decides the day, and a duplicate row would count
        # the same defect twice.
        key = (kw.get("day"), tuple(budget))
        if key not in seen:
            seen.add(key)
            for u, d in out.items():
                if d["cost"] > budget[u]:
                    rows.append((kw.get("day"), u, budget[u], d["cost"]))
        return out, left

    replay, schedule, team = B.TAPES[TAPE]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA
    C.plan = plan
    SA.DP.plan = plan
    try:
        opp = lambda: B.tape_policy(str(REPO / replay), team, 1)               # noqa: E731

        def ours():
            a = SA.make_agent(sched, 0)
            return lambda o, t: a(o)                                           # noqa: E731

        B.run(ours, opp, SEED, WEEDS, stop_day=DAYS + 1)
    finally:
        C.plan = real_plan
        SA.DP.plan = real_plan
    return rows


def test_no_hand_is_planned_a_tour_longer_than_its_turn_budget(overruns):
    """Exact, no tolerance. One turn over is one stop that silently does not happen."""
    detail = "\n".join(f"    d{d} u{u}: budget {b}, planned {c} ({c - b} turns over)"
                       for d, u, b, c in overruns)
    assert not overruns, f"{len(overruns)} tour(s) planned past the day:\n{detail}"
