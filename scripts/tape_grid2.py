"""All 13 library tapes in all 64 worlds, seeds allocated by world.

The first grid drew seeds at random and got 42 worlds with one seed each, which
cannot decide anything. The world at step 144 is a pure function of the seed
(measured: independent of tape, opponent and seat), so seeds are grouped by world
here and a fixed number is spent in each.

Selection runs against ONE opponent and the first SEEDS_PER_WORLD seeds. The
remaining seeds and the other opponents are the holdout -- picking and checking on
the same games is how a null becomes a win.

Resumable: every finished game is appended to the CSV and reloaded on --resume.
"""
import argparse, csv, os
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPP = str(ROOT/"submission"/"shop0909"/"main.py")
PICK = str(ROOT/"submission"/"hay_pick"/"main.py")
N_TAPES = 13
SEEDS_PER_WORLD = 8
ROUTE_STEP = 144
OUT = ROOT/"data/logs/tape_grid2.csv"
FIELDS = ["world", "seed", "tape", "seat", "world_seen", "ours", "margin", "status"]


def play(job):
    world, seed, tape, seat = job
    os.environ["HAY_TAPE"] = str(tape)
    from kaggle_environments import make
    pair = [PICK, OPP] if seat == 0 else [OPP, PICK]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    obs = env.steps[ROUTE_STEP][seat]["observation"]
    seen = "|".join(((obs.get("town") or {}).get("unlocked_shops") or [])[:2])
    r = [s["reward"] for s in env.steps[-1]]
    st = [s["status"] for s in env.steps[-1]]
    return {"world": world, "seed": seed, "tape": tape, "seat": seat, "world_seen": seen,
            "ours": r[seat], "margin": r[seat]-r[1-seat], "status": "/".join(st)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--seeds-per-world", type=int, default=SEEDS_PER_WORLD)
    args = ap.parse_args()

    by_world = defaultdict(list)
    for r in csv.DictReader((ROOT/"data/logs/seed_worlds.csv").open()):
        if int(r["n_shops"]) == 2:
            by_world[r["world"]].append(int(r["seed"]))
    chosen = {w: sorted(s)[:args.seeds_per_world] for w, s in by_world.items()}
    thin = {w: len(s) for w, s in chosen.items() if len(s) < args.seeds_per_world}
    print(f"{len(chosen)} worlds; {len(thin)} have fewer than {args.seeds_per_world} seeds", flush=True)
    if thin:
        print("  thin:", ", ".join(f"{w}={n}" for w, n in sorted(thin.items(), key=lambda kv: kv[1])), flush=True)

    jobs = [(w, s, t, seat) for w, seeds in chosen.items() for s in seeds
            for t in range(N_TAPES) for seat in (0, 1)]

    done = set()
    if args.resume and OUT.exists():
        for r in csv.DictReader(OUT.open()):
            done.add((r["world"], int(r["seed"]), int(r["tape"]), int(r["seat"])))
        print(f"resumed: {len(done)} games already played", flush=True)
    jobs = [j for j in jobs if j not in done]
    print(f"{len(jobs)} games to play", flush=True)

    with OUT.open("a" if done else "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if not done:
            w.writeheader(); fh.flush()
        with Pool(6) as pool:
            for i, r in enumerate(pool.imap_unordered(play, jobs), 1):
                w.writerow(r); fh.flush()
                if i % 200 == 0 or i == len(jobs):
                    print(f"  {i}/{len(jobs)}", flush=True)
    print("GRID_DONE", flush=True)


if __name__ == "__main__":
    main()
