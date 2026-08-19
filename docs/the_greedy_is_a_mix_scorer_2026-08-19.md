# The greedy is a mix scorer, and that makes stage 1 searchable

2026-08-19, evening session.
Everything here is measured on each arm's own tape and seed, replaying d4-d11 then playing our planner.

## The finding

Turning off every solved route from d12 onward costs a flat ~4% on the three-quadrant arms and
**gains** money on one four-quadrant arm:

```
 arm        solved routes   greedy from d12    delta      mix change
 straw_q3      160,183         154,277        -5,906      wheat 120 -> 123, rest identical
 melon_q3      145,068         137,529        -7,539      wheat 135 -> 134, rest identical
 q4_melon       93,929          81,834       -12,095      wheat 133 -> 130, rest identical
 q4_straw       78,305          79,527        +1,222      wheat 128 -> 127, rest identical
```

Two things matter more than the deltas.

**The mix is preserved.** The herd is identical on every arm and the crop counts move by at most
three wheat tiles. So the greedy plays the same season, slightly worse -- it does not play a
different season.

**A season takes 8-25 seconds.** The solve it replaces takes about two hours per arm.

That combination makes the greedy a usable RANKER for a stage-1 mix. It is not a substitute for the
final number -- confirm any winner against re-solved routes before shipping -- but it removes the
coupling that made every stage-1 experiment cost a solve, which is what
`the_mix_and_the_routes_are_one_artifact_2026-08-19.md` recorded as the obstacle.

## The q4 tables are actively harmful

`q4_straw` banks **more** with no routes than with its solved table. A table you beat by deleting it
is doing damage, not merely drifting. Those two tables are the only ones never re-solved during the
day's mix work, and `q4_branch.install` runs them right through d29 (`q4_branch.py:294` resets
`cover.UNSOLVE_DAYS` to `()`), so the drift reaches the closing days where there is no slack.

`scripts/resolve_q4_full.sh` re-solves both, d12-d29. Until it has run, **no q4 experiment measures
the idea being tested -- it measures the table.**

## A comparison that measured nothing, and how to spot it

`scripts/q4_vs_q3.py` patched to unsolve both arms returned delta **exactly +$0 on all 12 seeds**,
with matching quadrant counts. Two different schedules cannot produce identical money to the dollar
twelve times. The harness is not applying the q4 plan.

The tell is the one this project keeps re-learning: an implausible number is a broken instrument, not
a finding. Here it is implausible in the other direction -- a PERFECT null across independent seeds
is as suspect as a $10,000 swing. **q4 remains untested.**

## Hires are NOT being lost -- corrected

Three mechanisms can in principle shrink the crew below the schedule row: affordability in
`_hires_this_turn`, the `_fit_slots` cut when a turn's orders exceed `ORDER_SLOTS = 10` (the env's
own `maxMarketOrdersPerTurn`), and `_do_hire` failing silently on a thin bank.

Measured per day on both q3 arms, none of them does:

```
 straw_q3   row 277   landed 277   short +0 on EVERY day   slotcut 32
 melon_q3   row 277   landed 277   short +0 on EVERY day   slotcut 33
```

`_fit_slots` does cut ~32 hires a season, and every one is re-issued on a later hour and lands. It is
a deferral, not a leak.

So the "we hire 11, tetsuya hires 6" gap is not a defect. **We hire 11 because kawa's schedule row
says 11, and we get all 11.** It is another stage-1 quantity inherited wholesale through a stage-2
artifact. The ladder is `mult * fib(n)`, so 11 costs $232 a day against 6 at $20 -- roughly $4,000
across d8-d27, buying hands that then `PASS` 124 times against his 16.

The hand count changes the unit set and therefore desyncs every route, so it can only be swept with
routes off. That is the correct instrument, not a workaround.

## Why the schedule's "harvest 10" never reaches the router

The row's counts are not carried anywhere. Pins hold only `PLANT` and `BUILD`
(`schedule_agent.py:1298`, `:1313`) -- **there is no harvest pin.** `_live_ops` (`:1282`) re-derives
the work from the live cell at every stop:

> "The route fixes *which tiles* a unit visits and in what order... What it does when it gets there
> is read off the cell, so a stop whose work another unit already did, or whose crop weeded
> overnight, simply returns nothing and the stop is dropped."

If three tiles are ripe you get three harvests, whatever the row says. Nothing checks the row's
number and nothing reports the shortfall.

