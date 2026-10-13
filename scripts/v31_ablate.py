"""What is each of v31's market layers worth? Ablate one at a time.

v31 carries nine layers over its tape spine; ours carries three. Turning one off
and replaying the same seeds against the same opponent prices that layer. This
measures THEIR agent, to find out which layer is worth porting onto ours.
"""
import csv, statistics
from multiprocessing import Pool
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ARMS = {"v31_full": str(ROOT / "submission" / "v31" / "main.py")}
for p in sorted((ROOT / "submission" / "v219_tune").glob("*.py")):
    ARMS[p.stem] = str(p)
OPP = {"shop0909": str(ROOT / "submission" / "shop0909" / "main.py"),
       "shop0908": str(ROOT / "submission" / "shop0908" / "main.py")}

def play(job):
    arm, seed, opp, seat = job
    from kaggle_environments import make
    pair = [ARMS[arm], OPP[opp]] if seat == 0 else [OPP[opp], ARMS[arm]]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r = [s["reward"] for s in env.steps[-1]]
    return {"arm": arm, "seed": seed, "opponent": opp, "seat": seat,
            "ours": r[seat], "theirs": r[1-seat], "margin": r[seat]-r[1-seat]}

if __name__ == "__main__":
    seeds = [11 + 7919*i for i in range(8)]
    jobs = [(a, s, o, seat) for a in ARMS for s in seeds for o in OPP for seat in (0,1)]
    print(f"{len(jobs)} games, {len(ARMS)} arms", flush=True)
    rows=[]
    with (ROOT/"data/logs/v219_tune.csv").open("w", newline="") as fh:
        w=csv.DictWriter(fh, fieldnames=["arm","seed","opponent","seat","ours","theirs","margin"])
        w.writeheader(); fh.flush()
        with Pool(5) as pool:
            for i,r in enumerate(pool.imap_unordered(play, jobs),1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i%25==0 or i==len(jobs): print(f"  {i}/{len(jobs)}", flush=True)
    base=None
    print(f"\n{'arm':18} {'win':>6} {'mean bank':>11} {'mean margin':>12} {'layer worth':>12}")
    for a in ARMS:
        rs=[r for r in rows if r["arm"]==a]
        m=statistics.mean(r["margin"] for r in rs)
        if a=="v31_full": base=m
        worth = "" if a=="v31_full" else f"{base-m:>+12,.0f}"
        print(f"{a:18} {sum(1 for r in rs if r['margin']>0)/len(rs):>6.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} {m:>+12,.0f} {worth}")
