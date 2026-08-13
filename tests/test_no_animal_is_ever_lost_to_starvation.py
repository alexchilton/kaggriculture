"""An animal lost to hunger is a compounding loss, not a bad day.

`kaggriculture.py:804` -- two consecutive unfed days and the animal escapes, leaving the empty
structure behind.  Every milk, egg, wool and fertilizer unit it would have produced for the rest of
the season goes with it, and the pen that housed it was paid for.  Alex, 2026-08-10: *"thats
fertilizer and milk so early is cumulative"*.

On `seb1326`, seed 11, we lost two cows between d7 and d8:

    d6   7 animals, 3 empty pens   unfed=1: COW (4,2), SHEEP (4,3), SHEEP (4,4)
    d7   7 animals, 9 empty pens   unfed=1: COW (2,4), COW (3,3), COW (3,4)
    d8   5 animals, 11 empty pens

Note the two sets are DISJOINT: we fed the first three on d7 and starved a different three.
`feed 4/7`, `4/3`, `5/7` across those days -- never the whole herd on any of them -- so somebody is
always carrying a 1 and only has to be missed once more.

The invariant is stated over the outcome rather than the feed count on purpose.  A `feed` row that
matches the tape is not the goal; a herd that survives is, and the tape's own `feed 7/3/7` shows it
feeding everything on d6 precisely so d7 can be light.
"""
import collections
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
SEED, WEEDS, TPD, DAYS = 11, 0.0, 24, 9
MODULE = "kagg.search.schedule_agent"
TAPE = "seb1326"


@pytest.fixture(scope="module")
def herd_by_day():
    """`{day: (live animals, empty structures)}` plus every escape, for our agent."""
    import importlib

    import breakdown as B
    from kaggle_environments import make

    replay, schedule, team = B.TAPES[TAPE]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA = importlib.import_module(MODULE)
    CREW = importlib.import_module("kagg.search.crew")

    was = CREW.STRICT_FEASIBILITY
    CREW.STRICT_FEASIBILITY = False
    try:
        env = make("kaggriculture",
                   configuration=dict(B.env_config(str(REPO / replay)),
                                      seed=SEED, weedSpawnChance=WEEDS),
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(sched, 0, router=True)
        opp = B.tape_policy(str(REPO / replay), team, 1)
        out, escapes, prev = {}, [], None
        for t in range(TPD * DAYS):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if t % TPD == TPD - 1:
                farm = env.state[0].observation["farms"][0]
                live = {}
                for y, row in enumerate(farm["tiles"]):
                    for x, c in enumerate(row):
                        if isinstance(c, dict) and c.get("animal"):
                            live[(y, x)] = (c["animal"], c["consecutive_unfed"])
                day = t // TPD
                if prev is not None:
                    for tile, (kind, _u) in prev.items():
                        if tile not in live:
                            escapes.append((day, tile, kind))
                out[day] = live
                prev = live
        return out, escapes
    finally:
        CREW.STRICT_FEASIBILITY = was


def test_no_animal_escapes_through_hunger(herd_by_day):
    _live, escapes = herd_by_day
    assert not escapes, (
        "animals lost to starvation (day, tile, kind): "
        + ", ".join(f"d{d} {t} {k}" for d, t, k in escapes)
        + "\n  Every one of these was paid for and stops producing for the rest of the season."
    )


@pytest.mark.parametrize("day", range(DAYS))
def test_no_animal_ends_a_day_one_miss_from_escaping(herd_by_day, day):
    """`consecutive_unfed == 1` is not a warning, it is the whole of the margin.

    Separate from the escape test because it fails a day EARLIER, on the day the ration was
    actually missed rather than the day the animal walks off -- which is the day a fix has to
    target.
    """
    live, _escapes = herd_by_day
    at_risk = {t: k for t, (k, unfed) in live.get(day, {}).items() if unfed >= 1}
    assert not at_risk, (
        f"day {day}: {len(at_risk)} animals go into tomorrow unfed, one miss from escaping: "
        + ", ".join(f"{t} {k}" for t, k in sorted(at_risk.items()))
    )
