> **TARGET SUPERSEDED, added 2026-08-11.** Measured against the Seb tape (`90494364`), optimal under
> the OLD `townCenterSellInterval=12` economy. His median bank halved and he has since withdrawn from
> the ladder (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats). The planning-cadence findings
> below (single dawn plan, the four blind spots) are architecture, not target-dependent, and still
> stand — only "match the tape op-for-op" as the definition of done is now known to cap the ceiling.

# Planning the day once: four correct diagnoses, three of them net-negative

2026-08-09, seed 11, weeds off, Seb tape `90494364`, measured by
`scripts/breakdown.py --module schedule_agent --days 7`.
The criterion is d0-d6 matching the tape op-for-op, never money.

## The question

Alex's spec: *"you should do the whole plan 1 time per day no replans no urgency and optimise it so
the schedule can be implemented - when you have done that the d0 - d6 should match"*.

An earlier session had solved this with plans at h0, h1 and h2 and he did not accept it: the day is
deterministic, so there should be no reason to replan at all.

## What was actually replanning, and why

`URGENT_OPS` is empty and the idle top-up was deleted in `5aa233e`, so exactly one trigger was left:
`state["crew"] != len(live)`.
`tests/test_the_first_seven_days_match_the_plan.py::test_the_day_is_planned_once_and_only_at_dawn`
counts `_solve` calls per day and measured **d0 planning three times (h0, h1, h3) and d1-d6 twice
(h0, h1)**.

The cause is phase order, not hiring policy.
`interpreter` applies unit actions and only then calls `_process_market`
(`kaggriculture.py:922` then `:928`).
So a hand bought at hour 0 does not exist when hour 0 is planned, appears at hour 1, and the dawn
plan is thrown away.
What actually covered 23 of the 24 hours was an hour-1 plan.

## Four blind spots in the dawn plan, all real, all confirmed by a red test

1. **The crew.** The dawn plan cannot see hands the same turn is about to hire.
   Fixed by `_arrivals` + `_hires_this_turn` (`PLAN_THE_CREW_THAT_ARRIVES`), which model the env
   exactly: hires all settle in ONE turn because the atomic block re-enters per order SLOT
   (`kaggriculture.py:550,564`), `_hire_cost` is `mult * fib(hires_today)` per DAY, and `_do_hire`
   fails silently when the bank is short (`:691`).
   `_spawn_hand` gives the landing square, so phantom index `len(units)+k` is the same unit as real
   index `len(units)+k` an hour later.

2. **The goods.** `buys` lands at the END of hour 0, so the dawn plan reads a shed without it.

3. **The animals.** `BUY_ANIMAL` commits to `private["shed"]` like a product (`:672`), and
   `build_nodes` gates its PLACE branch on `shed[a] > 0` -- so an empty pen the day means to fill
   offered nothing at dawn. This is why d3 and d6 planned **zero** placements while owning the pen.
   2 and 3 are fixed together by `PLAN_TODAYS_PURCHASES`, which credits both rows at hour 0 only.

4. **The pens.** `build_nodes` reaches PLACE only through `elif kind in ("PASTURE", "COOP")` -- a
   tile that is ALREADY a pen. On d0 the pens are built during the day, so the entire dawn node set
   is `{BUILD: 8, PLANT: 17}` with no placement in it to route, and everything
   `SERVE_THE_ANIMAL_IT_PLACES` hangs off a placement goes with it.
   **`feed 0/4` on a planned-once day 0 was never a feeding defect. It was two placements that were
   never in the plan.**
   Attempted fix `BUILD_THEN_PLACE`: a pinned BUILD carries the PLACE, FEED and CARE for the animal
   `_refresh_pins` already chose that ground for.

## The measurement, and why three of the four are OFF

Work turns d0-d6, tape 339. Higher is closer.

    config                                             geometry OFF   geometry ON
    HEAD (5aa233e), nothing added                          317            305
    + PLAN_TODAYS_PURCHASES                                290            308
    + purchases + BUILD_THEN_PLACE (merged onto build)      --            281
    + purchases + PLAN_THE_CREW_THAT_ARRIVES               239            273
    full plan-once, PLACE merged onto the build node        --            276
    full plan-once, PLACE as its OWN node                   --            284

The last two are the same feature implemented two ways, and the difference is instructive.
`Node.prize` sums its ops and `Node.service` counts them, so folding PLACE + FEED + CARE onto the
BUILD made a four-op node that outbids and out-costs everything near it: the allocation reshuffled
and `build_pasture` went 8/8 -> 6/8 and `plant` 17/17 -> 14/17 to buy two placements.
Emitting the placement as a SEPARATE node on the same tile leaves the build untouched, which is
what the hour-1 replan used to produce -- the route is a visit ORDER and `_live_ops` re-derives the
work at each stop, so the second visit reads a pen that is now standing.
That is worth +8 over the merged form and it is still 33 short of HEAD.

