"""SpaTaro's days as (board at dawn -> 24 turns), for splicing when the board matches.

His blocks cannot be selected by a tree: 44 distinct blocks in 44 games on every one of
the 30 days, so `fit_day_classifier` returns +0.0% over the majority baseline everywhere
and `export_block_agent` would ship no days at all.

So selection is by BOARD MATCH instead. Splice his day when our board is one he has
actually played; fall back to the planner when it is not. This script builds the library
and measures the only thing that decides whether that is viable: leave one season out,
and ask how close the nearest OTHER season's board is.

Distance is L1 over the structural columns -- what is standing in the ground, what is in
the herd, what is in hand -- normalised per column by its spread across his seasons, so
a 40-tile crop count and a 2-animal count are not compared on the same scale.
"""
import argparse, json, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROWS = ROOT / "data/logs/day_rows_spataro.json"
BLOCKS = ROOT / "data/logs/day_rows_spataro.blocks.json"
OUT = ROOT / "data/spataro_blocks.json"

# The columns that say what the board IS. Market prices and opponent state are excluded:
# a block is replayable or not because of our own farm, not because of the book.
STRUCT = ["my_crop_WHEAT", "my_crop_CARROT", "my_crop_TOMATO", "my_crop_STRAWBERRY",
          "my_crop_MELON", "my_animal_COW", "my_animal_SHEEP", "my_animal_GOOSE",
          "my_empty", "my_hands", "my_quadrants", "my_weeds", "my_thirsty",
          "my_seed_WHEAT", "my_seed_MELON", "my_seed_STRAWBERRY", "my_seed_CARROT",
          "my_shed_WHEAT", "my_shed_FERTILIZER"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--thresholds", type=float, nargs="*", default=[0.5, 1.0, 2.0, 4.0])
    args = ap.parse_args()

    rows = json.loads(ROWS.read_text())
    blocks = json.loads(BLOCKS.read_text())
    cols = [c for c in STRUCT if any(c in r["x"] for r in rows)]
    missing = [c for c in STRUCT if c not in cols]
    if missing:
        print(f"columns absent from the rows, dropped: {missing}")

    # per-column scale, so counts on different scales are comparable
    scale = {}
    for c in cols:
        v = [r["x"].get(c, 0) for r in rows]
        s = statistics.pstdev(v)
        scale[c] = s if s > 1e-9 else 1.0

    by_day = defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r)

    lib = {}
    print(f"\n{len(rows)} rows, {len(cols)} structural columns, "
          f"{len(by_day)} days, {len({(r['game'], r['seat']) for r in rows})} game-seats")
    print(f"\n{'day':>3} {'n':>3} {'nearest-neighbour distance':>30}   coverage at threshold")
    print(f"{'':>3} {'':>3} {'min   p25   p50   p75   max':>30}   " +
          "  ".join(f"{t:>5}" for t in args.thresholds))
    cover = defaultdict(list)
    for day in sorted(by_day):
        rs = by_day[day]
        dists = []
        for i, a in enumerate(rs):
            best = None
            for j, b in enumerate(rs):
                if i == j:
                    continue
                d = sum(abs(a["x"].get(c, 0) - b["x"].get(c, 0)) / scale[c] for c in cols) / len(cols)
                best = d if best is None or d < best else best
            if best is not None:
                dists.append(best)
        if not dists:
            continue
        dists.sort()
        q = lambda f: dists[min(len(dists) - 1, int(f * len(dists)))]
        cells = []
        for t in args.thresholds:
            frac = sum(1 for d in dists if d <= t) / len(dists)
            cover[t].append(frac)
            cells.append(f"{100*frac:>4.0f}%")
        print(f"{day:>3} {len(rs):>3} {dists[0]:>5.2f} {q(.25):>5.2f} {q(.5):>5.2f} "
              f"{q(.75):>5.2f} {dists[-1]:>5.2f}   " + "  ".join(cells))
        lib[str(day)] = [{"x": {c: r["x"].get(c, 0) for c in cols},
                          "block": blocks[str(day)][r["block"]]}
                         for r in rs if r["block"] in blocks.get(str(day), {})]

    print("\nmean coverage over all 30 days:")
    for t in args.thresholds:
        print(f"  threshold {t:>4}: {100*statistics.mean(cover[t]):>5.1f}% of days have a match")
    OUT.write_text(json.dumps({"columns": cols, "scale": scale, "days": lib}))
    n = sum(len(v) for v in lib.values())
    print(f"\nwrote {OUT}  ({n} day-blocks with board signatures)")


if __name__ == "__main__":
    main()
