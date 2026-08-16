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

#: An op that prevents an IRREVERSIBLE loss today, assigned in its own pass ahead of MANDATORY.
#:
#: A tier and not a bigger number, deliberately. `plan_routes` ranks inside a pool by
#: `prize / marginal cost`, and every mandatory prize sits on the 100,000 floor, so urgency separates
#: two FEED nodes by about 1% while distance separates them by up to 8x. Measured on Seb's tape,
#: seed 11, day 16:
#:
#:     at-risk pen   prize 101,500, 8 steps away  ->  score  12,687
#:     healthy pen   prize 100,160, 1 step  away  ->  score 100,160    wins by 8x
#:
#: So the near healthy pen is served and the far animal starves out, with ten wheat spare in the
#: shed. Raising the at-risk prize cannot fix that -- it would have to beat an 8x denominator swing,
#: and then it would outrank genuinely urgent work on the next board. Ordering by tier says the
#: actual thing: losing the animal is not a bigger prize, it is a different kind of event.
CRITICAL = 1_000_000

#: Whether a pen one missed day from losing its animal is CRITICAL rather than merely mandatory.
#: A flag so the arm stays attributable, and because this repo records four separate occasions where
#: an animal verdict turned out to be a measurement artifact. Any accepted version must be judged on
#: ANIMALS STANDING IN PENS per day, never on cells or money alone.
FEED_IS_CRITICAL_WHEN_AT_RISK = True


#: The last day whose carried load is banked overnight. d29's own drop lands after the final turn.
LAST_FREE_DROP_DAY = R.SEASON_DAYS - 2

HARVEST_IS_CRITICAL_ON_ITS_LAST_SAFE_DAY = True

#: **Day 9, so the matched opening cannot move.** Wheat planted d0 reaches `age == max_day` on d4,
#: so an ungated version WOULD re-rank d4 -- inside the d0-d8 window that is matched to the tape op
#: for op and must not regress. Nothing actually rots before d16 on seed 11, so gating here costs
#: nothing measurable and removes the whole class of risk by construction.
HARVEST_CRITICAL_FROM_DAY = 9

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

#: Whether a PLACE joins the MANDATORY pool, which `plan_routes` assigns against an empty budget,
#: instead of the optional pool it is offered to once the day is spent. `None` restores the old
#: behaviour exactly; an int is the first day it applies, so the early days can be held fixed.
#:
#: **The stranded animal is a budget failure, not a pricing one, and that is measured.** Seb's tape,
#: seed 11, two SHEEP in the shed beside the empty pens at (8,0) and (9,0) from day 14 to season end.
#: Every `plan_routes` call on days 14 and 15 refused them, and every refusal was OVER BUDGET:
#:
#:     d14 h0   cheapest append 16 turns, u0 had used 23 of 23
#:     d14 h1   cheapest append  8 turns, u1 had used 21 of 22
#:     d14 h2   cheapest append  4 turns, u10 had used 21 of 21
#:     d14 h12  cheapest append 18 turns, u0 had used  8 of 11
#:     d14 h19  cheapest append 10 turns, u5 had used  0 of  4
#:
#: Not one refusal was a ratio loss. Early in the day there is budget and no free unit; late there is
#: a free unit and no budget, because `budget = TPD - hour - 1` has collapsed to single digits while
#: the round trip to the far corner still costs ten to eighteen turns. The two windows never overlap,
#: which is why the animal sits there for sixteen days rather than a few.
#:
#: MEASURED, and it is the reason this is not a price: multiplying the PLACE prize by 2, 3, 5 and 10
#: leaves the season **identical to the dollar** -- penned, animals in the shed and money agree on
#: every one of eighteen days. Only x0 moves anything. `days_left * BASE_PRICE["FERTILIZER"]` on the
#: prize, tried before this, is the same non-event for the same reason.
#:
#: This does NOT let a placement jump the budget: mandatory nodes are still refused when
#: `used + cdelta > cap`. It only gives the placement first claim on turns that are otherwise gone by
#: the time it is offered. Nor does it outrank a hungry animal -- ordering inside the pool is still
#: `prize / cost`, and a FEED's $100,900 over two turns beats a placement's $101,100 over ten.
#:
#: SWEPT on the gate day, seed 11, Seb's tape, `breakdown.py --days 17 --diff` differing cells:
#:
#:     gate        d0-d11    d12  d13  d14  d15  d16     animals in pens d13-d28
#:     None (off)  baseline   12   12   14   17   16     17 x12 then 18 18 18 18
#:     0           identical  --   --   --   --   --     16 from d14, and never recovers
#:     6           identical  --   --   --   --   --     16 from d14, and never recovers
#:     12          identical  13   12   12   18   18     17 18 18 18 18 17 ... 17
#:     13          identical  12   14   16   17   20     18 19 18 18 ... 17
#:     14          identical  12   12   12   17   19     17 19 19 17 17 ... 17
#:
#: **14, because it is the only gate that moves the target day without moving an earlier one.**
#: d0-d11 are byte-identical under every gate. 0 and 6 drop the herd to 16 and hold it there, which
#: is the starvation floor and disqualifying on its own. 12 pays d12 12 -> 13. 13 pays d13 12 -> 14
#: AND makes the target day worse, 14 -> 16. Only 14 leaves every earlier day untouched.
#:
#: At d14 it takes the two fields this is about to EXACT: `sheep` -2 -> 0 and `place` -2 -> 0, with
#: `feed` -2 -> -1, `care` -2 -> -1 and idling +17 -> +5. The shed holds no animal from d14 on.
#:
#: **What it exposed, which is a SEPARATE defect and is left open deliberately.** d16 goes 16 -> 19
#: cells and the season bank ends $102,083 against $104,469. The cause is not the placement; it is
#: what the two extra animals cost once they are in pens. Measured at d16, ours minus tape, off ->
#: on: `water` +3 -> -1, `strawb` -3 -> -7, `weeds` 0 -> +2, `dig` +2 -> +5, `harvest` -2 -> -4.
#: Two more pens is six more ops a day (FEED, CARE, COLLECT_FERTILIZER x2) and they come out of
#: WATER, so strawberry tiles weed and then have to be dug.
#:
#: The herd shows it too: penned peaks at 19 on d14-d15 and falls back to 17 on d16 with the shed
#: EMPTY, so two animals starved and escaped rather than being sold. The old run only looked
#: healthier because those two animals were parked in the shed, where nothing can starve them and
#: they also earn nothing -- the flat 17 was hiding a feed pipeline that cannot carry 19.
#:
#: The gap does NOT compound: -$1,510 at d16 and -$2,386 twelve days later, because the animals that
#: do survive earn most of it back. So the next question is the feed/turn budget at 19 pens, not
#: whether to place them.
#:
#: **The gate day is fitted to one seed and one tape and should be treated as such.** The rule it
#: encodes -- a placement must be offered before the budget is spent -- is general; the number 14 is
#: not, and it is where the schedule stops buying animals on THIS tape, so a stranded one stays
#: stranded. A gate keyed on "this animal was already in the shed yesterday" would say the same thing
#: without the magic number, and needs the shed's age plumbed through `build_nodes`. Worth doing
#: before this is trusted on another seed.
PLACE_IS_MANDATORY_FROM_DAY = 14

CHAIN_OPS = ()          # MEASURED WORSE as a hard one-unit rule: 53 cells against 42,
                        # last PLACE pushed hour 20 -> 22. Our four pens are not one tour.

SERVICE_ROUND = 10

#: `FILLING_WATER` -- the water that takes a one-shot crop to `max_yield` also offers its HARVEST.
#:
#: **This is the day-10 melon, and it was never a delivery fault.** Measured on Seb's tape, seed 11,
#: day 10, weeds off (`scripts/when_the_melon_fills.py`), the hour each of the three ripe MELON tiles
#: first reads 6/6 and so becomes harvestable at all:
#:
#:     SEB   (4,2)=h6   (3,1)=h9   (4,1)=h9        -> SELL 12 @h13, SELL 6 @h15, 0 in shed at dawn
#:     OURS  (2,0)=h15  (1,0)=h16  (0,0)=h18       -> harvested h17/h19/h20, 18 in shed at dawn
#:
#: Both sides wake with the same three tiles at **5/6**. MELON is a one-shot, and
#: `_one_shot_is_finished` refuses HARVEST while `room > 0` -- correctly, since HARVEST demolishes
#: the tile. So the harvest could not have happened earlier than the fill on either side, and ours
#: lands one to three turns after it. The HARVEST is prompt; the WATER is seven hours late. Seven
#: previous arms moved the delivery leg, which is two steps downstream of this.
#:
#: The water is late because of its price. An in-window one-shot water is priced at the single unit
#: of yield it adds, $250. An out-of-window survival water on an immature melon is priced at
#: `_crop_remaining`, the whole tile, $1,250-$1,500. So the planner ranked insurance on a tile that
#: cannot yield for two more days five times above the one water that unlocks same-day money, and
#: `plan_routes` -- prize-sorted, `prize / cost`-scored -- put it at dusk.
#:
#: That price is right for a water with room to spare and wrong for the LAST one, which is the only
#: thing between the tile and its whole harvest. When the water fills the tile, the node offers the
#: HARVEST too: `_live_ops` re-derives at the tile, so the unit waters, and next turn `room == 0`
#: makes `_one_shot_is_finished` true and the same stop emits the HARVEST. No new mechanism -- the
#: crew already does exactly this back-to-back pair, and this only makes the planner see it coming.
FILLING_WATER = True

