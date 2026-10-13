"""Does handing our planner a strong tape board beat letting the tape finish?

Every arm plays the SAME opening, so the only difference is who plays days N..29.
The control is the unmodified tape playing all 30 days. Opponent is fixed.

    .venv-sub/bin/python -u scripts/hybrid_sweep.py --seeds 10 --jobs 5
"""
import argparse
import csv
import statistics
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAPE = str(ROOT / "submission" / "shop0909" / "main.py")
ARMS = {"tape(control)": TAPE,
        "planner_only": str(ROOT / "submission" / "main_own.py"),
        "hybrid_d6": str(ROOT / "submission" / "hybrid_d6.py"),
        "hybrid_d12": str(ROOT / "submission" / "hybrid_d12.py"),
        "hybrid_d18": str(ROOT / "submission" / "hybrid_d18.py"),
        "hybrid_d24": str(ROOT / "submission" / "hybrid_d24.py")}
OPPONENTS = {"shop0908": str(ROOT / "submission" / "shop0908" / "main.py"),
             "v31": str(ROOT / "submission" / "v31" / "main.py")}


def play(job):
    seed, arm, opp, seat = job
    from kaggle_environments import make
    pair = [ARMS[arm], OPPONENTS[opp]] if seat == 0 else [OPPONENTS[opp], ARMS[arm]]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    try:
        env.run(pair)
        rewards = [s["reward"] for s in env.steps[-1]]
        status = [s["status"] for s in env.steps[-1]]
    except Exception as exc:                      # a crashed arm is a result, not a stop
        return {"seed": seed, "arm": arm, "opponent": opp, "seat": seat,
                "ours": 0, "theirs": 0, "margin": 0, "status": f"ERROR {exc}"[:60]}
    return {"seed": seed, "arm": arm, "opponent": opp, "seat": seat,
            "ours": rewards[seat], "theirs": rewards[1 - seat],
            "margin": rewards[seat] - rewards[1 - seat], "status": "/".join(status)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--out", default="data/logs/hybrid_sweep.csv")
    args = ap.parse_args()
    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(s, a, o, seat) for s in seeds for a in ARMS for o in OPPONENTS for seat in (0, 1)]
    print(f"{len(jobs)} games", flush=True)

    out = ROOT / args.out
    rows = []
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["seed", "arm", "opponent", "seat", "ours", "theirs",
                                           "margin", "status"])
        w.writeheader(); fh.flush()
        with Pool(args.jobs) as pool:
            for i, r in enumerate(pool.imap_unordered(play, jobs), 1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i % 20 == 0 or i == len(jobs):
                    print(f"  {i}/{len(jobs)}", flush=True)

    print(f"\n{'arm':16} {'games':>5} {'win rate':>9} {'mean margin':>13} {'mean bank':>11} {'errors':>7}")
    for arm in ARMS:
        rs = [r for r in rows if r["arm"] == arm]
        ok = [r for r in rs if r["status"].startswith("DONE")]
        err = len(rs) - len(ok)
        if not ok:
            print(f"{arm:16} {len(rs):>5} {'-':>9} {'-':>13} {'-':>11} {err:>7}")
            continue
        wr = sum(1 for r in ok if r["margin"] > 0) / len(ok)
        print(f"{arm:16} {len(ok):>5} {wr:>8.2f} {statistics.mean(r['margin'] for r in ok):>+13,.0f} "
              f"{statistics.mean(r['ours'] for r in ok):>11,.0f} {err:>7}")


if __name__ == "__main__":
    main()
