"""Does the late carrot pay? Swept over the condition that decides it, and scored on WIN RATE.

Alex, 2026-08-25: *"rather than do a sweep which I asked for, you did one number of tiles on one
seed against one opponent."* Correct. This replaces that.

WHAT THE ARM CHANGES, before any number: from day `start`, the agent converts up to `max_tiles` of
the schedule's own `PLANT WHEAT` to CARROT and sells them into the town. It WINS if the town's
carrot drain absorbs those units above what the displaced wheat earned. It LOSES if the book
saturates, or the conversions cost harvests elsewhere.

So the conditioning variable is the town's CARROT DRAIN, set by the shop draw. Holding it fixed can
only return one town's answer -- which is what `docs/the_optimal_carrot_2026-08-24.md` did: one
game, one seed, one opponent.

MEASURED 2026-08-25, drain over 400 random seeds at d20:

    drain  0:73  1:60  2:100  3:71  4:43  5:37  6:12  7:4      nothing above 7

The old analysis was built on a drain-11 town. Drain 11 does not occur in 400 random seeds, so any
policy tuned on it is tuned on a town the ladder will not draw.

WHY IT BUILDS A BUNDLE PER ARM. `kagg.arena.evaluate(agent_path, ...)` plays a BUILT submission in
a subprocess pool. Monkeypatching `schedule_agent.CARROT_SWAP_DAYS` in this process never reaches
those workers -- the first version of this script did exactly that and every arm silently measured
the shipped agent. So each arm patches the source, builds its own bundle, and is played from disk.

`tiles = 0` is the control and must reproduce the shipped agent. If the control moves, the harness
is broken and no other row means anything.

    python -u scripts/the_carrot_sweep_alex_asked_for.py --seeds 12 --workers 14 --starts 21
"""

import argparse
import collections
import csv
import itertools
import pathlib
import re
import shutil
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

#: Multiples of 4, because a tile yields 4 -- `corner_the_book.YIELD_PER_TILE["CARROT"] = 4` and
#: `plan` divides the absorbable units by it, so the position only moves in fours.
TILES = (0, 4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 56)

#: **d19 is deliberately absent.** CARROT has `max_yield_day = 3`, so a d19 sowing is ripe on d22 --
#: inside the solver zone, since `cover.UNSOLVE_DAYS = range(24, 30)` hands only d24-d29 to the live
#: planner. A precomputed route is keyed on `(tile, ops)`, that tile's route carries WHEAT ops, and
#: the carrot harvest stop drops SILENTLY. Sweeping d19 would measure a crop planted and never
#: picked. d21 -> ripe d24, d23 -> ripe d26, d25 -> ripe d28: all land in the planner zone.
STARTS = (21, 23, 25)

BUCKETS = ((0, 3), (4, 6), (7, 9), (10, 99))
AGENT = REPO / "kagg" / "search" / "schedule_agent.py"
CORNER = REPO / "kagg" / "search" / "corner_the_book.py"


def carrot_drain(seed, day=20):
    """The town's CARROT drain on `day`, off the env's own shop table."""
    from kaggle_environments import make
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    idle = [{"farmer": ["PASS"], "hands": [], "market": []}] * 2
    for _ in range(day * 24):
        env.step(idle)
        if env.done:
            break
    shops = (env.state[0].observation.get("town") or {}).get("unlocked_shops") or []
    return sum(2 if len(KG.SHOPS.get(s) or []) == 1 else 1
               for s in shops if "CARROT" in (KG.SHOPS.get(s) or []))


