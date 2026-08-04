"""The mutation operator for direct 720-turn trajectory optimisation.

Extracted from `scripts/optimise_script.py` so it can be tested. It was not testable in the script,
and both defects `tests/test_script_mutation_space.py` pins were found by reading rather than by a
failing test -- exactly the situation `CLAUDE.md` forbids.

**What a mutation may touch, and why that list matters more than the search algorithm.**
The optimiser cannot find play it cannot propose. Every field of `Actions` is therefore reachable
here, and the two that were not are the two that were quietly capping the ceiling:

- `hire` was bool in the candidate array, so a "hire 3" edit stored `True` == 1. The Fibonacci ladder
  resets each dawn and costs $1,$1,$2,$3,$5,$8, so the 2nd-6th hires of a day are nearly free and a
  one-per-turn cap is a hard ceiling on crew size.
- `buy_land` was never mutated. Three of the four quadrants start LOCKED, so the search was confined
  to a quarter of the board.

**No legality machinery, deliberately.** An illegal op degrades to NOOP inside the simulator, so an
illegal mutation only wastes that unit-turn and scores worse; the optimiser rejects it unaided. The
one exception worth spending code on is the *live crew*: there are 24 unit slots against a crew
averaging 5, so an edit above `crew[t]` is a guaranteed no-op and would burn ~80% of the budget.
"""

import numpy as np

from kagg.sim import ops as O

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")

# Every op. NOOP is in so a mutation can also *remove* a wasted action; the animal chain
# (PICKUP/PLACE/FEED/CARE) and BUILD_PASTURE/BUILD_COOP are in because the seed contains zero of them
# and roughly 35% of leader revenue is livestock.
OP_ALPHABET = np.array([
    O.NOOP, O.NORTH, O.SOUTH, O.EAST, O.WEST,
    O.WATER, O.HARVEST, O.PLANT_OP, O.DIG,
    O.PICKUP, O.DROP, O.PLACE, O.FEED, O.CARE, O.COLLECT_FERT, O.FERTILIZE,
    O.BUILD_COOP, O.BUILD_PASTURE,
], dtype=np.int64)

N_ITEMS = 12          # WHEAT..SHEEP, the `unit_item` domain for PICKUP / DROP / PLACE
MAX_QTY = 6           # exclusive upper bound for a carried quantity
MAX_HIRE = 5          # per turn; ten order slots cap it anyway, and the ladder gets steep past six


def candidates(base, n_cand):
    """`n_cand` copies of `base`, widened to int64.

    The widening is the fix for defect 1. `np.repeat` preserves the recorder's dtype, and the
    recorder stores whatever the seed agent emitted -- `jax_heuristic` emits a bool `hire`. A bool
    candidate field clamps every mutation into {0, 1} with no error anywhere.
    """
    return {f: np.repeat(np.asarray(base[f])[None].astype(np.int64), n_cand, axis=0)
            for f in FIELDS}


def mutate(base, rng, n_cand, n_edits, crew):
    """`n_cand` copies of `base`, each with `n_edits` random single-slot edits.

    `crew[t]` is the number of units alive at turn `t`, recorded by `scripts/extract_seed_script.py`.

    The `kind` weights are a bias, not a restriction: every field remains reachable. They lean toward
    the levers the seed measurably lacks -- it hires 140 times against the leaders' ~300, builds no
    structure, buys no animal, and never unlocks a quadrant.
    """
    cand = candidates(base, n_cand)
    T = cand["unit_op"].shape[1]
    crew = np.asarray(crew)
    for c in range(n_cand):
        for _ in range(n_edits):
            kind = rng.random()
            t = int(rng.integers(0, T))
            if kind < 0.50:                                   # a unit's op
                u = int(rng.integers(0, max(int(crew[t]), 1)))   # live slots only
                op = int(OP_ALPHABET[rng.integers(0, len(OP_ALPHABET))])
                cand["unit_op"][c, t, u] = op
                if op == O.PLANT_OP:
                    cand["unit_crop"][c, t, u] = rng.integers(0, cand["buy_seed"].shape[-1])
                elif op in (O.PICKUP, O.DROP, O.PLACE):
                    cand["unit_item"][c, t, u] = rng.integers(0, N_ITEMS)
                    cand["unit_qty"][c, t, u] = rng.integers(1, MAX_QTY)
            elif kind < 0.64:                                 # hiring
                cand["hire"][c, t] = rng.integers(0, MAX_HIRE)
            elif kind < 0.76:                                 # selling
                i = int(rng.integers(0, cand["sell"].shape[-1]))
                cand["sell"][c, t, i] = rng.integers(0, 12)
            elif kind < 0.86:                                 # seed / wheat-as-feed
                if rng.random() < 0.5:
                    i = int(rng.integers(0, cand["buy_seed"].shape[-1]))
                    cand["buy_seed"][c, t, i] = rng.integers(0, 8)
                else:
                    i = int(rng.integers(0, cand["buy_product"].shape[-1]))
                    cand["buy_product"][c, t, i] = rng.integers(0, 8)
            elif kind < 0.94:                                 # the animal chain -- seed has zero
                a = int(rng.integers(0, cand["buy_animal"].shape[-1]))
                cand["buy_animal"][c, t, a] = rng.integers(0, 2)
            else:                                             # unlock a quadrant
                cand["buy_land"][c, t] = rng.integers(0, 2)
    return cand
