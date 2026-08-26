"""How many units does each HARVEST actually collect, ours against カワシギ?

The one gap that survived every other test today. Measured over d12-d29, per seat:

    PLANT     112.0 ours   115.8 his      equal
    HARVEST   348.5 ours   358.5 his      ten ops
    standing at the bell   14.0 units on 6.6 tiles ours   2.2 on 1.5 his

Equal plantings and near-equal harvest OPS cannot produce a 6x difference in what is left on the
field unless the harvests differ in SIZE. A HARVEST collects whatever the tile holds
(`reference/kaggriculture.py:409`), so taking a tile at 1 unit and taking it at 4 are the same op
and the same turn.

For every HARVEST op, this reads `yield_units` on the acting unit's tile at that turn -- what the
harvest actually banked -- and buckets it. Also counts, at the bell, tiles that were planted and
NEVER harvested at all, which is the other way the same gap could arise.

**Unit positions in a replay are bare `[y, x]` lists** (`farmer: [6, 3]`), not dicts with a
`position` key, and `build_nodes` stores `(x, y)`. Kept in `(y, x)` here throughout since everything
is read off the replay board directly.
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
FROM_DAY = 12


def harvests(replay, seat):
    """`[(day, units, crop)]` for every HARVEST this seat emitted from FROM_DAY."""
    out = []
    for t, step in enumerate(replay.get("steps") or []):
        day = t // TPD
        if day < FROM_DAY or seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        obs = (step[0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        if seat >= len(farms):
            continue
        f = farms[seat]
        tiles = f.get("tiles") or []
        pos = [f.get("farmer")] + list(f.get("hands") or [])
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        for i, op in enumerate(ops):
            if not (op and op[0] == "HARVEST") or i >= len(pos) or not pos[i]:
                continue
            y, x = pos[i]
            if y < len(tiles) and x < len(tiles[y]) and isinstance(tiles[y][x], dict):
                cell = tiles[y][x]
                out.append((day, int(cell.get("yield_units", 0) or 0), cell.get("crop")))
    return out


def standing(replay, seat):
    last = (replay["steps"][-1][0] or {}).get("observation") or {}
    farms = last.get("farms") or []
    if seat >= len(farms):
        return 0, 0
    u = t = 0
    for row in (farms[seat].get("tiles") or []):
        for c in row:
            if isinstance(c, dict) and c.get("crop"):
                n = int(c.get("yield_units", 0) or 0)
                if n:
                    u += n
                    t += 1
    return u, t


def report(label, pairs):
    if not pairs:
        print(f"{label}: no seats"); return
    n = len(pairs)
    sizes = collections.Counter()
    tot_ops = tot_units = 0
    su = st = 0
    by_crop = collections.defaultdict(lambda: [0, 0])
    for replay, seat in pairs:
        for _day, units, crop in harvests(replay, seat):
            sizes[min(units, 6)] += 1
            tot_ops += 1
            tot_units += units
            by_crop[crop][0] += 1
            by_crop[crop][1] += units
        u, t = standing(replay, seat)
        su += u
        st += t
    print(f"{label}   ({n} seats)")
    print(f"   HARVEST ops/seat   {tot_ops/n:>7.1f}")
    print(f"   units taken/seat   {tot_units/n:>7.1f}")
    print(f"   units per harvest  {tot_units/max(1,tot_ops):>7.2f}")
    print(f"   left standing      {su/n:>7.1f} units on {st/n:.1f} tiles")
    print(f"   {'units':>7}{'share of harvests':>20}")
    for k in sorted(sizes):
        lbl = f"{k}+" if k == 6 else str(k)
        print(f"   {lbl:>7}{100*sizes[k]/max(1,tot_ops):>19.1f}%")
    print(f"   {'crop':<12}{'ops/seat':>10}{'units/op':>10}")
    for crop, (o, u) in sorted(by_crop.items(), key=lambda kv: -kv[1][0]):
        if crop:
            print(f"   {crop:<12}{o/n:>10.1f}{u/max(1,o):>10.2f}")
    print()


def main(our_files):
    kawa = []
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json"))[:60]:
            try:
                r = json.loads(f.read_text())
            except Exception:                                             # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA in names:
                kawa.append((r, names.index(KAWA)))
    ours = []
    for path in our_files:
        f = pathlib.Path(path)
        if f.name.startswith("_"):
            continue
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        ours.append((r, names.index(US) if US in names else 0))
    report("KAWASHIGI", kawa)
    report("OURS", ours)


if __name__ == "__main__":
    main(sys.argv[1:])
