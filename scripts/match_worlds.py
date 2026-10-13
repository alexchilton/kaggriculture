"""Our board against his, PER WORLD -- because one world is one draw, not a result.

`scripts/match_d12.py` pools every seed and compares our median to his global distribution. That
hides the thing that matters: his own day-12 board differs by world (11 sheep in a yarn town, 2 in
a smoothie town; 14 carrots in a pet-cafe town, 0 anywhere else before d20), so a pooled median can
sit inside his pooled interquartile range while being wrong in every individual world.

So each of our games is labelled by the cluster of the FIRST shop it actually drew, and compared
only against his seasons in that same cluster. Like for like.

Both sides are read by `spataro_state_targets.board`, the one definition, so ours and his cannot
drift apart by definition-shift -- which is how the first `places` count came to include shed drops.
"""
import argparse, json, statistics, sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.spataro_state_targets import board
from scripts.spa_targets import SHOP_CLUSTER, CLUSTERS

ARMS = {"planner_kawa": ROOT / "submission/planner_pure/main.py",
        "planner_spa":  ROOT / "submission/planner_spa/main.py",
        "planner_tgt":  ROOT / "submission/planner_tgt/main.py",
        "planner_route": ROOT / "submission/planner_route/main.py",
        "hay_router":   ROOT / "submission/hay_router/main.py",
        # SpaTaro's own d0-6 tape replayed, his schedule from d7. The shape Alex asked for from the
        # start: his tape to begin, the planner after.
        "spa_tape":     ROOT / "submission/spa_tape/main.py",
        # The full shape: the same tape, plus the five cluster schedules routed on the first shop.
        "spa_full":     ROOT / "submission/spa_full/main.py",
        # Full tape through d29 on the tape's OWN world (milk_berry, his most common at 30.7%),
        # tape to d6 plus the cluster schedule everywhere else.
        "spa_deep":     ROOT / "submission/spa_deep/main.py",
        # Routed to five REAL seasons rather than model-generated rows. Generated rows measured
        # -$11,940 against a single real season; a per-day median need not be consistent with the
        # other days, a recorded season is by construction.
        "spa_real":     ROOT / "submission/spa_real/main.py",
        # One tape on its own world (full season), d0-6 elsewhere, no routing, + the level-4
        # feed-stop rule. The arm the numbers currently favour.
        "spa_own":      ROOT / "submission/spa_own/main.py",
        "spa_family":   ROOT / "submission/spa_family/main.py"}
OPP = ROOT / "submission/shop0909/main.py"
TPD = 24
#: **Animals and plants. Money is NOT scored, on Alex's instruction, twice given:** "you dont need
#: to look at the money initially at the end of the day - the more important thing is do we manage
#: to get the same amount of animals / plants", and "the money doesnt matter!". It is a consequence
#: of the board, not the target, and scoring it lets a cash number stand in for a board that does
#: not match. `owned` stays: it is tiles, and it bounds what can be planted.
AXES = ("COW", "SHEEP", "WHEAT", "STRAWBERRY", "CARROT", "MELON", "planted", "owned")


def value(row, q):
    if q in ("COW", "SHEEP", "GOOSE"):
        return row["animals"].get(q, 0)
    if q in ("WHEAT", "STRAWBERRY", "CARROT", "MELON", "TOMATO"):
        return row["crops"].get(q, 0)
    return row.get(q, 0)


