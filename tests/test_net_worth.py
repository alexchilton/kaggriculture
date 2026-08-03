"""Net-worth potential: what a farm is worth marked to market, and why that shape is the safe one.

**The theory, stated before the code.** `kagg/rl/money_potential.py` values *cash*, so it punishes the
animal chain at the moment of investment: buying a goose takes money from $12,000 to $11,600 and the
milk arrives 100+ turns later. Alex's objection, and it is correct -- a cash potential makes the cost
of the chain more visible while leaving the benefit exactly as far away, which is the opposite of what
is wanted. A goose in a pasture is *capital*, and cash accounting books it as pure loss until it
produces.

Valuing assets instead makes a purchase at fair value a **wash**: cash down $400, livestock up $400,
`PHI` unchanged. No penalty for investing, and no reward either -- see
`test_buying_an_animal_at_cost_is_a_wash`, which is the property that makes this accounting rather
than strategy. It says assets are worth what they would fetch; it does not say animals are good.

**Why that is still safe.** `F(s, s') = gamma * PHI(s') - PHI(s)` leaves the optimal policy provably
unchanged (Ng, Harada & Russell 1999), and at gamma 1.0 the terms telescope to `PHI(end) - PHI(start)`.
That holds for *any* `PHI`, so the invariance is not what distinguishes a good one from a bad one --
the distinction is whether it biases finite-sample search toward a belief of ours. Marking to market
does not; hand-weighting the links of the animal chain would.

**The trap this file exists to pin.** Naive book-cost accounting gets the sign *backwards* on the two
ops that matter most. `FEED` destroys a unit of wheat and adds nothing to a balance sheet; `FERTILIZE`
destroys a unit of fertiliser and adds nothing. Under a naive net worth both are **negative**, so it
would actively discourage the two strongest money predictors in the game -- FEED +0.452 and CARE
+0.441 over 312 real leaderboard seats (`CLAUDE.md`).

The fix is to value the intangible each one buys, and the simulator supplies a non-arbitrary basis:
`jax_sim.py:1159` escapes an animal at `consecutive_unfed >= 2`, so an animal one night from bolting
really is worth less than a fed one. That is the sim's own rule, not a dial we chose.
`test_feeding_pays_on_the_turn_it_happens` is the acceptance test for the whole idea.
"""

import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.sim import jax_sim as J          # noqa: E402
from kagg.sim import market as M           # noqa: E402

NW = pytest.importorskip("kagg.rl.net_worth")


@pytest.fixture(scope="module")
def state():
    return J.reset_with_shops(2, seed=0)


# ---- the layout assumption, pinned rather than trusted --------------------------------------------


def test_animals_occupy_the_tail_of_the_item_axis():
    """`net_worth` slices `shed[..., N_PRODUCTS:]` and indexes it with `ANIMAL_COST`, which is only
    valid because `market.ITEMS == PRODUCTS + ANIMALS`. If an item is ever inserted in the middle,
    livestock in the shed would be priced with a product's price and nothing would raise."""
    assert M.ITEMS[:M.N_PRODUCTS] == M.PRODUCTS
    assert list(M.ANIMAL_ITEM) == list(range(M.N_PRODUCTS, M.N_ITEMS))


# ---- the core accounting property ----------------------------------------------------------------


def test_buying_an_animal_at_cost_is_a_wash(state):
    """**The property that makes this accounting and not strategy.** Cash out, asset in, `PHI` flat.

    A cash-only potential would show this as a loss and discourage every investment. A potential that
    *rewarded* it would be encoding our belief that animals are good, which is the thing that biases
    the search. Fair value means neither.
    """
    before = NW.net_worth(state)
    cost = float(J.ANIMAL_COST[0])                        # a goose

    # Pay for it and receive it into the shed, exactly as the market phase does.
    farm = state.farm._replace(
        money=state.farm.money.at[:, 0].add(-cost),
        shed=state.farm.shed.at[:, 0, M.N_PRODUCTS + 0].add(1),
    )
    after = NW.net_worth(state._replace(farm=farm))

    assert float(after[0, 0]) == pytest.approx(float(before[0, 0]), abs=1e-3)


def test_an_animal_one_night_from_escaping_is_worth_less_than_a_fed_one(state):
    """`jax_sim.py:1159` escapes at `consecutive_unfed >= 2`. An animal with one night of slack left
    is a depreciating asset and must mark below a fresh one, or skipping a feed costs nothing."""
    placed = _with_animal(state, unfed=0, fed_today=True)
    hungry = _with_animal(state, unfed=1, fed_today=False)
    assert float(NW.net_worth(hungry)[0, 0]) < float(NW.net_worth(placed)[0, 0])