Also found and reverted: `DRAWN` contains BUILD and a pinned build carries the animal in its item
slot, though `_emit` uses it only to pick BUILD_PASTURE over BUILD_COOP and consumes nothing. While
BUILD and PLACE shared a node, `Node.needs` summed them and demanded two cows to fill one pen.
Separate nodes make the question moot.

**Nothing beats HEAD's 317.** Each diagnosis is mechanically right and each fix makes the table
worse. Recorded plainly because the temptation next session will be to re-derive them.

- `PLAN_THE_CREW_THAT_ARRIVES` is the second time phantom-crew planning has been tried and the first
  time with the arrival model read off the env rather than guessed. It still loses. The two-stage
  plan with real units beats a one-stage plan with phantoms on every day. **The h1 replan is not a
  defect.**
- `BUILD_THEN_PLACE` first chained a PLACE onto every pinned pen, because `pen_for` names an animal
  for all of them -- d0 pins eight pens against four bought animals and every one became a four-op
  node, so the crew built two pens instead of eight (`build_pasture` 8/8 -> 2/8). Budgeting the
  chain by animals that exist recovered it to 6/8 and 281 work turns, still under HEAD.
- `PLAN_TODAYS_PURCHASES` is **the one interaction worth keeping**: it is -27 with geometry off and
  +3 with geometry on. The two are not independent.

## Geometry

`DEPOT_RING_FIRST` is **1 (ON)**, Alex's explicit call, twice reaffirmed.
The prior OFF verdict in `router.py` is a money argument and money is not the criterion; it was also
measured with the idle top-up and crew replan still in place, i.e. against a planner that no longer
exists.

On the cell criterion, geometry ON alone costs 12 work turns against HEAD and breaks seven rows that
were exact on d6 (`plant 14/14`, `water 17/17`, `harvest 2/2`, `sell 19/19`, `buy_product 9/9`,
`buy_animal 2/2`). With `PLAN_TODAYS_PURCHASES` on it is +18 instead. Shipped config is therefore
geometry ON **with** purchases on, 308.

Not yet measured on the metric Alex named for it: **pen and animal distance**, via
`scripts/where_the_walking_goes.py`. Work turns are the wrong lens for a siting change.

## The real open item: delivery has no deadline

Alex: *"sometimes there are things which need to be delivered to the shed so they can be sold before
something can be bought like land or more animals - that needs to be part of the plan too"*, and
*"if the money is going to be short the harvest or fertilizer should be optimally sold early in the
day"*.

What exists:

- `owed_sale` -- today's `sells` row minus what is already in the shed, passed to `_solve` as
  `wanted=`, so the plan knows which goods must physically reach the shed today.
- `FUND_THE_DAY_WHEN_SHORT` -- `_days_bill(row) > money` sets `fund=True`, which harvests first and
  delivers on sight instead of batching. `_days_bill` counts animals, seeds, buys, hires and land.
- `cover.materialise` appends the walk home when a job yields or the predicted hand is non-empty.

What does not exist: **any ordering or deadline**. `short_of_cash` is one boolean for the whole day.
Nothing expresses "the $2,000 parcel at hour 20 needs those 14 wheat in the shed and sold by hour
12". A delivery has no due hour, and sell-before-buy is not sequenced. That is the unbuilt piece,
and on this tape it is what d4, d6, d8 and d10 turn on.

Two further rules Alex has named and which are also unbuilt: **do not dig weeds that are not in the
geometry plan** (`DIG_ONLY_IF_REPLANTING` gates on global `plants_left`, not per-tile), and **do not
plant what cannot finish** (`_pointless_tiles` drops existing tiles, it does not refuse new ones).

## Tests added

All in `tests/test_the_first_seven_days_match_the_plan.py`, all verified red before the fix:

- `test_the_day_is_planned_once_and_only_at_dawn` -- counts `_solve` per day.
- `test_the_dawn_plan_can_see_the_goods_the_day_is_about_to_buy` -- spies the `supply` kwarg.
- `test_the_dawn_plan_offers_a_place_for_every_animal_the_day_buys` -- spies the node set.

The first is red again with `PLAN_THE_CREW_THAT_ARRIVES = False`, which is the shipped setting. It
is kept because it is the statement of the goal, not a regression guard for it.
