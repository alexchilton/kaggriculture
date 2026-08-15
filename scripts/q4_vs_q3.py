"""The four-quadrant tape against the shipped three-quadrant one, one OS process per game.

## What the two arms are

`data/seed_scripts/kawashigi_q4c/schedule.json` is q3's rows for d0-d8 and Kawashigi's FOUR-quadrant
tape (`91907974`) from d9 on. d9 is where the two tapes first disagree -- through d8 they are the
same plan, same land day, same animals -- so the split costs nothing in the opening and the standing
"do not regress d0-d8" rule is satisfied by construction rather than by measurement.

What the q4 branch actually is, read off his tape rather than inferred:

    land bought d6, d11, d12      -> quadrants unlock d7, d12, d13
    herd COW 6 / SHEEP 12 = 18    -> against our COW 10 / SHEEP 4 = 14
    202 tile-plantings, 12 hands

**Both arms run routes live from d9.** The solved routes were built for a 75-tile three-quadrant
board and `_apply_precomputed` keys a stop on `(tile, ops)`, so a q4 board drops those stops rather
than adapting. Handicapping both arms identically is what makes the comparison about the plan. The
handicap is real -- the derived q4 draft measured it at -$1,873 and 2 wins -- and it is the thing a
re-solve on the 100-tile board is meant to give back.

## Why this reports quadrants and herd per seed

A money column alone cannot distinguish "the four-quadrant plan is worth $15k" from "the parcel was
never bought". The derived q4 draft bought the land and left it empty on 7 of 11 seeds, and its SE
crop count was the finding, not its bank. So every row states what was actually built.

Single-seed deltas here are near-worthless: measured 2026-08-15, one animal moved a bank by $22,785
and the opponent's by $36,847 on one seed, and two seeds out of fourteen drove an entire 38-config
sweep. Read the median and the count of seeds up, not any one row.

    python -u scripts/q4_vs_q3.py --seeds 1 2 3 4 5 6 7 8 9 10 11 12
"""
import argparse
import collections
import importlib
import importlib.util
import json
import pathlib
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
ARMS = {"q3": "data/seed_scripts/kawashigi/schedule.json",
        "q4": "data/seed_scripts/kawashigi_q4c/schedule.json"}
SPLIT = 9


