# The tape and the planner

This doc merges 58 source files (57 markdown, 1 raw log) diagnosing planner, routing, and
watering bugs against a recorded reference tape.
The target tape moved three times: Seb -> Victor/Kawashigi -> tetsuya.
A bug-level finding usually survives the target change; a "we now match X" framing usually
does not.
Every original is preserved in `docs/history/` after this consolidation.
Status banners already present in a source file (SUPERSEDED, CLOSED, HISTORICAL,
"unsure — needs an owner's eye") are carried forward, not re-decided.

Three parts, in date order: Seb-era (2026-08-09/10, historical, target superseded),
the Victor/Kawashigi/tetsuya lineage 2026-08-11 to 08-14, and 2026-08-15 to 08-21.

---

## Seb-era tape matching (2026-08-09 to 2026-08-10) — HISTORICAL, target superseded

TARGET SUPERSEDED, added 2026-08-11.
Seb's tape was optimal under the OLD `townCenterSellInterval=12` economy.
Seb's own median bank halved ($137,747 -> $77,737) when the town rebalance landed.
He has since withdrawn from the ladder (`docs/the_ladder_is_two_scripts.md`, measured from 2,744 ladder seats).
The bug findings below are still real bugs.
The "now matches Seb" framing is not the goal.
The field plants 108-147 WHEAT tiles a season; the agent plants 24.

---

### Planning the day once, at dawn — the four blind spots

source: plan_once_and_the_dawn_blind_spots_2026-08-09.md, dated 2026-08-09
source: handoff_plan_once_2026-08-09.md, dated 2026-08-09 (evening handoff)

Alex's spec: plan the whole day once, no replans, no urgency, so the schedule can be implemented, and d0-d6 should then match the tape.
An earlier session solved this with plans at h0, h1 and h2.
Alex did not accept that: the day is deterministic, so there is no reason to replan at all.

**What was actually causing replans.**
`URGENT_OPS` was empty and the idle top-up was deleted in commit `5aa233e`.
One trigger remained: `state["crew"] != len(live)`.
The test `tests/test_the_first_seven_days_match_the_plan.py::test_the_day_is_planned_once_and_only_at_dawn` counts `_solve` calls per day.
Measured: d0 planned three times (h0, h1, h3).
d1-d6 planned twice each (h0, h1).
Cause: phase order, not hiring policy.
`interpreter` applies unit actions and only then calls `_process_market` (`kaggriculture.py:922` then `:928`).
A hand bought at hour 0 does not exist when hour 0 is planned; it appears at hour 1; the dawn plan is thrown away.
What actually covered 23 of the 24 hours was an hour-1 plan.

**Four blind spots in the dawn plan, all confirmed by a red test:**

1. The crew. The dawn plan cannot see hands the same turn is about to hire.
   Fixed by `_arrivals` + `_hires_this_turn` (flag `PLAN_THE_CREW_THAT_ARRIVES`).
   Hires all settle in ONE turn because the atomic block re-enters per order SLOT (`kaggriculture.py:550,564`).
   `_hire_cost` is `mult * fib(hires_today)` per day.
   `_do_hire` fails silently when the bank is short (`:691`).
2. The goods. `buys` lands at the END of hour 0, so the dawn plan reads a shed without it.
3. The animals. `BUY_ANIMAL` commits to `private["shed"]` like a product (`:672`).
   `build_nodes` gates its PLACE branch on `shed[a] > 0`, so an empty pen the day means to fill offered nothing at dawn.
   d3 and d6 planned zero placements while owning the pen, for this reason.
   Items 2 and 3 fixed together by flag `PLAN_TODAYS_PURCHASES`, which credits both rows at hour 0 only.
4. The pens. `build_nodes` reaches PLACE only through `elif kind in ("PASTURE", "COOP")` — a tile that is ALREADY a pen.
   On d0 the pens are built during the day, so the entire dawn node set is `{BUILD: 8, PLANT: 17}` with no placement in it to route.
   Everything hanging off a placement (feed, care) goes missing with it.
   Finding: `feed 0/4` on a planned-once day 0 was never a feeding defect — it was two placements never in the plan.
   Attempted fix `BUILD_THEN_PLACE`: a pinned BUILD carries the PLACE, FEED and CARE for the animal `_refresh_pins` already chose ground for.

**Measurement table, work turns d0-d6, tape 339 (higher = closer):**

```
config                                             geometry OFF   geometry ON
HEAD (5aa233e), nothing added                          317            305
+ PLAN_TODAYS_PURCHASES                                290            308
+ purchases + BUILD_THEN_PLACE (merged onto build)      --            281
+ purchases + PLAN_THE_CREW_THAT_ARRIVES               239            273
full plan-once, PLACE merged onto the build node        --            276
full plan-once, PLACE as its OWN node                   --            284
```
source: plan_once_and_the_dawn_blind_spots_2026-08-09.md

The last two rows are the same feature implemented two ways.
`Node.prize` sums its ops and `Node.service` counts them, so folding PLACE+FEED+CARE onto the BUILD made a four-op node that outbid and outcosted everything near it.
`build_pasture` went 8/8 -> 6/8 and `plant` 17/17 -> 14/17 to buy two placements when merged.
Emitting the placement as a SEPARATE node on the same tile left the build untouched: +8 over the merged form, still 33 short of HEAD's 317.

Also found and reverted: while BUILD and PLACE shared a node, `Node.needs` summed them and demanded two cows to fill one pen (`DRAWN` contains BUILD; a pinned build carries the animal in its item slot, but `_emit` only used it to choose BUILD_PASTURE vs BUILD_COOP).
Separate nodes made the question moot.

**Verdict: nothing beat HEAD's 317.**
Each diagnosis was mechanically right and each fix made the table worse.
`PLAN_THE_CREW_THAT_ARRIVES` is the second time phantom-crew planning was tried, and the first with the arrival model read off the env rather than guessed — it still loses.
The two-stage plan with real units beats a one-stage plan with phantoms, on every day.
**The h1 replan is not a defect.**
`BUILD_THEN_PLACE` first chained a PLACE onto every pinned pen (because `pen_for` names an animal for all of them) — d0 pins eight pens against four bought animals, so every one became a four-op node, and the crew built two pens instead of eight (`build_pasture` 8/8 -> 2/8).
Budgeting the chain by animals that exist recovered it to 6/8 and 281 work turns — still under HEAD.
`PLAN_TODAYS_PURCHASES` is the one interaction worth keeping: -27 with geometry off, +3 with geometry on. The two are not independent.

**Geometry.** `DEPOT_RING_FIRST` is 1 (ON), Alex's explicit call, twice reaffirmed.
The prior OFF verdict in `router.py` was a money argument (money is not the criterion), and was measured against a planner (idle top-up, crew replan) that no longer exists.
On the cell criterion, geometry ON alone costs 12 work turns against HEAD and breaks seven rows that were exact on d6 (`plant 14/14`, `water 17/17`, `harvest 2/2`, `sell 19/19`, `buy_product 9/9`, `buy_animal 2/2`).
With `PLAN_TODAYS_PURCHASES` on, it is +18 instead.
Shipped config: geometry ON with purchases on, 308.
Not yet measured on the metric Alex named for it — pen and animal distance, via `scripts/where_the_walking_goes.py`. Work turns are the wrong lens for a siting change.

**Handoff status, 2026-08-09 evening (source: handoff_plan_once_2026-08-09.md), branch `shaping-potential`, HEAD `f5b1e3e`:**

```
python -u -m pytest tests/test_each_day_matches_the_tape.py -q
python -u scripts/breakdown.py --module schedule_agent --days 7

d0  PASSES
d1  PASSES
d2  sell 4/5   money 561/659
d3  sell 6/5
d4  care 6/7   sell 30/32   money 126/1311   owned 50/25
d5  sell 28/26  money 860/1855  owned 50/25  pen 9/8
d6  plant 13/14  water 16/17  feed 7/8  care 7/8  place 0/1  sell 17/19
    buy_product 6/9  money 1481/2565  owned 50/25  pen 9/8
```

`d0-d6 work 334/339` at the peak; `329` as shipped with the care arm off.
It was **274** when this session's planner work began.
d2's `sell 4/5` and d3's `6/5` are one unit sliding a day and reconcile — d3's money is exact.

**Getting to one plan a day needed four fixes shipped (same list as above, restated in the handoff):**
the crew (`_arrivals` + `_hires_this_turn`), the goods and the animals (`PLAN_TODAYS_PURCHASES`), the pens (`BUILD_THEN_PLACE` + `PLACE_FOLLOWS_ITS_BUILD` in `cover.slot`), and the morning delivery (`WAIT_FOR_THE_MORNING_DELIVERY`: an empty shed at h0 is not treated as a shortfall).

**Two biggest single fixes, both found by watching rather than reasoning:**
- The feed was drawn twice per pen. `DRAWN` contains FEED whose item IS "WHEAT", so once FEED sat on the placement node, `PLACE_DRAWS_FEED` added a second unit for a feed that eats one. A hand sat at the shed hoovering the drip while another placed cows empty-handed.
- Hands walked over hungry animals while carrying eight wheat. The route is a visit ORDER and `_live_ops` is consulted at STOPS only. `underfoot()` in the tour walker now feeds the ground a hand is standing on, out of surplus, from BOTH the depot and travel branches.

**Measured nulls — do not re-derive:**
- `RESERVATION_SLIP` 0.10 -> 0: whole grid byte-identical. The sell bunching is delivery, not the cap.
- `CHAIN_OPS`: byte-identical. `COVER_PLANNER = True`, so `router.plan_routes` never runs.
- "deliver a finished row" / "deliver a finished product" in `materialise` rule 2: never fire. Rule 2 inserts before a LATER job and the fertilizer is collected by the tour's last jobs.
- `SELL_ROW_PRODUCE_GOES_FIRST` (drop the `fund` gate on `Job.funds`): no change.
- `END_NEAR_THE_SHED` ranking tie-break: null on d4, a real loss on d6.
- Phantom-crew planning WITHOUT the other three fixes: 317 -> 273. It only pays as a set.

