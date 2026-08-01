"""Island-model ES over `converter`'s dials, scored on a graded opponent ladder.

**Why islands, and why the islands differ by opponent.** A parallel ES whose demes all face the
same opposition converges to the same place -- the subpopulations add compute, not diversity. The
axis that actually matters here is *who the candidate plays*: `docs/experiment_log.md` records that
the old opponent pool was `heuristic.make_agent` with different dials, so it varied crop mix and
nothing else, and a candidate tuned against it scored 72% locally while losing three ranked matches
in a row. So each island gets a different slice of `kagg.arena.ladder.LADDER`, and migration carries
a genome that survived one opposition into a population facing another. An island that only ever
plays `starter` is free to find something cheap and fragile; the migration is what tests it.

**Why a ladder and not just `contrarian`.** `converter` wins 0 of 16 seed-paired games against
`contrarian`, before and after two real fixes. A fitness that reads 0 for every candidate ranks
nothing, and eight rounds of hand-tuning were sampling exactly that flat surface. Across the ladder
the same agent scores 0.100 against `rancher`'s 0.600 and `contrarian`'s 0.800, so there is a
gradient to climb.

**Two lessons from the last search are built in, not optional.** Seeds are resampled every
generation, because a fixed three-seed objective once reported +40% where held-out seeds said
+12.8%. And a challenger that beats the incumbent is re-scored on a *fresh* draw before it is
accepted, because taking the best of N noisy estimates against a once-scored incumbent biases every
comparison upward -- the winner's curse, measured at 11 accepted moves in 14 generations for +1.6%.

Run:  .venv/bin/python -u scripts/tune_converter.py [generations] 2>&1 | tee data/logs/tune_converter.log
"""

import json
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from kagg.agents import converter
from kagg.arena import ladder

# (low, high, is_integer). Only the dials that are genuinely free: `land_days` is a tuple and
# `cows_per_sheep` a ratio whose sign matters more than its value, so both are left alone.
BOUNDS = {
    "target_herd": (0, 30, True),
    "expand_day": (2, 20, True),
    "max_hands": (2, 22, True),
    "min_hands": (0, 8, True),
    "work_per_hand": (0.5, 6.0, False),
    "wheat_buffer": (0, 80, True),
    "wheat_per_turn": (1, 8, True),
    "wheat_cheap": (20, 60, True),
    "wheat_stock_qty": (1, 12, True),
    "shed_sell_at": (20, 95, True),
    "melon_tiles": (0, 40, True),
    "sell_every": (1, 8, True),
    "min_sell_qty": (1, 10, True),
    "reserve": (0.0, 1500.0, False),
}

# Each island faces a different slice of the ladder. The floor island exists because a candidate
# that cannot beat `pass` -- and `converter` currently cannot -- gets no signal at all from the top
# of the ladder, and the top island exists so that whatever the floor island finds has somewhere to
# be refuted.
ISLANDS = {
    "floor": ("pass", "starter", "rancher"),
    "mid": ("starter", "rancher", "heuristic"),
    "top": ("rancher", "heuristic", "contrarian"),
}

SEED_POOL = tuple(range(60))
HOLDOUT = tuple(range(100, 112))      # never used for selection, only for the closing report
SEEDS_PER_EVAL = 4
POPULATION = 6
MIGRATE_EVERY = 3


def _score(job):
    """Ladder score for one genome on one island. Module level so it survives pickling."""
    params, rungs, seeds = job
    return ladder.evaluate(("converter", dict(params)), seeds, rungs=rungs, workers=1).score


def mutate(params, rng, scale=0.3):
    """Perturb one to three dials, so single-parameter effects stay visible in the log."""
    child = dict(params)
    for key in rng.sample(list(BOUNDS), k=rng.randint(1, 3)):
        low, high, is_int = BOUNDS[key]
        value = child[key] + rng.gauss(0, scale * (high - low))
        value = max(low, min(high, value))
        child[key] = int(round(value)) if is_int else round(value, 2)
    return child


