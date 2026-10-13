"""Record which world each seed draws, so grid seeds can be allocated by world.

The world is the first two shops the town has unlocked at step 144, which is the
step the router keys on. Measured tape-independent (the first 144 turns of all 13
library tapes are identical) and measured independent of opponent and seat, so one
game per seed labels it.
"""
import argparse, csv, os
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
N_SEEDS = 300
ROUTE_STEP = 144


def label(seed):
    os.environ["HAY_TAPE"] = "0"
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([str(ROOT/"submission"/"hay_pick"/"main.py"), str(ROOT/"submission"/"shop0909"/"main.py")])
    obs = env.steps[ROUTE_STEP][0]["observation"]
    shops = ((obs.get("town") or {}).get("unlocked_shops") or [])[:2]
    return {"seed": seed, "world": "|".join(shops), "n_shops": len(shops)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=N_SEEDS)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    out = ROOT/"data/logs/seed_worlds.csv"
    rows, done = [], set()
    if args.resume and out.exists():
        rows = [{"seed": int(r["seed"]), "world": r["world"], "n_shops": int(r["n_shops"])}
                for r in csv.DictReader(out.open())]
        done = {r["seed"] for r in rows}
        print(f"resumed: {len(done)} seeds already labelled", flush=True)
    seeds = [s for s in (11 + 7919*i for i in range(args.n)) if s not in done]
    print(f"{len(seeds)} seeds to label", flush=True)
    with out.open("a" if done else "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["seed", "world", "n_shops"])
        if not done:
            w.writeheader()
        fh.flush()
        with Pool(6) as pool:
            for i, r in enumerate(pool.imap_unordered(label, seeds), 1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i % 25 == 0 or i == len(seeds):
                    print(f"  {i}/{len(seeds)}", flush=True)
    short = sum(1 for r in rows if r["n_shops"] < 2)
    counts = Counter(r["world"] for r in rows if r["n_shops"] == 2)
    print(f"\n{len(rows)} seeds, {short} with fewer than two shops at step {ROUTE_STEP}")
    print(f"{len(counts)} distinct worlds\n")
    print(f"{'world':32} {'seeds':>5}")
    for world, n in counts.most_common():
        print(f"{world:32} {n:>5}")
    print(f"\nwrote {out}")
