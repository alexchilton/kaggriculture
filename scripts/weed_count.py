"""How many of our own tiles go to weed, across seeds. A watering-quality measure, not a weed one.

At `weedSpawnChance 0.0` -- the sweep's default and this script's -- the town spawns nothing, so a
weed can only be a tile of ours that went two days without water (`reference/kaggriculture.py:771`).
Every weed on the board is therefore a water we missed, and the count is the cleanest per-seed
reading of watering quality we have.

Both arms run in the SAME process and the flag is set on the imported module, so no file is edited
and the two arms cannot disagree about anything else.

**A caveat that applies to every arm comparison in this repo.** Crops differ in how long they hold
their ground, so an arm that plants differently empties tiles on different days -- and `_spawn_weeds`
draws `rng.random()` once per EMPTY tile before the shop unlock is chosen. Two arms therefore see
different shop draws on the same seed. Per-seed differences are confounded by that; the mean over
many seeds is not, because both arms sample the same distribution of draws. Read the mean, not a row.
This is the confound that invalidated three weed measurements on 2026-08-09 (commit f460719).

    python -u scripts/weed_count.py --seeds 16
"""

import argparse
import collections
import importlib
import json
import pathlib
import statistics
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

import breakdown as B
from kaggle_environments import make

TPD = 24
OURS = "data/seed_scripts/top_guys/90976060/schedule.json"
#: One strong recorded seat, driven in seat 1. The opponent is held fixed across arms on purpose:
#: weeds are a property of OUR field, so a varied field would only add noise to the thing measured.
RIVAL = "data/seed_scripts/top_guys/90976060.json"


def play(seed, days, weeds, module, schedule, replay, flag):
    """One game. Returns `(weeds_on_our_farm, our_money, live_crop_tiles, shop_draw)`."""
    raw = json.loads(pathlib.Path(schedule).read_text())
    sched = {int(k): {a: b for a, b in v.items() if a not in B.TAPE_ONLY}
             for k, v in raw.items()}
    B.schedule_agent = SA = importlib.import_module(module)
    CREW = importlib.import_module("kagg.search.crew")
    was_strict, CREW.STRICT_FEASIBILITY = CREW.STRICT_FEASIBILITY, False
    was_flag, SA.SHOP_ADAPT_CROPS = SA.SHOP_ADAPT_CROPS, flag
    try:
        env = make("kaggriculture",
                   configuration=dict(B.env_config(replay), seed=seed, weedSpawnChance=weeds),
                   debug=False)
        env.reset(2)
        agent = SA.make_agent(sched, 0, router=True)
        team = ((json.loads(pathlib.Path(replay).read_text()).get("info") or {})
                .get("TeamNames") or ["", ""])[1]
        opp = B.tape_policy(replay, team, 1)
        for t in range(min(719, TPD * days)):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if env.state[0].status == "DONE":
                break
        obs = env.state[0].observation
        tiles = obs["farms"][0]["tiles"]
        weed = sum(1 for r in tiles for c in r if c == "WEED")
        crops = collections.Counter(c.get("crop") for r in tiles for c in r
                                    if isinstance(c, dict) and c.get("kind") == "PLANT")
        shops = tuple(sorted(collections.Counter(
            (obs.get("town") or {}).get("unlocked_shops") or []).items()))
        return weed, float(obs["farms"][0]["money"]), crops, shops
    finally:
        CREW.STRICT_FEASIBILITY = was_strict
        SA.SHOP_ADAPT_CROPS = was_flag


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--first-seed", type=int, default=11)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--module", default="kagg.search.schedule_agent")
    ap.add_argument("--schedule", default=OURS)
    ap.add_argument("--replay", default=RIVAL)
    args = ap.parse_args()

    seeds = list(range(args.first_seed, args.first_seed + args.seeds))
    print(f"weedSpawnChance {args.weeds} -- every weed below is a water WE missed")
    print(f"seeds {seeds}\n")
    print(f"  {'seed':>5} {'weeds ON':>9} {'weeds OFF':>10} {'money ON':>10} {'money OFF':>10} "
          f"{'same draw?':>11}")
    got = {True: [], False: []}
    same = 0
    for seed in seeds:
        row = {}
        for flag in (True, False):
            row[flag] = play(seed, args.days, args.weeds, args.module, args.schedule,
                             args.replay, flag)
            got[flag].append(row[flag])
        agrees = row[True][3] == row[False][3]
        same += agrees
        print(f"  {seed:>5} {row[True][0]:>9} {row[False][0]:>10} {row[True][1]:>10,.0f} "
              f"{row[False][1]:>10,.0f} {('yes' if agrees else 'NO'):>11}")

    print()
    for flag in (True, False):
        w = [r[0] for r in got[flag]]
        m = [r[1] for r in got[flag]]
        crops = collections.Counter()
        for r in got[flag]:
            crops.update(r[2])
        print(f"  SHOP_ADAPT_CROPS = {str(flag):<5}  weeds mean {statistics.mean(w):>6.1f}  "
              f"median {statistics.median(w):>5.1f}  range {min(w)}-{max(w)}   "
              f"money median ${statistics.median(m):>9,.0f}")
        print(f"      closing crop tiles, summed over seeds: "
              f"{ {k: v for k, v in crops.most_common()} }")
    print(f"\n  shop draw identical on {same}/{len(seeds)} seeds -- where it differs, the per-seed "
          f"row is confounded and only the mean is readable.")


if __name__ == "__main__":
    main()
