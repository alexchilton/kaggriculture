is cl# Register — what is open, what is closed, and what keeps reopening

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
>
> **Second version caveat, added 2026-08-11.** The `STATE at last update` block below, and the
> baseline command it names, judge the agent against Seb's recorded tape. `docs/the_ladder_is_two_scripts.md`
> (2,744 ladder seats) found that tape was optimal under the OLD `townCenterSellInterval=12` economy —
> Seb's own median bank halved when the rebalance landed and he has since withdrawn from the ladder.
> Matching his tape op-for-op is still useful as a bug-finding harness (see the mechanism note on
> OPEN-1 through OPEN-8), but it is no longer the strategic target. The field plants 108-147 WHEAT
> tiles a season; our schedule plants 24. See `docs/the_ladder_is_two_scripts.md` for the rebase
> recommendation (Dmitry Belan or Efe Can Celiksoy) and `docs/what_the_town_will_actually_eat.md` for
> the current market-appetite picture.

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

### OPEN-5b — The same starvation now fires on the LADDER, and it is a cash failure

Owner: nobody. Evidence: `data/seed_scripts/ours_ladder_new/`, 2026-08-13.
`scratchpad/escapes.py` reproduces it from a downloaded replay in one pass.

OPEN-5 above is the seed-11 tape version of this. On the ladder it is worse and the trigger is
plainly **cash**, not reachability:

```
day  feeds  harv  wheat_shed  money  hands
  8      9     1           0    137      6
  9     10     4           0  1,377      7
 10      1     1           0      1     14     <-- first escape
 11      0     0           0     75     10
 12      0    13           0     22     10     <-- eight escape in one day
 13      0     0           7    167      8
```

`FEED` takes one WHEAT from the acting hand (`kaggriculture.py:496`); two consecutive unfed days and
the animal leaves and the pen stays (`:804`). The shed held **zero wheat from d8 to d12** while the
bank was at $1, $75, $22 — neither the stock nor the cash to buy it. Twelve of fourteen animals
walked: $5,200 of stock plus seventeen days of milk and wool.

**It is not a regression from the carrot release.** Verified with the carrot-sell discriminator:
`92566708` (new build) and `92535914` (old build, zero carrot sells) have the identical signature —
12 escapes, 2 surviving cows, 13 bare pens. The old-build game is also the worst margin in the whole
downloaded set, $46,313 against $154,391.

Nothing reserves the feed bill. `RESERVE_THE_SEED_BILL` does exactly this for seeds, and the feed
bill is the more expensive liability: a missed seed costs a planting, a missed feed costs the animal.

### OPEN-5c — A pen is built after the last animal is bought, and stands empty to the close

Owner: nobody. Present in **every** downloaded ladder game, both builds.

Fifteen `BUILD_PASTURE` ops against fourteen animals. The last `BUY_ANIMAL` lands on d18; pens are
still going up on d21 (2) and d24 (1). The d24 pen is bare from d24 to d29 while the bank holds
$53k-$95k and a sheep costs $500. In `92550780` the town was draining 1,074 wool and wool closed at
$252 — above base — so that empty pen was worth roughly $250 a unit, all season.

Distinct from OPEN-5b: no animal died here, one was simply never bought for a pen we paid to build.

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

