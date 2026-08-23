"""What a farm is worth marked to market, and the potential built on it.

**Why this exists rather than `money_potential` alone.** That one values *cash*, so it punishes the
animal chain at the moment of investment: buying a goose moves money $12,000 -> $11,600 and the milk
arrives 100+ turns later. It makes the *cost* of the chain more visible while leaving the benefit
exactly as far away, which is the opposite of the intent. Alex's objection, and it is correct -- a
goose in a pasture is **capital**, and cash accounting books it as pure loss until it produces.

Valuing assets makes a purchase at fair value a **wash**: cash down $400, livestock up $400, `PHI`
unchanged. That single property is what makes this accounting rather than strategy. It says assets are
worth what they would fetch; it does not say animals are good. A `PHI` that *rewarded* buying an
animal would be encoding our belief, and while it would still be policy-invariant -- any potential
telescopes -- it would bias finite-sample search toward that belief.

**What it does and does not buy.** It removes the penalty on the chain's head; it does not create a
pull up it. Under fair-value accounting every pure conversion is `dPHI = 0`:

    BUILD_PASTURE   free, worthless            dPHI = 0
    BUY_ANIMAL      cash -$400, asset +$400    dPHI = 0
    PICKUP / PLACE  nothing moves              dPHI = 0
    FEED            -wheat, +restored slack    dPHI > 0
    HARVEST         product appears            dPHI > 0

So the head is a **plateau**, not a hill. That converts a 600-turn credit desert into a ~4-action
plateau, which is a real gain -- the tail now pays on the turn it happens without depending on a critic
sitting at `ev_signal` 0.30 -- but entropy is still the only thing crossing it. The reason to cross has
to come from an opponent that melon cannot beat. See `docs/ideas.md`.

**The trap, and why FEED is positive here.** Naive book-cost accounting gets the sign backwards on the
two ops that matter most: `FEED` destroys a unit of wheat and `FERTILIZE` destroys a unit of
fertiliser, and neither adds anything to a balance sheet. Under a naive net worth both are negative --
it would discourage the strongest money predictors in the game (FEED +0.452, CARE +0.441 over 312 real
seats, `CLAUDE.md`).

The fix is to value the intangible, on a basis the simulator supplies rather than one we choose:
`jax_sim.py:1147-1159` escapes an animal at `consecutive_unfed >= 2`, so an animal one night from
bolting really is worth less than a fed one. Feeding restores that slack, and the arithmetic
($50 of wheat against half of a $300-$500 animal) makes FEED strongly positive.

**The daily oscillation is signal, not noise.** Because freshness is computed from what
`consecutive_unfed` *will* be tonight, a fed animal marks at 1.0 and drops to 0.5 after the nightly
pass -- so an animal fed every day oscillates. That looked like noise worth avoiding, but it is not:
it is a **daily rent**. Feed and you take the gain; skip and you take only the loss. Over a season the
terms telescope to `PHI(end) - PHI(start)` regardless, so nothing is being invented.

**Standing crops are deliberately NOT valued.** Expected yield x price x maturity is the most
judgement-laden piece and the easiest place to smuggle in a strategy. v1 leaves it out; a harvest
shows up as inventory the moment it lands, which is one link later but still ~700 turns earlier than
today.

**Known conservatism.** Held product is marked at the town's current price, but selling N units moves
that price down (`price(inventory)`), so a large holding is marked optimistically. A first-order mark
is the sim's own number and is the honest default; it is recorded here so nobody reads the figure as a
liquidation value.
"""

import jax.numpy as jnp

from kagg.sim import jax_sim as J

# Re-exported so there is exactly one convex-potential formula in the project. `money_potential`
# documents the choice of each constant: zero at the $3,000 opening stake so hoarding earns nothing,
# normalised at $100,000 so a realistic winning season sits at PHI ~ 1 rather than dwarfing the
# terminal reward, and convex so a $5 win over an equally broke mirror is worth almost nothing.
from kagg.rl.money_potential import (  # noqa: F401
    DEFAULT_COEF, EXPONENT, FLOOR, SCALE, potential, shaping,
)

# `jax_sim.py:1159`: `escaped = has_animal & (unfed >= 2)`. Not a tunable -- it is the rule.
ESCAPE_AFTER = 2.0

# **What unpicked yield is worth against the same product sitting in the shed.**
#
# v1 marked it at 1.0, and that made HARVEST pay exactly nothing: a ripe melon was $250 on the tile and
# $250 in the hand, so `PHI` did not move. Measured on `shaped-20260823-205541`, `harv` ran at 0.07% of
# ops against a teacher harvest/plant ratio of 2.05 to our 0.37 -- the op we most wanted was the one op
# the ledger was silent about. Alex, 2026-08-23: *"the only thing he is not doing is harvest and
# collecting milk and wool -- that is where we want the encouragement"*.
#
# The discount splits the credit: half when the crop ripens or the cow fills, half on the turn a hand
# picks it up. It is not a thumb on the scale. Unpicked yield really is worth less than shed product
# because it can still be lost -- `jax_sim.py:1249` zeroes `yield_units` when a crop dies of thirst and
# `:1332` zeroes it when an animal escapes. Nothing can take product out of the shed.
#
# It must never reach 0. At 0 the FERTILIZE hole reopens: fertiliser destroys a ~$100 unit and its
# doubled yield would show up nowhere until picked, which is the trap `standing_yield_value` exists to
# close. `test_uncollected_yield_is_still_worth_something` pins that.
UNPICKED = 0.5