#: Ops whose item really is drawn at the shed. `BUILD` is here because the unit may as well carry the
#: animal on the same trip and PLACE it the turn after the pen goes up.
DRAWN = ("FEED", "FERTILIZE", "PLACE", "BUILD")

#: Ops that put a sellable item into the unit's own inventory. The market only ever reads the SHED,
#: so anything still in a hand at dusk is unsold -- it arrives overnight, a turn too late.
YIELDING = ("HARVEST", "COLLECT_FERTILIZER")



#: **A pen is placed with the animal it was BUILT for.**
#:
#: This is the "upstream of `build_nodes`, in the buy/place order" the note above ends on, and it
#: turns out to be one line of bookkeeping rather than a new ranking. `_refresh_pins` already sites
#: pens one at a time against the schedule's ORDERED `places` row and stamps each with an animal --
#: `pins[spot] = ("BUILD", a, cost)`. The near ground is pinned first, so the row's order already
#: decides who gets the short walk. Seb's day-0 row is `['SHEEP', 'SHEEP', 'COW', 'COW']` and his
#: board reads exactly that. The assignment was being made correctly and then thrown away: the
#: instant the pen is BUILT the tile stops being `None`, `_refresh_pins` pops the pin, and the
#: animal is re-derived here from `R.ANIMAL_NAMES = ["GOOSE", "COW", "SHEEP"]` -- so COW wins every
#: PASTURE. Measured, seed 11, weeds off, at day 1 dawn:
#:
#:     Seb   SHEEP@(4,4)d0  SHEEP@(4,3)d1  COW@(3,3)d2  COW@(2,3)d3    sheep walk 0 + 1 = 1
#:     ours  COW@(4,4)d0    SHEEP@(3,4)d1  COW@(2,4)d2  SHEEP@(1,4)d3  sheep walk 1 + 3 = 4
#:
#: Both blocks sum to 22 from the depot, so no SITING rule can close this -- it is not a shape
#: problem. `PEN_SPOTS`, `PEN_NEAREST_DEPOT` and `PEN_NEAREST_DEPOT_FROM_DAY` all move WHERE a pen
#: goes and none of them can move WHICH animal ends up in it.
#:
#: It is not the value tie-break rejected in `build_nodes` either, which cost **-$5,676** on the
#: 12-seed ladder. That one ranked animals by same-turn worth and so could not see that the season
#: wants 8 COW against 6 SHEEP; this one ranks nothing and reads back a decision the schedule
#: already made. The failure mode they share -- refusing an available animal while waiting for a
#: better one -- is excluded by construction: an unfillable reservation falls straight through to
#: the old order, pinned by
#: `tests/test_the_pen_holds_the_animal_it_was_built_for.py::test_a_reservation_the_shed_cannot_fill_falls_back_rather_than_stalling`.
PEN_KEEPS_ITS_ANIMAL = True

#: Cost an insertion as a CLOSED tour -- `delta + homeward(after) - homeward(before)` -- rather than
#: charging a flat return reserve at acceptance. It is the textbook closed-tour marginal and it is
#: exact at every insertion position, not only when the node lands at the current end of the route,
#: so a far node can be resequenced onto the way back instead of being refused outright.
#: It needs `SUPPLY_LEDGER`: on its own it MEASURED as day 3 `sell` 5/5 -> 3/5 and day 4 `place`
#: 1/1 -> 0/1, because costing the tour honestly sorts a phantom PLACE node to the tail of the day,
#: which is exactly where a node that turns out to be fake does the most damage.
CLOSED_TOUR = True

#: Turns charged for the DROP that ends a carrying tour. `delta` already prices the depot DRAW -- one
#: turn per item picked up, plus the detour -- but nothing has ever priced putting the load DOWN, so
#: the return leg, the opportunistic drop and `DELIVER_THE_SELL_ROW` are all free at plan time and
#: cost a real turn at run time. Measured 2026-08-07 over days 0-12 of seed 11, restricted to stops
#: the unit actually reached: depot cells were planned at 77 turns and took 114 (63% of visits
#: overrun), field tiles 410 against 454. See `docs/service_undercount_2026-08-07.md`.
#: **TRIED and REVERTED at 1 and 2.** A flat charge on the homeward leg is the wrong SHAPE: the
#: overrun the probe found is concentrated on DEPOT-TILE nodes (63% of visits, +48%), not at tour
#: ends. At 1 the first day it touches regresses -- d2 4 -> 6 and d5 7 -> 8 -- which under "days
#: match IN ORDER" is disqualifying, even though d6, d7 and d8 all improve (11->10, 15->13, 13->12).
#: At 2 it is a rout: d6 11 -> 19, d7 15 -> 20, d10 19 -> 24.
HOMEWARD_DROP_TURNS = 0

#: Extra turns added to a node's service when its tile is a shed-access cell. Pens sit ON those cells
#: by design, so a unit servicing one also PICKUPs and DROPs there, and none of that is in `node.ops`
#: -- which is why d0 u0 at (4,4) was planned at 1 turn and took 7.
#:
#: **TRIED and REVERTED at 1, 2 and 3**, alongside `HOMEWARD_DROP_TURNS` above:
#:
#:                d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11
#:     0 (ships)   7  6  4  7  7  7 11 15 13 15  19  20
#:     1           7  6  6  7  9 12 13 13 14 19  23  24
#:     2           7  7  6  7  9  9 13 15 10 17  19  21
#:     3           7  6  5  7  9  7 11 14 11 12  20  24
#:
#: Every arm regresses d2 and d4, the earliest days it touches, and days are matched IN ORDER.
#:
#: **The under-count is real; making the estimate honest is not the fix.** Both levers price the
#: missing turns correctly and both make day-matching worse, because a cheaper tour packs more stops
#: and that happens to reproduce the tape's day shape better than an accurate one does. So the two
#: constants stay at 0 as documentation of a measured dead end, and a delivery node is NOT gated on
#: correcting the estimate the way `docs/idle_at_h10_2026-08-07.md` proposed -- inflating costs is
#: not a route to it. Anything that adds a stop has to EARN its turns, not be handed them.
DEPOT_NODE_EXTRA_SERVICE = 0

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------------------------------------------------------------------
# placement: the static half of the problem, solved once per land unlock rather than per turn
# ---------------------------------------------------------------------------------------------

#: Quadrants in the order the reference sells them (`LAND_ORDER` at [1000, 2000, 4000]), NW being free.
_QUAD_ORDER = ("NW",) + tuple(R.LAND_ORDER)


