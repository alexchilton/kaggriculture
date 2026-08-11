"""Seed for a crop is held before the day's plan first stands on a tile of that crop.

The day is planned ONCE at h0, and the route is a visit ORDER -- `_live_ops` re-derives the work from
the live board at each stop, and a stop that returns nothing is dropped **silently**. `_apply_unit_action`
refuses a PLANT outright when `private["seeds"].get(crop, 0) <= 0` (`kaggriculture.py:412`). So a unit
that reaches its tile before the seed is bought does not wait, does not come back, and leaves no trace:
the tile is simply never sown.

Seeds are bought dearest-BLOCK-first (`schedule_agent_1455mh.py:3971`, `-SEED_COST[crop] * qty`). That
rule was measured and TAKEN on 2026-08-07 and its docstring is right about what it was measured on --
under a thin bank, filling the dear block whole beats spreading. What it never consulted is **when the
plan needs each crop**, and on a day where those two orders disagree it funds the later crop first.

Measured on Victor's d10, seed 11 -- the first day the grid diverges after nine matching days:

    plan holds 23 PLANT stops   12 MELON + 11 STRAWBERRY
    emitted                     11 -- every STRAWBERRY, not one MELON

    first stop per crop   MELON  h2   (then h3 h4 h4 h5 h5 h6 h6 h8 h10 h13 h15)
                          STRAW  h5   (then h6 h7 h7 h7 h8 h8 h9 h10 h12 h15)
    seed arrives          MELON  h18  -- after the last melon stop, by three hours
                          STRAW  h2   -- before the first strawberry stop, by three

    block cost            STRAW  16 x $100 = $1,600   sorted FIRST
                          MELON  14 x  $80 = $1,120   sorted second, bank $46 by h2

The bank is $2,125 at dawn and $46 by h2: fourteen hires and the strawberry block take it, and melon
waits for melon revenue, which `LATE_SELL_BIAS` does not release until h16+. Victor's own row buys
`BUY_SEED MELON 5` at h1 and puts his strawberry at h12/h13/h15 -- need order, not price order.

This is not about which crop is worth more, and not about the total seed spend. Both rows are bought
in full by dusk (`buy_seed 31/31`). It is only about ORDER: a crop the plan walks past at h2 cannot be
funded at h18.

Three assertions, in order, because each is only meaningful if the one before it holds:

  1. **The premise.** The plan holds PLANT stops for more than one crop on the day under test, and the
     crops' first-need hours differ. With one crop, or with equal need hours, there is no ordering to
     get wrong and this file proves nothing -- fail loudly rather than pass for the wrong reason.
  2. Seed is held by the hour the plan first stands on that crop's tile.
  3. The day emits as many PLANT ops as the plan committed to.

It says nothing about WHICH crop should be planted -- the row names exact tiles -- nor about how much
seed to buy, only about the order the rows are offered in.
"""
import collections
import importlib
import json
import pathlib
import sys

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

REPLAY = REPO / "data/seed_scripts/top2/91854176.json"
SCHEDULE = REPO / "data/seed_scripts/victor/schedule.json"
TEAM = "Victor @ Tufa Labs"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
SEED = 11
DAYS = 12
TPD = 24
#: The first day the grid diverges, and the day the melon block is lost.
FOCUS_DAY = 10


