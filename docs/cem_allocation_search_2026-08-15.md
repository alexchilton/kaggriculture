# CEM over the crop and herd allocation dials, 2026-08-15

**Result: NULL. No dial change beat the shipped allocation on a held-out seed draw.**
The best finalist scored 0.521 against the shipped agent where a copy of the shipped agent scores
0.500, on 48 duel games — a margin of one game — and banked less money.
The search space is not empty of information, though: it says clearly that **geese lose**, that the
**melon fork should stay on**, and that **large shifts of any kind lose**.

## Where everything is

| what | path |
| --- | --- |
| worktree (this doc, the scripts, the tests) | `/Users/alexchilton/DataspellProjects/kaggriculture/.claude/worktrees/agent-ad41a3e7598e524c4` |
| run log, on the Windows box | `/home/alex/kagg-cem/logs/cem_allocation.log` |
| machine-readable history | `/home/alex/kagg-cem/logs/cem_allocation.json` |
| pinned code copy on the box | `/home/alex/kagg-cem` (`kagg/` rsynced from the main tree; `data/` and `reference/` symlinked to `~/kaggriculture`) |
| python | `/home/alex/kaggriculture/.venv/bin/python`, `kaggle-environments 1.32.7` |

The box is the Windows machine at `192.168.1.128`, reached over WSL2 direct SSH on port 2222.
16 cores, 13 GB RAM.
`kagg` is not installed into the venv, so it resolves from the working directory; running from
`/home/alex/kagg-cem` picks up the pinned copy and not `~/kaggriculture`.

The pinned copy was taken from the **main tree working state**, not from a commit, because that is
where today's measurements were made and the branch was moving during the session.
Hashes at the time of the rsync:

    2917218870709210a17323c1d69c11a9  kagg/search/schedule_agent.py
    8e45c9a19574d8ca9ff9e2583014f84d  kagg/search/cover.py
    99ca87d36e991b1586a7b194780ac29a  kagg/arena/pool.py
    924c60dc6cf6a13671230363ecb3cc10  data/seed_scripts/kawashigi/schedule.json

## What was searched

| dial | name in `schedule_agent` | range | what fixes the bound |
| --- | --- | --- | --- |
| `fork` | `MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT` | 0..1 | a flag |
| `m` | `CROP_TILE_SHIFTS` `WHEAT -> MELON` | 0..24 | wheat plant stops in d12..d17 |
| `t` | `CROP_TILE_SHIFTS` `WHEAT -> TOMATO` | 0..14 | wheat stops left before d18 |
| `c` | `CROP_TILE_SHIFTS` `WHEAT -> CARROT` | 0..24 | wheat stops left before d26 |
| `s` | `CROP_TILE_SHIFTS` `STRAWBERRY -> WHEAT` | 0..7 | all the late strawberry there is |
| `g` | `HERD_GEESE` | 0..3 | the dial saturates; 4 is byte-identical to 3 |

Every bound is pinned by `tests/test_the_allocation_dials_reach_the_tiles_they_claim.py`, 13 tests,
all green.

## Three things found before the search started, each of which changed the design

### 1. `CROP_TILE_SHIFTS` cannot reduce melon, so the melon fork had to go in the search space

The schedule plants melon on **d0, d6 and d7 only**, and `LATE_CROP_FROM_DAY` is 12.
A `MELON -> WHEAT` shift therefore moves exactly zero tiles.
Counted off `schedule.json`, the plantings reachable from d12 are WHEAT 109, CARROT 8,
STRAWBERRY 7 — and no melon at all.

So the brief's "melon tile count" is not reachable through the shift dial in the raising direction
only; it is not reachable through it *at all* in the lowering direction, and the shipped
MELON 12 / STRAWBERRY 41 split is set before d12.
The one dial that moves it is `MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`, which converts the d6/d7
melon rows to strawberry once the opponent shows 7+ melon tiles.
Turning it off holds MELON 20 / STRAWBERRY 34 — which is Kawashigi's own allocation and the
direction today's sweep pointed.
That is why the fork is dial number one.

### 2. Win rate against `pool.OPPONENTS` is saturated and cannot rank anything

The first design scored candidates against six pool opponents.
Measured on 2 seeds, both seatings:

    call 0: 24 games in 30.9s   win 0.8333 draw 0.1667 mean $146,050
      carrot_25:1.00  contrarian:1.00  cow_heavy:1.00  melon_heavy:1.00  mirror:0.00  wheat_only:1.00

The shipped agent wins **100%** against every member except `mirror`, which it *draws* 100% of the
time because it is the same file playing itself.
A first smoke run of the CEM confirmed it end to end: every candidate in the generation scored
`elo 1.000`, and the held-out table was four rows of `1.000`.

