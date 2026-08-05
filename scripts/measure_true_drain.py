"""Is `DRAIN_UNITS` right? The inventory trace on a real tape says how much the town truly absorbs.

`chains.DRAIN_UNITS` is the number every allocation argument in this project rests on -- the mix, the
scheduler's payback ranking, `allocation_calculator.py`, the melon-saturates-at-11-tiles conclusion. It
was measured in `data/logs/market_ceiling.log` from `kagg/economics/market.py`'s schedule, i.e. from our
model of the shops, never against a real game.

`measure_realised_revenue.py` says both seats together bank **1.40x** the purse that table implies. One
of the two numbers is wrong, and since the banks are read straight off the tape it is the table.

Town inventory is the arbiter. It starts at 10,000 per product; players' fills add to it and the shops'
demand removes it, so across the whole season:

    inv_final - 10000  =  total_fills - total_absorbed
    total_absorbed     =  total_fills - inv_final + 10000

and if `inv_final` sits near 10,000 the market **cleared** -- everything both players sold was eaten,
and the ceiling was never reached. If it climbs far above 10,000 the market **glutted** and the drain
really was the binding constraint.

That distinction decides the whole strategy. A cleared market means the constraint is our own
production capacity, not the town's appetite, and every "saturates at N tiles" conclusion this project
has drawn is an artifact of the table rather than a fact about the game.
"""

import json
import pathlib

import numpy as np

from kagg.search import chains as C

START_INV = 10000
REPLAYS = sorted(pathlib.Path("data/seed_scripts/new_leader").glob("*.json"))


def inventory_trace(path):
    """`{product: [inventory at each recorded turn]}` plus the price trace alongside it."""
    d = json.load(open(path))
    inv, pri = {}, {}
    for step in d["steps"]:
        obs = (step[0] or {}).get("observation") or {}
        m = obs.get("market")
        if not m:
            continue
        for p, v in m["inventory"].items():
            inv.setdefault(p, []).append(int(v))
        for p, v in m["prices"].items():
            pri.setdefault(p, []).append(float(v))
    return inv, pri


print("=" * 104)
print("TOWN INVENTORY ACROSS A REAL SEASON.  starts at 10,000.  up = players outsell the shops")
print("=" * 104)
print(f"{'product':>12} {'DRAIN_UNITS':>12} {'inv min':>9} {'inv max':>9} {'inv final':>10} "
      f"{'net':>8} {'price 1st':>10} {'price last':>11} {'verdict':>10}")

verdicts = {}
for path in REPLAYS[:1]:
    inv, pri = inventory_trace(path)
    for prod in sorted(C.DRAIN_UNITS, key=lambda p: -C.DRAIN_UNITS[p]):
        a = np.asarray(inv[prod])
        p = np.asarray(pri[prod])
        net = int(a[-1]) - START_INV
        # Glutted means the players' supply outran the town: inventory piled up and the price sagged.
        # Cleared means the shops ate everything offered and the ceiling never bound.
        glut = net > 500
        verdicts[prod] = "GLUT" if glut else "CLEARED"
        print(f"{prod:>12} {C.DRAIN_UNITS[prod]:>12} {a.min():>9,} {a.max():>9,} {a[-1]:>10,} "
              f"{net:>+8,} {p[0]:>10.0f} {p[-1]:>11.0f} {verdicts[prod]:>10}")

print()
print("=" * 104)
print("WHAT THIS MEANS FOR `DRAIN_UNITS`")
print("=" * 104)
cleared = [p for p, v in verdicts.items() if v == "CLEARED"]
glutted = [p for p, v in verdicts.items() if v == "GLUT"]
print(f"CLEARED (town ate everything offered; the drain never bound): {', '.join(sorted(cleared)) or 'none'}")
print(f"GLUTTED (supply outran demand; the drain is real):            {', '.join(sorted(glutted)) or 'none'}")
print()
if cleared:
    print("For every CLEARED product, `DRAIN_UNITS` is NOT a ceiling on what we can sell -- the shops")
    print("were still hungry at the final bell. Sizing a mix 'to the drain' therefore *undersizes* it,")
    print("and every saturation conclusion drawn from that table needs re-deriving.")