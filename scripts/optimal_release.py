"""How much revenue is left on the table by WHEN we sell, holding production fixed.

The season splits into two decisions that are not equally hard:

  * **allocation** -- how many tiles of each crop, how many of each animal. Decided by d10, largely
    irreversible, and coupled to turns and land.
  * **release** -- which day each produced unit is sold on. Decided daily, fully reversible, and
    coupled to nothing except the market curve and the shed.

This prices the second one exactly, because it can be priced exactly. Production is taken as
measured -- what actually reached our shed, day by day, in a real game -- so the answer is "given
what we grew, what was the best we could have done", never a claim about what we should have grown.

**The model is the environment's own arithmetic, not an approximation.**

  * `market_price` is a pure function of inventory (`kaggriculture.py`), so a sale of n units is
    walked one unit at a time and each unit re-quotes. A unit clearing at `PRICE_FLOOR` pays out but
    does NOT raise inventory, exactly as `_commit_unit` has it.
  * The town removes stock every `townShopSellInterval = 4` steps -- six times a day -- one unit per
    unlocked shop instance per product it stocks, doubled for single-product shops, plus one unit
    per `TOWN_CENTER_PRODUCTS` entry every `townCenterSellInterval`. That is `_town_consume`,
    restated here as a per-day rate.
  * Both seats settle into ONE book. The opponent's flow is read from a recorded tape rather than
    assumed, which is fair in this competition specifically: the top agents submit fixed 720-turn
    scripts, so a recorded action stream IS what they do.

**Why a greedy release is near-optimal here, and where it is not.** Revenue is concave in units sold
on a day (each unit clears lower than the last) and the drain is linear, so the unconstrained
optimum equalises marginal revenue across days -- a water-filling solution. The binding constraints
are all one-sided: a unit cannot be sold before it is produced, the shed holds 100 items total
across nine products, and there is no day 30. So the policy below -- sell down to the drain rate,
carry the rest, never exceed what the shed can hold overnight -- is the water-filling solution
subject to availability, and the only place it can be beaten is the melon race, where the drain is
1/day and waiting is never right.

    PYTHONPATH=. python -u scripts/optimal_release.py
    PYTHONPATH=. python -u scripts/optimal_release.py --seed 11 --tape kawashigi
"""
import argparse
import collections
import importlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import kagg.plan as _PLAN                                                    # noqa: E402
from kagg.analysis.fills import record_fills                                 # noqa: E402
from reference import kaggriculture as kg                                    # noqa: E402

I0 = kg.MARKET_I0
#: Products whose release we optimise. FERTILIZER is excluded: nothing drains it and it is bought
#: back by the other seat, so its book is not a scheduling problem in the same sense.
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL")


def drain_per_day(unlocked_shops):
    """`_town_consume` as a per-day rate, from the shop draw the game actually made."""
    per = collections.Counter()
    for name in unlocked_shops:
        prods = kg.SHOPS.get(name) or ()
        mult = 2 if len(prods) == 1 else 1
        for item in prods:
            per[item] += 6 * mult                       # six shop ticks a day
    for item in kg.TOWN_CENTER_PRODUCTS:
        per[item] += 1                                  # one town-centre tick a day
    return per


def walk(product, above, n):
    """Sell n units from inventory I0+above. Returns (revenue, new_above). The env's own loop."""
    inv, rev = I0 + above, 0
    for _ in range(n):
        q = kg.market_price(product, inv)
        rev += q
        if q > kg.PRICE_FLOOR:
            inv += 1
    return rev, inv - I0


def season(product, ours, theirs, drain):
    """Both seats into one book, day by day. Returns OUR revenue and the units we actually moved."""
    above, rev, sold = 0, 0, 0
    for d in range(30):
        r, above = walk(product, above, ours[d])
        rev += r
        sold += ours[d]
        _r, above = walk(product, above, theirs[d])      # their flow lifts the same book
        above = max(0, above - drain)
    return rev, sold


