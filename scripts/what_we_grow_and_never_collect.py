"""What do we BUY and never sow, and PLANT and never harvest? Both are paid for up front.

Alex, 2026-08-25: *"if we know a priori that we cant harvest all of it why are we even planting or
buying the seed"*.

Three separate wastes, and only the third has been measured here before:

1. **Seed bought and never sown.** `BUY_SEED` is paid on purchase (`reference/kaggriculture.py`
   `_do_buy_seed`), so seed sitting in `private["seeds"]` at the bell is cash converted to nothing.
   The carrot arm was cut on 2026-08-25 for exactly this -- 546 seeds against 45 sown, $10,760.
2. **Tiles planted and never harvested.** A PLANT costs a turn and a seed. A tile still carrying
   unharvested yield at the end, or turned to WEED by two unwatered days (`:783`), returns neither.
3. **Stock harvested and then destroyed at the dawn drop.** Already measured: 27.5 units and $3,716
   a season, once hour-23 sales are excluded from the count.

The first two are decided BEFORE the work happens, which is what makes them the interesting ones:
they are knowable a priori. The third is a storage failure at the end of the chain.

Seed prices come from `CROPS[crop]["seed"]`, yield from `max_yield`, and the sale value of a
standing crop is priced at the closing book -- an upper bound, since selling it would walk the book.

    python -u scripts/what_we_grow_and_never_collect.py --range 700 6
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
from concurrent.futures import ProcessPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def _play(job):
    seed, opponent, module_name = job
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    planted = collections.Counter()
    cm = record_fills()
    fills = cm.__enter__()
    try:
        env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
        env.reset(2)
        me = SA.make_agent(sched, 0, router=True)
        them = _build(OPPONENTS[opponent], None)
        for t in range(30 * TPD):
            o0 = env.state[0].observation
            a0 = me(o0, env.configuration)
            for a in [a0["farmer"]] + list(a0["hands"] or []):
                if len(a) >= 2 and a[0] == "PLANT":
                    planted[a[1]] += 1
            n0 = len(o0["farms"][0].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                       "market": a0["market"]},
                      them(env.state[1].observation, env.configuration)])
            if env.done:
                break

        # Seed BOUGHT is an exact fill; seed LEFT is read off the final private state.
        bought = collections.Counter()
        for d, h, op, item, price in fills.at_turn(0, op="BUY_SEED"):
            bought[item] += 1
        obs = env.state[0].observation
        priv = obs.get("private") or {}
        left = {k: int(v or 0) for k, v in (priv.get("seeds") or {}).items()}
        book = {k: int(v or 0) for k, v in
                (((obs.get("market") or {}).get("inventory")) or {}).items()}

        # Standing crop and weeds at the bell.
        standing = collections.Counter()
        weeds = 0
        for row in (obs["farms"][0].get("tiles") or []):
            for cell in row:
                if not isinstance(cell, dict):
                    continue
                if cell.get("kind") == "WEED":
                    weeds += 1
                    continue
                if cell.get("kind") != "PLANT":
                    continue
                crop = cell.get("crop")
                spec = KG.CROPS.get(crop)
                if not spec:
                    continue
                lost = int(spec.get("max_yield", 0)) - int(cell.get("yield_units", 0) or 0)
                if lost > 0:
                    standing[crop] += lost

        seed_cost = {c: KG.CROPS[c]["seed"] for c in KG.CROPS}
        wasted_seed = sum(left.get(c, 0) * seed_cost.get(c, 0) for c in left if c in seed_cost)
        standing_val = sum(n * KG.market_price(c, book.get(c, KG.MARKET_I0))
                           for c, n in standing.items())
        return (dict(bought), dict(planted), dict(left), dict(standing),
                wasted_seed, standing_val, weeds, float(obs["farms"][0]["money"]))
    finally:
        cm.__exit__(None, None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", nargs=2, type=int, default=[700, 6], metavar=("FIRST", "COUNT"))
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()

    seeds = list(range(a.range[0], a.range[0] + a.range[1]))
    jobs = [(s, a.opponent, a.module) for s in seeds]
    print(f"{len(jobs)} seasons vs {a.opponent}, seeds {seeds}\n", flush=True)

    B = collections.Counter()
    P = collections.Counter()
    L = collections.Counter()
    S = collections.Counter()
    tot_seed = tot_stand = tot_weeds = 0.0
    banks = []
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for (seed, _o, _m), r in zip(jobs, pool.map(_play, jobs)):
            bought, planted, left, standing, ws, sv, weeds, bank = r
            B.update(bought)
            P.update(planted)
            L.update(left)
            S.update(standing)
            tot_seed += ws
            tot_stand += sv
            tot_weeds += weeds
            banks.append(bank)
            print(f"  seed {seed:<5} unsown seed ${ws:>8,.0f}   standing crop ${sv:>9,.0f}   "
                  f"weeds {weeds:>3}   bank ${bank:>10,.0f}", flush=True)

    n = max(1, len(seeds))
    print(f"\nper season, mean of {n}\n")
    print(f"{'crop':<13}{'seed bought':>13}{'planted':>9}{'seed LEFT':>11}"
          f"{'units standing':>16}")
    for c in sorted(set(B) | set(P) | set(L) | set(S)):
        print(f"{c:<13}{B[c] / n:>13.1f}{P[c] / n:>9.1f}{L[c] / n:>11.1f}{S[c] / n:>16.1f}")

    print(f"\n{'seed bought and never sown':<34}${tot_seed / n:>10,.0f}")
    print(f"{'crop standing unharvested at bell':<34}${tot_stand / n:>10,.0f}")
    print(f"{'stock destroyed at dawn (measured)':<34}${3716:>10,.0f}")
    print(f"{'weeds on the board at the bell':<34}{tot_weeds / n:>11.1f}")
    print(f"\nmean bank ${sum(banks) / n:,.0f}   "
          f"the first two together are "
          f"{100.0 * (tot_seed + tot_stand) / n / max(1.0, sum(banks) / n):.1f}% of it")
    print("\nBoth of the first two are decided BEFORE the work happens, which is what makes them")
    print("different from the dawn drop: they are knowable a priori.")


if __name__ == "__main__":
    main()
