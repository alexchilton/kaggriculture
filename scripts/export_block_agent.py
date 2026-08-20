"""Freeze the per-day trees and the block library into one artifact an agent can play from.

This is the build behind Alex's "ah ok a decision tree sounds good" and "i am waiting for the kawa
dt build".

What it writes, per day:

    {"day": {"features": [...names...],          # the exact order the tree expects
             "tree": <sklearn tree, pickled>,
             "blocks": {block_id: [24 actions]},
             "n_train": int, "holdout_acc": float, "baseline": float}}

**Trained on ALL games, reported on a held-out split.** Two different things, and conflating them is
how a number becomes meaningless. The accuracy quoted in the artifact comes from a game-level
holdout; the shipped tree is then refitted on everything, because at play time there is no reason to
throw away a third of the data.

**Only days the tree actually beats a constant are exported.** Measured on カワシギ, the tree stops
adding anything at d17 (4.5% baseline -> 6.0%) and is exactly zero from d18. Shipping those days
would mean picking a random block out of 131 and calling it a plan; the planner is better than that,
so those days are simply absent and the caller falls back.

**The features come from `build_day_rows.features`, which was verified to run unchanged on a LIVE
observation** -- 64 values, `town` present, no exception. That check exists because four separate
field-name mismatches produced clean fabricated results earlier in the same session.

    python -u scripts/export_block_agent.py --rows data/day_rows_kawa.json \\
        --out data/block_agent_kawa.pkl
"""

import argparse
import collections
import json
import pathlib
import pickle
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

MIN_GAIN = 0.05          # a day must beat the majority baseline by this much to be worth shipping


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--holdout", type=float, default=0.3)
    ap.add_argument("--min-games", type=int, default=12)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    import numpy as np
    from sklearn.tree import DecisionTreeClassifier

    rows = json.loads(pathlib.Path(args.rows).read_text())
    blocks_path = pathlib.Path(args.rows).with_name(pathlib.Path(args.rows).stem + ".blocks.json")
    library = json.loads(blocks_path.read_text())

    names = sorted({k for r in rows for k in r["x"]})
    index = {n: i for i, n in enumerate(names)}

    games = sorted({(r["game"], r["seat"]) for r in rows})
    rng = np.random.default_rng(args.seed)
    rng.shuffle(games)
    test_games = set(map(tuple, games[:max(1, int(len(games) * args.holdout))]))

    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r)

    def mat(rs):
        x = np.zeros((len(rs), len(names)))
        for i, r in enumerate(rs):
            for k, v in r["x"].items():
                x[i, index[k]] = v
        return x

    out = {}
    print("%4s %8s %9s %9s %8s %s" % ("day", "games", "baseline", "holdout", "blocks", "shipped"))
    for day in sorted(by_day):
        day_rows = by_day[day]
        tr = [r for r in day_rows if (r["game"], r["seat"]) not in test_games]
        te = [r for r in day_rows if (r["game"], r["seat"]) in test_games]
        if len(tr) < args.min_games or not te:
            continue

        ytr = [r["block"] for r in tr]
        yte = [r["block"] for r in te]
        majority = collections.Counter(ytr).most_common(1)[0][0]
        base = sum(1 for y in yte if y == majority) / len(yte)

        probe = DecisionTreeClassifier(max_depth=args.depth, random_state=args.seed)
        probe.fit(mat(tr), ytr)
        acc = float((probe.predict(mat(te)) == np.array(yte)).mean())

        ship = (acc - base) >= MIN_GAIN
        lib = {b: seq for b, seq in library.get(str(day), {}).items() if len(seq) == 24}
        if ship and lib:
            # Refit on everything for the shipped model; the number above stays the honest one.
            full = DecisionTreeClassifier(max_depth=args.depth, random_state=args.seed)
            full.fit(mat(day_rows), [r["block"] for r in day_rows])
            out[day] = {"tree": full, "blocks": lib, "n_train": len(day_rows),
                        "holdout_acc": acc, "baseline": base,
                        "fallback": collections.Counter(
                            r["block"] for r in day_rows).most_common(1)[0][0]}
        print("%4d %8d %8.1f%% %8.1f%% %8d %s"
              % (day, len(day_rows), 100 * base, 100 * acc, len(lib),
                 "yes" if day in out else "no -- falls back to the planner"))

    payload = {"features": names, "days": out, "depth": args.depth,
               "source_rows": str(args.rows)}
    path = pathlib.Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        pickle.dump(payload, fh)
    covered = sorted(out)
    print("\nwrote %s" % path)
    print("days covered: %s" % (covered or "NONE"))
    print("blocks stored: %d" % sum(len(v["blocks"]) for v in out.values()))
    if covered:
        print("beyond d%d the caller must fall back to the planner." % covered[-1])


if __name__ == "__main__":
    main()
