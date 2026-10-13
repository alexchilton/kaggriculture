"""Does he wait for the book to bounce? Price at his sell turns against the price one drain ago.

The town lifts stock every `townShopSellInterval` = 4 turns and `market_price` rises as the book
empties, so a seller who waits for the recovery is selling into a RISING quote. Mechanically that is
`price[t] > price[t-4]`.

Measured per seat on the same episode, so both sides face the same book and the comparison is a
controlled one.

    python -u scripts/bounce_rule.py 107642213 107646523 ...
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    agg = collections.defaultdict(lambda: collections.Counter())
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        for seat, team in enumerate(teams):
            prices = collections.defaultdict(dict)
            sells = collections.defaultdict(list)
            for t, step in enumerate(rep.get("steps") or []):
                cell = (step[seat] if seat < len(step) else None) or {}
                for k, v in ((cell.get("observation") or {}).get("market") or {}).get("prices", {}).items():
                    prices[k][t] = v
                for o in (cell.get("action") or {}).get("market") or []:
                    if o and o[0] == "SELL":
                        sells[o[1]].append(t)
            for prod, ts in sells.items():
                for t in ts:
                    now, then = prices[prod].get(t), prices[prod].get(t - 4)
                    if now is None or then is None:
                        continue
                    agg[team]["n"] += 1
                    if now > then:
                        agg[team]["rising"] += 1
                    elif now < then:
                        agg[team]["falling"] += 1
                    else:
                        agg[team]["flat"] += 1
    print(f"{'team':22}{'sell turns':>11}{'rising':>9}{'falling':>9}{'flat':>8}  "
          f"{'sells into a RISING book'}")
    for team, c in sorted(agg.items(), key=lambda kv: -kv[1]["rising"] / max(1, kv[1]["n"])):
        n = c["n"]
        print(f"{team[:22]:22}{n:>11,}{c['rising']:>9,}{c['falling']:>9,}{c['flat']:>8,}"
              f"  {100*c['rising']/max(1,n):>10.1f}%")


if __name__ == "__main__":
    main()
