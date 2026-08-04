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
    SEED_COST,
    FarmState,
    buy_land,
    buy_seeds,
    end_of_day,
    hire,
)
from kagg.sim.market import (
    ANIMAL_COST,
    ANIMAL_ITEM,
    BUYABLE,
    I0,
    N_ANIMALS,
    N_PRODUCTS,
    PRICE_FLOOR,
    PRODUCT_INDEX,
    price,
    price_of,
)
from kagg.sim.tiles import (
    COOP,
    CROP_INDEX,
    CROPS,
    EMPTY,
    PASTURE,
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

# `maxMarketOrdersPerTurn`. The reference truncates each player's list to this before pairing them.
MAX_ORDERS = 10

# Order kinds, in the order an agent writes them. `_order_book` compacts a turn's orders into slots
# using exactly this order, because the reference pairs the two players' i-th *orders* rather than
# matching them up by product.
(
    ORDER_NONE, ORDER_SELL, ORDER_BUY_SEED, ORDER_BUY_PRODUCT, ORDER_BUY_ANIMAL,
    ORDER_HIRE, ORDER_BUY_LAND,
) = range(7)


class Actions:
    """One turn's actions for every game and both players.

    - `unit_op` [B, P, MAX_UNITS]  -- op code per unit, from `kagg.sim.ops`
    - `unit_crop` [B, P, MAX_UNITS] -- crop id for PLANT ops, ignored otherwise
    - `sell` [B, P, N_PRODUCTS]   -- units offered for sale
    - `buy_seed` [B, P, N_CROPS]  -- seeds to buy
    - `hire` [B, P]               -- hire one hand this turn
    - `buy_land` [B, P]           -- unlock the next quadrant
    """

    __slots__ = (
        "unit_op", "unit_crop", "unit_item", "unit_qty",
        "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land",
        # Optional explicit market-order list; see `__init__` for why slot order matters.
        "order_op", "order_item", "order_qty",
    )

    def __init__(self, batch, players=N_PLAYERS):
        self.unit_op = np.zeros((batch, players, MAX_UNITS), dtype=np.int64)
        self.unit_crop = np.zeros((batch, players, MAX_UNITS), dtype=np.int64)
        # PICKUP and PLACE both take an item and a count; every other op ignores them.
        self.unit_item = np.zeros((batch, players, MAX_UNITS), dtype=np.int64)
        self.unit_qty = np.zeros((batch, players, MAX_UNITS), dtype=np.int64)
        self.sell = np.zeros((batch, players, N_PRODUCTS), dtype=np.int64)
        self.buy_seed = np.zeros((batch, players, N_CROPS), dtype=np.int64)
        # Only WHEAT and FERTILIZER are buyable; the rest of the column is ignored.
        self.buy_product = np.zeros((batch, players, N_PRODUCTS), dtype=np.int64)
        self.buy_animal = np.zeros((batch, players, N_ANIMALS), dtype=np.int64)
        # **Counts, not flags.** HIRE and BUY_LAND are atomic *per order slot*, not per turn:
        # `reference/kaggriculture.py:538` walks the order slots and fires one hire for each slot
        # holding a HIRE, so `[["HIRE"], ["HIRE"]]` hires twice. `senkin13` opens with exactly that
        # and the recorded observation shows `hires_today: 2`. These were `bool` until 2026-08-04,
        # which made the leaders' own turns inexpressible and any exact replay impossible --
        # positions tracked for 209 turns and then the season ended at $0 against $145,034.
        # Assigning `True` still works: it stores as 1.
        self.hire = np.zeros((batch, players), dtype=np.int64)
        self.buy_land = np.zeros((batch, players), dtype=np.int64)
        # **An optional explicit order list, for when slot order carries money.**
        #
        # The per-product vectors above are a convenience: `_order_book` lays them out in the fixed
        # canonical sequence every agent in this project emits. That is lossless for a turn whose
        # orders are each a distinct `(op, item)`, and `tests/test_split_sell_orders.py` shows even
        # splitting one SELL into pieces settles identically.
        #
        # It is *not* lossless when a turn interleaves orders on the same product. Turn 11 of day 0 on
        # episode 89873723 is `SELL WHEAT 1 / BUY_PRODUCT WHEAT 2 / SELL WHEAT 2`; totals collapse
        # that to `SELL 3 / BUY 2`, and since SELL raises inventory while BUY_PRODUCT quotes at
        # `inventory - 1`, moving both sells ahead of the buy reprices it -- $58 recorded against $33
        # merged. Replaying the winner's tape is dollar-exact for turns 0-10 and breaks there.
        #
        # Left all-zero, `_order_book` behaves exactly as before, so every existing caller and the
        # parity gate are untouched. Set `order_op` for a seat and that seat's list is used verbatim.
        self.order_op = np.zeros((batch, players, MAX_ORDERS), dtype=np.int64)
        self.order_item = np.zeros((batch, players, MAX_ORDERS), dtype=np.int64)
        self.order_qty = np.zeros((batch, players, MAX_ORDERS), dtype=np.int64)


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

                unit_pos = farm.unit_pos[:, u, :]
                carried_u = farm.carried[:, u, :]          # a view, so ops mutate in place
                item = actions.unit_item[:, p, u]
                qty = actions.unit_qty[:, p, u]

                O.water(tiles, unit_pos, active & (op == O.WATER), day)

                harvested = np.zeros((self.batch, N_CROPS), dtype=np.int64)
                harvested = O.harvest(
                    tiles, unit_pos, active & (op == O.HARVEST), day, harvested
                )
                if harvested.any():
                    for c in range(N_CROPS):
                        farm.carried[:, u, CROP_TO_PRODUCT[c]] += harvested[:, c]
                # HARVEST branches on the tile, not the op: the same op takes milk off a cow.
                O.harvest_animals(tiles, unit_pos, active & (op == O.HARVEST), carried_u)

                O.dig(tiles, unit_pos, active & (op == O.DIG))

                # ---- logistics and the animal economy ----------------------------------------
                O.drop(tiles, unit_pos, active & (op == O.DROP), carried_u, farm.shed)
                O.pickup(tiles, unit_pos, active & (op == O.PICKUP), item, qty, carried_u, farm.shed)
                O.place(tiles, unit_pos, active & (op == O.PLACE), item, qty,
                        carried_u, farm.shed, day)
                O.build(tiles, unit_pos, active & (op == O.BUILD_COOP), COOP)
                O.build(tiles, unit_pos, active & (op == O.BUILD_PASTURE), PASTURE)
                O.feed(tiles, unit_pos, active & (op == O.FEED), carried_u)
                O.care(tiles, unit_pos, active & (op == O.CARE))
                O.collect_fertilizer(tiles, unit_pos, active & (op == O.COLLECT_FERT), carried_u)
                O.fertilize(tiles, unit_pos, active & (op == O.FERTILIZE), carried_u, day)

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

    def _order_book(self, actions):
        """Compact this turn's orders into `[B, P, MAX_ORDERS]` op / item / qty arrays.

        `_process_market` walks the two players' order *lists* in lockstep, pairing their i-th
        orders, so the simulator needs the same notion of a slot. Callers still supply the
        convenient per-product arrays; this lays them out in the order an agent writes them --
        sells, then seeds, then products, then animals, then HIRE, then BUY_LAND -- which is the
        order `heuristic`, `contrarian`, `rancher` and `search/agent` all emit, and the order the
        parity harness builds its market list in.

        Anything past the tenth slot is dropped, exactly as `maxMarketOrdersPerTurn` does.
        """
        b, p = self.batch, N_PLAYERS
        cand_op, cand_item, cand_qty = [], [], []

        def add(op, item, qty):
            cand_op.append(np.full((b, p), op, dtype=np.int64))
            cand_item.append(np.full((b, p), item, dtype=np.int64))
            cand_qty.append(qty)

        for i in range(N_PRODUCTS):
            add(ORDER_SELL, i, actions.sell[:, :, i])
        for c in range(N_CROPS):
            add(ORDER_BUY_SEED, c, actions.buy_seed[:, :, c])
        for i in range(N_PRODUCTS):
            add(ORDER_BUY_PRODUCT, i, actions.buy_product[:, :, i])
        for a in range(N_ANIMALS):
            add(ORDER_BUY_ANIMAL, a, actions.buy_animal[:, :, a])
        # One slot per hire, because the reference spends a slot per atomic order. A count of `n`
        # therefore emits `n` candidates of quantity 1 each; `present = c_qty > 0` drops the rest, and
        # the `slot < MAX_ORDERS` clamp below applies `maxMarketOrdersPerTurn` exactly as it would to
        # any other order. Capping the loop at MAX_ORDERS is not a further restriction: an eleventh
        # hire could not reach a slot anyway.
        n_hire = np.asarray(actions.hire, dtype=np.int64)
        n_land = np.asarray(actions.buy_land, dtype=np.int64)
        for k in range(MAX_ORDERS):
            add(ORDER_HIRE, 0, (n_hire > k).astype(np.int64))
        for k in range(MAX_ORDERS):
            add(ORDER_BUY_LAND, 0, (n_land > k).astype(np.int64))

        c_op = np.stack(cand_op, axis=2)
        c_item = np.stack(cand_item, axis=2)
        c_qty = np.stack(cand_qty, axis=2).astype(np.int64)

        present = c_qty > 0
        slot = np.cumsum(present, axis=2) - 1
        keep = present & (slot < MAX_ORDERS)

        op = np.zeros((b, p, MAX_ORDERS), dtype=np.int64)
        item = np.zeros((b, p, MAX_ORDERS), dtype=np.int64)
        qty = np.zeros((b, p, MAX_ORDERS), dtype=np.int64)
        gi, pi, ki = np.nonzero(keep)
        si = slot[gi, pi, ki]
        op[gi, pi, si] = c_op[gi, pi, ki]
        item[gi, pi, si] = c_item[gi, pi, ki]
        qty[gi, pi, si] = c_qty[gi, pi, ki]

        # **An explicit order list overrides the canonical layout, per seat.**
        #
        # Compacted the same way rather than copied straight through: `_parse_order` rejects a
        # quantity <= 0 while the reference has already spent that slot positionally
        # (`reference/kaggriculture.py:534` truncates before parsing), so a zero entry must vanish
        # instead of padding. That is the same `present`/`cumsum` rule applied above, which is why a
        # caller cannot use this to smuggle in more than `MAX_ORDERS` orders.
        explicit = np.asarray(getattr(actions, "order_op", None))
        if explicit.ndim == 3 and explicit.any():
            e_qty = np.asarray(actions.order_qty, dtype=np.int64)
            e_item = np.asarray(actions.order_item, dtype=np.int64)
            e_present = (explicit != ORDER_NONE) & (
                (e_qty > 0) | np.isin(explicit, (ORDER_HIRE, ORDER_BUY_LAND)))
            e_slot = np.cumsum(e_present, axis=2) - 1
            e_keep = e_present & (e_slot < MAX_ORDERS)
            # Only seats that actually supplied a list; the others keep their canonical book.
            uses = explicit.any(axis=2)
            op = np.where(uses[:, :, None], 0, op)
            item = np.where(uses[:, :, None], 0, item)
            qty = np.where(uses[:, :, None], 0, qty)
            gi, pi, ki = np.nonzero(e_keep)
            si = e_slot[gi, pi, ki]
            op[gi, pi, si] = explicit[gi, pi, ki]
            item[gi, pi, si] = e_item[gi, pi, ki]
            # HIRE and BUY_LAND carry no quantity; the atomic branch keys off the op alone, and a
            # zero here would read as "not present" on the next pass.
            qty[gi, pi, si] = np.maximum(e_qty[gi, pi, ki], 1)
        return op, item, qty

    def _quote(self, op, item):
        """[B] price each player would pay or receive for the next unit of its current order.

        Every seat is quoted from the *same* pre-commit inventory: `_process_market` fills both
        `quoted` entries before calling `_commit_unit` on either, which is why a contested unit
        pays both seats alike, and why a same-slot buy is priced against the pre-sale book.
        """
        safe_product = np.clip(item, 0, N_PRODUCTS - 1)
        sell_grid = price(self.inventory)                       # [B, N_PRODUCTS]
        # BUY_PRODUCT quotes at the post-buy inventory, so a buy/sell round trip nets zero.
        buy_grid = price(self.inventory - 1)
        rows = np.arange(self.batch)

        out = np.zeros(self.batch, dtype=np.float64)
        out = np.where(op == ORDER_SELL, sell_grid[rows, safe_product], out)
        out = np.where(op == ORDER_BUY_PRODUCT, buy_grid[rows, safe_product], out)
        out = np.where(op == ORDER_BUY_SEED, SEED_COST[np.clip(item, 0, N_CROPS - 1)], out)
        out = np.where(op == ORDER_BUY_ANIMAL, ANIMAL_COST[np.clip(item, 0, N_ANIMALS - 1)], out)
        return out

    def _commit(self, p, op, item, unit_price, live):
        """Commit one unit of each live order for seat `p`. Returns [B] bool: did it go through?

        Mirrors `_commit_unit`, including its failure semantics -- a sale with an empty shed or a
        purchase that cannot be afforded returns False, and the caller then abandons the whole
        remaining order rather than retrying it.
        """
        farm = self.farms[p]
        rows = np.arange(self.batch)
        safe_product = np.clip(item, 0, N_PRODUCTS - 1)

        selling = live & (op == ORDER_SELL) & (farm.shed[rows, safe_product] > 0)
        buying = live & (op == ORDER_BUY_PRODUCT) & (farm.money >= unit_price)
        seeding = live & (op == ORDER_BUY_SEED) & (farm.money >= unit_price)
        animaling = live & (op == ORDER_BUY_ANIMAL) & (farm.money >= unit_price)

        if selling.any():
            farm.money = np.where(selling, farm.money + unit_price, farm.money)
            np.add.at(farm.shed, (rows[selling], safe_product[selling]), -1)
            # A unit clearing at the floor pays out but does not deepen the glut.
            deepens = selling & (unit_price > PRICE_FLOOR)
            np.add.at(self.inventory, (rows[deepens], safe_product[deepens]), 1)

        if buying.any():
            farm.money = np.where(buying, farm.money - unit_price, farm.money)
            np.add.at(farm.shed, (rows[buying], safe_product[buying]), 1)
            np.add.at(self.inventory, (rows[buying], safe_product[buying]), -1)

        if seeding.any():
            farm.money = np.where(seeding, farm.money - unit_price, farm.money)
            np.add.at(farm.seeds, (rows[seeding], np.clip(item, 0, N_CROPS - 1)[seeding]), 1)

        if animaling.any():
            farm.money = np.where(animaling, farm.money - unit_price, farm.money)
            item_id = ANIMAL_ITEM[np.clip(item, 0, N_ANIMALS - 1)]
            np.add.at(farm.shed, (rows[animaling], item_id[animaling]), 1)

        return selling | buying | seeding | animaling

    def _process_market(self, actions):
        """Settle the turn's orders slot by slot, both players in lockstep.

        This is a port of `_process_market`'s shape, not just its arithmetic. It walks the players'
        order lists **by slot**, because that is what the reference pairs: the two players' i-th
        orders trade against each other and against the same inventory. Settling all sells and then
        all buys -- which this did until `BUY_PRODUCT` existed to expose it -- prices a same-slot
        buy against a book that the sells have already lifted.

        Within a slot, HIRE and BUY_LAND resolve once in seat order, then SELL and the BUY_* orders
        settle one unit at a time until neither side can trade.
        """
        op, item, qty = self._order_book(actions)
        remaining = qty.copy()

        for slot in range(MAX_ORDERS):
            sop = op[:, :, slot]
            if not (sop != ORDER_NONE).any():
                continue
            sitem = item[:, :, slot]
            srem = remaining[:, :, slot].copy()

            # Atomic orders resolve once, in seat order, and then the slot is spent.
            for p in range(N_PLAYERS):
                hiring = sop[:, p] == ORDER_HIRE
                if hiring.any():
                    hire(self.farms[p], hiring)
                landing = sop[:, p] == ORDER_BUY_LAND
                if landing.any():
                    buy_land(self.farms[p], self.tiles[p], landing)
            atomic = (sop == ORDER_HIRE) | (sop == ORDER_BUY_LAND)
            srem = np.where(atomic, 0, srem)

            # A malformed sub-op is dropped rather than retried: BUY_PRODUCT only accepts the two
            # products the reference lists, and everything else in the slot is already valid.
            bad = (sop == ORDER_BUY_PRODUCT) & ~BUYABLE[np.clip(sitem, 0, N_PRODUCTS - 1)]
            srem = np.where(bad, 0, srem)

            while True:
                live = (srem > 0) & (sop != ORDER_NONE)
                if not live.any():
                    break
                # Both seats quoted before either commits.
                quoted = [self._quote(sop[:, p], sitem[:, p]) for p in range(N_PLAYERS)]
                committed = np.zeros(self.batch, dtype=bool)
                for p in range(N_PLAYERS):
                    ok = self._commit(p, sop[:, p], sitem[:, p], quoted[p], live[:, p])
                    srem[:, p] -= ok.astype(np.int64)
                    # A failed commit abandons the rest of that order, as the reference does.
                    srem[:, p] = np.where(live[:, p] & ~ok, 0, srem[:, p])
                    committed |= ok
                if not committed.any():
                    break

            remaining[:, :, slot] = srem

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
                # `_end_of_day` refreshes plants and then animals, in that order, per farm.
                O.daily_refresh_animals(t, self.day)
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
