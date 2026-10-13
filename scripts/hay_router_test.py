"""Does routing over Hayashi's 13 live tapes beat replaying his one tape, and
beat the published 13?

  twocoins     E184 chassis over the PUBLISHED 13 tapes   (what is on the ladder)
  hay_one      E184 chassis, all 13 routes = his ONE live tape (today's best)
  hay_router   E184 chassis over his 13 live tapes, world-keyed

hay_router - hay_one is what the routing buys. It can only pay in worlds where
the key selects something other than the default, so the split by world is the
result, not the pooled mean.
"""
import csv, os, statistics
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS = {"twocoins":   str(ROOT/"submission"/"twocoins"/"main.py"),
        "hay_one":    str(ROOT/"submission"/"hay_chassis"/"main.py"),
        "hay_router": str(ROOT/"submission"/"hay_router"/"main.py")}
OPP = {"shop0909": str(ROOT/"submission"/"shop0909"/"main.py"),
       "shop0908": str(ROOT/"submission"/"shop0908"/"main.py"),
       "v32":      str(ROOT/"submission"/"v32"/"main.py")}


def play(job):
    arm, seed, opp, seat = job
    from kaggle_environments import make
    pair = [ARMS[arm], OPP[opp]] if seat == 0 else [OPP[opp], ARMS[arm]]
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
    return {"arm": arm, "seed": seed, "opponent": opp, "seat": seat,
            "world": "|".join(shops[:2]), "ours": r[seat],
            "margin": r[seat]-r[1-seat], "status": "/".join(st)}


if __name__ == "__main__":
    seeds = [11 + 7919*i for i in range(16)]
    jobs = [(a, s, o, seat) for a in ARMS for s in seeds for o in OPP for seat in (0, 1)]
    print(f"{len(jobs)} games", flush=True)
    rows = []
    with (ROOT/"data/logs/hay_router_test.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["arm","seed","opponent","seat","world","ours","margin","status"])
        w.writeheader(); fh.flush()
        with Pool(6) as pool:
            for i, r in enumerate(pool.imap_unordered(play, jobs), 1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i % 24 == 0 or i == len(jobs):
                    print(f"  {i}/{len(jobs)}", flush=True)

    print(f"\n{'arm':12} {'win':>6} {'mean bank':>11} {'mean margin':>12} {'errors':>7}")
    for a in ARMS:
        rs = [r for r in rows if r["arm"] == a]
        err = sum(1 for r in rs if not r["status"].startswith("DONE"))
        print(f"{a:12} {sum(1 for r in rs if r['margin']>0)/len(rs):>6.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f} {err:>7}")

    pair = defaultdict(dict)
    for r in rows:
        pair[(r["seed"], r["opponent"], r["seat"])][r["arm"]] = r

    def delta(x, y, keep=lambda v: True):
        d = [v[x]["margin"]-v[y]["margin"] for v in pair.values() if x in v and y in v and keep(v)]
        return (statistics.mean(d) if d else 0.0), sum(1 for q in d if q > 0), len(d)

    yarn = lambda v: "YARN_STORE" in v["twocoins"]["world"]
    for x, y in (("hay_router","hay_one"), ("hay_router","twocoins"), ("hay_one","twocoins")):
        for label, keep in (("all", lambda v: True), ("yarn", yarn),
                            ("non-yarn", lambda v: not yarn(v))):
            m, better, n = delta(x, y, keep)
            print(f"{x:11} - {y:9} {label:9} {m:>+12,.0f}   better in {better}/{n}")
        print()

    worlds = defaultdict(list)
    for v in pair.values():
        if "hay_router" in v and "hay_one" in v:
            worlds[v["twocoins"]["world"]].append(v["hay_router"]["margin"]-v["hay_one"]["margin"])
    print(f"{'world':34} {'n':>3} {'router - one tape':>18}")
    for wname, ds in sorted(worlds.items(), key=lambda kv: -statistics.mean(kv[1])):
        print(f"{wname:34} {len(ds):>3} {statistics.mean(ds):>+18,.0f}")
