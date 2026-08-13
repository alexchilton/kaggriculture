"""Shed-access ground is held back for pens the schedule owes TODAY, not for pens ten days out.

`router.field_order` leaves the four shed-access cells out of the placement sweep on purpose -- "they
are worth more as pens, where FEED, CARE, COLLECT_FERTILIZER, PICKUP and DROP all happen without a
single move". That is right while a pen is actually waiting for ground. It is wrong once the
schedule's next pen is a fortnight away, because the cell then sits empty for a fortnight.

Measured on Victor's d11, seed 11. The day owes eleven plantings and gets ten:

    owed = cumulative want - planted     MELON 2   WHEAT 4   STRAWBERRY 5   = 11
    pinned                               MELON 2   WHEAT 4   STRAWBERRY 0   =  6
    replanted onto cleared tiles                             STRAWBERRY 4   =  4
    offered                                                                 = 10

Four of the five strawberry ride on the wheat tiles a harvest clears (`REPLANT_A_CLEARED_TILE`), and
the fifth has nowhere to go. The board has seven empty owned squares:

    (4,1) (3,2) (4,2) (2,3) (1,4) (0,9)   in field_order, all six pinned
    (4,5)                                 shed-access, excluded, unpinned

The schedule builds 15 pens across the season, 12 of them by d8 and the last three on **d21 and
d24**. So at d11 nothing is owed -- `have >= want_pens`, which `_refresh_pins` already computes --
and (4,5) is being kept clear for a pen ten days away while a planting goes unmade.

Asserted on the offer rather than on `plant` emitted, because d11 has a second, independent defect
in the executor: one of the four committed WHEAT stops is not emitted either.
"""
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
FOCUS_DAY = 11


def _offered_and_unpinned(day):
    """(PLANT ops in the dawn job list, empty owned tiles left unpinned) on `day`."""
    from kaggle_environments import make

    import breakdown as B
    from kagg.search import routines as R

    SA = importlib.import_module("kagg.search.schedule_agent")
    RT = importlib.import_module("kagg.search.router")
    replay, schedule, team = B.TAPES["victor"]
    raw = json.loads(pathlib.Path(schedule).read_text())
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
            for k, r in raw.items()}

    seen = {}
    real = RT.build_nodes

    def spy(tiles, d, shed, carried, unlocked, pinned, hour=0, **kw):
        out = real(tiles, d, shed, carried, unlocked, pinned, hour, **kw)
        if d == day and "seen" not in seen:
            seen["seen"] = True
            seen["offered"] = collections.Counter(
                i for n in out for o, i, *_ in n.ops if o == "PLANT")
            seen["free"] = [(x, y) for y, r in enumerate(tiles) for x, c in enumerate(r)
                            if c is None and R.quadrant_of(x, y) in unlocked
                            and (x, y) not in (pinned or {})]
        return out

    RT.build_nodes = SA.RT.build_nodes = spy
    try:
        env = make("kaggriculture",
                   configuration=dict(B.env_config(replay), seed=11, weedSpawnChance=0.0),
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        opp = B.tape_policy(replay, team, 1)
        for t in range(TPD * day + 1):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        RT.build_nodes = SA.RT.build_nodes = real
    return seen.get("offered", collections.Counter()), seen.get("free", [])


def test_the_premise_the_next_pen_is_a_long_way_off():
    """If the schedule grows a pen near d11 this test is measuring nothing. Fail loudly."""
    sched = json.loads((REPO / "data/seed_scripts/victor/schedule.json").read_text())
    later = sorted(int(d) for d in sched
                   if int(d) > FOCUS_DAY and int(sched[d].get("builds", 0) or 0))
    assert later and later[0] >= FOCUS_DAY + 5, (
        f"the next pen after d{FOCUS_DAY} is due on d{later[0] if later else None}; the ground held "
        f"for it is not idle for long and this test's premise is stale.")


def test_the_day_is_offered_every_planting_it_owes():
    offered, free = _offered_and_unpinned(FOCUS_DAY)
    sched = json.loads((REPO / "data/seed_scripts/victor/schedule.json").read_text())
    want = collections.Counter(sched[str(FOCUS_DAY)].get("plants") or [])
    assert offered == want, (
        f"d{FOCUS_DAY} owes {dict(want)} and its dawn job list offers {dict(offered)}, with "
        f"{free} empty and unpinned. `field_order` holds the four shed-access cells back for pens, "
        f"and by d{FOCUS_DAY} every pen the schedule owes is already standing -- the next is ten "
        f"days out.")
