"""What separates a rich seat from a poor one, across every downloaded ladder game, both seats.

We are confident about geometry, the day planner and now the sell rule, and the schedule is copied
from a long-standing leader. So the question is no longer "is our execution good" but "what is on
the board that we never touch". This ranks the observable levers by how well they predict money,
over ~120 real seats rather than over a fixture, and then says where our own seats sit in each
distribution.

Everything here is read off the replay: units hired, animals standing, tiles owned, and the volume
of each market order type. No model of the game is involved.

    PYTHONPATH=. python3 -u scripts/what_the_others_do.py data/ladder/*/*.json
"""

import collections
import glob
import json
import statistics
import sys

ME = "alex chilton"
LEVERS = ("hires", "herd", "tiles", "buy_product_offered", "buy_animal_offered", "sell_units_offered",
          "sell_orders", "feed", "care", "plant", "water", "harvest", "fertilize")


def seats(path):
    d = json.loads(open(path).read())
    teams = (d.get("info") or {}).get("TeamNames") or []
    steps = d["steps"]
    rewards = d.get("rewards") or [s.get("reward") for s in steps[-1]]
    out = []
    for pl in (0, 1):
        row = collections.Counter()
        peak_hires = peak_herd = peak_tiles = 0
        for t, step in enumerate(steps):
            act = (step[pl] or {}).get("action") or {}
            for o in act.get("market", []) or []:
                if not o:
                    continue
                if o[0] == "SELL":
                    row["sell_units_offered_offered"] += int(o[2])
                    row["sell_orders"] += 1
                elif o[0] == "BUY_PRODUCT":
                    row["buy_product_offered_offered"] += int(o[2])
                elif o[0] == "BUY_ANIMAL":
                    row["buy_animal_offered_offered"] += int(o[2]) if len(o) > 2 else 1
            for h in act.get("hands", []) or []:
                if h and h[0] in ("FEED", "CARE", "PLANT", "WATER", "HARVEST", "FERTILIZE"):
                    row[h[0].lower()] += 1
            f = act.get("farmer")
            if f and f[0] in ("FEED", "CARE", "PLANT", "WATER", "HARVEST", "FERTILIZE"):
                row[f[0].lower()] += 1
            peak_hires = max(peak_hires, len(act.get("hands") or []))
            obs = (step[pl] or {}).get("observation") or {}
            if obs.get("farms") and t % 24 == 0:
                farm = obs["farms"][obs.get("player", pl)]
                peak_tiles = max(peak_tiles, sum(1 for r in farm["tiles"] for c in r
                                                 if c != "LOCKED"))
                peak_herd = max(peak_herd, sum(1 for r in farm["tiles"] for c in r
                                               if isinstance(c, dict) and c.get("animal")))
        row["hires"], row["herd"], row["tiles"] = peak_hires, peak_herd, peak_tiles
        out.append((teams[pl] if pl < len(teams) else "?", rewards[pl] or 0, row))
    return out


def corr(xs, ys):
    if len(xs) < 3 or statistics.pstdev(xs) == 0 or statistics.pstdev(ys) == 0:
        return 0.0
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    return num / (len(xs) * statistics.pstdev(xs) * statistics.pstdev(ys))


def main(paths):
    rows = []
    for p in paths:
        try:
            rows.extend(seats(p))
        except Exception:
            continue
    money = [r[1] for r in rows]
    ours = [r for r in rows if r[0] == ME]
    rich = sorted(rows, key=lambda r: -r[1])[:max(3, len(rows) // 5)]
    poor = sorted(rows, key=lambda r: r[1])[:max(3, len(rows) // 5)]

    print(f"  {len(rows)} seats from {len(paths)} games; {len(ours)} of them ours\n")
    print(f"  {'lever':<14}{'corr w/ money':>14}{'top 20%':>10}{'bottom 20%':>12}"
          f"{'OURS mean':>11}{'our percentile':>16}")
    for lever in LEVERS:
        xs = [r[2][lever] for r in rows]
        c = corr(xs, money)
        hi = statistics.mean([r[2][lever] for r in rich])
        lo = statistics.mean([r[2][lever] for r in poor])
        om = statistics.mean([r[2][lever] for r in ours]) if ours else 0
        pct = 100.0 * sum(1 for x in xs if x < om) / max(1, len(xs))
        print(f"  {lever:<14}{c:>+14.3f}{hi:>10.0f}{lo:>12.0f}{om:>11.0f}{pct:>15.0f}%")

    print(f"\n  money: ours mean ${statistics.mean([r[1] for r in ours]):,.0f}   "
          f"field mean ${statistics.mean(money):,.0f}   "
          f"top-20% mean ${statistics.mean([r[1] for r in rich]):,.0f}")


if __name__ == "__main__":
    args = sys.argv[1:] or glob.glob("data/ladder/*/*.json")
    main(args)