An Elo objective needs an opponent that can beat us.
The strongest available is a **frozen copy of the shipped agent**, injected as
`pool.OPPONENTS["shipped"]`.
`carrot_25` and `melon_heavy` stay in as guards — `CLAUDE.md` records melon going 25 -> 12 -> 25
because a mirror-only sweep pointed the wrong way, on this exact dial, and `melon_heavy` is the only
guard that fires the fork at all.

### 3. Two candidate files in one process shared one set of dials

`scripts/cem_collection.py` reported **byte-identical** tiles, bank and collection for `m8`, `c8`,
`s4` and the zero vector — MELON 12, WHEAT 132, STRAWBERRY 41, CARROT 8, $132,959 on all four.
The dials were not reaching the game.

The cause: a candidate file sets its dials on the shared module.

    import kagg.search.schedule_agent as A
    A.CROP_TILE_SHIFTS = (("WHEAT", "MELON", 8),)

`import` returns the module already in `sys.modules`, so the second file to load wins and **both**
agents play its dials.
This is not a scripting nuisance — it silently turns every duel in the objective into a mirror
match, and it does so without an error.
`scripts/geese_pool_eval.py` and any other script using that `write_candidate` pattern has the same
hazard whenever two dial-setting files meet in one process.

The fix is a private copy of the agent module per candidate file, loaded from source under a unique
name with `__package__` set so its relative imports still resolve.
Pinned by `tests/test_two_candidate_files_do_not_share_one_set_of_dials.py`, 4 tests, including a
deliberate reproduction of the bug.

## The routing regime: the unsolve is not needed, and it costs money

`cover.PRECOMPUTED_ROUTES` covers exactly d12-d29 — the days the shifts touch — and keys a stop on
`(tile, ops)`, so `scripts/swap_one_crop.py` unsolves those days unconditionally, on the argument
that a re-crewed stop would otherwise be dropped from the solved route.
Unsolving costs **3x the wall clock** (the same 24 pool games: 96s unsolved, 31s solved), so it was
worth measuring rather than inheriting.

Seed 3, against the frozen shipped agent, `scripts/cem_collection.py`:

    config        regime      bank      tiles                                   collection
    zero dials    SOLVED    $132,959   MELON 12 WHEAT 132 STRAW 41 CARROT  8    CARROT 100% MELON 100% STRAW 100% WHEAT 97%
    zero dials    UNSOLVED  $120,047   MELON 12 WHEAT 130 STRAW 41 CARROT  8    CARROT 100% MELON 100% STRAW  98% WHEAT 95%
    m8            SOLVED    $121,887   MELON 20 WHEAT 125 STRAW 41 CARROT  8    CARROT  96% MELON 100% STRAW  96% WHEAT 96%
    m8            UNSOLVED  $115,261   MELON 20 WHEAT 113 STRAW 41 CARROT  8    CARROT  95% MELON 100% STRAW  98% WHEAT 93%
    c8            SOLVED    $132,902   MELON 12 WHEAT 125 STRAW 41 CARROT 16    CARROT  96% MELON 100% STRAW 100% WHEAT 96%
    c8            UNSOLVED  $117,482   MELON 12 WHEAT 124 STRAW 41 CARROT 16    CARROT  96% MELON 100% STRAW  97% WHEAT 92%
    s4            SOLVED    $127,232   MELON 12 WHEAT 135 STRAW 37 CARROT  8    CARROT  96% MELON 100% STRAW 100% WHEAT 96%
    fork0         SOLVED    $158,786   MELON 19 WHEAT 133 STRAW 33 CARROT  8    CARROT  91% MELON  99% STRAW  99% WHEAT 98%

**The shifted crop is collected at 96-100% with the routes kept.**
The dropped-stop worry does not show up: `m8` puts 8 more melon tiles in and collects 100% of them,
`c8` puts 8 more carrot tiles in and collects 96%.
Unsolving costs $6k-$15k a season on this seed and buys nothing measurable in collection.

So the search runs **solved**, which is also what ships.
`--unsolved` is kept as a flag with the measurement in its help text.

Single-seed money deltas here carry almost no causal signal — one animal moved a bank $22,785 on one
seed today — so the money column above is context, not evidence. The collection column is the
load-bearing part, and it is the same either way.

## Search design

    population 10 (+ baseline + incumbent, deduplicated -> 11 distinct evaluations per generation)
    elite      4
    generations 8
    seeds      9 per generation, redrawn every generation, none reused, none shared with the holdout
    field      shipped (frozen zero-dial agent), carrot_25, melon_heavy -- both seatings
    objective  Elo expected score, win + 0.5 * draw
    holdout    24 seeds never used in any generation, 144 games per row

Common random numbers: every candidate inside a generation is scored on the same seed set.
The seed set is redrawn every generation, and the 24 holdout seeds are partitioned out before the
first generation, so nothing the search saw can appear in the confirmation.

