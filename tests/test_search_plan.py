"""The plan encoding, and that the search actually searches.

The second half matters more than the first. A CEM loop that runs without error and reports
improving numbers is exactly what a broken one looks like too -- if the executor ignored the plan,
every candidate would score the same, elite selection would be pure noise, and the *best of a
population* would still drift upward simply because the maximum of more samples is larger. So the
test here is on the **population mean**, which noise cannot move, and on the fitted distribution
moving away from uniform.
"""

import numpy as np

from kagg.search import cem, library
from kagg.search import plan as P


def test_gene_layout_covers_every_field_exactly_once():
    total = 0
    for name, count, cats in P.SPEC:
        lo, hi = P.gene_slice(name)
        assert hi - lo == count
        assert lo == total
        total = hi
        assert cats >= 2
    assert total == P.N_GENES


def test_decode_reads_back_a_hand_written_plan():
    genome = library.melon_wheat()
    plan = P.decode(genome[None, :])

    nw = library.nw_quadrant()
    melon = P.CROP_NAMES.index("MELON")
    wheat = P.CROP_NAMES.index("WHEAT")
    assert set(plan.crop_of[0, nw]) == {melon}
    others = [i for i in range(P.TILES) if i not in set(nw)]
    assert set(plan.crop_of[0, others]) == {wheat}

    assert int(plan.sell_every[0]) == 4
    assert int(plan.dump_day[0]) == 28
    assert list(plan.land_day[0]) == [6, 12, 21]     # snapped to the nearest allowed day


def test_fallow_is_encoded_as_a_crop_of_minus_one():
    plan = P.decode(library.carrot_small()[None, :])
    nw = set(library.nw_quadrant())
    fallow = [i for i in range(P.TILES) if i not in nw]
    assert (plan.crop_of[0, fallow] == P.FALLOW).all()


def test_uniform_probs_are_a_proper_distribution_per_gene():
    probs = P.uniform_probs()
    assert probs.shape[0] == P.N_GENES
    assert np.allclose(probs.sum(axis=1), 1.0)
    for gene in range(P.N_GENES):
        assert (probs[gene, P.N_CATS[gene]:] == 0).all()


def test_sampling_respects_each_genes_category_count():
    rng = np.random.default_rng(0)
    genomes = P.random_genomes(64, rng)
    assert genomes.shape == (64, P.N_GENES)
    assert (genomes >= 0).all()
    assert (genomes < P.N_CATS[None, :]).all()


def test_repeat_and_take_keep_plans_aligned():
    plans = P.decode(library.opposition())
    repeated = plans.repeat(2)
    assert repeated.size == 6
    # np.repeat keeps the plan index varying slowest, which is what `rollout.evaluate` assumes.
    assert (repeated.crop_of[0] == plans.crop_of[0]).all()
    assert (repeated.crop_of[1] == plans.crop_of[0]).all()
    assert (repeated.crop_of[2] == plans.crop_of[1]).all()

    picked = plans.take([2, 0])
    assert (picked.crop_of[0] == plans.crop_of[2]).all()
    assert (picked.crop_of[1] == plans.crop_of[0]).all()


def test_search_raises_the_population_mean_not_only_its_maximum():
    """A broken executor would still show a rising *best*; only the mean is proof of learning."""
    result = cem.search(library.opposition(), generations=4, pop=48, schedules=1,
                        seed=3, log=lambda _: None)
    first, last = result.history[0], result.history[-1]
    assert last["mean_win"] > first["mean_win"] + 0.05, result.history
    assert last["elite_win"] >= first["elite_win"]


def test_the_fitted_distribution_moves_away_from_uniform():
    result = cem.search(library.opposition(), generations=4, pop=48, schedules=1,
                        seed=4, log=lambda _: None)
    lo, hi = P.gene_slice("crop_of")
    crop = result.probs[lo:hi, : P.N_CROPS + 1]
    # Uniform over 6 categories is 1/6 everywhere; a search that learned nothing stays there.
    assert np.abs(crop - 1 / 6).max() > 0.2
