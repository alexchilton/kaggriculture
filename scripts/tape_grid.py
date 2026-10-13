"""Every library tape in every world, so the world -> tape map can be measured.

Hayashi's map is an observation: he ran a tape in a world a few times and kept it.
Any of his 13 tapes is legal in any world. This plays all 13 over the same seeds,
seats and opponents and reports the best per world.

The leave-one-seed-out column is the guard. A world whose winner changes when one
seed is dropped was picked by that seed, not by the tape, and must keep the
default instead.
"""
import csv, os, statistics
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PICK = str(ROOT/"submission"/"hay_pick"/"main.py")
OPP = {"shop0909": str(ROOT/"submission"/"shop0909"/"main.py"),
       "v32":      str(ROOT/"submission"/"v32"/"main.py")}
N_TAPES = 13
SEEDS = [11 + 7919*i for i in range(48)]


def play(job):
    tape, seed, opp, seat = job
    os.environ["HAY_TAPE"] = str(tape)
    from kaggle_environments import make
    pair = [PICK, OPP[opp]] if seat == 0 else [OPP[opp], PICK]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    shops = []
    for step in env.steps:
        for s in (step[0]["observation"].get("town") or {}).get("unlocked_shops") or []:
            if s not in shops:
                shops.append(s)
        if len(shops) >= 2:
            break
    r = [s["reward"] for s in env.steps[-1]]
    st = [s["status"] for s in env.steps[-1]]
    return {"tape": tape, "seed": seed, "opponent": opp, "seat": seat,
            "world": "|".join(shops[:2]), "ours": r[seat],
            "margin": r[seat]-r[1-seat], "status": "/".join(st)}


if __name__ == "__main__":
    jobs = [(t, s, o, seat) for t in range(N_TAPES) for s in SEEDS
            for o in OPP for seat in (0, 1)]
    print(f"{len(jobs)} games", flush=True)
    rows = []
    out = ROOT/"data/logs/tape_grid.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["tape","seed","opponent","seat","world","ours","margin","status"])
        w.writeheader(); fh.flush()
        with Pool(6) as pool:
            for i, r in enumerate(pool.imap_unordered(play, jobs), 1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i % 100 == 0 or i == len(jobs):
                    print(f"  {i}/{len(jobs)}", flush=True)

    err = sum(1 for r in rows if not r["status"].startswith("DONE"))
    print(f"\nerrors: {err}")

    # margin by (world, tape), paired implicitly by using the same cell set
    by = defaultdict(lambda: defaultdict(list))     # world -> tape -> [(seed, margin)]
    for r in rows:
        by[r["world"]][r["tape"]].append((r["seed"], r["margin"]))

    def best(cells, drop=None):
        scores = {}
        for tape, vals in cells.items():
            keep = [m for s, m in vals if s != drop]
            if keep:
                scores[tape] = statistics.mean(keep)
        return max(scores, key=scores.get), scores

    print(f"\n{'world':30} {'n':>3} {'best':>5} {'margin':>10} {'default(0)':>11} "
          f"{'gain':>9}  {'stable':>7}")
    picks = {}
    for world in sorted(by, key=lambda w: -len(by[w][0])):
        cells = by[world]
        b, scores = best(cells)
        seeds_here = sorted({s for _, vals in cells.items() for s, _ in vals})
        flips = sum(1 for d in seeds_here if best(cells, drop=d)[0] != b)
        stable = flips == 0
        picks[world] = b if stable else 0
        print(f"{world:30} {len(cells[0]):>3} {b:>5} {scores[b]:>10,.0f} "
              f"{scores[0]:>11,.0f} {scores[b]-scores[0]:>+9,.0f}  "
              f"{'yes' if stable else f'no({flips})':>7}")

    slots = {v: k for k, v in
             __import__("json").loads((ROOT/"submission"/"hay_pick"/"slots.json").read_text()).items()}
    print("\nmeasured map (stable worlds only):")
    for world, t in sorted(picks.items()):
        if t:
            print(f'  "{world}": "{slots[t]}",')
    (ROOT/"data/logs/tape_grid_picks.json").write_text(
        __import__("json").dumps({w: slots[t] for w, t in picks.items()}, indent=2, sort_keys=True))
    print(f"\nwrote {ROOT/'data/logs/tape_grid_picks.json'}")
