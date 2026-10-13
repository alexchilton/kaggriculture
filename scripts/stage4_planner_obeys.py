"""Stage 4: given a plan row, does the planner DO it? Asked versus landed, across every world.

The chain this sits in, each stage with its own number so a failure localises to one:

    1 splits    is the world read right                  5 clusters at d3, measured
    2 values    are the amounts right for that world     ridge, held out 5-fold
    3 outcome   does the board end up like his           `scripts/match_worlds.py`
    4 planner   does the planner execute what it is passed   <- this file

Stages 1 and 2 pass and stage 3 fails, so the fault is between them. There are exactly two
candidates and they need different fixes:

    the plan never binds     the planner overrides `plants`/`seeds`/`animals_bought` with its own
                             logic. Fix: make the rows binding.
    the plan is undeliverable  the rows ask for what our bank cannot buy, so they are dropped.
                             Fix: the values, not the wiring.

Asked-versus-landed tells them apart directly, and per world, because a row that binds in one
world and not another is a third thing again.

`landed_rows` reads our own game back with the SAME function that read his, so the two sides
cannot drift apart by definition-shift.
"""
import argparse, json, statistics, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.spataro_landed_schedule import landed_rows
from scripts.spa_targets import SHOP_CLUSTER, CLUSTERS

ARMS = {"planner_tgt":   (ROOT / "submission/planner_tgt/main.py",
                          "data/seed_scripts/spa_targets/milk_berry.json"),
        "planner_spa":   (ROOT / "submission/planner_spa/main.py",
                          "data/seed_scripts/spataro/schedule.json"),
        "planner_kawa":  (ROOT / "submission/planner_pure/main.py",
                          "data/seed_scripts/kawashigi/schedule.json"),
        # The tape arm: d0-6 replayed from his own season, planner from d7 on the SAME season's
        # rows. This is the only arm where "does the planner execute" is a fair question, because
        # it is the only one that hands the planner a board that is actually his.
        "spa_own":       (ROOT / "submission/spa_own/main.py",
                          "data/seed_scripts/spataro/schedule.json")}
OPP = ROOT / "submission/shop0909/main.py"
TPD = 24
CROPS = ("WHEAT", "STRAWBERRY", "CARROT", "MELON")


