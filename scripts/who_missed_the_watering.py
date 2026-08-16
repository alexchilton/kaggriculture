"""Track every tile through d0-d12 and name the ones that go unwatered, on the day it happens.

## The defect

Live ladder games, 2026-08-16: the opening is clean through d8 (0-2 weeds) and then a cluster appears
on d9-d10 -- 1-2 tiles in every game and occasional 7-10 tile blowouts. It is present in the 1947.9
build too, so it is long-standing rather than a regression.

The tiles are not random. Across six independent games with different opponents and seeds:

    (2,2) WHEAT weeds on d9   in 4 games
    (3,2) WHEAT weeds on d9   in 3 games
    (8,4) MELON weeds on d9   in 3 games

A crop becomes WEED after **two consecutive unwatered days** (`reference/kaggriculture.py`
`_daily_refresh_plants`), so a weed appearing on d9 was last watered on **d7**. The miss is at d7/d8,
at the edge of the opening we protect, and the same coordinates fail every time.

Random spawns are a separate and smaller thing: `_spawn_weeds` only fires on tiles that are `None`
(empty ground), at `weedSpawnChance` -- **0.005 on the ladder, not 0** as our local grids have it.
So a weed on a tile that held a crop is always our own missed watering; a weed on empty ground is
the dice.

## What this prints

Per day, per tile: the crop, its `consecutive_unwatered` count, and whether the day's action stream
contained a WATER for that tile. A tile that reaches `consecutive_unwatered == 1` is one day from
dying, and is the last moment a fix can act.

`WATER` ops are counted from the ACTIONS we submit, not inferred, because the counter on the tile
resets silently and an op that was planned but never reached is indistinguishable from one that was
never planned -- which is exactly the distinction that matters here.

    python -u scripts/who_missed_the_watering.py --seed 3 --through 12
"""
import argparse
import collections
import importlib
import importlib.util
import pathlib
import sys

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--through", type=int, default=12)
    ap.add_argument("--weeds", type=float, default=0.005, help="the LADDER value")
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    a = ap.parse_args()

    from kaggle_environments import make

    A = importlib.import_module("kagg.search.schedule_agent")
    PLAN = importlib.import_module("kagg.plan")
    sp = importlib.util.spec_from_file_location("opp", str(REPO / a.opponent))
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)

    env = make("kaggriculture",
               configuration={"seed": a.seed, "weedSpawnChance": a.weeds}, debug=False)
    env.reset(2)
    me = A.make_agent(PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json")), me=0)

    watered = collections.defaultdict(set)     # day -> tiles we submitted a WATER for
    planted_on = {}                            # tile -> day it was planted
    dying = collections.defaultdict(list)      # day -> tiles at consecutive_unwatered >= 1
    died = {}                                  # tile -> (day, crop) it became WEED
    prev = {}

    for t in range((a.through + 1) * 24):
        o = env.state[0].observation
        day = t // 24
        cur = {}
        for y, row in enumerate(o["farms"][0]["tiles"]):
            for x, c in enumerate(row):
                k = (x, y)
                if isinstance(c, dict) and c.get("crop"):
                    cur[k] = c["crop"]
                    planted_on.setdefault(k, c.get("planted_day"))
                    if t % 24 == 23 and c.get("consecutive_unwatered", 0) >= 1:
                        dying[day].append((k, c["crop"], c["consecutive_unwatered"]))
                elif (c == "WEED" or (isinstance(c, dict) and c.get("kind") == "WEED")) \
                        and k not in died:
                    died[k] = (day, prev.get(k, "EMPTY"))
        prev = cur

        act = me(o, t)
        # **`WATER` carries no coordinates.** It is bare `['WATER']` and acts on whatever tile the
        # unit is standing on, so the tile comes from the UNIT's position this turn. The op list is
        # `[farmer] + hands` in order, and `farm["farmer"]` / `farm["hands"][i]` are `[x, y]`.
        farm = o["farms"][0]
        units = [farm.get("farmer")] + list(farm.get("hands") or [])
        for i, op in enumerate([act.get("farmer")] + list(act.get("hands") or [])):
            if op and op[0] == "WATER" and i < len(units) and units[i]:
                watered[day].add((units[i][0], units[i][1]))
        env.step([act, mod.agent(env.state[1].observation, t)])
        if env.done:
            break

    print(f"seed {a.seed}, weedSpawnChance {a.weeds}\n")
    print(f"{'day':>4}{'crops':>7}{'watered':>9}{'at risk at dusk':>17}  tiles one day from dying")
    for day in range(a.through + 1):
        risk = dying.get(day) or []
        names = " ".join(f"{k}{c[:2]}" for k, c, _n in risk[:8])
        ncrops = sum(1 for _k, _v in prev.items()) if day == a.through else ""
        print(f"{day:>4}{'':>7}{len(watered.get(day, ())):>9}{len(risk):>17}  {names}")

    print(f"\ntiles that DIED, and what they were:")
    for k, (day, was) in sorted(died.items(), key=lambda kv: kv[1][0]):
        origin = "OUR MISS" if was not in ("EMPTY", None) else "random spawn (empty ground)"
        last = max([d for d in watered if k in watered[d]] or [-1])
        print(f"   {str(k):>8} d{day:<3} was {str(was):<12} {origin:<28} "
              f"last WATER we submitted: {'d' + str(last) if last >= 0 else 'never'}")

    ours = [k for k, (_d, w) in died.items() if w not in ("EMPTY", None)]
    print(f"\n{len(ours)} of {len(died)} were crops -- our misses. "
          f"A crop dies two days after its last water, so look one and two days BEFORE the day "
          f"it died.")


if __name__ == "__main__":
    main()
