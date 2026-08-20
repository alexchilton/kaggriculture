"""The schedule's `seeds` row is bought, not re-derived from what today can plant.

`seeds` and `plants` are separate rows in the schedule and they deliberately disagree. Victor's d6
asks for `seeds {WHEAT: 1, STRAWBERRY: 3}` against `plants` of ONE: he buys four, plants one, and
carries three into d7 -- which needs fifteen seeds for fourteen plants (twelve bought plus the three
in hand). Pre-stocking is load-bearing, and seeds live in `private["seeds"]`, not the shed, so a
surplus carries with no capacity cost.

Under `router` the agent sets `want_seed` from the remaining PLANT pins instead
(`schedule_agent.py:3500`). On d6 the board has one free tile, so exactly one pin exists and
exactly one seed is bought: `buy_seed 1/4`. The row is ignored. d7 then over-buys on the day,
`buy_seed 14/12`, paying for at dawn what should already have been in hand.

The assertion is per day and per crop, against what is HELD at dawn: a row asking for N seeds must
offer at least the N it does not already have. It says nothing about buying MORE than the row -- the
pin-driven figure is still allowed to exceed it, which is what keeps a day that can plant more than
the row planned from starving.
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
DAYS = 12
TPD = 24


@pytest.fixture(scope="module")
def bought():
    """`{day: (Counter of BUY_SEED emitted, Counter of seeds held at dawn)}`."""
    SA = importlib.import_module(MODULE)
    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    emitted = collections.defaultdict(collections.Counter)
    at_dawn = {}
    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    for t in range(TPD * DAYS):
        o0 = env.state[0].observation
        if t % TPD == 0:
            at_dawn[t // TPD] = collections.Counter(o0["farms"][0].get("seeds") or {})
        a0, a1 = agent(o0), opp[t]
        for o in (a0.get("market") or []):
            if o and o[0] == "BUY_SEED":
                emitted[t // TPD][o[1]] += int(o[2])
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return {day: (emitted[day], at_dawn.get(day, collections.Counter())) for day in at_dawn}


def _rows():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): dict(v.get("seeds") or {}) for k, v in raw.items()}


def test_the_premise_a_row_asks_for_more_seed_than_it_plants(bought):
    """Guard. Without a pre-stocking day in range this test proves nothing."""
    raw = json.loads(SCHEDULE.read_text())
    days = [int(k) for k, v in raw.items()
            if int(k) < DAYS and sum((v.get("seeds") or {}).values()) > len(v.get("plants") or [])]
    assert days, f"no day in d0-d{DAYS - 1} buys more seed than it plants; nothing to pre-stock"


@pytest.mark.parametrize("day", range(DAYS))
def test_a_days_seed_row_is_offered_in_full(bought, day):
    """Every crop the row asks for is offered, net of what is already held at dawn."""
    rows = _rows()
    want = rows.get(day) or {}
    if not want:
        pytest.skip(f"d{day} buys no seed")
    got, held = bought.get(day, (collections.Counter(), collections.Counter()))
    short = {c: (int(q) - int(held.get(c, 0)), int(got.get(c, 0)))
             for c, q in want.items()
             if int(got.get(c, 0)) < int(q) - int(held.get(c, 0))}
    assert not short, (
        f"d{day} row wants {want}, held at dawn {dict(held)}, offered {dict(got)}; "
        + ", ".join(f"{c}: needed {n}, offered {g}" for c, (n, g) in sorted(short.items())))