def measured(seed, tape):
    """Play the shipped agent and record, per day: units that REACHED us, and units we sold."""
    import scripts.breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    replay, schedule, team = B.TAPES[tape]
    sched = _PLAN.load(schedule)

    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, me=0)
    opp = B.tape_policy(replay, team, 1)

    sold = {p: [0] * 30 for p in PRODUCTS}
    theirs = {p: [0] * 30 for p in PRODUCTS}
    arrived = {p: [0] * 30 for p in PRODUCTS}            # units that became sellable that day
    prev = {p: 0 for p in PRODUCTS}
    prev_t = {p: 0 for p in PRODUCTS}
    held = {p: 0 for p in PRODUCTS}
    shops = []
    with record_fills() as fills:
        for t in range(719):
            o0, o1 = env.state[0].observation, env.state[1].observation
            env.step([me(o0, t), opp(o1, t)])
            if t % 24 == 23:
                d = t // 24
                obs = env.state[0].observation
                shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
                shed = (obs.get("private") or {}).get("shed") or {}
                for p in PRODUCTS:
                    u, _ = fills.sold(player=0, product=p)
                    sold[p][d] = u - prev[p]; prev[p] = u
                    v, _ = fills.sold(player=1, product=p)
                    theirs[p][d] = v - prev_t[p]; prev_t[p] = v
                    now = int(shed.get(p, 0) or 0)
                    # what became available today = what we sold today + the change in stock
                    arrived[p][d] = max(0, sold[p][d] + now - held[p])
                    held[p] = now
            if env.done:
                break
    return sold, theirs, arrived, shops


def water_fill(arrived, drain, cap=None):
    """Sell down to the drain rate, carry the rest. The water-filling policy under availability."""
    plan, stock = [0] * 30, 0
    for d in range(30):
        stock += arrived[d]
        take = min(stock, drain) if d < 29 else stock       # no day 30: liquidate
        plan[d] = take
        stock -= take
    return plan


#: A product whose daily drain is at or below this is a RACE, not a spread. Not because the book
#: cannot recover at all -- it recovers at the drain rate, so against an opponent selling NO
#: melon a spread is harmless -- but because the recorded opponents sell 114-120 melons into a
#: 1/day drain, and against that flow whoever sells first gets the fresh book while anything
#: held meets the floor on d29. MELON is the only member: no shop stocks it, the town centre
#: takes 1/day.
NO_DRAIN_THRESHOLD = 1


def front_load(arrived):
    """Sell every unit the day it reaches the shed. Optimal when the book cannot recover."""
    return list(arrived)


def release(product, arrived, drain):
    """The release policy for one product: front-load a race, water-fill a drained book."""
    if drain <= NO_DRAIN_THRESHOLD:
        return front_load(arrived)
    return water_fill(arrived, drain)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--tape", default=_PLAN.SHIPPED_PLAN.parent.name)
    args = ap.parse_args()

    print(f"measuring the shipped agent, seed {args.seed}, tape {args.tape} ...", flush=True)
    sold, theirs, arrived, shops = measured(args.seed, args.tape)
    drain = drain_per_day(shops)
    print(f"shop draw at the end: {sorted(collections.Counter(shops).items())}")
    print(f"drain per day: {dict(sorted(((p, drain[p]) for p in PRODUCTS), key=lambda kv: -kv[1]))}")
    print()

    print(f"{'product':<12}{'produced':>9}{'we sold':>9}{'drain':>7}"
          f"{'ACTUAL $':>11}{'OPTIMAL $':>11}{'left on table':>15}")
    tot_a = tot_o = 0
    rows = []
    for p in PRODUCTS:
        if not sum(arrived[p]) and not sum(sold[p]):
            continue
        d = drain[p]
        act_rev, act_units = season(p, sold[p], theirs[p], d)
        best = release(p, arrived[p], max(1, d))
        opt_rev, opt_units = season(p, best, theirs[p], d)
        tot_a += act_rev; tot_o += opt_rev
        rows.append((opt_rev - act_rev, p))
        print(f"{p:<12}{sum(arrived[p]):>9}{act_units:>9}{d:>7}"
              f"{act_rev:>11,}{opt_rev:>11,}{opt_rev - act_rev:>+15,}")
    print(f"{'TOTAL':<12}{'':>9}{'':>9}{'':>7}{tot_a:>11,}{tot_o:>11,}{tot_o - tot_a:>+15,}")
    print()
    print("biggest prizes:", ", ".join(f"{p} {v:+,}" for v, p in sorted(rows, reverse=True)[:4]))
    json.dump({"actual": tot_a, "optimal": tot_o,
               "per_product": {p: {"arrived": arrived[p], "sold": sold[p], "theirs": theirs[p]}
                               for p in PRODUCTS}},
              open("data/logs/optimal_release.json", "w"), indent=1)
    print("detail -> data/logs/optimal_release.json")


if __name__ == "__main__":
    main()
