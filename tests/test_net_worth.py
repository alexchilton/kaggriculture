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


def test_inventory_is_marked_below_the_towns_price(state):
    """Held product is an asset, but not worth as much as the cash it fetches.

    **Was `== 10 * px` until 2026-08-24.** Marking held stock at the town's FULL price is what made
    SELL pay nothing: goods and the cash for them were the same number, so the last link in the chain
    -- the only one the game actually scores -- moved `PHI` not at all. `HELD` is the discount that
    makes selling pay the remainder; `test_selling_pays_the_gap_between_book_value_and_cash` is the
    acceptance test and this one is the guard that the mark is still most of the price, so a harvest
    still lands as an asset rather than as nothing.
    """
    before = NW.net_worth(state)
    farm = state.farm._replace(shed=state.farm.shed.at[:, 0, 0].add(10))   # 10 wheat
    after = NW.net_worth(state._replace(farm=farm))
    px = float(J.price(state.inventory)[0, 0])
    gain = float(after[0, 0] - before[0, 0])

    assert gain == pytest.approx(10 * px * NW.HELD, rel=1e-3)
    assert 0.0 < gain < 10 * px


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
    assert float(after[0, 0] - before[0, 0]) == pytest.approx(6 * melon_px * NW.UNPICKED, rel=1e-3)


def test_animal_product_uses_the_sims_own_pairing(state):
    """Unpicked eggs must be priced as eggs. The pairing comes from `J.ANIMAL_TO_PRODUCT`, not from
    this module guessing that animal *i* maps to product *5 + i*."""
    before = NW.net_worth(state)
    goose = _with_animal(state, unfed=0, fed_today=True)
    t = goose.tiles
    goose = goose._replace(tiles=t._replace(yield_units=t.yield_units.at[:, 0, 0].set(4)))
    egg_px = float(J.price(state.inventory)[0, int(J.ANIMAL_TO_PRODUCT[0])])
    gain = float(NW.net_worth(goose)[0, 0] - before[0, 0])
    assert gain == pytest.approx(float(J.ANIMAL_COST[0]) + 4 * egg_px * NW.UNPICKED, rel=1e-3)


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


def test_hoarding_the_opening_stake_earns_exactly_nothing(state):
    """Alex's requirement is "0 for 0", and standing still on the $3,000 stake must earn nothing.

    **Rewritten 2026-08-23, when EXPONENT went 2.0 -> 1.0 (Alex's call, on the numbers in
    `docs/fable_shaping_scale_and_plant_2026-08-23.md`).** This used to assert the stake was under 2%
    of a $28k season, which is a statement about the potential's *level* and was carrying the
    requirement only by accident. Linear puts the stake at 10.6% of a season and the assertion failed,
    while the thing Alex actually asked for was untouched.

    What enforces "0 for 0" is not the level, it is the telescoping. Episodes start at $3,000
    (`jax_sim.py:487`) and shaping pays `PHI(end) - PHI(start)`, so a policy that ends on its opening
    stake earns zero however the curve is shaped. That is asserted directly here rather than inferred
    from a ratio, and it holds for any EXPONENT.
    """
    assert float(NW.potential(jnp.asarray(0.0))) == pytest.approx(0.0)
    assert float(NW.shaping(3_000.0, 3_000.0, coef=1.0)) == pytest.approx(0.0)

    # And going broke is a loss rather than a free option, which the old hard floor at $3,000 made it.
    assert float(NW.shaping(3_000.0, 0.0, coef=1.0)) < 0.0


def test_a_bare_win_over_an_equally_broke_mirror_earns_almost_nothing():
    """**Alex's actual requirement**, which convexity was one way of delivering and SCALE is another.

    The old test asserted convexity itself -- `far > 10 * near` -- which is the mechanism, not the
    goal, and linear fails it by construction while satisfying the goal comfortably: $5 over a broke
    mirror is 5e-5 against a terminal win of 1.0, one part in 20,000. The margin is not what the Elo
    ladder scores (`CLAUDE.md`: *"A $43k win and a $4k win score identically"*), so what matters is
    that a hairline margin cannot compete with the win itself.
    """
    edge = float(NW.shaping(3_000.0, 3_005.0, coef=1.0))
    assert 0.0 < edge < 1e-4, edge

    # A real season, by contrast, must be worth a visible fraction of a win -- that is the whole point
    # of the rescale. $28,168 is the scripted farmer's bank.
    season = float(NW.shaping(3_000.0, 28_168.0, coef=1.0))
    assert 0.1 < season < 1.0, season
    assert season > 1_000 * edge


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
    assert 0.0 < ours < theirs < 0.5, (ours, theirs)


