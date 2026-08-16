"""One game with one dial vector, reporting per-crop COLLECTION RATE as well as money.

Two jobs.

**Deciding the routing regime for the CEM.** `cover.PRECOMPUTED_ROUTES` covers d12-d29 and keys a
stop on `(tile, ops)`, so a re-crewed stop can be dropped from the solved route rather than adapted
to -- which would make a crop shift measure a routing failure wearing a crop's name.
`scripts/swap_one_crop.py` handles that by unsolving d12-d29 unconditionally. Measured 2026-08-15,
that unsolve costs **3x the wall clock** (24 pool games: 96s unsolved against 31s solved), which is
the difference between a CEM that fits in an evening and one that does not. So: run the same shift
both ways and read the destination crop's collection rate. If the solved route still collects the
new crop, the CEM can keep the precomputed routes and buy three times the seeds with the savings.

**The check the brief demands on any money figure.** A config whose crop is collected at 30% is a
routing result, not a crop result.

    python -u scripts/cem_collection.py --seed 3 --dials 1 8 0 0 0 0
    python -u scripts/cem_collection.py --seed 3 --dials 1 8 0 0 0 0 --solved
"""
import argparse
import collections
import importlib
import importlib.util
import json
import pathlib
import sys

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from kagg.search import melon_branch as _MB


def run(seed, v, solved, opponent):
    from kaggle_environments import make

    from cem_allocation import BASELINE, write_candidate

    A = importlib.import_module("kagg.search.schedule_agent")
    C = importlib.import_module("kagg.search.cover")
    PLAN = importlib.import_module("kagg.plan")

    fork, melon, tomato, carrot, straw_off, geese = v
    shifts = [("WHEAT", "MELON", melon), ("WHEAT", "TOMATO", tomato),
              ("WHEAT", "CARROT", carrot), ("STRAWBERRY", "WHEAT", straw_off)]
    # The boolean flag is gone: the branch is chosen by the opponent-melon THRESHOLD.
    # 0 makes every opponent qualify, 99 none. See kagg/search/melon_branch.py.
    _MB.OPPONENT_MELON = 0 if fork else 99
    A.CROP_TILE_SHIFTS = tuple((a, b, int(n)) for a, b, n in shifts if n > 0)
    A.LATE_CROP_FROM_DAY = 12
    A.HERD_GEESE = int(geese)
    if not solved:
        C.UNSOLVE_DAYS = tuple(range(12, 30))
        C.PRECOMPUTED_ROUTES = {d: r for d, r in C.PRECOMPUTED_ROUTES.items()
                                if d not in C.UNSOLVE_DAYS}

    # The opponent is the frozen SHIPPED agent -- the same bar the CEM's objective uses -- loaded
    # from its own file so its module globals are not the ones mutated above.
    path = opponent or write_candidate(BASELINE, solved=True)
    sp = importlib.util.spec_from_file_location("opp", path)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    opp = mod.agent

    sched = PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json"))
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)

    grown, collected, weeded = collections.Counter(), collections.Counter(), collections.Counter()
    planted = collections.defaultdict(set)
    prev = {}
    for t in range(719):
        o = env.state[0].observation
        cur, weed_now = {}, {}
        for y, row in enumerate(o["farms"][0]["tiles"]):
            for x, c in enumerate(row):
                k = (x, y)
                if isinstance(c, dict) and c.get("crop"):
                    cur[k] = (c["crop"], c.get("yield_units", 0))
                    planted[c["crop"]].add((x, y, c.get("planted_day")))
                elif c == "WEED" or (isinstance(c, dict) and c.get("kind") == "WEED"):
                    weed_now[k] = True
                    if prev.get(k):
                        weeded[prev[k][0]] += 1
        for k, (crop, u) in cur.items():
            was = prev.get(k)
            if was and was[0] == crop:
                if u > was[1]:
                    grown[crop] += u - was[1]
                elif u < was[1]:
                    collected[crop] += was[1] - u
            elif u:
                grown[crop] += u
        for k, (crop, u) in prev.items():
            if u and cur.get(k, (None,))[0] != crop and not weed_now.get(k):
                collected[crop] += u
        prev = cur
        # `env.run` injects `step` into the observation; stepping by hand does not, and the
        # candidate files read `obs['step']` to drive the schedule. Add it rather than special-case
        # the opponent, so the file under test is byte-identical to the one the pool evaluates.
        o1 = dict(env.state[1].observation)
        o1["step"] = t
        env.step([me(o, t), opp(o1, None)])
        if env.done:
            break

    return dict(seed=seed, dials=list(v), solved=solved,
                money=env.steps[-1][0]["reward"], opp_money=env.steps[-1][1]["reward"],
                grown=dict(grown), collected=dict(collected),
                tiles={c: len(s) for c, s in planted.items()}, weeded=dict(weeded))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--dials", type=int, nargs=6, default=[1, 0, 0, 0, 0, 0],
                    help="fork melon tomato carrot straw_off geese")
    ap.add_argument("--solved", action="store_true", help="keep cover.PRECOMPUTED_ROUTES for d12-29")
    ap.add_argument("--opponent", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    r = run(a.seed, tuple(a.dials), a.solved, a.opponent)
    if a.json:
        print(json.dumps(r))
        return
    g, c = r["grown"], r["collected"]
    rate = lambda k: f"{c.get(k, 0) / g[k]:.0%}" if g.get(k) else "-"
    tag = "SOLVED  " if a.solved else "UNSOLVED"
    print(f"{tag}  dials {a.dials}  seed {a.seed}  bank ${r['money']:,.0f} "
          f"(opp ${r['opp_money']:,.0f})")
    print(f"  tiles     {r['tiles']}")
    print(f"  collected " + "  ".join(f"{k}:{rate(k)}" for k in sorted(g)))
    print(f"  weeded    {r['weeded']}")


if __name__ == "__main__":
    main()
