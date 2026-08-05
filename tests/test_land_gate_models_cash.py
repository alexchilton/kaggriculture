"""The land gate must weigh the amount, not just the day.

We own **25 tiles**. The leader owns **75** -- NE on day 7 and SW on day 10, $3,000 in total, never SE.
That is three times the board, all season, and it is the whole difference. Our best genome orders
**zero parcels**.

The reason it never buys any is this gate. `_affordable` refused a parcel only when it was ordered
before `EARLIEST_REVENUE_DAY` and the running total exceeded the opening bank; from day 3 onward every
parcel was assumed affordable **whatever it cost and whatever else the farm had committed to**. So a
genome that wants two parcels passes, buys one, and `_do_buy_land` silently no-ops the other -- after
which the chain walks until a LOCKED tile stops it and builds there, and `decode()` still reports it as
`used`.

The search then learns exactly the wrong lesson. Every land-based genome it tried came back looking like
a loss, because half of them were farms that had paid for ground they did not get. So it stopped
proposing land, and stayed on 25 tiles.

The fix is not a cleverer heuristic. It is to make the estimate account for what the farm has already
spent by that day, so a plan that cannot pay is **refused and counted** rather than half-executed and
reported as fine. A refused chain scores as a missing chain, which is honest; a relocated one scores as
a mystery.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")


def _row(kind, what, block_i, start_day, land_day=0):
    what_i = (R.ANIMAL_NAMES if kind == "ranch" else R.CROPS).index(what)
    row = [C.KINDS.index(kind), what_i, block_i,
           C.START_DAY_CHOICES.index(start_day), C.LAND_DAY_CHOICES.index(land_day)]
    return row + [0] * (len(C.GENES) - len(row))


def _genome(rows, n_slots=8):
    g = np.zeros((n_slots, len(C.GENES)), dtype=np.int64)
    for i, r in enumerate(rows):
        g[i] = r
    return g.reshape(-1)


def _block_needing(parcels):
    for i, b in enumerate(C.BLOCKS):
        if R.land_purchases_for(b[0]) == parcels:
            return i, b
    return None, None


def _locked_at_bell(script, seed=0):
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in FIELDS}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return int((np.asarray(state.tiles.kind)[0, 0] == J.LOCKED).sum())


def test_the_premise_we_start_with_one_quadrant():
    """25 tiles of 100. Everything in this file is about the other 75."""
    owned = [(x, y) for y in range(R.BOARD_SIZE) for x in range(R.BOARD_SIZE)
             if R.land_purchases_for((x, y)) == 0]
    assert len(owned) == 25
    assert sum(R.LAND_PRICES[:2]) == 3000, "NE + SW is what the leader buys"


def test_a_single_cheap_parcel_out_of_revenue_is_still_allowed():
    """The gate must not become so strict that it refuses the leader's own move.

    One parcel on day 7 is $1,000 against a week of revenue. This has to pass, or we have replaced
    'always yes' with 'always no' and lost the same 50 tiles a different way.
    """
    i, _b = _block_needing(1)
    if i is None:
        pytest.skip("no single-parcel block")
    _script, used, skipped = C.decode(_genome([_row("grow", "MELON", i, 9, land_day=7)]), 8)
    assert skipped == 0 and used, "a $1,000 parcel funded by a week of revenue was refused"


def test_two_parcels_and_a_seed_bill_on_the_same_day_are_refused_or_delivered():
    """The defect, stated as a contract rather than a mechanism.

    A chain on SW ordering both parcels from day 7 while buying its own seed either has to be refused
    (and counted in `skipped`), or the parcels have to actually clear. What it must not do is report the
    chain as placed while standing on locked ground.
    """
    i, _b = _block_needing(2)
    if i is None:
        pytest.skip("no two-parcel block")
    script, used, skipped = C.decode(_genome([_row("grow", "MELON", i, 8, land_day=7)]), 8)
    if skipped:
        return                                   # refused up front: honest
    # Otherwise both parcels must genuinely have cleared: NW+NE+SW owned leaves 25 locked.
    assert _locked_at_bell(script) <= 25, (
        f"reported {used} as placed, but the board still has "
        f"{_locked_at_bell(script)} locked tiles -- a parcel silently failed")


def test_seven_thousand_of_land_is_refused_while_the_farm_cannot_pay():
    """Three parcels is $7,000 against a $3,000 bank.

    Deliberately scoped to the days where it is *unaffordable*, not to the whole season. By day 20 a
    real farm may genuinely hold $7,000, and the gate's job is to model cash, not to overrule strategy --
    if a late SE purchase is a bad idea, the score should say so, not the decoder.
    """
    i, _b = _block_needing(3)
    if i is None:
        pytest.skip("no three-parcel block")
    for land_day in (0, 3, 5, 9):
        _script, used, skipped = C.decode(
            _genome([_row("grow", "MELON", i, min(land_day + 3, 28), land_day=land_day)]), 8)
        assert skipped >= 1 or not used, (
            f"land_day={land_day}: $7,000 of land reported as usable on a $3,000 bank ({used})")


def test_the_gate_weighs_the_amount_not_only_the_day():
    """Directly: two plans on the same day, one cheap and one dear, must not be judged alike."""
    cheap, _ = _block_needing(1)
    dear, _ = _block_needing(3)
    if cheap is None or dear is None:
        pytest.skip("need both a one-parcel and a three-parcel block")
    _s1, u1, sk1 = C.decode(_genome([_row("grow", "MELON", cheap, 12, land_day=9)]), 8)
    _s2, u2, sk2 = C.decode(_genome([_row("grow", "MELON", dear, 12, land_day=9)]), 8)
    assert (sk1, bool(u1)) != (sk2, bool(u2)), (
        "a $1,000 plan and a $7,000 plan on the same day decode identically; the gate is reading the "
        "day and ignoring the price")


def test_a_farm_that_earns_first_can_afford_more_than_one_that_does_not():
    """The point of the whole exercise: land bought out of revenue is a real strategy, and the gate has
    to be able to tell the difference between a farm that earned it and one that did not."""
    dear, _ = _block_needing(2)
    if dear is None:
        pytest.skip("no two-parcel block")
    nw = next(i for i, b in enumerate(C.BLOCKS) if C.land_cost(b[0]) == 0)
    alone = _genome([_row("grow", "MELON", dear, 8, land_day=7)])
    earning = _genome([_row("grow", "MELON", nw, 0),
                       _row("grow", "MELON", dear, 12, land_day=10)])
    _sa, _ua, ska = C.decode(alone, 8)
    _se, ue, ske = C.decode(earning, 8)
    assert ske <= ska, (
        "a farm with a revenue-earning chain in front of its land purchase is refused at least as "
        "often as one with nothing earning; the gate is not modelling cash at all")