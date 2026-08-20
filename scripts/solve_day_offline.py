"""Is a day's job set actually coverable? Solve it offline, with no 1-second budget.

The board has NO random terrain. `_initial_tile(x, y, board_size)` is a pure function of
coordinates and `_default_spawn` is deterministic; the ONLY rng in `kaggriculture.py` is
`random.Random((seed * 1_000_003) ^ day)` at line 858, used for exactly two things -- the shop
unlock draw and weed spawns. So the geometry, the depots and every walking distance are identical
in every game ever played, and a route solved once is reusable. The shop draw changes what is worth
SELLING, not where anyone walks.

That is what makes this worth doing: the day planner is up against a 1s/turn `actTimeout`
(`docs/competition_brief.md`) and the greedy alone already costs 0.37-0.5s by d10-d17. Offline there
is no such limit, so the question "did our planner leave a job on the table, or was the day simply
full?" can be answered exactly rather than argued about.

Uses `cover.py`'s OWN `cover()` -- the same `slot`/`cost`/`materialise` the shipped planner uses --
so a route it reports as feasible is feasible under the real cost model, not a second model of the
game that might be optimistic about walking distances. The only thing changed is how long the
search is allowed to run and how many times it restarts.

    python -u scripts/solve_day_offline.py tests/fixtures/lns_day_18_seed11_victor.json \
        --seconds 30 --restarts 8
"""
import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from kagg.search import cover as C                                        # noqa: E402


def load(path):
    d = json.loads(pathlib.Path(path).read_text())
    jobs = [C.Job(tile=j["tile"],
                  ops=[(o[0], o[1]) for o in j["ops"]],
                  needs=j.get("needs") or None,
                  gives=j.get("gives") or None,
                  at_risk=j.get("at_risk", False),
                  products=j.get("products") or ())
            for j in d["jobs"]]
    for job, raw in zip(jobs, d["jobs"]):
        job.funds = bool(raw.get("funds", False))
    kw = dict(
        units=[tuple(u) for u in d["units"]],
        budget=list(d["budget"]),
        depots=tuple(tuple(x) for x in d["depots"]),
        carry={int(k): v for k, v in (d.get("carry") or {}).items()},
        supply=d.get("supply"),
        deliver=d.get("deliver", True),
        wanted=d.get("wanted"),
        rush=d.get("rush", False),
        day=d.get("day"),
        due=d.get("due"),
    )
    return jobs, kw


def run(jobs, kw, seconds, seed):
    C.RUIN_AND_RECREATE = seconds > 0
    C.RUIN_AND_RECREATE_SECONDS = seconds
    C.RUIN_SEED = seed
    routes, left = C.cover(jobs=list(jobs), **kw)
    return routes, left


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture")
    ap.add_argument("--seconds", type=float, default=30.0)
    ap.add_argument("--restarts", type=int, default=8)
    ap.add_argument("--dump-route", default=None)
    args = ap.parse_args()

    jobs, kw = load(args.fixture)
    total = len(jobs)
    print(f"{args.fixture}")
    print(f"  day {kw['day']}   {len(kw['units'])} units   budget {kw['budget'][:3]}...   "
          f"{total} jobs   depots {kw['depots']}\n")

    routes, left = run(jobs, kw, 0.0, C.RUIN_SEED)          # the shipped greedy, no LNS
    base_cov = total - len(left)
    print(f"  shipped planner (greedy, no LNS):   {base_cov}/{total} covered, "
          f"{len(left)} left")
    for j in left:
        print(f"      LEFT {j.tile} {[o[0] for o in j.ops]} at_risk={j.at_risk} "
              f"required={j.required}")

    best = (base_cov, routes, left)
    print(f"\n  offline search: {args.restarts} restarts x {args.seconds}s")
    for i in range(args.restarts):
        r, lf = run(jobs, kw, args.seconds, 20260812 + i * 7919)
        cov = total - len(lf)
        flag = ""
        if cov > best[0]:
            best = (cov, r, lf)
            flag = "  <- new best"
        print(f"    restart {i}  seed {20260812 + i*7919}  covered {cov}/{total}{flag}")

    cov, routes, left = best
    print(f"\n  BEST {cov}/{total}")
    if cov == total:
        print("  ==> EVERY job is coverable. The day is NOT full; the planner left work undone.")
    elif cov > base_cov:
        print(f"  ==> {cov - base_cov} more than the shipped planner, but {total - cov} still "
              f"uncovered -- not proven full, only not-yet-solved.")
    else:
        print("  ==> No arrangement beat the shipped planner. Consistent with the day being full, "
              "but this is a SEARCH, not a proof of infeasibility.")
    for j in left:
        print(f"      STILL LEFT {j.tile} {[o[0] for o in j.ops]}")

    used = sum(len(v) for v in routes.values())
    print(f"\n  turns per unit (budget {kw['budget'][0]}):")
    for u, work in sorted(routes.items()):
        if not work:
            continue
        tour = C.materialise(kw["units"][u], work, carry=kw["carry"].get(u),
                             depots=kw["depots"], wanted=kw["wanted"],
                             deliver=kw["deliver"], rush=kw["rush"])
        t = C.turns(kw["units"][u], tour) if tour is not None else None
        print(f"    u{u:<3} start {kw['units'][u]}  jobs {len(work):>2}  turns {t}")
    print(f"  {used} job-slots filled")

    if args.dump_route:
        out = {str(u): [{"tile": list(j.tile), "ops": [list(o) for o in j.ops]} for j in work]
               for u, work in routes.items()}
        pathlib.Path(args.dump_route).write_text(json.dumps(out, indent=2))
        print(f"\n  route written to {args.dump_route}")


if __name__ == "__main__":
    main()
