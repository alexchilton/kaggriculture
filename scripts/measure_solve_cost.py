"""What does it cost the teacher to SOLVE a day instead of replaying a stored route?

This is the number that decides whether DAgger is affordable. In DAgger the student drives, so it
reaches boards no stored route was solved for, and `PRECOMPUTED_ROUTES` is keyed on the exact
`(tile, ops)` tuple. A drifted board falls through to the live solver at almost every stop, so the
labelling cost is the SOLVED cost, not the shipped cost.

**Two earlier versions of this probe were invalid, in the same way, and both nearly got reported.**

  1. `mod.UNSOLVE_DAYS = ()` on the loaded bundle. No such attribute exists, so Python created a
     new one nobody reads. Timing came back 1.1x.
  2. Patching `SOLVED_DAYS` in the bundle's source text, then checking `getattr(mod,
     "PRECOMPUTED_ROUTES", {})`. That name is not at the bundle's top level either, so the guard
     read the DEFAULT and passed for the wrong reason. Timing came back 1.0x, on both arms.

The bundle keeps its planner sources in `_SOURCES` as strings and execs them into real entries in
`sys.modules`. The name the code actually reads is:

    sys.modules["kagg.search.cover"].PRECOMPUTED_ROUTES

which holds 12 days as shipped. That is what this patches, and the count is printed on BOTH arms
before either is timed. If the shipped arm does not show a non-zero count, the probe is broken and
no timing below it means anything.

    python -u scripts/measure_solve_cost.py --agent submission/main.py --days 12
"""

import argparse
import importlib.util
import sys
import time

from kaggle_environments import make

COVER = "kagg.search.cover"
SOLVED_MODULES = ("kagg.search.solved_days", "kagg.search.solved_days_q4",
                  "kagg.search.solved_days_straw", "kagg.search.solved_days_straw_q4")


def load(path, name):
    """Exec the bundle. It registers its planner modules into `sys.modules` as a side effect."""
    for m in (COVER,) + SOLVED_MODULES:
        sys.modules.pop(m, None)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def route_count():
    """What the code actually reads. Not a getattr default."""
    cover = sys.modules.get(COVER)
    if cover is None:
        raise SystemExit("%s is not in sys.modules -- the bundle changed shape and this probe is "
                         "measuring nothing. Stop." % COVER)
    return (len(cover.PRECOMPUTED_ROUTES), len(cover.SOLVED_DAYS), len(cover.UNSOLVE_DAYS))


def unsolve_everything():
    """Force every day through the live solver, at the names the planner reads.

    `SOLVED_DAYS` is cleared as well as `PRECOMPUTED_ROUTES`, because the agent constructor rebuilds
    the routes from it (`main.py:4529` and `:4836`, the second on the four-quadrant arm where
    `cover.UNSOLVE_DAYS` is set back to `()`). Clearing only the derived dict would be undone the
    moment an agent is built, silently.
    """
    cover = sys.modules[COVER]
    cover.PRECOMPUTED_ROUTES = {}
    cover.SOLVED_DAYS = {}
    cover.UNSOLVE_DAYS = tuple(range(30))
    for m in SOLVED_MODULES:
        if m in sys.modules:
            sys.modules[m].SOLVED_DAYS = {}


def timed_game(agent, seed, days):
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    turns, t0 = 0, time.time()
    while not env.done:
        if int(env.state[0].observation.get("day", 0) or 0) > days:
            break
        env.step([agent(env.state[s].observation, env.configuration) for s in (0, 1)])
        turns += 1
    return turns, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="submission/main.py")
    ap.add_argument("--days", type=int, default=12)
    ap.add_argument("--seed", type=int, default=12345)
    args = ap.parse_args()

    shipped = load(args.agent, "teacher_shipped")
    r0 = route_count()
    print("AS SHIPPED       routes=%d  solved_days=%d  unsolve_days=%d" % r0)
    if r0[0] == 0:
        raise SystemExit("shipped arm shows ZERO stored routes. The probe is not reading what the "
                         "planner reads, and every number below it would be a null dressed as a "
                         "measurement. Stop.")
    t_ship = timed_game(shipped.agent, args.seed, args.days)
    print("                 d0-d%d  %d turns  %.1fs  (%.4fs/turn)"
          % (args.days, t_ship[0], t_ship[1], t_ship[1] / max(1, t_ship[0])))

    solved = load(args.agent, "teacher_solved")
    unsolve_everything()
    r1 = route_count()
    print("\nEVERY DAY SOLVED routes=%d  solved_days=%d  unsolve_days=%d" % r1)
    if r1[0] != 0 or r1[1] != 0:
        raise SystemExit("routes survived the patch -- the timing would be the shipped path twice.")
    t_solve = timed_game(solved.agent, args.seed, args.days)
    print("                 d0-d%d  %d turns  %.1fs  (%.4fs/turn)"
          % (args.days, t_solve[0], t_solve[1], t_solve[1] / max(1, t_solve[0])))

    per_ship = t_ship[1] / max(1, t_ship[0])
    per_solve = t_solve[1] / max(1, t_solve[0])
    print("\nratio %.1fx" % (per_solve / max(1e-9, per_ship)))
    print("one 720-turn game : shipped %5.0fs   solved %5.0fs" % (per_ship * 720, per_solve * 720))
    print("640 games, 16 way : shipped %5.0f min solved %5.0f min"
          % (per_ship * 720 * 40 / 60, per_solve * 720 * 40 / 60))


if __name__ == "__main__":
    main()
