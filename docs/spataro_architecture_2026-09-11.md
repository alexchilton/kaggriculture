# What SpaTaro is, and the agent it implies

Measured 2026-09-11 from 62 SpaTaro seasons in `data/replays_2026-09-07/08/09`, against
109 Hayashi seasons in `data/replays_hayashi` as the tape baseline.
SpaTaro is rank 1 at 3130.8; Hayashi, the only tape-based agent in the top 34, is 34th at 2879.2.

## 1. He is a recipe, not a tape — and not a fresh plan either

Two instruments disagree, and the per-turn one is the wrong one.

    per-turn action strings   676-707 of 719 turns differ between any two seasons
    realised board, d0-d6     within-world variance 1 planted tile, 0 animals
    day-6 geometry            10 tiles invariant across 62/62 seasons

Counting action strings counts quantity jitter and discarded orders as strategy.
**20.5% of his market order slots are malformed** — `BUY_PRODUCT` of TOMATO, CARROT,
STRAWBERRY, MELON, none of which the engine sells (only WHEAT and FERTILIZER are
buyable). They cost nothing: he hits the 10-order cap on 1.6% of turns and submits
no orders at all on 41.9%.
Strip those and drop quantities and the turn-0 opening is **3 distinct op sequences per
seat**, one covering 28 of 37 games — not the 21 "variants" a raw diff reports.

## 2. The invariant opening geometry

Board at day 6, step 144, 62 seasons. Tile is `(y, x)`.

| tile | content | share | placed/planted |
|---|---|---:|---|
| (3,3) | SHEEP | 62/62 | d0 |
| (4,2) | SHEEP | 62/62 | d0 |
| (4,3) | COW | 62/62 | d0 |
| (4,4) | COW | 62/62 | d0 |
| (1,3) | MELON | 62/62 | d0 |
| (2,3) | MELON | 62/62 | d0 |
| (3,4) | MELON | 60/62 | d0 |
| (1,2) | MELON | 57/58 | d0 |
| (4,0) | MELON | 59/61 | d0 |
| (0,2) | MELON | 50/53 | d0 |
| (2,4) | COW | 53/62 | d4 |
| (4,1) | COW | 35/61 | d5 |
| (2,2) | MELON | 59/59 | d3 |
| (3,1) | COW | 43/59 | d3 |

25 tiles are ever used. The outer ring — (0,1), (1,1), (3,0), (2,1) — is where the
variation lives.

**This is the part `schedule_agent` cannot express.** Its schedule is "counts per day,
no tile coordinates"; `plant_tiles` exists in `scripts/build_schedule.py`'s row template
but `schedule_agent` never reads it, and its own comments at lines 853 and 883 record
that `build_tiles` contradicts the board. Geometry has to come from an authored opening
or from new coordinate support in the planner.

## 3. The day targets

`data/spataro_targets.json` — median and quartiles per day, per latch.
Days 0-6 are identical for both branches, so one opening serves both.

    day 1   COW 2 [2-2]   SHEEP 2 [2-2]   MELON 8 [7-9]    WHEAT 7 [6-7]   planted 16
    day 3   COW 2 [2-2]   SHEEP 2 [2-2]   MELON 10 [9-11]  WHEAT 4 [3-5]
    day 6   COW 4 [2-4]   SHEEP 3 [2-5]   MELON 12 [10-13]

## 4a. CORRECTION — the world is NOT a function of the seed

Asserted earlier in this session and **wrong**. Shops unlock on town demand satisfied by
BOTH farms, so our own selling moves them. One seed, one opponent, four agents:

    seed 11        world at step 144
    hay_router     FARMERS_MARKET|YARN_STORE
    spa_router     PIZZA_SHOP|SMOOTHIE_SHOP
    twocoins       PIZZA_SHOP|BAKERY
    shop0908       PIZZA_SHOP|BAKERY

The test that produced the wrong claim varied opponent and seat but held the AGENT fixed,
and the three tapes it did vary share turns 0-143 by construction, so it could not have
detected this.

What this invalidates:

- `data/logs/seed_worlds.csv` (900 seeds) is a seed->world table **for hay_pick only**,
  not in general.
- `scripts/tape_grid2.py`'s 13,312 games allocated seeds by world on that premise. The
  per-tape margins stand; the claim that a seed names a world does not.
- A world-keyed router over SpaTaro's tapes is **circular**: it keys on a town its own
  tape choice creates. That is the mechanism behind §8a.

