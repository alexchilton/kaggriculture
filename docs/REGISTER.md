# Register — what is open, what is closed, and what keeps reopening

Last updated 2026-08-13, on `shaping-potential`.

## What is in which file

**`docs/` holds four files, plus this one.** A second severe pass on 2026-08-13 went from 17 (the
first pass's result) down to four, because 17 was still too many to open. Nothing measured was lost
in either pass — every number, seed range, date and verdict from every deleted file was copied into
whichever surviving file now covers its topic, and the "Where deleted content went" table below names
every one, for both passes.

| File | What it answers |
|---|---|
| `REGISTER.md` (this file) | The live open/closed list. Check it before opening anything — items here reopen under new names, sometimes six times. |
| `competition_brief.md` | **The game.** Rules, scoring, deadlines, the action/observation space, engine rules that have each cost a day, the 1.32.2/1.32.6 version skew, and the measured economics — yields, town drain, supply vs drain, storage timing value, the price-curve mechanics and depth/saturation tables. Facts about the environment, not about us. |
| `architecture.md` | **The agent.** What it actually is, how a day is planned and executed, which flags ship OFF and why (with the numbers that turned them off), the harness warnings, current pool score, the current herd/wool sizing rules, and every planner bug found by diffing against a reference tape (Seb's and Victor's), the spawn-ring misprediction, and the fertilizer/wheat supply defects. |
| `experiment_log.md` | **Everything measured, in date order.** Every experiment and its score (§1-24), plus (added this pass) the market findings-about-us, the two real-loss depth analyses, the ladder-population study, what real opponents do, the Orbit Wars lessons, the RL track's full argument (including the warning not to reintroduce the per-step reward it overruled), the problem-framing note, and the throughput measurements. |

## Two corrections that apply to almost everything measured before 2026-08-13

1. **`SELLABLE` excluded CARROT, TOMATO and EGG until commit `c99a8a5` (2026-08-13).** Our own agent
   could not emit a SELL for those three products regardless of market conditions. Any older
   conclusion about carrots not selling, or about geese/eggs being unprofitable, was measured with
   that revenue line disconnected and is void — flagged inline wherever it survives below. See the
   third version-caveat block further down for the full statement.
2. **The ladder moved to `kaggle-environments` 1.32.6 on 2026-08-07/08** — town-centre drain fell
   roughly 8x (`townCenterSellInterval` 12→24, the late-season demand ramp deleted). Any dollar
   figure dated before that is on a different economy; `competition_brief.md` "Version skew" has the
   mechanics.
3. **The herd count is a floor, not a fixed number, since `1f7d457` (2026-08-13).** Any doc that
   still says the schedule's animal count is what ships, or that `SHOP_ADAPT_FROM_DAY = 3`, predates
   `HERD_GROWS_WITH_THE_DRAIN` and is stale — `architecture.md`'s herd-sizing section has the current
   rule.

## Where deleted content went

### Second pass, 2026-08-13: 17 files down to 4

`README.md` is gone — its index became the table above, its "what got deleted and where" record is
this section, extending the same record forward.

**Into `competition_brief.md`:** `economics_q5_findings.md` (whole — yields, town drain, supply,
allocation, storage, selling into a shared book), plus the analytical, environment-mechanics
sections of `the_market.md` (the derived price-curve depth table and the per-product/per-head
saturation tables — computed from `reference/kaggriculture.py`'s formulas, not from play).

**Into `architecture.md`:** `matching_the_tape_mechanisms.md`, `spawn_ring_and_routing.md` and
`fertilizer_and_wheat_supply.md` (each whole, as new sections), plus a new herd-sizing section
sourced from commit `1f7d457`.

**Into `experiment_log.md`:** the remaining, findings-about-us sections of `the_market.md` (the
87-tape appetite measurement, fills-vs-offers, intra-day cadence, the late-season investigation,
carrot economics, ranked levers); `market_depth_and_the_morning_losses_2026-08-13.md` (whole — its
depth table was cross-referenced, not duplicated, in the first pass, and now lives here verbatim);
`the_ladder_is_two_scripts.md` and `the_field.md` (whole); `lessons_carried_over.md`, `rl_feasibility.md`
(whole, with `CLAUDE.md`'s warning that reading it alone would reintroduce the overruled per-step
reward carried across intact), `what_kind_of_problem_this_is.md` and `throughput_measurements.md`
(whole).

### First pass, 2026-08-13: 45-49 files down to 17

Condensed; the full per-file table is in git history (the commit that first wrote this section).
`the_market.md` absorbed nine 2026-08-09/-10/-12/-13 market write-ups plus carrot economics.
`the_ladder_is_two_scripts.md` absorbed six field-description and loss-forensics write-ups.
`matching_the_tape_mechanisms.md` absorbed ten tape-diffing write-ups. `spawn_ring_and_routing.md`
absorbed three routing write-ups. `fertilizer_and_wheat_supply.md` absorbed two supply-defect
write-ups. This file (`REGISTER.md`) absorbed four more as new OPEN items or extended CLOSED
entries. `architecture.md` absorbed the parity-restoration headline and the shipped-pool-score
table. `experiment_log.md` gained two entries (§25-26) for the stage-1 abandonment and a pointer to
the wheat-supply fix.

### Earlier: 2026-08-08 (87 files → 11) and 2026-08-11 (added the ladder-population study)

Condensed further still; git history has the full record (`git log --follow -- docs/README.md`).
Most of the 2026-08-08 cut was session narration, superseded diagnosis, or an advisor write-up whose
recommendation had been measured and rejected. 2026-08-11 added what became
`the_ladder_is_two_scripts.md`'s content after the official episode datasets (2,744 seats) overturned
the working assumption that Seb's tape was the strategic target.

## The rules that survived every cull, in one place

- **Check the env version before trusting a number.** 1.32.2 → 1.32.6 on 2026-08-07/08: town-centre
  drain halved (then halved again on the later `townCenterSellInterval` 12→24 move — 8x total), melon
  absorption fell, the `BUY_PRODUCT`-bypasses-`shedCapacity` loophole closed.
- **Check SELLABLE before trusting a carrot/tomato/egg/goose number.** Fixed 2026-08-13, `c99a8a5`.
- **Check the herd-sizing flags before trusting an animal-count number.** `HERD_GROWS_WITH_THE_DRAIN`
  and `SHOP_ADAPT_FROM_DAY = 0` landed 2026-08-13, `1f7d457`.
- **The ladder is Elo and starts at 600.** Winning matters, margin does not. Select on win rate.
- **We are not close to the field.** Best submission 1,257.9 against a field top of ~3,210 (2,744
  ladder seats, `experiment_log.md`).
- **The ladder deals one fixed board, not a random draw per seed.** "Seed variance ~15%" describes
  `kagg.arena`'s randomly-drawn boards, not the ladder.
- **Never evaluate against `starter` alone, the arena pool, or the handover fixture as the whole
  story.** `vs_tapes.py` against `oldleader` is the instrument that currently discriminates.
- **A mirror match is not a best response.** An Elo ladder rewards beating a *field*.
- **Judge a fix at the day it targets, field by field.** Season totals are a weak signal, and
  `breakdown.py --diff`'s `money` row is an *area*, not a deficit.
- **A gate only tests what it exercises.** Ask what a passing test could not reach.
- **After fixing, revert the fix and confirm the test goes red.**
- **Before believing a measurement about a mechanic, ask what the code could not express.** Animal
  economics have been an artifact of our own code five separate times now.
- **Prefer a replay to an aggregate whenever the aggregate could be a tie.**
- **We plant a fifth of the wheat the field does.** 24 tiles against the field's 108-147.
- **The cow COUNT is what floors our own milk price**, not sell timing — every recent real loss
  where `SHOP_ADAPT_HERD` cut cows to 6 closed milk above base; every one at 8-9 cows floored it.
  (Pre-`1f7d457`; the herd is no longer pinned at the schedule's count, re-verify once measured in
  the arena.)

`CLAUDE.md` at the repo root holds the project rules, the kill criteria, and the "lessons learned the
hard way" list. It is not superseded by anything here.

> **Version caveat, added 2026-08-09.** The ladder moved to `kaggle-environments` 1.32.6 on
> 2026-08-07/08. The `STATE at last update` block below, and most dollar figures elsewhere in this
> file, were measured on 1.32.2 or against a fixture that did not yet reflect the town rebalance
> (`competition_brief.md`, "version skew"). Both simulators briefly **failed parity on 1.32.6** (8
> failures) earlier on 2026-08-09 and were **restored to exact parity the same day** — four
> behavioural rule fixes (locked-tile movement, DROP/PICKUP/PLACE ordering, shed-capacity caps on
> BUY, shop unlock with replacement); see `architecture.md`'s PARITY CORRECTION note. One search-layer
> regression was left open: `test_two_different_far_tiles_are_not_the_same_farm`. The *mechanisms*
> below (routing, feed, geometry, discard timing) are still believed correct; the *dollar sizes* are
> not to be trusted without re-measuring on 1.32.6. See `docs/experiment_log.md`'s "the market"
> section for the current, 1.32.6-dated market picture and its "the ladder is two scripts" section
> for the current ladder gap.
>
> **Second version caveat, added 2026-08-11.** The `STATE at last update` block below, and the
> baseline command it names, judge the agent against Seb's recorded tape. `docs/experiment_log.md`'s
> "the ladder is two scripts" section (2,744 ladder seats) found that tape was optimal under the OLD
> `townCenterSellInterval=12` economy — Seb's own median bank halved when the rebalance landed and he
> has since withdrawn from the ladder. Matching his tape op-for-op is still useful as a bug-finding
> harness (see the mechanism note on OPEN-1 through OPEN-8), but it is no longer the strategic target.
> The field plants 108-147 WHEAT tiles a season; our schedule plants 24. See `docs/experiment_log.md`
> for the rebase recommendation (Dmitry Belan or Efe Can Celiksoy) and the current market-appetite
> picture.
>
> **Third version caveat, added 2026-08-13.** `SELLABLE` excluded CARROT, TOMATO and EGG until
> commit `c99a8a5` (2026-08-13, "Three of the nine products could never be sold, and the wool rule
> fired too late") — our own agent could never emit a SELL for those three products regardless of
> market conditions. **Any measurement or verdict below (or in any deleted doc folded in here) about
> carrot not selling, or about geese/eggs being unprofitable, was taken with that revenue line
> disconnected and is VOID.** C-23 below is the clearest casualty: the crops it says the ladder
> "plants 0.2%/0.0% of the time" include carrot, measured while carrot could not be sold by us at
> all. Geese/eggs are now a live axis in the running product-mix sweep rather than a closed question.
> See `docs/experiment_log.md`'s "market depth and the morning losses" section for the corrected
> depth table (EGG is one of only two products — with WHEAT — that never floors) and the
> confirmation that this revenue line is now connected.

This file exists because items in this project get closed under one name and reopen under another.
Melon has been opened and closed at least four times.
**Before opening anything, check the CLOSED section — and check whether your item is really OPEN-1
wearing a new label.**

Ground rules:

- An item is CLOSED only if there is a measurement or a test that would go red if it came back.
  "We tried it and it seemed fine" is not closed.
- Every claim names the file that proves it. A claim with no artifact is UNVERIFIED and must not be
  quoted as fact.
- The reference tape is a **diagnostic**, not the goal. Beating it is the goal, so "the tape doesn't
  do this" is never an argument against a change.

The framing, the architecture and the harness caveats live in `architecture.md`. Read the harness
section there before quoting any number below — three separate instruments in this project have
mis-scored an arm.

> **READ FIRST — the `money` season total is an AREA, not a deficit.**
>
> `breakdown.py --diff` sums the per-day difference between two bank curves.
>
> ```
> money   ... d27 -1781   d28 +1365   d29 +4586
> final bank    OURS 121,221    TAPE 116,635    -> we finish $4,586 AHEAD
> ```
>
> This was misread as a deficit for a whole day and drove several wrong conclusions, including
> calling the `FILLING_WATER` arm a regression when it moved the FINAL BANK from +4,586 to **+5,736**
> while moving the area from -103,724 to -106,686.
>
> **Judge an arm on d29, or on the day it targets. Never on the season total.**

---

## The thing that keeps reopening

**OPEN-1 is one defect that has been worked under at least six different names.**

Melon timing, the stranded carrier, the return leg, the delivery node, the sell-row delivery, and
"shed to shop" are all the same failure: **product is harvested late in the day and is still in a
unit's hands at dusk, so it reaches the shed via the overnight sweep and cannot be sold until
tomorrow.**

Each label got investigated, partially disproved on its own terms, and closed — and then the defect
resurfaced under the next label, because what was disproved was that particular *mechanism*, never
the *symptom*. That is why it reads as "opened and reopened like mad and never solved".

Seven separate arms were attempted and all seven reverted. **All seven were judged on season
totals**, which is the wrong metric, and none checked field-by-field whether the arm moved the field
it targeted. So "seven failures" is much weaker evidence than it sounds.

Anything that looks like late selling, idle hands at dusk, product sitting in inventories, or a
missed same-day sale belongs to OPEN-1. Do not open it as a new item.

---

## OPEN

### OPEN-1 — the largest open defect. Animal produce is sold a day late, all season

Owner: nobody.

Milk and wool ride in a unit's hand for the whole day and only reach the shed via the **overnight
rollover sweep**, so what we sell today is yesterday's production. The shed then holds roughly
**twice the tape's milk for twelve days** and dumps **103 units on d29** into a falling price curve.

This is the same symptom as the six labels above, now measured on the product that carries the
revenue rather than on day 10's melon. It is not a delivery-threshold problem and it is not a
harvest-ordering problem — both of those were chased and closed (C-19, C-20). It is that the shed
trip for a *yielding* pen is not planned as a stop with the rest of the day.

Two cures were built and both ship OFF with their numbers in the source; do not rebuild either
without beating them. See `architecture.md`, "the flags that ship OFF":

- `cover.DELIVER_SURPLUS_NOT_THE_ROW` — the broad version measured **-$15,272 over twelve seeds**.
- `schedule_agent.STAND_AT_A_DRY_SHED` — **money@d16 23,483 → 16,363, cows 8/8 → 5/8**.

The direction that has *not* been tried: make the draw and the delivery **see the shed contention at
plan time**, rather than reacting to it at execution time.

### OPEN-2 — Survival water is never discounted for how far off the yield is

Owner: nobody. Split out of the `FILLING_WATER` fix; d11 regresses `-422 → -1516` with `weeds +3`,
`strawb -3`, `water -3`.

`_crop_remaining` prices a survival water as the whole tile regardless of how many days away that
tile's yield is, so insurance on an immature crop is never discounted for waiting.

**Do not fix this by weakening `FILLING_WATER`** — that is exactly what the rejected arm did, and it
gave back the whole d10 gain (see `experiment_log.md` §19).

Almost certainly the same mispricing behind OPEN-4: a survival water over-priced early is also
over-priced late.

### OPEN-3 — `sh:milk +464` and `buy_product -164`: possibly one mechanism, possibly the whole play

Owner: nobody.

The two largest unowned rows. We hold up to **+50** more milk in the shed than the tape at d22, and
the tape **buys 164 more product units** than we do across 27 of 30 days.

Possibly one mechanism, not two: buy wheat → feed animals → produce milk. The teardown of the top
agents found the winner drew ~83% of revenue from milk and wool by converting **bought** wheat into
animal products (`docs/experiment_log.md`, "what the opponents actually do"). So `buy_product -164`
may not be a bug at all — it may be the one
strategic play we never make.

The mechanism behind the milk half is exact and is at `schedule_agent.py:1649,1655`:

```python
n = min(have, allow, rate[prod])
n = min(n, allow - state["ordered"][("sold", prod)])    # allow = the schedule row for the DAY
```

**We sell exactly the quantity the schedule row names and no more, however much the shed holds.**
That is why "we sell every day" and "the shed has heaps in it" are both true: the cap is Seb's
production rate, and we produce more than Seb. The row is an absolute count read off *his*
trajectory.

A parked arm nearly fixes it — sell down to a `shed_dusk` target: `sh:milk` +446 → +46, and the
final bank lands within **$62** of his. It costs d4 and d5, which currently match, via an unexplained
`sh:wheat -2` from d4. The obvious explanation (the WHEAT/FERTILIZER reserve subtracted twice) was
tested and is **not** the cause. Left unfed until the cause is found; see the comment block at
`schedule_agent.py:1630`.

Constraint on any fix: CARE correlates **+0.441** with money across 312 real leaderboard seats, so
"do less CARE" is not a safe inference from the diff alone.

**Partially superseded 2026-08-09.** `PRICE_AWARE_SELL_CAP` and `RESERVATION_SELL_CAP` are both now
`True` in `schedule_agent.py`, replacing the schedule-row-only `allow` this section describes with a
live-price rule. Whether that closes this item has not been re-measured against the mechanism
described here; see `docs/experiment_log.md`'s "the market" section (§4-5 of the merged content),
which found milk and wool still under-priced on real ladder losses even with both flags on.

### OPEN-4 — The strawberries die eleven days too early

Owner: nobody. `scripts/thirsty_strawberries.py`, `data/logs/thirsty_strawberries.log`.

Counting every tile transition across the season, both seats:

```
                 died of THIRST              first death
OURS   STRAWBERRY 41, WHEAT 2                d11
SEB    STRAWBERRY 41, WHEAT 1                d22
```

**The totals are identical** — we are not losing crops Seb keeps alive. The difference is entirely
*when*:

```
OURS  d11 1, d13 1, d15 2, d16 3, d21 2, d22 5, d23 6, d24 4, d26 9, d27 3, d28 5
SEB                                        d22 3, d23 8, d24 8, d26 9, d27 3, d28 10
```

Seb loses his entirely from d22 — the final week, when another watering cannot pay itself back. That
is deliberate end-of-season abandonment. We start at **d11**, when each tile still had ten or more
days of yield left. That is the whole of `strawb -94` and `sh:straw -78`.

NOT caused by the sheep-placement fix or by `FEED_TURN_CAP` — the first death is d11, which precedes
both.

### OPEN-5 — The herd starves from d16, and it is a reachability failure

Owner: nobody. `scripts/which_pens_go_hungry.py`, `scripts/is_the_feed_wheat_gone.py`,
`data/logs/two_missing_sheep.log`.

```
        d13  d14  d15  d16  d17 ... d28
OURS      9   11   11    9    9        9    empty_pens 0,0,0,2,2..2   in_shed 0
SEB       9   11   11   11   11       11    empty_pens 0 throughout
```

Three escapes, not two: `(8,0)` d16, `(6,5)` d17, `(9,0)` d18. It is a **death**, not a failure to
buy and not the shed-stranding bug, and the register's own rule says correctness floors are never
traded away. It appeared as a consequence of fixing C-12: placing more animals filled 19 pens, and
the feed cadence cannot carry 19 pens. **Third time a fix has exposed a defect the old bug masked.**

The difference from the tape is not how many pens go hungry — he leaves 1-3 unfed most days too. It
is that **he never leaves the same pen unfed twice running**; his hungry set is different every day
and ours repeats:

```
OURS  d15 (8,0)=0 -> d16 (8,0)=1 -> ESCAPED      SEB  d15 (1,3),(2,2)  d16 (1,2),(2,3)
      d16 (6,5)=0 -> d17 (6,5)=1 -> ESCAPED           d17 (1,6)        d18 (1,2),(3,2)
      d17 (9,0)=0 -> d18 (9,0)=1 -> ESCAPED
```

Three candidate causes tested and **all three dead**: not the price (`router.py:554` already sets
`hungry = consecutive_unfed >= 1` and adds the escape-prevention bonus on top of MANDATORY); not the
stock (at d16 h20 we hold 10 wheat with one pen at risk); not the `have_wheat` guard (our wheat never
reaches zero on d15-d18).

The decisive observation: at d16 h20 we hold ten wheat, a FEED **is** emitted, and it goes to a pen
that is *not* the one about to lose its animal. So what remains is **reachability** — the at-risk pen
was not servable by whichever unit held the wheat. That is a routing failure, not an economics one.

One contrast worth keeping, not established as causal: Seb reaches **every** dawn holding exactly 19
wheat, one per pen (d15-d18 all read 19), and draws 16 into hands by h4. We reach dawn with 6-10 and
top up through the day.

*Correction on the record:* first reported as "-2 from d10". That was a column-offset miscount. It is
**d16**, and the `sheep` row is `an_SHEEP`, animals standing, not an op count.

### OPEN-6 — Idle diverges only when the board gets busy

Owner: nobody.

`idle +427` over the season; `pass` is the same row. Small early, growing with board complexity:
d5 +25, d9 +24, d10 +39, d27 +54. d5 is the isolation point — 208 unit-turns and 9 pens against
d10's 294 and 15.

Recurring shape, observed twice and not explained: *early there is budget but no free unit; late
there is a free unit but no budget.*

Note the day-10 finding that reframes this. It was measured under the old `plan_routes` planner and
has **not** been re-measured under `cover.py`, but the shape is the reason chasing the idle row
directly has failed: at h2 — the last crew-change replan — the planner produced tours totalling
**195 turns against 273 turns of crew capacity**, so 78 turns were surplus *at plan time*, before a
unit had moved. Measured idle on the day was 72-73. **The idle was in the plan from the morning**,
and no executor path can recover work the node set never contained. The whole day's node inventory
was 34 at h0 and 37 by h1 — there is not 273 turns of board work in it, and `build_nodes` has no
other vocabulary. Re-measuring this under the covering planner is the first move on this item.

### OPEN-7 — The PLACE gate is fitted to one seed

Owner: nobody.

`PLACE_IS_MANDATORY_FROM_DAY = 14` in `kagg/search/router.py` works and is a day number read off
seed 11; generalising it cost $15,882 on another. The general rule is believed to be "this animal
was already in the shed yesterday", which needs shed age plumbed through `build_nodes`.

### OPEN-8 — A same-turn `HIRE` then `BUY_ANIMAL` can be booked as bought and silently refused

Owner: nobody. Traced 2026-08-08 in `logs/confer_diag_place2*.log`.

`schedule_agent`'s order-construction closure tracks a local `money` to gate `BUY_LAND` and
`BUY_ANIMAL`. `HIRE` appears nowhere in the list of places that variable is decremented, so
day 4 emits `[SELL WHEAT 2, HIRE x8, BUY_ANIMAL COW 1]`, the local gate sees ~$404 against a $400
cow and accepts, and the real env — which settles sequentially — has $384 + ~$20 − $54 of hires =
~$350 and **silently refuses**. Because `state["bought"]` is incremented unconditionally at
construction and `want_total` is cumulative, **the animal is gone for the rest of the game**, not
delayed a day.

Signature in the diff: the `an_COW` row pinned at **-1 for 27 of 30 days**.

This is the **second distinct trigger** for a symptom already fixed once: slot-count truncation past
`orders[:10]` did the same thing and was fixed by `FIT_ORDER_SLOTS`/`_fit_slots` "uncounting"
anything cut for space. Insufficient real funds is not guarded.

### OPEN-9 — Merge to `main`

Unblocked as of the green slow suite.

### OPEN-10 — Rebase the schedule off Dmitry Belan or Efe Can Celiksoy, not Seb

Owner: nobody. `docs/experiment_log.md`, "the ladder is two scripts" section, 2,744 ladder seats.

Seb's tape (`data/seed_scripts/top_guys/90976060/schedule.json`, the plan this repo matches
op-for-op) was optimal under the OLD `townCenterSellInterval=12` economy: WHEAT 24 / STRAWBERRY 41 /
MELON 17. His own median bank halved ($137,747 -> $77,737) when the town rebalance landed and he has
since withdrawn from the ladder. The field's answer to the new economy is the thing he does not do:
plant 108-147 wheat.

**Dmitry Belan** (35 games, `COW 9..9 SHEEP 4..4 WHEAT 142..143 STRAW 36..37`) is recommended as the
rebase target — near-zero variance makes it a pure script, so the plan reads noise-free. **Efe Can
Celiksoy** (53 games, WHEAT 143..146) is an equally clean second source for cross-checking. Not
THUNDER THUNDER (the #1 by rating): it is reactive (7/30 days identical across its own games; one
same-seat pair only 1.2% identical), so there is no fixed plan to extract from it — it is a sparring
opponent and the evidence that an adaptive cow/sheep split is worth roughly 110 rating points on top
of a fixed script.

This is not the planner, the watering or the market logic; it is the target. Nothing in the
"matching-the-tape" line of work (OPEN-1 through OPEN-9 above, and the mechanism docs banded
2026-08-11) needs to be redone — it needs to be repointed at a different tape and re-derived, the way
the router's tape fixture was once already repointed for the 1.32.2 -> 1.32.6 move (see
`docs/architecture.md`, "matching the tape" section, "the mechanical fix: repointing the tape").

### OPEN-11 — Watering: 61 of our tiles go to weed against the opponent's 0, in a real loss

Owner: nobody. Loss `91888327` (seed unrecorded here, `weedSpawnChance=0.005`,
`townCenterSellInterval=24`), re-verified 2026-08-11 with `python -u scripts/why_we_lost.py
data/seed_scripts/ladder/91888327.json --me "alex chilton"`:

```
WEEDS by origin (CROP = a missed watering, EMPTY = a spawn):
   US    from CROP  64  from EMPTY   6  cleared   9  DIGs   9  final  61
   THEM  from CROP  34  from EMPTY  15  cleared  49  DIGs  49  final   0
```

We lose 64 tiles to a missed watering against their 34, clear 9 of ours against their 49, and finish
the season with 61 dead tiles standing against their 0. This is a distinct failure from OPEN-4 (the
strawberries die eleven days too early) — that item is about *when* a tile is allowed to die at
season end; this one is about *how many* die from under-watering and are then never cleared.

**A claim reported to this session and not independently re-verified in this pass: 44 of 64 losses in
the loss sample show a weed-driven divergence concentrated on d13 and d16.** No script or log
producing that aggregate was found under `data/logs/` or `scripts/` as of 2026-08-11 — the per-episode
figure above is confirmed, the 44-of-64 aggregate is not. Per this file's own ground rule, treat the
aggregate as UNVERIFIED until a script that reproduces it is committed and named here.

### OPEN-12 — The feed reserve's eviction throttle is unpaced against reachable room

Owner: nobody. `docs/fable_the_discard_problem_2026-08-09.md` (folded in here; file deleted).

**Self-correction on the record first:** the discard metric this item used to be measured on
(`held_at_dusk − shed_at_dawn`) double-counted hour-23 `SELL`/`BUY_PRODUCT` as loss. Corrected,
env-exact figures: full season **7 units** discarded (not the 105-137 first reported), handover-11
**123 units** (not 145) — a ~15x overstatement. Final money was identical either way. Do not quote
the old 105/145 figures.

**A real, fixed bug (shipped):** `FEED_RESERVE_YIELDS_TO_OVERFLOW` had no day gate despite every
comment describing it as a day-16+ lever — it fired from day 0 against a 4-animal herd. Fixed at two
sites in `schedule_agent.py` (sell-side ~line 2549, buy-side ~line 3109), gated on
`day >= FEED_DAYS_FROM_DAY`. RED before (`tests/test_the_feed_gate_is_a_late_season_lever.py`, 15/16
days differed), GREEN after, reverted and reconfirmed RED.

**Tried and NOT shipped (measured, not a win):** releasing the wheat reserve broadly to evict more
aggressively. Across 7 seed/mode combinations (seeds 11-14, handover-11 and full-season), it made
discards **worse in 5 of 7** and money **worse in 4 of 7** — worst case full-season seed 12,
**-$13,304** for 39 fewer units discarded. Do not rebuild the broad eviction fix without beating
this.

**Still open:** the router's "unreachable room" claim (the reason we don't evict more: there's
nowhere to put it) is only **partially** true. Of 17 residual discard nights on seed-11 handover-11,
10 had wheat already at/below the eviction floor (claim holds, nothing left to sell) but **5 nights
(d16, 17, 18, 20, 24) had wheat sitting 9-29 units above the floor while product still died** — d20
is the sharpest: 48 units of wheat in shed (the entire shed) against a floor of 19, 29 units of
reachable room unused, 15 units of other product destroyed the same night. This is a sell-side /
eviction-throttle pacing question, not a room question, and it is untested.

