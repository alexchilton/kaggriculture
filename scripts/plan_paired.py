"""The planner on one plan versus the planner on another, paired on seed and seat.

The planner's EXECUTOR is not what is being measured here -- it is byte-identical between the
arms, because both artifacts are built from the same four modules by
`scripts/build_planner_submission.py` and differ only in the embedded `_PLAN_JSON`. So any
difference is the PLAN, which is the thing under test: カワシギ's August rows (engine 1.32.6,
`townCenterSellInterval` 12) against SpaTaro's, extracted from submission 56114097.

Paired, not averaged: the same seed played from the same seat by every arm, so the margin
difference per cell is a difference between two plans on one board and not two samples of the
world distribution. `hay_router` and `twocoins` ride along as the scale -- the tape arms already
measured on these seeds (+76,011 and +4,999 mean margin), so a plan arm can be read against a
number that is known rather than against itself.
"""
import argparse, csv, statistics
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS = {"hay_router":   ROOT / "submission/hay_router/main.py",
        "twocoins":     ROOT / "submission/twocoins/main.py",
        "planner_kawa": ROOT / "submission/planner_pure/main.py",
        "planner_spa":  ROOT / "submission/planner_spa/main.py"}
OPP = {"shop0909": ROOT / "submission/shop0909/main.py",
       "v32":      ROOT / "submission/v32/main.py"}
OUT = ROOT / "data/logs/plan_paired.csv"
FIELDS = ["arm", "seed", "opponent", "seat", "ours", "margin", "status"]


def play(job):
    arm, seed, opp, seat = job
    from kaggle_environments import make
    pair = [str(ARMS[arm]), str(OPP[opp])] if seat == 0 else [str(OPP[opp]), str(ARMS[arm])]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r = [s["reward"] for s in env.steps[-1]]
    ours = r[seat] if r[seat] is not None else 0
    them = r[1 - seat] if r[1 - seat] is not None else 0
    return {"arm": arm, "seed": seed, "opponent": opp, "seat": seat, "ours": ours,
            "margin": ours - them,
            "status": "/".join(str(s["status"]) for s in env.steps[-1])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    ap.add_argument("--opponents", nargs="+", default=["shop0909"])
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--procs", type=int, default=5)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    for a in args.arms:
        if not ARMS[a].exists():
            raise SystemExit(f"{a}: {ARMS[a]} does not exist -- build it first")

    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(a, s, o, t) for a in args.arms for s in seeds for o in args.opponents for t in (0, 1)]

    done, rows = set(), []
    if args.resume and OUT.exists():
        for r in csv.DictReader(OUT.open()):
            key = (r["arm"], int(r["seed"]), r["opponent"], int(r["seat"]))
            done.add(key)
            rows.append({**r, "seed": int(r["seed"]), "seat": int(r["seat"]),
                         "ours": float(r["ours"]), "margin": float(r["margin"])})
        jobs = [j for j in jobs if j not in done]
        print(f"resumed: {len(done)} games already played")

    print(f"{len(jobs)} games to play", flush=True)
    if jobs:
        with Pool(args.procs) as pool:
            for i, r in enumerate(pool.imap_unordered(play, jobs), 1):
                rows.append(r)
                if i % 16 == 0 or i == len(jobs):
                    print(f"  {i}/{len(jobs)}", flush=True)
                    with OUT.open("w", newline="") as fh:   # every batch, so a crash is cheap
                        w = csv.DictWriter(fh, FIELDS); w.writeheader(); w.writerows(rows)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, FIELDS); w.writeheader(); w.writerows(rows)

    print(f"\n{len(rows)} games, "
          f"{sum(1 for r in rows if not str(r['status']).startswith('DONE'))} errors\n")
    print(f"{'arm':14} {'win':>5} {'mean bank':>11} {'mean margin':>12} {'errors':>7}")
    for a in args.arms:
        rs = [r for r in rows if r["arm"] == a]
        if not rs:
            continue
        print(f"{a:14} {sum(1 for r in rs if r['margin'] > 0) / len(rs):>5.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f} "
              f"{sum(1 for r in rs if not str(r['status']).startswith('DONE')):>7}")

    cell = {}
    for r in rows:
        cell.setdefault((r["seed"], r["opponent"], r["seat"]), {})[r["arm"]] = r
    print()
    for x, y in (("planner_spa", "planner_kawa"), ("planner_spa", "hay_router"),
                 ("planner_kawa", "hay_router"), ("planner_spa", "twocoins")):
        d = [v[x]["margin"] - v[y]["margin"] for v in cell.values() if x in v and y in v]
        if d:
            print(f"{x:13} - {y:13} {statistics.mean(d):>+10,.0f}  "
                  f"better in {sum(1 for q in d if q > 0)}/{len(d)}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
