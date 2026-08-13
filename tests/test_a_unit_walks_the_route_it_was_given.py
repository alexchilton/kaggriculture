"""A unit's first stop is the first stop its dawn route names.

The day is planned once and the route is a visit ORDER. If the executor reaches the stops in a
different order it pays walks the cost model never charged, and the tail of the tour falls off the
end of the day -- silently, because a stop that returns nothing is dropped rather than reported.

Measured on the Victor grid, seed 11, day 4. The plan for u0, cost 21 against a budget of 24:

    Shed(4,4)[WHEAT x2] -> (2,4)[FEED,CARE,COLLECT] -> (3,4)[FEED,CARE,COLLECT]
                        -> (1,4)[WATER] -> (2,3)[WATER] -> (0,4)[WATER,HARVEST]

u0 begins the day standing on (4,4), which IS the depot -- the draw costs one turn and no walking.
What it actually walked:

    h00 (4,4) NORTH      <- steps off the shed
    h01 (4,3) SOUTH      <- and back
    h02 (4,4) WEST
    h03 (3,4) WEST
    h04 (2,4) COLLECT_FERTILIZER
    h05 (2,4) EAST
    h06 (3,4) EAST
    h07 (4,4) PICKUP WHEAT 2   <- the depot stop, walked back to, four stops late
    h08 (4,4) WEST
    h09 (3,4) WEST
    h10 (2,4) FEED

Ten turns for one op. The depot was planned FIRST and taken FOURTH, so (2,4) is visited twice and
the walk between them is paid twice. The tail job (0,4) is never reached: `water 14/15` and
`harvest 4/5` are the same dropped stop, and the wheat tile it should have cleared stays standing,
which is what leaves d5 without ground for its fifth plant.

The h00 NORTH / h01 SOUTH pair is `_clear_the_spawn_ring` stepping the farmer off the ring so hires
land on usable squares. That is deliberate and is not what this asserts -- the farmer is allowed to
spend a turn on it. What it must not do is lose its place in the route.

The assertion is on the FIRST stop only. It is the narrowest statement that catches this: a unit
that starts its tour at the wrong stop has already paid the wrong walk, and everything after
inherits it.
"""
import collections
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top2/91854176.json"
SCHEDULE = REPO / "data/seed_scripts/victor/schedule.json"
TEAM = "Victor @ Tufa Labs"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAYS = 8
TPD = 24
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


@pytest.fixture(scope="module")
def walked():
    """`{day: {unit: (planned_first_tile, actual_first_tile, trace)}}` for the dawn route."""
    SA = importlib.import_module(MODULE)
    DP = importlib.import_module("kagg.search.cover")
    CREW = importlib.import_module("kagg.search.crew")
    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    planned, seen = {}, set()
    now = {"d": 0, "h": 0}
    real, strict = DP.plan, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, *a, **kw):
        out, unc = real(units, jobs, budget, *a, **kw)
        if now["h"] == 0 and now["d"] not in seen:
            seen.add(now["d"])
            planned[now["d"]] = {u: (tuple(st["route"][0].tile) if st.get("route") else None)
                                 for u, st in out.items()}
        return out, unc

    DP.plan, CREW.STRICT_FEASIBILITY = spy, False
    acted = collections.defaultdict(dict)
    trace = collections.defaultdict(lambda: collections.defaultdict(list))
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            now["d"], now["h"] = t // TPD, t % TPD
            o0 = env.state[0].observation
            farm = o0["farms"][0]
            pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
            a0, a1 = agent(o0), opp[t]
            n0 = len(farm.get("hands") or [])
            for u, act in enumerate([a0["farmer"]] + list(a0["hands"] or [])[:n0]):
                if not act or u >= len(pos):
                    continue
                trace[now["d"]][u].append(f"h{now['h']:02d} {pos[u]} {act[0]}")
                if act[0] not in MOVES and act[0] != "PASS" and u not in acted[now["d"]]:
                    acted[now["d"]][u] = pos[u]
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        DP.plan, CREW.STRICT_FEASIBILITY = real, strict

    return {day: {u: (planned.get(day, {}).get(u), acted[day].get(u), trace[day][u])
                  for u in planned.get(day, {})}
            for day in planned}


def test_the_premise_units_are_given_routes(walked):
    """Guard. If no unit has a planned first stop the assertion below is vacuous."""
    n = sum(1 for day in walked.values() for p, _a, _t in day.values() if p)
    assert n, "no unit in d0-d7 was given a dawn route at all"


@pytest.mark.parametrize("day", range(DAYS))
def test_the_first_stop_walked_is_the_first_stop_planned(walked, day):
    """The tile where a unit first works is the tile its route names first."""
    rows = walked.get(day)
    if not rows:
        pytest.skip(f"d{day} had no dawn plan")
    bad = []
    for u, (want, got, trace) in sorted(rows.items()):
        if want is None or got is None:
            continue
        if tuple(want) != tuple(got):
            bad.append(f"u{u}: route starts at {tuple(want)}, first worked {tuple(got)}\n"
                       + "\n".join("        " + line for line in trace[:12]))
    assert not bad, f"d{day}\n" + "\n".join("    " + b for b in bad)
