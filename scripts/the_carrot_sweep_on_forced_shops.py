"""Does the late carrot pay? Swept over a SET town appetite, not a hunted one.

Replaces `the_carrot_sweep_alex_asked_for.py`, which was blocked for three days on finding seeds
whose CARROT drain landed in a bucket. Its last scan of 60 seeds produced ONE seed in bucket 7-9
and NONE above, so the deep-drain case the arm exists for was barely in the sample -- and then the
run was killed off a dropped SSH session at 09:18 with 31 rows written.

Two changes, both of which remove a reason that sweep could not answer the question.

**1. The shops are forced, so drain is an axis.** `_town_consume` reads
`town["unlocked_shops"]` off the live observation every turn (`reference/kaggriculture.py:739`).
Pinning that list sets the appetite exactly: CARROT sits in PET_CAFE (single product, so
`multiplier = 2`) and FARMERS_MARKET (×1), so `k` pet cafes give `2k` units drained per
`townShopSellInterval`. Verified against the measured book in `scripts/force_the_shops.py`, which
must be run before trusting anything here.

**2. The opponent is a tape, because the pool is saturated.** Every row of the previous sweep read
`win 95%`, for both `tiles=0` and `tiles=4`, in every drain bucket -- we beat all nine non-mirror
opponents in every game and draw the mirror, so the metric is `9.5/10` regardless of the arm. It
cannot express the thing being measured. Against Kawashigi's recorded actions we win about 78%,
which leaves room in both directions.

**In process, not through a bundle.** The old sweep patched the source and built a submission per
arm because `kagg.arena.evaluate` plays a file in a subprocess pool. This drives the env directly,
so each worker imports the module and sets the two knobs itself -- no source rewriting, and nothing
left patched on disk if the run is killed.

`tiles=0` is the control and must reproduce the shipped agent in the `as_drawn` world. If the
control moves, the harness is broken and no other row means anything.

    python -u scripts/force_the_shops.py --verify          # first, always
    python -u scripts/the_carrot_sweep_on_forced_shops.py --seeds 6 --workers 14
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
TAPE = ("data/seed_scripts/kawa_2026-08-24/97466318.json", "カワシギ")

#: Multiples of 4: a tile yields 4 (`corner_the_book.YIELD_PER_TILE["CARROT"]`), so the position
#: only moves in fours.
TILES = (0, 4, 8, 12, 16, 24)
#: d19 is absent on purpose -- CARROT ripens in 3 days, so a d19 sowing lands inside the solver
#: zone where the precomputed route carries WHEAT ops and the harvest stop drops silently.
STARTS = (21, 23)
#: Per-tick CARROT drain. 0 is a town that never wants carrots; 12 is six pet cafes.
DRAINS = (0, 2, 4, 6, 8, 12)


#: **Whether the drain is CONTESTED is a separate question from how big it is.** A town that eats
#: 8 carrots a tick is worth nothing if the opponent is already supplying 8. These three span it:
#:
#:   tape:kawa     sells 19 carrots all season -- the drain is effectively ours alone
#:   carrot_25     a permanent carrot farm, selling as it harvests -- contested continuously
#:   carrot_hinge  0 carrot tiles until d21, 32 by d26, sells NOTHING until d29 then dumps 76
#:                 units -- uncontested exactly while our arm is running, then a wall at the close
#:
#: The third is the one the old sweep could not produce at all, and it is the case where a late
#: carrot position is most likely to be wrong.
OPPONENTS_AXIS = ("tape:kawa", "carrot_25", "carrot_hinge")


def _play(job):
    tiles, start, drain, seed, opponent = job
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from force_the_shops import shops_for_drain

    SA = importlib.import_module("kagg.search.schedule_agent")
    CORNER = importlib.import_module("kagg.search.corner_the_book")

    # The two knobs, set on the imported modules rather than rewritten into the files.
    SA.CARROT_SWAP_DAYS = tuple(range(start, 28))
    d = list(CORNER.plan.__defaults__)
    d[-1] = int(tiles)                      # max_tiles is the last default of plan(...)
    CORNER.plan.__defaults__ = tuple(d)

    shops, achieved = (None, None) if drain is None else shops_for_drain("CARROT", drain)

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}
    steps = him = them = None
    cfg = {}
    if opponent.startswith("tape:"):
        rec = json.loads((REPO / TAPE[0]).read_text())
        steps = rec["steps"]
        names = (rec.get("info") or {}).get("TeamNames") or []
        him = names.index(TAPE[1]) if TAPE[1] in names else 0
        cfg = dict(rec.get("configuration") or {})
        cfg.pop("seed", None)
    else:
        from kagg.arena.pool import OPPONENTS, _build
        them = _build(OPPONENTS[opponent], None)

    env = make("kaggriculture", configuration=dict(cfg, seed=int(seed)), debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    carrot_sold = 0
    for t in range(30 * TPD):
        if shops is not None:
            env.state[0].observation["town"]["unlocked_shops"] = list(shops)
        o = env.state[0].observation
        a = me(o, env.configuration)
        for order in (a["market"] or []):
            if (isinstance(order, (list, tuple)) and len(order) > 2
                    and str(order[0]).upper() == "SELL" and order[1] == "CARROT"):
                carrot_sold += int(order[2])
        n0 = len(o["farms"][0].get("hands") or [])
        if steps is not None:
            at = steps[t + 1][him].get("action") if t + 1 < len(steps) else None
            at = at if isinstance(at, dict) else {}
            n1 = len(o["farms"][1].get("hands") or [])
            yours = {"farmer": at.get("farmer") or ["PASS"],
                     "hands": list(at.get("hands") or [])[:n1],
                     "market": at.get("market") or []}
        else:
            yours = them(env.state[1].observation, env.configuration)
        env.step([{"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n0],
                   "market": a["market"]}, yours])
        if env.done:
            break
    farms = env.state[0].observation["farms"]
    del KG
    return (float(farms[0]["money"]), float(farms[1]["money"]), carrot_sold)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--first-seed", type=int, default=9000)
    ap.add_argument("--tiles", default=",".join(map(str, TILES)))
    ap.add_argument("--starts", default=",".join(map(str, STARTS)))
    ap.add_argument("--drains", default=",".join(map(str, DRAINS)))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--opponents", default=",".join(OPPONENTS_AXIS))
    ap.add_argument("--out", default="data/logs/carrot_forced_shops.csv")
    a = ap.parse_args()

    tiles_arms = [int(x) for x in a.tiles.split(",") if x != ""]
    start_arms = [int(x) for x in a.starts.split(",") if x != ""]
    drain_arms = [int(x) for x in a.drains.split(",") if x != ""]
    opp_arms = [x for x in a.opponents.split(",") if x]
    seeds = list(range(a.first_seed, a.first_seed + a.seeds))

    jobs = [(ti, st, dr, sd, op)
            for ti in tiles_arms for st in start_arms for dr in drain_arms
            for op in opp_arms for sd in seeds]
    print(f"{len(tiles_arms)} tiles x {len(start_arms)} starts x {len(drain_arms)} drains "
          f"x {len(opp_arms)} opponents x {len(seeds)} seeds = {len(jobs)} seasons, "
          f"{a.workers} workers")
    print(f"tiles {tiles_arms}   starts {start_arms}   drains {drain_arms}")
    print(f"opponents {opp_arms}")
    print(f"seeds {seeds}\nrows -> {a.out}\n", flush=True)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("tiles,start,drain,opponent,seed,ours,theirs,win,carrot_sold\n")
    fh.flush()

    cell = collections.defaultdict(lambda: [0, 0, 0.0, 0])
    clock = time.perf_counter()
    done = 0
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for job, r in zip(jobs, pool.map(_play, jobs)):
            ti, st, dr, sd, op = job
            ours, theirs, csold = r
            win = 1 if ours > theirs else 0
            fh.write(f"{ti},{st},{dr},{op},{sd},{ours:.0f},{theirs:.0f},{win},{csold}\n")
            fh.flush()
            c = cell[(ti, st, dr, op)]
            c[0] += win
            c[1] += 1
            c[2] += ours
            c[3] += csold
            done += 1
            if done % 25 == 0:
                print(f"  {done}/{len(jobs)}  {time.perf_counter() - clock:.0f}s", flush=True)
    fh.close()

    # **Every table is per OPPONENT.** Averaging a contested drain together with an uncontested one
    # is what would hide the answer: the whole question is whether the town's appetite is ours.
    for op in opp_arms:
        for st in start_arms:
            print(f"\n=== {op}, start d{st} -- delta vs tiles=0 at the SAME drain "
                  f"(win, then bank) ===")
            print(f"{'tiles':<7}" + "".join(f"{'drain ' + str(d):>17}" for d in drain_arms))
            base = {dr: cell[(0, st, dr, op)] for dr in drain_arms}
            for ti in tiles_arms:
                row = f"{ti:<7}"
                for dr in drain_arms:
                    w, n, money, csold = cell[(ti, st, dr, op)]
                    bw, bn, bmoney, _ = base[dr]
                    if not n or not bn:
                        row += f"{'-':>17}"
                        continue
                    row += f"{(w / n) - (bw / bn):>+8.0%}{(money / n) - (bmoney / bn):>+9,.0f}"
                print(row)

    print(f"\n=== control check: tiles=0 must be identical across drains if the arm is off ===")
    for op in opp_arms:
        w, n, money, csold = (0, 0, 0.0, 0)
        row = f"{op:<14}"
        for dr in drain_arms:
            w, n, money, csold = cell[(0, start_arms[0], dr, op)]
            row += f"{(money / n if n else 0):>12,.0f}"
        print(row)
    print("These SHOULD differ -- the drain changes the town for every product, not just carrot.")
    print("What must NOT differ is tiles=0 between two runs of this script on the same drain.")

    print(f"\ncarrot units sold, start d{start_arms[0]}")
    for op in opp_arms:
        print(f"  {op}")
        print(f"  {'tiles':<7}" + "".join(f"{'drain ' + str(d):>10}" for d in drain_arms))
        for ti in tiles_arms:
            print(f"  {ti:<7}" + "".join(
                f"{(cell[(ti, start_arms[0], dr, op)][3] / max(1, cell[(ti, start_arms[0], dr, op)][1])):>10.0f}"
                for dr in drain_arms))

    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
