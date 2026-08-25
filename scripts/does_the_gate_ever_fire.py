"""How often is the shed actually PRESSED, per opponent? The fix only exists for pressed turns.

`schedule_agent:4626` releases stock before `LATE_SELL_FROM_HOUR` only when
`day >= SHED_HEADROOM_FROM_DAY (12)` and `sum(shed) >= SHED_TARGET (90)`. On every other turn the
changed code and the base code are the same code.

So before reading any base-vs-change number, count the turns where the branch can fire at all. A
pool that never presses the shed cannot measure this change, and its delta is the sort order plus
seed noise -- which is exactly the shape of a measured null that reads like a loss.

The reference point is our own ladder games (`data/logs/sell_shape.log`, 35 games): **137 solver-zone
turns at the 100 cap and 969 at 90-99, with zero units filled across all of them.** That is the
state the fix was built for. This script asks which opponents reproduce it.

    python -u scripts/does_the_gate_ever_fire.py --seeds 700,701,702,703
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

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
TAPE = ("data/seed_scripts/kawa_2026-08-24/97466318.json", "カワシギ")
SHED_TARGET = 90
FROM_DAY = 12
LATE_SELL_FROM_HOUR = 16


def _play(job):
    """Returns (pressed_before_h16, pressed_total, capped, units_in_zone, final)."""
    opponent, seed = job
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module("kagg.search.schedule_agent")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    steps = him = None
    if opponent.startswith("tape:"):
        rec = json.loads((REPO / TAPE[0]).read_text())
        steps = rec["steps"]
        names = (rec.get("info") or {}).get("TeamNames") or []
        him = names.index(TAPE[1]) if TAPE[1] in names else 0

    pressed_early = pressed = capped = 0
    with record_fills() as fills:
        env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
        env.reset(2)
        me = SA.make_agent(sched, 0, router=True)
        them = None if steps else _build(OPPONENTS[opponent], None)
        for t in range(30 * TPD):
            o0 = env.state[0].observation
            day, hour = t // TPD, t % TPD
            total = sum(int(v or 0) for v in ((o0.get("private") or {}).get("shed") or {}).values())
            if day >= FROM_DAY and total >= SHED_TARGET:
                pressed += 1
                pressed_early += hour < LATE_SELL_FROM_HOUR
            capped += total >= 100
            a0 = me(o0, env.configuration)
            n0 = len(o0["farms"][0].get("hands") or [])
            mine = {"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                    "market": a0["market"]}
            if steps:
                at = steps[t + 1][him].get("action") if t + 1 < len(steps) else None
                at = at if isinstance(at, dict) else {}
                n1 = len(o0["farms"][1].get("hands") or [])
                yours = {"farmer": at.get("farmer") or ["PASS"],
                         "hands": list(at.get("hands") or [])[:n1],
                         "market": at.get("market") or []}
            else:
                yours = them(env.state[1].observation, env.configuration)
            env.step([mine, yours])
            if env.done:
                break
        units = sum(1 for d, _h, _o, _i, _p in fills.at_turn(0, op="SELL")
                    if d is not None and 12 <= d <= 23)
        final = float(env.state[0].observation["farms"][0]["money"])
    return (pressed_early, pressed, capped, units, final)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="700,701,702,703")
    ap.add_argument("--opponents", default="wheat_only,strawberry,cow_heavy,carrot_hinge,"
                                          "contrarian,tape:kawa")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

    seeds = [int(x) for x in args.seeds.split(",")]
    opponents = args.opponents.split(",")
    jobs = [(o, s) for o in opponents for s in seeds]
    print(f"{len(opponents)} opponents x {len(seeds)} seeds = {len(jobs)} seasons\n", flush=True)

    agg = collections.defaultdict(lambda: [0, 0, 0, 0, 0.0, 0])
    clock = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for (opp, seed), r in zip(jobs, pool.map(_play, jobs)):
            pe, p, c, u, f = r
            a = agg[opp]
            a[0] += pe
            a[1] += p
            a[2] += c
            a[3] += u
            a[4] += f
            a[5] += 1
            print(f"  {opp:<14} seed {seed:<5} pressed<h16 {pe:>4}  pressed {p:>4}  "
                  f"at cap {c:>4}  units d12-23 {u:>5}  bank {f:>10,.0f}", flush=True)

    print(f"\n{'opponent':<14}{'pressed<h16':>13}{'pressed':>9}{'at cap':>9}"
          f"{'units d12-23':>14}{'mean bank':>12}")
    for opp in opponents:
        pe, p, c, u, f, n = agg[opp]
        if not n:
            continue
        print(f"{opp:<14}{pe / n:>13.0f}{p / n:>9.0f}{c / n:>9.0f}{u / n:>14.0f}{f / n:>12,.0f}")
    print("\nour 35 real ladder games, for comparison: 137 turns at the cap and 969 at 90-99")
    print("in d12-d23, with ZERO units filled (data/logs/sell_shape.log).")
    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