Owner: nobody. `docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats.

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
`router_tape_repoint_2026-08-09.md` did once already for the 1.32.2 -> 1.32.6 move.

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

---

### OPEN-CLI — carried over from the CLI task list, 2026-08-09

The CLI task list was cleared on 2026-08-09 because it had grown to ~57 entries and was crowding the
terminal. These are the ones that were still open; nothing here has been closed by being moved.

- **1.32.6 test failures.** 9 left, 8 of them inside `schedule_agent.py`. Both simulators fail
  parity on 1.32.6 — see the version caveat at the top of this file.
- **Submission base undecided:** HEAD vs `schedule_agent`. 1455mh is the only artifact that
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

**Re-measured 2026-08-12 at HEAD against Victor's tape, `--days 17 --moves`.**
d0–d10 is now op-for-op exact on every non-exempt row *except* three cells, and two of the three are
the tape being wrong rather than us:

- **d1 `care 0/5` is NOT a defect — do not close it.** `reference/kaggriculture.py:816` banks the
  bonus only `if tile["cared_today"] and tile["fed_today"]`, and `:820` wipes `cared_today` either
  way. d1 is a day nobody feeds (`feed 0/0`, both sides), so Victor's five CAREs bank exactly zero.
  `router.py:852` gates `if not cell["cared_today"] and fed:` and is correct by the source.
  This is a **plan** difference, not an execution one: with `fed` False the CARE op is never emitted
  into the node set, so no amount of routing could produce it.
  It is also not a turn we reclaim — d1 idles 31/28, so the five turns are spare either way.
- **d5 `dig 0/1` and d7 `dig 0/1`** — the only other cells. `weeds` is `0/0` on all eleven days and
  the grid runs `weedSpawnChance 0.0`, so there is nothing to dig; Victor digs blind because an
  open-loop tape cannot see which tile the RNG weeded. On the ladder (`0.005`) that insurance is
  not free. **Do not chase these two cells on seed 11** — the grid cannot reach the condition that
  makes them right or wrong.
- **d4 `feed 6/7` / `care 6/7`** — CLOSED at HEAD, both now 5/5 through d4.
- **d6 `place 0/1`, `plant 13/14`, `water 16/17`, `buy_product 7/9`** — CLOSED at HEAD, all exact.

**d11 is where the season actually starts diverging, and it is a self-sustaining loop.**
It is an *execution* problem — movement — not a plan shortfall, and unlike d1 it is worth fixing.

```
                    d10     d11     d12     d13     d14     d15     d16
  water           43/43   40/41   43/46   28/27   41/45   35/35   50/59
  weeds             0/0     1/0     1/0     1/0     2/0     2/0     2/0
  strawb          31/31   35/36   35/36   35/36   35/36   35/36   35/36
  dig               0/0     0/1     0/0     1/0     0/0     0/0     0/0
  drop              3/5     5/0     6/1     7/0     5/0     4/2     4/1
  move            124/144 128/99  117/100 105/86  110/97  114/108 138/128
  idle             98/78   23/57   23/39   19/48   24/38   13/23   60/49
  mv/wk         1.06/1.23 1.24/1.02 1.04/0.88 1.25/1.18 1.13/1.04 1.10/1.09 1.13/0.92
