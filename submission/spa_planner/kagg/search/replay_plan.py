"""Read a winning seat's plan -- chains bound to squares -- out of a replay, as a genome.

`plan.leaders_genome()` states the gap this closes:

    "The *spatial* layout is ours, not theirs -- the counts are measured but which tile holds what is
     not extracted yet, so pastures go nearest the shed and the crops fill outward in serpentine
     order. CEM will move them."

`crop_of` is a per-tile gene, so which square holds which chain is exactly what the genome encodes
and exactly what was being guessed. The episode observations carry the whole `tiles` grid at every
step, so nothing needs reconstructing from the action tape.

It also corrects three counts that `docs/episode_teardown_2026-08-03.md` took from three episodes.
Mining all 312 seats (`scripts/mine_build_orders.py`) and reading one $132,245 seat square by square
(`scripts/extract_winner_plan.py`) gives:

    pastures      28, not 14
    land parcels  1 (day 10), not 2 (days 7 and 10)
    dump day      ~20, not 26 -- and day 20 is exactly where TOWN_CENTER_DEMAND_SCHEDULE steps to 4x

**This is a starting distribution, not an answer.** `plan.probs_around` keeps mass on every
alternative so CEM can leave it; `tests/test_replay_plan.py` pins that no gene is pinned.
"""

import collections
import statistics
import json
from dataclasses import dataclass, field

import numpy as np

from . import plan as P

TURNS_PER_DAY = 24
# `crop_of` is the reference's `tiles[y][x]` flattened row-major, which is how `executor.py` indexes
# it. Pinned by `tests/test_replay_plan.py` via the round-trip rather than assumed here.
def tile_index(x, y):
    return y * P.BOARD + x


@dataclass
class Layout:
    """One seat's committed square roles plus its season parameters, all measured."""

    money: float = 0.0
    pasture: tuple = ()
    coop: tuple = ()
    crops: dict = field(default_factory=dict)          # (x, y) -> crop name
    animal_counts: dict = field(default_factory=dict)  # species -> live count at the end
    land_days: tuple = ()
    crew_by_day: tuple = ()
    animals_by_day: tuple = ()
    wheat_total: int = 0
    dump_day: int = 20
    # Per-product sell behaviour, measured off the seat's own orders rather than assumed. Keyed by
    # product name: the median quantity per selling turn, and the lowest price-over-base it ever
    # accepted. `genome_from_layout` used a single `put("sell_qty", 3)` for all five crops and left the
    # four animal-product genes at 0, so the encoded winner dumped WHEAT -- its feed input -- at 0.3x
    # base while never selling MILK, WOOL, EGG or FERTILIZER at all.
    sell_median: dict = field(default_factory=dict)     # product -> median qty per selling turn
    sell_floor: dict = field(default_factory=dict)      # product -> min accepted price / base

    @property
    def n_pasture(self):
        return len(self.pasture)

    @property
    def n_coop(self):
        return len(self.coop)

    @property
    def crop_counts(self):
        return dict(collections.Counter(self.crops.values()))


def _role(tile):
    if tile is None or isinstance(tile, str):
        return None, None
    if "animal" in tile:
        return "ANIMAL", tile["animal"]
    kind = tile.get("kind")
    if kind == "PLANT":
        return "PLANT", tile.get("crop")
    if kind in ("PASTURE", "COOP"):
        return kind, None
    return None, None


