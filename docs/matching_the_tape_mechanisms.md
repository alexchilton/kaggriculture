# Matching the tape — planner mechanisms found by diffing against a reference

Merged 2026-08-13 from ten 2026-08-09/-10/-11 write-ups that found real planner bugs by diffing our
agent's day-by-day behaviour against a recorded opponent tape, op for op. Source files deleted:
`fable_matching_the_tape_2026-08-10.md`, `how_sebs_planner_works_2026-08-10.md`,
`how_seb_feeds_the_herd.md`, `the_day_is_a_cash_ledger.md`,
`plan_once_and_the_dawn_blind_spots_2026-08-09.md`, `handoff_plan_once_2026-08-09.md`,
`router_tape_repoint_2026-08-09.md`, `the_tape_column_does_not_replay_his_game_2026-08-09.md`,
`fable_the_d4_d5_planner_2026-08-11.md`, `fable_the_d7_feed_2026-08-11.md`.

> **Two different tapes appear below — read the section headers.** Sections 2-5 are measured against
> **Seb's tape**, which `docs/the_ladder_is_two_scripts.md` and `docs/REGISTER.md` OPEN-10 have since
> shown was optimal only under the OLD `townCenterSellInterval=12` economy — his median bank halved
> when the town rebalanced and he has withdrawn from the ladder. **The target is superseded; the
> mechanism findings are not** — every bug found this way is a real planner defect, independent of
> which tape exposed it. Section 6 is measured against **Victor's tape**
> (`data/seed_scripts/victor/`), the field's #2-rated player and the currently-active submission
> target — referenced live in `cover.py`, `schedule_agent_1455mh.py`, `build_planner_submission.py`
> and current tests. **Section 6 carries no target-supersession caveat: it is live, current work.**

---

## 1. What a good planner looks like — Seb's route architecture

Reconstructed directly from recorded observation/action pairs across four independent tapes (seeds
`1012428555`/`231975074`/`658760367`/`1440180345`, four different opponents, both seats, both
`townCenterSellInterval` economies), confirmed by replay on five of our own seeds.

**The opening is byte-identical across all four tapes through day 3** (units 24/24, market 24/24 or
near it) and diverges starting day 4 — the first day after `townShopUnlockInterval=3` gives the
agent its first live information.

**Each hand is assigned one of four fixed roles for the whole day** (waterer/feeder/collector/
builder) and **owns a contiguous tile block, walked once, never revisited.** Our own global
re-ranking is measured to cost **16 plants lost to thirst** (14 strawberry, 2 melon) in a season
where Seb's equivalent loses exactly one animal. A worked d0 example: unit 6 sweeps column y=4, then
row x=0, PLANT/WATER on consecutive turns at the same tile — a literal lawnmower.

**Idle time is deliberate, not filled**: 707 idle turns over d0-d16 (124 on d1 alone), work at only
32.7% of all turns season-wide (14.0%-43.3% by day), against 49.1% spent walking — a finished hand
is never reassigned.

