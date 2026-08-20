"""Fork one board at turn X and run every crop config from the SAME position.

## Why forking, rather than replaying whole seasons

A full re-run per config re-rolls the entire season, so ~15% seed variance swamps any crop effect --
that is this project's own measured figure, and it is an order of magnitude larger than the thing
being swept. Forking removes it: every config inherits an identical board, bank, herd and crew, so
the only difference downstream is the crop decision. It is the common-random-numbers trick, and it
also costs less, because only the tail is simulated.

The environment is deterministic given a seed and an action sequence, so the fork is exact rather
than approximate: the base run's actions are replayed into a fresh env up to the fork turn, and the
live agents take over from there.

**Fork on an h0 boundary.** The agent plans a whole day once, at hour 0, and never replans
(`plan_once`). Forking mid-day would hand the new config a plan built by the old one.

**What a fork cannot answer.** Whether a config would have REACHED that position. Melon is planted
on d0/d6/d7, so a fork at d8 cannot test melon at all -- it is already in the ground. Crops whose
plantings straddle the fork are only partly testable. The fork turn is therefore a real constraint
on the question, not a free parameter.

## Cadence

Crops differ in how often they must be watered and harvested, and that is the cost a crop-value
model cannot see:

    WHEAT       one-shot, first yield d+2,  6 units      -- harvest every ~4 days
    CARROT      one-shot, first yield d+2,  4 units      -- harvest every ~3 days
    TOMATO      ONGOING,  first yield d+8,  interval 1   -- harvest EVERY DAY for 4 days
    STRAWBERRY  ONGOING,  first yield d+10, interval 2   -- harvest every 2 days
    MELON       one-shot, first yield d+10, 6 units      -- harvest every ~12 days

Tomato's daily cadence is the expensive one: four harvest visits per tile per cycle against wheat's
one. `PER-CROP HARVESTS` is reported for exactly this reason -- a config whose harvests do not rise
with its tiles is one the crew could not actually serve, and its revenue number is fiction.

Run with the solver OFF over the fork range, so each config is routed from its own board. Measured
cost of that handicap: win rate unchanged (84.5% both), money -$3,047. Both arms pay it equally.
"""
import argparse
import collections
import copy
import importlib
import json
import pathlib
import sys
import time

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent

#: `(src, dst, tiles)` triples. Isolation first, then combinations of whatever moved.
CONFIGS = {
    "baseline":            (),
    # **Tomato, in isolation at four depths.** No top player grows it -- Kawashigi, Emon xu and
    # Yura are zero across 40+ games -- so its book is uncontested, and the 2026-08-15 note says it
    # becomes viable in ~50% of games. Both facts argue for testing it; the second says expect half
    # the seeds to show nothing.
    #
    # TOMATO is ONGOING: first yield d+8, then daily to 4 units. Planted after ~d18 it cannot
    # complete a cycle, so the fork must be early enough to leave a planting window.
    "wheat->tomato 4":     (("WHEAT", "TOMATO", 4),),
    "wheat->tomato 8":     (("WHEAT", "TOMATO", 8),),
    "wheat->tomato 16":    (("WHEAT", "TOMATO", 16),),
    "straw->tomato 8":     (("STRAWBERRY", "TOMATO", 8),),
    # the comparison crops, so tomato is judged against an alternative use of the same tiles
    "wheat->carrot 8":     (("WHEAT", "CARROT", 8),),
    "straw->wheat 8":      (("STRAWBERRY", "WHEAT", 8),),
    # combinations -- the crops compete for the same crew turns, so isolation is not additive
    "tomato 8 + carrot 8": (("WHEAT", "TOMATO", 8), ("WHEAT", "CARROT", 8)),
    "straw->wheat + tomato 8": (("STRAWBERRY", "WHEAT", 8), ("WHEAT", "TOMATO", 8)),
}


_ALL_ROUTES = None


def configure(shifts, fork_day):
    """Apply one config to the live modules. Routes go live from the fork day onward.

    The full route table is snapshotted once, on first call, because `configure` filters
    `PRECOMPUTED_ROUTES` in place -- reading it again after a filter would compound the filters and
    silently unsolve days that should stay solved.
    """
    global _ALL_ROUTES
    A = importlib.import_module("kagg.search.schedule_agent")
    C = importlib.import_module("kagg.search.cover")
    if _ALL_ROUTES is None:
        _ALL_ROUTES = dict(C.PRECOMPUTED_ROUTES)
    A.CROP_TILE_SHIFTS = shifts
    A.LATE_CROP_FROM_DAY = 0
    C.UNSOLVE_DAYS = tuple(range(fork_day, 30))
    C.PRECOMPUTED_ROUTES = {d: v for d, v in _ALL_ROUTES.items() if d not in C.UNSOLVE_DAYS}
    return A


def base_actions(seed, fork_turn, opponent):
    """Play to the fork turn with the baseline config, recording every action for exact replay."""
    from kaggle_environments import make

    A = configure((), 30)                    # baseline, solver fully on, before the fork
    PLAN = importlib.import_module("kagg.plan")
    sched = PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json"))

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)
    opp = _resolve(opponent, 1)
    recorded = []
    for t in range(fork_turn):
        o0, o1 = env.state[0].observation, env.state[1].observation
        acts = [me(o0, t), opp(o1, t)]
        recorded.append(copy.deepcopy(acts))
        env.step(acts)
        if env.done:
            break
    return recorded


