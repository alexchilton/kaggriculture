"""Is his sell timing worth anything? Price HIS schedule and the OTHER season's on the SAME book.

Two of his seasons share a byte-identical 719-turn farm and identical season sell totals per
product, differing only in which hour each sale is offered. That makes a clean counterfactual: take
season B's offer schedule, evaluate it against season A's own price series, and compare with what A
actually did. Same goods, same amounts, same book -- only the hours change.

    python -u scripts/timing_counterfactual.py 107041112 107064978

CAVEAT, and it bounds the whole result: the price series is ENDOGENOUS. `market_price` falls as the
book fills, so had he really sold on B's hours, A's prices would not have been what we read. This
values a schedule against observed prices, which is an approximation that ignores his own impact.
It can say whether the chosen hours look better than the alternative on the same tape; it cannot
give the true revenue difference.
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def pull(ep, team):
    rep = json.loads(find(ep).read_text())
    seat = (rep["info"]["TeamNames"]).index(team)
    prices, sells = collections.defaultdict(dict), []
    for t, step in enumerate(rep.get("steps") or []):
        cell = (step[seat] if seat < len(step) else None) or {}
        for k, v in ((cell.get("observation") or {}).get("market") or {}).get("prices", {}).items():
            prices[k][t] = v
        for o in (cell.get("action") or {}).get("market") or []:
            if o and o[0] == "SELL":
                sells.append((t, o[1], int(o[2])))
    return prices, sells


def value(schedule, prices):
    """Sum of units x quoted price, per product, skipping turns that product has no quote for."""
    tot = collections.Counter()
    for t, prod, n in schedule:
        p = prices.get(prod, {}).get(t)
        if p is not None:
            tot[prod] += n * p
    return tot


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    team = sys.argv[3] if len(sys.argv) > 3 else "mtmr_s1"
    pa, sa = pull(a, team)
    pb, sb = pull(b, team)
    for who, prices, own, other, oep in ((a, pa, sa, sb, b), (b, pb, sb, sa, a)):
        v_own, v_oth = value(own, prices), value(other, prices)
        print(f"\n=== book of {who}: his own hours vs season {oep}'s hours ===")
        print(f"{'product':12}{'his hours':>14}{'other hours':>14}{'his edge':>12}{'%':>8}")
        to, tt = 0, 0
        for prod in sorted(set(v_own) | set(v_oth)):
            x, y = v_own[prod], v_oth[prod]
            to += x
            tt += y
            print(f"{prod:12}{x:>14,.0f}{y:>14,.0f}{x - y:>12,.0f}"
                  f"{(100 * (x - y) / y if y else 0):>8.1f}")
        print(f"{'TOTAL':12}{to:>14,.0f}{tt:>14,.0f}{to - tt:>12,.0f}"
              f"{(100 * (to - tt) / tt if tt else 0):>8.1f}")


if __name__ == "__main__":
    main()
