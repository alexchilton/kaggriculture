"""Offline plan search on the batched simulator, and its verification in the real environment.

Three stages, run separately because only the middle one is fast:

``calibrate``
    Play the hand-written opposition plans (`kagg.search.library`) in the **real** environment
    against `kagg.arena`'s opponent pool. This answers the question the search cannot answer about
    itself: is the field it is optimising against strong enough to be worth beating? `CLAUDE.md`
    is explicit that a weak field inflates every number about twofold.

``search``
    CEM over plans, on the simulator. Two rounds: the second adds the first round's winner to the
    opposition, so the search has to beat a strong plan and not only the hand-written ones.

``evaluate``
    The number that decides anything: the searched plan against the same opponent pool, in the
    real environment, on held-out seeds, judged on **win rate**.

Run:
    .venv/bin/python scripts/search_plans.py calibrate
    .venv/bin/python scripts/search_plans.py search [generations] [population]
    .venv/bin/python scripts/search_plans.py evaluate [first_seed] [n_seeds]
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from kagg.arena.pool import COMPETITIVE, evaluate as pool_evaluate  # noqa: E402
from kagg.search import agent as plan_agent  # noqa: E402
from kagg.search import cem, library  # noqa: E402
from kagg.search import plan as P  # noqa: E402

MODULE_SPEC = ("module", "kagg.search.agent")
TUNING_SEEDS = tuple(range(200, 212))
HELD_OUT_SEEDS = tuple(range(400, 412))


def measure(genome, seeds, label, workers=8):
    """Play one genome against the real opponent pool, in the real environment."""
    import os

    path = ROOT / "data" / f"plan_{label}.json"
    plan_agent.save_best(genome, {"note": label}, path=path)
    os.environ["KAGG_SEARCH_PLAN"] = str(path)
    result = pool_evaluate(MODULE_SPEC, seeds, opponents=COMPETITIVE, workers=workers)
    print(f"{label:>14}: {result}", flush=True)
    return result


def calibrate(seeds=TUNING_SEEDS[:6]):
    """How strong is the opposition the search plays against? Measured in the real environment."""
    for name, genome in zip(library.NAMES, library.opposition()):
        measure(genome, seeds, name)


def run_search(generations=16, pop=192, schedules=1):
    """Two CEM rounds. A generation costs one 719-step pass of `pop x opponents x seatings` games.

    `schedules` is the number of shop-unlock draws each generation scores on. One is enough
    *because a fresh one is drawn every generation* -- the failure the heuristic tuner hit was a
    fixed seed set, not a small one -- and the winner is re-scored on six fresh draws afterwards.
    """
    t0 = time.time()
    print("=== round 1: against the hand-written opposition ===", flush=True)
    first = cem.search(library.opposition(), generations=generations, pop=pop,
                       schedules=schedules, seed=7)

    print("\n=== round 2: the round-1 winner joins the opposition ===", flush=True)
    stronger = np.concatenate([library.opposition(), first.best_genome[None, :]])
    second = cem.search(stronger, generations=generations, pop=pop,
                        schedules=schedules, seed=11)

    # Winner's curse: re-score both winners and both modal plans on a fresh draw before choosing.
    contenders = np.stack([
        first.best_genome,
        second.best_genome,
        cem.modal_genome(first.probs),
        cem.modal_genome(second.probs),
    ])
    labels = ["round1_best", "round2_best", "round1_modal", "round2_modal"]
    win, delta = cem.confirm(contenders, stronger, schedules=6)
    for label, w, d in zip(labels, win, delta):
        print(f"confirm {label:>13}: win {w:.2f} delta {d:+.0f}")
        # Kept so a contender the simulator ranked second can still be measured in the real
        # environment, which is the only ranking that decides anything.
        plan_agent.save_best(contenders[labels.index(label)], {"note": label},
                             path=ROOT / "data" / f"plan_{label}.json")

    pick = int(np.lexsort((delta, win))[-1])
    print(f"\nchosen: {labels[pick]}  ({time.time() - t0:.0f}s total)")
    print(P.describe(contenders[pick]))

    plan_agent.save_best(contenders[pick], {
        "source": labels[pick],
        "sim_win_rate": float(win[pick]),
        "sim_mean_delta": float(delta[pick]),
    })
    with open(ROOT / "data" / "search_history.json", "w") as handle:
        json.dump({"round1": first.history, "round2": second.history}, handle, indent=1)
    _report_distribution(second.probs)


def _report_distribution(probs):
    """What the fitted distribution says, which is the readable form of the result."""
    lo, hi = P.gene_slice("crop_of")
    crop = probs[lo:hi, : P.N_CROPS + 1]
    names = ["FALLOW"] + P.CROP_NAMES
    print("\nfitted crop distribution, averaged over tiles:")
    for i, name in enumerate(names):
        print(f"  {name:>11}: {crop[:, i].mean():.3f}")

    lo, hi = P.gene_slice("hires")
    hires = probs[lo:hi, : len(P.HIRE_LEVELS)]
    expected = hires @ P.HIRE_LEVELS
    print("expected headcount by day: " + " ".join(f"{v:.0f}" for v in expected))


def evaluate(first_seed=400, n_seeds=12):
    seeds = tuple(range(first_seed, first_seed + n_seeds))
    genome = plan_agent.load_best(plan_agent.DEFAULT_PLAN)
    print(f"seeds {seeds[0]}-{seeds[-1]}")
    return measure(genome, seeds, "searched")


def inspect(path=None):
    """Print the saved plan as a board, next to what the heuristic would have done."""
    from kagg.search.executor import ORDER

    genome = plan_agent.load_best(path or plan_agent.DEFAULT_PLAN)
    decoded = P.decode(genome[None, :])
    letters = {-1: ".", 0: "W", 1: "C", 2: "T", 3: "S", 4: "M"}

    grid = [[" "] * 10 for _ in range(10)]
    for i, (x, y) in enumerate(ORDER):
        grid[y][x] = letters[int(decoded.crop_of[0, i])]
    print("crop layout  (W wheat, C carrot, T tomato, S strawberry, M melon, . fallow)")
    print("             the NW 5x5 block is the only land that starts unlocked")
    for y, row in enumerate(grid):
        west, east = "".join(row[:5]), "".join(row[5:])
        tail = "   <- south of here starts locked" if y == 4 else ""
        print(f"  {west} | {east}{tail}")
    print()
    print(P.describe(genome))


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "search"
    if command == "calibrate":
        calibrate()
    elif command == "search":
        run_search(*[int(a) for a in sys.argv[2:]])
    elif command == "evaluate":
        evaluate(*[int(a) for a in sys.argv[2:]])
    elif command == "inspect":
        inspect(*sys.argv[2:])
    else:
        raise SystemExit(__doc__)