def layout_from_replay(path, seat=1, hold_share=0.70):
    """Extract the square roles and season parameters for one seat.

    A square's role is the *first* non-empty thing it held, because that is the commitment the plan
    made; an animal placed on a pasture later does not change which chain owns the square. Species is
    read from the live animals at the end instead, since `herd` is a per-species target.

    `dump_day` is the earliest day from which `hold_share` of all sell volume still lies ahead --
    i.e. when the seat stops trickling and starts emptying the shed.
    """
    ep = json.loads(open(path).read())
    steps = ep["steps"]
    money = float(ep["rewards"][seat])

    role_of, crops = {}, {}
    land_days, crew, live = [], {}, {}
    wheat = 0
    sells = collections.Counter()
    animal_counts = {}
    # Per-product sell behaviour, for `Layout.sell_median` / `Layout.sell_floor`. The floor is the
    # lowest price-over-base the seat ever accepted, which is the quantity `plan.floor_frac` encodes.
    per_product = collections.defaultdict(list)
    price_floor = {}

    for t, step in enumerate(steps):
        day = t // TURNS_PER_DAY
        obs = step[seat].get("observation") or step[0].get("observation")
        farms = (obs or {}).get("farms")
        if farms and seat < len(farms):
            farm = farms[seat]
            crew[day] = 1 + len(farm.get("hands") or [])
            species = collections.Counter()
            n_live = 0
            for y, row in enumerate(farm["tiles"]):
                for x, tile in enumerate(row):
                    role, subject = _role(tile)
                    if role is None:
                        continue
                    if role == "ANIMAL":
                        species[subject] += 1
                        n_live += 1
                    key = (x, y)
                    if key not in role_of:
                        # An animal implies the pasture/coop that must already be under it.
                        role_of[key] = "PASTURE" if role == "ANIMAL" else role
                        if role == "PLANT":
                            crops[key] = subject
                    elif role == "PLANT" and key not in crops:
                        crops[key] = subject
            live[day] = n_live
            if species:
                animal_counts = dict(species)
        action = step[seat].get("action")
        if isinstance(action, dict):
            for order in action.get("market") or []:
                if not order:
                    continue
                if order[0] in ("BUY_LAND", "BUID_LAND"):
                    land_days.append(day)
                elif order[0] == "BUY_PRODUCT" and len(order) >= 3 and order[1] == "WHEAT":
                    wheat += int(order[2])
                elif order[0] == "SELL" and len(order) >= 3:
                    # **WHEAT is excluded from the dump-day estimate.** It is bought as feed and
                    # resold as arbitrage, so it trades all season: 15,247 units for this seat with
                    # only 47.9% of them late, against 98-99% for MILK, WOOL and FERTILIZER. Folding
                    # it in dragged the estimated onset from day 20 to day 22 and buried the signal.
                    # `dump_day` governs holding produce for the demand window, which is what those
                    # three do.
                    if order[1] != "WHEAT":
                        sells[day] += int(order[2])
                    name = order[1]
                    if name in P.BASE_PRICE_OF:
                        per_product[name].append(int(order[2]))
                        quote = ((obs or {}).get("market") or {}).get("prices") or {}
                        px = quote.get(name)
                        if px:
                            ratio = float(px) / P.BASE_PRICE_OF[name]
                            price_floor[name] = min(price_floor.get(name, ratio), ratio)

    total = sum(sells.values()) or 1
    dump = 20
    for d in range(P.SEASON_DAYS):
        if sum(n for k, n in sells.items() if k >= d) / total < hold_share:
            dump = max(d - 1, 0)
            break

    return Layout(
        money=money,
        pasture=tuple(sorted(k for k, v in role_of.items() if v == "PASTURE")),
        coop=tuple(sorted(k for k, v in role_of.items() if v == "COOP")),
        crops={k: v for k, v in crops.items() if role_of.get(k) == "PLANT" and v},
        animal_counts=animal_counts,
        land_days=tuple(sorted(set(land_days))),
        crew_by_day=tuple(crew.get(d, 0) for d in range(P.SEASON_DAYS)),
        animals_by_day=tuple(live.get(d, 0) for d in range(P.SEASON_DAYS)),
        wheat_total=wheat,
        dump_day=dump,
        sell_median={k: statistics.median(v) for k, v in per_product.items() if v},
        sell_floor=dict(price_floor),
    )


def _nearest(table, value):
    return int(np.argmin(np.abs(np.asarray(table, dtype=np.float64) - float(value))))