### OPEN-14 — The late-season STRAWBERRY dump, and the ladder is one fixed board, not a random draw

Owner: nobody. `fable_where_next_2026-08-11.md` and `kawashigi_one_board_2026-08-13.md` (both
folded in here and into `docs/experiment_log.md`'s "the ladder is two scripts" section; both files
deleted).

**The dump, ranked #1 by net-trade gap.** Against Victor's tape (seed 11, replayed), the per-product
gap is STRAWBERRY **-$22,323** (dominant — half volume, half a late-season dump: 30u@$168 d20 →
29u@$68 d22 → 12u@$20 d23 → 28u@$7 d24, while Victor sells *more* volume the same days at
$182/$162/$114), then WHEAT -$4,948, MELON -$3,166, FERTILIZER -$869. **WOOL is a proven win
(+$10,146)** — holding instead of dumping already beats the tape. MILK is a wash (+$1,533) because
Victor's own milk book floors at $1-5 from d16, capping any herd-split cleverness at "low thousands,
not tens" — the same floor `docs/experiment_log.md`'s "market depth and the morning losses" section
documents independently on real ladder losses. **This is the same failure class that section's two
named losses (92550780, 92562037) describe: we ship volume into a book that's about to floor instead of
holding it.** Not yet fixed; the likely site is `SELL_TO_MAKE_ROOM` or shed pressure overriding the
reservation logic in the late-season sell block.

