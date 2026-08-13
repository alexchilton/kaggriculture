"""A one-shot harvest frees its tile, and the dawn plan has to count that as plantable ground.

Same argument as `_land_this_turn`, on a different asset: **the board the plan reasons about must be
the board the day will have.** A parcel bought at h13 is invisible to a plan built at h0 unless the
plan is told; so is a tile that this day's own HARVEST is going to clear.

`HARVEST` on a one-shot crop sets the cell to `None` (`kaggriculture.py:454-455`,
`if not crop_data["ongoing"]: farm["tiles"][fy][fx] = None`). On an ongoing crop, and on a PASTURE or
COOP, it does not -- it is a collection, not a demolition. Only the first kind makes room.

Measured on the Victor grid, seed 11, day 8. The two boards are IDENTICAL at dawn -- 33 crops in the
same states, 10 pens, 50 tiles, so 7 free squares each:

    row      2 builds + 10 plants = 12 placements wanted
    tape     harvests 6 during the day, plants 10, waters 22
    ours     dawn plan: BUILD 2, PLANT 5, WATER 11   (7 free - 2 builds = exactly 5)

The plan is capped at the ground standing free at dawn. Five of the ten seeds are never planned, and
`water 17/22` is downstream of it rather than a watering defect at all: a new plant starts at
`consecutive_unwatered = 1` (`reference/kaggriculture.py:209`), so each of his ten plants needs a
water the same day. His 22 = 11 in-window yields + 10 new plants + 1 standing brink tile. Every one
of his waters is at the brink or inside a yield window; NONE is a top-up of a safe tile, which is
what the `TOP_UP_SAFE_TILES` arm would have added and is why that arm is not the answer here.

The assertion is on the DAWN PLAN and on the node, not on which tile gets which seed: a stop that
harvests a one-shot crop must also carry the PLANT that the cleared tile can take, while the day's
row still wants seeds. Which crop goes in is the schedule's business, and where the seeds go once
the ground exists is the router's.
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
DAYS = 12
TPD = 24


@pytest.fixture(scope="module")
def dawn():
    """`{day: (plan_nodes, board, row)}` for the first `cover.plan` call of each day.

    `plan_nodes` is `[(tile, [ops])]` flattened across units; `board` is the dawn tile grid.
    """
    SA = importlib.import_module(MODULE)
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

    plans, seen = {}, set()
    now = {"d": 0, "h": 0}
    real, strict = DP.plan, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, *a, **kw):
        out, unc = real(units, jobs, budget, *a, **kw)
        if now["h"] == 0 and now["d"] not in seen:
            seen.add(now["d"])
            plans[now["d"]] = [(tuple(n.tile), [o for o, _i in getattr(n, "ops", [])])
                               for st in out.values() for n in (st.get("route") or [])]
        return out, unc

    DP.plan, CREW.STRICT_FEASIBILITY = spy, False
    boards = {}
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            now["d"], now["h"] = t // TPD, t % TPD
            o0 = env.state[0].observation
            if now["h"] == 0:
                boards[now["d"]] = [list(r) for r in o0["farms"][0]["tiles"]]
            a0, a1 = agent(o0), opp[t]
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        DP.plan, CREW.STRICT_FEASIBILITY = real, strict
    return {day: (plans.get(day, []), boards.get(day, []), sched.get(day) or {})
            for day in boards}


def _one_shot_harvest_nodes(nodes, board):
    """Stops that harvest a tile the harvest will CLEAR -- one-shot crops only."""
    from kagg.search import router as R

    out = []
    for tile, ops in nodes:
        if "HARVEST" not in ops:
            continue
        x, y = tile
        cell = board[y][x] if y < len(board) and x < len(board[y]) else None
        if not isinstance(cell, dict) or cell.get("kind") != "PLANT":
            continue                      # a pen harvest collects, it does not demolish
        if R.CROP[cell["crop"]]["ongoing"]:
            continue
        out.append((tile, ops))
    return out


def test_the_premise_a_day_wants_more_seed_than_it_has_dawn_ground(dawn):
    """Guard. If the row always fits on dawn-free ground there is nothing to prove."""
    hits = []
    for day, (nodes, board, row) in dawn.items():
        free = sum(1 for r in board for c in r if c is None)
        want = len(row.get("plants") or []) + int(row.get("builds", 0) or 0)
        if want > free and _one_shot_harvest_nodes(nodes, board):
            hits.append(day)
    assert hits, ("no day in range wants more placements than it has dawn-free ground while also "
                  "harvesting a one-shot crop; this file would pass vacuously")


@pytest.mark.parametrize("day", range(DAYS))
def test_a_stop_that_clears_a_tile_also_plants_it(dawn, day):
    nodes, board, row = dawn[day]
    free = sum(1 for r in board for c in r if c is None)
    want = len(row.get("plants") or []) + int(row.get("builds", 0) or 0)
    if want <= free:
        pytest.skip(f"d{day} wants {want} placements and has {free} free at dawn; no squeeze")
    clearing = _one_shot_harvest_nodes(nodes, board)
    if not clearing:
        pytest.skip(f"d{day} plans no one-shot harvest, so it frees no ground")
    short = want - free
    replanted = [t for t, ops in clearing if "PLANT" in ops]
    assert len(replanted) >= min(short, len(clearing)), (
        f"d{day} wants {want} placements on {free} free squares and plans "
        f"{len(clearing)} one-shot harvests, each of which empties its tile "
        f"({sorted(t for t, _o in clearing)}) -- but only {len(replanted)} of them carry a PLANT. "
        f"The plan is capped at the ground standing free at dawn.")