def patch(tiles, start):
    """Set the two knobs in the source, so the BUILT bundle carries them."""
    # **Assert the pattern MATCHED, not that the text changed.** An arm whose value already equals
    # the file's is a no-op substitution, and `a2 != a` called that "not found" -- which killed the
    # very first arm, start=21, because the shipped line is already `tuple(range(21, 28))`.
    a = AGENT.read_text()
    a2, n = re.subn(r"^CARROT_SWAP_DAYS = .*$",
                    f"CARROT_SWAP_DAYS = tuple(range({start}, 28))", a, count=1, flags=re.M)
    assert n == 1, "CARROT_SWAP_DAYS not found -- refusing to build an unpatched arm"
    AGENT.write_text(a2)

    c = CORNER.read_text()
    c2, n = re.subn(r"(def plan\(obs, shops, me=0, product=\"CARROT\", ours_already=0, "
                    r"max_tiles=)\d+", rf"\g<1>{tiles}", c, count=1)
    assert n == 1, "plan(max_tiles=) not found -- refusing to build an unpatched arm"
    CORNER.write_text(c2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=12, help="seeds per drain bucket")
    ap.add_argument("--scan", type=int, default=400)
    ap.add_argument("--first-seed", type=int, default=9000)
    ap.add_argument("--workers", type=int, default=14)
    ap.add_argument("--out", default="data/logs/the_carrot_sweep.csv")
    ap.add_argument("--tiles", default=",".join(map(str, TILES)))
    ap.add_argument("--starts", default=",".join(map(str, STARTS)))
    ap.add_argument("--scan-only", action="store_true")
    a = ap.parse_args()
    tiles_arms = [int(x) for x in a.tiles.split(",") if x]
    start_arms = [int(x) for x in a.starts.split(",") if x]

    # **Back the two sources up before touching them.** This script rewrites files that ship.
    backups = {p: p.read_text() for p in (AGENT, CORNER)}

    print(f"scanning {a.scan} seeds for CARROT drain at d20 ...", flush=True)
    by_bucket, dist = collections.defaultdict(list), collections.Counter()
    t0 = time.time()
    for i in range(a.scan):
        s = a.first_seed + i
        d = carrot_drain(s)
        dist[d] += 1
        for lo, hi in BUCKETS:
            if lo <= d <= hi:
                if len(by_bucket[(lo, hi)]) < a.seeds:
                    by_bucket[(lo, hi)].append(s)
                break
        if all(len(by_bucket[b]) >= a.seeds for b in BUCKETS):
            break
    print(f"  drain distribution over {sum(dist.values())} seeds: {dict(sorted(dist.items()))}"
          f"   ({time.time() - t0:.0f}s)", flush=True)
    for b in BUCKETS:
        print(f"  bucket {b}: {len(by_bucket[b])} seeds {by_bucket[b]}", flush=True)
    if a.scan_only:
        return

    seeds = [(b, s) for b in BUCKETS for s in by_bucket[b]]
    from kagg.arena import COMPETITIVE, evaluate

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh, w = out.open("w", newline=""), None
    try:
        for start, tiles in itertools.product(start_arms, tiles_arms):
            if tiles == 0 and start != start_arms[0]:
                continue                     # the control does not depend on the start day
            patch(tiles, start)
            bundle = REPO / f"submission/_sweep_t{tiles}_d{start}.py"
            r = subprocess.run([sys.executable, "-u", "scripts/build_planner_submission.py",
                                "--out", str(bundle)], cwd=REPO, capture_output=True, text=True,
                               env={**__import__("os").environ, "PYTHONPATH": "."})
            if r.returncode != 0 or not bundle.exists():
                print(f"\narm tiles={tiles} start=d{start}: BUILD FAILED\n{r.stdout[-800:]}"
                      f"\n{r.stderr[-800:]}", flush=True)
                continue
            print(f"\narm tiles={tiles} start=d{start}  -> {bundle.name}", flush=True)
            for (lo, hi), s in seeds:
                res = evaluate(str(bundle), [s], opponents=COMPETITIVE, workers=a.workers)
                row = dict(tiles=tiles, start=start, bucket=f"{lo}-{hi}", seed=s,
                           win_rate=res.win_rate, money=getattr(res, "mean_money", ""),
                           per_opponent=str(getattr(res, "per_opponent", "")))
                if w is None:
                    w = csv.DictWriter(fh, fieldnames=list(row))
                    w.writeheader()
                w.writerow(row)
                fh.flush()
                print(f"   drain {lo}-{hi} seed {s}: win {res.win_rate:.0%}", flush=True)
            bundle.unlink(missing_ok=True)
    finally:
        for p, text in backups.items():
            p.write_text(text)
        fh.close()
        print("\nsources restored to their pre-sweep contents", flush=True)
    print(f"rows -> {a.out}")


if __name__ == "__main__":
    main()
