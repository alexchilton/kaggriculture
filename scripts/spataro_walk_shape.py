"""His WALK SHAPE, read off the tape across the whole corpus -- not one day, not one season.

`spataro_tours.py` prints one day of one replay by hand. This scans every SpaTaro replay on disk,
every day, every unit, and classifies the LOCAL sweep each unit's tour is built from: row-major
(a serpentine.py-style boustrophedon by row) vs column-major (by column) vs neither (nearest-
neighbour / unstructured), whether direction alternates run-to-run (true boustrophedon) or resets
(scanline with carriage return), and which axis is the LONG axis of the unit's own bounding box --
so the question "row or column" can be answered against the shape actually swept, not assumed.

Unlike `spataro_geometry.py` (board EVENTS -- build/place/plant, from what changed) this reads
POSITION, every hour, the same signal `spataro_tours.py` prints for one day.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TPD = 24
TEAM = "SpaTaro"
WORK_OPS = ("PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER",
            "DIG", "BUILD_COOP", "BUILD_PASTURE", "PLACE", "PICKUP", "DROP")


def units_at(obs, seat):
    farm = (obs.get("farms") or [])[seat]
    out = [tuple(farm.get("farmer") or (0, 0))]
    for h in (farm.get("hands") or []):
        out.append(tuple(h))
    return out


def unit_day_track(steps, seat, day):
    """[(hour, (x,y), op)] for one unit's whole day -- reused per unit below."""
    tracks = {}
    for h in range(TPD):
        t = day * TPD + h
        if t >= len(steps):
            break
        obs = steps[t][seat].get("observation") or {}
        act = steps[t][seat].get("action") or {}
        pos = units_at(obs, seat)
        acts = [act.get("farmer")] + list(act.get("hands") or [])
        for u, p in enumerate(pos):
            op = (acts[u] or [None])[0] if u < len(acts) else None
            tracks.setdefault(u, []).append((h, p, op))
    return tracks


def runs_of(pts):
    """Collapse a point sequence into maximal straight RUNS along a fixed axis.

    A run is a maximal stretch where one coordinate is constant and the other is monotonic (in
    either direction) -- a single "pass" of a row or a column. Consecutive duplicate points (a
    unit standing still to work a tile) collapse to one point first, so dwell time never fakes a
    run boundary.
    """
    dedup = []
    for p in pts:
        if not dedup or dedup[-1] != p:
            dedup.append(p)
    if len(dedup) < 2:
        return []
    out, cur, axis, direction = [], [dedup[0]], None, None
    for p in dedup[1:]:
        dx, dy = p[0] - cur[-1][0], p[1] - cur[-1][1]
        if dx != 0 and dy != 0:
            # a diagonal jump (teleport / non-adjacent step) -- close the run
            if len(cur) >= 2:
                out.append((axis, direction, list(cur)))
            cur, axis, direction = [p], None, None
            continue
        this_axis = "x" if dx != 0 else ("y" if dy != 0 else axis)
        this_dir = (1 if dx > 0 else -1) if dx != 0 else ((1 if dy > 0 else -1) if dy != 0 else direction)
        if axis is None:
            axis, direction = this_axis, this_dir
            cur.append(p)
        elif this_axis == axis and (this_dir == direction or dx == 0 and dy == 0):
            cur.append(p)
        else:
            if len(cur) >= 2:
                out.append((axis, direction, list(cur)))
            cur, axis, direction = [cur[-1], p], this_axis, this_dir
    if len(cur) >= 2 and axis is not None:
        out.append((axis, direction, list(cur)))
    return out


