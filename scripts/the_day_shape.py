"""The schedule, day by day: what share of each day goes to the ANIMALS and what to the PLANTS.

Season totals hide the schedule. Two agents with the same 30-day op mix can run completely
different seasons -- one front-loading the pens and coasting, the other building the herd late.
Alex, 2026-08-24: *"the interesting thing is the schedule and the animal / plant split per day."*

Per day this reports, averaged over an agent's games:

    plant   PLANT + WATER + HARVEST + FERTILIZE + DIG        work on the crop tiles
    anim    FEED + CARE + COLLECT_FERTILIZER + PLACE + BUILD work on the pens
    a%      anim as a share of (plant + anim) -- the SPLIT, which is the question
    till    crop tiles standing at that day's dawn
    pens    pens standing at that day's dawn
    buys    BUY_ANIMAL orders submitted that day
    sells   SELL orders submitted that day

Movement and PASS are excluded on purpose: they are the cost of the routing, not the schedule, and
Alex has ruled them uninteresting. `till` and `pens` are STATE, so they say what the schedule built
rather than what it spent turns on.
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
PLANT_OPS = {"PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG"}
ANIM_OPS = {"FEED", "CARE", "COLLECT_FERTILIZER", "PLACE", "BUILD_PASTURE", "BUILD_COOP"}


def per_day(steps, seat, days):
    out = []
    for d in range(days):
        t0 = d * TPD
        if t0 >= len(steps):
            break
        o = steps[t0][seat]["observation"]
        farm = o["farms"][seat]
        till = pens = 0
        for row in (farm.get("tiles") or []):
            for tile in row:
                if not isinstance(tile, dict):
                    continue
                if tile.get("crop"):
                    till += 1
                if tile.get("kind") in ("PASTURE", "COOP"):
                    pens += 1
        p = an = buys = sells = 0
        for t in range(t0, min(t0 + TPD, len(steps) - 1)):
            a = steps[t + 1][seat].get("action")
            if not isinstance(a, dict):
                continue
            for x in [a.get("farmer")] + list(a.get("hands") or []):
                if isinstance(x, (list, tuple)) and x:
                    if x[0] in PLANT_OPS:
                        p += 1
                    elif x[0] in ANIM_OPS:
                        an += 1
            for ordr in (a.get("market") or []):
                if isinstance(ordr, (list, tuple)) and ordr:
                    if ordr[0] == "BUY_ANIMAL":
                        buys += 1
                    elif ordr[0] == "SELL":
                        sells += 1
        out.append((p, an, till, pens, buys, sells))
    return out


def profile(files, who, days):
    acc = collections.defaultdict(lambda: [0.0] * 6)
    n = 0
    for f in files:
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if who not in names:
            continue
        seat = names.index(who)
        rows = per_day(rec["steps"], seat, days)
        for d, r in enumerate(rows):
            for i, v in enumerate(r):
                acc[d][i] += v
        n += 1
    if not n:
        return None, 0
    return {d: [v / n for v in r] for d, r in acc.items()}, n


def show(label, prof, n, days):
    print(f"\n{label}  (n={n})")
    print(f"{'day':>4} {'plant':>7} {'anim':>7} {'a%':>6} {'till':>6} {'pens':>6} "
          f"{'buys':>6} {'sells':>7}")
    for d in range(days):
        if d not in prof:
            break
        p, an, till, pens, buys, sells = prof[d]
        tot = p + an
        pct = (100.0 * an / tot) if tot else 0.0
        print(f"{d:>4} {p:>7.1f} {an:>7.1f} {pct:>5.0f}% {till:>6.1f} {pens:>6.1f} "
              f"{buys:>6.1f} {sells:>7.1f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--who", default="")
    a = ap.parse_args()

    dl = sorted(glob.glob("/Users/alexchilton/Downloads/*.json"))
    ours = sorted(glob.glob(str(REPO / "data/seed_scripts/losses/*.json")))
    kawa = []
    for name in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c"):
        kawa += sorted(glob.glob(str(REPO / f"data/seed_scripts/{name}/*.json")))

    who = [("SOUTA", dl, "SOUTA Sakurai"),
           ("kawashigi", kawa, "カワシギ"),
           ("us", ours, "alex chilton")]
    if a.who:
        who = [(a.who, dl + ours + kawa, a.who)]

    for label, files, name in who:
        prof, n = profile(files, name, a.days)
        if prof is None:
            print(f"\n{label}: no games")
            continue
        show(label, prof, n, a.days)


if __name__ == "__main__":
    main()
