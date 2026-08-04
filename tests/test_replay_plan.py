"""A winning seat's *spatial* layout, encoded as a genome. Genome level, not action level.

`plan.leaders_genome()` is honest about the gap it leaves:

    "The *spatial* layout is ours, not theirs -- the counts are measured but which tile holds what
     is not extracted yet, so pastures go nearest the shed and the crops fill outward in serpentine
     order. CEM will move them."

`crop_of` is a per-tile gene, so which square holds what is exactly the thing the genome encodes and
exactly the thing we were guessing. The episode observations carry the full `tiles` grid at every
step, so it does not need guessing.

It also corrects three counts. `leaders_genome()` came from `docs/episode_teardown_2026-08-03.md`,
three episodes: 14 pastures, dump day 26, two land parcels. Mining all 312 seats
(`scripts/mine_build_orders.py`) and reading one $132,245 seat square by square
(`scripts/extract_winner_plan.py`) gives 28 pastures, ~98% of sells on day 20+, and one parcel.

This tests the *genome*: that the layout survives encode -> decode. Whether it scores well is a
separate question for `rollout.evaluate`, and whether CEM can improve on it is the point of having
it at all -- it is a starting distribution, not an answer.
"""

import numpy as np
import pytest

from kagg.search import plan as P
from kagg.search import replay_plan as RP

EPISODE = "data/89113699.json"
SEAT = 1


@pytest.fixture(scope="module")
def layout():
    return RP.layout_from_replay(EPISODE, seat=SEAT)


def test_the_replay_yields_the_measured_square_counts(layout):
    """21 crop tiles (12 MELON, 9 CARROT) and 28 pasture tiles, per `data/logs/winner_plan.log`."""
    assert layout.n_pasture == 28
    assert layout.n_coop == 0
    assert sum(layout.crop_counts.values()) == 21
    assert layout.crop_counts["MELON"] == 12
    assert layout.crop_counts["CARROT"] == 9


def test_only_two_unlocked_quadrants_are_used(layout):
    """One land parcel: NW + NE. Every committed square must lie in y < 5."""
    for (x, y) in list(layout.pasture) + list(layout.crops):
        assert y < 5, f"({x},{y}) is in a quadrant this seat never unlocked"


def test_the_genome_round_trips_the_layout(layout):
    """The whole point: `crop_of` is per tile, so the layout must survive encode -> decode intact."""
    g = RP.genome_from_layout(layout)
    assert g.shape == (P.N_GENES,)
    decoded = P.decode(g[None])

    use = np.asarray(decoded.structure_of[0])
    crop = np.asarray(decoded.crop_of[0])
    for (x, y) in layout.pasture:
        assert use[y * P.BOARD + x] == P.PASTURE, f"pasture at ({x},{y}) lost in decode"
    for (x, y), name in layout.crops.items():
        i = y * P.BOARD + x
        assert use[i] == P.NO_STRUCTURE
        assert crop[i] == P.CROP_NAMES.index(name), f"crop at ({x},{y}) decoded wrong"
    assert int((use == P.PASTURE).sum()) == 28
    assert int((crop >= 0).sum()) == 21


def test_it_corrects_the_three_counts_leaders_genome_guessed(layout):
    """Different from `leaders_genome()` in the three places the measurement disagrees.

    Not a style preference: 14 vs 28 pastures, day 26 vs day 20 dumping, and two vs one land parcel
    are each a measured correction, and each is worth testing so a future edit cannot quietly undo it.
    """
    g = RP.genome_from_layout(layout)
    old = P.leaders_genome()

    lo, hi = P.gene_slice("crop_of")
    n_new = int((g[lo:hi] == P.CROP_GENE_PASTURE).sum())
    n_old = int((old[lo:hi] == P.CROP_GENE_PASTURE).sum())
    assert n_new == 28 and n_old == 14

    lo, _ = P.gene_slice("dump_day")
    assert P.DUMP_DAYS[g[lo]] == 20, "the measured seats dump from day 20, when town demand hits 4x"

    lo, hi = P.gene_slice("land_day")
    bought = int((P.LAND_DAYS[g[lo:hi]] != P.NEVER).sum())
    assert bought == 1, "this seat bought exactly one parcel, on day 10"


def test_the_seed_is_a_distribution_not_an_answer(layout):
    """`probs_around` must leave real mass on alternatives, or the seed caps the ceiling.

    `CLAUDE.md`: a prior that is a shape is fine, a prior that is a policy is not. The test is that
    every gene keeps a route to every other category.
    """
    g = RP.genome_from_layout(layout)
    probs = P.probs_around(g)
    assert probs.shape[0] == P.N_GENES
    for i in range(P.N_GENES):
        k = P.N_CATS[i]
        row = probs[i, :k]
        assert row.min() > 0.0, f"gene {i} cannot reach one of its categories"
        assert row.max() < 1.0, f"gene {i} is pinned to the seed"