## 4. The latch: one binary read of the town

    YARN_STORE in the first two shops    peak sheep  10 [2-22]
    no yarn store                        peak sheep   2 [2- 4]

First shop unlocks d3, second d6, third d9 or d12, in all 62 seasons. The base holds
through d6 and splits at d7: yarn goes sheep and holds strawberry back, non-yarn goes
strawberry and more cows.

**No opponent read found anywhere.** His peak herd against the opponent's herd at day 6
is **+0.09**. Peak-against-peak is +0.68 inside yarn towns, which is two agents scaling
to the same town. Mid-season planting residual against ~60 opponent and board features,
at n=62: top |r| 0.28, which is noise at that n. The opponent reaches him only through
shared prices.

## 5. The exit rule

    WOOL price peak in season   217-242 (p50 217)
    WOOL price at cull start    1-233   (p50 11)
    cull start day              18-28   (p50 26)
    sheep herd falls >= 2       50 of 62 seasons

When wool is on the floor he stops feeding. Two unfed days and the animal escapes
(`_daily_refresh_animals`, `consecutive_unfed >= 2`), leaving the structure; `DIG`
cannot remove a placed animal, so starvation is the only exit. FEED ops fall 25/day
to 3/day over the window while 10-11 sheep sit unfed at midnight.
The freed worker-turns go to **carrot and wheat** — crop mix moves from
`{STRAWBERRY 34, WHEAT 26}` at d20 to `{CARROT 25, WHEAT 34}` at d25. Carrot is the
three-day crop, the only one that still matures before turn 719.
Empty pasture is NOT left idle: it rises then falls in 61 of 62 seasons.

## 5a. How long one of his tapes stays valid

14 of his seasons, each replayed on ITS OWN SEED against shop0909, comparing the unlock
sequence to his recording. A replay is fully deterministic -- in BOTH players' actions. We
supply one, so it is a different game.

    unlocks matched before diverging   [0,0,1,1,1,1,1,1,2,2,2,3,3,5]
    tape valid to day                  min 3,  p50 9,  max 30
    bank, replay vs his own            mean -14,331,  better in 4/14

**Median validity is day 9; two of fourteen diverge before the first shop opens; one
survives the season.** The seam is therefore not a constant -- it has to be detected live
by watching the unlock sequence against the tape's own, and handing over the turn it
differs.

Replayed tapes are not simply degraded: two beat his own recording by +6,745 and +9,551.

## 6. Compute

8-9 seconds burned on the **first action**, then never over the per-turn budget again
for 718 turns (`remainingOverageTime` 60 -> 50.5-52.4, one drop at t1).
Mengfei Li, rank 11, is the other architecture: nothing up front, then a re-solve every
24 steps from day 12. Otter Vibe, ymg_aq, binghua and Hayashi spend **zero** overage.

## 7. The agent this implies

    turns   0-167   authored opening, hitting the §2 geometry and §3 targets
    turn    168     latch on YARN_STORE in the first two shops
                      -> sheep branch
                      -> strawberry branch
    turns 168-600   planner against the §3 day targets for that branch
    turn   ~600+    exit rule: wool below ~20 -> stop feeding, plant carrot + wheat
    throughout      the E184 market layer, unchanged

Flows for the planner are extracted per branch in
`data/spataro_schedule_{yarn,non_yarn}.json` (`scripts/spataro_schedule.py`), in
`schedule_agent`'s own row format: `plants`, `animals_bought`, `hires`, `hands`, `land`,
`seeds`, `buys`, `sells`.

### The market layer is not optional

Keep E184 (`submission/twocoins`, `sale_horizon=2`): sales that can already be filled
are brought forward over a two-action window from day 12 step 288, with a per-due-step
reservation so an advanced sale is not counted twice. Measured +948 mean margin against
v32, 20/20, and the horizon sweep reproduces the author's choice (h1 +428, h2 +948,
h3 +846).
Two standing market constraints from `docs/REGISTER.md`, neither to be relitigated:
exiting a flooded milk/wool book **gifts the opponent ~$9-10k of price suppression** —
our own gate reproduced it at -$11,822/season and +$6,130 to them, so the fix is release
timing inside the book, not exit from it. And `buy_product` is not a bug: the measured
winner drew the bulk of revenue from milk and wool by converting **bought** wheat into
animal products.

## 8. What is measured and what is not

Measured: everything in §1-§6, and that `submission/hay_router` (E184 chassis, Hayashi's
13 recovered live tapes) beats the published tapes by **+61,054 mean margin, 880/880
paired cells**, on held-out seeds and held-out opponents.

