"""How long goods sit before they are sold. The measure that separates a timing rule from none.

If a product's units leave the shed the moment they arrive, there is no timing rule to find: the
sale is a consequence of production, and the market layer is just "clear what came in". If they sit
for many turns, something is choosing when -- and that something is worth copying.

Per product per seat, this tracks the shed level and matches arrivals to departures FIFO, reporting
the median turns a unit waited. Shed levels come straight from each turn's observation, so no
inference about offers is involved.

    python -u scripts/time_in_shed.py 107642213 107041112 107399673 107646523 107674019
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    waits = collections.defaultdict(lambda: collections.defaultdict(list))
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        for seat, team in enumerate(teams):
            levels = collections.defaultdict(list)
            for step in rep["steps"]:
                shed = (((step[seat] if seat < len(step) else None) or {})
                        .get("observation") or {}).get("private", {}).get("shed") or {}
                for p in PRODUCTS:
                    levels[p].append(int(shed.get(p, 0) or 0))
            for p in PRODUCTS:
                q, series = collections.deque(), levels[p]
                for t in range(1, len(series)):
                    d = series[t] - series[t - 1]
                    if d > 0:
                        q.extend([t] * d)               # arrivals, stamped
                    elif d < 0:
                        for _ in range(-d):             # departures, FIFO
                            if q:
                                waits[team][p].append(t - q.popleft())
    print(f"{'team':20}{'all':>7}   median turns a unit waits, per product")
    prods = [p for p in PRODUCTS]
    print(f"{'':20}{'':7}   " + "".join(f"{p[:5]:>7}" for p in prods))
    for team in sorted(waits, key=lambda t: -sum(len(v) for v in waits[t].values())):
        allw = [x for v in waits[team].values() for x in v]
        row = f"{team[:20]:20}{statistics.median(allw) if allw else 0:>7.0f}   "
        for p in prods:
            v = waits[team][p]
            row += f"{statistics.median(v):>7.0f}" if v else f"{'-':>7}"
        print(row)


if __name__ == "__main__":
    main()
