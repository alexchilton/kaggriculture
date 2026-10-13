"""When does he sell? Price at the moment of each SELL, against the price available all season.

Two of his seasons can have a byte-identical 719-turn farm and identical season sell TOTALS to the
unit, and still differ on 8-94 turns -- so the quantities are planned and only the hour is chosen.
This measures what the hour is chosen on: the live quote.

For every SELL, the product's price on that turn is scored as a percentile of that product's price
over the whole season, and over the +-12 turn window around it. 50 means he sold at a typical
price; 90 means he waited for a good one.

    python -u scripts/sell_timing.py 107041112 107064978
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    for d in DIRS:
        p = ROOT / d / f"{ep}.json"
        if p.exists():
            return p
    return None


def pct(value, pool):
    pool = [x for x in pool if x is not None]
    if not pool:
        return None
    return 100.0 * sum(1 for x in pool if x < value) / len(pool)


def main():
    for ep in sys.argv[1:]:
        p = find(int(ep))
        if p is None:
            print(f"{ep}: no replay held")
            continue
        rep = json.loads(p.read_text())
        teams = (rep.get("info") or {}).get("TeamNames") or []
        steps = rep.get("steps") or []
        for seat, team in enumerate(teams):
            prices = collections.defaultdict(list)      # product -> price per turn
            sells = []                                  # (turn, product, units)
            for t, step in enumerate(steps):
                obs = ((step[seat] if seat < len(step) else None) or {}).get("observation") or {}
                pr = (obs.get("market") or {}).get("prices") or {}
                for k, v in pr.items():
                    while len(prices[k]) < t:
                        prices[k].append(None)
                    prices[k].append(v)
                act = ((step[seat] if seat < len(step) else None) or {}).get("action") or {}
                for o in act.get("market") or []:
                    if o and o[0] == "SELL":
                        sells.append((t, o[1], int(o[2])))
            if not sells:
                continue
            print(f"\n=== {ep} seat {seat} {team}: {len(sells)} SELL orders ===")
            print(f"{'product':12}{'n':>5}{'season pct':>12}{'local pct':>11}{'mean price':>12}"
                  f"{'season mean':>12}")
            for prod in sorted({s[1] for s in sells}):
                series = prices.get(prod) or []
                if not series:
                    continue
                sp, lp, at = [], [], []
                for t, q, _n in sells:
                    if q != prod or t >= len(series) or series[t] is None:
                        continue
                    at.append(series[t])
                    sp.append(pct(series[t], series))
                    lo, hi = max(0, t - 12), min(len(series), t + 13)
                    lp.append(pct(series[t], series[lo:hi]))
                if not at:
                    continue
                pool = [x for x in series if x is not None]
                print(f"{prod:12}{len(at):>5}{statistics.mean(sp):>12.1f}"
                      f"{statistics.mean(lp):>11.1f}{statistics.mean(at):>12.1f}"
                      f"{statistics.mean(pool):>12.1f}")


if __name__ == "__main__":
    main()
