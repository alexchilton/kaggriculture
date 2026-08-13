"""On a lost game, how much revenue was available from the SAME production, sold differently.

"He out-traded us" is not actionable until it names a quantity. This does, exactly, with no model
of the game beyond the environment's own price function.

The book is fully reconstructible from a replay: every step records `market.inventory`, and holding
the OPPONENT'S schedule exactly as it was, our own sell schedule can be re-priced. Scaling our
per-turn quantities and re-walking the book gives the revenue we would have banked selling more or
less of the same goods at the same times -- the counterfactual the ladder cannot show us.

**The quantities scaled are FILLS.** They used to be `sells[t][pl][item] += int(o[2])` off the
action stream, and our agent re-posts a standing quota on every turn until it fills, so that counted
one intended sale up to 24 times. The counterfactual was then walking a phantom quantity down the
price curve -- 0.5x of an inflated schedule can exceed what we really sold, which turns "sell less"
into "sell more" while still printing a saving. `sold_by_turn` in `kagg/analysis/replay_fills.py` is
what changed hands, per turn, per seat.

`replay()` below already knew half of this: its docstring notes that a 21,216-unit MILK offer sits
in one of these recordings and refuses to add the OPPONENT'S orders to the book for that reason. The
same objection applies to ours, which is the number being scaled.

Two things this deliberately does NOT claim:

- It holds the opponent fixed. A real opponent reacts, so a large cut of our supply would raise
  their price and might raise their volume. Read the numbers as an upper bound on the easy win.
- It re-prices only. It does not re-plan production, so "sell 0.6x" means the other 40% was
  produced and wasted, not that the farm should have been smaller. The production question is
  `revenue_rate` in `kagg/search/scheduler.py`, and it is a different fix.

    PYTHONPATH=. python3 -u scripts/what_we_should_have_sold.py data/ladder/losses/*.json
"""

import collections
import json
import sys

import kaggle_environments.envs.kaggriculture.kaggriculture as kg

sys.path.insert(0, ".")

from kagg.analysis.replay_fills import seat_of, trade_fills

ME = "alex chilton"

#: **Only downward.** A first version searched up to 1.5x and reported that every loss was winnable,
#: with wheat the biggest line in all fourteen -- because scaling a sale up means selling goods we
#: never held, and nothing here checks inventory. Selling *less* needs no feasibility argument: the
#: goods existed, we simply keep them (and they are then destroyed at midnight, which is why the
#: gain below is real revenue rather than a stock transfer).
SCALES = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def load(path):
    """Per-step inventory and the units each side actually SOLD on each turn.

    The recovered town drain and the per-turn buys used to come back from here too and were read by
    nobody -- `replay()` needs the inventory path and our own quantities, and nothing else. The
    drain was a residual of the sell counts, so a wrong sell count produced a matching wrong drain
    and the two then agreed with each other, which is the most convincing way to be wrong.
    """
    d = json.loads(open(path).read())
    teams = (d.get("info") or {}).get("TeamNames") or []
    seat = seat_of(d, ME)
    steps = d["steps"]
    rewards = d.get("rewards") or [s.get("reward") for s in steps[-1]]

    fills = trade_fills(d)
    inv, sells = [], []
    for t, step in enumerate(steps):
        obs = (step[0] or {}).get("observation") or {}
        book = (obs.get("market") or {}).get("inventory")
        if book is None:
            continue
        inv.append(dict(book))
        sells.append([collections.Counter(fills.sold_by_turn[0][t]),
                      collections.Counter(fills.sold_by_turn[1][t])])
    return teams, seat, rewards, inv, sells, fills


def replay(item, seat, inv, sells, scale):
    """Revenue on `item` if our per-turn quantities are scaled, everything else as it happened.

    **Perturbs the OBSERVED book rather than reconstructing it.** The observed inventory path
    already contains the opponent's true effect and the town drain is independent of inventory, so
    removing a fraction of *our own* sales shifts the whole path by exactly our withheld cumulative
    volume:

        inv_cf[t] = inv_obs[t] - (1 - scale) * (our sales before t)

    Each unit is then priced at the shifted inventory and moves it, matching `_process_market`'s
    per-unit lockstep.
    """
    revenue = 0.0
    sold = 0
    withheld = 0
    for t in range(len(inv)):
        ours = int(round(sells[t][seat][item] * scale))
        book = inv[t][item] - withheld
        for _ in range(ours):
            revenue += kg.market_price(item, book)
            book += 1
        sold += ours
        withheld += sells[t][seat][item] - ours
    return revenue, sold


def main(paths):
    grand = collections.Counter()
    for path in paths:
        teams, seat, rewards, inv, sells, fills = load(path)
        gap = (rewards[1 - seat] or 0) - (rewards[seat] or 0)
        print(f"\n{path.split('/')[-1]}   ours ${rewards[seat] or 0:,.0f}   "
              f"{teams[1-seat][:22]} ${rewards[1-seat] or 0:,.0f}   gap ${gap:,.0f}")
        print("  unit columns are FILLS recovered from the shed and the market ledger, never "
              "orders;")
        print("  a product both sides traded on the same turn can be understated -- see "
              f"floored/shared: {sorted(fills.floored)}")
        print(f"  {'product':<12}{'we sold':>9}{'they sold':>11}{'our $':>10}"
              f"{'best x':>8}{'units':>7}{'best $':>10}{'gain':>10}")
        total_gain = 0.0
        for item in ("MILK", "WOOL", "STRAWBERRY", "MELON", "WHEAT", "FERTILIZER"):
            if item not in inv[0]:
                continue
            base_rev, base_units = replay(item, seat, inv, sells, 1.0)
            best = max(((replay(item, seat, inv, sells, s), s)
                        for s in SCALES), key=lambda r: r[0][0])
            (best_rev, best_units), best_scale = best
            gain = best_rev - base_rev
            total_gain += gain
            theirs = sum(sells[t][1 - seat][item] for t in range(len(inv)))
            print(f"  {item:<12}{base_units:>9,}{theirs:>11,}{base_rev:>10,.0f}"
                  f"{best_scale:>8.1f}{best_units:>7,}{best_rev:>10,.0f}{gain:>+10,.0f}")
            grand[item] += gain
        verdict = "WOULD HAVE WON" if total_gain > gap else "still short"
        print(f"  {'TOTAL':<12}{'':>9}{'':>11}{'':>10}{'':>8}{'':>7}{'':>10}"
              f"{total_gain:>+10,.0f}   gap ${gap:,.0f} -> {verdict}")

    print(f"\n\n  where the recoverable money is, summed over {len(paths)} games")
    for item, gain in grand.most_common():
        print(f"    {item:<12}{gain:>+12,.0f}")


if __name__ == "__main__":
    main(sys.argv[1:])