#: Whether the placement order is sorted by distance to the depot ring, with the sweep as tie-break,
#: instead of being quadrant-major.
#:
#: **What it is for.** `field_order` is content-BLIND -- the Nth thing placed gets the Nth tile of the
#: sweep, whatever it is -- and different contents want wildly different numbers of visits. Measured
#: over a whole season, seed 11, weeds off, ours against Seb's tape
#: (`scripts/where_the_walking_goes.py`, `data/logs/geometry_measure.log`), work turns landed per tile:
#:
#:     pen, COW                       7 tiles    991 visits   141.6 per tile
#:     pen, SHEEP                     8 tiles    579 visits    72.4 per tile
#:     strawberry                    37 tiles    592 visits    16.0 per tile
#:     melon                          8 tiles     90 visits    11.2 per tile
#:
#: So the depot ring is worth five to nine times more to a pen than to a crop, and the sweep hands it
#: out on arrival order. Our own board pays for that: pens at (7,0) d6, (8,0) d7 and (9,0) d8, all
#: sited on day 9 at the TAIL of NE, while the near band of SW sat empty. Total pen distance 52 against
#: the tape's 45 over the same nineteen pens.
#:
#: Sorting by distance is the whole of the fix that is reachable from here. `schedule_agent._refresh_pins`
#: already consumes the order pens-first WITHIN a day, so a distance-sorted order gives the near ground
#: to the pens automatically; what it cannot do is reserve near ground on day 0 for a pen that arrives
#: on day 9, which needs the schedule and lives upstream.
#:
#: The sort is STABLE, so the sweep still orders each distance band and a block stays as compact as a
#: Manhattan ring allows. It is not contiguous any more --
#: `test_the_placement_order_is_a_contiguous_sweep_from_the_shed` is asserted against the flag OFF for
#: exactly that reason.
#:
#: `None` restores the plain quadrant-major sweep exactly. An int is the minimum number of owned
#: QUADRANTS at which the sort applies, which is the only "how late is it" this function can see --
#: `field_order` is handed `unlocked` and nothing else. 1 means always; 3 means from the day SW is
#: bought, around day 8, which is where the far pens actually appear.
#:
#: **THE GEOMETRY LANDS AND THE SEASON DOES NOT PAY FOR IT. SHIPPED OFF.**
#: Full write-up in `docs/geometry_placement_2026-08-08.md`; logs `data/logs/geometry_ab*.log`.
#:
#: At `1` it does exactly what it claims, seed 11: pen distance sum 52 -> 30 against the tape's 45,
#: the three far pens gone, placement waste 1,644 -> 985 depot-steps, work turns 2,680 -> 2,895, idle
#: 1,883 -> 1,423, bank $104,257 -> $117,844. And on the six NON-ARTIFACT seats of the 6-seed x 2-seat
#: ladder it is **-$33,133, better on 2 of 6, and it costs a win** (seed 23 seat 0, WIN -> loss).
#:
#: At `3` the money is a null and the win rate is the only thing that moves:
#:
#:     seeds 11,7,23,3,42,101      sum +20,526   better  9/12   valid wins 2/6 -> 2/6
#:     seeds 19,22,33,44,55,77     sum -11,111   better  6/12   valid wins 1/6 -> 3/6   HELD OUT
#:     pooled, 24 seats            sum  +9,415   better 15/24   valid wins 3/12 -> 5/12
#:
#: +$392 a seat is inside the ~15% seed noise, and the money sign REVERSED on the fresh draw, which is
#: the winner's curse this repo has already been bitten by. The win rate gained 2 valid seats and lost
#: none (McNemar exact p = 0.25), and it gained them only on the held-out half. Two unconfirmed halves
#: pointing opposite ways is a null, not a win, so nothing changes on the strength of it.
#:
#: **Why the always-on arm loses, which is the reusable part.** The near ground it frees was not the
#: binding constraint: measured over the season we already walked 3,460 turns against the tape's 4,025
#: and idled 1,426 against its 999, so the crew was never turn-starved by distance. What the sort DOES
#: bind is the herd -- seed 11 goes 17 animals to 18 and gains $7,895, seed 23 goes 17 to 16 and loses
#: $23,369, seed 101 goes 16 to 15 and loses $14,779, with land purchases byte-identical on every seed.
#: The season's money rides on one or two animals, and shuffling the ground moves that in both
#: directions for reasons that have nothing to do with walking.
#:
#: Note also that the pen half of this was already half-shipped: `schedule_agent.PEN_NEAREST_DEPOT_FROM_DAY`
#: is 11, so from day 11 pens already take nearest ground. The marginal effect of `1` on PENS is
#: therefore days 0-10 only -- where our layout already matches the tape's distance exactly, 22 vs 22
#: on day 0 -- and most of what it actually moves is CROPS, which are the low-visit class the
#: visit-weighting says should NOT get the near ground. That is the mechanism, and it is why `3` (which
#: starts around day 8) is the better-behaved of the two.
#: **ON, 2026-08-09, Alex's call.** Everything above is a MONEY argument, and money is not the
#: criterion -- the criterion is d0-d6 matching Seb's tape op-for-op. A season bank cannot rank two
#: planners against that, and the A/B was additionally run with the idle top-up and crew-change
#: replan still in place, which is the mechanism that was destroying delivery legs. So the null it
#: reported is a null about a planner that no longer exists.
DEPOT_RING_FIRST = 1


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
    if DEPOT_RING_FIRST is not None and len(unlocked) >= DEPOT_RING_FIRST:
        # Only the shed cells we OWN are depots -- a locked one is not reachable, and measuring
        # against it would rank the whole of NE as near before NE is bought. Same rule as
        # `plan_routes`, for the same reason. Stable, so the sweep breaks every tie.
        depots = [c for c in SHED if R.quadrant_of(c[0], c[1]) in unlocked] or [R.SPAWN]
        out.sort(key=lambda t: min(dist(t, c) for c in depots))
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


#: Water a tile that is NOT at risk, so the field stops coming due all on one day.
#:
#: The alternate-day rule (`consecutive_unwatered >= 1`) is correct per tile and synchronises the
#: field in aggregate: everything watered on d11 falls due together on d13. Measured on seed 11,
#: tiles on the brink at dawn against tiles rescued -- d12 has 15 due and 136 idle turns and still
#: loses 2; d15 has 34 due, 2 idle turns in the entire day, and loses 6. The trough has turns going
#: spare while the spike cannot cover its backlog.
#:
#: **Priced at a fraction of the survival water, never level with it.** A tile that weeds tonight is
#: an asset lost outright; a top-up is a convenience. At equal price a spike day spends its turns on
#: tiles that were never at risk.
#: **MEASURED AND OFF.** It does what it was built for and loses the season doing it. Seed 11,
#: tape 91422988, final bank: baseline $79,905 with 16 tiles starved; with this on, $63,645 with 5
#: starved. Stacked on the crew planner for d0-d3 it is $91,943 -> $62,284. Brink misses over
#: d0-d20 fall 13 -> 4 and the board carries zero dry tiles from d27 -- the rule is not broken, the
#: tiles are simply worth less than the turns it takes to save them.
#:
#: The argument for switching it on was that the earlier `>= 0` widening had been rejected for
#: reasons that had expired (wrong tape, measured only over d0-d7 where 17 tiles fit in a day). That
#: argument was wrong on its own terms: the trough day's idle turns are not free, because spending
#: them puts the hand somewhere else when the next spike lands.
#: **Water half the SAFE tiles each day, alternating, instead of none of them.**
#:
#: A tile watered yesterday cannot weed tonight, so the survival rule skips it entirely -- which is
#: why d3 emitted 7 waters against the leader's 14. See the note at the emission.
WATER_ROTATION = True

TOP_UP_SAFE_TILES = False
#: Not before day 7. Seventeen tiles fit inside one day with room to spare, Seb waters alternate days
#: there and takes zero weeds doing it, and d0-d6 is matched to the tape op for op.
TOP_UP_FROM_DAY = 7
TOP_UP_DISCOUNT = 8.0