**Field never buys a 4th quadrant.** Every one of 20 top-ladder seats sampled finishes at exactly 3
quadrants; the 15th/16th daily hire costs $610/$987 in Fibonacci pricing at that crew size —
marginal at best. Not worth chasing ahead of the dump above.

**The ladder runs on ONE fixed board, not a random per-seed draw — this changes what "seed
variance" means for the ladder specifically.** 16 downloaded games of the ladder's then-current #1
(カワシギ, 15-1, bank range $44.9k-$150.0k) plus 4 of our own games are hash-identical on
world/market/tiles observation (terrain, land parcels, town positions, opening prices) across all 20
games and both seats. **The project's "seed variance ~15%" figure describes `kagg.arena`'s randomly
drawn boards and does not apply to the ladder**, which deals the same board every game; only the
shop-unlock draw and weed placement vary.

**This also corrects the standing "winners are open-loop" framing for the current #1 specifically**
(`docs/experiment_log.md`'s "what the opponents actually do" section's finding still holds for the
players it measured — this is additive, not a reversal of that evidence). All 16 of カワシギ's games
are byte-identical for exactly the first 74 turns (d0 through d3 hour 1) — the exact window before
the first shop-unlock draw (`townShopUnlockInterval=3`). After that, pairwise action-vector identity
drops to 26%-82% and divergence tracks the **shop draw**, not the opponent (same-opponent pairs
diverge as early as d5 h15). Hour 1 stays identical across all 16 games through d23; hour 0 is the
most divergent hour from d14 on. **Correction, 2026-08-13 (`1f7d457`): `SHOP_ADAPT_HERD` no longer
starts on day 6.** `SHOP_ADAPT_FROM_DAY` moved 3→0 the same day this item was written — day 0 was
buying `COW 1 + SHEEP 4` blind, before any shop draw exists, which is now recognised as the single
largest uninformed commitment of the season and has been fixed to float from day 0 instead. カワシギ's
response still reaches the whole plan from day 3, one shop-draw cycle earlier than our now-day-0
species floor can react to an actual draw (the first draw lands day 3 regardless of when the code is
willing to read it). Diffing
his fixed 74-turn opening op-for-op against ours is cheap and unexplored.

