"""When one player's two games differ on the same day, WHAT differs? Movement, planting, selling?

Alex, 2026-08-20: "so what are the differences? just movement or what?"

Every count so far says days ARE different -- 212 distinct blocks in 228 of Kawashigi's games by
d29 -- without saying in what respect. That matters a lot for the design:

  If the difference is MOVEMENT (route order, which tile first), a stored block is close to right
  and a repair step that re-derives the route from the live board fixes it. That is what the
  teacher's own `_live_ops` already does.

  If the difference is WHICH CROP or HOW MUCH TO SELL, the block encodes a different decision, and
  no repair recovers it -- you would be executing the wrong plan neatly.

So this diffs the modal block against every other block for the same player and day, turn by turn,
and attributes each mismatch to the op that changed.

    python -u scripts/what_differs_between_blocks.py --player カワシギ --days 14 \\
        --dirs data/seed_scripts/kawashigi data/seed_scripts/downloads_2026-08-14to16
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TURNS_PER_DAY = 24
MOVES = frozenset(("NORTH", "SOUTH", "EAST", "WEST"))
FIELD = frozenset(("PLANT", "WATER", "HARVEST", "FERTILIZE", "CLEAR"))
CARRY = frozenset(("PICKUP", "DROP", "PLACE"))
HERD = frozenset(("FEED", "CARE", "BUILD_PASTURE", "BUILD_COOP"))
MARKET = frozenset(("SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "HIRE", "BUY_LAND"))


def bucket(op_name):
    if op_name in MOVES:
        return "movement"
    if op_name in FIELD:
        return "field work"
    if op_name in CARRY:
        return "carry/place"
    if op_name in HERD:
        return "herd upkeep"
    if op_name in MARKET:
        return "market"
    if op_name == "PASS":
        return "idle"
    return "other"


def unit_ops(action):
    acts = [action.get("farmer")] + list(action.get("hands") or [])
    return [(str(a[0]) if a else "PASS", tuple(map(str, a[1:])) if a else ()) for a in acts]


def day_of(rep, seat, days):
    out = collections.defaultdict(dict)
    for step in rep.get("steps") or []:
        if seat >= len(step):
            continue
        cell = step[seat]
        obs = cell.get("observation") or {}
        day, hour = int(obs.get("day", 0) or 0), int(obs.get("hour", 0) or 0)
        if day >= days or cell.get("action") is None:
            continue
        out[day][hour] = cell["action"]
    return {d: v for d, v in out.items() if len(v) == TURNS_PER_DAY}


def diff(a, b, tally):
    """Attribute every mismatch between two whole days."""
    for hour in range(TURNS_PER_DAY):
        ua, ub = unit_ops(a[hour]), unit_ops(b[hour])
        for i in range(max(len(ua), len(ub))):
            oa = ua[i] if i < len(ua) else ("MISSING", ())
            ob = ub[i] if i < len(ub) else ("MISSING", ())
            if oa == ob:
                continue
            if oa[0] != ob[0]:
                tally["op differs: %s" % bucket(oa[0])] += 1
                tally["_pair_%s->%s" % (oa[0], ob[0])] += 1
            else:
                tally["same op, different target: %s" % bucket(oa[0])] += 1
        ma = sorted(map(str, a[hour].get("market") or []))
        mb = sorted(map(str, b[hour].get("market") or []))
        if ma != mb:
            tally["market orders differ"] += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--player", required=True)
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--max-games", type=int, default=60)
    args = ap.parse_args()

    paths = []
    for d in args.dirs:
        paths += sorted(glob.glob(d.rstrip("/") + "/*.json"))

    seasons = []
    for p in paths:
        if len(seasons) >= args.max_games:
            break
        try:
            rep = json.loads(pathlib.Path(p).read_text())
        except Exception:                                            # noqa: BLE001
            continue
        if not isinstance(rep, dict) or not rep.get("steps"):
            continue
        info = rep.get("info")
        names = info.get("TeamNames") if isinstance(info, dict) else None
        if not names:
            continue
        for seat, n in enumerate(names):
            if n == args.player:
                d = day_of(rep, seat, args.days)
                if d:
                    seasons.append(d)
    print("%s: %d seasons compared\n" % (args.player, len(seasons)))
    if len(seasons) < 2:
        raise SystemExit("need at least two seasons")

    for day in range(args.days):
        have = [s[day] for s in seasons if day in s]
        if len(have) < 2:
            continue
        tally = collections.Counter()
        ref = have[0]
        pairs = 0
        for other in have[1:]:
            diff(ref, other, tally)
            pairs += 1
        total = sum(v for k, v in tally.items()
                    if not k.startswith("_") and k != "market orders differ")
        if total == 0:
            print("day %-2d  %d pairs  IDENTICAL" % (day, pairs))
            continue
        parts = [(k, v) for k, v in tally.items()
                 if not k.startswith("_") and k != "market orders differ"]
        parts.sort(key=lambda kv: -kv[1])
        print("day %-2d  %d pairs  %d differing unit-slots  (%.1f per pair), market turns %d"
              % (day, pairs, total, total / pairs, tally["market orders differ"]))
        for k, v in parts[:5]:
            print("        %5.1f%%  %s" % (100.0 * v / total, k))
        # **Which field ops, specifically.** "field work" mixes a real decision with work that is
        # re-derivable from the board: PLANT chooses a crop and a tile, but WATER/HARVEST/FERTILIZE/
        # CLEAR are dictated by what is standing there -- and `_live_ops` already re-derives exactly
        # those at each stop. So a block that disagrees on WATER costs nothing to repair, and one
        # that disagrees on PLANT is a different plan.
        field = collections.Counter()
        for k, v in tally.items():
            if not k.startswith("_pair_"):
                continue
            a, _, b = k[len("_pair_"):].partition("->")
            for name in (a, b):
                if name in FIELD:
                    field[name] += v
        if field:
            n = sum(field.values())
            print("        of which field ops: %s"
                  % "  ".join("%s %.0f%%" % (k, 100.0 * v / n)
                              for k, v in field.most_common()))


if __name__ == "__main__":
    main()
