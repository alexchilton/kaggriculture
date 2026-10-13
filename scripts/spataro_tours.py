"""His WALK: where each unit stands, turn by turn, and what it does there.

The schedule rows carry counts and no geometry, so our tour is re-derived from `router.crop_ops`
prizes while his comes off the tape. At the d7 handover the board is identical at dawn and the walk
still differs -- `move 102/86`, `water 22/26` -- so the walk is the last thing being invented rather
than measured.

Alex: "we have the possibility to follow his move algo... is it lawnmower or ?"

This prints the sequence of (x, y) a unit occupies across a day with the op it issued, so the shape
is readable directly instead of inferred from a move count.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TPD = 24
WORK = ("PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER",
        "DIG", "BUILD_COOP", "BUILD_PASTURE", "PLACE", "PICKUP", "DROP")


def units_at(obs, seat):
    farm = (obs.get("farms") or [])[seat]
    out = [tuple(farm.get("farmer") or (0, 0))]
    for h in (farm.get("hands") or []):
        out.append(tuple(h))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", default="data/replays_spa_sub/107068412.json")
    ap.add_argument("--team", default="SpaTaro")
    ap.add_argument("--day", type=int, default=7)
    a = ap.parse_args()

    blob = json.loads(Path(a.replay).read_text())
    names = list((blob.get("info") or {}).get("TeamNames") or [])
    seat = names.index(a.team) if a.team in names else 0
    steps = blob["steps"]

    tours = {}
    for h in range(TPD):
        t = a.day * TPD + h
        if t >= len(steps):
            break
        obs = steps[t][seat].get("observation") or {}
        act = steps[t][seat].get("action") or {}
        pos = units_at(obs, seat)
        acts = [act.get("farmer")] + list(act.get("hands") or [])
        for u, p in enumerate(pos):
            op = (acts[u] or [None])[0] if u < len(acts) else None
            tours.setdefault(u, []).append((h, p, op))

    print(f"day {a.day}, {len(tours)} units, seat {seat}\n")
    for u in sorted(tours):
        row = tours[u]
        line = []
        for h, p, op in row:
            mark = "" if op in ("NORTH", "SOUTH", "EAST", "WEST", "PASS", None) else f"*{op[:4]}"
            line.append(f"{p[0]}{p[1]}{mark}")
        print(f"  unit{u:>2}  " + " ".join(line))
    print()
    # Shape: how far each step is, and whether rows are swept in one direction
    for u in sorted(tours):
        pts = [p for _h, p, _o in tours[u]]
        rows_ = Counter(p[1] for p in pts)
        turns_ = sum(1 for i in range(2, len(pts))
                     if (pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
                     != (pts[i - 1][0] - pts[i - 2][0], pts[i - 1][1] - pts[i - 2][1]))
        span = (min(p[0] for p in pts), max(p[0] for p in pts),
                min(p[1] for p in pts), max(p[1] for p in pts))
        print(f"  unit{u:>2}  rows visited {sorted(rows_)}  direction changes {turns_}  "
              f"bbox x{span[0]}-{span[1]} y{span[2]}-{span[3]}")


if __name__ == "__main__":
    main()
