is # Register — what is open, what is closed, and what keeps reopening

Last updated 2026-08-08, on `shaping-potential`.

> **Version caveat, added 2026-08-09.** The ladder moved to `kaggle-environments` 1.32.6 on
> 2026-08-07/08. The `STATE at last update` block below, and most dollar figures elsewhere in this
> file, were measured on 1.32.2 or against a fixture that did not yet reflect the town rebalance
> (`competition_brief.md`, "version skew"). Both simulators now **fail parity on 1.32.6** — 8
> failures, not the "300/300 exact" figure this file and `architecture.md` used to treat as current.
> The *mechanisms* below (routing, feed, geometry, discard timing) are still believed correct; the
> *dollar sizes* are not to be trusted without re-measuring on 1.32.6. See
> `docs/the_market_2026-08-09.md` for the current, 1.32.6-dated market picture and
> `docs/the_top_five_clusters_2026-08-09.md` for the current ladder gap (we score 1,123.5 against a
> field whose floor is ~3,117).

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
animal products (`the_field.md`). So `buy_product -164` may not be a bug at all — it may be the one
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
described here; see `docs/the_market_2026-08-09.md` §4-5, which found milk and wool still
under-priced on real ladder losses even with both flags on.

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
| C-21 | Pen geometry is a lever | FALSE. His exact tiles buy 2 cells of 150, and the Manhattan sum from (4,4) is 22 for both day-0 blocks. `DEPOT_RING_FIRST` ships off; its money sign reversed on a held-out draw. | `experiment_log.md` §21 |
| C-22 | `Node.service` under-counting is a bug to fix | It is the packing calibration that matches the tape. Correct prices, worse reproduction, every arm. Both constants ship at 0 and will not move. | `experiment_log.md` §22 |

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