## 8a. Measured nulls from this session -- do not redo

- **`submission/spa_router`** -- his seasons as a world-keyed library in the E184 chassis,
  all 40 worlds he has played given their own tape (the chassis's "exactly 13" assert
  relaxed). **-112,790 against hay_router, 0/16; -41,778 against twocoins, 0/16.** Cause
  is §4a: his tapes unlock a different town than the router is keyed on.
- **Verbatim splice of his turns 0-167 onto Hayashi's tapes** -- **-167,577, 0/16.**
- **A hand-written executor for days 0-6** (`kagg/search/spa_opening.py`) reproducing his
  geometry rather than his turns. Five iterations, each fix breaking a different two-strike
  constraint: plant without watering lost the field by day 1; water first left MELON 4 of
  11; buying the d3-d5 cows starved the herd; gating the herd on feed fixed the herd and
  left the crops short; planting before fertilizer fixed the crops and lost the herd. The
  tape satisfies all of these at once for free. **This is the argument for a tape base.**
- **De-jittering his day-blocks to find repeats.** All 62 blocks stay distinct on every one
  of the 30 days even after dropping malformed orders, dropping quantities, sorting hands
  and dropping movement (`scripts/dejitter_blocks.py`). There is no exact-match block
  library to build; matching has to be approximate.

## 8b. What worked

**`submission/spa_blocks`** -- his day-blocks selected by nearest board at dawn
(`data/spataro_blocks.json`, 1,860 blocks with board signatures; threshold `SPA_MAX_DIST`).
It splices **days 0-8** and reproduces his opening: at day 6, `{MELON 8, STRAWBERRY 3,
WHEAT 2}` and `{COW 5, SHEEP 2}` against targets of MELON 11 [11-12], COW 4 [4-5],
SHEEP 2 [2-3]. From day 9 no block is within range and it falls back -- the same day-9
boundary §5a finds independently. Its fallback is PASS, deliberately, to isolate the
splice; that is why the season ends at $945 and says nothing about the design.

Note on library size: going from 12 routed worlds to 40 changed nothing, and the block
splicer already chooses from all 62 seasons. **Coverage is not what limits the horizon** --
the opponent moving the unlocks is. More tapes will not push day 9 later; keying the
library on the unlock sequence SO FAR rather than on the world might.

## 8d. The planner's execution rate is the biggest lever, and it is Alex's standing note

`schedule_agent`'s own docstring records, measured against the tape's own schedule, ops
EMITTED against ops that actually LANDED:

                        ours emit/land    tape emit/land
    CARE                     312 / 150         308 / 308
    FEED                     312 / 142         319 / 319
    WATER                    766 / 455         851 / 846
    COLLECT_FERTILIZER       297 / 143         318 / 318
    HARVEST                  286 / 149         338 / 337

**48% against ~100% -- and MEASURED HISTORICAL 2026-09-11.** The eight bugs the same
docstring describes fixing were the whole of it. Current rates, seed 11 against shop0909:

    op        planner emit/land  rate    hay_router emit/land  rate
    WATER         906 / 845      0.93        1100 / 1016       0.92
    FEED          321 / 317      0.99         367 /  366       1.00

The executor is as reliable as a tape. The gap is the PLAN: the planner does ~80% of the
tape's volume on every axis (WATER 906 vs 1100, PLANT 183 vs 239, CARE 318 vs 397,
COLLECT_FERTILIZER 306 vs 385) and banks 37,142 against 135,963 on that seed, because its
schedule is カワシギ's, built in August on engine 1.32.6.

    arm              win   mean bank  mean margin   (8 seeds, both seats, vs shop0909)
    hay_router      1.00     139,701      +76,011
    twocoins        1.00     103,992       +4,999
    planner_pure    0.00      72,404      -30,098    0/16 vs either

So a stale plan executed well, not a good plan executed badly. **Swapping the schedule is
the job.** Build with `PYTHONPATH=. .venv-sub/bin/python scripts/build_planner_submission.py
--replay-days N`; the planner is driven every turn through the replayed opening so its pins
and pen reservations are warm at the handover.

This is why the tape runs as long as it is valid and the schedule only takes over when the
tape would be aimed at a board that no longer exists. Not because the schedule is better --
it is derived from the tape and can do nothing the tape did not -- but because it survives a
board the tape did not expect.