def crop_ops(cell, day, have_fertilizer, fertilizer_price=None, tile=None):
    """`[(op, item, prize)]` worth doing on a planted tile today, in the order they must be emitted.

    FERTILIZE precedes WATER because WATER reads `fertilized_until_day` at the moment it runs.

    `fertilizer_price` is what one unit would fetch RIGHT NOW, and it is the opportunity cost of
    putting that unit in the ground instead of on the market. Defaulting to `BASE_PRICE` keeps every
    caller that has not been threaded behaving exactly as before -- see
    `test_the_default_is_the_old_constant`.

    **Why a live price and not the constant.** Nothing in the game eats fertilizer -- no shop lists
    it and the town centre is built as `[p for p in PRODUCTS if p != "FERTILIZER"]` -- so its book
    only ratchets up and its price only falls. Across the 85 recorded games carrying a market trace
    it is at $50 by day 17 and $20 by day 26, in essentially every one. Valuing it at a flat $100
    means refusing to fertilize a tile on the grounds that the unit is worth five times what anyone
    will actually pay for it, and refusing hardest at the end of the season when the tile has least
    time to earn any other way.
    """
    info = CROP[cell["crop"]]
    price = BASE_PRICE[cell["crop"]]
    fert_price = BASE_PRICE["FERTILIZER"] if fertilizer_price is None else float(fertilizer_price)
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
            # **Clipped to the season, not just to the window.** A tile whose window runs past the
            # last day is credited with waters nobody will ever give it, and the FERTILIZER it
            # spends is a PRODUCT that could have been sold instead. `_crop_remaining` and the
            # window pricer below already clip this way; these two gates did not.
            waters_left = min(info["max_day"] - age + 1, R.SEASON_DAYS - day)
            if (not fertilized and have_fertilizer and waters_left < room
                    and day < FERTILIZE_UNTIL_DAY
                    and cell.get("fertilized_until_day", -1) < day):
                gain = min(room, waters_left * 2) - min(room, waters_left)
                if gain * price > fert_price:
                    out.append(("FERTILIZE", "FERTILIZER", gain * price))
                    fertilized = True
            if not cell["watered_today"]:
                # **A tile can be inside its window AND on the brink of weeding on the same day, and
                # this branch used to price only the first of those.** An in-window water is worth the
                # unit it adds; a water on a tile at `consecutive_unwatered >= 1` is worth the whole
                # tile, because tomorrow there is no tile. Wheat sown on d26 hits both on d28 -- age
                # reaches `first` exactly as the second dry night falls -- and at one unit (~$25) it
                # lost every auction: 3 weeds on d28, 4 on d29, and seven of d29's turns spent
                # DIGging them. Held to d26+ purely for scope; the mispricing is not late-specific.
                unit = price * (2 if fertilized else 1)
                if (day >= min(LATE_TRUNCATED_PLANT_DAY,
                               BRINK_WATER_IS_WORTH_THE_TILE_FROM_DAY)
                        and cell["consecutive_unwatered"] >= 1):
                    unit = max(unit, _crop_remaining(cell, day))
                out.append(("WATER", None, unit))
                # **The LAST water is not worth one unit, it is worth the tile.** See
                # `FILLING_WATER`. It takes `room` to 0, which is exactly the condition
                # `_one_shot_is_finished` waits for, so the HARVEST becomes legal on the next turn
                # with the unit already standing here. Offering it on the same node prices the visit
                # at what it actually banks and lets `_live_ops` emit WATER then HARVEST back to
                # back, which is what the crew already does -- just seven hours too late.
                # **TRIED and MEASURED WORSE: price this at `held`, not `held + gain`.** It is the
                # strictly correct marginal -- the WATER above already carries the unit it adds, so
                # the full tile bills that unit twice, $1,750 for a stop that banks $1,500 -- and it
                # is what every other HARVEST is priced at. On seed 11 day 10 it gave back the whole
                # gain: money -1,548 -> -3,082 and `sh:melon` 0 -> +6, i.e. baseline. The $250 is
                # what breaks a TIE: an immature melon's survival water is `_crop_remaining`, also
                # exactly $1,500, and at $1,500 each the filling water no longer outranks it.
                # `test_a_filling_water_outranks_survival_water_on_a_tile_that_cannot_yield_yet`
                # goes red on precisely that. Certain money today and contingent value tomorrow are
                # not the same $1,500, and this node is the only place the difference is expressible.
                gain = 2 if fertilized else 1
                if FILLING_WATER and age >= info["first"] and gain >= room:
                    out.append(("HARVEST", None, min(info["max_yield"], held + gain) * price))
        elif (not cell["watered_today"] and cell["consecutive_unwatered"] >= 1
              and not upkeep_buys_nothing(day)):
            # The last-day gate: this water buys the tile surviving TONIGHT's rollover, and after
            # d29's rollover there is no tile to have saved. Same switch as FEED/CARE.
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
        elif (WATER_ROTATION and tile is not None and not cell["watered_today"]
              and (tile[0] + tile[1] + day) % 2 == 0
              and not upkeep_buys_nothing(day)):
            # Same last-day gate as the survival water above: the alternation only exists to keep
            # `consecutive_unwatered` below 2 across days, and there is no next day.
            # **Half the safe tiles, alternating -- which is what the leader actually does.**
            #
            # Measured off カワシギ's own d3, seed 11: his board at dawn is 19 tiles, every one at
            # `consecutive_unwatered = 0`, all planted d0 -- 7 WHEAT and 12 MELON -- and he emits
            # **14** waters. We emitted 7, exactly the wheat, because wheat at age 3 is inside
            # `in_window` ((4+1)//2 = 2 <= 3 <= 4) and melon at age 3 is far from its own 6..12.
            # His extra seven are melon: he is not watering all twelve, he waters about half and
            # takes the rest tomorrow.
            #
            # Parity on `(x + y + day)` is that alternation with no state to carry. It flips every
            # day, so a tile skipped today is offered tomorrow and `consecutive_unwatered` can never
            # reach the 2 that weeds it (`reference/kaggriculture.py:770`).
            #
            # **Not `TOP_UP_SAFE_TILES`, which is the same slot and the wrong shape.** That flag
            # offers EVERY safe tile from a fixed day, which put d3 at 19 against his 14 and d5 at
            # 20 against his 13 -- overshooting the tape rather than matching it.
            out.append(("WATER", None, _crop_remaining(cell, day) / TOP_UP_DISCOUNT))
    else:
        # An ongoing crop produces at dawn regardless of water. Water is survival, plus the
        # fertilizer bonus on a production day. Watering it on any other day is pure walk.
        # `day + 1 < R.SEASON_DAYS` because "tomorrow" on the last day is a day that never runs, and
        # both the fertilizer bonus and the water below are bought purely for that production.
        produces_tomorrow = (day + 1 < R.SEASON_DAYS
                             and age + 1 >= info["first"]
                             and (age + 1 - info["first"]) % info["interval"] == 0)
        # **Decided BEFORE the water is priced, and appended first, exactly as the one-shot branch
        # above does it.** The water clause below reads `fertilized`, so testing it first meant a
        # tile the plan had already decided to fertilize was priced as though it had not been: the
        # stop shipped as `('FERTILIZE',)` and `_live_ops`, re-reading the cell after the FERTILIZE
        # had run, found the water it unlocks and spent a turn nobody budgeted. On seed 11 day 16
        # that was three turns off u9 and three off u13, and the tiles their tours could no longer
        # reach -- (8,0) and (9,0) -- weeded. Order in `out` matters for the same reason it does
        # above: WATER reads `fertilized_until_day` at the moment it runs.
        if (produces_tomorrow and not fertilized and have_fertilizer and room > 1
                and day < FERTILIZE_UNTIL_DAY
                and price > fert_price):
            out.append(("FERTILIZE", "FERTILIZER", price))
            fertilized = True
        if not cell["watered_today"]:
            if cell["consecutive_unwatered"] >= 1:
                out.append(("WATER", None, _crop_remaining(cell, day)))
            elif produces_tomorrow and room > 0 and (fertilized or day >= FERTILIZE_UNTIL_DAY):
                # **Past `FERTILIZE_UNTIL_DAY` this branch is the ONLY water a safe tile can be
                # offered.** A tile watered yesterday has `consecutive_unwatered == 0`, so the
                # survival branch above never fires for it, and `fertilized` is False by construction
                # once fertilizing stops. Measured: twelve wheat planted d26 took their planting-day
                # water and then nothing -- 3 weeds by d28, 4 by d29, and seven of d29's turns spent
                # DIGging our own dead tiles.
                out.append(("WATER", None, price))
            elif TOP_UP_SAFE_TILES and day >= TOP_UP_FROM_DAY:
                out.append(("WATER", None, _crop_remaining(cell, day) / TOP_UP_DISCOUNT))

    if held > 0 and age >= info["first"] and (info["ongoing"]
                                              or _one_shot_is_finished(info, age, room, day)):
        prize = held * price
        # **Its last safe day, and there is no second chance.** See
        # `HARVEST_IS_CRITICAL_ON_ITS_LAST_SAFE_DAY`. `age >= max_day` is the day the harvest
        # becomes legal; `age >= max_day + 1` is the day `_decay_plants` starts eating it, one unit
        # every two steps from h00. So this fires on exactly the one day the tile can be taken
        # whole, and on any day after it while something is still left to save.
        last_free = False
        if (last_free
                or (HARVEST_IS_CRITICAL_ON_ITS_LAST_SAFE_DAY
                    and day is not None and day >= HARVEST_CRITICAL_FROM_DAY
                    and age >= _last_safe_age(info))):
            prize += CRITICAL
        out.append(("HARVEST", None, prize))
    # **A finished ongoing crop is ground, not a crop.** A one-shot HARVEST clears its tile
    # (`kaggriculture.py:454-455`); an ongoing one only collects, so a spent strawberry sits on its
    # square for the rest of the season while the schedule still wants somewhere to plant.
    #
    # The signal is exact and needs no estimate. `_new_crop` starts an ongoing crop at
    # `max_lifespan_step = -1` (`:211`) and `_daily_refresh_crops` sets it once, to
    # `(next_day + 1) * turns_per_day`, at the moment `production_count == cd["max_yield"]` (`:789`).
    # From that step the tile only rots (`:746-752`). So `>= 0` means "will never produce again".
    #
    # Emitted AFTER the harvest above, so a spent tile still holding units is stripped before it is
    # demolished -- `_live_ops` walks the ops in order.
    #
    # Priced at the planting it unblocks, exactly as the WEED branch in `build_nodes` prices its own
    # DIG, and halved for the same reason: clearing ground is worth what goes into it, and only if
    # something does. Victor digs 30 spent strawberries from d19 on and replants behind them; we hold
    # the dead tiles and `plant` falls to 3/16 by d23 while `sell` collapses.
    if (DIG_A_SPENT_ONGOING_CROP and info["ongoing"]
            and int(cell.get("max_lifespan_step", -1)) >= 0):
        best = max((plant_prize(c, day) for c in R.CROPS), default=0)
        if best > 0:
            out.append(("DIG", None, best * 0.5))
    return out


#: The first day no tile is offered a FERTILIZE. The fertilizer it saves is a PRODUCT that sells,
#: and the turn it saves goes to a water or a planting -- the two rows the late season is short of.
#: Ours runs 9/2, 11/0, 5/0 against the tape on d26-d28, i.e. 25 turns spent on a row the tape has
#: essentially stopped playing. **TRIED at 23 and measured -$2,547**, which is why this sits at 26:
#: d23-d25 fertilize still fills tiles that have a window left to fill.
LATE_SEASON_PAIR = True

