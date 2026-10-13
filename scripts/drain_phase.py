"""Do his sells lock to the town's drain clock? Sell turns modulo the shop and centre intervals.

`townShopSellInterval: 4` and `townCenterSellInterval: 24` (both in every replay's configuration):
the town lifts stock out of the book on a fixed cadence, and `market_price` rises as it empties. So
the best hour to sell is a fixed phase of that clock, and the rule -- if there is one -- is visible
as a lopsided histogram of sell turns modulo 4 and modulo 24. A flat histogram means the clock is
not what he is watching.

    python -u scripts/drain_phase.py mtmr_s1 Majkel1337 "Yusuke Hayashi" SpaTaro
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def main():
    teams = sys.argv[1:] or ["mtmr_s1"]
    seen = set()
    m4 = collections.defaultdict(collections.Counter)
    m24 = collections.defaultdict(collections.Counter)
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen:
                continue
            seen.add(r["episode"])
            for seat, team in enumerate(r["teams"]):
                if team not in teams or seat >= len(r["actions"]):
                    continue
                for t, a in enumerate(r["actions"][seat]):
                    if isinstance(a, str):
                        a = json.loads(a)
                    if any(o and o[0] == "SELL" for o in (a or {}).get("market") or []):
                        m4[team][t % 4] += 1
                        m24[team][t % 24] += 1
    for team in teams:
        c4, c24 = m4[team], m24[team]
        n = sum(c4.values())
        if not n:
            continue
        print(f"\n{team}: {n:,} turns carrying a SELL")
        print("   turn mod 4 (shop drain): " +
              "  ".join(f"{k}:{100*c4[k]/n:5.1f}%" for k in range(4)))
        top = sorted(c24.items(), key=lambda kv: -kv[1])[:6]
        print("   hour of day, top 6:      " +
              "  ".join(f"h{k}:{100*v/n:4.1f}%" for k, v in top))
        flat = 100 / 24
        print(f"   (flat would be 25.0% and {flat:.1f}%)")


if __name__ == "__main__":
    main()
