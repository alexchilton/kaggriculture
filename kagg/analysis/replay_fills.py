"""What a DOWNLOADED game really did: fills, real plants, real herd -- never offers.

`kagg/analysis/fills.py` is the right answer for a game we simulate, because it wraps the env's own
`_commit_unit`. It cannot help with a ladder replay: those carry `seed: None`, so the game cannot be
re-played and there is no commit to wrap. Every tool that reads a downloaded game has therefore
reached for the action stream instead, and the action stream is a list of REQUESTS.

That has now cost this project time four times (`feedback_offers_are_not_fills`, and the three
variants listed in `fills.py`'s own docstring). The last one is worth stating plainly because it is
what this module was written for: `scripts/why_we_lost.py` printed a column headed
`crops planted (offers)` whose values were BUY_SEED order quantities. Against tile transitions in
the same four recordings:

    92564858   real  WHEAT 138  STRAWBERRY 34  MELON 18   printed  MELON 251, WHEAT 148, STRAW 92
    92566708   real  WHEAT 139  STRAWBERRY 36  MELON 19   printed  STRAW 460, MELON 386, WHEAT 378

The agent re-posts a standing order every turn until it fills, so `386 melon` is nineteen melons
asked for twenty times.

## What is exact here, and why

**Real plants** (`real_plants`). `_apply_unit_action`'s PLANT branch writes `_new_plant` onto a tile
that was `None`. The plant is therefore standing on the board in the next recorded observation, with
`planted_day` on it. Counting transitions is exact and needs nothing else.

**Seed purchases** (`seed_fills`). `private["seeds"]` has exactly two writers -- `BUY_SEED` adds one,
`PLANT` removes one -- and both seats' `private` is recorded. So `bought = delta + planted`, exact.

**Hires and land** (`hires`, `land`). `_do_hire` and `_do_buy_land` silently return when the bank is
short, so an emitted HIRE is an offer like any other. `farm["hires_today"]` and
`farm["unlocked_quadrants"]` are recorded, so both are read off state rather than off the request.

**Herd** (`animals_alive`). A count of the board.

## What is a lower bound, and where the bound comes from

Sales and product purchases have no single recorded field, so `trade_fills` reconciles two
independent ledgers:

1. **The seat's own shed.** `_commit_unit` is the only market path that touches `private["shed"]`.
   `DROP`, `PICKUP` and `PLACE` are the only unit ops that touch the same field, and the end-of-day
   rollover empties every inventory into it. Where none of those reached a given item, that item's
   shed delta IS that seat's fill -- exact, and it still works when the price is on the floor.
   Readability is per ITEM, not per turn: `PICKUP` and `PLACE` name the one thing they move, so a
   `PICKUP WHEAT` says nothing about the cow bought on the same turn.
2. **The market inventory.** `inv(t) - inv(t-1) + town_drain(t) = sold - bought` summed over both
   seats, with `town_drain` exact from the shop list and `step % townShopSellInterval` /
   `step % townCenterSellInterval`. This covers the turns the shed cannot, and has one blind spot
   the shed does not: `_commit_unit` does not add to supply when a unit sells at $1, so a product
   sitting on `PRICE_FLOOR` moves invisibly through this ledger.

Where one seat's shed is clean, the other seat's volume follows from the ledger, so both are exact.
Where neither is clean and both had an order for that product, the TOTAL is still exact but the
split is not, and those units are reported in `shared` rather than divided by a guess. Units the
floor hid land in `unresolved`. **`sold`/`bought` are lower bounds; `sold + shared + unresolved` is
the accounting.** Callers must print `shared` and `unresolved` beside the split, never fold them in.
"""

import collections
import json
import pathlib

from reference.kaggriculture import (PRICE_FLOOR, PRODUCTS, SHOPS,
                                     TOWN_CENTER_PRODUCTS)

#: Unit ops that move product across the same `private["shed"]` boundary `_commit_unit` settles
#: against, so a shed delta on a turn where one of these fired cannot be read as a fill.
SHED_TAINTING_OPS = ("DROP", "PICKUP", "PLACE")


def load(path):
    """A replay dict from a path, or the dict straight through if already loaded."""
    if isinstance(path, dict):
        return path
    return json.loads(pathlib.Path(path).read_text())