### OPEN-13 — `run_arena`'s seat swap corrupts any agent with a baked-in seat

Owner: nobody. `docs/arena_state_leak_2026-08-09.md` (folded in here; file deleted). Found while
fixing the state-leak bug below (C-25) and deliberately not chased in the same pass.

`run_arena` swaps seats to measure both orderings, but has no way to tell an agent factory which
seat it is building for. An agent constructed as `make_agent(schedule, me=0)` and then placed in
seat 1 by the swap still believes it is seat 0. `confirm_late_sell_bias.py` handles this correctly
(rebuilds per match, per seat); `run_arena` cannot as written. **The shipped artifact is immune**
(`submission/main.py` reads `obs["player"]` rather than baking in a seat), so this is a harness gap,
not a shipped bug — but any future arena measurement using a seat-baked factory through `run_arena`
will silently corrupt half its games the same way C-25 did.

---

### OPEN-CLI — carried over from the CLI task list, 2026-08-09

The CLI task list was cleared on 2026-08-09 because it had grown to ~57 entries and was crowding the
terminal. These are the ones that were still open; nothing here has been closed by being moved.

- **1.32.6 test failures.** 9 left, 8 of them inside `schedule_agent.py`. Both simulators fail
  parity on 1.32.6 — see the version caveat at the top of this file.