@pytest.fixture(scope="module")
def season():
    """`{day: {crop: (first_need_hour, seed_hour, planned, emitted)}}`.

    `first_need_hour` is the earliest hour a unit stands on a tile the dawn plan holds a PLANT stop
    for, in that crop. `seed_hour` is the first hour `private["seeds"][crop]` is positive, or None.
    """
    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    DP = importlib.import_module("kagg.search.cover")

    raw = json.loads(SCHEDULE.read_text())
    sched = {int(k): v for k, v in raw.items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    plan_tiles = collections.defaultdict(lambda: collections.defaultdict(set))
    seen = set()
    now = {"d": 0}
    real = DP.plan

    def spy(units, jobs, budget, *a, **kw):
        out, unc = real(units, jobs, budget, *a, **kw)
        if now["d"] not in seen:
            seen.add(now["d"])
            for st in out.values():
                for n in (st.get("route") or []):
                    tile = getattr(n, "tile", None)
                    for o, item in getattr(n, "ops", []):
                        if o == "PLANT" and tile is not None:
                            plan_tiles[now["d"]][item].add(tuple(tile))
        return out, unc

    need = collections.defaultdict(dict)          # day -> crop -> hour
    seed_at = collections.defaultdict(dict)       # day -> crop -> hour
    emitted = collections.defaultdict(collections.Counter)

    DP.plan = spy
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            day, hour = t // TPD, t % TPD
            now["d"] = day
            o0 = env.state[0].observation
            a0 = agent(o0)                        # the h0 call is what populates `plan_tiles[day]`

            for crop, n in (o0["private"].get("seeds") or {}).items():
                if int(n) > 0:
                    seed_at[day].setdefault(crop, hour)
            f = o0["farms"][0]
            here = {(int(u[0]), int(u[1]))
                    for u in [f.get("farmer")] + list(f.get("hands") or []) if u}
            for crop, tiles in plan_tiles[day].items():
                if here & tiles:
                    need[day].setdefault(crop, hour)
            for h in a0["hands"]:
                if h and h[0] == "PLANT":
                    emitted[day][h[1]] += 1
            if a0["farmer"] and a0["farmer"][0] == "PLANT":
                emitted[day][a0["farmer"][1]] += 1

            n0 = len(f.get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": opp[t]["farmer"], "hands": list(opp[t]["hands"])[:n1],
                       "market": opp[t]["market"]}])
    finally:
        DP.plan = real

    return {day: {crop: (need[day].get(crop), seed_at[day].get(crop),
                         len(tiles), int(emitted[day][crop]))
                  for crop, tiles in plan_tiles[day].items()}
            for day in plan_tiles}


def test_the_premise_the_focus_day_plants_two_crops_it_needs_at_different_hours(season):
    """With one crop, or with equal need hours, there is no ordering to get wrong.

    If this fails the `11/23` on d10 has some other cause and the fix below would be built against a
    mechanism that is not there.
    """
    row = season.get(FOCUS_DAY) or {}
    assert len(row) > 1, f"d{FOCUS_DAY} plan holds one crop only: {row}"
    hours = {crop: v[0] for crop, v in row.items() if v[0] is not None}
    assert len(set(hours.values())) > 1, (
        f"d{FOCUS_DAY} needs every crop at the same hour {hours}; nothing to order")


@pytest.mark.parametrize("day", range(DAYS))
def test_the_seed_is_held_before_the_plan_stands_on_the_tile(season, day):
    row = season.get(day) or {}
    if not row:
        pytest.skip(f"d{day} plan holds no PLANT stop")
    late = {crop: (nh, sh) for crop, (nh, sh, _p, _e) in row.items()
            if nh is not None and (sh is None or sh > nh)}
    assert not late, (
        f"d{day} walks past ground it cannot sow: " + "; ".join(
            f"{crop} first stop h{nh}, seed at "
            + ("never" if sh is None else f"h{sh}") for crop, (nh, sh) in sorted(late.items()))
        + f". The plan holds {sum(v[2] for v in row.values())} PLANT stops and the day emits "
          f"{sum(v[3] for v in row.values())}. A stop with no seed is dropped silently -- the crop "
          f"rows are offered dearest-block-first, which is a price order, not the order the plan "
          f"needs them in.")


@pytest.mark.parametrize("day", range(DAYS))
def test_the_day_plants_what_the_plan_committed_to(season, day):
    row = season.get(day) or {}
    if not row:
        pytest.skip(f"d{day} plan holds no PLANT stop")
    short = {crop: (p, e) for crop, (_n, _s, p, e) in row.items() if e < p}
    assert not short, (
        f"d{day} plan holds " + ", ".join(f"{p} {crop}" for crop, (p, _e) in sorted(short.items()))
        + " and emits " + ", ".join(f"{e}" for _c, (_p, e) in sorted(short.items()))
        + ". The route reached the tiles; the seed was not there when it did.")
