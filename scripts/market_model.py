"""The order book as a standalone system, with no game attached.

**Why this exists.** Every market conclusion in this project has been reached by playing 720-turn
seasons and reading the bank afterwards, which is slow, confounded by routing and feeding and land
buying, and has produced at least three confident wrong answers in a single day. The book itself is
much simpler than the game around it, and most of the questions are about the book:

  - how much can we actually sell before the price stops being worth having?
  - does selling in fewer, larger batches beat selling every turn, and by how much?
  - how much does an opponent selling the same product cost us?

None of those need a farm. They need `market_price`, a production stream, and the town's drain.

**The model, stated exactly.** `market_price` is a pure function of `inventory` and
`_process_market` moves it by one per unit committed, so a sale of `n` units walks the book down one
step at a time and earns the sum of those `n` prices -- not `n` times the quoted price. The town
removes stock on a fixed interval, which is the only thing that ever pushes the book back up. So:

    inventory(t+1) = inventory(t) + our_sales(t) + their_sales(t) - town_drain(t)
    revenue of selling n at time t = sum_{k=0}^{n-1} market_price(inventory(t) + k)

That is the whole system, and it is exact against the environment rather than an approximation --
`test_the_price_curve_math.py` pins the price function and `kagg/analysis/fills.py` confirmed the
one-unit-at-a-time settlement in real games.

    PYTHONPATH=. python3 -u scripts/market_model.py
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "reference"))
import kaggriculture as kg  # noqa: E402

TURNS = 720
SHOP_TICK = 4
CENTRE_TICK = 24


def drain_per_turn(prod, n_shop_instances):
    """Units the town removes on an average turn, from `_town_consume`'s two clocks."""
    per_shop_tick = 0.0
    for shop, prods in kg.SHOPS.items():
        if prod in prods:
            per_shop_tick += (2.0 if len(prods) == 1 else 1.0)
    # `n_shop_instances` is how many of the 8 draws landed on shops selling this product; scale the
    # per-type rate by the observed count rather than assuming one of each.
    if per_shop_tick > 0:
        share = n_shop_instances / max(1.0, sum(1 for p in kg.SHOPS.values() if prod in p))
        per_shop_tick *= share
    centre = 1.0 if prod in kg.TOWN_CENTER_PRODUCTS else 0.0
    return per_shop_tick / SHOP_TICK + centre / CENTRE_TICK


def sell(inventory, n, prod):
    """Revenue for dumping `n` units starting at `inventory`, walking the book one unit per sale."""
    total = 0
    for k in range(n):
        total += kg.market_price(prod, inventory + k, None)
    return total, inventory + n


def simulate(prod, produced, shops, policy, rival_per_turn=0.0, start=None):
    """Run one season of the book alone. `policy(turn, held)` returns units to offer this turn."""
    inv = float(kg.MARKET_I0 if start is None else start)
    d = drain_per_turn(prod, shops)
    held = 0.0
    made_per_turn = produced / float(TURNS)
    revenue = 0
    sold = 0
    for t in range(TURNS):
        held += made_per_turn
        n = int(min(held, policy(t, held)))
        if n > 0:
            r, inv = sell(int(round(inv)), n, prod)
            revenue += r
            held -= n
            sold += n
        inv += rival_per_turn
        inv = max(0.0, inv - d)
    return revenue, sold, inv


def policies(shops, prod, produced):
    """The candidate shapes, including the two the agent actually implements."""
    d = drain_per_turn(prod, shops)
    return {
        "dump everything on turn 0": lambda t, h: (10 ** 6 if t == 0 else 0),
        "sell everything, every turn": lambda t, h: h,
        "every turn, capped at 30": lambda t, h: min(h, 30),
        "every 4th turn (drain cadence)": lambda t, h: (h if t % 4 == 0 else 0),
        "every 4th turn, capped 30": lambda t, h: (min(h, 30) if t % 4 == 0 else 0),
        "at the town's drain rate": lambda t, h: min(h, max(1.0, d)),
        "hold to the last day, then dump": lambda t, h: (10 ** 6 if t >= TURNS - 24 else 0),
    }


def main():
    print("The book alone: no farm, no routing, no feeding. Revenue for one season of production.\n")
    print("Shops = how many of the 8 unlocked draws sell this product. `drain` is units/turn the")
    print("town removes. Production is spread evenly across the season.\n")

    for prod, produced in (("WOOL", 160), ("MILK", 235), ("STRAWBERRY", 280), ("MELON", 82)):
        for shops in (0, 1, 3):
            d = drain_per_turn(prod, shops)
            print(f"=== {prod}  produced {produced}  shops {shops}  "
                  f"drain {d:.3f}/turn = {d * TURNS:.0f} a season  "
                  f"base ${kg.MARKET_PARAMS[prod]['base']} ===")
            rows = []
            for name, pol in policies(shops, prod, produced).items():
                rev, sold, inv = simulate(prod, produced, shops, pol)
                rows.append((rev, name, sold, inv))
            best = max(r[0] for r in rows)
            for rev, name, sold, inv in sorted(rows, reverse=True):
                gap = "" if rev == best else f"  ({100.0 * rev / best:.0f}% of best)"
                print(f"    {name:<32} ${rev:>8,}  {sold:>4} units  "
                      f"${rev / max(1, sold):>6.1f}/unit  end inv {inv - kg.MARKET_I0:+.0f}{gap}")
            print()

    print("=" * 78)
    print("CONTESTED: the same book with an opponent adding units every turn (WOOL, 1 shop)")
    print("=" * 78)
    for rival in (0.0, 0.1, 0.2, 0.4):
        row = []
        for name, pol in policies(1, "WOOL", 160).items():
            rev, sold, _inv = simulate("WOOL", 160, 1, pol, rival_per_turn=rival)
            row.append((rev, name))
        row.sort(reverse=True)
        print(f"  rival adds {rival:.1f}/turn ({rival * TURNS:.0f} a season):  "
              f"best = {row[0][1]!r} at ${row[0][0]:,}   "
              f"worst = {row[-1][1]!r} at ${row[-1][0]:,}")


if __name__ == "__main__":
    sys.exit(main())
