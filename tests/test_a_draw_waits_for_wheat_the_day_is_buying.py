"""A depot draw short of stock the day is still buying waits, it does not throw the want away.

`_router_acts` walks a depot stop and takes `min(node.pick[item], shed[item])`. A partial draw leaves
the remainder owed -- `node.pick[item] -= take` -- so the unit is free to top up on the next turn.
But if the next turn's shed reads zero, an ordinary draw deletes the want outright and the stop is
finished. That is deliberate: standing and retrying EVERY momentary shortfall was measured to regress
day 4's land purchase and day 5's sell-slot ordering, and most shortfalls are not an animal about to
starve.

`WAIT_FOR_THE_MORNING_DELIVERY` already carves out the one case where waiting is certain to pay --
an item the day's own row is buying, at hour 0, when nothing bought can be in the shed yet because
the unit phase runs before `_process_market`. The same argument holds at every other hour of a day
whose row is still buying: the drip has not finished, the wheat IS coming, and one turn of waiting is
cheaper than a pen going unfed.

Measured on Victor's d7, seed 11. The dawn plan is correct and complete -- `FEED 10`, `CARE 10`,
`uncovered: []`, with draws to match:

    u0   3 FEED stops   needs {WHEAT 3}            depot picks {WHEAT 3}
    u1   4 FEED stops   needs {WHEAT 4, COW 2}     depot picks {WHEAT 4, COW 2}
    u4   3 FEED stops   needs {WHEAT 3, COW 1}     depot picks {WHEAT 3, COW 1}

Ten draws for ten feeds. What is actually drawn is `u0 3, u1 4, u4 2` -- nine. u4 asks for WHEAT x2
at h05 because the shed holds exactly 2 at that moment; the third is owed, the next turn reads an
empty shed, and the want is deleted. The day buys fourteen wheat and the third ration arrives hours
later with nobody coming back for it. `feed 9/10`, `care 9/10` -- CARE mirrors it because
`animal_ops` offers CARE only on a pen it is feeding -- and `collect_fert 6/7` is the same tour
running out of day.

The assertion is that the day emits as many FEEDs as its own dawn plan committed to. It says nothing
about how many the plan should contain, which is `test_the_herd_is_fed_on_the_tapes_cadence`'s
question, and nothing about days whose plan is already short.
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
def played():
    """`{day: (feeds_planned_at_dawn, feeds_emitted)}` for our seat."""
    SA = importlib.import_module("kagg.search.schedule_agent")
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
            planned[now["d"]] = sum(1 for st in out.values() for n in (st.get("route") or [])
                                    for o, _i in getattr(n, "ops", []) if o == "FEED")
        return out, unc

    DP.plan, CREW.STRICT_FEASIBILITY = spy, False
    emitted = collections.Counter()
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
            for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
                if a and a[0] == "FEED":
                    emitted[now["d"]] += 1
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        DP.plan, CREW.STRICT_FEASIBILITY = real, strict
    return {day: (planned.get(day, 0), emitted[day]) for day in planned}


def test_the_premise_some_dawn_plan_commits_to_a_feed(played):
    """Guard. With no planned FEED anywhere the assertion below is vacuous."""
    assert any(p for p, _e in played.values()), "no dawn plan in range committed to a FEED"


@pytest.mark.parametrize("day", range(DAYS))
def test_the_day_emits_every_feed_its_plan_committed_to(played, day):
    want, got = played[day]
    if not want:
        pytest.skip(f"d{day} planned no FEED")
    assert got >= want, (
        f"d{day} dawn plan committed to {want} FEEDs and the day emitted {got}. A depot draw short "
        "of wheat the day is still buying deletes the want instead of waiting for the delivery.")
