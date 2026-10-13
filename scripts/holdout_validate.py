"""Validate the measured map on games that had no part in choosing it.

Held out two ways:
  seeds       the grid used seeds 1..8 per world; this uses 9..12
  opponents   the grid used shop0909 only; this uses v32 and shop0908

Arms: hay_router  (Hayashi's own world -> tape map, 10 tapes)
      hay_router2 (the measured map, 4 tapes)
      twocoins    (the published tapes, what is on the ladder)

What would disprove the map: if hay_router2 - hay_router falls below about $1,000
or flips sign here, the 17 picks were seed noise and his map should stand.
"""
import argparse, csv, os, statistics
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS = {"twocoins":    str(ROOT/"submission"/"twocoins"/"main.py"),
        "hay_router":  str(ROOT/"submission"/"hay_router"/"main.py"),
        "hay_router2": str(ROOT/"submission"/"hay_router2"/"main.py")}
OPP = {"v32":      str(ROOT/"submission"/"v32"/"main.py"),
       "shop0908": str(ROOT/"submission"/"shop0908"/"main.py")}
SKIP, TAKE = 8, 4
OUT = ROOT/"data/logs/holdout_validate.csv"
FIELDS = ["arm", "world", "seed", "opponent", "seat", "ours", "margin", "status"]


def play(job):
    arm, world, seed, opp, seat = job
    from kaggle_environments import make
    pair = [ARMS[arm], OPP[opp]] if seat == 0 else [OPP[opp], ARMS[arm]]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    r = [s["reward"] for s in env.steps[-1]]
    st = [s["status"] for s in env.steps[-1]]
    return {"arm": arm, "world": world, "seed": seed, "opponent": opp, "seat": seat,
            "ours": r[seat], "margin": r[seat]-r[1-seat], "status": "/".join(st)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    by_world = defaultdict(list)
    for r in csv.DictReader((ROOT/"data/logs/seed_worlds.csv").open()):
        if int(r["n_shops"]) == 2:
            by_world[r["world"]].append(int(r["seed"]))
    held = {w: sorted(s)[SKIP:SKIP+TAKE] for w, s in by_world.items()}
    thin = [w for w, s in held.items() if len(s) < TAKE]
    print(f"{len(held)} worlds, {len(thin)} with fewer than {TAKE} held-out seeds", flush=True)

    jobs = [(a, w, s, o, seat) for a in ARMS for w, seeds in held.items()
            for s in seeds for o in OPP for seat in (0, 1)]
    done = set()
    if args.resume and OUT.exists():
        for r in csv.DictReader(OUT.open()):
            done.add((r["arm"], r["world"], int(r["seed"]), r["opponent"], int(r["seat"])))
        print(f"resumed: {len(done)} games already played", flush=True)
    jobs = [j for j in jobs if j not in done]
    print(f"{len(jobs)} games to play", flush=True)

    rows = []
    with OUT.open("a" if done else "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if not done:
            w.writeheader(); fh.flush()
        with Pool(6) as pool:
            for i, r in enumerate(pool.imap_unordered(play, jobs), 1):
                w.writerow(r); fh.flush(); rows.append(r)
                if i % 200 == 0 or i == len(jobs):
                    print(f"  {i}/{len(jobs)}", flush=True)

    rows = [dict(r, seed=int(r["seed"]), seat=int(r["seat"]), margin=float(r["margin"]),
                 ours=float(r["ours"])) for r in csv.DictReader(OUT.open())]
    err = sum(1 for r in rows if not r["status"].startswith("DONE"))
    print(f"\n{len(rows)} games, {err} errors")
    print(f"\n{'arm':12} {'win':>6} {'mean bank':>11} {'mean margin':>12}")
    for a in ARMS:
        rs = [r for r in rows if r["arm"] == a]
        if not rs: continue
        print(f"{a:12} {sum(1 for r in rs if r['margin']>0)/len(rs):>6.2f} "
              f"{statistics.mean(r['ours'] for r in rs):>11,.0f} "
              f"{statistics.mean(r['margin'] for r in rs):>+12,.0f}")

    cell = defaultdict(dict)
    for r in rows:
        cell[(r["world"], r["seed"], r["opponent"], r["seat"])][r["arm"]] = r
    def delta(x, y, keep=lambda k: True):
        d = [v[x]["margin"]-v[y]["margin"] for k, v in cell.items()
             if x in v and y in v and keep(k)]
        return (statistics.mean(d) if d else 0.0), sum(1 for q in d if q > 0), len(d)
    routed = set(__import__("json").loads((ROOT/"data/logs/picks_vs_best.json").read_text()))
    print()
    for x, y in (("hay_router2","hay_router"), ("hay_router2","twocoins"), ("hay_router","twocoins")):
        for label, keep in (("all", lambda k: True),
                            ("routed worlds", lambda k: k[0] in routed),
                            ("default worlds", lambda k: k[0] not in routed)):
            m, b, n = delta(x, y, keep)
            print(f"{x:12} - {y:11} {label:15} {m:>+10,.0f}  better in {b}/{n}")
        print()
    for opp in OPP:
        m, b, n = delta("hay_router2", "hay_router", lambda k: k[2] == opp)
        print(f"hay_router2 - hay_router  vs {opp:10} {m:>+10,.0f}  better in {b}/{n}")


if __name__ == "__main__":
    main()
