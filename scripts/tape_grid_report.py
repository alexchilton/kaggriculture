"""Read data/logs/tape_grid.csv and choose a world -> tape map that survives a test.

Selection is paired: every tape played the same (seed, opponent, seat) cells in a
world, so best-minus-default is computed cell by cell. A pick is kept only when it
beats the default in most cells, not only on the mean -- one cell with a $25k swing
can carry a mean on its own.
"""
import csv, json, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_CELLS = 6          # below this the world has 1 seed and cannot be judged
MIN_WIN_RATE = 0.70
MIN_GAIN = 2000.0


def main():
    rows = list(csv.DictReader((ROOT/"data/logs/tape_grid.csv").open()))
    for r in rows:
        r["tape"] = int(r["tape"]); r["margin"] = float(r["margin"])
    slots = {v: k for k, v in json.loads(
        (ROOT/"submission"/"hay_pick"/"slots.json").read_text()).items()}
    lib_index = json.loads((ROOT/"submission"/"hay_library"/"index.json").read_text())
    name2slot = json.loads((ROOT/"submission"/"hay_pick"/"slots.json").read_text())

    cell = defaultdict(dict)                       # world -> cell -> tape -> margin
    for r in rows:
        cell[r["world"]].setdefault((r["seed"], r["opponent"], r["seat"]), {})[r["tape"]] = r["margin"]

    print(f"{len(cell)} worlds drawn over 48 seeds, {len(rows)} games\n")
    print(f"{'world':30} {'cells':>5} {'seeds':>5} {'best':>4} {'mean gain':>10} "
          f"{'wins':>7} {'his':>4} {'his gain':>9}  verdict")
    picks, total_gain = {}, []
    for world in sorted(cell, key=lambda w: -len(cell[w])):
        cells = cell[world]
        tapes = sorted({t for v in cells.values() for t in v})
        mean = {t: statistics.mean(v[t] for v in cells.values() if t in v) for t in tapes}
        best = max(mean, key=mean.get)
        gains = [v[best]-v[0] for v in cells.values() if best in v and 0 in v]
        wins = sum(1 for g in gains if g > 0)
        his_name = lib_index.get(world)
        his = name2slot.get(his_name) if his_name else None
        his_gain = (mean[his]-mean[0]) if his in mean else None
        ok = (len(cells) >= MIN_CELLS and gains
              and wins/len(gains) >= MIN_WIN_RATE and mean[best]-mean[0] >= MIN_GAIN)
        if ok and best != 0:
            picks[world] = best
            total_gain.append(mean[best]-mean[0])
        print(f"{world:30} {len(cells):>5} {len({c[0] for c in cells}):>5} {best:>4} "
              f"{mean[best]-mean[0]:>+10,.0f} {wins:>3}/{len(gains):<3} "
              f"{('-' if his is None else his):>4} "
              f"{('      -' if his_gain is None else f'{his_gain:+9,.0f}')} "
              f" {'KEEP' if ok and best != 0 else 'default'}")

    print(f"\n{len(picks)} worlds get a measured route, "
          f"mean gain in those worlds {statistics.mean(total_gain) if total_gain else 0:+,.0f}")
    out = ROOT/"data/logs/tape_grid_picks.json"
    out.write_text(json.dumps({w: slots[t] for w, t in picks.items()}, indent=2, sort_keys=True))
    print(f"wrote {out}")

    agree = sum(1 for w, t in picks.items() if lib_index.get(w) == slots[t])
    print(f"\nagrees with Hayashi's own choice in {agree}/{len(picks)} of those worlds")


if __name__ == "__main__":
    main()
