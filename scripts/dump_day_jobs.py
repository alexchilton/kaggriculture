"""Capture one day's job set from a live game, in the shape `solve_day_offline.py` reads.

`solve_day_offline.py` searches seatings for a day and is the tool that produced the routes behind
"8 days solved offline (d12,16,18,23-27)". It takes a fixture -- units, budget, depots, carry,
supply, and the day's job list -- and **nothing in the tree wrote one.** The existing fixtures under
`tests/fixtures/` were made by hand, which is why the solved days are the days somebody hand-built a
fixture for. Wanting a new day solved meant hand-building another.

This runs the real agent, on a real board, against a real tape, and copies the arguments out of
`cover.cover` on the target day. So the fixture is exactly what the shipped planner was asked to
cover at that moment -- not a reconstruction of it, which is the failure mode the solver's own
docstring warns about ("Running the solver against the wrong `cover.py` reported 47/47 covered for a
day the shipped planner seats 45 of").

    python -u scripts/dump_day_jobs.py --day 3 --tape kawashigi \
        --out tests/fixtures/day_3_kawashigi.json
    python -u scripts/solve_day_offline.py tests/fixtures/day_3_kawashigi.json --restarts 400
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import kagg.plan as _PLAN                                                 # noqa: E402
from kagg.search import cover as C                                        # noqa: E402


def _jsonable(job):
    return {"tile": list(job.tile),
            "ops": [[o[0], o[1]] for o in job.ops],
            "needs": dict(job.needs or {}),
            "gives": dict(job.gives or {}),
            "at_risk": bool(getattr(job, "at_risk", False)),
            "funds": bool(getattr(job, "funds", False)),
            "products": list(getattr(job, "products", ()) or ())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", type=int, required=True)
    ap.add_argument("--tape", default="kawashigi")
    ap.add_argument("--schedule", default=None)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--module", default="schedule_agent")
    #: **Which BOARD to dump.** A route is keyed on `(tile, ops)` by `cover._apply_precomputed`, so
    #: a set solved for one board drops rather than adapts on another -- `q4_branch`'s own docstring
    #: says so for 75 tiles against 100. The same holds for the crop mix: the strawberry season and
    #: the melon season put different crops on different tiles from d5. Four boards exist (melon/
    #: straw x three/four quadrants) and only the two melon ones have ever been solved.
    ap.add_argument("--arm", choices=("melon", "straw"), default="melon",
                    help="straw arms the strawberry branch (melon_branch); melon holds it quiet")
    ap.add_argument("--q4", action="store_true",
                    help="force the four-quadrant branch on, whatever the town draws")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    import importlib
    import scripts.breakdown as B
    B.TAPES.setdefault("kawashigi", ("data/seed_scripts/kawashigi/92498144.json",
                                     "data/seed_scripts/kawashigi/schedule.json", "カワシギ"))
    SA = importlib.import_module("kagg.search." + args.module)
    B.schedule_agent = SA
    from kagg.search import melon_branch as _MB
    from kagg.search import q4_branch as _Q4
    # The tape's own opponent does not hold nine melon at d3, so the strawberry branch would stay
    # quiet and `--arm straw` would silently dump the melon board. 0 arms on any opponent, 99 none.
    _MB.OPPONENT_MELON = 0 if args.arm == "straw" else 99
    if args.q4:
        _Q4.BRANCH.trigger = lambda observation: True

    replay, schedule, team = B.TAPES[args.tape]
    sched = _PLAN.load(args.schedule or schedule)

    grabbed = {}
    real = C.plan

    import inspect
    sig = inspect.signature(real)

    def spy(*a, **kw):
        # Bind against `cover`'s real signature rather than assuming a positional order: `depots`,
        # `day` and `rush` all have defaults and any of them may arrive either way. Guessing the
        # calling convention is the mistake that made the parity harness send actions no agent
        # sends -- see CLAUDE.md, "check that a harness sends what an agent would send".
        bound = sig.bind(*a, **kw)
        bound.apply_defaults()
        p = bound.arguments
        # The planner may call cover more than once in a day; the FIRST call of the target day is
        # the dawn plan, which is the one that decides the day (`plan once, never replan`).
        if p.get("day") == args.day and not grabbed:
            grabbed.update(units=[list(u) for u in p["units"]],
                           budget=list(p["budget"]),
                           depots=[list(d) for d in p["depots"]],
                           carry={str(k): v for k, v in (p.get("carry") or {}).items()},
                           supply=p.get("supply"),
                           deliver=p.get("deliver", True),
                           wanted=p.get("wanted"),
                           rush=bool(p.get("rush", False)),
                           day=args.day,
                           due=p.get("due"),
                           jobs=[_jsonable(j) for j in p["jobs"]])
        return real(*a, **kw)

    C.plan = spy
    try:
        B.run(lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(sched, 0, router=True)),
              lambda: B.tape_policy(replay, team, 1),
              args.seed, args.weeds, stop_day=args.day + 1,
              economy=B.env_config(replay), shops=B.recorded_shops(replay))
    finally:
        C.plan = real

    if not grabbed:
        raise SystemExit("cover.plan() was never called with day=%d -- is COVER_PLANNER on, and does the "
                         "day have any work? (a day whose job pool is empty never reaches it)"
                         % args.day)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(grabbed, indent=1))
    print("%s  day %d, %d units, %d jobs, budget %s"
          % (out, args.day, len(grabbed["units"]), len(grabbed["jobs"]), grabbed["budget"]))


if __name__ == "__main__":
    main()
