"""Find the group of seasons that agree with each other -- the line a tree can learn.

Alex, 2026-08-21: "we are looking for the similarity in the tapes cos it has to match the dt not
anything else".

Selection so far has been by bank (wrong -- the ladder is Elo, and the top of this field is
separated by $77 to $3,000, so bank is variance) and then by margin. Both ask "which season is
best". The tree does not care which is best. It cares whether the seasons AGREE, because a target
row that occurs once cannot be predicted however strong the dependence.

That is very likely why exact row-match collapsed after d13: 150 distinct rows across 150 training
games. If one player runs two or three distinct season-long lines, pooling them makes every late day
unique -- while each line, taken alone, might repeat cleanly.

So: similarity between whole seasons, as the fraction of days whose target rows match exactly. Then
the largest mutually-similar group, and the per-day distinct counts INSIDE it. If those collapse,
the late-day cliff was an artifact of mixing lines and the fix is to train per line.

    python -u scripts/cluster_tapes.py --targets data/target_rows_kawa.json --threshold 0.5
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="fraction of days that must match for two seasons to be neighbours")
    ap.add_argument("--upto", type=int, default=30, help="compare days [0, upto)")
    ap.add_argument("--days-shown", nargs="*", type=int,
                    default=[3, 6, 9, 12, 14, 16, 18, 20, 22, 25, 29])
    args = ap.parse_args()

    rows = json.loads(pathlib.Path(args.targets).read_text())
    by_game = collections.defaultdict(dict)
    for r in rows:
        if r["day"] < args.upto:
            by_game[(r["game"], r["seat"])][r["day"]] = r["target_id"]

    games = sorted(by_game)
    full = [g for g in games if len(by_game[g]) == args.upto]
    print("%d seasons, %d complete over days 0-%d\n" % (len(games), len(full), args.upto - 1))
    if len(full) < 4:
        raise SystemExit("too few complete seasons to cluster")

    def sim(a, b):
        A, B = by_game[a], by_game[b]
        return sum(1 for d in range(args.upto) if A.get(d) == B.get(d)) / args.upto

    # Neighbour counts. O(n^2) on a few hundred seasons is nothing.
    neigh = {g: set() for g in full}
    for i, a in enumerate(full):
        for b in full[i + 1:]:
            if sim(a, b) >= args.threshold:
                neigh[a].add(b)
                neigh[b].add(a)

    seed_game = max(full, key=lambda g: len(neigh[g]))
    cluster = {seed_game} | neigh[seed_game]
    print("largest neighbourhood: %s seat %d with %d seasons within %.0f%% agreement"
          % (seed_game[0], seed_game[1], len(cluster), 100 * args.threshold))

    sizes = sorted((len(v) for v in neigh.values()), reverse=True)
    print("neighbourhood sizes, top 10: %s" % sizes[:10])
    print("seasons with NO neighbour at this threshold: %d\n"
          % sum(1 for v in neigh.values() if not v))

    def counts(members, label):
        print("%s  (%d seasons)" % (label, len(members)))
        print("  %4s %8s %10s %8s" % ("day", "seasons", "distinct", "top"))
        for day in args.days_shown:
            if day >= args.upto:
                continue
            c = collections.Counter(by_game[g].get(day) for g in members
                                    if day in by_game[g])
            if not c:
                continue
            n = sum(c.values())
            print("  %4d %8d %10d %7.1f%%"
                  % (day, n, len(c), 100.0 * c.most_common(1)[0][1] / n))
        print()

    counts(full, "ALL SEASONS POOLED")
    counts(cluster, "INSIDE THE LARGEST CLUSTER")

    # Where do the members of the cluster part company? That is the day the line itself branches.
    print("Within the cluster, the first day at which the modal row covers < 60%:")
    for day in range(args.upto):
        c = collections.Counter(by_game[g].get(day) for g in cluster if day in by_game[g])
        if not c:
            continue
        share = c.most_common(1)[0][1] / sum(c.values())
        if share < 0.6:
            print("  day %d, modal row covers %.0f%% of the cluster" % (day, 100 * share))
            break
    else:
        print("  never -- the cluster agrees on a modal row every day to d%d" % (args.upto - 1))


if __name__ == "__main__":
    main()
