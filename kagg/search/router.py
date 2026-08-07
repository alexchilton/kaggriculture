"""Layer 3 as the optimisation problem it actually is, solved as one thing instead of five patches.

Named properly, the daily problem is a **Team Orienteering Problem on a grid**: a fixed depot (the
four shed-access cells), `k` vehicles (the farmer and its hands), a hard per-vehicle budget of
`TURNS_PER_DAY - 1` turns, mandatory nodes (FEED -- two missed days and the animal is gone outright,
`kaggriculture.py:786`), optional prize-bearing nodes (WATER, HARVEST, CARE, FERTILIZE), and nodes
whose service requires an item drawn at the depot first. Across the season, with water every second
day and feed every day, it is a Periodic VRP. Choosing *which* tiles to work is a separate, static
p-median problem, solved once per land unlock rather than per turn.

This matters because it says what the previous five attempts were missing. Every one of them keyed
the choice on a **priority rank** -- `(rank, distance)`, then `(distance, rank)`, then a rank table
reordered by hand -- and the standard TOP heuristic is neither. It is

    insert the node maximising  prize / marginal insertion cost

so a rank table is the numerator of a fraction that was never written down. That is why reweighting
it always made things worse: `(rank, d)` sent twelve hands across the board for the highest-priority
task anywhere at ~7 move turns per work turn; `(d, rank)` banked $809 because the nearest task is
never the important one. Both are degenerate limits of the same missing ratio.

It also says ES and RL are the wrong tools here, and not for want of ambition: the objective is
deterministic, exact and costs microseconds; the instance is ~40 nodes and ≤12 vehicles; Manhattan
distance on a grid admits no metric pathologies. Learning an approximation of something computable
exactly is strictly worse. Same conclusion this project already reached at the schedule layer.

Three things the reference gives us that change the shape of the problem, all read off the source
rather than assumed:

- **PICKUP has no capacity limit.** `n = min(n, available)` then `_inv_add(inv, item, n)`
  (`kaggriculture.py:340`). One turn draws the whole day's feed, so a unit servicing fourteen pens
  needs **one** depot stop, not fourteen. `schedule_agent` drew one wheat at a time.
- **A tile is one stop with several ops.** An animal tile wants FEED, CARE, COLLECT_FERTILIZER and
  HARVEST -- four turns, no movement between them. So the routing nodes are *tiles*, and a tile's
  service time is however many ops it wants. This is why pens on the shed cells are nearly free.
- **A one-shot crop's yield comes only from WATER inside its window**, and `FERTILIZE` is read at
  WATER time (`bonus = 2 if tile["fertilized_until_day"] >= day else 1`), so within a visit
  FERTILIZE must be emitted *before* WATER. An ongoing crop's production needs no water at all --
  water only resets `consecutive_unwatered` and enables the fertilizer bonus -- which is the derived
  reason "water every tile every day" measured at **-$18,569**.

## The prize table is derived, not tuned

Every prize below is a marginal dollar figure computed from the reference's own mechanics, which is
what makes the ratio meaningful. The interesting ones:

    HARVEST          yield_units x base price                                exact
    WATER  one-shot  base price, doubled if fertilized, 0 at max_yield       exact: one water = one unit
    WATER  survival  the tile's whole remaining value                        consecutive_unwatered >= 1
    WATER  ongoing   0 unless fertilized into a production day               water does not produce
    CARE             base price of the product                               +1 unit next production
    FEED   hungry    animal cost + remaining production                      mandatory
    COLLECT_FERT.    100                                                     FERTILIZER base price
    FERTILIZE        the doubling it will actually buy, over 3 days

`CARE` coming out near $160 for one turn on a cow is not a thumb on the scale -- `pending_care_bonus`
accrues on every cared-and-fed day and is consumed as extra units on the next production day
(`kaggriculture.py:795-799`). It is genuinely one of the best ops in the game, which is what the
leaderboard correlation already said (CARE +0.441 against PLANT -0.358) and what nothing in this
project had acted on.
"""

import collections

from . import routines as R

TPD = R.TURNS_PER_DAY
WORK_TURNS = TPD - 1
SHED = tuple(R.shed_access_tiles())
SHED_SET = frozenset(SHED)
CROP = R.CROP_TABLE
ANIMALS = R.ANIMALS

#: The reference's `MARKET` bases (`kaggriculture.py:25-49`). Prices move with inventory during the
#: season, but the *ranking* is what the router needs and that is stable, so the bases are the right
#: constant to plan against rather than the live quote.
BASE_PRICE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
              "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}