- **Submission base undecided:** HEAD vs `schedule_agent_1455mh`. 1455mh is the only artifact that
  ever scored 1455 and is what every measurement this session was taken on.
- **Re-run every market A/B** once the sell and feed reds are green. They were all measured against
  a planner that has since changed.
- **Fable's fixes** must clear the d0-d16 breakdown, every field, before merge.
- **FEED_DAYS_FLOOR=2** — confirm on a fresh seed draw; it is the only figure clearing one SE.
- **SELL_ON_DRAIN_CADENCE** consolidates the sell shape but loses money — sweep the interval.
- **LATE_SELL_BIAS** — the +12.5pp is dead and there is no pool that can re-measure it.
- **Melon wide blocks** — small change, but `chains.py` is NOT in the shipped agent.
- **Shop-adaptive herd** shipped and measured; floors still open. **Geese deferred** by Alex on
  2026-08-09 until the cow/sheep split works.
- **CMA-ES on the JAX sim** over a direct market policy — parity green, never run.
- **Score the market changes on cash** via paired-margin mirror runs.

### OPEN-CLI-2 — what today's planner work leaves open

Measured on the `matching-the-tape` grid, seed 11, `90494364`, at `9ec3ebc`. d0 and d1 pass.

- **d4 `feed 6/7` / `care 6/7`** — one animal unserved. Real, ours.
- **d6 `place 0/1`, `plant 13/14`, `water 16/17`, `buy_product 7/9`** — real, ours.
- **d4 `tiles 50/25` is NOT a defect.** Seb buys that parcel on d4 in his own game; the tape column
  is degraded because he is $35 poorer at h22 when replayed against us. The money column from d4 on
  inherits the same contamination. See the skill `.claude/skills/matching-the-tape`.
