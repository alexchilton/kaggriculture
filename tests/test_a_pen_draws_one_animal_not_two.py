"""A tour draws one animal per pen it fills, not two.

`BUILD_THEN_PLACE` builds the pen chain as `ops = [("BUILD", animal, ...)]` plus a later
`("PLACE", animal, ...)`, so the animal name appears on BOTH ops. `cover.DRAWN` contains "BUILD",
and `Job.needs` is `Counter(i for o, i in ops if i and o in DRAWN)` -- so each pen asks the shed for
two animals and `materialise` draws them.

`BUILD_PASTURE` takes nothing out of the shed (`kaggriculture.py:486-490`); it costs money and a
turn. `router.py:1258` already records this exact trap -- "PLACE only, never BUILD. BUILD is in
DRAWN and carries the animal name too" -- and guards its own supply check. `cover.Job.needs` was
never given the same guard.

Measured on the Victor grid, seed 11, day 0. The materialised routes, verbatim:

    u0  draw COW x2, SHEEP x2, WHEAT x2
        Shed -> (2,4)[BUILD] -> (2,4)[PLACE,FEED,CARE] -> (3,4)[BUILD] -> (3,4)[PLACE,FEED,CARE]
    u3  draw SHEEP x6, WHEAT x3
        Shed -> (4,4)[BUILD] -> (4,4)[PLACE,FEED,CARE] -> (4,3)[BUILD] -> ... -> (3,3)[PLACE,...]

Ten animals demanded for five pens, on a day whose row buys five (`COW 1, SHEEP 4`). The shed runs
dry before the last pen, its PLACE finds nothing in hand, and the day reads `place 4/5` with
`build_pasture 5/5` -- five pens standing, four filled -- taking `feed 4/5` and `care 4/5` with it.

The assertion is on the DRAW, per unit: animals drawn == PLACE ops in that unit's route. Not on the
`place` row, which is downstream and would pass for the wrong reason if some other cap moved.
"""
import collections
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
SCHEDULE = REPO / "data/seed_scripts/victor/schedule.json"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent_1455mh"
SEED = 11
DAYS = 9
TPD = 24
ANIMALS = ("COW", "SHEEP", "CHICKEN", "GOOSE", "PIG")


@pytest.fixture(scope="module")
def routes():
    """`{day: [(draw, n_places), ...]}` from the DAWN `cover.plan` of each day, per unit."""
    SA = importlib.import_module(MODULE)
    DP = importlib.import_module("kagg.search.cover")
    CREW = importlib.import_module("kagg.search.crew")
    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}

    out, seen = collections.defaultdict(list), set()
    now = {"day": 0}
    real, strict = DP.plan, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, *a, **kw):
        plan, unc = real(units, jobs, budget, *a, **kw)
        if now["day"] not in seen:
            seen.add(now["day"])
            for _u, st in sorted(plan.items()):
                draw = collections.Counter({k: v for k, v in (st.get("draw") or {}).items()
                                            if k in ANIMALS})
                places = sum(1 for step in st.get("route") or []
                             for o, _i in (getattr(step, "ops", None) or ())
                             if o == "PLACE")
                out[now["day"]].append((dict(draw), places))
        return plan, unc

    DP.plan, CREW.STRICT_FEASIBILITY = spy, False
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            now["day"] = t // TPD
            o0 = env.state[0].observation
            a0 = agent(o0)
            n0 = len(o0["farms"][0].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": ["PASS"], "hands": [], "market": []}])
    finally:
        DP.plan, CREW.STRICT_FEASIBILITY = real, strict
    return dict(out)


def test_the_premise_some_dawn_route_places_an_animal(routes):
    """Guard. With no placement anywhere in range the assertion below is vacuous."""
    total = sum(p for day in routes.values() for _d, p in day)
    assert total, f"no dawn route in d0-d{DAYS - 1} places an animal at all"


@pytest.mark.parametrize("day", range(DAYS))
def test_a_route_draws_exactly_one_animal_per_placement(routes, day):
    """Animals drawn by a tour == placements in that tour. A BUILD consumes nothing."""
    rows = routes.get(day)
    if not rows:
        pytest.skip(f"d{day} had no dawn plan")
    bad = []
    for u, (draw, places) in enumerate(rows):
        n = sum(draw.values())
        if n != places:
            bad.append(f"u{u}: draws {draw} = {n} animals for {places} placement(s)")
    assert not bad, f"d{day}\n" + "\n".join("  " + b for b in bad)
