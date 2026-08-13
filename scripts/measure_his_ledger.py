"""Where his $141,256 actually comes from -- revenue and cost, priced off the tape.

The census says he HARVESTs 338 times and we HARVEST 607, yet he banks six times what we do. So the
money is not coming out of the ground at a rate we are failing to match. He also BUYs 967 WHEAT and
SELLs 1,131 units with only 319 going to FEED, which is the shape of a trader, not a grower. This
prices every order on his tape against that day's market so the question "is he farming or trading?"
is answered in dollars.
"""
import argparse, collections, json, sys
sys.path.insert(0, ".")

ap = argparse.ArgumentParser()
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--team", default="somewhere after")
a = ap.parse_args()

TD = 24
d = json.load(open(a.replay))
seat = d["info"]["TeamNames"].index(a.team)

# Prices live in the observation. Find where.
step0 = d["steps"][0][seat] or {}
obs0 = step0.get("observation") or {}
print("observation keys:", sorted(obs0.keys()))
mkt = obs0.get("market") or obs0.get("prices") or {}
print("market sample:", json.dumps(mkt)[:600])

sell_rev = collections.Counter()
sell_qty = collections.Counter()
buy_cost = collections.Counter()
buy_qty = collections.Counter()
by_day = collections.defaultdict(lambda: dict(rev=0.0, cost=0.0))
land_cost = hire_cost = 0.0

def price_of(obs, product):
    """The town's posted price for `product` this turn -- `market.prices`, which moves with
    `market.inventory`: every unit sold adds to the town's stock and walks the price down. That drain
    is why a 4,427-unit season spread over nine products banks more than the same volume in two."""
    pr = ((obs.get("market") or {}).get("prices") or {})
    v = pr.get(product)
    return float(v) if v is not None else None

for t, step in enumerate(d["steps"]):
    day = t // TD
    s = step[seat] or {}
    obs = s.get("observation") or {}
    act = s.get("action") or {}
    for o in (act.get("market") or []):
        if not o:
            continue
        kind = o[0]
        item = o[1] if len(o) > 1 else None
        n = int(o[2]) if len(o) > 2 else 1
        p = price_of(obs, item) if item else None
        if kind == "SELL":
            sell_qty[item] += n
            if p is not None:
                sell_rev[item] += p * n
                by_day[day]["rev"] += p * n
        elif kind in ("BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL"):
            buy_qty[(kind, item)] += n
            if p is not None:
                buy_cost[(kind, item)] += p * n
                by_day[day]["cost"] += p * n

print()
print("=" * 100)
print("SOLD")
print("=" * 100)
for k, v in sell_qty.most_common():
    print(f"  {k:>14} {v:>6} units   revenue ${sell_rev[k]:>12,.0f}   "
          f"avg ${sell_rev[k]/max(v,1):>7.2f}")
print(f"  {'TOTAL':>14} {sum(sell_qty.values()):>6} units   revenue ${sum(sell_rev.values()):>12,.0f}")
print()
print("=" * 100)
print("BOUGHT")
print("=" * 100)
for k, v in buy_qty.most_common():
    print(f"  {str(k):>34} {v:>6}   cost ${buy_cost[k]:>12,.0f}")
print(f"  {'TOTAL':>34} {sum(buy_qty.values()):>6}   cost ${sum(buy_cost.values()):>12,.0f}")

print()
print("=" * 100)
print("PRICE EROSION -- what the town pays as his volume lands")
print("=" * 100)
first = (d["steps"][0][seat] or {}).get("observation") or {}
last = (d["steps"][-1][seat] or {}).get("observation") or {}
print(f"{'product':>14} {'day 0':>8} {'day 29':>8} {'sold':>7} {'revenue':>13} {'avg $':>8}")
for k, v in sell_qty.most_common():
    p0, p1 = price_of(first, k), price_of(last, k)
    print(f"{k:>14} {(p0 or 0):>8.0f} {(p1 or 0):>8.0f} {v:>7} "
          f"${sell_rev[k]:>12,.0f} ${sell_rev[k]/max(v,1):>7.2f}")

gross = sum(sell_rev.values())
spend = sum(buy_cost.values())
print()
print(f"  gross revenue  ${gross:>12,.0f}")
print(f"  purchases      ${spend:>12,.0f}")
print(f"  gross - buys   ${gross - spend:>12,.0f}   (crew, land and pens make up the rest of the gap")
print(f"  final bank     ${141_256:>12,}    to his $141,256)")

print()
print("=" * 100)
print("HIS SELL CADENCE -- units sold per day, by product")
print("=" * 100)
per_day = collections.defaultdict(collections.Counter)
for t, step in enumerate(d["steps"]):
    s_ = step[seat] or {}
    for o in ((s_.get("action") or {}).get("market") or []):
        if o and o[0] == "SELL":
            per_day[t // TD][o[1]] += int(o[2]) if len(o) > 2 else 1   # offered
prods = [k for k, _ in sell_qty.most_common()]
print("  SELL units OFFERED per day -- an order re-posted until it fills is counted once "
      "per turn it stood.")
print(f"{'day':>4} " + " ".join(f"{p[:5]:>6}" for p in prods) + f" {'total':>7}")
for day in sorted(per_day):
    r = per_day[day]
    print(f"{day:>4} " + " ".join(f"{r.get(p,0):>6}" for p in prods) + f" {sum(r.values()):>7}")
