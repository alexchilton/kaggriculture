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

#: Whether a pen's YIELDING ops are served BEFORE its consuming ones, rather than after.
#:
#: A stop's ops run in list order, and `animal_ops` built them in the order the rules are written:
#: FEED, CARE, COLLECT_FERTILIZER, HARVEST. That puts the two ops that produce something sellable
#: last, so a pen visited at dawn does not yield until its fourth turn.
#:
#: Measured on Seb's tape, seed 11, day 6 -- the same pen, the same four ops, opposite order:
#:
#:     tape  F  h0 HARVEST  h1 COLLECT_FERTILIZER  h2 DROP  h3 PICKUP  h5 FEED  h6 CARE
#:     ours  u3 h3 FEED     h4 CARE  h5 COLLECT_FERTILIZER  h6 HARVEST  h7 walk  h8 DROP
#:
#: Six wool either way. His are in the shed at hour 2 and pay for that turn's BUY_SEED; ours are in
#: a hand until hour 8. Day 6's entire gap is one $800 strawberry order placed at hour 1 against a
#: $296 bank, and an hour-2 sale of that wool covers it.
#:
#: **TRIED AND REVERTED 2026-08-07.** It is the right reading of the tape and it does not help,
#: because the hour it saves is not the hour that is missing. Measured, days 0-6, ours minus tape:
#: d2 4 -> 8 cells, d3 7 -> 8, money newly diverging on d2 and d3, and **day 6 unchanged at 14**.
#:
#: The reason it cannot work on its own: his farmer HARVESTs at hour 0 because the sheep pen IS the
#: depot tile (4,4). Ours is at (3,4), and the unit that serves it is doing a PICKUP at (4,4) on
#: hour 1 and does not stand on the pen until hour 3. Re-ordering the ops moves the yield from that
#: unit's 4th turn to its 1st -- hour 3 rather than hour 6 -- which is still three hours past the
#: hour-2 sale that pays for the strawberry. The lever is WHERE the pen is, not what order it is
#: served in; `build_tiles` is in `TAPE_ONLY` and stripped, so we choose our own tiles and chose a
#: worse one.
YIELD_FIRST = False

#: Whether the FOUR shed-access cells pick their animal by the size of one harvest, instead of by
#: position in `R.ANIMAL_NAMES` -- which is `["GOOSE", "COW", "SHEEP"]`, so a COW takes any shared
#: PASTURE whenever both are in the shed at once.
#:
#: Deliberately NOT the reverted global tie-break a few lines below. That one value-ranked EVERY
#: pasture and measured -$5,676 on the 12-seed ladder, because the season wants 8 COW to 6 SHEEP and
#: a same-turn ranking reallocates far more pens than the one it was diagnosed on. This ranks only
#: the four cells where a harvest can be DROPPED without moving, which is a property no field tile
#: has at any price. The rest of the board keeps the fixed order untouched.
#:
#: Measured on Seb's tape, seed 11, day 6 -- identical boards, one different occupant:
#:
#:     (4,4)  ours {'kind': 'PASTURE', 'animal': 'COW'}     our SHEEP sits at (3,4)
#:     (4,4)  tape {'kind': 'PASTURE', 'animal': 'SHEEP'}
#:
#: A full load is 6 WOOL at $200 against 6 MILK at $160, and his farmer takes it at hour 0 and drops
#: it at hour 2 without a step -- which is what pays for day 6's $800 strawberry order.
#: **TRIED AND REVERTED 2026-08-07.** Measured, days 0-6, cells ours-minus-tape per day:
#: d2 4 -> 6, d3 7 -> 8, d4 7 -> 9, d5 7 -> 8, d6 14 -> 15; 52 -> 59 total. Worse on every day it
#: touched and it did not even fix the day it was built for.
#:
#: So the narrowing argument above is sound and still insufficient: WHICH animal ends up on (4,4) is
#: not a free choice made at that cell. It is decided days earlier by what the schedule has bought
#: and by SHEEP `first_yield_day` 6 against COW's 8, and forcing the sheep there re-times the whole
#: herd. Same shape of failure as the global tie-break it was distinguished from -- a same-turn
#: ranking cannot see a season's allocation -- which is the third time that has been measured here.
#: Whatever puts his sheep on the depot cell is upstream of `build_nodes`, in the buy/place order.
DEPOT_PEN_BY_LOAD = False

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

