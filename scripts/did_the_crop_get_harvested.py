"""Per crop: how many units the ground produced, how many we collected, and where the rest went.

A crop allocation is only worth what the crew actually harvests. Every crop-value model in this
repo -- the analytic curve, the fork sweep -- prices UNITS GROWN, and is fiction if those units are
never picked up. This measures the gap directly.

Units are tracked off the board rather than the action stream, because the action encoding has
already produced three wrong answers today (offers counted as fills, `BUY_SEED` parsed as empty,
`HARVEST` counted as zero). A tile's `yield_units` rising is production; falling is collection;
holding units at the close, or turning to WEED while holding them, is loss.

Cadence is the thing to watch, because the crops differ sharply:

    WHEAT       one-shot, first yield d+2,  6 units       collect once per cycle
    CARROT      one-shot, first yield d+2,  4 units       collect once per cycle
    TOMATO      ONGOING,  first yield d+8,  interval 1     collect EVERY DAY, 4 times
    STRAWBERRY  ONGOING,  first yield d+10, interval 2     collect every 2 days, 4 times
    MELON       one-shot, first yield d+10, 6 units        collect once per cycle

Tomato's daily cadence costs four visits per tile per cycle against wheat's one. If tomato shows a
low collection rate, that is the crew failing to keep up rather than the crop being weak -- a
different conclusion with a different fix.

Watering matters for the same reason: `weedSpawnChance` is 0 on our grids, so **every weed is a
tile we stopped watering** (two days unwatered turns a crop into a weed).

    python -u scripts/did_the_crop_get_harvested.py --seed 3
    python -u scripts/did_the_crop_get_harvested.py --seed 3 --opponent data/sweep/frozen_1186_opponent.py
"""
import argparse
import collections
import importlib
import pathlib
import sys

sys.path.insert(0, ".")

import reference.kaggriculture as KG

REPO = pathlib.Path(__file__).resolve().parent.parent


def audit(seed, opponent, module="kagg.search.schedule_agent"):
    from kaggle_environments import make

    A = importlib.import_module(module)
    PLAN = importlib.import_module("kagg.plan")
    sched = PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json"))

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)

    grown = collections.Counter()      # units that appeared on a tile
    collected = collections.Counter()  # units that left a tile while it stayed a crop
    unwatered = collections.Counter()  # tile-days a crop sat unwatered
    weeded = collections.Counter()     # tiles that became WEED (all of them are missed waterings)
    rotted = collections.Counter()     # units lost ON a tile that turned to WEED
    prev = {}

    for t in range(719):
        o = env.state[0].observation
        cur, weed_now = {}, {}
        for y, row in enumerate(o["farms"][0]["tiles"]):
            for x, c in enumerate(row):
                key = (x, y)
                if isinstance(c, dict) and c.get("crop"):
                    cur[key] = (c["crop"], c.get("yield_units", 0))
                    if c.get("consecutive_unwatered", 0) > 0:
                        unwatered[c["crop"]] += 1
                elif c == "WEED" or (isinstance(c, dict) and c.get("kind") == "WEED"):
                    was = prev.get(key)
                    weed_now[key] = True
                    if was:
                        weeded[was[0]] += 1
        for key, (crop, units) in cur.items():
            was = prev.get(key)
            if was and was[0] == crop:
                if units > was[1]:
                    grown[crop] += units - was[1]
                elif units < was[1]:
                    collected[crop] += was[1] - units
            elif units:
                grown[crop] += units
        # **A tile that STOPS being its crop had its units collected.** A one-shot HARVEST
        # demolishes the tile, so tracking only same-crop decreases counted wheat, carrot and melon
        # at 0-2% while strawberry -- ongoing, tile persists -- read a correct 100%. Units on a tile
        # that turned to WEED are a loss, not a collection, and are attributed there instead.
        for key, (crop, units) in prev.items():
            if units and cur.get(key, (None,))[0] != crop:
                if weed_now.get(key):
                    rotted[crop] += units
                else:
                    collected[crop] += units
        prev = cur
        env.step([me(o, t), env.state[1].observation and opponent(env.state[1].observation, t)])
        if env.done:
            break

    fin = env.state[0].observation
    standing = collections.Counter()
    for row in fin["farms"][0]["tiles"]:
        for c in row:
            if isinstance(c, dict) and c.get("crop") and c.get("yield_units"):
                standing[c["crop"]] += c["yield_units"]
    return grown, collected, standing, unwatered, weeded, rotted, env.steps[-1][0]["reward"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--opponent", default="submission/main.py")
    args = ap.parse_args()

    import importlib.util
    spec = importlib.util.spec_from_file_location("opp", args.opponent)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    opp = mod.agent

    grown, collected, standing, unwatered, weeded, rotted, money = audit(args.seed, opp)

    print(f"seed {args.seed}, opponent {args.opponent}, final bank ${money:,.0f}\n")
    print(f"{'crop':<12}{'cadence':>10}{'grown':>8}{'collected':>11}{'rate':>7}"
          f"{'standing':>10}{'rotted':>8}{'weeded':>8}")
    for c in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"):
        s = KG.CROPS[c]
        cad = f"every {s['interval']}d" if s["ongoing"] else "one-shot"
        g, k = grown[c], collected[c]
        rate = f"{k / g:.0%}" if g else "-"
        print(f"{c:<12}{cad:>10}{g:>8}{k:>11}{rate:>7}{standing[c]:>10}"
              f"{rotted[c]:>8}{weeded[c]:>8}")
    tot_g, tot_k = sum(grown.values()), sum(collected.values())
    print(f"\n{'TOTAL':<12}{'':>10}{tot_g:>8}{tot_k:>11}"
          f"{(tot_k / tot_g if tot_g else 0):>7.0%}{sum(standing.values()):>10}"
          f"{sum(rotted.values()):>8}{sum(weeded.values()):>8}")
    print("\nweeded tiles are ALL missed waterings: weedSpawnChance is 0 on our grids")


if __name__ == "__main__":
    main()
