"""One day, printed in full: what we sold, at what price, and what was destroyed at dawn.

Every number today has been an average over seasons, and averages cannot show whether the trade
Alex describes -- dump a wheat, save a wool -- was actually available on a given day. This prints a
single day the way you would look at it if you were playing it:

    the shops that exist and what they drain, per product
    the price of every product at dawn, at dusk, and what it did in between
    every fill we made that day, hour by hour, at the price that unit actually fetched
    what we were holding at dusk, and exactly what the dawn drop destroyed

Fills come from `record_fills`, which wraps `_commit_unit` -- offers are not fills, and shed deltas
are not fills either (`kagg/analysis/fills.py` lists three ways that has gone wrong here).

The destroyed column is `(shed + carried at dusk) - (shed at dawn)`, which is what
`_drop_inventories_to_shed` actually did (`reference:843`).

    python -u scripts/one_day_of_selling.py --seed 700 --day 20
    python -u scripts/one_day_of_selling.py --seed 700 --worst     # the day that lost the most
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=700)
    ap.add_argument("--day", type=int, default=20)
    ap.add_argument("--worst", action="store_true", help="print the day with the costliest rot")
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    a = ap.parse_args()

    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{a.module}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    books = {}           # (day, hour) -> {product: book}
    held_dusk = {}       # day -> Counter of shed+carried at h23
    shed_dawn = {}       # day -> Counter of shed at h0
    shops_by_day = {}

    with record_fills() as fills:
        env = make("kaggriculture", configuration={"seed": a.seed}, debug=False)
        env.reset(2)
        me = SA.make_agent(sched, 0, router=True)
        them = _build(OPPONENTS[a.opponent], None)
        for t in range(30 * TPD):
            o0 = env.state[0].observation
            day, hour = t // TPD, t % TPD
            priv = o0.get("private") or {}
            shed = collections.Counter({k: int(v or 0)
                                        for k, v in (priv.get("shed") or {}).items()})
            books[(day, hour)] = {k: int(v or 0) for k, v in
                                  (((o0.get("market") or {}).get("inventory")) or {}).items()}
            if hour == 0:
                shed_dawn[day] = shed
                shops_by_day[day] = list((o0.get("town") or {}).get("unlocked_shops") or [])
            if hour == TPD - 1:
                carried = collections.Counter()
                for inv in (priv.get("inventories") or []):
                    for k, v in (inv or {}).items():
                        carried[k] += int(v or 0)
                held_dusk[day] = shed + carried

            a0 = me(o0, env.configuration)
            n0 = len(o0["farms"][0].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                       "market": a0["market"]},
                      them(env.state[1].observation, env.configuration)])
            if env.done:
                break

    # ---- destroyed per day, to pick the worst if asked ------------------------------------
    destroyed = collections.defaultdict(collections.Counter)
    cost = collections.Counter()
    for d in sorted(held_dusk):
        nxt = shed_dawn.get(d + 1)
        if nxt is None:
            continue
        for p in set(held_dusk[d]) | set(nxt):
            gone = held_dusk[d][p] - nxt[p]
            if gone > 0 and p in KG.PRODUCTS:
                destroyed[d][p] += gone
                cost[d] += gone * KG.market_price(p, books[(d, TPD - 1)].get(p, KG.MARKET_I0))

    day = max(cost, key=lambda k: cost[k]) if (a.worst and cost) else a.day
    dusk = books.get((day, TPD - 1), {})
    dawn = books.get((day, 0), {})

    print(f"seed {a.seed}   vs {a.opponent}   DAY {day}"
          + ("   (worst rot day of the season)" if a.worst else ""))

    shops = shops_by_day.get(day, [])
    print(f"\nshops open: {', '.join(shops) if shops else '(none)'}")
    drain = collections.Counter()
    for name in shops:
        prods = KG.SHOPS.get(name, ())
        for p in prods:
            drain[p] += 2 if len(prods) == 1 else 1

    print(f"\n{'product':<13}{'drain/tick':>11}{'price dawn':>12}{'price dusk':>12}"
          f"{'shed dawn':>11}{'held dusk':>11}{'DESTROYED':>11}{'lost $':>10}")
    rows = sorted(set(list(dusk)) & set(KG.PRODUCTS),
                  key=lambda p: -destroyed[day].get(p, 0))
    tot_lost = 0.0
    for p in rows:
        d_units = destroyed[day].get(p, 0)
        pr_dusk = KG.market_price(p, dusk.get(p, KG.MARKET_I0))
        lost = d_units * pr_dusk
        tot_lost += lost
        if (shed_dawn.get(day, {}).get(p, 0) or held_dusk.get(day, {}).get(p, 0) or d_units):
            print(f"{p:<13}{drain.get(p, 0):>11}"
                  f"{KG.market_price(p, dawn.get(p, KG.MARKET_I0)):>12}"
                  f"{pr_dusk:>12}"
                  f"{shed_dawn.get(day, {}).get(p, 0):>11}"
                  f"{held_dusk.get(day, {}).get(p, 0):>11}"
                  f"{d_units:>11}{lost:>10,.0f}")
    print(f"{'':<13}{'':>11}{'':>12}{'':>12}"
          f"{sum(shed_dawn.get(day, {}).values()):>11}"
          f"{sum(held_dusk.get(day, {}).values()):>11}"
          f"{sum(destroyed[day].values()):>11}{tot_lost:>10,.0f}")

    print(f"\nevery fill we made on day {day}:")
    day_fills = [(h, item, price) for (d, h, op, item, price) in fills.at_turn(0, op="SELL")
                 if d == day]
    if not day_fills:
        print("  none")
    else:
        by_hour = collections.defaultdict(collections.Counter)
        rev = collections.defaultdict(float)
        for h, item, price in day_fills:
            by_hour[h][item] += 1
            rev[(h, item)] += price
        print(f"  {'hour':<6}{'product':<13}{'units':>7}{'revenue $':>12}{'$/unit':>9}")
        for h in sorted(by_hour):
            for item, n in by_hour[h].items():
                r = rev[(h, item)]
                print(f"  {h:<6}{item:<13}{n:>7}{r:>12,.0f}{r / n:>9.0f}")
        print(f"  {'TOTAL':<19}{len(day_fills):>7}"
              f"{sum(rev.values()):>12,.0f}")

    print(f"\nthe trade, stated for this day: we destroyed "
          f"{sum(destroyed[day].values())} units worth ${tot_lost:,.0f}. "
          f"Selling one more unit of the cheapest thing we held")
    cheapest = min(((KG.market_price(p, dusk.get(p, KG.MARKET_I0)), p)
                    for p in rows if held_dusk.get(day, {}).get(p, 0) > 0), default=(0, "-"))
    dearest = max(((KG.market_price(p, dusk.get(p, KG.MARKET_I0)), p)
                   for p in rows if destroyed[day].get(p, 0) > 0), default=(0, "-"))
    print(f"({cheapest[1]} at ${cheapest[0]}) would have saved one unit of the dearest thing "
          f"destroyed ({dearest[1]} at ${dearest[0]}).")
    print(f"Net on that single swap: ${dearest[0] - 0:,.0f} rescued for ${cheapest[0]:,.0f} "
          f"of stock given up.")

    print(f"\nseason rot by day, worst first: "
          + ", ".join(f"d{d}:${cost[d]:,.0f}" for d in sorted(cost, key=lambda k: -cost[k])[:8]))


if __name__ == "__main__":
    main()
