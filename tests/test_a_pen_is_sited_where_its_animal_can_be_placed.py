"""A pen the day means to fill is sited where the same day can reach it.

`_refresh_pins` sites a pen through a ladder: `PEN_SPOTS` (empty), then the four shed-access cells,
then `_nearest_ground` -- but only from `PEN_NEAREST_DEPOT_FROM_DAY` -- and finally `_next_ground`,
the field sweep. The sweep's job is to keep a CROP block compact; it knows nothing about a pen being
a fixed daily round trip, so before that day-gate the pens land wherever the sweep happens to be.

Measured on Victor's d8, seed 11. Both boards are identical at dawn -- 7 free squares, 33 crops --
and the row asks for `builds 2, places ['COW', 'COW']`. We pin `(0,3)` and `(9,2)`: opposite corners
of the board. u1 starts on `(5,4)`, walks to `(9,2)`, gets the BUILD in as the last stop of its tour,
and the chained PLACE has no turns left:

    UNCOVERED: [(0,2)['WATER','HARVEST','PLANT'], (9,2)['BUILD'], (9,2)['PLACE','FEED','CARE']]

`place 1/2`, and `cow 7/8` for the rest of the season.

The tape grows its pens outward from the shed ring as a block -- d6 `(5,4) (6,4)`, d7 `(5,3) (5,2)`,
d8 `(6,3) (7,4)` -- and builds and places on CONSECUTIVE turns with one unit: d8 h05 BUILD `(6,3)`,
h06 PLACE `(6,3)`, h11 BUILD `(7,4)`, h12 PLACE `(7,4)`. No walking between the two halves at all.

`PEN_NEAREST_DEPOT_FROM_DAY` already encodes this rule and is set to 11. Its own docstring records a
sweep -- None/11/12/13/9 -- in which 9 was rejected because it made the d10 land purchase LATE and
cost the quadrant. That measurement predates the dawn plan learning to predict a sales-funded parcel,
after which d10's bank is $5,230 where it was $3,719, so the reason to hold the gate at 11 is worth
re-testing rather than assumed.

The assertion is that the dawn plan does not leave a PLACE uncovered on a day whose row asks for one.
It says nothing about WHERE a pen should go -- only that wherever it goes must be reachable by the
plan that puts an animal in it. A day that runs out of animals, or asks for no placement, is skipped.
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
SEED = 11
DAYS = 12
TPD = 24


@pytest.fixture(scope="module")
def dawn():
    """`{day: (planned_places, uncovered_places, row)}` for the first `cover.plan` call of each day."""
    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    DP = importlib.import_module("kagg.search.cover")
    CREW = importlib.import_module("kagg.search.crew")

    raw = json.loads(SCHEDULE.read_text())
    sched = {int(k): v for k, v in raw.items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    got, seen = {}, set()
    now = {"d": 0, "h": 0}
    real, strict = DP.plan, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, *a, **kw):
        out, unc = real(units, jobs, budget, *a, **kw)
        if now["h"] == 0 and now["d"] not in seen:
            seen.add(now["d"])
            placed = sum(1 for st in out.values() for n in (st.get("route") or [])
                         for o, _i in getattr(n, "ops", []) if o == "PLACE")
            missed = [(tuple(j.tile), [o for o, _i in j.ops]) for j in unc
                      if any(o == "PLACE" for o, _i in j.ops)]
            got[now["d"]] = (placed, missed)
        return out, unc

    DP.plan, CREW.STRICT_FEASIBILITY = spy, False
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            now["d"], now["h"] = t // TPD, t % TPD
            o0 = env.state[0].observation
            a0, a1 = agent(o0), opp[t]
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        DP.plan, CREW.STRICT_FEASIBILITY = real, strict
    return {day: (p, m, sched.get(day) or {}) for day, (p, m) in got.items()}


def test_the_premise_some_day_plans_a_placement(dawn):
    """Guard. With no PLACE anywhere in range this file proves nothing."""
    assert any(p for p, _m, _r in dawn.values()), "no dawn plan in range contains a PLACE"


@pytest.mark.parametrize("day", range(DAYS))
def test_no_placement_is_stranded_on_ground_the_day_cannot_reach(dawn, day):
    placed, missed, row = dawn[day]
    if not (row.get("places") or []):
        pytest.skip(f"d{day} asks for no placement")
    if not missed:
        return
    assert not missed, (
        f"d{day} row places {row.get('places')}, the dawn plan covers {placed} and leaves "
        f"{missed} uncovered. A pen sited past the crew's reach is an animal that stays in the shed: "
        "the tape grows its pens outward from the shed ring and builds then places on consecutive "
        "turns with one unit.")
