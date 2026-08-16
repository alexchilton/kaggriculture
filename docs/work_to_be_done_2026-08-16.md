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
