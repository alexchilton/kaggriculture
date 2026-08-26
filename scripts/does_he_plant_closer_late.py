"""Does カワシギ plant his LATE crops closer to the shed than we do?

Alex: *"we leave them because its on the edge and too far away to harvest ... my q is whether he
plants more strategically"*.

The shed sits in the middle of the board -- its access tiles are (4,4), (5,4), (4,5), (5,5) on a
10x10 (`routines.shed_access_tiles`). So "on the edge" is literally distance from the centre, and a
late planting's distance decides whether a unit can get to it, work it, and still bank the produce.

Measured per PLANT op, which is a unit op emitted once and carries the tile it lands on via the
acting unit's position. Distance is Chebyshev (a step may be diagonal) to the nearest shed-access
tile, which is the number of moves to carry a harvest home.

Printed per side: mean distance of plantings by day, so a strategy that pulls inward late shows as
a falling curve. For our own games it additionally splits the late plantings by whether the tile was
still holding produce at the bell -- the abandoned ones should be the far ones if Alex is right.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
SHED = [(4, 4), (5, 4), (4, 5), (5, 5)]
KAWA = "カワシギ"
US = "alex chilton"
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")


def dist(y, x):
    return min(max(abs(y - sy), abs(x - sx)) for sy, sx in SHED)


def _unit_positions(obs, seat):
    """`[(y, x)]` for the farmer then each hand, in the order the action list uses.

    **Read off a real replay, not guessed.** A unit's position is a bare `[y, x]` list on the farm
    -- `farmer: [6, 3]`, `hands: [[4, 3], ...]` -- not a dict with a `position` key. The first cut
    of this assumed the dict form, found nothing, and printed an empty table for both sides.
    """
    farms = (obs or {}).get("farms") or []
    if seat >= len(farms):
        return []
    f = farms[seat]
    out = [tuple(f["farmer"]) if f.get("farmer") else None]
    for h in (f.get("hands") or []):
        out.append(tuple(h) if h else None)
    return out


def plantings(replay, seat):
    """`[(day, y, x, crop)]` for every PLANT this seat emitted."""
    out = []
    for t, step in enumerate(replay.get("steps") or []):
        if seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        obs = (step[0] or {}).get("observation") or {}
        pos = _unit_positions(obs, seat)
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        for i, op in enumerate(ops):
            if op and op[0] == "PLANT" and len(op) >= 2 and i < len(pos) and pos[i]:
                y, x = pos[i]
                out.append((t // TPD, y, x, op[1]))
    return out


def curve(rows, label):
    by = collections.defaultdict(list)
    for day, y, x, _c in rows:
        by[day].append(dist(y, x))
    print(f"  {label}")
    print(f"    {'day':>5}{'plants':>8}{'mean dist':>11}")
    for day in sorted(by):
        v = by[day]
        print(f"    {day:>5}{len(v):>8}{sum(v)/len(v):>11.2f}")
    late = [dist(y, x) for day, y, x, _c in rows if day >= 20]
    early = [dist(y, x) for day, y, x, _c in rows if day < 20]
    if early and late:
        print(f"    early (d<20) mean {sum(early)/len(early):.2f} over {len(early)}   "
              f"LATE (d>=20) mean {sum(late)/len(late):.2f} over {len(late)}")
    print()


def main(our_files):
    # --- kawa, from the recorded tapes
    rows, seats = [], 0
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json"))[:40]:
            try:
                r = json.loads(f.read_text())
            except Exception:  # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA not in names:
                continue
            seats += 1
            rows.extend(plantings(r, names.index(KAWA)))
    if rows:
        print(f"KAWASHIGI  ({seats} seats)")
        curve(rows, "all plantings")

    # --- us, from the downloaded ladder games
    for path in our_files:
        f = pathlib.Path(path)
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        seat = names.index(US) if US in names else 0
        rows = plantings(r, seat)
        print(f"OURS  {f.stem}")
        curve(rows, "all plantings")
        last = (r["steps"][-1][0] or {}).get("observation") or {}
        tiles = (last.get("farms") or [])[seat].get("tiles")
        left = {(y, x) for y, row in enumerate(tiles) for x, t in enumerate(row)
                if isinstance(t, dict) and t.get("crop") and t.get("yield_units", 0) > 0}
        lt = [(dist(y, x), (y, x) in left) for day, y, x, _c in rows if day >= 20]
        if lt:
            ab = [d for d, was_left in lt if was_left]
            ok = [d for d, was_left in lt if not was_left]
            print(f"    late plantings: {len(lt)}   "
                  f"ABANDONED {len(ab)} mean dist {sum(ab)/len(ab):.2f}" if ab else
                  f"    late plantings: {len(lt)}   ABANDONED 0")
            if ok:
                print(f"    {'':<18}collected {len(ok)} mean dist {sum(ok)/len(ok):.2f}")
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
