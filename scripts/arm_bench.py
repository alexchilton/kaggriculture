"""Banks and paired margins for a list of built arms, against one opponent.

Paired on (seed, seat), so an arm-to-arm difference is a difference on ONE board and not two
samples of the world distribution. Bank against a real opponent is the gate; `env.run` against
`starter` is not -- it banks ~$3,500 and every number against it reads about 2x reality.
"""
import argparse, statistics
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPP = ROOT / "submission/shop0909/main.py"


def _arm_path(name):
    return ROOT / "submission" / name / "main.py"


def play(job):
    arm, seed, seat = job
    from kaggle_environments import make
    pair = ([str(_arm_path(arm)), str(OPP)] if seat == 0
            else [str(OPP), str(_arm_path(arm))])
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r = [x["reward"] for x in env.steps[-1]]
    ours, them = r[seat] or 0, r[1 - seat] or 0
    return {"arm": arm, "seed": seed, "seat": seat, "ours": ours, "margin": ours - them,
            "status": "/".join(str(x["status"]) for x in env.steps[-1])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", required=True)
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--procs", type=int, default=5)
    args = ap.parse_args()

    for a in args.arms:
        if not _arm_path(a).exists():
            raise SystemExit(f"{a}: {_arm_path(a)} does not exist -- build it first")

    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(a, s, t) for a in args.arms for s in seeds for t in (0, 1)]
    print(f"{len(jobs)} games", flush=True)
    with Pool(args.procs) as pool:
        rows = pool.map(play, jobs)

    print(f"\n{'arm':13} {'win':>5} {'mean bank':>11} {'mean margin':>12} {'errors':>7}")
    for a in args.arms:
        rs = [r for r in rows if r["arm"] == a]
        print(f"{a:13} {sum(1 for r in rs if r['margin'] > 0) / len(rs):>5.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f} "
              f"{sum(1 for r in rs if not r['status'].startswith('DONE')):>7}")

    cell = {}
    for r in rows:
        cell.setdefault((r["seed"], r["seat"]), {})[r["arm"]] = r
    print()
    base = args.arms[0]
    for y in args.arms[1:]:
        d = [v[base]["margin"] - v[y]["margin"] for v in cell.values() if base in v and y in v]
        if d:
            print(f"{base:12} - {y:12} {statistics.mean(d):>+10,.0f}   "
                  f"better in {sum(1 for q in d if q > 0)}/{len(d)}")


if __name__ == "__main__":
    main()