**The control.** The baseline is re-scored in every generation on that generation's own seeds, and
its duel column is the check: a frozen copy of the shipped agent playing itself should score about
0.5. It does not score *exactly* 0.5 — the two seats are not the same board, so identical policies
diverge — which is why the duel has genuine variance rather than being a certain draw.

**The resolution limit, stated up front.** 9 seeds x 2 seatings is 18 duel games per candidate, so
one game is 0.056 of the duel score and the sampling sd of a coin-flip duel is ~0.12. With 11
candidates a generation, the best of them sits ~1.5 sd above 0.5 on noise alone. This search can
only find large effects. The held-out draw, at 48 duel games, is the arbiter.

## Generation by generation

91 candidate evaluations, 4,914 games, 147.2 minutes.
`best` is the top vector of that generation on that generation's own 9 seeds; `baseline` is the
shipped agent re-scored on the same 9 seeds; `delta` is the margin between them.
One game is 0.019 of the elo score, so a delta of +0.019 is literally one game.

    gen  best vector                elo    baseline   delta    refit mu [fork m t c s g]
      0  fork1 m0 t0 c0 s0 g0     0.833     0.833    +0.000    [0.82 1.56 2.84 2.21 4.00 0.57]
      1  fork1 m0 t0 c0 s0 g0     0.833     0.833    +0.000    [0.94 1.52 2.62 2.56 4.65 0.20]
      2  fork1 m0 t0 c0 s0 g0     0.833     0.833    +0.000    [0.82 0.70 2.87 1.87 4.55 0.07]
      3  fork1 m1 t5 c4 s7 g0     0.852     0.833    +0.019    [0.94 1.22 2.47 1.96 3.71 0.02]
      4  fork1 m3 t0 c1 s4 g0     0.852     0.833    +0.019    [0.98 1.40 2.33 1.50 3.90 0.01]
      5  fork1 m0 t3 c0 s2 g0     0.833     0.833    +0.000    [0.99 1.30 1.30 0.69 2.83 0.00]
      6  fork1 m0 t3 c0 s2 g0     0.889     0.833    +0.056    [1.00 0.94 1.11 0.89 1.80 0.00]
      7  fork1 m4 t2 c5 s1 g0     0.870     0.833    +0.037    [1.00 1.14 1.04 1.45 1.28 0.00]

In three of eight generations **not one of the ten sampled candidates beat the shipped vector**, and
in the other five the winner was ahead by one to three games out of 54.
The distribution collapsed onto the shipped agent rather than away from it: `fork` went 0.5 -> 1.00,
`geese` went 0.7 -> 0.00, and the three shift dials went from a mean of 4/3/4 tiles to 1.1/1.0/1.5.

### What the 91 evaluations say about each dial

Marginal mean of the duel win rate, pooling every candidate the search ever scored.
These are marginals over a CEM's own non-random sample and the dials move together, so read them as
direction and size, not as clean single-dial effects.

    fork          n     mean duel win        geese       n     mean duel win
      0          17         0.085              0        68         0.350
      1          74         0.317              1        16         0.035
                                               2         6         0.083
                                               3         1         0.000

    melon         n     mean duel win        straw_off   n     mean duel win
      0          42         0.308              0        15         0.270
      1          14         0.337              1        12         0.431
      2           7         0.349              2        13         0.312
      3           9         0.216              3         4         0.306
      4           7         0.341              4         7         0.349
      5+         12         0.037              5+       40         0.199

**Geese lose, and they lose hard.** One goose takes the duel win rate from 0.350 to 0.035.
This is a re-measurement with the `SELLABLE` fix in place, so it is not the earlier verdict that was
an artifact of EGG being unsellable — the eggs reach the market now and the birds still lose.

**The melon fork should stay on.** Turning it off, which is the only way to reach Kawashigi's own
MELON 20 / STRAWBERRY 34, scores 0.085 against 0.317.

**Small shifts are neutral, large ones lose.** Melon is flat from 0 to 4 tiles and collapses at 5+;
strawberry removal is flat from 0 to 4 and drops at 5+.
Nothing in the 1-4 band separates from zero.

## Held-out confirmation