# ---- the ops the policy will not do --------------------------------------------------------------
#
# Alex, 2026-08-23: *"the only thing he is not doing is harvest and collecting milk and wool -- that is
# where we want the encouragement"*. Measured on the running job, `harv` is 0.07-0.09% of ops and
# `feed` is 0.00%, against a teacher harvest/plant ratio of 2.05 to our 0.37.
#
# v1 could not encourage either, and the reason is that it marked uncollected yield at FULL price. The
# milk was already on the books the moment the cow made it, so HARVEST moved $160 from one term to
# another and `PHI` did not change. The strongest thing in the ledger paid exactly nothing.
#
# Marking uncollected yield BELOW price splits the credit: some when it appears, the rest on the turn a
# hand picks it up. The discount is not a thumb on the scale -- uncollected yield is genuinely at risk
# in a way shed product is not. `jax_sim.py:1249` zeroes `yield_units` when a crop dies of thirst and
# `:1332` zeroes it when an animal escapes. Product in the shed cannot be lost either way.


def test_harvesting_a_ripe_crop_pays_on_the_turn_it_happens(state):
    """**The acceptance test for the whole change.** Under v1 this was worth exactly zero.

    A ripe melon is $250 on the tile and $250 in the hand, so the difference was nil and the op with
    the second-strongest correlation to money paid nothing at all.
    """
    ripe = _with_yield(state, crop=4, units=1)                 # melon on the tile
    picked = _harvested(ripe, product=M.PRODUCTS.index("MELON"), units=1)

    assert float(NW.net_worth(picked)[0, 0]) > float(NW.net_worth(ripe)[0, 0])


def test_collecting_milk_pays_on_the_turn_it_happens(state):
    """The animal side of the same defect. `ANIMAL_TO_PRODUCT` maps a cow to MILK, so milk sitting on
    the cow was already marked at $160 and the hand that walked over to collect it earned nothing."""
    full = _with_yield(state, animal=1, units=1)                # cow
    picked = _harvested(full, product=M.PRODUCTS.index("MILK"), units=1)

    assert float(NW.net_worth(picked)[0, 0]) > float(NW.net_worth(full)[0, 0])


def test_uncollected_yield_is_still_worth_something(state):
    """The guard on the other side, and it is load-bearing. Marking uncollected yield at zero would
    make HARVEST pay the most, and would also make FERTILIZE strictly negative again -- it destroys a
    $100 unit of fertiliser and its doubled yield would show up nowhere until picked. That is the exact
    trap `standing_yield_value` was written to close, so the discount must be a fraction, never zero."""
    bare = float(NW.net_worth(state)[0, 0])
    ripe = float(NW.net_worth(_with_yield(state, crop=4, units=1))[0, 0])
    price = float(J.price(state.inventory)[0, M.PRODUCTS.index("MELON")])

    assert 0.0 < (ripe - bare) < price, (ripe - bare, price)


def test_the_three_steps_of_a_crop_sum_to_its_price(state):
    """Nothing is invented and nothing is lost. Ripening, picking and selling must together be worth
    exactly what the product fetches, or the potential pays a bonus for the round trip."""
    bare = float(NW.net_worth(state)[0, 0])
    px = float(J.price(state.inventory)[0, M.PRODUCTS.index("MELON")])

    ripe = _with_yield(state, crop=4, units=1)
    picked = _harvested(ripe, product=M.PRODUCTS.index("MELON"), units=1)
    sold = state._replace(farm=state.farm._replace(money=state.farm.money.at[:, 0].add(px)))

    assert float(NW.net_worth(sold)[0, 0]) - bare == pytest.approx(px, abs=1e-3)
    # And each step is a strict increase, so no link in the chain is a dead spot.
    assert bare < float(NW.net_worth(ripe)[0, 0]) < float(NW.net_worth(picked)[0, 0]) \
        < float(NW.net_worth(sold)[0, 0])


