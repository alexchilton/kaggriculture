"""Does our artifact reach SpaTaro's BOARD by day 12? Not his bank -- his board.

The first effort is a state match, because a bank match can be reached from a board that plays out
completely differently and tells us nothing about which layer is wrong. This prints our p50 against
his p25/p50/p75 on every axis he is measured on, per day, and counts how many axes land inside his
interquartile range.

His distribution is `data/spataro_state.json` (179 seasons of submission 56114097,
`scripts/spataro_state_targets.py`). Ours is read out of the same `observation["farms"][seat]`
structure by the SAME function, so the two sides cannot drift apart by definition-shift -- which is
how the first `places` count ended up counting shed drops as herd placements.
"""
import argparse, json, statistics, sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.spataro_state_targets import board, ANIMALS, CROPS   # one definition, both sides

ARMS = {"planner_kawa": ROOT / "submission/planner_pure/main.py",
        "planner_spa":  ROOT / "submission/planner_spa/main.py",
        # The target algorithm's schedule, differenced into planner rows by
        # `scripts/targets_to_schedule.py`. One cluster only for now -- the router that picks the
        # cluster at d3 is the next piece, and this measures whether the generated rows are worth
        # routing to before that gets built.
        "planner_tgt":  ROOT / "submission/planner_tgt/main.py",
        "hay_router":   ROOT / "submission/hay_router/main.py"}
OPP = ROOT / "submission/shop0909/main.py"
TPD = 24
AXES = ["money", "owned", "planted", "animals_total", "empty_struct", "hands"]


def play(job):
    arm, seed, seat, days = job
    from kaggle_environments import make
    pair = [str(ARMS[arm]), str(OPP)] if seat == 0 else [str(OPP), str(ARMS[arm])]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    out = {}
    for day in days:
        i = day * TPD
        if i < len(env.steps):
            b = board(env.steps[i][0].get("observation") or {}, seat)
            if b:
                out[day] = b
    final = env.steps[-1]
    return {"arm": arm, "seed": seed, "seat": seat, "state": out,
            "bank": final[seat]["reward"],
            "status": "/".join(str(s["status"]) for s in final)}


def axis(rows, key, species=None, crop=None):
    if species:
        return [r["animals"].get(species, 0) for r in rows]
    if crop:
        return [r["crops"].get(crop, 0) for r in rows]
    if key == "animals_total":
        return [sum(r["animals"].values()) for r in rows]
    return [r[key] for r in rows]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", default=["planner_spa", "planner_kawa"])
    ap.add_argument("--days", nargs="+", type=int, default=[3, 6, 9, 12])
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--procs", type=int, default=5)
    ap.add_argument("--his", default="data/spataro_state.json")
    args = ap.parse_args()

    his = json.loads((ROOT / args.his).read_text())
    print(f"his distribution: {len(his)} seasons\n", flush=True)

    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(a, s, t, tuple(args.days)) for a in args.arms for s in seeds for t in (0, 1)]
    print(f"{len(jobs)} games", flush=True)
    with Pool(args.procs) as pool:
        rows = pool.map(play, jobs)
    bad = [r for r in rows if not r["status"].startswith("DONE")]
    if bad:
        print(f"!! {len(bad)} games did not finish DONE: "
              f"{sorted({r['status'] for r in bad})}", flush=True)

    def q(v):
        v = sorted(v)
        return v[len(v) // 4], statistics.median(v), v[(3 * len(v)) // 4]

    specs = ([(k, None, None) for k in AXES]
             + [(s, s, None) for s in ANIMALS] + [(c, None, c) for c in CROPS])
    for arm in args.arms:
        mine = [r for r in rows if r["arm"] == arm]
        print(f"\n================ {arm}   "
              f"mean bank {statistics.mean(r['bank'] or 0 for r in mine):,.0f}")
        for day in args.days:
            h = [s["state"][str(day)] for s in his if str(day) in s["state"]]
            o = [r["state"][day] for r in mine if day in r["state"]]
            if not h or not o:
                continue
            inside = total = 0
            print(f"--- dawn of day {day}      ours(n={len(o)})   "
                  f"his p25/p50/p75 (n={len(h)})")
            for label, sp, cr in specs:
                hv, ov = axis(h, label, sp, cr), axis(o, label, sp, cr)
                if not max(hv) and not max(ov):
                    continue
                h25, h50, h75 = q(hv)
                o50 = statistics.median(ov)
                ok = h25 <= o50 <= h75
                inside += ok
                total += 1
                print(f"    {label:14} ours {o50:>9,.0f}    his {h25:>8,.0f} {h50:>8,.0f} "
                      f"{h75:>8,.0f}   {'IN ' if ok else '   '}"
                      f"{'' if not h50 else f'{o50 / h50:>5.2f}x'}")
            print(f"    -> {inside}/{total} axes inside his interquartile range")


if __name__ == "__main__":
    main()