def seat_of(replay, team):
    """The seat `team` sat in, or 0 if the name is not in this game.

    Seat 0 is not "us". Of the tapes in `scripts/breakdown.py` one has the leader seated second,
    and anything that reads seat 0 by hand gets the opponent.
    """
    names = (replay.get("info") or {}).get("TeamNames") or []
    return names.index(team) if team in names else 0


def _cfg(replay, key, default):
    value = (replay.get("configuration") or {}).get(key)
    return default if value is None else value


def _obs(replay, t, seat=0):
    step = replay["steps"][t]
    return (step[seat] or {}).get("observation") or {} if seat < len(step) else {}


def _action(replay, t, seat):
    step = replay["steps"][t]
    return ((step[seat] or {}).get("action") or {}) if seat < len(step) else {}


def _tiles(replay, t, seat):
    farms = _obs(replay, t).get("farms") or []
    return farms[seat]["tiles"] if seat < len(farms) else []


# ----------------------------------------------------------------------------- offers


def offered(replay, seat):
    """What the seat ASKED FOR, per market op: `{op: Counter(item -> units offered)}`.

    Kept, and deliberately named, because an offer is a real thing an agent did and the cadence of
    re-offering is itself a finding. It is only wrong when it is printed as a quantity. Any caller
    putting one of these on a page must put the word `offered` in the heading.
    """
    out = collections.defaultdict(collections.Counter)
    for t in range(len(replay["steps"])):
        for order in (_action(replay, t, seat).get("market") or []):
            if not order:
                continue
            item = order[1] if len(order) > 1 else ""
            try:
                units = int(order[2]) if len(order) > 2 else 1
            except (TypeError, ValueError):
                units = 1
            out[order[0]][item] += units
    return dict(out)


# ----------------------------------------------------------------------------- board counts


def real_plants(replay, seat):
    """Tiles that BECAME a plant, per crop. A count of the board, not of an order.

    Counted as a TRANSITION per square, not as a snapshot: `HARVEST` sets a finished non-ongoing
    crop's tile back to `None` and the same square is replanted later in the season, so a count of
    what is standing at the close reports a fraction. On the four games this module was written
    for it reports about a fifth.

    The `planted_day` half of the key only discriminates a harvest and a replant inside a SINGLE
    turn, which needs two units on one square in one turn and cannot be produced by a replant on a
    later day (the tile reads `None` in between and the transition is already caught). No recording
    here has exercised it and no test covers it; it is one term in a tuple and is kept because the
    alternative is a silent undercount in the one case nothing would flag.
    """
    out = collections.Counter()
    previous = None
    for t in range(len(replay["steps"])):
        current = {}
        for y, row in enumerate(_tiles(replay, t, seat)):
            for x, tile in enumerate(row):
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    current[(x, y)] = (tile.get("crop"), tile.get("planted_day"))
        if previous is not None:
            for square, ident in current.items():
                if previous.get(square) != ident:
                    out[ident[0]] += 1
        previous = current
    return out


def animals_alive(replay, seat, when=-1):
    """Head count standing on the board, per species. `when` is a step index."""
    out = collections.Counter()
    for row in _tiles(replay, when % len(replay["steps"]), seat):
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal"):
                out[tile["animal"]] += 1
    return out


def weeds_by_origin(replay, seat):
    """`(from_crop, from_empty, cleared)`. A tile that went CROP -> WEED is a missed watering and
    an EMPTY -> WEED is a spawn; they are different problems and only one is bad luck."""
    origin = collections.Counter()
    cleared = 0
    previous = None
    for t in range(len(replay["steps"])):
        current = {}
        for y, row in enumerate(_tiles(replay, t, seat)):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict):
                    current[(x, y)] = "EMPTY"
                elif tile.get("kind") == "WEED":
                    current[(x, y)] = "WEED"
                elif tile.get("crop"):
                    current[(x, y)] = "CROP"
                else:
                    current[(x, y)] = "OTHER"
        if previous is not None:
            for square, kind in current.items():
                if kind == "WEED" and previous.get(square) != "WEED":
                    origin[previous.get(square)] += 1
                elif previous.get(square) == "WEED" and kind != "WEED":
                    cleared += 1
        previous = current
    return origin.get("CROP", 0), origin.get("EMPTY", 0), cleared