```

The consequence chain is not in doubt: **+29 move turns → one water short → a weed → a tile gone.**
`consecutive_unwatered >= 2` turns the tile into a WEED (`kaggriculture.py:770`), `weedSpawnChance`
is 0.0 on this grid, so every weed here is our own missed water; it costs the tile permanently
(`strawb 35/36` to the end of the run) plus a turn to clear (`dig 1/0` at d13).
`idle 23/57` says we are near-saturated while the tape has 57 turns spare and still waters more.

Note `water 43/43` at d10 with a weed appearing at d11: the *count* matches and the *coverage* does
not. We water the wrong 43. Do not read the water row as a throughput number.

**What the +29 move turns are NOT.** Two causes were proposed and both are dead:

- **Mid-day ferrying — NO.** `scripts/day_ops.py --day 11` shows 3 of our 5 drops at **h23**, the
  closing walk home. Only two are mid-day, both by u6. The free drop is gated on
  `dist(pos,d) + dist(d,j.tile) == dist(pos,j.tile)` (`cover.py:708`) — zero detour by
  construction — so drops cannot buy movement, and `BANK_MID_TOUR_WHEN_THE_DAY_IS_UNFUNDED` is
  already `False`. The `drop 5/0` row reads like ferrying and is not.
- **Pen siting — NO, and it was already measured.** Our d11 pen set is genuinely more spread than
  the tape's (sum-to-depot 41 vs 29; worst pen 7 steps vs 3; `(9,1) (9,2) (0,3) (0,4)`), and that
  difference **does not propagate**. The `PEN_SPOTS` comment records a ceiling test that pinned
  Victor's own pen tiles and moved 150 cells to 148. An arm wiring the ungated catch-up siting in
  `build_nodes` to `_nearest_ground` produced a **byte-identical 17-day grid** — reverted same day,
  along with its test. Distance-to-depot of the pen SET is not the quantity that predicts movement.

- **Brink-water pricing — NO, and this one narrows the problem.** The tile that dies is `(1,2)`, a
  strawberry, and it was not unlucky: `d4:1 d6:1 d8:1 d10:1`, skipped every even day for a week,
  then skipped again on d11. That is the designed alternate-day cadence
  (`router.crop_ops`, `consecutive_unwatered >= 1`), which Seb runs too — so ~20 tiles sit one miss
  from death every day, board-wide, all season. Adding the weed's own cost (the lost square plus
  the DIG) to the brink WATER prize at both sites produced a **byte-identical 17-day grid** and
  `(1,2)` still died. Reverted with its test.
  **What that rules out is the whole priority story:** raising every brink water by the same amount
  changes no ordering among brink tiles, so if `(1,2)` were losing a triage it would now win one.
  It is not losing a triage — **it is never reached.** This is a REACHABILITY problem, not a
  pricing or ranking one, and any further prize/rank arm is answering the wrong question.
  (Do not confuse this with `router.py:656`, the *separate* recorded arm that promoted brink water
  into the MANDATORY pass and measured **-$2,804** over twelve seeds.)

- **The closing walk home — NO, and the reason is decisive.** `_end_of_day` calls
  `_drop_inventories_to_shed` (`kaggriculture.py:865`): every hand is emptied into the shed at the
  rollover, free, no walk, and the units are teleported home anyway. So a closing trip is only
  needed when today's market must see the goods while it is open, or when the shed would overflow
  (the sweep DISCARDS overflow). Victor exploits this — he does `drop 0` on d11.
  There is also a genuine internal mismatch: `cost` prices a reserve day with `wanted_only=True`
  (`cover.py:941`) while `_solve` materialised the route without it (`cover.py:1430`), and a
  synthetic WOOL tour against a WHEAT row was priced at 10 turns and built at 19.
  Threading the flag through produced a **byte-identical 17-day grid**. Reverted with its test.
  **Why it is null: on d10-d16 every tour's load is already `wanted`.** d11's row is
  `sells={'MILK': 6, 'FERTILIZER': 24}` and the three units that drop at h23 spent the day on
  `COLLECT_FERTILIZER`, so the market genuinely needs those drops and `wanted_only` suppresses
  nothing. The 9-turn gap exists only for loads the sell row ignores, which this schedule does not
  produce. Classic "check the harness sends what the agent would send" — the test built a case the
  game never reaches.

**Do not re-derive any of these four.** The open question is unchanged and unanswered: where do the
29 turns go? The one lead not yet tested is the planting frontier — the tape puts 7 of its 11 d11
plantings in the SW quadrant and waters 8 tiles there; we put 1 there and cram 10 into the two north
quadrants that already hold every pen. That is `field_order`'s fixed `_QUAD_ORDER`, which fills a
quadrant before opening the next, and it is a CROP siting question, not a pen one.
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
| C-23 | `SHOP_ADAPT_CROPS` should swap crops toward the shop draw | Tried and reverted, three pairs. `WHEAT<->CARROT` / `TOMATO<->STRAWBERRY` shipped, measured 0.806 vs HEAD's 0.871 over 232 matched games — both swap toward crops the ladder plants 0.2%/0.0% of the time. `STRAWBERRY<->MELON` produces an identical 54/4 split on every board tested, because no shop carries melon so its drain is 29 everywhere — a pair with one board-independent member cannot adapt. Flag OFF as of 2026-08-11. **AMENDED 2026-08-15 — the melon half was closed for the wrong reason; see C-23a.** | `kagg/search/schedule_agent.py:2129` (`SHOP_ADAPT_CROPS = False`), full record in the flag's own docstring; `docs/the_ladder_is_two_scripts.md` |
| C-23a | The strawberry/melon split cannot adapt | FALSE — it adapts, just not to shops. Across all 16 downloaded カワシギ games the split has exactly two states and the total is **always 54**: `STRAW 34 / MELON 20` (10 games) and `STRAW 42 / MELON 12` (6). Every game buys `MELON 12` on d0; the whole decision is one binary +8 executed `d5:+3 d6:+5`. It separates **16/16 on the opponent** — all six `researchstudio.site` games hold at 12, every game against Yusuke Hayashi / Filip Strzałka / Arda Ceylan tops up to 20 — and the signal is on the board he can see at d5: `MELON 9, WHEAT 7` against `MELON 5, STRAWBERRY 3, WHEAT 6`. The first shop unlocks at d2h23 in all sixteen and does **not** separate them (`PIZZA_SHOP` and `SMOOTHIE_SHOP` appear on both sides). Melon is the one crop no shop buys (`kaggriculture.py:91-98`), so its price is set purely by what the two farms dump into the town book; an opponent on nine melon tiles floods it, and the eight tiles are worth more in a crop somebody bids for. C-23's reasoning — "a pair with one board-independent member cannot adapt" — is correct about `SHOP_ADAPT_CROPS` and wrong as a verdict on the question: the signal was never the shop draw. Implemented 2026-08-15. | `kagg/search/schedule_agent.py` (`MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`), `tests/test_melon_yields_to_a_melon_heavy_opponent.py` |
| C-24 | Fertilizer priced at its $100 base when deciding whether to fertilize | Fixed. The live market quote (`obs["market"]["prices"]["FERTILIZER"]`) is read every turn and threaded into `_router_acts` as `fertilizer_price` — nothing eats fertilizer, so its book only ratchets up ($50 by day 17, $20 by day 26 in 85/85 recorded games), and pricing at base meant refusing to fertilize a tile for a price nobody would pay. Shipped, unconditional (no flag to disable). | `kagg/search/schedule_agent.py:2602-2612` |

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
