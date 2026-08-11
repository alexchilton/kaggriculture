"""A stop that harvests a tile and replants it costs FOUR turns, not three.

`Job.turns` (`cover.py:348`) already knows a PLANT is two turns and not one -- a tile is created at
`consecutive_unwatered = 1` and weeds at 2, so a planting nobody waters is a seed thrown away, and
the executor emits that WATER on the next turn because `_live_ops` re-derives at the tile. What the
planner is charged is

    len(ops) + (1 if any PLANT and not any WATER else 0)

The guard is wrong on the one shape where a WATER is already in the list for a different reason.
A mature tile that is harvested and immediately re-sown reads

    [WATER, HARVEST, PLANT]

and that WATER belongs to the OLD crop -- on a one-shot it *is* the yield (`router.crop_ops:626`),
which is why it precedes the HARVEST. The new seed still needs its own water, so the executor spends
four turns and the planner budgeted three.

Measured on Victor's d8, seed 11 -- the day the grid reads `plant 9/10`:

    u6 (0,2)   h17 WATER   h18 HARVEST   h19 PLANT   h20 WATER      job costed 3, spent 4
    u3 (1,1)   h15 WATER   h16 HARVEST   h17 PLANT   h18 WATER      job costed 3, spent 4
    u3 (1,0)   h20 WATER   h21 HARVEST   h22 PLANT   h23 WATER      job costed 3, spent 4

u6's tour was costed at exactly its budget of 23. Having lost a turn at (0,2) it reaches its last
stop (0,1) at h22 with three ops and two hours left: `h22 WATER, h23 HARVEST`, and the PLANT is
never emitted. The day's tenth planting, and one STRAWBERRY seed still in the store at h23.

Two assertions, mechanism and consequence.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import kagg.search.cover as DP  # noqa: E402


def test_a_harvest_and_replant_stop_is_charged_for_both_waters():
    """The mechanism, priced straight off `Job`. No board, no game."""
    job = DP.Job((0, 2), [("WATER", None), ("HARVEST", None), ("PLANT", "WHEAT")])
    assert job.turns == 4, (
        f"a stop that waters, harvests and re-sows is costed at {job.turns} turns. The executor "
        f"spends four -- the WATER in the ops list is the old crop's (on a one-shot it is the yield "
        f"itself, which is why it comes before the HARVEST), and `_live_ops` re-derives the tile "
        f"after the PLANT and emits a second WATER. `Job.turns` skips its `+1` whenever ANY water is "
        f"present, so every harvest-and-replant stop under-charges the tour by one turn.")


def test_the_plain_shapes_are_unchanged():
    """The `+1` must still fire on a bare PLANT and must still stay off a stop with no PLANT."""
    assert DP.Job((0, 0), [("PLANT", "WHEAT")]).turns == 2
    assert DP.Job((0, 0), [("HARVEST", None), ("PLANT", "WHEAT")]).turns == 3
    assert DP.Job((0, 0), [("WATER", None)]).turns == 1
    assert DP.Job((0, 0), [("WATER", None), ("HARVEST", None)]).turns == 2


def test_day_eight_emits_every_planting_its_plan_committed_to():
    """The consequence, end to end: the tape plants ten on d8 and so must we."""
    import importlib

    from kaggle_environments import make

    import breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    replay = REPO / "data/seed_scripts/top2/91854176.json"
    team = "Victor @ Tufa Labs"
    seed, tpd, day = 11, 24, 8

    raw = json.loads((REPO / "data/seed_scripts/victor/schedule.json").read_text())
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
            for k, r in raw.items()}
    want = sum(int(q) for q in (thin[day].get("seeds") or {}).values())

    d = json.loads(replay.read_text())
    seat = d["info"]["TeamNames"].index(team)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)

    planted = 0
    for t in range(tpd * (day + 1)):
        o0 = env.state[0].observation
        a0 = agent(o0)
        if t // tpd == day:
            planted += sum(1 for h in ([a0["farmer"]] + list(a0["hands"]))
                           if h and h[0] == "PLANT")
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": opp[t]["farmer"], "hands": list(opp[t]["hands"])[:n1],
                   "market": opp[t]["market"]}])

    assert planted == want, (
        f"d{day} emitted {planted} PLANT against the tape's {want}. The plan committed to all "
        f"{want} stops with nothing uncovered, so the shortfall is the tour running out of hours: "
        f"every harvest-and-replant stop is charged three turns and spends four.")
