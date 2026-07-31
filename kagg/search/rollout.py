"""Playing plans against plans on the batched simulator.

The batch dimension is the population. One call to :func:`play` advances every candidate, every
opponent and every seating of a generation in lockstep, so a 200-plan generation costs one pass of
719 simulator steps rather than 200 episodes.

Everything here is *simulator* measurement. It is used to rank candidates during the search and for
nothing else -- the number that decides whether the search worked comes from `kagg.arena.evaluate`
in the real environment, because a plan that only wins in the simulator has proved nothing.
"""

import numpy as np

from kagg.search import executor as X
from kagg.search.plan import N_CROPS
from kagg.sim.game import Actions, Game
from kagg.sim.market import price
from kagg.sim.town import SHOPS, SHOP_INDEX

SHOP_UNLOCK_INTERVAL = 3


def sample_unlock_schedule(rng):
    """A plausible shop unlock order: one random remaining shop every third day.

    Mirrors `_end_of_day`, which unlocks on days divisible by `townShopUnlockInterval`. The order
    is the only meaningful seed-to-seed variation the simulator has, so it stands in for the
    reference environment's seed.
    """
    order = list(rng.permutation(len(SHOPS)))
    return {SHOP_UNLOCK_INTERVAL * (k + 1): int(shop) for k, shop in enumerate(order)}


def build_view(game, player, day, hour):
    """Read one player's state out of a batched :class:`~kagg.sim.game.Game`."""
    tiles, farm = game.tiles[player], game.farms[player]
    ordering = X.TILE_OF_ORD
    pos = farm.unit_pos[:, : X.MAX_EXEC_UNITS, :]
    return X.View(
        day=day,
        hour=hour,
        kind=tiles.kind[:, ordering],
        crop=tiles.crop[:, ordering],
        planted_day=tiles.planted_day[:, ordering],
        watered=tiles.watered_today[:, ordering],
        yield_units=tiles.yield_units[:, ordering],
        unit_ord=X.ORD_OF_TILE[pos[:, :, 1] * X.BOARD + pos[:, :, 0]].astype(np.int64),
        n_units=farm.n_units,
        money=farm.money,
        seeds=farm.seeds,
        shed=farm.shed[:, :N_CROPS],
        prices=price(game.inventory)[:, :N_CROPS],
        n_land=farm.n_land,
    )


def _write(actions, player, decision):
    actions.unit_op[:, player, : X.MAX_EXEC_UNITS] = decision.unit_op
    actions.unit_crop[:, player, : X.MAX_EXEC_UNITS] = decision.unit_crop
    actions.sell[:, player, :N_CROPS] = decision.sell
    actions.buy_seed[:, player, :] = decision.buy_seed
    actions.hire[:, player] = decision.hire
    actions.buy_land[:, player] = decision.buy_land


def play(seat_plans, unlock_schedule, weed_chance=0.005, rng=None, steps=None):
    """Play a full season. `seat_plans` is a pair of Plans, each already sized to the batch.

    Returns final money as ``[B, 2]``.
    """
    batch = seat_plans[0].size
    game = Game(batch, weed_chance=weed_chance, rng=rng, unlock_schedule=unlock_schedule)
    actions = Actions(batch)
    total = steps if steps is not None else 719

    for step in range(total):
        day, hour = step // 24, step % 24
        for player in (0, 1):
            view = build_view(game, player, day, hour)
            _write(actions, player, X.decide(view, seat_plans[player]))
        if game.step(actions):
            break
    return game.money()


def evaluate(candidates, opponents, schedules, weed_chance=0.005, seed=0):
    """Score every candidate against every opponent, both seatings, on every unlock schedule.

    Returns ``(win_rate[N], mean_delta[N])`` -- win rate is the selection criterion because the
    ladder is Elo and margin does not count; the money delta is carried only to break the many
    ties a 0-1 signal produces over a handful of games.
    """
    n = candidates.size
    m = opponents.size
    wins = np.zeros(n)
    delta = np.zeros(n)
    games = 0

    rng = np.random.default_rng(seed)
    for schedule in schedules:
        for swapped in (False, True):
            # Each candidate meets every opponent: candidate index varies slowest.
            cand = candidates.repeat(m)
            opp = opponents.take(np.tile(np.arange(m), n))
            pair = (opp, cand) if swapped else (cand, opp)
            money = play(pair, schedule, weed_chance=weed_chance, rng=rng)
            mine = money[:, 1] if swapped else money[:, 0]
            theirs = money[:, 0] if swapped else money[:, 1]
            wins += (mine > theirs).reshape(n, m).sum(axis=1)
            delta += (mine - theirs).reshape(n, m).sum(axis=1)
            games += m

    return wins / games, delta / games


def shop_name(index):
    return SHOPS[index]


def shop_index(name):
    return SHOP_INDEX[name]
