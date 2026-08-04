"""The trajectory optimiser's mutation space must actually reach every action field.

Two defects found by audit on 2026-08-04, both of which silently shrink the search space rather than
failing loudly -- which is why they need pinning tests rather than a code read.

1. **`hire` was bool-typed in the candidate array.** The recorder stores whatever the seed agent
   emitted, and `jax_heuristic` emits a bool. `np.repeat` preserves dtype, so `cand["hire"][c, t] = 3`
   stored `True`, i.e. 1. The multi-hire rule fixed in `game.py` and pinned by
   `tests/test_multiple_hires_per_turn.py` was therefore unreachable from the optimiser: it could
   never propose more than one hire per turn, against the leaders' ~300 a season.

2. **`buy_land` was never mutated at all.** Three of the four quadrants start LOCKED, so the whole
   board expansion -- 4x the plantable tiles -- sat outside the search space.
"""

import numpy as np
import pytest

from kagg.search import script_mutate as M

FIELDS = M.FIELDS


@pytest.fixture
def base():
    """A seed-shaped script with the recorder's real dtypes, including the bool `hire`."""
    T, U = 48, 24
    return {
        "unit_op": np.zeros((T, U), dtype=np.int32),
        "unit_crop": np.zeros((T, U), dtype=np.int32),
        "unit_item": np.zeros((T, U), dtype=np.int32),
        "unit_qty": np.zeros((T, U), dtype=np.int32),
        "sell": np.zeros((T, 9), dtype=np.int32),
        "buy_seed": np.zeros((T, 5), dtype=np.int32),
        "buy_product": np.zeros((T, 9), dtype=np.int32),
        "buy_animal": np.zeros((T, 3), dtype=np.int32),
        # The dtype that caused defect 1. Kept bool here deliberately: the fix must survive it.
        "hire": np.zeros(T, dtype=bool),
        "buy_land": np.zeros(T, dtype=bool),
    }


def test_a_multi_hire_mutation_is_not_collapsed_to_one(base):
    """Defect 1. Every candidate field must be widened to an integer dtype before editing."""
    cand = M.candidates(base, n_cand=4)
    cand["hire"][0, 5] = 3
    assert int(cand["hire"][0, 5]) == 3, (
        f"hire candidate dtype is {cand['hire'].dtype}; a 3-hire mutation collapsed to "
        f"{int(cand['hire'][0, 5])}"
    )


def test_no_candidate_field_is_boolean(base):
    """A bool anywhere in the candidate clamps that field to {0, 1} without any error."""
    cand = M.candidates(base, n_cand=2)
    bad = {f: cand[f].dtype for f in FIELDS if cand[f].dtype == np.bool_}
    assert not bad, f"boolean candidate fields silently clamp mutations to 0/1: {bad}"


def test_the_search_actually_proposes_more_than_one_hire_in_a_turn(base):
    """End-to-end: over many draws, at least one turn must carry a hire count above 1."""
    rng = np.random.default_rng(0)
    crew = np.full(base["unit_op"].shape[0], 5)
    cand = M.mutate(base, rng, n_cand=64, n_edits=16, crew=crew)
    assert int(np.max(cand["hire"])) > 1, (
        "no candidate proposed a multi-hire turn; the Fibonacci ladder makes the 2nd-6th hires of a "
        "day cost $1-$8, so a one-per-turn cap is a hard ceiling on crew size"
    )


def test_buy_land_is_inside_the_search_space(base):
    """Defect 2. Three of four quadrants start LOCKED; unlocking is ~4x the plantable tiles."""
    rng = np.random.default_rng(0)
    crew = np.full(base["unit_op"].shape[0], 5)
    cand = M.mutate(base, rng, n_cand=128, n_edits=16, crew=crew)
    assert int(np.max(cand["buy_land"])) >= 1, (
        "buy_land was never mutated, so the optimiser can only ever farm the NW quadrant"
    )


def test_every_action_field_is_reachable(base):
    """No field may be silently frozen. This is the check the audit should not have needed."""
    rng = np.random.default_rng(1)
    crew = np.full(base["unit_op"].shape[0], 5)
    cand = M.mutate(base, rng, n_cand=256, n_edits=24, crew=crew)
    frozen = [f for f in FIELDS if not np.any(np.asarray(cand[f]) != np.asarray(base[f]))]
    assert not frozen, f"fields never touched by any mutation: {frozen}"


def test_mutations_never_target_a_unit_slot_that_holds_no_unit(base):
    """24 slots against a crew of ~5. Editing a dead slot is a guaranteed no-op.

    This project has taken a share over `MAX_UNITS` rather than the live crew four separate times.
    """
    rng = np.random.default_rng(2)
    T = base["unit_op"].shape[0]
    crew = np.full(T, 3)
    cand = M.mutate(base, rng, n_cand=64, n_edits=32, crew=crew)
    touched = np.asarray(cand["unit_op"]) != np.asarray(base["unit_op"])[None]
    dead = touched[:, :, 3:]
    assert not dead.any(), f"{int(dead.sum())} edits landed on slots above the crew size of 3"


def test_the_whole_op_alphabet_can_be_proposed(base):
    """Including BUILD_PASTURE and the animal chain, which the seed contains zero of."""
    from kagg.sim import ops as O

    rng = np.random.default_rng(3)
    crew = np.full(base["unit_op"].shape[0], 24)
    cand = M.mutate(base, rng, n_cand=512, n_edits=32, crew=crew)
    seen = set(np.unique(np.asarray(cand["unit_op"])).tolist())
    missing = [o for o in M.OP_ALPHABET.tolist() if o not in seen]
    assert not missing, f"ops never proposed in 512x32 draws: {missing} (BUILD_PASTURE is {O.BUILD_PASTURE})"
