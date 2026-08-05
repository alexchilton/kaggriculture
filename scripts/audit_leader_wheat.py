"""What does the leader actually do with wheat? Kimi's question, answered off the tape.

Wheat is the one product whose absorbed/drain ratio is absurd: 3.41, against 0.88-1.01 for everything
else (`scripts/measure_true_drain.py`). And each seat spends **$43,475 on BUY_PRODUCT** while the whole
crop-seed bill is $16,638. So wheat is moving through his farm at a volume no 40-tile planting explains.

Three hypotheses, and they imply completely different chain libraries:

1. **Pure production.** He grows 40 tiles and sells the harvest. Makes no sense against a 662-unit
   drain, and would mean our 16-tile answer is right and his is wasteful.
2. **Animal feed.** FEED consumes one wheat per animal per feeding. 14 animals over ~23 feeds each is
   ~320 units he must source, and growing it avoids buying it. This is a *production* chain we already
   have (`grow(sell=False)` + `ranch(buy_feed=False)`), just never selected.
3. **Commodity arbitrage.** Buy wheat at 25 early, sell at 54 late, pocket the spread. This needs no
   tiles, no units and no land -- only capital and the inventory slot -- and our chain library **cannot
   express it at all**. If this is what he is doing, it is a whole missing dimension of the search.

The tape distinguishes them exactly, because every wheat order and every FEED op is recorded. The
accounting identity is:

    wheat_bought + wheat_harvested  =  wheat_fed + wheat_sold + wheat_left_in_shed

so whichever term dominates the right-hand side names the strategy.
"""

import collections
import json
import pathlib

import numpy as np

LEADER = "somewhere after"
FEED_OPS = {"FEED"}


def audit(path):
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    seat = names.index(LEADER)
    bought = collections.Counter()      # day -> units of WHEAT bought
    sold = collections.Counter()
    seeds = collections.Counter()
    feeds = collections.Counter()       # day -> FEED ops
    buy_cost, sell_take = 0.0, 0.0
    shed_wheat = []
    for t, step in enumerate(d["steps"]):
        st = step[seat] or {}
        obs = st.get("observation") or {}
        day = obs.get("day", t // 24)
        prices = (obs.get("market") or {}).get("prices", {})
        priv = obs.get("private") or {}
        shed = priv.get("shed") or {}
        if "WHEAT" in shed:
            shed_wheat.append((day, int(shed["WHEAT"])))
        a = st.get("action") or {}
        for o in (a.get("market") or []):
            if not o:
                continue
            qty = int(o[2]) if len(o) > 2 and str(o[2]).lstrip("-").isdigit() else 1
            if o[1] != "WHEAT" if len(o) > 1 else True:
                continue
            if o[0] == "BUY_PRODUCT":
                bought[day] += qty
                buy_cost += qty * float(prices.get("WHEAT", 0))
            elif o[0] == "SELL":
                sold[day] += qty
                sell_take += qty * float(prices.get("WHEAT", 0))
            elif o[0] == "BUY_SEED":
                seeds[day] += qty
        # Unit ops live under `farmer` (a single op list) and `hands` (one op list per hand) -- there is
        # no `units` key. Reading a key that does not exist reported FEED = 0 for a farm with 14
        # animals, which is the kind of silent zero this project keeps being bitten by.
        farmer = a.get("farmer") or []
        if farmer and farmer[0] in FEED_OPS:
            feeds[day] += 1
        for hand in (a.get("hands") or []):
            if hand and hand[0] in FEED_OPS:
                feeds[day] += 1
    return dict(bought=bought, sold=sold, seeds=seeds, feeds=feeds,
                buy_cost=buy_cost, sell_take=sell_take, shed=shed_wheat, names=names, seat=seat)


for path in sorted(pathlib.Path("data/seed_scripts/new_leader").glob("*.json"))[:1]:
    r = audit(path)
    tb, ts, tsd, tf = (sum(r[k].values()) for k in ("bought", "sold", "seeds", "feeds"))
    print("=" * 96)
    print(f"LEADER WHEAT AUDIT -- {path.name}, seat {r['seat']} of {r['names']}")
    print("=" * 96)
    print(f"  wheat SEEDS bought (tiles planted) : {tsd:>6}")
    print(f"  wheat PRODUCT bought from town     : {tb:>6}   costing ${r['buy_cost']:>10,.0f}")
    print(f"  wheat SOLD to town                 : {ts:>6}   taking  ${r['sell_take']:>10,.0f}")
    print(f"  FEED ops emitted (1 wheat each)    : {tf:>6}")
    print()
    print(f"  net wheat trade P&L (sell - buy)   : ${r['sell_take'] - r['buy_cost']:>+10,.0f}")
    print()

    print("  by day -- when he buys, when he sells, when he feeds")
    print(f"  {'day':>4} {'bought':>7} {'sold':>6} {'seeds':>6} {'feeds':>6} {'shed':>6}")
    shed_by_day = {}
    for day, q in r["shed"]:
        shed_by_day[day] = q
    for day in range(30):
        b, s, sd, f = (r[k].get(day, 0) for k in ("bought", "sold", "seeds", "feeds"))
        if not (b or s or sd or f):
            continue
        print(f"  {day:>4} {b:>7} {s:>6} {sd:>6} {f:>6} {shed_by_day.get(day, 0):>6}")

    print()
    print("=" * 96)
    print("VERDICT")
    print("=" * 96)
    if tf and tb:
        print(f"  FEED needs ~{tf} wheat; he bought {tb}. "
              f"{'feed alone explains the buying' if tb <= tf * 1.3 else 'buying EXCEEDS feed need by ' + str(tb - tf) + ' units'}")
    if ts > tf:
        print(f"  he SELLS {ts} wheat, more than the {tf} he feeds -- so wheat leaves the farm as a")
        print(f"  product, not only as feed")
    # **The spread is what separates arbitrage from sourcing, not the volume.** A large round-trip at a
    # thin spread is not a trade; it is a supply chain that happens to resell its surplus.
    buy_px = r["buy_cost"] / max(tb, 1)
    sell_px = r["sell_take"] / max(ts, 1)
    resale = max(0, tb - tf)
    print()
    print(f"  mean BUY price  ${buy_px:>6.2f}")
    print(f"  mean SELL price ${sell_px:>6.2f}   spread {(sell_px / max(buy_px, 1e-9) - 1) * 100:+.1f}%")
    print(f"  wheat bought beyond the {tf} FEED needs : {resale} units")
    print()
    if sell_px > buy_px * 1.5:
        print("  => COMMODITY ARBITRAGE: buy cheap early, sell dear late. No tiles, no units, no land,")
        print("     only capital -- and our chain library cannot express it at all.")
    else:
        print("  => NOT arbitrage. The realised spread is thin, so he is not buying low and selling")
        print("     high; he buys and sells at much the same price nearly every day. The buying is")
        print("     dominated by FEED sourcing -- he *buys* his feed instead of growing it, which our")
        print("     library does express (`ranch(buy_feed=True)`, the default) -- and the surplus is")
        print("     flipped at a small margin.")
        print(f"     Whole operation nets ${r['sell_take'] - r['buy_cost']:+,.0f}, "
              f"which is real but not where the game is won.")