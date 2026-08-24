"""The live shop price must reach the close, and nothing before it.

`00229c8` is titled "Price the last two days at the shop" and its measurement is 24 games replayed
to **d28 h0**, then our agent plays out. That harness cannot reach d0-d27 by construction, so it
approved a change whose other half runs on every day of the season:

    router.py:661            the CRITICAL removal IS gated on `the_close(day)`   -- d28, d29
    schedule_agent.py:1320   `product_price=(prices or {}).get(...)`             -- ungated
    schedule_agent.py:1351   same for `animal_ops`                               -- ungated

So HARVEST and COLLECT have been ranked at the town's live quote since d0, which was never
measured and is not what the commit says it does. `e2500_close` then lost 101 rating points against
`e2500_shopprice`.

Measured 2026-08-24, `scripts/what_cost_the_hundred_points.py`, 6 ladder games paired, both tapes
replayed to the handover:

    handover d24    reverting the live pricing   +$361/game     reverting both   +$976/game
    handover d27    reverting the live pricing        $0/game   reverting both   -$183/game

d27 is inside the window the original harness tested and roughly agrees with it. d24 -- the first
measurement that lets the agent PLAY with the change rather than inherit it -- reverses the sign.
That is the signature of an unmeasured season-wide effect, so this pins the scope to what was
actually measured.

The wheat number below is the real one from the commit that introduced the close: town paying $21
against a base of $25. Before the close that gap must not move the ranking, because the tile has a
tomorrow and the quote does not.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from kagg.search import router as RT                                        # noqa: E402
from kagg.search import schedule_agent as SA                                # noqa: E402

SEASON_DAYS = RT.R.SEASON_DAYS
CHEAP = {"WHEAT": 21.0}          # what the town actually paid on 98428765
DEAR = {"WHEAT": 400.0}


def _ripe_wheat_tile(day):
    return {"kind": "PLANT", "crop": "WHEAT", "planted_day": day - 4, "yield_units": 3,
            "watered_today": False, "fertilized_until_day": -1, "consecutive_unwatered": 0}


def _emitted(day, prices):
    """What the EXECUTOR emits at this tile, in order.

    `_live_ops` returns `(op, item)` -- it uses the price to ORDER the work, not to report a prize,
    so the observable effect of reading the book is the sequence itself.
    """
    return list(SA._live_ops((0, 0), _ripe_wheat_tile(day), day,
                             {"FERTILIZER": 0, "WHEAT": 9}, {}, {}, prices=prices))


def test_before_the_close_the_quote_does_not_move_the_ranking():
    """d15: a tile with a tomorrow is worth its crop, not today's quote."""
    cheap = _prizes(15, CHEAP)
    dear = _prizes(15, DEAR)
    assert cheap == dear, (
        "the town's live quote is ranking work on d15; the close was measured at d28 h0 and "
        "nothing outside it was ever tested")


def test_the_close_itself_still_reads_the_shop():
    """d29: the tile is sold today or discarded, so the quote is the only thing that matters."""
    cheap = _prizes(SEASON_DAYS - 1, CHEAP)
    dear = _prizes(SEASON_DAYS - 1, DEAR)
    assert cheap != dear, "the close stopped reading the shop -- that is the change worth keeping"


def test_the_penultimate_day_reads_the_shop_too():
    """`the_close` is d28 AND d29, deliberately: a FEED on d28 still pays out."""
    cheap = _prizes(SEASON_DAYS - 2, CHEAP)
    dear = _prizes(SEASON_DAYS - 2, DEAR)
    assert cheap != dear, "d28 is inside the close and must read the shop"