def test_an_animal_that_has_already_escaped_is_worth_nothing(state):
    """The floor. `NO_ANIMAL` on a bare structure must contribute zero, so the escape shows up as the
    full loss rather than a partial one."""
    empty = _with_animal(state, unfed=0, fed_today=False, animal=J.NO_ANIMAL)
    bare = NW.net_worth(empty)[0, 0]
    assert float(bare) == pytest.approx(float(state.farm.money[0, 0]), abs=1e-3)


def test_feeding_pays_on_the_turn_it_happens(state):
    """**The acceptance test for the whole idea.** FEED destroys a unit of wheat, so naive book-cost
    accounting scores it negative. Valuing the animal against its escape clock makes it positive: the
    wheat is worth ~$50 and the restored slack on a $300-$500 animal is worth far more.

    Note the credit lands on the FEED turn, not at the nightly pass, because the valuation uses what
    `consecutive_unfed` *will* be tonight rather than what it is now.
    """
    hungry = _with_animal(state, unfed=1, fed_today=False, carry_wheat=True)
    fed = _with_animal(state, unfed=1, fed_today=True, carry_wheat=False)
    assert float(NW.net_worth(fed)[0, 0]) > float(NW.net_worth(hungry)[0, 0])


def test_missing_a_feed_costs_something_on_the_turn_the_clock_moves(state):
    """The mirror of the above, and the reason the daily oscillation is signal rather than noise:
    an animal not fed today loses value tonight. Take that loss every day and never take the
    corresponding gain and the arithmetic says the animal was a bad purchase -- which is true."""
    fed = _with_animal(state, unfed=0, fed_today=True)
    skipped = _with_animal(state, unfed=0, fed_today=False)
    assert float(NW.net_worth(skipped)[0, 0]) < float(NW.net_worth(fed)[0, 0])


def test_inventory_is_marked_to_the_towns_price(state):
    """Held product is an asset. Without this a harvest would look like it created nothing until the
    sale, which is the same credit-delay problem one link further down the chain."""
    before = NW.net_worth(state)
    farm = state.farm._replace(shed=state.farm.shed.at[:, 0, 0].add(10))   # 10 wheat
    after = NW.net_worth(state._replace(farm=farm))
    px = float(J.price(state.inventory)[0, 0])
    assert float(after[0, 0] - before[0, 0]) == pytest.approx(10 * px, rel=1e-3)


# ---- the potential and the shaping ---------------------------------------------------------------


def test_unharvested_yield_on_a_plant_is_an_asset(state):
    """**The FERTILIZE fix.** `yield_units` is product that exists and is waiting to be picked
    (`jax_sim.py:1048` decrements it on harvest), so it must mark to market. Without this a doubled
    melon yield is worth nothing until the sale and FERTILIZE is strictly negative."""
    before = NW.net_worth(state)
    t = state.tiles
    tiles = t._replace(
        kind=t.kind.at[:, 0, 0].set(J.PLANT),
        crop=t.crop.at[:, 0, 0].set(4),                      # melon
        yield_units=t.yield_units.at[:, 0, 0].set(6),
    )
    after = NW.net_worth(state._replace(tiles=tiles))
    melon_px = float(J.price(state.inventory)[0, 4])
    assert float(after[0, 0] - before[0, 0]) == pytest.approx(6 * melon_px, rel=1e-3)


def test_animal_product_uses_the_sims_own_pairing(state):
    """Unpicked eggs must be priced as eggs. The pairing comes from `J.ANIMAL_TO_PRODUCT`, not from
    this module guessing that animal *i* maps to product *5 + i*."""
    before = NW.net_worth(state)
    goose = _with_animal(state, unfed=0, fed_today=True)
    t = goose.tiles
    goose = goose._replace(tiles=t._replace(yield_units=t.yield_units.at[:, 0, 0].set(4)))
    egg_px = float(J.price(state.inventory)[0, int(J.ANIMAL_TO_PRODUCT[0])])
    gain = float(NW.net_worth(goose)[0, 0] - before[0, 0])
    assert gain == pytest.approx(float(J.ANIMAL_COST[0]) + 4 * egg_px, rel=1e-3)


