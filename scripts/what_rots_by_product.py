"""What actually gets destroyed at dawn, PER PRODUCT, and what was it worth at that moment?

Alex, 2026-08-25: *"i still can not believe if wool is 240 in the shop and wheat is 40 that selling
the excess wheat and then not rotting the wool is not beneficial."*

That is only true if WOOL is in the pile that rots. Every rot arm so far has been measured in total
units, which cannot answer it -- 200 wheat and 5 wool destroy the same "205 units" and are worth
$8,000 and $1,200 of very different money.

**How the destruction actually happens.** `_drop_inventories_to_shed` (`reference:843`, called from
`_end_of_day` at `:878`) walks each farmer's inventory, moves what fits into the shed, and does
`del inv[item]` on the rest -- unconditionally, whether or not it fitted. So the loss is:

    (shed at dusk + everything the hands are carrying at dusk) - (shed at dawn)

per product. Measured at the day boundary, not inferred from a money delta -- `fills.py` records
three separate ways that inference has been wrong here.

It is valued at `market_price(product, book)` at that moment, which is the price the unit would
have fetched had it been sold instead of dropped. That is an upper bound: selling it would have
pushed the book up and the next unit down.

    python -u scripts/what_rots_by_product.py --range 700 6 --opponent contrarian
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
from concurrent.futures import ProcessPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def _play(job):
    seed, opponent, module_name = job
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    fills_cm = record_fills()
    fills = fills_cm.__enter__()
    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    them = _build(OPPONENTS[opponent], None)

    lost_units = collections.Counter()
    lost_value = collections.Counter()
    held_dusk = None
    price_dusk = {}

    for t in range(30 * TPD):
        o0 = env.state[0].observation
        priv = o0.get("private") or {}
        shed = collections.Counter({k: int(v or 0) for k, v in (priv.get("shed") or {}).items()})
        book = {k: int(v or 0)
                for k, v in (((o0.get("market") or {}).get("inventory")) or {}).items()}

        # **Subtract the hour-23 fills.** A SELL on the last turn of the day settles in the SAME
        # `env.step` as `_drop_inventories_to_shed`, so stock that was SOLD reads as stock that was
        # destroyed. `fills.py` records this as mistake (2) and says it overstated a previous
        # measurement 15x. Day 10 of seed 700 is the proof: 8 MELON "destroyed" at $1,824 are the
        # same 8 MELON sold at h23 for $1,796.
        if t % TPD == 0 and held_dusk is not None:
            # Dawn: whatever we held last night and no longer have was destroyed by the drop.
            sold_h23 = collections.Counter()
            for d, h, op, item, price in fills.at_turn(0, op="SELL"):
                if d == (t // TPD) - 1 and h == TPD - 1:
                    sold_h23[item] += 1
            for p in set(held_dusk) | set(shed):
                gone = held_dusk[p] - shed[p] - sold_h23[p]
                if gone > 0 and p in KG.PRODUCTS:
                    lost_units[p] += gone
                    lost_value[p] += gone * KG.market_price(p, price_dusk.get(p, KG.MARKET_I0))

        if t % TPD == TPD - 1:
            # Dusk: shed plus every unit still in a hand's inventory.
            carried = collections.Counter()
            for inv in (priv.get("inventories") or []):
                for k, v in (inv or {}).items():
                    carried[k] += int(v or 0)
            held_dusk = shed + carried
            price_dusk = dict(book)

        a0 = me(o0, env.configuration)
        n0 = len(o0["farms"][0].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                   "market": a0["market"]},
                  them(env.state[1].observation, env.configuration)])
        if env.done:
            break

    final = float(env.state[0].observation["farms"][0]["money"])
    fills_cm.__exit__(None, None, None)
    return dict(lost_units), dict(lost_value), final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--range", nargs=2, type=int, default=[700, 6], metavar=("FIRST", "COUNT"))
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()

    seeds = ([int(x) for x in a.seeds.split(",")] if a.seeds
             else list(range(a.range[0], a.range[0] + a.range[1])))
    jobs = [(s, a.opponent, a.module) for s in seeds]
    print(f"{len(jobs)} seasons vs {a.opponent}, seeds {seeds}\n", flush=True)

    units = collections.Counter()
    value = collections.Counter()
    banks = []
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for (seed, _o, _m), (u, v, final) in zip(jobs, pool.map(_play, jobs)):
            units.update(u)
            value.update(v)
            banks.append(final)
            tot = sum(u.values())
            print(f"  seed {seed:<6} destroyed {tot:>5} units worth "
                  f"{sum(v.values()):>10,.0f}   bank {final:>10,.0f}", flush=True)

    n = max(1, len(seeds))
    print(f"\ndestroyed at dawn, per season (mean of {n} seeds)\n")
    print(f"{'product':<14}{'units':>9}{'value $':>13}{'$/unit':>10}")
    for p, u in sorted(value.items(), key=lambda kv: -kv[1]):
        uu = units[p]
        print(f"{p:<14}{uu / n:>9.1f}{value[p] / n:>13,.0f}{(value[p] / uu if uu else 0):>10.0f}")
    print(f"{'TOTAL':<14}{sum(units.values()) / n:>9.1f}{sum(value.values()) / n:>13,.0f}")
    print(f"\nmean bank {sum(banks) / n:,.0f}   destroyed as a share of it: "
          f"{100.0 * (sum(value.values()) / n) / max(1.0, sum(banks) / n):.2f}%")
    print("\nValue is `market_price(p, book)` at that dusk -- an UPPER bound, since selling those")
    print("units would have walked the book down as they went.")


if __name__ == "__main__":
    main()
