"""WHERE he puts things, over 179 seasons -- and whether the where depends on the world.

The amounts are covered: `scripts/spa_targets.py` predicts his d3-8 board to within 0.3 of an
animal and 1.6 tiles from the shop set alone. So the only thing a BRANCH TAPE could still carry
that an algorithm cannot is geometry -- which tile, in which order. If the geometry is invariant
across branches, one tape serves every branch and the species comes from the algorithm; if it
splits by branch, the branch tapes are real.

Reads tile COORDINATES out of the replays, which the count-based extractors deliberately threw
away.
"""
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEASON, TPD = 30, 24
ANIMALS = ("COW", "SHEEP", "GOOSE")
STRUCTS = ("PASTURE", "COOP")
TEAM = "SpaTaro"


def events(steps, seat):
    """[(day, x, y, kind, what)] for every placement, build and plant, from the board changing."""
    out, prev = [], None
    for i, s in enumerate(steps):
        obs = s[seat].get("observation") or {}
        farms = obs.get("farms") or []
        if len(farms) <= seat:
            continue
        cur = farms[seat].get("tiles") or []
        day = min(i // TPD, SEASON - 1)
        if prev is not None:
            for y, row in enumerate(cur):
                for x, t in enumerate(row):
                    o = prev[y][x] if y < len(prev) and x < len(prev[y]) else None
                    if t == "LOCKED" or o == "LOCKED":
                        continue
                    od, td = (o if isinstance(o, dict) else None), (t if isinstance(t, dict) else None)
                    if td and td.get("kind") in STRUCTS and not (od and od.get("kind") in STRUCTS):
                        out.append((day, x, y, "BUILD", td["kind"]))
                    if td and "animal" in td and not (od and "animal" in od):
                        out.append((day, x, y, "PLACE", td["animal"]))
                    oc, tc = (od or {}).get("crop"), (td or {}).get("crop")
                    if tc and tc != "WEED" and tc != oc:
                        out.append((day, x, y, "PLANT", tc))
        prev = cur
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+",
                    default=["data/replays_spa_sub", "data/replays_2026-09-07",
                             "data/replays_2026-09-08", "data/replays_2026-09-09"])
    ap.add_argument("--ids", default="/tmp/spa_new_ids.txt")
    ap.add_argument("--out", default="data/spataro_geometry.json")
    args = ap.parse_args()

    allow = None
    p = Path(args.ids)
    if p.exists():
        allow = {int(x) for x in p.read_text().split()}

    flows = {p["ep"]: p["unlocks"]
             for p in json.loads((ROOT / "data/spataro_plan_rows.json").read_text())}

    seasons, seen = [], set()
    for d in args.dirs:
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
            if ep in seen or (allow is not None and ep not in allow):
                continue
            r = json.loads(f.read_text())
            names = (r.get("info") or {}).get("TeamNames") or []
            if TEAM not in names:
                continue
            seen.add(ep)
            seat = names.index(TEAM)
            seasons.append({"ep": ep, "bank": r["rewards"][seat],
                            "unlocks": flows.get(ep) or [],
                            "events": events(r["steps"], seat)})
            if len(seasons) % 25 == 0:
                print(f"  {len(seasons)} seasons", flush=True)

    n = len(seasons)
    print(f"\n{n} seasons\n", flush=True)
    (ROOT / args.out).write_text(json.dumps(seasons, separators=(",", ":")))

    print("--- WHERE the animals go, cumulative through each day (tile set, species ignored)")
    print(f"{'thru day':>9} {'distinct tile sets':>19} {'top':>5} {'cover':>6}  top set")
    for upto in (1, 3, 5, 6, 9, 12):
        c = Counter(tuple(sorted({(x, y) for d, x, y, k, w in s["events"]
                                  if k == "PLACE" and d < upto})) for s in seasons)
        t, cnt = c.most_common(1)[0]
        print(f"{upto:>9} {len(c):>19} {cnt:>5} {100 * cnt / n:>5.0f}%  "
              f"{' '.join(f'{x},{y}' for x, y in t)}")

    print("\n--- and the same tile set WITH species")
    print(f"{'thru day':>9} {'distinct':>9} {'top':>5} {'cover':>6}  top")
    for upto in (1, 3, 5, 6, 9):
        c = Counter(tuple(sorted({(x, y, w) for d, x, y, k, w in s["events"]
                                  if k == "PLACE" and d < upto})) for s in seasons)
        t, cnt = c.most_common(1)[0]
        print(f"{upto:>9} {len(c):>9} {cnt:>5} {100 * cnt / n:>5.0f}%  "
              f"{' '.join(f'{x},{y}:{w[0]}' for x, y, w in t)}")

    print("\n--- does the PLACE geometry through d5 depend on the first shop?")
    by = defaultdict(Counter)
    for s in seasons:
        first = next((sh for dd, sh in sorted(s["unlocks"]) if dd <= 3), None)
        tiles = tuple(sorted({(x, y) for d, x, y, k, w in s["events"] if k == "PLACE" and d < 6}))
        by[first][tiles] += 1
    print(f"{'first shop':16} {'n':>4} {'distinct':>9} {'top':>5} {'cover':>6}")
    for shop, c in sorted(by.items(), key=lambda kv: -sum(kv[1].values())):
        tot = sum(c.values())
        print(f"{str(shop):16} {tot:>4} {len(c):>9} {c.most_common(1)[0][1]:>5} "
              f"{100 * c.most_common(1)[0][1] / tot:>5.0f}%")

    print("\n--- the d0 build set (pens before any shop)")
    c = Counter(tuple(sorted({(x, y) for d, x, y, k, w in s["events"] if k == "BUILD" and d < 1}))
                for s in seasons)
    for t, cnt in c.most_common(4):
        print(f"    {cnt:>4} ({100 * cnt / n:>3.0f}%)  {' '.join(f'{x},{y}' for x, y in t)}")


if __name__ == "__main__":
    main()
