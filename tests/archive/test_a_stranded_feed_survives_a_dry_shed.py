"""Day 12, seed 11, weeds off: one SHEEP starves at (1,6) though every FEED job on the board is
covered (`scripts/matched_days.py`, `docs/brief_d12_unfed_sheep_2026-08-08.md`).

Root cause, traced turn by turn with the real board: `cover.materialise` plans the depot stop
correctly -- u7's route opens with `Depot(pick={WHEAT: 2})` before the two FEED jobs it owns. But
by the hour that stop is actually WALKED, the live shed reads `WHEAT: 0` -- drained by the sell
block and by other units' own draws inside the same replan, which `materialise` cannot see because
it plans each unit's tour independently with no cross-unit accounting of the shed's real stock.

The executor's response to that is the bug: `_router_acts`'s depot branch pops the wanted item off
`node.pick` UNCONDITIONALLY, before checking whether the shed could supply it --

    item = min(node.pick)
    want = node.pick.pop(item)
    take = min(want, shed.get(item, 0))
    if take <= 0:
        continue          # <- node.pick is now missing `item` regardless

-- so on the very next loop iteration `node.pick` reads empty, the depot stop pops itself off the
route unworked, and the WHEAT need is gone. Not "gone until the shed refills" -- gone outright,
even though `BUY_PRODUCT` tops the shed back up a few turns later (verified on the real trace:
`WHEAT` reads 0 at hour 3 and 6 by hour 6). The animal never gets a second chance because nothing
in the model remembers it was owed one.
"""
import collections

import pytest

from kagg.search import routines as R
from kagg.search import schedule_agent as SA

TPD = R.TURNS_PER_DAY
DEPOT = (4, 4)
PEN = (2, 2)


def _sched(days=2):
    base = dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                seeds={}, buys={}, sells={}, hands=0)
    return {d: dict(base) for d in range(days)}


def _board():
    """A 10x10 NW-only board: the farmer starts on a depot tile, one SHEEP pen sits at (2,2),
    already one missed feed from escaping (`consecutive_unfed=1`, so `_at_risk_tiles` marks it),
    and needs nothing else this turn -- cared, no fertilizer standing, nothing ripe -- so the only
    op the board can possibly offer there is FEED.
    """
    tiles = [["LOCKED" if R.quadrant_of(x, y) != "NW" else None for x in range(10)]
             for y in range(10)]
    tiles[PEN[1]][PEN[0]] = dict(animal="SHEEP", fed_today=False, cared_today=True,
                                 consecutive_unfed=1, fertilizer_available=False, yield_units=0,
                                 placed_day=0)
    return tiles


def _obs(day, hour, shed_wheat):
    # A second hand, far from the pen, ALREADY carrying wheat it drew for its own feed job. Its only
    # purpose is to make `have_wheat` (`build_nodes`, shed OR carried) true from the crew's carried
    # stock even though the live SHED itself is empty -- exactly the day-12 board at hour 3, where
    # u0/u1/u3 held 5+3+2 WHEAT between them while the shed itself read 0. Without this second hand
    # the FEED node is never even offered (`have_wheat` false outright) and the test would be
    # exercising a different bug than the one measured.
    farm = {"tiles": _board(), "money": 100_000, "farmer": list(DEPOT), "hands": [[9, 9]],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {"WHEAT": shed_wheat}, "seeds": {}, "inventories": [{}, {"WHEAT": 3}]}
    return {"day": day, "hour": hour, "farms": [farm], "private": priv, "step": day * TPD + hour}


def test_a_depot_draw_the_shed_cannot_fill_yet_survives_to_be_retried():
    """The theory, stated as an assertion. Two calls of the SAME agent, one hour apart, same day.

    Hour 3: the shed is empty (matches the real board's `WHEAT: 0` at that hour) and the farmer
    starts standing ON a depot tile with an at-risk FEED job elsewhere -- so the plan opens with a
    depot draw the shed cannot fill right now.

    Hour 4: the shed has refilled (matches the real board's recovery to `WHEAT: 6` two hours later,
    via the ordinary `BUY_PRODUCT` drip). If the FEED requirement survived hour 3, the farmer -- who
    should still be standing at the depot rather than having wandered off empty-handed -- draws the
    wheat now. If it did not survive, the farmer is already walking toward the pen with nothing to
    feed it, and the SHEEP goes unfed for the rest of the day exactly as it did on day 12.
    """
    agent = SA.make_agent(_sched(), 0, router=True)

    act3 = agent(_obs(0, 3, shed_wheat=0))
    assert act3["farmer"][0] != "PICKUP", "the shed had no wheat; a PICKUP here would be fiction"

    act4 = agent(_obs(0, 4, shed_wheat=6))
    assert act4["farmer"] == ["PICKUP", "WHEAT", 1], (
        f"hour 4 returned {act4['farmer']} with the shed holding wheat and an at-risk pen still "
        "unfed. The draw planned for hour 3 was discarded outright instead of surviving to be "
        "retried once the shed refilled -- which is exactly how the day-12 SHEEP at (1,6) starves."
    )