#: TRIED: comparing fertilizing's gain against the fertilizer's mean REALISED sale price ($53, measured
#: via `scripts/the_market_ledger.py` on seed 11: 239 units sold for $12,601) instead of
#: `BASE_PRICE["FERTILIZER"]` (100, the market's I0 equilibrium price nobody actually pays). The
#: reasoning holds -- we collect 314 fertilizer-days a season against only 62-67 FERTILIZE ops, so
#: almost every unit is heading for a SELL order anyway, and the honest opportunity cost of routing one
#: into a tile is what it would have sold for. MEASURED NULL on the 12-seed ladder: identical
#: $109,688, FERTILIZE still 67/season, because the only case the threshold change touches is an
#: ongoing crop priced between $53 and $100 (TOMATO, $60), and this schedule's crop mix is
#: WHEAT/STRAWBERRY/MELON only -- confirmed by reading `data/seed_scripts/new_leader/schedule.json`,
#: no TOMATO or CARROT ever appears in a `plants` row. WHEAT's own best one-shot gain is a fixed $50
#: (2 extra units at $25), which sits just under $53 too, so it stays unaffected either way. Reverted
#: per protocol -- a tie does not beat the baseline -- and left here so the $53 number is not
#: re-derived and re-tried against a schedule it structurally cannot move.

#: Prize for a node that must be served or something dies. Large enough to dominate any ordinary
#: prize, finite so that two mandatory nodes still order by cost between themselves.
MANDATORY = 100_000

#: The reference's seed prices (`CROPS[...]["seed"]`). Seeds are NOT held in the shed or in a unit's
#: inventory -- `private["seeds"]` is consumed directly by PLANT -- which is why PLANT never generates
#: a depot stop no matter that it carries an item name.
SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}

#: Turns a unit needs to place an animal and then actually serve it the same day: walk to the shed,
#: draw wheat, walk back, FEED and CARE. Below this many turns left, a placement banks no product
#: today, and `build_nodes` prices it accordingly.
#: Ops forming the animal chain, assigned WHOLE to one unit before anything else. Empty restores plain
#: cheapest-insertion over every node. See the block in `plan_routes` for the day-0 measurement.
#: Whether a PLACE node also draws one WHEAT, for the feed that placement necessarily creates. Off
#: restores the old needs exactly. See `Node.__init__` for the day-0 measurement.
PLACE_DRAWS_FEED = True

CHAIN_OPS = ()          # MEASURED WORSE as a hard one-unit rule: 53 cells against 42,
                        # last PLACE pushed hour 20 -> 22. Our four pens are not one tour.

SERVICE_ROUND = 10

#: Ops whose item really is drawn at the shed. `BUILD` is here because the unit may as well carry the
#: animal on the same trip and PLACE it the turn after the pen goes up.
DRAWN = ("FEED", "FERTILIZE", "PLACE", "BUILD")


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------------------------------------------------------------------
# placement: the static half of the problem, solved once per land unlock rather than per turn
# ---------------------------------------------------------------------------------------------

#: Quadrants in the order the reference sells them (`LAND_ORDER` at [1000, 2000, 4000]), NW being free.
_QUAD_ORDER = ("NW",) + tuple(R.LAND_ORDER)


def field_order(unlocked, board_size=R.BOARD_SIZE):
    """Every workable tile we own, in the order it should be taken. Deterministic, no board state.

    Choosing WHICH tiles to farm is a facility-location problem, not a per-turn one: the set is worked
    ~20 times a season, so its shape is paid for over and over while the choice itself is made once.
    `_nearest_empty` scored one tile at a time on `(adjacency, distance)`, which grows a SNAKE out from
    whichever tile happened to be planted first -- locally adjacent at every step and globally a long
    thin thing to walk.

    A compact block is the right shape, and on a grid the right visiting order for a block is a
    **boustrophedon sweep**: rows taken in alternating direction, so consecutive tiles are always
    adjacent and covering `n` tiles costs `n - 1` steps. Anchoring each quadrant's sweep at its
    shed-access corner means the first tiles taken are the ones nearest the depot, so a farm that only
    ever fills half its ground automatically fills the near half.

    The four shed-access cells are left out: they are worth more as pens, where FEED, CARE,
    COLLECT_FERTILIZER, PICKUP and DROP all happen without a single move.
    """
    half = board_size // 2
    out = []
    for quad in _QUAD_ORDER:
        if quad not in unlocked:
            continue
        xs = range(0, half) if quad.endswith("W") else range(half, board_size)
        ys = range(0, half) if quad.startswith("N") else range(half, board_size)
        # Sweep away from the shed: rows nearest the middle first, and each row swept from the
        # middle outwards, alternating so the end of one row touches the start of the next.
        rows = sorted(ys, key=lambda y: -y if quad.startswith("N") else y)
        cols = sorted(xs, key=lambda x: -x if quad.endswith("W") else x)
        for i, y in enumerate(rows):
            for x in (cols if i % 2 == 0 else cols[::-1]):
                if (x, y) not in SHED_SET:
                    out.append((x, y))
    return out