24 seeds drawn before generation 0 and never used in any of them.
144 games per row, 48 of them against the frozen shipped agent.

    config                    elo    duel win  duel elo    win     money      note
    fork1 m0 t0 c0 s0 g0    0.833     0.333     0.500     0.778   132,339    SHIPPED baseline (control)
    fork1 m1 t1 c1 s1 g0    0.840     0.521     0.521     0.840   131,396    best finalist
    fork1 m1 t0 c0 s1 g0    0.819     0.458     0.458     0.819   132,215
    fork1 m2 t1 c2 s1 g0    0.799     0.396     0.396     0.799   130,844
    fork1 m0 t3 c0 s2 g0    0.771     0.312     0.312     0.771   130,380    gen-6 best, +0.056 in-sample

    per-opponent
      fork1 m0 t0 c0 s0 g0   carrot_25 1.00/$155,430   melon_heavy 1.00/$149,129   shipped 0.33/$92,458
      fork1 m1 t1 c1 s1 g0   carrot_25 1.00/$155,228   melon_heavy 1.00/$147,131   shipped 0.52/$91,828
      fork1 m1 t0 c0 s1 g0   carrot_25 1.00/$155,561   melon_heavy 1.00/$148,022   shipped 0.46/$93,062
      fork1 m2 t1 c2 s1 g0   carrot_25 1.00/$154,594   melon_heavy 1.00/$146,641   shipped 0.40/$91,296
      fork1 m0 t3 c0 s2 g0   carrot_25 1.00/$153,064   melon_heavy 1.00/$146,125   shipped 0.31/$91,952

**The control is exact.** The baseline's duel is 16 wins, 16 draws, 16 losses out of 48 — an
expected score of 0.500 against a copy of itself. The `duel win` and `duel elo` columns differ only
for that row, because it is the only configuration that can draw the frozen agent at all.

**The winner's curse is visible in one line.** The gen-6 best was +0.056 on its own nine seeds and
comes last here at 0.312.

**The best finalist is one game.** `fork1 m1 t1 c1 s1 g0` scores 0.521 against 0.500 on 48 duel
games — 25 wins where 24 is the expectation. The sampling sd of a fair 48-game duel is 0.072, so
this is +0.3 sd. It also banks **$131,396 against the baseline's $132,339**, and it is the rounded
final CEM mean, which is to say the vector the search converged on is one tile of each crop away
from doing nothing.

Collection rates for that finalist, seed 3, against the frozen shipped agent
(`logs/collect_finalist.log`):

    dials [1,1,1,1,1,0]  bank $133,658 (opp $132,473)
      tiles      MELON 13  WHEAT 128  STRAWBERRY 40  CARROT 9  TOMATO 1
      collected  CARROT 100%  MELON 100%  STRAWBERRY 100%  TOMATO 100%  WHEAT 98%

Nothing here is a routing failure wearing a crop's name; every crop is collected at 98-100%.
The tiles move exactly as asked and the money does not follow.

## Verdict

The CEM found nothing.
Across 91 candidate evaluations and 4,914 games it never produced a vector that beats the shipped
allocation by more than noise, and on a held-out draw of 24 unseen seeds the best of them wins one
extra game in 48 while banking $943 less.
The correct read is that the shipped allocation — fork on, no crop shifts, no geese — is at a local
optimum that these six dials cannot improve on, and the search's own distribution agrees: it
collapsed onto the shipped vector rather than away from it, driving geese to zero and the fork to
one.
Two negatives inside that null are worth more than the null itself, because both were live
questions this morning: **geese cost about 0.3 of duel win rate per bird even now that EGG is
sellable**, and **turning the melon fork off — the only reachable route to Kawashigi's own MELON 20
/ STRAWBERRY 34, and the direction today's sweep pointed — is the single worst thing in the space at
0.085 against 0.317.**
The prior that motivated the search (melon up, strawberry down) does not survive contact with a
win-rate objective: it was measured on money, on 12 seeds, in the unsolved routing regime, and the
melon and strawberry dials are flat against the shipped agent right up to the point where they start
losing.
The honest caveat is resolution: 18 duel games per candidate can only find large effects, so this
run rules out a big win from these dials and says nothing about a $2,000 one.

### Two bugs found on the way, both of which invalidate earlier numbers

1. **Win rate against `pool.OPPONENTS` is saturated at 100%.** Any tuning result selected on pool
   win rate is selecting on a constant. This affects how `scripts/geese_pool_eval.py` should be
   read.
2. **Two candidate files in one process share one set of dials.** The `write_candidate` pattern in
   `scripts/geese_pool_eval.py` sets dials on the shared `kagg.search.schedule_agent` module, so
   whichever file loads second silently plays both seats. Any A/B run through that pattern with two
   dial-setting files in one process measured a mirror match. `scripts/cem_allocation.py` fixes it
   with a private module copy per candidate; the fix is not backported, and backporting it is a
   decision for whoever owns those scripts.

### Files

    scripts/cem_allocation.py                                        the search
    scripts/cem_collection.py                                        one game, per-crop collection rates
    scripts/cem_probe.py                                             timing and discrimination probes
    tests/test_the_allocation_dials_reach_the_tiles_they_claim.py    13 tests, the bounds
    tests/test_two_candidate_files_do_not_share_one_set_of_dials.py   4 tests, the shared-module bug

Nothing in `kagg/` was changed. This was an experiment; the deliverable is the measurement and the
scripts.