# ----------------------------------------------------------------------------- closed ledgers


def seed_fills(replay, seat):
    """`BUY_SEED` units that actually committed, per crop. Exact.

    `private["seeds"]` is a closed ledger: `BUY_SEED` adds one unit (`_commit_unit`) and `PLANT`
    removes one (`_apply_unit_action`); nothing else reads or writes it, and seeds never pass
    through the shed. So `bought = (seeds_end - seeds_start) + planted`, and `planted` is a count
    of the board.
    """
    steps = replay["steps"]
    first = ((steps[0][seat] or {}).get("observation") or {}).get("private") or {}
    last = ((steps[-1][seat] or {}).get("observation") or {}).get("private") or {}
    out = collections.Counter()
    for crop, planted in real_plants(replay, seat).items():
        out[crop] += planted
    for crop in set((first.get("seeds") or {})) | set((last.get("seeds") or {})):
        out[crop] += ((last.get("seeds") or {}).get(crop, 0)
                      - (first.get("seeds") or {}).get(crop, 0))
    return collections.Counter({k: v for k, v in out.items() if v})


def hires(replay, seat):
    """Hands that were actually hired. `_do_hire` returns silently when the bank is short, so the
    emitted HIRE is an offer; `farm["hires_today"]` is the state it moved and is recorded."""
    total = 0
    previous = 0
    for t in range(len(replay["steps"])):
        farms = _obs(replay, t).get("farms") or []
        now = int((farms[seat].get("hires_today") or 0) if seat < len(farms) else 0)
        if now > previous:                       # resets to 0 at the day rollover
            total += now - previous
        previous = now
    return total


def land(replay, seat):
    """Parcels actually bought. `_do_buy_land` is refused for want of a dollar exactly as often as
    a schedule is optimistic, so the emitted BUY_LAND says nothing."""
    farms = _obs(replay, len(replay["steps"]) - 1).get("farms") or []
    if seat >= len(farms):
        return 0
    return max(0, len(farms[seat].get("unlocked_quadrants") or ["NW"]) - 1)


# ----------------------------------------------------------------------------- the town


def town_drain(step, shops, shop_interval=4, center_interval=24):
    """Units the town removes from the market on `step`. Exact -- `_town_consume` is arithmetic.

    A shop instance takes one of each product it sells, doubled when it sells only one; the town
    centre takes one of everything but fertilizer. `shops` may list the same shop more than once:
    instances are drawn with replacement and each consumes independently.
    """
    out = collections.Counter()
    if shop_interval and step % shop_interval == 0:
        for name in shops:
            products = SHOPS.get(name) or []
            multiplier = 2 if len(products) == 1 else 1
            for product in products:
                out[product] += multiplier
    if center_interval and step % center_interval == 0:
        for product in TOWN_CENTER_PRODUCTS:
            out[product] += 1
    return out


def shop_instances(replay):
    """`Counter(shop name -> instances)` from the FINAL observation, i.e. the season's full draw.

    Read off the recording rather than derived from the seed. The draw looks seed-pure -- one
    `rng.choice` per unlock off `random.Random((seed * 1_000_003) ^ day)` -- but `_end_of_day` runs
    `_spawn_weeds` on the same generator first, once per empty tile per player, so the position in
    the stream depends on how much of the board each side had built on. Deriving it from the seed
    would be a guess dressed as arithmetic.
    """
    town = _obs(replay, len(replay["steps"]) - 1).get("town") or {}
    return collections.Counter(town.get("unlocked_shops") or [])


def shop_demand(shops, steps, shop_interval=4, center_interval=24):
    """Units per product the town drains over `steps` turns. The real measure of demand -- a shop
    NAME is not a quantity, and two instances of one shop drain twice as hard as one."""
    out = collections.Counter()
    for step in range(steps):
        out.update(town_drain(step, shops, shop_interval, center_interval))
    return out


def carriers(shops, product):
    """How many unlocked shop INSTANCES sell `product`. The conditioning variable for any question
    of the form "does this crop pay", which has opposite answers at 1 instance and at 5."""
    return sum(1 for name in shops if product in (SHOPS.get(name) or []))


# ----------------------------------------------------------------------------- the market


