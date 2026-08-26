"""Day by day from d12, ours against カワシギ: what each side DOES with its turns.

Alex: *"i suspect strongly that we plant more or over plant earlier - i remember seeing d20-29 grid
and it showed we were planting more than kawa - i thought it didnt really matter - i think that is
the reason we cant harvest everything - however check it and see what the other differences more
closely from d12 - d29"*.

The standing-crop gap is settled: **14.0 units on 6.6 tiles for us, 2.2 on 1.5 for him**, and the
planting GEOMETRY is identical (same nearest-neighbour, same clump count, same clump size at 54
games). So the gap is in the ratio of work started to work finished, not in where the work is.

This prints, per day, per side, the mean per seat of:

    PLANT / WATER / HARVEST / FEED / CARE   unit ops, counted from the action stream. A unit op is
                                            emitted once per turn per unit, so these do not
                                            double-count the way a market order would.
    MOVE                                    turns spent walking. The d29 breakdown showed 118 of
                                            264 unit-turns went on moving, so this is the budget
                                            the harvests are competing for.
    PASS                                    turns spent doing nothing.
    crew                                    farmer + hands alive that day.
    tiles                                   owned tiles, so plant rate can be read per tile.
    standing                                units sitting unharvested on crop tiles at day end.

`plant - harvest` per day is the quantity Alex is pointing at: if we open more tiles than we close,
the excess has to end up standing at the bell, and it does not matter how well placed it is.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
KAWA = "カワシギ"
US = "alex chilton"
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")
OPS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "MOVE", "PASS")
FROM_DAY = 12


def seat_days(replay, seat):
    """`{day: {op: count, ...}}` plus crew/tiles/standing per day, for one seat."""
    out = collections.defaultdict(lambda: collections.Counter())
    steps = replay.get("steps") or []
    for t, step in enumerate(steps):
        if seat >= len(step):
            continue
        day = t // TPD
        if day < FROM_DAY:
            continue
        act = (step[seat] or {}).get("action") or {}
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        row = out[day]
        for op in ops:
            if not op:
                continue
            name = op[0] if isinstance(op, (list, tuple)) else str(op)
            row[name] += 1
        # crew/tiles are read off the observation at the LAST turn of the day
        if t % TPD == TPD - 1:
            obs = (step[0] or {}).get("observation") or {}
            farms = obs.get("farms") or []
            if seat < len(farms):
                f = farms[seat]
                row["crew"] = 1 + len(f.get("hands") or [])
                tiles = f.get("tiles") or []
                owned = standing = 0
                for r in tiles:
                    for tile in r:
                        if not isinstance(tile, dict):
                            continue
                        if tile.get("owned", True):
                            owned += 1
                        if tile.get("crop"):
                            standing += int(tile.get("yield_units", 0) or 0)
                row["tiles"] = owned
                row["standing"] = standing
    return out


def collect(paths_and_seats):
    """Mean per seat, per day, of every counter."""
    acc = collections.defaultdict(lambda: collections.defaultdict(list))
    n = 0
    for replay, seat in paths_and_seats:
        n += 1
        for day, row in seat_days(replay, seat).items():
            for k, v in row.items():
                acc[day][k].append(v)
    return acc, n


def table(label, acc, n):
    print(f"=== {label}   ({n} seats)")
    cols = list(OPS) + ["crew", "tiles", "standing"]
    print("   day " + "".join(f"{c:>9}" for c in cols) + f"{'plant-harv':>12}")
    tot = collections.Counter()
    for day in sorted(acc):
        row = acc[day]
        def m(k):
            v = row.get(k) or [0]
            return sum(v) / len(v)
        line = f"   {day:>3} " + "".join(f"{m(c):>9.1f}" for c in cols)
        print(line + f"{m('PLANT') - m('HARVEST'):>12.1f}")
        for c in cols:
            tot[c] += m(c)
    print("   SUM " + "".join(f"{tot[c]:>9.1f}" if c in OPS else f"{'':>9}" for c in cols)
          + f"{tot['PLANT'] - tot['HARVEST']:>12.1f}")
    print()
    return tot


def main(our_files):
    kawa = []
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json")):
            try:
                r = json.loads(f.read_text())
            except Exception:                                             # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA in names:
                kawa.append((r, names.index(KAWA)))
    ours = []
    for path in our_files:
        r = json.loads(pathlib.Path(path).read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        ours.append((r, names.index(US) if US in names else 0))

    ka, kn = collect(kawa)
    ta = table("KAWASHIGI", ka, kn)
    oa, on = collect(ours)
    to = table("OURS", oa, on)

    print("=== d12-d29 totals, ours minus his (per seat)")
    for c in list(OPS) + ["standing"]:
        if c == "standing":
            continue
        print(f"   {c:<10}{to[c]:>9.1f}{ta[c]:>9.1f}{to[c]-ta[c]:>+9.1f}")
    print(f"   {'plant-harv':<10}{to['PLANT']-to['HARVEST']:>9.1f}"
          f"{ta['PLANT']-ta['HARVEST']:>9.1f}"
          f"{(to['PLANT']-to['HARVEST'])-(ta['PLANT']-ta['HARVEST']):>+9.1f}")


if __name__ == "__main__":
    main(sys.argv[1:])