- **The closing shed trip is uncharged**, so a hand can end the day in the far corner holding
  produce the row wants. Four fixes were tried and every one either measured null or cost more
  elsewhere than it bought — the working version needs a per-TOUR reserve, not a per-day one.
- **Never built:** don't dig weeds outside the geometry plan (`DIG_ONLY_IF_REPLANTING` gates on
  global `plants_left`, not per-tile); don't plant what cannot finish before season end
  (`_pointless_tiles` drops existing tiles, it does not refuse new ones).

## CLOSED — with the artifact that would go red

Do not reopen without new evidence that contradicts the named artifact.

| # | Item | Why it is closed | Artifact |
|---|---|---|---|
| C-1 | Melon "refuses to harvest" | `first_yield_day` is 10; a HARVEST below it is a no-op that still costs the turn. Our gate matches the env rule exactly. | `router.py:243`, `competition_brief.md` |
| C-2 | "We never plant day 6's six melons" | FALSE. We buy 6 and plant 6, funded at h8 by a same-turn `SELL WOOL 6`. The probe stopped printing once the order landed. | verified on this tree |
| C-3 | "Day 6's melons are never harvested by d11" | Correct but not a defect — day 6 + 10 = day 16. Seb's tape leaves its d6 batch equally unharvested. | verified on this tree |
| C-4 | "Melon is never sold, so land can't be funded" | 18 units sold at d11, funding the $4,000 parcel same-turn. The first two parcels predate any melon harvest. | verified on this tree |
| C-5 | Milk is under-sold | FALSE. We meet every sell row the schedule names; we over-**produce**. Moved to OPEN-3. | commit `cdac079`, `tests/test_stock_the_schedule_never_names.py` |
| C-6 | Pens on the depot ring block delivery | Clean negative, 7 tests including a positive control that LOCKED *does* block. | `tests/test_pens_do_not_block_the_depot_ring.py` |
| C-7 | PLACE is under-priced | Prize sweep 2x-10x changes nothing. It is a **budget** refusal, not a price. | commit `9a89ecd` |
| C-8 | `buy_seed +42` at d6 | Logging bug. `breakdown.py` counted offers; we re-offer every turn. Season total went to 0 once fills were counted. | commit `096d581` |
| C-9 | `sell` overstated 11x | Same root cause as C-8: 165 offers → 15 fills. Every number taken before 2026-08-08 used the wrong yardstick. | `experiment_log.md` §23 |
| C-10 | d10 `tiles -25` is a lost quadrant | FALSE. A one-day delay; `tiles` is a dawn snapshot at the window edge. | verified on this tree |
| C-11 | Feed bought in one block | `FEED_TURN_CAP = 6`; the herd bypassed the drip. Animals-in-pens went 17 → 18, not down. | commit `260db7a` |
| C-12 | The sheep never get placed | Fixed. d14 sheep -2 → 0, place -2 → 0, d0-d13 byte-identical. | commit `9a89ecd` |
| C-13 | `sh:wheat -2` at d4 | Does not exist on our tree. A mis-relayed figure from an agent branch. | verified d0-d7 exact |
| C-14 | The tape idles 0 turns on day 1 | Harness artifact — the tape was replayed into seat 1 with truncated hands. Real figures 144/131. | test removed |
| C-15 | GPU thermal throttling | Ruled on and closed. Do not re-rank it into any review. | — |
| C-16 | `weeds -174` means we beat the tape | FALSE, and the opposite. He finishes with 42 weeds standing, we with 8, because we DIG ours (`dig +35`). Clearing ground he was never going to replant costs us 35 unit-turns. | `data/logs/thirsty_strawberries.log` |
| C-17 | Feeding the animals starves the crops of water | FALSE. Thirst deaths are 41 STRAWBERRY on each side. The real difference is timing, now OPEN-4. First strawberry death is d11, preceding both the sheep-placement fix and `FEED_TURN_CAP`. | `scripts/thirsty_strawberries.py` |
| C-18 | `sh:wheat -139` from d8 is a defect | NOT a defect. HARVEST identical (2/2), net market delta identical (+10/+10). The -1 lives in the DROP / dusk-sweep / PICKUP mix and is the opposite way round from the assumption: **the tape** holds 3 units until the dusk auto-drop, we drop mid-day. Verified by an exact accounting identity holding every day for both sides. No fix, deliberately — forcing our order to match would be cloning the tape. | `experiment_log.md` §23 |
| C-19 | The d10 melon is a delivery defect | FALSE, after seven arms. Both sides wake with three tiles at 5/6; a one-shot cannot be harvested before it fills, so **neither side could harvest earlier**. The WATER ran seven hours late. | `experiment_log.md` §19, `tests/test_the_filling_water_carries_the_harvest.py` |
| C-20 | Dropping the harvest earlier is free money | FALSE. Four arms; the one that worked mechanically moved the first DROP h19 → h5 and still lost $8,292, because `DROP 116 → 137` bought `HARVEST 300 → 294`. A late harvest is already priced. | `experiment_log.md` §20 |
| C-21 | Pen geometry is a lever | FALSE, confirmed a third time on two fresh loss episodes (`91229682`, `91231728`, 2026-08-09, folded in from `docs/geometry_of_the_herd_2026-08-09.md`, file deleted). His exact tiles buy 2 cells of 150, and the Manhattan sum from (4,4) is 22 for both day-0 blocks. `DEPOT_RING_FIRST` ships off; its money sign reversed on a held-out draw. **Third confirmation:** our pens form a smear (21 tiles, row-3 x=0-9, ring-depth 3.25, mean shed-distance 2.86) against the opponent's compact block (14 tiles, ring-depth 1.90, mean shed-distance 1.21) — geometrically worse by every measure — yet **walk-per-work-op is BETTER for us in both episodes** (1.028 vs 1.118; 1.210 vs 1.445), and total realized walking (position-diffed, not raw move-op counts) is roughly level or lower for us despite the worse layout. The real divergence between winning and losing sides in both episodes is PASS (1.5-1.7x more for us) and WATER (1.6-1.9x more for the opponent) — production/idle time, not walking. A previously-cited "1.86 vs 2.93" ring-depth figure does **not reproduce** under either Manhattan (3.25/1.90) or Euclidean (2.69/1.50) recomputation — do not cite it going forward; use the figures above. Pen siting (`_refresh_pins` in `schedule_agent.py`) falls through an empty `PEN_SPOTS`, then shed-access tiles, then (only from day 11) nearest-depot search, defaulting before that to the same boustrophedon field-order sweep used for crops — mechanically why pens land late and far, since crops eat the near ground first. `PEN_NEAREST_DEPOT=True` was reverted historically on a cell-count-vs-tape proxy metric, never actually tested on bank or win rate — still technically open, but low-expected-value given walking isn't the binding cost. | `experiment_log.md` §21 |
| C-22 | `Node.service` under-counting is a bug to fix | It is the packing calibration that matches the tape. Correct prices, worse reproduction, every arm. Both constants ship at 0 and will not move. | `experiment_log.md` §22 |
| C-23 | `SHOP_ADAPT_CROPS` should swap crops toward the shop draw | Tried and reverted, three pairs. `WHEAT<->CARROT` / `TOMATO<->STRAWBERRY` shipped, measured 0.806 vs HEAD's 0.871 over 232 matched games — both swap toward crops the ladder plants 0.2%/0.0% of the time. `STRAWBERRY<->MELON` produces an identical 54/4 split on every board tested, because no shop carries melon so its drain is 29 everywhere — a pair with one board-independent member cannot adapt. Flag OFF as of 2026-08-11. **Measured before the SELLABLE fix (`c99a8a5`, 2026-08-13): our own agent could not sell CARROT at all, so `WHEAT<->CARROT`'s 0.806 was measured with carrot's revenue line disconnected. Not re-verified since; treat as UNVERIFIED, not re-affirmed.** | `kagg/search/schedule_agent_1455mh.py:2129` (`SHOP_ADAPT_CROPS = False`), full record in the flag's own docstring; `docs/experiment_log.md`, "the ladder is two scripts" section |
| C-24 | Fertilizer priced at its $100 base when deciding whether to fertilize | Fixed. The live market quote (`obs["market"]["prices"]["FERTILIZER"]`) is read every turn and threaded into `_router_acts` as `fertilizer_price` — nothing eats fertilizer, so its book only ratchets up ($50 by day 17, $20 by day 26 in 85/85 recorded games), and pricing at base meant refusing to fertilize a tile for a price nobody would pay. Shipped, unconditional (no flag to disable). | `kagg/search/schedule_agent_1455mh.py:2602-2612` |

