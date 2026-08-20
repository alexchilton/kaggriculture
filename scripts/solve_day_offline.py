"""Is a day's job set coverable? Solve it offline, against the SHIPPED planner, no 1s budget.

The board has no random terrain -- `_initial_tile` is a pure function of coordinates and the only
RNG in `kaggriculture.py` (line 858) drives the shop draw and weed spawns. Geometry, depots and
every walking distance are identical in every game, so a route solved once is reusable and the
1s/turn `actTimeout` stops being a limit on route QUALITY. See
`docs/the_route_is_precomputable_2026-08-12.md`.

**The search lives here, not in `cover.py`.** `cover()`'s greedy is cheapest-insertion under a fair
share cap, run over the job pool in the order it is handed. That order is the only lever needed:
re-offering the same jobs in a different order explores different seatings, and the best one found
is a valid plan by construction, because it came out of `cover` itself. Nothing about the shipped
planner changes -- no flag, no new code path, and the cost model is `cover`'s own `slot`/`cost`/
`materialise` rather than a second model of the game that might be optimistic about distances.

This matters because there are two `cover.py` in this tree: the one the agent ships and the one in
the LNS worktree, which differs by ~248 lines. Running the solver against the wrong one reported
"47/47 covered" for a day the shipped planner seats 45 of. Import path decides the answer, so this
script lives beside the agent it is measuring.

    python -u scripts/solve_day_offline.py tests/fixtures/lns_day_12_seed11_victor.json \
        --restarts 400
"""
import argparse
import collections
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from kagg.search import cover as C                                        # noqa: E402


def load(path):
    d = json.loads(pathlib.Path(path).read_text())
    jobs = []
    for j in d["jobs"]:
        job = C.Job(tile=j["tile"],
                    ops=[(o[0], o[1]) for o in j["ops"]],
                    needs=j.get("needs") or None,
                    gives=j.get("gives") or None,
                    at_risk=j.get("at_risk", False),
                    products=j.get("products") or ())
        job.funds = bool(j.get("funds", False))
        jobs.append(job)
    kw = dict(
        units=[tuple(u) for u in d["units"]], budget=list(d["budget"]),
        depots=tuple(tuple(x) for x in d["depots"]),
        carry={int(k): v for k, v in (d.get("carry") or {}).items()},
        supply=d.get("supply"), deliver=d.get("deliver", True), wanted=d.get("wanted"),
        rush=d.get("rush", False), day=d.get("day"), due=d.get("due"),
    )
    return jobs, kw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture")
    ap.add_argument("--restarts", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260812)
    ap.add_argument("--dump-route", default=None)
    args = ap.parse_args()

    jobs, kw = load(args.fixture)
    total = len(jobs)
    print(f"{args.fixture}")
    print(f"  day {kw['day']}   {len(kw['units'])} units   {total} jobs   "
          f"budgets {kw['budget'][:3]}...   depots {kw['depots']}\n")

    routes, left = C.cover(jobs=list(jobs), **kw)
    base = total - len(left)
    print(f"  shipped planner, jobs in their natural order:  {base}/{total}")
    for j in left:
        print(f"      LEFT {tuple(j.tile)} {[o[0] for o in j.ops]} "
              f"at_risk={j.at_risk} required={j.required}")

    rng = random.Random(args.seed)
    best, best_routes, best_left = base, routes, left
    hist = collections.Counter([base])
    for i in range(args.restarts):
        pool = list(jobs)
        rng.shuffle(pool)
        r, lf = C.cover(jobs=pool, **kw)
        cov = total - len(lf)
        hist[cov] += 1
        if cov > best:
            best, best_routes, best_left = cov, r, lf
            print(f"    restart {i}: {cov}/{total}  <- better")

    print(f"\n  {args.restarts} shuffled restarts, coverage distribution: "
          f"{dict(sorted(hist.items()))}")
    print(f"  BEST {best}/{total}")
    if best == total:
        print("  ==> every job is coverable; the shipped planner leaves work on the table.")
    elif best > base:
        print(f"  ==> {best - base} more than the shipped order, {total - best} still uncovered.")
    else:
        print("  ==> no ordering beat the shipped planner. Consistent with the day being full; "
              "this is a SEARCH, not a proof of infeasibility.")
    for j in best_left:
        print(f"      STILL LEFT {tuple(j.tile)} {[o[0] for o in j.ops]}")

    if args.dump_route:
        out = {str(u): [{"tile": list(j.tile), "ops": [list(o) for o in j.ops]} for j in work]
               for u, work in best_routes.items()}
        pathlib.Path(args.dump_route).write_text(json.dumps(out, indent=2))
        print(f"\n  route written to {args.dump_route}")


if __name__ == "__main__":
    main()
