"""v32 against v31, same seed, same seat, same opponent. Paired delta only.

The author reports +6 wins and about +62 mean own cash over 1,536 games, from a
final-day route that avoids one hire when a paid worker can finish the harvest
and return in time. This checks that on our seeds before spending a submission.
"""
import csv, statistics
from multiprocessing import Pool
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ARMS = {"v32": str(ROOT/"submission"/"v32"/"main.py")}
for _p in sorted((ROOT/"submission"/"v32_toggle").glob("*.py")): ARMS[_p.stem] = str(_p)
OPP = {"shop0909": str(ROOT/"submission"/"shop0909"/"main.py"),
       "shop0908": str(ROOT/"submission"/"shop0908"/"main.py")}

def play(job):
    arm, seed, opp, seat = job
    from kaggle_environments import make
    pair = [ARMS[arm], OPP[opp]] if seat == 0 else [OPP[opp], ARMS[arm]]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r = [s["reward"] for s in env.steps[-1]]
    return {"arm": arm, "seed": seed, "opponent": opp, "seat": seat,
            "ours": r[seat], "margin": r[seat]-r[1-seat]}

if __name__ == "__main__":
    seeds = [11 + 7919*i for i in range(10)]
    jobs = [(a, s, o, seat) for a in ARMS for s in seeds for o in OPP for seat in (0,1)]
    print(f"{len(jobs)} games", flush=True)
    rows=[]
    with (ROOT/"data/logs/v32_toggle.csv").open("w", newline="") as fh:
        w=csv.DictWriter(fh, fieldnames=["arm","seed","opponent","seat","ours","margin"]); w.writeheader(); fh.flush()
        with Pool(5) as pool:
            for i,r in enumerate(pool.imap_unordered(play, jobs),1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i%20==0 or i==len(jobs): print(f"  {i}/{len(jobs)}", flush=True)
    pair={}
    for r in rows: pair.setdefault((r["seed"],r["opponent"],r["seat"]),{})[r["arm"]]=r
    print()
    for a in ARMS:
        rs=[r for r in rows if r["arm"]==a]
        print(f"{a:16} win {sum(1 for r in rs if r['margin']>0)/len(rs):.2f}  "
              f"mean bank {statistics.mean(r['ours'] for r in rs):>9,.0f}  "
              f"mean margin {statistics.mean(r['margin'] for r in rs):>+9,.0f}")
    print()
    for a in ARMS:
        if a=="v32": continue
        d=[v[a]["margin"]-v["v32"]["margin"] for v in pair.values() if a in v and "v32" in v]
        print(f"{a:16} paired vs v32: n={len(d)}  mean delta {statistics.mean(d):+,.1f}  "
              f"better {sum(1 for x in d if x>0)}  worse {sum(1 for x in d if x<0)}  same {sum(1 for x in d if x==0)}")
