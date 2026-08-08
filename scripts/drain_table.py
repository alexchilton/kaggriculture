"""Measure the town's whole-season absorption per product, on the installed environment.

`kagg.search.chains.DRAIN_UNITS` is a hard-coded copy of this. It has to be a copy, because the
planner reads it before an episode exists -- but a copy drifts, and this one drifted across an
environment upgrade without anything going red. Run this to regenerate it.

The draw matters. 1.32.6 picks shops **with replacement** up to `MAX_SHOP_INSTANCES`, so a product
can be served by the same shop twice and its drain doubles. That makes the season total a
distribution rather than a number: wool ranges 30 to 750 depending on whether YARN_STORE repeats.
The table stores the mean; the spread is printed here so a caller can see what the mean hides.

    python3 -u scripts/drain_table.py --seeds 32 | tee data/logs/drain_table.log
"""

import argparse
import statistics

from kagg.economics import market as M

BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
        "EGG": 50, "MILK": 160, "WOOL": 200}


def measure(seeds):
    """Season drain per product, as {product: [total for each seed]}."""
    per = {item: [] for item in BASE}
    for seed in seeds:
        totals = {k: sum(v) for k, v in M.drain_per_day(M.observe_unlocks(seed)).items()}
        for item in per:
            per[item].append(totals.get(item, 0))
    return per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=32)
    ap.add_argument("--start", type=int, default=1000)
    args = ap.parse_args()

    seeds = list(range(args.start, args.start + args.seeds))
    per = measure(seeds)

    try:
        from kagg.search import chains as C
        shipped = dict(C.DRAIN_UNITS)
    except Exception:
        shipped = {}

    print(f"  {len(seeds)} seeds, {seeds[0]}..{seeds[-1]}\n")
    print(f"  {'product':<12}{'shipped':>9}{'mean':>8}{'median':>8}{'min':>6}{'max':>6}"
          f"{'stdev':>8}{'ratio':>8}{'$ mean':>10}")
    worth = 0.0
    for item in sorted(BASE, key=lambda x: -BASE[x]):
        vals = per[item]
        mean = statistics.mean(vals)
        worth += mean * BASE[item]
        old = shipped.get(item, 0)
        print(f"  {item:<12}{old:>9}{mean:>8.0f}{statistics.median(vals):>8.0f}"
              f"{min(vals):>6}{max(vals):>6}{statistics.pstdev(vals):>8.0f}"
              f"{(old / mean if mean else 0):>7.2f}x{mean * BASE[item]:>10,.0f}")
    print(f"\n  whole market at base price: ${worth:,.0f}")
    print("\n  paste into kagg/search/chains.py:")
    print("    DRAIN_UNITS = {" + ", ".join(
        f'"{k}": {round(statistics.mean(per[k]))}' for k in BASE) + "}")


if __name__ == "__main__":
    main()