FERTILIZE_UNTIL_DAY = 26 if LATE_SEASON_PAIR else 99

#: Whether a one-shot whose growing window cannot close before the season ends is offered for
#: HARVEST anyway, taking a partial yield. Only reachable from d26. See the body.
HARVEST_A_TRUNCATED_ONE_SHOT = LATE_SEASON_PAIR

#: The first day a one-shot may be planted with a window the season cannot finish. Below it
#: `plant_prize` keeps returning 0, which is right: a wheat sown on d20 has time for a full window
#: and truncating it would only waste the ground.
LATE_TRUNCATED_PLANT_DAY = 26 if LATE_SEASON_PAIR else 99

#: **From which day a tile that is PRODUCING and one dry night from weeding is priced at the whole
#: tile**, rather than at the single unit the water adds.
#:
#: `crop_ops` has two branches for a dry tile. One outside its yield window gets a proper survival
#: price -- the water buys the tile surviving tonight. One INSIDE its window took the in-window
#: price of one unit, and the survival price was applied only behind `LATE_TRUNCATED_PLANT_DAY`,
#: which is 26. The comment on that branch says the gate was arbitrary: "Held to d26+ purely for
#: scope; the mispricing is not late-specific."
#:
#: It is not. Measured on live ladder games 2026-08-16, tracked tile by tile on our own farm:
#:
#:     (8,4) STRAWBERRY  died d9   last watered d6   -- d7 and d8 both missed
#:     (9,1) WHEAT       died d11  last watered d8   -- d9 and d10 missed
#:     (9,2) STRAWBERRY  died d11  last watered d8
#:
#: and the same coordinates die across independent games with different seeds and opponents --
#: (2,2) and (3,2) wheat on d9 in four and three games. At d8 dusk eight tiles sat at
#: `consecutive_unwatered >= 1`, one night from death and visible in the observation, while we
#: watered sixteen others. A producing wheat tile was being offered at $25.
#:
#: **This is NOT `TOP_UP_SAFE_TILES`.** That rule waters tiles which are SAFE, and it is measured
#: and off -- $79,905 -> $63,645, because a spike day then spends its turns on tiles never at risk.
#: This one only ever fires at `consecutive_unwatered >= 1`, which is a tile that weeds tonight;
#: `test_a_tile_watered_yesterday_is_not_given_the_survival_price` pins the difference.
#: **MEASURED A NULL 2026-08-15 AND OFF.** Byte-identical on seeds 3/7/11: same weeds,
#: same bank. `crop_ops` IS on the path (1,364 calls on d8, 131 of them brink tiles) but
#: `cover` chooses STOPS by rules on the board, not by price -- 'There is no price table
#: in here, and that is the point.' The price only decides what to do at a stop already
#: being visited. The lever is `cover.AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP`.
BRINK_WATER_IS_WORTH_THE_TILE_FROM_DAY = 99


def _last_safe_age(info):
    """The age at which a crop's produce must be off the tile, for BOTH crop shapes.

    `_decay_plants` (`kaggriculture.py:752`) eats one unit every two steps once `step` passes
    `max_lifespan_step`, and turns the tile to WEED at zero. That deadline is set in two different
    places, and reading only the one-shot half is what let four strawberry tiles bleed out on
    seed 11:

    one-shot  `:224`      `(planted_day + max_yield_day + 1) * 24`, fixed at planting.
                          Last safe age == `max_day`.

    ongoing   `:224`      planted with `-1`, which `_decay_plants` skips -- it never decays while
                          it is still producing.
              `:801-802`  on the day its LAST production lands, and only then:
                              if production_count == cd["max_yield"]:
                                  tile["max_lifespan_step"] = (next_day + 1) * turns_per_day
                          So the clock starts at the final production. `production_count` is
                          `days_since_first // interval + 1`, so it reaches `max_yield` at
                          `first + interval * (max_yield - 1)`.

    Water does not extend either one.
    """
    if not info["ongoing"]:
        return info["max_day"]
    return info["first"] + info["interval"] * (info["max_yield"] - 1)


def _one_shot_is_finished(info, age, room, day=None):
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
    if (HARVEST_A_TRUNCATED_ONE_SHOT and day is not None
            and day + (info["max_day"] - age) > R.SEASON_DAYS - 1):
        # **The window cannot close before the season does, so waiting forfeits the tile.** This is
        # the second half of `docs/the_late_season_is_one_defect_in_two_halves_2026-08-12.md`, and it
        # only ever fires from d26 -- at d25 a wheat still reaches `max_day` on d29, the last day.
        # Measured ALONE on the 12-seed ladder it cost -$92, because there was nothing extra standing
        # to collect; it is paired here with the `plant_prize` change that puts the crop in the ground.
        # Victor takes 26 wheat on d29 at age 2-3, `held 4 / max 6` (`91854176.json`).
        return True
    return age >= info["max_day"] or room <= 0


def produces_tonight(cell, day):
    """Whether tonight's refresh adds `yield_units` to this pen.

    The env's own arithmetic, copied rather than approximated (`kaggriculture.py:809-810`): the
    refresh runs for `next_day = day + 1`, so the offset is measured against TOMORROW. Reading it
    off `day` instead shifts every pen by one night, which no season total can show.
    """
    a = ANIMALS[cell["animal"]]
    since = (day + 1) - int(cell.get("placed_day", 0)) - a["first_yield_day"]
    if since < 0:
        return False
    return a["interval"] <= 0 or since % a["interval"] == 0


#: Feeds still available to pens that arrived TODAY. Set per turn by the agent from the schedule's
#: `feeds` row; see `will_be_fed`. Module-level so the predicate stays a pure function of the cell.
ARRIVAL_FEED_REMAINING = 0

#: First day the cadence applies. **The tape feeds everything, every day, until d5.** Its feed row
#: over d0-d4 is 4, 5, 5, 6, 7 against 8 pens -- all of them, allowing for the ones placed that day
#: -- and the cycling starts at d5 (4 of 7) and is unmistakable by d7 (3 of 17).
#:
#: Applied from d0 it drags days that have nothing to do with feeding: a rolling half-herd is hungry
#: every morning, every one of those feeds prices as CRITICAL, and the routes reorder around them.
#: d2 `sell 4/5 -> 2/5` and d3 `water 14/14 -> 12/14` are rows that are exact in the tape and were
#: exact in ours.
FEED_CADENCE_FROM_DAY = 7


def will_be_fed(cell, day):
    """Whether `animal_ops` would offer this pen a FEED today. The market block sizes its wheat
    purchases off this, so it has to be the same rule and not a second copy of it."""
    # **The last day, before everything else.** Dropping FEED from `animal_ops` alone measured
    # d29 `feed 14/0 -> 14/0` unchanged: the route is a visit ORDER, the executor re-derives work
    # at stops and crossings, and `underfoot()` (`schedule_agent:2458`) feeds any pen this
    # predicate says yes to. One predicate, so the last day says no exactly once.
    if upkeep_buys_nothing(day):
        return False
    # **An animal placed TODAY cannot be fed into producing anything, and is not at risk.** FEED
    # does exactly two things (`_daily_refresh_animals`, kaggriculture.py:795-820): it resets
    # `consecutive_unfed`, which is already 0 on the turn the animal is placed, and on a production
    # night it releases `pending_care_bonus` -- and a pen placed today is `first_yield_day` away
    # from its first production night (8 for a COW, 6 for a SHEEP). So the ration buys nothing at
    # all, and the animal is removed only at `consecutive_unfed >= 2` (`:804`), which is two days
    # away. It is fed tomorrow with nothing lost.
    #
    # d0 on the kawashigi tape is exactly this. Both sides put the SAME net wheat in the shed --
    # he buys 8 and sells 3, we buy 5 and sell none, +5 each, his `BUY 9 / SELL 3` being a wash --
    # and the whole difference into d1 is what we ate:
    #
    #             buys filled   sells   feeds   into d1 shed
    #     him          8          -3      -2          3
    #     us           5           0      -4          1
    #
    # Those two rations are the reason d1 opens on one wheat, makes three separate shed trips with
    # a single unit, and leaves (3,4) unfed while idling h22-h23 one step away.
    if int(cell.get("placed_day", -1)) == int(day):
        # **How many of today's arrivals get fed is the TAPE's number, not a rule of ours.**
        # `ARRIVAL_FEED_REMAINING` is set once per turn by the agent from the day's `feeds` row
        # minus the pens that were already standing, and counted down off the board (`fed_today` on
        # a pen whose `placed_day` is today), so it needs no state of its own and self-corrects if a
        # feed is emitted by a path this predicate never saw.
        #
        # It is a budget because his own numbers are a budget: d0 places four and feeds two, d3
        # places one and feeds none of it, d5 places one and feeds it, d7 places three and feeds two.
        # No predicate on the animal reproduces that -- "feed everything" and "feed only what is
        # producing" were both measured, and both lose.
        return ARRIVAL_FEED_REMAINING > 0
    return True
    if cell.get("consecutive_unfed", 0) >= 1:
        return True
    a = ANIMALS[cell["animal"]]
    return ((day + 1) - int(cell.get("placed_day", 0)) - a["first_yield_day"]) >= 0


