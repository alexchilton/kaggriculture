"""The farmer must not be standing on the spawn ring when the day's hires settle.

`_spawn_hand` (`reference/kaggriculture.py`) puts each new hand on the least-occupied shed-access
tile, ties broken by the NWSE order of `_shed_access_tiles`, and it counts the FARMER:

    all_pos = [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]

The ring is `[(4,4), (5,4), (4,5), (5,5)]`. While only the NW quadrant is owned, all four orthogonal
neighbours of `(5,5)` are locked, so a hand that spawns there cannot move, cannot work, and cannot
be walked home -- `schedule_agent._mobile` writes it off, correctly, for the whole day.

With the ring clear, seven hires land `(4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5)` -- ONE on the dead
tile. With the farmer parked on `(4,4)` the whole rotation shifts one step and the 3rd AND 7th land
there -- TWO dead hands, 46 turns.

Measured on d4 of `seb1326`, seed 11:

    Seb  farmer at (4,3) when the hires settle   hands (4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5)
    ours farmer at (4,4) doing a PICKUP          hands (5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5)

    our crew that day:  u2 0 work / 0 move / 23 idle,  u6 0 work / 0 move / 23 idle
    Seb's crew:         one idle seat, and 88 move turns against our 67

The unit phase runs before the market phase (`kaggriculture.py:922` then `:928`), so the farmer's
hour-0 action happens BEFORE the hires land. One step off the ring costs one turn and buys 23.

The assertion is on the number of seats the day can use, not on the farmer's square, because the
square is the mechanism and the seats are the point.
"""
import importlib
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
SEED, WEEDS, TPD = 11, 0.0, 24
TAPE = "seb1326"
MODULE = "kagg.search.schedule_agent"

#: The day the loss is measured on: 7 hires, one quadrant owned, and a 55-unit SELL row that needs
#: every hand it can get.
DAY = 4


@pytest.fixture(scope="module")
def seats():
    """`(seats the planner was given, seats the farm actually owns)` at `DAY` hour 0."""
    import breakdown as B
    from kaggle_environments import make

    replay, schedule, team = B.TAPES[TAPE]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {a: b for a, b in v.items() if a not in B.TAPE_ONLY}
             for k, v in raw.items()}
    B.schedule_agent = SA = importlib.import_module(MODULE)
    CREW = importlib.import_module("kagg.search.crew")

    got = []
    real = SA._solve

    def spy(units, nodes, budget, *a, **kw):
        out = real(units, nodes, budget, *a, **kw)
        got.append(len(units))
        return out

    was, SA._solve = SA._solve, spy
    strict, CREW.STRICT_FEASIBILITY = CREW.STRICT_FEASIBILITY, False
    try:
        env = make("kaggriculture",
                   configuration=dict(B.env_config(str(REPO / replay)),
                                      seed=SEED, weedSpawnChance=WEEDS),
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(sched, 0, router=True)
        opp = B.tape_policy(str(REPO / replay), team, 1)
        planned = owned = None
        for t in range(TPD * (DAY + 1)):
            o0, o1 = env.state[0].observation, env.state[1].observation
            if t == DAY * TPD:
                got.clear()
            a0, a1 = agent(o0), opp(o1, t)
            if t == DAY * TPD:
                planned = max(got) if got else 0
                owned = 1 + int((sched.get(DAY) or {}).get("hands", 0) or 0)
                break
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
        return planned, owned
    finally:
        SA._solve = was
        CREW.STRICT_FEASIBILITY = strict


def test_at_most_one_hire_is_lost_to_the_dead_corner(seats):
    """Seven hires over a four-tile ring can strand ONE hand on `(5,5)` and no more.

    The tape strands exactly one on this day and so should we; a second is the farmer's own
    occupancy shifting the rotation, and is ours to give away or keep.
    """
    planned, owned = seats
    assert planned >= owned - 1, (
        f"the day owns {owned} seats (farmer + {owned - 1} hands) and the dawn plan was given "
        f"{planned}. {owned - planned} hands spawn where they cannot move, against the tape's one.\n"
        f"  Each one is 23 turns, and day {DAY} finishes with 43 wheat in hands and sells 19 of 55."
    )
