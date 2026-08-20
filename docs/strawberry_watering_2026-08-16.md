# The strawberry watering defect, 2026-08-16

## Summary

The defect is **not** a priority-ordering problem and it is not a turn shortage.

`cover.cover` returns early on any day in `PRECOMPUTED_ROUTES`, and `_apply_precomputed` seats the
solved stops **without pricing them against the unit's turn budget**.
The file already says so, at `TRIM_HOME_DAYS`: "the reserve pricing cannot reach a precomputed day
(`_apply_precomputed` seats stops without pricing them)".
A day is 24 turns whether or not anyone counted them, so the tail of an over-long tour is simply
never walked, and nothing reports it — `PRECOMPUTED_MISSES` records a stop the board could not
FILL, and has no entry for a stop that was seated and then never reached.

On the gate's own season, ten tours are planned past the day and eleven WATER stops sit past the
cut. The tiles those waters name are the tiles that weed that same night.

The fix prices the seated tour and releases the surplus into the leftover pool, where the existing
at-risk-first insertion can re-seat it on a hand that still has slack.

Twelve seeds: **money +$1,165 mean (10 up / 2 down), tiles weeded 183 -> 120, strawberry deaths
117 -> 80, harvest 4,391 -> 4,548.**
The acceptance gates move **356 -> 359 failed**, and the reason is set out under "The gate went the
wrong way" below — seed 11 is one of the two seeds where the change loses money.

## What was tested, and where the logs are

All runs are tape `kawashigi` (`data/seed_scripts/kawashigi/92498144.json`), `weedSpawnChance`
0.005, 30 days, agent built exactly as `tests/test_each_day_matches_the_tape.py` builds it —
`SA.make_agent(sched, 0)`, `B.run(ours, opp, SEED, WEEDS, stop_day=31)`, no `router=`, no
`economy=`, no `shops=`.

Worktree: `.claude/worktrees/agent-ac5605e21153f7305`, branched from `kawashigi-plan` at `0af2764`.

    data/logs/gate_baseline.log                    both gates, before any change
    data/logs/gate_final.log                       both gates, after the change
    data/logs/thirst_kawashigi_s11_baseline.log    every tile that weeded, seed 11, before
    data/logs/thirst_kawashigi_s11_fixed.log       the same, after
    data/logs/brink_stage_kawashigi_s11.log        WHICH stage lost each dying tile's water
    data/logs/over_budget_kawashigi_s11.log        tours planned past the turn budget
    data/logs/who_overruns_s11.log                 solved stops vs leftover insertion
    data/logs/does_slip_fire_s11.log               coverage of the reverted refinement
    data/logs/ab_season_kawashigi_s11.log          season A/B, seed 11
    data/logs/ab_multiseed.log                     season A/B, 12 seeds

Note on the worktree: `data/` is gitignored, so a fresh worktree has no tapes and every gate test
ERRORs on a missing `schedule.json`. `data/seed_scripts` is symlinked to the main checkout's copy,
read-only. Nothing was written to the main checkout.

## How the defect was localised

Every tile that weeds was attributed to the stage that lost its water
(`brink_stage_kawashigi_s11.log`). All fifteen deaths sit at `consecutive_unwatered == 1` at dawn,
none was dropped by `_pointless_tiles`, and every one was OFFERED a water:

    VERDICT TALLY: {'seated, not executed': 9, 'uncovered': 6}

So the water job exists and the planner accepts it. Nine times it is seated in a route and the
WATER never happens; six times `_insert_leftovers` cannot fit it at all.

Both are the same root cause one step apart. `_insert_leftovers` prices each insertion against
`budget[u]`, so when the base tour is already over budget no insertion is possible and the job
falls out as "uncovered"; when the tour is over budget with the water already in it, the water is
"seated, not executed". `who_overruns_s11.log` separates the two candidates and the solved stops
alone are over budget in every case, before the insertion adds anything — the insertion is
innocent.

    day  unit  budget  cost  over  WATER tiles past the cut
     16     6      23    28     5  (1,4) (0,4)
     19    12      23    25     2  (0,5)
     22     0      24    25     1  (1,3)
     23     3      23    33    10  (9,8)
     24     0      24    26     2  (3,1)
     25     9      23    29     6  (6,0) (6,1)
     26     4      23    26     3  (6,2)
     27    10      23    25     2  (8,7)
     28     3      23    25     2  (9,6)

Cross-referenced against the deaths: (1,4) and (0,4) weed at the end of d16, (0,5) at the end of
d19, (6,2) at the end of d26, (8,7) at the end of d27.

STRAWBERRY is `ongoing: True`, so it must be watered every second day for the whole season. A tile
at `consecutive_unwatered == 1` at dawn has exactly one water between it and a WEED, and that water
was being planned into turns the hand did not have.

## The failing test, written first

`tests/test_a_hand_is_never_given_more_tour_than_its_day.py` — one theory, one test.
It wraps `cover.plan` over the gate's own season and asserts no unit is handed a tour costing more
turns than it has.

Before the fix, RED with ten rows:

    d16 u6:  budget 23, planned 28 (5 turns over)
    d19 u12: budget 23, planned 25 (2 turns over)
    d22 u0:  budget 24, planned 25 (1 turns over)
    d23 u3:  budget 23, planned 33 (10 turns over)
    d24 u0:  budget 24, planned 26 (2 turns over)
    d25 u9:  budget 23, planned 29 (6 turns over)
    d26 u4:  budget 23, planned 26 (3 turns over)
    d27 u4:  budget 23, planned 25 (2 turns over)
    d27 u10: budget 23, planned 25 (2 turns over)
    d28 u3:  budget 23, planned 25 (2 turns over)

After the fix, GREEN. The fix was then backed out again and the test returned to RED with the same
ten rows, so the test genuinely covers the change rather than merely not being broken by it.

## What changed, and where

`kagg/search/cover.py`, one new function and one call site. **No flag, no constant, no `else`
branch.** +61 lines, nothing deleted, nothing gated.

`_apply_precomputed` now ends:

    left += _trim_to_the_day(routes, units, budget, depots, carry, wanted, deliver, rush, due)

`_trim_to_the_day` is the named rule: **a hand is never given more tour than its day can walk.**
It prices each seated sequence with the same `materialise`/`turns` pair `plan` uses, pops stops off
the end until the tour fits, and returns what it released. The released stops join `left`, so they
go through `_insert_leftovers`, which already sorts at-risk first — a water on a tile that dies
tonight gets re-seated on whichever hand still has slack instead of being abandoned on the hand
that ran out.

Every other seating path in the file already obeys this rule: `slot`/`claim` price a job against
`budget[u]` before taking it, and `_insert_leftovers` prices each insertion the same way.
`_apply_precomputed` was the one exception.

## Per-day rows that changed, ours vs tape

The row this work targets is `weed`. It moves toward the tape on every day it appears:

    day   weed ours/tape BEFORE     weed ours/tape AFTER
    d16          3 / 2                     1 / 2
    d17          3 / 1                     0 / 1      <- now EXACT
    d19          5 / 1                     2 / 1
    d20          5 / 1                     2 / 1
    d21          6 / 2                     4 / 2
    d22         10 / 1                     6 / 1
    d23         11 / 3                     6 / 3
    d26         16 / 1                     8 / 1
    d27         12 / 0                     8 / 0

Season, seed 11: tiles weeded 15 -> 9, of which STRAWBERRY 11 -> 8; weeds standing on the board at
d29 15 -> 11; DIG turns 31 -> 27; HARVEST 366 -> 385; WATER 972 -> 1011.

## Both gates, before and after

Baseline re-measured in this worktree — it matches the number in the task, not the 311/590 recorded
in `docs/work_to_be_done_2026-08-16.md`, which is stale:

    BEFORE   356 failed, 545 passed, 115 xfailed, 35 xpassed
    AFTER    359 failed, 542 passed, 115 xfailed, 35 xpassed

### The gate went the wrong way, and this is the honest reading

Five cells went green and eight went red. Net -3.

    FIXED    PLANT-26  WATER-22  crop_CARROT-26  crop_STRAWBERRY-22  weed-17

    BROKEN   PLACE-19            ours 2/2  -> 0/2      a real loss: two placements dropped
             WATER-16            ours 37/37 -> 39/37
             WATER-20            ours 54/54 -> 56/54
             WATER-27            ours 36/36 -> 42/36
             HARVEST-21          ours 36/36 -> 39/36
             crop_STRAWBERRY-19  ours 30/30 -> 33/30
             crop_STRAWBERRY-20  ours 30/30 -> 33/30
             crop_STRAWBERRY-23  ours 22/22 -> 23/22

Seven of the eight breakages are the same event: we now keep more strawberry alive than the tape
does, so we water more, harvest more, and hold more live tiles. Those cells were exact and are now
over. Only `PLACE-19` is a straightforward loss.

The gate counts cells, not distance, so it cannot reward closing a large gap and can only punish
opening a small one. Going from `weed 16/1` to `weed 8/1` does not flip a cell; going from
`crop_STRAWBERRY 30/30` to `33/30` does. Both statements are true and they point in opposite
directions.

**This is not offered as an excuse for the -3.** It is why the season measurement below was run
before drawing any conclusion, and why the conclusion does not rest on seed 11.

## Twelve seeds

Tape `kawashigi`, `weedSpawnChance` 0.005, both arms on each seed. The OFF arm is a runtime
monkeypatch inside the scratch driver; nothing in the shipped code is gated.

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

    money  delta     +1,165 mean, +529 median, 10 up / 2 down
    weeds  OFF/ON       183 / 120      (-34%)
    strawb OFF/ON       117 / 80       (-32%)
    harv   OFF/ON     4,391 / 4,548

Seed 11, the gate's seed, is one of the two seeds where the change loses money. Seed variance on
this project is ~15%, so a $1,165 mean on twelve seeds is not a large effect; the 10/2 split and
the monotone weed/strawberry/harvest columns are what the claim rests on, not the dollar figure.

## Ruled out, with the measurement that ruled it out

- **The pass-order fix (`AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP`) is not the defect.** It
  reorders the greedy passes, and the greedy does not run on any day where a strawberry died —
  `PRECOMPUTED_ROUTES` covers d9-d29 under the gate's exact configuration and every one of the
  fifteen deaths falls on d16 or later (`thirst_kawashigi_s11_baseline.log`). The constant was not
  touched, not flipped, and not read.

- **"The d12 water job is never offered" is refuted.** Every one of the fifteen dying tiles was
  offered a water on the day it died (`brink_stage_kawashigi_s11.log`, `offered = True` on all
  fifteen rows). `_pointless_tiles` dropped none of them. This confirms the existing note in the
  task brief rather than contradicting it.

- **`_pointless_tiles` / `LATE_SEASON_TRIAGE` is not implicated.** `pointless = False` on all
  fifteen deaths. Reading the code agrees: the ongoing branch only triages a tile that cannot reach
  its FIRST yield, which a mid-season strawberry always can.

- **The leftover insertion is not the cause of the overrun.** `who_overruns_s11.log` prices the
  seated sequence before and after `_insert_leftovers`; the solved stops alone already exceed the
  budget on every affected day.

