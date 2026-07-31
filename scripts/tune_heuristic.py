"""Evolutionary search over the heuristic agent's parameters.

A (1 + lambda) hill-climbing ES: perturb the incumbent, evaluate the population in parallel,
move if anything beats it. No gradients, no credit assignment, no differentiable simulator.

Why this rather than RL for the parameter layer: the thing we want to optimise is final bank,
which is a single scalar at the end of a 720-step episode. ES cares only about that scalar, so
the long delay between planting and payout -- the credit-assignment problem that makes PPO hard
here -- simply does not arise. It is also embarrassingly parallel across CPU cores, which is what
this machine has.

The ceiling is the heuristic's own structure: ES tunes the numbers, it cannot invent a strategy
the policy has no knobs for. That is the known limitation, and the reason it is a complement to
learning rather than a replacement.

Run: .venv/bin/python scripts/tune_heuristic.py [generations]
"""

import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor

# (low, high, is_integer)
BOUNDS = {
    "tiles_per_hand": (2, 14, True),
    "max_hands": (4, 22, True),
    "carry_before_drop": (5, 90, True),
    "seed_buffer": (0, 30, True),
    "land_slack": (1.0, 8.0, False),
    "productive_gate": (0.0, 0.98, False),
    "phase_mod": (1, 8, True),
}
# Seeds are RESAMPLED every generation from this pool, and the incumbent is re-scored on the
# same fresh seeds each time. Measured necessity, not caution: with three fixed seeds the search
# gained 40% on those seeds and only 12.8% on held-out ones -- two thirds of the "improvement"
# was memorising the seeds. Fresh seeds each generation make that impossible to accumulate.
SEED_POOL = tuple(range(60))
SEEDS_PER_EVAL = 8
POPULATION = 10
HOLDOUT = tuple(range(100, 112))  # never used for selection, only for honest reporting


def _evaluate(job):
    """Mean final bank over SEEDS, playing seat 0 against `starter`."""
    params, seeds = job
    from kaggle_environments import make

    from kagg.agents import heuristic

    heuristic.PARAMS.update(params)
    total = 0.0
    for seed in seeds:
        env = make("kaggriculture", configuration={"seed": seed}, debug=False)
        env.run([heuristic.agent, "starter"])
        total += env.steps[-1][0]["reward"]
    return total / len(seeds)


def mutate(params, rng, scale=0.35):
    child = dict(params)
    # Perturb a random subset so single-parameter effects stay visible.
    for key in rng.sample(list(BOUNDS), k=rng.randint(1, 3)):
        low, high, is_int = BOUNDS[key]
        span = high - low
        value = child[key] + rng.gauss(0, scale * span)
        value = max(low, min(high, value))
        child[key] = int(round(value)) if is_int else round(value, 3)
    return child


def main():
    generations = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    rng = random.Random(0)

    from kagg.agents import heuristic

    incumbent = {k: heuristic.PARAMS[k] for k in BOUNDS}
    start_params = dict(incumbent)

    started = time.time()
    with ProcessPoolExecutor(max_workers=10) as pool:
        for gen in range(1, generations + 1):
            seeds = tuple(rng.sample(SEED_POOL, SEEDS_PER_EVAL))
            candidates = [incumbent] + [mutate(incumbent, rng) for _ in range(POPULATION)]
            scores = list(pool.map(_evaluate, [(c, seeds) for c in candidates]))

            # Index 0 is the incumbent, re-scored on this generation's seeds so the comparison
            # is like-for-like rather than against a stale lucky draw.
            # Confirm the winner on a *fresh* draw before accepting it. Without this, taking
            # the best of POPULATION noisy estimates against an incumbent scored once biases
            # every comparison upward -- the winner's curse -- and the search wanders without
            # improving. Measured: 11 accepted moves in 14 generations for +1.6% total.
            ranked = sorted(range(len(candidates)), key=lambda i: -scores[i])
            top = ranked[0]
            if top != 0:
                confirm_seeds = tuple(rng.sample(SEED_POOL, SEEDS_PER_EVAL))
                challenger, holder = pool.map(
                    _evaluate, [(candidates[top], confirm_seeds), (incumbent, confirm_seeds)]
                )
                if challenger <= holder:
                    top = 0
            if top == 0:
                print(f"gen {gen:2d}  held  incumbent {scores[0]:9.0f}  (best child {max(scores[1:]):9.0f})")
            else:
                incumbent = candidates[top]
                print(f"gen {gen:2d}  moved {scores[top]:9.0f}  (was {scores[0]:9.0f})   {incumbent}")

    print(f"\nsearch took {time.time() - started:.0f}s")
    print("Honest comparison on held-out seeds never used for selection:")
    before = _evaluate((start_params, HOLDOUT))
    after = _evaluate((incumbent, HOLDOUT))
    print(f"  start  {before:9.0f}")
    print(f"  tuned  {after:9.0f}   ({after / max(before, 1) - 1:+.1%})")
    print("PARAMS =", incumbent)


if __name__ == "__main__":
    main()
