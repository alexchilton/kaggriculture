"""The batched game loop: B two-player games advancing in lockstep.

Ties together `market`, `tiles`, `ops`, `town` and `farm`. One `step()` advances every game in the
batch by one turn, in the reference environment's order:

1. unit actions for both players
2. market orders, settled one unit at a time with the players alternating
3. town consumption
4. plant decay
5. end of day, on the last turn of each day

That ordering is not cosmetic. Selling happens *before* the town drains, so the price a player
receives is set by the pre-drain inventory; swapping them shifts every sale price in the game.

Actions are supplied as arrays rather than dicts, one entry per game per player, so a policy can
drive the whole batch with a single forward pass. See `Actions` for the layout.
"""

import numpy as np

from kagg.sim import ops as O
from kagg.sim.farm import (
    MAX_UNITS,
    N_CROPS,
    FarmState,
    buy_land,
    buy_seeds,
    end_of_day,
    hire,
)
from kagg.sim.market import I0, N_PRODUCTS, PRODUCT_INDEX, price, price_of
from kagg.sim.tiles import (
    CROP_INDEX,
    CROPS,
    EMPTY,
    WEED,
    LOCKED,
    TILES,
    TURNS_PER_DAY,
    TileState,
    daily_refresh_plants,
    decay_plants,
)
from kagg.sim.town import N_SHOPS, drain_at

N_PLAYERS = 2
SEASON_DAYS = 30
EPISODE_STEPS = 720
LAST_STEP = EPISODE_STEPS - 2   # the last step the interpreter actually processes

CROP_TO_PRODUCT = np.array([PRODUCT_INDEX[c] for c in CROPS], dtype=np.int64)


class Actions:
    """One turn's actions for every game and both players.

    - `unit_op` [B, P, MAX_UNITS]  -- op code per unit, from `kagg.sim.ops`
    - `unit_crop` [B, P, MAX_UNITS] -- crop id for PLANT ops, ignored otherwise
    - `sell` [B, P, N_PRODUCTS]   -- units offered for sale
    - `buy_seed` [B, P, N_CROPS]  -- seeds to buy
    - `hire` [B, P]               -- hire one hand this turn
    - `buy_land` [B, P]           -- unlock the next quadrant
    """

    __slots__ = ("unit_op", "unit_crop", "sell", "buy_seed", "hire", "buy_land")

    def __init__(self, batch, players=N_PLAYERS):
        self.unit_op = np.zeros((batch, players, MAX_UNITS), dtype=np.int64)
        self.unit_crop = np.zeros((batch, players, MAX_UNITS), dtype=np.int64)
        self.sell = np.zeros((batch, players, N_PRODUCTS), dtype=np.int64)
        self.buy_seed = np.zeros((batch, players, N_CROPS), dtype=np.int64)
        self.hire = np.zeros((batch, players), dtype=bool)
        self.buy_land = np.zeros((batch, players), dtype=bool)


