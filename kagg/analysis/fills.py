"""The one correct way to count what actually traded. Use this instead of inferring.

**Read this before writing another market measurement.** This project has now got the same answer
wrong three separate ways, each time by using a plausible proxy for a quantity the environment
already knows exactly:

1. **Summing `o[2]` from the action stream.** The agent re-posts each quota on all 24 turns of a
   day, so one intended sale is counted up to 24 times. Recorded in `feedback_offers_are_not_fills`.
2. **`held_at_dusk - shed_at_dawn` as the discard.** Hour 23's SELL and BUY_PRODUCT settle in the
   same `env.step` as the shed rollover, so a sale counted as a loss -- 15x overstated
   (`docs/fable_the_discard_problem_2026-08-09.md`).
3. **"holdings fell and money rose, therefore a sale."** FEED consumes wheat, so every unit fed on a
   turn where anything else sold was booked as a wheat sale; and a HARVEST raises holdings, so wheat
   picked on a turn where anything was bought was booked as a wheat purchase. This produced a
   fictitious "854 bought / 816 sold wheat round trip" that does not exist.

All three are the same mistake. The fix is not a better proxy.

`kaggriculture._commit_unit` is where a single unit actually changes hands: it is the only function
that moves `private["shed"]` and `farm["money"]` together for a market order, it is called once per
unit, and it returns `False` on the attempts that fail. Wrapping it yields the ground truth --
per player, per product, per unit, at the price that unit actually fetched.

    with record_fills() as fills:
        env.run([a, b])
    fills.sold(player=0, product="WHEAT")     # units, revenue

**Player attribution is the part that is easy to get wrong, so read this before changing it.**
The first version bound `id(farm) -> seat` once from `env.state[0].observation["farms"]` and recorded
zero fills for the whole episode. `kaggle_environments` rebuilds `env.state` between steps, so that
map pointed at dead copies within one turn.

`_process_market` re-reads the live list every call (`farms = obs0.farms`, line 534 of the reference)
and commits with `farms[player_id]`, so the map is rebuilt inside a wrapper on `_process_market` --
once per turn, from the same object the commit will use. `_commit_unit` then resolves against a map
that is never more than one call old. A fill whose farm is not in the map is dropped rather than
guessed at, and `unattributed` counts those so a silent zero cannot masquerade as "nothing traded".
"""

import collections
import contextlib


class Fills:
    """Every unit that actually traded, keyed by player."""

    def __init__(self):
        #: (player, op, item) -> [prices], one entry per UNIT
        self._rows = collections.defaultdict(list)
        self._farm_ids = {}
        #: fills whose farm was not in the current map -- must stay 0, see the module docstring
        self.unattributed = 0

    def bind_farms(self, farms):
        """Rebuild `id(farm dict) -> seat` from the list `_process_market` is about to commit against.

        Called once per turn rather than once per episode: the observation objects do not survive a
        step, so a map built at episode start resolves nothing.
        """
        self._farm_ids = {id(f): i for i, f in enumerate(farms)}

    def _seat(self, farm):
        return self._farm_ids.get(id(farm))

    def record(self, op, item, price, farm):
        seat = self._seat(farm)
        if seat is None:
            self.unattributed += 1
            return
        self._rows[(seat, op, item)].append(price)

    def _agg(self, player, op, product=None):
        units = 0
        value = 0.0
        for (p, o, item), prices in self._rows.items():
            if p != player or o != op:
                continue
            if product is not None and item != product:
                continue
            units += len(prices)
            value += sum(prices)
        return units, value

    def units(self, player, op, product=None):
        """Units of `op` that actually committed. `_commit_unit` handles SELL, BUY_PRODUCT,
        BUY_SEED and BUY_ANIMAL, and `_do_hire` / `_do_buy_land` are wrapped alongside it, so all
        SIX market ops are exact here -- there is no reason for any caller to infer one of them
        from a shed delta, which is mistake (2) and (3) in this docstring, nor to count HIRE and
        BUY_LAND off the action stream, which is mistake (1).
        """
        return self._agg(player, op, product)[0]

    def spent(self, player, op, product=None):
        """What `op` actually cost, in dollars. For HIRE that is the fibonacci ladder the farm
        really climbed, which no count of emitted orders can give."""
        return self._agg(player, op, product)[1]

    def sold(self, player, product=None):
        """(units, revenue) actually sold. Never an offer."""
        return self._agg(player, "SELL", product)

    def bought(self, player, product=None):
        """(units, cost) actually bought as BUY_PRODUCT. Excludes seed and animals."""
        return self._agg(player, "BUY_PRODUCT", product)

    def products(self):
        return sorted({item for (_p, _o, item) in self._rows})

    def ops(self):
        return sorted({op for (_p, op, _i) in self._rows})


@contextlib.contextmanager
def record_fills(env=None):
    """Wrap the env's per-unit commit for the duration of the block.

    Only successful commits are recorded: `_commit_unit` returns False when the shed is empty, the
    bank is short or the shed is full, and those are attempts rather than trades. That distinction
    is the whole point -- an offer that fills nothing must contribute nothing.

    Four patches, because one is the ground truth, one is the only place a seat is known, and two
    more ops never reach `_commit_unit` at all. `env` is accepted and ignored; it is no longer
    needed, and the parameter stays so existing call sites keep working.

    **HIRE and BUY_LAND are fills too.** `_process_market` handles them as "atomic orders" before
    the per-unit loop, so they go through `_do_hire` and `_do_buy_land` instead, and BOTH return
    silently when the bank is short. An emitted HIRE is therefore an offer exactly like a SELL, and
    counting them off the action stream is the mistake this module exists to end -- it was simply
    the one place the module did not reach. Neither returns a status, so success is read off the
    state each one moves: a hand appended, a quadrant unlocked. The price is the money the farm
    actually parted with, which for HIRE is the fibonacci ladder and is not knowable from the order.
    """
    import kaggle_environments.envs.kaggriculture.kaggriculture as kg

    fills = Fills()
    original_commit = kg._commit_unit
    original_market = kg._process_market
    original_hire = kg._do_hire
    original_land = kg._do_buy_land

    def commit(op, item, price, farm, private, market, *a, **kw):
        ok = original_commit(op, item, price, farm, private, market, *a, **kw)
        if ok:
            fills.record(op, item, price, farm)
        return ok

    def do_hire(farm, private, board_size, *a, **kw):
        before_hands, before_money = len(farm["hands"]), farm["money"]
        out = original_hire(farm, private, board_size, *a, **kw)
        if len(farm["hands"]) > before_hands:
            fills.record("HIRE", "HAND", before_money - farm["money"], farm)
        return out

    def do_buy_land(farm, board_size, *a, **kw):
        before_quads, before_money = len(farm["unlocked_quadrants"]), farm["money"]
        out = original_land(farm, board_size, *a, **kw)
        if len(farm["unlocked_quadrants"]) > before_quads:
            fills.record("BUY_LAND", "QUADRANT", before_money - farm["money"], farm)
        return out

    def process_market(state, env_):
        # The live list, re-read exactly as `_process_market` itself re-reads it.
        fills.bind_farms(state[0].observation.farms)
        return original_market(state, env_)

    kg._commit_unit = commit
    kg._do_hire = do_hire
    kg._do_buy_land = do_buy_land
    kg._process_market = process_market
    try:
        yield fills
    finally:
        kg._commit_unit = original_commit
        kg._do_hire = original_hire
        kg._do_buy_land = original_land
        kg._process_market = original_market
