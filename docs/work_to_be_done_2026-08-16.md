# Work to be done, as at 2026-08-16

Written at the end of a long session so the open threads are not re-derived tomorrow.
Everything here has a measurement behind it; where it does not, that is said explicitly.

## 1. The opening, d1 to d8 — the largest known defect

The per-cell gate (`tests/test_each_day_matches_the_tape.py`, 30 days x 26 rows) fails 260 cells.
Days match IN ORDER, so the lowest failing day is the one to fix.

    d1  COLLECT_FERTILIZER  4/3      + PLACE          <- lowest failing day
    d3  WATER              13/14
    d4  WATER              16/15
    d5  WATER              12/13
    d6  WATER              16/19     + PLACE, crop_MELON, weed
    d6  BUY_LAND           ours h9 / tape h4          five hours late
    d7  WATER              28/27     + crop_MELON, weed
    d8  WATER              17/33     + PLANT 8/9, DIG, crop_MELON, crop_WHEAT

The cadence gate (`tests/test_the_money_lands_on_his_turn.py`) adds a second, independent defect:
**we buy seed at dawn, he defers it to dusk.**

    d10  BUY_SEED  ours h[1,1,1]   tape h[20,21,22,23]
    d12  BUY_SEED  ours h[1 x9]    tape h[14,16,18]
    d15  BUY_SEED  ours h[1,1,1]   tape h[16,16,18,18,20,22,22,23]

Seed is for TOMORROW's planting. He keeps the bank liquid through the day; we commit it at h1 on
days that open at $4, and `_do_hire` fails SILENTLY on a short bank.

## 2. Watering priority — a fix that exists, is measured, and is switched off

`cover.AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP` is uncommitted and False. It makes a tile one dry
night from weeding outrank a pen that was fed yesterday, which is `REQUIRED_OPS`' own argument
applied to the other half of the board.

Measured on seed 11 at `weedSpawnChance` 0: kills the two d8 weeds, d8 feed 9/10 -> 10/10, plant
6/9 -> 9/9 EXACT, strawberry 10/11 -> 11/11 EXACT — but costs d10 sell 95 -> 68 and $4,619, because
d10 is a `WALK_THE_LOAD_HOME_DAYS` day and the at-risk tiles take the turns the melon delivery needs.
By d13 the money is a wash ($18,960 vs $18,880) and the weed count is WORSE — it kills the d8 weed
and grows a new one at d11 that survives to d13.

**Next step:** exempt the walk-home days (10, 29) and re-run. And re-measure at
`weedSpawnChance` 0.005, the ladder value — the numbers above are from a board nobody plays.

### 2a. It is TWO defects, and only one of them has a fix written

Added 2026-08-16, later the same day.
The pass-order fix above is aimed at **turn-constrained days, d7 to d11**.
It cannot be the mechanism for the d12-d14 deaths, and the idle counts say so outright.

    day  unit-turns  idle  water  dig      game 93593633, planner, LOST
     12         256    77     22    0
     13         275    93     27    0
     14         211    41     29    0      <- eight strawberry tiles die here
     15         294    30     41   17

A cheapest-insertion greedy with 77 spare unit-turns places every job it is HANDED.
So on d12 the WATER job for those tiles was never in the pool.
That makes the d12-d14 failure a **job-generation** defect, not a pass-order one, and the fix at
`cover.py:1584` will not touch it.

The mechanism suspected was the precomputed path.
`cover.cover` returns EARLY on any day in `PRECOMPUTED_ROUTES`:

    pre = _apply_precomputed(day, units, jobs, ...)
    if pre is not None:
        return pre

So on those days **none of the greedy machinery runs** — not the `at_risk` pass order, not `REPAIR`,
not `COMPACT`.
A job the solved route has no stop for goes to `_insert_leftovers`, a cheapest FEASIBLE insertion into
tours that are already built, and whatever will not fit is simply not done.
The solved days start at **d12** on a three-quadrant board and **d9** on a four-quadrant one, which is
exactly where the deaths start.

### 2a-i. Measured, and the d12 half of it is a NULL

