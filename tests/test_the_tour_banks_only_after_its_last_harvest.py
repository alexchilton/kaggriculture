"""Harvest all day, bank at dusk.  Never the other way round.

Seb's day 4 on both tapes, his own actions, hour by hour:

    seb (interval 12)   HARVEST 4 6 7 8 9 11 12 12 13 14 15 15 15 17   DROP 20 20 21 22 23
    seb1326 (24)        HARVEST 4 6 8 9 10 11 11 13 14 14 14 14 15 18  DROP 18 21 21 21 22 23 23

Fourteen harvests both times and not one DROP until the harvesting is finished.  The env change
moved the sweep earlier -- h18 rather than h20, seven drops rather than five, because at
`townCenterSellInterval` 24 the town absorbs less per tick -- but the ordering rule is identical.

Ours on `seb1326` day 4 drops at h14 and h16, sells those partial loads for $282 and $507, and then
takes its LAST drop at h21 while still harvesting at h21, h21 and h22.  That produce is in hand when
the day ends.  The row asks for `WHEAT 49, FERTILIZER 6`; we fill 27 and 3.

So a mid-tour drop is only ever right when the tour has no harvest left to take.  `materialise` had
three paths that could fire one -- the free drop, the redraw, and the rule-2 delivery -- and none of
them looked ahead for produce still to come.

The closing drop is untouched: it runs after every job by construction, which is the behaviour this
test is protecting rather than restricting.
"""
import collections
import importlib

import pytest

DP = importlib.import_module("kagg.search.cover")


def _harvest(tile, units=3):
    """A job that PRODUCES -- the thing a tour must not bank ahead of."""
    return DP.Job(tile, [("WATER", None), ("HARVEST", None)],
                  gives={"WHEAT": units}, products=frozenset({"WHEAT"}))


def _chore(tile):
    """A job that produces nothing, so a tour of these may bank whenever it likes."""
    return DP.Job(tile, [("WATER", None)])


def _drops_before(route, work):
    """(index of the last yielding job in `route`, indices of drop stops before it)."""
    last_yield = max((n for n, s in enumerate(route)
                      if isinstance(s, DP.Job) and s.yields()), default=-1)
    return last_yield, [n for n, s in enumerate(route[:last_yield])
                        if isinstance(s, DP.Depot) and s.drop]


SHED = [(4, 4)]


def test_a_tour_does_not_bank_while_it_still_has_produce_to_take():
    """The tour stands on the shed between two harvests.  It must walk past it."""
    work = [_harvest((4, 3)), _harvest((4, 5)), _harvest((3, 4))]
    route = DP.materialise((4, 4), work, depots=SHED, wanted={"WHEAT": 20})
    last, early = _drops_before(route, work)
    assert not early, (
        "banked before the last harvest: drops at route positions "
        f"{early}, last yielding job at {last}\n  route: {route}"
    )


def test_the_closing_drop_is_still_planned():
    """Suppressing the early drop must not cost the walk home -- that is the whole delivery."""
    work = [_harvest((4, 3)), _harvest((4, 5))]
    route = DP.materialise((4, 4), work, depots=SHED, wanted={"WHEAT": 20})
    assert isinstance(route[-1], DP.Depot) and route[-1].drop, (
        f"the tour does not end with a drop, so nothing is ever banked\n  route: {route}"
    )


def test_a_tour_with_no_harvest_left_may_still_bank_where_it_stands():
    """The narrowing is 'not before the last harvest', not 'never'.

    A tour that has finished producing -- or never produced -- keeps the free drop, which is the
    behaviour `DROP_WHERE_THE_TOUR_ALREADY_STANDS` was measured for and must not be reverted by
    accident.
    """
    work = [_harvest((4, 3)), _chore((4, 5)), _chore((3, 4))]
    route = DP.materialise((4, 4), work, depots=SHED, wanted={"WHEAT": 20})
    drops = [n for n, s in enumerate(route) if isinstance(s, DP.Depot) and s.drop]
    assert drops, f"no drop planned at all on a tour that finishes producing early\n  route: {route}"


@pytest.mark.parametrize("n_harvests", [2, 4, 6])
def test_the_rule_holds_however_long_the_tour(n_harvests):
    tiles = [(4, 3), (4, 5), (3, 4), (5, 4), (3, 3), (5, 5)][:n_harvests]
    work = [_harvest(t) for t in tiles]
    route = DP.materialise((4, 4), work, depots=SHED, wanted={"WHEAT": 50})
    last, early = _drops_before(route, work)
    assert not early, (
        f"{n_harvests} harvests: banked early at {early}, last yielding job at {last}\n"
        f"  route: {route}"
    )