So `harvest 0/10` on d3 is not a planner failure and no flag is blocking it -- the crop was not
ripe. The lever is WHEN a tile becomes harvestable, and it lives in `router.crop_ops`, not in the
schedule. WHEAT is `first_yield 2, max_day 4`: tetsuya harvests at d3 and turns the ground over, we
wait for `max_day` and take more units per tile while the tile stays occupied. That is what leaves us
full at d7 with zero empty squares, which is what stalls our pens at 9 while his reach 15.

**Untested.** It is the same trade as the strawberry cap -- less per tile, more throughput -- and it
is the tetsuya-tracking change most worth measuring next.

## Flags deleted, verified byte-identical

Ten flags and five orphaned constants, removed in a worktree and checked on all four arms:

```
 arm        money      baseline    herd            seed   plants
 straw_q3   160,183    160,183 ok  COW10 SHEEP4    $30    W120 M12 S37 T1 C5
 melon_q3   145,068    145,068 ok  COW10 SHEEP4    $10    W135 M20 S34 C8
 q4_melon    93,929     93,929 ok  COW6  SHEEP12   $180   W133 M20 S34 C7
 q4_straw    78,305     78,305 ok  COW6  SHEEP12   $130   W128 M12 S42 C7
```

`cover`: `AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP`, `SUPPLY_LIMITS_EVERY_DRAW`,
`SUPPLY_CHECKED_OPS`, `DELIVER_SURPLUS_NOT_THE_ROW`, `BANK_THE_ROWS_PRODUCE_WHILE_REAPING`.
`router`: `TOP_UP_SAFE_TILES`, `TOP_UP_FROM_DAY`, `BRINK_WATER_IS_WORTH_THE_TILE_FROM_DAY`
(INERT -- it only reached the board through `min(LATE_TRUNCATED_PLANT_DAY, 99)`), `CLOSED_TOUR`.
`schedule_agent`: `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE` with `EARLY_WOOL_SHEEP`,
`MILK_POOR_SHOP_COUNT`, `MILK_POOR_COW`, `MILK_POOR_SHEEP`, and `SEED_BEFORE_LIVESTOCK`.

**`SHOP_ADAPT_CROPS` was deliberately NOT removed.** Its dead branch, `_adapt_crops`, is 83 lines
that pick a crop from town-drain headroom, priced per tile and costed over re-sow cycles. That is
stage-1 logic, and our strawberry cap is a hand-rolled special case of it. It belongs in the sweep as
a config to measure, not in the bin.

## Correction, 2026-08-19: three of the four "holes" were the harness, not the planner

The first grid read `BUILD 0/15`, `PLACE 29/15` and `BUY_ANIMAL 10/15` and all three were counting
errors in `tets_grid3.py`. Corrected on tetsuya's own board (`94345389.json`, seed 959074148, seat 0):

- **`BUILD 0/15` -> 15/15, exact every day.** The env has no `BUILD` op. It has `BUILD_COOP` and
  `BUILD_PASTURE` (`reference/kaggriculture.py:493,499`), and `schedule_agent.py:1274` emits those
  names. The grid counted the string `"BUILD"` and matched nothing.
- **`PLACE 29/15` -> 15/15, exact.** `PLACE` is not animals-only. 14 of the 29 are
  `PLACE FERTILIZER`. Animal placements are COW 6, SHEEP 6, GOOSE 3 -- the row exactly.
- **`BUY_ANIMAL 10/15` -> all 15 heads bought.** The row asks 15 HEADS; `schedule_agent.py:4901`
  emits one order per SPECIES (`["BUY_ANIMAL", a, want]`), so 15 heads leave in 10 orders. Orders
  were being counted against heads. Same shape as `feedback_offers_are_not_fills`, one field over.

A whole session's worth of "missing planner methods" was three unit mismatches in the instrument.
Before implementing against a grid cell, check the op NAME the env actually uses and the UNIT the
column counts.

## What actually tracks, and what does not

Following tetsuya's schedule, on his own board and seed:

    hands      exact every day except d12 (9/11)
    plants     212/212 season
    crop mix   WHEAT 164/164  STRAWBERRY 32/32  MELON 8/8  CARROT 8/8
    builds     15/15
    places     15/15 animals
    animals    15/15 heads
    FEED       314/353
    CARE       316/353
    herd       14 standing, COW 5 SHEEP 6 GOOSE 3

