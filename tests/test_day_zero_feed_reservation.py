"""The day-0 feed reservation must not consume the stake the animals need.

Measured 2026-08-04 (`data/logs/executor_vs_tape_by_day.log`), running the winner's tape and our
executor side by side with seat 1, the shop schedule and the seed held identical, so seat 0 is the
only difference::

    day | TAPE  money alive pens plants | OURS  money alive pens plants | bought  feed
      0 |         42     4    4     17  |         304     0    5     16  |      1    32
      5 |        642     6    6     18  |           0     0    5     20  |      1    38
     12 |     14,165    14   14     43  |           0     0    5      4  |      1    38

We finish day 0 holding **more** pens than the tape (5 against 4) and **no** animals. Money then sits
at $0 from day 5 to day 12, plants collapse 20 -> 4 for want of seed money, land arrives on day 13
instead of the tape's days 7 and 10, and the season ends on $0 against $147,178.

**The mechanism under test**, `executor.py:528-570`. On day 0 `want_wheat = feed_wheat * intended`,
and `intended` is the whole target herd from `stock_day` onward -- 2 x 14 = 28 units -- ordered before
a single animal is owned. That order is then charged against cash at `WHEAT_PRICE_CAP` before the
animals are priced::

    cash = np.maximum(view.money - wheat_order * WHEAT_PRICE_CAP, 0.0)

28 x $60 = $1,680 of a $3,000 stake. The comment there says the reservation deliberately
over-estimates so it "under-buys animals rather than overdrawing", which is the right instinct; the
question this file settles is whether the magnitude is what empties the farm.

**The discriminator is the point of this file.** Two candidate causes predict different things:

- *the reservation starves the purchase* -> pre-filling the shed with the feed (so nothing is ordered
  and nothing is reserved) restores the purchase;
- *something else eats the cash* -> pre-filling the shed changes nothing.

`test_a_shed_already_holding_the_feed_buys_the_herd` is that experiment. A fix aimed at the wrong one
of these would be indistinguishable from a fix aimed at the right one if only the outcome were
asserted, which is why both are here.
"""

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.search import plan as P

TILES = X.TILES
STAKE = 3_000.0          # the real opening bank
PENS = 14                # the leaders build 14 pastures, 0 coops


def _leaders():
    return P.decode(P.leaders_genome()[None, :])


def _view(shed_wheat=0, money=STAKE, pens=PENS, day=0, hour=0):
    """Day 0 at dawn: `pens` empty pastures standing, crew on the shed, nothing planted."""
    kind = np.full((1, TILES), X.EMPTY, dtype=np.int64)
    kind[0, :pens] = X.PASTURE
    return X.View(
        day=day, hour=hour,
        kind=kind,
        crop=np.full((1, TILES), -1, dtype=np.int64),
        planted_day=np.zeros((1, TILES), dtype=np.int64),
        watered=np.zeros((1, TILES), dtype=bool),
        yield_units=np.zeros((1, TILES), dtype=np.int64),
        unit_ord=np.full((1, X.MAX_EXEC_UNITS), int(X.SHED_ORDS[0]), dtype=np.int64),
        n_units=np.array([1]),
        money=np.array([money]),
        seeds=np.zeros((1, P.N_CROPS), dtype=np.int64),
        shed=np.zeros((1, P.N_PRODUCTS if hasattr(P, "N_PRODUCTS") else 9), dtype=np.int64),
        prices=np.full((1, 9), 100, dtype=np.int64),
        n_land=np.array([0]),
        animal=np.full((1, TILES), -1, dtype=np.int64),
        fed_today=np.zeros((1, TILES), dtype=bool),
        cared_today=np.zeros((1, TILES), dtype=bool),
        consecutive_unfed=np.zeros((1, TILES), dtype=np.int64),
        fertilizer_available=np.zeros((1, TILES), dtype=bool),
        shed_animals=np.zeros((1, P.N_ANIMALS), dtype=np.int64),
        shed_wheat=np.array([shed_wheat]),
        carried_wheat=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        carried_animal=np.full((1, X.MAX_EXEC_UNITS), -1, dtype=np.int64),
    )


def test_the_fixture_is_the_configuration_that_failed():
    """Anti-vacuity: pens standing, stocking day reached, feed budgeted, cash on hand.

    If any of these were false the executor would be right to buy nothing, and every other
    assertion here would be measuring the wrong gate.
    """
    plan = _leaders()
    assert int(plan.stock_day[0]) <= 0, "stocking has not started on day 0 -- wrong gate"
    assert int(plan.herd[0].sum()) == 14, f"herd target moved: {plan.herd[0].tolist()}"
    assert int(plan.feed_wheat[0]) > 0, "feed_wheat 0 disables livestock by design"


def test_day_zero_spends_the_stake_on_animals_rather_than_reserving_it_for_feed():
    """**The claim.** $3,000 and 14 empty pens must buy more than one animal.

    The tape ends day 0 with four animals standing and $42 in the bank. Ours ends with one bought,
    none standing, and $304 held back.
    """
    d = X.decide(_view(), _leaders())
    bought = int(d.buy_animal[0].sum())
    wheat = int(d.buy_product[0, X.WHEAT_ITEM])
    reserved = wheat * X.WHEAT_PRICE_CAP

    assert bought >= 2, (
        f"bought {bought} animal(s) on day 0 from a ${STAKE:,.0f} stake with {PENS} empty pens, "
        f"while ordering {wheat} wheat -- ${reserved:,.0f} reserved at WHEAT_PRICE_CAP, "
        f"{reserved / STAKE:.0%} of the stake, before any animal was priced")


def test_a_shed_already_holding_the_feed_buys_the_herd():
    """**The discriminator.** No feed to order means no reservation; does the purchase come back?

    If this passes while the test above fails, the reservation is the cause and the fix belongs in
    how `wheat_order` is priced against `cash`. If this fails too, the reservation is innocent and
    something else is consuming the stake -- a different fix entirely.
    """
    plan = _leaders()
    stocked = int(plan.feed_wheat[0]) * int(plan.herd[0].sum())
    d = X.decide(_view(shed_wheat=stocked), plan)

    assert int(d.buy_product[0, X.WHEAT_ITEM]) == 0, (
        "the shed already holds the full requirement, so nothing should be ordered -- fixture is "
        "not isolating the reservation")
    bought = int(d.buy_animal[0].sum())
    afford = int(STAKE // X.ANIMAL_COST.min())
    assert bought >= min(2, afford), (
        f"bought {bought} with the feed already in the shed and ${STAKE:,.0f} in hand -- the "
        f"reservation is not what is starving the purchase")


@pytest.mark.parametrize("money", [3_000.0, 5_000.0])
def test_the_reservation_never_exceeds_half_the_bank(money):
    """The reservation is meant to over-estimate, not to dominate.

    Stated as a fraction rather than a dollar figure so it keeps meaning if `WHEAT_PRICE_CAP` or the
    opening stake moves.
    """
    d = X.decide(_view(money=money), _leaders())
    reserved = int(d.buy_product[0, X.WHEAT_ITEM]) * X.WHEAT_PRICE_CAP
    assert reserved <= money / 2, (
        f"${reserved:,.0f} of ${money:,.0f} ({reserved / money:.0%}) reserved for feed before a "
        f"single animal was priced")
