"""Every gene `decode()` reads must be something the search can actually set.

This has now been the same defect three times, and each time it silently capped the ceiling while
looking like a finding about the game:

1. `fertilize` was added to `GENES` and `decode()`, and `catalog()` never offered the fertilized
   variant. So no genome fertilized anything, and `fertilize=1` vs `fertilize=0` measured identical --
   which reads as "fertilizer does not help".
2. `LAND_DAY_CHOICES` was widened from 6 days to all 30 *specifically* to reach the leader's day-7
   buy, and `catalog()` kept `land_day = LAND_DAY_CHOICES.index(0)` hardcoded. The forward pass -- where
   the crop and animal mix is decided -- could only ever propose day 0. Fixing it was worth +$1,654
   and produced the first SHEEP the project has ever placed.
3. `feed_loop` was added to `GENES` and `decode()`, and `catalog()` never emitted it. The wheat ->
   animal loop `production.py:53` calls "the main structural reason to keep animals" was expressible
   and unreachable.

The root cause is structural: `decode()` and `catalog()` are two independent vocabularies and nothing
made them agree. This test makes them agree.

It deliberately checks *reachability*, not value. A gene may well be worth nothing -- melon gains
exactly zero from fertilizer -- but "the search tried it and declined" and "the search could not
express it" are completely different states, and only the first is a fact about the game.
"""

import importlib.util
import pathlib
import sys

import numpy as np
import pytest

from kagg.search import chains as C

BEAM = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "beam_chains.py"


def _catalog_module():
    """Import `beam_chains` with argv stubbed, since it parses arguments at module scope."""
    if not BEAM.exists():
        pytest.skip("scripts/beam_chains.py not present")
    argv = sys.argv
    sys.argv = ["beam_chains.py", "--slots", "8", "--chunk", "16", "--refine", "0"]
    try:
        spec = importlib.util.spec_from_file_location("_beam_under_test", BEAM)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except SystemExit:                     # missing opponent tapes, or --help
        pytest.skip("beam_chains.py could not initialise in this environment")
    finally:
        sys.argv = argv


def test_a_catalog_entry_is_a_full_gene_row():
    """The mechanical form: an entry shorter than `GENES` cannot set the genes it omits."""
    mod = _catalog_module()
    for slot in (0, 3):
        for action in mod.catalog(slot):
            assert len(action) == len(C.GENES), (
                f"catalog entry {action} has {len(action)} fields against {len(C.GENES)} genes "
                f"{C.GENES}; the trailing genes are unreachable")


@pytest.mark.parametrize("gene", [g for g in C.GENES if g not in ("kind",)])
def test_every_gene_takes_more_than_one_value_somewhere_in_the_catalog(gene):
    """The substantive form: for each gene, some pair of catalog entries must differ in it.

    A gene fixed to one value across the whole catalog is not being searched, whatever the genome
    layout claims. `kind` is excluded only because "off" is a separate branch rather than a value the
    other entries vary.
    """
    mod = _catalog_module()
    i = C.GENES.index(gene)
    seen = set()
    for slot in range(4):
        for action in mod.catalog(slot):
            if action[0] == "off":
                continue
            seen.add(action[i])
    assert len(seen) > 1, (
        f"every catalog entry sets {gene}={seen.pop() if seen else None}; `decode()` reads this gene "
        f"but the search can never vary it")


def test_the_land_day_actually_offered_is_not_silently_day_zero():
    """The specific regression that cost the most. Day 0 is the one day nothing has been earned, so a
    catalog pinned there cannot express buying land out of revenue -- the leader's whole approach."""
    mod = _catalog_module()
    i = C.GENES.index("land_day")
    days = {C.LAND_DAY_CHOICES[a[i] % len(C.LAND_DAY_CHOICES)]
            for slot in range(4) for a in mod.catalog(slot)
            if a[0] != "off" and C.land_cost(
                C.RANCH_TILES[a[2] % len(C.RANCH_TILES)] if a[0] == "ranch"
                else C.BLOCKS[a[2] % len(C.BLOCKS)][0]) > 0}
    assert days, "no catalog entry needs land at all; this test cannot see the defect"
    assert days != {0}, (
        "every land-needing entry buys on day 0. The grid runs to 30 days and the leader buys on 7 "
        "and 10; a catalog pinned to day 0 makes that unreachable.")


def test_a_catalog_row_survives_decode():
    """End to end: whatever the catalog emits must decode without raising, or the beam is scoring
    candidates that silently became something else."""
    mod = _catalog_module()
    for slot in (0, 5):
        cat = mod.catalog(slot)
        for action in (cat[0], cat[len(cat) // 2], cat[-1]):
            genome = mod.with_slot(np.zeros(8 * len(C.GENES), dtype=np.int64), slot, action)
            C.decode(genome, 8)
