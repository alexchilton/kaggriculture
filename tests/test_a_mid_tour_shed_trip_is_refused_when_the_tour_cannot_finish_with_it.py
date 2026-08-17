"""A detour is affordable only against the work still ahead, not against the clock.

`schedule_agent._router_acts` lets a hand standing on a hungry pen with no wheat go back to the shed
rather than abandon the animal. The comment says it is "costed, not assumed: the round trip is the
walk to the shed, the walk to the pen, the PICKUP and the FEED, and it is only taken if that many
turns are actually left". The code then tests:

    trip = _md(pos, home) + _md(home, node.tile) + 2
    if TPD - hour >= trip:

`TPD - hour` is the turns left in the DAY. It never subtracts the stops still on this tour, so a
unit with four stops ahead and twelve hours left takes a five-turn detour it cannot afford and
silently loses its tail.

Measured, seed 11, melon arm, d6. u4 is routed nine stops:

    (4,4)[PICKUP] (3,4)[HARVEST] (4,4)[PLACE] (4,4)[FEED,CARE,COLLECT_FERTILIZER]
    (4,4)[DROP] (5,4)[BUILD] (6,4)[BUILD] (8,4)[PLANT,WATER] (7,3)[PLANT,WATER]

and takes an unplanned shed round trip at h13-h16 to feed the animal it placed at h11. It reaches
its second pasture at h20 and the day ends. `(8,4)` and `(7,3)` are never visited, which is both of
d6's missing plants AND two of its missing waters -- the day reads `PLANT 0/2` and `WATER 17/19`
while three other units sit idle from h18.

The fix is to price the detoured route with the same function the planner uses, `cover.turns`, and
refuse it when the whole remaining tour no longer fits.
"""
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
REPLAY = "data/seed_scripts/kawashigi/92498144.json"
TEAM = "カワシギ"


def day_ops(day, seed=11, weeds=0.005):
    """`{op: count}` and `{unit: [(hour, op)]}` for seat 0 on `day`."""
    from kaggle_environments import make

    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / REPLAY)
    env = make("kaggriculture", configuration=dict(B.env_config(replay), seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, 0)
    opp = B.tape_policy(replay, TEAM, 1)
    counts, per_unit = {}, {}
    for t in range((day + 1) * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        d, h = divmod(t, TPD)
        if d == day:
            n0 = len(o0["farms"][0].get("hands") or [])
            for u, a in enumerate([a0["farmer"]] + list(a0["hands"] or [])[:n0]):
                if a and a[0] not in ("PASS", "NORTH", "SOUTH", "EAST", "WEST"):
                    counts[a[0]] = counts.get(a[0], 0) + 1
                    per_unit.setdefault(u, []).append((h, a[0]))
        env.step([a0, a1])
        if env.done:
            break
    return counts, per_unit


def test_day_six_reaches_both_of_its_plant_stops():
    """Both `(8,4)` and `(7,3)` carry `[PLANT, WATER]`; the tape plants twice on d6."""
    counts, per_unit = day_ops(6)
    assert counts.get("PLANT", 0) == 2, (
        f"d6 planted {counts.get('PLANT', 0)} of 2. Both stops are seated; the unit carrying them "
        f"spends its tail on an unbudgeted shed trip. per-unit: {per_unit.get(4)}")


def test_day_six_waters_every_tile_it_planned_to():
    """The two lost plant stops carry a WATER each, so the same defect costs both rows."""
    counts, _ = day_ops(6)
    assert counts.get("WATER", 0) == 19, (
        f"d6 watered {counts.get('WATER', 0)} of the 19 it seated.")