`scripts/what_the_solved_day_drops.py`, seed 11, `weedSpawnChance` 0.005, kawashigi schedule.
Two arms: the shipped gate, and `--fork` forcing `MELON_YIELD_OPPONENT_MELON` to 0.
Logs at `data/logs/precomputed_drops_2026-08-16.log` and `..._fork_2026-08-16.log`.

     day    jobs seated ins DROP water  |  jobs seated ins DROP water      no fork -> fork
      12      43     37   6    0     0  |    39     32   7    0     0
      13      62     56   6    0     0  |    63     53  10    0     0
      14      52     48   4    0     0  |    45     38   7    0     0
      18      57     49   8    0     0  |    59     31  28    0     0
      20      72     60   8    4     3  |    71     51  15    5     5
      23      70     58  11    1     1  |    70     47  19    4     4
      24      73     49  14   10    10  |    69     39  16   14    14
      25      70     53  14    3     2  |    70     43  18    9     4
      27      71     58   7    6     6  |    72     47  17    8     7
      29      37     16  21    0     0  |    38     14  24    0     0

**Zero jobs are dropped on d12-d19 in either arm.** The hypothesis that a d12 water job goes
unoffered or unplaced is not reproduced on this seed, and it should not be carried forward as
though it were.
Game 93593633 was a different board, seed and opponent, so this does not refute it either — it means
the mechanism has not been caught in a sim yet.

**What the run DID measure, and it is the fork's real cost on the back half:**

- On the fork board the solved day stops MATCHING. d18 seats 31 of 59 stops against 49 of 57
  unforked; d24 seats 39 against 49. The solve is roughly half discarded, and `_insert_leftovers`
  carries the rest — 28 insertions on d18 against 8.
- Tiles whose WATER is dropped on two or more solved days go **3 -> 8** with the fork on.
  `(0,7)` and `(9,4)` are dropped on three days each. Two dry days is a weed, so a tile appearing
  here twice on consecutive days is one we killed.
- The damage is at **d20-d27**, not d12-d14. d24 drops 14 waterings with the fork against 10
  without.

This is one seed. The direction is consistent with the ladder replays; the magnitude is not
established.

### 2b. The solved tail is per BOARD SHAPE, and there are four shapes, not three

Alex's point, 2026-08-16.
Two independent branches decide the back half of the season, and their product is four boards:

                    3 quadrants (75 tiles)      4 quadrants (100 tiles)
    melon  (34 st)  A3  91919278                Q4  91907974
    straw  (42 st)  B3  91891131                MISSING

The strawberry-forked four-quadrant board is the worst case on both axes at once — 42 permanently
watered tiles spread across 100 tiles — and it is the one branch with no recorded tape and no solved
tail.
That is the most likely reason the strawberry deaths cluster in fork games.

So "fix the watering" on the tape path means recording or synthesising **B4**.
On the planner path it is one solver, but the solved days still have to be re-solved per shape, which
is the same four cases.

### 1a. REGRESSION, found 2026-08-16 — the gate moved and nobody said so

The grid gate is **303 failed / 477 passed** at `c5831f9`, against **260 / 520** at `8b74e05`.
Forty-three cells went from green to red.
Bisected by running the CURRENT gate file against each commit in a worktree, with the CWD inside the
worktree so `import kagg` resolves there — the first two attempts silently imported the main repo's
`kagg` and reported a false "no change":

    8b74e05   260 failed  520 passed   Delete eight flags whose ON branch has never executed
    ed927fe   300 failed  480 passed   The four-quadrant herd is COW 6 / SHEEP 10          <- +40
    6a01c59   303 failed  477 passed   Restore the q4 herd to COW 6 / SHEEP 12             <- +3
    c5831f9   303 failed  477 passed   (docs and scripts; no change)

The failing rows are led by `an_SHEEP` (21 days) and `an_COW` (21 days).
**Seed 11 arms the four-quadrant branch**, so the q4 herd numbers are live in the gate, and the note
in section 5 that the gate "held at 311/590/115/35 through all three deletions" describes only the
deletions — it was never re-run after the herd work.

This is a d1-onward regression that shipped in the tape bundles. Fix before anything else.

## 3. Strawberry is what actually dies, and the fork makes it worse

Live ladder game 93593633 (planner, LOST $90,355 v $101,782), tile by tile:

    21 tiles became WEED. 20 were ours. NINETEEN were STRAWBERRY.

    d9 1   d10 4   d11 4   d12 1   d14 8   d15 1   d27 1

    day  unit-turns  idle  water  dig
     12         256    77     22    0
     13         275    93     27    0
     14         211    41     29    0
     15         294    30     41   17