---

## SELECTION RULE — how to judge any arm

Alex's, and it governs everything above.

- Judge a fix at the **day it targets**, field by field.
- Target day improves → good fix, take it.
- A **later** day regresses → a different problem with its own origin. Log it, do **not** revert.
- An **earlier** day regresses → a question, not an automatic veto. It may mean the earlier fix was
  wrong and this change exposed it.
- Season totals and single-seed dollar swings are **weak** signals. Judging by totals is the error
  that ran through the whole late-delivery effort.
- Hard constraint: do not regress d0-d5. Their differing-cell floor is currently `3,3,3,5,3,3`.
- Correctness floors are not metrics and are never traded away. The herd must not starve — measure
  **animals in pens per day**, because a previous change collapsed that 17 → 8 and was nearly
  shipped on cells and money alone.

If the behaviour is now correct and a number got worse, the old bug was probably **masking** a second
defect that the change exposed. Reverting hides it again.

---

## STATE at last update

```
branch          shaping-potential
baseline        seed 11, weeds 0.0, tape seb, days 0-29

HEAD, full 30 days, ours vs the tape
  bank          120,424 / 116,635      -> +3,789
  work            3,092 / 2,703
  move            2,782 / 4,025
  tiles             100 / 100          pens 19 / 19   cows 8 / 8   sheep 11 / 11
  animals lost in our own season: 0

fast suite      805 passed,  70 skipped, 7 xfailed, 0 failed
slow suite      240 passed,  25 skipped, 4 xfailed, 0 failed   (3m31s)
```

Baseline command, and the only metric that counts:

```
python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff --no-moves
```

Market rows (`sell`, `buy_product`, `buy_animal`, `buy_seed`) are **fills**; everything else,
including `hire` and `buy_land`, is still an **offer**. Fill rows are a lower bound — a turn dirtied
by DROP/PICKUP/PLACE contributes zero — so confirm a difference is real before explaining it.

**The uncontested number says we finish ahead. The contested head-to-head says we lose both seatings
on the valid seed.** Nothing here is a ladder result until that closes.
