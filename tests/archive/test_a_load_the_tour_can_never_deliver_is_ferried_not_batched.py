"""`DELIVER_MIN` batching is only coherent when a later delivery exists.

Day 6, seed 11, the kawashigi grid: the hand that shears (4,3) takes 4 WOOL -- the row asks for
12 -- and then walks to the cow pens at (0,0) and (1,0), which are not shed-access tiles. Every
delivery rule in `materialise` declined it:

- rule 0 fires only on a hand that STARTS loaded; this one starts empty,
- the free drop and the re-draw fire only at a zero-detour depot, and neither (4,3) nor anything
  after it is one,
- rule 2 refused because WOOL 4 is under `DELIVER_MIN` 6 -- whose own docstring defers the load to
  "the end of the tour, which ends at the shed anyway",
- and rule 3, the closing trip, is never charged (`DELIVER_CUTOFF_TURNS` is 99), and could not fit
  this tour even when forced: 21 turns spent of 23, and the walk home costs 8. That is the measured
  null of the cutoff=12 arm.

So the wool rode to (1,0), sat there from h09, and reached the shed only via the overnight sweep --
after the market had closed. The day sold 10 against the tape's 17 with 4 of the row's product in a
hand all afternoon.

The rule under test: when the closing trip is not charged and no remaining stop of the tour stands
on a depot tile, there IS no later delivery to batch for, and a positive load of the row's produce
ships now, `DELIVER_MIN` notwithstanding. The ferry must still re-draw what the rest of the tour
needs, because DROP is all-or-nothing (`kaggriculture.py:333`).
"""

import sys

sys.path.insert(0, ".")

from kagg.search import cover

DEPOTS = ((4, 4), (4, 5), (5, 4), (5, 5))


def d6_shear_tour():
    """Unit 1's day-6 work sequence, as `cover.plan` assigned it: shear, then two far cow pens."""
    shear = cover.Job((4, 3), [("FEED", "WHEAT"), ("CARE", None), ("COLLECT_FERTILIZER", None),
                               ("HARVEST", None)],
                      gives={"FERTILIZER": 1, "WOOL": 4})
    cow_a = cover.Job((0, 0), [("FEED", "WHEAT"), ("CARE", None), ("COLLECT_FERTILIZER", None)],
                      gives={"FERTILIZER": 1})
    cow_b = cover.Job((1, 0), [("FEED", "WHEAT"), ("CARE", None), ("COLLECT_FERTILIZER", None)],
                      gives={"FERTILIZER": 1})
    return [shear, cow_a, cow_b]


def test_a_load_the_tour_can_never_deliver_is_ferried_not_batched():
    work = d6_shear_tour()
    route = cover.materialise((5, 4), work, carry=None, depots=DEPOTS,
                              wanted={"WOOL": 12}, deliver=False, rush=True)
    drops = [i for i, s in enumerate(route) if getattr(s, "depot", False) and s.drop]
    shear_at = next(i for i, s in enumerate(route) if s is work[0])
    feeds_at = next(i for i, s in enumerate(route) if s is work[1])
    assert drops, "the sheared wool is planned into the shed, not left to the overnight sweep"
    ferry = next(i for i in drops if shear_at < i)
    assert ferry < feeds_at, "the ferry goes in before the tour walks away from the shed"
    assert route[ferry].pick.get("WHEAT", 0) == 2, \
        "the same stop draws back the wheat the two pens ahead still eat"


def test_the_ferry_defers_to_a_depot_the_tour_still_touches():
    """A remaining stop ON a shed-access tile is a later delivery, so batching still holds there.

    This is the herd-tour shape: pens sit on depot tiles by design, the zero-detour rules own the
    decision, and their refusals are measured (`REDRAW_ONLY_WHAT_THE_MARKET_WONT_TAKE`). The new
    rule must not fire a walking ferry past them.
    """
    shear = cover.Job((4, 3), [("FEED", "WHEAT"), ("CARE", None), ("HARVEST", None)],
                      gives={"WOOL": 4})
    pen_on_depot = cover.Job((4, 4), [("FEED", "WHEAT"), ("CARE", None)])
    work = [shear, pen_on_depot]
    route = cover.materialise((5, 4), work, carry=None, depots=DEPOTS,
                              wanted={"WOOL": 12}, deliver=False, rush=True)
    tiles = [(5, 4)] + [tuple(s.tile) for s in route]
    for i, stop in enumerate(route):
        if getattr(stop, "depot", False) and stop.drop:
            before, here = tiles[i], tiles[i + 1]
            after = tiles[i + 2] if i + 2 < len(tiles) else here
            detour = cover.dist(before, here) + cover.dist(here, after) - cover.dist(before, after)
            assert detour == 0, "no walking ferry was bought past a depot the tour already touches"
