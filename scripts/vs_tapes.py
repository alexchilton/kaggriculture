"""Our agent against the TOP seat of every tape we hold, not against the seat that lost.

## Why this exists

`scripts/breakdown.py` and `scripts/handover.py` put the tape's OPPONENT on seat 1
(`tape_policy(replay, team, 1)` resolves to `1 - seat`), because their job is to compare our
trajectory against the tape's on a shared order book. That makes every "WIN" they print a win over
the player the tape beat -- on `seb1326`, kakuteki, who lost $70,886 to $128,518.

This script puts the tape's OWN actions on seat 1 instead, so the question is the one that matters:
can we beat the plan we have been copying.

## What a result does and does not mean

The tape is open-loop -- a fixed script that cannot respond to us. A real ladder opponent can. So a
win here is necessary, not sufficient; a loss here is decisive. Seat 0 and seat 1 hold separate
farms with identical starting boards, and the order book is shared, so the tape's script is as valid
on seat 1 as it was on seat 0 except where its market orders now contend with ours.

    python -u scripts/vs_tapes.py
    python -u scripts/vs_tapes.py --seeds 11,12,13 --handover 11
"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

DAYS = 30


def play(tape, seed, weeds, handover):
    from kaggle_environments import make

    replay, schedule, team = TAPES[tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True, start_day=handover or None)
    # Seat 1 is the tape's OWN play. `seat_wanted=0` resolves to the named team's actions.
    foe = tape_policy(replay, team, 0)
    mine_tape = tape_policy(replay, team, 0) if handover else None

    for t in range(24 * DAYS - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a1 = foe(o1, t)
        if handover and t // 24 < handover:
            ours(o0)
            a0 = mine_tape(o0, t)
        else:
            a0 = ours(o0)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    f = env.state[0].observation["farms"]
    return int(f[0]["money"]), int(f[1]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tapes", default=",".join(sorted(TAPES)))
    ap.add_argument("--seeds", default="11,12,13")
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--handover", type=int, default=0,
                    help="tape plays OUR days 0..N-1 too; 0 means we play the whole season")
    args = ap.parse_args()

    seeds = [int(s) for s in args.seeds.split(",")]
    print(f"our agent (seat 0) vs the tape's OWN play (seat 1)   weeds {args.weeds}   "
          f"handover d{args.handover}\n")
    print(f"  {'tape':<10} {'seed':>5} {'ours':>11} {'tape':>11}  {'result':<6} margin")
    tally = {}
    for tape in args.tapes.split(","):
        w = 0
        for seed in seeds:
            a, b = play(tape, seed, args.weeds, args.handover)
            w += a > b
            print(f"  {tape:<10} {seed:>5} {a:>11,} {b:>11,}  "
                  f"{'WIN' if a > b else 'LOSS':<6} {a - b:>+9,}")
        tally[tape] = (w, len(seeds))
    print("\n  win rate by tape:  " + "   ".join(
        f"{t} {w}/{n}" for t, (w, n) in tally.items()))
    tw = sum(w for w, _ in tally.values())
    tn = sum(n for _, n in tally.values())
    print(f"  overall: {tw}/{tn} = {tw / tn:.0%}")


if __name__ == "__main__":
    main()