def play(job):
    arm, seed, seat, upto = job
    from kaggle_environments import make
    path, _ = ARMS[arm]
    pair = [str(path), str(OPP)] if seat == 0 else [str(OPP), str(path)]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    got = landed_rows(env.steps, seat)
    first = None
    for i in range(0, min(len(env.steps), upto * TPD)):
        town = ((env.steps[i][seat].get("observation") or {}).get("town") or {})
        for shop in (town.get("unlocked_shops") or ()):
            if first is None and shop in SHOP_CLUSTER:
                first = shop
    return {"arm": arm, "seed": seed, "seat": seat, "cluster": SHOP_CLUSTER.get(first),
            "rows": {d: {"plants": Counter(got[d]["plants"]),
                         "places": list(got[d]["places"]),
                         "hires": got[d]["hires"], "land": got[d]["land"],
                         "builds": got[d]["builds"],
                         # The MONEY side. Never instrumented before, and the herd stall points
                         # straight at it: one arm asks for 14 animals and another for 23 and both
                         # land ~9, so what binds is cash, not the row. `buys` and `sells` are the
                         # only rows that make cash, and they are the two the extractor leaves as
                         # REQUESTED because the engine clamps them -- so "asked" and "landed"
                         # genuinely differ here and the gap is the thing to read.
                         "buys": dict(got[d]["buys"]), "sells": dict(got[d]["sells"]),
                         "money_dawn": got[d]["money_dawn"]} for d in range(upto)},
            "bank": env.steps[-1][seat]["reward"] or 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", default=["planner_tgt", "planner_spa"])
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--upto", type=int, default=13)
    ap.add_argument("--procs", type=int, default=5)
    args = ap.parse_args()

    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(a, s, t, args.upto) for a in args.arms for s in seeds for t in (0, 1)]
    print(f"{len(jobs)} games, days 0..{args.upto - 1}\n", flush=True)
    with Pool(args.procs) as pool:
        rows = pool.map(play, jobs)

    for arm in args.arms:
        path, plan_path = ARMS[arm]
        plan = json.loads((ROOT / plan_path).read_text())
        mine = [r for r in rows if r["arm"] == arm]
        print(f"{'=' * 76}\n{arm}   plan {plan_path}   mean bank "
              f"{statistics.mean(r['bank'] for r in mine):,.0f}")

        # Season totals first: the single number that says whether the plan binds at all.
        asked = Counter()
        for d in range(args.upto):
            asked.update(plan[str(d)].get("plants") or [])
        ask_herd = Counter()
        for d in range(args.upto):
            ask_herd.update(plan[str(d)].get("places") or [])
        got_c, got_h = Counter(), Counter()
        for r in mine:
            for d in range(args.upto):
                got_c.update(r["rows"][d]["plants"])
                got_h.update(r["rows"][d]["places"])
        n = len(mine)
        print(f"  plants  asked {dict(asked)} total {sum(asked.values())}")
        print(f"          landed " + str({k: round(v / n, 1) for k, v in got_c.items()})
              + f" total {sum(got_c.values()) / n:.1f}   (mean per game)")
        print(f"  herd    asked {dict(ask_herd)} total {sum(ask_herd.values())}")
        print(f"          landed " + str({k: round(v / n, 1) for k, v in got_h.items()})
              + f" total {sum(got_h.values()) / n:.1f}")

        print(f"\n  per day, asked -> landed (mean over {n} games)")
        print(f"  {'d':>2} {'plants asked':>26} {'plants landed':>26} "
              f"{'hire':>9} {'land':>9} {'built':>9}")
        for d in range(args.upto):
            row = plan[str(d)]
            a = Counter(row.get("plants") or [])
            l = Counter()
            for r in mine:
                l.update(r["rows"][d]["plants"])
            f = lambda c, div=1: " ".join(
                f"{k[:4]}{v / div:.0f}" for k, v in sorted(c.items()) if v / div >= 0.5) or "-"
            print(f"  {d:>2} {f(a):>26} {f(l, n):>26} "
                  f"{row.get('hands', 0):>4}/{statistics.mean(r['rows'][d]['hires'] for r in mine):<4.1f} "
                  f"{row.get('land', 0):>4}/{statistics.mean(r['rows'][d]['land'] for r in mine):<4.1f} "
                  f"{row.get('builds', 0):>4}/{statistics.mean(r['rows'][d]['builds'] for r in mine):<4.1f}")

        print(f"\n  the MONEY side: what the row asked to buy and sell, and what settled")
        print(f"  {'d':>2} {'money dawn':>11} {'buy WHEAT':>18} {'sell asked':>34} "
              f"{'sell settled':>34}")
        for d in range(args.upto):
            row = plan[str(d)]
            ask_b = int((row.get("buys") or {}).get("WHEAT", 0))
            got_b = statistics.mean(r["rows"][d]["buys"].get("WHEAT", 0) for r in mine)
            ask_s = row.get("sells") or {}
            got_s = Counter()
            for r in mine:
                got_s.update(r["rows"][d]["sells"])
            f = lambda c, div=1: " ".join(
                f"{k[:4]}{v / div:.0f}" for k, v in sorted(c.items()) if v / div >= 0.5) or "-"
            dawn = [r["rows"][d]["money_dawn"] for r in mine
                    if r["rows"][d]["money_dawn"] is not None]
            print(f"  {d:>2} {statistics.mean(dawn) if dawn else 0:>11,.0f} "
                  f"{ask_b:>8}/{got_b:<8.1f} {f(ask_s):>34} {f(got_s, n):>34}")

        print(f"\n  does the LANDED board differ by world? (if not, the plan is not what drives it)")
        print(f"  {'cluster':12} {'n':>3} " + " ".join(f"{c[:5]:>7}" for c in CROPS)
              + f" {'COW':>5} {'SHEEP':>6}")
        for c in CLUSTERS:
            here = [r for r in mine if r["cluster"] == c]
            if not here:
                continue
            cc, hh = Counter(), Counter()
            for r in here:
                for d in range(args.upto):
                    cc.update(r["rows"][d]["plants"])
                    hh.update(r["rows"][d]["places"])
            k = len(here)
            print(f"  {c:12} {k:>3} " + " ".join(f"{cc[x] / k:>7.1f}" for x in CROPS)
                  + f" {hh['COW'] / k:>5.1f} {hh['SHEEP'] / k:>6.1f}")
        print()


if __name__ == "__main__":
    main()