def main():
    generations = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    rng = random.Random(0)
    out = Path("data/tune_converter")
    out.mkdir(parents=True, exist_ok=True)

    base = {k: converter.PARAMS[k] for k in BOUNDS}
    incumbents = {name: dict(base) for name in ISLANDS}
    best_seen = {name: float("-inf") for name in ISLANDS}
    started = time.time()

    print(f"islands: {', '.join(f'{n}{list(r)}' for n, r in ISLANDS.items())}")
    print(f"{POPULATION} children/island/generation, {SEEDS_PER_EVAL} seeds resampled each "
          f"generation, migration every {MIGRATE_EVERY}\n")

    with ProcessPoolExecutor(max_workers=8) as pool:
        for gen in range(1, generations + 1):
            seeds = tuple(rng.sample(SEED_POOL, SEEDS_PER_EVAL))

            jobs, index = [], []
            for name, rungs in ISLANDS.items():
                family = [incumbents[name]] + [mutate(incumbents[name], rng)
                                               for _ in range(POPULATION)]
                for genome in family:
                    jobs.append((genome, rungs, seeds))
                    index.append((name, genome))
            scores = list(pool.map(_score, jobs))

            per_island = {}
            for (name, genome), score in zip(index, scores):
                per_island.setdefault(name, []).append((score, genome))

            for name, ranked in per_island.items():
                held_score, held = ranked[0]           # index 0 is the incumbent, re-scored today
                top_score, top = max(ranked, key=lambda sg: sg[0])

                if top is not held and top_score > held_score:
                    # Confirm on a fresh draw. Without this the best of POPULATION noisy estimates
                    # beats a once-scored incumbent by luck alone, and the search wanders.
                    confirm = tuple(rng.sample(SEED_POOL, SEEDS_PER_EVAL))
                    rungs = ISLANDS[name]
                    chal, hold = pool.map(_score, [(top, rungs, confirm), (held, rungs, confirm)])
                    if chal > hold:
                        incumbents[name] = top
                        best_seen[name] = max(best_seen[name], chal)
                        print(f"gen {gen:2d} {name:6} moved {held_score:.3f} -> {top_score:.3f} "
                              f"(confirmed {chal:.3f} vs {hold:.3f})")
                        continue
                    print(f"gen {gen:2d} {name:6} held   {held_score:.3f}  "
                          f"(challenger {top_score:.3f} failed confirmation {chal:.3f})")
                    continue
                print(f"gen {gen:2d} {name:6} held   {held_score:.3f}")

            # **Migration is the point of the islands.** A genome that won against one opposition
            # is dropped into a population facing another, where it either survives the next
            # generation's comparison or is discarded. Nothing is copied in blindly: the migrant
            # only becomes an incumbent by beating the resident on the resident's own rungs.
            if gen % MIGRATE_EVERY == 0 and len(ISLANDS) > 1:
                names = list(ISLANDS)
                for i, name in enumerate(names):
                    donor = names[(i + 1) % len(names)]
                    rungs = ISLANDS[name]
                    confirm = tuple(rng.sample(SEED_POOL, SEEDS_PER_EVAL))
                    mig, res = pool.map(
                        _score, [(incumbents[donor], rungs, confirm),
                                 (incumbents[name], rungs, confirm)])
                    if mig > res:
                        incumbents[name] = dict(incumbents[donor])
                        print(f"gen {gen:2d} {name:6} <- migrant from {donor} "
                              f"({mig:.3f} vs {res:.3f})")

            (out / "incumbents.json").write_text(json.dumps(incumbents, indent=2))

        # Honest closing comparison on seeds never used for selection, over the whole ladder
        # rather than any one island's slice.
        print(f"\nsearch took {time.time() - started:.0f}s")
        print("Held-out seeds, full ladder, never used for selection:")
        finals = list(pool.map(_score, [(base, ladder.RUNGS, HOLDOUT)]
                              + [(incumbents[n], ladder.RUNGS, HOLDOUT) for n in ISLANDS]))
        print(f"  {'start':8} {finals[0]:.3f}")
        for name, score in zip(ISLANDS, finals[1:]):
            print(f"  {name:8} {score:.3f}   {'BETTER' if score > finals[0] else ''}")

        winner = max(zip(ISLANDS, finals[1:]), key=lambda ns: ns[1])
        print(f"\nbest island: {winner[0]} at {winner[1]:.3f}")
        print("PARAMS =", json.dumps(incumbents[winner[0]], indent=2))
        (out / "best.json").write_text(json.dumps(incumbents[winner[0]], indent=2))


if __name__ == "__main__":
    main()
