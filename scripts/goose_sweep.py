"""How many of the schedule's animals should be GEESE? Swept over counts and over seeds.

Each arm plays the SAME agent with a different `HERD_GEESE` against a FROZEN `HERD_GEESE = 0`
baseline -- the agent as shipped -- over a seed list, both seatings.

Three things this is careful about, each of which has burned this project before:

* **Both seatings, every seed.** Market orders settle in seat order, so seat 0 is a real advantage
  and a one-sided sweep measures it rather than the change.
* **A fresh agent per match.** `make_agent` builds its `state` once in a closure; a finished season
  walked into the next match and killed the agent outright, for a measured 17.8x error
  (`kagg/arena/arena.py`). Every match here builds both sides from scratch inside the worker.
* **Weeds ON.** The configuration is left at the environment default, which is `0.005` -- the value
  every downloaded ladder game carries. Our grids run `0.0` to keep the tape comparison clean, and
  no agent number in `docs/` has ever been scored under the game actually being played.

**Win rate is the decision, money is context.** The ladder is an Elo rating, so a $43k win and a $4k
win score identically. The money columns are printed to catch an arm that wins by banking $3,000 --
the opening stake, i.e. an agent that did nothing.

    PYTHONPATH=. .venv/bin/python -u scripts/goose_sweep.py --seeds 24 --counts 0,2,3,4,5,6
"""
import argparse
import collections
import json
import pathlib
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
PLAN = REPO / "data/seed_scripts/victor/schedule.json"
TAPE_ONLY = ("money_dawn", "money_dusk", "bank", "tiles", "weeds")


def _schedule():
    raw = json.loads(PLAN.read_text())
    return {int(k): {kk: vv for kk, vv in row.items() if kk not in TAPE_ONLY}
            for k, row in raw.items()}


def _build(geese, seat):
    """A brand new agent with `HERD_GEESE` forced to `geese`, built inside this worker."""
    from kagg.search import schedule_agent_1455mh as SA

    SA.HERD_GEESE = geese
    return SA.make_agent(_schedule(), seat, router=True)


def _play(job):
    """One seating of one seed: candidate at `geese` against the frozen baseline."""
    geese, seed, swapped = job
    from kaggle_environments import make

    me_seat = 1 if swapped else 0
    me = _build(geese, me_seat)
    them = _build(0, 1 - me_seat)
    pair = (them, me) if swapped else (me, them)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(list(pair))
    final = env.steps[-1]
    mine = final[me_seat]["reward"]
    theirs = final[1 - me_seat]["reward"]
    return geese, seed, swapped, float(mine or 0), float(theirs or 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--first-seed", type=int, default=900)
    ap.add_argument("--counts", default="0,2,3,4,5,6")
    ap.add_argument("--workers", type=int, default=14)
    args = ap.parse_args()

    counts = [int(c) for c in args.counts.split(",") if c.strip()]
    seeds = list(range(args.first_seed, args.first_seed + args.seeds))
    jobs = [(g, s, sw) for g in counts for s in seeds for sw in (False, True)]

    print(f"HERD_GEESE {counts} vs a frozen HERD_GEESE=0 baseline")
    print(f"seeds {seeds[0]}-{seeds[-1]}, both seatings, weeds at the env default "
          f"= {len(jobs)} games\n")

    clock = time.perf_counter()
    if args.workers > 1:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            rows = list(pool.map(_play, jobs))
    else:
        rows = [_play(j) for j in jobs]

    per = collections.defaultdict(list)
    for geese, seed, swapped, mine, theirs in rows:
        per[geese].append((mine, theirs, seed, swapped))

    print(f"  {'geese':>6} {'games':>6} {'win':>7} {'draw':>6} {'mean ours':>11} "
          f"{'mean theirs':>12} {'mean margin':>12} {'seed sd':>9}")
    for g in counts:
        rs = per[g]
        wins = sum(1 for m, t, _, _ in rs if m > t)
        draws = sum(1 for m, t, _, _ in rs if m == t)
        ours = statistics.mean(m for m, _, _, _ in rs)
        thrs = statistics.mean(t for _, t, _, _ in rs)
        margins = [m - t for m, t, _, _ in rs]
        sd = statistics.pstdev(margins)
        print(f"  {g:>6} {len(rs):>6} {wins / len(rs):>6.1%} {draws / len(rs):>5.1%} "
              f"{ours:>11,.0f} {thrs:>12,.0f} {statistics.mean(margins):>12,.0f} {sd:>9,.0f}")

    # Per seed, so a single lucky board cannot carry an arm. The baseline arm (0) is the control and
    # must come out near 50% -- if it does not, the harness is measuring the seating, not the change.
    print(f"\n  per-seed margin (ours - theirs), averaged over both seatings:")
    print(f"  {'seed':>6} " + "".join(f"{g:>10}" for g in counts))
    for s in seeds:
        cells = []
        for g in counts:
            rs = [m - t for m, t, sd_, _ in per[g] if sd_ == s]
            cells.append(f"{statistics.mean(rs):>10,.0f}" if rs else f"{'-':>10}")
        print(f"  {s:>6} " + "".join(cells))

    print(f"\n  {time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