class TradeFills:
    """Units that changed hands, per seat, with the ambiguity kept beside them.

    `sold[seat]` and `bought[seat]` are LOWER BOUNDS. `shared` holds units that certainly moved but
    whose owner two independent ledgers could not agree on; `unresolved` holds units the market
    ledger could not see at all because the product was at `PRICE_FLOOR` on a turn where the shed
    was also unreadable. A caller printing the split must print these two beside it.
    """

    def __init__(self):
        self.sold = [collections.Counter(), collections.Counter()]
        self.bought = [collections.Counter(), collections.Counter()]
        #: seat -> day -> product -> units, so a closing-week table does not have to fall back on
        #: order counts to say what moved on a given day
        self.sold_by_day = [collections.defaultdict(collections.Counter),
                            collections.defaultdict(collections.Counter)]
        self.bought_by_day = [collections.defaultdict(collections.Counter),
                              collections.defaultdict(collections.Counter)]
        #: `BUY_ANIMAL` lands the beast in the shed like any other purchase, but COW and SHEEP are
        #: not in `PRODUCTS` so the market-inventory ledger never sees them; only the shed does.
        self.animals_bought = [collections.Counter(), collections.Counter()]
        self.shared_sold = collections.Counter()
        self.unresolved_sold = collections.Counter()
        #: products that touched $1 at some point, where the market ledger is blind
        self.floored = set()
        self.hired = [0, 0]
        self.land = [0, 0]
        #: (turns where this seat's shed was readable, turns played)
        self.shed_clean = [0, 0]
        self.turns = 0

    def coverage(self, seat):
        return self.shed_clean[seat] / self.turns if self.turns else 0.0

    def as_rows(self, seat):
        """`[(product, sold, bought, shared, unresolved)]`, products with any movement only."""
        products = (set(self.sold[seat]) | set(self.bought[seat])
                    | set(self.shared_sold) | set(self.unresolved_sold))
        return sorted((p, self.sold[seat][p], self.bought[seat][p],
                       self.shared_sold[p], self.unresolved_sold[p]) for p in products)


def _shed(replay, t, seat):
    private = ((replay["steps"][t][seat] or {}).get("observation") or {}).get("private") or {}
    return private.get("shed") or {}


def _shed_readable_items(replay, t, seat, turns_per_day):
    """Which items' shed levels are readable across the step starting at `t`, as a predicate.

    Per ITEM rather than per turn, because the three tainting ops are not equally destructive.
    `PICKUP` and `PLACE` name the one item they move, so they cost that item and nothing else.
    `DROP` dumps the acting unit's WHOLE inventory and the action does not say what was in it, so
    it costs every item. `_end_of_day` does the same to every unit, so the last turn of a day is
    unreadable outright. Blanket-tainting a turn on a single `PICKUP WHEAT` was throwing away
    every cow purchase that happened to share a turn with one.
    """
    if (t + 1) % turns_per_day == 0:          # `_end_of_day` empties every inventory into the shed
        return lambda _item: False
    action = _action(replay, t, seat)
    units = [action.get("farmer")] + list(action.get("hands") or [])
    tainted = set()
    for unit in units:
        if not unit:
            continue
        if unit[0] == "DROP":
            return lambda _item: False
        if unit[0] in ("PICKUP", "PLACE") and len(unit) > 1:
            tainted.add(unit[1])
    return lambda item: item not in tainted


