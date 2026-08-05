"""How much of the town's money did the leader actually take?

`measure_market_share.py` showed the order counts are useless as a share estimate: he *requests*
171-226% of every drain, because over-requesting a SELL is free (`_process_market` stops when the shed
runs dry). So the tape's SELL quantities measure intent, not capture.

Money is the honest axis. Every turn carries the seat's bank and the market's quoted prices, so:

    gross_revenue  ~=  final_bank - 3000 + total_spend

and the two spend terms that dominate -- BUY_PRODUCT (his wheat trading operation) and BUY_SEED -- are
priced on the tape at the turn they were ordered. Hires and land are fixed-price ladders we already know.

Two bounds are reported rather than one number, because a fill walks the price and an order is quoted
at the pre-walk price:

- **lower bound** on revenue: assume every BUY order filled at its quoted price (max spend)
- **upper bound**: assume the buys we cannot price cost nothing

The question this settles is narrow and worth stating: is a single player's realised take of a
contested drain nearer **0.5** (the old `OPPONENT_SHARE`) or **1.0** (what reproduces his herd)? Any
estimate inside +-10% answers it, so precision beyond that is not needed.
"""

import collections
import json
import pathlib

import numpy as np

from kagg.search import chains as C

LEADER = "somewhere after"
START_BANK = 3000.0
# The Fibonacci hire ladder, reset every dawn (`kaggriculture.py:847-851`). Index = nth hire that day.
HIRE_LADDER = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
LAND_PRICES = [1000, 2000, 4000]


def walk(path):
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    per = {}
    for seat, name in enumerate(names):
        spend = collections.Counter()
        sell_revenue_pure = 0.0        # money gained on turns with sells and no buys: exact
        pure_turns = 0
        sell_turns = 0
        bank = START_BANK
        hires_today, day_now = 0, 0
        n_land = 0
        for t, step in enumerate(d["steps"]):
            st = step[seat] or {}
            obs = st.get("observation") or {}
            farms, market = obs.get("farms"), obs.get("market")
            day = obs.get("day", day_now)
            if day != day_now:
                hires_today, day_now = 0, day
            prev_bank = bank
            if farms and seat < len(farms):
                bank = float(farms[seat]["money"])
            prices = (market or {}).get("prices", {})
            orders = (st.get("action") or {}).get("market") or []
            has_sell = any(o and o[0] == "SELL" for o in orders)
            has_buy = any(o and o[0] in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL",
                                         "HIRE", "BUY_LAND") for o in orders)
            if has_sell:
                sell_turns += 1
                if not has_buy and bank > prev_bank:
                    sell_revenue_pure += bank - prev_bank
                    pure_turns += 1
            for o in orders:
                if not o:
                    continue
                kind = o[0]
                qty = int(o[2]) if len(o) > 2 and str(o[2]).lstrip("-").isdigit() else 1
                if kind == "BUY_PRODUCT":
                    spend["BUY_PRODUCT"] += qty * float(prices.get(o[1], 0))
                elif kind == "BUY_SEED":
                    spend["BUY_SEED"] += qty * float(prices.get(o[1], 0))
                elif kind == "BUY_ANIMAL":
                    spend["BUY_ANIMAL"] += qty * 500.0
                elif kind == "HIRE":
                    spend["HIRE"] += HIRE_LADDER[min(hires_today, len(HIRE_LADDER) - 1)]
                    hires_today += 1
                elif kind == "BUY_LAND":
                    if n_land < len(LAND_PRICES):
                        spend["BUY_LAND"] += LAND_PRICES[n_land]
                        n_land += 1
        per[name] = dict(bank=bank, spend=spend, total_spend=sum(spend.values()),
                         pure=sell_revenue_pure, pure_turns=pure_turns, sell_turns=sell_turns)
    return names, per


# The season's whole purse: what the town pays out across every product, at base price.
BASE_PRICE = {"WHEAT": 24.15, "CARROT": 33.98, "TOMATO": 57.68, "STRAWBERRY": 116.41,
              "MELON": 250.0, "EGG": 49.06, "MILK": 156.86, "WOOL": 199.78}
PURSE = sum(C.DRAIN_UNITS[p] * BASE_PRICE[p] for p in C.DRAIN_UNITS)

print("=" * 100)
print(f"THE TOWN'S PURSE: ${PURSE:,.0f} across all eight products (drain units x base price)")
print("=" * 100)

rows = []
for path in sorted(pathlib.Path("data/seed_scripts/new_leader").glob("*.json")):
    names, per = walk(path)
    if LEADER not in per:
        continue
    print(f"\n{path.name}")
    for name in names:
        p = per[name]
        gross_hi = p["bank"] - START_BANK + p["total_spend"]
        tag = "LEADER" if name == LEADER else "opp   "
        print(f"  {tag} {name:<16} bank ${p['bank']:>9,.0f}  spend ${p['total_spend']:>9,.0f}"
              f"  => gross ${gross_hi:>9,.0f}  = {gross_hi/PURSE:>5.0%} of purse")
        print(f"         spend breakdown: "
              + "  ".join(f"{k} ${v:,.0f}" for k, v in sorted(p["spend"].items())))
        print(f"         exact pure-sell revenue ${p['pure']:>9,.0f} "
              f"over {p['pure_turns']}/{p['sell_turns']} unambiguous sell turns")
        if name == LEADER:
            rows.append((gross_hi, p["pure"], p["bank"]))
        else:
            rows.append((-gross_hi, -p["pure"], -p["bank"]))

his = [r for r in rows if r[0] > 0]
opp = [(-a, -b, -c) for a, b, c in rows if r"" == "" and a < 0]
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
if his:
    g = float(np.mean([r[0] for r in his]))
    pu = float(np.mean([r[1] for r in his]))
    print(f"his mean gross revenue      ${g:,.0f}   = {g/PURSE:.2f} of the town's purse")
    print(f"his mean exact pure-sell    ${pu:,.0f}   = {pu/PURSE:.2f} (a floor: excludes mixed turns)")
if opp:
    go = float(np.mean([r[0] for r in opp]))
    print(f"opponent mean gross revenue ${go:,.0f}   = {go/PURSE:.2f}")
    print(f"both seats together                      = {(g+go)/PURSE:.2f} of the purse")
print()
print("If both seats together approach 1.0, a single seat's realised share is ~0.5 and the old")
print("OPPONENT_SHARE was right for REVENUE. Sizing capacity is still a separate question: you")
print("must be able to serve the whole drain to be the one who serves half of it.")