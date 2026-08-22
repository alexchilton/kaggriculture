"""No unit is planned to PLACE on a tile before the pen is built there.

The dawn plan splits a pen's BUILD and its PLACE across two units and orders them wrongly.
Measured on the Victor grid, seed 11, day 0 -- the dawn `crew.cover` call, verbatim:

    u0: BUILD(2,4) PLACE(2,4) | BUILD(3,4) PLACE(3,4) | BUILD(4,4)
    u3: PLACE(4,4) | BUILD(4,3) PLACE(4,3) | BUILD(3,3) PLACE(3,3)

`(4,4)` is built by u0 as its FIFTH job and placed by u3 as its FIRST. PLACE on a tile with no pen
no-ops (`kaggriculture.py`), so the animal stays in the shed: five BUILDs, four PLACEs, and the grid
reads `place 4/5`, `sheep 3/4`, `feed 4/5`, `care 4/5` on d0 with every later day inheriting a herd
one head light.

`BUILD_THEN_PLACE` is already True, so the pin DOES carry the placement -- the failure is not that
the PLACE is missing, it is that nothing constrains the two jobs to the same unit or to an order.

The assertion is on the PLAN, not on the emitted ops, because the day is planned once at dawn: a
placement sequenced before its pen is a placement that cannot happen, whatever the walker does
later. Sequence position is compared per unit against the BUILD's position on its own unit; when
both land on the same unit the BUILD must simply come first.
"""
import collections
import kagg.plan as _PLAN
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top2/91854176.json"
SCHEDULE = _PLAN.SHIPPED_PLAN
TEAM = "Victor @ Tufa Labs"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAYS = 9
TPD = 24


@pytest.fixture(scope="module")
def dawn_plans():
    """`{day: {unit: [(tile, [op, ...]), ...]}}` for the FIRST `crew.cover` call of each day."""
    SA = importlib.import_module(MODULE)
    CREW = importlib.import_module("kagg.search.crew")
    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    plans, seen = {}, set()
    now = {"day": 0}
    real, strict = CREW.cover, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, *a, **kw):
        work, left = real(units, jobs, budget, *a, **kw)
        if now["day"] not in seen:
            seen.add(now["day"])
            plans[now["day"]] = {u: [(tuple(j.tile), [o for o, _i in j.ops]) for j in s]
                                 for u, s in work.items()}
        return work, left

    CREW.cover, CREW.STRICT_FEASIBILITY = spy, False
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            now["day"] = t // TPD
            o0 = env.state[0].observation
            a0, a1 = agent(o0), opp[t]
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        CREW.cover, CREW.STRICT_FEASIBILITY = real, strict
    return plans


def test_the_premise_some_dawn_plan_builds_and_places(dawn_plans):
    """Guard. If no plan in range contains both a BUILD and a PLACE this proves nothing."""
    days = [d for d, p in dawn_plans.items()
            if any("BUILD" in ops for s in p.values() for _t, ops in s)
            and any("PLACE" in ops for s in p.values() for _t, ops in s)]
    assert days, f"no dawn plan in d0-d{DAYS - 1} both builds and places; plans={list(dawn_plans)}"


@pytest.mark.parametrize("day", range(DAYS))
def test_no_placement_is_sequenced_before_its_pen_is_built(dawn_plans, day):
    """Every PLACE on a tile is preceded by the BUILD of that tile, on the same unit."""
    plan = dawn_plans.get(day)
    if not plan:
        pytest.skip(f"d{day} had no dawn plan")
    builds, places = {}, {}
    for u, seq in plan.items():
        for i, (tile, ops) in enumerate(seq):
            if "BUILD" in ops:
                builds.setdefault(tile, (u, i))
            if "PLACE" in ops:
                places.setdefault(tile, (u, i))
    bad = []
    for tile, (pu, pi) in places.items():
        if tile not in builds:
            continue                       # pen already standing; nothing to order against
        bu, bi = builds[tile]
        if pu != bu:
            bad.append(f"{tile}: BUILD on u{bu} step {bi}, PLACE on u{pu} step {pi} "
                       "-- different units, so nothing orders them")
        elif bi > pi:
            bad.append(f"{tile}: BUILD on u{bu} step {bi} AFTER its PLACE at step {pi}")
    assert not bad, f"d{day}\n" + "\n".join("  " + b for b in bad)