#: Whether a tour that ends on a YIELDING node reserves the walk back to the nearest depot.
#:
#: The tour is otherwise costed as an OPEN route -- walk plus service from where the unit stands,
#: nothing for getting back -- which is correct for a tile that only consumes and wrong for one that
#: yields. Measured on Seb's tape, seed 11, day 3: our u4 collects a fertilizer, its tour ends at
#: hour 17 seven steps out, the return leg turns it home on hour 18 and it walks into dusk without
#: arriving. `sell 4/5`, day-4 dawn bank $388 against his $482, and $388 does not buy a $400 cow.
#:
#: This is a RESERVE, not work: it is charged against the budget at every acceptance test and never
#: added to `cost`, so it shortens a tour rather than booking turns the unit does not spend. Off
#: restores the open route exactly.
RETURN_LEG = True

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

#: Whether the shed's stock of an animal is a budget shared across units, the way turns already are.
#: See the note in `plan_routes`. Off restores the pre-2026-08-07 behaviour, where one COW and three
#: empty pens produced three full-prize PLACE nodes and two units were sent to fetch the same animal.
SUPPLY_LEDGER = True


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
        # A hungry pen is one missed day from the animal escaping outright
        # (`reference/kaggriculture.py:786`), which is irreversible: the structure survives, the
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
        out.append(("HARVEST", None, cell["yield_units"] * price))
    if YIELD_FIRST:
        # Stable, so COLLECT_FERTILIZER still precedes HARVEST and FEED still precedes CARE. Built
        # in rule order above because the CARE prize is conditional on FEED being served; only the
        # SERVICE order changes here, never which ops the pen is offered.
        out.sort(key=lambda o: o[0] not in YIELDING)
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


def build_nodes(tiles, day, shed, carried, unlocked, pinned, hour=0, pen_for=None):
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
                order = list(R.ANIMAL_NAMES)
                if DEPOT_PEN_BY_LOAD and tile in SHED_SET:
                    order = sorted(order, key=lambda a: -(
                        BASE_PRICE[ANIMALS[a]["product"]] * ANIMALS[a]["max_held"]))
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
                best = max((plant_prize(c, day) for c in R.CROPS), default=0)
                ops = [("DIG", None, best * 0.5)] if best else []
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
            ops.extend(crop_ops({"kind": "PLANT", "crop": item, "planted_day": day,
                                 "watered_today": False, "consecutive_unwatered": 0,
                                 "yield_units": 0, "fertilized_until_day": -1},
                                day, have_fert))
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


