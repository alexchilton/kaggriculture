"""The stage-1 planner must price volume on a curve, not clip it at the town's drain.

`revenue_rate` caps production at `DRAIN_UNITS * OPPONENT_SHARE` and then values every unit at
half base price.  The drain is not a ceiling.  Each book starts 10,000 deep and `market_price` is a
smooth decreasing function of `inventory - I0`, so selling past the drain lowers the price and does
not stop the sale.  Two consequences, both measured on 2026-08-09:

* **The estimate goes flat.**  Melon yields 12 units a tile against a cap of 15, so two melon tiles
  and sixteen melon tiles score identically.  The planner cannot see the difference and stops
  buying melon ground -- which is what the stage-1 run does, landing on 4 tiles.
* **Correcting `DRAIN_UNITS` to 1.32.6 made it worse, not better.**  Melon's drain fell 140 -> 30,
  so the cap fell 70 -> 15 and the forgone revenue multiplied by 4.67.

Revenue-maximising volume against the cap, priced on the environment's own curve:

    product   drain  cap now  opt vol   $ at opt   $ at cap   forgone
    MELON        30       15      180     31,509      3,750     27,759
    MILK        322      161      320     51,200     25,760     25,440
    WOOL        204      102      225     42,947     20,400     22,547
    STRAW       452      226      400     48,000     27,120     20,880

These tests pin the *shape* of the estimate rather than any particular number, because the numbers
are a scheduling heuristic and the simulator is the judge.  What must hold is that more production
is worth more money, by less and less.
"""

import pytest

from kagg.search import chains as C
from kagg.search import scheduler as S


def test_melon_is_not_blind_past_one_tile():
    """The measured failure: 2 tiles and 16 tiles priced identically.

    Melon's cap is 15 units against a per-tile yield of 12, so the cap binds almost immediately.
    A planner that cannot tell 2 tiles from 16 will never allocate melon ground, and stage 1's
    run on 2026-08-09 allocated exactly 4 tiles.
    """
    small = S.revenue_rate("grow", "MELON", 2)
    large = S.revenue_rate("grow", "MELON", 16)
    assert large > small, (
        f"2 melon tiles score {small:.2f} and 16 score {large:.2f}. The cap "
        f"({C.DRAIN_UNITS['MELON']} drain) clips both to the same volume, so every melon tile past "
        "the first is invisible to the planner."
    )


@pytest.mark.parametrize("what", ["MELON", "STRAWBERRY", "WHEAT"])
def test_more_ground_is_never_worth_less(what):
    """Non-decreasing in tiles, and it must discriminate across the range.

    The first version of this test asserted *strictly* increasing and was wrong. Past some acreage
    the estimate goes flat, and that flat is the real answer rather than a defect: owning the tile
    does not oblige us to sell its output, so beyond the revenue-maximising volume the extra
    production is worth exactly nothing. Melon saturates at 8 tiles (525, 525, 525 for 8/16/24).

    What must never happen is a *decrease* -- that would say ground destroys money -- or a flat
    estimate across the whole range, which is the original bug where 2 melon tiles and 16 scored
    identically at 62.50.
    """
    rates = [S.revenue_rate("grow", what, n) for n in (1, 2, 4, 8, 16)]
    assert all(b >= a for a, b in zip(rates, rates[1:])), (
        f"{what}: rates {[round(r, 1) for r in rates]} for 1/2/4/8/16 tiles decrease somewhere. "
        "Owning more ground cannot be worth less money -- the surplus can simply go unsold."
    )
    assert rates[-1] > rates[0] * 2, (
        f"{what}: rates {[round(r, 1) for r in rates]} barely move across a 16x change in acreage. "
        "The planner cannot allocate ground it cannot price."
    )


#: Where each product stops paying for more ground, measured 2026-08-09 with `CONTEST = 1.0`.
#: These are the numbers that make overproduction visible, so they are pinned: a silent change here
#: silently rewrites every allocation the search produces.
SATURATION = {("grow", "MELON"): 8, ("ranch", "COW"): 4, ("ranch", "SHEEP"): 4}


@pytest.mark.parametrize("kind,what,tiles", [(k, w, n) for (k, w), n in SATURATION.items()])
def test_saturation_is_where_we_think_it_is(kind, what, tiles):
    """Doubling the acreage past saturation must add nothing, and just below it must add something."""
    at = S.revenue_rate(kind, what, tiles)
    beyond = S.revenue_rate(kind, what, tiles * 2)
    below = S.revenue_rate(kind, what, max(1, tiles // 2))
    assert beyond == pytest.approx(at, rel=0.02), (
        f"{what}: {tiles} tiles -> {at:.0f}, {tiles * 2} tiles -> {beyond:.0f}. Saturation is not "
        f"at {tiles} any more; every overproduction figure quoted from it is stale."
    )
    assert below < at * 0.99, f"{what}: saturation is below {tiles}, not at it ({below:.0f} vs {at:.0f})"


@pytest.mark.parametrize("what", ["MELON", "STRAWBERRY", "MILK_HERD"])
def test_the_marginal_tile_is_worth_less_than_the_one_before(what):
    """Concavity -- the whole point of pricing on a curve.

    Without this the estimate is linear and the planner allocates the entire farm to whichever
    product has the highest base price, because nothing tells it the book fills up.
    """
    if what == "MILK_HERD":
        f = lambda n: S.revenue_rate("ranch", "COW", n)
    else:
        f = lambda n: S.revenue_rate("grow", what, n)
    steps = [f(n + 1) - f(n) for n in (1, 2, 4, 8)]
    assert all(b <= a for a, b in zip(steps, steps[1:])), (
        f"{what}: marginal value of the next tile went {[round(s, 1) for s in steps]}. It must not "
        "increase -- a book that fills has diminishing returns by construction."
    )


def test_animals_are_priced_on_the_same_curve():
    """`ranch` has its own copy of the cap, and it clips milk and wool the same way."""
    small = S.revenue_rate("ranch", "COW", 2)
    large = S.revenue_rate("ranch", "COW", 12)
    assert large > small, (
        f"2 cows score {small:.2f} and 12 score {large:.2f}: the herd is capped at "
        f"{C.DRAIN_UNITS['MILK'] * S.OPPONENT_SHARE:.0f} units of milk and the planner cannot see "
        "past it."
    )
