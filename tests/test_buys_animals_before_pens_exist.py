"""Day 0, hour 1: the winner buys a cow with no pasture built. We buy nothing.

Measured on episode 89873723 seat 0, teacher-forced on the correct pre-action board
(`data/logs/day_diff_0_aligned.log`):

    h1  $3,000 crew 1
        theirs  BUY_ANIMAL/COWx1  BUY_SEED/MELONx6  BUY_SEED/WHEATx6  HIREx2  SELL/WHEATx5
        ours    BUY_SEED/WHEATx8  HIREx3

    decide wants buy_animal {GOOSE: 0, COW: 0, SHEEP: 0}
    pens on board now: 0
    herd target: [GOOSE 0, COW 8, SHEEP 4]

`executor.housing` is `n_pens_free - shed_stock`, and `n_pens_free` counts pens **already standing**.
At hour 1 of day 0 nothing is built yet, so housing is 0 and no animal is ever ordered. The seat being
copied buys three cows and a sheep across day 0 -- $3,000, its entire stake -- into the *shed*, and
places them as the pastures go up (its first `PLACE` lands at h4).

An animal in the shed needs no pen. `BUY_ANIMAL` deposits it there and `PLACE` consumes it later, which
is why `View` carries `shed_animals` at all. So the gate has to be the pens the plan *commits* --
`plan.crop_of` -- not the pens that happen to exist at this hour. This is the same defect as
`want_wheat` being gated on placed animals rather than intended ones, fixed earlier the same day.

The cap still has to exist: an animal that can never be housed is money lit on fire, and one unfed two
nights escapes with its whole purchase price (`jax_sim.py:1057`). It just has to count planned pens.
"""

import numpy as np
import pytest

from kagg.search import agent as A
from kagg.search import executor as X
from kagg.search import plan as P, replay_plan as RP
from kagg.sim.tiles import EMPTY

EPISODE = "data/episodes/89873723.json"
COW = P.ANIMAL_NAMES.index("COW")


def _plan(pens=4, herd=4, feed=2, stock_day=0):
    """A plan that commits `pens` pastures and wants `herd` cows, with feed budgeted."""
    g = np.zeros(P.N_GENES, dtype=np.int64)
    lo, _ = P.gene_slice("crop_of")
    g[lo:lo + pens] = P.CROP_GENE_PASTURE
    a, _ = P.gene_slice("herd")
    g[a + COW] = P.herd_gene(herd)
    lo, _ = P.gene_slice("feed_wheat")
    g[lo] = int(np.flatnonzero(np.asarray(P.FEED_WHEAT) == feed)[0])
    lo, _ = P.gene_slice("stock_day")
    g[lo] = int(np.abs(np.asarray(P.STOCK_DAYS) - stock_day).argmin())
    return P.decode(g[None])


def _bare_view(money=3000.0):
    """An empty farm on day 0: no pens standing, nothing in the shed. The opening board."""
    tiles = 100
    return X.View(
        day=0, hour=1,
        kind=np.full((1, tiles), EMPTY, dtype=np.int64),
        crop=np.full((1, tiles), -1, dtype=np.int64),
        planted_day=np.zeros((1, tiles), dtype=np.int64),
        watered=np.zeros((1, tiles), dtype=bool),
        yield_units=np.zeros((1, tiles), dtype=np.int64),
        unit_ord=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        n_units=np.array([1]),
        money=np.array([money]),
        seeds=np.zeros((1, P.N_CROPS), dtype=np.int64),
        shed=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
        prices=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
        n_land=np.array([0]),
    )


@pytest.mark.xfail(strict=True, reason="deferred: Alex parked the decision/gate work until action-tape replication was proven. The gate is `executor.housing`, which counts pens already standing rather than pens `plan.crop_of` commits.")
def test_an_animal_is_bought_although_no_pen_is_standing_yet():
    """**The bug.** Four pastures planned, none built, day 0 -- the order must still go in."""
    decision = X.decide(_bare_view(), _plan(pens=4, herd=4))

    assert int(decision.buy_animal[0, COW]) > 0, (
        "no cow ordered on an empty day-0 board. The plan commits four pastures and wants four cows; "
        "`housing` counts only pens already standing, so nothing is ever bought on the day the pens "
        "are raised. The seat being copied spends its entire $3,000 stake on animals during day 0.")


def test_it_never_orders_more_animals_than_the_plan_has_pens_for():
    """The cap must survive the fix -- an animal that can never be housed is a pure loss."""
    decision = X.decide(_bare_view(money=100_000.0), _plan(pens=2, herd=8))

    assert int(decision.buy_animal[0, COW]) <= 2, (
        f"plan commits 2 pastures but ordered {int(decision.buy_animal[0, COW])} cows")


def test_stock_day_still_holds_the_order_back():
    """`stock_day` is the gene that says *when* to stock, and it must keep working."""
    decision = X.decide(_bare_view(), _plan(pens=4, herd=4, stock_day=8))

    assert int(decision.buy_animal[0, COW]) == 0, "bought before stock_day"


def test_no_animals_when_the_plan_budgets_no_feed():
    """`feed_wheat = 0` means "no animals" -- a herd with no feed reserve starves by construction."""
    decision = X.decide(_bare_view(), _plan(pens=4, herd=4, feed=0))

    assert int(decision.buy_animal[0, COW]) == 0


@pytest.mark.skipif(not __import__("pathlib").Path(EPISODE).exists(), reason="replay not present")
@pytest.mark.xfail(strict=True, reason="deferred: Alex parked the decision/gate work until action-tape replication was proven. The gate is `executor.housing`, which counts pens already standing rather than pens `plan.crop_of` commits.")
def test_on_the_winners_own_opening_board_an_animal_is_ordered():
    """End to end on the real tape, at the hour the seat bought its first cow."""
    layout = RP.layout_from_replay(EPISODE, seat=0)
    plan = P.decode(RP.genome_from_layout(layout)[None])

    for turn, obs, theirs in RP.teacher_forced_pairs(EPISODE, seat=0):
        if turn != 1:
            continue
        decision = X.decide(A.observation_view(obs), plan)
        assert int(decision.buy_animal[0].sum()) > 0, (
            "hour 1 of day 0: they ordered a COW and we ordered no animal at all")
        return
    pytest.fail("turn 1 not present in the replay")
