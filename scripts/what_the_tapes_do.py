"""Do the downloaded replays exercise the mechanics our teacher never touches?

13 of 115 input features are identically zero across the planner's 920,320 self-play turns
(`check_feature_scales.py`, 2026-08-20): TOMATO as a crop tile / carried item / seed / shed entry,
GOOSE as an animal tile / carried / shed, and EGG as carried / shed. The cause is the teacher's
repertoire, not the encoder -- it never plants tomato and has no geese, so it never holds eggs.

Imitation cannot reach a mechanic the teacher never demonstrates, at any data volume. Adding the
Kaggle replays to the BC set would fix that IF the replays actually play those mechanics. This
measures whether they do, before any work is done on the strength of the assumption.

**Two caveats on the answer, both recorded rather than discovered again.**

  - The downloads are SELECTED, not a sample. They are mostly losses, so a mechanic being common
    here is not evidence it wins.
  - `SELLABLE` blocked CARROT, TOMATO and EGG from being sold at all for a period, which
    invalidated four carrot arms and the goose verdict. Two of the three dead features are exactly
    those products, so "our teacher does not do it" may descend from a bug rather than a judgement.

    python -u scripts/what_the_tapes_do.py --replays data
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

#: The mechanics the planner never demonstrates, and what an action looks like for each.
WATCH = {
    "PLANT TOMATO": ("unit", "PLANT", "TOMATO"),
    "PLANT CARROT": ("unit", "PLANT", "CARROT"),
    "BUY_SEED TOMATO": ("market", "BUY_SEED", "TOMATO"),
    "BUY_SEED CARROT": ("market", "BUY_SEED", "CARROT"),
    "BUY_ANIMAL GOOSE": ("market", "BUY_ANIMAL", "GOOSE"),
    "SELL EGG": ("market", "SELL", "EGG"),
    "SELL TOMATO": ("market", "SELL", "TOMATO"),
    "SELL CARROT": ("market", "SELL", "CARROT"),
    # Baselines, so a zero above can be read against a mechanic that is definitely present.
    "PLANT MELON": ("unit", "PLANT", "MELON"),
    "BUY_ANIMAL COW": ("market", "BUY_ANIMAL", "COW"),
    "SELL MILK": ("market", "SELL", "MILK"),
}


def scan(path, counts, games_with):
    """Count matching actions across every recorded turn of one replay, both seats."""
    try:
        raw = json.loads(pathlib.Path(path).read_text())
    except Exception:                                          # noqa: BLE001
        return False
    steps = raw.get("steps") or []
    seen = set()
    turns = 0
    for step in steps:
        for seat_state in step:
            action = (seat_state or {}).get("action")
            if not isinstance(action, dict):
                continue
            turns += 1
            units = [action.get("farmer")] + list(action.get("hands") or [])
            market = action.get("market") or []
            for label, (kind, op, item) in WATCH.items():
                if kind == "unit":
                    hit = any(a and str(a[0]) == op and len(a) > 1 and str(a[1]) == item
                              for a in units if a)
                else:
                    hit = any(isinstance(o, (list, tuple)) and len(o) > 1
                              and str(o[0]) == op and str(o[1]) == item for o in market)
                if hit:
                    counts[label] += 1
                    seen.add(label)
    for label in seen:
        games_with[label] += 1
    return turns > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replays", default="data")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    paths = sorted(glob.glob(args.replays.rstrip("/") + "/*.json"))
    if args.limit:
        paths = paths[:args.limit]
    if not paths:
        raise SystemExit("no *.json under %s" % args.replays)

    counts = collections.Counter()
    games_with = collections.Counter()
    ok = 0
    for p in paths:
        if scan(p, counts, games_with):
            ok += 1
    print("scanned %d replays (%d parsed)\n" % (len(paths), ok))

    print("%-20s %12s %14s" % ("mechanic", "turns", "games (of %d)" % ok))
    for label in WATCH:
        n, g = counts[label], games_with[label]
        flag = ""
        if n == 0:
            flag = "   <-- ABSENT here too"
        elif g >= max(1, ok // 4):
            flag = "   <-- common"
        print("%-20s %12s %10d%s" % (label, format(n, ","), g, flag))

    print("\nThe planner's own 920,320 turns contain ZERO of: PLANT TOMATO, BUY_ANIMAL GOOSE,")
    print("SELL EGG, and every tomato/goose/egg carry and shed entry. Anything above with a")
    print("non-zero count is a mechanic BC could learn from the tapes and cannot learn from")
    print("the planner. Anything at zero here is unreachable by imitation from either source,")
    print("and only RL or a new planner arm could find it.")


if __name__ == "__main__":
    main()