def genome_from_layout(layout):
    """Encode a `Layout` as a categorical genome, following `plan.leaders_genome`'s conventions."""
    g = np.zeros(P.N_GENES, dtype=np.int64)

    def put(name, value):
        a, b = P.gene_slice(name)
        g[a:b] = value

    # ---- the squares: this is the part that was previously guessed --------
    use = np.zeros(P.TILES, dtype=np.int64)            # 0 == fallow
    for (x, y) in layout.pasture:
        use[tile_index(x, y)] = P.CROP_GENE_PASTURE
    for (x, y) in layout.coop:
        use[tile_index(x, y)] = P.CROP_GENE_COOP
    for (x, y), name in layout.crops.items():
        use[tile_index(x, y)] = P.CROP_NAMES.index(name) + 1
    a, b = P.gene_slice("crop_of")
    g[a:b] = use

    # ---- season parameters ------------------------------------------------
    put("phase", 0)
    put("stop_plant", _nearest(P.STOP_PLANT_DAYS, 14))
    put("harvest_par", 2)                              # cut at max_yield_day
    put("sell_every", _nearest(P.SELL_EVERY, 2))
    put("seed_reserve", 1)                             # keep $200 for feed

    # ---- what to sell, and at what price, per product ---------------------
    #
    # **This was one blanket constant and it inverted the strategy.** `put("floor_frac", 1)` and
    # `put("sell_qty", 3)` set every crop to "10 a tick at 0.3x base" and left the four animal-product
    # genes at level 0, i.e. quantity zero. So the encoded winner dumped WHEAT -- the feed its whole
    # season runs on -- at any price above 0.3x, and never sold MILK, WOOL, EGG or FERTILIZER at all.
    # Measured on the $147,178 seat's own board, day 0 came out at net **+$2,922** against the seat's
    # own **-$4,442**: we liquidated where they invested, and FEED fired 0 times against their 4
    # because the mask needs carried wheat we had already sold.
    #
    # Both now come from the tape (`data/logs/winner_sell_profile.log`), the median quantity per
    # selling turn and the lowest price-over-base ever accepted:
    #
    #     WHEAT      1131 units / 135 turns  median 4  min 0.96x   <- and 967 units *bought*
    #     STRAWBERRY  653 /  85  median 5  min 1.24x
    #     MILK        717 /  89  median 8  min 1.19x
    #     MELON       235 /  37  median 6  min 0.58x
    #     WOOL        404 /  53  median 4  min 0.01x
    #     FERTILIZER  445 /  93  median 3  min 0.13x
    #
    # The wheat floor is the load-bearing number: it holds feed off the market unless the price is at
    # base, which is what makes wheat an input rather than a product. A seat that trades 1131 out and
    # 967 in is market-making, not farming wheat.
    for name, qty_key, floor_key, base in (
            ("sell_qty", "sell_qty", "floor_frac", P.CROP_NAMES),
            ("sell_qty_animal", "sell_qty_animal", "floor_frac_animal", P.ANIMAL_PRODUCT_NAMES),
    ):
        a, b = P.gene_slice(qty_key)
        levels = np.array([_nearest(P.SELL_QTYS, layout.sell_median.get(p, 0)) for p in base])
        # Block-major: `decode` reshapes to (N_BLOCKS, n_products), so tile the per-product row.
        g[a:b] = np.tile(levels, (b - a) // len(base))
        a, b = P.gene_slice(floor_key)
        g[a:b] = [_nearest(P.FLOOR_FRACS, layout.sell_floor.get(p, 0.0)) for p in base]
    put("dump_day", _nearest(P.DUMP_DAYS, layout.dump_day))
    put("fert_policy", P.FERT_APPLY_THEN_SELL)         # 243 collects per top seat, ~26 fertilises

    # Crew is re-hired every dawn, so headcount is a genuinely daily decision.
    a, b = P.gene_slice("hires")
    g[a:b] = [_nearest(P.HIRE_LEVELS, n) for n in layout.crew_by_day]

    # Animals from day 0 if the seat had any on day 0.
    put("stock_day", _nearest(P.STOCK_DAYS, 0 if layout.animals_by_day[0] else 4))
    # Wheat held per animal per day. `feed_wheat` is a stock target, not a season total.
    peak = max(max(layout.animals_by_day), 1)
    put("feed_wheat", _nearest(P.FEED_WHEAT, layout.wheat_total / peak / P.SEASON_DAYS))

    # Herd targets per species, from the live census. Clipped to the ladder, and never below the
    # pens available -- a herd target under the pen count leaves pens standing empty.
    a, _ = P.gene_slice("herd")
    pens = max(layout.n_pasture + layout.n_coop, 1)
    counts = layout.animal_counts or {}
    for i, name in enumerate(P.ANIMAL_NAMES):
        want = counts.get(name, 0)
        g[a + i] = _nearest(P.HERD_LEVELS, min(want, pens))

    # Land: one gene per parcel, in LAND_ORDER sequence, NEVER for parcels never bought.
    a, b = P.gene_slice("land_day")
    g[a:b] = len(P.LAND_DAYS) - 1                      # NEVER
    for i, day in enumerate(layout.land_days[:3]):
        g[a + i] = _nearest(P.LAND_DAYS, day)
    return g


def genome_from_replay(path, seat=1):
    return genome_from_layout(layout_from_replay(path, seat=seat))


def teacher_forced_pairs(path, seat=0):
    """Yield `(turn, observation_before, their_action)` for every decided turn.

    **The observation in a replay is recorded AFTER that turn's action was applied**, which is the same
    mutation CLAUDE.md warns about for `env.steps`: "the interpreter mutates the very dicts the recorder
    holds, so seed counts read back post-planting and the hand list read back post-hiring". Measured on
    episode 89873723 seat 0:

        step 1: obs hands=2  hires_today=2  seedsWHEAT=6
                action [HIRE], [HIRE], [BUY_SEED, WHEAT, 6]
        step 2: obs hands=3  hires_today=3  seedsWHEAT=11
                action [HIRE], [BUY_SEED, WHEAT, 5]

    The counts in the observation are the post-action totals every time. So pairing `steps[t].observation`
    with `steps[t].action` asks a plan to buy six wheat seeds on a board that already holds them, and to
    hire two hands that have already been hired -- unsatisfiable whatever the genes say. That pairing is
    what produced "0 of 720 turns identical, first divergence turn 0" and it was a property of the
    harness, not of the representation.

    The correct pre-action state for turn `t` is the observation recorded at `t - 1`. Turn 0 uses its own
    observation, which is the initial state: its action is `PASS` with an empty market, so post-action
    and pre-action coincide there.
    """
    steps = json.loads(open(path).read())["steps"]
    previous = None
    for t, step in enumerate(steps):
        cell = step[seat]
        obs, action = cell.get("observation"), cell.get("action")
        before = previous if t else obs
        previous = obs if obs and "farms" in obs else previous
        if not isinstance(action, dict) or not before or "farms" not in before:
            continue
        before = dict(before)
        before.setdefault("player", seat)
        yield t, before, action