#: **No FEED and no CARE on the last day. Both pay out at a rollover that scores nothing.**
#:
#: `_daily_refresh_animals` runs inside `_end_of_day`, so on d29 it fires at the rollover into day
#: **30**. The base unit and the care bonus land on the pen and no turn ever exists to harvest them.
#: The other thing a FEED buys is survival, and that is worthless too: the score is banked money, so
#: an animal that escapes after the final turn costs nothing.
#:
#: Measured on the kawashigi grid, last three days, ours/tape:
#:
#:     row              d27       d28       d29
#:     feed           14/14     14/10     14/0
#:     care           14/12     14/9      14/0
#:     harvest        31/35     29/32     26/19
#:     drop            0/0       2/0       2/9
#:
#: The tape does ZERO upkeep on its last day and spends it harvesting and walking produce in -- nine
#: DROPs to our two. Our 28 upkeep turns are most of the ~36 needed to send six loaded hands to the
#: shed, and the season currently ends with 51 sellable units stranded in hands, about $1,192.
#:
#: HARVEST and COLLECT_FERTILIZER are deliberately NOT dropped: milk, wool and fertilizer already on
#: the pen are real produce that can still be sold today if it reaches the shed.
#:
#: **Parked 2026-08-15, re-opened the same day once the landmine was defused.** The first attempt
#: measured harvest 396 -> 389, sell 1489 -> 1474, because `cover._apply_precomputed` matched a stop
#: by the exact `(tile, ops)` tuple: a pen whose job was `[FEED, CARE, COLLECT_FERTILIZER, HARVEST]`
#: became `[COLLECT_FERTILIZER, HARVEST]`, the key stopped matching the solved plan, and the stop
#: dropped out of the route rather than getting cheaper. `cover.MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE`
#: now seats the reduced stop on the unit the solve chose, which is what this flag was waiting for.
NO_UPKEEP_ON_THE_LAST_DAY = True


def upkeep_buys_nothing(day):
    """True on the last day, when FEED and CARE pay out at a rollover the season never reaches.

    The one gate for every upkeep path: `animal_ops` (the plan), `will_be_fed` (the executor's
    underfoot FEED and the wheat-purchase sizing), and `underfoot()`'s CARE branch, which cannot
    ask `animal_ops` and needs the same answer.
    """
    return NO_UPKEEP_ON_THE_LAST_DAY and day is not None and day >= R.SEASON_DAYS - 1


def animal_ops(cell, day, have_wheat):
    """`[(op, item, prize)]` for a stocked pen. FEED is mandatory the day after a missed feed."""
    a = ANIMALS[cell["animal"]]
    price = BASE_PRICE[a["product"]]
    out = []
    fed = cell["fed_today"]
    if upkeep_buys_nothing(day):
        # Collect what is already there; buy nothing that pays out tomorrow.
        if cell.get("fertilizer_available"):
            out.append(("COLLECT_FERTILIZER", None, BASE_PRICE["FERTILIZER"]))
        if cell.get("yield_units", 0) > 0:
            out.append(("HARVEST", None, cell["yield_units"] * price))
        return out
    if not fed and have_wheat:
        hungry = cell.get("consecutive_unfed", 0) >= 1
        # **A feed buys two things, and on most nights it buys neither.** From
        # `_daily_refresh_animals` (`kaggriculture.py:795-820`):
        #
        #     if days_since_first >= 0 and days_since_first % a["interval"] == 0:
        #         base = 1
        #         bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
        #         tile["yield_units"] = min(a["max_held"], tile["yield_units"] + base + bonus)
        #
        # `base = 1` lands whether or not the animal was fed. Production never reads `fed_today`.
        # So a FEED resets `consecutive_unfed`, and on a production night it releases
        # `pending_care_bonus` -- and on any other night it buys nothing at all.
        #
        # The comment that stood here said the opposite -- "skipping it forfeits the day's
        # production AND the care bonus" -- and that false half is what made every feed MANDATORY.
        # The +0.452 correlation with money is real and is not evidence for feeding daily; it is
        # evidence for keeping animals alive, which the hungry branch below already does.
        #
        # The tape feeds on a cycle and uses the whole of the one-day slack: seventeen pens on d7
        # and THREE feeds, four feeds on d5 against seven pens. The intervals agree -- a COW
        # produces every second night and a SHEEP every third -- so a daily feed on a cow is wasted
        # on at least half the nights by construction.
        # **Producing, not "tonight".** The first cut of this asked whether the pen yields TONIGHT
        # and fed only then. It measured d16 money $9,975 -> $4,814, and the reason is the care
        # chain: `CARE` is offered only on a pen that is fed (below), and `pending_care_bonus` is
        # banked only on a night that is BOTH fed and cared. Feed nightly and a production night
        # pays `base 1 + bonus 1`; feed only on the payout night and it pays 1. Same turns per unit
        # of product, half the product.
        #
        # So the waste is not the daily feed. It is the daily feed of an animal that has not STARTED
        # producing: a COW placed on d0 first yields on d8 (`first_yield_day 8`), so eight days of
        # feeding it buy nothing but its survival, which one feed in two also buys.
        #
        # That is what the tape does, and it is why d7 looks the way it does -- he goes from 7 pens
        # to 17 that day and feeds THREE. The twelve he has just placed are years from a yield in
        # game terms; the three that are producing get fed. By d9 he is feeding 11 of 17 and by d10,
        # 12 of 18, as the rest come on line.
        if will_be_fed(cell, day):
            # A hungry pen is one missed day from the animal escaping outright
            # (`reference/kaggriculture.py:804`), which is irreversible: the structure survives, the
            # animal does not, and nothing on the board buys it back the same day. See `CRITICAL`.
            floor = CRITICAL if (hungry and FEED_IS_CRITICAL_WHEN_AT_RISK) else MANDATORY
            prize = floor + price + ((a["cost"] + _animal_remaining(cell, day)) if hungry else 0)
            out.append(("FEED", "WHEAT", prize))
            fed = True
    if not cell["cared_today"] and fed:
        # `pending_care_bonus` is only consumed on a day the animal is ALSO fed, so an uncared or
        # unfed pen banks nothing. One care = one extra unit of product on the next production day.
        out.append(("CARE", None, price))
    if cell.get("fertilizer_available"):
        out.append(("COLLECT_FERTILIZER", None, BASE_PRICE["FERTILIZER"]))
    if cell.get("yield_units", 0) > 0:
        prize = cell["yield_units"] * price
        out.append(("HARVEST", None, prize))
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
        if days_left < info["max_day"] and day < LATE_TRUNCATED_PLANT_DAY:
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

_DEPOT_TILES = frozenset(tuple(t) for t in R.shed_access_tiles())


class Node:
    """One tile, every op worth doing there today, and what must be drawn at the depot first."""

    __slots__ = ("tile", "ops", "prize", "service", "needs", "mandatory", "critical")

    def __init__(self, tile, ops):
        self.tile = tile
        self.ops = [(op, item) for op, item, _p in ops]
        self.prize = sum(p for _o, _i, p in ops)
        self.service = len(ops) + (DEPOT_NODE_EXTRA_SERVICE
                                   if tuple(tile) in _DEPOT_TILES else 0)
        # **A BUILD draws nothing.** `BUILD_PASTURE`/`BUILD_COOP` take no item out of the shed
        # (`kaggriculture.py:486-490`); they cost money and a turn. `DRAWN` carries "BUILD" because
        # its supply check downstream wants the pin's animal NAME, and `BUILD_THEN_PLACE` writes that
        # name onto the BUILD op as well as the PLACE that follows it -- so counting both asked the
        # shed for two animals per pen.
        #
        # Measured on the Victor grid, seed 11, d0: u0 drew `COW x2 SHEEP x2` for two pens and u3
        # drew `SHEEP x6` for three. Ten animals for five pens on a day whose row buys five
        # (`COW 1, SHEEP 4`). The shed ran dry before the last pen, its PLACE found nothing in hand,
        # and the day read `place 4/5` against `build_pasture 5/5` -- five pens standing and four
        # filled -- taking `feed 4/5` and `care 4/5` with it, and every later day inheriting a herd
        # one head light.
        #
        # `router.py`'s own supply check already records the trap ("PLACE only, never BUILD. BUILD is
        # in DRAWN and carries the animal name too"); `needs` never got the same guard. Fixed here
        # rather than in `DRAWN` because that tuple is what the supply check reads.
        self.needs = collections.Counter(i for o, i, _p in ops
                                         if i and o in DRAWN and o != "BUILD")
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
        # **Only if the FEED is not already on this node.** `needs` is built from every DRAWN op,
        # and `DRAWN` contains FEED whose item IS "WHEAT" -- so once `SERVE_THE_ANIMAL_IT_PLACES`
        # put the FEED on the placement node, this added a second unit for a feed that eats one.
        # A hand drew two wheat per pen, and PICKUP is one item per TURN against a shed the day's
        # row fills a unit at a time, so it sat at the shed hoovering up the drip.
        #
        # Traced on day 0, seed 11: u0 has two placements, draws WHEAT at h2, h3, h4 and h5, feeds
        # twice and carries two spare to dusk -- while u4, standing beside the cow it placed at
        # (4,3), reads an empty shed at h5 and loses that feed for the day. `feed 3/4`.
        if PLACE_DRAWS_FEED and not any(o == "FEED" for o, _i, _p in ops):
            for o, _i, _p in ops:
                if o == "PLACE":
                    self.needs["WHEAT"] += 1
        self.mandatory = any(p >= MANDATORY for _o, _i, p in ops)
        self.critical = any(p >= CRITICAL for _o, _i, p in ops)

    def __repr__(self):
        return f"Node{self.tile}{[o for o, _ in self.ops]}@${self.prize:.0f}/{self.service}t"


