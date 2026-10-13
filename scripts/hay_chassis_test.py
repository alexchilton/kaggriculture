"""Does the E184 chassis add value on top of Hayashi's live tape?

Three arms, same opponents, same seeds:
  twocoins       E184 chassis over the PUBLISHED 13 tapes (what we submitted today)
  hay_blind      Hayashi's live tape replayed raw, no chassis, no repairs
  hay_chassis    E184 chassis with all 13 routes replaced by that same live tape

hay_chassis - hay_blind is the chassis's contribution.
hay_blind - twocoins is the tape's contribution.
"""
import csv, os, statistics
from multiprocessing import Pool
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
STREAM = "hay_107392777_BRUNCH_SPOT_BAKERY.json"
ARMS = {"twocoins_published": str(ROOT/"submission"/"twocoins"/"main.py"),
        "hay_blind": str(ROOT/"submission"/"mined"/"main.py"),
        "hay_chassis": str(ROOT/"submission"/"hay_chassis"/"main.py")}
OPP = {"shop0909": str(ROOT/"submission"/"shop0909"/"main.py"),
       "shop0908": str(ROOT/"submission"/"shop0908"/"main.py"),
       "v32": str(ROOT/"submission"/"v32"/"main.py")}

def play(job):
    arm, seed, opp, seat = job
    os.environ["MINED_STREAM"] = STREAM
    from kaggle_environments import make
    pair = [ARMS[arm], OPP[opp]] if seat == 0 else [OPP[opp], ARMS[arm]]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r=[s["reward"] for s in env.steps[-1]]; st=[s["status"] for s in env.steps[-1]]
    return {"arm":arm,"seed":seed,"opponent":opp,"seat":seat,"ours":r[seat],
            "margin":r[seat]-r[1-seat],"status":"/".join(st)}

if __name__ == "__main__":
    seeds=[11+7919*i for i in range(8)]
    jobs=[(a,s,o,seat) for a in ARMS for s in seeds for o in OPP for seat in (0,1)]
    print(f"{len(jobs)} games", flush=True)
    rows=[]
    with (ROOT/"data/logs/hay_chassis_test.csv").open("w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=["arm","seed","opponent","seat","ours","margin","status"]); w.writeheader(); fh.flush()
        with Pool(5) as pool:
            for i,r in enumerate(pool.imap_unordered(play,jobs),1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i%30==0 or i==len(jobs): print(f"  {i}/{len(jobs)}",flush=True)
    pair={}
    for r in rows: pair.setdefault((r["seed"],r["opponent"],r["seat"]),{})[r["arm"]]=r
    print(f"\n{'arm':22} {'win':>6} {'mean bank':>11} {'mean margin':>12} {'errors':>7}")
    for a in ARMS:
        rs=[r for r in rows if r["arm"]==a]
        err=sum(1 for r in rs if not r["status"].startswith("DONE"))
        print(f"{a:22} {sum(1 for r in rs if r['margin']>0)/len(rs):>6.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f} {err:>7}")
    def delta(x,y):
        d=[v[x]["margin"]-v[y]["margin"] for v in pair.values() if x in v and y in v]
        return statistics.mean(d), sum(1 for q in d if q>0), len(d)
    for x,y,label in (("hay_chassis","hay_blind","chassis on top of his tape"),
                      ("hay_blind","twocoins_published","his tape vs the published tapes"),
                      ("hay_chassis","twocoins_published","both changes together")):
        m,better,n=delta(x,y)
        print(f"\n{label:38} {m:>+12,.0f}   better in {better}/{n}")