def freshness(tiles):
    """`[B, P, TILES]` in [0, 1]: how much of an animal's value survives tonight.

    Computed from what `consecutive_unfed` **will be** after the nightly pass, not what it is now, so
    the credit for a FEED lands on the turn the unit feeds rather than hours later at the day boundary.
    An animal already at `unfed == 1` and unfed again tonight escapes, so it marks at zero -- which is
    correct, and is what makes skipping a feed cost something immediately.
    """
    tonight = jnp.where(tiles.fed_today, 0, tiles.consecutive_unfed + 1).astype(jnp.float32)
    return jnp.clip(1.0 - tonight / ESCAPE_AFTER, 0.0, 1.0)


def livestock_value(tiles):
    """`[B, P]` -- placed animals at cost, discounted by how close they are to escaping."""
    has_animal = tiles.animal != J.NO_ANIMAL
    cost = J.ANIMAL_COST[jnp.clip(tiles.animal, 0, J.ANIMAL_COST.shape[0] - 1)]
    return jnp.where(has_animal, cost.astype(jnp.float32) * freshness(tiles), 0.0).sum(axis=-1)


def stock_value(state):
    """`[B, P]` -- everything in the shed and in units' hands, marked to market.

    The item axis is `PRODUCTS + ANIMALS` (`market.py:42`), so the split below is a slice. That layout
    is pinned by `tests/test_net_worth.py::test_animals_occupy_the_tail_of_the_item_axis` rather than
    assumed: an item inserted in the middle would silently price livestock as a product.

    An animal in the shed is not yet on a feeding clock, so it marks at full cost -- which is what
    makes buying one a wash.
    """
    held = (state.farm.shed + state.farm.carried.sum(axis=2)).astype(jnp.float32)
    px = J.price(state.inventory).astype(jnp.float32)              # [B, N_PRODUCTS]
    products = (held[..., :J.N_PRODUCTS] * px[:, None, :]).sum(axis=-1)
    animals = (held[..., J.N_PRODUCTS:] * J.ANIMAL_COST[None, None, :].astype(jnp.float32)
               ).sum(axis=-1)
    return products + animals


def standing_yield_value(state):
    """`[B, P]` -- product that has grown but not yet been harvested, marked at `UNPICKED` of price.

    The discount is what makes HARVEST pay; see the constant for why it is neither 1.0 nor 0.0.

    **This is the fix for the FERTILIZE hole, and it is load-bearing.** Without it `FERTILIZE` is
    strictly negative: it destroys a ~$100 unit of fertiliser and, with nothing on the plant side of
    the ledger, adds nothing. So v1 would have *discouraged* the op that the replay measures at
    exactly `raw 0` -- the precise trap this module's own docstring was written to warn about, and one
    that only FEED had a test for.

    Unpicked yield genuinely is an asset: `jax_sim.py:1048` decrements `yield_units` when a unit
    harvests it, so it is product that exists and is waiting to be collected. Valuing it means a
    doubled melon yield shows up ~a day after fertilising rather than never, which puts the credit
    ~24 turns out instead of ~700.

    It stops short of valuing *future* yield -- expected units x price x maturity -- which is where the
    judgement lives and where a strategy could be smuggled in. A plant that will produce tomorrow is
    worth nothing here until it does.

    `ANIMAL_TO_PRODUCT` and `CROP_TO_PRODUCT` are the simulator's own tables (`jax_sim.py:169`,
    `tiles.py:61`), so the pairing is not something this file decides.
    """
    t = state.tiles
    px = J.price(state.inventory).astype(jnp.float32)                  # [B, N_PRODUCTS]
    has_animal = t.animal != J.NO_ANIMAL
    crop_product = J.CROP_TO_PRODUCT[jnp.clip(t.crop, 0, J.CROP_TO_PRODUCT.shape[0] - 1)]
    animal_product = J.ANIMAL_TO_PRODUCT[jnp.clip(t.animal, 0, J.ANIMAL_TO_PRODUCT.shape[0] - 1)]
    product = jnp.where(has_animal, animal_product, crop_product)      # [B, P, TILES]

    wide = jnp.broadcast_to(px[:, None, :], product.shape[:-1] + (px.shape[-1],))
    unit_price = jnp.take_along_axis(wide, product, axis=-1)
    return (t.yield_units.astype(jnp.float32) * unit_price * UNPICKED).sum(axis=-1)


def net_worth(state):
    """`[B, P]` -- cash plus livestock plus stock plus unharvested yield.

    Structures are free to build (`jax_sim.py:613`), so they are worth nothing -- which is why the
    chain's head is a plateau rather than a hill. See the module docstring.
    """
    return (state.farm.money.astype(jnp.float32)
            + livestock_value(state.tiles)
            + stock_value(state)
            + standing_yield_value(state))


def net_worth_shaping(before, after, coef=DEFAULT_COEF):
    """`coef * (PHI(net_worth(after)) - PHI(net_worth(before)))`, shaped `[B, P]`.

    `gamma` is 1.0 throughout this project, so the discount in `gamma * PHI(s') - PHI(s)` is the
    identity and is omitted. The terms telescope, so a season's total shaping is
    `PHI(end) - PHI(start)` whatever route was taken -- it cannot pay for a detour.
    """
    return shaping(net_worth(before), net_worth(after), coef=coef)
