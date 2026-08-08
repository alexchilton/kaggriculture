"""Per-product season absorption budget vs price depth, computed from the env source alone.

Produces the tables in `docs/fable_market_technique_2026-08-08.md`: how many units of each product
the town will ever absorb in a season, how deep the book is at an acceptable price, and what a dump
of n units actually realises. Nothing here plays a game -- it is arithmetic on `MARKET_PARAMS`,
`SHOPS` and `TOWN_CENTER_PRODUCTS`, so it follows the installed env version automatically.

    python -u scripts/market_absorption.py
"""
import sys
sys.path.insert(0, ".")
from kaggle_environments.envs.kaggriculture import kaggriculture as kg

P = list(kg.PRODUCTS)
I0 = kg.MARKET_I0

# --- 1. which shops carry which product, and the per-tick pull
print("=== shops per product (1 per shop-tick, 2 if the shop has a single product) ===")
pull = {}
for item in P:
    tot = 0
    names = []
    for s, prods in kg.SHOPS.items():
        if item in prods:
            m = 2 if len(prods) == 1 else 1
            tot += m
            names.append(f"{s}x{m}")
    pull[item] = tot
    print(f"{item:11s} shop_pull_per_tick(all 8 unlocked)={tot:3d}  {names}")

# --- 2. season drain, both econ versions, assuming shops unlock every 3 days in some order
TPD = 24
DAYS = 30
SHOP_INTERVAL = 4


def season_drain(center_interval, center_schedule, unlock_every=3, n_shops=8):
    """Units of each product the town removes over the whole 30-day season.

    Shops unlock one every `unlock_every` days. Order is RNG so we average over the
    8! orders by using the expected count: on day d, k=min(8, d//unlock_every) shops
    are live, and each is a uniform draw without replacement, so the expected pull for
    product p is k/8 * (total pull if all 8 were live).
    """
    tot = {p: 0.0 for p in P}
    for day in range(DAYS):
        k = min(n_shops, day // unlock_every)
        for off in range(TPD):
            step = day * TPD + off
            if step % SHOP_INTERVAL == 0:
                for p in P:
                    tot[p] += pull[p] * k / 8.0
            if step % center_interval == 0:
                cm = next(m for th, m in center_schedule if day >= th)
                for p in kg.TOWN_CENTER_PRODUCTS:
                    tot[p] += cm
    return tot


d_1322 = season_drain(12, [(20, 4), (10, 2), (0, 1)])
d_1326 = season_drain(24, [(0, 1)])

print("\n=== season-total town absorption (expected, uniform unlock order) ===")
print(f"{'product':11s} {'1.32.2':>9s} {'1.32.6':>9s}   {'per-day late (all 8 shops)':>28s}")
for p in P:
    late = pull[p] * (TPD // SHOP_INTERVAL) + (1 if p in kg.TOWN_CENTER_PRODUCTS else 0)
    print(f"{p:11s} {d_1322[p]:9.0f} {d_1326[p]:9.0f}   {late:28d}")

# --- 3. depth: units sellable from I0 before price falls below fractions of base
print("\n=== depth from balanced book (inv = I0): units to reach x*base ===")
hdr = f"{'product':11s} {'base':>5s}"
for f in (0.9, 0.75, 0.5, 0.25):
    hdr += f" {'>='+str(f):>10s}"
print(hdr + "   above_func")
for p in P:
    row = f"{p:11s} {kg.MARKET_PARAMS[p]['base']:5d}"
    for f in (0.9, 0.75, 0.5, 0.25):
        inv, n = I0, 0
        while n < 100000 and kg.market_price(p, inv) >= f * kg.MARKET_PARAMS[p]["base"]:
            inv += 1
            n += 1
        row += f" {n:10d}"
    print(row + f"   {kg.MARKET_PARAMS[p]['above_func']}")

# --- 4. the premium for waiting: price at a deficit built by k days of drain
print("\n=== price after k days of untouched drain (1.32.6, all 8 shops live) ===")
print(f"{'product':11s} {'base':>5s} {'d=0':>6s} {'2d':>6s} {'5d':>6s} {'10d':>6s}")
for p in P:
    late = pull[p] * (TPD // SHOP_INTERVAL) + (1 if p in kg.TOWN_CENTER_PRODUCTS else 0)
    row = f"{p:11s} {kg.MARKET_PARAMS[p]['base']:5d}"
    for k in (0, 2, 5, 10):
        row += f" {kg.market_price(p, I0 - late * k):6d}"
    print(row)

# --- 5. marginal revenue of dumping vs drip, wheat and melon, 1.32.6 late season
print("\n=== dump n now vs drip at the drain rate: mean $/unit ===")
from kagg.economics import market as M
for p in ("WHEAT", "MELON", "MILK", "WOOL", "STRAWBERRY", "FERTILIZER"):
    late = pull[p] * (TPD // SHOP_INTERVAL) + (1 if p in kg.TOWN_CENTER_PRODUCTS else 0)
    print(f"\n{p}: drain {late}/day at full unlock")
    for n in (10, 25, 50, 100, 200, 400):
        rev, inv, _ = M.sell_revenue(p, I0, n)
        print(f"  dump {n:4d} from balanced book -> ${rev:8d}  mean ${rev/n:7.2f}  end price ${kg.market_price(p, inv)}")
