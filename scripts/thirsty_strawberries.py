"""Alex's theory: feeding more animals steals the waters, so the strawberries die of thirst.

The chain he proposes is: the sheep-placement fix filled 19 pens -> FEED and CARE eat the unit-turns
-> WATER drops (-59 on the season) -> tiles hit `consecutive_unwatered >= 2` -> they become WEED
(`reference/kaggriculture.py:746-753`) -> we DIG them (+35) -> `strawb` -94 and `weeds` reads LOWER
than the tape's rather than higher.

Every step of that is checkable. This watches every PLANT tile across the season and records the
exact transition: which crop, on which day, and by which of the two routes a tile can become a WEED.

  route A  `consecutive_unwatered >= 2`      -- death by thirst, line 753
  route B  lifespan expired, yield exhausted -- natural end of life, line 735

Route A is the theory. Route B is a tile that finished its useful life and would have gone anyway.
If our strawberries die by route A and his do not, the theory is right. If they mostly go by route B,
the tiles were spent and the -94 means something else entirely.
"""
import collections
import json
import pathlib
import sys

sys.path.insert(0, "/Users/alexchilton/DataspellProjects/kaggriculture")

from kaggle_environments import make

from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

DAYS = 30
replay, schedule, team = TAPES["seb"]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def snapshot(obs):
    """(x, y) -> (crop, consecutive_unwatered) for every standing PLANT tile."""
    out = {}
    for y, row in enumerate(obs["farms"][0]["tiles"]):
        for x, cell in enumerate(row):
            if isinstance(cell, dict) and cell.get("kind") == "PLANT":
                out[(x, y)] = (cell.get("crop"), int(cell.get("consecutive_unwatered", 0)))
    return out


def kinds(obs):
    out = collections.Counter()
    for row in obs["farms"][0]["tiles"]:
        for cell in row:
            out[cell.get("kind") if isinstance(cell, dict) else None] += 1
    return out


def run(make_seat0, label):
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    p0 = make_seat0()
    opp = tape_policy(replay, team, 1)
    prev = snapshot(env.state[0].observation)
    thirst = collections.Counter()      # (crop) -> tiles lost to consecutive_unwatered >= 2
    spent = collections.Counter()       # (crop) -> tiles lost any other way
    by_day = collections.defaultdict(collections.Counter)
    for t in range(24 * DAYS - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
        now = snapshot(env.state[0].observation)
        for pos, (crop, unwatered) in prev.items():
            if pos in now:
                continue
            # The tile stopped being a PLANT this turn. It was one unwatered day short of death at
            # the previous observation, so `>= 1` there means the second dry day landed here.
            if unwatered >= 1:
                thirst[crop] += 1
                by_day[t // 24][crop] += 1
            else:
                spent[crop] += 1
        prev = now
    k = kinds(env.state[0].observation)
    print(f"\n===== {label} =====")
    print(f"  died of THIRST (consecutive_unwatered >= 2): {dict(thirst)}   total {sum(thirst.values())}")
    print(f"  ended some other way (lifespan/spent):       {dict(spent)}   total {sum(spent.values())}")
    print(f"  final board: WEED={k['WEED']}  PLANT={k['PLANT']}  empty={k[None]}")
    if by_day:
        print("  thirst deaths by day:")
        for d in sorted(by_day):
            print(f"    d{d:<3} {dict(by_day[d])}")
    return thirst, spent


run(lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True)), "OURS")
run(lambda: tape_policy(replay, team, 0), "SEB (the tape)")
