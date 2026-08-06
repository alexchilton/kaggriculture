"""Crop tiles, day by day, ours against the tape's -- before reading anything into the water count.

`WATER 642 against the tape's 846` was reported as a shortfall. It is only a shortfall if both farms
are standing over the same number of plants. Watering 76% as often across an equal field is a bug;
watering 76% as often across 76% as many plants is the same policy on a smaller farm, and the thing
to fix is then the field, not the watering.

Two constraints from the reference make the per-day view necessary rather than nice:

    a tile is planted with `consecutive_unwatered = 1` (kaggriculture.py:207), and any tile reaching
    2 turns to WEED at end of day (:752). So every crop needs a water on its PLANTING day and at
    least every other day after -- watering is not optional upkeep, it is the survival condition.

    a WEED is not a neutral empty tile: it occupies the ground, and only DIG clears it.

So this prints per day, both arms: live crop tiles, weeds, tiles planted, tiles lost to weeds, WATER
ops emitted, and waters per crop-tile-day. The last column is the one that answers the question --
if it matches, we water exactly as hard as the winner and simply farm less ground.
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import schedule_agent
import agent_ladder as L

ONGOING = ("TOMATO", "STRAWBERRY")


def _cells(tiles, pred):
    return [c for row in tiles for c in row if isinstance(c, dict) and pred(c)]


def run(seed, make_us=None, tape=None, theirs=None):
    """One season; per-day crop census at dawn plus the day's PLANT/WATER/DIG ops."""
    env = L._env(seed, 0.0)
    us = make_us() if make_us else None
    rows, ops = {}, collections.defaultdict(collections.Counter)
    for t in range(719):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        farm = obs["farms"][0]
        if hour == 0:
            tiles = farm["tiles"]
            crops = _cells(tiles, lambda c: c.get("kind") == "PLANT")
            rows[day] = dict(
                crops=len(crops),
                ongoing=sum(1 for c in crops if c.get("crop") in ONGOING),
                weeds=len(_cells(tiles, lambda c: c.get("kind") == "WEED")),
                # A tile one dry day from turning to weed. If this is ever large we are not
                # maintaining the field, we are gambling with it.
                dry=sum(1 for c in crops if c.get("consecutive_unwatered", 0) >= 1),
            )
        if us is not None:
            a = us(obs)
            f0, h0, m0 = a["farmer"], a["hands"], a["market"]
        else:
            f0, h0, m0 = tape[t] if t < len(tape) else (["PASS"], [], [])
        n0 = len(farm.get("hands") or [])
        for act in [f0, *list(h0)[:n0]]:
            if isinstance(act, list) and act and act[0] in ("WATER", "PLANT", "DIG", "HARVEST",
                                                            "FERTILIZE"):
                ops[day][act[0]] += 1
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": f0, "hands": list(h0)[:n0], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    for d, r in rows.items():
        r.update(ops[d])
        prev = rows.get(d - 1)
        # Weeds only appear from a crop that went two days dry, so the rise in the weed count is the
        # number of plants killed by neglect that night (DIG removes them, hence the max()).
        r["lost"] = max(0, r["weeds"] - prev["weeds"]) if prev else 0
    return rows, float(env.state[0].observation["farms"][0]["money"])


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    mine, theirs = L.tape_plans()
    sched = {int(k): v for k, v in json.loads(pathlib.Path(L.SCHEDULE).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    tape_rows, tape_money = run(seed, tape=mine, theirs=theirs)
    our_rows, our_money = run(seed, make_us=lambda: schedule_agent.make_agent(sched, 0, router=True),
                              theirs=theirs)

    print(f"seed {seed}   tape ${tape_money:,.0f}   ours ${our_money:,.0f} "
          f"({100 * our_money / tape_money:.0f}%)\n")
    print(f"{'':>4} {'CROP TILES':>11} {'ONGOING':>11} {'WEEDS':>11} {'PLANTED':>11} "
          f"{'LOST':>11} {'WATER':>11} {'WATER/CROP':>13}")
    print(f"{'day':>4} {'ours':>5}{'tape':>6} {'ours':>5}{'tape':>6} {'ours':>5}{'tape':>6} "
          f"{'ours':>5}{'tape':>6} {'ours':>5}{'tape':>6} {'ours':>5}{'tape':>6} "
          f"{'ours':>6}{'tape':>7}")
    tot = collections.Counter()
    for d in sorted(set(our_rows) | set(tape_rows)):
        o, t = our_rows.get(d, {}), tape_rows.get(d, {})
        g = lambda r, k: int(r.get(k, 0))
        for k in ("crops", "ongoing", "weeds", "PLANT", "lost", "WATER", "HARVEST", "DIG",
                  "FERTILIZE"):
            tot["o_" + k] += g(o, k)
            tot["t_" + k] += g(t, k)
        ow = g(o, "WATER") / max(1, g(o, "crops"))
        tw = g(t, "WATER") / max(1, g(t, "crops"))
        print(f"{d:>4} {g(o,'crops'):>5}{g(t,'crops'):>6} {g(o,'ongoing'):>5}{g(t,'ongoing'):>6} "
              f"{g(o,'weeds'):>5}{g(t,'weeds'):>6} {g(o,'PLANT'):>5}{g(t,'PLANT'):>6} "
              f"{g(o,'lost'):>5}{g(t,'lost'):>6} {g(o,'WATER'):>5}{g(t,'WATER'):>6} "
              f"{ow:>6.2f}{tw:>7.2f}")
    print()
    print(f"  crop-tile-days (sum of crops)  ours {tot['o_crops']:>6}   tape {tot['t_crops']:>6}"
          f"   {100 * tot['o_crops'] / max(1, tot['t_crops']):>5.0f}%")
    print(f"  of which ongoing               ours {tot['o_ongoing']:>6}   tape {tot['t_ongoing']:>6}")
    for k in ("PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG", "lost"):
        print(f"  {k:<30} ours {tot['o_' + k]:>6}   tape {tot['t_' + k]:>6}")
    print(f"\n  WATER per crop-tile-day        ours {tot['o_WATER'] / max(1, tot['o_crops']):>6.2f}"
          f"   tape {tot['t_WATER'] / max(1, tot['t_crops']):>6.2f}")


if __name__ == "__main__":
    main()
