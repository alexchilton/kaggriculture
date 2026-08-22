"""Which day should the fourth quadrant be bought? Scored on WIN RATE, not bank.

    .venv/bin/python -u scripts/land_grid_verdict.py [rows.csv]

Reads the `town_arm_grid.py` row format:

    town,stratum,tape,opponent,band,rank,arm,seed,ours,theirs,weed,drain_<PRODUCT>...

**Win rate, never money.** The ladder is Elo: a $43k win and a $4k win score identically
(`CLAUDE.md`). The 2026-08-22 tape shootout is the standing example -- `91906088` banks $822 LESS
than the incumbent and wins 27.9 points more, and it is the one that shipped. Bank is printed here
only as a tie-breaker and a sanity check, never as the ranking.

**Restricted to the seasons an arm actually CHANGED.** Most (town, opponent, seed) cells play out
identically under every arm, because the land day only matters when the bank is near the parcel
price on that day. Averaging over all 6,048 seasons dilutes a real effect by however many cells
were never in play -- the shootout's 27.9-point swing is a number over 420 contested seasons and
would have read as +1.9 over the full grid.

A cell counts as CHANGED when the arm's `ours` differs from control's `ours` on the same
(town, opponent, seed). That is exact: the sim is deterministic given a seed, so an identical bank
means an identical season.

Written 2026-08-22 while the grid was still running, so the answer is one command when it lands.
"""
import collections
import csv
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT = REPO / "data/logs/land_rows_2026-08-22.csv"


def load(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def cell(r):
    return (r["town"], r["opponent"], r["seed"])


def won(r):
    return int(r["ours"]) > int(r["theirs"])


def main():
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.exists():
        sys.exit(f"no rows at {path} -- the grid writes them when it exits")
    rows = load(path)
    if not rows:
        sys.exit(f"{path} is empty")

    by_arm = collections.defaultdict(dict)
    for r in rows:
        by_arm[r["arm"]][cell(r)] = r
    if "control" not in by_arm:
        sys.exit("no `control` arm in the rows; nothing to compare against")
    control = by_arm["control"]

    print(f"{path}   {len(rows)} rows, {len(by_arm)} arms, {len(control)} control cells\n")
    print("Restricted to the seasons each arm CHANGED against control "
          "(identical bank == identical season, the sim is deterministic).\n")
    print("%-12s %7s %9s %11s %8s %14s" %
          ("arm", "n diff", "arm win%", "control win%", "swing", "mean delta $"))

    verdicts = []
    for arm in sorted(by_arm):
        if arm == "control":
            continue
        diff = [(a, control[k]) for k, a in by_arm[arm].items()
                if k in control and int(a["ours"]) != int(control[k]["ours"])]
        if not diff:
            print("%-12s %7d %9s %11s %8s %14s" % (arm, 0, "-", "-", "-", "identical"))
            continue
        aw = 100.0 * sum(won(a) for a, _c in diff) / len(diff)
        cw = 100.0 * sum(won(c) for _a, c in diff) / len(diff)
        dm = sum(int(a["ours"]) - int(c["ours"]) for a, c in diff) / len(diff)
        verdicts.append((aw - cw, arm, len(diff), aw, cw, dm))
        print("%-12s %7d %8.1f%% %10.1f%% %+8.1f %+14.0f" % (arm, len(diff), aw, cw, aw - cw, dm))

    if not verdicts:
        print("\nNo arm changed a single season. The land day is not in play on this grid.")
        return
    verdicts.sort(reverse=True)
    swing, arm, n, aw, cw, dm = verdicts[0]
    print(f"\nBest on win rate: {arm}  {aw:.1f}% vs control {cw:.1f}%  ({swing:+.1f} points "
          f"over {n} contested seasons, mean bank {dm:+.0f})")
    if swing <= 0:
        print("  -- control wins. Do not move the land day.")
    elif dm < 0:
        print("  -- banks LESS and wins MORE. That is the shootout pattern; win rate is the "
              "selection criterion on an Elo ladder.")

    print("\nBy opponent band, best arm only:")
    best = by_arm[arm]
    bands = collections.defaultdict(lambda: [0, 0])
    for k, a in best.items():
        if k not in control or int(a["ours"]) == int(control[k]["ours"]):
            continue
        b = bands[a["band"]]
        b[0] += won(a)
        b[1] += 1
    for b in sorted(bands):
        w, n_ = bands[b]
        print("  %-8s %3d contested   %5.1f%%" % (b, n_, 100.0 * w / n_ if n_ else 0.0))


if __name__ == "__main__":
    main()
