"""Gluzdov's sale window against v32, and its horizon swept 1/2/3.

Same 13 yhay81 tapes underneath every arm and the same opponents, so the only
difference is the chassis and the sale horizon.
"""
import csv, statistics
from multiprocessing import Pool
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ARMS = {"v32": str(ROOT/"submission"/"v32"/"main.py"),
        "twocoins_h2": str(ROOT/"submission"/"twocoins_h2"/"main.py"),
        "t4": str(ROOT/"submission"/"t4"/"main.py"),
        "e182": str(ROOT/"submission"/"e182"/"main.py")}
# Passive tapes vs a preempting chassis: T4 escalates to lead-2 only when it
# observes the opponent preempting, so the opponent's own sale policy is the
# variable that decides whether its gate fires.
OPP = {"passive_0909": str(ROOT/"submission"/"shop0909"/"main.py"),
       "preempt_twocoins": str(ROOT/"submission"/"twocoins_h2"/"main.py"),
       "preempt_t4": str(ROOT/"submission"/"t4"/"main.py")}

def play(job):
    arm, seed, opp, seat = job
    from kaggle_environments import make
    pair = [ARMS[arm], OPP[opp]] if seat == 0 else [OPP[opp], ARMS[arm]]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    try:
        env.run(pair)
        r=[s["reward"] for s in env.steps[-1]]; st=[s["status"] for s in env.steps[-1]]
    except Exception as e:
        return {"arm":arm,"seed":seed,"opponent":opp,"seat":seat,"ours":0,"margin":0,"status":str(e)[:40]}
    return {"arm":arm,"seed":seed,"opponent":opp,"seat":seat,"ours":r[seat],
            "margin":r[seat]-r[1-seat],"status":"/".join(st)}

if __name__ == "__main__":
    seeds=[11+7919*i for i in range(10)]
    jobs=[(a,s,o,seat) for a in ARMS for s in seeds for o in OPP for seat in (0,1)]
    print(f"{len(jobs)} games", flush=True)
    rows=[]
    with (ROOT/"data/logs/t4_vs_preempt.csv").open("w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=["arm","seed","opponent","seat","ours","margin","status"]); w.writeheader(); fh.flush()
        with Pool(5) as pool:
            for i,r in enumerate(pool.imap_unordered(play,jobs),1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i%25==0 or i==len(jobs): print(f"  {i}/{len(jobs)}",flush=True)
    pair={}
    for r in rows: pair.setdefault((r["seed"],r["opponent"],r["seat"]),{})[r["arm"]]=r
    print(f"\n{'arm':14} {'win':>6} {'mean bank':>11} {'mean margin':>12} {'paired vs v32':>15} {'errors':>7}")
    for a in ARMS:
        rs=[r for r in rows if r["arm"]==a]
        err=sum(1 for r in rs if not r["status"].startswith("DONE"))
        d=[v[a]["margin"]-v["v32"]["margin"] for v in pair.values() if a in v and "v32" in v]
        dd="" if a=="v32" else f"{statistics.mean(d):>+15,.1f}"
        print(f"{a:14} {sum(1 for r in rs if r['margin']>0)/len(rs):>6.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f} {dd} {err:>7}")