def play(job):
    arm, seed, seat, days = job
    from kaggle_environments import make
    pair = [str(ARMS[arm]), str(OPP)] if seat == 0 else [str(OPP), str(ARMS[arm])]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    state, first = {}, None
    for day in days:
        i = day * TPD
        if i >= len(env.steps):
            continue
        obs = env.steps[i][0].get("observation") or {}
        b = board(obs, seat)
        if b:
            state[day] = b
            for shop in b["shops"]:
                if first is None and shop in SHOP_CLUSTER:
                    first = shop
    final = env.steps[-1]
    return {"arm": arm, "seed": seed, "seat": seat, "state": state,
            "first_shop": first, "cluster": SHOP_CLUSTER.get(first),
            "bank": final[seat]["reward"] or 0,
            "status": "/".join(str(s["status"]) for s in final)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", default=["planner_tgt", "planner_spa"])
    ap.add_argument("--days", nargs="+", type=int, default=[6, 9, 12])
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--procs", type=int, default=5)
    args = ap.parse_args()

    for a in args.arms:
        # Named arms only, and say so: a typo used to come out as a bare `KeyError` from inside the
        # existence check, which reads like a missing FILE rather than a missing NAME.
        if a not in ARMS:
            raise SystemExit(f"unknown arm {a!r}; known arms are {sorted(ARMS)}")
        if not ARMS[a].exists():
            raise SystemExit(f"{a}: {ARMS[a]} does not exist -- build it first")

    # His distribution, bucketed by the cluster of HIS first shop.
    his_by_cluster = defaultdict(lambda: defaultdict(list))
    flows = {p["ep"]: p["unlocks"]
             for p in json.loads((ROOT / "data/spataro_plan_rows.json").read_text())}
    for s in json.loads((ROOT / "data/spataro_state.json").read_text()):
        first = next((shop for d, shop in sorted(flows.get(s["ep"]) or []) if d <= 3), None)
        c = SHOP_CLUSTER.get(first)
        if not c:
            continue
        for day in args.days:
            if str(day) in s["state"]:
                his_by_cluster[c][day].append(s["state"][str(day)])
    print("his seasons per cluster: " + "  ".join(
        f"{c}={len(his_by_cluster[c][args.days[-1]])}" for c in CLUSTERS) + "\n", flush=True)

    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(a, s, t, tuple(args.days)) for a in args.arms for s in seeds for t in (0, 1)]
    print(f"{len(jobs)} games", flush=True)
    with Pool(args.procs) as pool:
        rows = pool.map(play, jobs)
    bad = [r for r in rows if not r["status"].startswith("DONE")]
    if bad:
        print(f"!! {len(bad)} games not DONE: {sorted({r['status'] for r in bad})}", flush=True)

    def q(v):
        v = sorted(v)
        return v[len(v) // 4], statistics.median(v), v[(3 * len(v)) // 4]

    for arm in args.arms:
        mine = [r for r in rows if r["arm"] == arm]
        print(f"\n{'=' * 78}\n{arm}   mean bank {statistics.mean(r['bank'] for r in mine):,.0f}   "
              f"worlds drawn: " + " ".join(
                  f"{c}={sum(1 for r in mine if r['cluster'] == c)}" for c in CLUSTERS))
        for day in args.days:
            print(f"\n--- dawn of day {day}    ours p50 / his p50, and IN when inside his p25-p75")
            print(f"{'cluster':12} {'n':>3}  " + "  ".join(f"{a[:5]:>11}" for a in AXES))
            tot_in = tot = 0
            for c in CLUSTERS:
                ours = [r["state"][day] for r in mine if r["cluster"] == c and day in r["state"]]
                his = his_by_cluster[c][day]
                if not ours or not his:
                    continue
                cells, inside, n = [], 0, 0
                for a in AXES:
                    hv = [value(x, a) for x in his]
                    ov = [value(x, a) for x in ours]
                    if not max(hv) and not max(ov):
                        cells.append(f"{'-':>11}")
                        continue
                    h25, h50, h75 = q(hv)
                    o50 = statistics.median(ov)
                    ok = h25 <= o50 <= h75
                    inside += ok
                    n += 1
                    mark = "*" if ok else " "
                    cells.append(f"{o50:>5,.0f}/{h50:<4,.0f}{mark}" if a != "money"
                                 else f"{o50 / 1000:>4.0f}k/{h50 / 1000:<3.0f}k{mark}")
                tot_in += inside
                tot += n
                print(f"{c:12} {len(ours):>3}  " + "  ".join(cells) + f"   {inside}/{n}")
            if tot:
                print(f"{'ALL':12} {'':>3}  " + " " * 60 + f"   {tot_in}/{tot} axes inside")


if __name__ == "__main__":
    main()
