# CEM over the crop and herd allocation dials, 2026-08-15

**Status: RESULT PENDING — this file is written as the run completes. See the verdict at the bottom.**

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

RESULTS PENDING

## Held-out confirmation

RESULTS PENDING

## Verdict

RESULTS PENDING