We idle 77 and 93 unit-turns on d12-d13, eight strawberry tiles die on d14 (a crop weeds after two
dry days), and d15 spends 17 turns digging the corpses. **It is not a turn shortage.**

The mechanism is in the reference: MELON is `ongoing: False` — water it to day 10-12, harvest once,
tile spent. STRAWBERRY is `ongoing: True` — water it EVERY day to the end of the season or it weeds,
harvest every 2 days. The melon fork takes strawberry from 34 tiles to 42, converting eight finite
obligations into eight permanent ones.

**The fork fires on 44% of real games** (32 of 72 downloaded replays). Real opponents cluster at 8
and 12 melon tiles at d3, and the rule's threshold of 9 splits those clusters exactly.

### 3a. The fork CAUSES the deaths; it does not by itself decide the game

Measured on submission 55548563's real 28-episode ladder record, pulled from the Kaggle API rather
than from `~/Downloads` — see the selection-bias warning at the bottom of this file.

                     games   weed tile-days   strawberry tiles died   mean margin
    fork FIRED / W       8             62.0                    11.9         +42,798
    fork FIRED / L       4             43.8                    13.0          -6,904
    fork quiet / W      15             43.7                     5.5         +16,722
    fork quiet / L       1             20.0                    10.0         -10,716

Two readings, and they point in different directions:

- **The fork more than doubles strawberry deaths — 5.5 without it, 12.4 with it.**
  That holds in both the wins and the losses, so it is a property of the fork rather than of the
  games it happened to be drawn into. The mechanism is confirmed.
- **It does not separate wins from losses.** Within fork games the death count barely moves
  (11.9 in wins, 13.0 in losses), and fork-fired wins still average +$42,798.

The observational data cannot go further than that, because the fork's trigger — opponent melon >= 9
at d3 — is itself a proxy for opponent strength.
Against 12-melon builds the fork ALWAYS fires, so there is no control group.
The only clean test is a ladder A/B: the same bundle with the fork off, against the same population.
If fork-off also goes ~50/50 against 12-melon opponents, the fork is innocent.

### 3b. Two more games, 2026-08-16 12:59

    episode    our seat   ours       theirs     margin    opp melon d3   fork    straw died   weed tile-days
    93605352   1          153,932    155,937    -2,005    12             FIRED    4           18
    93606247   0           87,539     85,733    +1,806     5             quiet    4           97

Both inside $2,100, and both fit the pattern: the loss is a 12-melon opponent with the fork armed,
the win is a 5-melon opponent with the fork quiet.
The loss killed only **four** strawberry tiles, so this one is not a watering blowout — it is a close
game against a strong build, which is the reading 3a leaves open.
Planner record now 24W-6L.

## 4. The melon fork is NOT implementable as a tape rewrite

Measured, 24 games against the frozen opponent: token-swapping MELON to STRAWBERRY inside a tape
recorded for melon scores **0.0% win rate against 66.7% with the swap off**, -$17,297 a game.
Adding a dig-guard lifts it to 12.5% and no further.

Product level, seed 3: the swap is +$2,966 on CROPS (fewer melons at $233 rather than $170, because
we stop crashing our own book) and -$8,365 on ANIMAL products. **The animal side is unexplained.**

One cause is identified and is a bug in the guard: keeping the strawberry alive leaves the tile
occupied, and the tape then plants on it — 12 wasted PLANTs against 1 with the swap off. The guard
must also suppress the REPLANT that follows the dig it cancelled.

The fork belongs in the planner, which knows each tile's crop and `ongoing` flag. A tape cannot
adapt maintenance to a crop it was not recorded for.

## 5. Refactoring — started, not finished

    done   plan_routes + _two_opt + _path_len + COVER_PLANNER     -319 lines, 10 tests deleted
    done   board_layout.py, sa_hiscadence_probe.py                -269 lines
    done   8 hard-OFF flags and their unreachable branches
           the three live files: 9,881 -> 9,245 lines

    left   10 hard-OFF flags  blocked by scripts/tests that set them at runtime
           101 hard-ON flags  same delete, keeping the branch that runs
           63 tests           assert a constant equals itself; they die with their flag
           3 constants        defined TWICE in the same file, the second silently wins:
                              SELLS_FUND_THE_TURN, URGENT_OPS, STEAL_FROM_DAY (read nowhere)
           victor             still a live tape in TAPES with 3 tests bound to it