**Feed routing splits a pen's day across hands, contradicting our own `crew.cover` design
principle** ("the unit of ownership is the TILE, not the op... a pen's whole day belongs to one
hand"). Read directly off tape `91422988` day 4: Seb scores FEED 7 / CARE 7 / COLLECT_FERTILIZER 6
against our FEED 5 / CARE 5 on the identical board. His day uses three roles — two wheat carriers
that load their whole draw once at dawn (h1, h2) and never return to the shed, plus one animal
carrier that carries the COW for ten hours doing the zero-carry-cost ops (CARE, COLLECT_FERTILIZER)
at every pen it passes. The animal carrier places the cow at (1,3) h12 *without* feeding it; a wheat
carrier already mid-sweep feeds it two hours later at h14 — Seb solves "feed is invisible until the
animal is placed" with a second hand's timed sweep, not by giving the pen to one hand.

Traced identically on our side: one herd hand (u4) carries cow, wheat, feed and care alone, mid-tour
DROPs at h6 (all-or-nothing per `kaggriculture.py:333`, so it dumps the cow too), re-picks up only 1
of 3 wheat requested, and the second cow it places at h14 is never fed or cared for at all. The
wheat ledger is identical both sides (6 dawn + 1 bought = 7 animals) — **we are not underfunded, we
spend a wheat unit on a round trip Seb's design never requires.** Two threads left open: the source
of Seb's seventh FEED against only 6 drawn wheat, and whether our h6-h8 loss of 1 wheat + fertilizer
is shed-capacity overflow or a different hand drawing it first.

Implications for a future planner, not yet built: assign role + contiguous block per hand at dawn,
no global re-rank; emit PLANT+WATER as one owned tile; let a finished hand idle rather than force
work; d0-d3 need no board reading at all (constant); d4+ input is just the shop unlock plus bank.

## 2. The tape-column harness bug — the reason several money/state columns are unreliable

**Proved the `breakdown.py` "tape" column does not reproduce Seb's actual recorded game.** Pushing
his own recorded actions for both seats through a fresh env on seed 11 diverges from his real
recorded bank starting **turn 32 (day 1, hour 8)** by exactly one dollar ($29 charged vs $30
recorded for the same WHEAT purchase) and compounds to a final simulated bank of $10,264-$11,711
against his real $110,820 — roughly 9% reproduction. Root cause: his replay predates the 2026-08-08
kaggle-environments 1.32.6 switch, which re-priced wheat, so his recorded game is fundamentally not
reproducible under the currently-installed engine at all; `weedSpawnChance` (0.0 vs 0.005) makes no
difference to the divergence point. **This closes a disagreement that had recurred "roughly ten
times across sessions."**

Verified clean by the same pass: the starting board is exact (seed 11 reproduces his step-0 board
cell-for-cell) and the schedule derivation is exact (builds/places match his tape every day across 17
days, 19/19, zero mismatches).

**What this invalidates:** every "tape column" state/fill/money figure quoted from
`breakdown.py --tape seb...` after day 1 — melon, pastures, sells, and money are all measuring an
environment that stopped being his game on day 1, not a real target. Two illustrative false
positives: `melon 7/6` and `pens 9/8` at d5 both looked like *our* over-buying but are actually the
*column* being short — the schedule's cumulative counts (7 melon, 9 builds by d5) match our actual
play exactly. This also corrects two specific wrong prior beliefs (recorded in
`.claude/skills/matching-the-tape` and formerly in `REGISTER.md`) that the contamination was
money-only and started at d4 — it is state+fills+money, and starts day 1 hour 8.

**The ruling that follows: the schedule (build/place/plant/buy/sell counts per day) remains the
valid target; money and realized fill prices are not portable across env versions and should never
be tuned against.**

### The mechanical fix: repointing the tape

Repointed the test harness's tape fixture (`TAPE_REPLAY`/`TAPE_SCHEDULE`/`TAPE_TEAM`) from Seb's
1.32.2-played tape (`90494364`) to a 1.32.6-played one (`90976060`, "seb1326") and re-derived every
day-specific asserted number from scratch via a ground-truth replay script, because the two tapes
differ structurally (land-buy days 5/9/11 vs 4/6/10, ~19 vs 21 pens, herd flipped MILK 179→303/WOOL
230→104/MELON 132→96), not just numerically. A sanity check reproduced the pre-existing day-6
dawn-bank figure of $1,855 exactly by replaying the old tape under the current env, validating the
method.

The repoint revealed that **days 0-3, previously asserted "already exact," are NOT exact under the
new tape** (day 0 FEED 1/4 CARE 1/4 SELL 7/0, day 3 FEED 4/6 CARE 4/6 SELL 7/5) — so day 4's known
shortfall inherits upstream drift rather than being a standalone day-4 defect. Of 76 tests, 4 were
deleted outright because the economic conditions they measured (a day-5 wheat-reserve race, a
day-6 $800 seed bill, a day-6 wool-sale geometry) simply don't occur in the new tape's schedule
rows, 2 were re-derived and now pass, and 5 remain failing — all pre-existing gaps re-measured
against the corrected target, none newly discovered, including day 4's `HARVEST 11/14, WATER 12/17,
SELL 22/55` and day 6's plant count flipping from under- to over-planting (6 planted against a
target of 4, was 14). **`seb1326` is itself flagged as still the stale interval-12-economy build —
the further recommended repoint is onto Dmitry Belan or Efe Can Celiksoy (`REGISTER.md` OPEN-10).**

## 3. The plan-once architecture and its dawn blind spots

Diagnosed four blind spots in a single-dawn-plan architecture, all traced to `interpreter` applying
unit actions before `_process_market` (`kaggriculture.py:922` then `:928`), all confirmed by a
red-then-green test in `tests/test_the_first_seven_days_match_the_plan.py`:

1. **The crew** — the dawn plan can't see hands hired that same turn. Fixed by
   `PLAN_THE_CREW_THAT_ARRIVES`, modeling hire cost and silent-failure-when-short exactly.
2. **The goods** — a `buy` lands at the end of hour 0, invisible to the dawn plan.
3. **The animals** — `BUY_ANIMAL` commits to shed like a product; `build_nodes` gates PLACE on
   `shed[a]>0`, so an empty pen offers nothing at dawn. Caused d3 and d6 to plan **zero**
   placements despite owning the pen.
4. **The pens** — `build_nodes` only reaches PLACE through an *already-built* pen tile; on d0 pens
   are built during the day, so the whole dawn node set that day is `{BUILD:8, PLANT:17}` with zero
   placements. **"`feed 0/4` on a planned-once day 0 was never a feeding defect — it was two
   placements that were never in the plan."**

**Measured on work-turns-to-tape-339 (d0-d6, against the OLD pre-repoint Seb tape `90494364` — treat
these numbers as target-stale even by the standard of the other sections here):**

```
config                                              geom OFF   geom ON
HEAD (5aa233e)                                          317        305
+ PLAN_TODAYS_PURCHASES                                 290        308
+ purchases + BUILD_THEN_PLACE (merged)                   —        281
+ purchases + PLAN_THE_CREW_THAT_ARRIVES                239        273
full plan-once, PLACE merged onto build                   —        276
full plan-once, PLACE as own node                          —        284
```

**Nothing beats HEAD's 317.** `PLAN_THE_CREW_THAT_ARRIVES` (an env-accurate phantom-crew model)
still loses to the existing two-stage plan-then-replan-at-h1 approach — "the h1 replan is not a
defect." `BUILD_THEN_PLACE` initially collapsed `build_pasture` from 8/8→2/8 by chaining PLACE onto
every pinned pen regardless of whether an animal existed; recovered to 6/8 (281) by budgeting
against actual animal count, still under HEAD. **Only `PLAN_TODAYS_PURCHASES` is kept**: −27 with
geometry off, **+3** with geometry on (interaction-dependent, not independent). Shipped config:
geometry ON + purchases ON = 308.

`DEPOT_RING_FIRST` (the geometry flag) stays ON — Alex's explicit call, twice reaffirmed — despite
costing 12 work turns alone against HEAD and breaking 7 previously-exact d6 rows; the prior OFF
verdict was money-based (money isn't the criterion) and measured against an obsolete planner.

**Two further fixes, found by direct observation:** FEED was being drawn twice per pen because
`PLACE_DRAWS_FEED` added a second wheat unit on top of one already implicit in the placement node's
own `DRAWN` set; and hands were walking straight past hungry animals while carrying 8 wheat because
`_live_ops` was only consulted at tour stops — `underfoot()` now feeds the ground under a moving
hand from both the depot and travel branches.

**Measured nulls, recorded so they are not re-derived:** `RESERVATION_SLIP` 0.10→0 byte-identical;
`CHAIN_OPS` byte-identical (dead code, `COVER_PLANNER=True` means `router.plan_routes` never runs);
several `materialise` delivery rules never fire; `SELL_ROW_PRODUCE_GOES_FIRST` no change;
`END_NEAR_THE_SHED` null on d4, real loss on d6; phantom-crew planning alone (without the other 3
fixes) 317→273 — "it only pays as a set."

**Open items still handed off:** d6 as the worst real day (`place 0/1, plant 13/14, water 16/17,
buy_product 6/9, feed 7/8`); d4's single unfed `care 6/7` (`CARE_WHAT_YOU_STAND_ON` tried and shipped
OFF, xfail strict, because it buys 1 care at the cost of 9 others); the closing shed trip uncharged
(4 fixes tried, all null/negative, needs a per-TOUR not per-day reserve); two never-built rules —
don't dig weeds outside the geometry plan, don't plant what can't finish before season end.

## 4. The cash-ledger / funding-sequencing bug

`schedule_agent_1455mh.sell_deadline`'s `short_of_cash` flag collapses an entire day's bill into one
boolean, ignoring when each obligation is actually due. On day 4 this sums a $400 cow (due h0,
already covered by the dawn bank), a $1000 land parcel (due h21 — the only item genuinely needing
sale revenue), $33 hires and ~$28 wheat into ~$1461 against $480 cash, forcing the whole day into an
h0 sell-everything rush. Seb's actual day 4, read off tape `91422988`, sits idle on $12 from h2 to
h18 at zero cost — nothing is due before h21 — then sells in four waves (h18/21/22/23, summing to 55
wheat+fertilizer) and buys land at h21 funded by earlier order slots the same turn; our agent
rushes selling by h2, dribbles small sells from h6, and stops selling entirely once the land purchase
clears, missing the two biggest waves (his h22 sells 12 more, h23 sells 21 more, ours sells nothing
either hour). `feed 6/7`/`care 6/7` on d4 are downstream of the same bug: the h0 cow purchase drops
the bank to $15 by h2, so the seventh animal's wheat is unaffordable that morning — a
cash-sequencing failure, not a routing one.

**Proposed (unbuilt) fix**: a dated-obligations ledger — walk `[(hour, cash)]` against the live
opening balance to find the first hour the running balance actually goes negative, turn each deficit
into a "N units in shed by hour H" delivery obligation for routing, and space sell waves to let the
book recover between them. A related measurement found landing a load in two waves banked $542 for
54 units against four waves' $774 for 41.

**Ruled out**: staggering hire arrivals off tile (5,5) to avoid crowding — measured LOSS on d4
(water 17/17→16/17, harvest 14/14→12/14, place 1/1→0/1) — because Seb's own tape boxes two hands
doing nothing on that exact tile through d0-d4 with zero cost. `_days_bill` counts the cow correctly
— the bug was never a missing term, it was summing terms with different due dates.

This is the same "no delivery deadline" gap section 3 independently named one day earlier — this
section goes further with a concrete ledger design.

## 5. d4 sell shortfall and d9/d10 placement failures

**d4 — we sell only 41 of the 55 wheat units Seb's tape sells** (5+12+12+20 vs our 39, both matching
their respective breakdown rows exactly), while `buy_product` reads 21/1 — a mirror-image wash
trade. Traced hour-by-hour, HARVEST and delivery timing match exactly on both sides (14/14); the
defect is entirely `DUSK_FEED_TOPUP` (`schedule_agent_1455mh.py:3606-3634`) recomputing the same
feed-reserve quantity (`feed_days(day)*alive` = 7 on d4) independently of the sell-side reserve at
`:2909-2933`, so from hour 18 the agent sells wheat down to the reserve floor then immediately rebuys
toward the same floor, every turn, for the rest of the day. End-of-day wheat is 0/0 both sides, so
nothing is lost — the cost is a spread paid twice on ~20 units/day, contributing to a ~$289 d4 money
gap not fully isolated. No fix was written (read-only pass); the shape needed is unifying the two
reserve computations.

**d9 and d10 both read `place 0/4`** — three chained causes, all directly instrumented:
`router.build_nodes`'s species tie-break types every open pen "PLACE COW" (never SHEEP) whenever
both have nonzero supply — only 2 of 10 identical COW claims are ever affordable against
`plan_supply`'s `stock[COW]=2`; `SHOP_ADAPT_HERD` (active from day 6) buys 4 SHEEP and 0 COW on both
days because it re-derives species from live market headroom rather than the schedule's day mix (all
4 buys both days are SHEEP — already logged in `REGISTER.md`'s OPEN-CLI-2); and the 2 routed COW
claims draw against a shed that genuinely never holds a COW, fail silently (non-critical, no
replan), and strand all 4 real SHEEP purchased that day with no pen ever typed to receive them.

## 6. Current work — Victor's tape (not superseded)

**Measured against Victor's tape — the field's #2-rated, currently-active submission target, not
Seb's.** No target-supersession caveat applies to this section.

### The spawn-ring step-off drops the depot draw

Found and fixed a bug where the farmer's hour-0 spawn-ring step-off overwrites the planned action
*after* the route has already consumed that hour's real action (a WHEAT pickup on days 3-5), so the
route believes wheat was drawn that never was. This costs 6 unpriced turns (2 for the wasted round
trip, 4 for a triggered fetch-recovery), which on day 4 drops the tour's final stop
`(0,4)[WATER,HARVEST]` — measured as `water 14/15, harvest 4/5` — and cascades to day 5's
`plant 4/5, strawb 6/7`.

The fix ("defer, don't delete," `hold_farmer` + `farmer_start`) makes `_router_acts` skip walking
the farmer's route on an overwritten turn rather than deleting the step, so the real pickup lands
one turn later instead of being lost. Two other fix shapes were tried and rejected: removing the
step-off entirely re-strands a second hand for 23 idle turns; guarding to "only overwrite a MOVE"
silently reduces to the same removal on exactly the days that matter (PICKUP days). Verified with a
test red-at-baseline, green-with-fix, red-on-revert; days 4 and 5 now match on every non-exempt row.

**The fix exposes a genuine, previously-latent router defect**: a newly planted tile starts with
`consecutive_unwatered:1` and weeds at 2, so any plant not watered the same day becomes a weed —
measured directly on tile (5,3), planted day 6 hour 13, weeded day 7 hour 23, never watered once —
because the router prices WATER as a prize rather than a hard co-requisite of PLANT. Stated rule for
future work: "a PLANT whose same-day WATER cannot also be executed is worth LESS than nothing."

Also surfaced: an earlier, still-uninvestigated divergence at day 1 (`care 0/5`), predating and
unrelated to this fix — by the project's days-in-order rule this is technically the first open day
and was not chased in this pass.

A retracted "replant the harvested tile" idea (code-read only, not re-measured) necessarily fails
regardless of router-side fixes, because the pinned-tile gate exists in TWO places
(`router.build_nodes:956` and `schedule_agent_1455mh.py`'s `_live_ops:1349-1352`) and any future
attempt must patch both.

### The d7 order-queue starvation

The dawn plan correctly sizes and funds day 7's whole 14-unit wheat order at hour 0 ($2,512 bank
against a $480ish order), but the order is silently dropped because the h00 queue already holds ten
other orders (wool/fertilizer sells, seven hires, two cow buys) and the append is gated
`len(orders) < 9` — traced directly to `norders=10, REFUSED`. The agent then falls back to a
1-unit/turn drip through hour 15, which the crew's depot draws (h02-h05) outpace; one hand's 3-unit
want is deleted entirely against a momentarily-empty shed at h02, and a later recovery mechanism
only restores 2 of it. This produces `feed 9/10, care 9/10, collect_fert 6/7` on day 7, and the same
signature (`norders>=9` at h0) recurs on days 8, 9, 11 and 12 — 5 of 13 days measured, only day 7 was
fixed in this pass.

**The fix** keeps the dawn boost live (via a `dawn_row_sent` flag) until the block is actually queued
rather than expiring it at `hour==0`, so a refused block goes out whole at the first turn with a free
slot instead of dripping — which matches Victor's own cadence exactly (his h01 queue is also ten
orders deep, and his wheat block also waits for h02). Result: day 7 now matches on
feed/care/collect_fert (9/10→10/10, 9/10→10/10, 6/7→7/7), d0-d6 are byte-identical, and days 8-10
move toward the tape wherever they move (d10 harvest 5/6→6/6, money 3719→5230 against a 5630 target),
with three cells past the frontier drifting by one, explained as noise inherited from already-
diverged ground rather than a regression.

**Explicitly ruled out as fixes**: waiting longer at the depot (the wheat supply rate itself is the
bottleneck, not patience); marking the feed draw critical (deforms the tour the same way as the
d4/d5 regressions above); re-slotting wheat ahead of hires in the queue (Victor's own tape doesn't do
this either — his h01 queue is also exactly ten orders, and his wheat also waits for a free slot at
h02).

**Open frontier after this fix**: d1 `care 0/5` (explained as us being *correct* — the reference only
banks the care bonus on a fed animal, `kaggriculture.py:816`); no-op digs on empty tiles (tape digs
unconditionally); d7's own pre-existing `buy_seed 11/12` (untouched, now the first live divergence);
then d8 (`plant 8/10, water 18/22, harvest 4/6, feed 11/12, care 11/12, place 1/2`) — d8/d9 still
show a residual `feed 11/12` signature suggesting a related but distinct remaining cause, not chased.
