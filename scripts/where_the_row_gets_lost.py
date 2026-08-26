"""Follow one day through every stage and find where the row's numbers disappear.

Alex, 2026-08-26: *"go systematically through and look why we dont have a plan and a route which
should make the numbers match his schedule"*.

The compliance report (`data/logs/row_compliance.log`) says WHAT is missed -- 920 sell-units, every
PLACE the row asks for, 121 feeds -- and nothing about WHERE. There are four stages and a
requirement can die at any of them:

    ROW         what `schedule.json` asks for that day
    OFFERED     nodes `router.build_nodes` builds from the live board. A requirement that never
                becomes a node cannot be planned, however good the router is.
    ROUTED      stops `_solve` actually seats on a unit. Offered minus routed is the planner
                declining work it was shown.
    EMITTED     ops that reached the environment. Routed minus emitted is the executor: the route
                is a visit ORDER and `_live_ops` re-derives the work at each stop, so a stop that
                returns nothing is dropped silently.

Counted per op kind, per day. Nothing is patched into the shipped path -- `build_nodes` and `_solve`
are wrapped in this process only.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
WATCH = ("PLACE", "FEED", "CARE", "PLANT", "HARVEST", "PICKUP", "DROP", "WATER")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="clone_open")
    ap.add_argument("--seed", type=int, default=123641874)
    ap.add_argument("--handover", type=int, default=12)
    ap.add_argument("--days", default="12,18,22,26")
    args = ap.parse_args()

    from kaggle_environments import make
    import scripts.breakdown as B
    from kagg.search import schedule_agent as SA
    from kagg.search import router as RT

    want_days = {int(d) for d in args.days.split(",")}
    offered = collections.defaultdict(collections.Counter)
    routed = collections.defaultdict(collections.Counter)
    emitted = collections.defaultdict(collections.Counter)
    cur = {"day": 0}

    inner_nodes, inner_solve = RT.build_nodes, SA._solve

    def wrapped_nodes(tiles, day, *a, **k):
        out = inner_nodes(tiles, day, *a, **k)
        d = int(day) if day is not None else -1
        if d in want_days and not offered[d]:          # dawn call only -- the plan's own view
            for n in out:
                for op in getattr(n, "ops", ()) or ():
                    name = op[0] if isinstance(op, (tuple, list)) else op
                    if name in WATCH:
                        offered[d][name] += 1
        return out

    def wrapped_solve(units, nodes, *a, **k):
        out = inner_solve(units, nodes, *a, **k)
        d = int(k.get("day") if k.get("day") is not None else cur["day"])
        if d in want_days and not routed[d]:
            seq = out[0] if isinstance(out, tuple) else out
            for work in (seq or {}).values() if isinstance(seq, dict) else (seq or []):
                for job in work or ():
                    for op in getattr(job, "ops", ()) or ():
                        name = op[0] if isinstance(op, (tuple, list)) else op
                        if name in WATCH:
                            routed[d][name] += 1
        return out

    RT.build_nodes, SA._solve = wrapped_nodes, wrapped_solve
    try:
        rel, sched_rel, team = B.TAPES[args.tape]
        path = str(REPO / rel)
        economy, shops = B.env_config(path), B.recorded_shops(path)
        tape = B.tape_policy(path, team, 0)
        raw = json.loads((REPO / sched_rel).read_text())
        sched = {int(k): v for k, v in raw.items()}
        thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
        ours = SA.make_agent(thin, 0, router=True, start_day=args.handover)

        env = make("kaggriculture", configuration=dict(economy, seed=args.seed), debug=False)
        env.reset(2)
        opp = B.tape_policy(path, team, 1)
        for t in range(719):
            env.state[0].observation.town["unlocked_shops"] = list(shops(t))
            env.state[1].observation.town["unlocked_shops"] = list(shops(t))
            cur["day"] = t // TPD
            obs = env.state[0].observation
            a0 = tape(obs, t) if t < args.handover * TPD else ours(obs)
            if cur["day"] in want_days:
                for op in [a0.get("farmer") or ["PASS"]] + list(a0.get("hands") or []):
                    if op and op[0] in WATCH:
                        emitted[cur["day"]][op[0]] += 1
            env.step([a0, opp(env.state[1].observation, t)])
    finally:
        RT.build_nodes, SA._solve = inner_nodes, inner_solve

    print(f"tape {args.tape}  seed {args.seed}  handover d{args.handover}")
    print("ROW = what the schedule asks, OFFERED = nodes built, "
          "ROUTED = stops seated, EMITTED = ops sent\n")
    row_key = {"PLACE": "places", "FEED": "feeds", "CARE": "cares", "PLANT": "plants"}
    for d in sorted(want_days):
        r = sched.get(d) or {}
        print(f"--- day {d}")
        print(f"    {'op':<10}{'ROW':>6}{'OFFERED':>10}{'ROUTED':>9}{'EMITTED':>9}")
        for op in WATCH:
            k = row_key.get(op)
            v = r.get(k) if k else None
            asked = (len(v) if isinstance(v, list) else int(v or 0)) if v is not None else None
            print(f"    {op:<10}{('-' if asked is None else asked):>6}"
                  f"{offered[d][op]:>10}{routed[d][op]:>9}{emitted[d][op]:>9}")
        print()


if __name__ == "__main__":
    main()