The herd climbs monotonically 5 -> 14 by d12 and never drops -- nothing dies. But 15 placements
leave 14 animals standing, so one COW placement lands on ground that already holds one. One cow's
FEED and CARE across the back of the season is the shape of the 39-op shortfall. That is the next
thing to fix, and it is one defect, not two.

## TOMATO is not in ANY schedule, and the adapt rule did not fire

Alex's challenge, 2026-08-19: "tetsuya plants no tomato at all - that is against your original
evidence, that's why we added tomato to kawa because on some seeds he does."

Correct, and broader than one player. No schedule file in the repo carries a TOMATO row:

    tetsuya           WHEAT 164  STRAWBERRY 32  MELON  8  CARROT 8
    tetsuya_93866112  WHEAT 135  STRAWBERRY 37  MELON 15
    kawashigi         WHEAT 136  STRAWBERRY 34  MELON 20  CARROT 8
    kawashigi_b3      WHEAT 124  STRAWBERRY 42  MELON 12  CARROT 5
    victor            WHEAT 139  STRAWBERRY 36  MELON 19  CARROT 6

Tomato reaches the board ONLY through `WHEAT_TILES_TO_TOMATO = 1` (`schedule_agent.py:3461`), which
converts wheat tiles at run time on the shop draw. Tetsuya's own two games disagree with each other
-- carrot 8 on one draw, none on the other -- which is the seed-dependence the rule exists for.

So "our crop mix matches his to the unit" is a WEAKER statement than it looks: WHEAT came out at
164, identical to the row, with TOMATO 0. The conversion never ran on this seed. A column that
matches because a rule did not fire is not evidence the rule is right. `WHEAT_TILES_TO_TOMATO`
is armed and unexercised here, and needs a draw that unlocks tomato before anything can be said
about it.

## 2026-08-19, later: the one-schedule approach is wrong, measured on 78 games

Alex: "if you only read 1 schedule how the hell can you make a bloody adaptable dynamic rule" and
"you will fit the 1 schedule and it will be broken everywhere."

Correct. The tetsuya schedule was extracted from ONE replay (94345389) and followed all night. We
hold **78 tetsuya replays**. Against them, the game we fitted is an outlier on nearly every axis:

    field         94345389      across 78 games
    WHEAT              164      99-187   mean 135
    STRAWBERRY          32      24-50    mean  37
    MELON                8      8-19     mean  13    <- the MINIMUM he ever plants
    CARROT               8      0-65     present in  9/78 games
    TOMATO               0      0-22     present in  4/78 games

### The invariant, and the response

    TOTALS                       min  max   mean    sd    cv
      herd total                  15   18   15.2   0.5  0.03
      straw + melon               32   65   49.8   5.8  0.12
      tiles planted              160  246  187.7  17.8  0.09
    SPLITS
      COW                          4   12    7.6   2.8  0.37
      SHEEP                        3   11    6.4   2.7  0.43
      GOOSE                        0    5    1.2   1.4  1.16
      CARROT                       0   65    2.2   8.8  4.07
      TOMATO                       0   22    0.7   3.3  4.64

**His herd total is 15, cv 0.03.** The cow share of the pasture moves 0.29 -> 0.80 and CLUSTERS --
18 games at 0.80, 13 at 0.50, 16 near 0.30. Clusters are the signature of a shop draw, not noise.

So the rule is: pin the total, adapt the split.

  - pin: herd total ~15, straw+melon ~50
  - adapt on the draw: cow/sheep split, goose count, carrot, tomato
  - scale with land: total tiles planted

### The change this reverses

`SHOP_ADAPT_HERD` -- 47 lines re-splitting cow/sheep on the shop draw -- was DELETED earlier the
same day so that the geese would come out 3/3 on game 94345389. The 78-game spread says the split
is exactly the quantity that must stay adaptive, and that a 3/3 goose match on one replay is
fitting to a draw that 35 of his 78 games do not have at all (goose is absent in 35).

That deletion should come back. Matching one tape's herd exactly is the failure mode, not the goal.

## The pivot lands: `_herd_split` now follows tetsuya

Two test files were added, both scoring at HIS DECISIONS rather than at the final board:

  - `tests/test_the_herd_split_answers_tetsuyas_shop_draws.py`
  - `tests/test_the_crop_mix_answers_tetsuyas_shop_draws.py`

**Scoring at the decision, not the census, is the whole method.** Reading the end-of-season herd and
asking the rule about it hands the rule a day-29 shop list nobody had on day 4. Each animal he put
in a pen is one question, asked with the day and the shops unlocked at that turn. That change alone
moved the measured baseline from 11.5% to 55.8% without touching a line of the rule -- the old number
was measuring the instrument.

