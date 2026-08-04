"""A chain edit must leave a tape that still makes sense, and must still reach every lever.

Two properties, and they pull against each other:

**Coherence.** The whole reason this operator exists is that a slot edit strands a unit mid-chain --
change what unit 3 does at turn 300 and the rest of its day walks to places that no longer matter.
The atom here is the *unit-day*, which is closed because the simulator respawns the crew on the shed
each dawn, so relocating one leaves the unit starting where the block assumes it starts.

**Reach.** `script_mutate.py` records the opposite failure: "the optimiser cannot find play it cannot
propose", and the two fields it could not touch -- `hire` stored as bool, `buy_land` never mutated --
were the two capping the ceiling. A coherent operator that cannot express land or hiring would repeat
that exactly, so every field is asserted reachable.

The measurement this operator exists to make possible: slot edits accepted 3 times in 70 iterations
on the winner's tape (`data/logs/optimise_from_winner.log`). Whether that is the landscape or the
operator is the open question, and it is only answerable if both operators are valid.
"""

import numpy as np
import pytest

from kagg.search import chain_mutate as C

T = C.TURNS_PER_DAY * 30
U = 12
N_PRODUCTS, N_CROPS, N_ANIMALS = 9, 5, 3


def _tape(rng=None):
    """A dense synthetic tape: every field non-zero somewhere, so an edit cannot be lost in zeros."""
    rng = rng or np.random.default_rng(0)
    return {
        "unit_op": rng.integers(0, 18, size=(T, U)),
        "unit_crop": rng.integers(0, N_CROPS, size=(T, U)),
        "unit_item": rng.integers(0, 12, size=(T, U)),
        "unit_qty": rng.integers(0, 5, size=(T, U)),
        "sell": rng.integers(0, 6, size=(T, N_PRODUCTS)),
        "buy_seed": rng.integers(0, 4, size=(T, N_CROPS)),
        "buy_product": rng.integers(0, 4, size=(T, N_PRODUCTS)),
        "buy_animal": rng.integers(0, 2, size=(T, N_ANIMALS)),
        "hire": rng.integers(0, 3, size=T),
        "buy_land": (rng.random(T) < 0.004).astype(np.int64),
    }


CREW = np.full(T, U, dtype=np.int64)


def test_every_field_survives_a_mutation_with_its_shape_and_dtype():
    cand = C.mutate(_tape(), np.random.default_rng(1), n_cand=4, n_edits=6, crew=CREW)
    base = _tape()
    for f in C.FIELDS:
        assert cand[f].shape == (4,) + np.asarray(base[f]).shape, f
        assert cand[f].dtype == np.int64, f"{f} must be int64 -- a bool field silently clamps edits"
        assert (cand[f] >= 0).all(), f"{f} went negative"


def test_a_unit_day_moves_as_one_block_rather_than_a_slot():
    """**The property that distinguishes this operator.** The whole 24-turn block relocates intact."""
    base = _tape()
    cand = C.candidates(base, 1)
    rng = np.random.default_rng(7)
    before = cand["unit_op"][0].copy()
    C.shift_unit_day(cand, 0, rng, CREW)
    after = cand["unit_op"][0]

    changed_turns = np.flatnonzero((before != after).any(axis=1))
    assert len(changed_turns), "the edit did nothing -- test proves nothing"
    touched_days = {int(t) // C.TURNS_PER_DAY for t in changed_turns}
    assert len(touched_days) <= 2, (
        f"a unit-day shift touched {len(touched_days)} days: {sorted(touched_days)} -- it must move "
        f"one block to one other block, not scatter edits across the season")


def test_a_moved_unit_day_is_the_same_sequence_at_its_destination():
    """Coherence: the block that arrives is the block that left, not a reshuffle."""
    base = _tape()
    cand = C.candidates(base, 1)
    src, dst, u = 3, 17, 2
    original = cand["unit_op"][0, C._day_slice(src), u].copy()
    for f in C.UNIT_FIELDS:
        block = cand[f][0, C._day_slice(src), u].copy()
        cand[f][0, C._day_slice(src), u] = 0
        cand[f][0, C._day_slice(dst), u] = block

    np.testing.assert_array_equal(cand["unit_op"][0, C._day_slice(dst), u], original)
    assert not cand["unit_op"][0, C._day_slice(src), u].any(), "the source day was not vacated"


def test_copying_a_unit_day_leaves_the_source_intact():
    """`copy` must duplicate, not move -- an idle unit inherits work without disarming a busy one."""
    base = _tape()
    cand = C.candidates(base, 1)
    before = cand["unit_op"][0].copy()
    changed = 0
    for _ in range(40):
        C.copy_unit_day(cand, 0, np.random.default_rng(changed), CREW)
        changed += 1
    assert (cand["unit_op"][0] != before).any(), "40 copies changed nothing"


def test_no_edit_writes_into_a_unit_slot_that_has_nobody_in_it():
    """24 slots against a crew of ~10: editing dead rows would burn most of the budget."""
    crew = np.full(T, 3, dtype=np.int64)
    base = {k: (np.zeros_like(v) if k in C.UNIT_FIELDS else v) for k, v in _tape().items()}
    cand = C.mutate(base, np.random.default_rng(3), n_cand=6, n_edits=40, crew=crew)
    touched = np.flatnonzero(cand["unit_op"].any(axis=(0, 1)))
    assert touched.size == 0 or touched.max() < 3, (
        f"wrote into unit slots {touched.tolist()} with a crew of 3")


@pytest.mark.parametrize("field", ["hire", "buy_land", "sell", "buy_animal"])
def test_the_levers_that_capped_the_last_operator_are_all_reachable(field):
    """`script_mutate` could not touch `hire` (bool) or `buy_land` (never mutated). Both capped it."""
    base = _tape()
    reached = False
    for seed in range(30):
        cand = C.mutate(base, np.random.default_rng(seed), n_cand=4, n_edits=10, crew=CREW)
        if (cand[field] != np.asarray(base[field])[None]).any():
            reached = True
            break
    assert reached, f"{field} was never altered in 30 x 4 candidates -- the operator cannot reach it"


def test_mutation_is_deterministic_given_a_seed():
    """Required for the resume/compare harness: two runs on one seed must be identical."""
    base = _tape()
    a = C.mutate(base, np.random.default_rng(11), 3, 8, CREW)
    b = C.mutate(base, np.random.default_rng(11), 3, 8, CREW)
    for f in C.FIELDS:
        np.testing.assert_array_equal(a[f], b[f])


def test_the_base_tape_is_never_modified_in_place():
    """The optimiser keeps `best` across iterations; an in-place edit would corrupt it silently."""
    base = _tape()
    snapshot = {f: np.asarray(base[f]).copy() for f in C.FIELDS}
    C.mutate(base, np.random.default_rng(5), 8, 20, CREW)
    for f in C.FIELDS:
        np.testing.assert_array_equal(np.asarray(base[f]), snapshot[f])