# ---------------------------------------------------------------------------------------------
# prizes
# ---------------------------------------------------------------------------------------------

def _crop_remaining(cell, day):
    """Dollar value still recoverable from a planted tile, used as the cost of letting it weed."""
    info = CROP[cell["crop"]]
    price = BASE_PRICE[cell["crop"]]
    if not info["ongoing"]:
        age = day - cell["planted_day"]
        window_end = info["max_day"]
        if age > window_end:
            return cell.get("yield_units", 0) * price
        waters_left = window_end - max(age, (window_end + 1) // 2) + 1
        room = info["max_yield"] - cell.get("yield_units", 0)
        return max(0, min(room, waters_left)) * price
    # ongoing: one unit per production, `interval` days apart, `max_yield` productions in total
    age = day - cell["planted_day"]
    done = 0 if age < info["first"] else (age - info["first"]) // info["interval"] + 1
    left = max(0, info["max_yield"] - done)
    days_left = R.SEASON_DAYS - 1 - day
    return min(left, days_left // max(1, info["interval"]) + 1) * price


def _animal_remaining(cell, day):
    a = ANIMALS[cell["animal"]]
    price = BASE_PRICE[a["product"]]
    age = day - cell["placed_day"]
    days_left = R.SEASON_DAYS - 1 - day
    if age < a["first_yield_day"]:
        days_left -= a["first_yield_day"] - age
    return max(0, days_left) // a["interval"] * price


def crop_ops(cell, day, have_fertilizer):
    """`[(op, item, prize)]` worth doing on a planted tile today, in the order they must be emitted.

    FERTILIZE precedes WATER because WATER reads `fertilized_until_day` at the moment it runs.
    """
    info = CROP[cell["crop"]]
    price = BASE_PRICE[cell["crop"]]
    age = day - cell["planted_day"]
    held = cell.get("yield_units", 0)
    room = info["max_yield"] - held
    fertilized = cell.get("fertilized_until_day", -1) >= day
    out = []

    if not info["ongoing"]:
        in_window = (info["max_day"] + 1) // 2 <= age <= info["max_day"]
        # A one-shot water inside the window IS the yield: one unit, two if fertilized. So a melon
        # water is worth $250 -- the single highest-value op available -- and a melon water outside
        # the window is worth nothing at all.
        if in_window and room > 0:
            # Worth fertilizing only if the remaining window cannot fill the tile on plain waters.
            waters_left = info["max_day"] - age + 1
            if (not fertilized and have_fertilizer and waters_left < room
                    and cell.get("fertilized_until_day", -1) < day):
                gain = min(room, waters_left * 2) - min(room, waters_left)
                if gain * price > BASE_PRICE["FERTILIZER"]:
                    out.append(("FERTILIZE", "FERTILIZER", gain * price))
                    fertilized = True
            if not cell["watered_today"]:
                out.append(("WATER", None, price * (2 if fertilized else 1)))
        elif not cell["watered_today"] and cell["consecutive_unwatered"] >= 1:
            # Outside the window water buys nothing but survival, and it is only needed on the day
            # the tile would otherwise weed. This is the every-SECOND-day rule, derived:
            # `consecutive_unwatered` starts at 1 on the planting day and weeds the tile at 2, so a
            # tile watered yesterday is safe tonight and only the ones at 1 are on the brink.
            #
            # It is NOT mandatory, though the loss is real and permanent. Promoting it into the
            # mandatory pass alongside fourteen pens was measured over twelve seeds at **-$2,804**:
            # harvests recovered 296 -> 318 and feeding fell straight back, 321 -> 301, because a pass
            # that contains everything cannot triage.
            #
            # **This gate was widened to `>= 0` and then narrowed back, and the widening was an
            # error of attribution.** The justification was a table of waters per live plant tile
            # showing "the tape" watering ~1.06 every day against our alternating 0.06/1.00, with
            # day 1 at 18 waters to our 1. That table is real, and it is the OLD LEADER's tape.
            # Measured on the same harness the same day, seed 11, waters ours/tape:
            #
            #     oldleader   d0 16/17   d1 17/18   d2 18/19   d3 18/19      waters daily
            #     seb         d0 17/17   d1 17/0    d2 17/17   d3 17/14      waters alternate days
            #
            # The two tapes genuinely differ here, and Seb -- the stronger tape, and the one we are
            # matching -- reaches dawn on day 2 with all 17 tiles sitting at `consecutive_unwatered
            # = 1` and takes **zero weeds** through day 7 doing it. Watering the other 17 tiles on
            # day 1 is 17 work turns and ~31 walk turns for nothing at all.
            out.append(("WATER", None, _crop_remaining(cell, day)))
    else:
        # An ongoing crop produces at dawn regardless of water. Water is survival, plus the
        # fertilizer bonus on a production day. Watering it on any other day is pure walk.
        produces_tomorrow = (age + 1 >= info["first"]
                             and (age + 1 - info["first"]) % info["interval"] == 0)
        if not cell["watered_today"]:
            if cell["consecutive_unwatered"] >= 1:
                out.append(("WATER", None, _crop_remaining(cell, day)))
            elif fertilized and produces_tomorrow and room > 0:
                out.append(("WATER", None, price))
        if (produces_tomorrow and not fertilized and have_fertilizer and room > 1
                and price > BASE_PRICE["FERTILIZER"]):
            out.append(("FERTILIZE", "FERTILIZER", price))

    if held > 0 and age >= info["first"] and (info["ongoing"] or _one_shot_is_finished(info, age, room)):
        out.append(("HARVEST", None, held * price))
    return out


def _one_shot_is_finished(info, age, room):
    """Has a one-shot crop stopped being able to grow? Only then is harvesting it free money.

    HARVEST sets the tile to `None` (`kaggriculture.py:409`), so on a one-shot crop it is not a
    collection, it is a demolition. Offering it at `held * price` the moment the first unit lands made
    an age-3 wheat worth $25 to harvest against $25 for another water -- and since both ops hang off
    the SAME node, the visit did both: watered to two units, then deleted a tile that had a third
    water still owed to it. Seed 11 lost five crop tiles on day 3 that way.

    Nothing is forfeited once the window has shut (no further water can add a unit) or the tile is
    already at `max_yield`. Waiting past that only feeds the rot at `max_lifespan_step`.

    TRIED: also finishing a tile once `day >= R.SEASON_DAYS - 1` (or `- 2`), so a tile planted too late
    for its window to ever CLOSE would still get harvested rather than left standing forever --
    `age >= info["max_day"]` needs a day that may not exist. Diagnosed as real: 32 of 66 wheat
    plantings on seed 11 (48%) were still standing, unharvested, at season end, almost all of them from
    day 26-27, because `plant_prize` correctly still plants a truncated-window tile while this gate
    never recognised the window could not close. MEASURED as a LOSS on the 12-seed ladder even though
    the underlying bug is real and HARVEST count rose exactly as predicted (296 -> 323 a season):
    forcing the harvest one day (`day >= SEASON_DAYS - 1`) cost **-$92**; forcing it two days early
    (`- 2`, tested stacked with the PASTURE fix below) cost far more. The harvested units still have to
    reach the shed (DROP) and clear a SELL order before the game ends, and a late-season forced harvest
    does not reliably get there -- so the fix converts "still growing, banks $0" into "harvested but
    unsold, banks $0" at the cost of a turn that would otherwise have gone to something that clears.
    Reverted. The bug is real; this fix for it is not a net win on this benchmark.
    """
    return age >= info["max_day"] or room <= 0


def animal_ops(cell, day, have_wheat):
    """`[(op, item, prize)]` for a stocked pen. FEED is mandatory the day after a missed feed."""
    a = ANIMALS[cell["animal"]]
    price = BASE_PRICE[a["product"]]
    out = []
    fed = cell["fed_today"]
    if not fed and have_wheat:
        hungry = cell.get("consecutive_unfed", 0) >= 1
        # **Every feed is mandatory, not only the one that prevents an escape.** Priced at one unit of
        # product a cow's FEED was $160 for a turn against a melon water's $250, so on any tight day the
        # ratio rule skipped the pen -- and skipping it forfeits the day's production AND the care
        # bonus, since `pending_care_bonus` is only paid out on a day the animal is also fed. Across 312
        # leaderboard seats FEED correlates +0.452 with final money and WATER -0.276, so the ranking was
        # inverted against the only op-level evidence we have.
        #
        # A hungry day is still worth more than a healthy one -- the animal itself is on the line -- so
        # the two stay ordered above the shared mandatory floor.
        prize = MANDATORY + price + ((a["cost"] + _animal_remaining(cell, day)) if hungry else 0)
        out.append(("FEED", "WHEAT", prize))
        fed = True
    if not cell["cared_today"] and fed:
        # `pending_care_bonus` is only consumed on a day the animal is ALSO fed, so an uncared or
        # unfed pen banks nothing. One care = one extra unit of product on the next production day.
        out.append(("CARE", None, price))
    if cell.get("fertilizer_available"):
        out.append(("COLLECT_FERTILIZER", None, BASE_PRICE["FERTILIZER"]))
    if cell.get("yield_units", 0) > 0:
        out.append(("HARVEST", None, cell["yield_units"] * price))
    return out


def plant_prize(crop, day):
    """What a fresh planting is worth, or 0 if the season cannot finish it.

    A melon needs to reach age 12 and a wheat age 4, so late in the season most of the crop table is
    literally worth nothing and the ground is better left empty than seeded.
    """
    info = CROP[crop]
    price = BASE_PRICE[crop]
    days_left = R.SEASON_DAYS - 1 - day
    if not info["ongoing"]:
        # **A one-shot crop pays only through a HARVEST, and HARVEST is only offered once the yield
        # window has SHUT** (`_one_shot_is_finished`). So the crop must reach age `max_day` with a turn
        # left to collect it -- reaching `first_yield_day` buys nothing at all. Gating on `first`
        # planted wheat that could never be collected: 32 of 66 wheat plantings sat unharvested at
        # season end against the tape's 1 of 66, each costing a seed, a PLANT turn and a WATER turn,
        # and holding ground that a later replant could have used.
        if days_left < info["max_day"]:
            return 0
        window_end = min(info["max_day"], days_left)
        waters = window_end - (info["max_day"] + 1) // 2 + 1
        return max(0, min(info["max_yield"], waters)) * price
    if days_left < info["first"]:
        return 0
    prods = (days_left - info["first"]) // info["interval"] + 1
    return min(info["max_yield"], prods) * price


# ---------------------------------------------------------------------------------------------
# nodes
# ---------------------------------------------------------------------------------------------

class Node:
    """One tile, every op worth doing there today, and what must be drawn at the depot first."""

    __slots__ = ("tile", "ops", "prize", "service", "needs", "mandatory")

    def __init__(self, tile, ops):
        self.tile = tile
        self.ops = [(op, item) for op, item, _p in ops]
        self.prize = sum(p for _o, _i, p in ops)
        self.service = len(ops)
        self.needs = collections.Counter(i for o, i, _p in ops if i and o in DRAWN)
        # **A PLACE draws the feed for the animal it is about to put in the pen.**
        # `build_nodes` cannot emit a FEED node for a tile until an animal is standing on it, so the
        # feed that MUST follow a placement is invisible at plan time and no wheat is ever drawn for
        # it. Measured on Seb's tape, seed 11, day 0: u0 leaves the shed at hour 6 carrying a cow and
        # no wheat, builds at (2,3) on hour 9, places on hour 10, and then stands beside a hungry
        # animal with an empty route on hour 11. The wheat only arrives on a second shed trip at
        # hour 15 -- and the same unit walks over an unfed sheep at (3,4) on the way to fetch it.
        #
        # PICKUP is unbounded and the shed trip is already being made for the animal, so carrying the
        # feed on the same trip costs nothing but the draw itself. The tape does exactly this: it
        # picks up at hours 1, 3 AND 8, moving animals and wheat together.
        if PLACE_DRAWS_FEED:
            for o, _i, _p in ops:
                if o == "PLACE":
                    self.needs["WHEAT"] += 1
        self.mandatory = any(p >= MANDATORY for _o, _i, p in ops)

    def __repr__(self):
        return f"Node{self.tile}{[o for o, _ in self.ops]}@${self.prize:.0f}/{self.service}t"


def build_nodes(tiles, day, shed, carried, unlocked, pinned, hour=0):
    """Every tile worth visiting today, as routing nodes.

    `carried` is the union of what the crew already holds, so a task whose input is neither in the
    shed nor in a hand is never queued at all -- the deadlock that cost $45,623 was a unit holding
    the board's highest-priority job while standing on an empty shed.
    """
    have_wheat = shed.get("WHEAT", 0) > 0 or carried.get("WHEAT", 0) > 0
    have_fert = shed.get("FERTILIZER", 0) > 0 or carried.get("FERTILIZER", 0) > 0
    nodes = []
    for y, row in enumerate(tiles):
        for x, cell in enumerate(row):
            tile = (x, y)
            if tile in pinned or not isinstance(cell, dict):
                continue
            if R.quadrant_of(x, y) not in unlocked:
                continue
            kind = cell.get("kind")
            if kind == "PLANT":
                ops = crop_ops(cell, day, have_fert)
            elif "animal" in cell:
                ops = animal_ops(cell, day, have_wheat)
            elif kind in ("PASTURE", "COOP"):
                # TRIED: PASTURE is shared by COW and SHEEP, and picking the first match in
                # `R.ANIMAL_NAMES = ["GOOSE", "COW", "SHEEP"]` order means COW wins every time both are
                # in the shed at once, regardless of which is actually worth more or bought first.
                # Diagnosed as real: a SHEEP bought seed 11 day 5 hour 1 was not PLACEd until day 8 hour
                # 9, three days idle in the shed, while later COWs kept taking the one open pasture.
                #
                # Replacing the fixed order with "score every available type by `cost + remaining` and
                # let the better one win" (matching every other node's economics) MEASURED as a LOSS of
                # **-$5,676** on the 12-seed ladder -- animal-days and money both fell. The isolated
                # theory (SHEEP at day 5 is worth $1700 against COW's $1680) is correct in the one
                # example it was built from, but the schedule wants 8 COW against 6 SHEEP for the whole
                # season, and a value-ranked tie-break reallocates far more pastures than the one it was
                # diagnosed on -- it does not know the season wants more COWs than SHEEP overall, only
                # that SHEEP looks marginally better THIS turn. Reverted. The bug (one SHEEP idle three
                # days) is real; ranking every tie by same-turn value is not the fix for it.
                ops = []
                for a in R.ANIMAL_NAMES:
                    if ANIMALS[a]["structure"] != kind:
                        continue
                    if shed.get(a, 0) > 0 or carried.get(a, 0) > 0:
                        # **Price the hour in.** A placement is not worth the same all day: an animal
                        # put in a pen at dawn is fed, cared for and starts producing today, while one
                        # placed at dusk gets none of that -- a FEED is a shed round trip of ~8 turns
                        # against a budget of `TPD - hour - 1`. Measured on Seb's tape, seed 11, day 0,
                        # our last two animals land at hour 18 and are never fed: `feed -2`, `care -2`.
                        #
                        # A flat price gives the planner no reason to serve it early, and FORCING it to
                        # (an urgent-op replan trigger) just makes it outbid something else -- PLANT
                        # fell 17 -> 16 and an existing day-0 test went red. Pricing the hour honestly
                        # fixes both directions: a dawn placement wins on merit, a dusk one correctly
                        # loses to a plant rather than being forced through.
                        served = ANIMALS[a]["cost"] + _animal_remaining(
                            {"animal": a, "placed_day": day}, day)
                        if TPD - hour - 1 < SERVICE_ROUND:
                            served -= BASE_PRICE[ANIMALS[a]["product"]]
                        ops = [("PLACE", a, max(1.0, served))]
                        break
            elif kind == "WEED":
                # Worth exactly the planting it unblocks, so late in the season a weed is furniture.
                best = max((plant_prize(c, day) for c in R.CROPS), default=0)
                ops = [("DIG", None, best * 0.5)] if best else []
            else:
                ops = []
            if ops:
                nodes.append(Node(tile, ops))

    for tile, (op, item, prize) in pinned.items():
        if R.quadrant_of(tile[0], tile[1]) in unlocked:
            nodes.append(Node(tile, [(op, item, prize)]))
    return nodes


# ---------------------------------------------------------------------------------------------
# routing: cluster-first is implicit in cheapest-insertion, then 2-opt each route
# ---------------------------------------------------------------------------------------------

def _path_len(start, seq):
    d, cur = 0, start
    for t in seq:
        d += dist(cur, t)
        cur = t
    return d


def _two_opt(start, seq, keep_prefix=0):
    """Standard 2-opt on an OPEN path. `keep_prefix` pins the depot stop at the front."""
    if len(seq) - keep_prefix < 3:
        return seq
    best = list(seq)
    best_len = _path_len(start, best)
    improved = True
    while improved:
        improved = False
        for i in range(keep_prefix, len(best) - 1):
            for j in range(i + 1, len(best)):
                cand = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                cl = _path_len(start, cand)
                if cl < best_len - 1e-9:
                    best, best_len, improved = cand, cl, True
    return best


def plan_routes(units, nodes, budget, depots=SHED, carry=None):
    """Assign nodes to units and order each unit's tour. Returns `{unit: [Node, ...]}`.

    Greedy cheapest-insertion on **prize / marginal cost**, which is the standard Team Orienteering
    heuristic, then 2-opt per route. Mandatory nodes are placed first and unconditionally, so a
    hungry animal is never outbid by a melon.

    The marginal cost of inserting node `n` between `prev` and `next` is
    `d(prev,n) + d(n,next) - d(prev,next) + n.service`, evaluated in O(1), so the whole assignment is
    a few hundred thousand integer operations -- run once per replan, not per turn.
    """
    # **Only shed cells we OWN are depots.** `_spawn_hand` ignores ownership, so hands wake on `(5,4)`,
    # `(4,5)` and `(5,5)`, which are LOCKED until $1,000, $2,000 and $7,000 of land is bought -- and
    # `_apply_unit_action` returns on a LOCKED tile *before* it reaches PICKUP. Treating all four as
    # depots put three of five hands on a locked cell emitting a PICKUP that did nothing, all day.
    depots = tuple(depots) or SHED
    routes = {u: [] for u in range(len(units))}
    used = {u: 0 for u in range(len(units))}
    depot = {u: collections.Counter() for u in range(len(units))}
    depot_at = {u: None for u in range(len(units))}
    # **A vehicle arrives with a load.** Hands are hired through the morning and every hire forces a
    # replan, so by mid-morning units are already carrying wheat, fertilizer and animals. Costing every
    # item-bearing stop as a fresh shed trip sent a unit with an empty hand to an empty shed while
    # another stood holding the feed: eight wheat carried, four hungry animals, FEED 0, herd gone.
    held = {u: collections.Counter((carry or {}).get(u) or {}) for u in range(len(units))}
    left = list(nodes)

    def seq(u):
        out = []
        if depot_at[u] is not None:
            out.append(depot_at[u])
        out.extend(n.tile for n in routes[u])
        return out

    def delta(u, n, i):
        """Turn cost of putting `n` at position `i` of unit `u`'s route, depot stop included."""
        s = seq(u)
        off = 1 if depot_at[u] is not None else 0
        at = i + off
        prev = s[at - 1] if at > 0 else units[u]
        nxt = s[at] if at < len(s) else None
        d = dist(prev, n.tile) + (dist(n.tile, nxt) - dist(prev, nxt) if nxt else 0)
        extra = n.service
        short = _uncovered(u, n)
        if short:
            if depot_at[u] is None:
                # One shed trip per unit per day: PICKUP is unbounded in quantity, so the only cost
                # of another pen on the round is the walk to it.
                home = min(depots, key=lambda c: dist(c, units[u]))
                first = s[0] if s else n.tile
                extra += len(short) + dist(units[u], home) + dist(home, first) - dist(units[u], first)
            else:
                extra += sum(1 for it in short if depot[u][it] == 0)
        return d + extra

    def _uncovered(u, n):
        """What this node needs that the unit is not already carrying, after everything assigned so far."""
        return {it: c - held[u][it] for it, c in n.needs.items() if c > held[u][it]}

    def commit(u, n, i, c):
        """Put `n` at position `i` of unit `u`, paying `c` turns and booking whatever it must draw."""
        short = _uncovered(u, n)
        routes[u].insert(i, n)
        used[u] += c
        # Consume the load first, and only draw the remainder. `held` going down as stops are added
        # is what stops three pens on one unit each costing a shed trip.
        for it, qty in n.needs.items():
            held[u][it] = max(0, held[u][it] - qty)
        if short:
            if depot_at[u] is None:
                depot_at[u] = min(depots, key=lambda t: dist(t, units[u]))
            depot[u].update(short)

    # ------------------------------------------------------------------ the animal chain, kept whole
    # **PICKUP -> PLACE -> FEED -> CARE is a chain, not four independent prizes.** It has real
    # precedence and a same-day deadline: an animal must be in a pen before it can be fed, and fed
    # before CARE banks anything (`pending_care_bonus` is consumed only on a day the animal is also
    # fed). Cheapest-insertion has no representation for either, so it interleaves the chain with
    # fungible work and fragments it across units and hours.
    #
    # Measured on Seb's tape, seed 11, day 0. Both sides plant 17, water 17, build 8 pastures and
    # place 4 animals -- the schedule lands either way. The whole difference is the chain:
    #
    #     tape u0   B u d u L ^ L v u ^ < L ^ L v v > c ^ < c     places at 4, 6, 11, 13
    #     ours u0   B u L < < B L ^ B < B . v > > > u ^ < < L <   places at 2, 6, and 20
    #
    # The tape dedicates one unit to the chain and never lets it build. Ours places two animals, wanders
    # off to BUILD_PASTURE at hours 5, 8 and 10, returns for a pickup at 16 and places the fourth at
    # hour 20 -- too late to feed or care it. That is the entire day-0 work gap: FEED 3/4, CARE 3/4.
    #
    # So the chain is assigned first, whole, to the single unit that serves it cheapest. Everything
    # after it is order-free and still goes to plain cheapest-insertion.
    if CHAIN_OPS:
        chain = [n for n in left if any(o in CHAIN_OPS for o, _i in n.ops)]
        if chain:
            def chain_cost(u):
                pos, total = units[u], 0
                for n in chain:
                    total += dist(pos, n.tile) + n.service
                    pos = n.tile
                return total

            best_u = min(range(len(units)), key=lambda u: (chain_cost(u), used[u]))
            for n in sorted(chain, key=lambda n: -n.prize):
                spot = min(((delta(best_u, n, i), i) for i in range(len(routes[best_u]) + 1)),
                           default=None)
                if spot is None or used[best_u] + spot[0] > budget[best_u]:
                    continue                  # no room today; it stays in `left` for the general pass
                commit(best_u, n, spot[1], spot[0])
                left.remove(n)

    order = sorted(left, key=lambda n: -n.prize)
    # Mandatory nodes are assigned in their own pass, so a hungry animal cannot be outbid on ratio by a
    # melon that happens to be nearer. Within the pass they still order by cost.
    for pool in ([n for n in order if n.mandatory], [n for n in order if not n.mandatory]):
        remaining = list(pool)
        # **Parallel insertion, least-loaded unit first.** The obvious construction -- scan every
        # (node, unit, position) and commit the single best `prize / delta` -- minimises total walking,
        # and total walking is the wrong objective here. Units are hired for the whole day whether they
        # move or not, so an idle unit's turns are free and the scarce resource is per-unit TIME.
        #
        # On a serpentine field that distinction is decisive: appending the next tile to the unit
        # already standing on the previous one costs delta 2, while starting an idle unit from the shed
        # costs delta 6, so the sequential rule packs one vehicle and starves the rest. Day 0 of seed 11
        # measured `10, 9, 2, 0, 0` across five units -- two saturated at 21 and 20 turns against a
        # budget of 21, two given nothing -- and six of the twenty-one pinned jobs were never started.
        #
        # But pure round-robin -- every unit claims one node per round -- overcorrects, because it hands
        # a job to a distant idle unit even when a loaded one is standing beside it. Measured over five
        # seasons it converted 776 idle turns into 742 extra MOVES for no extra work at all
        # (`moves per work op` 0.94 -> 1.26) and cost the herd 26 feeds, since a far unit now outbid the
        # unit already at the pen.
        #
        # So: keep the global cheapest-insertion rule, and only force the spread when a unit reaches its
        # fair share of the day. The cap starts at `budget / n_units` and relaxes in `n_units` steps, so
        # walking is minimised inside each pass and no unit can eat the whole field before the others
        # have been offered any of it. The final pass has cap == budget, so nothing is ever left unserved
        # that the plain rule would have served.
        n_u = max(1, len(units))
        for step in range(1, n_u + 1):
            cap = {u: budget[u] * step / n_u for u in range(len(units))}
            while remaining:
                best = None
                for n in remaining:
                    for u in range(len(units)):
                        for i in range(len(routes[u]) + 1):
                            c = delta(u, n, i)
                            if used[u] + c > cap[u]:
                                continue
                            score = n.prize / max(1, c)
                            if best is None or score > best[0]:
                                best = (score, n, u, i, c)
                if best is None:
                    break                          # nothing more fits under this cap; relax it
                _s, n, u, i, c = best
                commit(u, n, i, c)
                remaining.remove(n)

    for u in routes:
        if len(routes[u]) < 3:
            continue
        by_tile = {n.tile: n for n in routes[u]}
        start = depot_at[u] if depot_at[u] is not None else units[u]
        ordered = _two_opt(start, [n.tile for n in routes[u]])
        new = [by_tile[t] for t in ordered]
        cost = _path_len(start, ordered) + sum(n.service for n in new)
        if depot_at[u] is not None:
            cost += dist(units[u], depot_at[u]) + len(depot[u])
        if cost <= budget[u]:
            routes[u] = new
            used[u] = cost

    return {u: dict(route=routes[u], depot=depot_at[u], draw=depot[u], cost=used[u])
            for u in routes}
