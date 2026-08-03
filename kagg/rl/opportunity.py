"""Find the turns at which a payoff becomes available, so P2b can resume just before one.

**The problem this is for.** With `--horizon 32` and `--gae-lambda 0.95` the effective GAE reach is
about 20 turns against a 719-turn season, so a direct path from the terminal reward back to an action
exists only for roughly the last 32 turns; for the other ~96% the critic is the sole carrier of
credit (`docs/opus_review_2026-08-03.md`). Meanwhile the policy ends every season on $0
(`docs/bankrupt_every_game_2026-08-03.md`), and the reward is piecewise constant over exactly the
range it occupies (`docs/the_reward_is_a_step_function_2026-08-03.md`).

Both of those are the same shape of problem: **the payoff for acting is out of reach of the action.**
Grading the opponent on money does not fix it, because spending precedes earning -- any reward that
is a function of final bank punishes the spend before it pays the earn, so a valley sits between "do
nothing" and "farm well" wherever the zero is put. Shortening the distance from action to payoff is
the one intervention that does not have that shape.

**Ripening, not harvesting.** `docs/fable_review_day0_launch_2026-08-03.md` picked the *opportunity*
over the *event*: HARVEST runs 0.18-0.24% of ops, so waiting for one to fire and succeed means resume
points do not exist until the problem has half-solved itself. A ripening needs only an earlier
PLANT+WATER, and PLANT runs 1-3%.

**Rising edges, not levels.** A ripe crop stays ripe until something harvests it, so recording the
level would emit one resume state per turn per crop and drown the buffer.

Nothing here is wired into the trainer. These are pure functions over `jax_sim.Tiles`, so they can be
called on a rollout, on a replay, or on hand-built tiles in a test -- which is how they are tested,
because a real 32-turn window ripens nothing at current planting rates and every count would read
zero.
"""

import jax
import jax.numpy as jnp

from kagg.sim import jax_sim as J

# One turn of slack past the ripening, plus room for the walk. `resume_turns`' caller chooses;
# this is only the value the docs argue for -- inside GAE's ~20-turn reach, far outside 1.
DEFAULT_LOOKBACK = 8


def crop_ready(tiles, day):
    """`[B, P, TILES]` -- a planted tile that can be harvested right now.

    Mirrors `ripe_plant` in `jax_masks.py:80` exactly, minus the per-unit position test: a tile is
    ready if it is PLANT, still has yield on it, and has aged past its crop's `FIRST_YIELD_DAY`.
    The `>=` boundary is the mask's, and being off by one here is being off by a game-day.

    `crop` is clipped before indexing because an EMPTY tile carries crop 0 as filler, and a gather
    with an out-of-range index lowers to a silent clamp rather than an error under jit.
    """
    crop_safe = jnp.clip(tiles.crop, 0, J.N_CROPS - 1)
    age = day[:, None, None] - tiles.planted_day
    return ((tiles.kind == J.PLANT)
            & (tiles.yield_units > 0)
            & (age >= J.FIRST_YIELD_DAY[crop_safe]))


def animal_ready(tiles):
    """`[B, P, TILES]` -- an animal with product waiting to be collected.

    The occupancy test is on `animal`, not on `kind`: an empty COOP is a structure, and
    `yield_units` on an empty pen is stale rather than meaningful.
    """
    return (tiles.animal != J.NO_ANIMAL) & (tiles.yield_units > 0)


def feed_ready(tiles):
    """`[B, P, TILES]` -- an animal that has not been fed today.

    FEED and CARE are the two ops `CLAUDE.md` measures as the strongest money predictors (+0.452,
    +0.441 over 312 real seats) and the op census reads FEED at 0.01%, so this is the trigger for
    the half of the game the policy has never touched.
    """
    return (tiles.animal != J.NO_ANIMAL) & (tiles.fed_today == 0)


def ready(tiles, day):
    """`[B, P, TILES]` -- any of the three, as one mask.

    Reporting only. **Do not take a rising edge of this** -- see `newly_ready`.
    """
    return crop_ready(tiles, day) | animal_ready(tiles) | feed_ready(tiles)


def newly_ready(before, before_day, after, after_day):
    """`[B, P, TILES]` -- tiles that became ready between two consecutive turns.

    The rising edge only. Ready-to-not-ready is a harvest, which is a payoff already collected, and
    steady-ready is the same crop reported again.

    **Each kind gets its own edge, and the edges are OR'd -- not the levels.** A test caught this:
    `feed_ready` is true from the moment an animal is placed, since a new animal has `fed_today == 0`,
    so a combined level is already high and the animal's later *collect* flip can never fire against
    it. Three separate transitions is also the truer statement: an animal becoming feedable and the
    same animal producing are different opportunities that happen to share a tile.
    """
    crop = crop_ready(after, after_day) & ~crop_ready(before, before_day)
    coll = animal_ready(after) & ~animal_ready(before)
    feed = feed_ready(after) & ~feed_ready(before)
    return crop | coll | feed


def any_opportunity(before, before_day, after, after_day):
    """`[B, P]` -- did *any* new opportunity appear, per game and seat.

    Reduced over tiles because a resume point is a position, not a tile: three crops ripening on one
    turn is one state worth resuming from, not three.
    """
    return newly_ready(before, before_day, after, after_day).any(axis=-1)


def resume_turns(fires, lookback=DEFAULT_LOOKBACK):
    """`[N, 2]` of `(turn, game)` -- where to restart, given a `[T, B]` mask of firing turns.

    **Before the opportunity, not on it.** Resuming on the ripe turn hands the policy a free harvest
    and teaches nothing about reaching one. Resuming `lookback` turns earlier leaves a short chain
    whose payoff is inside GAE's reach -- which is the entire point of P2b.

    Clamped at 0 rather than wrapped, so a crop ripening at turn 2 with a lookback of 8 resumes at
    the start of the window instead of at the end of it. Returned as concrete indices rather than a
    mask because the caller stores states by index, and because an empty result must be an empty
    array rather than an all-False mask a caller could iterate over forever.
    """
    idx = jnp.argwhere(jnp.asarray(fires))
    turn = jnp.maximum(idx[:, 0] - lookback, 0)
    return jnp.stack([turn, idx[:, 1]], axis=-1)


def gather_states(stacked, idx):
    """Pull the states at `[N, 2]` `(turn, game)` indices out of a `[T, B, ...]` scan output.

    `jax.lax.scan` stacks whatever it emits with turn on axis 0 and game on axis 1, so a resume point
    is a pair and every leaf has to be indexed with the *same* pair. Indexing one leaf by (turn,
    game) and another by (game, turn) yields a state of the right shape assembled from two different
    games, which no shape check would catch -- hence the two-leaf assertion in the test.

    An empty `idx` gives leaves with a zero-length leading axis rather than an error, because in a
    32-turn window at today's planting rates most updates find nothing.
    """
    turn, game = idx[:, 0], idx[:, 1]
    return jax.tree_util.tree_map(lambda a: a[turn, game], stacked)