def test_fertilizing_is_not_punished_once_the_yield_lands(state):
    """The end-to-end version of the fix: spend a unit of fertiliser and gain the doubled melon it
    buys, and net worth must be higher than it was before. This is the acceptance test for the op the
    replay measures at `raw 0`."""
    t = state.tiles
    plant = t._replace(kind=t.kind.at[:, 0, 0].set(J.PLANT), crop=t.crop.at[:, 0, 0].set(4))

    holding = state._replace(
        tiles=plant._replace(yield_units=plant.yield_units.at[:, 0, 0].set(3)),
        farm=state.farm._replace(carried=state.farm.carried.at[:, 0, 0, 8].add(1)),
    )                                                        # 3 melons + a unit of fertiliser
    doubled = state._replace(
        tiles=plant._replace(yield_units=plant.yield_units.at[:, 0, 0].set(6)),
    )                                                        # fertiliser spent, yield doubled
    assert float(NW.net_worth(doubled)[0, 0]) > float(NW.net_worth(holding)[0, 0])


def test_the_opening_stake_is_worth_a_rounding_error(state):
    """Alex's requirement is "0 for 0", and standing still on the $3,000 stake must earn effectively
    nothing.

    **This asserted `PHI(3_000) == 0` exactly until the floor moved to $0 on 2026-08-03.** The hard
    floor turned out to be a dead zone: `bank_final_med` fell to $1,856, so whole seasons sat where the
    gradient was identically zero. The convexity does the same job -- the stake is 1.1% of a $28k
    season -- without deleting the signal. See `tests/test_potential_floor_and_cap.py`.
    """
    assert float(NW.potential(jnp.asarray(0.0))) == pytest.approx(0.0)
    stake = float(NW.potential(jnp.asarray(3_000.0)))
    season = float(NW.potential(jnp.asarray(28_168.0)))
    assert stake >= 0.0 and stake / season < 0.02


def test_the_potential_is_convex_above_the_stake():
    """Alex's requirement: the same $1,000 is worth far more at $90k than at $4k, so a $5 win over an
    equally broke mirror earns almost nothing."""
    near = NW.potential(jnp.asarray(5_000.0)) - NW.potential(jnp.asarray(4_000.0))
    far = NW.potential(jnp.asarray(91_000.0)) - NW.potential(jnp.asarray(90_000.0))
    assert float(far) > 10 * float(near)


def test_the_shaping_telescopes_so_only_the_endpoints_matter():
    """The invariance, checked directly rather than cited. A path's shaping sums to
    `PHI(end) - PHI(start)` whatever route it took, so it cannot pay for a detour."""
    path = [3_000.0, 12_000.0, 400.0, 28_000.0, 9_000.0]
    total = sum(float(NW.shaping(a, b, coef=1.0)) for a, b in zip(path, path[1:]))
    endpoints = float(NW.potential(jnp.asarray(path[-1])) - NW.potential(jnp.asarray(path[0])))
    assert total == pytest.approx(endpoints, abs=1e-6)


def test_a_zero_coefficient_is_exactly_off(state):
    """A run with shaping off must be byte-identical to a run made before the term existed, or the
    A/B is not an A/B."""
    assert float(NW.shaping(3_000.0, 90_000.0, coef=0.0)) == 0.0


def test_the_potential_of_a_realistic_season_stays_below_the_terminal_reward(state):
    """**The scale check that matters.** Invariance protects the optimum, not the learning dynamics:
    a `PHI` whose range swamps the terminal reward's 1.0 becomes the objective in practice whatever
    the theorem says. The replayed policy banks ~$12.5k and the scripted farmer ~$28.2k, so the gap
    we are trying to close must sit well under 1.0."""
    ours = float(NW.potential(jnp.asarray(12_478.0)))
    theirs = float(NW.potential(jnp.asarray(28_168.0)))
    assert 0.0 < ours < theirs < 0.25, (ours, theirs)


# ---- helpers -------------------------------------------------------------------------------------


def _with_animal(state, unfed, fed_today, animal=0, carry_wheat=False):
    """Seat 0 owns one animal on tile 0, with the given feeding clock."""
    t = state.tiles
    kind = t.kind.at[:, 0, 0].set(J.PASTURE if animal != 0 else J.COOP)
    tiles = t._replace(
        kind=kind,
        animal=t.animal.at[:, 0, 0].set(animal),
        consecutive_unfed=t.consecutive_unfed.at[:, 0, 0].set(unfed),
        fed_today=t.fed_today.at[:, 0, 0].set(fed_today),
    )
    carried = state.farm.carried
    if carry_wheat:
        carried = carried.at[:, 0, 0, 0].add(1)
    return state._replace(tiles=tiles, farm=state.farm._replace(carried=carried))
