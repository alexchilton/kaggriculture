"""The plan genome must be able to express a livestock farm, because the leaders' plans are ~35% one.

**The gap this closes, measured.** `docs/episode_teardown_2026-08-03.md` tears down real episodes from
the top of the leaderboard. `Dmitry Larko` (#1), `IY` (#4) and `Juste Me` (#5) all submit the *same*
plan, down to identical integers:

    seeds   MELON 21   WHEAT 66   STRAWBERRY 44
    animals COW 8      SHEEP 6    GOOSE 0
    14 BUILD_PASTURE, 0 BUILD_COOP, 306 hires, 2 land, 967 wheat bought as feed

and they draw **34.9% of revenue from milk and wool** plus ~6% from reselling fertiliser collected free
off the animals.

`grep -icE "animal|cow|sheep|pasture|coop|feed" kagg/search/plan.py` returned **0**. `crop_of` had
`N_CROPS + 1` categories -- five crops and fallow -- so the search space could not put a structure on a
tile, could not own an animal, and could not express any part of the strategy that is actually winning.
CEM over that space searches the crop-only subspace we have already measured losing: `farm` banks
$28,168 against their ~$100k-$144k.

This is the same blind spot from the other track. `CLAUDE.md` records the heuristic line scoring 712
"with the livestock half of `converter` still broken", and the simulator itself modelled 9 of 18 ops
until 2026-08-01 -- the missing half being the animal economy, every time.

**The migration property is the one that matters.** `kagg/search/best_plan.json` holds a 277-gene
genome from before this change, and `kagg/search/agent.py` loads it as the default plan. Appending genes
must leave it decoding to *exactly* the plan it decoded to yesterday, or the extension silently changes
what an existing submission does. That is
`test_a_pre_extension_genome_decodes_to_exactly_the_same_plan`.
"""

import numpy as np
import pytest

from kagg.search import plan as P

OLD_N_GENES = 277        # TILES*2 + 1 + 5 + 30 + 30 + 1 + 5 + 1 + 3 + 1, before the animal blocks


# ---- the space exists ----------------------------------------------------------------------------


def test_the_spec_still_totals_n_genes():
    """The invariant every other consumer relies on -- `cem.py` iterates `range(N_GENES)`."""
    assert sum(n for _, n, _ in P.SPEC) == P.N_GENES
    assert len(P.N_CATS) == P.N_GENES


def test_the_genome_grew_rather_than_being_rearranged():
    """Append-only. Inserting a block in the middle would repoint every gene after it, silently
    changing what `best_plan.json` means."""
    assert P.N_GENES > OLD_N_GENES
    names = [name for name, _, _ in P.SPEC]
    assert names[:11] == ["crop_of", "phase", "stop_plant", "harvest_par", "hires", "sell_qty",
                          "sell_every", "floor_frac", "seed_reserve", "land_day", "dump_day"]
    for name in ("herd", "stock_day", "feed_wheat", "fert_policy"):
        assert name in names, f"{name} missing from SPEC"
        lo, _hi = P.gene_slice(name)
        assert lo >= OLD_N_GENES, f"{name} was inserted before the old genes"


def test_a_tile_can_hold_a_structure():
    """`crop_of` gains COOP and PASTURE categories, so a tile's *use* is one decision rather than
    two competing gene blocks."""
    lo, hi = P.gene_slice("crop_of")
    assert hi - lo == P.TILES
    assert P.N_CATS[lo] == P.N_CROPS + 3, "expected fallow + 5 crops + coop + pasture"


def test_the_herd_has_one_gene_per_species():
    lo, hi = P.gene_slice("herd")
    assert hi - lo == P.N_ANIMALS == 3


# ---- decoding -----------------------------------------------------------------------------------


def _genome(**over):
    g = np.zeros(P.N_GENES, dtype=np.int64)
    for name, values in over.items():
        lo, hi = P.gene_slice(name)
        g[lo:hi] = values
    return g


def test_a_structure_tile_is_not_also_a_crop_tile():
    """A pasture tile must decode to `FALLOW` in `crop_of`, or the executor would try to plant it."""
    crop = np.zeros(P.TILES, dtype=np.int64)
    crop[0] = P.CROP_GENE_COOP
    crop[1] = P.CROP_GENE_PASTURE
    crop[2] = 5                                     # melon (gene 5 -> crop id 4)
    pl = P.decode(_genome(crop_of=crop))
    assert pl.structure_of[0, 0] == P.COOP
    assert pl.structure_of[0, 1] == P.PASTURE
    assert pl.structure_of[0, 2] == P.NO_STRUCTURE
    assert pl.crop_of[0, 0] == P.FALLOW and pl.crop_of[0, 1] == P.FALLOW
    assert pl.crop_of[0, 2] == 4


