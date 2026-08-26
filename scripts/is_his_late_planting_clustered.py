"""Does カワシギ place his LATE plantings so one trip can sweep them, and does he collect them?

Alex: *"look at the late planting of kawa in terms of geometry - where does he plant so he is able
to later get it - it could also be he is planning this from way before"*.

An earlier cut measured mean distance from the shed and found no difference (his 3.23 early vs 3.25
late, ours 3.27 vs 3.41). **That was the wrong geometry.** Radius does not decide whether a tile can
be collected; what decides it is whether the tile sits near OTHER work, so one walk out serves
several stops and the walk home is amortised. On d29 of our own game, 118 of 264 unit-turns went on
moving and every unit finished at the shed with two turns spare -- the day was full of walking, not
idle.

So this measures spread rather than radius:

    nearest-neighbour   for each late planting, the distance to the closest OTHER late planting.
                        Small means clustered; a lone tile four steps out is what gets abandoned.
    clumps              late plantings grouped by single-linkage at distance 1 (touching tiles),
                        and the size of those groups.
    left standing       units still on crop tiles at the bell -- the outcome that matters. If he
                        clusters and we scatter, he should be leaving near zero and we should not.
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
#: All five post-balance-change dirs. The first cut scanned three and sliced 25 files from each,
#: which matched only 3 seats of him -- enough to be worth chasing, not enough to build on.
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")
FILES_PER_DIR = 300
LATE_FROM = 20


def _positions(obs, seat):
    farms = (obs or {}).get("farms") or []
    if seat >= len(farms):
        return []
    f = farms[seat]
    return [tuple(f["farmer"]) if f.get("farmer") else None] + \
           [tuple(h) if h else None for h in (f.get("hands") or [])]


def late_plantings(replay, seat):
    out = []
    for t, step in enumerate(replay.get("steps") or []):
        if seat >= len(step):
            continue
        day = t // TPD
        if day < LATE_FROM:
            continue
        act = (step[seat] or {}).get("action") or {}
        pos = _positions((step[0] or {}).get("observation") or {}, seat)
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        for i, op in enumerate(ops):
            if op and op[0] == "PLANT" and i < len(pos) and pos[i]:
                out.append(pos[i])
    return out


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def stats(tiles):
    """(mean nearest-neighbour distance, number of clumps, mean clump size)."""
    uniq = sorted(set(tiles))
    if len(uniq) < 2:
        return float("nan"), len(uniq), float(len(uniq))
    nn = [min(cheb(a, b) for b in uniq if b != a) for a in uniq]
    # single-linkage at distance 1
    seen, clumps = set(), []
    for a in uniq:
        if a in seen:
            continue
        stack, group = [a], []
        while stack:
            c = stack.pop()
            if c in seen:
                continue
            seen.add(c); group.append(c)
            stack.extend(b for b in uniq if b not in seen and cheb(b, c) <= 1)
        clumps.append(group)
    return sum(nn) / len(nn), len(clumps), sum(len(g) for g in clumps) / len(clumps)


def standing(replay, seat):
    last = (replay["steps"][-1][0] or {}).get("observation") or {}
    farms = last.get("farms") or []
    if seat >= len(farms):
        return 0, 0
    units = tiles = 0
    for row in (farms[seat].get("tiles") or []):
        for t in row:
            if isinstance(t, dict) and t.get("crop"):
                u = int(t.get("yield_units", 0) or 0)
                if u:
                    units += u; tiles += 1
    return units, tiles


def report(label, rows):
    if not rows:
        print(f"{label}: no data"); return
    nn = [r[0] for r in rows if r[0] == r[0]]
    print(f"{label}  ({len(rows)} seats)")
    print(f"   late plantings/seat   {sum(r[3] for r in rows)/len(rows):>6.1f}")
    print(f"   nearest-neighbour     {sum(nn)/len(nn):>6.2f}   (lower = clustered)")
    print(f"   clumps/seat           {sum(r[1] for r in rows)/len(rows):>6.1f}")
    print(f"   mean clump size       {sum(r[2] for r in rows)/len(rows):>6.2f}")
    print(f"   LEFT STANDING at bell {sum(r[4] for r in rows)/len(rows):>6.1f} units "
          f"on {sum(r[5] for r in rows)/len(rows):.1f} tiles")
    print()


def main(our_files):
    rows = []
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json"))[:FILES_PER_DIR]:
            try:
                r = json.loads(f.read_text())
            except Exception:  # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA not in names:
                continue
            seat = names.index(KAWA)
            lp = late_plantings(r, seat)
            nn, nc, cs = stats(lp)
            u, t = standing(r, seat)
            rows.append((nn, nc, cs, len(lp), u, t))
    report("KAWASHIGI", rows)

    rows = []
    for path in our_files:
        r = json.loads(pathlib.Path(path).read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        seat = names.index(US) if US in names else 0
        lp = late_plantings(r, seat)
        nn, nc, cs = stats(lp)
        u, t = standing(r, seat)
        rows.append((nn, nc, cs, len(lp), u, t))
    report("OURS", rows)


if __name__ == "__main__":
    main(sys.argv[1:])
