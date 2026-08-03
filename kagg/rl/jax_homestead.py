"""A mixed farm: half the crew on crops, half on the herd. The shape the public meta actually runs.

**Why this exists.** `docs/public_meta_2026-08-03.md` measured the gap: the public field banks
$90k-$123k and our best training opponent (`jax_heuristic`, "farm") banks $23,783. The current common
public plan -- `raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta`, and
`beicicc/kaggriculture-c04-target-herd-15` as shipping code -- is **8 cows, 5 sheep, 5 strawberry
plots, 12 hands**. Nothing in our opponent pool runs crops *and* livestock together, so a trainee can
climb the whole pool without ever meeting one.

**Composed, not ported, and that is the point.** `jax_rancher` already runs `TARGET_HANDS = 12` and
`TARGET_ANIMALS = 11` and banks $12,078 -- it is not weak, it simply grows nothing and buys all 295
of its wheat orders from the market. `jax_heuristic` runs the crop half and banks $23,783 with no
animals at all. Both are jitted, tested and already in the rollout. Splitting one crew between them
costs ~100 lines instead of a 1,704-line port, and it is the same "an opponent does not need to be
our best agent" argument `jax_heuristic`'s own docstring makes.

**Two attempts at the crew allocation, both measured, the second worse. Recorded so nobody repeats
them.** Both parents assign jobs with `rank = jnp.arange(MAX_UNITS)` (`jax_heuristic.py:171`), so unit
*i* walks to the *i*-th nearest job, assuming it owns the whole crew. Splitting the crew by index
therefore leaves the nearest K crop jobs unserved.

- **v1, plain index split:** $24,957 against `jax_heuristic`'s $30,292, lost 0/48.
- **v2, roll each arm's units to indices `0..n-1` and trim `n_units`:** **$16,422**, and it began
  losing to `jax_rancher` as well. The reason is that the crew is *dynamic and small* -- `n_units`
  starts at 1 and is rebuilt from scratch every dawn -- so rolling unit 7 to index 0 when only three
  units exist made the crop arm plan for phantom units while all three real ones went to the herd.
  A fixed index split cannot work against a crew that grows.

**v1 is what ships.** A correct fix needs the split to be a function of the *live* crew rather than of
`MAX_UNITS` -- either a rank offset threaded into both parents, or a per-unit priority merge ("take
the herd op if this unit has an animal job within reach, else the crop op"). Neither is a composition
any more, which is the honest conclusion: composing two agents that each assume they own the crew is
not the cheap win it looked like.

**So this is NOT a stronger opponent and must not be sold as one.** `jax_heuristic` banks more. What
it is, is the only member of the pool that farms and ranches at once -- the only one that punishes a
policy for ignoring livestock while still contesting the crop market. That is a reason to include it,
not a reason to prefer it.

**Not a submission.** `CLAUDE.md`: a heuristic agent is a teacher and a sparring partner, never the
final policy. This exists to be *played against*.
"""

import jax
import jax.numpy as jnp

from kagg.rl import jax_heuristic as HEUR
from kagg.rl import jax_rancher as RANCH
from kagg.sim import jax_sim as J

# 12 hands is both parents' target and the field's measured plateau -- `prvsiyan`'s per-day census of
# episode 89517103 reads `hire` at 0.422 per turn, and `romanrozen` prices twelve hands at 376 coins
# for 288 extra actions, about 1.3 coins each against $250 for one in-window melon watering.
#
# The split is the c16 ratio rounded to whole units: 13 animals against 5 crop plots is roughly two
# thirds of the crew on livestock. Deliberately a constant rather than a schedule -- a schedule would
# be reading a plan off a replay, which is what `CLAUDE.md` forbids in a prior and is no more
# defensible in an opponent we intend to measure ourselves against.
HERD_UNITS = 7


def actions(state):
    """A `jax_sim.Actions` for both seats, mixing the two parents' plans across one crew.

    Unit ops are selected by unit index; market orders are merged rather than selected, because the
    two parents never compete for the same head -- the rancher buys wheat and animals, the farmer
    buys seed and sells crops.
    """
    herd = RANCH.actions(state)
    crop = HEUR.actions(state)

    # `[1, 1, U]` against `[B, P, U]` -- the low indices tend the herd, the rest farm.
    idx = jnp.arange(J.MAX_UNITS)[None, None, :]
    on_herd = idx < HERD_UNITS

    def pick(a, b):
        return jnp.where(on_herd, a, b)

    return J.Actions(
        unit_op=pick(herd.unit_op, crop.unit_op),
        unit_crop=pick(herd.unit_crop, crop.unit_crop),
        unit_item=pick(herd.unit_item, crop.unit_item),
        unit_qty=pick(herd.unit_qty, crop.unit_qty),
        # **Market orders are unioned, not selected.** Each parent zeroes the heads it does not use
        # -- the rancher's `buy_seed` is all zeros and the farmer's `buy_animal` is all zeros
        # (`jax_heuristic.py:192`) -- so a sum is a union rather than a collision. `sell` is the one
        # head both touch, and adding is right there too: they sell different products.
        sell=herd.sell + crop.sell,
        buy_seed=herd.buy_seed + crop.buy_seed,
        buy_product=herd.buy_product + crop.buy_product,
        buy_animal=herd.buy_animal,
        # Hire whenever *either* wants to, since the crew now serves both jobs and the Fibonacci fee
        # resets nightly. This is the one place the composition is strictly more aggressive than
        # either parent, and it is the field's behaviour.
        hire=herd.hire | crop.hire,
        buy_land=herd.buy_land | crop.buy_land,
    )