#: **Serve the animal on the turn it is placed, instead of discovering it a turn later.**
#: A PLACE node also carries the FEED and CARE that animal needs today. Ships ON: the alternative
#: is that the ops only come into existence once the animal is standing on the tile, which is a
#: board the dawn plan never sees, and the day is fully deterministic so there is nothing to
#: discover. See the note at the PLACE branch for the d0 measurement.
SERVE_THE_ANIMAL_IT_PLACES = True

#: Whether a pinned BUILD carries the PLACE (and its FEED and CARE) for the animal the pin was made
#: for, so the pen is built and filled by one chain in one plan. OFF restores the old behaviour: the
#: placement cannot be seen until a later turn finds the pen already standing, which needs a replan.
BUILD_THEN_PLACE = True

#: Whether a pinned PLANT carries the WATER (and FERTILIZE) the seed will need the moment it is in
#: the ground. Same defect and same shape as `BUILD_THEN_PLACE`: without it the dawn plan cannot see
#: the 17 waters day 0 creates for itself, and only a replan finds them.
PLANT_THEN_WATER = True

#: Whether an ongoing crop that has produced its lifetime maximum is offered a DIG, so the
#: ground it is sitting on can be replanted. See the note in `crop_ops`.
DIG_A_SPENT_ONGOING_CROP = True

#: Whether a stop that HARVESTS a one-shot crop also carries the PLANT its cleared tile can take.
#: Third instance of the same shape as `BUILD_THEN_PLACE` and `PLANT_THEN_WATER`, and the same shape
#: again as `_land_this_turn`: the board the plan reasons about must be the board the day will have.
#:
#: HARVEST on a one-shot crop sets the cell to `None` (`kaggriculture.py:454-455`); on an ongoing
#: crop, a PASTURE or a COOP it does not, so only the first kind makes room. `_refresh_pins` pins
#: PLANTs onto ground that is empty at DAWN, which is why d8 planned exactly five: 7 free squares
#: less 2 builds, against a row of ten. The tape reaches ten by harvesting six during the day.
#:
#: Chained onto the node rather than pinned, deliberately. A pin would be worse than useless here:
#: `build_nodes` skips a pinned tile outright and `_live_ops` returns nothing on one, so pinning a
#: tile that still holds a crop would delete the very HARVEST that was going to clear it.
REPLANT_A_CLEARED_TILE = True


def _freshly_planted(crop, day):
    """The cell the environment will create for `crop` planted today (`kaggriculture.py:205-211`).

    Priced through `crop_ops` like any other tile, so the survival rule and the fertilizer decision
    stay in one place -- but only if the cell is the one the game actually makes. It was not: this
    carried `consecutive_unwatered: 0` where `:209` starts a fresh plant at **1** ("planting day
    counts as unwatered"), and `yield_units: 0` where `:210` gives a one-shot **1**. At 0 the
    survival-water clause cannot fire, so the planting-day water was free in the plan and cost a
    turn at the stop.
    """
    return {"kind": "PLANT", "crop": crop, "planted_day": day, "watered_today": False,
            "consecutive_unwatered": 1, "yield_units": 0 if CROP[crop]["ongoing"] else 1,
            "fertilized_until_day": -1}


def _best_replant_crop(replant, day, dated=None):
    """Which crop to put in ground the day has just cleared, or None if nothing can finish.

    **The budget's iteration order is not a ranking.** This was `next((c for c in replant if ...))`,
    which takes the first crop with any positive prize, so WHEAT won at d26 on dict order while
    pricing $50 against CARROT's $70 -- carrot's `max_yield_day` is 3 against wheat's 4, so from d26
    it is the only crop the season can still finish. The #1 player plants carrot, and nothing else,
    in exactly this window in all 16 of his downloaded games
    (`docs/kawashigi_one_board_2026-08-13.md`).

    Ties fall to the crop already earlier in the budget, so the pre-crossover behaviour is unchanged.

    **`dated` is what the schedule asked for TODAY, and it outranks the prize.** `replant` is
    cumulative, so on any late day it carries a large standing WHEAT figure beside whatever small
    request today's row actually made. Ranking the two against each other on price is a category
    error: the standing budget is never exhausted, so it wins every cleared tile forever. Wheat
    prices $75 against carrot's $70 from d21 to d25, which is exactly the window the leader plants
    carrot in, and the result on seed 11 was that none of the six scheduled carrots landed inside
    its window -- one on d26, five on d27, all of them past the day they could still yield. The arm
    read -$837 and that number is six wasted seeds, not carrot.

    He plants 1-2 carrot BESIDE 4-11 wheat on the same days in all 66 games. The dated ask is one
    tile; once it is met the rest of the day's cleared ground falls straight back to the standing
    budget below, which is that same shape.

    The window still governs: a dated crop whose `plant_prize` is 0 cannot finish and is refused
    exactly as an undated one is. Urgency reorders the eligible; it never adds to them.

    **Within `dated`, the SCARCEST request goes first, and that is the whole rule.** Today's row is
    not one crop -- d21 asks for `{WHEAT: 9, CARROT: 1}` -- so serving it in dict order just hands
    the tile back to wheat and changes nothing. It was byte-identical when written that way. The
    day's cleared ground is allocated greedily one tile at a time, so a nine-tile ask absorbs
    everything before a one-tile ask is ever considered, whatever the prize says. Ordering by
    ascending remaining count is what stops the small request being starved by the large one, and it
    self-limits: once carrot's single tile is spent, `dated[CARROT]` is 0 and wheat takes the rest of
    the day -- which is exactly the 1-2 carrot beside 4-11 wheat that all 66 games show.
    """
    for crop, qty in sorted((dated or {}).items(), key=lambda kv: kv[1]):
        if qty > 0 and replant.get(crop, 0) > 0 and plant_prize(crop, day) > 0:
            return crop
    best, best_prize = None, 0
    for crop, qty in replant.items():
        if qty <= 0:
            continue
        prize = plant_prize(crop, day)
        if prize > best_prize:
            best, best_prize = crop, prize
    return best


