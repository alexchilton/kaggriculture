"""Read the plan-level build order off real leaderboard seats, instead of searching for it.

Alex's direction, and it is the right one: we hold 168 episode JSONs including seats that banked
$106k-$145k against our $23.8k. The expensive parts of a plan search -- *when* to buy each land
parcel, *how many* animals and of which kind, *how much* crew, *when* to sell -- are all recorded.
Searching for them from a crop-only seed is paying compute to rediscover what is already on disk.

This extracts, per seat, only the **plan-level** decisions -- the genome, not the action tape:

- the day each `BUY_LAND` fired, and how many parcels were bought at all
- the animal portfolio: which animals, bought on which day
- `HIRE` orders per day, i.e. crew size, which the dawn reset makes a daily decision
- `BUY_PRODUCT` wheat, the feed supply that the wheat-into-animal-product conversion runs on
- `SELL` volume per product per day, to see the real cadence against our naive sell-everything-daily
- the op census that tells us whether a seat ran animals at all (FEED / CARE / COLLECT_FERTILIZER)

It doubles as the coverage test for the routine library: any pattern here that
`kagg/search/routines.py` cannot express at *any* parameters is a measured gap, not an opinion.

    PYTHONPATH=. python3 -u scripts/mine_build_orders.py --top 12 2>&1 | tee data/logs/mine_build_orders.log
"""

import argparse
import collections
import glob
import json
import pathlib

TURNS_PER_DAY = 24
ANIMALS = ("GOOSE", "COW", "SHEEP")
UNIT_OPS = ("FEED", "CARE", "COLLECT_FERTILIZER", "HARVEST", "PLANT", "WATER",
            "BUILD_PASTURE", "BUILD_COOP", "PLACE", "PICKUP", "DROP", "FERTILIZE", "DIG", "PASS")


def seats(path):
    """Yield `(seat, final_money, per-seat plan facts)` for one episode file."""
    with open(path) as fh:
        ep = json.load(fh)
    rewards = ep.get("rewards") or []
    steps = ep.get("steps") or []
    for seat in range(len(rewards)):
        money = rewards[seat]
        if money is None:
            continue
        land, animals, hires, wheat = [], [], collections.Counter(), collections.Counter()
        sells = collections.defaultdict(collections.Counter)
        ops = collections.Counter()
        for t, step in enumerate(steps):
            if seat >= len(step):
                continue
            action = step[seat].get("action")
            if not isinstance(action, dict):
                continue
            day = t // TURNS_PER_DAY
            for order in action.get("market") or []:
                if not order:
                    continue
                op = order[0]
                if op in ("BUY_LAND", "BUID_LAND"):
                    land.append(day)
                elif op == "HIRE":
                    hires[day] += 1
                elif op == "BUY_ANIMAL" and len(order) >= 2:
                    animals.append((day, order[1]))
                elif op == "BUY_PRODUCT" and len(order) >= 3 and order[1] == "WHEAT":
                    wheat[day] += int(order[2])
                elif op == "SELL" and len(order) >= 3:
                    sells[order[1]][day] += int(order[2])
            units = [action.get("farmer")] + list(action.get("hands") or [])
            for u in units:
                if u:
                    ops[u[0]] += 1
        yield seat, money, {
            "land_days": land, "animals": animals, "hires": hires,
            "wheat": wheat, "sells": sells, "ops": ops,
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--glob", default="data/*.json")
    a = ap.parse_args()

    rows = []
    for path in sorted(glob.glob(a.glob)):
        try:
            for seat, money, facts in seats(path):
                rows.append((money, pathlib.Path(path).stem, seat, facts))
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
    rows.sort(key=lambda r: -r[0])
    print(f"{len(rows)} seats across {len(set(r[1] for r in rows))} episodes\n")

    print("=" * 108)
    print(f"{'money':>9} {'episode':>10} {'st':>2} | {'land days':>14} {'animals':>26} "
          f"{'hire/day':>9} {'wheat':>7} {'FEED':>6}")
    print("=" * 108)
    for money, ep, seat, f in rows[:a.top]:
        ld = ",".join(str(d) for d in sorted(set(f["land_days"]))) or "-"
        an = collections.Counter(name for _d, name in f["animals"])
        an_s = " ".join(f"{n}x{name[:2]}@d{min(d for d, m in f['animals'] if m == name)}"
                        for name, n in an.items()) or "-"
        hires = sum(f["hires"].values())
        print(f"{money:>9,.0f} {ep:>10} {seat:>2} | {ld:>14} {an_s:>26} "
              f"{hires/30:>9.1f} {sum(f['wheat'].values()):>7} {f['ops']['FEED']:>6}")

    # ---- aggregate: what do the winners do that we do not ----------------
    top = rows[:a.top]
    bot = rows[-a.top:]
    print("\n" + "=" * 108)
    print(f"{'':22} {'TOP ' + str(a.top):>14} {'BOTTOM ' + str(a.top):>14}")
    print("=" * 108)

    def agg(group, fn):
        return sum(fn(f) for _m, _e, _s, f in group) / max(len(group), 1)

    metrics = [
        ("final money", lambda f: 0),          # filled below from the money column
        ("land parcels bought", lambda f: len(set(f["land_days"]))),
        ("first land purchase day", lambda f: min(set(f["land_days"])) if f["land_days"] else 30),
        ("animals bought", lambda f: len(f["animals"])),
        ("hires per day", lambda f: sum(f["hires"].values()) / 30),
        ("wheat bought", lambda f: sum(f["wheat"].values())),
        ("FEED ops", lambda f: f["ops"]["FEED"]),
        ("CARE ops", lambda f: f["ops"]["CARE"]),
        ("COLLECT_FERTILIZER ops", lambda f: f["ops"]["COLLECT_FERTILIZER"]),
        ("FERTILIZE ops", lambda f: f["ops"]["FERTILIZE"]),
        ("PLANT ops", lambda f: f["ops"]["PLANT"]),
        ("HARVEST ops", lambda f: f["ops"]["HARVEST"]),
        ("PASS ops", lambda f: f["ops"]["PASS"]),
    ]
    print(f"{'final money':22} {sum(m for m,_,_,_ in top)/len(top):>14,.0f} "
          f"{sum(m for m,_,_,_ in bot)/len(bot):>14,.0f}")
    for name, fn in metrics[1:]:
        print(f"{name:22} {agg(top, fn):>14.1f} {agg(bot, fn):>14.1f}")

    # ---- sell cadence: is it daily, or concentrated late? ----------------
    print("\n" + "=" * 108)
    print("SELL volume by day-decile, top seats (does the town's day-10 / day-20 demand step show?)")
    print("=" * 108)
    for money, ep, seat, f in top[:6]:
        by_day = collections.Counter()
        for _product, days in f["sells"].items():
            for d, n in days.items():
                by_day[d] += n
        total = sum(by_day.values()) or 1
        thirds = [sum(n for d, n in by_day.items() if lo <= d < hi) / total
                  for lo, hi in ((0, 10), (10, 20), (20, 30))]
        bar = "  ".join(f"d{lo}-{hi}: {p:5.1%}" for (lo, hi), p in
                        zip(((0, 10), (10, 20), (20, 30)), thirds))
        print(f"{money:>9,.0f} {ep:>10} {seat:>2} | total {total:>5} units | {bar}")


if __name__ == "__main__":
    raise SystemExit(main())
