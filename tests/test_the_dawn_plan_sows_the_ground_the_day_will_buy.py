"""A land day's dawn plan sows the ground that day's own purchase unlocks.

The day is planned ONCE, at hour 0, and only walked thereafter. So the board the plan reasons about
must be the board the day will HAVE, not the board it starts with. That principle is already
implemented twice in this file for other ops -- `SELLS_FUND_THE_DAWN_PARCEL` tells the dawn plan that
the day's sells will pay for a parcel, and `HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS` makes a hire wait for
the squares that free it -- and it has never been applied to PLANT.

Measured on Victor's d10, seed 11, where the grid first diverges after nine matching days:

    day               d9          d10          d11          d12
    plant            2/1        11/23        21/11          7/8
    water          29/28        28/43        51/41        30/46
    melon            5/5         0/12        13/14        13/14
    work           77/74       94/117       117/97       96/113

His row is the one we execute, coordinates and all: `land 1`, `seeds {MELON 14, STRAWBERRY 16,
WHEAT 1}`, 23 `plant_tiles`. We buy the same seeds (`buy_seed 31/31`) and the same parcel
(`buy_land 1/1`, tiles 75/75 by dusk) and plant **11 of 23**. The twelve we miss are the melon, and
the melon is what the season is decided on: planted d10 it fills by d22, planted d11 it fills by d23,
and the opponent sells his flush into a $238 book on d20 while our vines are still filling. In ladder
game 91989194 that one day is $13,522 of a $14,810 loss.

The mechanism this file asserts is the LOCKED ground. `_process_market` runs after the unit phase
(`kaggriculture.py:922` then `:928`), so a parcel bought on d10 unlocks partway through d10 -- at h0
those squares still read `"LOCKED"` and no plant can be planned onto them.

Two assertions, in order, because the second is only meaningful if the first holds:

  1. **The premise.** Some of the row's own `plant_tiles` are LOCKED at dawn on the land day. If they
     are not, this whole explanation is wrong however real the `11/23` is, and the test must say so
     rather than pass for the wrong reason.
  2. The dawn plan covers as many plants as the row asks for.

This says nothing about WHERE a crop should go -- the row names exact tiles -- and nothing about days
with no `land` in the row, where the dawn board is already the whole board.
"""
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
#: The first day the grid diverges, and the only `land` day in range after the d6 parcel.
LAND_DAY = 10


@pytest.fixture(scope="module")
def dawn():
    """`{day: (plants_planned, plants_uncovered, locked_row_tiles)}` for each day's h0 plan."""
    SA = importlib.import_module("kagg.search.schedule_agent")
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
    now = {"d": 0, "h": 0, "locked": 0}
    real, strict = DP.plan, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, *a, **kw):
        out, unc = real(units, jobs, budget, *a, **kw)
        if now["h"] == 0 and now["d"] not in seen:
            seen.add(now["d"])
            planted = sum(1 for st in out.values() for n in (st.get("route") or [])
                          for o, _i in getattr(n, "ops", []) if o == "PLANT")
            missed = sum(1 for j in unc for o, _i in j.ops if o == "PLANT")
            got[now["d"]] = (planted, missed, now["locked"])
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
            if now["h"] == 0:
                tiles = o0["farms"][0]["tiles"]
                want = [tuple(c) for c, _crop in ((sched.get(now["d"]) or {}).get("plant_tiles") or [])]
                now["locked"] = sum(1 for (x, y) in want if tiles[y][x] == "LOCKED")
            a0, a1 = agent(o0), opp[t]
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        DP.plan, CREW.STRICT_FEASIBILITY = real, strict
    return {day: (p, m, lk, sched.get(day) or {}) for day, (p, m, lk) in got.items()}


def test_the_premise_the_land_days_row_names_ground_that_is_still_locked(dawn):
    """If nothing the row asks for is LOCKED at dawn, this file's explanation is wrong.

    It would mean the 11/23 has some other cause -- turn budget, seeds, routing -- and the fix below
    would be built against a mechanism that is not there. Fail loudly rather than pass silently.
    """
    planned, missed, locked, row = dawn[LAND_DAY]
    assert row.get("land"), f"d{LAND_DAY} row has no `land`; wrong day for this test"
    assert locked > 0, (
        f"d{LAND_DAY} buys a parcel and NONE of its {len(row.get('plant_tiles') or [])} plant_tiles "
        f"are LOCKED at h0. The dawn plan can already reach every square the row names, so the "
        f"locked-ground explanation for `plant {planned}/{len(row.get('plants') or [])}` is wrong.")


@pytest.mark.parametrize("day", range(DAYS))
def test_the_dawn_plan_covers_the_rows_plants(dawn, day):
    planned, missed, locked, row = dawn[day]
    want = len(row.get("plants") or [])
    if not want:
        pytest.skip(f"d{day} row asks for no plants")
    assert planned >= want, (
        f"d{day} row asks for {want} plants and the dawn plan covers {planned} "
        f"({missed} left uncovered). {locked} of the row's own plant_tiles read LOCKED at h0 -- the "
        f"parcel this day's `land {row.get('land')}` buys is what unlocks them, and the plan is "
        f"built before the purchase settles. The day is planned once, so ground that arrives later "
        f"is ground that is never sown.")