_OPP_CACHE = {}


def _resolve(spec, seat):
    """A CALLABLE opponent.

    `arena._resolve` hands a file path straight back, which `env.run` accepts and a manual
    `env.step` loop does not. Forking steps by hand, so the path is loaded as a module here and its
    `agent` entry point taken. Cached: the submission bundle is 775 KB and rebuilding its embedded
    modules per fork would dominate the run.
    """
    if callable(spec):
        return spec
    if isinstance(spec, str) and spec.endswith(".py"):
        if spec not in _OPP_CACHE:
            import importlib.util
            name = "opp_" + pathlib.Path(spec).stem
            sp = importlib.util.spec_from_file_location(name, spec)
            mod = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(mod)
            fn = getattr(mod, "agent", None)
            if fn is None:                       # fall back to the last callable defined
                fn = [v for v in vars(mod).values() if callable(v)][-1]
            _OPP_CACHE[spec] = fn
        return _OPP_CACHE[spec]
    from kagg.arena.arena import _resolve as R
    return R(spec, seat)


def run_from_fork(seed, fork_turn, fork_day, shifts, recorded, opponent):
    """Replay to the fork, then hand over to a fresh agent carrying `shifts`."""
    from kaggle_environments import make

    A = configure(shifts, fork_day)
    PLAN = importlib.import_module("kagg.plan")
    sched = PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json"))

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    for acts in recorded:
        env.step(copy.deepcopy(acts))
        if env.done:
            break

    me = A.make_agent(sched, me=0)
    opp = _resolve(opponent, 1)
    harvests = collections.Counter()
    for t in range(len(recorded), 719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        before = {}
        for row in o0["farms"][0]["tiles"]:
            for c in row:
                if isinstance(c, dict) and c.get("crop"):
                    before[(c.get("crop"))] = before.get(c.get("crop"), 0) + c.get("yield_units", 0)
        a0 = me(o0, t)
        env.step([a0, opp(o1, t)])
        for op in a0 or []:
            if isinstance(op, list) and op and op[0] == "HARVEST":
                harvests["HARVEST"] += 1
        if env.done:
            break

    fin = env.steps[-1]
    obs = fin[0]["observation"]
    tiles = collections.Counter()
    for row in obs["farms"][0]["tiles"]:
        for c in row:
            if isinstance(c, dict) and c.get("crop"):
                tiles[c["crop"]] += 1
    return fin[0]["reward"], fin[1]["reward"], harvests["HARVEST"], dict(tiles)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fork-day", type=int, default=8, help="h0 of this day is the fork point")
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(1, 9)))
    ap.add_argument("--opponent", default="submission/main.py")
    args = ap.parse_args()

    fork_turn = args.fork_day * 24
    print(f"fork at d{args.fork_day} h0 (turn {fork_turn}), seeds {args.seeds}, "
          f"opponent {args.opponent}")
    print(f"routes LIVE from d{args.fork_day}; melon is planted d0/d6/d7 so it is only testable "
          f"with --fork-day 0\n")

    results = collections.defaultdict(list)
    for seed in args.seeds:
        t0 = time.time()
        recorded = base_actions(seed, fork_turn, args.opponent)
        line = [f"seed {seed:>3}"]
        for label, shifts in CONFIGS.items():
            try:
                mine, theirs, harv, tiles = run_from_fork(
                    seed, fork_turn, args.fork_day, shifts, recorded, args.opponent)
            except Exception as e:
                print(f"  {label:<30} FAILED {type(e).__name__}: {e}", flush=True)
                continue
            results[label].append((mine, theirs, harv))
        base = results["baseline"][-1][0] if results.get("baseline") else 0
        print(" ".join(line) + "  " + "  ".join(
            f"{lab.split('->')[-1][:9]}:{results[lab][-1][0]-base:+,.0f}"
            for lab in CONFIGS if results.get(lab) and lab != "baseline"), flush=True)
        print(f"      baseline ${base:,.0f}   [{time.time()-t0:.0f}s]", flush=True)

    print(f"\n{'config':<32}{'mean $':>11}{'vs base':>10}{'wins':>7}{'harvests':>10}")
    base_mean = sum(m for m, _, _ in results["baseline"]) / max(1, len(results["baseline"]))
    rows = []
    for label in CONFIGS:
        rs = results.get(label) or []
        if not rs:
            continue
        mean = sum(m for m, _, _ in rs) / len(rs)
        wins = sum(1 for m, t, _ in rs if m > t)
        harv = sum(h for _, _, h in rs) / len(rs)
        rows.append((label, mean, mean - base_mean, wins, len(rs), harv))
        print(f"{label:<32}{mean:>11,.0f}{mean-base_mean:>+10,.0f}{wins:>4}/{len(rs)}{harv:>10.0f}")
    json.dump([list(r) for r in rows], open(REPO / "data/logs/fork_compare.json", "w"), indent=1)
    best = max(rows, key=lambda r: r[1])
    print(f"\nbest by mean money: {best[0]}  {best[2]:+,.0f} vs baseline")
    print("NOTE: money, not win rate. The ladder is Elo -- confirm any winner on win rate before "
          "shipping it.")


if __name__ == "__main__":
    main()
