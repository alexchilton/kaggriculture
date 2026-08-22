"""A cache must return what the function returned, over the WHOLE key space -- not on a spot check.

`nearest` picks which depot a tour detours through, so a changed answer is a changed route, a changed
plan and a changed season. The optimisation is only admissible if it is invisible.

The failure mode worth guarding is not "the cache returns nonsense" -- it is the tie-break. `nearest`
breaks ties on the coordinate itself (`key=(cost, c)`), which makes it total; a memo keyed on
anything coarser than the real arguments would return a DIFFERENT but equally-cheap depot, produce a
legal-looking route, and quietly diverge. So this compares against the unmemoised definition on every
reachable key rather than asserting the cache is populated.
"""

import itertools

import pytest

from kagg.search import cover


def _reference(depots, frm, to=None):
    """The definition, verbatim from before the cache. Deliberately duplicated: a reference that
    imports the thing under test proves nothing."""
    if to is None:
        return min(depots, key=lambda c: (cover.dist(c, frm), c))
    return min(depots, key=lambda c: (cover.dist(frm, c) + cover.dist(c, to), c))


DEPOTS = [
    tuple(cover.SHED),
    ((0, 0), (9, 9)),
    ((4, 4), (4, 5), (5, 4), (5, 5)),
    ((0, 0), (0, 9), (9, 0), (9, 9), (4, 4)),
    ((3, 3),),
]


@pytest.mark.parametrize("depots", DEPOTS)
def test_every_one_argument_key_matches_the_definition(depots):
    for frm in itertools.product(range(10), repeat=2):
        assert cover.nearest(depots, frm) == _reference(depots, frm), frm


@pytest.mark.parametrize("depots", DEPOTS[:3])
def test_every_two_argument_key_matches_the_definition(depots):
    cells = list(itertools.product(range(10), repeat=2))
    for frm in cells:
        for to in cells:
            assert cover.nearest(depots, frm, to) == _reference(depots, frm, to), (frm, to)


def test_a_second_call_is_served_from_the_cache():
    """If this fails the memo is not being hit and the speedup is imaginary, even though every
    answer above is still correct -- a silently inert optimisation is the failure mode that reads
    like success."""
    cover._NEAREST.clear()
    depots = ((0, 0), (9, 9), (4, 4))
    cover.nearest(depots, (1, 1), (8, 8))
    assert len(cover._NEAREST) == 1
    cover.nearest(depots, (1, 1), (8, 8))
    assert len(cover._NEAREST) == 1, "a repeat call added a second entry; the key is not stable"


def test_a_list_of_depots_does_not_raise():
    """Not every caller passes a tuple, and an unhashable key would raise rather than merely miss."""
    assert cover.nearest([(0, 0), (9, 9)], (1, 1)) == (0, 0)


def test_the_tie_break_is_still_the_coordinate():
    """Two depots equidistant from the target must resolve to the smaller coordinate, both from cold
    and from the cache. This is the property a coarser key would silently break."""
    cover._NEAREST.clear()
    depots = ((0, 1), (1, 0))          # both at distance 1 from (0, 0)
    assert cover.nearest(depots, (0, 0)) == (0, 1)
    assert cover.nearest(depots, (0, 0)) == (0, 1)
