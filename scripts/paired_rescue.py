"""Is the seven-turn terminal rescue worth anything? Paired, same seeds, same opponent.

E182 is the unmodified Shop Router 0909 plus a bounded planner over the last seven
turns. So the only honest comparison plays both against the SAME opponent on the
SAME seed and subtracts:

    delta = (E182 margin) - (0909 margin)

A positive mean delta is the rescue earning its place. Zero means it does nothing.
Negative means it costs, and it goes.

    .venv-sub/bin/python -u scripts/paired_rescue.py --seeds 24 --jobs 5
"""
import argparse
import csv
import statistics
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
E182 = str(ROOT / "submission" / "e182" / "main.py")
PARENT = str(ROOT / "submission" / "shop0909" / "main.py")
OPPONENTS = {"shop0908": str(ROOT / "submission" / "shop0908" / "main.py"),
             "v31": str(ROOT / "submission" / "v31" / "main.py")}


def play(job):
    seed, who, opp_name, our_seat = job
    from kaggle_environments import make
    ours = E182 if who == "e182" else PARENT
    theirs = OPPONENTS[opp_name]
    pair = [ours, theirs] if our_seat == 0 else [theirs, ours]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    rewards = [s["reward"] for s in env.steps[-1]]
    return {"seed": seed, "who": who, "opponent": opp_name, "our_seat": our_seat,
            "ours": rewards[our_seat], "theirs": rewards[1 - our_seat],
            "margin": rewards[our_seat] - rewards[1 - our_seat]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--out", default="data/logs/paired_rescue.csv")
    args = ap.parse_args()

    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(s, who, opp, seat) for s in seeds for opp in OPPONENTS
            for who in ("e182", "parent") for seat in (0, 1)]
    print(f"{len(jobs)} games", flush=True)

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with out.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["seed", "who", "opponent", "our_seat",
                                                "ours", "theirs", "margin"])
        writer.writeheader()
        fh.flush()
        with Pool(args.jobs) as pool:
            for i, row in enumerate(pool.imap_unordered(play, jobs), 1):
                writer.writerow(row)
                fh.flush()
                rows.append(row)
                if i % 20 == 0 or i == len(jobs):
                    print(f"  {i}/{len(jobs)}", flush=True)

    paired = {}
    for r in rows:
        paired.setdefault((r["seed"], r["opponent"], r["our_seat"]), {})[r["who"]] = r["margin"]
    deltas = [v["e182"] - v["parent"] for v in paired.values() if len(v) == 2]
    nonzero = [d for d in deltas if d != 0]
    print(f"\npaired games: {len(deltas)}")
    print(f"rescue changed the result in {len(nonzero)} of them")
    if deltas:
        print(f"mean delta   {statistics.mean(deltas):+,.1f}")
        print(f"median delta {statistics.median(deltas):+,.1f}")
        print(f"worst        {min(deltas):+,.0f}    best {max(deltas):+,.0f}")
        wins = sum(1 for d in deltas if d > 0)
        print(f"rescue better in {wins}, worse in {sum(1 for d in deltas if d < 0)}, "
              f"identical in {sum(1 for d in deltas if d == 0)}")


if __name__ == "__main__":
    main()