**The real open item at handoff: delivery has no deadline.**
Alex: purchases like land or animals sometimes need produce sold first to fund them, and that sequencing needs to be part of the plan.
What existed at this point: `owed_sale` (today's sells row minus what is already in the shed, passed to `_solve` as `wanted=`); `FUND_THE_DAY_WHEN_SHORT` (`_days_bill(row) > money` sets `fund=True`, harvest-first and deliver-on-sight instead of batching; `_days_bill` counts animals, seeds, buys, hires, land); `cover.materialise` appends the walk home when a job yields or the predicted hand is non-empty.
What did NOT exist: any ordering or deadline. `short_of_cash` was one boolean for the whole day. Nothing expressed "the $2,000 parcel at hour 20 needs those 14 wheat in the shed and sold by hour 12." This is what d4, d6, d8 and d10 turned on.
Two further named-but-unbuilt rules: don't dig weeds outside the geometry plan (`DIG_ONLY_IF_REPLANTING` gates on global `plants_left`, not per-tile); don't plant what cannot finish before season end (`_pointless_tiles` drops existing tiles, does not refuse new ones).

**Tests added** (all in `tests/test_the_first_seven_days_match_the_plan.py`, all verified red before the fix): `test_the_day_is_planned_once_and_only_at_dawn`; `test_the_dawn_plan_can_see_the_goods_the_day_is_about_to_buy`; `test_the_dawn_plan_offers_a_place_for_every_animal_the_day_buys`.
The first is red again with `PLAN_THE_CREW_THAT_ARRIVES = False` (the shipped setting) — kept deliberately as a statement of the goal, not a regression guard.

**Handoff open list, in order:**
1. d6 is the worst real day: `place 0/1`, `plant 13/14`, `water 16/17`, `buy_product 6/9`, `feed 7/8`.
2. d4 `care 6/7` — one care. `CARE_WHAT_YOU_STAND_ON` buys it and spends nine others; measured, shipped OFF, test xfail(strict).
3. The closing shed trip is uncharged, so a hand can end the day in the far corner holding produce the row wants. Four fixes tried, all null or net-negative; needs a per-TOUR reserve, not per-day.
4. Label the tape column in `breakdown.py` for what it is (see tape-replay-fidelity section below).
5. Never built: don't dig weeds outside the geometry plan; don't plant what cannot finish.

**Housekeeping note:** five `while pgrep -f pytest; do sleep N; done` waiters from earlier sessions were found spinning forever and killed. `data/logs` and `data/seed_scripts` excluded in `.idea/kaggriculture.iml`. Do not delete `data/logs`: gitignored, deletion permanent, 92 log paths cited as evidence in 84 files.

**Shipped vs diagnosed:** `PLAN_THE_CREW_THAT_ARRIVES`, `PLAN_TODAYS_PURCHASES`, `BUILD_THEN_PLACE`/`PLACE_FOLLOWS_ITS_BUILD`, `WAIT_FOR_THE_MORNING_DELIVERY`, and the plan-once architecture itself all landed in code.
`CARE_WHAT_YOU_STAND_ON` was tried and shipped OFF.
The delivery-deadline/ledger item was diagnosed only, not built, at this point (built next — see cash-ledger section).

---

### The cash-ledger bug (`short_of_cash` is one boolean, not a ledger)

source: the_day_is_a_cash_ledger.md — Alex, 2026-08-10, correcting the `sell_deadline` design built the same day

**The bug.** `schedule_agent.sell_deadline(hour, selling, short_of_cash)` returns one hour, and `short_of_cash` is one boolean over the whole day's bill:

```
short_of_cash = FUND_THE_DAY_WHEN_SHORT and any(owed_sale.values()) and _days_bill(row) > money
```

On day 4 that reads:

```
cow    400   needed at h0    <- covered by the $480 dawn bank, needs no sale at all
land  1000   needed at h21   <- the only thing the day's produce has to fund
hires   33   h0
wheat  ~28   h0
----------
      ~1461  vs $480         ->  short_of_cash = True  ->  due = 0, rush = True
```

A purchase not due until h21, and a purchase already paid for, are summed into one number and turned into "deliver everything at hour 0." That forces the rush on d4.

**What the day actually is** (read off tape 91422988, day 4, Seb's own seat):

```
h0    BUY_ANIMAL COW       -400      from the dawn bank
h0    HIRE x7               -33
h2    BUY_PRODUCT WHEAT    ~-28
h18   SELL WHEAT 5         +165
h21   SELL FERTILIZER 5, SELL WHEAT 12
h21   BUY_LAND            -1000      funded by the two SELLs in EARLIER ORDER SLOTS of this turn
h22   SELL WHEAT 12        +239
h23   SELL WHEAT 20, SELL FERTILIZER 1
```

He sits on $12 from h2 to h18 and it costs nothing, because nothing owed is due before h21.

Ours, same day, same board:

```
h0    BUY_ANIMAL COW, BUY_PRODUCT WHEAT      $480 -> $15 by h2
h6    SELL FERTILIZER 1, SELL WHEAT 1
h7    SELL WHEAT 1
h14   SELL WHEAT 8
h16   SELL WHEAT 16
h18   BUY_PRODUCT WHEAT 5                    -$154
h19   SELL WHEAT 5
h21   SELL FERTILIZER 2, BUY_LAND            -> $115
h22   --
h23   --                                     dusk $115 against his $1115
```

Two differences, both caused by the scalar: we sell early and small into a book that has not recovered, and we stop selling the moment the parcel is bought while he sells 12 more at h22 and 21 more at h23.

**The shape step 1 should have** (proposed, not yet built as of this doc): emit a ledger at dawn from the row and the live bank.
1. Dated obligations `[(hour, cash)]`, one per thing the row buys, at the hour it is bought (animals and hires at h0; land at its own hour; feed/seed buys at theirs).
2. Opening balance = the live bank, not the row's `money_dawn` (a different farm's number).
3. The shortfall curve: walk obligations in hour order against the balance; the first hour the running balance goes negative is the first hour the day genuinely needs a sale, and the deficit there is how much. Everything before it needs nothing.
4. Delivery obligations: turn each deficit into "this many units of this product in the SHED by this hour" — `cover`'s `due`, but as a list, not an int.
5. Sell waves: spread sells so the book recovers between them, and keep selling after the last purchase. `market_price` falls as town inventory rises — measured: landing a load in two DROP waves banked **$542 for 54 units**, where four waves banked **$774 for 41**.

Day 4 under that model asks for nothing before h21, then $1000 by h21, then sells the remainder at h22 and h23 — which is the tape.

**Why `feed 6/7` and `care 6/7` are downstream of this.** The cow lands at h0 and takes the bank to $15 by h2. The seventh animal's wheat is then unaffordable for the rest of the morning, so it is neither fed nor cared for. A cash-sequencing failure, not a routing failure — no amount of lane cutting closes it.

**Measured, so not to be re-derived:**
- Staggering the hires to keep hands off `(5,5)` is a LOSS on day 4 (reason in `_arrival_plan`'s docstring). Baseline d4 matches `water 17/17`, `harvest 14/14`, `place 1/1`; with staggering those go to 16/17, 12/14, 0/1. Two boxed hands cost d4 nothing measurable, because six seats already covered every tile.
- The tape boxes hands too: Seb's `u2` and `u6` sit on `(5,5)` doing nothing on d0, d1 and d3, and one of them on d2 and d4. It stops at d5, when he owns a second quadrant.
- `_days_bill` does count the cow. The bug was never a missing term; it was adding terms with different due dates together.

**Status: diagnosed and a design proposed by Alex. Not confirmed built in this doc** — treat the ledger shape as the fix direction, not a shipped change, unless later docs record it landing.

---

### The market cadence gap, across all products

source: the_market_cadence_over_all_products_2026-08-10.md — measured 2026-08-10, seed 11, tape `91422988`, crew planner on d0-d6

Method: ours = exact fills diffed out of `record_fills` after every step (what committed). His = the `orders` field of the derived schedule, read straight off his replay. Raw log: `data/logs/cadence_all.log`.
Both sides trade roughly the right quantities. The hours are wrong, in the same direction on every product.

**The table (hour-by-hour, ours vs seb):**

```
--- day 0 ---
  BUY_PRODUCT  WHEAT   ours h01x1 h02x1 h03x1 h04x1 h05x1 h06x1 h07x1 h08x1
                       seb  h05x1 h07x1 h09x1 h11x1 h12x1 h14x1 h17x1 h19x1

--- day 1 ---
  BUY_PRODUCT  WHEAT   ours h00x1 h01x1 h02x1 h06x1 h07x1 h08x1
                       seb  h01x1 h04x2 h06x1 h07x1 h12x1
  SELL         FERT    ours h06x1 h08x1 h09x1 h10x1        seb h04x2 h10x1 h12x1

--- day 2 ---
  BUY_PRODUCT  WHEAT   ours h00x1 h01x1 h02x1 h03x1 h04x1  seb h02x1 h04x1 h06x1 h08x2
  SELL         FERT    ours h07x1 h08x1 h12x1 h13x2        seb h15x3 h19x2

--- day 3 ---
  BUY_PRODUCT  WHEAT   ours h00x1 h01x1 h02x1 h03x1 h04x1 h05x1 h07x1
                       seb  h01x1 h03x1 h05x1 h06x1 h07x1 h08x1 h15x1
  SELL         FERT    ours h07x1 h12x1 h13x2 h14x1        seb h15x4 h18x1

--- day 4 ---
  BUY_PRODUCT  WHEAT   ours h00x1 h22x4                    seb h02x1
  SELL         FERT    ours h16x3 h18x3                    seb h21x5 h23x1
  SELL         WHEAT   ours h16x25 h21x8 h23x1              seb h18x5 h21x12 h22x12 h23x20

--- day 5 ---
  BUY_PRODUCT  WHEAT   ours h13x1 h18x4                    seb h17x2 h21x1
  SELL         FERT    ours h04x2 h13x2 h14x1 h18x2        seb h17x1 h19x3 h20x3
  SELL         WHEAT   ours h00x7                          seb  (none)

--- day 6 ---
  BUY_PRODUCT  WHEAT   ours h08x1 h12x1 h14x1 h16x1 h17x1 h18x3 h19x1
                       seb  h09x4 h11x1 h13x1 h15x1 h19x1
  SELL         FERT    ours h07x1 h12x1 h13x2 h19x1 h20x2  seb h09x2 h13x2 h14x2 h16x1
  SELL         WHEAT   ours h00x2 h07x1                    seb  (none)
  SELL         WOOL    ours h07x1 h19x5                    seb h09x6 h13x6

--- day 7 ---
  BUY_PRODUCT  WHEAT   ours h01x1 h02x1 h03x1 h18x5        seb h17x2 h22x1
  SELL         FERT    ours h05x1 h19x2                    seb h17x1 h22x3 h23x3
  SELL         WHEAT   ours h00x5                          seb  (none)
```

**Three general defects, none product-specific:**

1. **The carry dumps at hour 0.** `SELL WHEAT h00x7` on d5, `h00x2` on d6, `h00x5` on d7 — fourteen units at dawn across three days, against a schedule that asks for no wheat sale at all on any of them.
   It is `CUMULATIVE_SELLS` recovering d4's unfilled row: d4 asks for 49 and we fill 34, so 15 carry forward and go out on the next three dawns.
   Hour 0 is the worst hour available for it, for three reasons at once: the day's harvest has not happened yet, so the only stock is the herd's feed; the town has not drained the book, so the price is at its lowest; it is the same hour our own `BUY_PRODUCT WHEAT` fires, so we pay the spread on both legs.
   The reserve fix in commit `b52e210` stops this on d4, where the row places an animal. It does NOT stop it on d5-d7, because the carry is a different code path from the row.
2. **Sells fire in the morning; his fire in the evening.** FERTILIZER is the clearest, traded every day by both sides:
   ```
          ours                          seb
     d2   h07 h08 h12 h13               h15 h19
     d3   h07 h12 h13 h14               h15 h18
     d5   h04 h13 h14 h18               h17 h19 h20
     d7   h05 h19                       h17 h22 h23
   ```
   `townCenterSellInterval = 24` on this economy: the town drains the book once a day. Selling into an undrained book is selling into the bottom of the price curve. He sells after the drain; we sell before it.
3. **Buys are front-loaded into a block; his drip.** d0 is the extreme case — identical quantity, opposite distribution:
   ```
     ours  h01 h02 h03 h04 h05 h06 h07 h08     eight consecutive turns
     seb   h05 h07 h09 h11 h12 h14 h17 h19     spread across fifteen
   ```
   `BUY_DRIP` exists for this and meters one unit per turn, but it starts at h00 and runs out by h08. The shops restock every 4 steps, so his spacing buys each unit into a restocked book, and ours buys the second half into a book its own first half has already lifted.

**What it costs, where priced:**
- The d6 land parcel. He sells `WOOL 6` at h09 and `WOOL 6` at h13, taking his bank $5 -> $1,349, and buys the parcel at h13. We sell `WOOL 1` at h07 and `WOOL 5` at h19, hold $47 at h13, and do not reach $1,400 until h23. Same twelve units, ten hours late, and `buy_land 0/1` on d6 follows from it. This is why the crew planner READS AS costing the parcel; it does not.
- d4's wheat. `h16x25` in one order against his `h18x5 h21x12 h22x12 h23x20`. `market_price` falls per unit inside a single order, so a 25-lump clears at a materially worse mean than four blocks across four turns with restocks between them.

**What has NOT been measured:** whether moving sells later is worth it in money. Every number above is a timing observation. The obvious experiment — a `SELL_AFTER_HOUR` floor, and denying the carry hour 0 — is unrun. Two prior occasions on record where a cadence change that looked obviously right measured as a loss, so this gets a grid before an opinion.

**Status: diagnosed only, not built.** `b52e210` (partial fix for d4's carry-at-dawn case only) had already shipped; the general SELL_AFTER_HOUR / carry-hour-0 fix had not been run at time of writing.

---

### Tape-replay fidelity bug — the tape column does not reproduce his game

source: the_tape_column_does_not_replay_his_game_2026-08-09.md — measured 2026-08-09

Alex's position, stated correct: the tape is the JSON replay of the game he actually played; the schedule was derived from that JSON; if our harness disagrees with the tape, our harness is wrong. This had never been tested end to end before this doc.

**The measurement.** Push his own recorded actions for BOTH seats through a fresh env on seed 11 and compare, every turn, against the money recorded in his own replay:

```
weeds=0.0    first money divergence  turn 32 (d1 h8)  sim=188  rec=187   FINAL sim=10,264   recorded=110,820
weeds=0.005  first money divergence  turn 32 (d1 h8)  sim=188  rec=187   FINAL sim=11,711   recorded=110,820
```

His actions, his opponent's actions, his board — the simulation ends on **9%** of his real bank, and starts diverging on day 1, hour 8, by one dollar.

**Cause: replaying a pre-1.32.6 game under 1.32.6.** Turn 31, both sides otherwise idle, only his `BUY_PRODUCT WHEAT 1` on the book:

```
turn 30   246 -> 217   recorded charge 29   installed env charge 29
turn 31   217 -> 188   recorded charge 30   installed env charge 29   <-- the dollar
```

Installed `kaggle-environments` is 1.32.6; his replay predates the 2026-08-08 switch. The two price wheat differently. One dollar at d1 h8 compounds to $10,264 against $110,820.
`weedSpawnChance` is not the cause: 0.0 and 0.005 both diverge at the same turn and both end ~10x short.
Alex has stated this roughly ten times across sessions and been argued with every time. It is closed. `docs/REGISTER.md`'s OPEN-CLI already carried it as "1.32.6 test failures ... Both simulators fail parity on 1.32.6"; that entry and this doc are the same fact.

**What IS verified:** the starting board is exact — seed 11 reproduces his step-0 tiles cell for cell, same money, same town, so the seed choice is right and the divergence is not a different board. The schedule is derived correctly — against his recorded actions across 17 days, `builds` and `places` match every single day, zero mismatches, 19 builds against 19.

**What this invalidates.** `breakdown.py`'s tape column (`breakdown.py:274`) runs his actions forward in our env, both seats from the replay. Since that run diverges at d1 h8, the column is his action sequence executed into a state that stopped being his after day 1, not his game.
- State rows (money, tiles, pens, crops, herd) are not targets. His real melon reaches 18; the column shows 7. His real pastures reach 19; the column shows 8, flat, all season.
- Fill rows (sell, buy_product, buy_seed, buy_animal) run through a book that is no longer his, so they degrade too.
- Emitted-op rows are the least damaged (still literally his recorded actions), but the board they land on is wrong from d1 h8, so a refused or no-op action is counted where his succeeded.

Two rows chased in this session illustrate it: `melon 7/6` at d5 and `pens 9/8` at d5 both read as us over-buying. Neither is — the schedule's cumulative melon seeds are 7 by d5 and cumulative builds are 9 by d5, and we hit both exactly. The column is what is short.

**Prior record was wrong on three counts.** `.claude/skills/matching-the-tape` and `docs/REGISTER.md` both described this as a money contamination starting at d4, caused by the replayed Seb selling into a book we have lifted. Both were wrong: it starts at d1 h8, not d4; it affects state and fills, not just money; the tape run never faces our agent at all (`opp` is the replay's own seat 1). The skill also noted "$2 a day compounds, and the $2 on d1 was hiding a defect worth $1,590 on d6" — that d1 dollar was seen and filed as small; it is the same dollar as turn 32 here.

**Alex, 2026-08-09: the schedule is still the target.** Market prices vary between env versions; that is expected, not a defect to chase. The schedule (what to build, place, plant, buy, sell, on which day) is the portable thing derived from the replays. Money and realised fill prices are not portable and never will be. So the scoreboard for d0-d6 is our actions against the schedule (`test_our_sells_match_the_plan_every_day`, `test_our_buys_match_the_plan_every_day`, the per-day op rows), not our money against the tape column. Do not open a money gap as a defect.

**Next step named:** do not tune against the tape column until the replay reproduces his bank. First job: turn 32, one dollar, day 1, hour 8, with both sides playing his recorded actions. Not established whether this was subsequently fixed — no later doc in this set confirms it.

**Status: bug diagnosed, root cause identified (version skew, 1.32.2 replay vs 1.32.6 installed env). No fix recorded as shipped in this doc or the others in this set.**

---

### d4 sell shortfall and d9/d10 place 0/4 — measured 2026-08-10

source: fable_matching_the_tape_2026-08-10.md — measured on `tape seb2988`, seed 11, `weeds 0.0`, module `schedule_agent`, against `data/seed_scripts/top_guys/91422988.json` / `.../schedule.json`, branch `shaping-potential`.
Caveat carried in the source doc: the working tree was being edited by someone else, read-only, during this measurement session; `kagg/search/schedule_agent.py` changed mid-session (`FEED_DAYS 2->1`, new `WALK_THE_LOAD_HOME` flag, `CARE_WHAT_YOU_STAND_ON` False->True, a new `day` parameter into `_solve`) in the same territory as the Q1/Q2 findings below. Line numbers were re-checked after that edit landed; content at each cited location was unchanged.

#### Q1 — why d4 sells only ~41 of 55 while Seb sells 55

Measured. Not the order book, not the price curve, not "produce not in the shed." It is the agent's own `DUSK_FEED_TOPUP` block re-buying wheat the sell block just sold, same turn, from hour 18 onward.

Baseline (`python -u scripts/breakdown.py --module schedule_agent --tape seb2988 --days 7`, d4 column):
```
sell         41/55       buy_product   21/1
```
Schedule row for d4 (`schedule.json` key `"4"`): `"sells": {"WHEAT": 49, "FERTILIZER": 6}` (=55), `"buys": {"WHEAT": 1}`. 5+12+5+12+20+1 = 55 sums exactly from his own recorded orders. This IS a real target.

His d4, hour by hour (`data/logs/fable_d4_trace.log`):
```
d4h18  shed WHEAT=1        orders=[SELL WHEAT 5]                       -> FILLED SELL 5
d4h21  shed WHEAT=7        orders=[SELL FERTILIZER 5, SELL WHEAT 12, BUY_LAND]  -> FILLED SELL 17
d4h22  shed WHEAT=7        orders=[SELL WHEAT 12]                      -> FILLED SELL 12
d4h23  shed WHEAT=7        orders=[SELL WHEAT 20, SELL FERTILIZER 1]   -> FILLED SELL 21
```
WHEAT sold: 5+12+12+20 = 49. FERTILIZER: 5+1 = 6. Total 55, exact match to schedule row. No BUY_PRODUCT after h2.

Ours, same day (same log):
```
d4h14  SELL WHEAT 8                      -> FILLED SELL 8
d4h17  SELL WHEAT 8, SELL FERTILIZER 1   -> FILLED SELL 9
d4h18  BUY_PRODUCT WHEAT 6               -> FILLED BUY_PRODUCT 6
d4h19  SELL WHEAT 6, BUY_PRODUCT WHEAT 1 -> FILLED SELL 6, FILLED BUY_PRODUCT 1
d4h20  SELL WHEAT 8                      -> FILLED SELL 8
d4h21  BUY_PRODUCT WHEAT 6               -> FILLED BUY_PRODUCT 6
d4h22  SELL WHEAT 6, BUY_PRODUCT WHEAT 1 -> FILLED SELL 6, FILLED BUY_PRODUCT 1
d4h23  SELL WHEAT 1, BUY_PRODUCT WHEAT 6 -> FILLED SELL 1, FILLED BUY_PRODUCT 6
```
WHEAT sold: 2(h0)+8+8+6+8+6+1 = 39, FERTILIZER 1+1 = 2, total 41 — matches breakdown row exactly. BUY_PRODUCT WHEAT total: 1(h1)+6+1+6+1+6 = 21 — also matches (`buy_product 21/1`).

**Mechanism, proved from the code.** From hour 18 on, every turn both sell wheat AND buy it straight back, same turn.
`DUSK_FEED_TOPUP` (`kagg/search/schedule_agent.py:3606-3634`), re-evaluated every turn:
```python
if (DUSK_FEED_TOPUP and day >= DUSK_FROM_DAY and hour >= DUSK_FEED_HOUR
        and len(orders) < 9):
    arriving = len((sched.get(day + 1, {}) or {}).get("places") or [])
    gap = (alive + arriving) - int(shed.get("WHEAT", 0))
    gap = min(gap, FEED_TURN_CAP, int(money // quote))
    if gap > 0:
        orders.append(["BUY_PRODUCT", "WHEAT", gap])
```
`DUSK_FEED_HOUR = 18`, `DUSK_FROM_DAY = 2` (`:576`, `:580`), `FEED_TURN_CAP = 6` (`:546`). On d4, `alive` = 7 (cow 5 + sheep 2). d5's schedule row has `"places": []` so `arriving = 0`. The SELL order is appended earlier in the same turn's order list; within `_process_market` (`reference/kaggriculture.py:550`, `for i in range(max_len)` walks order SLOTS — SELL is slot 0, BUY_PRODUCT a later slot), SELL settles completely before BUY_PRODUCT is quoted (`:570-613`). So the sell drains the shed toward zero, then the SAME turn's dusk topup sees `shed=0`, computes `gap=7`, caps at `FEED_TURN_CAP=6`, buys 6 straight back. Next turn (h19) the sell block sells 6 of it right back down, gap recomputes to 1, a 1-unit topup fires again. Repeats h21-h23. Every BUY_PRODUCT logged for d4 lands in this window (h18, h19, h21, h22, h23) — five of six buy events — plus one feed-drip buy at h1 from a separate block (`:3566-3604`).

The sell block itself already tries to hold back a feed reserve before offering wheat (`:2909-2933`):
```python
have = max(0, have - max(0, feed_days(day) * alive - carried_wheat - drawn - will_buy))
```
`feed_days(day) * alive` = 1*7 = 7 for d4 — the SAME floor `DUSK_FEED_TOPUP` targets. But the sell-side reserve nets off `carried_wheat` and `will_buy`, while `DUSK_FEED_TOPUP`'s own comment (`:3610-3615`) argues the opposite — hand-carried wheat should NOT count, because it may be drawn for a pen before the overnight rollover returns it to the shed (its own change note: "d4 we harvest 14 wheat, it is still in hands at h18, and the top-up ordered 21 units against a tape that buys 1"). Two blocks target the identical number (7 = alive) from two different bases, each blind to what the other has already reserved.

Ruled out: order-book/slot mechanics (every turn carries 1-2 market orders, nowhere near `maxMarketOrdersPerTurn = 10`, `reference/kaggriculture.py:538`). Ruled out: "produce not in the shed" — harvest counts match 14/14 on d4; the unit phase (HARVEST+DROP) runs before the market phase within the same turn (`reference/kaggriculture.py:922` then `:928`) and refills the shed in time for that turn's SELL, true for both sides.

End-of-day wheat is 0/0 both sides — the 14-unit shortfall (55 vs 41) is wheat bought back and fed to animals, not wheat that vanished. Cost is the spread, paid twice on ~20 units a day from h18 on, plus each round trip occupies an order slot and a market-lockstep iteration that buys nothing. Money at d4 end: 774/1063 (ours/tape), a ~$289 gap, consistent with a repeated wash trade though not isolated exactly how much of the gap is this mechanism versus everything else that differs by dusk.

**Status: diagnosed only, not fixed.** Read-only investigation; fix shape proposed (make `DUSK_FEED_TOPUP`'s floor agree with what the sell-side reserve already believes is reserved) but not implemented in this doc.

#### Q2 — is the fix to match the work order (harvest early, deliver, sell in bursts), not the sell block?

Measured evidence says no. HARVEST counts already match exactly (d4: `harvest 14/14`). Wheat already reaches the shed the same turn a SELL clears it, on both sides (proved above). The defect is entirely on the market-order side (two independent feed-reserve computations), not on tour order / work sequencing. Reordering what the crew does on tiles would not touch either block.

#### Q3 — why cover leaves 8 of 10 d9 placements unassigned, and the 2 routed emit nothing

Measured, three layers, chaining into one cause. `place` reads 0/4 on both d9 and d10. Not a turn-budget problem: d9 measured 277 unit-turns of budget against 155 used, 122 turns free (`scratchpad/d9_place_trace.py`, `data/logs/fable_d9_place_trace.log`) — note this is a DIFFERENT number from the "101 idle unit-turns" figure quoted in the original prompt; the two were not reconciled but support the same conclusion (large free capacity, ruling out turn-budget).

**Layer 1 — all 10 open pens typed "PLACE COW", none "PLACE SHEEP".** Instrumented `cover.cover()` for the day-9 dawn solve:
```
total jobs offered=53   PLACE jobs among them=10
  PLACE job: tile=(4,1) ops=[('PLACE','COW'),('FEED','WHEAT'),('CARE',None)] ...
  ... (all 10, every one COW) ...
supply given to cover()={..., 'COW': 2, 'SHEEP': 2, ...}
PLACE jobs routed: 2 / 10
```
Schedule's own d9 row asks for `['COW','COW','SHEEP','SHEEP']` — two of each — but zero of the ten offered nodes are typed SHEEP. Comes from `router.build_nodes`'s PASTURE/COOP tie-break (`kagg/search/router.py:836-865`): an open pen with no specific reservation iterates `R.ANIMAL_NAMES = ["GOOSE","COW","SHEEP"]` and takes the first species with nonzero shed/supply — COW whenever both present, a behavior the code's own comment already documents as measured and accepted in isolation. Combined with `cover()`'s supply gate (`affordable()`, `kagg/search/cover.py:812-816`, `stock[COW] = 2` from `plan_supply`), only 2 of the 10 identically-typed COW claims can ever be affordable — not because turns are scarce, but because the model believes only 2 COWs exist and none of the ten nodes is typed SHEEP.

**Layer 2 — the animals the model expects were never bought.** `plan_supply` (`schedule_agent.py:1562-1568`) credits `sched[day]["animals_bought"]` (`{COW:2, SHEEP:2}` on d9) into the dawn plan's supply, under `PLAN_TODAYS_PURCHASES = True` (`:260`). But actual `BUY_ANIMAL` orders come from a separate, later block, `SHOP_ADAPT_HERD` (`:2067`, active from `SHOP_ADAPT_FROM_DAY = 6`, `:2088`, active on both d9 and d10), which re-derives the COW/SHEEP split from live market headroom rather than reading the schedule's per-day species mix (`:3317-3404`). Measured directly:
```
d9h 0  BUY_ANIMAL SHEEP 1     d9h7  BUY_ANIMAL SHEEP 1, SHEEP 1     d9h12 BUY_ANIMAL SHEEP 1
d10h0  BUY_ANIMAL SHEEP 1, SHEEP 1     d10h16  BUY_ANIMAL SHEEP 1, SHEEP 1
```
(`data/logs/fable_d9_shed_cow.log`, `fable_d10_shed_cow.log`). Zero `BUY_ANIMAL COW` orders fire either day. Shed COW reads 0 every hour of d9. `buy_animal` fills still read 4/4 both days in the breakdown table because the COUNT matches Seb's — only the species differs, exactly what `SHOP_ADAPT_HERD`'s own docstring says it is designed to do (`:3317-3318`). Already flagged in `docs/REGISTER.md` OPEN-CLI ("Shop-adaptive herd shipped and measured; floors still open"); this doc adds the specific causal link to `place 0/4`.

So the dawn plan is built against a purchase that never happens: 10 pens typed and routed assuming 2 COWs arriving; 0 COWs ever arrive; the 4 SHEEP that do arrive all day are never offered as a placement target, because no node was ever typed SHEEP.

**Layer 3 — the 2 routed jobs draw against an empty shed and are abandoned, silently.** The 2 jobs `cover()` does route are planned correctly at the routing layer (`scratchpad/d9_solve_trace.py`, `data/logs/fable_d9_solve_trace.log`):
```
LOCAL unit 1  start=(5,4)
    Shed(5,4)[COWx1+WHEATx2]
    Job(5,4)['PLACE','FEED','CARE']  needs=Counter({'COW': 1, 'WHEAT': 1})
    Job(4,4)['FEED','CARE','COLLECT_FERTILIZER','HARVEST']
    Shed(4,4)[DROP]
```
Cross-referenced against the turn-by-turn execution trace (`data/logs/fable_d9_place_execute_trace.log`): the unit at `(5,4)` at hour 1 emits `PICKUP WHEAT 2` and never picks up a COW. A season-wide scan (`data/logs/fable_d9_all_units_trace.log`) confirms COW and SHEEP never enter any hand's inventory, and PLACE never fires at any point on d9, even though real SHEEP sit in the shed by hour 1. The COW half of the depot draw fails because the shed never holds a COW (Layer 2); the executor does not retry or reroute around a failed draw unless the job is `critical` — `Depot.critical` is set only when `at_risk and required` (`cover.py:330-335`, `:585-587`); the PLACE job here is `required=True` but `at_risk=False`, so `critical=False`. Combined with "the day is planned once, no replan" (project-wide rule), the fixed route never revisits `build_nodes` later in the day, so the 4 real animals purchased that day are never routed to a pen either.

**Net chain:** `SHOP_ADAPT_HERD` buys the wrong species (by design) -> `plan_supply`/`build_nodes` tie-break still assume the schedule's species mix, so every open pen is typed for a species that will not arrive -> `cover()`'s supply gate caps routing at the phantom count -> the 2 it does route chase a COW never in the shed and get silently abandoned, non-critical -> 0 PLACE ops fire, 8 of 10 jobs never attempted, 4 real SHEEP stranded with no node ever typed to receive them.

**Status: diagnosed only, not fixed** (read-only investigation; no test or fix written per the source doc's own scope). Not verified: whether `SHOP_ADAPT_HERD`'s species reallocation is a good idea in aggregate (already logged shipped-and-measured elsewhere) — only that it is the direct, provable cause of `place 0/4` here.

---

### How Seb's planner works — route reconstruction

source: how_sebs_planner_works_2026-08-10.md — measured 2026-08-10 off four tapes, by reconstructing positions from recorded observations paired with the action emitted from each. Not inferred from op counts; every claim is a route.

**1. The opening is open-loop, and it stops the day the shop speaks.**
Every farmer and hand action is identical across all four tapes for the first 96 turns:
```
per-day agreement across all four tapes (turns of 24 with an identical unit action)
  d0  units 24/24   market 24/24
  d1  units 24/24   market 24/24
  d2  units 24/24   market 24/24
  d3  units 24/24   market 22/24
  d4  units  1/24   market 17/24
  d5  units  1/24   market 10/24
  d6+ units  0-1/24
```
Four seeds (`1012428555`, `231975074`, `658760367`, `1440180345`), four opponents (Valmorlee, Pranshu Ghori, kakuteki, Leon Christians), both seats, both economies (`townCenterSellInterval` 12 and 24), all `weedSpawnChance 0.005`. Confirmed independently by replaying those 96 turns on seeds 11, 7, 123, 999 and 20260810: board and crew size come out identical every time.
It stops at d3/d4 because `townShopUnlockInterval = 3` — d3 is the first day a shop unlocks (`91422988` d3 opens with `shops ['ICE_CREAM_SHOP']`), the first information the agent has.
The unit streams part at t97 (d4 h01): `90494364` has an EIGHTH hand there — the richer `sellInterval 12` economy could afford one more hire, so the crew is a different size, so every route after it differs. The other three stay identical for 121 turns, through d5 h00.
**The only closed loop in the opening is `market -> money -> hire count -> crew size`, and the crew size sizes the plan.**

**2. A hand is given a role for the day, and it keeps it.** Work ops only (moves/passes dropped), `91422988`, d11:
```
u1  PURE crop  7/7    WATERx6 PLANTx1
u6  PURE crop  9/9    WATERx6 PLANTx3
u9  PURE crop  8/8    WATERx6 HARVESTx1 PLANTx1
u11 PURE crop  9/9    WATERx6 PLANTx3
u12 domi herd  8/10   CAREx3 COLLECT_FERTILIZERx3 FEEDx2 BUILD_PASTUREx1 PICKUPx1
u3       herd  7/11   CAREx3 FEEDx2 COLLECT_FERTILIZERx2 PICKUPx1 BUILD_PASTUREx1 PLANTx1 WATERx1
u8       haul  5/12   DROPx3 FEEDx3 PICKUPx2 HARVESTx2 CAREx1 COLLECT_FERTILIZERx1
```
Four roles, mixing almost entirely within a role: waterer (WATER/PLANT/HARVEST, never touches an animal); feeder (PICKUP WHEAT -> FEED -> CARE); collector (CARE -> COLLECT_FERTILIZER -> DROP, one pen round trip); builder (BUILD_PASTURE, PLACE, day 0 and land days). PICKUP/DROP/PLACE on a herd hand is the load that role carries, not a second assignment.

**3. A hand owns a tile end to end, and a contiguous run of them.** PLANT and WATER emitted on consecutive turns at the same position, every time; tile never revisited.
```
d0  u6  spawn(4,5)  h03(3,4)PLANT[WHEAT] h04(3,4)WATER  h06(2,4)PLANT h07(2,4)WATER
                    h09(1,4)PLANT h10(1,4)WATER  h12(0,4)PLANT h13(0,4)WATER
                    h15(0,3)PLANT h16(0,3)WATER  h18(0,2)PLANT h19(0,2)WATER
```
A lawnmower sweep down column y=4 then along row x=0 — a contiguous block handed to one hand at dawn, walked in order. Same shape on other crop hands:
```
d0  u2  (4,1)MELON (4,0)WHEAT (2,0)WHEAT (0,0)WHEAT
d0  u4  builds (4,3)(3,3)(3,2)(2,2) then plants (2,1)(1,1)(0,1)
d0  u5  (3,1)MELON (3,0)WHEAT (1,0)WHEAT then builds (1,2)(2,3)
```
The farmer (u0) never leaves the shed's 3x3 on d0: BUILD_PASTURE, PICKUP, PLACE, CARE.
**This is the difference from ours:** we hold one global priority queue, every hand eligible for every op, re-ranked at every stop. Measured over a full season, our agent loses 16 plants to thirst (14 strawberry, 2 melon), every one after d9, while losing exactly one animal.

**4. He does not fill the turns, and that is deliberate.**
```
 day  crew  slots  turns  work  move  pass  idle-all-day  work%
   0     7      8    178    60    60    58             2  33.7%
   1     7      8    178    25    29   124             2  14.0%
   2     7      8    178    38    64    76             1  21.3%
   3     7      8    178    37    47    94             2  20.8%
   4     7      8    178    61    88    29             1  34.3%
   5     7      8    178    51    98    29             0  28.7%
  ...
  11    12     13    286   122   158     6             0  42.7%
  15    12     13    284   123   161     0             0  43.3%

d0-d16 totals: work 1277 (32.7%)  move 1917 (49.1%)  pass 707 (18.1%)
```
Two hands stand still for the whole of d0 and d3. Day 1 is 124 PASS turns out of 178 — the crew does 25 work ops all day, because everything planted on d0 was watered on d0 and `consecutive_unwatered >= 2` means d1 can simply be skipped. A hand that finishes its block idles; it is not reassigned.

**5. Where the headroom is.** 707 idle turns over d0-d16, 124 of them on d1 alone. 49.1% of all turns are walking; work is 32.7%. The early days are loosest: d1-d3 run 14-21% work against 40%+ from d11. None of this argues his plan is bad — it wins. It argues the ceiling above this plan is high, and that a planner built the same way (role per hand, contiguous block, idle when done) has room to beat it without needing to be cleverer per turn.

**What this implies for our planner (proposed, not built as of this doc):**
1. Assign a role and a contiguous block to each hand at dawn. Do not re-rank globally.
2. Emit PLANT+WATER as one owned tile, not two independent jobs.
3. Let a hand idle when its block is done. Filling turns is what drags waterers onto feeds.
4. d0-d3 needs no board reading at all — it is a constant; crew size is the only output that matters to d4.
5. From d4 the input is the shop unlock and the bank: which animal is buyable, and whether the extra hire is affordable.

**Status: diagnosis and architecture recommendation only. No fix confirmed shipped in this doc.**

---

### How Seb feeds seven animals on day 4

source: how_seb_feeds_the_herd.md — read straight off tape 91422988, seed 11, Seb's own seat, day 4.
He scores `FEED 7`, `CARE 7`, `PLACE 1`, `COLLECT_FERTILIZER 6`. We score `FEED 5`, `CARE 5`, `PLACE 1` from the same board.

**The shape of his day.** Three pickups, all in the first two hours, three different hands:
```
h1  u1  PICKUP WHEAT 3
h2  u2  PICKUP WHEAT 3
h2  u6  PICKUP COW 1
```
Seven drops, none before hour 18: `h18 u7 | h21 u2, u3, u6 | h22 u5 | h23 u0, u1`.
The shed runs 6 -> 3 -> 1 in the first two hours and sits on 1 until h18, when the harvest lands. He empties it deliberately and never goes back.

**Three roles, not one:**
- u1 — wheat carrier A: draws 3 at h1, spends them walking outward (`h1 (4,4) PICKUP W3, h2 (4,4) FEED, h4 (4,3) FEED, h7 (3,2) FEED, h8 (3,2) CARE, h9 (3,2) COLLECT_FERTILIZER`, then crop work to dusk).
- u2 — wheat carrier B: draws 3 at h2, sweeps a different arc (`h2 (4,4) PICKUP W3, h5 (3,3) FEED, h9 (2,2) FEED, h14 (1,3) FEED`, with CARE and COLLECT_FERTILIZER at each, then south to the shed).
- u6 — animal carrier and CARE sweeper: draws the COW at h2 and carries it ten hours, doing the itemless work at every pen passed (`h2 PICKUP COW 1; h3 (4,4) CARE; h4 COLLECT_FERTILIZER; h6 (4,3) CARE; h7 COLLECT_FERTILIZER; h9 (3,3) COLLECT_FERTILIZER; h12 (1,3) PLACE COW; h13 (0,3) WEST; h14 WATER; h15 HARVEST`).

**Three rules this implies:**
1. Load once, in parallel, at dawn. Two carriers take the whole shed between them in hours 1-2. No second trip, no mid-day DROP, so no wheat is ever put back into a shed another hand has already emptied.
2. The hand with no wheat does the work that needs no item. CARE costs nothing to carry, so the animal carrier pays for its long walk by caring for every pen it crosses.
3. A pen's day is SPLIT ACROSS HANDS, and the feed arrives after the placement. u6 places the cow at `(1,3)` at h12; it does not feed it. u2 feeds it at h14, two hours later, on wheat drawn at h2 for a pen that had no animal in it at the time.

**Why rule 3 matters.** `crew.cover`'s docstring states the opposite as a design principle: "The unit of ownership is the TILE, not the op. A pen's whole day — build it, put the animal in, feed it, care for it, take the fertilizer — belongs to one hand." Its second justification: an animal placed today must be FED today, and `build_nodes` cannot emit a FEED for a tile until an animal is standing on it, so the feed is invisible at plan time. Seb's answer is not to give the pen to one hand — he sends a second hand, already carrying wheat, past the pen later in the day than the hand that filled it. The feed is not invisible to him because it is not planned as part of the placement at all; it is one stop on a wheat carrier's sweep, timed to arrive after the placement.
Tile ownership is not wrong — it fixed a real pairing failure (`place 3/4`, `feed 3/4`, d3 bank $28 against $478). But it is what forces the placing hand to carry its own feed, which forces the mid-tour re-supply DROP, which loses the wheat.

**What it costs us on day 4.** Our herd hand u4 does all three roles alone:
```
h1 PICKUP COW 1   h2 PICKUP WHEAT 4   h3 FEED (4,4)   h4 CARE
h6 DROP           h7 PICKUP COW 1     h8 PICKUP WHEAT 1   <- asked 3, got 1
h10 FEED (4,3)    h11 CARE            h14 PLACE COW (3,3)   <- arrives empty
h15 walks off; the cow is never fed or cared for
```
`DROP` is all-or-nothing (`kaggriculture.py:333`), so the h6 re-supply dumps the cow too and pays to pick it up again. By h8 the shed holds 1 wheat, the leftover want is deleted (`schedule_agent.py:1761`), and the shed is bare h9-h18, so `FETCH_THE_FEED_AND_RETURN` cannot fire either.
Wheat ledger, both sides: 6 in the shed at dawn, 1 bought during the day, 7 animals. He buys exactly what we buy. He is not better funded; he simply never spends a wheat on a round trip.

**Open questions, not resolved in this doc:**
- Seb performs 7 FEEDs having drawn only 6 wheat. u7 feeds `(2,3)` at h7 without ever visiting the shed, so it began the day holding wheat. Not yet confirmed whether the midnight sweep (`_drop_inventories_to_shed`) leaves a remainder in hand or whether the seventh wheat comes from somewhere else. **Not established.**
- Between our h6 DROP and our h8 re-pickup, one wheat AND the collected fertilizer both disappear from the shed. Either the drop overflowed shed capacity (overflow discarded outright, `kaggriculture.py:340`) or another hand drew them. Not yet separated — matters, because if it is capacity, the round trip is destroying goods, not merely costing turns. **Not established.**

**Status: diagnosis only. No fix recorded as built in this doc.**

---

### Tape repointing: `seb` -> `seb1326`, and re-deriving every asserted day

source: router_tape_repoint_2026-08-09.md — Task #53, `tests/test_router.py`

`TAPE_REPLAY` / `TAPE_SCHEDULE` / `TAPE_TEAM` (added commit `a34cc1e`) repointed from `data/seed_scripts/top_guys/90494364` (`seb`, played on 1.32.2) to `data/seed_scripts/top_guys/90976060` (`seb1326`, played on 1.32.6). Note: `seb1326` is itself later identified as Seb's interval-12-shaped low-wheat build that he kept running after the town rebalance — the same tape whose bank halved (see status note at top). The two tapes land quadrants on different days (5/9/11 vs 4/6/10), carry different pen counts (~19 vs 21), and re-cut the herd from wool to milk (MILK 179->303, WOOL 230->104, MELON 132->96), so every day-specific number in the test file had to be re-derived, not merely re-run.

**Method.** Two temporary scripts (not committed, logs under `data/logs/`): `tape_truth.py` replays the leader's own recorded actions against his real recorded opponent from the episode JSON — deterministic given seed+actions, so it reproduces the historical episode exactly (output: `data/logs/tape_truth_90976060.log`, dawn bank/sells/op tallies/seed peaks/first-sell/first-buy hours per day 0-11). `day_by_day_diff.py` runs the same replay for the tape's actions and for `schedule_agent`-driven ours (against the same real opponent sequence) and diffs the op tally per day (output: `data/logs/day_by_day_diff.log`).
Sanity check: replaying the OLD tape's own actions under current 1.32.6 gives dawn day 6 = $1,855, matching the number already in the `TAPE_REPLAY` comment block before this pass. Same method, same answer.

**Finding that changes the triage shape: days 0-3 are no longer exact under `seb1326`.** The day-4 gate's docstring had claimed "days 0-3 already exact" — true of the old tape, false of the new one. Op-for-op diff, our agent vs the tape's own replayed actions, days 0-3:
```
day 0: {'FEED': '1/4', 'CARE': '1/4', 'SELL': '7/0'}
day 1: {'SELL': '2/4'}
day 2: {'SELL': '6/5'}
day 3: {'FEED': '4/6', 'CARE': '4/6', 'SELL': '7/5'}
```
So day 4's shortfall inherits upstream drift; not separately gated (no day-0/1/2/3 op-for-op test exists; day 0/1's own gates are `@pytest.mark.skip`d for an unrelated tour-shape reason).

**Per-test outcomes:**
| Test | Verdict | Number / finding |
|---|---|---|
| `test_a_carried_sell_row_never_offers_more_than_the_biggest_day_ever_asked` | real gap, untouched | Hand-built harness, no tape reference. `sched[0]["sells"]={"MELON":5}` twice, shed holds 20; agent offers `SELL MELON 20` instead of capping the carry at 5. Pre-existing bug, independent of the tape. Out of scope (`schedule_agent.py` owned by another agent). |
| `test_a_hand_full_of_the_days_sell_row_walks_it_in_when_there_are_turns_to_spare` | real gap, untouched | Hand-built harness. Unit holding MELON 12 with 12 turns of slack and a 5-turn detour home emits NORTH instead of EAST/SOUTH — never triggers `DELIVER_FERRY`. Pre-existing, independent of the tape. |
| `test_the_sells_row_is_a_day_total_not_a_per_turn_quota` | re-derived, still a real gap | Day 4 target changed `{WHEAT:28, FERTILIZER:4}` -> `{WHEAT:49, FERTILIZER:6}`. Agent currently delivers `{FERTILIZER:3, WHEAT:19}` — well under. Gap traced to HARVEST/WATER shortfall — less produce exists to sell. |
| `test_the_feed_top_up_counts_wheat_already_standing_ripe_in_the_field` | re-derived, now passes | Day 4 target changed `bought == 0` -> `bought == 1`. Agent already buys exactly 1. |
| `test_day_four_matches_seb_on_every_op_it_works` | real gap, docstring corrected | `HARVEST 11/14`, `WATER 12/17`, `SELL 22/55` (ours/tape). Also corrected the false "days 0-3 already exact" premise. |
| `test_the_biggest_sale_takes_the_earliest_slot` | re-derived (assertion dropped), now passes | Slot-order invariant kept (passes unmodified). Dropped `dawn6 >= 860` — day 6's seed row is `{}` under `seb1326`; tape's own dawn-day-6 bank, replayed, is $0; ours is $26 — already ahead. |
| `test_wheat_drawn_this_turn_is_the_herds_reserve_not_extra_to_it` | deleted | Day 5's row is `sells: {FERTILIZER: 5}` under `seb1326`, no WHEAT key, so the race this test measured doesn't occur. Agent still sells 10 unrequested wheat that day — possibly the same carry-logic family, but a different, unopened question. |
| `test_day_six_gets_a_load_to_the_shed_early_enough_to_fund_the_strawberry` | deleted | Day 6 has neither `animals_bought` nor `seeds` under `seb1326` (both `{}`) — no $800 bill to fund by hour 2. Was `xfail(strict=True)`, had started silently XPASSing from an unrelated hour-0 FERTILIZER carryover sale. |
| `test_day_six_sells_the_wool_as_soon_as_the_walk_allows` | deleted | Same day-6 board change; specific sheep-pen geometry (`(1,4)`/`(3,4)` vs tape's `(4,4)`/`(4,3)`) belongs to the old tape's day 6, no longer this shape. Also spuriously XPASSing. |
| `test_day_six_plants_every_tile_the_row_asks_for` | re-derived, still a real gap | Day 6 target changed `planted == 14` -> `planted == 4`. Agent plants 6 — over-planting, not the old under-planting bug. |
| `test_the_days_seed_is_bought_before_the_days_livestock` | deleted | Day 6 has neither `animals_bought` nor `seeds` under `seb1326` — the funding race this test measured doesn't occur that day. Mechanism still exists in code; days 9 and 11 both carry simultaneous rows and could host a rebuilt version, but needs a fresh hour-by-hour trace not done in this pass. |

**Result: 72 tests collected (was 76; 4 deleted). 5 failing, all real gaps, none newly discovered:**
```
FAILED test_a_hand_full_of_the_days_sell_row_walks_it_in_when_there_are_turns_to_spare
FAILED test_a_carried_sell_row_never_offers_more_than_the_biggest_day_ever_asked
FAILED test_the_sells_row_is_a_day_total_not_a_per_turn_quota
FAILED test_day_four_matches_seb_on_every_op_it_works
FAILED test_day_six_plants_every_tile_the_row_asks_for
```
61 passed, 6 skipped (unrelated, pre-existing tour-shape skips). Confirmed by deselecting the 5 known-red tests and re-running the rest clean.
No fix moved a threshold to whatever the code currently produces — every changed number traces to `schedule.json`'s own row for that day, cross-checked against a full replay of the tape's own recorded actions against its real recorded opponent.

**Status: test-suite repoint shipped** (the fixture repoint itself, the 4 deletions, and the re-derived assertions all landed in `tests/test_router.py`). **The 5 failing gaps themselves are diagnosed, not fixed.**

---

## Victor / Kawashigi / tetsuya lineage, 2026-08-11 to 2026-08-14

From 2026-08-11 the diagnostic target shifted from the Seb tape to Victor, kawashigi, and tetsuya.
All measurements below are seed 11 unless stated otherwise.
Each finding is tagged with its source file and date.

### d4/d5: the spawn step-off deletes the depot draw

Source: fable_the_d4_d5_planner_2026-08-11.md, 2026-08-11.

`acts[0] = [step_off]` overwrites the farmer's hour-0 action after the router has already walked the route for that hour.
On d4 the overwritten action was `PICKUP WHEAT 2`.
The route believed the wheat was drawn.
It was not.

The tour was costed at 21 turns against a 24-turn budget.
The bug added 6 unpriced turns: 2 for the step-off round trip, 4 for the recovery fetch.
21 + 6 = 27, over budget by 3.
The dropped tail stop cost d4 `water 14/15` and `harvest 4/5`.
It also cost d5 `plant 4/5` and `strawb 6/7`.

Fix shipped as two deltas in `kagg/search/schedule_agent.py`, flagged EXPERIMENT:
- Delta 1 (`hold_farmer`): when the call site overwrites the farmer's action, the router must not walk the route that turn.
- Delta 2 (`farmer_start`): also cut the tour to start one turn poorer, from the stepped tile.

Two earlier reverted attempts, for the record:
- Removing the step-off entirely re-ran the spawn rotation and idled a hand 23 turns on d3-d5.
- "Only overwrite a MOVE" suppressed the step on exactly the days the bug fires, wrecking d3.

After the fix, d4 and d5 match the tape on every non-exempt row except d5 `dig 0/1` (the tape digs an unconditional script action; our board has no weed there, so 0/1 is correct) and a pre-existing sell shortfall.
The first divergence moves from d4 to d6.

A second finding in the same file: a PLANT whose same-day WATER cannot also execute converts a seed into a weed.
`consecutive_unwatered` starts at 1 on planting day (`kaggriculture.py:209`) and weeds at 2 (`:766-771`).
Measured: tile (5,3) went LOCKED -> None (d6 h13) -> WEED (d7 h23) without ever being watered.
Not yet encoded as a rule.

### d7: the dawn wheat block is dropped for a full order queue

Source: fable_the_d7_feed_2026-08-11.md, 2026-08-11.

The dawn plan sizes the h00 wheat order at the full 14-unit row (`BUY_THE_ROW_AT_DAWN`).
The bank covers it: $2,512 at h00.
The order is dropped because d7's h00 queue already holds 10 orders and the append gate is `len(orders) < 9`.
From h01 the boost expires (`hour == 0` only) and the row falls back to `BUY_DRIP = 1`/turn.
Result: d7 closes `feed 9/10`, `care 9/10`, `collect_fert 6/7`.

Every day from d7 with a big hire row drops its dawn block: d8 (`norders=9`), d9 (10), d11 (10), d12 (10).
d8/d9 `feed 11/12`, `care 11/12` carry the same signature.

Fix shipped in `kagg/search/schedule_agent.py`: the boost condition becomes `not state.get("dawn_row_sent", False)`, set True at the append (even a money-shrunk partial send), reset daily.
Days whose h00 block already goes out (d0-d6) are bit-identical.
Measured: d7 `feed 9/10 -> 10/10`, `care 9/10 -> 10/10`, `collect_fert 6/7 -> 7/7`.
d8-d10 moved toward the tape (d10 `harvest 5/6 -> 6/6`, `money 3719 -> 5230` against tape 5630).
d0-d6 byte-identical.

Ruled out, do not retry: waiting at the depot (upstream cadence problem, not downstream patience); marking the FEED draw critical (would deform the tour the same way the d4/d5 bug did); re-slotting the queue ahead of hires (the tape itself does not do this).

### Where next: priorities set 2026-08-11

Source: fable_where_next_2026-08-11.md, 2026-08-11.

The "arithmetically impossible" money gap was closed: it was two different games' numbers mixed into one equation.
Our own numbers reproduce exactly: sell fills 1,159 units / $93,298, net trade $71,734, final bank $64,730 = 3000 + 71,734 - 10,004.
Victor replayed: 1,434 units / $112,925, net trade $90,315, bank $83,311.

Net-trade gap decomposed by product (ours minus Victor, same seed/opponent):
- STRAWBERRY: 213u/$24,107 ($113/u) vs 274u/$46,430 ($170/u) — delta -$22,323 (the biggest single line item; a late dump problem, not a volume-only problem)
- WHEAT: 313u/$14,009 vs 446u/$18,957 — delta -$4,948
- MELON: 102u/$13,376 vs 114u/$16,542 — delta -$3,166
- FERTILIZER: 201u/$12,903 vs 237u/$13,772 — delta -$869
- WOOL: 134u/$22,244 ($166/u) vs 138u/$12,098 ($88/u) — delta **+$10,146** (we already beat the tape here by holding instead of dumping)
- MILK: 196u/$6,659 vs 225u/$5,126 — delta +$1,533 (his own milk book floors at $1-5 from d16)

Priority ranking set that day (D1-D6): D1 stop the late-season strawberry/melon dump (worth $10k+); D2 rebuild the parameter sweep space on the Windows box; D3 fix the production oscillation and the late-PLANT-cannot-water rule (worth $5-15k gross); D4 keep grinding the day-by-day frontier; D5 fold cow/sheep/goose split into D2 (geese: zero field evidence across 2,744 seats, not worth a COOP); D6 fourth quadrant parked (marginal at best against fib-priced crew costs).

### Ladder losses, 2026-08-11 — sample caveat

Source: ladder_losses_2026-08-11.md, 2026-08-11.

**This file self-flags: THIS IS A SAMPLE OF LOSSES, NOT A RECORD.**
Alex downloads games we lose, so any "we out-earn them and spend the difference" style finding from this sample is conditioned on having lost and must not be read as a win-rate statement.
Carried forward as stated in the source: not biased are the shop-coverage table, per-seed drain figures, and our own fixed play (MELON 69, COW 10 SHEEP 4 on every board).

Unbiased finding: **no shop drains MELON, ever, on any seed** (`SHOPS` in `reference/kaggriculture.py:90`).
It closed at $4-$25 against a base of $250 across 10 recordings, 0 units drained in all 10.
Measured on episode 92077611 (loss by $1,386): our second melon wave (9 tiles planted d10, ripe d20, 66 units) sold into the book our own first wave had just spent, netting $4,758 (~$72/unit down to $1).
Melon is a race for a fixed pot: the opponent's last 72 units fetched $4.71 each because our wave hit the book first, plausibly costing him $6-7k against $1,300 to us on a game lost by $1,386.
Rule stated: melon's lever is not planting less, it is ripening earlier (a wave planted d8 lands d18, ahead of the opponent's second wave).

We plant the same crop list on every seed regardless of town demand: MELON 69 on six different seeds with six different towns.
We never plant CARROT or TOMATO, both of which closed above base in 10/10 games (CARROT $40-42 vs base $35; TOMATO $77-118 vs base $60) because both are shop-drained and we never supply them.

The open, unmeasured lead at end of file: on 92077611, we spent $21,585 against their $17,161 — $4,424 more, on a game lost by only $1,386.

### Spawn-ring misprediction, and its review — 2026-08-12

Source: spawn_ring_misprediction_2026-08-12.md and fable_spawn_ring_verdict_2026-08-12.md, 2026-08-12.

`_arrivals` predicts hire landing tiles using the ring order `[(4,4),(5,4),(4,5),(5,5)]` counted at the moment the hire settles.
Hires settle in the market phase, which runs after the unit phase, so the ring the hires see already has the farmer's hour-0 move applied — but the predictor assumes the farmer is still on `(4,4)`.
Every hand of the day then lands one ring slot early.
Measured cost on d11, seed 11: u10's tour was priced at exactly 23 turns against a 23-turn budget (zero slack), woke 2 tiles off-plan, and finished 2 tiles short.
Tile (1,2) weeded that night.

**Obvious fix (pin the farmer on hire turns) was tried and is a measured LOSS.**
17-day grid, seed 11, victor tape: money@d16 17,459 -> 16,044; weeds 2 -> 4; strawb from d11 35/36 -> 33/36.
Tile (1,2) lived; (0,2), (1,4), (2,1) died in its place.
Reverted.

The 08-12 review of this finding (fable_spawn_ring_verdict) measured two things not in the original doc:
- A two-pass re-solve (predict, then correct from the farmer's actual hour-0 move) converges within 2 corrections on every day tested (9, 10, 11) — not always 1, but it does not diverge.
- Wall-clock cost of an extra solve: 0.372-0.496s at d10-d17 crew sizes, against a 1-second `actTimeout`. Day 10 needs 3 solves to converge, which exceeds 1.1s and would blow the per-turn budget on the solve alone.

Verdict: ranked (b) — a flat turn-budget haircut on phantom vehicles at `_router_acts` line 1697-1698 — above (a) the two-pass re-solve, because it is cheap, has no solve cost, and generalizes to any 1-2 turn slip, not just this one.
(a) recommended too, but capped at 2 iterations with a wall-clock guard.
(c) "bind tours to landing tile not arrival order" rejected as scoped: checked on d11, predicted per-tile counts (5,4):3 (4,5):3 (5,5):2 (4,4):2 do not match actual (4,4):3 (5,4):3 (4,5):2 (5,5):2 — a different multiset, not just a different order.

New finding (d, not previously in the register): `_hires_this_turn` does not apply `_unwalled_landing_slots`, but the market block that actually emits HIRE orders does.
On a land-buying day the dawn plan's `arriving` list can contain more phantom hands than actually get hired at hour 0.
Day 10 (`land: 1, hands: 14`) is exactly the day both the pin experiment (14 wrong -> 7, not 0) and the two-pass experiment (needs 3 solves) flag as the hard case.
Neither (a) nor (b) alone fixes this; it needs `_hires_this_turn` to gain the same landing-slot cap the market block already has.
Not attempted as of this doc.

Framing note carried forward: the scheduler prices tours with zero margin anywhere, and this bug is a *trigger* for that vulnerability, not the vulnerability itself.

### The route is precomputable — 2026-08-12

Source: the_route_is_precomputable_2026-08-12.md, 2026-08-12.

The board geometry is identical in every game: `_initial_tile` and `_default_spawn` are pure functions of coordinates, and the only RNG in `kaggriculture.py` (`random.Random((seed*1_000_003)^day)`, line 858) drives only the shop-unlock draw and `_spawn_weeds`.
So a route solved once offline is reusable; the 1s/turn `actTimeout` is not a constraint on route quality if solved ahead of time.

`scripts/solve_day_offline.py` runs `cover.py`'s own `cover()` with the LNS deadline raised and multiple restarts.
Result on d12: shipped greedy planner covers 48/49 (leaves one job); the offline solve with 5 seconds and 2 restarts covers 49/49, both restarts independently.
The existing ruin-and-recreate code already solves d12 at 5 seconds — it just fails at the in-game budget of `RUIN_AND_RECREATE_SECONDS = 0.25`.
At 0.25s across a full season it measured slightly worse than off (work 1591 vs 1613 over 20 days), so it must not ship at that budget.

d18 was previously reported as "66 of a proven 67 covered" — **that does not reproduce from the saved fixture, which contains 66 jobs total.** That lead is closed.

Season totals, d0-d19, seed 11, victor: we work 1,613 turns vs the tape's 1,556 (more), move 1,646 vs 1,536 (more), idle 539 vs 692 (less), and still bank $26,105 vs $27,133 (less).
Capacity is not the binding constraint — freeing more turns gives us more of what we already have a surplus of.
The lever is the mix of ops, not the count.

### d16: the fertilizer starvation is a d11-d14 selling decision, not a routing bug

Source: d16_fertilizer_starvation_2026-08-12.md, 2026-08-12.

d16 has 0 uncovered jobs and 96 turns of priced slack; the work was offered but failed silently.
`_apply_unit_action` fails FERTILIZE silently on an empty hand (`kaggriculture.py:465`).
Per-unit on d16: u13 planned a draw of FERTILIZER 6, got 0, fired 0 of 6 fertilizes.
Total planned draw was 12; units that reach the shed first drain it.

Root cause is 4-5 days earlier: dawn shed fertilizer tracked the tape exactly through d10 (15/15), then diverged and never recovered (d11 10/12, d12 4/9, d13 4/12, d14 1/12, d15 4/12, d16 10/12) — `collect_fert` production is identical (12/12 every day d9-d16), so the stock is spent differently: the sell rows ask for FERTILIZER 24 on d11, 14 on d12, 8 on d14, drawn from the same stock the fertilizing needs.
`fertilize` first goes wrong at d12 (2/3), not d16.

Worth noting: FERTILIZE sets `fertilized_until_day = day+2`, doubling water yield for 3 days, so a missed fertilize costs 3 days of half-value watering, not one op.

Landmine flagged from `cover.py`: refusing a job for short supply already measured worse three times (d16 money 7,293 -> 3,280 -> 0); `SUPPLY_LIMITS_EVERY_DRAW` stays off for that reason.
Candidate fixes proposed, not yet built: reserve the day's planned FERTILIZE draw before filling the sell quota; buy the shortfall (we hold $14,407 at dawn d16 with 96 idle turns); or cap the planned depot pick at real stock.

Same-day side finding: d18 has exactly one uncovered job, `(0,0) [WATER, FERTILIZE, HARVEST]`, and that is where weeds go 2 -> 4 and strawb drops 35 -> 33.
d19 is where the season turns: leading $23,454/$22,551 at d18, trailing $26,215/$27,133 at d19.

### d18: harvest and sell gaps are cadence, not defects — one real deficit

Source: d18_harvest_and_sells_2026-08-12.md, 2026-08-12.

`harvest 11/14` on d18 is not 3 missing harvests — we took them on d17 instead (our d17 harvest was 22 ops against the tape's 18).
Cumulative d16-d18 harvest ops are exactly 46/46.
No fix needed.

`sell 35/61` on d18 mirrors `sell 90/39` on d17 — both sides follow the same schedule row; cumulative sell units at end of d18 are 499 (ours) vs 489 (tape), money $25,596 vs $22,551, we are $3,045 up.
Mechanism: `LATE_SELL_FROM_HOUR = 16` sells late into our own dawn production; the tape posts its sell row at h0.

The one genuine, unreconciled deficit: FERTILIZER 0/8 on d18.
Our shed holds 9-13 fertilizer all through d18, the row asks for 8, but the reserve rule (`FERTILIZER_RESERVE_LOOKAHEAD_DAYS = 1`) computes `want = max(today, tomorrow's FERTILIZE-eligible tiles) = 12`, so `have = max(0, 9-12) = 0` and nothing is offered.
The tape sells its 8 at d18 h23 and still fertilizes 12 on d19.
Cumulative FERTILIZER is -8 at end of d18 and still -8 at end of d19 — does not reconcile.
Whether releasing this reserve is safe is **not established**: the same reserve exists because d16 previously fired only 6 of 12 fertilizes when the shed was starved.
Diagnosis only, no fix attempted.

Side observation, not investigated: on d18 we buy a COW where the schedule row says SHEEP 1.

### The late season is one defect in two halves — 2026-08-12, superseded 2026-08-22

Source: the_late_season_is_one_defect_in_two_halves_2026-08-12.md, 2026-08-12.
**The file itself carries a note added 2026-08-22 pointing to the 2026-08-13 measurement below** (`the_market_is_the_late_season_2026-08-13.md`) for the combined, dated result.
This section is the diagnosis; the 08-13 section has the measured outcome.

State rows match the tape to d24, then diverge: `fertilize` 127/71 (+56, the only row where we do MORE), `harvest` 322/360 (-38), `plant` 182/194 (-12), `water` 906/965 (-59).

Half one: DIG clears ground to None exactly like a one-shot HARVEST, but `REPLANT_A_CLEARED_TILE` only chains onto HARVEST, not DIG — a day that demolishes ground (via DIG) plants nothing on it.
Seed 11 d26: schedule row asks 11 WHEAT, pool contains 11 HARVEST/DIG, PLANT ops offered = 0.
**Fixed, measured, REVERTED**: extending the replant condition to include DIG cost -$2,898 (money d24 53,031 -> 51,523; d26 56,453 -> 55,259; d28 62,743 -> 59,845) and the target cell (d26 plant) did not move (0/11 -> 0/11 unchanged) because of half two.

Half two: `plant_prize('WHEAT', 26) = 0.0` — a wheat planted d26 cannot reach age 4 (max_day) before season end (d30), so `_one_shot_is_finished` never offers a harvest for it and the planner correctly prices it at nothing.
Victor's own recorded game does not play by this rule: he plants 11 wheat on d26 and harvests 26 units on d29 at partial age (held 4 of max 6) — the env allows a partial harvest once `day - planted_day >= first_yield_day`.
This is crop-specific, not general: his melon harvests are always full (held 6/6 at age exactly 10); only wheat gets partial late harvests.

Conclusion: the two halves must be fixed together and measured as a pair, never separately — half one alone plants tiles nothing can collect; half two alone has nothing to chain onto.

### d6: the stranded wool, found and fixed — 2026-08-13, kawashigi tape

Source: d6_stranded_wool_2026-08-13.md, 2026-08-13.

d6 row asks `sells={FERTILIZER: 5, WOOL: 12}`; board produces 9 wool from two shear jobs.
Baseline sold 10 of 17 (5 fertilizer + 5 wool at h09); 4 wool rode a hand from h09 to dusk and reached the shed only via the overnight sweep, after market close.

The hand carrying the wool never touched a depot tile, so every delivery rule in `materialise` declined it for its own documented reason (RUSH_BANK_MIN needs a hand that starts loaded; the free-drop and re-draw rules fire only at a zero-detour depot; the closing-trip rule is never charged because `DELIVER_CUTOFF_TURNS = 99` makes `deliver` False on every 24-turn day).
`DELIVER_MIN`'s own docstring assumed a small load gets delivered "at the end of the tour, which ends at the shed anyway" — false when `deliver` is False.

**Fix shipped: `SHIP_WHAT_NO_LATER_STOP_CAN_BANK = True`** in `kagg/search/cover.py`.
New clause in rule 2: when the closing trip is uncharged and no remaining stop touches a depot, a positive load of the row's produce ships now regardless of `DELIVER_MIN`.

Measured, kawashigi tape, d0-d5 byte-identical.
d6: sell 10/17 -> 14/17; sh:wool end of day 4/0 -> 0/0; buy_seed 7/15 -> 15/15; money 3/957 -> 358/957.
14/17 is the ceiling by construction (row asks WOOL 12, board only grows 9).
d7 reconciles to exact: sell 10/6 -> 6/6, buy_seed 5/4 -> 4/4.
Downstream, d16 money closes at 22,246 vs baseline 19,067, but the herd also ends bigger (11 vs 10 at d16) and two rows move the other way (second sheep lost d8 in both arms; weed timing shifts d12-d13 vs d14/d16, both within one weed by d16) — noted, not hidden.

### d6: the two missing waters — 2026-08-13, kawashigi tape, HISTORICAL/REVERTED

Source: d6_water_2026-08-13.md, 2026-08-13.
**Diagnosed, tried, measured as a net loss, reverted. Do not retry as written.**

d6 row reads `water 17/19`.
Both boards carry 19 established crop tiles at dawn; the tape waters 17 of 19 plus 2 new plantings = 19; we water 15 of 19 plus 2 new = 17.
The 2 skipped tiles are strawberries (2,3), (3,3), (0,4), (1,4) — specifically the two even-parity ones, (3,3) and (0,4).
Cause: `WATER_ROTATION` (water half the safe tiles by `(x+y+day)` parity) was added only to the one-shot branch (melon), never to the ongoing branch (strawberry/tomato).

Fix tried: same parity clause added to the ongoing branch's safe-tile slot.
It worked at the op level (both tiles offered and toured) but **measured as a LOSS**: `water 17/19 unchanged`, `plant 2/2 -> 0/2`, `melon end-of-day 14/14 -> 12/14`.
The two 1-turn waters ate the slack two far PLANT jobs needed; the plants slid to d7, a d6 regression.
Reverted same day; test deleted with it.

What a future attempt needs to fix, if retried: stop a top-up water from displacing scheduled work (the greedy currently ranks only on insertion cost, so a 1-turn water always beats a 2-turn plant), or find the 3 unit-turns the tape has and we don't (crew arrival timing, not willingness to water, is the real binding constraint on d6).
The rotation-asymmetry finding itself is reusable: from d7 onward, rotation-on-ongoing tracked the tape's water column more closely (d11 39/39, d12 40/40 exact).

### The late season is a market problem — 2026-08-13, seed 11, victor tape

Source: the_market_is_the_late_season_2026-08-13.md, 2026-08-13.
This is the measured outcome that the 2026-08-12 "one defect in two halves" diagnosis produced.

**Turns are not the constraint.** Raising `hands` from 10 to 14 on d26-d29 cost -$3,350 and the extra hands stood still (pass turns d26 36 -> 124, water unchanged 36/36).
Season totals: we already do 178 more ops than Victor (work 2,978/2,800) and idle less (862/935), and finish ~$11k behind him.

**Routing is not the constraint either.** Re-solved d26-d29 in day order: the shipped greedy already covers 60/60, 61/61, 25/25 (d28 improves 48/51 -> 51/51 with a solve).
But dropping those days from `SOLVED_DAYS` on the "greedy already covers them" reasoning cost -$2,277 and put weeds back to 5/day — coverage and visit order are different claims.

**`LATE_SEASON_PAIR` shipped** (three changes in `kagg/search/router.py`, gated to d26+): `FERTILIZE_UNTIL_DAY = 26` (no FERTILIZE offered after d26), `LATE_TRUNCATED_PLANT_DAY = 26` (plant_prize stops zeroing for a window the season can't finish), `HARVEST_A_TRUNCATED_ONE_SHOT` (partial harvest once the window can't close before d29).
Measured, control -> arm, season money:
- stale routes: 72,184 -> 70,321 (-$1,863)
- re-solved routes: 72,184 -> 71,814 (-$370)
- routes dropped entirely: 72,184 -> 69,537 (-$2,647)

**-$370 on one seed is called undecided, not a win** — inside the ~15% seed variance, decided by `scripts/field_sweep.py` against recorded opponents, not this grid.
Rows do land close to the tape when re-solved: plant d26 0 -> 12 (tape 11), water d28 26 -> 38 (tape 39), harvest d28 17 -> 30 (tape 20).

**CORRECTION (same day): the milk floor is a HARNESS artifact.** Three real ladder episodes (92450417, 92443929, 92442061) show MILK never floors: it moves 169 -> 279, 169 -> 258, 169 -> 154 across the season.
`breakdown.py` seats our agent against a replayed tape and both sell into one book, so a tape that already sold 303 milk in its own game sells it again next to us — a harness-only glut.
**Everything in this doc's "we flood our own book" section is unproven on the ladder and must be re-measured from a ladder replay before acting.**
With that caveat stated: in the harness, 159 milk units sold at $1-5 vs $223.81/unit realized elsewhere (episode 92077611); wool sold at $1 on d19 then $160/$109/$181/$146 on d24-28 in smaller lots, showing the town's demand does refill if not flooded.

**The geese verdict was measuring our own bug, not geese.** Two earlier outcome-only sweeps (`c9c1c18`, `7a88d30`) killed geese on win rate and mean money alone.
Re-run with `HERD_GEESE = 2` through `sell_when.py`, reading fills: **0 eggs sold, whole season.**
Season money 48,196 vs 71,814 without geese; sell revenue 188,908 vs 214,385.
The birds are bought, fed, and cared for 30 days and produce nothing sellable — the -42 points of win rate is the cost of 3 animals' turns and money against zero revenue, and says nothing about whether a goose is worth owning.
This is the fifth time an animal verdict here turned out to be an artifact; an outcome-only sweep is not a test of a mechanic.

### The ladder is lost by a nose — 2026-08-13, 60 downloaded ladder games

Source: the_ladder_is_lost_by_a_nose_2026-08-13.md, 2026-08-13.

**Self-correction in the file, carried forward: this is NOT a win-rate measurement.**
The 60 games in `data/seed_scripts/ours_ladder/` were downloaded because they were losses.
Every win-rate number originally in this file ("5-54", "win rate 0.085", the "+$6,000 takes us to 0.475" table) was computed on a sample conditioned on the outcome being measured and was removed rather than annotated, specifically so it is not re-derived.

**What survives**: given that we lost, by how much.
54 losses: median -$8,900, mean -$11,600.
6 losses inside $600; 11 inside $2,100; 23 inside $6,000; 31 inside $10,000.
Two losses inside $150: -$70 vs TrebolNoir_, -$135 vs Mirza Yasir Abdullah Baig.
This licenses "we often lose by an amount a single good day would cover" — it says nothing about how often we lose.

5 wins in the same set ($13.9k, $13.5k, $78.4k, $91.0k, $65.2k) are not a sample of our wins either, just whatever was downloaded alongside.

Ruled out: stranded stock (final shed on seed 11 is fully empty, $0 of all 9 products — `LIQUIDATE_LAST_DAY` works); a single catastrophic matchup (losses spread across 54 distinct opponents, worst -$39,200, median ~-$8,900).

Separately noted, unquantified: episode 91304798, a self-play validation on seed 0, ended TIMEOUT/TIMEOUT at step 531 of 720 — one game of 60, our own agent both seats, not in the ladder sample, but a reminder nothing currently measures our per-turn latency.

### The last growing day's water — 2026-08-14, kawashigi tape, HISTORICAL/REVERTED

Source: the_last_growing_days_water_2026-08-14.md, 2026-08-14.
**Status in the file: DIAGNOSED, FIX REVERTED, DO NOT RETRY AS WRITTEN.**

The defect is real: the water window check is `in_window = (max_day+1)//2 <= age <= max_day` (inclusive at the top), but `_one_shot_is_finished` already offers HARVEST at `age >= max_day`.
So at `age == max_day` a tile can still bank one more water-driven unit while the harvest gate has already declared it closed; a tour that reaches the tile harvests before it waters, and the water lands on bare ground.
Wheat is `max_day 4`; all 7 tiles sown d0 stood at `yield_units = 3` (not 4) at d4 dawn for us, banking 26 total against the tape's 28 (every tile full).
This traces through the wheat ledger to a real, persistent deficit of 2 units, visible through d9.

**Fix tried (`HARVEST_WAITS_FOR_THE_LAST_GROWING_DAYS_WATER`, gate harvest on `watered_today` at `age == max_day`): makes d4 bank 28, and loses $19,595.**
Deferred harvest = tile that doesn't clear = doesn't replant = wheat pipeline stalls = shed never refills = animals miss 2 consecutive feeds and get removed.
Measured: d8 animals 9 -> 0 (whole herd starves, tape had 10); d9 animals 12 -> 2 (tape 12); d16 animals 13 -> 5 (tape 14); d16 money 30,585 -> 10,990 (tape 32,566).

Lesson stated in the file: HARVEST is not only collection on a one-shot, it is demolition that frees ground on the critical path for the next sowing — any harvest-delay rule must be measured against the replant it blocks, not the units it collects.
If retried, the shape to try is ordering without delay (reach the tile earlier, or water-then-harvest within the same visit) — never withholding the HARVEST op.

### d8: the milk must be in the shed by h05 — 2026-08-14, kawashigi tape

Source: the_milk_must_be_in_the_shed_by_h05_2026-08-14.md, 2026-08-14.
This supersedes the "first milk day" framing in the wheat-row doc below.

Decisive measurement: forcing the tape's exact d8 orders (buys and sells) but banking our milk 6 hours earlier than baseline (h07 vs the tape's h05) changed nothing — sell stayed 6/18, feed 9/10, care 9/10, sold $524 vs the tape's $3,177, byte-identical to the un-early version.
**"Earlier" is not the requirement. "By h05" is.**

His plan, read from the raw replay: both his ripe-cow units start their day ON the ripe pen, run PICKUP -> FEED -> CARE -> HARVEST -> PLACE(bank) in immediate consecutive turns with no revisit, and he never makes a delivery trip because `_refresh_pins` sites pens on shed-access tiles — the pen IS the depot.
Ours has the same shape on the first pen, then loses 2 turns delivering and 8 turns reaching the second pen.

Flag `BANK_THE_ROWS_PRODUCE_WHILE_REAPING` tried first: moved milk h17 -> h07, made the herd exact from d10, but did not move d8's target cells (buy_product 5/17, feed 2/10, care 2/10 unchanged) and cost -$1,098 at d16 (32,419 -> 31,321).
Shipped **False**.

Root mechanism found: **every delivery path in `materialise` computes the bank stop as part of a TRANSITION to the next job** (`d = nearest(depots, pos, j.tile)`), so none of them can express "bank here, now, without moving on" — which is exactly what his plan does (harvest and PLACE on the same tile, next turn).

**Fix shipped: `BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY`.** Appends the bank stop directly after a funding pen, gated on the pen's own yield being in `wanted` (not on what the hand carries generally — a looser version was caught banking at every pen on a day whose row sells the wheat the herd eats, and rejected).
Measured: feed 2/10 -> 6/10, care 2/10 -> 6/10, pass 122/36 -> 107/36, buy_product 5/17 unchanged, season exact cells 447/697 -> 467/697 (+20), d16 money 32,419 -> 31,816 (-$603).
Half the milk lands on time; the second cow is still harvested late (h11) because it's job 1 on a hand that must first feed an at-risk pen.

Separately tried and shipped **False**: `ONE_HAND_PER_FUNDING_PEN` (split the two funding pens onto separate hands instead of one hand doing both back to back).
Split alone: exact 468 (+21), d16 -531.
Split + bank together: byte-identical to bank alone (465 exact, -1,098) — once each funding pen gets its own depot stop, the greedy separates them without being asked, so the two fixes are not complementary; bank supersedes split.

What is binding now, per the file: `buy_product 5/17` is not a milk problem any more, it is that `state["ordered"]` is credited on QUEUE not FILL, so a refused order (from `HIRE_FIRST` putting 9 hires ahead of wheat at h00) is never re-offered even once cash exists.
Fix proposed, not yet built: credit on fill, not queue.
Explicitly stated: do NOT reopen the herd mix, d8's routing/job list, or the sizing of the wheat row.

### d8: the wheat row and the turn's own spending — 2026-08-14, kawashigi tape, HISTORICAL/REVERTED

Source: the_wheat_row_and_the_turns_own_spending_2026-08-14.md, 2026-08-14.
**Status in the file: DIAGNOSED, FIX REVERTED, DO NOT RETRY AS WRITTEN.**

d8 row asks `buys {WHEAT: 17}`.
`_process_market`'s running `money` tracker debits for BUY_LAND, BUY_ANIMAL and BUY_PRODUCT WHEAT, but **not** for HIRE or BUY_SEED — and with `HIRE_FIRST` on, both sit above the wheat row in the queue.
At h01, $594 of the turn's bank (2 hires at fib prices + 2 seed buys) is already committed before the wheat order is priced; only ~$147 reaches it, and only 5 of 17 wheat fill.
Because `state["ordered"]` credits on QUEUE not FILL, the remaining 12 units are silently dropped and never re-offered even as the day's later sales land.
Result: d8 closes buy_product 5/17, feed 2/10, care 2/10.

**Fix 1 tried (`THE_BANK_IS_DEBITED_FOR_WHAT_THE_TURN_ALREADY_ORDERED`): fixes d8 exactly (buy_product 17/17) and loses $9,577 at d16** (32,419 -> 22,842, tape 32,566).
The loss traces to d6, not d8: debiting for seed alone (hires untouched) reproduces the same loss, so it isn't the hire-affordability guard being double-charged.
Day 6 is when the schedule takes a $1,000 parcel; the extra debit shrinks the running bank enough that d6's own wheat order shrinks (buy_product 6/6 -> 0/6) and sell drops 17/17 -> 11/17.

**Fix 2 tried (size the wheat order locally against turn-remaining money, without mutating the shared `money`): identical loss, to the dollar** (22,842, same as fix 1).
This refutes the "shared mutable bank" theory — a fully local, non-mutating version produces the same season, so the cause is the *size* of the row shrinking on d6, not the plumbing.
At baseline, d6's over-sized wheat order fills (buy_product 6/6 exact); sizing it "honestly" against turn-remaining cash refuses an order the market would have honored, because the honest estimate is pessimistic about pending sell revenue (which is real) while being exact about hires and seed (which are also real) — the pessimism lands entirely on the purchase side.

Lesson stated: a running estimate with several readers is not safe to make more accurate for only one of them — the same shape as the reverted last-growing-day water fix, where one unit of yield was traded for the herd.
**Both sizing attempts shrank the order, and shrinking the order is what loses d6. Do not try a third way of sizing it.**
The one shape not yet tried: credit `state["ordered"]` on FILL rather than QUEUE, so a refused order is re-offered later in the day, without shrinking anything.

This document's own investigation is superseded by the h05-milk finding above: forcing the tape's exact d8 market (buys and sells together) shows `sell 6/18` — the milk sale (`SELL MILK 12`) fills zero because we hold no milk, so buy_product cannot match until sells match, and sells can't match until the milk exists.
The wheat row was a symptom; d8 is the first milk-payout day (cows placed d0, `first_yield_day 8`), and the binding constraint is getting milk to the shed by h05, covered in the section above.
Explicitly stated: do NOT reopen the herd mix, d8's routing/job list, or the sizing of the wheat row.

---

## Victor / Kawashigi / tetsuya lineage, 2026-08-15 to 2026-08-21

### 2026-08-15 — the ladder state and the stale precomputed routes

source: handoff_2026-08-15.md, 2026-08-15

Two submissions had gone backwards before this date.
Ladder history recorded:

    2026-08-13 03:39   1890.2   LATE_SEASON_PAIR + re-solved d26-d29 routes
    2026-08-13 05:21   1428.4   carrot reaches the market (SELLABLE fix) + pins + wool rule
    2026-08-15 02:50   1030.0   d8 sheep placed + melon yields to a melon-heavy opponent

`kagg/search/solved_days.py` was solved on seed 11 against the **victor** tape, but `SHIPPED_PLAN` had been **kawashigi** since 2026-08-13.
Measured, `--tape kawashigi --days 30`:

    precomputed ON (shipped)     d29 $139,025    work 2979  move 3036  idle 987
    PRECOMPUTED_ROUTES = {}      d29 $118,660    work 2895  move 3150  idle 957

`cover.PRECOMPUTED_MISSES` seated only **143 of 571 stops (25%)**.
`scripts/resolve_days.py` was launched to re-solve d12-d29 in day order.

One agent, one name: `schedule_agent.py` (3,610 lines) was a dead predecessor; the shipped agent is `schedule_agent_1455mh.py`.
75 scripts had imported the dead file, including three sell diagnostics.
22,777 lines were deleted in commit `fa96ace`.
Build gate passed: `env.run` banked $141,449 against starter's $3,660.

Three flags were confirmed as ladder losses, 12 recorded opponents, both seatings, env-default weeds, seeds 1300-1305:

    HERD_GEESE             0 → 69.4% win, +$15,502 margin
                           2 → 38.9% win,  −$2,432
                           4 → 41.7% win,  −$1,338
    WHEAT_TILES_TO_CARROT  0 → 69.4%   8 → 61.1%   16 → 63.9%   28 → 66.0%
    WHEAT_TILES_TO_TOMATO  0 → 69.4%   8 → 61.1%   16 → 63.9%   28 → 68.1%

All three stayed at 0.
Carrot raises mean money (88,810 → 90,080) while lowering win rate — strictly worse on an Elo ladder.

### 2026-08-15 — why production stops from d19 (standing-crop attrition, not digs/fert/caps)

source: fable_production_decay_d19_2026-08-15.md, 2026-08-15 (seed 11, tape kawashigi, weeds 0.0; per-tile counts are route-sensitive and will shift once solved_days regen lands)

Three briefed hypotheses were killed with numbers:

- **Digging live crops: NO.** Ours 54 digs / tape 40, classified: ours 18 spent-strawberry + 21 decay-weed + 14 thirst-weed + 1 other; tape 31 spent-strawberry + 5 decay-weed + 0 thirst-weed + 4 other. Zero PLANT digs with units held on either side.
- **Fertilize stealing harvest turns: NO, marginal.** Ours 100 ops (49 strawberry + 51 wheat) banking 185 bonus units = 1.85 units/op. Tape 72 ops, all strawberry, banking 142 bonus units = 1.97 units/op.
- **Cap discards: NO. Zero on both farms, all 30 days.**

The real mechanism is **standing-producer attrition**: only 13 of our strawberry tiles complete their lifecycle against the tape's 31.
Harvest d19+: ours 247 / tape 275.
Weed births: ours 34 (13 thirst + 21 decay) / tape 10 (0 thirst + 10 decay).
Two channels: thirst kills live strawberries mid-life (13 vs 0), and one-shots left past their harvest window rot into decay weeds at 1 unit per 2 turns.

Caveat: `LATE_SEASON_TRIAGE` deliberately stops watering tiles that cannot produce again before d29, so part of the 13 thirst-weed count is policy, not defect.

Candidate fix (not implemented, pending the route regen): mark a tile on its final-production day as `at_risk`, since it decays and weeds overnight if not harvested and dug that day.

### 2026-08-15 — watering post-d8 is a well-evidenced negative

source: fable_watering_post_d8_2026-08-15.md, 2026-08-15

Superseded mid-session by the 30-day measurement: summed d9-d29 water is ours 798 / tape 795 — **no volume shortfall**.
Per-day cells that look short (d10 25/32, d12 30/40) are cancelled by days we over-water (d13 47/41, d23 41/31).

One fix was tried and measured as a loss, **do not rebuild it**: `ONGOING_TOP_UP_FROM_DAY = 9` gave a safe ongoing crop a discounted preventive water from d9.
d0-d8 was zero changed cells, but on the grid environment: post-d9 weed births rose 2 → 3, money at d16 fell $32,794 → $31,743 (**-$1,051**), and one of the three new weeds was a MELON survival rescue displaced by the cheap offers.
Reverted immediately.

What actually kills 2-3 tiles a season: covered rescues on tours that cannot run.
Every killed tile's survival water was offered, covered, and routed, and died at execution.
d15 dawn trace showed unit 6 with budget 23 costing 25 (over budget) and unit 9 budget 23 costing 26 — both tails carried the doomed WATER stops.
This is a reliability defect in tour pricing (two cost models disagreeing on `RESERVE_DAYS`), not a node-count defect.
Left open deliberately.

### 2026-08-15 — the season ends with the crew holding the margin (CLOSED)

source: the_stranded_load_is_the_loss_2026-08-15.md, 2026-08-15

> CLOSED by the_last_two_days_2026-08-17.md — both halves the old note asked for are shipped there (a CRITICAL-priority d28 harvest plus a re-seated d29 drop, d29 drop now 9/9 against the tape).
> The three failed fixes recorded below are still real null results — do not re-try them.

Measured off three downloaded ladder replays at the final step of d29:

    episode     our stranded          their stranded     result
    93318573    81 units  ~$3,264      4 units  ~$19     lost by   $645
    93323101    55 units  ~$3,526      0 units    $0     lost by $3,919
    93286476    70 units  ~$2,238      0 units    $0     lost by   $962

In all three the stranded value exceeded the losing margin.
Cause: `_drop_inventories_to_shed` runs after the final `_process_market` on d29, so a d29 harvest not walked to the shed is worth exactly zero.
The tape spends 9 DROPs on d29 against our 2.

Three fixes were tried and all failed (do not re-try blind):
1. `WALK_THE_LOAD_HOME_DAYS = (10, 29)` recovered only 7 of 58 units — a solved route stores work stops only, and `materialise` appends the shed trip from slack that d29 does not have.
2. `NO_UPKEEP_ON_THE_LAST_DAY` regressed the grid: harvest 396 → 389, sell 1489 → 1474, d29 HARVEST 27 → 20 for +28 turns, because `cover._apply_precomputed` keys a stop on `(tile, ops)` and a changed op set drops the stop from the route rather than cheapening it.
3. `UNSOLVE_DAYS = (29,)` raised sell 1489 → 1502 (+$256) but stranded rose 51 → 78.

Also ruled out: d28 under-prioritizing (byte-identical three ways), planting-date mismatch (identical to the tape), shed overflow (5 units/season), and spreading the sell across hours (+$64).

### 2026-08-15 — the brief to Fable: copy カワシギ's close

source: fable_brief_sell_the_close_2026-08-15.md, 2026-08-15

Alex's instruction verbatim: "we really need to copy kawa to get those items sold. no watering no feed and care just get shit sold on d29 and as much as possible on d28."
Closing grid, ours/tape: d29 feed 14/0, care 14/0, collect_fert 14/0, harvest 26/19, drop 2/9, sell 93/148, pass 30/56.
He does zero feed/care/fert-collection on d29 against our 42 unit-turns, harvests 32 on d28 to our 27 (banked free overnight), and turns d29 into pure selling.
The fix Alex endorsed: "a delivery that's planned, not appended."
Constraints given: do not regress d0-d8, one delta at a time, write the test RED first, never sum offers, never call a mismatch small, do not run the full suite.

### 2026-08-15 — closing the season: the eight-delta build

source: fable_close_the_season_2026-08-15.md, 2026-08-15 (baseline HEAD eb8845e)

Six named deltas, each measured in both a grid world (`--days 30`, recorded economy/shops) and a test world (the xfail fixture, no recorded shops):

- **Delta 1** `cover.MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE` (commit 798d459): null by construction, byte-identical in both worlds; d29 exact-key misses fell 14 → 9.
- **Delta 2** `NO_UPKEEP_ON_THE_LAST_DAY = True` gated through one function `router.upkeep_buys_nothing(day)` (commit c1c49f7): grid world d29 feed 14/0 → 0/0, care 14/0 → 0/0, harvest 27/19 → 26/19, sell 93/148 → 120/148, sold $7,474 → $9,547, season close $150,728 → $152,801 (tape $150,076 — **we now out-bank the tape**). Test world: stranded 62 → 51, money $82,305 → $83,826. A half-step with only `animal_ops` gated measured WORSE (harvest 384 → 377, money -$157) because the executor spent the freed turns anyway.
- **Delta 3** `WALK_THE_LOAD_HOME_DAYS = (10, 29)` (commit 30ad651): test world stranded 51 → 28 (~$672), d29 sell fills 123 → 148 (matches the tape's own number), money $83,826 → $84,560. Grid world: byte-identical op rows, sold $9,547 → $9,543 (-$4 fill-price slide).
- **Delta 4** survival/rotation waters and weed digs (commit efd3dfa): grid world d29 dig 5/0 → 0/0, sell 120 → 123, close $152,848, weeds at close 1 → 6 (free, tape closes at 14). Test world: stranded 28 → 26, d29 sell 148 → 153, money $84,699.
- **Delta 5** `TRIM_A_TAIL_THAT_CANNOT_COME_HOME`, d29-only (commit 407d08d): grid world sell 123 → 129, close $152,974, d29 water 18/11 → 16/11, harvest 26/19 → 25/19, drop 5 → 6, sold $9,594 → $9,720. Test world byte-identical to delta 3.
- **Delta 6** the last-day deadline walk, executor-side (commit d0a21f1): test world stranded 26 → 16, d29 harvest 22 → 19. Grid world: harvest 25 → 23, water 16 → 14, closing shed wheat 2 → 4, money unchanged in both worlds.

Two nulls, reverted: `feed_days(29) = 0` (byte-identical both worlds — binding constraint is the schedule's sell row, not the feed reserve) and the yield gate `yield_is_deliverable` (byte-identical, designed off a stale pre-delta-6 trace).

The quota finding: the d29 schedule row asks for exactly 148 units and we fill 153-154 with the cumulative carry; the market block offers nothing more past the row whatever sits in the shed. Selling past the row at the close is flagged as the open money question, out of scope here.

Secondary target: `BANK_THE_FIELD_ON_THE_LAST_FREE_DROP_DAY = True` (commit 5dbff17) — d28 pen HARVEST priced CRITICAL. Grid-world null (d28 already saturated); test-fixture gain d28 water 35 → 37, money $84,699 → $84,945 (+$246).

Final state:

    seed 11, kawashigi                     baseline eb8845e     final 5dbff17
    GRID world season close (ours/tape)  $150,728/$150,076    $152,974/$150,076
    GRID world harvest / sell                    396 / 1489           392 / 1525
    TEST world stranded at snapshot            58-62u ~$2,414          16u ~$324
    TEST world season money (ours/tape)       $82,305/$66,919      $84,945/$66,801

The strict xfail (`TOLERATED_UNITS = 12` against our 16) stays.
Two caveats on the 16: the fixture plays `range(719)` and never plays the final turn; by that instrument the tape itself "strands" 7.
The marginal units are quota-bound, so h22/h23 arrivals cost ~$0 either way.
Fable declined to widen the deadline bound to satisfy the instrument, calling it Alex's call.

### 2026-08-15 — what shipped, and the fourth-quadrant / tomato / goose questions raised after

source: after_the_close_release_2026-08-15.md, 2026-08-15 (submission 55530699, built from 2a2e291, merged at 081c24f)

    season close vs kawashigi tape   150,728 -> 152,974   (tape 150,076)
    stranded at the close            62 units -> 16       (tape 7)
    d29 feed 14->0  care 14->0  drop 3->7  sell fills 96->154  harvest 22->19

d0-d27 byte-identical; d28 moved only on the last delta.
Measured on seed 11 and the kawashigi tape only — no held-out seeds, no arena pool, by explicit decision.
Previous build `55527916` sat at rating 1855.0.

**The fourth quadrant.** Two losses downloaded after release: 93335778 (us $89,518 vs Artem Voronov $103,607, -$14,089) and 93337672 (us $74,289 vs Anhad Mahajan $77,703, -$3,414).
Artem owns four quadrants and 100 tiles to our 75.
Quadrant-unlock table (games / games reaching 4 quadrants / NE / SW / SE unlock times): alex chilton (archive) 69 games, 66 reach 4q, NE d4h22, SW d8h20, SE d11h1; カワシギ 16 games, 4 reach 4q, NE d6h5, SW d11h1, SE d12h1; Seb (allegedly) 16 games, all 16 reach 4q, NE d4h22, SW d6h15, SE d10h14; Victor @ Tufa Labs 7 games, 0 reach 4q, NE d6h17, SW d10h1, SE never; Francesco Montone 2 games, both reach 4q, NE d5h0, SW d8h22, SE d10h16.
Artem's line (NE d6h5, SW d11h1, SE d12h1) matches カワシギ's median to the hour.
We used to buy the fourth quadrant in 66 of 69 archived games and EARLIER than Artem does (SE d11h1 against his d12h1, SW d8h20 against his d11h1); we stopped when rebased onto Victor, who takes it in 0 of 7.
Across all five downloaded losses our unlock turns are byte-identical — NW d0h0, NE d6h10, SW d11h1 — while opponents vary (NE d6h5 to d7h2); we do not adapt at all.
Across all five downloaded losses our unlock turns are byte-identical (NW d0h0, NE d6h10, SW d11h1) — we do not adapt to opponent at all.

**Tomato.** Both losses show TOMATO and EGG closing above base with nobody producing either: 93335778 TOMATO $74 of $60 base (drained 179), EGG $67 of $50 (drained 537), MILK $1 of $160 floor, STRAWBERRY $5 of $120; 93337672 TOMATO $165 of $60 (drained 358), EGG $66 of $50 (drained 358), MILK $1 floor, STRAWBERRY $43 of $120.
Swept on seed 11 vs kawashigi (`tomato_sweep.log`): tomato tiles 0 → 24 moves our money 84,945 → 78,231, monotonically down, while tape money stays 66,801-69,781 and closing TOMATO price falls 70 → 53.
**Unconditional tomato loses money on this board, monotonically.**
Not a verdict on tomato broadly — the balance note states tomato is viable in ~50% of games, carrot 26%, eggs 22%, deliberately not universal.

**The goose kill was 23 hours too early.** REGISTER.md's caveat already voids every geese/eggs verdict taken before commit `c99a8a5` (2026-08-13), when SELLABLE finally held all nine products.
`7a88d30` ("Delete the geese rather than leave a losing flag in the tree") landed 2026-08-12 06:34, **before** an egg could be sold at any price.
Cost/structure/timing table: GOOSE $300 COOP first-yield d4 interval 1 max_held 4 (EGG); COW $400 PASTURE d8 interval 2 max_held 6 (MILK); SHEEP $500 PASTURE d6 interval 3 max_held 6 (WOOL).
The goose is cheapest, earliest, fastest of the three, and EGG closed above base in both losses while MILK sat at the floor.
Caution: animals have produced a wrong negative five separate times in this project.

### 2026-08-15 — where the harvest gap comes from (a hypothesis, not yet measured)

source: where_the_harvest_gap_is_2026-08-15.md, 2026-08-15

Contaminated grid warning: measured while solved routes were only 72% seated.
Seed 11, kawashigi tape, d15-d27: we do more total work than the tape (150-160 turns vs 130-140) and convert less into produce. Season d9-d29: water +65, harvest -19, market fills down 1378/1455.
Candidate cause: `router.WATER_ROTATION` ships `True` with no day gate, based on a single d3 measurement ("his board at dawn is 19 tiles, he emits 14 waters, we emitted 7").
Counter-argument: watering a one-shot crop raises eventual yield, so a lower harvest OP count is not automatically a loss — the market-fills drop (1378/1455) is the stronger evidence it is one.
Experiment proposed, not yet run: day-gate `WATER_ROTATION` off from d15/d20/d25/never, judged per-day after the solved-route regen, requiring d0-d8 byte-identical.

---

### CALLOUT — unresolved contradiction (a): the tape-gate baseline number

> `work_to_be_done_2026-08-16.md` records the tape-gate baseline as **311 failed / 590 passed**.
> `strawberry_watering_2026-08-16.md`, written the **same day**, re-measures the same starting state as **356 failed / 545 passed** and explicitly flags `work_to_be_done`'s baseline as stale.
> Neither number has been reconciled since.

---

### 2026-08-16 — the strawberry watering defect: not priority, not turns, a pricing gap on precomputed days

source: strawberry_watering_2026-08-16.md, 2026-08-16 (worktree `.claude/worktrees/agent-ac5605e21153f7305`, branched from `kawashigi-plan` at `0af2764`)

`cover.cover` returns early on any precomputed day, and `_apply_precomputed` seats solved stops **without pricing them against the unit's turn budget**.
On the gate's own season, ten tours are planned past the day and eleven WATER stops sit past the cut — the tiles those waters name are the tiles that weed the same night.

Localisation: every one of 15 dying tiles was offered a water, none dropped by `_pointless_tiles`.
`VERDICT TALLY: {'seated, not executed': 9, 'uncovered': 6}`.
Over-budget table (day, unit, budget, cost, over-by):
d16 u6 23/28/5, d19 u12 23/25/2, d22 u0 24/25/1, d23 u3 23/33/10, d24 u0 24/26/2, d25 u9 23/29/6, d26 u4 23/26/3, d27 u4 23/25/2, d27 u10 23/25/2, d28 u3 23/25/2.

Red-first test `tests/test_a_hand_is_never_given_more_tour_than_its_day.py`: RED with the same ten rows before the fix, GREEN after, RED again on revert.

Fix: `kagg/search/cover.py`, one new function `_trim_to_the_day` + one call site, **no flag, no constant, no else branch, +61 lines**.
It prices each seated sequence, pops stops off the end until it fits, and releases the surplus into `_insert_leftovers`, which already sorts at-risk first.

Per-day weed row moved toward the tape on every day it appears (d16 3/2→1/2, d17 3/1→0/1 exact, d19 5/1→2/1, d20 5/1→2/1, d21 6/2→4/2, d22 10/1→6/1, d23 11/3→6/3, d26 16/1→8/1, d27 12/0→8/0).
Season seed 11: tiles weeded 15 → 9 (strawberry 11 → 8), weeds standing at d29 15 → 11, DIG turns 31 → 27, HARVEST 366 → 385, WATER 972 → 1011.

Both acceptance gates, this worktree's own re-measurement (see contradiction callout above):

    BEFORE   356 failed, 545 passed, 115 xfailed, 35 xpassed
    AFTER    359 failed, 542 passed, 115 xfailed, 35 xpassed

Net -3 cells, but 5 went green and 8 went red, and 7 of the 8 breakages are the SAME event: we now keep more strawberry alive than the tape does (PLACE-19 is the one straightforward loss — placements dropped 2/2 → 0/2).
The gate counts cells, not distance, so closing a large gap cannot flip a cell while opening a small one can.

Twelve-seed A/B (kawashigi tape, weedSpawnChance 0.005):

    seed |      money OFF       money ON     delta |  weeds OFF/ON | strawb OFF/ON | harv OFF/ON
       3 |        120,043        120,175       132 |     16/11     |     10/6      |   368/378
       5 |         62,347         66,082     3,735 |     17/14     |      8/6      |   362/372
       7 |         91,950         95,138     3,188 |     17/12     |      8/6      |   369/385
      11 |         99,528         98,632      -896 |     15/9      |     11/8      |   366/385
      13 |        115,556        118,120     2,564 |     14/10     |     10/7      |   365/379
      17 |         99,169         99,491       322 |     15/13     |      9/7      |   371/379
      19 |         69,636         69,726        90 |     15/8      |      9/6      |   372/380
      23 |        112,661        114,953     2,292 |     14/10     |     10/7      |   365/379
      29 |         60,117         62,560     2,443 |     17/11     |     13/9      |   352/371
      31 |        105,887        106,623       736 |     15/8      |     11/6      |   361/381
      37 |         52,017         51,244      -773 |     14/7      |      9/6      |   368/379
      41 |         80,486         80,635       149 |     14/7      |      9/6      |   372/380

Money delta: +1,165 mean, +529 median, 10 up / 2 down.
Weeds OFF/ON 183/120 (-34%). Strawberry OFF/ON 117/80 (-32%). Harvest OFF/ON 4,391/4,548.
Seed 11 (the gate's own seed) is one of the two seeds where the change loses money; seed variance on this project is ~15%, so the $1,165 mean is not by itself large — the 10/2 split and the monotone weed/strawberry/harvest columns are what the claim rests on.

Ruled out with measurement: the pass-order fix `AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP` is not the defect (greedy never runs on any day a strawberry died); "the d12 water job is never offered" is refuted (all 15 deaths were offered); `_pointless_tiles`/`LATE_SEASON_TRIAGE` not implicated (pointless=False on all 15); leftover insertion not the cause (solved stops alone already exceed budget).
Reverted, measured null: trimming the last SLIPPABLE stop rather than the last stop — byte-identical gates and same nine tiles weeded; deleted, reason recorded in the docstring.

Still open: nine remaining deaths (six real, three at d29 costing nothing); PLACE-19 regression 2/2 → 0/2; why the solved tours are over budget at all (not attempted here); only the kawashigi tape run — B3/B4 strawberry boards not tested.

### 2026-08-16 — marginal units, the shared book, and the shop draw's real worth

source: marginal_units_and_the_shared_book_2026-08-16.md, 2026-08-16 (branch kawashigi-plan at 3f9fb83)

**1. Revenue is the wrong objective, and it reversed a decision.** The fertilizer sell exemption (`NEVER_DRAINED = ("FERTILIZER",)`), seed 11, ours: revenue fell WOOL 42,871→42,051, WHEAT 19,925→20,408, FERTILIZER 14,302→14,612, MELON 14,179→14,179, MILK 12,006→8,058, STRAWBERRY 10,942→5,970, CARROT 704→806, total 114,929→106,084 (-8,845). Theirs: WHEAT 45,222→43,963, WOOL 20,954→20,715, MILK 18,130→12,117, MELON 16,648→16,648, STRAWBERRY 10,434→3,917, FERTILIZER 8,972→8,820, total 120,360→106,180 (-14,180). Banks: ours 80,581→71,254 (-9,327), theirs 61,474→48,117 (-13,357), **margin +19,107 → +23,137 (+4,030)**. Fertilizer's own revenue moves only +$310 — the exemption frees the h0-h15 window and collapses both players' strawberry/milk books. Not unconditionally good: on seed 3 it is -2,081; rematch corpus 69/97 against 66/97 (p~0.27), not established.

**2. The book is shared.** Seed 11 both seats: MILK ours 186/theirs 249/total 435 into 1 shop-slot at $64/unit; WOOL ours 189/theirs 94/total 283 into 1 slot at $227/unit; STRAWBERRY ours 277/theirs 261/total 538 into 4 slots at $40/unit; WHEAT ours 469/theirs 1,062/total 1,531 into 6 slots at $42/unit. Milk floors because 249 of 435 units are his.

**3. Drain is not what sets the price — supply is.** WOOL is the LEAST-drained product (mean 1.12 shop-slots over seeds 1-40) yet our best-priced at $227/unit.

**4. One wheat tile to tomato: a null on both seeds.** Seed 11 (0 tomato slots): base +19,107 → tomato1 +19,093 (-14). Seed 3 (5 slots): +6,602 → +5,579 (-1,023), 7 units sold @ $63. Combined with the fertilizer exemption: seed 11 -2,702, seed 3 +835. It also cannibalises carrot: seed 3 base sells 12 CARROT at $265/unit and the tomato arm drops it to 11 units at $122.

**5. One goose on a cow: the d0 result is an artifact, again.** `HERD_GEESE=1, HERD_GEESE_FROM=("COW",)` took the d0 cow at places index 1. Margin seed 11 +19,107 → **-12,494**; seed 3 +6,602 → **-2,801**. Not the goose — wool fell $38,207 (189 units @$227=42,871 → 88 units @$53=4,664) because a COOP displaced the COW paired with the first sheep, breaking the FEED/CARE pairing bonus. Every late-day goose swap (d3/d5/d9/d9+d11) was measured byte-identical to base on both seeds 11 and 3 — `SHOP_ADAPT_HERD` overwrites `want_total` and never reads a GOOSE row.

**6. Milk is a denial weapon, not a revenue line.** Model validated: replaying reproduces the recorded season exactly (MILK 12,010 vs recorded 12,006 ours; 18,128 vs 18,130 theirs). Removing one of our four cows, seed 11: our units 186→139 (-47, all $1 units), revenue $12,010→$12,192 (+$182); his units unchanged at 249, revenue $18,128→$24,145 (**+$6,017**). Dropping a cow costs us $0 and hands him $6,017.

**7. CORRECTION: the herd count in section 5/6 was wrong.** Counted off tiles, seed 11: end d0 OURS {SHEEP 2, COW 2} THEIRS {SHEEP 2, COW 2}; end d6 OURS {COW 4, SHEEP 2} THEIRS {COW 4, SHEEP 2}; end d9 OURS {COW 6, SHEEP 4} THEIRS {COW 8, SHEEP 3}; end d20 **OURS {COW 6, SHEEP 8} THEIRS {COW 9, SHEEP 3}**. We run 6 cows / 8 sheep (14 animals), not 4/4. Every denial figure in section 6 is scaled wrong (it assumed 4 cows) and must be re-run.

**8. Production is exact and the grid can be solved.** Per-animal season yield by placement day (COW d0 39...d12 21; SHEEP d0 38...d12 22; GOOSE d0 **56**...d12 32). Validated: 6 cows predict 202 milk against 186 sold (92%); 8 sheep predict 227 wool against 189 sold (83%). Goose out-produces a cow 56 to 39 but sells into a $70 ceiling vs $256. Best-reply table (his cows → our best): he plays 9, our best reply is 5, we play 6 — close to right, worth about $1k on the (later-voided) PASS-agent grid.

**9. CORRECTION: the shop draw is ENDOGENOUS.** `_spawn_weeds` consumes the day's rng once per tile before the shop draw, so tile count (decided by land purchases) moves every later draw. Section 3's table and section 8's grid were built on PASS-agent runs and are **void**. Corrected grid (real shops), seed 11 (CARROT:2 EGG:2 MILK:2 STRAWBERRY:3 TOMATO:2 WHEAT:5 WOOL:2): fixed point at 4 cows. Seed 3 (CARROT:5 EGG:2 MILK:1 STRAWBERRY:1 WHEAT:2): fixed point at 2 cows. Against his real 9 cows on seed 11, our best is 4 and we run 6 — about $7k gap (was $1k on the void grid).

**10. The goose is conditional on YARN_STORE.** At 14 slots, geese take 8 of 14 at 0 milk/0 yarn shops (margin +$13,089, vs -$2,355 with geese banned — a $15,444 swing); at 1 milk/0 yarn, 7 geese (+$11,276 vs -$2,001); at 2+ yarn stores, geese leave the optimum entirely (0 geese, margin +$21,678 to +$26,753). Measured over 24 seeds real play: **38% of draws have no yarn store.** At 18 slots, a yarn store is worth $7,369-$24,287 more than a fourth quadrant purchase ($7,000) at various milk/yarn combos — a no-yarn no-milk board gains only $3,988-$5,963 from Q4 on animals, i.e. **Q4 does not pay for itself on animals alone** on that board type.

**11. What section 10 assumes, and what was tested.** Assumed opponent 9 cows/3 sheep, zero geese, no crops at all. Tested: does the goose survive an opponent who also buys geese? Our best response never leaves geese (rises 8→10, stays there against his 12), margin collapses +18,802 → +2,039 as his geese rise 0→12 — same "contested book pays little either side, hold the position to deny" structure as milk.

**12/13. The ideal split and the d7 uncertainty correction.** No shop exists before d3, so the opening's first six slots are fixed at 3 cows + 3 sheep. Section 12's table (assuming shop counts known) says: no yarn + 0-1 milk → all geese; no yarn + 2 milk → half cows/half geese; any yarn + 0-1 milk → all sheep; +2 milk → 6 sheep 2 cows; +3 milk → 5 sheep 3 cows; +4 milk → all cows. But at d7 only 2 of 8 shops have been drawn, and geese enter EV-optimally only in proportion to egg shops ALREADY SEEN (0 seen → 0 geese, 1 seen → 2 geese, 2 seen → 3 geese). So **`HERD_GEESE=0` is the correct d7 choice on a blind board**, wrong only as a season-long constant. Staging (commit only 3 slots at d7, decide the other 5 informed) captures **74%** of the value of perfect information. Cows are the hedge at d7, not the preference (milk is the modal shop type at 3/8 vs wool's 1/8).

**14. MEASURED AND REVERTED: the milk-conditioned cow cap.** `EARLY_YARN_COW_BY_MILK = (4,4,5,6)` replacing flat `WOOL_SHOP_COW_CAP=6`. Rematch corpus, 97 games: **63/97 against baseline's 66/97. Reverted.** Four played seeds showed the opposite on margin (mean +$2,622, but three fewer wins) — "bigger margin, fewer wins," the same divergence the fertilizer exemption showed pointing the other way. Selecting on money remains wrong even when the money is a margin.

**15. Marginal value per crop unit — wheat is the worst thing on the board.** Per-unit $: MELON 268 (seed 11) / 187 (seed 3); CARROT 63/219; EGG 51/59; STRAWBERRY 105/44; WHEAT 21/20. Per planting (both cap at max_yield 6): melon $1,608 vs wheat $126 — **12.8x**. Adding 72 wheat units costs the opponent only $82 (wheat denial theory is dead); adding 12 melon units costs him -$1,730.

**16. Crop value vs opponent holding — an inverted U.** Contested crops (melon, strawberry) are an inverted U in his holding: strawberry with him ABSENT is -$3,657 (we flood our own book), positive once he is present. Uncontested crops (carrot, egg) are perfectly flat regardless of his play.

**17. The mirror: what a Kawashigi-vs-Kawashigi board pays.** Per-unit price, solo/actual/mirror: MILK 231.3/64.6/51.1 (-78% vs solo); STRAWBERRY 134.8/39.5/40.9 (-70%); MELON 243.2/196.9/147.0 (-40%); WHEAT 31.2/19.8/19.6 (-37%); WOOL 236.7/226.8/224.3 (-5%, the only survivor). This explains why the old goose verdict (measured in a mirror, commit c9c1c18, "-$21k a game at one bird") was garbage — a mirror gluts a shared book by construction. The goose has now been condemned by three unrelated artifacts: SELLABLE omitting EGG, the d0 pen-pairing break, and the mirror glut.

### 2026-08-16 — work to be done (flagged by a prior index pass as the most actionable punch list of the batch)

source: work_to_be_done_2026-08-16.md, 2026-08-16

**1. The opening, d1-d8 — largest known defect.** Per-cell gate fails 260 cells (see contradiction (a) above re: this baseline). Lowest failing day d1 (COLLECT_FERTILIZER 4/3 + PLACE); also d3 WATER 13/14, d4 WATER 16/15, d5 WATER 12/13, d6 WATER 16/19 + PLACE/crop_MELON/weed, d6 BUY_LAND ours h9 vs tape h4 (five hours late), d7 WATER 28/27, d8 WATER 17/33 + PLANT 8/9 + DIG + crop_MELON + crop_WHEAT.
Cadence gate: we buy seed at dawn, the tape defers to dusk (d10 ours h[1,1,1] vs tape h[20-23]; d12 ours h[1×9] vs tape h[14,16,18]; d15 ours h[1,1,1] vs tape h[16,16,18,18,20,22,22,23]).

**2. Watering priority — a fix that exists, is measured, and is switched OFF.** `cover.AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP`, uncommitted, False. Measured seed 11 weeds=0: kills the two d8 weeds, d8 feed 9/10→10/10, plant 6/9→9/9 exact, strawberry 10/11→11/11 exact — but costs d10 sell 95→68 and $4,619 because d10 is a `WALK_THE_LOAD_HOME_DAYS` day. By d13 money is a wash ($18,960 vs $18,880) and weed count is WORSE.

**2a. It is TWO defects.** The pass-order fix targets turn-constrained d7-d11 only. d12-14 deaths (8 strawberry tiles die on d14) are a job-generation defect: `cover.cover` returns early on precomputed days (d12-29 on a 3-quadrant board, d9-29 on a 4-quadrant board) and none of the greedy machinery runs there.
d12-d13 idle: d12 256 unit-turns/idle 77, d13 275/93, d14 211/41 (8 strawberry tiles die), d15 294/30.

**2a-i. Measured, and the d12 half is a NULL.** `scripts/what_the_solved_day_drops.py`: zero jobs dropped on d12-d19 in either arm (no-fork / fork). The fork's real cost is on the back half: d20-27 solved-stop matching collapses (d18 seats 31/59 vs 49/57 unforked), tiles with WATER dropped on 2+ days rise 3→8 with the fork on.

**2b. The solved tail is per BOARD SHAPE — four shapes, not three.** melon-3quad (A3, 91919278), straw-3quad (B3, 91891131), melon-4quad (Q4, 91907974), and straw-4quad — **MISSING, no recorded tape, no solved tail**. Likely the biggest cause of strawberry deaths clustering in fork games.

**1a. REGRESSION found 2026-08-16 — the gate moved and nobody said so.** Bisected: `8b74e05` 260 failed/520 passed → `ed927fe` 300/480 (the q4 herd forced to COW 6/SHEEP 10, +40) → `6a01c59` 303/477 (restored to COW 6/SHEEP 12, +3) → `c5831f9` 303/477 (docs only). The note that the gate "held at 311/590/115/35 through all three deletions" describes only the deletions, not the herd work.

**3. Strawberry is what actually dies, and the fork makes it worse.** Live ladder game 93593633 (planner, LOST $90,355 v $101,782): 21 tiles weeded, 20 ours, **19 strawberry**. Fork fires on 44% of real games (32/72 downloaded replays).

**3a. The fork CAUSES the deaths but doesn't by itself decide the game.** Submission 55548563's 28-episode ladder record: fork FIRED/W (8 games) weed tile-days 62.0, strawberry died 11.9, mean margin +42,798; fork FIRED/L (4 games) 43.8/13.0/-6,904; fork quiet/W (15 games) 43.7/5.5/+16,722; fork quiet/L (1 game) 20.0/10.0/-10,716. The fork more than doubles strawberry deaths (5.5 without vs 12.4 with) in both wins and losses, but doesn't separate wins from losses.

**4. The melon fork is NOT implementable as a tape rewrite.** 24 games: token-swapping MELON→STRAWBERRY inside a melon-recorded tape scores 0.0% win rate against 66.7% with swap off, -$17,297/game. A dig-guard lifts it to 12.5% only. Seed 3 product level: swap is +$2,966 on CROPS, -$8,365 on ANIMAL products (unexplained). One bug identified: 12 wasted PLANTs against 1, because the guard did not suppress the REPLANT after the cancelled dig.

**5. Refactoring — started, not finished.** Deleted so far: `plan_routes`+`_two_opt`+`_path_len`+`COVER_PLANNER` (-319 lines, 10 tests), `board_layout.py`+`sa_hiscadence_probe.py` (-269 lines), 8 hard-OFF flags. Three live files: 9,881 → 9,245 lines. Remaining: 10 hard-OFF flags (blocked by scripts/tests setting them at runtime), 101 hard-ON flags, 63 self-asserting tests, 3 doubly-defined constants (`SELLS_FUND_THE_TURN`, `URGENT_OPS`, `STEAL_FROM_DAY` — second definition silently wins), `victor` still a live tape with 3 bound tests.
The gate for every delete: both suites must report **311 failed, 590 passed, 115 xfailed, 35 xpassed** — unchanged through all three deletions so far (see contradiction (a) — this figure was already stale the same day it was recorded).
`coverage --branch` over five seeds: 25 scripts import 0%-coverage modules, 22 run — `chains`, `dayplan`, `executor`, `library`, `replay_plan` are NOT free deletes.

**5a. The end state, agreed 2026-08-16: split `make_agent`.** `schedule_agent.py` is 5,156 lines, 2,696 comments + 365 blank = 2,095 lines of code, 47 top-level defs of which `make_agent` alone is 1,638 lines. Order of work: finish flag deletions → resolve 8 doubly-defined constants first → collect surviving numbers into one block per file → then split, one module at a time.

**6. What the allocation LP says** (see `docs/allocation_bounds_2026-08-16.md`): leader's MELON 20/STRAWBERRY 34 is not inside the 1% near-optimal region (-1.78% vs zero opponent, -3.9% vs his own supply, -23% vs double supply); strawberry 34 IS inside the 1% interval in two of three scenarios. Melon's 1% interval slides [14,42]→[0,31]→[0,12] with the opponent. Geese become obligatory against a flooder ([8,22] at double supply).

**7. Open and unexplained:** the animal-product loss under the melon swap (-$8,365 on milk/wool, one seed); why swap-OFF wastes 19 FEED/19 CARE/17 COLLECT ops while swap-ON wastes none yet earns more; the ~550 rating points between `fe7aad6`'s 1947.9 and current builds (close package ruled out by ablation: +41.7pp win rate, carried by NO_UPKEEP_ON_THE_LAST_DAY and WALK_THE_LOAD_HOME_DAYS); the q4 branch's yarn-store unlock is not a pure function of the seed.

**8. Live submissions at end of session:** `55548563` (planner, post-1947.9, q4 armed, melon fork d3≥9, ~1500 rating; known defect: q4 rows carry SHEEP 10 while the tape buys SHEEP 12, fixed in `6a01c59` AFTER this bundle was built); `55549820` (tape3, two tapes, dig with day-slack and must-dig, both swaps).
Selection bias warning restated: `~/Downloads` replays are hand-picked LOSSES; within-sample comparisons are fine, a win rate computed from them is not.

### 2026-08-17 — the last two days: dead code, a real gap closed, and what's still open

source: the_last_two_days_2026-08-17.md, 2026-08-17 (branch kawashigi-plan, seed 11, shipped kawashigi plan)

`banking = False` gated a d28 "bank the field" branch on a hardcoded False, pointing at a constant (`BANK_THE_FIELD_ON_D28`) that no longer existed. Deleted.
**The stranded-load gap is CLOSED.** The xfail (51 units, ~$1,192) went XPASS; d29 drop is now 9/9 against the tape; marker removed so a regression is a plain failure.

The one real gap implemented: a ripe PEN on d28 was never promoted to CRITICAL (only crops had a filling-window trigger). `router.animal_ops` now adds CRITICAL to a HARVEST prize on d28 only. Red-first confirmed, all 20 last-day tests pass after.

Result:

    row          d25      d26      d27      d28        d29
    harvest    27/29    24/14    26/35    32/32      19/19      unchanged, before and after
    sell       95/149   87/80    92/72    84 -> 87   160 -> 159
    drop        2/0      2/0      0/0      0 -> 1     9/9
    pass        2/0      0/1      0/0      0 -> 13    22/56
    final money   154,740 -> 155,155   (+$415), tape 150,076

d0-d27 byte-identical between the two runs.
**Harvest did not move** — the finding — because d28/d29 are both in `SOLVED_DAYS` and `_apply_precomputed` seats stops by `(tile, ops)` key without pricing them, so a prize change cannot move a solved day; the +$415 is leftover-greedy margin only. `scripts/resolve_days.py --days 28,29` was running to test whether re-solving closes it (result not in this doc).

Traps recorded: `scripts/diagnose_season.py` hardcodes a different plan (`top_guys/90976060/schedule.json`) and reports $52k against the real $155k — discard any number read off it; seeds do not vary this harness (`--seed 11` vs `--seed 14` byte-identical, since shops come from the replay and terrain is a pure coordinate function); `tests/test_the_second_to_last_day_banks_the_field.py`'s docstring quotes stale numbers (d28 27/32, d29 27/19) against the live grid's 32/32 and 19/19.

Open: eight red tests in `tests/test_the_first_seven_days_match_the_plan.py` (8 failed/6 passed), pre-dating this work, confirmed by stash-and-rerun — real defects: a hand walks off a tile holding a hungry animal while carrying its feed (14 times over d0-d6); animals unfed at dusk with wheat on the farm; a PLACE planned onto a hand that does not build that pen; SELL/BUY_PRODUCT diverging from plan d2-d6.

Four new losses, a different shape (`data/seed_scripts/ladder_2026-08-17/`, 23 replays; two games are byte-identical, so 3 distinct games not 4):

    93850943  vs kaggricultureomnidimensionalut  100,033/106,095  LOSS -6,062
    93850122  vs Пётр П                          125,613/131,285  LOSS -5,672
    93849246  vs Panchajanya Banerjee             54,940/ 60,306  LOSS -5,366
    93846497  vs Sirui Zeng                       89,509/ 98,615  LOSS -9,106

Harvest is LEVEL in all of them — not harvest-deficit losses.
We out-water by 200-275 in every game including wins.
Plant is 5-11 behind.
Correction on a first read: one opponent's CARE 967 vs our 318 is CARE EMITTED not CARE LANDED — `cared_today` gates the effect at ~570/pen-per-day ceiling; it says their agent spams CARE, not that they care 3x more.

**The herd never moves, and one board had ZERO milk shops.** We ran COW 10/SHEEP 4 in all six sampled games across milk-shop counts of 0, 2, 3, 3, 3 and 5 — including the milk=0 board, where milk floors at $1 with zero drain and we flood a buyerless book. This is `MILK_POOR_SHOP_COUNT=1` failing again, now with a milk=0 counter-example. Caveat: milk-slot counts here are from the FINAL town, while the herd is committed d3-d7 — the decision's knowability at commit time was not checked.

### 2026-08-17 — the d5-d11 tape replay cannot converge (HISTORICAL — settled dead end, diagnostic only)

source: replay_window_cannot_converge_2026-08-17.md, 2026-08-17

Inside the replay window the actions are his, so any mismatch there is a defect, not a strategy difference.
Grid (ours/tape), MELON arm: melon d10 11/8, d11 11/8, d12 13/8; strawb d6 2/4 ... d12 28/34; money d6 959/957, d8 1433/1431, d10 12374/16162.
STRAWBERRY arm: melon d10 3/0 ... d12 0/0; strawb d6 4/6 ... d12 36/39; money d10 13020/16403.
Strawberry runs exactly -2 every day from d6 in both arms; melon exactly +3 at d10.
Root cause: our d0-d4 plants MELON on (0,0), (1,1), (3,0); his plants WHEAT there, which clears by d5 and frees the tile for his d5 strawberry (melon stands until ~d10).
Fix: `OPENING_GEOMETRY` pins six squares to the crop he actually sows. After the fix, melon exact at d10/d11 both arms, strawberry closed -2→-1, money at d10 moved from $3.4k-$3.8k behind to level; refusals fell from 5 to 1.
Season money not yet measurable — `solved_days*.py` was solved on the old geometry and needs re-solving on all four arms.
Season totals for the record: our own d0-d29 banks 153,492; best replay window (d5-d11) banks 143,454 — **the replay is a diagnostic here, not a candidate.**
Two bugs found on the way: `replayed` keyed on a name (`state["branch_armed"]`) nothing ever wrote, silently pinning the strawberry latch False; and `state["bought"]` leaked the discarded planner's purchase increments into replayed turns.

### 2026-08-17 — the third quadrant arrives a day late

source: the_third_quadrant_arrives_a_day_late_2026-08-17.md, 2026-08-17 (19 ladder replays)

Two theories died: "we over-water" (we out-water every opponent by +190 to +970 in d11-29 and win most of those games — not a defect); "the problem starts ~d20" (plantings deficit opens at d8, peaks at d10 50 vs 74, closes by d15).
**Q3 lands on d11 in every single one of 19 games, zero variance.** The 821-script buys Q3 on d10. Constraint is cash: at d10 h1 we hold $986 against Q3's $2,000 price; our money arrives in a lump at d10 h23 ($1,527→$6,395) while his arrives smoothly across the day. `LATE_SELL_FROM_HOUR=16` is the obvious suspect, not yet tested.
Cost: 21 tiles lose a full day of growth in every game against this opponent.
Not sufficient on its own: Tom Yim runs the same 821-script profile and we beat him by $5,275.
Never bought Q4 ($4,000) except one game.
Next untried test: get $2,000 into the bank by d10h1 and buy Q3 on d10 — judge on the d10 planting count and d11-29 harvest, not season money.

### 2026-08-17 — wasted late turns

source: wasted_late_turns_2026-08-17.md, 2026-08-17 (fresh download 93880775.json, our seat is 1)

On d28 a hand stood on top of a 3-unit ripe WHEAT tile (9,1) for **seven consecutive hours (h14-h22)** emitting PASS.
On d29 h23 (final hour), all 8 hands were idle while 18 units stood on the field.
Per-day unit-turns d25-d29: idle rises 0/1/1/14/21 as the crew draws down 11→10→8 hands.
Feasibility test (`hours_left >= 2*distance`): 35 idle hand-hours d28+d29, 20 feasible. Deduplicated: (4,6) WHEAT 1, (9,1) WHEAT 3, (2,4) COW pasture 3, (4,6) WHEAT 2, (5,3) COW pasture 2 — 11 units reachable-and-unharvested, 7 of them still standing at the actual close.
Separate defect, not counted above: at hour 1 of every day d25-29, `action['hands']` is empty while `farm['hands']` shows 10 (d29: 8) positions still on the board, and 10 HIRE orders fire the same turn — ~300 unit-turns/season, systemic, not diagnosed.
Data-shape trap recorded: tiles are indexed `tiles[y][x]` (row, column), not `[x][y]`; caught via a LOCKED-tile consistency check (correct indexing hits exactly the 4 shed-adjacent tiles, wrong indexing produced 260 bogus hits).

### 2026-08-17 — dead-constant audit of kagg/search/

source: dead_constant_audit_2026-08-17.md, 2026-08-17

40 module-level boolean constants checked by reading the guard, not grep. **17 have a branch that cannot execute.**
The one that matters: `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE=False` at `schedule_agent.py:2761` makes block 2796-2814 unreachable, killing `MILK_POOR_COW`, `MILK_POOR_SHEEP`, `MILK_POOR_SHOP_COUNT` — the herd has never responded to the milk draw because the rule is switched off, not mis-gated.
Other dead branches listed by constant/file:line/value: `AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP` (cover.py:113, False), `SUPPLY_LIMITS_EVERY_DRAW` (cover.py:170, False), `DELIVER_SURPLUS_NOT_THE_ROW` (cover.py:240, False — kept deliberately, REGISTER.md OPEN-1, measured -$15,272/12 seeds), `BANK_THE_ROWS_PRODUCE_WHILE_REAPING` (cover.py:274, False), `STRICT_FEASIBILITY` (crew.py:126, False), `SHOP_ADAPT_CROPS` (schedule_agent.py:2624, False), plus several hard-True dead-else flags: `MEMOISE_SLOT`, `BRANCH_ON_THE_YARN_STORE`, `LIVESTOCK_ENABLED`, `PLAN_THE_CREW_THAT_ARRIVES`, `LATE_SEASON_PAIR`, `HIRE_FIRST`, `ANIMAL_OVER_HIRE`.
Orphaned (defined, never read as a condition): `CLOSED_TOUR`, `TOP_UP_SAFE_TILES`, `SEED_BEFORE_LIVESTOCK`.
Note on `HARVEST_WHAT_YOU_STAND_ON`: listed live here, yet the same-day wasted-turns doc measures a hand standing on ripe wheat for 7 hours doing nothing — "live" means the guard can execute, not that it fires when it should.

---

### CALLOUT — unresolved contradiction (b): full-season vs partial-replay head-to-head

> `the_last_two_days_2026-08-17.md` reports the full shipped season finishing **+$415 ahead of the tape** (154,740 → 155,155 vs 150,076).
> `the_tape_beats_our_planner_2026-08-21.md` reports that at a d24 tape-to-planner handover, the planner **LOSES $7,713** to a full tape replay, before that day's three one-line bug fixes.
> The setups differ (full season vs. partial replay-then-planner) and neither file cites the other or states whether the fixes since 08-17 changed the 08-21 number.
> Not necessarily a real conflict — flagged so nobody quotes either number as "the" head-to-head result.

---

### 2026-08-19 — MEASURED AND REVERTED: the strawberry cap loses $28,259 (do not retry)

source: the_tapes_are_both_strawberry_rich_2026-08-19.md, 2026-08-19

Both kawashigi tapes are strawberry-RICH boards (92466371: d12 straw 37/4-of-4 strawberry-shops; 92498144: d12 straw 27/3-of-4 shops), so on those boards 37-42 strawberry tiles is the correct allocation and neither tape can measure the strawberry float.
Cross-check against tetsuya's 79 seats confirms it: at 4 strawberry-shops he plants 36.8, matching kawa's 37-42.
The flood is that we plant 42 on EVERY board, including the ~31% of draws with 0-1 strawberry shops, where both leaders plant only 26.

**`STRAWBERRY_TILES_BY_DRAIN = (26, 26, 35, 36, 37)` was implemented, measured against baseline `b35feee`, and REVERTED.**

    arm           baseline    with float    delta      strawberry   wheat
    straw_q3       155,601      145,048    -10,553      42 -> 37    124 -> 120
    melon_q3       139,453      139,453          0      34 -> 34    134 -> 134
    q4_melon        93,929       78,594    -15,335      34 -> 30    133 -> 125
    q4_straw        78,305       75,934     -2,371      42 -> 38    128 -> 124

Three losses, one structural null. **-$28,259 in total.**
Mechanism: cutting strawberry did NOT hand the ground to wheat — wheat went down on every arm that moved (124→120, 133→125, 128→124). Strawberry seed also sat unsown in the shed. The suspected cause (precomputed routes solved against the schedule's own crop counts, `_apply_precomputed` keying on exact `(tile, ops)`) is **not established** — the one isolation test run (a 2x2 dropping the routes) pointed the OTHER way for tomato: tomato's loss got WORSE without routes (-1,117 → -13,156), refuting the route-desync theory for tomato on that arm. The strawberry isolation itself has not been run.
`melon_q3` returned byte-identical on both route settings — a non-experiment, because the melon/q4 branch resets `UNSOLVE_DAYS` and the override never took.

Order required before any crop-mix test means anything: choose the target mix, re-solve all four route tables against it (days 12-23), A/B mix-vs-mix each on its own routes, score on paired-seat win rate — not money.
The same confound applies to `WHEAT_TILES_TO_CARROT` and `WHEAT_TILES_TO_TOMATO`.

Tomato, for the record, same session: the "tomato-shops at d12" column used to justify a conditional gate was **read from the tape JSON, not the live env** — the forced seed re-rolls the shop draw. Printed live: straw_q3 4-drain tomato1 -1,117; melon_q3 2-drain +5,692; q4 1-drain -11,655. No monotone shop condition; the conditional-tomato gate was implemented, measured, found to fire on the q4 board and lose $11,655, and reverted.
Timing constraint: d4-d11 are replayed from the tape, so 37 of 42 strawberry tiles are already standing at d12 dawn regardless of any float — the honest ceiling for a post-d11 float is the last few tiles plus replant decisions from d12 on.

### 2026-08-20 — flag audit: 151 constants, 14 deleted, 27 inert, 22 one-branch

source: flag_audit_2026-08-20.md, 2026-08-20 (base commit 486d51c, kawashigi-plan; scope schedule_agent.py/cover.py/router.py, 5762/1723/1454 lines)

**151 module-level constants found by AST walk (92 in schedule_agent.py, 25 in cover.py, 34 in router.py), not the 145 estimated in the brief.**
Result: 14 constants deleted, 4 lines of unreachable code deleted, 11 docstrings corrected, harness byte-identical before/after.
Totals: TUNING NUMBER 48, LIVE 40, INERT 27, ONE-BRANCH 22, DELETED 14 — **27 of 151 are inert and 22 more have a dead branch: a third of the module-level surface does not discriminate anything at runtime.**

Method miss worth keeping: an AST walk over `Name`/`Attribute` reads misses `setattr`-by-string ablation drivers. `scripts/close_package_ablation.py` flips flags through `setattr(mods[mod], flag, want)` from a dict of NAME STRINGS. `TRIM_A_TAIL_THAT_CANNOT_COME_HOME` was deleted and then restored after this was caught — had it shipped deleted, the ablation would have silently set an attribute nothing reads and reported a byte-identical arm indistinguishable from a measured null. Same recovery applied to `STEAL_FROM_DAY_MARGIN` (read only by `scripts/who_claimed_the_last_work.py:38`). Standing rule for future audits: grep the quoted string too, and check `setattr` sites.

14 deletions, each zero-reader or hard-flag-with-no-external-reader (proved by AST + literal-string grep + setattr audit): `LAST_FREE_DROP_DAY` (both copies), `WORK_TURNS`, `CHAIN_OPS`, `YIELDING` (router.py copy), `MIN_SELL_ROW_DROP`, `DELIVER_FERRY_MARGIN`, `RANK_HOME_DAYS`, `PLACE_DRAWS_FEED`, `LATE_SEASON_PAIR`, `HARVEST_A_TRUNCATED_ONE_SHOT`, `HARVEST_WHAT_YOU_STAND_ON`, `ANIMAL_OVER_HIRE`, `SELLS_FUND_THE_TURN`, and 4 unreachable lines in `will_be_fed`.

Eleven docstring/code contradictions corrected (prose only, no code changed to match prose), the most consequential: `router.py:838` `will_be_fed` had an unconditional `return True` sitting in front of its own stated rule, making the actual rule-code below it dead — this is also why `FEED_CADENCE_FROM_DAY=7`'s cadence never existed, and why `test_a_pen_that_has_not_started_producing_is_not_fed_unless_it_is_hungry` **fails at the base commit** (left red and documented, not fixed — three non-equivalent ways out identified: delete constant+test, re-enable the cadence, or leave it red). Also: `WHEAT_TILES_TO_TOMATO`'s headline still said "unconditional" after a 2026-08-19 retraction at the foot of the same block already said otherwise.

Proof of no behaviour change: tetsuya's own tape/seat/opponent (seed 959074148), before/after grids byte-identical (`PLANT 212/212 BUILD 15/15 FEED 309/353 CARE 310/353 HARVEST 393 WATER 1031 PASS 1373`, herd COW 6/SHEEP 5/GOOSE 3 vs his COW 8/SHEEP 2/GOOSE 3, crop counts CARROT 8/MELON 8/STRAWBERRY 32/WHEAT 164 all matching row targets exactly). Wide test suite: 28 failed/107 passed/4 skipped before and after, identical FAILED set.

Needs-a-decision items (nothing deleted, each has a reason to wait for Alex): the six close-package ablation flags (may never be deleted while that script exists); `STEAL_FROM_DAY`/`STEAL_FROM_DAY_MARGIN` (zero/one readers respectively, deleting means deleting a diagnostic script); `FEED_CADENCE_FROM_DAY` and its failing test; nine hard-True flags with long cited comment blocks; `HOMEWARD_DROP_TURNS=0` kept deliberately as half of a recorded measurement pair; the whole precomputed-route mechanism (intentionally off in the shipped agent, `UNSOLVE_DAYS=range(0,30)`, but live tooling for three rebuild scripts); `HIRE_PINNED_DAYS=frozenset(range(30))` always true (narrowing is a behaviour question); `FEED_DAYS == FEED_DAYS_LATE == 1` (three tuning numbers, one live value).

### 2026-08-20 — our geometry is not tetsuya's

source: our_geometry_is_not_his_2026-08-20.md, 2026-08-20 (tetsuya seat 0, seed 959074148, `data/seed_scripts/downloads_2026-08-19/94345389.json`)

Boards diverge at **d1**, the first placement day, and never converge: 14 of 100 cells differ at d1h0, 14 at d2, 14 at d3, 20 at d4, 17 at d5, 20 at d6.
`PLANT 90/90` on the d0-d10 grid means the same NUMBER of tiles planted, never the same TILES — the count grid is blind to geometry by construction.
Three costed differences: his field is a solid block (rows 0-2), ours is scattered including the far corner (3,0)/(3,1)/(4,0), so every water/harvest walks further; pen cells differ (four of five shared, one moved); crops land on the wrong tiles (d1 he puts STRAWBERRY at (0,0)/(0,1)/(0,2), we put WHEAT there and strawberry elsewhere).
Three independent causes, all measured: tetsuya's schedule carries no coordinates (fixed 2026-08-20, `tape.json` now built, 242 placements over 73 tiles, but the schedule has not been regenerated from it); `plan.load(strip_tape_only=True)` by default strips coordinates and nothing in the repo passes `strip_tape_only=False`; the live agent (`schedule_agent.py`) never reads `plant_tiles`/`build_tiles` at all — only two comments say it derives placement off the board instead, and `dayplan.py`'s coordinate-carrying branch is offline-only and unreachable from the shipped agent.
Worth: the tape's own tiles banked $11,638 against $6,794 for ours on the earlier `new_leader` board (1.7x, 2 refusals vs 17) — quoted as the reason the mechanism exists, not re-measured on tetsuya's board.

### 2026-08-20 — PLANT is a money problem, not a planting problem

source: plant_is_a_money_problem_2026-08-20.md, 2026-08-20 (same board/seed as above, d0-d10)

Router == Plan on every single day (ROUTER == PLAN == 72 across the season) — the router and planner are not the defect. Season sum: pins 72, ROUTER 72, PLAN 72, EXEC 57, his 68.
**d7: 4 missing plants belong to a unit that was never hired.** All four stops at (8,3)/(9,3)/(9,4)/(8,4) with PLANT+WATER were never reached — `_do_hire` fails silently on a thin bank, and the whole four-stop tour for the phantom 11th hand vanished with it. Seeds were not the constraint (18 STRAWBERRY seed arrive h1, 4 still sit in the shed at h23; all 14 submitted plants landed).
**d10: the bank is $0 from h2 to h17.** `BUY_SEED CARROT 8 / WHEAT 9` re-posts every hour and cannot fill until h18, when all 16 seeds arrive at once and only 5 plants follow in the remaining 6 hours.
`REPLANT_A_CLEARED_TILE` never fires: `chain` is 0 every day — the ten tiles the d3 harvest clears are never re-sown (a real, separate hole in `router.build_nodes`).
Consequence: do not tune the planting path — the binding constraint is cash at hour zero.

### 2026-08-20 — the day idles while the herd starves

source: the_day_idles_while_the_herd_starves_2026-08-20.md, 2026-08-20 (same board/seed, d4)

Chain: two hands never assigned → 3 pens unfed on d4 → escape at d4 night → herd 7 vs his 8 on d5, 1-3 short every day after → fewer mouths → FEED/CARE trail all season.
d4 detail: row asks feeds=8, places=['COW','COW'], buys={'WHEAT':6}; 7 pens reach the ground, only 4 are fed. Slots 4 and 8 are PASS in every single hour of the day. Idle climbs 2→6 after h17, day ends with 3 unfed pens. ~67 unit-turns idle on d4.
One hungry pen had also missed d3, hit `consecutive_unfed >= 2`, and escaped overnight — herd reads 7 on d4, 6 on d5.
Reframes the standing "PASS 911 vs his 679" open item as the SAME item as the FEED/CARE gap, not a separate one.
Ruled out: wheat supply (all 4 sent FEEDs on d4 landed), the arrival budget (`ARRIVAL_FEED_REMAINING` computes correctly at 2), `will_be_fed` (standing animals reach the unconditional return True), the market slot gate (measured inert twice).

### 2026-08-20 — the ration is not in the shed when the plan says it is

source: the_ration_is_not_in_the_shed_when_the_plan_says_it_is_2026-08-20.md, 2026-08-20 (same board/seed)

Three-checkpoint trace (ROUTER/PLAN/EXEC) shows the router offers FEED on every pen every day and the plan commits to every one — four instances fail purely at EXEC: d3 (4,3) COW, d4 (3,3) SHEEP, d4 (4,2) COW, d4 (4,3) COW (unfed=1).
The break: the dawn plan credits the row's full `buys={'WHEAT':6}` at hour 0 and routes a PICKUP-then-pen tour, but the unit reaches the shed at h1 before the wheat has arrived (PICKUP loads nothing, or a COW instead), arrives at the pen with no ration, and `FEED` (which draws from the ACTING UNIT'S CARRIED inventory, not the shed) silently drops, taking CARE with it — the turn goes to COLLECT_FERTILIZER instead and the unit walks away. Wheat trickles in h2-h6; by h9 the unit carries one and walks past the now-already-spent pen stop.
`RANK = dict(FEED=0, CARE=1, COLLECT_FERTILIZER=2, ...)` was never overridden — FEED lost the turn because it was never offered, not because it lost a priority contest.
Cost: pen (4,3) misses d3 and d4, hits the escape threshold, and escapes at d4 night.
Not verified: whether the h1-empty-shed is our own buy cadence dripping the order across the day, or the book being too thin to fill at h0 — these need different fixes.

### 2026-08-20 — the sells land after the hire

source: the_sells_land_after_the_hire_2026-08-20.md, 2026-08-20 (same board/seed)

Harvest is exact on every day d0-d10 (10/10, 3/3, 2/2, 5/3 on d9, 4/4) — not a defect, don't look at it again on this board.
Selling fertilizer is his strategy too: d0-d10 fills WHEAT ours 28/his 35, FERTILIZER 58/66, WOOL 22/27, MILK 9/12, revenue $12,473/$13,968 — the "we sell fertilizer we should use" theory is refuted.
Real divergence: **he blocks his sells at dusk, we dribble all day.** His two biggest hiring days are funded by a block sale at h23 landing as cash at next day's h0: d6h23 sold 14 units → +$2,302 at d7h0 (11 hands that day); d9h23 sold 12 units → +$1,543 at d10h0 (9 hands). Ours on the same transitions: d6 sold h7:7+h16:7, only +$87 cash at h7 with 10 hands; d9→d10 sold just 1 unit, +$81 cash, 7 hands.
We reach d10 dawn with $1,164 against his $2,073; bank sits at $0 from h2-h17, 11 of the day's 19 plantings die there. He is not richer over 11 days ($13,968 vs $12,473, a $1,495 gap) — he has the money AT HOUR ZERO and we do not.
Two genuine revenue holes flagged, not yet separated: d3 he sells 30 WHEAT to our 15 off the same 10 harvested tiles; d8 he sells 21 units for $3,213 (MILK 12) to our 7 for $975 (MILK 6), the largest single-day gap at -$2,238.
MEASURED NULL: pricing a FEED at the CARE bonus it releases (`min(max_held,held+1+bank)-min(max_held,held+1)` times price) was correct economics but measured byte-identical on the d0-d10 grid — reverted. It is not a ranking-contest loss; the pen is failing for lack of stock (shed empty from h8 on d7, unit arrives at h15 with an empty hand).

### 2026-08-20 — FEED is measured against ops he wasted, not ops that landed

source: feed_is_measured_against_ops_he_wasted_2026-08-20.md, 2026-08-20 (tetsuya seat 0, seed 959074148)

`FEED` draws from the acting unit's carried inventory, not the shed — if empty, it returns silently and the animal stays unfed. Nine of tetsuya's own FEED ops in the first 16 days do exactly that.
Submitted vs landed, d0-d15 cumulative: FEED 158 submitted / 149 landed; CARE 158/158 (CARE has no input cost, submitted always equals landed).
On d0 he submits 5 FEEDs and lands ZERO — buys 5 WHEAT at h1, sells all 5 back at h2, shed reads 0 the rest of the day.
Corrects the d0-d10 grid reading: the FEED gap is really **73 against 76** (his achieved total), not 73 against 85 (his submitted total) — three ops, not twelve; the CARE gap of nine is real and is now the LARGER of the two.
Retires the wheat-supply theory for d0 entirely: matching him exactly on d0 would mean WASTING five turns — feeding the d0 arrivals is a place we can beat him, not a place we are behind.
General rule restated: measure at the decision (post-step), not at the census (the action dict) — an op counted from the action stream is only an intention.

### 2026-08-20 — the tape dies at d13, and the unit slot is why

source: the_tape_dies_at_d13_2026-08-20.md, 2026-08-20 (kawashigi, 191 downloaded games, holdout 94439800, full 30-day seasons)

The `(day, hour, unit)` tape clone matches op counts to 6.5% but banks **$22,592 against the teacher's $153,443**. Exact through d18, then flat: d11 clone 17,419/teacher 17,025 (ahead); d16 27,757/24,705 (ahead); d18 35,977/35,321 (level); d19 40,141/44,712 (breaks); d24 43,395/91,154; d29 42,976/139,400. $2,835 earned d19-29 against his $94,688; bank FALLS d24-d26.
Cause: unwatered crops, not spawned weeds. `weedSpawnChance=0.005` for both, teacher holds 0-1 weeds through d28; clone crop/weed counts d12→d29: 53/0 → 1/48, teacher 54/0 → 3/17. Every one of the 48 weeds is a missed water (two dry days = WEED). Chain: phase drift by d12 → WATER fires on the wrong tile → tiles go dry → WEED → PLANT blocked (needs EMPTY) → seeds stack (clone WHEAT seed stack 5→20 over d15-18 while teacher holds steady at 8) → crops collapse 53→1 → production stops, wages continue.
**The 6.5% op-match figure never measured execution** — both sides count are pre-`env.step` requests; op NAMES match, tile ARGUMENTS do not. A HARVEST on a bare tile, a FEED with no wheat, a PLANT onto a weed all score as "matches."
**The unit slot is not stable between games**: arm-vs-arm tape diff read 42-55% of slots differing, but within-arm control (47 v 47 games, 5 splits) reads 17.2-22.0%, and two INDIVIDUAL games in the SAME arm differ on up to 61.5% of slots — more than arm-vs-arm. Hands are indexed by hire/arrival order, which varies between games, so the modal tape blends incompatible tours (e.g. `d0h4 u4 BUILD_PASTURE ↔ u5 WEST` swapped between games).
Two binary branch decisions found: melon-12/no-q4 (n=94, median $86,974), melon-20/no-q4 (n=45, $91,981), melon-12/q4-on-d12 (n=32, $103,431), melon-20/q4-on-d12 (n=20, $100,577) — **we currently ship the weakest of the four lines**, and the q4 branch is worth ~$15k median and is the later, easier decision. Melon branch opens d6; land branch opens d12 and always bundles Q4 with two late SHEEP.
Standing constraint: an open-loop tape has a shelf life of about **twelve days** on a board it did not create — independently re-derives the d12 handover the shipped agent already uses.

### 2026-08-21 — d0-d3, cell by cell

source: d0_to_d3_cell_by_cell_2026-08-21.md, 2026-08-21 (game 92498144, seed 11, seed-first ordering AND netting both in place)

**0 of 4 days exact by the grid's own count.** Per-day differing cells: d0=3, d1=3, d2=1, d3=4 (then d4=3, d5=7, d6=16, d7=13, d8=19, d9=14, d10=17, d11=17, d12=13).
d0's 3 cells (money -3, SELL 0/3, BUY_PRODUCT 5/8) are entirely a netting artifact: every board/shed quantity matches exactly (shed_WHEAT 3/3 both sides, net wheat traded +5 both sides); he round-trips buy-8-sell-3 for the same net +5 that we get from buy-5-sell-0. **Expected-different, should not be chased** — if d0 is wanted green, netting has to come out, and it cannot be both.
d1's 3 cells (money -3 inherited, COLLECT_FERTILIZER 4/3, PLACE 3/2, shed_FERTILIZER 1/0) are a cadence difference: we dispose of fertilizer one unit at a time as collected (h3/h9/h15/h22, the h22 one never disposed), he accumulates three and clears them in one PLACE + one SELL x3 at h18.
d2's 1 cell (money +2) is unexplained — every op, crop, shed level and herd count match; no SELL on either side, BUY_PRODUCT 4/4, so it's a realised-price/fill difference the grid aggregates, not a trade-count difference. Flagged as the cheapest next diagnostic in the whole problem, not yet taken.
d3's 4 cells (money +22, crop_WHEAT -7, HARVEST +7, BUY_SEED -1) are one decision: **we harvest seven wheat tiles he leaves standing.** WHEAT is harvestable d2-d4 (first_yield_day 2, max_yield_day 4); he waits, we take it immediately. d3 is also the melon/strawberry split day, making this the wrong day to be diverging on. Not diagnosed further.

### 2026-08-21 — d1's fertilizer dribble is a named, measured rule — and fixing it reverts a win

source: d1_bank_cadence_handoff_2026-08-21.md, 2026-08-21

Mechanism located, NOT changed — a policy call for Alex.
`BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY` in `cover.py`'s `materialise` loop (~line 723) banks immediately whenever a pen job yields something the row sells and the unit stands on a depot tile (pens sit on shed-access tiles by construction). On d1 with four pens on depot tiles, this banks after every COLLECT_FERTILIZER, producing exactly the three non-inherited d1 cells (PLACE 3/1, COLLECT_FERTILIZER 4/3, shed_FERTILIZER 1/0).
The conflict: the sibling rule's own docstring, from a DIFFERENT tape (Seb's, day 1, seed 11), argues explicitly FOR spreading over batching, with its own measurement: dribbling 4 units across h4-h12 realises $2 more than batching the same 4 units in one turn, because the market walks price down within a turn. Our own d1 trade is exact against Kawashigi otherwise (BUY_PRODUCT 5/5, SELL 3/3, shed_WHEAT 4/4) — the -$3 is entirely inherited from d0, and d1 loses zero money on its own, only three op-count cells.
Stated plainly: matching Kawashigi requires suppressing a rule that is a measured win against Seb's tape. Kawashigi banks once; Seb's tape banks four times; the executor has one global answer and can only agree with one player.
Recommended next steps, not acted on: decide the d1 policy question; take d2's still-unexplained $2 turn-level cash trace; look at d3's wheat-harvest-timing as one ranking rule, likely worth more than d1's three cells since it's also the melon/strawberry split day.

### 2026-08-21 — unsure, needs an owner's eye: BUY_SEED outranks BUY_PRODUCT

source: seed_outranks_product_the_fix_and_its_cost_2026-08-21.md, 2026-08-21

> Read this first: the fix regresses `tests/test_each_day_matches_the_tape.py` from 263 failing cells to 301. It was asked for, it does what it was asked to do, and it makes the shipped agent's own gate worse. That is a decision for Alex, not for me, and nothing is reverted or disabled.

`schedule_agent._wheat_row_first`'s hour-0 `BUY_PRODUCT WHEAT` insertion point is now clamped to sit after the last `BUY_SEED` in the same turn (days with no seed order that turn are untouched). Confirmed red on revert.
On game 92498144's own rows, d0-d12: differing cells before 132 total (d0=6...d12=14) → after 106 total (d0=2...d12=10). Money at d12: 7,150/15,565 before → 12,666/15,565 after (**+$5,516**). Weeds at d11: 13/0 → 6/0. d0 PLANT 18/19 → 19/19, BUY_SEED 18/19 → 19/19.
**d0 is still NOT exact** — two cells remain, opposite sign to the original defect: money ours 100/tape 16 (+84), BUY_PRODUCT ours 5/tape 8 (-3). Fixing the seed-money leak now under-fills the product order and closes the day $84 rich.

**The cost, on the gate that drives the SHIPPED agent** (a different Kawashigi season, 92498144, from the one this fix was tuned against): baseline 263 failed/517 passed → with fix **301 failed/479 passed** — 38 cells flipped from pass to fail.
Two readings offered, not separated by this measurement: (1) the ordering is right and the shipped grid was passing for the wrong reason, tuned against a front-loading executor; (2) the ordering is genuinely player-specific — Victor orders product first, Kawashigi orders it last, and no single global answer serves both. Reading 2 is called the more likely one.

**Recommendation: do not ship this as it stands.** Options stated, none taken: keep it and re-tune the shipped grid against the new ordering; revert it and accept the executor cannot round-trip a seed-first row; or — since neither is a flag — make the ordering a property of the ROW (whose season it came from) rather than a boolean on the module.
Part 2 (rebuilding the plan library smaller) was explicitly NOT started, because the precondition (the executor round-trips a row) still fails: 0 of 13 days exact, d0 two cells away, d6-d12 nine to sixteen cells each.

### 2026-08-21 — the executor cannot play his own row, and it misses from d0

source: the_executor_cannot_play_his_own_row_2026-08-21.md, 2026-08-21 (answers Alex's question "strange that it cant match the d3 -12...")

Feeding the executor game 92498144's own d0-d12 target rows (not action replay — a target row carries no hours/coordinates/movement/WATER, the router regenerates all of that): **0 of 13 days are exact, and the first divergence is d0.** Per-day differing cells: d0=6, d1=5, d2=2, d3=4, d4=4, d5=7, d6=10, d7=12, d8=19, d9=15, d10=18, d11=16, d12=14.
d0 hour-by-hour: ours spends h0 on `BUY_PRODUCT WHEAT x9` + 5 HIREs, leaving $7 at h1 for `SELL WHEAT x3, BUY_SEED MELON x1, BUY_SEED WHEAT x1` — the WHEAT seed order posts every hour from h2 to h23 and never fills again ($6 against a $10 seed cost). The tape instead does all 5 HIREs plus all 19 seed buys at h0, spreads the wheat PRODUCT buy over h6/h12, and ends d0 with $16 against our $6.
d0 field diffs: money -10, crop_WHEAT -1, PLANT -1 (18/19), WATER -1 (18/19), BUY_PRODUCT +1 (9/8), BUY_SEED -1 (18/19) — one plant short, $10 short, exactly one wheat seed.
Same failure family already documented for BUY_ANIMAL vs BUY_SEED (`SEED_BEFORE_LIVESTOCK`); BUY_PRODUCT is simply not in that ordering at all. Pinned by `tests/test_the_seed_order_outranks_the_product_order_at_dawn.py`, `xfail(strict=True)` — not fixed in this doc (the fix is the seed_outranks_product work, above).
Cost cascade traced: d5 sell 13/23, d6 money $16/$957, d8 crew 3/11 (`_do_hire` silent fail on thin bank), d10 crew 5/11, water 3/32, unit-turns 139/270, d11 thirteen weeds against his zero.
Conclusion (the fork this doc resolves): **BRANCH B — the executor does not reproduce a row it was handed.** Do NOT build a d7-d13 row-selector: feeding the PERFECT row for d0-d12 still produces 0/13 exact days and leaves us $8,415 behind at d12 ($7,150 vs $15,565) — selection was worth $4,644 by d13, execution is worth more than that on its own. Order of work: fix d0, re-grade, move to the next divergent day, only reopen selection once the executor round-trips a given row.

### 2026-08-21 — the carrot window is three days wide

source: the_carrot_window_is_three_days_2026-08-21.md, 2026-08-21

Answers Alex: "how can we perturb kawa and add carrot without breaking stuff in the back half" / "carrot friendly towns throw in some carrots in the backend instead of wheat."
Instrument: `kagg/search/tape_edit.py`, seam already used by the submission bundler, nothing shipped as a flag. Control-arm check: `surplus_sells` wrapper banks $96,198 with or without itself — silent when the tape already covers a sale.
First sweep (2 tiles/day, d20-25, seed 11): **-$6,787 for twelve tiles**, $566/tile — far more than a wheat crop is worth. Cause is lifespan, not economics: CARROT dies (`planted+4` days) and WEEDS faster than WHEAT (`planted+5`), and the sweep created 7 extra weeds landing entirely in the last two days' harvest, while total PLANT ops stayed 203/203 in both runs (nothing dropped by the atomic rule, the plants just died standing).
Corrected measurement — the carrot window is d25-d27 specifically, where a five-day sowing cadence gets truncated by the season's final bell (27-32 tiles per tape on those three days, where carrot's max_yield_day 3 fits inside the truncation and wheat's max_yield_day 4 does not):

    arm                        bank        delta    weeds   plants
    control                  $96,198          +0       25      203
    carrot, all of d27       $96,139         -59       25      203
    carrot, all of d26-d27   $96,073        -125       25      203
    carrot, all of d25-d27   $95,807        -391       25      203
    tomato, 1 tile d12-d15   $95,758        -440       27      203

Loss collapsed from $6,787 to $59 by narrowing the window; weed count returned to control's 25.
Caveat: seed 11 has no carrot drain — CARROT drains at/above WHEAT on 4 of 16 towns measured (seeds 1337, 4096, 13001, 60013), and that's where this has to be judged.

**Eight-town run, twelve arms, scored twice — money and margin disagree.** carrot2_d25d27 -$92 money/-$105 margin (4/8 wins); carrot_d26_all -$110/-$126; carrot_d25_all -$206/-$258; carrot4_d25d27 -$293/-$317; carrot_d27_all -$300/-$302; carrot_d26d27_all -$439/-$458; carrot_d25d26d27_all -$869/-$957; carrot2_20_26 -$3,239/-$3,770; **tomato1 +$4,846 money / -$5,546 margin**; tomato2 +$4,455/-$8,633; tomato3 +$286/-$11,579. Every arm held the control's 4/8 win count — nothing here changed a single win.
Tomato's opposite-sign columns are the "select on win rate, not money" lesson in its most expensive form: the mechanism is that tomato arms plant fewer wheat tiles, lowering our own wheat supply into the shared book and raising the price for BOTH seats — seed 42 shows tomato1 making us $21,517 richer and $16,684 further behind in margin.
Sample-size correction, same day: the town draws 8 shops WITH REPLACEMENT from 8 types (8^8 ≈ 16.7M draws, not ~70) — the eight sampled towns were seed-picked, four deliberately because they drain carrot, biasing the carrot arms upward.

**3,648-season town grid (48 towns x 19 opponents x 4 arms), added later the same day.** Pooled, the full carrot arm reads -$370 (looks like every other null), but split by town CARROT drain it is not: drain 0 → -$2,133 mean margin (26% win), drain 6 → **+$1,937 mean margin (40% win)**. Drain-6 towns are 11% of the true draw distribution (drain ≥4 is 36.7%) — a conditional rule would fire ~1 game in 9, worth roughly **+$210/game in expectation**, resting on only 3 towns / 57 seasons (thin). Tomato is dead at every drain level (-$675 to -$7,040 across drain 0-6, 2% win rate vs the mirror).
Herd probe: herd_cow_d8 -$1,048 margin (5/12 wins, not a real "more cows" test — `_herd_split` has already capped cows on dry towns by d8); herd_sheep_d8 -$19,651 (1/12); herd_counter_d8 -$13,217 (3/12); herd_counter_d12 -$808 (5/12). `tape_edit.herd_shift` (bounded post-d0 head moves): +4 cows -$34,089, -4 cows -$9,459 — a local optimum in both directions, one town/one opponent.
Two coverage failures found only by instrumenting: the q4 tape never armed in the whole 3,648-season grid (0/76 combinations — needs a d3 YARN_STORE which uniform draws rarely place there; fixed via `stratified_towns`); the opponent pool spans leaderboard rank, not behaviour (7 cow-leaning/2 sheep-leaning, three strongest sheep players absent) — replaced with an explicit `BEHAVIOUR_SPAN`.
Timing is closed, five independent negative results: fixed-hour sales lose $4,698 (h23) to $26,601 (h0); adding an order without removing his is a wash; intraday WHEAT price range is under 2%; no top-six agent sizes an offer against the book; the SEASONAL gradient (WHEAT +81%, STRAWBERRY +58%, MILK +30%, WOOL -98%) is what matters, not the hour.

### 2026-08-21 — the tape beats our planner, and three bugs were hiding it

source: the_tape_beats_our_planner_2026-08-21.md, 2026-08-21 (commits 1be532f, 032254c, b105d05)

Playing カワシギ's recorded season all the way to d29 finishes **+$240 ahead of him** on seed 11, with zero differing cells every day through d20, 1-2/day after (see contradiction (b) above regarding how this relates to the d28/d29 +$415 full-season figure from 08-17).
Handover-boundary sweep (`--replay-days N`), money as a level (ours minus tape) at end of day:

    handover   season money vs tape   cells d24-d29
      d24            -$7,713          13 14 15 16 14 8
      d28            -$1,615           2  2  1  2 12 10
      none            +$240            2  2  1  2  1  1

The planner turns 2 differing cells/day into 13-16 the moment it takes over, wherever the handover sits.
Three one-line bugs found and fixed: (1) only one of four tapes was ever reachable — `_MB.arm`/`_Q4.arm` were deleted for an unrelated reason, so `melon_armed`/`q4_armed` were never written and `_replay_opening` always read `(False, False)`; (2) `DECIDE_BY_DAY` moved 6→5 because the q3/q4 tapes actually split at d5, not the schedule-row split day of 9; (3) our own BUY_SEED trim left us $60 richer than the tape at d6, silently buying a hand (`_do_hire`, silent fail on thin bank) at d8 that the tape itself was refused — cascading into weed/WHEAT/STRAWBERRY divergence for the rest of the season. This trim was found to be dropped on the strawberry arm but KEPT on the melon arm, where it is the entire +$240.

16 seed-drawn towns, d0-d29, cells against the tape the latches actually chose: q4/yarn-by-d3 (6 seeds) 23-35 → **0**; q4/yarn-at-d6 (3 seeds) 69 → 43 (now declines the q4 plan); melon/no-yarn (7 seeds) 34-41 → 34-43; strawberry (5 seeds) 60-132 → **0**; strawberry (10 seeds) 130-132 → 25; strawberry (1 seed) 40 → 40. **11 of 32 arm/seed combinations now play an exact whole season.** Residual on clean arms is money and sell-cadence cells only, not field ops.

Disproved along the way: the herd re-label (removing it was byte-identical — reverted, not left runnable); "verified on seeds 11-14" (the harness injects the tape's own recorded town into both columns, so four seeds was one measurement repeated four times); "200 different plans by d20" (conflated ~174 distinct whole rows, mostly executor noise, with 25 distinct crop multisets and 4 real replay branches — the middle number is one plan with a wobbling tile count, not 200 strategies).

Geese/tomato census, 4,022 seats: geese CLOSED by absence (best goose seat plays 3-4/season, nobody builds around them). Tomato OPEN: one real candidate, game 94469635, banks $162,943 with 105 tomato ops — $13k above our current tape — but the archive's best bank overall touches neither token, at $185,263, so tomato is not where the top of the distribution lives.
Not established: the melon/strawberry latch tested against only two opponents (16/16 both ways, but two values of one variable); how often a melon opponent appears on the ladder at all (never counted, scales all of section 4); everything in the headline is one seed on the tape's own recorded game; whether game 94469635's opening is itself a fixed script (which would make it a fifth tape).

### 2026-08-15 log — why we lost: two ladder replays, unit-level

source: why_we_lost_93318573_93323101.log, 2026-08-15 (raw script-output dump, not summarised into a table)

Two downloaded LOSSES on `weedSpawnChance=0.005`, `townCenterSellInterval=24`, our seat 0. Game 93318573: LOSS, us $68,714 vs James Mancillas $69,359 (margin -$645); town shops BAKERY(1)/BRUNCH_SPOT(1)/FARMERS_MARKET(2)/PIZZA_SHOP(1)/SMOOTHIE_SHOP(1)/YARN_STORE(2); we ran COW 10/SHEEP 4 planting WHEAT 223/STRAWBERRY 165/CARROT 97/MELON 12 against his COW 8/SHEEP 6 planting WHEAT 67/STRAWBERRY 41/MELON 26; MILK closed at the $1 floor (drained 358) while WOOL closed $232 (above $200 base, drained 716), EGG $65 (above $50 base), TOMATO $280 (far above $60 base, drained 537) with neither side producing tomato; closing-week deltas show both sides accelerating spend d23-d28 (us $54,673→$65,004, them $51,333→$58,479); weeds: us 28 from crop-miss + 5 from spawn (55 DIGs, 2 final), them 32 from crop-miss + 6 from spawn (29 DIGs, 16 final). Game 93323101: LOSS, us $119,623 vs Adarsh $123,542 (margin -$3,919); shops FARMERS_MARKET(1)/ICE_CREAM_SHOP(1)/PET_CAFE(1)/PIZZA_SHOP(1)/SMOOTHIE_SHOP(1)/YARN_STORE(3); we ran COW 6/SHEEP 8 planting WHEAT 252/STRAWBERRY 160/CARROT 63/MELON 12 against his COW 8/SHEEP 6 planting WHEAT 92/STRAWBERRY 42/MELON 24; here MILK closed AT base $160 (not floored, drained 537) and WOOL closed $246 (drained 1,074); closing week both sides added money every day (us $82,431→$111,642, them $86,556→$113,396); weeds: us 28 crop-miss + 2 spawn (49 DIGs, 0 final), them 17 crop-miss + 0 spawn (43 DIGs, 0 final). Both losses are the pair analysed in `the_stranded_load_is_the_loss_2026-08-15.md` above (stranded produce exceeding the losing margin).