def trade_fills(replay, team=None):
    """Reconcile the shed and the market inventory into per-seat SELL / BUY_PRODUCT fills.

    See the module docstring for why neither ledger alone is enough and what the two blind spots
    are. `team` is accepted for symmetry with the other readers here and is unused: both seats are
    always computed, because the opponent's volume is half of every market question.
    """
    replay = load(replay)
    steps = replay["steps"]
    turns_per_day = int(_cfg(replay, "turnsPerDay", 24))
    shop_interval = int(_cfg(replay, "townShopSellInterval", 4))
    center_interval = int(_cfg(replay, "townCenterSellInterval", 24))

    out = TradeFills()
    out.turns = max(0, len(steps) - 1)
    for seat in (0, 1):
        out.hired[seat] = hires(replay, seat)
        out.land[seat] = land(replay, seat)

    for t in range(1, len(steps)):
        # The interpreter that produced `steps[t]` ran on step `t - 1`: it applied the actions
        # recorded at `steps[t - 1]`, then the market, then `_town_consume(step=t - 1)`, then --
        # last of all -- `_end_of_day`, which is where a shop unlocks. So the drain used the shop
        # list as it stood at `steps[t - 1]`, not the one recorded at `steps[t]`.
        before, after = _obs(replay, t - 1), _obs(replay, t)
        market_before = (before.get("market") or {}).get("inventory") or {}
        market_after = (after.get("market") or {}).get("inventory") or {}
        prices_before = (before.get("market") or {}).get("prices") or {}
        prices_after = (after.get("market") or {}).get("prices") or {}
        shops = (before.get("town") or {}).get("unlocked_shops") or []
        drain = town_drain(t - 1, shops, shop_interval, center_interval)

        readable = [_shed_readable_items(replay, t - 1, seat, turns_per_day) for seat in (0, 1)]
        for seat in (0, 1):
            out.shed_clean[seat] += 1 if readable[seat]("") else 0
        shed_before = [_shed(replay, t - 1, seat) for seat in (0, 1)]
        shed_after = [_shed(replay, t, seat) for seat in (0, 1)]

        wants = [collections.defaultdict(set), collections.defaultdict(set)]
        for seat in (0, 1):
            for order in (_action(replay, t - 1, seat).get("market") or []):
                if order and order[0] in ("SELL", "BUY_PRODUCT") and len(order) > 1:
                    wants[seat][order[1]].add(order[0])

        # Animals never enter `market["inventory"]`, so the shed is the only witness. On a turn
        # nothing else moved that seat's shed, a rise in COW is a cow that was paid for.
        for seat in (0, 1):
            for animal in ("COW", "SHEEP", "CHICKEN", "GOOSE", "PIG"):
                if not readable[seat](animal):
                    continue
                gained = shed_after[seat].get(animal, 0) - shed_before[seat].get(animal, 0)
                if gained > 0:
                    out.animals_bought[seat][animal] += gained

        for product in PRODUCTS:
            at_floor = (prices_before.get(product, 99) <= PRICE_FLOOR
                        or prices_after.get(product, 99) <= PRICE_FLOOR)
            if at_floor:
                out.floored.add(product)
            # Net units the market absorbed: positive means more was sold into it than bought out.
            moved = (market_after.get(product, 0) - market_before.get(product, 0)
                     + drain.get(product, 0))
            active = [s for s in (0, 1) if wants[s].get(product)]
            if not active and not moved:
                continue

            # A readable shed gives that seat's own net exactly, floor price or not -- but only
            # when the seat asked in one direction, since a SELL and a BUY_PRODUCT of the same
            # product on the same turn net out inside one delta.
            net = [None, None]
            for seat in (0, 1):
                if not readable[seat](product) or len(wants[seat].get(product) or ()) > 1:
                    continue
                net[seat] = (shed_before[seat].get(product, 0)
                             - shed_after[seat].get(product, 0))   # sold minus bought

            known = [s for s in (0, 1) if net[s] is not None]
            if len(known) == 2:
                pass                                    # both exact, nothing to infer
            elif len(known) == 1 and not at_floor:
                # The other seat is the remainder of a ledger that balances.
                other = 1 - known[0]
                net[other] = moved - net[known[0]]
            elif len(active) == 1 and not at_floor:
                net[active[0]] = moved
                net[1 - active[0]] = 0
            elif len(known) == 1:
                pass                                    # floored: trust only what was read
            else:
                if moved:
                    out.shared_sold[product] += abs(moved)
                continue

            day = (t - 1) // turns_per_day
            for seat in (0, 1):
                if net[seat] is None:
                    continue
                if net[seat] > 0:
                    out.sold[seat][product] += net[seat]
                    out.sold_by_day[seat][day][product] += net[seat]
                elif net[seat] < 0:
                    out.bought[seat][product] += -net[seat]
                    out.bought_by_day[seat][day][product] += -net[seat]
            if len(known) == 1 and at_floor:
                # What the ledger saw and the one readable shed did not claim is real volume of
                # unknown ownership -- but at the floor the ledger itself is short, so this is the
                # part that is simply not recoverable from the recording.
                rest = moved - (net[known[0]] or 0)
                if rest:
                    out.unresolved_sold[product] += abs(rest)

    return out