# ---- the link that paid nothing: selling ----------------------------------------------------------
#
# Alex, 2026-08-24: *"i still think the money should be a dense strategy"*, and *"it aint learning
# that money is important at all"*. He is right, and the reason is in this file rather than in the
# trainer. `stock_value` marked shed goods at the town's full price, so swapping $160 of milk for
# $160 of cash moved `PHI` by nothing -- and slightly DOWN once the sale pushes the price on the
# stock still held. The ledger was indifferent between a barn full of wool and the money for it.
#
# Cash is the only thing the game scores: `END` is `bank_final_med`, the median bank a season
# FINISHED on, and `shaped2` sat at $0-$1 for 136 updates while harvesting and feeding both climbed.
# Marking held goods BELOW their sale price makes the last link pay, and the discount is honest for
# the same reason `UNPICKED` is: shed stock is marked optimistically, since selling N units walks the
# price down (`net_worth.py` "Known conservatism").


def test_selling_pays_the_gap_between_book_value_and_cash(state):
    """**The acceptance test for money being dense.** Under v1 this was worth exactly zero."""
    px = float(J.price(state.inventory)[0, M.PRODUCTS.index("MILK")])
    holding = state._replace(farm=state.farm._replace(
        shed=state.farm.shed.at[:, 0, M.PRODUCTS.index("MILK")].add(1)))
    sold = state._replace(farm=state.farm._replace(money=state.farm.money.at[:, 0].add(px)))

    assert float(NW.net_worth(sold)[0, 0]) > float(NW.net_worth(holding)[0, 0])


def test_holding_stock_is_still_worth_most_of_its_price(state):
    """The guard on the other side. Marking shed goods at zero would make HARVEST and every
    collection pay nothing again, and would price a full shed as an empty one."""
    px = float(J.price(state.inventory)[0, M.PRODUCTS.index("MILK")])
    bare = float(NW.net_worth(state)[0, 0])
    holding = state._replace(farm=state.farm._replace(
        shed=state.farm.shed.at[:, 0, M.PRODUCTS.index("MILK")].add(1)))

    assert 0.0 < float(NW.net_worth(holding)[0, 0]) - bare < px


def test_an_animal_in_the_shed_is_still_marked_at_full_cost(state):
    """**The discount is on PRODUCTS only.** Livestock must stay at cost or BUY_ANIMAL stops being
    neutral and the ledger starts arguing against the animal chain -- the exact thing this module was
    written to prevent. `test_buying_an_animal_at_cost_is_a_wash` is the pair to this."""
    before = NW.net_worth(state)
    cost = float(J.ANIMAL_COST[0])
    farm = state.farm._replace(shed=state.farm.shed.at[:, 0, M.N_PRODUCTS + 0].add(1))
    after = NW.net_worth(state._replace(farm=farm))

    assert float(after[0, 0] - before[0, 0]) == pytest.approx(cost, abs=1e-3)


# ---- helpers -------------------------------------------------------------------------------------


def _with_yield(state, crop=J.NO_CROP, animal=J.NO_ANIMAL, units=1):
    """Seat 0 has `units` of unpicked yield on tile 0, from a crop or from an animal."""
    t = state.tiles
    kind = J.PASTURE if animal != J.NO_ANIMAL else J.PLANT
    tiles = t._replace(
        kind=t.kind.at[:, 0, 0].set(kind),
        crop=t.crop.at[:, 0, 0].set(crop),
        animal=t.animal.at[:, 0, 0].set(animal),
        yield_units=t.yield_units.at[:, 0, 0].set(units),
        fed_today=t.fed_today.at[:, 0, 0].set(True),
    )
    return state._replace(tiles=tiles)


def _harvested(state, product, units=1):
    """`jax_sim.py:668,846` -- the op decrements `yield_units` and the product lands in a unit's hands."""
    t = state.tiles
    tiles = t._replace(yield_units=t.yield_units.at[:, 0, 0].add(-units))
    farm = state.farm._replace(carried=state.farm.carried.at[:, 0, 0, product].add(units))
    return state._replace(tiles=tiles, farm=farm)


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
