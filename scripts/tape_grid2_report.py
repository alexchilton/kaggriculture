"""Choose a world -> tape map from tape_grid2.csv, and keep only picks that survive.

Every tape played the same (seed, seat) cells in a world, so best-minus-default is
paired cell by cell. A pick needs BOTH a mean gain and a majority of cells, because
one cell can swing $30k and carry a mean on its own.
"""
import argparse, csv, json, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_WIN_RATE = 0.70
MIN_GAIN = 2000.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(ROOT/"data/logs/tape_grid2.csv"))
    ap.add_argument("--min-win-rate", type=float, default=MIN_WIN_RATE)
    ap.add_argument("--min-gain", type=float, default=MIN_GAIN)
    args = ap.parse_args()

    rows = list(csv.DictReader(Path(args.csv).open()))
    bad = [r for r in rows if r["world"] != r["world_seen"]]
    err = [r for r in rows if not r["status"].startswith("DONE")]
    print(f"{len(rows)} games, {len(err)} errors, {len(bad)} with world != world_seen")

    slots = json.loads((ROOT/"submission"/"hay_pick"/"slots.json").read_text())
    name_of = {v: k for k, v in slots.items()}
    his = json.loads((ROOT/"submission"/"hay_library"/"index.json").read_text())

    cells = defaultdict(lambda: defaultdict(dict))      # world -> cell -> tape -> margin
    for r in rows:
        cells[r["world"]][(int(r["seed"]), int(r["seat"]))][int(r["tape"])] = float(r["margin"])

    print(f"\n{'world':30} {'cells':>5} {'best':>4} {'gain':>9} {'wins':>7} "
          f"{'his':>4} {'his gain':>9}  verdict")
    picks, kept_gain = {}, []
    for world in sorted(cells):
        cs = cells[world]
        full = {c: v for c, v in cs.items() if len(v) == 13}
        if not full:
            print(f"{world:30} {len(cs):>5}    -         -       -     -         -  no complete cell")
            continue
        mean = {t: statistics.mean(v[t] for v in full.values()) for t in range(13)}
        best = max(mean, key=mean.get)
        gains = [v[best]-v[0] for v in full.values()]
        wins = sum(1 for g in gains if g > 0)
        gain = mean[best]-mean[0]
        hslot = slots.get(his.get(world)) if his.get(world) else None
        hg = (mean[hslot]-mean[0]) if hslot is not None else None
        ok = best != 0 and wins/len(gains) >= args.min_win_rate and gain >= args.min_gain
        if ok:
            picks[world] = best
            kept_gain.append(gain)
        print(f"{world:30} {len(full):>5} {best:>4} {gain:>+9,.0f} {wins:>3}/{len(gains):<3} "
              f"{('-' if hslot is None else hslot):>4} "
              f"{('        -' if hg is None else f'{hg:+9,.0f}')}  {'KEEP' if ok else 'default'}")

    print(f"\n{len(picks)} of {len(cells)} worlds get a measured route")
    if kept_gain:
        print(f"mean gain in kept worlds {statistics.mean(kept_gain):+,.0f}, "
              f"expected over all worlds {sum(kept_gain)/len(cells):+,.0f} per game")
    agree = sum(1 for w, t in picks.items() if his.get(w) == name_of[t])
    print(f"agrees with Hayashi's own tape in {agree}/{len(picks)} kept worlds")

    out = ROOT/"data/logs/tape_grid2_picks.json"
    out.write_text(json.dumps({w: name_of[t] for w, t in picks.items()}, indent=2, sort_keys=True))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