def build_nodes(tiles, day, shed, carried, unlocked, pinned, hour=0, pen_for=None,
                plantable=None, fertilizer_price=None, replant=None, dated=None):
    """Every tile worth visiting today, as routing nodes.

    `carried` is the union of what the crew already holds, so a task whose input is neither in the
    shed nor in a hand is never queued at all -- the deadlock that cost $45,623 was a unit holding
    the board's highest-priority job while standing on an empty shed.

    `replant` is the CUMULATIVE plants budget; `dated` is only what today's own row asked for, and
    it is consumed alongside it so a one-tile request is met once and not on every cleared tile.
    See `_best_replant_crop`.
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
                ops = crop_ops(cell, day, have_fert, fertilizer_price, tile=tile)
                # **A one-shot harvest is a demolition, so the tile it clears is plantable ground.**
                # See `REPLANT_A_CLEARED_TILE`. Budgeted from the day's remaining `plants` row, in
                # iteration order, exactly as `chain_left` budgets placements: the row is a count and
                # this must not invent one. Priced at `plant_prize` like every other PLANT, so the
                # combined stop outbids a bare harvest by what the seed is actually worth.
                if (REPLANT_A_CLEARED_TILE and replant
                        and (any(o == "HARVEST" for o, _i, _p in ops)
                             and not CROP[cell["crop"]]["ongoing"]
                             # **A DIG clears ground exactly as a one-shot HARVEST does**
                             # (`kaggriculture.py:477` vs `:454-455`), so the same replant is owed to
                             # it. Held to d26+ because the all-season version measured -$2,898 on
                             # its own -- with `plant_prize` 0 from d26 it planted only where the
                             # ground was already worth planting, and paid a turn for the privilege.
                             or (day >= LATE_TRUNCATED_PLANT_DAY
                                 and any(o == "DIG" for o, _i, _p in ops)))):
                    crop = _best_replant_crop(replant, day, dated)
                    if crop is not None:
                        replant[crop] -= 1
                        if dated and dated.get(crop, 0) > 0:
                            dated[crop] -= 1
                        ops = list(ops) + [("PLANT", crop, plant_prize(crop, day))]
                        if PLANT_THEN_WATER:
                            ops.extend(crop_ops(_freshly_planted(crop, day), day, have_fert))
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
                order = list(R.ANIMAL_NAMES)
                # **The pen remembers what it was built for.** See `PEN_KEEPS_ITS_ANIMAL`. This is
                # not the value rank rejected above: it ranks nothing, it reads back the assignment
                # `_refresh_pins` already made from the schedule's own ordered `places` row. A pen
                # with no reservation, or one the shed cannot fill, falls through to `order`
                # untouched -- a preference, never a lock, because a lock is what left a SHEEP idle
                # in the shed for three days.
                want = (pen_for or {}).get(tile) if PEN_KEEPS_ITS_ANIMAL else None
                if want in order and ANIMALS[want]["structure"] == kind:
                    order = [want] + [a for a in order if a != want]
                for a in order:
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
                        served = max(1.0, served)
                        # See `PLACE_IS_MANDATORY_FROM_DAY`. The refusal is a budget refusal, so the
                        # only thing that reaches it is being offered before the budget is spent.
                        if (PLACE_IS_MANDATORY_FROM_DAY is not None
                                and day >= PLACE_IS_MANDATORY_FROM_DAY):
                            served += MANDATORY
                        # **A placement is a PLACE, a FEED and a CARE, in one visit.**
                        # The day is deterministic: the schedule names the animals bought and
                        # placed, `_refresh_pins` has already chosen the ground for each, and an
                        # animal placed today needs feeding and caring today or it produces
                        # nothing and starts its `consecutive_unfed` count. Emitting only the
                        # PLACE meant the FEED and CARE could not exist until the animal was
                        # already standing there -- i.e. until a LATER turn, on a board the dawn
                        # plan had not seen. Nothing then went back for them: with no mid-day
                        # replan the pen is simply never revisited, and with one it was revisited
                        # by a unit that had dropped its delivery leg. Measured on d0 of Seb's
                        # tape: four animals placed at hours 4-10, `feed 1/4` and `care 1/4`, and
                        # the crew PASSing 8/8 from hour 20 with three animals unfed.
                        #
                        # Priced exactly as `animal_ops` prices them for a pen that already holds
                        # the animal, so a placement does not outbid a standing pen's own feed.
                        # `("FEED", "WHEAT", ...)` carries the item, so `materialise` plans the
                        # depot draw for the wheat as part of the same tour.
                        price = BASE_PRICE[ANIMALS[a]["product"]]
                        ops = [("PLACE", a, served)]
                        if SERVE_THE_ANIMAL_IT_PLACES and TPD - hour - 1 >= SERVICE_ROUND:
                            ops.append(("FEED", "WHEAT", MANDATORY + price))
                            ops.append(("CARE", None, price))
                        break
            elif kind == "WEED":
                # Worth exactly the planting it unblocks, so late in the season a weed is furniture.
                #
                # **And worth nothing at all on ground we are not going to plant.** A weed blocks
                # only the tile it sits on, so clearing one we will never sow is a turn spent to
                # tidy up. `DIG_ONLY_IF_REPLANTING` already asks whether the SEASON has plantings
                # left, but that is one global flag for the whole board -- it says yes while 25
                # squares are pinned for pasture and 15 more are outside any plan, and every weed
                # on them still offers a DIG. `plantable` is the per-tile form of the same
                # question, which is what Alex asked for: do not randomly dig.
                #
                # Measured on 91422988: `dig 5/0` on d5 against a tape that digs nothing all
                # season, plus stray digs on d12, d13 and d14.
                best = max((plant_prize(c, day) for c in R.CROPS), default=0)
                ops = ([("DIG", None, best * 0.5)]
                       if best and (plantable is None or tile in plantable) else [])
            else:
                ops = []
            if ops:
                nodes.append(Node(tile, ops))

    # **The chain is budgeted by the animals that exist, not by the pens that want one.**
    # `pen_for` names an animal for every pinned pen, so gating on `shed[a] > 0` alone chained a
    # PLACE onto ALL of them -- day 0 pins eight pens against four bought animals and every one
    # became a four-op node. Each chained node costs BUILD + PLACE + FEED + CARE in service plus an
    # animal draw and a wheat draw, so the crew built two pens instead of eight: `build_pasture`
    # 8/8 -> 2/8. Pins are inserted nearest-ground-first, so spending the budget in iteration order
    # gives the animals to the closest pens, which is the same rule the siting already used.
    chain_left = collections.Counter()
    for _tile, (_op, _item, _prize) in pinned.items():
        if _op == "BUILD" and _item in ANIMALS:
            chain_left[_item] = shed.get(_item, 0) + carried.get(_item, 0)

    for tile, (op, item, prize) in pinned.items():
        if R.quadrant_of(tile[0], tile[1]) not in unlocked:
            continue
        ops = [(op, item, prize)]
        later = []
        # **A pen is BUILT and FILLED on the same square, so it is one chain, not two jobs.**
        # The PLACE branch above is reached through `elif kind in ("PASTURE", "COOP")` -- a tile that
        # is ALREADY a pen. Ground that becomes a pen later today is not one yet, so on day 0 the
        # whole dawn node set is `{BUILD: 8, PLANT: 17}` with no placement anywhere in it. The four
        # placements that happen today exist only because the crew-change replan rebuilds the plan
        # at hours 1 and 3 against a board where some pens have since appeared, and everything
        # hanging off a PLACE goes with it -- a planned-once day 0 measured `feed 0/4`, `care 0/4`,
        # `place 2/4`, with two sheep left in the shed until dusk.
        #
        # The pin already holds both halves of the answer: `_refresh_pins` writes
        # `pins[spot] = ("BUILD", animal, cost)`, choosing the ground and the beast together, from
        # the schedule's own ordered row and through the same siting rules as every other pen. So
        # the placement IS geometry -- it is decided where the pasture is decided -- and all this
        # does is let the node say so.
        if BUILD_THEN_PLACE and op == "BUILD" and item in ANIMALS and chain_left[item] > 0:
            chain_left[item] -= 1
            served = ANIMALS[item]["cost"] + _animal_remaining(
                {"animal": item, "placed_day": day}, day)
            if TPD - hour - 1 < SERVICE_ROUND:
                served -= BASE_PRICE[ANIMALS[item]["product"]]
            served = max(1.0, served)
            if PLACE_IS_MANDATORY_FROM_DAY is not None and day >= PLACE_IS_MANDATORY_FROM_DAY:
                served += MANDATORY
            later.append(("PLACE", item, served))
            # Priced exactly as the standing-pen branch prices them, so a fresh pen's dinner does
            # not outbid an existing animal's. A BUILD costs a turn before the PLACE can start, so
            # the service round needs one more turn of headroom here than it does there.
            if SERVE_THE_ANIMAL_IT_PLACES and TPD - hour - 2 >= SERVICE_ROUND:
                price = BASE_PRICE[ANIMALS[item]["product"]]
                later.append(("FEED", "WHEAT", MANDATORY + price))
                later.append(("CARE", None, price))
        # **A seed put in the ground is a tile that needs watering, and it needs it today.**
        # Same defect as the pen, same shape: `crop_ops` is only reached for a tile that is ALREADY
        # planted, so at dawn a pinned PLANT offers one op and the WATER it creates cannot be seen
        # until a later turn finds the seed in the ground. On day 0 that is 17 waters invisible to
        # the plan. `crop_ops` is called on the tile as it will stand once planted rather than
        # re-deriving a price here, so the survival rule, the yield window and the fertilizer
        # decision stay in exactly one place.
        elif PLANT_THEN_WATER and op == "PLANT" and item in CROP:
            ops.extend(crop_ops(_freshly_planted(item, day), day, have_fert))
        nodes.append(Node(tile, ops))
        # **A SEPARATE node on the same tile, not extra ops on the build.** Merging them was tried
        # and is wrong: `Node.prize` sums its ops and `Node.service` counts them, so a four-op build
        # outbids and out-costs everything around it and the whole allocation reshuffles --
        # `build_pasture` 8/8 -> 6/8, `plant` 17/17 -> 14/17, for two placements gained.
        # A second stop changes nothing about the build and is exactly what the hour-1 replan used to
        # produce. The route is a visit ORDER; `_live_ops` re-derives the work from the live board at
        # each stop (`schedule_agent:1201`), so the second visit reads a pen that is now standing and
        # emits the PLACE, while a stop whose pen never got built simply returns nothing and drops.
        if later:
            nodes.append(Node(tile, later))
    return nodes


# ---------------------------------------------------------------------------------------------
# routing: cluster-first is implicit in cheapest-insertion, then 2-opt each route
# ---------------------------------------------------------------------------------------------

