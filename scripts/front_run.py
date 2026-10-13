"""Does he sell into the book BEFORE the opponent does? Lead/lag on the same product, same episode.

Both farms trade one shared book, and `market_price` falls as it fills, so whoever gets a product
away first is paid more for it. If his edge is timing rather than plan -- his season sell TOTALS are
identical across seasons to the unit, only the hours move -- then the hours should line up against
the opponent, not against the clock.

For every SELL he makes, this finds the opponent's nearest SELL of the SAME product and reports the
signed gap in turns. Negative = he went first.

    python -u scripts/front_run.py mtmr_s1
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def sells(stream):
    out = collections.defaultdict(list)
    for t, a in enumerate(stream):
        if isinstance(a, str):
            a = json.loads(a)
        for o in (a or {}).get("market") or []:
            if o and o[0] == "SELL":
                out[o[1]].append(t)
    return out


def main():
    teams = sys.argv[1:] or ["mtmr_s1"]
    seen = set()
    rows = collections.defaultdict(list)      # team -> gaps
    first = collections.defaultdict(lambda: [0, 0])   # team -> [went first, total]
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen or len(r["teams"]) < 2:
                continue
            seen.add(r["episode"])
            for seat, team in enumerate(r["teams"]):
                if team not in teams or seat >= len(r["actions"]):
                    continue
                opp = 1 - seat
                if opp >= len(r["actions"]):
                    continue
                mine, theirs = sells(r["actions"][seat]), sells(r["actions"][opp])
                for prod, ts in mine.items():
                    ots = theirs.get(prod) or []
                    if not ots:
                        continue
                    # first offer of the product, each side: who opens the book
                    first[team][1] += 1
                    if min(ts) < min(ots):
                        first[team][0] += 1
                    for t in ts:
                        rows[team].append(min(ots, key=lambda o: abs(o - t)) - t)
    for team in teams:
        g = rows[team]
        if not g:
            print(f"{team}: no paired sells found")
            continue
        ahead = sum(1 for x in g if x > 0)
        print(f"\n{team}: {len(g):,} sells matched to an opponent sell of the same product")
        print(f"   he is EARLIER on {ahead:,} ({100*ahead/len(g):.1f}%), "
              f"later on {sum(1 for x in g if x < 0):,}, same turn {sum(1 for x in g if x == 0):,}")
        print(f"   median gap {statistics.median(g):+.0f} turns, mean {statistics.mean(g):+.1f}")
        f = first[team]
        print(f"   opened the book first on {f[0]}/{f[1]} product-episodes "
              f"({100*f[0]/f[1] if f[1] else 0:.1f}%)")


if __name__ == "__main__":
    main()
