"""What the planner is handed at the tape's last day, against what HE had there.

If the bank and the shed at the handover are his, the planner has what it needs and any failure
after is the planner's. If they are not, the failure is inherited and no amount of planner work
fixes it -- his rows from d7 are priced against his d7 bank, and a STRAWBERRY seed is $100.
"""
import argparse, json, sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TPD = 24


def _state(obs, seat):
    farms = obs.get("farms") or []
    if len(farms) <= seat:
        return None
    farm = farms[seat]
    priv = obs.get("private") or {}
    crops, animals, owned = Counter(), Counter(), 0
    for row in (farm.get("tiles") or []):
        for t in row:
            if t == "LOCKED":
                continue
            owned += 1
            if isinstance(t, dict):
                if "animal" in t:
                    animals[t["animal"]] += 1
                elif t.get("crop") and t.get("crop") != "WEED":
                    crops[t["crop"]] += 1
    return {"money": round(float(farm.get("money") or 0)),
            "hands": len(farm.get("hands") or []),
            "crops": dict(crops), "animals": dict(animals), "owned": owned,
            "seeds": {k: v for k, v in (priv.get("seeds") or {}).items() if v},
            "shed": {k: v for k, v in (priv.get("shed") or {}).items() if v}}


def run(job):
    seed, arm, day = job
    sys.path.insert(0, str(ROOT))
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([str(ROOT / "submission" / arm / "main.py"),
             str(ROOT / "submission/shop0909/main.py")])
    i = day * TPD
    return _state(env.steps[i][0].get("observation") or {}, 0) if i < len(env.steps) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="spa_own")
    ap.add_argument("--day", type=int, default=7, help="dawn of the first day the planner drives")
    ap.add_argument("--episode", type=int, default=107068412)
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--procs", type=int, default=5)
    args = ap.parse_args()

    r = json.loads((ROOT / f"data/replays_spa_sub/{args.episode}.json").read_text())
    seat = r["info"]["TeamNames"].index("SpaTaro")
    his = _state(r["steps"][args.day * TPD][seat]["observation"], seat)

    seeds = [11 + 7919 * i for i in range(args.seeds)]
    with Pool(args.procs) as pool:
        rows = [x for x in pool.map(run, [(s, args.arm, args.day) for s in seeds]) if x]

    def med(f):
        v = sorted(f(x) for x in rows)
        return v[len(v) // 2] if v else 0

    print(f"dawn of day {args.day} -- {args.arm} over {len(rows)} games vs his ep {args.episode}\n")
    print(f"{'':14} {'OURS p50':>12} {'HIS':>12}")
    for lab, f, g in (("money", lambda x: x["money"], his["money"]),
                      ("hands", lambda x: x["hands"], his["hands"]),
                      ("owned tiles", lambda x: x["owned"], his["owned"]),
                      ("planted", lambda x: sum(x["crops"].values()), sum(his["crops"].values())),
                      ("animals", lambda x: sum(x["animals"].values()),
                       sum(his["animals"].values())),
                      ("shed units", lambda x: sum(x["shed"].values()), sum(his["shed"].values())),
                      ("seeds held", lambda x: sum(x["seeds"].values()),
                       sum(his["seeds"].values()))):
        print(f"{lab:14} {med(f):>12,} {g:>12,}")
    print(f"\n{'':14} ours (a game at the median money)")
    mid = sorted(rows, key=lambda x: x["money"])[len(rows) // 2]
    for k in ("crops", "animals", "shed", "seeds"):
        print(f"{k:14} {mid[k]}")
        print(f"{'his ' + k:14} {his[k]}")


if __name__ == "__main__":
    main()
