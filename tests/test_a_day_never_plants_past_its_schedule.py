"""The schedule is a CEILING on everything the day acquires, not a suggestion.

Alex, 2026-08-10: *"hard constraint on max buys and pens and everything from the schedule d5 and 6
and onwards"*.

Measured, the ceiling already holds on every quantity -- plants, pens, land, feed, animals and
seed are each exactly on the schedule's cumulative row or under it through d9.  What looked like
over-acquiring in the grid (`pen 9/8`, `crop_MELON 11/6` on d6) is the REPLAYED tape delivering
less than its own schedule asks for, not us delivering more.  So this file is a guard rather than
a fix: it fails the moment any path starts acquiring past the plan.

Cumulative, not per-day.  A pen the schedule ordered on d5 that the crew could not reach until d6
is late, not extra, and a per-day cap would delete real backlog -- which is exactly what a
per-day seed cap did when it was tried: byte-identical on d0-d6 and -$2,682 by d16.

Read against `TAPES["seb"]` (90494364), the same tape as the day-matching gate.  Written down
because the first draft of this file measured against `91422988` instead, and a ceiling test read
off the wrong ceiling passes for no reason at all.
"""
import collections
import importlib
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
SEED, WEEDS, TPD, DAYS = 11, 0.0, 24, 7
MODULE = "kagg.search.schedule_agent"
TAPE = "seb"

#: The acquisitions, and the schedule key that caps each.  `builds` is counted from the emitted
#: BUILD ops rather than the pen count on the board, so a pen the env refuses still counts against
#: the ceiling -- the constraint is on what the day TRIES to acquire.
ACQUIRED = (
    ("builds", "builds", ("BUILD_PASTURE", "BUILD_COOP")),
    ("land", "land", ("BUY_LAND",)),
    ("feed", "buys", ("BUY_PRODUCT",)),
    ("animals", "animals_bought", ("BUY_ANIMAL",)),
    ("seed", "seeds", ("BUY_SEED",)),
)


def _ceiling(sched, key, day):
    """The schedule's CUMULATIVE allowance for `key` through `day`.

    The rows are shaped three ways -- an int (`builds`, `land`), a dict of item to count (`buys`,
    `seeds`, `animals_bought`) and a list (`plants`) -- so the total is taken by shape, not by name.
    """
    total = 0
    for d in sorted(sched):
        if d > day:
            break
        v = sched[d].get(key) or 0
        total += sum(v.values()) if isinstance(v, dict) else (len(v) if isinstance(v, list)
                                                              else int(v))
    return total


@pytest.fixture(scope="module")
def measured():
    """`(plants_by_day, acquisitions_by_day, sched)` -- what the day emits, against its plan.

    Driven through `breakdown.run` so this counts the same agent against the same opponent as the
    day-matching gate.  A private harness written for this question read a different opponent and
    reported crop counts a whole day out of step with the grid.

    Emitted rather than landed on purpose: a plant or a build the env refuses still spent what it
    was given, and the ceiling is on what the day tries to do.
    """
    import breakdown as B

    replay, schedule, team = B.TAPES[TAPE]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA = importlib.import_module(MODULE)
    CREW = importlib.import_module("kagg.search.crew")

    plants = collections.defaultdict(collections.Counter)
    unit_ops = collections.defaultdict(collections.Counter)

    def ours():
        a = SA.make_agent(sched, 0, router=True)

        def f(o, t):
            act = a(o)
            n0 = len(o["farms"][0].get("hands") or [])
            for op in [act["farmer"]] + list(act["hands"] or [])[:n0]:
                if not op:
                    continue
                if op[0] == "PLANT":
                    plants[t // TPD][op[1]] += 1
                unit_ops[t // TPD][op[0]] += 1
            return act
        return f

    was = CREW.STRICT_FEASIBILITY
    CREW.STRICT_FEASIBILITY = False
    try:
        # `ops` carries the market rows as EXACT FILLS from `kagg/analysis/fills.py`; `unit_ops`
        # carries the build ops, which the market never sees. Neither is inferred from the board.
        _days, ops = B.run(ours, lambda: B.tape_policy(str(REPO / replay), team, 1), SEED, WEEDS,
                           stop_day=DAYS + 1)
    finally:
        CREW.STRICT_FEASIBILITY = was

    acquired = collections.defaultdict(collections.Counter)
    for day in range(DAYS):
        for name, _key, op_names in ACQUIRED:
            src = unit_ops if name == "builds" else ops
            acquired[day][name] = sum(src[day][o] for o in op_names)
    return dict(plants), dict(acquired), sched


@pytest.mark.parametrize("day", range(DAYS))
def test_no_crop_is_planted_past_what_the_schedule_has_asked_for(measured, day):
    plants, _acquired, sched = measured

    allowed = collections.Counter()
    for d in sorted(sched):
        if d <= day:
            allowed.update(sched[d].get("plants") or [])

    got = collections.Counter()
    for d in range(day + 1):
        got.update(plants.get(d, {}))

    over = {c: (got[c], allowed[c]) for c in got if got[c] > allowed[c]}
    assert not over, (
        f"day {day}: planted past the schedule (ours / rows through d{day}): "
        + ", ".join(f"{c} {a}/{b}" for c, (a, b) in sorted(over.items()))
    )


@pytest.mark.parametrize("day", range(DAYS))
def test_nothing_is_acquired_past_what_the_schedule_has_asked_for(measured, day):
    """Pens, land, feed, animals and seed, cumulatively, against their rows."""
    _plants, acquired, sched = measured

    over = []
    for name, key, _ops in ACQUIRED:
        got = sum(acquired.get(d, {}).get(name, 0) for d in range(day + 1))
        cap = _ceiling(sched, key, day)
        if got > cap:
            over.append(f"{name} {got}/{cap}")

    assert not over, (
        f"day {day}: acquired past the schedule (ours / rows through d{day}): " + ", ".join(over)
    )