class Game:
    """A batch of B two-player games."""

    def __init__(self, batch, starting_money=3000.0, weed_chance=0.005, rng=None,
                 unlock_schedule=None):
        """`unlock_schedule` maps day -> shop index, per game or shared across the batch.

        Which shop unlocks on a given day cannot be derived offline: `_spawn_weeds` consumes one
        Python RNG draw per empty tile *before* `rng.choice` picks the shop, so the order depends
        on both players' board occupancy. Reproducing that draw-for-draw would cost millions of
        Python-level RNG calls per batch. The schedule is therefore supplied by the caller --
        observed from a real episode for parity testing, or sampled for training.
        """
        self.batch = batch
        self.step_index = 0
        self.weed_chance = weed_chance
        self.rng = rng if rng is not None else np.random.default_rng()
        self.unlock_schedule = unlock_schedule or {}
        self.tiles = [TileState(batch) for _ in range(N_PLAYERS)]
        self.farms = [FarmState(batch, starting_money) for _ in range(N_PLAYERS)]
        self.inventory = np.tile(I0.astype(np.int64), (batch, 1))
        self.unlocked_shops = np.zeros((batch, N_SHOPS), dtype=bool)

        # Only the NW quadrant starts unlocked.
        locked = np.zeros(TILES, dtype=bool)
        for y in range(10):
            for x in range(10):
                if not (x < 5 and y < 5):
                    locked[y * 10 + x] = True
        for t in self.tiles:
            t.kind[:, locked] = LOCKED

    @property
    def day(self):
        return self.step_index // TURNS_PER_DAY

    def money(self):
        """[B, P] current bank for each player -- the environment's reward."""
        return np.stack([f.money for f in self.farms], axis=1)

    # ---- phases ---------------------------------------------------------------------------

    def _plant_blocked(self, actions, p):
        """[B, N_CROPS] bool: crops whose PLANT requests must ALL be dropped this turn.

        The reference validates PLANT atomically per crop across every one of a player's units:
        if the total requests for a crop exceed the seeds held, it drops **all** of them, not the
        excess. Spending greedily unit by unit -- which is what this simulator did until it was
        caught -- plants some where the reference plants none.

        The parity harness could not have found this: it drove exactly one unit per player, and
        with one unit the two rules agree. Fixed alongside a harness that drives a full crew.
        """
        farm = self.farms[p]
        live = farm.unit_mask()
        demand = np.zeros((self.batch, N_CROPS), dtype=np.int64)
        for c in range(N_CROPS):
            asking = live & (actions.unit_op[:, p, :] == O.PLANT_OP) & (actions.unit_crop[:, p, :] == c)
            demand[:, c] = asking.sum(axis=1)
        return demand > farm.seeds

    def _apply_unit_actions(self, actions):
        day = self.day
        for p in range(N_PLAYERS):
            tiles, farm = self.tiles[p], self.farms[p]
            live = farm.unit_mask()
            blocked = self._plant_blocked(actions, p)

            for u in range(MAX_UNITS):
                active = live[:, u]
                if not active.any():
                    continue
                op = actions.unit_op[:, p, u]
                pos = farm.unit_pos[:, u, :]

                moving = active & (op >= O.NORTH) & (op <= O.WEST)
                if moving.any():
                    moved = O.move(tiles, pos, np.where(moving, op, O.NOOP))
                    farm.unit_pos[:, u, :] = np.where(moving[:, None], moved, pos)

                O.water(tiles, farm.unit_pos[:, u, :], active & (op == O.WATER), day)

                harvested = np.zeros((self.batch, N_CROPS), dtype=np.int64)
                harvested = O.harvest(
                    tiles, farm.unit_pos[:, u, :], active & (op == O.HARVEST), day, harvested
                )
                if harvested.any():
                    for c in range(N_CROPS):
                        farm.carried[:, u, CROP_TO_PRODUCT[c]] += harvested[:, c]

                O.dig(tiles, farm.unit_pos[:, u, :], active & (op == O.DIG))

                planting = active & (op == O.PLANT_OP)
                if planting.any():
                    # PLANT is validated atomically per crop: if a player's requests for a crop
                    # exceed the seeds held, the reference drops *all* of them. Enforced here by
                    # spending a seed per plant and refusing once the store is empty.
                    for c in range(N_CROPS):
                        want = (planting & (actions.unit_crop[:, p, u] == c)
                                & (farm.seeds[:, c] > 0) & ~blocked[:, c])
                        if not want.any():
                            continue
                        planted = O.plant(tiles, farm.unit_pos[:, u, :], want, c, day)
                        farm.seeds[:, c] -= planted.astype(np.int64)

    def _process_market(self, actions):
        """Settle sells one unit at a time with both players alternating, then buys.

        Mirrors `_process_market`: both players are quoted against the same pre-commit inventory
        and commit in seat order, so seat 0 gets the better price on each contested unit.
        """
        remaining = actions.sell.copy()

        for product in range(N_PRODUCTS):
            if not remaining[:, :, product].any():
                continue
            for _ in range(int(remaining[:, :, product].max())):
                if not remaining[:, :, product].any():
                    break
                for p in range(N_PLAYERS):
                    farm = self.farms[p]
                    want = remaining[:, p, product] > 0
                    have = farm.shed[:, product] > 0
                    doing = want & have
                    if not doing.any():
                        continue
                    unit_price = price_of(product, self.inventory[:, product])
                    farm.money = np.where(doing, farm.money + unit_price, farm.money)
                    farm.shed[:, product] -= doing.astype(np.int64)
                    remaining[:, p, product] -= doing.astype(np.int64)
                    # A unit clearing at the floor pays out but does not deepen the glut.
                    self.inventory[:, product] = np.where(
                        doing & (unit_price > 1), self.inventory[:, product] + 1,
                        self.inventory[:, product],
                    )

        for p in range(N_PLAYERS):
            for c in range(N_CROPS):
                want = actions.buy_seed[:, p, c]
                if want.any():
                    buy_seeds(self.farms[p], c, want)
            if actions.hire[:, p].any():
                hire(self.farms[p], actions.hire[:, p])
            if actions.buy_land[:, p].any():
                buy_land(self.farms[p], self.tiles[p], actions.buy_land[:, p])

    # ---- the loop -------------------------------------------------------------------------

    def step(self, actions):
        """Advance every game by one turn. Returns True once the episode is over."""
        self._apply_unit_actions(actions)
        self._process_market(actions)

        self._apply_unlocks()
        self.inventory -= drain_at(self.step_index, self.unlocked_shops)
        for t in self.tiles:
            decay_plants(t, self.step_index)

        if (self.step_index + 1) % TURNS_PER_DAY == 0:
            for t in self.tiles:
                daily_refresh_plants(t, self.day)
                self._spawn_weeds(t)
            for f in self.farms:
                end_of_day(f)

        self.step_index += 1
        return self.step_index > LAST_STEP

    def _apply_unlocks(self):
        """Open any shops whose unlock day has arrived. Shops consume from the day they appear."""
        if not self.unlock_schedule:
            return
        day = self.day
        for unlock_day, shop in self.unlock_schedule.items():
            if unlock_day <= day:
                self.unlocked_shops[:, shop] = True

    def _spawn_weeds(self, tiles):
        """Weeds on empty unlocked tiles, at the configured rate.

        **Statistically faithful, not sequence-identical.** The reference draws from a per-day
        Python `random.Random` shared by both farms, consuming one draw per empty tile -- so an
        exact port costs up to 6000 Python-level RNG calls per game, which at B=512 is over three
        million per batch and would dominate the entire step loop, destroying the ~1000x speedup
        this simulator exists for.

        The parity harness therefore runs with `weed_chance=0` on both sides, which makes the
        comparison exact for every deterministic mechanic. Weed *behaviour* is verified separately
        by a statistical test on the spawn rate. This is the one deliberate divergence in the
        simulator, and it is confined to a 0.5%-per-tile-per-day nuisance event.
        """
        if not self.weed_chance:
            return
        empty = tiles.kind == EMPTY
        spawn = empty & (self.rng.random(tiles.kind.shape) < self.weed_chance)
        tiles.kind = np.where(spawn, WEED, tiles.kind)

    def prices(self):
        return price(self.inventory)