def plan_routes(units, nodes, budget, depots=SHED, carry=None, supply=None):
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
    # **The shed's stock of a DRAWN item is a shared budget, exactly like turns.** `build_nodes`
    # prices a PLACE per DESTINATION TILE and gates it only on `shed[a] > 0`, so one COW and three
    # empty pens produce three nodes each worth the full $1,840. `held` and `depot` are per-unit and
    # nothing here notices that two units have claimed the same animal. Scarcity was enforced only at
    # execution -- first unit to a depot takes it, every later claimant's PICKUP draws nothing and
    # walks a full round trip to a pen with no animal in it.
    #
    # Measured on Seb's tape, seed 11, day 3: one COW, pens at (0,3), (1,3) and (0,4) all offered
    # from hour 1 to hour 17, two units sent. The day is exact anyway only because both wasted trips
    # land early enough to recover from -- which is why the closed-tour marginal broke it. Costing the
    # tour correctly ranks a phantom node last, and the tail of the day is where a fake node does the
    # most damage.
    #
    # **Only the animals.** Applied to every DRAWN item this MEASURED as a day-0 regression --
    # `feed` and `care` 4/4 -> 3/4 -- because the day-0 shed holds no wheat at dawn and every wheat
    # arrives later by BUY_PRODUCT. A plan that refuses to book feed against a shed that is empty
    # right now is refusing work that will be fundable by the time the unit walks there, and the
    # bought wheat comes in bulk so no unit's draw denies another's.
    #
    # An animal is the opposite on both counts: it is bought one at a time, it is the input to a
    # chain with a same-day deadline, and a second claimant on the same COW gets nothing at all.
    # `None` means unconstrained, for the synthetic router tests that pass no shed.
    stock = None if supply is None or not SUPPLY_LEDGER else collections.Counter(
        {k: v for k, v in supply.items() if k in R.ANIMAL_NAMES})
    booked = collections.Counter()
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
        # **A tour that yields is CLOSED: the depot is its last node.** Appending it here rather than
        # reserving turns separately is the whole difference between ordering a tour and truncating
        # one. As a reserve it refused the insertion outright, so day 4 lost a water and the far-corner
        # harvest at (0,1) -- which then rotted past its `max_lifespan_step` and cost a DIG on day 5.
        # As a closing node it only makes a far last stop *dearer* than the same stop taken mid-tour,
        # which is exactly the ordering the tape plays: work until hour 15-17, then walk in.
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

    # **TRIED and REVERTED: put the walk home in the RATIO, as `delta + homeward(after) - homeward(now)`.**
    # It is the textbook closed-tour marginal and it is exact at every insertion position, so it
    # should have let a far node be resequenced onto the way back rather than refused. On day 4 it
    # did exactly that -- `water` 16/17 -> 17/17, `harvest` 13/14 -> 14/14, and the day-5 DIG on the
    # rotted (0,1) tile disappeared. It still broke two earlier things:
    #
    #     d3  sell 5/5 -> 3/5      fertilizer stranded again, `pickup` 7/3, two units walking in at 23
    #     d4  place 1/1 -> 0/1     feed and care 7/7 -> 6/7; the animal chain lost to the reordering
    #
    # So the ratio was not the whole defect either. The likely remainder: `budget` is `TPD - hour - 1`
    # and only IDLE units are replanned, so a unit committed at hour 6 keeps a tour costed against a
    # budget that no longer exists, and the closed cost it was accepted under stops being true. Any
    # next attempt should fix the stale budget first and re-measure, not re-derive the marginal.

    def _uncovered(u, n):
        """What this node needs that the unit is not already carrying, after everything assigned so far."""
        return {it: c - held[u][it] for it, c in n.needs.items() if c > held[u][it]}

    def claim(u, n):
        """The animals this node's PLACE ops must draw, after what the unit already carries.

        **PLACE only, never BUILD.** `BUILD` is in `DRAWN` and carries the animal name too, so
        counting it as a claim MEASURED as day 0 `build_pasture` 8/8 -> 4/8: pens are built ahead of
        the animals that will fill them -- the tape builds eight on day 0 having bought four -- and a
        build does not consume the animal, it only says which one the pen is for.
        """
        want = collections.Counter(i for o, i in n.ops if o == "PLACE" and i in R.ANIMAL_NAMES)
        return {it: c - held[u][it] for it, c in want.items() if c > held[u][it]}

    def in_stock(u, n):
        """Is the animal this node would place actually left, after earlier units' commitments?"""
        if stock is None:
            return True
        return all(booked[it] + q <= stock[it] for it, q in claim(u, n).items())

    def homeward(u, n=None, i=None):
        """Turns reserved to walk home, if this tour would end holding something sellable.

        See `RETURN_LEG`. Zero unless the route yields, and measured from the LAST tile rather than
        from every yielding one, because one shed trip empties the whole hand.

        **TRIED and REVERTED: close the tour instead, by making the depot `delta`'s final node.** It
        is the better-shaped idea -- it makes a far last stop dearer than the same stop taken
        mid-tour, rather than refusing it -- and on day 4 it worked exactly as intended, taking
        `water` to 17/17 and `harvest` to 14/14 and rescuing the far-corner tile at (0,1) whose
        expiry costs a DIG on day 5. But it let units range further out on DAY 3, which was exact:
        `sell` went 5/5 -> 3/5, u0 and u2 both still walking home at hours 21-23, fertilizer reaching
        the shed one unit at a time on hours 6, 14 and 18 against his two big drops.
        Day 3 comes before day 4. The reserve stays until something does both.
        """
        if not RETURN_LEG:
            return 0
        route = list(routes[u])
        if n is not None:
            route.insert(i, n)
        if not route or not any(o in YIELDING for m in route for o, _i in m.ops):
            return 0
        return min(dist(route[-1].tile, d) for d in depots) + HOMEWARD_DROP_TURNS

    def cdelta(u, n, i):
        """Marginal cost of the insertion with the walk home priced in. See `CLOSED_TOUR`.

        Telescoping: `used[u]` therefore always holds the cost of the CLOSED tour as it stands, so
        acceptance is a plain `used[u] + cdelta <= budget` with no separate reserve.
        """
        if not CLOSED_TOUR:
            return delta(u, n, i)
        return delta(u, n, i) + homeward(u, n, i) - homeward(u)

    def reserve(u, n, i):
        """The return leg still charged separately, which under `CLOSED_TOUR` is already in `cdelta`."""
        return 0 if CLOSED_TOUR else homeward(u, n, i)

    def commit(u, n, i, c):
        """Put `n` at position `i` of unit `u`, paying `c` turns and booking whatever it must draw."""
        short = _uncovered(u, n)
        booked.update(claim(u, n))          # before `held` is spent below
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
                if not in_stock(best_u, n):
                    continue
                spot = min(((cdelta(best_u, n, i), i) for i in range(len(routes[best_u]) + 1)),
                           default=None)
                if (spot is None
                        or used[best_u] + spot[0] + reserve(best_u, n, spot[1]) > budget[best_u]):
                    continue                  # no room today; it stays in `left` for the general pass
                commit(best_u, n, spot[1], spot[0])
                left.remove(n)

    order = sorted(left, key=lambda n: -n.prize)
    # Mandatory nodes are assigned in their own pass, so a hungry animal cannot be outbid on ratio by a
    # melon that happens to be nearer. Within the pass they still order by cost.
    # Three tiers, not two. CRITICAL goes first because inside a single pool the ranking is
    # `prize / marginal cost`, and a 1% prize edge cannot survive an 8x difference in distance --
    # which is exactly how a pen one day from losing its animal lost to a healthy pen next door.
    for pool in ([n for n in order if n.critical],
                 [n for n in order if n.mandatory and not n.critical],
                 [n for n in order if not n.mandatory]):
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
                        if not in_stock(u, n):
                            continue
                        for i in range(len(routes[u]) + 1):
                            c = cdelta(u, n, i)
                            if used[u] + c + reserve(u, n, i) > cap[u]:
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
        # 2-opt reorders an OPEN path, so it can shorten the walk out and still leave the tour ending
        # further from the shed. Close the cost the same way `delta` does before comparing, or the
        # reorder is judged on a shorter path than the unit actually walks.
        home = (min(dist(ordered[-1], d) for d in depots)
                if RETURN_LEG and ordered
                and any(o in YIELDING for m in new for o, _i in m.ops) else 0)
        if cost + home <= budget[u]:
            routes[u] = new
            # Under `CLOSED_TOUR` every `used[u]` already carries the walk home, so the reordered
            # tour must be booked the same way or the next insertion is costed against a short tour.
            used[u] = cost + home if CLOSED_TOUR else cost

    return {u: dict(route=routes[u], depot=depot_at[u], draw=depot[u], cost=used[u])
            for u in routes}
