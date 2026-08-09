"""Play the BUILT submission against the opponent pool, and report win rate per opponent.

This is the gate `scripts/build_planner_submission.py` deliberately does not do, because it is
slow and because it answers a different question. The build asks "is the artifact the code we
measured". This asks "does that code beat a field".

Both matter and neither substitutes for the other. The deleted `build_submission.py`'s gate was
"beats `starter`", which this project's own notes call worthless: `starter` sells almost nothing,
so the market is never contested and every number off it is roughly 2x reality.

Two things to read here, in this order:

1. **Win rate, not money.** The ladder is an Elo-style rating. A $43k win and a $4k win score the
   same, so the money column is context, never the decision.
2. **Weeds are ON.** Every season number in `docs/` was measured with `weedSpawnChance = 0` to
   keep the tape comparison clean. The pool runs the environment's default, which is the game
   actually being played, and the planner has never been scored under it before.

    python -u scripts/gate_pool.py --seeds 6 | tee data/logs/gate_pool.log
"""

import argparse
import pathlib
import sys
import time

sys.path.insert(0, ".")

TARGET = "submission/main.py"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--first-seed", type=int, default=700)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--agent", default=TARGET)
    args = ap.parse_args()

    if not pathlib.Path(args.agent).exists():
        raise SystemExit(f"{args.agent} does not exist -- build it first")

    from kagg.arena import COMPETITIVE, evaluate

    seeds = list(range(args.first_seed, args.first_seed + args.seeds))
    print(f"{args.agent} vs {len(COMPETITIVE)} opponents, seeds {seeds[0]}-{seeds[-1]}, "
          f"both seatings = {len(COMPETITIVE) * len(seeds) * 2} games")
    clock = time.perf_counter()
    result = evaluate(args.agent, seeds, opponents=COMPETITIVE, workers=args.workers)
    print(f"\n{result}")
    print(f"\n{'opponent':<14}{'win':>7}{'ours':>11}")
    for name, (wr, money) in sorted(result.per_opponent.items(), key=lambda kv: kv[1][0]):
        print(f"{name:<14}{wr:>6.0%}{money:>11,.0f}")
    print(f"\n{time.perf_counter() - clock:.0f}s")

    # A losing record against a field is a result, not a build failure -- it is the number the
    # decision to submit rests on, and hiding it behind an exit code would be the worse outcome.
    if result.win_rate < 0.5:
        print("\nNOTE: below 50% against the pool.", file=sys.stderr)


if __name__ == "__main__":
    main()
