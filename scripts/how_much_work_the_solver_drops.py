"""Fable's discriminator: on a solved day, how much work does `cover` fail to seat?

`docs/where_the_turns_go_d12_d29_2026-08-26.md` measured 191 unit-turns per season spent standing
still beside ripe crop that no other unit collects, all of it in d12-d23, ending exactly at d24.
`docs/fable_the_idle_solver_zone_2026-08-26.md` gives five candidate links and one measurement that
tells them apart.

`cover()` returns `_apply_precomputed`'s result before the greedy body ever runs
(`kagg/search/cover.py:1160-1162`), so on a solved day the only route to a job that the fixture did
not name is one cheapest-insertion pass (`_insert_leftovers`, cover.py:1119). Whatever that pass
refuses is returned as `left` -- and `_solve` throws it away unread
(`out, _uncovered = DP.plan(...)`, schedule_agent.py:635).

So per day:

    jobs        what the day asked for
    seated      what the fixture routes named and the board could fill
    left        what fell through to insertion (fixture misses + tours trimmed to the day)
    DROPPED     what insertion refused -- work the day wanted, priced, and could not place

**A near-zero DROPPED column says the idle is pure fixture parking** (Fable's link 1: the offline
solve minimises turns after coverage, so it concentrates work and leaves hands at the shed) and the
fix belongs in the fixtures or the executor. **A DROPPED column that spikes on d12/d15/d18** -- the
worst idle days -- says links 3 and 4 carry it, and the fix is the control flow at cover.py:1160.

Nothing here is patched into the shipped path: `_apply_precomputed` is wrapped in this process only.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

ROWS = []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()

    from kaggle_environments import make

    from kagg.search import cover
    import scripts.breakdown as B

    replay, schedule, team = B.TAPES[B.DEFAULT_TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    # --- wrap, this process only
    real = cover._apply_precomputed

    def wrapped(day, units, jobs, budget, depots, carry, wanted, deliver, rush, due):
        n_before = len(cover.PRECOMPUTED_MISSES)
        out = real(day, units, jobs, budget, depots, carry, wanted, deliver, rush, due)
        if out is None:
            ROWS.append(dict(day=day, jobs=len(jobs), seated=None, dropped=None,
                             misses=len(cover.PRECOMPUTED_MISSES) - n_before, greedy=True))
            return out
        routes, left = out
        ROWS.append(dict(day=day, jobs=len(jobs),
                         seated=sum(len(v) for v in routes.values()),
                         dropped=len(left),
                         misses=len(cover.PRECOMPUTED_MISSES) - n_before, greedy=False))
        return out

    cover._apply_precomputed = wrapped

    from kagg.search import schedule_agent

    economy = B.env_config(replay)
    shops = B.recorded_shops(replay)
    cfg = dict(economy, seed=args.seed, weedSpawnChance=args.weeds)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    ours = schedule_agent.make_agent(thin, 0, router=True)
    opp = B.tape_policy(replay, team, 1)

    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        a0, a1 = ours(o0), opp(o1, t)
        env.step([a0, a1])
    print(f"final bank ours ${env.state[0].observation['farms'][0]['money']:,.0f}  "
          f"theirs ${env.state[0].observation['farms'][1]['money']:,.0f}")
    print()

    by = collections.defaultdict(lambda: collections.Counter())
    calls = collections.Counter()
    for r in ROWS:
        d = r["day"]
        calls[d] += 1
        by[d]["jobs"] += r["jobs"]
        by[d]["greedy"] += int(r["greedy"])
        if not r["greedy"]:
            by[d]["seated"] += r["seated"]
            by[d]["dropped"] += r["dropped"]
        by[d]["misses"] += r["misses"]

    print(f"{'day':>5}{'calls':>7}{'greedy':>8}{'jobs':>8}{'seated':>8}{'DROPPED':>9}{'misses':>8}")
    for d in sorted(by):
        r = by[d]
        print(f"{d:>5}{calls[d]:>7}{r['greedy']:>8}{r['jobs']:>8}{r['seated']:>8}"
              f"{r['dropped']:>9}{r['misses']:>8}")
    solved = [d for d in sorted(by) if 12 <= d <= 23]
    print()
    print(f"d12-d23 total DROPPED: {sum(by[d]['dropped'] for d in solved)}   "
          f"jobs {sum(by[d]['jobs'] for d in solved)}   "
          f"misses {sum(by[d]['misses'] for d in solved)}")
    for line in cover.PRECOMPUTED_MISSES[:40]:
        print("   MISS", line)


if __name__ == "__main__":
    main()
