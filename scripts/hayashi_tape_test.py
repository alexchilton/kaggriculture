"""Do Hayashi's LIVE tapes beat the 13 he published?

He replays with only 26 of 719 turns of deviation inside one world, so his stream
is a tape, not an adaptive trace. Mining failed this afternoon on SpaTaro (0 wins
in 30) precisely because SpaTaro is adaptive; this is the same test on an agent
that is not.

Control is the published tape the router would have picked, run through the same
blind-replay harness so the comparison is like for like.
"""
import csv, os, statistics
from multiprocessing import Pool
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
MINED = ROOT / "submission" / "mined"
OPP = {"shop0909": str(ROOT/"submission"/"shop0909"/"main.py"),
       "shop0908": str(ROOT/"submission"/"shop0908"/"main.py"),
       "v32": str(ROOT/"submission"/"v32"/"main.py")}

def play(job):
    stream, seed, opp, seat = job
    os.environ["MINED_STREAM"] = stream
    from kaggle_environments import make
    ours = str(MINED/"main.py")
    pair = [ours, OPP[opp]] if seat == 0 else [OPP[opp], ours]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r = [s["reward"] for s in env.steps[-1]]
    return {"stream": stream, "seed": seed, "opponent": opp, "seat": seat,
            "ours": r[seat], "margin": r[seat]-r[1-seat]}

if __name__ == "__main__":
    streams = sorted(p.name for p in MINED.glob("hay_*.json"))
    # published-tape control, replayed by the same blind harness
    import json
    json.dump(json.load(open(ROOT/"submission"/"shop0909"/"actions.json"))[0],
              open(MINED/"published_tape0.json","w"))
    streams = ["published_tape0.json"] + streams
    seeds = [11+7919*i for i in range(4)]
    jobs = [(s, sd, o, seat) for s in streams for sd in seeds for o in OPP for seat in (0,1)]
    print(f"{len(jobs)} games over {len(streams)} tapes", flush=True)
    rows=[]
    with (ROOT/"data/logs/hayashi_tape_test.csv").open("w", newline="") as fh:
        w=csv.DictWriter(fh, fieldnames=["stream","seed","opponent","seat","ours","margin"]); w.writeheader(); fh.flush()
        with Pool(5) as pool:
            for i,r in enumerate(pool.imap_unordered(play, jobs),1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i%25==0 or i==len(jobs): print(f"  {i}/{len(jobs)}", flush=True)
    print(f"\n{'tape':42} {'win':>6} {'mean bank':>11} {'mean margin':>12}")
    for s in streams:
        rs=[r for r in rows if r["stream"]==s]
        print(f"{s[:42]:42} {sum(1 for r in rs if r['margin']>0)/len(rs):>6.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f}")