### What changed in `kagg/search/schedule_agent.py`

    1  the opening       floors to SHEEP 3 / COW 2, applied sheep-first; an EMPTY `unlocked_shops`
                         returns before the wool branch
    2  the goose         `_herd_split` carries a GOOSE bucket from the schedule row
    3  the gradient      COW = CAP - (LIMIT - draw) for draws #1-#3, replacing the two-valued step
    4  the milk line     REVERTED, -16 points

Placement match against his 78 games: **55.8% -> 65.6%** (779/1187).

**(1) is the biggest single defect and it was a category error.** On day 0 `unlocked_shops` is EMPTY,
and the wool branch read that as "this board has no yarn store" and committed ten cows before a
single shop had landed. An undrawn deck is not a known deck. His first five animals are
`SHEEP SHEEP SHEEP COW COW` in 78 of 78 games -- unanimous, no exceptions -- and ours were cows.

**(4) failed for a reason worth keeping.** The milk covariate is real: over his 50 late/no-yarn games
the cow count is linear in the number of milk-draining shops, 6.0 / 7.5 / 8.6 / 9.8 / 10.9 / 12.0 for
one through six of them. But it is fitted on the FINAL board and was applied to the draw SO FAR. At
day 3 two shops have landed, the milk count is near zero, and the line asks for 6 cows on a board
that ends at 12. It needs the count he could have EXPECTED, not the count visible yet. Same
census-vs-decision error as above, one level down, made an hour after correcting it.

### カワシギ's tests: broken on purpose, xfail(strict), not deleted

One function cannot be two players. Four tests went red and Alex approved the breakage.

    test_the_herd_follows_the_wool_shop.py   draws #1 and #2 params -> xfail(strict)
    test_the_herd_split_answers_the_recorded_shop_draw.py
                                             ..._the_leaders_cow_count... -> xfail(strict)

`strict` on purpose: if the rule is ever pointed back at カワシギ these turn green and fail the suite,
which is the signal that the pivot has been undone.

`test_the_total_is_never_exceeded` was NOT xfailed. Its ceiling is a real invariant and still holds
on every input; only its `>= 12` FLOOR was wrong for the empty draw, so the empty case now asserts
the opening and every other assertion stays live.

### Still open

  - 65.6% -> 80%. The residual is largely ORDER, not mix: he exhausts all three sheep before the
    first cow, and `_herd_split` returns counts while ordering lives in the caller's pen siting.
  - the milk covariate, re-fitted on EXPECTED final shops rather than visible ones.
  - the crop side, untouched: `WHEAT_TILES_TO_TOMATO = 1` fires on 78/78 boards where he plants
    tomato in 4/78, and `SHOP_ADAPT_CROPS = False` leaves nothing connecting the draw to the crop
    choice while his carrot ranges 0-65 tiles.

## Where the herd rule actually fails, and why the milk line could not fix it

### Scoring per DAY, order-free inside it

`_herd_split` returns COUNTS. Which pen a hand reaches first comes from the schedule row via
`_outstanding_places`, so charging the split for his sheep-first opening scores it for something it
does not control. Order-free per-day scoring: **65.6% -> 77.9%**. Twelve points of the apparent gap
was the instrument again.

### The failure is entirely in the back half

     day   placed   right    rate    shops drawn by then
       0      390     344   88.2%    ~0
       3       78      70   89.7%    ~1
       4      148     139   93.9%    ~1
       7      124     110   88.7%    ~2
       9       98      66   67.3%    ~3
      10       99      63   63.6%    ~3
      11      143      86   60.1%    ~3
      12       67      32   47.8%    ~4
      13       29      12   41.4%    ~4
     season  925/1187 = 77.9%

d0-d7 is ~90%. It collapses from d9. The opening and the first two draws are solved; every remaining
error is late, which is Alex's read exactly -- "d0-d3 we know and then it gets more than 1 decision
d6 d9 d12".

### The milk line: measured twice, negative twice, and the second run explains the first

    visible milk count, fitted on the final board      65.6% -> 46.4%
    expected final milk, undrawn at 3/8 each           65.6% -> 63.0%
    flat WOOL_SHOP_NO_YARN_COW                         65.6%

