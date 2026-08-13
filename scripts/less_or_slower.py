"""Is the recoverable money in selling LESS, or in selling the SAME amount better spaced?

`what_we_should_have_sold.py` scaled our per-turn quantities down uniformly and found 12 of 14
losses flip. That test cannot tell the two apart: scaling down reduces the total *and* flattens
the peaks, so "sell 0.7x" is consistent with either diagnosis and the fixes are different. Selling
less means growing less; spacing better means the same farm with a different sell rule.

The book is separable, which makes the comparison exact. Our own contribution to the inventory
path is known, so the path the market would have had WITHOUT us is

    base[t] = inv_obs[t] - (our cumulative sales before t)

and any counterfactual schedule `q` can then be priced against `base[t] + cum_q[t]`, with each unit
quoting at the running inventory and moving it -- the same per-unit lockstep `_process_market` uses.

Four schedules are compared on the same production:

    observed     what we actually did
    downscaled   the best uniform scale <= 1.0 (fewer units, same shape)
    spread       every unit we actually sold, spread evenly over our selling window
    both         the best scale, spread evenly

If `spread` recovers most of the gain, this is a cadence bug in the sell rule and the farm is fine.
If only `downscaled` recovers it, we are growing more than the market can take.

    PYTHONPATH=. python3 -u scripts/less_or_slower.py data/ladder/losses/*.json
"""

import collections
import json
import sys

import kaggle_environments.envs.kaggriculture.kaggriculture as kg

ME = "alex chilton"
SCALES = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")


def load(path):
    d = json.loads(open(path).read())
    teams = (d.get("info") or {}).get("TeamNames") or []
    seat = teams.index(ME)
    steps = d["steps"]
    rewards = d.get("rewards") or [s.get("reward") for s in steps[-1]]
    inv, mine = [], []
    for step in steps:
        book = (((step[0] or {}).get("observation") or {}).get("market") or {}).get("inventory")
        if book is None:
            continue
        inv.append(dict(book))
        c = collections.Counter()
        for o in ((step[seat] or {}).get("action") or {}).get("market", []) or []:
            # SELL ORDER quantities. This script perturbs the observed inventory path by a
            # fraction of them, so an inflated schedule inflates the counterfactual -- see the
            # same argument, and the fix, in `scripts/what_we_should_have_sold.py`.
            if o and o[0] == "SELL":
                c[o[1]] += int(o[2])          # offered, not filled
        mine.append(c)
    return teams, seat, rewards, inv, mine


def base_path(item, inv, mine):
    """The inventory path the market would have had without our sales."""
    out, cum = [], 0
    for t in range(len(inv)):
        out.append(inv[t][item] - cum)
        cum += mine[t][item]
    return out


def price_schedule(item, base, q):
    """Revenue from selling `q[t]` units each turn against `base[t]` plus our own accumulation."""
    revenue, cum = 0.0, 0
    for t in range(len(base)):
        book = base[t] + cum
        for _ in range(int(q[t])):
            revenue += kg.market_price(item, book)
            book += 1
        cum += int(q[t])
    return revenue


def spread(total, turns, lo, hi):
    """`total` units spread as evenly as integer arithmetic allows over turns [lo, hi)."""
    q = [0] * turns
    width = max(1, hi - lo)
    for k in range(int(total)):
        q[lo + (k * width) // max(1, int(total))] += 1
    return q


def main(paths):
    tally = collections.Counter()
    print(f"  {'game':<13}{'product':<12}{'observed':>10}{'downscaled':>12}"
          f"{'spread':>10}{'both':>10}{'winner':>12}")
    for path in paths:
        teams, seat, rewards, inv, mine = load(path)
        name = path.split("/")[-1].split(".")[0]
        for item in ITEMS:
            if item not in inv[0]:
                continue
            base = base_path(item, inv, mine)
            obs_q = [mine[t][item] for t in range(len(inv))]
            total = sum(obs_q)
            if total == 0:
                continue
            active = [t for t, n in enumerate(obs_q) if n]
            lo, hi = active[0], active[-1] + 1

            r_obs = price_schedule(item, base, obs_q)
            best_scale = max(SCALES, key=lambda s: price_schedule(
                item, base, [int(round(n * s)) for n in obs_q]))
            r_down = price_schedule(item, base, [int(round(n * best_scale)) for n in obs_q])
            r_spread = price_schedule(item, base, spread(total, len(base), lo, hi))
            best_both = max(SCALES, key=lambda s: price_schedule(
                item, base, spread(round(total * s), len(base), lo, hi)))
            r_both = price_schedule(item, base, spread(round(total * best_both), len(base), lo, hi))

            cands = {"observed": r_obs, "downscaled": r_down, "spread": r_spread, "both": r_both}
            win = max(cands, key=cands.get)
            tally[win] += 1
            tally[("gain", "downscaled")] += r_down - r_obs
            tally[("gain", "spread")] += r_spread - r_obs
            tally[("gain", "both")] += r_both - r_obs
            print(f"  {name:<13}{item:<12}{r_obs:>10,.0f}{r_down:>12,.0f}"
                  f"{r_spread:>10,.0f}{r_both:>10,.0f}{win:>12}")

    print(f"\n  total gain over observed, summed across every game and product:")
    for k in ("downscaled", "spread", "both"):
        print(f"    {k:<12}{tally[('gain', k)]:>+14,.0f}   best in {tally[k]:>3} of "
              f"{sum(tally[x] for x in ('observed','downscaled','spread','both'))} cases")


if __name__ == "__main__":
    main(sys.argv[1:])
