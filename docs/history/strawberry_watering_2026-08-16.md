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