The gate for every delete: both acceptance suites must report **311 failed, 590 passed, 115 xfailed,
35 xpassed**. Unchanged through all three deletions so far. A moved number means the code was live.

`coverage --branch` over five seeds says 25 scripts import the 0%-coverage modules and 22 of them
run, so `chains`, `dayplan`, `executor`, `library` and `replay_plan` are load-bearing for tooling
even though they never execute in a season. They are NOT free deletes.

### 5a. The end state, agreed 2026-08-16: split `make_agent`

The file length is not the problem and never was.
`schedule_agent.py` is 5,156 lines of which **2,696 are comments and 365 are blank — 2,095 lines of
code.**
The problem is the shape:

    47 top-level defs, two of which are most of the code

      1,638 lines   make_agent      line 3519
        666 lines   _router_acts    line 1643
        154 lines   _refresh_pins
        101 lines   reservation_units

One 1,638-line function holding pins, hires, land, market orders, seed rows, the herd split and the
dusk top-up in a single mutable closure.
That is where "nobody can say whether the code being edited is live" comes from.

**How it is split does not matter much, as long as it makes sense.** Alex's call.
The point is that it stops being spaghetti — a reader should be able to find where a thing is
decided without reading 1,638 lines of one closure.

`kagg/search/q4_branch.py` is a reasonable example of the target readability: a trigger, a decision
taken once, and what changes when it fires, in one file you can read end to end.

**Order of work, and the reasons are dependencies rather than preference:**

1. Finish the flag deletions. Every flag is a cross-cutting condition; splitting around one means
   carrying it into two modules.
2. Resolve the eight doubly-defined constants FIRST. Today the second definition silently wins and
   the file still works. Split the file with a duplicate still in it and the two halves get
   different values — a real bug where there is currently only a readability defect.
3. Collect the surviving numbers into one block per file. Several of the remaining flags fold into a
   number, and they should land somewhere deliberate rather than beside whatever function used them.
4. Then split, one module at a time, gates green between each.

Not started, and not to be started while the watering work is live in the same three files.

## 6. What the allocation LP says (`docs/allocation_bounds_2026-08-16.md`)

The leader's MELON 20 / STRAWBERRY 34 is **not** inside the 1% near-optimal region: -1.78% against a
zero opponent, -3.9% against his own supply, -23% against double supply. Melon alone is the cause —
~30 units of town demand a season, `sq` crash above threshold, and no shop ever sells melon seed.
Strawberry 34 IS inside the 1% interval in two of three scenarios.

Melon's 1% interval slides `[14,42] -> [0,31] -> [0,12]` with the opponent, so no fixed melon count
is near-optimal against all three — an argument FOR a melon fork, though not for the one we have.

Geese become obligatory against a flooder (`[8,22]` at double supply) because egg's log-flat price
is the only crash-proof product. We ship geese off.

Caveats: these are LP-relaxation OUTER bounds, MILP gaps 0.4-2.0%, and Z* swings
$129k / $93k / $53k with the shop draw.

## 7. Open and unexplained

- The animal-product loss under the melon swap (-$8,365 on milk and wool, on one seed).
- Why swap-OFF wastes 19 FEED, 19 CARE and 17 COLLECT ops while swap-ON wastes none, yet earns more.
- The ~550 rating points between fe7aad6's 1947.9 and today's builds. The close package was ruled
  out by ablation (+41.7pp of win rate, carried by NO_UPKEEP_ON_THE_LAST_DAY and
  WALK_THE_LOAD_HOME_DAYS; the other four exact nulls).
- The q4 branch fires on ~15% of seeds by the old count, but **the yarn-store unlock is not a pure
  function of the seed** — it depends on how the town is played, and both seats affect it. Seed 3
  arms against the frozen opponent and not against an idle one; seed 7 is the reverse.

## 8. Live submissions at the end of the session

    55548563  planner  post-1947.9 lineage, q4 armed, melon fork d3>=9    ~1500
              KNOWN DEFECT: its q4 rows carry SHEEP 10, the herd standing at season end.
              The tape BUYS SHEEP 12. Fixed in 6a01c59, AFTER this bundle was built.
    55549820  tape3    two tapes, dig inserted with day-slack and must-dig, both swaps

Selection bias warning for any analysis of `~/Downloads`: those replays are LOSSES, chosen by hand.
Within-sample comparisons are fine; a win rate computed from them is not.