- **REVERTED, measured null: trim the last SLIPPABLE stop rather than the last one.** The clause is
  live, not dead — on seed 11 it fires on 2 of the 13 over-budget tours and picks a different stop
  (`does_slip_fire_s11.log`: 2 "slippable stop is NOT the tail", 8 "IS the tail", 3 "no slippable
  stop"). It is still a null: the gates return a byte-identical failing set and the season weeds
  the same nine tiles on the same days. The cause is that the released stop reaches
  `_insert_leftovers` either way and that already sorts at-risk first, so the ordering was being
  applied twice. The code was deleted and the reason recorded in the `_trim_to_the_day` docstring.

## What is still open

- **The remaining nine deaths.** Six are real (d21, d22 x2, d24 x2, plus one WHEAT); three fall at
  the end of d29, where the season is already over and they cost nothing.
- **`PLACE-19` regressed 2/2 -> 0/2.** A dropped PLACE is neither `at_risk` nor `required`
  (`REQUIRED_OPS = ("FEED",)`), so it sorts last in `_insert_leftovers` and loses. Whether a
  placement should outrank an ordinary stop is a separate question from this one and was not
  changed here.
- **Why the solved tours are over budget at all.** They were solved offline against a board this
  season does not quite reach; the stop keys still match, so the extra turns come from walking or
  from depot stops `materialise` adds, not from extra ops. Re-solving the affected days would
  remove the overrun at source and make `_trim_to_the_day` a guard rather than a repair. Not
  attempted here.
- **Only one tape.** Everything above is `kawashigi` (A3: melon, three quadrants). The strawberry
  boards B3/B4 were not run, because adding them to `TAPES` pairs a strawberry replay with the
  melon-board `schedule.json` that drives our own agent, which measures something else.

---

# Crop mix: carrot, and the strawberry allocation

## 2026-08-12 — The carrot swap, measured on Victor's tape

Folded in from docs/carrot_swap_2026-08-12.md.

Original title: "The carrot swap, measured on Victor's tape — CLOSED, and it is not the town."

**RETRACTED same day. Every early arm in this file is invalid.**
The schedule's `sells` rows never mention CARROT, so nothing in the first pass ever SOLD any carrot
it grew.
Measured directly: 2 carrot tiles put 6 units (seed 13) and 3 units (seed 14) into the shed and
**0 units out of it** for the whole season.
Every arm therefore paid the $20 seed, spent the tile and the turns, and banked nothing — a loss by
construction, on any crop, whatever the market says.
That applies to ALL of the early measurements: the tape arms, the 384-game `CARROT_SWAP` pool sweep,
the `CARROT_TILES` sweep, and the 2-for-2 substitution.
None of them measured carrot's economics.

A second, independent defect compounds it: carrot is `max_yield_day 3` against wheat's `4`, and the
schedule's harvest cadence is built for wheat, so the tile is visited a day late and does not deliver
its 4 units either (6 and 3 units from 2 tiles, against 8 expected).

**Carrot is UNTESTED, not disproven** by the retracted arms.
A real test needs CARROT in the sells row and a harvest on carrot's own clock.
The market analysis (the pocket ledger, the price curves) is still correct as arithmetic and is
still the right way to size the prize — it just did not decide any of the retracted arms.

### The frame was also wrong — 2026-08-13, from the leader's own tapes

Every retracted arm is a **swap**: `PLANT WHEAT -> PLANT CARROT` from day D, replacing a crop that
pays with one that pays less.
At base prices wheat is $140/tile against carrot's $120, so that question has a correct answer and
the answer is no.
It is not the question the leader is answering.

カワシギ (#1, 15-1 over 16 games, `docs/kawashigi_one_board_2026-08-13.md`) buys **8 carrot seeds on
d3/d6 in all 16 games** and then plants **no carrot at all until d21**.
From d21 to d26 he plants carrot in every game, 1-8 tiles, on ground that is otherwise finished:

    2407  d22:4 d25:4        0434  d21:3 d22:1 d25:1 d26:2
    8461  d21:2 d22:1 d24:3 d25:1    8144  d21:2 d22:2 d24:2 d25:2
    2932  d21:2 d22:2 d24:2 d25:1 d26:1   6371  d21:1 d22:1 d24:1 d25:1 d26:1

Carrot is `first_yield_day 2, max_yield_day 3` against wheat's `2, 4`.
A wheat sown on d26 reaches its window on d30, which does not exist; a carrot sown on d26 finishes.
**Carrot is not a competitor to wheat, it is the crop for the window in which wheat is unplantable**
— additive on dead tiles, never a substitution.

**The frame was forced by the fixture, which is the part that generalises.**
These arms were run by mutating a BAKED tape.
Its sell rows, its harvest cadence and its seed purchases are all fixed to wheat's clock, so the only
carrot experiment such a fixture can express is "rewrite some wheat tokens as carrot tokens".
A crop on a different clock has nowhere to live in it.
That single cause produces all three recorded symptoms: the harvest lands a day late (cadence baked
to `max_yield_day 4`), nothing is ever sold (no CARROT sell row), and `D=26` starves (seed buys baked
to wheat).
It also rules out the leader's actual play by construction, because planting into empty late tiles is
an ADDITION and a tape has no free slots to add to.

The same trap is live in `SOLVED_DAYS` / `PRECOMPUTED_ROUTES`: routes solved against a job pool that
contains no carrot cannot route a carrot.
Testing any new mechanic against baked routes measures whether the baked plan absorbs it, not whether
the mechanic pays.

The real test: carrot planted d21-d26 on tiles the plan leaves empty, with CARROT in the sells row.
`LATE_TRUNCATED_PLANT_DAY = 26` (2026-08-13) opened that window and fills it with wheat.

### Method, once the frame was fixed

Alex's method call, 2026-08-12: test the crop change on **Victor's tape**, not on our agent.
Sweeping a crop flag on our agent conflates "is carrot worth planting" with "does our planner cope
with a different job mix," and our planner's behaviour shifts unpredictably when the job mix changes.
The same call had just reversed the cow-cap result, so it was applied here too.

Harness: `scratchpad/tape_carrot.py` and `scratchpad/carrot_by_town.py`.
Logs: `data/logs/tape_carrot_2026-08-12.log`, `data/logs/tape_carrot_wheattiming_2026-08-12.log`,
`data/logs/carrot_by_town_2026-08-12.log`.

For turns on day >= D, on his own action stream: `PLANT WHEAT -> PLANT CARROT` and
`BUY_SEED WHEAT -> BUY_SEED CARROT`.
Every `SELL WHEAT q` is mirrored by an appended `SELL CARROT q` so the carrot can reach the book at
all — a SELL against an empty shed fails per unit with no penalty (`kaggriculture.py:_commit_unit`),
so the mirror cannot cost anything.

`BUY_PRODUCT WHEAT` is deliberately **not** rewritten.
FEED takes WHEAT 1 (`kaggriculture.py:495`) and he runs 14 animals over 299 FEED ops, so leaving his
wheat purchases alone keeps the herd alive and the result measures crop economics rather than
starvation.
The `starved` column counts FEED ops submitted with an empty wheat shed; the control's own baseline is
11 a season, and any arm where it moves is contaminated.

The control arm (D=99, nothing swapped) reproduces the tape at **$101,917** mean over seeds 11-14,
identical to `tape_cap.py`'s uncapped arm.
That is the gate that says the harness is faithful.

### The first result was entirely a lifecycle artifact — read the weeds column, not the money

```
     D  plants  seeds  starved   mean bank  weeds     delta
    99       0      0       11     101,917    1.5        +0
    26      11      2       11     100,900    1.5    -1,017
    23      55     34       11      93,472   29.2    -8,446
    20      81     89       18      83,835   44.2   -18,082
    16      97    105       33      77,726   45.2   -24,191
    10     114    123       37      59,262   45.2   -42,656
     6     127    136       47      43,522   45.2   -58,395
     0     139    148       73      26,498   45.2   -75,419
```

Weeds go **1.5 -> 45**. Forty-five of his tiles die, in two independent ways:

- **Lifecycle.** Wheat is `first_yield_day 2, max_yield_day 4`; carrot is `2, 3`.
  Past `max_lifespan_step` a tile sheds a yield unit every 2 steps and turns to `WEED`
  (`kaggriculture.py:745-752`). His HARVEST and WATER turns are baked to wheat's window, so a carrot
  tile rots before he reaches it.
- **Seed matching at the boundary.** He front-buys seed — 48 wheat seeds on d20 alone.
  At D=26 only 2 seeds were swapped against 11 plants, so 9 of those plants failed for want of carrot
  seed. D=26 and D=23 are seed-starved; D<=20 are seed-fine but lifecycle-broken.

**This is the difference between a crop swap and the cow cap.** Dropping a `BUY_ANIMAL` leaves every
timing untouched. Relabelling a crop moves the tile's clock while the tape's turns stay fixed.
A tape-side test is only valid for a change that does not move the schedule's own clock.

### Neutralising the lifecycle does not recover the money

Giving CARROT wheat's yield *days* while keeping carrot's own `max_yield` 4, seed $20 and market
prices:

```
     D  plants  starved   mean bank  weeds     delta
    99       0       11     101,917    1.5        +0
    20      81       18      83,782    1.5   -18,135
    16      97       33      76,866    1.5   -25,052
    10     114       37      56,826    1.5   -45,091
     6     127       50      35,064    1.5   -66,853
     0     139       78      14,917    2.8   -87,000
```

Weeds return to the control's 1.5 and **the loss is unchanged** (-18,135 against -18,082 at D=20).
So the dead tiles were never what cost the money.
D=20 is the clean arm: 81 tiles swapped, weeds flat, starvation +7 of 299 FEEDs, **-$224 per tile**.

### The town does not rescue it — 0 of 16 seeds

Alex's hypothesis: the shop draw is per-seed, carrot is carried by only `PET_CAFE` (single-product,
so it drains double) and `FARMERS_MARKET` against wheat's five, so a town drawing PET_CAFE repeatedly
should let carrot hold price while wheat collapses.

Sixteen towns, D=20, control and arm on the same seed, sorted by carrot-minus-wheat weighted drain
(abridged; full 16 rows in the log):

```
   c-w carr  wht   seed    control     carrot     delta  starv   shops
    -6    0    6     14    102,696     82,936   -19,760     18   BAKER BRUNCx2 ICE PIZZAx2 YARNx2
    -5    0    5     12    119,458     95,817   -23,641     18   BAKER BRUNCx2 ICE PIZZA SMOOTx3
    -4    1    5     15    145,607    119,313   -26,294     18   BAKER BRUNC FARME ICEx2 SMOOTx2 YARN
    -2    5    7     19     69,329     58,891   -10,438     18   BAKER BRUNC FARMEx3 PET PIZZAx2
    -1    4    5     11     83,632     69,842   -13,790     18   BAKER BRUNCx2 FARMEx2 PET SMOOT YARN
    +1    6    5     18     45,626     36,430    -9,196     18   BAKERx2 BRUNC ICE PETx3 PIZZA
    +2    6    4     22     72,616     60,682   -11,934     54   FARMEx2 ICEx2 PETx2 SMOOT YARN
```

**The trend runs the way the hypothesis predicted and never crosses zero.**
The smallest losses cluster at the top of the `c-w` column and the largest at the bottom, so the shop
draw genuinely modulates the size of the loss.
But the two seeds where carrot's weighted drain actually *exceeds* wheat's still lose: seed 18
(`PET_CAFE x3`) by $9,196, and seed 22 by $11,934 — and seed 22's `starved 54` against everyone else's
18 means it is feed-contaminated, so **seed 18 is the true best case in sixteen towns, and it is still
a $9.2k hole on 81 tiles.**

### Why the hole is five times the yield-table gap

At base prices wheat is 6 units at $25 less a $10 seed = $140/tile; carrot is 4 at $35 less $20 =
$120. That gap is $20/tile, or $1,620 over 81 tiles. The measured best case is $9,196.

The missing factor is that **wheat is not only a crop for this build, it is the feed supply**.
He buys 246 WHEAT as product across the season to feed 14 animals. Growing his own wheat puts supply
into the book and holds the wheat price down; swapping wheat out leaves those purchases quoting
against a scarcer book, so his feed bill rises at the same time his crop revenue falls.
A crop that feeds nothing cannot substitute 1:1 for one that does, whatever the town draws.

This decomposition (lost crop revenue vs. raised feed cost) was not isolated.

### There IS a sweet spot, it is tiny, and it does not survive a fixed setting

Alex, on being shown the 81-tile arms: "surely there is a sweet spot?? keep enough wheat for the
animal feed and then only swap x carrots."
Correct on both counts, and the day-boundary sweep above could not see it — it conflated HOW MANY
tiles with WHEN, and every arm was 81+ tiles, far past the peak.

Re-run by COUNT with the seed purchases explicitly paired (`scratchpad/carrot_n.py`: each swapped
plant claims an earlier unclaimed wheat seed unit, or it is not swapped, so a starved pairing can
never be misread as an economic result).

**Early tiles are the herd's feed and swapping them is catastrophic.** Swapping the first 2 wheat
tiles costs **$26,405** and drives `starv` 11 -> 34: an animal missing two FEEDs is REMOVED outright
(`kaggriculture.py:804`). The surplus wheat is late-season only.

Amount x start-day, seeds 18 and 11 (`data/logs/carrot_grid_2026-08-12.log`):

```
     D    N    delta   per-seed (18, 11)
    14    2     +122   +217  +28
    20    2     +300   +300  +301
    20    4     +260   +399  +121
    20    8   -1,072   -114  -2,030
    24    2       -4   +1    -8          <- too late to yield before the season ends
```

The pocket is real and sits at **D=20, N=2-4, worth ~$300**.
The ledger (below) put the peak at k=16; the simulator says negative by N=8, so the ledger overstated
the width by ~4x.

**But at a fixed setting across all sixteen towns it loses** (`data/logs/carrot_optN_2026-08-12.log`):

```
  fixed N=1  mean  -$486
  fixed N=2  mean  -$573
  per-seed argmax over 7 arms, 10 of 16 positive, mean  +$284   <- WINNER'S CURSE, not a result
```

Six seeds (12, 14, 15, 23, 25, 26) lose at every N, and three of those have carrot weights of 4, 3 and
3 — perfectly good carrot towns.
The argmax does **not** track the town's carrot drain (`carrot_w 3 -> argmax 1.5`, `carrot_w 6 ->
2.5`, `carrot_w 2 -> 3.3`), so the good seeds cannot be identified in advance.
A per-seed optimum we cannot predict is worth nothing on the ladder.

### The pocket is small because carrot's book is one of the worst in the game

Generalising the question Alex asked — "check it with the other items too" — the premium available in
a book nobody supplies is the integral of `(price(inv) - base)` over the town's season drain.
`scratchpad/pocket_all.py`, town seed18 (the most carrot-favourable of sixteen):

```
  product       drain   pocket$    p1   base   half@   glut     yield/op  seed$  fyd
  STRAWBERRY      300    29,172   265    120     226   linear          4    100   10
  MILK            210    17,696   286    160     157   linear          -      -    -
  WHEAT           696    12,246    51     25     514   log             6     10    2
  EGG             516     8,035    81     50     259   log             -      -    -
  CARROT          570     3,502    42     35     550   sqrt            4     20    2
  TOMATO           84       428    70     60      39   sqrt            4     50    8
```

Carrot drains 570 units and the price only reaches **$42**, because its scarcity curve is `log/0.20`
— the flattest of any crop. It gains almost nothing from being scarce and collapses on `sqrt/0.70`
when supplied. **Wheat is the exact inverse and is the best book in the game to dump into**:
`log/0.20` on the glut side, still above base after 500+ units. That is the quantitative reason every
carrot arm lost — we kept swapping out of the widest book into the shallowest.

`fyd` (`first_yield_day`) also settles which crops can take a LATE swap at all: 2 for wheat and
carrot, 8 for tomato, 10 for strawberry and melon. A tile swapped on d20 has ten days, so carrot is
structurally the only candidate for the late pocket regardless of how attractive tomato looks.

**The pocket ceiling is a property of the town and the market, not of the agent.** No planner, ours or
a perfect one, can extract more than ~$3,502 from carrot's book on the best of sixteen towns, or $91
on the worst.

### What the tape test can and cannot say

Worth stating plainly, because it is the opposite caveat to the cow cap.
The tape is a fixed script tuned to wheat: it cannot redeploy the freed cash, cannot re-route to the
carrot tiles, cannot harvest on carrot's own clock (the timing had to be overridden or 45 tiles rot),
and sells carrot only through mirrored orders.
**So the tape UNDERSTATES carrot**, where for the cow cap it removed a planner artifact that was
flattering the result.
A negative here is therefore not by itself a negative for our agent — the pocket ledger is, because it
is planner-independent.

### THE DECIDING MEASUREMENT — our agent, the real pool, win rate. CARROT_SWAP is OFF.

Everything above is tape-side diagnostics. This is the artifact that ships, scored the way the ladder
scores it. Run on the Windows box, `data/logs/carrot_swap_sweep_2026-08-12.log`
(pull with `scp alex@192.168.1.128:~/kaggriculture/data/logs/carrot_swap_sweep_2026-08-12.log .`).

```
  seeds 1300-1303, 24 recorded ladder opponents, both seatings, 192 games per arm
     value  games     win   mean ours  mean theirs  mean margin
         0    192  65.1%     130,168      109,698       20,470
         1    192  54.7%     124,304      111,341       12,963

  seeds 1306-1309 (chosen because the flag fires on 3 of 4), 192 games per arm
         0    192  67.2%     131,387      108,988       22,399
         1    192  59.4%     127,108      109,569       17,539
```

**-10.4 and -7.8 points, two independent seed sets, 384 games.** It is not one bad matchup: the flag
degrades `Subin An` 38->25 then 25->0, `YassY` 100->50, `Ahmet Abdullah Gültekin` 100->75, `Lemmes
Yad` 100->75, `Farm-ops` 100->88, `MakiMakiAi` 100->88, `UwU` 25->12, and improves against **nobody**.
Money and margin fall together.

`CARROT_SWAP = False` stays False. Do not re-enable it.

**The cheap ledger and the expensive sweep agree, by different routes.** `pocket_all.py` costs seconds
and put carrot's whole book at $3,502 on the best of sixteen towns and $91 on the worst,
planner-independently; the 384-game sweep costs ~40 minutes of box time and says -7.8 points.
That is worth remembering as method: the pocket ledger would have killed this before any of the tape
work.

### What the tape work got WRONG, and why it is recorded anyway

Three things in this file were stated with more confidence than they deserved, and the sequence is the
lesson:

1. **"Net negative at any fixed setting"** was computed on arms that were all silently killing a SHEEP.
   Swapping ONE wheat tile takes the herd from 5 sheep to 4 (`starv` 11 -> 18): his SELL WHEAT orders
   are sized against a shed that used to hold those 6 units, so the sells drain it to zero and the FEED
   finds nothing. A $500 animal plus its wool, charged against a ~$200 book trade, on every arm — the
   wins as well as the losses.
2. **The sweet-spot numbers** (+$300 at D=20 N=2, +$399 at N=4) were per-seed argmaxes over 7 arms. At
   a fixed N the same table is -$486 and -$573. Winner's curse, exactly as CLAUDE.md warns.
3. **The reserve fix made the instrument unusable, not better.** Holding wheat back from SELL cured the
   starvation (`starv` 18 -> 5) and the money went from -$1,199 to -$20,470, with one seed at +$8,614
   and another at -$49,064. Suppressing three sell orders cannot move $49k economically — it moves the
   ORDER SLOTS. A turn's orders compact into ten slots walked in lockstep against the opponent's, so
   dropping one realigns every slot after it and changes who wins each contested unit. **The tape
   instrument has a ±$40k noise floor on a ±$400 signal.**

So the tape was the right tool for the cow cap — where it REMOVED a planner artifact worth thousands —
and the wrong tool here, where the effect is smaller than its own noise. The rule that falls out: check
the instrument's noise floor against the size of the effect before trusting its sign. A tape is exact
for a change the script can absorb and noisy for one it cannot.

### The small version was tested too, on the pool. Also a null.

Alex's version of the idea, which is NOT what `CARROT_SWAP` tested: a fixed handful of late carrot
tiles rather than converting the whole unplanted row. Implemented as `CARROT_TILES = 4` from day 20,
swept on the box against the same 24 recorded ladder opponents, both seatings.

```
  seeds 1300-1303   0: 70.3%   4: 71.9%   (+1.6)
  seeds 1306-1309   0: 74.0%   4: 70.3%   (-3.7)
                    ------------------------------
  mean over 768     0: 72.2%   4: 71.1%   (-1.1)
```

One seed set up, one down, net slightly negative — inside noise. **Flag deleted, not left at 0.**

Read what it actually measured before re-deriving it. Locally the arm planted
`{WHEAT 94, MELON 19, STRAWBERRY 31, CARROT 3}` against a control of `{WHEAT 94, MELON 19, STRAWBERRY
31}` — **wheat is identical**. The rule cut the wheat *request*, later schedule rows refilled it, and
the carrot landed on three tiles that would otherwise have sat empty. So this arm is "carrot versus
bare dirt," the most favourable framing there is, with no feed displaced and no opportunity cost. It
is still a null.

That closes the last version of the question worth asking. The three framings are now all measured:
whole-row swap (-7.8/-10.4 points), small late swap (null), and carrot on idle ground (null, same
arm). Do not re-open without a mechanism none of these covers.

### Verdict (2026-08-12)

Carrot does not pay as a substitute for wheat on this build, on any of sixteen towns, with the
lifecycle confound removed and starvation controlled.
This is a *stronger* negative than C-23's `SHOP_ADAPT_CROPS` result, because it isolates
`WHEAT<->CARROT` alone (C-23 measured it jointly with `TOMATO<->STRAWBERRY` and never separated them),
removes our planner entirely, and varies the town.

Do not re-open on the argument that "CARROT closes above base in 10 of 10 games."
That is true and it is not sufficient: closing above base measures that nobody supplies carrot, not
that supplying it beats supplying wheat.

**Not tested at the time, and superseded by the 2026-08-19 leader-tape read below:** carrot as a
substitute for something *other* than wheat, and TOMATO, which `docs/ladder_losses_2026-08-11.md`
argues for on different grounds — that it is the right home for the ground currently growing the
second melon wave, which is a denial play rather than a yield play.

## 2026-08-19 — Carrot and the empty book

Folded in from docs/carrot_and_the_empty_book_2026-08-19.md.

Read-only analysis. Question: should our agent plant and sell more CARROT, or not.

**Verdict: no general increase.**
Carrot's book is not empty — 94% of strong players already sell some — and on a season-long,
tile-for-tile basis WHEAT nets more per tile-day and per action than CARROT, because carrot's seed
costs twice as much for a similar raw yield.
The one thing worth doing, and that top players already do, is planting carrot specifically as an
**end-of-season closer** on tiles a longer crop cannot finish, and leaning harder into it only when
`town.unlocked_shops` has drawn PET_CAFE or FARMERS_MARKET — that shop draw, not seller scarcity, is
what actually moves carrot's price.
This agrees with, and sharpens, the 2026-08-12 verdict above: carrot still does not pay as a
season-long wheat substitute, but the narrow late-window use the leader-tape evidence pointed at on
2026-08-13 is now measured directly across 120 leader seats, not one tape.

**A correction to the task's own premise, up front.** The background cited game
`ladder_2026-08-17b/94282682.json` as CARROT rising while STRAWBERRY also floored to $1. Replayed
directly: STRAWBERRY closed at **$219** (up from $120), not $1 — only MILK floored to $1. We were the
sole seller of both CARROT and STRAWBERRY in that game, and STRAWBERRY, not CARROT, was the big
winner: 287 units for $65,059 revenue. The "empty book lets the price run" mechanism is real, but it
ran on strawberry harder than on carrot in the one game the thesis was built from.

### Method

Downloaded replay JSON already contains the exact outcome, but the per-turn *action stream* is offers,
not fills (`kagg/analysis/fills.py`; re-posted orders can 24x-overstate a sale). To get ground truth
without touching any code under `kagg/`, `scripts/`, `tests/`, or `submission/`, both seats' own
recorded actions were replayed verbatim through a fresh `kaggriculture` env wrapped in
`record_fills()`, with the game's own `townCenterSellInterval` and its own recorded
`town.unlocked_shops` draw injected turn-by-turn (the same technique `scripts/breakdown.py:tape_policy`
and `env_config`/`recorded_shops` use). This reproduces the exact fills, not offers, for every
product, for both seats, in every game. Replay scripts and JSONL outputs are in the scratchpad only
(`/private/tmp/.../scratchpad/carrot_fills.py`), not committed.

Corpora used:
- **`leaders_2026-08-19`** — 60 games / 120 seats replayed (unbiased pull, winner bank >= $110k; a
  download was still running, so this is more than the 43 files listed at task start).
- **`ladder_2026-08-17b`** — 43 games / 86 seats replayed (our games; **selected losses**, used only
  for behavior/price description, never for a win rate).
- **`kawashigi/*.json`** — 19 of 20 files replayed (the 20th, `schedule.json`, is not a replay).
- **`downloads_2026-08-13/91907974.json`** — 1 reference tape, replayed.

### 1. Is the carrot book empty?

No. Across the 60 leader games (120 seats), CARROT is the **second-most universally sold** crop after
WHEAT/STRAWBERRY/MELON/MILK/WOOL/FERTILIZER, which every single seat sold at least once.
TOMATO and EGG are the genuinely empty books — literally zero seats sold either, and zero board tiles
ever showed a TOMATO plant across all 120 seats at d10/d20/d28 (EGG needs a GOOSE, already closed as a
settled negative — see `project_kaggriculture_animals_verdict`).

| product | seats selling (n=120) | % seats | total units | median units/seller |
|---|---|---|---|---|
| WHEAT | 120 | 100.0% | 84,396 | 601 |
| CARROT | 113 | 94.2% | 1,476 | 15 |
| STRAWBERRY | 120 | 100.0% | 29,797 | 246 |
| MELON | 120 | 100.0% | 12,364 | 120 |
| MILK | 120 | 100.0% | 28,800 | 259 |
| WOOL | 120 | 100.0% | 17,935 | 120 |
| FERTILIZER | 120 | 100.0% | 29,283 | 242 |
| TOMATO | 0 | 0.0% | 0 | — |
| EGG | 0 | 0.0% | 0 | — |

Carrot sellers cluster tightly: quartiles of units-sold-per-seller are 10 / 15 / 15, max 88 (one
outlier, see section 5). Everybody who touches carrot does roughly the same small amount of it. That
is the signature of a garnish crop, not a contested or an ignored one.

### 2. What does the CARROT price actually do?

Median dawn-of-day open vs. close, across the 60 leader games:

| product | median open | median close | close/open | n games |
|---|---|---|---|---|
| WHEAT | 25 | 48 | 1.92x | 60 |
| STRAWBERRY | 120 | 171 | 1.43x | 60 |
| TOMATO | 60 | 80 | 1.32x | 60 |
| CARROT | 35 | 46 | 1.31x | 60 |
| EGG | 50 | 58 | 1.16x | 60 |
| WOOL | 200 | 156 | 0.78x | 60 |
| MILK | 160 | 117 | 0.73x | 60 |
| MELON | 250 | 31 | 0.12x | 60 |
| FERTILIZER | 100 | 7 | 0.07x | 60 |

CARROT appreciates, but it is the **fourth**-biggest appreciator, behind WHEAT (1.92x), STRAWBERRY
(1.43x) and TOMATO (1.32x, on zero sellers — pure shop-drain with no supply at all). The 35->66 one-off
from the task premise is near the top of the observed range (closes ran 33-75 across the 60 games) but
is not typical; median close is 46.

**What actually drives the CARROT close, measured directly:** the number of PET_CAFE/FARMERS_MARKET
instances the town happened to draw (both consume CARROT specifically; shops are drawn with
replacement, so 0-4+ instances are possible in one game).

| carrot-shop instances (PET_CAFE + FARMERS_MARKET) | n games | closing price range |
|---|---|---|
| 0 | 8 | 33-37 |
| 1 | 30 | 38-55 |
| 2 | 10 | 47-61 |
| 3 | 10 | 56-69 |
| 4 | 1 | 65 |

Correlation (shop instances vs. closing price): **r = 0.90**. Correlation (total units sold in the
game vs. closing price): **r = 0.42**, and it's *positive* — more selling goes with a *higher* close,
not a lower one, because both are driven by the same underlying demand draw. This flatly contradicts a
"sellers are scarce, so the price runs" story; the price runs when the *shop draw* runs, and sellers
respond to that, they don't cause it.

### 3. Does carrot need a shop?

No shop is required to **sell** CARROT — `_process_market` will quote and fill a SELL order for any
product in `PRODUCTS` regardless of `unlocked_shops`; the base town-center consumption
(`TOWN_CENTER_PRODUCTS`, every 24 turns) applies to every product including CARROT. What a shop gates
is **demand**, i.e. whether the price is worth catching:

| shop | products | n games it ever unlocked (of 60) | median first day |
|---|---|---|---|
| ICE_CREAM_SHOP | STRAWBERRY, MILK, WHEAT | 54 | 6 |
| SMOOTHIE_SHOP | STRAWBERRY, MILK | 49 | 6 |
| YARN_STORE | WOOL | 42 | 9 |
| BRUNCH_SPOT | EGG, WHEAT, STRAWBERRY | 41 | 12 |
| FARMERS_MARKET | WHEAT, CARROT, TOMATO, STRAWBERRY | 37 | 12 |
| PIZZA_SHOP | MILK, TOMATO, WHEAT | 34 | 12 |
| BAKERY | EGG, WHEAT | 30 | 16.5 |
| PET_CAFE | CARROT | 26 | 16.5 |

PET_CAFE is CARROT's only dedicated shop and it is both the rarest (26/60 games) and the latest (median
first day 16.5) to unlock. FARMERS_MARKET is a second, earlier route to the same demand (median day
12, 37/60 games) but CARROT is only one of four products it consumes there, competing with
WHEAT/TOMATO/STRAWBERRY draw-down for the same instance. Net: carrot demand is gated by luck of the
draw more than by anything plannable, and it tends to land in the second half of the season if it
lands at all (8/60 games never drew either shop).

### 4. Is carrot worth the tile?

Per-cycle mechanics (both crops `first=2`; the difference is `max_yield_day`), confirmed against
`reference/kaggriculture.py` and matching `kagg/economics/production.py`'s own measured constants
exactly:

| | WHEAT | CARROT |
|---|---|---|
| seed cost | $10 | $20 |
| cycle length (plant to harvest) | 4 days | 3 days |
| units/cycle, unfertilized | 4 | 3 |
| units/cycle, fertilized | up to 6 | up to 4 |
| plantings/season (measured, 30-day) | 8 | 11 |
| season yield/tile, unfertilized (measured) | 28 | 29 |
| season yield/tile, fertilized (measured) | 42 | 39 |

Raw season yield per tile is nearly identical (28 vs 29). But CARROT needs **38% more plant/harvest
cycles** (11 vs 8) to get there, and its seed costs **2x** as much per planting. Using this season's
median season-average dawn price (WHEAT $39.1, CARROT $38.4 — also nearly identical):

| | WHEAT | CARROT |
|---|---|---|
| season revenue/tile (unfertilized) | $1,094.80 | $1,113.60 |
| less season seed cost | -$80 (8x$10) | -$220 (11x$20) |
| **net/tile, season** | **$1,014.80** | **$893.60** |
| net revenue per tile-day (÷30) | **$33.83** | **$29.79** |
| unit-actions/season (plant+harvest+water, no travel) | ~40 | ~44 |
| net revenue per unit-action | **$25.37** | **$20.31** |

**WHEAT nets ~13-25% more per tile-day and per action than CARROT run as a season-long staple.**
Fertilizer widens this gap, not narrows it: fertilized, WHEAT nets $52.06/tile-day vs CARROT's
$42.59/tile-day (+22% edge instead of +14%). Travel/routing cost to reach a tile is not modeled here
(a real cost — see the animals routing lesson in `CLAUDE.md`) and would very likely favor CARROT's
shorter cycle even less, since more plantings/season means more trips to the tile, not fewer.

The one real edge CARROT has: **it fits in a shorter window.** A tile that frees up on day 27 can
still run one full carrot cycle (finishes day 30) but cannot run a wheat cycle (would finish day 31,
after the season ends). That is a scheduling property, not a per-unit profitability property, and it
is exactly what the top players' boards show below.

### 5. What do the top players plant?

Board crop-tile counts, summed across all 120 leader-seats, at three checkpoints:

| day | CARROT tiles (sum) | seats with any CARROT | WHEAT (sum) | STRAWBERRY (sum) | MELON (sum) |
|---|---|---|---|---|---|
| 10 | 4 | 4/120 | 676 | 1,587 | 1,971 |
| 20 | **0** | **0/120** | 2,993 | 4,033 | 91 |
| 28 | 198 | 113/120 | 4,258 | 1,889 | 0 |

**Nobody runs a carrot-heavy board mid-season.** At day 20, not a single one of the 120 leader seats
has a single CARROT tile alive. By day 28, 113 of 120 seats have picked some up — this is the "plant
something in the last two days rather than leave the tile idle" move, done almost universally, at
small scale.

One outlier: `93804040`, seat 0 (Thomas Tschinkel, winner, $110,194 vs. opponent's $103,173) ran **35
CARROT tiles** by day 28 — the only genuinely carrot-heavy board in the sample. That game also drew 3
carrot-shop instances (PET_CAFE day 3, FARMERS_MARKET day 18), and its CARROT close hit $75, the
second-highest in the whole sample. He sold 88 CARROT units for $6,264 — his opponent sold 15 for
$1,033, a $5,231 swing that is not nothing against a $7,021 final margin. But even in this best-case
game, CARROT was **5.7% of his total sold revenue** ($6,264 of $110,194); STRAWBERRY ($42,732) and
MILK ($54,015) still did the heavy lifting.

### 6. Verdict

**Do not blanket-increase carrot tile allocation.** The book is not empty (94% already sell it), and
wheat beats it $/tile-day and $/action when run as a season-long crop. What the data supports instead,
bounded and specific:

1. **Keep — and if anything, make more systematic — the end-of-season carrot closer.** Any tile that
   frees up with 3-4 days left in the season (day ~26-29) and cannot finish a wheat/melon cycle should
   get carrot rather than sit idle. 113/120 top seats already do this; it costs nothing to formalize.
2. **Scale carrot up specifically when `town.unlocked_shops` shows PET_CAFE or FARMERS_MARKET**, which
   is readable in the observation and correlates r=0.90 with the closing price. Without either shop
   (8/60 games), do not expect carrot to clear the mid-$30s-$40s; do not overcommit tiles on the hope
   it will.
3. **Do not treat the 94282682 game (35->66/58) as the general case.** It sits near the top of a 33-75
   range driven by an above-median shop draw, not by an emptier book than usual (that game had a
   normal number of carrot sellers for its price level, per the units-vs-close table).

**What would falsify this:** (a) if routing/travel cost were priced in and it turned out CARROT's
shorter cycle needs materially *fewer* trips per unit than this estimate assumes — untested here,
would need a routed-tile-cost study, not board-snapshot counts; (b) if a larger, fresher unbiased
sample (the `leaders_2026-08-19` download was still growing during this analysis) shows the
shop-instance correlation weakening — it is single-sample and not seed-repeated; (c) if a robustness
check shows longer games simply draw more shop instances *and* score higher for reasons unrelated to
carrot (a confound this analysis did not control for, since shop draws accumulate with turns played and
both winners and the shop count grow with game length).

## 2026-08-19 — Both kawa tapes are strawberry-rich boards, so neither can measure the strawberry float

Folded in from docs/the_tapes_are_both_strawberry_rich_2026-08-19.md.

Measured straight off the two replays the agent builds on, counting standing crop tiles at dawn and
the strawberry-carrying shops unlocked at that moment. No agent involved — this is his own board in
his own game.

Strawberry-carrying shops are `BRUNCH_SPOT`, `ICE_CREAM_SHOP`, `SMOOTHIE_SHOP`, `FARMERS_MARKET` —
four of the eight types.

### `92466371`, the strawberry arm (seed 70683142)

```
  d8    straw 8    wheat 3    melon 12   | straw-shops 2 of 2
  d10   straw 19   wheat 5    melon 12   | straw-shops 3 of 3
  d12   straw 37   wheat 17  melon  0   | straw-shops 4 of 4
  d14   straw 42   wheat 18  melon  0   | straw-shops 4 of 4
  d16   straw 38   wheat 12  melon  0   | straw-shops 5 of 5
  d20   straw 38   wheat 22  melon  0   | straw-shops 6 of 6
  d29   straw 1    wheat 14  melon  0   | straw-shops 7 of 8
```

### `92498144`, the melon arm (seed 1240813987)

```
  d8    straw 7    wheat 3    melon 20   | straw-shops 2 of 2
  d10   straw 11   wheat 5    melon 20   | straw-shops 3 of 3
  d12   straw 27   wheat 17  melon  8   | straw-shops 3 of 4
  d14   straw 34   wheat 17  melon  8   | straw-shops 3 of 4
  d16   straw 32   wheat 16  melon  8   | straw-shops 5 -> 3 carry straw
  d20   straw 31   wheat 28  melon  0   | straw-shops 4 of 6
  d29   straw 3    wheat 11  melon  0   | straw-shops 6 of 8
```

### What this means

**The tapes are not neutral ground for this question.** Both draws are strawberry-heavy: the
strawberry arm has all four of its first four shops carrying strawberry, and the melon arm three of
four. On those boards 37-42 strawberry tiles is the *correct* allocation, and it is what he plays.

Cross-checked against tetsuya's 79 seats, which key the allocation on strawberry-draining shops
visible by d12:

```
  straw-shops   0 -> 25.5 tiles   1 -> 26.4   2 -> 34.9   3 -> 36.4   4 -> 36.8
  wheat         0 -> 28.0         1 -> 21.8   2 -> 21.3   3 -> 19.0   4 -> 18.0
```

At 4 shops he plants 36.8 and kawa plants 37-42.
The two leaders agree, and our 42 is very close to right **on these two boards**.

So the flood measured elsewhere is not "we always plant too much strawberry."
It is that we plant 42 on *every* board, including the ~31% of draws with 0-1 strawberry shops where
both leaders plant 26.
Strawberry halves at 31 units above `I0`, so on a thin board 42 tiles is dumping into a book that
physically cannot take it — and that is the case neither tape contains.

### Consequence for how the float gets judged

- On the strawberry arm a d12 cap of 37 trims 5 tiles. Small, and the right direction.
- On the melon arm (3 shops, target 36.4, we plant 34) it trims **nothing** — a structural null, not
  a measurement.
- The change is aimed at boards that appear in neither tape. **A tape-arm A/B cannot validate it**,
  and a null there must not be read as the change being worthless.

It therefore needs a fresh-seed sweep with varying shop draws, scored on **win rate** over paired
seats — which is exactly the instrument that correctly killed the unconditional carrot and tomato
arms, where mean money rose and win rate fell.

### MEASURED AND REVERTED: the float loses $28,259, and the reason is the solved routes

Implemented as `STRAWBERRY_TILES_BY_DRAIN = (26, 26, 35, 36, 37)` keyed on strawberry-draining shop
instances, floating from d12, capping `want["STRAWBERRY"]` in `_refresh_pins` and never retro-cutting
standing ground.
Measured against the seed-cap baseline `b35feee`, same harness, all four arms:

```
              baseline    with float    delta      strawberry   wheat
  straw_q3     155,601      145,048    -10,553      42 -> 37    124 -> 120
  melon_q3     139,453      139,453          0      34 -> 34    134 -> 134
  q4_melon      93,929       78,594    -15,335      34 -> 30    133 -> 125
  q4_straw      78,305       75,934     -2,371      42 -> 38    128 -> 124
```

Three losses, one structural null, **-$28,259 in total**. Reverted.

**The mechanism is in the wheat column, and it is not a tuning miss.** Cutting strawberry did not hand
the ground to wheat — wheat went DOWN on every arm that moved (124->120, 133->125, 128->124). We lost
the strawberry tiles *and* wheat tiles. Strawberry seed also sat unsown in the shed, $400-$500 an arm,
because the purchase was already committed before the cap declined the pin.

The SUSPECTED cause is the precomputed route tables. They are solved for days 12-23 **against the
schedule's own crop counts**, and `_apply_precomputed` keys every stop on the exact `(tile, ops)`
tuple; a miss demotes the job to `_insert_leftovers`, which needs slack the day does not have.
Changing the crop mix after d11 would then desynchronise the day from the route solved for it.

**This mechanism is NOT established, and the one isolation test run so far points the other way.**
Recorded here because the first version of this doc asserted it as fact.

The isolation is a 2x2: drop the solved routes (`cover.UNSOLVE_DAYS = range(12, 30)`) and then add the
crop change. If route conflict is the cause, the change should do BETTER with the routes gone.

```
  straw_q3            routes ON    routes OFF
    tomato 0           155,601      150,291      -5,310 = the cost of losing the routes
    tomato 1           154,484      137,135
    tomato delta        -1,117      -13,156      <- WORSE without routes, not better
```

So on the strawberry board tomato's loss is real crop economics — 0 tomato-draining shops at d12 —
and not route desync. The route hypothesis is refuted for tomato on this arm.

`melon_q3` returned **byte-identical** money on both route settings (139,453 at tomato 0, 145,145 at
tomato 1, either way), so that arm's override never took: the melon/q4 branch resets `UNSOLVE_DAYS`,
which is the trap `q4_branch`'s own note warns about — "an A/B there that reads byte-identical means
the reset line was left in." That half of the 2x2 is a non-experiment and nothing may be read from it.

**The strawberry isolation has NOT been run.** For strawberry the only evidence is the wheat column
above, which is suggestive and not decisive.

### What has to happen before any crop mix can be tested

Solving the routes for 42 strawberry and then planting 37 measures the MISMATCH, not the allocation.
So the order is:

1. Choose the target mix (tetsuya's table, or a swept variant).
2. Re-solve all four tables — `solved_days`, `solved_days_q4`, `solved_days_straw`,
   `solved_days_straw_q4` — against that mix, days 12-23.
3. A/B mix-vs-mix, each running on its OWN routes.
4. Score on paired-seat win rate, not money. That is the instrument that correctly killed the
   unconditional carrot and tomato arms, where mean money rose and win rate fell.

Until step 2 exists, every crop-mix number on the tape arms is confounded by the route tables, and a
loss there is not evidence the allocation is wrong.

The same confound applies to `WHEAT_TILES_TO_CARROT` and `WHEAT_TILES_TO_TOMATO`, which rewrite
`sched[day]` rows from `LATE_CROP_FROM_DAY = 12` — inside the solved range.

### Tomato, for the record

Measured against the seed-cap baseline, one tile from `LATE_CROP_FROM_DAY = 12`:

```
              baseline   tomato=1    tomato=2    tomato-shops at d12
  melon_q3    139,453     +5,692      -3,178     1  (FARMERS_MARKET)
  straw_q3    155,601     -1,117      -4,365     0
  q4_melon     93,929    -11,655      -2,134     0
  q4_straw     78,305     -1,031        +836     0
```

**The "tomato-shops at d12" column above is WRONG, and it invalidates the gate built on it.** Those
counts were read out of the tape JSON files. Our runs force `cfg["seed"]` to the tape's own seed, and
the shop draw is one of only two `random.Random` consumers in the environment, so the board actually
played has a different draw from the one the tape recorded. Printed from the live env at d12 h0 on the
seeds actually in play:

```
  arm        played seed     tomato-drain   straw-drain   tomato=1 result
  straw_q3   70683142              4             2           -1,117
  melon_q3   1240813987            2             4           +5,692
  q4         244615642             1             2          -11,655
```

Four drains loses, two gains, one loses badly. **There is no monotone shop condition here**, and the
"plant tomato only where something drains it" gate has no support: it was implemented, measured, and
found to fire on the q4 board and lose $11,655 while declining on the 4-drain board. Reverted.

Two separate lessons, both of which cost time in this session:

- **Read the draw from the env you are running, never from the tape file.** A forced seed re-rolls the
  shops. Every "shops visible" number in an experiment has to be printed from the live observation.
- **A "read once" rule has to name the day.** The first implementation created the tomato budget on the
  first day that happened to carry a planting row, so on the q4 board the read slid from d12 to d15 and
  saw a `PIZZA_SHOP` that had not existed at the decision point. The gate looked closed and fired.

Also fixed while here, and kept: this block did `sched[day] = _r` unconditionally, inserting an EMPTY
row on every day from `LATE_CROP_FROM_DAY` that the schedule does not plant on — the identical defect
already documented for `CROP_TILE_SHIFTS`, where it made ten different configs all return +$4,691. Both
integers ship at 0 so nothing live changes, but any future sweep of either would have been confounded
by it.

What tomato would still need: the re-solve above, then fresh seeds spanning tomato-shop draws, scored
on paired-seat win rate.

### Timing constraint from the taped opening

d4-d11 are replayed from the tape, so the opening's strawberry is committed whatever the draw says: 37
of 42 tiles are already standing at d12 dawn on the strawberry arm.
A float can only ever move what is left after d11.
Reaching the 26-tile behaviour on a thin board would mean changing the taped opening, which is out of
scope — the tape is the basis by instruction.
The honest ceiling for a post-d11 float is therefore the last few tiles, plus the replant decisions
from d12 on.

---

# Fertilizer, harvest cadence and the season turn (kawashigi/victor tapes, seed 11)

## 2026-08-12 — Day 18: the harvest gap and the sell gap are cadence. One real deficit: FERTILIZER.

Folded in from docs/d18_harvest_and_sells_2026-08-12.md.

Diagnosis by Fable, read-only, in `breakdown.py`'s OWN harness.
Script `<scratchpad>/diag_d18.py`, log `data/logs/diag_d18_sell_harvest.log`.

### Why this run is trustworthy where two earlier ones were not

Twice on 2026-08-12 a hand-rolled comparison seated the tape opposite our own agent.
`breakdown.run` plays BOTH sides as seat 0 against the SAME opponent, so those runs were a different
game and their numbers did not describe the grid.
This run copies `breakdown.run`'s loop exactly, installs the d12/d16/d18 routes, confirms
`PRECOMPUTED_MISSES == []`, and **reproduces the stated grid cell for cell**: d18 harvest 11/14,
water 53/54, feed 12/12, care 12/12, fertilize 4/4, sell 35/61, money 25596/22551.

### Q1 — `harvest 11/14` is NOT three missing harvests. We took them on d17.

    tape 14 = 8 pens (4 SHEEP yield 4, 4 COW yield 3) + 6 STRAWBERRY (planted d6 x1, d7 x3, d8 x2)
    ours 11 = 8 pens (the same 8)                     + 3 STRAWBERRY (planted d6 x1,          d8 x2)

The three extra are the tape's d7-cohort strawberries at `(7,2) (8,2) (9,2)`, each holding
`yield_units = 2` produced at **dawn d17** — STRAWBERRY is `first_yield_day 10, interval 2`, so a d7
planting yields on d17 and again on d19 (`reference/kaggriculture.py:778-789`).
The tape's d17 tours reached only 7 of its 10 d7-cohort tiles, so three carried their units overnight.

We harvested **all ten** of ours on d17 (our d17 harvest is 22 ops against the tape's 18), so at dawn
d18 the whole cohort reads `yield_units = 0` and `crop_ops` correctly offers nothing
(`kagg/search/router.py:705`, `held > 0` fails; the env would refuse it anyway at
`reference/kaggriculture.py:436`).

**Cumulative d16-d18 harvest ops are exactly 46/46.** Strawberry units over d17+d18: ours 40, tape 39.
The tape is a day behind on those tiles and catches up on d18. There is nothing to fix.

The crops both sides leave standing at d18 h23 are MELON planted d10/d11 — age 7-8 against
`first_yield_day 10`, genuinely unharvestable (`:440`) — and filling WHEAT planted d15-d17, which the
tape also leaves.

### Q2 — `sell 35/61` is the mirror of `sell 90/39` on d17.

Both sides follow the same schedule row, so "the row asks for less" is false by construction.
Exact fills from `_commit_unit` via `kagg/analysis/fills.py`, seat 0, ours/tape:

    day    total    STRAW    MILK    WHEAT    FERT    WOOL
    d16    52/56    14/14    18/21   13/13    7/0     0/8
    d17    90/39    16/2     27/3    38/25    9/9     0/0
    d18    35/61    20/27    3/18    0/8      0/8     12/0
    d19    31/45    8/25     18/3    1/1      0/0     4/16

**Cumulative SELL units at the end of d18: ours 499, tape 489.** Money 25596/22551, we are $3,045 up.
The d18 deficit of -26 is the mirror of the d17 surplus of +51.

The mechanism is our own late-sell bias (`LATE_SELL_FROM_HOUR = 16`, `kagg/search/schedule_agent.py:
2278/2282`). The tape posts the row at h0 against a dawn shed still holding yesterday's production; we
sell late on the same day and sweep our own production as it lands. So our dawn-d18 shed holds only
STRAW 20 and MILK 3, which is exactly what we offer — and **every unit we offered on d18 filled**.
WOOL 12/0 is `CUMULATIVE_SELLS` retrying the d16 row; wool reconciles to 84/84 by the end of d19.

#### The one genuine deficit: FERTILIZER 0/8

Our shed held 9-13 fertilizer all through d18 and the row asks for 8, but the sell reserve
(`FERTILIZER_RESERVE_LOOKAHEAD_DAYS = 1`, `:2937`, applied `:3492-3499`) computes
`want = max(today, tomorrow)` tiles offering FERTILIZE = **12**, so `have = max(0, 9 - 12) = 0` and
nothing is offered. The tape sells its 8 at d18 h23 and still fertilizes 12 on d19.

Cumulative FERTILIZER is -8 at the end of d18 and **still -8 at the end of d19** — the only per-product
deficit in the window that does not reconcile.

Whether releasing it is safe is NOT established. The comment at `:3480-3490` records d16 firing 6 of 12
FERTILIZEs when the shed was starved, which is why the reserve exists. Diagnosis only.

### Side observation, not investigated

On d18 our agent buys a COW where the schedule row says `SHEEP 1` (fills: ours `BUY_ANIMAL:COW 1`,
tape `BUY_ANIMAL:SHEEP 1`).

## 2026-08-12 — d16 `fertilize 6/13` is a d11-d14 selling decision, not a d16 routing bug

Folded in from docs/d16_fertilizer_starvation_2026-08-12.md.

Seed 11, tape `victor`. Found while looking for an easier problem than the d11 spawn-ring
misprediction.

### Why d16 looked easy, and was the wrong day

```
d16  unit-turns 320/316   work 122/139   idle 60/49
     UNCOVERED 0          priced slack 96 turns
     offered:  WATER 39   FERTILIZE 12   HARVEST 11
     emitted:  WATER 50   FERTILIZE  6   HARVEST 11
     tape:     WATER 59   FERTILIZE 13   HARVEST 14
```

Nothing uncovered and 96 turns of priced slack, so the crew was neither busy nor failing to reach
anything.
The work simply was not doable.

### The mechanism

`_apply_unit_action` fails FERTILIZE **silently** on an empty hand — `if not _inv_take(inv,
"FERTILIZER", 1): return` (`kaggriculture.py:465`).
`_live_ops` re-derives at each stop, so a unit that arrives with nothing emits nothing and walks on.
The stop is planned, the walk is paid for, the fertilize never happens, and nothing reports it.

Per-unit on d16 — planned depot draw vs what actually reached the hand:

| unit | planned pick | got | FERTILIZE fired |
|---|---|---|---|
| u8 | FERTILIZER 3 | 3 | 3 of 3 |
| u3 | FERTILIZER 2 | 1 | 2 (one from a COLLECT) |
| u12 | FERTILIZER 1 | 0 | 1 (from a COLLECT at h10) |
| u13 | **FERTILIZER 6** | **0** | **0 of 6** |

Total planned draw 12. The units that reach the shed first drain it; u13 plans a six-unit draw against
an empty shed and walks six stops for nothing.

### The actual cause is four days earlier

Dawn shed fertilizer, ours/tape:

```
sh:ferti  d0 0/0  d1 5/5  d2 5/5  d3 5/5  d4 5/5  d5 5/5  d6 3/3  d7 7/7  d8 10/10  d9 12/12
          d10 15/15  d11 10/12  d12 4/9  d13 4/12  d14 1/12  d15 4/12  d16 10/12
```

We track the tape **exactly** through d10, then diverge and never recover.
`collect_fert` is `12/12` every day from d9 to d16 — identical production.
So it is not made differently, it is **spent** differently: the sell rows ask for `FERTILIZER: 24` on
d11, `14` on d12, `8` on d14, and we fill them out of the same stock the fertilizing needs.

`fertilize` first goes wrong at **d12 (`2/3`)** — the day after the stock first diverges — not at d16.

### Why it is worth more than the op count

FERTILIZE sets `fertilized_until_day = day + 2` (`kaggriculture.py:468`), which doubles the yield each
WATER adds for three days.
A missed fertilize is not one op; it is every water on that tile for three days at half value.
That is part of why the `water` row also trails (`d16 50/59`) without any routing problem.

### The landmine to avoid

`cover.py:170-187` already records that refusing a job whose supply is short measured **worse three
times** — work down, idle up, d16 money 7,293 -> 3,280 -> 0.
`SUPPLY_LIMITS_EVERY_DRAW` is off for that reason, and the note ends: *"Turn this on only together
with a rule that raises the shortfall as a purchase."*

So the fix is NOT to refuse the stops.
The candidates, in the order to try them:

1. **Do not sell fertilizer the day's own plan is going to spend.** The row is a target, not a command;
   reserve the planned FERTILIZE draw before filling the FERTILIZER sell quota. This is where the
   divergence is actually created (d11-d14).
2. **Buy the shortfall.** `BUY_PRODUCT` accepts FERTILIZER (`kaggriculture.py:585`), base price 100,
   and we hold $14,407 at dawn on d16 with 96 idle turns. This is the precondition the `cover.py` note
   names.
3. Cap the planned depot pick at the shed's real stock so the plan stops lying to itself, and give the
   surplus FERTILIZE stops to units whose tour already includes COLLECT_FERTILIZER.

### Artifacts

- `tests/test_a_fertilize_stop_is_given_the_fertilizer_it_needs.py` — RED at 12 planned / 6 emitted.
  Asserts the plan against itself, so it cannot be satisfied by lowering the target.
- `data/logs/why_idle_2026-08-12.log` — offered / uncovered / priced-slack for d11,12,14,16,18,19.
- `data/logs/fert_hands_2026-08-12.log` — the per-unit draw table above.
- `data/logs/shed_d17_2026-08-12.log` — the `sh:ferti` row.
- `data/logs/day16_fert_2026-08-12.log` — hour-by-hour d16, ours vs tape.

### Two other things the same run found

- **d18 has exactly one uncovered job: `(0,0)` `[WATER, FERTILIZE, HARVEST]`** — and d18 is where
  weeds go 2 -> 4 and `strawb` drops 35 -> 33. That one uncovered job is a tile dying.
- **d19 is where the season turns.** We lead $23,454/$22,551 at d18 and trail $26,215/$27,133 at d19.

---

# Watering: harvest-window edge cases, day-6 rotation, post-d8 reliability

## 2026-08-13 — Day 6: the two missing waters, found, tried, and reverted on measurement

Folded in from docs/d6_water_2026-08-13.md.

Seed 11, kawashigi grid, weeds 0, recorded shop draw injected, measured on top of the d6 wool ferry
fix (`b92e1bc`).
The d6 row reads `water 17/19`.
This documents where the two waters are, what the fix did, and why it is reverted.

### Where the two waters are

A per-tile probe of d6 (every WATER op attributed to the acting unit's tile, both seats) says the gap
is entirely the ongoing crops:

- Both boards carry 19 established crop tiles at dawn d6: 3 wheat, 12 melon, 4 strawberry, all planted
  to the same schedule.
- The tape waters 17 of its 19 plus its 2 new plantings = 19.
- We water 15 of our 19 plus our 2 new plantings = 17.
- The four tiles we skip are our four strawberries: (2,3), (3,3), (0,4), (1,4).
- The tape skips only two of its strawberries: it waters 2 of 4, staggering the block half and half.

The mechanism is an asymmetry in `router.crop_ops`.
`WATER_ROTATION` — water half the SAFE tiles each day on `(x + y + day)` parity — was added to the
ONE-SHOT branch on melon evidence, and only there.
The ongoing branch (strawberry, tomato) offers a safe tile nothing: survival fires at
`consecutive_unwatered >= 1`, the production branch waits for `produces_tomorrow`, and
`TOP_UP_SAFE_TILES` is measured OFF.
So our strawberries, all planted d5, swing 0/4/0 on alternate days off the survival rule, where the
tape staggers 2/2.
On d6 the two even-parity strawberries (3,3) and (0,4) are exactly the two missing waters.

### The fix, and why it is reverted

The same parity clause was added to the ongoing branch's safe-tile slot, same top-up price
(`_crop_remaining / TOP_UP_DISCOUNT`), with a red-first test
(`test_a_safe_ongoing_tile_joins_the_water_rotation`, since deleted with the revert).
It did what it said at the op level — the probe shows Job(3,3) and Job(0,4) offered and toured — and
it measured as a LOSS at the target day:

| d6 row | before | with rotation on ongoing |
|---|---|---|
| water | 17/19 | **17/19 — unchanged** |
| plant | 2/2 | **0/2** |
| melon (end of day) | 14/14 | **12/14** |
| sell / buy_seed / feed | 14/17, 15/15, 6/6 | 14/17, 15/15, 6/6 |

The route dump shows why the count did not move: `cover.plan` seated the two 1-turn strawberry waters
and left `uncovered=[Job(7,4) PLANT, Job(5,3) PLANT]`.
The waters ate exactly the slack the two far PLANT jobs in the new quadrant needed — unit3 ended its
water run at (3,3) instead of finishing at (5,3), and unit4 spent its spare walking to (0,4).
The two plants slid to d7 (`plant 11/9`), which is a d6 regression under days-match-in-order, and two
waters for two plants is a bad trade the tape never makes.

The tape affords both rows because it has more day: 116 unit-turns to our 113.
Its hands arrive at h0-h1 where ours trickle in to h2, and three unit-turns is precisely the
walk-plus-work the two plants cost.
Crew arrival is out of scope here and is the real constraint.

So per the standing rule the clause was reverted the same day and the test deleted with it; this
section is the record, and the commit message named the null so it is not re-derived.
No note was left in `router.py` itself, deliberately: that file's `WATER_ROTATION` work was still
uncommitted on the branch at the time, and annotating it would have swept someone else's
work-in-progress into that commit.
`water 17/19` on d6 stands as accepted-for-now: the two missing waters are safe-tile top-ups on
strawberries that cannot weed tomorrow (both were watered on d5), while the two plants they displace
are the schedule's row.

### What a future fix needs

- The finding about WHERE the waters go is solid and cheap to reuse: the rotation asymmetry between
  the one-shot and ongoing branches is real, and from d7 onward the rotation-on-ongoing grid actually
  tracked the tape's water column more closely (d11 39/39 and d12 40/40 exact, against 44/39 and 30/40
  without it).
- Any retry must stop a top-up water from displacing scheduled work — the greedy's final pass seats
  both and ranks only on insertion cost, so a 1-turn nearby water always beats a 2-turn far plant.
- Or it must find the three unit-turns: the binding constraint on d6 is crew arrival, not willingness
  to water.

## 2026-08-14 — The last growing day's water: a real 2 units, and a $19,595 fix

Folded in from docs/the_last_growing_days_water_2026-08-14.md.

**Status: DIAGNOSED, FIX REVERTED, DO NOT RETRY AS WRITTEN.**
Board: kawashigi, seed 11, `scripts/breakdown.py --tape kawashigi --days 17`.

### The defect is real

`crop_ops` appends WATER before HARVEST and `_live_ops` walks a stop's ops in order, so when both are
offered the sequence is right.
What decides whether the HARVEST is offered is `_one_shot_is_finished`, which reads
`age >= info["max_day"]`.

The water branch above it uses `in_window = (max_day + 1) // 2 <= age <= max_day` — **inclusive at the
top**.
So at `age == max_day` one more water is still worth one more unit, while the gate has already
declared the window shut.
A tour that reaches the tile before its water demolishes a crop with a unit still owed to it, and the
water lands afterwards on bare ground.

Wheat is `max_day 4`; sown on d0 it hits that on d4.
Every one of the seven tiles stands at `yield_units = 3` at d4 dawn.

    ours                                  tape
      h06 (3,2)  3 -> 0   reached first     h08 (4,1)  4 -> 0
      h07 (4,1)  4 -> 0   W h05, H h06      h10 (3,0)  4 -> 0
      h09 (2,2)  4 -> 0   W h07, H h08      h11 (1,4)  4 -> 0
      h14 (1,4)  3 -> 0   never watered     h14 (0,0)  4 -> 0
      h17 (0,4)  4 -> 0   W h15, H h16      h15 (1,1)  4 -> 0
      h18 (1,3)  4 -> 0   W h16, H h17      h16 (2,2)  4 -> 0
      h21 (2,3)  4 -> 0   W h19, H h20      h16 (1,3)  4 -> 0
      total 26                              total 28, every tile full

Five watered-then-harvested tiles bank 4; the two reached first bank 3.
His earliest harvest of the day is h08, after his watering round.

The two units never come back.
The wheat ledger — buys and sells from fills, harvest from board deltas, feeds from ops — closes
exactly against the dawn shed row and holds the gap at 2:

                   d0     d1     d2     d3      d4     d5     d6     d7      d8      d9
        buy       5/8    5/5    4/4    0/0     6/6    2/2    6/6    3/3    5/17   11/11
    harvest       0/0    0/0    0/0    0/0   26/28    0/0    0/0    0/0   11/12    0/0
       sell       0/3    0/0    0/0    0/0     0/0  18/18    0/0    0/0     0/0    8/8
       feed       2/2    4/4    4/4    4/4     5/5    6/6    6/6    8/9    2/10   11/11
       HELD       3/3    4/4    4/4    0/0   27/29    5/7    5/7    0/1   14/20   6/12

We open d7 holding **0 against his 1**, which is why a hand reaches the pen on `(4,2)` at h14 with
`inv_WHEAT = 0` and d7 reads `feed 8/9`.

Note d0 is **not** a loss: his buy 8 / sell 3 and our buy 5 / sell 0 both net +5, `HELD 3/3`.
The buy-9-sell-3 round trip is not a wheat-supply move and should not be read as one.

### The fix, and why it must not be retried as written

Gating the harvest on `watered_today` at `age == max_day`
(`HARVEST_WAITS_FOR_THE_LAST_GROWING_DAYS_WATER`) makes d4 bank 28 and the unit test pass.
It also loses **$19,595**.

    ours before -> after (tape)
      d4 wheat tiles standing     3 -> 6     (3)    harvests deferred, tiles never clear
      d7 buy_product               3 -> 0     (3)
      d8 buy_product               5 -> 4    (17)
      d8 animals                   9 -> 0    (10)    the entire herd starves
      d9 animals                  12 -> 2    (12)
      d16 animals                 13 -> 5    (14)
      d16 money              30,585 -> 10,990 (32,566)

A deferred harvest is a tile that does not clear, so it does not replant, so the wheat pipeline stalls,
so the shed never refills, so every animal misses two consecutive feeds and is removed
(`kaggriculture.py:804`).
One unit of yield was traded for the herd.

**The lesson is the coupling, not the gate.** HARVEST is not only a collection here; on a one-shot it
is a demolition that frees ground, and the ground is on the critical path for the next sowing. Any
rule that delays a harvest has to be measured against the replant it blocks, not against the units it
collects. The same trap is already recorded one level up in `_one_shot_is_finished`'s own docstring,
where forcing harvests *earlier* late in the season also measured negative.

If this is retried, the shape to try is **ordering without delay** — reach the tile earlier, or make
the tour water before it harvests within the same visit — never withholding the HARVEST op.

## 2026-08-15 — Watering post-d8: a well-evidenced negative, and what actually kills the odd tile

Folded in from docs/fable_watering_post_d8_2026-08-15.md.

Seed 11, tape `kawashigi`, weeds 0.0, worktree on `af3db5d`.
Grid: `PYTHONPATH=. python -u scripts/breakdown.py --tape kawashigi --module schedule_agent --days 17`.
**Superseded mid-session by Alex's 30-day measurement: summed d9-d29 water is ours 798 / tape 795.
There is no volume shortfall. This section records the evidence so nobody re-derives the lead.**
This 798/795 figure directly disproves the "water +65" premise of "Where the harvest gap is,"
below — see that section's DISPROVED header for the resolution.

### Watering is NOT under-planned — the per-day cells that said so are a distribution artifact

The d10 25/32 and d12 30/40 cells are real, but they cancel against d9 29/23, d13 47/41, d15 46/41,
d16 41/37: summed d9-d16 on the 17-day grid the baseline waters **299 against the tape's 274**, and
d9-d29 it is 798/795. Any fix shaped as "create more WATER nodes" is aimed at a gap that does not
exist.

### The one fix tried, and its measured LOSS (do not rebuild it)

`ONGOING_TOP_UP_FROM_DAY = 9` in `router.crop_ops`: a safe ongoing crop (strawberry/tomato) was
offered a discounted preventive water (`_crop_remaining / 8`) from d9, on the argument that ongoing
crops have no preventive cadence at all — `TOP_UP_SAFE_TILES = False` at `router.py:743` means a safe
strawberry is offered NOTHING, so it is watered exclusively by rescue at `consecutive_unwatered == 1`,
one lost stop from death every other day.

d0-d8: **zero changed cells** (verified cell-for-cell, `scratchpad/grid_diff.py`, logs
`data/logs/fable_water_baseline.log` vs `data/logs/fable_water_fix1.log`). But on the true grid
environment (recorded economy + shop draw, `data/logs/fable_probe_grid_baseline.log` vs
`fable_probe_grid_fix1.log`):

    post-d9 weed births   baseline: (0,3)@d16, (0,5)@d16                    = 2
                          fix:      (6,1)@d14 MELON, (0,8)@d16, (0,9)@d16   = 3
    money @ d16           32,794  ->  31,743   (-$1,051)
    d13 waters            baseline 45 offered / 45 watered
                          fix      54 offered / 51 watered, and one of the 3 lost was the
                                   (6,1) MELON survival rescue -> tile dead

The extra cheap offers displaced a rescue — the exact failure mode of the pin experiment in
`docs/spawn_ring_misprediction_2026-08-12.md` ("(1,2) lived and (0,2), (1,4), (2,1) died in its
place"). Reverted immediately; the red-first test
(`tests/test_a_safe_ongoing_crop_is_offered_a_preventive_water.py`) was confirmed red again on revert
and deleted with the fix.

### What actually kills the 2-3 tiles a season: covered rescues on tours that cannot run

Where the water decision is made, for the record:

- Offers: `router.crop_ops` (`kagg/search/router.py:590`), called per tile by `build_nodes`
  (`router.py:1178` at `:1202`). `cover.py` creates no WATER jobs; it covers what it is handed.
- Assignment: `cover.plan` (`cover.py:1893`) from the single dawn solve at `schedule_agent.py:2245`
  (`_solve` at `:752`). `crew.cover` owns d0-d7 only (`crew.ACTIVE_UNTIL_DAY = 8`); precomputed routes
  exist for d12, 16, 18, 23-29 (`cover.SOLVED_DAYS`).

Per-tile forensics on the grid environment (probe in scratchpad `water_probe.py`, log
`fable_probe_grid_baseline.log`): every killed tile's survival water was **offered, covered and
routed**, and died at execution. `data/logs/fable_d15_routes.log` has the smoking gun, d15 dawn:

    u6 start=(4,5) budget=23 cost=25  <-- OVER BUDGET
        DEPOT(4,5)pick{WHEAT:1} -> (4,5)[FEED,CARE,COLLECT] -> (1,4)[HARVEST] -> (0,4)[HARVEST]
        -> DEPOT(4,4)drop -> (0,3)[WATER] -> (0,5)[WATER]
    u9 start=(5,4) budget=23 cost=26  <-- OVER BUDGET

Both of u6's trailing waters — the two tiles that weed into d16 — sit at the tail of a tour the plan
itself prices at 25 turns against a 23-turn budget. The packer's admission check (`cover.cover`'s
`cost`, `cover.py:1280`) prices d10+ days with the closing trip charged (`RESERVE_DAYS`,
`deliver=True, wanted_only=True`), while the shipped route is materialised with `deliver=False`, where
`SHIP_WHAT_NO_LATER_STOP_CAN_BANK` inserts the mid-tour DEPOT drop instead. Two different cost models
price the same tour, a tour can fit under one and ship under the other, and the difference lands on
whatever stops sit at the tail. On d16 the same shape appears at exactly 23/23 — zero margin, which
the spawn-ring arrival slip (1-2 turns, see `fable_spawn_ring_verdict_2026-08-12.md`) then eats.

This is a RELIABILITY defect in tour pricing, not a node-count defect, it destroys ~2-3 tiles a
season on this seed, and it is route-sensitive: the solved_days regeneration in flight will move which
tiles it lands on. Left open deliberately — fixing it is a cover/materialise cost-model reconciliation,
global to all days, and cannot be gated to d9+ without new machinery.

This is the same tour-pricing/cost-model-mismatch family the 2026-08-16 fix at the top of this
document (`_trim_to_the_day`) later addressed for `_apply_precomputed`'s solved-route seating path
specifically; this section's over-budget d15 tours are the earlier, narrower observation of the same
shape.

### Numbers in this section that are route-sensitive

The specific tiles ((0,3), (0,5), (6,1)), the d15/d16 tour dumps, and anything touching d12/d16
(precomputed days under the old victor-solved routes). The rule-level findings — no volume shortfall,
top-up displacement risk, the two-cost-model over-budget mechanism, `crop_ops` branch map — survive a
re-route.

### Verdict

Watering post-d8 is not improvable by planning more water, and the attempt measured as a loss.
The residual watering loss (2-3 tiles/season) is an execution-reliability problem in tour pricing
shared with the spawn-ring family, already documented and owned elsewhere.

## 2026-08-15 — Where `harvest -19` against the tape comes from — DISPROVED

Folded in from docs/where_the_harvest_gap_is_2026-08-15.md.

**DISPROVED. Kept for the record so the same dead end is not re-walked.** The core premise below —
that `water` runs ahead of the tape by +65 units over d9-d29 and is displacing HARVEST — is
contradicted by the measurement in "Watering post-d8" above, made the same day: summed d9-d29 water
is ours 798 against the tape's 795, i.e. **no volume shortfall or surplus at all**. The +65 figure
below and the 798/795 figure cannot both be right about the same quantity on the same tape; the later,
independently-instrumented `record_fills`-based count is the one to trust. The hypothesis and its
proposed experiment are preserved below exactly as written, unrun.

Original framing: a hypothesis, not yet measured, written after the packing and melon fixes.
**Nothing in this section was ever an A/B result.** The grid it was read off was measured while the
solved routes were 72% seated, so the per-day numbers are contaminated. It names a candidate and an
experiment that was never run.

### The shape

Seed 11, kawashigi tape, `--days 30`. From d15 to the end it is the same trade every day:

     day   harvest   gap     water   gap      idle      work
      15     17/18    -1     47/41    +6     68/18   124/118
      19     23/24    -1     48/41    +7     21/22   142/121
      21     34/36    -2     40/34    +6      20/0   151/133
      23     31/30    +1     41/31   +10       9/0   144/128
      24     23/26    -3     53/44    +9       2/0   158/138
      25     28/29    -1     39/33    +6       8/0   144/124
      27     32/35    -3     47/36   +11       1/0   150/135

We do **more** total work than the tape — 150-160 turns against 130-140 — and convert less of it into
produce. Idle is at or near zero on those days, so the crew is saturated and every extra WATER is a
HARVEST not taken.

Season d9-d29: water +65, harvest -19, and the market fills row is also down (1378/1455).

### The candidate

`router.WATER_ROTATION`, emitted at `kagg/search/router.py:692`:

```python
elif (WATER_ROTATION and tile is not None and not cell["watered_today"]
      and (tile[0] + tile[1] + day) % 2 == 0):
    out.append(("WATER", None, _crop_remaining(cell, day) / TOP_UP_DISCOUNT))
```

It waters half the SAFE one-shot tiles — tiles that cannot weed tonight, because they were watered
yesterday — on alternating parity. It ships `True` with **no day gate at all**.

Its own docstring gives its whole evidence base, and it is one day:

> Measured off カワシギ's own d3, seed 11: his board at dawn is 19 tiles ... and he emits **14**
> waters. We emitted 7 ... His extra seven are melon: he is not watering all twelve, he waters about
> half and takes the rest tomorrow.

That is a d3 measurement applied to all thirty days. It is the same shape as two defects already found
the same day: `DELIVER_CUTOFF_TURNS = 99`, tuned on the victor grid and applied everywhere, and the
solved routes, solved against one plan and shipped against another.

`TOP_UP_SAFE_TILES`, which occupies the same slot, ships `False` and has `TOP_UP_FROM_DAY = 7`. So the
flag that IS day-gated is off and the one that is not is on.

### What makes this only a hypothesis (and it stayed only a hypothesis)

**Watering a one-shot crop is productive, not overhead.** Wheat and melon are `ongoing: false` with
`max_yield 6`, so each water raises the tile's eventual yield. More water can mean fewer harvest OPS
carrying more units each, and the grid's `harvest` row counts ops, not units. A harvest count below the
tape's is therefore not by itself a loss.

Two things argued it was a loss anyway, and neither was conclusive:

1. The market FILLS row is down as well (1378/1455), and that one counts units.
2. Late in the season a tile has fewer days left to use the yield it is being topped up toward, while
   the harvest it displaces is banked today.

### The experiment (never run — superseded by the 798/795 result above)

One delta, on a clean board — i.e. **after** the d12-d29 re-solve finishes, because the grid's late
days are exactly the ones whose routes are stale.

Add a day gate to `WATER_ROTATION` and sweep it: off from d15, d20, d25, and never. Judge on the
per-day grid at the target days, not on season money, and require d0-d8 to be byte-identical — which a
gate at d15 or later gives by construction.

The prediction written down first, so it could be checked: gating from d20 raises `harvest` toward the
tape and lowers `water`, and does **not** raise weeds, because the rule only ever waters tiles that
were watered yesterday and so cannot weed tonight.

**This prediction was never tested against data, because the premise it rests on (a real d9-d29 water
surplus) was independently measured false the same day.** Do not resume this experiment without first
re-establishing that a water/harvest imbalance actually exists on a clean, fully re-solved grid.

## 2026-08-09 — The discard problem: a seed-stable harness, a real bug fixed, and a mixed verdict on eviction

Folded in from `docs/fable_the_discard_problem_2026-08-09.md`.

> CORRECTION, 2026-08-09, same day. Every discard quantity in this document is wrong and overstates
> the loss by roughly 15x on the surface that matters. The metric used throughout --
> `held_at_dusk - shed_at_dawn` -- is not the discard: hour 23's SELL and BUY_PRODUCT settle in the
> same `env.step` as the shed rollover, so a sale is counted as a loss. Instrumenting
> `_drop_inventories_to_shed`, the only path that deletes product (`PLACE` into a full shed clamps and
> leaves the remainder in the hand):
>
> | seed 11 | this doc's delta method | env, exact |
> |---|---|---|
> | full season | 105 (below) / 137 | **7** |
> | handover 11 | 145 (below) | **123** |
>
> Final money is identical under both methods -- these are the same runs measured two ways.
> Consequence: on the canonical full-season surface the discard problem is **~20 units a season
> against a $55,837 bank**. It is real and large only on the handover-11 fixture, which is not the
> surface the agent is scored on. Any figure below that is a shed delta -- including a ladder-loss
> "263 units" and `SELL_TO_MAKE_ROOM`'s "101 units" -- needs re-reading with this 15x in mind. What
> survives unaffected: the seed-stability finding and the `FEED_RESERVE_YIELDS_TO_OVERFLOW` day-gate
> bug fix, which is a logic error rather than a measurement. Same class of mistake as
> `feedback_offers_are_not_fills`: a plausible proxy standing in for a quantity the environment
> already tracks exactly.

Branch `shaping-potential`. Starting point: `schedule_agent.py`'s `FEED_RESERVE_YIELDS_TO_OVERFLOW`
mechanism, committed mid-session as `35b83a7 WIP: the feed reserve garrisons half the shed while the
harvest is binned`.

**Verdict, up front.**
- The measurement harness is seed-stable. `make(configuration={"seed": seed}); env.reset(2)` produces
  byte-identical output across repeated process invocations and `PYTHONHASHSEED` values -- no
  reproduction anywhere of an earlier reported "$58,655 vs $66,397 on an identical config" instability.
- Found and fixed a real bug: `FEED_RESERVE_YIELDS_TO_OVERFLOW` had no day gate, so it fired from day
  0 against a four-animal herd, though every attached comment describes a day-16+ mechanism. It moved
  money by up to several thousand dollars on days 0-15 the mechanism was never meant to touch.
- The harder question -- does releasing the wheat reserve to evict actually reduce total product
  destroyed -- is **NOT a clean win**. Across 7 seed/mode combinations, discards got worse in 5 of 7
  and money got worse in 4 of 7, including one seed where releasing the reserve cost **$13,304** of
  final bank for 39 fewer units discarded.
- The router's claim ("no sell rule can close this, product in a hand at dusk was never sellable that
  day") is PARTIALLY confirmed: on the one seed traced night-by-night, 10 of 17 residual discard
  nights already had wheat at or below the eviction floor. But 7 of 17 nights still had wheat sitting
  well above the floor while product died -- the current eviction leaves real, reachable room unused.

**The harness is seed-stable.** `_initialize` calls `resolve_episode_seed(env)`, which reads
`env.info["seed"]` first and only falls back to `configuration["seed"]` if unset; `make()` already
runs one interpreter pass internally, so `env.info["seed"]` is set before the explicit `env.reset(2)`
runs -- the reset re-reads the same seed. Nothing in the schedule agent, router or bundled opponents
uses an unseeded RNG.

Evidence, same tape (`seb1326`), same schedule, same seed, same weeds, three separate process
invocations:

    run A (fresh process):              FINAL_MONEY 74320.0   (16 discard nights, 145 units)
    run B (fresh process, repeat):      FINAL_MONEY 74320.0   (16 discard nights, 145 units)
    run C (PYTHONHASHSEED=777):         FINAL_MONEY 74320.0   (16 discard nights, 145 units)
    diff A vs B: IDENTICAL
    diff A vs C: IDENTICAL

Also tape-vs-tape (both seats replayed straight, no agent) across three processes including two
`PYTHONHASHSEED` values -- identical $77,842 final money every time. If the earlier instability was
real, its source is somewhere other than this `make()+reset(2)` pattern.

**The real bug: the fix wasn't gated to the phase it was built for.** Both
`FEED_RESERVE_YIELDS_TO_OVERFLOW` guards (sell-side `releasable` override, buy-side `floor_short`
requirement) had no day check, though every attached comment frames it as day-16+.

RED test (`tests/test_the_feed_gate_is_a_late_season_lever.py`), full season, seed 11, weeds off,
seb1326 schedule, before the fix:

    day 1: OFF wheat=0 money=759.0   ON wheat=1 money=647.0
    day 2: OFF wheat=1 money=356.0   ON wheat=4 money=183.0
    ...
    day 14: OFF wheat=11 money=63.0   ON wheat=21 money=2478.0
    day 15: OFF wheat=21 money=721.0   ON wheat=21 money=2842.0

Day 0: `floor_short = max(0, FEED_DAYS_FLOOR*alive - shed_wheat) = max(0, 1*4 - 0) = 4` forces an
immediate `BUY_PRODUCT WHEAT` against a four-animal herd that never happens with the flag off.

Fix: gate both guards to `FEED_RESERVE_YIELDS_TO_OVERFLOW and day >= FEED_DAYS_FROM_DAY`, in
`schedule_agent.py` at the sell-side `releasable` override (~line 2549) and the buy-side
`floor_short` requirement (~line 3109). GREEN after; reverting locally reproduces the same 15/16-day
RED diff. `test_the_feed_reserve_yields_a_shed_slot.py`'s starvation guard still passes -- the herd
safety floor is untouched.

**The broader question: does releasing the reserve reduce discards? Mixed, not a win.**
`probe_discards.py`, methodology identical to `test_the_feed_reserve_yields_a_shed_slot.py`'s
fixture: replay the tape, take over with our agent, record every dusk rollover,
`lost = held_at_dusk - shed_after_rollover`, summed over nights where `lost > 0`. Two modes: handover
11 (tape plays d0-10, we take over d11) and full season (we play d0-29, the project's standard
baseline surface).

Handover 11:

    seed  fix    nights_with_loss/29   units_lost   final_money   Δunits   Δmoney
     11   OFF          13                  145         69,530
     11   ON           17                  228         69,036       +83      -494
     12   OFF          12                  101         83,448
     12   ON           11                   87         83,236       -14      -212
     13   OFF          14                   94         64,930
     13   ON           15                  149         66,765       +55     +1,835
     14   OFF          12                   88        128,080
     14   ON           13                   89        128,180        +1      +100

Full season:

    seed  fix    nights_with_loss/29   units_lost   final_money    Δunits    Δmoney
     11   OFF           9                  105         54,813
     11   ON            9                  106         54,474        +1        -339
     12   OFF          15                  117        103,273
     12   ON           12                   78         89,969       -39     -13,304
     13   OFF           5                   10         77,790
     13   ON            6                   20         77,798       +10          +8

Across all 7 seed/mode combinations: discards got worse in 5 of 7, better in 2 of 7; money got worse
in 4 of 7, better in 3 of 7. The one large swing, full-season seed 12, is **-$13,304** of final bank
for 39 fewer units discarded -- enough by itself to block calling this a fix. Not reverted by the
author; the day-gating fix is worth keeping regardless of what happens to the rest of the mechanism.

**Testing the router's claim, rather than assuming it.** For every night that still loses product
with the (day-gated) fix ON, check whether shed WHEAT was already at or below
`FEED_DAYS_FLOOR * alive`, the eviction floor. Seed 11, handover 11:

    day  shedWHEAT  floor(1*alive)  shedTOT  hands  lost  wheat_at_or_below_floor?
      4          7               7        7     21    21  True
      9         10              10       10     12     5  True
     12          8              17       13     16     2  True
     14         14              20       19     15     3  True
     16         28              19       28     73     2  False
     17         33              19       33     69     2  False
     18         35              19       36     69     5  False
     19         19              19       29     97    26  True
     20         48              19       48     61    15  False
     21         19              19       25    126    51  True
     22         19              19       44     64     8  True
     23         19              19       33     89    22  True
     24         20              19       40     60     1  False
     25         19              19       36     71    14  True
     26         19              19       42     65    23  True
     27         19              19       46     68    14  True
     28         19              19       53     49    14  True

10 of 17 nights have wheat already at the floor -- nothing left to evict, matching the router's
claim. But 5 nights (d16, d17, d18, d20, d24) have wheat sitting 9-29 units above the floor while
product dies -- most strikingly d20, 48 units of wheat in the shed (all of it,
`shedTOT == shedWHEAT`) against a floor of 19, 29 units of reachable room unused while 15 units of
other product were destroyed the same night. Conclusion: the router's claim is real for a majority of
residual nights, but roughly a third show the current eviction leaving real, already-identified room
on the table -- plausibly because `release_order`'s eviction is throttled by the same per-turn/
per-order caps as an ordinary sale. Flagged as the next thing to measure, not claimed as done.

**What changed.** `kagg/search/schedule_agent.py`: the day-gating fix (both guard sites) -- the only
code change, `kagg/sim/*` untouched. `tests/test_the_feed_gate_is_a_late_season_lever.py`: new, RED
before, GREEN after, reverted-and-confirmed-RED. `test_router.py`: not touched, but checked both
ways -- committed WIP (`35b83a7`, ungated) leaves it at 11 failed/59 passed/6 skipped; with the
day-gating fix, 8 failed/62 passed/6 skipped, a strict subset, three fixed outright, no new failure.
The remaining 8 failures pre-date this session and are a handoff item, not introduced or fixed here.

**Recommendation.** Keep the day-gating fix -- a strict improvement with no measured downside. Do not
ship `FEED_RESERVE_YIELDS_TO_OVERFLOW = True` as a discard fix on the strength of the 7-combination
A/B in this document. If picked back up, the next measurement is the eviction's own throttle (the "5
of 17 nights had unused room" finding), not the reserve floor or the router.