The expectation correction recovered thirteen of sixteen lost points, so reading a partial draw as
final WAS a real defect -- but not the only one. **A linear fit to a bimodal response lands between
both modes and matches neither.** His late/no-yarn boards cluster at COW 6 and COW 12; the per-milk
means of 6.0 ... 12.0 are averages OVER that split, not a trend within it. At three milk shops nine
boards go low and eight go high, so the fitted 8.6 is a value he essentially never plays. Both
reverted, both recorded in place.

A rule that beats the flat number must CLASSIFY, not interpolate.

### The classifier is probably the OPPONENT -- Alex's call, and it survives a control

     yarn store in draws 1-3       n     his sheep share
       opponent sheep <= 4        59          0.97
       opponent sheep >= 5        86          0.99      no opponent effect
     yarn store late or absent     n     his sheep share
       opponent sheep <= 4       198          0.41
       opponent sheep >= 5        15          0.07      strong, crowding direction

Uncontrolled, the opponent's sheep count predicts his choice in the WRONG direction -- both players
go sheep together, which is the signature of a common cause, and the common cause is the shared shop
draw. Controlled for the draw the picture inverts and sharpens: where the draw is informative the
opponent is irrelevant (0.97 vs 0.99); where the draw says nothing the opponent decides, and a
sheep-heavy opponent pushes him to cows.

That is a candidate for the bimodality the milk line could not reach. **n=15 in the deciding cell.**
One thin cell carrying the claim: a lead, not a result. It needs more late-yarn games before any
code is written against it.

## The herd clears the bar: 81.9%

Two more fixes after the first commit (`2b28fe1`):

  - **the goose is held to `GOOSE_FROM_DAY = 6`.** Offered at day 0 the bucket was spent on the
    opening and displaced a sheep -- a miss twice over, the goose early and the sheep missing. He
    places his first bird on d6 and nothing at all on d0-d5: d6:3 d7:8 d8:3 d9:9 d10:8 d11:28 d12:23
    d13:13. **Day 0 went from 88.2% to 100.0%, 390/390.**
  - **the tomato tile is gated on the draw.** See below.

     day   placed   right    rate
       0      390     390   100.0%
       4      148     140    94.6%
       7      124     110    88.7%
       9       98      66    67.3%
      11      143      86    60.1%
      13       29      12    41.4%
     season 972/1187 = 81.9%

The whole remaining error is d9 onward, and the opponent lead above is the only candidate that
reaches it.

## The plant side

### Tomato is a shop response and is now gated on one

    tomato-draining shops    0    1    2    3    4    5
    games                   10   24   25    9    7    3
    games with tomato        0    0    1    0    1    2

Not one tile across all 34 games with fewer than two draining shops. `TOMATO_DRAIN_SHOPS_NEEDED = 2`
is added to the existing `melon_armed and not q4_armed` conditions. A GATE, not a size -- the tile
count is untouched, so the only change is which boards get it.

### Three false premises in one session, all the same mistake

This is the one worth carrying forward. Three assertions were written against a NAME instead of the
BRANCH that reads it, and all three were wrong:

  1. "`WHEAT_TILES_TO_TOMATO` fires on every board, unconditionally" -- taken from its own docstring.
     The use site has gated it on `melon_armed and not q4_armed` all along.
  2. "`SHOP_ADAPT_CROPS = False`, so nothing connects the draw to the crop choice" --
     `STRAWBERRY_TILES_BY_DRAIN` caps strawberry on the draw and runs OUTSIDE that flag.
  3. "`_herd_through_day` re-labels every head, so a goose cannot survive" -- it iterates COW and
     SHEEP only and leaves other species alone.

And a fourth was caught before it shipped: the tomato gate was first written against the local
`unlocked`, which is `unlocked_quadrants`. Quadrant names never match shop names, so it would have
scored 0 on every board and switched the tile permanently off while reading like a working gate --
a silent null. `CLAUDE.md` already says "print the name the code actually reads before any A/B";
the docstring is not the name.

### Carrot has no predictor and no gate was invented for it

Carrot's nine games sit at drain counts 1,1,1,2,2,2,3,3,3 -- evenly spread -- and the five games
with FOUR draining shops have none. Non-monotone, so drain count is the wrong variable. Its
first-planted day splits into two clusters, d6-d10 and d25-d27, so the late one is end-of-season
opportunism on leftover ground rather than a crop plan at all.

`test_carrot_is_the_crop_with_no_predictor_yet` pins the non-monotonicity so nobody fits a line to
it -- which is exactly what cost sixteen points on the herd side -- and says to replace itself when
a predictor is found.
