"""Carrot drain runs 0 to 11. Does ANY player's carrot planting respond to it?

The town's carrot drain is set by the shop draw: `PET_CAFE` sells only CARROT so it pulls 2 a tick,
`FARMERS_MARKET` and the rest pull 1. Five pet cafes is drain 11 and a book that reaches $498; no
pet cafe is drain 0 and carrot is worth about what wheat is.

If a player reads that, their carrot tiles rise with the drain. If they do not, their carrot is a
constant and the correlation is flat. This measures exactly that, per player, over every game held:
the ladder corpus of 2026-08-23, SOUTA's 25, カワシギ's tapes and our own recorded games.

Reported per player with at least three games:

    r        Pearson correlation between the town's carrot drain and peak carrot tiles
    lo/hi    mean peak carrot tiles in that player's LOW-drain and HIGH-drain games,
             split at drain 5 -- the raw version of the same thing, since n is small
    span     the drain range that player actually saw; a player who only ever met drain 0-3
             cannot demonstrate a response and `r` over that span means nothing

**A flat r is not proof of a fixed policy.** It can equally mean the player never drew a deep town.
That is why `span` is printed beside it and why the split columns are raw means.
"""

import argparse
import collections
import glob
import json
import math
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "reference"))

TPD = 24


def _shops():
    import kaggriculture as KG
    return KG.SHOPS


def carrot_drain(obs, shops):
    d = 0
    for name in ((obs.get("town") or {}).get("unlocked_shops") or []):
        ps = shops.get(name) or []
        if "CARROT" in ps:
            d += 2 if len(ps) == 1 else 1
    return d


def peak_and_sold(steps, seat):
    peak = 0
    for d in range(30):
        t = d * TPD
        if t >= len(steps):
            break
        farm = steps[t][seat]["observation"]["farms"][seat]
        n = sum(1 for row in (farm.get("tiles") or []) for x in row
                if isinstance(x, dict) and x.get("crop") == "CARROT")
        peak = max(peak, n)
    return peak


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return float("nan")
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-games", type=int, default=3)
    a = ap.parse_args()
    shops = _shops()

    files = (glob.glob(str(REPO / "data/seed_scripts/leaders_2026-08-24/*.json"))
             + glob.glob("/Users/alexchilton/Downloads/*.json")
             + glob.glob(str(REPO / "data/seed_scripts/losses/*.json")))
    for name in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c"):
        files += glob.glob(str(REPO / f"data/seed_scripts/{name}/*.json"))

    per = collections.defaultdict(list)
    drains = collections.Counter()
    for f in sorted(set(files)):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        steps = rec["steps"]
        t = min(29 * TPD, len(steps) - 1)
        for seat, who in enumerate(names):
            dr = carrot_drain(steps[t][seat]["observation"], shops)
            per[who].append((dr, peak_and_sold(steps, seat)))
            if seat == 0:
                drains[dr] += 1
        print(f"  {pathlib.Path(f).stem}", flush=True)

    print("\nHOW OFTEN EACH DRAIN APPEARS (one count per game)")
    tot = sum(drains.values()) or 1
    for d in sorted(drains):
        print(f"  drain {d:>2}  {drains[d]:>4} games  {100.0 * drains[d] / tot:>5.1f}%")

    rows = []
    for who, obs in per.items():
        if len(obs) < a.min_games:
            continue
        xs = [o[0] for o in obs]
        ys = [o[1] for o in obs]
        lo = [y for x, y in obs if x < 5]
        hi = [y for x, y in obs if x >= 5]
        rows.append((pearson(xs, ys), who, len(obs), min(xs), max(xs),
                     (sum(lo) / len(lo)) if lo else float("nan"),
                     (sum(hi) / len(hi)) if hi else float("nan")))

    print(f"\nDOES CARROT PLANTING FOLLOW THE DRAIN?  ({len(rows)} players, "
          f">= {a.min_games} games)\n")
    print(f"{'r':>6} {'who':>26} {'n':>3} {'span':>8} {'lo<5':>7} {'hi>=5':>7}")
    for r, who, n, dmin, dmax, lo, hi in sorted(rows, key=lambda x: -(x[0] if x[0] == x[0] else -9)):
        rs = f"{r:>6.2f}" if r == r else f"{'n/a':>6}"
        los = f"{lo:>7.1f}" if lo == lo else f"{'-':>7}"
        his = f"{hi:>7.1f}" if hi == hi else f"{'-':>7}"
        print(f"{rs} {who[:26]:>26} {n:>3} {str(dmin) + '-' + str(dmax):>8} {los} {his}")


if __name__ == "__main__":
    main()