## 8c. Not measured, and the live risks:

- **The join.** A verbatim splice of SpaTaro's turns 0-167 onto Hayashi's tapes scored
  **-167,577, 0/16** — it runs clean and plays a ruined season, because Hayashi's
  turn-168-onward expects the farm his own opening built. An authored opening that hits
  the §2 geometry is a different thing from that splice, but the join is where this dies
  if it dies. `REPLAY_OPENING_DAYS` is recorded as dead for the same reason: a recording
  driving machinery built for someone else silently overrode the herd rule, 620 of 1187
  placements.
- **Herd size inside a yarn town still runs 2 to 22** and nothing measured says how big.
- A residual of +/-2 to 6 planted tiles after the full unlock schedule, no readable driver.
- Why 8-9 seconds at turn 1 produces what it produces.
- Every arm measured today wins 1.00 against every local opponent, so all margins here
  are **bank margins**, and bank margin has not been shown to predict ladder rating.
  Local `twocoins` beats the 2700-rated 0909 artifact 32/32, which cannot be reconciled
  with twocoins sitting at 2663.9 itself.

## §9 The collapse test, on 179 seasons of ONE submission

The earlier 62-season set mixed submissions and was thrown away.
`data/replays_spa_sub` now holds 162 replays of submission 56114097 (4.9 GB), which with the daily dumps gives **179 seasons of his current agent**.
Banks: min $59,417, p50 $102,438, max $169,037.

`scripts/spataro_schedules_from_sub.py` asked the question his "couple of base tapes" deserved, at count granularity — tiles, hands, order-within-turn and decoy quantities all thrown away:

```
 days     full plan    field only   herd + land   plants only
    1     179 (  1)     123 (  6)       4 (125)      76 ( 11)
    3     179 (  1)     178 (  2)      37 ( 63)     169 (  2)
    5     179 (  1)     179 (  1)     130 ( 10)     179 (  1)
    7     179 (  1)     179 (  1)     178 (  2)     179 (  1)
    9     179 (  1)     179 (  1)     179 (  1)     179 (  1)
```

**He has no base schedule.** Past day 3 every season is a distinct plan even on counts alone.
That kills the "6 spliced tapes" shape as stated: there is nothing to splice at whole-plan granularity, on any day past 3.

### What IS invariant, and it is the useful half

Field-by-field, the same 179 seasons split cleanly into a structure that repeats and volumes that do not:

| | day 0 | day 3 | day 5 | day 7 |
|---|---|---|---|---|
| `places` | 2 (178) | 4 (151) | 15 (122) | 55 (37) |
| `animals_bought` | 2 (178) | 20 (107) | 70 (35) | 149 (7) |
| `builds` | 3 (101) | 8 (80) | 40 (30) | 126 (7) |
| `land` | 3 (126) | 9 (98) | 24 (46) | 69 (19) |
| `plants` | 76 (11) | 169 (2) | 179 (1) | 179 (1) |
| `seeds` | 104 (13) | 171 (4) | 179 (1) | 179 (1) |
| `buys` | 41 (17) | 177 (3) | 179 (1) | 179 (1) |
| `sells` | 32 (26) | 176 (2) | 179 (1) | 179 (1) |

(distinct plans over days 0..N, largest group in brackets.)

His **structure** is one plan. His **volumes** are a continuous function of money and prices, unique in every season from day 4.

Re-measured with `places` as the ANIMAL SEQUENCE rather than a count — `PLACE` in the engine (`reference/kaggriculture.py:377`) is overloaded and also drops produce in the shed, so counting every `PLACE` counts loading trips as herd placements, and the first pass did:

```
 days   distinct     top  cover   top sequence
    1          3     170    95%   CCSS
    3          3     149    83%   CCSS
    4          6     134    75%   CCSSC
    5         10     128    72%   CCSSCC
    6         15      58    32%   CCSSCC
    9         41      28    16%   CCSSCCCCC
```

