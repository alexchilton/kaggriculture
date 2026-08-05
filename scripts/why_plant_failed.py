"""Every PLANT our tape emits, and for each one whether the environment actually planted it.

`scripts/which_tile_is_missing.py` proves the emitter puts all 126 PLANT ops on the right tiles on
the right days. So the missing plant is not an emission failure -- it is a **silent no-op inside the
environment**, and there are four ways that happens:

    LOCKED    `_apply_unit_action` bails before PLANT on unowned ground
    OCCUPIED  the tile already holds a crop, a weed, or a pen
    NO_SEED   `private["seeds"][crop] == 0`
    ATOMIC    `kaggriculture.py:888` -- if a turn's PLANT requests for a crop exceed the seeds held,
              **every** request for that crop that turn is dropped, not just the surplus

The last one is the trap: seeds bought at turn `t` only settle in `_process_market`, which runs
*after* the unit actions of turn `t`. A PLANT on the same turn as its own seed order always fails,
and takes every other plant of that crop on that turn down with it.

Steps the real environment one turn at a time and reports the verdict per PLANT.
"""

import collections
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import dayplan, routines as R
import build_script_submission as B

TPD = R.TURNS_PER_DAY
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")


def main():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    from kaggle_environments import make
    env = make("kaggriculture", debug=True)
    env.reset(2)

    verdicts = collections.Counter()
    detail = []

    for t in range(len(plan)):
        st = env.state
        obs = st[0].observation
        farms = obs["farms"]
        me = farms[0]
        private = obs["private"]
        seeds = dict(private.get("seeds") or {})
        board = me["tiles"]

        farmer, hands_, market = plan[t]
        n = len(me.get("hands") or [])
        acts = [farmer] + list(hands_[:n])

        # where does each unit stand right now
        units = [me["farmer"]] + list(me.get("hands") or [])

        demand = collections.Counter(a[1] for a in acts
                                     if isinstance(a, list) and len(a) >= 2 and a[0] == "PLANT")
        blocked = {c for c, k in demand.items() if k > seeds.get(c, 0)}

        for i, a in enumerate(acts):
            if not (isinstance(a, list) and len(a) >= 2 and a[0] == "PLANT"):
                continue
            crop = a[1]
            x, y = units[i] if i < len(units) else (None, None)
            tile = board[y][x] if x is not None else "?"
            if tile == "LOCKED":
                v = "LOCKED"
            elif tile is not None:
                v = "OCCUPIED"
            elif crop in blocked:
                v = "ATOMIC" if demand[crop] > 1 else "NO_SEED"
            else:
                v = "ok"
            verdicts[v] += 1
            if v != "ok":
                detail.append(f"turn {t:3d} (day {t // TPD:2d} h{t % TPD:2d}) unit {i} "
                              f"({x},{y}) PLANT {crop:10s} {v}  "
                              f"seeds={seeds.get(crop, 0)} demand={demand[crop]} tile={tile}")

        st2 = env.step([{"farmer": farmer, "hands": hands_[:n], "market": market},
                        {"farmer": ["PASS"], "hands": [], "market": []}])
        if st2[0].status == "DONE":
            break

    print("verdicts:", dict(verdicts))
    print()
    for line in detail[:60]:
        print(line)
    if len(detail) > 60:
        print(f"... and {len(detail) - 60} more")


if __name__ == "__main__":
    main()