def classify_unit_day(pts):
    """One unit's one day: bbox, long axis, run axis histogram, alternation, run count."""
    if len(pts) < 3:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    bbox = (min(xs), max(xs), min(ys), max(ys))
    w, ht = bbox[1] - bbox[0] + 1, bbox[3] - bbox[2] + 1
    rr = runs_of(pts)
    axis_counts = Counter(a for a, _d, _pts in rr if a)
    # alternation: for consecutive runs on the SAME axis, does direction flip (boustrophedon) or
    # repeat (scanline / carriage return)?
    flips, repeats = 0, 0
    by_axis = [r for r in rr if r[0]]
    for i in range(1, len(by_axis)):
        if by_axis[i][0] == by_axis[i - 1][0]:
            if by_axis[i][1] == by_axis[i - 1][1]:
                repeats += 1
            else:
                flips += 1
    return {
        "bbox": bbox, "w": w, "h": ht, "long_axis": "x" if w >= ht else "y",
        "n_runs": len(rr), "axis_counts": axis_counts,
        "dominant_run_axis": axis_counts.most_common(1)[0][0] if axis_counts else None,
        "flips": flips, "repeats": repeats,
        "tiles": len(set(pts)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+",
                     default=["data/replays_spa_sub", "data/replays_2026-09-07",
                              "data/replays_2026-09-08", "data/replays_2026-09-09"])
    ap.add_argument("--days", nargs="+", type=int, default=list(range(1, 13)))
    ap.add_argument("--max-seasons", type=int, default=0, help="0 = all")
    ap.add_argument("--min-tiles", type=int, default=4,
                     help="skip unit-days with fewer distinct tiles than this -- too short to")
    ap.add_argument("--out", default="/tmp/walk_shape.json")
    a = ap.parse_args()

    seen, files = set(), []
    for d in a.dirs:
        folder = ROOT / d
        if not folder.exists():
            continue
        for f in sorted(folder.glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            try:
                ep = int(f.stem)
            except ValueError:
                continue
            if ep in seen:
                continue
            seen.add(ep)
            files.append(f)
    if a.max_seasons:
        files = files[:a.max_seasons]

    records = []
    n_seasons = 0
    for f in files:
        try:
            blob = json.loads(f.read_text())
        except Exception:
            continue
        names = list((blob.get("info") or {}).get("TeamNames") or [])
        if TEAM not in names:
            continue
        seat = names.index(TEAM)
        steps = blob["steps"]
        n_seasons += 1
        for day in a.days:
            if day * TPD >= len(steps):
                continue
            tracks = unit_day_track(steps, seat, day)
            for u, row in tracks.items():
                pts = [p for _h, p, _op in row]
                work_hours = sum(1 for _h, _p, op in row if op in WORK_OPS)
                cls = classify_unit_day(pts)
                if cls is None or cls["tiles"] < a.min_tiles:
                    continue
                cls.update(ep=int(f.stem), day=day, unit=u, work_hours=work_hours,
                           track=[(h, list(p), op) for h, p, op in row])
                records.append(cls)
        if n_seasons % 25 == 0:
            print(f"  {n_seasons} seasons, {len(records)} unit-days", flush=True)

    print(f"\n{n_seasons} seasons scanned, {len(records)} unit-days kept "
          f"(>= {a.min_tiles} distinct tiles)\n")
    Path(a.out).write_text(json.dumps(records))
    print(f"wrote {a.out}")

    # ---- headline stats ----------------------------------------------------------------------
    print("\n--- long axis of the unit's own bbox vs the axis its RUNS actually sweep")
    agree = sum(1 for r in records if r["dominant_run_axis"] == r["long_axis"])
    disagree = sum(1 for r in records if r["dominant_run_axis"] and r["dominant_run_axis"] != r["long_axis"])
    none_ = sum(1 for r in records if not r["dominant_run_axis"])
    print(f"  runs sweep the LONG axis: {agree}   sweep the SHORT axis: {disagree}   "
          f"no dominant axis: {none_}   (of {len(records)})")

    print("\n--- row-major (y) vs column-major (x) run dominance, overall")
    dom = Counter(r["dominant_run_axis"] for r in records if r["dominant_run_axis"])
    print(f"  {dict(dom)}")

    print("\n--- alternation: does direction FLIP between consecutive same-axis runs "
          "(boustrophedon) or REPEAT (carriage return)?")
    tf, tr = sum(r["flips"] for r in records), sum(r["repeats"] for r in records)
    print(f"  total flips {tf}   total repeats {tr}   "
          f"flip rate {tf/(tf+tr):.2f}" if (tf + tr) else "  no multi-run unit-days")

    print("\n--- shape by DAY (mean bbox tiles, mean n_runs, row/col split)")
    by_day = {}
    for r in records:
        by_day.setdefault(r["day"], []).append(r)
    print(f"{'day':>4} {'n':>5} {'mean_w':>7} {'mean_h':>7} {'mean_tiles':>10} {'mean_runs':>9}  row/col")
    for day in sorted(by_day):
        rs = by_day[day]
        n = len(rs)
        mw = sum(r["w"] for r in rs) / n
        mh = sum(r["h"] for r in rs) / n
        mt = sum(r["tiles"] for r in rs) / n
        mr = sum(r["n_runs"] for r in rs) / n
        rc = Counter(r["dominant_run_axis"] for r in rs if r["dominant_run_axis"])
        print(f"{day:>4} {n:>5} {mw:>7.2f} {mh:>7.2f} {mt:>10.2f} {mr:>9.2f}  {dict(rc)}")


if __name__ == "__main__":
    main()