**One base skeleton covers days 0–5 in 128 of 179 seasons (72%), and days 0–3 in 170 of 179 (95%).**
It breaks at day 6 and reaches the same day-9 wall already found three independent ways (§6, the block splicer's fallback, the unlock-prefix collapse from 82.1% to 11.2%).

So the architecture is not tape-then-splice-then-planner. It is:

- **base plan owns** `places` `animals_bought` `builds` `land` — the geometry, d0–d5, one plan, 72% of his games
- **planner owns** `plants` `seeds` `buys` `sells` `hires` — the volumes, every day, because there is no plan there to copy

`hires` sits with the volumes: it is 5 distinct on day 0 alone and 87 by day 7, because he hires against whatever money is in the bank.

### The first artifact on his plan

`data/seed_scripts/spataro/schedule.json` — episode 107068412 of submission 56114097, $157,032, his best bank among the **58 seasons that run the majority d0–d5 skeleton**.
Picking his single best season would have taken 107020377 at $169,037 off a skeleton he plays in a minority of games.
Extracted by `scripts/spataro_plan_rows.py` into `data/spataro_plan_rows.json` (6.2 MB, 179 seasons in planner-row format); registered as `PLANS["spataro"]` in `kagg/plan.py`.

His day 0–9, in the planner's own row format:

```
d hands land builds places plants  seeds                      buys        sells
0   6     0     6    CCSS    13    MELON 14 WHEAT 3            WHEAT 31    WHEAT 14
1   6     0     0     -       3    MELON 1 WHEAT 4             WHEAT 44    WHEAT 5
2   6     0     0     -       0    -                           WHEAT 21    FERT 4 WHEAT 4
3   6     1     0    C        1    STRAW 4 WHEAT 2             WHEAT 4     FERT 4 WHEAT 8
4   6     0     1    C        5    STRAW 3                     WHEAT 13    FERT 7 WHEAT 6
5   6     0     0     -       0    -                           WHEAT 20    FERT 2 WHEAT 2
6   8     2     4    C       18    STRAW 15 WHEAT 6            WHEAT 13    FERT 6 WOOL 14 WHEAT 4
7   7     0     2    C        2    STRAW 6                     WHEAT 24    FERT 9 WHEAT 4
8   9     0     1    CCC      7    STRAW 8 WHEAT 2             WHEAT 16    FERT 5 MILK 12 WHEAT 4
9   9     0     0    CCC      0    WHEAT 1                     WHEAT 55    FERT 10 WHEAT 31 WOOL 8
```

Two things in that table are the two-coins market lesson made visible: he **buys wheat every single day**, 31/44/21/4/13/20/13/24/16/55, and he re-hires a fresh crew every dawn rather than holding one.
Wheat in, milk and wool out — the 83% of revenue in REGISTER OPEN-3.

`scripts/build_planner_submission.py` gained `--schedule` (a name in `PLANS` or a path), which rebinds the module-level `PLAN` that both `build()` and `reproduce()` read, so the artifact and the dollar-equality gate stay on the same plan.

## §10 The day-12 board, and the three layers Alex named

Alex, 2026-09-11: *"there will need to be some base tapes then base schedules then some jiggery pokery with fill the gaps with wheat or carrot or sheep till cant do any more then let the sheep die off partly when the market crashes etc."*
*"it will need to be slightly more fluid than the standard tape or schedule."*
*"but try and match it to around d12 or so as the first effort."*

§9's field split maps onto those three layers exactly:

| layer | fields | evidence it belongs there |
|---|---|---|
| base tape, d0–5 | `places` `animals_bought` `builds` `land` | one skeleton in 128/179 seasons (72%), 170/179 through d3 |
| base schedule, d6–29 | the per-day row as a starting sheet | breaks as a plan past d3, works as a target |
| fluid rule, every day | `plants` `seeds` `buys` `sells` `hires` | 179 distinct in every one of those fields from d4 |

**The cull is a FEED rule, not a sell rule.** `DIG` cannot remove a placed animal; `consecutive_unfed >= 2` escapes it and leaves the structure (`reference/kaggriculture.py:817`).
So "let the sheep die off partly" is the planner withholding `feeds` from N of M pens for two days, and the freed worker-turns are what pay for the wheat-and-carrot refill.

### The target, measured

`scripts/spataro_state_targets.py` → `data/spataro_state.json`, his BOARD at dawn over 179 seasons.
State, not flows, because `animals_bought` is 70 distinct plans by d5 while the placement sequence is 10 — arriving at the same herd on different purchase dates IS a match; copying his dates and arriving elsewhere is not.

```
dawn of day 12        p25       p50       p75
  money            11,108    12,737    15,080
  owned                75        75        75
  planted              56        61        64
  animals_total        10        14        17
  empty_struct          0         0         0
  COW                   5         7        11
  SHEEP                 2         3        10
  WHEAT                24        30        36
  STRAWBERRY           18        25        29
  MELON                 1         1         2
  CARROT                0         0         0
```

Three things in that sheet change what the first effort has to build:

1. **No cull logic is needed for d12.** `empty_struct` p50 is 0 at d12 and 1 at d9 — nothing has starved yet. His cull is day p50 26.
2. **Melon is an opening crop, cleared by d12.** 11 melons at dawn of d9, 1 at d12, while wheat goes 12 → 30. The melon money funds the board and then the tiles are turned over.
3. **Carrot is a LATE crop.** 0 at d12, 0 at d15 p50 (p75 12), and it is what the cull's freed worker-turns go into. "Fill the gaps with wheat or carrot" is two different phases: wheat before the cull, carrot after.

And the land is not optional: `owned` is 75 at p25 as well as p50, so he is on three quadrants by d12 in more than three-quarters of his games, having bought his first parcel on d3.

`scripts/match_d12.py` scores any artifact against this sheet — ours at p50 against his p25/p50/p75, per axis, per day, counting axes inside his interquartile range, with both sides read by the same `board()` function so the two cannot drift apart by definition-shift. That is how the first `places` count came to include shed drops.

## §11 The first artifact, measured — and the extraction bug it exposed

`submission/planner_spa/main.py`, the covering planner on `PLANS["spataro"]`.
Built by `PYTHONPATH=. scripts/build_planner_submission.py --schedule spataro --replay-days 0`; all six gates pass, `submission verified`, W2 D8 L2 over 12 games against the repo agent on the same plan (the packaging gate, which two identical agents should draw), 50.5s projected overage at 6x against a 60s bank.

Paired against the planner on カワシギ's plan, 16 cells (8 seeds x 2 seats) vs shop0909:

```
dawn of day 12     planner_spa   planner_kawa     his p25/p50/p75
  money                 7,316         7,702    11,108 12,737 15,080
  owned                    75            75        75     75     75   IN
  planted                  52            53        56     61     64
  animals_total            14            14        10     14     17   IN
  empty_struct              0             0         0      0      0   IN
  COW                       9             8         5      7     11   IN
  SHEEP                     5             6         2      3     10   IN
  WHEAT                    15            16        24     30     36
  STRAWBERRY               36            36        18     25     29
  MELON                     0             0         1      1      2
  -> axes inside his IQR   6/11          6/11
mean bank                77,907        72,404
```

+$5,503 for his plan, and the boards are one tile and $400 apart.
Same six axes in, same five out, same direction — under two plans whose `plants`, `buys` and `hires` rows share nothing.

**That is NOT the planner ignoring its plan.** `scripts/plan_vs_landed.py` puts the row asked next to what landed, on seed 11:

```
                   kawashigi: asked/landed        spataro: asked/landed
  hires      5/5 0/0 4/4 5/5 5/5 4/4 4/4 8/8     6/5 6/0 6/4 6/5 6/5 6/4 8/4 7/8
  land       d6 1/1, d11 1/1                     d3 1/0, d6 2/1, d10 1/0
  builds     4/4 0/0 1/1 0/0 1/1 0/0 2/2 2/2     6/4 0/0 0/1 0/0 1/1 0/0 4/2 2/2
  places     SCSC/SCSC  C/C  C/C  SCC/SCC        CCSS/SCSC  C/C  C/-(d4)  -/C(d5)
```

カワシギ's plan is followed to the letter on every axis for thirteen days.
SpaTaro's is not, and the reason is that I extracted what he ORDERED:

- **`land` is an over-request in 162 of 179 seasons.** 107068412 submits four `BUY_LAND` (d3, d6 x2, d10) and funds two; its board is 25 tiles until d7. A planner handed `land: 2` on d6 reserves money and seats routes for ground it will never own.
- **`hires` is his crew against HIS bank.** `6` on d1 and d2 is unaffordable from our opening, so 0 and 4 land.

So the schedule has to be built from what LANDED. `scripts/spataro_landed_schedule.py` derives every field the planner treats as a commitment from the board changing turn to turn — `land` from `farm["unlocked_quadrants"]`, `hires` from the engine's own `farm["hires_today"]`, `builds`/`places`/`plants`/`escapes` from tiles changing state.
`seeds`, `buys` and `sells` stay as requested on purpose: the planner clamps them with the engine's own rule (`n = min(have, row["sells"][prod])`, `schedule_agent.py:5111`), so an over-ask there is a no-op on both sides rather than an orphaned route.

Seed 11 alone, for scale on how much the plan matters once it IS deliverable: planner_spa $88,842, planner_kawa $37,142.
