"""Realized price per unit, ours against theirs, on the same book in the same game.

The question this settles, from the 2026-08-24 review: *"compute realized $/unit per product for our
seat vs their seat in every downloaded game. If we're below ~70% on any major product, sell cadence
and sizing is the biggest lever in the repo. If we're within 90%+, the endgame line stands as the
main effort."*

**Fills, not offers.** The agent re-posts each order every turn, so the action stream over-counts
sales by roughly 24x -- summing it is the single most repeated measurement error in this project.
This reads inventory instead: for a product whose only sink is the market, the drop in
`shed + carried` between two turns IS the number of units that sold.

    MILK, WOOL, EGG, MELON, STRAWBERRY, CARROT, TOMATO   only sink is SELL       exact
    WHEAT                                                also consumed by FEED   excluded
    FERTILIZER                                           also consumed by FERTILIZE  excluded

Revenue is those units priced at the town's quote on the turn they left. That is a slight
over-estimate, because a SELL walks the book down one unit at a time -- but it is the SAME
over-estimate for both seats in the same game on the same book, and the output is a ratio, so the
bias cancels where it matters.

**Both seats, same game, same town.** That is what makes this a controlled comparison rather than a
league table: any difference is cadence and sizing, not luck of the draw.

    python -u scripts/what_we_actually_get_paid.py --dirs downloads_2026-08-20 --limit 80
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
US = "alex chilton"

# Sold-only products. WHEAT and FERTILIZER have a second sink and cannot be inferred this way.
SOLD_ONLY = ("MILK", "WOOL", "EGG", "MELON", "STRAWBERRY", "CARROT", "TOMATO")


def _held(step, seat):
    """`{product: units}` across the shed and every unit's hands, for `seat`'s own observation."""
    priv = step[seat]["observation"]["private"]
    out = collections.Counter(priv.get("shed") or {})
    for inv in priv.get("inventories") or []:
        out.update(inv)
    return out


def audit(path):
    """`{product: [our_units, our_revenue, their_units, their_revenue]}` for one game, or None."""
    try:
        rep = json.loads(pathlib.Path(path).read_text())
    except Exception:
        return None
    # Not every .json in these folders is a replay -- some are action lists and schedules saved
    # alongside them. A dict with `steps` and `info` is the shape this reads; anything else is
    # skipped rather than crashed on.
    if not isinstance(rep, dict):
        return None
    info = rep.get("info") or {}
    names = info.get("TeamNames") or []
    if US not in names or len(rep.get("steps") or []) < 700:
        return None
    seat = names.index(US)
    steps = rep["steps"]

    out = {p: [0, 0.0, 0, 0.0] for p in SOLD_ONLY}
    prev = {0: _held(steps[0], 0), 1: _held(steps[0], 1)}
    for i in range(1, len(steps)):
        step = steps[i]
        px = ((step[0]["observation"].get("market") or {}).get("prices") or {})
        for s in (0, 1):
            now = _held(step, s)
            for p in SOLD_ONLY:
                gone = prev[s].get(p, 0) - now.get(p, 0)
                if gone > 0:
                    slot = 0 if s == seat else 2
                    out[p][slot] += gone
                    out[p][slot + 1] += gone * float(px.get(p, 0) or 0)
            prev[s] = now
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", default="downloads_2026-08-20",
                    help="comma-separated folders under data/seed_scripts")
    ap.add_argument("--limit", type=int, default=80)
    a = ap.parse_args()

    files = []
    for d in a.dirs.split(","):
        files += sorted(glob.glob(str(REPO / "data/seed_scripts" / d.strip() / "*.json")))
    print(f"scanning {len(files)} files from {a.dirs}", flush=True)

    total = {p: [0, 0.0, 0, 0.0] for p in SOLD_ONLY}
    games = 0
    for f in files:
        if games >= a.limit:
            break
        r = audit(f)
        if r is None:
            continue
        games += 1
        for p in SOLD_ONLY:
            for k in range(4):
                total[p][k] += r[p][k]
        if games % 10 == 0:
            print(f"  {games} games...", flush=True)

    print(f"\n{games} games where '{US}' played, both seats, same book\n")
    print(f"{'product':<12} {'our units':>10} {'our $/u':>9} {'their units':>12} "
          f"{'their $/u':>10} {'ours/theirs':>12}")
    for p in SOLD_ONLY:
        ou, orev, tu, trev = total[p]
        if not ou and not tu:
            continue
        opu = orev / ou if ou else 0.0
        tpu = trev / tu if tu else 0.0
        ratio = (opu / tpu) if tpu else float("nan")
        print(f"{p:<12} {ou:>10,} {opu:>9,.1f} {tu:>12,} {tpu:>10,.1f} {ratio:>11.0%}")

    print("\nBelow ~70% on a major product means cadence and sizing is the lever.")
    print("Within 90%+ means the market is being worked about as well as the field is.")


if __name__ == "__main__":
    main()
