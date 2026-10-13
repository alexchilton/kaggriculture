"""Does a mined stream still bank when replayed blind? Per archetype.

The classification from data/logs/classify_0909_wide.log says the top is not one
kind of agent:

  SpaTaro        adaptive from turn 0        -- a recording is a best response, not a plan
  Otter Vibe     fixed 4-day opening, then adaptive
  Matthew Huang  a TAPE with repairs, 64-112 bursts of 4-7 turns that always re-sync
  Mengfei Li     diverges at turn 65

Only the tape-shaped ones should survive replay. Measuring rather than assuming.
Control is the imported Shop Router 0909 on the same matchups.
"""
import argparse
import csv
import statistics
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MINED = ROOT / "submission" / "mined"
OPPONENTS = {"shop0909": str(ROOT / "submission" / "shop0909" / "main.py"),
             "shop0908": str(ROOT / "submission" / "shop0908" / "main.py"),
             "v31": str(ROOT / "submission" / "v31" / "main.py")}


def play(job):
    stream, seed, opp, seat = job
    import os
    os.environ["MINED_STREAM"] = stream
    from kaggle_environments import make
    ours = str(MINED / "main.py") if stream != "CONTROL" else OPPONENTS["shop0909"]
    pair = [ours, OPPONENTS[opp]] if seat == 0 else [OPPONENTS[opp], ours]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r = [s["reward"] for s in env.steps[-1]]
    return {"stream": stream, "seed": seed, "opponent": opp, "seat": seat,
            "ours": r[seat], "theirs": r[1 - seat], "margin": r[seat] - r[1 - seat]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--out", default="data/logs/mined_tape_sweep.csv")
    args = ap.parse_args()
    streams = ["CONTROL"] + sorted(p.name for p in MINED.glob("*.json"))
    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(s, sd, o, seat) for s in streams for sd in seeds for o in OPPONENTS for seat in (0, 1)]
    print(f"{len(jobs)} games over {len(streams)} streams", flush=True)

    rows = []
    out = ROOT / args.out
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["stream", "seed", "opponent", "seat", "ours", "theirs", "margin"])
        w.writeheader(); fh.flush()
        with Pool(args.jobs) as pool:
            for i, r in enumerate(pool.imap_unordered(play, jobs), 1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i % 30 == 0 or i == len(jobs):
                    print(f"  {i}/{len(jobs)}", flush=True)

    print(f"\n{'stream':28} {'games':>5} {'win':>6} {'mean bank':>11} {'mean margin':>12}")
    for s in streams:
        rs = [r for r in rows if r["stream"] == s]
        if not rs:
            continue
        print(f"{s:28} {len(rs):>5} {sum(1 for r in rs if r['margin']>0)/len(rs):>6.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f}")


if __name__ == "__main__":
    main()
