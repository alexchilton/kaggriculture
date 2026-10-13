"""Does one of Hayashi's tapes hold up in YARN worlds, or is that why there are 13?

His published router keys on nothing but YARN_STORE: 15 keys, every one containing
it, everything else falling through to plan 0. So one tape covering all non-yarn
draws is his own design, and our earlier +50,695 was measured entirely on non-yarn
seeds. The yarn draws are where the other eleven tapes exist.

Phase A maps seeds to worlds (one mirror game each). Phase B plays, on yarn seeds
only, his single tape against the full published router, which gets to pick its
correct yarn tape.
"""
import csv, os, statistics
from multiprocessing import Pool
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ROUTE_STEP = 144
STREAM = "hay_107392777_BRUNCH_SPOT_BAKERY.json"
PUB = str(ROOT/"submission"/"shop0909"/"main.py")
MINED = str(ROOT/"submission"/"mined"/"main.py")
OPP = {"twocoins": str(ROOT/"submission"/"twocoins"/"main.py"),
       "shop0908": str(ROOT/"submission"/"shop0908"/"main.py")}

def world_of(seed):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([PUB, PUB])
    return seed, "|".join(env.steps[ROUTE_STEP][0]["observation"]["town"]["unlocked_shops"][:2])

def duel(job):
    arm, seed, opp, seat = job
    os.environ["MINED_STREAM"] = STREAM
    from kaggle_environments import make
    ours = MINED if arm == "hayashi_tape" else PUB
    pair = [ours, OPP[opp]] if seat == 0 else [OPP[opp], ours]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r=[s["reward"] for s in env.steps[-1]]
    return {"arm":arm,"seed":seed,"opponent":opp,"seat":seat,"ours":r[seat],"margin":r[seat]-r[1-seat]}

if __name__ == "__main__":
    seeds=[11+7919*i for i in range(150)]
    with Pool(5) as pool:
        print(f"phase A: mapping {len(seeds)} seeds", flush=True)
        wm=dict(pool.imap_unordered(world_of, seeds))
        yarn=[s for s,w in wm.items() if "YARN_STORE" in w]
        nony=[s for s,w in wm.items() if "YARN_STORE" not in w]
        print(f"  {len(yarn)} yarn seeds, {len(nony)} non-yarn", flush=True)
        with (ROOT/"data/logs/world_map_150.csv").open("w",newline="") as fh:
            w=csv.writer(fh); w.writerow(["seed","world"])
            for s in sorted(wm): w.writerow([s,wm[s]])
        yarn=sorted(yarn)[:12]
        jobs=[(a,s,o,seat) for a in ("hayashi_tape","published_router") for s in yarn
              for o in OPP for seat in (0,1)]
        print(f"phase B: {len(jobs)} games on {len(yarn)} yarn seeds", flush=True)
        rows=[]
        with (ROOT/"data/logs/yarn_test.csv").open("w",newline="") as fh:
            w=csv.DictWriter(fh,fieldnames=["arm","seed","opponent","seat","ours","margin"]); w.writeheader(); fh.flush()
            for i,r in enumerate(pool.imap_unordered(duel,jobs),1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i%20==0 or i==len(jobs): print(f"  {i}/{len(jobs)}",flush=True)
    print(f"\nYARN WORLDS ONLY   {'win':>6} {'mean bank':>11} {'mean margin':>12}")
    for a in ("published_router","hayashi_tape"):
        rs=[r for r in rows if r["arm"]==a]
        print(f"{a:18} {sum(1 for r in rs if r['margin']>0)/len(rs):>6.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f}")
