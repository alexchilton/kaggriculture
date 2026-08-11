"""A PLANT stop whose seed has not been bought YET goes to the back of the tour, not in the bin.

`_live_ops` returns `[]` for a pinned PLANT when `private["seeds"][crop] <= 0`
(`kaggriculture.py:412` refuses the op outright), and the executor's `st["route"].pop(0)` treats an
empty op list as "somebody else did this" and drops the stop for good. That reading is right for a
tile another hand already sowed. It is wrong when the seed is simply still on today's shopping list:
the unit phase runs BEFORE `_process_market` (`kaggriculture.py:922` then `:928`), so seed the day
is buying lands hours after the tour was planned around it.

Measured on Victor's d10, seed 11. The row buys `{MELON 14, STRAWBERRY 16, WHEAT 1}` on a $2,127
dawn bank. Melon is ordered first (`_seed_need_order` -- its stops come at h4), which leaves $400 of
the strawberry affordable at h2 and pushes the other twelve behind the day's sells:

    h2   STRAWBERRY  4   MELON 14
    h11  STRAWBERRY  0                 exhausted
    h16  STRAWBERRY 12                 the rest finally settle

Four committed strawberry stops are reached inside that window and thrown away:

    u12  (1,9)  h12      u11  (0,6)  h13      u8  (4,9)  h11 and (3,8)  h15

Each unit then stands on the tile and passes to dusk -- 9, 11 and 12 idle turns -- with strawberry
seed in the store from h16. `plant 19/23`, and three strawberry seeds still unsown at h23 that the
tape does not have.

The stop must not simply be held: u8's (4,9) has a MELON stop behind it at (4,8) that it does go on
to plant, so blocking the hand there trades one plant for another. It goes to the BACK of the tour,
which is why this asserts on the count and not on the hour.
"""
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

DAY, SEED, TPD = 10, 11, 24


def _run():
    from kaggle_environments import make

    import breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    replay, schedule, team = B.TAPES["victor"]
    raw = json.loads(pathlib.Path(schedule).read_text())
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
            for k, r in raw.items()}

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    opp = B.tape_policy(replay, team, 1)

    planted, leftover = collections.Counter(), {}
    for t in range(TPD * (DAY + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        if t // TPD == DAY:
            for h in [a0["farmer"]] + list(a0["hands"]):
                if h and h[0] == "PLANT":
                    planted[h[1]] += 1
            if t % TPD == TPD - 1:
                leftover = {k: int(v) for k, v in (o0["private"].get("seeds") or {}).items()
                            if int(v)}
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return planted, leftover


def test_every_committed_plant_stop_is_sown():
    """The dawn plan commits 23 -- MELON 12, STRAWBERRY 11 -- with nothing uncovered."""
    planted, leftover = _run()
    want = {"MELON": 12, "STRAWBERRY": 11}
    assert dict(planted) == want, (
        f"d{DAY} sowed {dict(planted)} against the {want} its own plan committed to, and ended the "
        f"day holding {leftover}. A stop reached before its seed was bought is dropped by "
        f"`st['route'].pop(0)`, and the hand then stands on the tile passing until dusk while the "
        f"seed settles an hour later.")