def one(seed, arm, sched, opponent):
    """One season in its own process. See the module docstring on why a process is not reused."""
    from kaggle_environments import make

    A = importlib.import_module("kagg.search.schedule_agent")
    C = importlib.import_module("kagg.search.cover")
    PLAN = importlib.import_module("kagg.plan")

    # **Each arm runs the routes it was actually solved for**, which is the whole point of the
    # re-solve. `kagg/search/solved_days.py` was solved for the 75-tile three-quadrant board;
    # `solved_days_q4.py` was solved on 2026-08-15 against `kawashigi_q4c` on armed seed 3, covering
    # d9-d29 for the 100-tile board. `_apply_precomputed` keys a stop on `(tile, ops)`, so feeding a
    # four-quadrant board the three-quadrant routes drops most stops instead of adapting them --
    # that handicap fell entirely on q4 in the first comparison and is what this removes.
    if arm == "q4":
        Q4 = importlib.import_module("kagg.search.solved_days_q4")
        C.UNSOLVE_DAYS = ()
        C.PRECOMPUTED_ROUTES = {d: {u: [(tuple(t), tuple(ops)) for t, ops in seq]
                                    for u, seq in units.items()}
                                for d, units in Q4.SOLVED_DAYS.items()}

    sp = importlib.util.spec_from_file_location("opp", opponent)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(PLAN.load(str(REPO / sched)), me=0)

    grown, collected, prev = collections.Counter(), collections.Counter(), {}
    for t in range(719):
        o = env.state[0].observation
        cur = {}
        for y, row in enumerate(o["farms"][0]["tiles"]):
            for x, c in enumerate(row):
                if isinstance(c, dict) and c.get("crop"):
                    cur[(x, y)] = (c["crop"], c.get("yield_units", 0))
        for k, (crop, u) in cur.items():
            was = prev.get(k)
            if was and was[0] == crop:
                if u > was[1]:
                    grown[crop] += u - was[1]
                elif u < was[1]:
                    collected[crop] += was[1] - u
            elif u:
                grown[crop] += u
        for k, (crop, u) in prev.items():
            if u and cur.get(k, (None,))[0] != crop:
                collected[crop] += u
        prev = cur
        env.step([me(o, t), mod.agent(env.state[1].observation, t)])
        if env.done:
            break

    o = env.state[0].observation
    herd = collections.Counter(c["animal"] for row in o["farms"][0]["tiles"] for c in row
                               if isinstance(c, dict) and c.get("animal"))
    tg, tc = sum(grown.values()), sum(collected.values())
    return dict(seed=seed, arm=arm, money=env.steps[-1][0]["reward"],
                opp=env.steps[-1][1]["reward"],
                quads=len(o["farms"][0].get("unlocked_quadrants") or []),
                herd=dict(herd), collect=(tc / tg if tg else 0.0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(1, 13)))
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--child", nargs=3, default=None, help="internal: seed arm schedule")
    a = ap.parse_args()

    if a.child:
        seed, arm, sched = int(a.child[0]), a.child[1], a.child[2]
        print(json.dumps(one(seed, arm, sched, a.opponent)))
        return

    def child(job):
        seed, arm = job
        p = subprocess.run([sys.executable, "-u", __file__, "--child", str(seed), arm, ARMS[arm],
                            "--opponent", a.opponent],
                           capture_output=True, text=True, cwd=REPO,
                           env={**__import__("os").environ, "PYTHONPATH": "."})
        try:
            return json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:
            return dict(seed=seed, arm=arm, failed=(p.stderr or p.stdout)[-200:])

    jobs = [(s, arm) for s in a.seeds for arm in ARMS]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        rows = list(ex.map(child, jobs))

    by = {(r["seed"], r["arm"]): r for r in rows if not r.get("failed")}
    for r in rows:
        if r.get("failed"):
            print(f"seed {r['seed']} {r['arm']}: FAILED {r['failed'][:150]}")

    print(f"\n{'seed':>5}{'q3 $':>11}{'q4 $':>11}{'delta':>11}"
          f"{'q3 q':>5}{'q4 q':>5}  {'q4 herd':<22}{'q4 coll':>8}{'  winner'}")
    deltas, q4wins, q3wins = [], 0, 0
    for s in a.seeds:
        x, y = by.get((s, "q3")), by.get((s, "q4"))
        if not x or not y:
            continue
        d = y["money"] - x["money"]
        deltas.append(d)
        q4wins += y["money"] > y["opp"]
        q3wins += x["money"] > x["opp"]
        print(f"{s:>5}{x['money']:>11,.0f}{y['money']:>11,.0f}{d:>+11,.0f}"
              f"{x['quads']:>5}{y['quads']:>5}  {str(y['herd']):<22}{y['collect']:>7.0%}"
              f"   {'q4' if d > 0 else 'q3'}")
    if deltas:
        up = sum(1 for d in deltas if d > 0)
        print(f"\nq4 - q3 over {len(deltas)} seeds:  mean {statistics.mean(deltas):+,.0f}   "
              f"median {statistics.median(deltas):+,.0f}   "
              f"sd {statistics.stdev(deltas) if len(deltas) > 1 else 0:,.0f}   "
              f"{up}/{len(deltas)} seeds up")
        print(f"wins vs the frozen opponent:  q3 {q3wins}/{len(deltas)}   q4 {q4wins}/{len(deltas)}")
    print("\nBoth arms run routes LIVE from d9 and pay the same handicap. A re-solve on the "
          "100-tile board is what gives that back, and only to q4.")


if __name__ == "__main__":
    main()