def test_the_leaders_allocation_is_representable():
    """**The acceptance test.** Encode what the top three agents actually did and require it to
    survive a decode: 14 pastures, 8 cows, 6 sheep, no geese, no coops, and a three-crop mix."""
    crop = np.zeros(P.TILES, dtype=np.int64)
    crop[:14] = P.CROP_GENE_PASTURE                 # 14 BUILD_PASTURE, 0 BUILD_COOP
    crop[14:35] = 5                                 # melon
    crop[35:79] = 4                                 # strawberry
    herd = [0, P.herd_gene(8), P.herd_gene(6)]      # GOOSE 0, COW 8, SHEEP 6
    pl = P.decode(_genome(crop_of=crop, herd=herd))
    assert int((pl.structure_of[0] == P.PASTURE).sum()) == 14
    assert int((pl.structure_of[0] == P.COOP).sum()) == 0
    assert list(pl.herd[0]) == [0, 8, 6]
    assert int((pl.crop_of[0] == 4).sum()) == 21     # melon
    assert int((pl.crop_of[0] == 3).sum()) == 44     # strawberry


def test_the_new_fields_survive_repeat_and_take():
    """`Plan.repeat` lists every field by hand, so a new field is easy to forget -- and forgetting one
    means the replicates silently carry the wrong herd."""
    pl = P.decode(np.stack([_genome(herd=[1, 2, 3]), _genome(herd=[0, 0, 0])]))
    rep = pl.repeat(3)
    assert rep.size == 6
    assert list(rep.herd[0]) == list(pl.herd[0])
    assert list(rep.structure_of.shape) == [6, P.TILES]
    sel = pl.take([1, 0])
    assert list(sel.herd[0]) == list(pl.herd[1])


# ---- the migration ------------------------------------------------------------------------------


def test_a_pre_extension_genome_decodes_to_exactly_the_same_plan():
    """**The property that makes this safe.** A 277-gene genome saved before the animal blocks existed
    must decode identically -- `best_plan.json` is what `agent.py` runs by default."""
    rng = np.random.default_rng(0)
    old = np.stack([rng.integers(0, P.N_CATS[i]) if i < OLD_N_GENES else 0
                    for i in range(OLD_N_GENES)])
    old = np.array([min(int(v), 5) for v in old])            # legal under the OLD crop_of width too
    padded = P.pad_genome(old)
    assert padded.shape == (P.N_GENES,)

    a = P.decode(padded)
    for field in ("phase", "stop_plant", "harvest_par", "hires", "sell_qty", "sell_every",
                  "floor_frac", "seed_reserve", "land_day", "dump_day"):
        assert getattr(a, field).shape[0] == 1, field
    # No structures and no herd: byte-for-byte the old behaviour.
    assert int((a.structure_of[0] != P.NO_STRUCTURE).sum()) == 0
    assert list(a.herd[0]) == [0, 0, 0]


def test_padding_rejects_a_genome_that_is_too_long():
    """Silently truncating a longer genome would hide a real version mismatch."""
    with pytest.raises(ValueError):
        P.pad_genome(np.zeros(P.N_GENES + 1, dtype=np.int64))


def test_the_shipped_best_plan_still_loads():
    """The concrete instance of the migration, against the file on disk.

    Asserts only that it loads and decodes -- **not** what is in it. An earlier version required the
    shipped plan to contain no structures, which was true of the pre-extension file and stopped being
    true the moment a search ran and overwrote it: `save_best` writes the current genome width, so the
    file on disk is whatever the last search produced.
    """
    import json
    import pathlib
    f = pathlib.Path(P.__file__).with_name("best_plan.json")
    genome = np.asarray(json.loads(f.read_text())["genome"], dtype=np.int64)
    pl = P.decode(P.pad_genome(genome))
    assert pl.size == 1
    assert pl.crop_of.shape == (1, P.TILES)
    assert pl.structure_of.shape == (1, P.TILES)
    assert pl.herd.shape == (1, P.N_ANIMALS)
