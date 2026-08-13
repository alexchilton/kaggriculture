"""A/B one router flag over 6 seeds x both seatings, head to head against Seb's tape.

Same shape as `data/logs/planner_ab3.log`, and the same caveats:

- The tape is OPEN-LOOP. On some seed/seat pairs it collapses to ~$1-2k because its scripted buys
  fail against a board it never saw. Those are artifacts of the harness, not wins, so the money
  columns keep them and the WIN RATE strikes them (`valid` below counts only pairs where the tape
  banks over $10,000).
- Seed variance is ~15%. Six seeds is a small sample and the per-seat delta column is the honest
  read, not the mean.

    python -u scripts/ab_geometry.py --flag DEPOT_RING_FIRST
"""

import argparse
import json
import pathlib
import statistics
import sys
import time

sys.path.insert(0, ".")

from kagg.search import router as RT
from kagg.search import schedule_agent as SA
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy

SEEDS = [11, 7, 23, 3, 42, 101]
TAPE_FLOOR = 10_000


def play(thin, replay, team, seed, ours_seat):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, ours_seat, router=True)
    tape = tape_policy(replay, team, 1 - ours_seat)
    for t in range(719):
        obs = [env.state[0].observation, env.state[1].observation]
        acts = [None, None]
        acts[ours_seat] = agent(obs[ours_seat])
        acts[1 - ours_seat] = tape(obs[1 - ours_seat], t)
        payload = []
        for s in (0, 1):
            n = len(obs[0]["farms"][s].get("hands") or [])
            a = acts[s]
            payload.append({"farmer": a["farmer"], "hands": list(a["hands"])[:n],
                            "market": a["market"]})
        env.step(payload)
        if env.state[0].status == "DONE":
            break
    farms = env.state[0].observation["farms"]
    return int(farms[ours_seat]["money"]), int(farms[1 - ours_seat]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--flag", default="DEPOT_RING_FIRST")
    ap.add_argument("--values", default="None,1",
                    help="comma-separated arm values, eval'd; first is the baseline")
    ap.add_argument("--tape", default=DEFAULT_TAPE, choices=sorted(TAPES))
    ap.add_argument("--seeds", default=",".join(str(s) for s in SEEDS))
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    seeds = [int(s) for s in args.seeds.split(",")]
    original = getattr(RT, args.flag)

    print(f"flag {args.flag}   tape {args.tape}   seeds {seeds}   weeds 0.0")
    print(f"{'seed':>6}{'seat':>6}{'arm':>8}{'ours':>11}{'seb':>11}{'res':>7}{'sec':>7}")
    arms = [(v.strip(), eval(v.strip(), {"None": None, "True": True, "False": False}))
            for v in args.values.split(",")]
    base = arms[0][0]
    res = {}
    try:
        for seed in seeds:
            for seat in (0, 1):
                for arm, val in arms:
                    setattr(RT, args.flag, val)
                    t0 = time.time()
                    ours, his = play(thin, replay, team, seed, seat)
                    res[(seed, seat, arm)] = (ours, his)
                    print(f"{seed:>6}{seat:>6}{arm:>8}{ours:>11,}{his:>11,}"
                          f"{'WIN' if ours > his else 'loss':>7}{time.time() - t0:>7.1f}",
                          flush=True)
    finally:
        setattr(RT, args.flag, original)

    print(f"\n{'arm':>8}{'mean $':>12}{'median $':>12}{'wins':>9}{'valid wins':>13}")
    for arm, _v in arms:
        money = [res[(s, seat, arm)][0] for s in seeds for seat in (0, 1)]
        wins = sum(1 for s in seeds for seat in (0, 1)
                   if res[(s, seat, arm)][0] > res[(s, seat, arm)][1])
        valid = [(s, seat) for s in seeds for seat in (0, 1)
                 if res[(s, seat, arm)][1] >= TAPE_FLOOR]
        vwins = sum(1 for s, seat in valid if res[(s, seat, arm)][0] > res[(s, seat, arm)][1])
        n = len(seeds) * 2
        print(f"{arm:>8}{statistics.mean(money):>12,.0f}{statistics.median(money):>12,.0f}"
              f"{f'{wins}/{n}':>9}{f'{vwins}/{len(valid)}':>13}")

    for arm, _v in arms[1:]:
        deltas = [(s, seat, res[(s, seat, arm)][0] - res[(s, seat, base)][0])
                  for s in seeds for seat in (0, 1)]
        print(f"\nper-seat delta, {arm} minus {base}:")
        print("   " + "  ".join(f"s{s}/{seat}:{d:+,}" for s, seat, d in deltas))
        better = sum(1 for _s, _t, d in deltas if d > 0)
        print(f"   sum {sum(d for _s, _t, d in deltas):+,}   "
              f"mean {statistics.mean(d for _s, _t, d in deltas):+,.0f}   "
              f"median {statistics.median(d for _s, _t, d in deltas):+,.0f}   "
              f"better on {better}/{len(deltas)}")
        real = [(s, seat, d) for s, seat, d in deltas
                if res[(s, seat, base)][1] >= TAPE_FLOOR]
        if real:
            print(f"   NON-ARTIFACT seats only ({len(real)}): sum "
                  f"{sum(d for _s, _t, d in real):+,}   better on "
                  f"{sum(1 for _s, _t, d in real if d > 0)}/{len(real)}")
    tape_floor_hit = [(s, seat) for s in seeds for seat in (0, 1)
                      if min(res[(s, seat, a)][1] for a, _v in arms) < TAPE_FLOOR]
    if tape_floor_hit:
        print(f"   ARTIFACT seats (tape banks < ${TAPE_FLOOR:,}, struck from the win rate): "
              f"{tape_floor_hit}")


if __name__ == "__main__":
    main()
