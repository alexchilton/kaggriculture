# The measured economics

Filename kept because `CLAUDE.md` and `kagg/agents/heuristic.py` point at it.
It started as the answer to verification question 5 and is now the whole measured economics of the
game: yields, drain, allocation, and selling into a shared book.

Every number here came from a measurement, and each one names what produced it.
`kagg/economics/` is validated against live episodes step for step and product for product in
`tests/test_market_model.py`; `tests/test_production.py` re-measures the yield table on every run.

> **Version caveat, added 2026-08-09.** §1 (yields) and §3-5 (supply, allocation, storage) are
> version-independent — they come from per-tile production rules and `MARKET_PARAMS`, neither of
> which changed in 1.32.6. **§2 (town drain) and the market-ceiling table in §4 were measured before
> the 1.32.6 town rebalance and are now wrong by up to 4.67x (melon)** — `townCenterSellInterval`
> doubled from 12 to 24 and the late-season demand ramp was deleted. Use
> `docs/the_market_2026-08-09.md` §2 for the corrected 1.32.6 drain table, and
> `docs/what_saturates_and_what_does_not_2026-08-09.md` for the corrected per-head animal
> saturation and the melon-planning bug the old §2/§4 numbers caused.
>
> **2026-08-11 addendum.** `docs/what_the_town_will_actually_eat.md` supersedes §2/§4 again, this
> time with a direct measurement off 87 tapes' closing inventory rather than a computed table.

---

## 1. Yields — the table in the competition docs is wrong

`_daily_refresh_plants` stops producing once `production_count > max_yield`, so an **ongoing** crop
tile yields `max_yield` units for its *entire life* and then dies. The Object Types
"Max yield / tile / DAY" column is a lifetime total, not a rate.

Measured season output from one tile, optimal single-farmer play, no fertilizer:

| Crop | doc claimed /tile/day | measured /tile/season | measured /tile/day | doc overstated by |
|---|---|---|---|---|
| Wheat | 1.5 | 28 | 0.93 | 1.6x |
| Carrot | 1.333 | 29 | 0.97 | 1.4x |
| Tomato | 4.0 | 8 | 0.27 | **15x** |
| Strawberry | 2.0 | 6 | 0.20 | **10x** |
| Melon | 0.5 | 12 | 0.40 | 1.25x |
| Egg | 2.0 | 26 | 0.87 | 2.3x |
| Milk | 1.0 | 11 | 0.37 | 2.7x |
| Wool | 0.67 | 8 | 0.27 | 2.5x |

The error ran in exactly the direction that made premium crops look like the prize, and it cost a
day-1 wrong turn. Animals are the exception in the other direction: no `production_count` cap, so a
goose yields 26 eggs a season against a `max_held` of 4.

Fertilizer doubles ongoing-crop output (tomato 8→16, strawberry 6→12) and lifts wheat 28→42.
Buying it at $100 does not pay; **collecting it free from animals does** — `COLLECT_FERTILIZER`
costs one action, once per animal per day, and is worth ~$85.

---

## 2. Town drain — fixed, large, and randomly scheduled

Nothing either player does changes the drain. Measured over a full season (seed 11; totals move
only a few percent across seeds):

| Product | Shops | Season drain | Price at zero player sales | x base |
|---|---|---|---|---|
| Wheat | 5 | 662 | $51 | 2.04x |
| Carrot | 2 | 410 | $42 | 1.20x |
| Tomato | 2 | 410 | $109 | 1.82x |
| Strawberry | 4 | 536 | $314 | 2.62x |
| Melon | **0** | 140 | $293 | 1.17x |
| Egg | 2 | 320 | $69 | 1.38x |
| Milk | 3 | 446 | $344 | 2.15x |
| Wool | 1 | 320 | $250 | 1.25x |

**Melon appears in no shop.** Its only consumer is the town centre, so its drain is the smallest,
is exactly 140 on every seed, and never grows.

### The drain does not exist from day 0, and this is the largest correction to the model

Eight shops open on days 3, 6, 9 … 24, and **which shop lands on which day is drawn per game**
(`jax_sim.random_unlock_days`):

```
seed 0: [18, 21,  3,  9,  6, 15, 12, 24]
seed 1: [ 6,  9, 15, 21, 12,  3, 18, 24]
seed 2: [21, 24, 12, 15, 18,  6,  3,  9]
```

A product has no shop demand at all until one of its shops opens, so shop count is a **risk**
measure and the objective is market size **times robustness**.
`scheduler.expected_first_demand_day` computes the wait exactly, as the minimum of `k` draws
without replacement: wheat 4.5 days, strawberry 5.4, milk 6.8, **wool 13.5**.
Wool is a $56,800 market served by one shop that can open on day 24; a sheep bought early is money
asleep, which is why the leader under-commits to it.

**The opponent sells into the same inventory**, so every drain above is roughly halved in a
contested game.

---

## 3. Supply — one quadrant against that drain

25 tiles is the free NW quadrant, i.e. the commitment available without buying land.

| Crop | units/tile | 25 tiles | drain | supply/drain | tiles to saturate |
|---|---|---|---|---|---|
| Wheat | 28 | 700 | 662 | 1.06x | 23.6 |
| Carrot | 29 | 725 | 410 | 1.77x | 14.1 |
| Tomato | 8 | 200 | 410 | **0.49x** | 51.2 |
| Strawberry | 6 | 150 | 536 | **0.28x** | 89.3 |
| Melon | 12 | 300 | 140 | 2.14x | 11.7 |
| Egg | 26 | 650 | 320 | 2.03x | 12.3 |
| Milk | 11 | 275 | 446 | **0.62x** | 40.5 |
| Wool | 8 | 200 | 320 | **0.62x** | 40.0 |

Strawberry needs 89 tiles to saturate town demand — three and a half quadrants and $8,933 of seed
against a $3,000 start. Tomato needs 51 tiles, milk 40 cows, wool 40 sheep.
**None of these is reachable, which is precisely why their prices hold.**
Wheat, carrot, melon and egg *can* be oversupplied by a single quadrant; those are the goods where
dumping discipline matters.

---

## 4. The allocation is arithmetic, not search

`scripts/allocation_calculator.py` computes the target allocation from `chains.DRAIN_UNITS` and
`economics/production.py` with no fitted constants. Fill each market to its drain, ranked by
revenue per unit-day:

```
     product   base   drain      market $
        MILK    160     500        78,432   <- the biggest market in the game
  STRAWBERRY    120     572        66,586
        WOOL    200     284        56,736
       MELON    250     140        35,000
      TOMATO     60     374        21,574
         EGG     50     338        16,582
       WHEAT     25     662        15,986   <- seventh of eight
      CARROT     35     338        11,484
       TOTAL                      302,380
```

Divide each drain by per-season yield and you recover the leader's farm without searching anything:

| | computed | leader runs |
|---|---|---|
| cows | 500 / 66 = **7.6** | **8** |
| sheep | 284 / 48 = **5.9** | **6** |
| geese | worst pen, smallest market | **0** |
| strawberry | 572 / 12 = **47.7 tiles** | **41** |
| melon | 140 / 12 = **11.7 tiles** | **20** |

**Why this was invisible until 2026-08-05:** `DRAIN_UNITS` held the five crops only, so **$151,750
of demand — including milk, the largest single market — was missing from every allocation argument
this project made.** The numbers were sitting in `data/logs/market_ceiling.log` the whole time.

The one thing the calculator gets badly wrong is **wheat**: it computes 0 tiles against the
leader's 40, because wheat is an **input**. Fourteen pens eat ~420 units a season ($10,500 of feed)
and wheat is the only crop returning cash by day 3. A revenue ranking scores it last.

---

## 5. Storage caps the timing prize

There is **no long-term storage**. 100 items overnight, overflow destroyed; carried inventory is
uncapped during a day but emptied every night; an ongoing tile holds at most `max_yield` for about a
day before decay. All pinned in `tests/test_storage.py`.

Comparing an even daily drip against the latest schedule storage actually permits:

| Crop | qty | drip $/unit | deferred $/unit | gain | forced out early | held to end |
|---|---|---|---|---|---|---|
| Wheat | 700 | 21.7 | 27.4 | 1.26x | 600 | 100 |
| Carrot | 725 | 19.6 | 22.4 | 1.14x | 575 | 150 |
| Tomato | 200 | 77.1 | 90.1 | 1.17x | 100 | 100 |
| Strawberry | 150 | 257.2 | 300.3 | 1.17x | **0** | 150 |
| Melon | 300 | 175.5 | 203.2 | 1.16x | 200 | 100 |

The mechanism is real — town drain runs whether or not anyone sells, so an untouched market drifts
into scarcity — but the gain is a **uniform 1.14x-1.26x**, not the 1.5-1.75x an unlimited-storage
model suggests.

> **Correction on the record.** An earlier version claimed 1.75x for wheat and called wheat the
> biggest timing win. That was computed with a schedule holding 700 units, which no shed can do.
> Wheat's real gain is 1.26x and it is the crop *most* forced into drip selling.

**The lever is production timing, not sale timing.** A crop that matures in the last week needs no
storage at all — strawberry shows it cleanly, with its 150 units arriving on days 16 and 29 only.

---

## 6. Selling into a shared book

`market_price(item, inventory)` is a pure function of the shared book
(`reference/kaggriculture.py:177`). `MARKET_PARAMS` is a module constant and `_new_market` writes a
`params` key **only when the params are non-default**; a live game's observation carries `market`
with keys `['inventory', 'prices']` and no `params`, so the competition runs the defaults and
**we know the curve exactly**. Given `obs["market"]["inventory"]` we can compute what every
successive unit of a SELL will fetch before ordering it.

Above `I0` (10,000) the curve is brutally shallow for exactly the products we live on:

| units above I0 | 0 | +20 | +50 | +100 |
|---|---|---|---|---|
| MILK | 160 | 118 | 55 | 1 |
| WOOL | 200 | 177 | 55 | 1 |
| STRAWBERRY | 120 | 82 | 24 | 1 |
| MELON | 250 | 246 | 225 | 150 |

Both seats add to the same inventory, so an opponent selling what we sell taxes us without ever
touching our farm. Measured on two of our own leaderboard games:

| game | opponent | our units sold | milk price d15-29 | final |
|---|---|---|---|---|
| 90534961 | Sophie | 1058 | 101.1 | $103,367 **lost** |
| 90536513 | Mohit Babel | 1017 | 225.1 | $128,735 **won** |

We sold **more** units in the game we lost. Milk alone — ~135 units at ~$124/unit worse — is ~$16.7k
of the $25.4k gap; strawberry adds ~$8.8k.

### Two rejected arms, and why both had to fail

Both were **static rules against a level**, in a game whose realised price is bimodal:

| tried | measured | why it could not work |
|---|---|---|
| refuse to sell below 0.5x base | **-$16,025** | 0.5x base for milk is $80; the price is either ~$160 (book at I0) or ~$55 (book +50). The floor blocks everything or nothing. |
| cap the quota to a day total rather than a turn | **-$2,653** | Spaces by CLOCK, not by price. A standing offer collects each shop drain; a one-shot order does not. |

The rule that fits the mechanism is **marginal, not floored**: walk down the computed curve and
stop at the first unit whose price falls below a reservation value. Holding has a knowable value
because the drain is deterministic (`kaggriculture.py:706-716`).

**Blind spot to close first:** `scripts/agent_ladder.py` drives seat 1 from a fixed replay, so the
only contention it can ever measure is whatever that one tape did. Both negatives above were
measured against a non-contesting opponent. This is the "never evaluate against `starter` alone"
lesson in a new costume, and it has now cost a measured $25k in a live game.

### Market manipulation and timing are not where the money is

`scripts/measure_true_drain.py` on a real leader replay: the town inventory never saturates, so the
"everyone sells wheat on day 28 and the price crashes" tragedy-of-the-commons does not occur.
Shifting only the sell days moves money at most **+3.6% and the win rate not at all**.
Market timing, front-running and withholding together are ~3% of money and 0% of wins.
The leader's own gaps between sell days are 1.0 (wheat, fertilizer) to 1.4 (wool) days — he sells
nearly daily, because **a fixed tape cannot wait for a demand event it cannot observe**.
Daily is the robust choice, not the lazy one.

---

## 7. What this changes

- The strategy is neither "wheat volume" nor "premium timing". It is *pick crops by revenue per
  tile-day against measured yields, size each to its drain, and weight by how early its shop is
  likely to open.*
- **Animals are the only uncapped producer**, and they convert wheat into a product worth 4-8x the
  wheat. Milk at $344 with zero player sales is the strongest premium position on the board.
  See `experiment_log.md` for the four separate times "animals do not pay" turned out to be a
  limitation of our own code.
- **Melon is the least scalable product in the game** — no shop, fixed 140 units — and our own
  searches built a monoculture on it three times.
- There is no large untapped market left to discover. The whole market is $302,380, "1.0x if split
  evenly between two players", and the leader banks $139,121 — he captures nearly his entire share.
  The remaining edge is efficiency and robustness.

## Still not verified

- **Intra-day throughput.** The deferred schedules in §5 sell up to 150 units in one day, which is
  legal only because carried inventory is uncapped and selling from the shed frees room to drop
  more. Whether those instalments are routable inside the action budget is untested, so every
  deferred figure is an upper bound.
- **The CARE bonus** is excluded from every yield above, so they are floors rather than ceilings.

---

# Folded-in source material

Everything below this line was consolidated from ten separate allocation/economics docs on
2026-08-20, subject to the survival rule: no measured number was dropped.
Each section is dated and names its source file.
Where two sections disagree, both are kept; see the note inline where that happens (fourth
quadrant, below) rather than a picked winner.

---

## 2026-08-15 — CEM search over crop and herd allocation dials (run pending at time of writing)

Folded in from `docs/cem_allocation_search_2026-08-15.md`.

**Status: RESULT PENDING — this file is written as the run completes. See the verdict at the bottom.**

### Where everything is

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

### What was searched

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

### Three things found before the search started, each of which changed the design

#### 1. `CROP_TILE_SHIFTS` cannot reduce melon, so the melon fork had to go in the search space

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

#### 2. Win rate against `pool.OPPONENTS` is saturated and cannot rank anything

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

#### 3. Two candidate files in one process shared one set of dials

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

### The routing regime: the unsolve is not needed, and it costs money

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

### Search design

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

### Generation by generation

RESULTS PENDING

### Held-out confirmation

RESULTS PENDING

### Verdict

RESULTS PENDING

---

## 2026-08-15 — Allocation economics after the hinge: carrot, tomato, egg (Fable)

Folded in from `docs/fable_allocation_economics_2026-08-15.md`.

Every number below is either computed from `reference/kaggriculture.py` (1.32.7, hinge live)
or measured in real 1.32.7 games against the recorded ladder field.
Scripts: `scripts/optimal_release.py` (melon fix, in this worktree),
the paired sweep rows at `data/logs/fable_carrot_paired_sweep.jsonl` (216 games),
and the reruns in `data/logs/fable_optimal_release_rerun.log` / `data/logs/fable_breakdown30.log`.

### Headlines

1. **The deficit model is validated to the organiser's own numbers.**
   Monte Carlo over the shop draw gives P(hinge fires by d29, zero production) =
   CARROT 25.8%, TOMATO 53.4%, EGG 22.4% against the announced 26% / 50% / 22%.
   The mechanism is exactly as modelled: the town drain is unconditional, inventory is linear,
   and the premium is a function of which shops the RNG unlocked and when.
2. **Unconditional conversion has no edge, and the paired sweep shows why in dollars:
   wheat is itself on a starved book.** Five of eight shops stock wheat, so a zero-production
   wheat book reaches $48 by d29 on its own; our arm-0 games realise **$45.2/unit** on wheat.
   The extra carrots realise **$42-43/unit**. The "premium" crop pays LESS per unit than the
   crop it replaces, in the median game.
3. **The hinge is real but it is a CONDITIONAL play, and the condition is public.**
   The shop draw is in `obs.town.unlocked_shops`. By d12, four draws are visible and they
   separate the games sharply: with 2+ tomato-stocking instances visible (26% of games) the
   tomato hinge fires with certainty and the d29 book quotes a median of **$216/unit**;
   with 0-1 visible it quotes $70-91. Same shape for carrot and egg (tables below).
4. **Melon corrected: the release optimiser now front-loads it and the shipped agent is
   nearly optimal already** — ACTUAL $20,285 vs OPTIMAL $21,638, so melon leaves **+$1,353**
   on the table, not the -$11,929 the broken trickle model printed.
   Total release value for the seed-11 game: **+$5,653**.

### 1. The mechanism, from the env source

`market_price` below I0 (`reference/kaggriculture.py:198-201`):

    price = base * (1 + below_target * hinge(x / T)),   x = I0 - inventory
    hinge(u) = u + 8.0 * max(0, u - 1)^2                 (:68-73)

`_town_consume` (`:728-749`) subtracts stock **unconditionally** — one unit per shop instance
per stocked product, 6 ticks/day, doubled for single-product shops, plus 1/day town centre —
so with no production the deficit x grows linearly in each instance's active days.
Shops unlock at d3, d6, ..., d24, drawn uniformly WITH replacement from the eight names (`:886-891`).

Because inventory is linear, **the end-of-season deficit depends only on totals, but the price
each unit fetches depends on when it is sold** — below I0 the deficit only deepens, so for a
pure scarcity play the optimal release is to hold and dump at d29 (shed cap permitting), and
every unit sold lifts the book and decays the premium for the next one.

### 2. What the book quotes, by day (zero production, quantiles over 20k shop draws)

    CARROT (base 35, T 450, bt 1.00)      TOMATO (base 60, T 200, bt 0.40)     EGG (base 50, T 332, bt 0.40)
    day   p25  med  p75  p90   max        p25  med  p75  p90   max             p25  med  p75  p90  max
    10     36   38   41   43    50         61   63   67   69    72              51   51   54   54   56
    15     37   41   46   51    68         63   68   72   76    90              51   53   56   58   64
    20     39   45   53   60   180         67   73   80   88   298              53   57   60   63   81
    25     44   53   63   74   500         71   80  101  160   956              56   60   65   70  202
    29     49   58   71  116  1068         77   86  165  317  1803              58   63   69   83  397

    WHEAT, same premise (base 25, sqrt below-curve, FIVE shops stock it):
    d10 33, d15 37, d20 41, d25 45, d29 48 (medians)

Selling into the starved book decays the premium slowly (T is large):
a d29 dump at the median draw pays CARROT $51-56/unit even out to 120 units,
TOMATO $73-82, EGG $57-61; at the p90 draw CARROT $79-102, TOMATO $154-258, EGG $69-76.
Volume is not the binding problem — the level of the premium is.

### 3. What a tile is worth (through real yields)

Per PLANTING (one stop), unfertilized / fertilized, from the env source and confirmed against
`kagg/economics/production.py`: WHEAT 4/6 units, CARROT 3/4, TOMATO 4/8 (harvest between events).
Measured in the sweep: 28 carrot conversions produced +84.0 sold units/game = **3.0/stop**,
and cost -70.8 wheat units/game = **2.5/stop** of wheat actually forgone.

    one late stop (d12+)         units   $/unit realised/modelled       gross    seed     net
    WHEAT (what it does today)     2.5   $45.2 measured (arm 0)          $113     $10    $103
    CARROT, agent cadence          3.0   $42.2-42.8 measured             $127     $20    $107
    CARROT, held to d29, median    3.0   ~$55 modelled                   $165     $20    $145
    CARROT, 2+ relevant shops      3.0   $81-187 modelled                $243+    $20    $223+
    TOMATO, held to d29, median    4     ~$80 modelled                   $320     $50    $270
    TOMATO, 2+ relevant shops      4     $150-216 modelled               $600+    $50    $550+

So even played optimally, carrot in the MEDIAN game is worth ~+$40/stop over wheat before the
costs below — noise. The conditional plays are worth 2-5x a wheat stop, in ~26% of games.

**EGG / goose:** cost 300 + coop + place; FEED takes 1 WHEAT/day whose opportunity cost is the
same ~$45 starved-book wheat; fed+cared it yields 2 eggs/day from placement+4.
Median realised ~$55-60/egg late season: (2 x 57 - 45) = ~$69/day gross, minus 3 unit-ops/day
and the ferry, ~17 days from a d12 start = **roughly $870/goose net of the animal, before op
costs, in the median game**. The egg hinge fires in 22% of games and needs TWO egg shops
(bakery/brunch) drawn early — visible by d12 like the others. Egg is the weakest of the three:
the same wheat scarcity that feeds the hinge thesis is the goose's feed bill.

### 4. Why the field sweep said conversion loses win rate — resolved

Paired re-run: `WHEAT_TILES_TO_CARROT` 0/8/28, 12 richest recorded opponents, seeds 1300-1302,
both seatings — 72 paired boards per arm, per-product FILLS recorded both seats
(`data/logs/fable_carrot_paired_sweep.jsonl`). The parent sweep's percentages resolve to
100/144, 88/144, 92/144, 95/144, i.e. 24 opponents x 3 seeds x 2 seatings.

    arm    win     margin delta vs 0 (paired)    sign of margin delta
      0   80.6%              —                          —
      8   83.3%    mean +12, median +906         44/72 positive
     28   77.8%    mean -1,614, median -1,883    52/72 NEGATIVE  (sign test p < 0.001)

The arm-28 loss decomposes, per game:

    direct swap:      carrot +84u -> +$3,524   wheat sold -70.8u -> -$2,616     net  +$908
    gift to opponent: THEIR wheat +$725 on the SAME units (+0.2u)               net  -$725
    feed cascade:     our MILK -18.6u, WOOL -11.1u; our str/milk/wool -$1,981,
                      their milk/wool +$1,474                                   net ~-$1,800

Four mechanisms, in order of size:

1. **Wheat's own scarcity premium.** The forgone wheat unit sells at $45, the gained carrot
   unit at $42. The direct swap is a wash in the median game (+$32/stop at arm 28); the
   whole "carrot pays a premium" framing forgot that wheat's below-I0 book is starved too.
2. **The book is shared, so withdrawing supply is a price gift.** The recorded opponents sell
   1.5-2x our wheat volume. Selling 70 fewer wheat units leaves their book less lifted and
   hands them +$725/game on unchanged units. Our bank does not record this; the margin does.
   This is also the precise reason "carrot raised mean money while lowering win rate":
   money is our side of a two-sided ledger, and Elo pays the sign of the difference.
3. **The wheat buffer feeds the herd on the margin.** The flag's own docstring says the herd
   is fed entirely out of purchases (422 bought vs 329 fed) — true on average, false at the
   margin: at 28 conversions our milk drops 18.6u and wool 11.1u per game. Those are missed
   FEED days. At 8 conversions the effect is absent (milk -0.3u, wool -0.0u) — 8 is inside
   the buffer, 28 is not.
4. **Three of twelve opponents already produce the "no production" crops**
   (tawashi 58 carrots/game, YassY 24; HoJoonYun 24 tomatoes), so in a quarter of the field
   games the premise is partly false before we plant anything.

Note the honest discrepancy: in MY 12-opponent field, arm 8 was a slight paired WIN (+2.7pt,
44/72 positive) while the parent's 24-opponent run had 8 losing 8.3pt. Both are inside noise
for a ~$0 mean effect; the strong, replicable result is arm 28's paired loss.

### 5. The play this buys, if any

Not a fixed conversion — the sweep is right to reject that. The candidate worth testing is:

- **Gate on the observed draw at d12** (below). Convert to TOMATO only with 2+ relevant
  instances visible (26% of games, hinge certain, d29 median $216); carrot likewise
  (26% of games, d29 median $81+). 0-1 visible: plant wheat, as today.
- **Cap at ~8 stops** (inside the feed buffer; mechanism 3 starts somewhere between 8 and 28).
- **Hold the crop and release late** — selling on arrival realises $42 where holding
  realises $55+; below I0 the deficit only deepens.

    visible by d12     P(games)   P(tomato hinge)   tomato d29 med   carrot: P(hinge)  carrot d29 med
    0 relevant           31%            4%                $70              0%              $43
    1 relevant           42%           61%                $91             16%              $60
    2 relevant           21%          100%               $216             68%              $81
    3+ relevant           5%          100%               $546+            96%             $187+

    (relevant = PIZZA_SHOP/FARMERS_MARKET for tomato; PET_CAFE/FARMERS_MARKET for carrot;
     BAKERY/BRUNCH_SPOT for egg. Egg: 2 visible -> 68% fire, d29 median $72 — not worth a goose.)

Expected value of the gated tomato play, before cascade costs: ~26% of games x 8 stops x
(~$550 - $103) = **~$900/game mean, concentrated as ~$3,600 in the fired games** — real but
modest, and it must be bought without disturbing the schedule (mechanisms 2 and 3 still apply
to the 8 wheat stops given up: about -$200 of gift and, at 8 stops, no feed cascade measured).
A well-implemented version is worth one careful sweep; an unconditional one is settled: no.

### 6. Melon: the front-load fix and the corrected number

`scripts/optimal_release.py` grew a `release()` dispatcher: drain <= `NO_DRAIN_THRESHOLD` (1)
front-loads (sell on arrival), else `water_fill` as before.
Red-first test: `tests/test_a_no_drain_product_is_sold_the_day_it_arrives.py`
(3 tests; red before the fix, green after; fix backed out -> red again; restored -> green).

One finding from the test itself, worth keeping: **with no opponent melon flow, trickling is
harmless** — above I0 the book recovers at the 1/day drain. The race exists because the
recorded opponents dump 114-120 melons into the same book; against that flow, whoever sells
first gets the fresh book and anything held meets the floor on d29. The first draft of the
test used `THEIRS = 0` and correctly failed the revenue assertion; the premise was wrong,
not the fix.

Corrected release table (seed 11, tape kawashigi, rerun in
`data/logs/fable_optimal_release_rerun.log`):

    product      produced  we sold  drain   ACTUAL $  OPTIMAL $  left on table
    WHEAT             531      471     31     10,367     11,710         +1,343
    CARROT             12        6     19        204        404           +200
    STRAWBERRY        212      204     31     11,464     12,502         +1,038
    MELON             114      114      1     20,285     21,638         +1,353
    MILK              177      171     13     12,194     13,163           +969
    WOOL              193      176     13     29,273     30,023           +750
    TOTAL                                     83,787     89,440         +5,653

`docs/when_and_what_to_sell_2026-08-15.md` §3 carries a correction block now: the +$12,136
"even spread" number compared against an infeasible baseline; the real release value is +$5,653.

### 7. Code changes, and the d0-d8 gate

- `scripts/optimal_release.py`: `NO_DRAIN_THRESHOLD`, `front_load()`, `release()`; `main()`
  now calls `release()`. Analysis script only.
- `tests/test_a_no_drain_product_is_sold_the_day_it_arrives.py`: new, 3 tests, all green.
- `docs/when_and_what_to_sell_2026-08-15.md`: correction block in §3.
- **No agent code was touched** — `schedule_agent.py`, `cover.py`, the router and the schedule
  are byte-identical to the session start, so the d0-d8 grid cannot have moved. Confirmed by
  running the full 30-day grid (`data/logs/fable_breakdown30.log`): the season closes
  ours $149,207 / tape $150,076 on seed 11, every cash column reconciling to the dollar.

### 8. Nulls, losses, and honest caveats

- **My first test premise was wrong** (melon trickle vs front-load with zero opponent flow:
  front-load does NOT win there; the book recovers 1/day). Kept in the test as a comment.
- **Arm 8 vs arm 0 is a null**: mean margin +12 on 72 paired games. The parent's -8.3pt at
  arm 8 and my +2.7pt cannot both be treated as signal; the mean effect is ~$0.
- **The zero-production price tables are a premise, not a forecast**: our own selling decays
  the premium (quantified in §2), our shipped plan already grows ~12 carrots, and 3/12
  recorded opponents produce carrot or tomato.
- The conditional-play EV in §5 is a model number, not a measured one — it inherits the
  d29-dump release assumption and charges no routing cost for the late harvest/water pattern
  (tomato planted d12 wants ~12 daily waters and harvests d20-23; the grid currently carries
  13-90 idle unit-turns/day mid-season, so turns exist, but the router has to actually reach
  the tiles).
- The paired sweep field skews to games Alex kept, which skews to losses (CLAUDE.md); win
  rates here are "vs these opponents", never a rating.

---

## 2026-08-15 — Fourth quadrant, first verdict: no path at quadrant scale (Fable)

Folded in from `docs/fable_fourth_quadrant_2026-08-15.md`.

Verdict up front: **no path at quadrant scale — closed by the fibonacci hire curve, not by the
bank.** Crewing 25 new tiles costs ~$21,960 in marginal hires over d12-29 against a measured
marginal crop value of $6,039 (wheat) or $15,298 (tomato, best realistic conditional case).
One arithmetic sliver survives — a conditional PARTIAL planting of ~8 tomato tiles, ~5-26% of
games — and it is operationally unreachable while cover.py cannot seat the harvest jobs it
already builds. Numbers below; nothing in agent code was changed for this.

### 1. Cost and timing — the bank does not close this

- The fourth parcel is the THIRD purchase: `LAND_ORDER = ["NE", "SW", "SE"]`,
  `LAND_PRICES = [1000, 2000, 4000]` (`reference/kaggriculture.py:96-97`). **$4,000, SE.**
- Purchases are sequential but nothing stops two in one day. Earliest covered turn: **d11**,
  alongside the third parcel — d11 currently closes at $12,699 after seeds $2,380, animal $800,
  hires $376 and the $2,000 parcel; adding $4,000 still closes ~$8,700, and every later day
  closes higher (d12 $16,246, d14 $21,799). No scheduled seed/animal/hire purchase is starved.
- So affordability is not the question. The crew is.

### 2. Can the crew work it — the closer

Working 25 wheat tiles in steady state needs ~35 work ops/day (25 water + ~5 plant + ~5
harvest) plus ~25-28 moves to snake the quadrant from the shed spawn: **~60-65 unit-turns/day,
i.e. ~2.6 dedicated hands.**

The schedule already hires 12 hands/day at $376 = sum(fib(0..11)) exactly — confirmed against
the grid's hire row. The hire curve is `cost = fib(n_already_today)`
(`reference/kaggriculture.py:698`), so the marginal hands cost:

    13th hand  $233/day
    14th hand  $377/day
    15th hand  $610/day     -> 3 extra hands = $1,220/day
    over d12-29 (18 days)   -> ~$21,960

Against that, the crop side (section 3): $6,039 for wheat, $15,298 for the best realistic
tomato case. **The crew costs 1.4-3.6x everything the quadrant can grow.**

The "use the idle instead" escape is refuted by Alex's own measurement, not by a model:
d9-29 idle is 979 turn-slots against the tape's 383, and yet 16 tiles a season die holding
units, 11 of them with a HARVEST job built on their one safe day that was not seated — and
`cover.py` contains zero references to `max_lifespan_step`, so the visit order cannot even see
the deadline. Idle turn-slots are positional; they are demonstrably not fungible into located,
deadline-day work in the quadrants we already own. A 26th-through-50th tile only multiplies the
population exposed to that mechanism: **an unreachable one-shot tile is worth negative** (seed
paid, ops spent, unit decayed to WEED), and wheat/carrot — the only crops with spare-tile-scale
economics — are exactly the crops with the one-day window.

### 3. What it would grow, measured on the real books

**Wheat** (+25 tiles from d12 = 3 cycles x 4u = +300 units), marginal revenue on the REAL
seed-11 book — recorded arrivals and both seats' sells, optimal release, via
`scripts/optimal_release.py`'s own season model:

    baseline optimal   531u -> $11,710   ($22.1/u)
    with +300u         831u -> $17,749   marginal $6,039 = $20.1/u

    net: $6,039 - $750 seeds - $4,000 land - $21,960 crew  =  ~ -$20,700   CLOSED

(The $45/u wheat realised against the ladder field does not rescue it: even at $45/u the 300
units gross $13.5k against $26.7k of costs.)

**Tomato, conditional on the d12-visible shop draw** (the only play my allocation work left
open) — exact d29 dump revenue at the median deficit of each visibility bucket, zero
production premise, premium decay included:

    visible by d12    P(games)    32u        100u        200u (fertilized)
    0                  31.3%     $2,183     $6,324     $10,324
    1                  42.2%     $2,773     $8,179     $15,121
    2                  21.4%     $6,178    $15,298     $24,012
    3+                  5.0%    $16,043    $41,423     $62,588

A FULL quadrant of tomato (100u unfert / 200u fert): at 2-visible it grosses $15-24k against
~$27k of land+seeds+crew — still negative. Only the 3+-visible bucket (5% of games) covers the
costs, and two things eat that tail: the shed caps at 100 items TOTAL so a 200u hold-to-d29
dump is infeasible (the release must spill early into a shallower deficit), and the number
assumes flawless daily watering of 25 far tiles for 18 days by a router that today drops
seated jobs in the quadrants it knows.

### 4. The sliver that survives arithmetic, and why it still fails

Conditional partial use: buy the parcel at d12 ONLY when 2+ tomato-stocking instances are
visible (26.4% of games), plant ~8 tomato tiles, crew them from existing idle (no 13th hand),
hold and release late:

    2-visible:  32u -> $6,178 - $4,000 land - $400 seeds  =  +$1,778   (21.4% of games)
    3+-visible: 32u -> $16,043 - $4,400                   =  +$11,643  ( 5.0% of games)
    unconditional EV                                      ~  +$960/game

Tomato is `ongoing: true` — no one-day harvest window, so the crop-death mechanism does not
apply to it; the risk is two missed waters = WEED. That is the same seating problem in a
different costume: ~10 SE unit-turns/day for 18 days with a no-miss-twice constraint, from a
planner that currently leaves 11 built jobs unseated per season. It also requires agent code
that does not exist (a conditional BUY_LAND, SE routing), and ~$1k/game EV is under the
seed-noise floor (~15%) — it could not even be measured cleanly today.

### 5. Bottom line

    marginal crew for a workable quadrant      -$21,960
    best full-quadrant crop value (realistic)  +$6,039 wheat / +$15,298 tomato 2-visible
    -> full quadrant                            NO, in every bucket except a 5% tail the
                                                shed cap and the seating defect both bite
    -> conditional 8-tile sliver                +$960/game EV on paper, unreachable until
                                                the router can seat deadline-day jobs

The same crew-seating defect that kills the fourth quadrant is already costing 16 dying tiles
a season in the three we own. Fixing the seating pays there first, with no land, no hires and
no new code path — and only after that fix would the sliver above even be measurable.

---

## 2026-08-15 — Fourth quadrant, reopened against the field — retracts the crew-cost closer above (Fable)

Folded in from `docs/fable_fourth_quadrant_reopened_2026-08-15.md`.

**Same day, same author, explicit self-retraction of the section above.** The prior section's
"no path — closed by the crew cost" verdict rested on a $21,960 marginal-crew number for a plan
(full 25-tile cultivation, hired crew) that no field agent actually plays. This section retracts
that number directly (§1 below) after reading 60 fresh episodes, and finds the fourth quadrant is
bought as a small conditional package (land + 4 sheep + relocated wheat), not full cultivation.
Both verdicts are kept, in full, because the retraction is on the record in the source and the
earlier arithmetic is still correct **for the plan it priced** — it was the premise that changed.

Data: the 60 fresh episodes (`data/9*.json`, 120 seats), extracted to
`data/logs/fable_field_seats.jsonl` (per seat, per day: money, quadrants, hires, per-quadrant
planted/weed/pen counts, plant/water op counts, opening fingerprint).
Scratch: `extract_field.py`, `field_analysis.py`, `buy_land_mechanism.py`, `trigger_test.py`.

### 1. The $21,960 crew number: RETRACTED as the closer

My number priced full cultivation of 25 new tiles (~60-65 unit-turns/day) bought with marginal
hires on the fib curve. The field does neither:

- All three 100-tile seats run **277 season hires — zero more than the 75-tile seats** (264-277).
- Plant ops d13-29: 100-tile 100 vs same-script 75-tile 107. Waters: 616-628 vs 649-655.
  **The quadrant is worked by RELOCATING the same ops, not adding any.**
- SE utilisation: ~5-11 planted tiles (of 25) plus 3-4 pens, weeds 0-4. Half the ground stays
  empty. Extra tiles that cannot be reached are simply not planted — they are worth zero, not
  negative, because nobody plants what they cannot water.

What the fixed-ops quadrant actually buys is **slots the full 75-tile board cannot host**:
every 100-tile seat carries **18 animals against the 75-tile seats' 14** (the +4 are SHEEP, in
SE, from d12), plus 6-8 planted tiles of headroom. The SE crop is **WHEAT in all three games**
(tile-days: wheat 110-129, sheep 56-62; nothing else) — consistent with my earlier finding that
wheat's own starved book pays ~$45/unit and needs no premium story.

My crew arithmetic was correct about the plan it priced; the field plays a different plan.
What survives of the original answer: nothing at quadrant-cultivation scale was ever the play,
and the seating/deadline risk still applies to whatever IS planted there (weeds 1-4 appear in
SE in two of three games).

### 2. The selection problem — the mechanism, measured

The purchase is **not bank selection, and not a symptom of a rich first half.** Direct reads:

- The script family emits `BUY_LAND` at d6h5 and d11h1 in ALL 17 cluster games. The d12h1
  order for the 4th parcel is emitted **only in the three games that end at 100 tiles.**
- Every 75-tile seat had $13,173-$15,480 at d12h1 — ample for a $4,000 parcel — and did not
  order. The three that DID order held $7,953-$10,425, the POOREST of the cluster at that turn
  (they had just bought extra animals). Wealth anti-selects; the purchase is a deliberate
  conditional in the script.
- Before any divergence (d10), the eventual-100 games sit INSIDE the 75-tile money range
  (16,363 vs [15,253..17,282]). The d1-d12 trajectory is NOT already better.

I could not pin the trigger from 17 games. It is not yarn count alone (100T draws: yarn 2,1,1;
five 75T games also show yarn=1), not milk-carrier count, not bank. What is unambiguous is that
the parcel fires as one PACKAGE with the herd expansion: +1 animal by d12, +4 by d18, all
sheep, all in SE, wheat around them.

**Consequently the headline gap (100-tile mean $131,344 vs 75-tile $89,229) is mostly the
trigger's selection, not the parcel.** The script buys in games its condition says are good for
an expanded herd, and those are exactly the games wool/milk print in. Cross-game comparison
overstates the parcel ~5-10x.

The cleanest causal number that exists: **the within-game pair.** `92816217` holds a 75-tile
variant (s0, fp a014, $120,160) and a 100-tile variant (s1, fp fe64, $127,645) of the same
meta-script family against the same market, same draw: **+$7,485 for the expansion package.**
One pair, different script variants, so it is an estimate, not a proof — but it agrees with
the bottom-up arithmetic: 4 extra sheep on a wool-friendly draw ~ $8-15k gross minus $2,000
animals minus $4,000 land minus ~zero marginal crew.

### 3. The buy rule, if we adopt it

What the evidence supports (and no more):

- **Conditional, at d12, as a package: $4,000 parcel + 4 sheep + relocate ~8 wheat plantings
  onto SE.** Never unconditional: the 75-tile mode is the majority mode of the best scripts
  (14 of 17 cluster games), and the field's top-vs-bottom split shows tiles/herd do NOT
  separate seats on average.
- **Trigger, ours to define since the field's is unreadable at n=3:** the draw must support
  the extra herd's OUTPUT. Given Alex's own calibration measurement (8 sheep on 1 yarn floods
  by 61 units, wool $35; on 2 stores $243) the defensible trigger is **2+ YARN_STORE visible
  by d12** for the sheep package (P ~ 8% of games), or — per my earlier conditional-tomato
  work — **2+ tomato-stocking instances by d12** (P ~ 26%), in which case the ground takes the
  gated tomato stops instead of wheat and the timing lines up exactly (parcel d12, plant
  d12-13, first fruit d20-23, hinge fires with certainty in that bucket).
- Bank is never the constraint: our shipped plan closes d11 at $12,699 and d12 at $16,246;
  the field buys on less.
- Expected value if the trigger fires: ~+$7.5k (within-game pair) against seed-noise of ~15%
  of an ~$150k season — real but small, and it inherits the same seating discipline the
  quadrant's weeds (1-4 even in the field's games) warn about.

### 4. Corrections to my previous answer, stated plainly

1. **$21,960 marginal crew: retracted.** It priced a plan (full cultivation, hired crew) that
   no one plays. The field's marginal crew cost is zero by relocation.
2. **"Extra tiles that cannot be reached are worth NEGATIVE": wrong in practice.** Nobody
   plants them; unreachable ground is worth zero minus the $4,000 gate.
3. **"No path" -> there IS a narrow path**, and it is the one the best seat in the field
   (One-For-All, $143,621) walks: a conditional d12 package of land + sheep + relocated wheat,
   in a minority of games. Its honest value is ~+$7.5k per triggered game, not the +$42k the
   raw 100-vs-75 means suggest.
4. What my original answer got right and keep: affordability was never the question; full
   cultivation is uneconomic; and the cross-game bank gap is selection — Alex's instinct to
   distrust the n=3 comparison was correct, just with wealth-selection replaced by
   trigger-selection.

---

## 2026-08-15 — A four-quadrant variant, first draft and first measurement

Folded in from `docs/q4_variant_first_draft_2026-08-15.md`.

Worktree: `/Users/alexchilton/DataspellProjects/kaggriculture/.claude/worktrees/agent-aba114beb8852f9e4`.
Nothing here is committed and nothing in the main tree was touched.

Files added:

- `kagg/search/q4_agent.py` — the variant.
- `scripts/q4_probe.py` — the measurement, one OS process per cell.
- `tests/test_the_fourth_quadrant_branch_leaves_the_opening_alone.py` — 7 fast tests, 11 slow.

Logs: `data/logs/q4_probe.log`, `data/logs/q4_probe.json`, `data/logs/q4_shopscan.log`,
`data/logs/q4_opening_test.log`.

### What was built

The shipped agent is not edited and its behaviour is unchanged.
`q4_agent.make_agent` wraps `schedule_agent.make_agent` and the whole branch is an edit to ONE ROW
of the schedule, day 12.

That works because `schedule_agent` reads its schedule live rather than latching it at
construction: the land block walks `sched[d]["land"]` every turn to find the next parcel due,
`want_total` re-accumulates `animals_bought` every turn, and `_refresh_pins` re-reads `builds` and
`places` every turn.
`schedule_agent.make_agent` also shallow-copies the outer schedule dict and shares every row object
with its caller, which is what lets the wrapper arm the day-12 row at day 6 and have the agent see
it at day 12.

The trigger is `q4_agent.the_town_promised_wool_early(obs)`.
It reads `observation["town"]["unlocked_shops"]` and tests for `YARN_STORE` among the first two
draws.
`YARN_STORE` is pinned against `reference.kaggriculture.SHOPS` by a test, because a predicate keyed
on a misspelled shop never fires and reads exactly like a measured null.
Shops unlock every `townShopUnlockInterval = 3` days (`reference/kaggriculture.py:867,886`), so d6
hour 0 has seen exactly the d3 and d6 draws and "a yarn store by d3-d6" is exactly the first two
entries of the list.

When the trigger fires the branch writes four things onto the day-12 row — `land: 1`,
`animals_bought: {SHEEP: 4}`, `builds: 4`, `places: ["SHEEP"] * 4` — and drops the solved routes
from d12 onward.
`_do_buy_land` takes `LAND_ORDER[len(unlocked) - 1]` (`reference/kaggriculture.py:712-725`), so
owning NW, NE and SW makes the third parcel SE deterministically; it is not a choice the branch
makes.
The four extra animals take the schedule's herd from 14 to 18, and on an early-yarn board
`_herd_split` already caps cows at six, so the split spends all four on sheep and returns
COW 6 / SHEEP 12.

Refusals are reported rather than swallowed.
`_do_buy_land` returns silently on a short bank and so does `_do_hire`, so a run that quietly
stayed on three quadrants would otherwise be measured and written up as "the parcel does not pay".
Every refusal is printed to stderr once and recorded in `agent.q4_report`.

### The opening is action-for-action what ships, and the test that says so is not vacuous

`test_the_opening_is_action_for_action_what_ships` plays the shipped agent against the environment,
hands the q4 agent the identical observation every turn, and compares the two actions.
11 seeds, 11 passed, no divergence before d12.

Arming at d12 is not obviously inert before d12 and this was the one real risk in the design.
`_pens_due_before_more_land(sched, day)` scans days AFTER today for the next parcel and counts the
pens due before it, so adding `builds: 4` at d12 alone would change what d11 believes about its own
pens from 0 to 4, and adding `land: 1` at d12 cuts the scan short and returns it to 0.
Neither edit is safe on its own; the pair is.

Two checks were run against the test itself.
Moving the package from d12 to d10 makes all three probed seeds diverge at exactly d10h0, so the
comparison discriminates.
More importantly, the first version of the test was **vacuous and passed**: it picked its seed by
stepping a PASS-only game, and the shop draw comes off the environment's own `rng`, which the weed
spawn and everything else also consume — so a game where nobody plants anything draws a different
shop stream from the game the agents play.
The pre-scan said seed 0 had an early yarn store; the real game shows `['BAKERY', 'PET_CAFE']`.
Every identity assertion passed while the branch under test never armed.
The seed list is now measured from real games (`data/logs/q4_shopscan.log`) and the test asserts
`armed` at the end.

Early-yarn boards are 11 of seeds 0-69, a base rate of 15.7% against a theoretical
1 - (7/8)**2 = 23.4%.

### The measurement

Three arms, because two would not have been interpretable.
`cover._apply_precomputed` keys a stop on `(tile, ops)` against routes solved for a 75-tile board,
so the q4 arm has to plan d12-29 live, and live routing costs real money on its own.
`shipped_live` is the shipped agent paying that same handicap and nothing else, which is what makes
`q4 - shipped_live` a statement about the parcel rather than about the router.

One OS process per cell, per the 2026-08-15 finding that the first run in a process differs.
There is a second reason here: `q4_agent` mutates `cover.PRECOMPUTED_ROUTES`, which is
process-global, so two arms in one process would contaminate each other's routing.

Opponent `data/sweep/frozen_1186_opponent.py`.
Seeds 3, 10, 17, 18, 22, 45, 47, 53, 60, 65, 66 — every seed under 70 whose town draws a yarn store
in its first two draws.
All eleven arm the branch, so this is the CONDITIONAL effect, not the season average.

```
 seed arm                 bank        opp  R  quad  COW  SHP    CARRO  MELON  STRAW  WHEAT
    3 shipped          133,082    131,472  W     3    6    8     100%   100%   100%    97%
    3 shipped_live     133,221    125,186  W     3    6    8     100%   100%    98%    95%
    3 q4               127,806    123,072  W     4    6   12     100%   100%    99%    95%

   10 shipped           93,307     90,274  W     3    6    8     100%   100%    99%    95%
   10 shipped_live      94,620     90,051  W     3    6    8     100%   100%    97%    96%
   10 q4                86,025     81,800  W     4    6   12     100%   100%    99%    97%

   17 shipped           77,707     75,923  W     3    6    8      91%   100%    97%    97%
   17 shipped_live      78,855     79,568  L     3    6    8      88%   100%    98%    92%
   17 q4                70,734     66,509  W     4    6   12      91%   100%    99%    94%

   18 shipped           89,266     89,051  W     3    6    8     100%   100%    99%    95%
   18 shipped_live      82,258     81,723  W     3    6    8      96%   100%    99%    93%
   18 q4                81,682     81,063  W     4    6   12     100%   100%    99%    96%

   22 shipped          117,959    107,563  W     3    6    8      96%   100%   100%    97%
   22 shipped_live     108,441    104,525  W     3    6    8     100%   100%    98%    95%
   22 q4                97,011     87,855  W     4    6   12      91%   100%   100%    95%

   45 shipped          106,157    100,507  W     3    6    8     100%   100%   100%    97%
   45 shipped_live     101,878     98,330  W     3    6    8     100%   100%    98%    94%
   45 q4               100,182     97,762  W     4    6   11      96%   100%   100%    96%

   47 shipped          106,923    104,961  W     3    6    8     100%   100%    97%    94%
   47 shipped_live     107,848    105,359  W     3    6    8      86%   100%    98%    94%
   47 q4               106,351    102,464  W     4    6   12     100%   100%   100%    96%

   53 shipped           70,506     69,593  W     3    6    8      91%   100%    97%    96%
   53 shipped_live      69,385     69,814  L     3    6    8      89%   100%    97%    93%
   53 q4                75,169     69,702  W     4    6   12     100%   100%    98%    97%

   60 shipped          103,693    101,640  W     3    6    8     100%   100%    97%    94%
   60 shipped_live     104,443    101,406  W     3    6    8      86%   100%    98%    94%
   60 q4               108,889    104,082  W     4    6   12     100%   100%   100%    94%

   65 shipped          112,169    112,382  L     3    6    8     100%   100%    97%    94%
   65 shipped_live     112,971    110,258  W     3    6    8      86%   100%    98%    94%
   65 q4               109,401    104,574  W     4    6   12      91%   100%   100%    94%

   66 shipped          116,568    114,236  W     3    6    8      96%   100%    95%    96%
   66 shipped_live     112,813    116,243  L     3    6    8     100%   100%    98%    92%
   66 q4               135,609    134,737  W     4    6   12      87%   100%    98%    97%

arm               mean bank      median    wins  mean quads  mean herd  collect
shipped             102,485     106,157   10/11        3.00      14.00      97%
shipped_live        100,612     104,443    8/11        3.00      14.00      95%
q4                   99,896     100,182   11/11        4.00      17.91      97%

comparison                              mean d    median d  seeds better  W/L swing
shipped_live - shipped                  -1,873        +139       6/11         -2   the LIVE-ROUTE handicap alone
q4 - shipped_live                         -716      -1,696       3/11         +3   the PARCEL + herd, handicap paid by both
q4 - shipped                            -2,589      -5,276       3/11         +1   what actually ships vs the variant, all-in

q4 armed on 11/11 seeds; SE actually unlocked on 11/11. Buy days: [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
refusals: ['herd short at d20: COW 6 / SHEEP 11 against target COW 6 / SHEEP 12, bank $41,689']
animals standing in SE at d29: [4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4] of [18, 18, 18, 18, 18, 17, 18, 18, 18, 18, 18] total
SE tiles still carrying a crop at d29: [0, 0, 0, 1, 3, 0, 0, 0, 4, 0, 1] (of 25)
```

Collection rates are 94-100% on every arm and every crop, so no money figure in this table is a
routing failure wearing a crop's name.
The mechanism landed on 11 of 11 seeds: SE unlocked on d12 every time, and the herd finished at
COW 6 / SHEEP 12 on 10 of 11.
Seed 45 finished one sheep short with a bank of $41,689, so that is a placement failure and not an
affordability one; the refusal reporter caught it.

### What the numbers say

**The money result is a null with a wide error bar, not a loss.**
`q4 - shipped_live` is -$716 with a per-seed standard deviation of $9,408, so the standard error on
that mean is $2,837 and the spread runs from -$11,430 to +$22,796.
`q4 - shipped` is -$2,589 with a standard error of $3,026.
Neither is distinguishable from zero on 11 seeds.
The median deltas are more negative than the means (-$1,696 and -$5,276) because two seeds carry
large positive tails, which is worth stating rather than smoothing away.

**The routing handicap is the larger of the two effects and it is separable.**
`shipped_live - shipped` is -$1,873 and costs two wins.
That is the cost of dropping solved routes from d12, paid by both live arms, and it has nothing to
do with the parcel.
Most of what `q4 - shipped` measures is therefore the router, not the fourth quadrant.

**The win rate moves the other way from the money, and the reason is measurable.**
q4 wins 11/11 against shipped's 10/11 and shipped_live's 8/11.
Mean margin over the opponent is +$4,113 for q4 against +$2,703 for shipped, because the
opponent's mean bank falls further (-$3,998) than ours (-$2,589).
The four extra sheep flood a shared wool book, and against an opponent selling the same products
that hurts the opponent more than us.
**This is a near-mirror result and must not be read as a ladder result.**
`frozen_1186_opponent.py` is a frozen copy of our own agent family, so the suppression works
because both sides sell the same things; a field with a different crop mix need not respond the
same way.
And 11/11 against 10/11 is one seed.

**The fourth quadrant is bought and then left empty.**
Four of the eighteen animals stand in SE, which is exactly the +4 sheep the package added, and that
is the whole use the branch makes of 25 tiles.
The SE crop count at d29 is 0 on seven of eleven seeds.
That number is a floor — a tile harvested before d29 reads empty — but the direction is not in
doubt, because nothing in this draft relocates any planting onto the new ground.
The direct outlay is $4,000 for the parcel plus 4 x $500 for the sheep; pastures are free.
So $6,000 buys four pen sites, and the measured return on that is -$716 +/- $2,837.

This is the gap the module docstring flags in advance and it is the gap against the field.
`docs/fable_fourth_quadrant_reopened_2026-08-15.md` measures the 2026-08-14 field and finds the
100-tile seats run 277 season hires — exactly what the 75-tile seats run — and work the quadrant by
RELOCATING roughly eight wheat plantings onto it, with the SE crop being wheat in all three games.
This draft implements the herd half of that package and none of the crop half.

### One contested number, left visible

The brief specifies COW 6 / SHEEP 12 = 18 and the code implements it.
`schedule_agent.WOOL_SHOP_SETS_THE_HERD` records a 2026-08-15 measurement over 74 Kawashigi seats
in which his four-quadrant herds run 13-16 and never 18, with a maximum of 16 over all 74.
`docs/fable_fourth_quadrant_reopened_2026-08-15.md` records 18 for the 2026-08-14 field's 100-tile
seats.
Both can be true — they are different players — but 18 is the field's number and not the leader's,
and it is one of the two places to look if this is retried.

### Verdict

Four quadrants is worth pursuing, but not in this form, and the reason is specific rather than a
hedge.
The branch does what it was asked to do — it fires on the right boards, takes SE on d12 on 11 of 11
seeds, and lands COW 6 / SHEEP 12 on 10 of 11 — and buying 25 tiles to stand four sheep on is
measurably worth about nothing: -$716 against the arm that pays the same routing handicap, with a
standard error four times that.
The two things standing between this draft and a real test of the idea are both identified and
neither is the parcel.
First, the solved routes are solved for 75 tiles, and dropping them costs -$1,873 and two wins
before the fourth quadrant does anything at all; re-solving the day routes for a 100-tile board
would remove that confound entirely and is a bounded piece of work.
Second, and more important, the field's package is land plus sheep plus roughly eight relocated
wheat plantings, and this draft ships the first two and none of the third — so the honest summary
is that the parcel has not yet been given a job.
The one genuinely encouraging signal, that q4 wins 11/11 and widens the mean margin over the
opponent by $1,410, is a market-suppression effect measured in a near-mirror against a frozen copy
of ourselves, and should be re-run against the real pool before anyone believes it.

---

## 2026-08-16 — Allocation bounds: the near-optimal region for every crop and species

Folded in from `docs/allocation_bounds_2026-08-16.md`.

2026-08-16.
Model and solver: `scripts/allocation_bounds.py`.
Run log: `data/logs/allocation_bounds.log`.

The question answered: given the game's constraints, what RANGE must the season allocation lie in?
The deliverable is a near-optimal region per crop and per species — the interval each season total
can move over while end-of-season money stays within 1% (and 5%) of the model optimum.

### Headline

The leader's MELON 20 / STRAWBERRY 34 split is NOT inside the 1% near-optimal region in any
of the three scenarios.
Pinning it costs 1.78% of the optimum when the opponent sells nothing, 3.9% against the
leader's own supply, and 23% against double supply.
It IS inside the 5% region in the first two scenarios.
The reason is melon alone: the melon book absorbs only ~30 units of town demand a season and
its price falls as 250 − 0.01·(surplus)², so 20 melon tiles (120 melons) is near-optimal only
when the OPPONENT is not also selling melons.
His strawberry 34 sits inside the 1% interval in scenarios 1 and 2.

The herd answer is shop-draw dependent, not universal: under this game's draw (SMOOTHIE x4 =
strawberry+milk demand) the model wants 9-18 cows and his cross-game modal COW 6 is below the
1% interval, while under an average draw the optimal herd collapses to COW ~2.
His measured play IN this game (COW 10, SHEEP 4) matches the model's scenario-1 optimum
(COW 9, SHEEP 6) far better than his cross-game modal 6/8 — consistent with
"the leader re-plans on the shop draw".

### Results

All money figures are end-of-season money minus the $3000 start (Z).
Base MILP solves reached mip gaps of 0.4-0.7% at the 150 s limit (flagged in the log);
the pinned leader checks reached 0.4-2.0%, so quote their drops with that width.
Ranges are LP-relaxation OUTER bounds (see below): outside them the loss certainly exceeds
the tolerance; inside them not every point is achievable — the pinned checks close that gap
for the leader's own point.

Units: crops = tile-cycles planted over the season (a melon cycle is 1 tile for 11 days);
animals = head bought.  "leader" = his measured allocation over 51 games.

    S1  opponent = leader's per-day fills      Z* = $129,045   (bank $132,045)
    item         base       [1% range]       [5% range]   leader
    WHEAT          93        [15, 185]         [0, 229]        -
    CARROT         16         [0, 144]         [0, 194]        -
    TOMATO         22          [0, 68]          [0, 85]        -
    STRAWBERRY     29         [15, 50]          [7, 64]       34
    MELON           6          [0, 31]          [0, 45]       20
    GOOSE           2          [0, 15]          [0, 21]        0
    COW             9          [6, 17]          [5, 22]        6
    SHEEP           6          [4, 15]          [3, 20]        8
    pinned MELON=20,STRAW=34             -> Z $123,989, drop 3.92%  (>= 2.0% after gap)
    pinned MELON=20,STRAW=34,COW=6,SHEEP=8 -> Z $118,148, drop 8.44%

    S2  opponent = zero                        Z* = $190,247   (bank $193,247)
    item         base       [1% range]       [5% range]   leader
    WHEAT          65         [2, 148]         [0, 181]        -
    CARROT          7          [0, 86]         [0, 135]        -
    TOMATO          2          [0, 38]          [0, 56]        -
    STRAWBERRY     33         [20, 51]          [9, 62]       34
    MELON          27         [14, 42]          [6, 55]       20
    GOOSE           0          [0, 10]          [0, 17]        0
    COW            18         [13, 24]          [8, 30]        6
    SHEEP          10          [7, 18]          [5, 24]        8
    pinned MELON=20,STRAW=34             -> Z $186,856, drop 1.78%
    pinned MELON=20,STRAW=34,COW=6,SHEEP=8 -> Z $161,856, drop 14.92%

    S3  opponent = 2x leader's fills           Z* = $56,125    (bank $59,125)
    item         base       [1% range]       [5% range]   leader
    WHEAT         110        [47, 197]        [31, 227]        -
    CARROT         43         [0, 130]         [0, 165]        -
    TOMATO         40         [16, 64]          [6, 74]        -
    STRAWBERRY      9          [1, 20]          [0, 27]       34
    MELON           0          [0, 12]          [0, 20]       20
    GOOSE          16          [8, 22]          [5, 25]        0
    COW             0           [0, 5]           [0, 7]        6
    SHEEP           0           [0, 3]           [0, 6]        8
    pinned MELON=20,STRAW=34             -> Z $43,198, drop 23.03%
    pinned MELON=20,STRAW=34,COW=6,SHEEP=8 -> Z $31,545, drop 43.79%

Base solution details, scenario 1: hands 8.1/day mean (leader measured 9.6 units/day incl.
farmer), 2 land parcels, wheat bought 142, fertilizer collected 335 and sold 145
(the leader sold 249), sold MELON 36 / STRAWBERRY 232 / MILK 294 / WOOL 164.

#### What holds in all three scenarios

- Some strawberry is always in (min never 0 at 1% in S1/S2; 1.5 in S3), and 34 tiles is
  never harmful by more than ~2% except under a double-supply flood.
- Melon is the contested resource: its 1% interval slides from [14, 42] (empty market)
  to [0, 31] (leader present) to [0, 12] (flooded).  There is no melon count that is
  near-optimal in all three scenarios — melon allocation is a bet on what the opponent sells,
  not a fixed constant.  20 is the S2 answer played unconditionally.
- Wheat is wide everywhere ([15-47 min, 148-197 max @1%]): dozens of wheat cycles are
  interchangeable with bought wheat at a few dollars margin.  A wide range is a real finding:
  wheat count is nearly a free parameter.
- Geese are never obligatory below double supply, but become the SAFE HAVEN when everything
  else floods (egg price is log-flat above I0): S3 forces 8-22 geese.  This is the first
  measured case where geese are the right play — against a flooder, not against the field.
- The herd (cow+sheep) tracks milk/wool demand from the shop draw, from 0 to 28 head.

#### Shop-draw sensitivity (scenario-1 economics)

    draw            Z*        WHEAT CARROT TOMATO STRAW MELON  GOOSE COW SHEEP
    actual (SMOOTHIEx4) $129,045   93    16    22     29     6      2   9    6
    expected (avg shop) $93,073    85    42    29     16    11     10   2    5
    no shops            $53,038   141    46    23      0    13     17   0    0

The draw moves Z* by a factor of 2.4 and reallocates the whole farm: strawberry 29 -> 0,
cows 9 -> 0, geese 2 -> 17.  Melon moves only 6 -> 13 because melon has no shop —
its demand is the town center's 1/day regardless of the draw.
Any fixed season allocation is therefore an average over draws; the measured leader behaviour
(fixed 74-turn opening, then adapt to the draw) is what this table predicts a good player
must do.

### Ground truth and inputs

- Rules, prices, growth data: imported at runtime from the installed
  `kaggle-environments 1.32.7` kaggriculture module, which is byte-identical to the main repo's
  `reference/kaggriculture.py`.
  The worktree copy of `reference/kaggriculture.py` in this branch is STALE
  (pre-hinge, pre town-drain change); it was not used.
- Opponent supply: episode 92498144 (カワシギ $149,998 vs Yusuke Hayashi $143,436, seed 1240813987),
  re-run through the real engine with the recorded actions and seed, logging every `_commit_unit`
  fill.
  The recorded rewards reproduce to +$78/+$0 (0.05%); the drift is the 1.32.7 repricing of
  CARROT/TOMATO/EGG (the episode was recorded on module 1.32.6).
  Fills are exact, not inferred from the action stream (offers are not fills).
- Leader's measured season, from those fills:
  sold WHEAT 522 / STRAWBERRY 223 / MELON 120 / MILK 279 / WOOL 120 / FERTILIZER 249 / CARROT 20;
  bought WHEAT 423;
  seed buys WHEAT 144 / MELON 20 / STRAWBERRY 34 / CARROT 16; animal buys COW 10 / SHEEP 4.
  The MELON 20 / STRAWBERRY 34 seed buys equal the reference allocation measured over 51 games.
- Shop draw in that game (with replacement, active-from-day):
  d3 SMOOTHIE, d6 ICE_CREAM, d9 FARMERS_MARKET, d12 YARN, d15 PIZZA, d18/21/24 SMOOTHIE.
  Season town drain under that draw: WHEAT 390, CARROT 156, TOMATO 246, STRAWBERRY 624, MELON 30,
  EGG 30, MILK 588, WOOL 246, FERTILIZER 0.

### The model (MILP over days 0..29)

Decision variables (all per day):

- `x[c,fert,d]` int — tiles starting a crop cycle of variant (crop, fertilised?) on day d.
  Variants: WHEAT_u/f, CARROT_u/f, MELON_u, TOMATO_u/f, STRAWBERRY_u/f.
- `y[a,d]` int — animals of species a bought, penned and placed on day d.
- `h[d]` int — hands hired that day (hands are per-day in this game; the crew resets at dawn).
- `land[k,d]` bin — k-th parcel bought on day d (ordered, prices 1000/2000/4000).
- `u[p,k]` cont — units of product p sold in sell-slot k (see Revenue).
- `wbuy[d], g[d]` — wheat bought / own-grown wheat diverted to feed.
- `fbuy[d], fcol[d]` — fertilizer bought / collected from animals (1 op per unit).

Every cycle/placement expands to an exact per-day profile of work ops, yields, feed and
fertilizer use, simulated directly from the env rules (watering windows, `consecutive_unwatered`,
care-bonus accrual, held-unit caps, harvest cadence, decay + DIG).
Self-checked anchors: wheat_u 4 units/6 ops, melon 6 units/10 ops/11 tile-days,
tomato_f 8 units, strawberry_f 8 units with 2 fertilizer, goose first 4 eggs at day+4 then 2/day,
cow first 6 milk at day+8 then 3 per 2 days, sheep first 6 wool at day+6 then 4 per 3 days.

Constraints, all linear:

- Tiles: sum of active cycles + pens <= 25 + 25 * parcels bought by day d (max 100).
- Labour: (1 + lambda) * work_ops_d <= 24 * (1 + h_d), lambda = 3477/2773 = 1.254 —
  the leader's measured move/work ratio over a full season (seed 11 tape:
  work 2773, move 3477, idle 660 of 6910 unit-turns).
  Movement is charged on every work op; market orders (SELL/BUY/HIRE/BUY_LAND) cost no turns.
- Cash: running bank >= 0 every day, from $3000.
  HIRE cost is the exact per-day fibonacci sum (convex slot formulation).
- Growth: encoded in the cycle profiles; a cycle with no harvest before day 29 does not exist.
- Feed: 1 wheat per animal per day (fed through day 28); grown wheat usable the morning
  after harvest, bought wheat the same day at the simulated market price.
- Fertilizer: collected (1 op) from any live animal, at most 1/animal/day, or bought;
  used by fertilised cycle variants; sellable.
- Sales availability: cumulative units sold by a slot's day <= cumulative harvested by then.

Objective: end-of-season money = sum of slot revenues minus seeds, animals, land, hires,
wheat and fertilizer purchases.

#### Revenue (the hard part)

Price is the env's own `market_price` (hinge shapes included) on a per-product book:

    book(d) = I0 + own_sales(price>1) + opponent_net(d) − town_drain(d)

Each product gets K=30 sell slots of fixed width with FIXED assumed sell days:
slot k is sold on the earliest day where cumulative book room (town drain minus opponent
supply, made monotone) reaches k*width — i.e. the model sells unit-for-unit into demand as it
materialises, which is what the leader's cadence does.  Units beyond total season room sell at
day 29 (surplus tail); products with no demand regime (melon) spread uniformly over their window.

Slot k's value is simulated unit-by-unit with slots 1..k-1 already sold — the maximum possible
prior own supply — so every slot value is a LOWER bound on the realised price of those units for
any fill pattern the MILP chooses.  This makes the piecewise revenue LP-safe with no SOS2 or
binaries: skipping early slots and filling late ones only under-prices the late ones.
MELON's `sq` above-threshold shape (price 250 − 0.01*(inv−I0)^2, floor $1, floor sales do not
move the book) is priced exactly by this unit-level simulation.

#### How the ranges are computed

The base optimum Z* is a MILP solve (HiGHS via scipy, mip_rel_gap 2e-3, incumbents at the
time limit flagged in the log).
Each range endpoint is then min / max of the item's season total subject to all constraints
plus objective >= (1 - tol) * Z*, solved on the **LP relaxation**.
Every integer-feasible point is LP-feasible, so these are valid OUTER bounds on the true
integer range: outside the reported interval the objective certainly drops more than tol;
inside it, not every point need be achievable.
(Hard-floor integer range solves were tried first and are not tractable here: HiGHS needs
~150 s to find any integer point within 1% of Z*, and 96 such solves do not fit a day.)

Because an outer bound could make the leader's point look inside when it is not, the
leader's reference allocation is ALSO checked directly: MELON=20 and STRAWBERRY=34 (and
separately +COW=6, SHEEP=8) are pinned as equality constraints and the full MILP re-solved;
the realised objective drop is reported per scenario.

#### Assumptions, stated plainly

1. Walk cost is an average: 1.254 move-turns per work op, calibrated on the leader's own season.
   No per-quadrant term — the shed is central, so all four quadrants have the same distance
   distribution (mean Manhattan distance 4.0 from the shed corner to a quadrant tile).
2. Sell timing is an assumption, not a decision variable: sales follow the demand curve
   (surplus tail at day 29).  Slot values are conservative (max-prior-own-supply).
3. Within-day cash ordering is ignored (a day's revenue can fund that day's purchases);
   the leader's own play does sell-then-buy within a day.
4. Our own wheat BUY volume does not move the wheat book in the base solve; one feedback
   iteration re-prices wheat buys with the chosen volume folded in and re-solves
   (triggered above 100 units).  Fertilizer buys are priced the same way, without iteration.
5. Full husbandry on animals (daily feed + care, harvest at cap) and full watering on crops;
   weeds from missed watering and the 0.5% random weed spawn are not modelled.
   CARE is skipped when the bonus cannot land (cap or season end) — e.g. a cow placed day p
   is cared only 5 of its 8 pre-production days.
6. Shed capacity (100) and the 10-orders-per-turn cap are not binding at these volumes
   and are ignored.
7. Animals never escape and are never sold; pens hold one animal for the rest of the season.
8. GOOSE/COOP is modelled (nothing forbids it); the ranges answer whether it should exist.
9. Opponent behaviour is FIXED per scenario (the three opponent-supply scenarios);
   the market book is the only interaction channel modelled.  No Elo/win-rate objective —
   this is a money-maximising planning bound, as specified.

#### Known biases

- Revenue is a lower bound under the fixed sell schedule; a solver free to choose timing
  could do slightly better (melon especially: selling before the opponent floods the book).
- Labour is charged at the leader's realised walk ratio; a better router lowers it, a worse
  one raises it.  The leader also idled 9.6% of unit-turns which the model does not charge.
- Prices are conservative for high-volume products (max-prior-fill assumption), so
  high-volume items (milk, strawberry, wheat) are if anything UNDER-allocated by the model.

### Run facts

Full run 1975 s on 2026-08-16, log `data/logs/allocation_bounds.log`.
MILP sizes: 1140 variables (300 integer), 573 constraints; HiGHS via scipy 1.16.
Wheat-buy price feedback triggered in all three scenarios
(S1 bought 142, end price $42→$46; S2 bought 466, $45→$54; S3 bought 101, $39→$42);
the tables above are the post-feedback solves.
Sanity anchor: the model's S1 bank ($132k) sits between the leader's real $150k (a better
seller than the model's conservative slot pricing) and half of it, and the model's implied
play mirrors his measured season: hands 8.1 vs 9.6 units/day, cows 9 vs 10, sheep 6 vs 4,
strawberry 29 vs 34, fertilizer sold 145 vs 249, wheat grown-and-bought in both.

---

## 2026-08-16 — Allocation bounds, pass 2: narrower bands, per-draw policy, best response

Folded in from `docs/allocation_bounds_pass2_2026-08-16.md`.

2026-08-16.
Model: `scripts/allocation_bounds.py` (modes `attrib`, `policy`, `br`; pass-1 `scenarios`
mode unchanged).
Logs: `data/logs/allocation_bounds_pass2_attrib.log`, `..._policy.log`, `..._br.log`.
Ground truth remains the installed `kaggle-environments 1.32.7` kaggriculture module
(byte-identical to the main repo's `reference/kaggriculture.py`; the worktree copy of
`reference/` is stale and was not used).

### Headline

- The bands narrowed 24-32% from modelling fidelity (items 2+4), essentially 0% from the
  solver gap at the 1% tolerance, and a further ~25% by reporting at 0.1%:
  WHEAT [15, 185] -> [23, 135], CARROT [0, 144] -> [0, 86] (combined model, 0.1%).
  What width remains at 0.1% is genuine economics: carrot and tomato are near-zero-margin
  crops whose lower bound really is 0.
- The per-draw policy table is the actionable output: the optimal mix swings from
  SHEEP 20 / STRAWBERRY 9 (YARNx4 draw) to STRAWBERRY 28 / COW 9 (SMOOTHIEx4 draw) to
  GOOSE 6 / CARROT 37 (BAKERY+PET draw).  No fixed allocation is near-optimal across draws.
- MELON 20 / STRAWBERRY 34: melon 20 lies inside the 1% outer interval of every draw solved;
  strawberry 34 only under smoothie-heavy draws.  The JOINT point always costs more than 1%:
  3.7% under the actual draw and 13-15% under the others.
- Best-response iteration: every quantity except melon is stable from iteration 0
  (STRAW 26-30, COW 9-10, SHEEP 5-6, WHEAT 79-85, GOOSE 0-2); melon see-saws
  7 -> 18 -> 11 -> 12 tiles against opponent melon 120 -> 42 -> 108 -> 66, a contracting
  oscillation around ~12-14 tiles per player with combined sales pinned near the 188-unit
  season cap.  MELON 20 is the exploitable side of that fixed point: the best response to a
  20-tile melon opponent is 7 tiles, not 20.

### What was already in pass 1 (so it is not re-claimed here)

- Feeding consumes wheat: the herd's 1 wheat/animal/day comes from grown wheat (usable the
  morning after harvest) or market buys at the simulated day price; the S1 optimum grew 93
  wheat cycles and still bought 142 units.  Herd and crops were never independent.
- Animal yield schedules are simulated from the reference rules exactly, including
  `max_held` caps and the harvest cadence they force: cow first 6 milk at day+8 then 3/2d
  (harvest every 4 days), sheep first 6 wool at day+6 then 4/3d, goose first 4 eggs at
  day+4 then 2/d (harvest every 2 days).  Self-check asserts pin these.
- Fertilizer is a real lever with turn cost: COLLECT_FERTILIZER is 1 op per unit (max
  1/animal/day), fertilised crop variants carry their FERTILIZE ops and usage, and
  fertilizer is sellable (S1 optimum collected 335, used ~190, sold 145).
- Hire cost is the exact per-day fibonacci sum via a convex slot formulation, so hiring is
  lumpy and cash-timed in the model too.  (The reference's silent `_do_hire` failure on a
  short bank is an execution hazard, not a planning constraint; the model's bank >= 0 per
  day guarantees the plan never walks into it.)

### Corrections to the tasking, from the reference

Two factual points in the tasking do not match the 1.32.7 rules, and the model follows the
rules:

1. Ongoing crops do NOT need water every single day.  `_daily_refresh_plants` weeds a tile
   at `consecutive_unwatered >= 2`, so watering every other day keeps any crop alive, and
   unfertilised ongoing production does not require watering at all (only the fertiliser
   bonus checks `watered_today`).
2. An ongoing tile's obligation is finite, not to season end.  After `max_yield`
   productions the plant's `max_lifespan_step` is set and it decays; a strawberry planted
   day d produces evenings d+9/11/13/15 and is dead wood from d+17.

Pass 1 therefore already charged per-day maintenance for ongoing crops:
strawberry_u = 8 waters + 1 harvest + 1 dig over 17 tile-days (0.59 ops/tile-day),
tomato_u = 6 waters + 1 harvest + 1 dig over 12 tile-days (0.75),
vs melon = 10 ops over 11 tile-days (0.91 — melon is the op-DENSEST crop per tile-day
because one-shot yield requires 5 window waters).
The 19-strawberry-weed game (93593633) was an execution failure — idle turns existed on the
two days before the die-off — not a cost the planner omitted.
What pass 2 adds for it is a DAILY-WATER robustness variant: every ongoing tile watered
every day (the execution-safe schedule), costed and attributed below.

### The four items, what each changed

#### Item 3 — solver gap vs tolerance

Pass-1 base solves stopped at 0.4-0.7% gap against a 1% band: part of every band was slop.
Pass 2 solves the base MILP at `mip_rel_gap 5e-4` (600 s), reports the attained gap, and
adds 0.1% bands.  Bands remain LP-relaxation OUTER bounds with the floor on the incumbent
(floor = (1-tol)*Z_inc <= (1-tol)*Z_true, so outer validity is preserved); the attained gap
is the amount by which each band is still wider than the true-economics band.

#### Item 2 — ongoing maintenance (daily-water variant)

Profiles rebuilt with every ongoing tile watered daily (strawberry_u 8 -> 16 waters,
tomato_u 6 -> 11).  This is the execution-safe schedule that would have prevented the
weed die-off.

#### Item 4 — geometry walk model

The flat 1.254 move-turns per work op is replaced by:
1 move per tile VISIT (serpentine adjacency: consecutive worked tiles are neighbours), where
a crop op is one visit but an animal pen's whole daily block (feed+care+collect+harvest)
shares ONE visit; plus a fixed 8 moves per unit-day transit (the mean Manhattan distance
from a shed-access corner to a tile of its quadrant is exactly 4.0 each way, dawn out and
dusk walk-home-and-drop).
This prices animals cheaper per op and crops dearer than the flat average, which is the
"feasible on average" failure the flat model had.  The solution's implied move/work ratio
is printed against the tape's 3477/2773 = 1.254.
Note the geometry gives NO between-quadrant differentiation: the shed is central, so all
four quadrants have identical distance distributions — the Nth TILE is not further, only
the Nth VISIT costs another move.

#### Item 1 — per-draw policy

One correction to the premise: the pass-1 bands were ALREADY per-draw (S1 used the actual
92498144 draw); the 2.4x Z* swing across draws widened nothing in them.  What per-draw
solving adds is the POLICY: per draw, the clairvoyant optimal mix and its band — the
"given this draw, plant this" table.  Draws are sampled exactly as the env draws them:
8 instances at days 3,6,...,24, uniform over sorted(SHOPS) WITH replacement.
Opponent supply is held at the leader's recorded fills for every draw (his fills were a
response to the actual draw; SPECULATION: against a draw-adapted opponent the contested
books would be tighter than modelled).

### Town demand caps, explicit

Season units the shared book can absorb before the price floor, actual draw
(cap = town drain + surplus room above I0 until price 1; both players share it):

    product     drain  floor_room   season cap   price at I0+50  at I0+150
    WHEAT         390       >5000            -              22        21
    CARROT        156         842          998              27        21
    TOMATO        246         529          775              42        29
    STRAWBERRY    624          62          686              24         1
    MELON          30         158          188             225        25
    EGG            30       >5000            -              43        41
    MILK          588          76          664              55         1
    WOOL          246          59          305              55         1
    FERTILIZER      0         493          493              90        70

Demand-limited products: MELON (188 — the leader alone sells 120), WOOL (305),
FERTILIZER (493).  Labour-limited: WHEAT, EGG (price never floors).
STRAWBERRY/MILK sit in between: huge drain under this draw but a cliff just past it.
Shed capacity (100) never binds: the largest single-day harvest in any pass-2 base solution
is printed per run ("peak daily harvest") and stays under the cap, and sales settle the
same day the slot fires.

### Attribution: one item at a time (S1, actual draw, opponent = leader fills)

Each variant changes exactly one thing against the recomputed pass-1 baseline V0.
1% band WIDTHS (upper minus lower, LP outer bounds):

    item        V0 pass1   V1 tight-gap   V2 daily-water   V3 geom-walk   V4 combined
    WHEAT          169.6         169.7           153.6           146.7          128.7
    CARROT         144.3         144.3           127.8           113.7           97.8
    TOMATO          68.1          68.1            57.6            62.9           50.5
    STRAWBERRY      34.3          34.3            30.1            32.4           28.0
    MELON           31.2          31.2            28.8            28.6           26.1
    GOOSE           14.5          14.5            12.6            14.6           12.2
    COW             10.9          10.9             9.2            10.1            8.1
    SHEEP           10.7          10.7             9.4            10.2            8.4

    Z*          $129,045      $129,046        $127,578        $125,807       $123,827
    gap attained   0.40%       <=0.05%           0.20%           0.88%          0.09%

Attribution, stated plainly:

- Item 3 (gap): moved the 1% bands by 0.0-0.1 units.  The pass-1 1% bands were economics,
  not solver slop.  Where the gap DOES pay is the 0.1% tolerance: V4's 0.09% attained gap
  makes the 0.1% bands meaningful (effective tolerance <= 0.19%); under V0's 0.4% gap they
  were slop-dominated.
- Item 2 (daily-water on ongoing crops): -9% to -16% width on the crops that compete with
  ongoing for labour; Z* -1.1%.  Strawberry_u goes 8 -> 16 waters, tomato_u 6 -> 11.
- Item 4 (geometry walk): -3% to -21% width; Z* -2.5%.  The model's implied move/work
  ratio is 1.43-1.47 vs the tape's 1.254 — the geometry charges MORE than the flat model
  (transit for every unit-day dominates), so it is conservative, and it penalises
  crop-heavy, visit-dense mixes specifically (wheat/carrot narrowed most).
- Combined: -16% (melon) to -32% (carrot) width at 1%.

### The narrowed bands (combined model V4, S1, actual draw)

    item         base       0.1% band        1.0% band        5.0% band   leader
    WHEAT          83     [23, 135]        [15, 144]        [0, 178]         -
    CARROT         10     [0, 86]          [0, 98]          [0, 144]         -
    TOMATO         22     [0, 46]          [0, 51]          [0, 65]          -
    STRAWBERRY     28     [17, 40]         [15, 43]         [6, 55]         34
    MELON           7     [0, 23]          [0, 26]          [0, 38]         20
    GOOSE           2     [0, 10]          [0, 12]          [0, 19]          0
    SHEEP           6     [5, 11]          [4, 13]          [3, 18]          8
    COW             9     [7, 14]          [7, 15]          [5, 20]          6

Pass-1 vs pass-2 at 1%: WHEAT [15,185] -> [15,144], CARROT [0,144] -> [0,98],
TOMATO [0,68] -> [0,51], STRAWBERRY [15,50] -> [15,43], MELON [0,31] -> [0,26],
COW [6,17] -> [7,15], SHEEP [4,15] -> [4,13], GOOSE [0,15] -> [0,12].

### Per-draw policy (combined model, opponent = leader's recorded fills for every draw)

    draw                          Z*     W   C   T   S   M   G  Co  Sh   MELON 1%   STRAW 1%   20/34 pin
    actual  FARMERS,ICE,PIZZA,
            SMOOTHIEx4,YARN   $123,579  88  12  23  28   6   1   9   6    [0, 27]   [14, 43]      3.70%
    rng11   BRUNCH,FARMERSx2,
            ICE,YARNx4         $81,286  96  19  25   9   7   2   0  20    [0, 23]    [0, 22]     14.62%
    rng12   BAKERY,FARMERS,PET,
            PIZZAx2,SMOOTHIE,
            YARNx2            $103,883  74  37  38   3  12   6   2  10    [1, 26]    [0, 17]     13.69%
    rng13   FARMERSx4,ICEx2,
            PETx2              $73,048  65  13  37  29  13  12   0   0    [4, 25]   [20, 44]      3.66%
    rng14   BRUNCHx2,ICE,
            PETx4,YARN         $65,629  94  43  10   9  12  16   0   3    [0, 32]    [0, 29]     12.23%
    rng15   BAKERYx4,FARMERSx2,
            ICEx2              $63,876  81  33  30  13   9  13   0   0    [0, 30]    [0, 32]     12.31%

The policy reading across all six draws: the draw is revealed one shop every 3 days from
day 3, and the first 2-3 shops carry most of the signal.  Wool-heavy draws (YARNx2+) flip
the pen mix to sheep and kill strawberry; goose becomes the herd (12-16 birds) whenever
the draw gives neither milk nor wool demand (PET/BAKERY-heavy: rng13/14/15 all have
COW=0); strawberry >= 20 is only optimal under smoothie/ice-cream/farmers-market demand.
Melon's optimum is 6-13 tiles in EVERY draw — melon has no shop, so no draw ever rescues
a 20-tile melon commitment against an opponent who also sells 120 melons.
The 20/34 pin costs 3.7% under the two draws closest to his real game and 12-15%
elsewhere.
Z* across draws spans $64k-$124k (1.9x) with the opponent held fixed: most of the
pass-1 "scenario spread" was demand, not opponent.

### The leader's measured trigger, against this model

Measured on his 67 games (briefed 2026-08-16 14:21): melon at day 9 is bimodal 12 or 20,
melon + strawberry always 31, and the switch is the OPPONENT'S day-3 melon count
(>= 9 -> 12/19, < 9 -> 20/11), separating the populations with zero errors.

That is precisely the structure this model derives:

- Best response to a melon-flooding opponent: 7-12 melon tiles (BR iterations 0/2/3 vs
  opponent melon 120/108/66).  His contested mode is 12.
- Best response to a low-melon opponent: 14-27 tiles (S2 base 27, 1% band [14, 42];
  BR iteration 1 vs opponent melon 42: 18).  His uncontested mode is 20 — inside the
  band, on its cautious side.
- The BR fixed point ~12-14 tiles per player is exactly his contested mode, and the
  contracting oscillation explains why a trigger at day 3 (before any melon exists on
  the board — the earliest melon harvest is day 10, so day-3 melon count means PLANTED
  tiles, which are visible) is the right instrument: commit to the low-melon branch only
  once the opponent is seen to have committed to the high one.
- What the model does NOT reproduce is the constant sum melon + strawberry = 31.
  Our per-draw optima put melon+straw at 22-42.  SPECULATION: his constant 31 is a
  fixed-labour-block swap (8 tiles retasked between two crops with near-equal daily
  maintenance), which keeps his opening script and crew size unchanged — an execution
  constraint, not a market optimum.

Consequence for the brief: the "optimal fixed allocation" question is settled as moot —
the leader himself does not play one, and the model agrees no fixed melon count is
near-optimal against both of his modes.  The deliverable that stands is the per-draw,
per-opponent-mode policy: melon 12 contested / ~20 uncontested, strawberry filling the
demand the draw provides, herd species from the draw's milk/wool/egg demand.

On the fourth quadrant: he buys it in 21/67 games, independent of the crop swap.
This model chooses parcels endogenously and lands on 2 parcels (75 tiles) in the S1
optimum and 3 (100 tiles) in S2 — the marginal parcel tracks total demand, which is
consistent with an independent-of-crop-swap decision.  Tile budget was never binding at
75 in the S1 base (peak concurrent occupancy ~60), so the 4th-quadrant purchase is about
demand-rich draws, not about the melon/strawberry swap.

### Best-response iteration (combined model, actual draw, start = leader's fills)

    iter   opp MELON/STRAW/MILK    our mix (W,C,T,S,M,G,Co,Sh)      our Z*     our melon sold
    0        120 / 223 / 279      85,10,24,27, 7, 1, 9, 6         $123,484        42
    1         42 / 216 / 297      85,11,10,27,18, 1,10, 5         $120,369       108
    2        108 / 216 / 303      79,10,20,26,11, 2,10, 6         $119,185        66
    3         66 / 208 / 306      85,13,15,30,12, 0,10, 5         $119,606        72

Melon is the only strategically live quantity; the oscillation contracts (120/42 ->
108/66) toward ~12-14 tiles (~70-85 units) each, combined ~150 units against the 188-unit
season cap.  Everything else is a fixed point from the first iteration.
Gap caveat: iteration solves attained 0.1-0.3% gaps against differences of $1-4k between
iterations, so the melon trajectory is solver-noise-free; the +/-1 wobbles in
tomato/carrot are within gap and not meaningful.
SPECULATION: the symmetric equilibrium melon is 12-14 tiles per player; proving it needs a
simultaneous (not alternating) solve.

### Residual model risks

- The geometry walk model overcharges movement relative to the tape (1.43-1.47 vs 1.254
  measured), so pass-2 Z* and bands are conservative on labour.
- Peak daily harvest in the base solutions is 170-207 units against a shed capacity of 100.
  Sales settle the same day the slots fire, and DROP is capped at capacity without
  discarding (mid-day overflow stays in unit inventories; only the END-OF-DAY drop
  discards), so the plan is executable — but it requires intra-day drop/sell sequencing on
  ~3-5 peak days, which the model does not schedule.  An agent that dumps everything at
  dusk would lose the overflow.
- Opponent supply is the leader's recording under every draw; his real play would adapt.
- LP-relaxation bands remain OUTER bounds; the joint-point pin checks close that gap only
  at the specific tested points.

### Run facts

attrib 2734 s (5 variants), policy 3294 s + 2150 s (first launch killed by the runner
after 3 of 6 draws; remaining 3 in `allocation_bounds_pass2_policy2.log`, run at
time-limit 250 s / gap 1e-3 — their gaps 0.1-0.5%), br 1802 s (4 iterations).
MILP: 1104-1140 vars (264-300 int), 573 constraints; HiGHS mip_rel_gap 5e-4 targeted,
attained per solve as printed in the logs.

---

## 2026-08-16 — カワシギ's decision points, scored as selectors

Folded in from `docs/decision_points_2026-08-16.md`.

2026-08-16.
Script: `scripts/decision_points.py`.
Log: `data/logs/decision_points.log`.
Machine-readable result: `data/logs/decision_points.json`.
Classification cache: `data/logs/decision_points_classify.json`.

### What was measured, and why this is not the separation table again

The belief under test is that the #1 player's season is a fixed tape plus a small number of binary
decisions taken off the board.
A previous analysis reported the *separation* table -- the rule cleanly splits his own games -- as if
it were a result.
It is not.
A rule that separates 51 games perfectly and does not beat the better of the two branches it selects
between is worth nothing.

So each decision point has three arms, and the arm under test is the third:

    always-A    play branch A's tape for the whole season
    always-B    play branch B's tape for the whole season
    selector    play A up to the decision turn, then switch to B if the rule fires

Every arm is a RECORDED TAPE on our seat.
Our own planner is not in the measurement at all.

Method, in one list:

- 96 seeds x 2 seats per arm = **192 games per arm, 1,152 games total**.
- Both seats, always. `_process_market` walks player 0 then player 1 per unit, so a tape moved to
  the other seat loses price priority. Identical policies do not draw here.
- `weedSpawnChance = 0.005`, the ladder value.
- One OS process per game (`--child` subprocess).
- Opponent: `data/sweep/frozen_1186_opponent.py`, a built bundle loaded by path with
  `importlib.util.spec_from_file_location`. It carries its own module copies and cannot share dials
  with the arm under test. No arm is ever the opponent.
- **Win rate is the score.** Money is printed as a diagnostic column only.
- Noise floor `2*sqrt(0.25/192) = 7.2%`. Anything smaller is a null, not a small effect.

**Every arm is open-loop and therefore handicapped.**
A tape cannot react to an opponent it never met.
A tape arm that WINS has won despite that handicap; a tape arm that loses proves less.
The comparison *between* arms is still fair, because the handicap is the same for all three.

### Classifying his 51 games

`data/seed_scripts/downloads_2026-08-13/` holds 79 JSON files.
Two of them (`91304798-0.json`, `91304798-1.json`) are bare step lists with no `info` block, so the
seat cannot be identified and they are skipped rather than guessed.
Of the remaining 77, **51 contain カワシギ**, which matches the brief.

Counting his own PLANT emissions -- a PLANT is emitted once, unlike a market order our agent
re-posts every turn:

```
  MELON  STRAW         WHEAT  games   episodes
     20     34       120-147     41   91889284 91890202 91892046 91893908 91894829 91895772 ...
     12     42       117-130      9   91891131 91892982 91896693 91897619 91898549 91899475 ...
     20     33       159-159      1   91918341
```

**The brief's 42/9 split is 41/9 plus one outlier.**
41 games are exactly MELON 20 / STRAWBERRY 34.
One more (`91918341`) is MELON 20 / STRAWBERRY 33 with WHEAT 159, well outside the 120-147 wheat
range of the melon-heavy class -- a different game, not a rounding difference.
The 9-game strawberry-heavy class matches exactly.

He wins 47 of these 51 games.

#### The d3 rule does separate his games -- 51/51

Opponent MELON tiles at dawn of d3 (turn 72), read off his own replays:

```
  MELON/STRAW  games  opp melon d3 min   max  >= 9  YARN by d6
        20/34     41                 4     8      0       15/41
        12/42      9                 9    13      9        1/9
        20/33      1                 5     5      0        1/1
```

The two classes do not overlap and do not touch: melon-heavy tops out at 8, strawberry-heavy starts
at 9.
The threshold of 9 separates all 51 games.
**This is the hypothesis, not the result.** The result is further down.

#### Representative tapes

Chosen as the game whose per-day action hashes agree with its class's modal day script on the most
days, ties broken on the episode name.
Deliberately **not** the richest game in the class: selecting the representative on money would put
the branch's luckiest board into the arm and then credit the branch with the board.

| decision point | branch | episode | why | his result in that game |
|---|---|---|---|---|
| dp1 | A, melon-heavy (MELON 20 / STRAW 34, 41 games) | `91919278` | agrees with the class's modal day script on 20/30 days | seat 1, $79,486 vs $80,026 |
| dp1 | B, straw-heavy (MELON 12 / STRAW 42, 9 games) | `91891131` | agrees with the class's modal day script on 21/30 days | seat 1, $67,971 vs $1,142 |
| dp2 | A, three-quadrant | `92498144` (`data/seed_scripts/kawashigi/`) | given in the brief | - |
| dp2 | B, four-quadrant | `91907974` | given in the brief | seat 0, $88,763 vs $49,859 |

Caveat on `91891131`: his opponent in that game collapsed to $1,142, so his own bank there says
little. It is used only as a source of *actions*, never of a result.

#### The four-quadrant herd is COW 6 / SHEEP 10, not COW 6 / SHEEP 8

Read from the final observation of `91907974`:

    herd  COW 6, SHEEP 10          tiles owned  100
    crops WHEAT 142, MELON 20, STRAWBERRY 34, CARROT 7
    YARN_STORE unlocked by d6: True

The sheep count in the brief is wrong by two.
Note also that `91907974` is itself a **melon-heavy** game (MELON 20 / STRAW 34), so dp2's branch B
is not a strawberry-heavy tape.

#### Splice validity

A selector splices two tapes at a turn. That is only exact where the two tapes agree before it.

```
  dp1  72/72 turns identical before the switch, no difference anywhere in d0-d2
  dp2  170/216 turns identical before the switch, first difference at turn 96 (d4)
```

dp1's splice is **exact**: the two branches are byte-identical for the whole opening, so the
selector arm is one season with a fork in it.

dp2's is not. The two tapes already differ on d4, so `dp2/selector` is a hybrid of two seasons and
carries an extra handicap that neither constant has. That matters for reading its number: it is a
lower bound.

### Result

Opponent `data/sweep/frozen_1186_opponent.py`, `weedSpawnChance 0.005`, 96 seeds x 2 seats.

```
arm                   games     WIN   draw   loss  mean $ (diag)  mean margin  B fired
--------------------------------------------------------------------------------------
dp1/always-melon        192   62.5%   0.0%  37.5%         89,381         +990
dp1/always-straw        192   60.4%   0.0%  39.6%         90,871       +1,067
dp1/selector            192   60.4%   0.0%  39.6%         90,871       +1,067     100%
dp2/always-3q           192   52.6%   0.0%  47.4%         86,455       -1,420
dp2/always-4q           192   19.3%   0.0%  80.7%         80,196      -13,701
dp2/selector            192   62.0%   0.0%  38.0%         86,896         +234      16%

noise floor 2*sqrt(0.25/n) at n=192 is 7.2%. Anything smaller than that is a NULL.
```

```
point  better constant       its WIN  selector WIN    delta  paired W-L   sign p  does the selector beat it?
------------------------------------------------------------------------------------------------------------
dp1    dp1/always-melon        62.5%         60.4%    -2.1%       31-35    1.000  NO -- and UNTESTED (see below)
dp2    dp2/always-3q           52.6%         62.0%    +9.4%        19-1    0.000  YES
```

The paired columns compare the selector with the better constant on the same (seed, seat).
They are secondary to the noise floor and are reported because the two arms share every board and
are byte-identical wherever the rule did not fire, which makes an unpaired floor over all 192 games
the wrong yardstick for them. A sign test on a handful of discordant pairs is not proof either.

### Verdict, decision point 1 -- melon vs strawberry at d3: NO, and the test did not run

`-2.1%`, inside the 7.2% floor. But the number is not the point.

**The rule fired on 100% of the 192 games.**
`frozen_1186_opponent.py` plays カワシギ's own schedule, which buys MELON 12 on d0, so it holds
**12 melon tiles at dawn of d3 on every seed** -- measured directly, seeds 1, 2, 3 all read 12.
The threshold is 9.
So `dp1/selector` is byte-identical to `dp1/always-straw` by construction, and its row reproduces
that arm to the dollar ($90,871 on both, 60.4% on both, 0 discordant pairs against it).

**This is a fact about the opponent, not evidence about the rule.**
A delta of 0.0 against a constant that the selector *is* reads exactly like a measured null, and
must not be recorded as one.

The mandated opponent is effectively a mirror of the player whose rule is being tested, and a mirror
cannot exercise a rule that keys on the opponent's crop mix.
For reference, the two branch tapes are also indistinguishable from each other here: melon-heavy
62.5% vs strawberry-heavy 60.4%, a 2.1% gap inside the same 7.2% floor.

To actually test dp1, a **built bundle** opponent holding fewer than 9 melon tiles at d3 is needed.
None exists in `data/sweep/`. The `cand_*.py` files there look like candidates but are not usable:
they `import kagg.search.schedule_agent` live and set module-level dials, which would overwrite the
arm under test in the same process, and their entry point takes `(obs, config)` and raises
`KeyError: 'step'` when called with a turn index. One would have to be built with
`scripts/build_planner_submission.py` and a melon-reducing dial.

### Verdict, decision point 2 -- four quadrants at d6: YES

`+9.4%` over the better constant, above the 7.2% floor, paired 19-1 (sign test p < 0.001).

The split by whether the rule fired is what makes it readable:

```
subset          games         always-3q       always-4q        selector
fired              30        3/30 = 10%     23/30 = 77%     21/30 = 70%
did not fire      162      98/162 = 60%     14/162 = 9%    98/162 = 60%
```

This is a clean interaction, not a main effect.

- The four-quadrant tape is a **disaster** as a constant: 19.3% over the season, 9% on the boards
  where YARN_STORE has not unlocked by d6.
- On the 30 boards where YARN_STORE *has* unlocked by d6, it inverts completely: 77% against the
  three-quadrant tape's 10%.
- `YARN_STORE in town.unlocked_shops` at the last turn of d6 identifies exactly those boards, and
  the selector converts a 10% subset into a 70% one.
- On the 162 boards where it does not fire, the selector is identical to `always-3q` by
  construction, which is why the whole-set delta (+9.4%) is much smaller than the subset delta
  (+60 points) -- the whole-set number is diluted by the 84% of games the rule never touches.

Two things bound this result:

1. The selector reaches 70% on the fired subset where `always-4q` reaches 77%. The 7-point gap is
   the splice: the selector plays the three-quadrant opening (d0-d8) and then the four-quadrant
   tape, and those two tapes already differ at d4. A tape solved as one season would presumably do
   better. **70% is a lower bound.**
2. The rule fired on 30/192 = 15.6% of our seeds, consistent with the project's existing "15 of 100
   seeds" note. In his own 51 games it fired on 17/51 = 33%. Those are different populations (our
   seeds 1-96 versus his ladder boards) and I have not checked why they differ. On the ladder the
   payoff scales with whichever rate is real.

### What this does and does not license

- dp2 is a **real, measured, positive selector**, and it is the first thing in this line of work
  that beats its own better constant rather than merely separating his games.
- dp1 is **open**. The separation is perfect and the mechanism is plausible (melon is the one crop
  no shop buys, so its price is set entirely by what the two farms dump into the town book), but no
  measurement has been taken. Do not carry the separation table forward as support for it.
- Nothing here says our live planner should adopt either branch. Every arm was a tape.

---

## 2026-08-16 — Marginal units, the shared book, and what the shop draw is worth

Folded in from `docs/marginal_units_and_the_shared_book_2026-08-16.md`.

Measured 2026-08-16 on branch `kawashigi-plan` at `3f9fb83`.
All seasons are the straw arm, our live agent in seat 0, Kawashigi's recorded actions in seat 1,
`weedSpawnChance=0.0`, one season per arm.
Logs: `data/logs/pricedist_fert_off.log`, `data/logs/pricedist_fert_on.log`,
`data/logs/shop_draws_by_seed.log`, `data/logs/goose_tomato_arms.log`,
`data/logs/goose_late_arms.log`.

### 1. Revenue is the wrong objective, and it reversed a decision

The fertilizer sell exemption (`prod not in NEVER_DRAINED`, `NEVER_DRAINED = ("FERTILIZER",)`,
which lets fertilizer sell before `LATE_SELL_FROM_HOUR = 16`) was measured on seed 11 both ways.

Ours, revenue by product:

| product | fert OFF | fert ON | delta |
|---|---:|---:|---:|
| WOOL | 42,871 | 42,051 | -820 |
| WHEAT | 19,925 | 20,408 | +483 |
| FERTILIZER | 14,302 | 14,612 | +310 |
| MELON | 14,179 | 14,179 | 0 |
| MILK | 12,006 | 8,058 | -3,948 |
| STRAWBERRY | 10,942 | 5,970 | -4,972 |
| CARROT | 704 | 806 | +102 |
| **TOTAL** | **114,929** | **106,084** | **-8,845** |

Theirs:

| product | fert OFF | fert ON | delta |
|---|---:|---:|---:|
| WHEAT | 45,222 | 43,963 | -1,259 |
| WOOL | 20,954 | 20,715 | -239 |
| MILK | 18,130 | 12,117 | -6,013 |
| MELON | 16,648 | 16,648 | 0 |
| STRAWBERRY | 10,434 | 3,917 | -6,517 |
| FERTILIZER | 8,972 | 8,820 | -152 |
| **TOTAL** | **120,360** | **106,180** | **-14,180** |

Banks: ours 80,581 -> 71,254 (-9,327), theirs 61,474 -> 48,117 (-13,357),
**margin +19,107 -> +23,137 (+4,030)**.

Fertilizer's own revenue moves **+$310**. The exemption does not work by selling fertilizer better.
It frees the h0-h15 window, and the knock-on collapses the strawberry and milk books for **both**
players. We lose $8,920 on those two lines; he loses $12,530. We bank less and win by more.

**This is why a revenue table must never be used to rank an arm.** The same mistake had already
been made twice in one session: the new 4-board solve was shelved partly because it showed
STRAWBERRY $67,838 against the committed routes' $10,942, and that comparison measures nothing.
Only the margin, or the win, counts.

The exemption is **not** unconditionally good. On seed 3 it is **-2,081**. The rematch corpus put it
at 69/97 against 66/97 (7 gained, 4 lost, p~0.27). It is not established.

### 2. The book is shared, so our own count is not the lever

Seed 11, both seats, units into the same town inventory against the shops that drain it:

| product | ours | theirs | total | shop-slots draining it | our $/unit |
|---|---:|---:|---:|---:|---:|
| MILK | 186 | 249 | 435 | 1 | 64 |
| WOOL | 189 | 94 | 283 | 1 | 227 |
| STRAWBERRY | 277 | 261 | 538 | 4 | 40 |
| WHEAT | 469 | 1,062 | 1,531 | 6 | 42 |
| EGG | 0 | 0 | 0 | 6 | -- |

Milk is at the floor because 435 units go into one shop's worth of drain and **249 of them are
his**. Cutting our own cow count cannot fix a book he floods anyway. Wool holds $227 on the same
single slot only because 283 units exist in total.

### 3. Drain is not what sets the price -- supply is

Mean shop-slots draining each product, over seeds 1-40 (`data/logs/shop_draws_by_seed.log`):

| product | mean slots |
|---|---:|
| WHEAT | 5.22 |
| STRAWBERRY | 3.85 |
| MILK | 3.17 |
| EGG | 2.05 |
| TOMATO | 1.95 |
| CARROT | 1.65 |
| WOOL | 1.12 |

**WOOL is the least-drained product in the game and our best-priced at $227/unit.** So "is this a
good seed for crop X" cannot be read off the shop draw alone. What matters is units already in the
book, and the draw only matters where the book is contested.

Seed 11 is the extreme egg seed of the sample: `BRN BAK BRN BAK YRN BAK BRN SMO`, six of eight
shops draining EGG, zero draining TOMATO or CARROT.
Seed 3 is the best tomato seed of the sample: `BRN YRN ICE PIZ FRM FRM PIZ PIZ`, five slots.

### 4. One wheat tile to tomato: a null on both seeds

`WHEAT_TILES_TO_TOMATO = 1`, margin against the same base:

| seed | base | tomato1 | delta | tomato sold |
|---|---:|---:|---:|---|
| 11 (TOM 0 slots) | +19,107 | +19,093 | **-14** | 8 units @ $91 |
| 3 (TOM 5 slots) | +6,602 | +5,579 | **-1,023** | 7 units @ $63 |

On top of the fertilizer exemption: seed 11 -2,702, seed 3 +835.

So the answer is no, including on the best tomato seed in a 40-seed sample. The earlier
`WHEAT_TILES_TO_TOMATO = 24` result (49/97) was read as "flooding is bad, one unit might be fine".
One unit is not fine either. It is simply worth nothing.

**And it cannibalises carrot.** On seed 3 the base sells 12 CARROT at **$265/unit** -- our best
per-unit line on that board, better than wool -- and the tomato arm drops it to 11 units at $122.
Carrot at 12 units is the underexploited line here, not tomato.

### 5. One goose on a cow: the d0 result is an artifact, again

`HERD_GEESE = 1`, `HERD_GEESE_FROM = ("COW",)`. The swap took the **d0 cow at places index 1**:

    d0: BEFORE places ['SHEEP','COW','SHEEP','COW']   bought {COW:2, SHEEP:2}
         AFTER places ['SHEEP','GOOSE','SHEEP','COW']  bought {COW:1, SHEEP:2, GOOSE:1}

Margin seed 11 +19,107 -> **-12,494**. Seed 3 +6,602 -> **-2,801**.

That is not the goose. The eggs behaved exactly as predicted -- 54 units at $53 into an empty book,
$2,862 of revenue on both seeds. The damage is wool:

| | units | $/unit | revenue |
|---|---:|---:|---:|
| base | 189 | 227 | 42,871 |
| goose1cow | 88 | 53 | 4,664 |

**Wool fell $38,207.** A COOP displaced the COW that commit `3f9fb83` had just paired with the first
sheep on the prime zero-walk cell, and the sheep's feed/care cadence broke. `pending_care_bonus`
only rises on a night both fed and cared (`reference/kaggriculture.py:823`), so a broken pairing
halves the yield of the best product on the board.

This is the sixth time an animal verdict here has been an artifact of something the code could not
express or something unrelated that broke. See `CLAUDE.md` and
`project_kaggriculture_animals_verdict`.

The schedule buys cows on d0, d3, d5, d7, d9 and d11 -- ten cows and four sheep -- so the goose
should be able to take a late cow and leave the d0 pen untouched.

**It cannot. Every late swap is a no-op.** Margins on seeds 11 and 3, five arms
(`data/logs/goose_late_arms.log`, `data/logs/goose_d3_arms.log`):

| arm | seed 11 | seed 3 |
|---|---:|---:|
| base | +19,107 | +6,602 |
| goose1@d3 | +19,107 | +6,602 |
| goose1@d5 | +19,107 | +6,602 |
| goose1@d9 | +19,107 | +6,602 |
| goose2@d9,d11 | +19,107 | +6,602 |

Byte-identical, every product line included. `swap_in_geese` itself is fine -- called directly it
rewrites the right row at every floor:

    EARLIEST=(0,...)  d0  ['SHEEP','COW','SHEEP','COW'] -> ['SHEEP','GOOSE','SHEEP','COW']
    EARLIEST=(3,...)  d3  ['COW']                       -> ['GOOSE']
    EARLIEST=(5,...)  d5  ['COW']                       -> ['GOOSE']
    EARLIEST=(9,...)  d9  ['COW','COW']                 -> ['GOOSE','COW']
    EARLIEST=(11,...) d11 ['COW','COW']                 -> ['GOOSE','COW']

The rows are simply never acted on. Censused over a full season on seed 11, base and `goose1@d5`
emit exactly the same orders:

    BUY_ANIMAL: {COW: 4, SHEEP: 4}
    PLACE     : COW 6, SHEEP 8, FERTILIZER 6, WOOL 1

**The schedule asks for ten cows and four sheep. The live agent buys four and four.** The purchase
path is not `animals_bought` per row: `want_total` is a cumulative target
(`schedule_agent.py:4539`), and from `SHOP_ADAPT_FROM_DAY` on, `SHOP_ADAPT_HERD` overwrites
`want_total["COW"]` and `want_total["SHEEP"]` outright from `_herd_split` (`:4556-4588`). A GOOSE
inserted into a row it never reads changes nothing.

So the only swap that bites is d0, and d0 is the one that breaks the sheep pairing. **The goose
question remains unanswerable without a change to the purchase path** -- `_herd_split` decides a
two-species split and there is no third slot for a bird. That is a code change, not a flag.

Second finding, worth more than the goose: we run **four cows**, not eight or ten. The user's
"8 is too much on some boards" is already true at four -- 186 units of milk from four cows into a
book the opponent adds 249 to.

### What this closes and what it opens

- **Closed:** one wheat tile to tomato, on a dead tomato seed and on the best tomato seed. Null and
  a small loss. Do not retry at any small count.
- **Closed:** revenue as a ranking statistic for any arm.
- **Void, not closed:** the goose. The only two goose measurements this project has ever taken were
  both confounded -- the first by `SELLABLE` omitting EGG, the second by the d0 pen.
- **Open:** carrot at $265/unit on seed 3 off 12 units.
- **Open:** ten cows into a book the opponent floods with 249 units of his own.

### 6. The counterfactual: our milk is a weapon, not a revenue line

The agent does not need changing to answer this. The season is played once, then the MARKET is
replayed under a counterfactual supply using the env's own `market_price` and its own per-unit
lockstep (`scripts/what_one_animal_is_worth.py`, logs `data/logs/counterfactual_cow_to_goose.log` and
`data/logs/counterfactual_by_seed.log`).

**The model is validated before it is used.** Replaying the recorded season reproduces it:

    item     replay ours   recorded ours   replay theirs   recorded theirs
    MILK          12,010          12,006          18,128            18,130
    WOOL          42,871          42,871          20,954            20,954

Two mechanics decide everything here, both read off `reference/kaggriculture.py`:

- `_commit_unit`: **"Sales at $1 do not increase market supply."** Flooding self-limits at the floor.
- EGG is `base 50, below_target 0.4`, so an egg can **never** fetch more than **$70**. MILK is
  `base 160, above_target 1.6`, ceiling $256, floor $1.

#### Take one of our four cows out, seed 11

    units ours   rev ours   $/unit  |  units theirs   rev theirs   $/unit
    base      186     12,010     64.6  |          249       18,128     72.8
    -1 cow    139     12,192     87.7  |          249       24,145     97.0
    delta     -47       +182           |                    +6,017

**Dropping a cow costs us $0 and hands him $6,017.** The 47 units lost are the $1 ones; the
remaining 139 reprice 64.6 -> 87.7 and cancel the loss exactly. His 249 units reprice 72.8 -> 97.0.

Our milk is not a revenue line. It is a **denial** instrument, and its value is proportional to
**his** volume, not ours. That inverts how every animal arm in this project has been judged.

#### It flips sign on the shop draw and on his volume

| seed | milk shops | egg shops | straw shops | his milk units | our milk units | denial value | our cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| 11 | 2 | 2 | 3 | 249 | 186 | +6,017 | +182 |
| 4 | 3 | 4 | 5 | 249 | 277 | +12,305 | +5,632 |
| 3 | 1 | 2 | 1 | 179 | 267 | +676 | -668 |
| 33 | 1 | 4 | 2 | 179 | 267 | +676 | -668 |

Cow -> goose, margin:

| seed | 1 egg/night | 2 eggs/night | 4 eggs/night |
|---|---:|---:|---:|
| 11 | -4,461 | -3,150 | -764 |
| 4 | -5,132 | -3,636 | -763 |
| 3 | +205 | +1,711 | +4,610 |
| 33 | +499 | +2,194 | +5,284 |

Where he lands 249 milk units the cow denies him $6k-$12k and no goose can replace it. Where he
lands 179 the denial is $676 and the goose wins. **The goose is a conditional buy, not a flat
yes or no** -- which is why every unconditional goose verdict this project has taken was wrong.

Cow -> strawberry, margin:

| seed | +22 units | +66 units |
|---|---:|---:|
| 11 | -2,995 | +1,195 |
| 4 | -2,315 | +4,553 |
| 3 | +244 | +2,158 |
| 33 | +1,485 | +6,334 |

**Positive on all four at +66, negative on two at +22.** Same mechanism: at volume our strawberry
denies him more than the milk did -- on seed 33 his strawberry revenue falls **-$5,019**. A half
swap gives up the milk denial without buying enough strawberry denial to replace it.

#### What this does not measure

- **One opponent.** Every seed is Kawashigi's tape, so his cow COUNT never varies. His milk units
  moved 179 vs 249 only as a price side effect. "It depends how many cows he has" is the right
  question and is **not answered here**; it needs a second opponent tape.
- **The strawberry arm is a market estimate, not a plan.** It assumes a cow's ~3 actions a day
  convert into +66 strawberry units. Whether the planner can grow and water them is unproven.
- Both arms hold all actions fixed. Correct for the opponent, whose fills are shed-limited; an
  approximation for us.

### 7. CORRECTION to sections 5 and 6: the herd count was wrong

**Section 5's claim "the live agent buys four cows and four sheep" is WRONG.** It came from counting
`BUY_ANIMAL` **orders** in the action stream -- the offers-are-not-fills mistake this project has a
standing rule against (`feedback_offers_are_not_fills`). The board census run beside it iterated
rows instead of cells, returned `{}`, and that empty result was not flagged.

Counted off the tiles, seed 11:

    end d 0  OURS {SHEEP 2, COW 2}   THEIRS {SHEEP 2, COW 2}
    end d 6  OURS {COW 4, SHEEP 2}   THEIRS {COW 4, SHEEP 2}
    end d 9  OURS {COW 6, SHEEP 4}   THEIRS {COW 8, SHEEP 3}
    end d20  OURS {COW 6, SHEEP 8}   THEIRS {COW 9, SHEEP 3}

**We run 6 cows and 8 sheep -- 14 animals. He runs 9 cows.** Placement days, both sides:

    OURS   COW d0x2 d3 d5 d7x2      SHEEP d0x2 d7 d8 d10x2 d12x2
    THEIRS COW d0x2 d3 d5 d7x4 d18  SHEEP d8

What this invalidates:

- per-cow yield is 186/6 = 31 units, not 46.5, so "his 249 milk is 5.4 cows" was wrong -- he has 9
- the section 6 counterfactual scaled our milk by 3/4; one cow out of six is 5/6, so every denial
  figure in that section is scaled wrong and must be re-run
- `the_best_answer_to_his_herd.py --pens 8` was clamped from the wrong number; it is 14

What survives: the goose row swaps are genuinely no-ops, and `SHOP_ADAPT_HERD` is why -- it
re-decides the schedule's 10 cows / 4 sheep into 6/8 and never reads a GOOSE row.

### 8. Production is exact, so the grid can be solved rather than sampled

`_daily_refresh_animals` (`reference:823`) makes a season's yield a pure function of species and
placement day, under best play (fed and cared every night, collected on every production day):

| animal | d0 | d3 | d6 | d9 | d12 |
|---|---:|---:|---:|---:|---:|
| COW | 39 | 33 | 30 | 24 | 21 |
| SHEEP | 38 | 34 | 30 | 26 | 22 |
| GOOSE | **56** | 50 | 44 | 38 | 32 |

Validated: our 6 cows on their real slots predict 202 milk against 186 sold (92%); 8 sheep predict
227 wool against 189 sold (83%). The shortfall is unfed nights and unsold stock.

**A goose out-produces a cow 56 units to 39** -- it just sells into a $70 ceiling instead of $256.

#### Both players 0..14 cows, seed 11 (`data/logs/cow_grid_exact.log`)

Margin in $k, our cow count down, his across, remainder sheep, purchase cost included:

    our\his     0     2     4     6     8    10    12    14
          0   0.9  -5.4   0.7   2.5   3.0   7.7   7.5   9.3
          2   8.5   1.8   6.1   7.3   8.6  15.1  14.9  16.7
          4   3.7  -0.2   3.2   5.6  11.7  28.3  30.4  37.7
          5   0.8  -2.0   1.1   4.6  15.4  31.2  36.7  41.9
          6  -1.0  -3.6  -0.8   4.4  14.7  30.1  34.8  39.7
          8  -0.8  -5.4  -2.8   1.1   9.2  21.5  25.9  30.5
         10  -3.1  -9.8 -12.1 -11.3  -1.7  10.1  14.6  19.2
         14  -9.9 -26.9 -40.6 -31.1 -20.2  -8.5  -3.8   0.8

Our best reply to his cow count:

    his cows  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
    our cows  2  2  2  2  2  2  2  6  5  5  5  5  5  5  5

**He plays 9. Our best reply is 5. We play 6.** So the herd is already close to right, worth about
$1k -- and the $30k+ in that table is not ours to take, it is his 9 cows into a one-MILK-shop seed.

The reply function is a step, not a slope: **2 cows while he is under-invested, 5 once he floods.**
Under 7 of his cows the milk book still pays, and the cheapest way to hold price is to stay out of
it; above that the book is dead either way and the extra cows are pure denial.

Caveats that bound this table: it forces all 14 slots to COW or SHEEP, so geese and crop are
excluded -- on seed 11, with 6 EGG shops and 1 MILK shop, the costed surface picks geese instead.
The single fixed point at 2 is a symmetric read, not an equilibrium: his placement slots differ
from ours, so a proper equilibrium needs his best reply iterated too, which is not run.

### 9. CORRECTION: the shop draw is ENDOGENOUS, and the 40-seed scan is void

`_spawn_weeds` consumes the day's rng **once per tile** before `rng.choice(sorted(SHOPS))` runs
(`reference:876-891`). Tile count therefore moves every later draw, and tile count is decided by
land purchases. The draw is a function of play, not of the seed.

Measured, same seed, same config, only the agents differ:

    seed 11  PASS: BRUNCH BAKERY BRUNCH BAKERY YARN BAKERY BRUNCH SMOOTHIE
    seed 11  REAL: PET_CAFE PIZZA YARN ICE_CREAM BAKERY BRUNCH FARMERS YARN
    seed  3  PASS: BRUNCH YARN ICE PIZZA FARMERS FARMERS PIZZA PIZZA
    seed  3  REAL: BAKERY BAKERY PET PET PET PET SMOOTHIE PET

**Section 3 is void.** The mean shop-slots-per-product table, "seed 11 is the extreme egg seed",
and "seed 3 is the best tomato seed" were all measured with PASS agents and describe draws that do
not occur in a played game. Section 8's grid is also void: it took its drain series from a PASS run.

It does explain the section 4 carrot result. Seed 3 under real play draws **five PET_CAFEs**, and
PET_CAFE is single-product so it drains CARROT at x2. Carrot realised $265/unit there because the
drain was enormous and we sold 12 units.

#### The corrected grid (`data/logs/cow_grid_real_shops.log`)

Our best reply in cows, remainder sheep, 14 animals, exact production, purchase cost included:

    seed 11   CARROT:2 EGG:2 MILK:2 STRAWBERRY:3 TOMATO:2 WHEAT:5 WOOL:2
      his cows  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
      our cows  8  7  5  5  4  4  5  4  4  4  3  3  3  3  3     fixed point 4

    seed  3   CARROT:5 EGG:2 MILK:1 STRAWBERRY:1 WHEAT:2
      his cows  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
      our cows  2  2  2  2  2  2  2  2  3  5  8  8  8  8 10     fixed point 2

**Two milk shops supports 4-8 cows; one supports 2.** The margin scale moves with it as well --
seed 11 reaches +$53.8k, seed 3 only +$13.8k, because with one milk shop and no yarn store both
animal books saturate and livestock cannot win much at all.

**Against his real 9 cows on seed 11, our best is 4 and we run 6: about $7k.** The PASS-agent grid
put the same gap at $1k.

#### What this means for strategy, and it is not a table lookup

Because the draw responds to play, a seed-keyed lookup is impossible in principle. Conditioning
must happen at RUNTIME -- shops unlock every 3 days and `town.unlocked_shops` is fully observable.
That is what `SHOP_ADAPT_HERD` already attempts; what it lacked was a correct target, which the
grid now supplies.

#### Standing rule this adds

Never characterise a seed from a run whose actions differ from the shipped agent's. The draw, the
drain and therefore every price in the season are downstream of what was played.

### 10. The goose is conditional on the YARN_STORE, and that is why every verdict was wrong

Optimal (cows/sheep/geese) against his 9 cows / 3 sheep, synthetic drain, exact production,
purchase cost included. `data/logs/optimal_herd_14_vs_18_slots.log`,
`data/logs/optimal_herd_18_slots.log`.

A milk shop drains 1 per event (all are multi-product). A YARN_STORE drains **2** (single-product
multiplier), so one yarn store absorbs roughly twice what one milk shop does.

#### 14 slots

| milk | yarn | cows | sheep | geese | margin | margin with geese BANNED |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 3 | 3 | **8** | +13,089 | -2,355 |
| 1 | 0 | 5 | 2 | **7** | +11,276 | -2,001 |
| 2 | 0 | 7 | 2 | **5** | +6,395 | -1,744 |
| 3 | 0 | 10 | 2 | 2 | +5,323 | +2,535 |
| 0 | 1 | 1 | 9 | 4 | +35,119 | +28,568 |
| 1 | 1 | 4 | 8 | 2 | +29,161 | +28,054 |
| 2 | 1 | 6 | 8 | 0 | +21,678 | +21,678 |
| 2 | 2 | 5 | 9 | 0 | +26,753 | +26,753 |

**Geese rescue exactly the boards with no yarn store** -- a $15,444 swing at `0 milk / 0 yarn`,
$13,277 at `1 milk / 0 yarn`. At two or more yarn stores they leave the optimum entirely.

Measured over 24 seeds under REAL play (`data/logs/shop_draws_real_play.log`), **38% of draws have
no yarn store**: seeds 2, 3, 4, 7, 9, 13, 14, 19, 23. Two of 24 (8%) have `milk<=1 and yarn 0`.

So the goose is worth five figures on 38% of boards and nothing on the other 62%. Every previous
verdict measured ONE board and generalised. `SELLABLE` blocking EGG was one artifact; the d0 pen
pairing that cost $38,207 of wool was another; **conditioning on the wrong variable was the third
and the one that mattered.**

#### 18 slots -- and Q4 costs $7,000, which is NOT in these numbers

| milk | yarn | 14 slots | 18 slots | Q4 gain |
|---:|---:|---|---|---:|
| 0 | 0 | 3/3/8 +13,089 | 3/3/12 +17,077 | +3,988 |
| 1 | 0 | 5/2/7 +11,276 | 5/3/10 +15,191 | +3,915 |
| 2 | 0 | 7/2/5 +6,395 | 8/3/7 +12,358 | +5,963 |
| 0 | 1 | 1/9/4 +35,119 | 2/9/7 +42,488 | +7,369 |
| 2 | 1 | 6/8/0 +21,678 | 7/8/3 +32,325 | +10,647 |
| 1 | 2 | 3/11/0 +40,357 | 3/15/0 +56,610 | +16,253 |
| 2 | 2 | 5/9/0 +26,753 | 6/12/0 +47,112 | +20,359 |
| 4 | 2 | 8/6/0 +12,102 | 9/9/0 +36,389 | +24,287 |

**No yarn store: the extra pens gain $3,900-$6,000 against a $7,000 quadrant -- Q4 does not pay for
itself on animals.** Two yarn stores: +$13k to +$24k, and it is one of the best buys in the game.

The optimum always fills every slot that exists; the extras go to **sheep on yarn boards, geese on
no-yarn boards**. At `0 milk / 0 yarn` geese take 12 of 18.

#### The decision rule, on two observable integers

Both counts are readable from `town.unlocked_shops` as shops unlock every 3 days, which is what
`SHOP_ADAPT_HERD` already watches -- it has never had a correct target.

    yarn 0:  geese-heavy. cows 3/5/7/10/13 as milk shops go 0->4, sheep 2-3, geese take the rest
    yarn 1:  1/9/4, 4/8/2, 6/8/0, 8/6/0, 9/5/0
    yarn 2+: no geese. 0/14, 3/11, 5/9, 8/6

His herd changes how much we WIN, not what we should DO: against 6 cows/6 sheep instead of 9/3, the
optimal allocation differs in two cells of twenty, by one animal each, while margins move by up to
$19k (`data/logs/optimal_herd_vs_6_6.log`).

#### Limits, and they are not small

- Sections 8-10 are synthetic drain plus exact production. **Not one played season.** Today's
  record is that every unreplayed claim here needed correcting.
- The 18-slot placement days (d14/16/18/20) are an ESTIMATE of when Q4 pens come online, not
  measured. Late slots are where the yield curve is steepest, so this assumption carries weight.
- The sweep never leaves a slot empty when an animal has positive value, so it cannot find the
  seed-3 played answer of running nine animals rather than fourteen.

### 11. What section 10 assumes about the opponent, and which assumptions were tested

Assumed: **9 cows, 3 sheep** on his real placement slots
`[0,0,0,3,5,7,7,7,7,8,18,18,18,18]`, read off seed 11's board at season end; **zero geese**;
**no crops at all** -- only MILK, WOOL and EGG are priced; and Kawashigi's tape as the opponent on
every seed.

#### Tested: does the goose survive an opponent who also buys geese?

Board `0 milk / 0 yarn / 2 egg`, his 14 slots split across cows/sheep/geese
(`data/logs/goose_vs_opposing_geese.log`):

| his geese | his cow | his sheep | our cow | our sheep | our geese | margin |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 10 | 4 | 3 | 3 | 8 | +18,802 |
| 2 | 9 | 3 | 2 | 2 | 10 | +12,407 |
| 4 | 7 | 3 | 2 | 2 | 10 | +7,472 |
| 6 | 6 | 2 | 2 | 2 | 10 | +5,323 |
| 8 | 4 | 2 | 2 | 2 | 10 | +2,039 |
| 12 | 1 | 1 | 2 | 2 | 10 | +5,314 |

**Our best response never leaves geese** -- it rises 8 -> 10 and stays there even against 12 of his.
What collapses is the board's VALUE: +$18,802 -> +$2,039.

Same structure as milk in section 6. A contested book pays almost nothing to either side, and you
hold the position to DENY rather than to earn. **The recommendation is robust; the prize is not.**

#### Not tested, and these matter more

- **The crop books are absent.** His strawberry, wheat and carrot are not modelled. On seed 3 the
  real money was five PET_CAFEs draining CARROT at x2 -- a book this sweep cannot see. So the herd
  optimum is chosen while ignoring what those pen slots could have grown instead, which is the same
  half-measure trap the cow->strawberry arms exposed in section 6: giving up the milk denial without
  buying enough of the replacement.
- **One opponent tape** on every seed. His herd is fixed at whatever Kawashigi ran.
- **No played season** confirms any cell in sections 8-11.

### 12. The ideal split given our BLIND opening -- the decision-ready table

No shop exists before d3 (`townShopUnlockInterval = 3`), so the opening cannot be conditioned on
the draw. Slots d0,d0,d0,d0,d3,d5 are fixed at **3 cows + 3 sheep** -- what we play now. The eight
later slots (d7,d7,d7,d8,d10,d10,d12,d12) are free and CAN react, because by d7 two shops are out.

14 animals total, exact production, purchase cost in, opponent 9 cows / 3 sheep / no geese, 2 egg
shops. `data/logs/ideal_split_fixed_opening.log`.

| milk | yarn | the 8 reactive slots | TOTAL c/s/g | margin |
|---:|---:|---|---|---:|
| 0 | 0 | 8 goose | 3/3/8 | +13,680 |
| 1 | 0 | 8 goose | 3/3/8 | +7,562 |
| 2 | 0 | 4 cow + 4 goose | 7/3/4 | -1,421 |
| 3 | 0 | 8 cow | 11/3/0 | -1,538 |
| 0 | 1 | 7 sheep + 1 goose | 3/10/1 | +34,729 |
| 1 | 1 | 7 sheep + 1 goose | 3/10/1 | +28,611 |
| 2 | 1 | 6 sheep + 2 cow | 5/9/0 | +12,451 |
| 3 | 1 | 3 sheep + 5 cow | 8/6/0 | +727 |
| 0 | 2 | 8 sheep | 3/11/0 | +41,493 |
| 1 | 2 | 8 sheep | 3/11/0 | +35,375 |
| 2 | 2 | 6 sheep + 2 cow | 5/9/0 | +14,614 |
| 3 | 2 | 5 sheep + 3 cow | 6/8/0 | +1,933 |
| 4 | any | 8 cow | 11/3/0 | ~+550 |

#### The rule for the reactive eight

    no yarn store  + 0-1 milk  ->  all geese
    no yarn store  + 2   milk  ->  half cows, half geese
    any yarn store + 0-1 milk  ->  all sheep
                   + 2   milk  ->  6 sheep, 2 cows
                   + 3   milk  ->  5 sheep, 3 cows
                   + 4   milk  ->  all cows

**Cows only earn a slot at 3+ milk shops.** Below that the eight go to sheep if a yarn store exists
and geese if one does not.

#### The margin column matters more than the split

Holding yarn fixed and raising milk shops: +41,493 -> +14,614 -> +1,933 -> +550.

**A milk shop makes the board WORSE for us regardless of allocation**, because it subsidises
whoever is the bigger dairy farmer and that is him: 9 cows against our 3-11. A yarn store is the
mirror gift -- he keeps 3 sheep, so the wool drain is nearly ours alone (+13,680 -> +41,493 going
0 -> 2 yarn stores at the same milk count).

So the draw sets the size of the prize; the herd only decides whether we collect it.

#### The live misallocation

Our shipped 6 cows / 8 sheep is optimal at `3 milk / 2 yarn` -- **a board worth $1,933**. On the
boards actually worth winning (0-1 milk, 2+ yarn, worth $35k-42k) the answer is **3 cows / 11
sheep** and we run nearly twice the cows. Unlike the $7k in section 8 this is not an artifact of a
forced constraint: the opening is pinned to what we actually play.

Caveats from section 11 still bind in full -- no crop books, one opponent tape, synthetic drain,
and **no played season confirms any cell here.**

### 13. The d7 decision is under UNCERTAINTY, and that changes the answer

Section 12 assumed the shop counts were known when the eight reactive slots are filled. They are
not. Shops unlock every 3 days to 8 instances (d3..d24), so **at d7 only two exist and six are
still to be drawn**.

The three animal books never share a shop, so the remaining draws are multinomial:

    milk-draining  PIZZA, ICE_CREAM, SMOOTHIE   3/8
    egg-draining   BAKERY, BRUNCH               2/8
    wool-draining  YARN_STORE                   1/8
    neither        PET_CAFE, FARMERS_MARKET     2/8

This predicts `1 - (7/8)^8 = 65.6%` of boards carry a yarn store; the 24-seed real-play scan
measured 62%. The uniform model is sound.

#### Committing all eight at d7 is expensive

`data/logs/d7_decision_under_uncertainty.log`:

| known at d7 | EV-best 8 slots | EV margin | perfect info | VOI |
|---|---|---:|---:|---:|
| 0milk 0yarn 0egg | 4cow 4sheep 0goose | -1,947 | +9,455 | +11,403 |
| 0milk 0yarn 1egg | 4cow 2sheep 2goose | -1,572 | +10,207 | +11,779 |
| 0milk 0yarn 2egg | 4cow 1sheep 3goose | +581 | +12,089 | +11,507 |
| 1milk 0yarn 0egg | 8cow 0sheep 0goose | -1,902 | +3,879 | +5,781 |
| 0milk 1yarn 0egg | 2cow 6sheep 0goose | +10,721 | +14,576 | +3,854 |
| 2milk 0yarn 0egg | 8cow 0sheep 0goose | +128 | +1,572 | +1,444 |

**Geese enter only in proportion to egg shops ALREADY SEEN** -- 0 seen: 0 geese; 1 seen: 2 geese;
2 seen: 3 geese. So `HERD_GEESE = 0` is the CORRECT d7 choice on a blind board, and was only ever
wrong as a season-long constant. The bird belongs in the d10/d12 slots once BAKERY or BRUNCH_SPOT
has actually appeared.

Section 12's confident "8 geese at 0 milk / 0 yarn" does not survive uncertainty: six unknown draws
will most likely deliver milk shops, so the EV answer is the hedge 4 cows / 4 sheep.

#### Staging recovers most of it

Commit only the three d7 slots, decide the other five informed
(`data/logs/d7_staged_vs_commit.log`; the last five get perfect information, so this is an UPPER
bound on staging):

| known at d7 | commit 3 at d7 | staged | all 8 at d7 | staging gain | perfect |
|---|---|---:|---:|---:|---:|
| 0milk 0yarn 0egg | 3 cow | +6,490 | -1,947 | +8,437 | +9,455 |
| 0milk 0yarn 1egg | 2 cow + 1 goose | +7,142 | -1,572 | +8,714 | +10,207 |
| 0milk 0yarn 2egg | 2 cow + 1 goose | +9,333 | +581 | +8,752 | +12,089 |
| 1milk 0yarn 0egg | 3 cow | +3,120 | -1,902 | +5,022 | +3,879 |
| 0milk 1yarn 0egg | 3 sheep | +14,279 | +10,721 | +3,557 | +14,576 |
| 0milk 1yarn 1egg | 3 sheep | +14,554 | +10,721 | +3,832 | +14,851 |
| 1milk 1yarn 0egg | 2 cow + 1 sheep | +5,145 | +2,928 | +2,217 | +5,960 |
| 2milk 0yarn 0egg | 3 cow | +1,525 | +128 | +1,397 | +1,572 |

Staging captures **74%** of the value of perfect information on a blind board.

#### The d7 rule

    yarn store already seen  ->  3 sheep
    no yarn, egg shop seen   ->  2 cows + 1 goose
    nothing useful seen      ->  3 cows

**Cows are the HEDGE at d7**, not the preference -- milk is the modal shop type at 3/8 against
wool's 1/8. You buy cows on a blind board because they are the most likely to be right, and you
keep the d10/d12 slots free to correct.

Caveats from section 11 still bind: no crop books, one opponent tape, synthetic drain, and no
played season confirms any cell in sections 8-13.

### 14. MEASURED AND REVERTED: the milk-conditioned cow cap

`EARLY_YARN_COW_BY_MILK = (4, 4, 5, 6)` replacing the flat `WOOL_SHOP_COW_CAP = 6` on the
early-yarn branch of `_herd_split`.

**Rematch corpus, 97 recorded ladder games: 63/97 against a baseline of 66/97. Reverted.**
`data/logs/rematch_milk_conditioned_cap.log`.

Four played seeds said the opposite, on margin:

| seed | yarn at | flat 6 | milk cap | delta |
|---|---|---|---|---:|
| 10 | draw 1 | 6c/12s +27,650 | 4c/14s +32,110 | +4,460 |
| 12 | draw 1 | 6c/12s +29,502 | 4c/14s +31,754 | +2,252 |
| 15 | draw 1 | 6c/12s +37,516 | 4c/14s +42,208 | +4,692 |
| 18 | draw 1 | 6c/12s +22,887 | 5c/13s +21,972 | -915 |

Mean +$2,622 of margin, and three fewer wins. **Bigger margin, fewer wins.** The same divergence
the fertilizer exemption showed pointing the other way (banks $9k less, wins $4k more). Selecting
on money remains wrong even when the money is a MARGIN rather than a bank.

#### Two facts worth keeping from the attempt

- **The change is unreachable unless YARN_STORE lands at draw 1 or 2.** `bought` floors the split
  and the opening buys four cows by d5, six by d7; `WOOL_SHOP_DRAW_LIMIT = 3` looks through d9.
  On seeds 11 and 3 the edit was byte-identical. By the leader's own distribution that is ~31% of
  boards. Any future cap change below 6 has to move the OPENING, not `_herd_split`.
- **Solved days do not block it.** Base solves d12-29, q4 solves d9-29; cows are bought d0-d7 and
  the four seeds above are all q4 (18 animals), yet the herd still moved 6/12 -> 4/14 with the
  total intact. A precomputed route is a visit ORDER and `_live_ops` re-derives the op at each stop,
  so a pen stop places whatever is in the shed.

#### What this says about sections 8-13

Every number there is a MARGIN computed on the market maths. Section 14 is the first time one of
them met the win-rate evaluator, and it did not survive. **Treat the whole surface as a generator of
hypotheses about money, not about wins**, until a cell is tested on the rematch corpus.

### 15. Marginal value per crop unit -- wheat is the worst thing on the board

Priced on the real books of a played season, adding units to our own supply and repricing both
sides (`data/logs/marginal_value_per_crop.log`).

| product | seed 11 $/unit | seed 3 $/unit | his units in book (11 / 3) |
|---|---:|---:|---|
| MELON | **268** | 187 | 106 / 64 |
| CARROT | 63 | **219** | 0 / 0 |
| EGG | 51 | 59 | 0 / 0 |
| STRAWBERRY | 105 | 44 | 261 / 192 |
| WHEAT | **21** | **20** | 1,062 / 951 |

Per PLANTING (both wheat and melon cap at `max_yield 6`): melon $1,608 against wheat $126 on
seed 11 -- **12.8x**.

#### The wheat denial theory is dead

Adding 72 of our wheat units costs him **$82**. The book holds 1,531 units, the curve is flat that
far out, and the `_commit_unit` floor rule stops dumping from moving supply at all once price hits
$1. Being the larger seller does not make him vulnerable in a saturated book.

Melon is the opposite profile and is where denial actually works: +12 melon units cost him
**-$1,730** on seed 11. Small book (178 units both sides), high price ($197-250), and he is in it.

#### Correction to section 14's arithmetic

I priced 72 marginal wheat units at the season AVERAGE $42 to get ~$3,024. They earn **$1,432**,
about $20 each. Average price where marginal price applies -- the same error class as the offers/
fills and PASS-agent mistakes earlier in this document.

#### What Kawashigi actually does with two freed pens

His three-quadrant 6-cow/6-sheep seats against his 10/4 seats (`data/logs/kawa_plants_by_herd.log`,
n=3 vs n=38, so weak):

| crop | 6/6 | 10/4 | delta |
|---|---:|---:|---:|
| WHEAT | 139.3 | 127.1 | +12.2 |
| STRAWBERRY | 34.0 | 35.7 | -1.7 |
| MELON | 20.0 | 18.3 | +1.7 |
| CARROT | 7.7 | 6.1 | +1.6 |

The marginal 14 plantings are 88% wheat, but priced by section 15 the **+1.7 melon is worth ~$2,700
and the +12.2 wheat ~$1,514**. Seven times fewer plantings, nearly twice the value. The wheat is
filler; the mix is the point.

#### Eggs versus the freed pens

| | seed 11 | seed 3 |
|---|---:|---:|
| +72 wheat | +1,514 | +1,467 |
| +70 eggs | +3,632 | +4,194 |

Eggs beat the wheat conversion 2.4x on market value. Against melon or carrot they lose.

#### The standing conclusion

**Melon and carrot are worth 4-10x everything else at the margin, both are shop-conditional, and
neither is reactive in our agent.** Tomato remains dead for the reason it always was: nobody is in
the book, so there is nothing to deny and the price is simply base.

All of section 15 is MARGIN. Section 14 showed twice in one night that margin does not reliably
convert to wins on the rematch corpus.

### 16. Crop value versus the OPPONENT'S holding -- an inverted U, and one negative

His supply of a product is scaled on a fixed board (seed 11), so the shop draw is held constant and
only his holding moves. `data/logs/crop_value_vs_his_holding.log`.

Margin to us of adding units:

| we add | his x0 | his x0.5 | his x1.0 | his x2.0 |
|---|---:|---:|---:|---:|
| 12 MELON | +2,493 | +2,719 | **+3,217** | +946 |
| 24 STRAWBERRY | **-3,657** | +1,492 | **+2,518** | +1,916 |
| 12 CARROT | +750 | +750 | +750 | +750 |
| 70 EGG | +3,592 | +3,592 | +3,592 | +3,592 |
| 72 WHEAT | -316 | +1,514 | +1,514 | +1,444 |

#### Two structures, not one

**Contested crops (melon, strawberry) are an inverted U in his holding.** Too little of his supply
and we simply flood our own book -- strawberry with him absent is **-$3,657**, actively negative,
because our existing 277 units reprice down and nobody absorbs the damage. Too much of his and the
book is already floored -- melon falls $3,217 -> $946 when his 106 units become 212. The peak sits
near where he actually plays.

**Uncontested crops (carrot, egg) are perfectly FLAT.** Identical value whatever he does, because
he is never in those books. Lower ceiling, zero variance, and they need no read on the opponent --
only on the shop draw.

#### This retires the "we only have one tape" objection, for crops

Scaling his supply on a fixed board isolates the dependence without needing a second opponent. The
answer is that melon and strawberry are bankable only because the field is homogeneous: the
124-game census put 21.5% of all field plantings on strawberry and 11.7% on melon, so an opponent
is reliably in both books. That is what makes the fragile crops safe, and it is the first thing
that would break if the field changed.

For ANIMALS the objection still stands -- his herd is fixed at whatever Kawashigi ran.

#### Practical split

- **Robust bets, shop-conditional only:** CARROT (needs PET_CAFE / FARMERS_MARKET), EGG (needs
  BAKERY / BRUNCH_SPOT, and no yarn store competing for the pens).
- **High-ceiling fragile bets, needing the opponent in the book:** MELON, STRAWBERRY.
- **Filler:** WHEAT at ~$20/unit, and negative if the opponent ever leaves that book.

Still margin, not wins. Section 14 stands: the one cell of this surface that met the rematch
corpus lost 63/97 against 66/97.

### 17. The mirror: what a Kawashigi-vs-Kawashigi board actually pays

Seed 11, per-unit realised price. `solo` = only we sell; `actual` = the played season; `mirror` =
both sides selling HIS volume. `data/logs/mirror_glut.log`.

| product | solo $/u | actual $/u | mirror $/u | mirror vs solo |
|---|---:|---:|---:|---:|
| MILK | 231.3 | 64.6 | 51.1 | **-78%** |
| STRAWBERRY | 134.8 | 39.5 | 40.9 | **-70%** |
| MELON | 243.2 | 196.9 | 147.0 | -40% |
| WHEAT | 31.2 | 19.8 | 19.6 | -37% |
| WOOL | 236.7 | 226.8 | 224.3 | **-5%** |
| CARROT | 64.0 | 64.0 | -- | he sells none |
| EGG | -- | -- | -- | neither sells any |

**Wool is the only product that survives a mirror.** He runs 3 sheep (94 units), so even doubled
the YARN_STORE's x2 drain absorbs it. Everything else he plays falls 37-78%.

Read the CARROT and EGG rows correctly: they are blank in the mirror because a Kawashigi mirror
sells **zero** of both, not because they crash. Those books are untouched by construction.

#### What this explains

- **Why every optimal-herd table in sections 10-13 piles into sheep.** Wool is the one animal book
  a homogeneous field cannot crush.
- **Why carrot realised $265/unit on seed 3** while we sold 12 units. Nobody is in it.
- **Why the old goose verdict was garbage.** "-$21k a game at one bird" was measured IN A MIRROR
  (commit `c9c1c18`), where both sides buy geese and glut the one book that was otherwise free. The
  deleting commit `7a88d30` even states that a mirror "gluts a shared book by construction and then
  measures the glut". That is precisely what happened. Combined with `SELLABLE` omitting EGG and the
  d0 pen pairing, the bird has now been condemned three times by three unrelated artifacts.

#### The standing strategic shape

Against a field that all plays the same tape, revenue lives in **WOOL, CARROT and EGG**. The
contested books -- MILK, STRAWBERRY, MELON, WHEAT -- are worth entering for DENIAL, not for
revenue, and section 16 gives the band of opponent holding where that denial actually pays.

This is the `CLAUDE.md` lesson restated as prices: the edge is in the dimensions where the field is
homogeneous, because those payoffs are contested and the value of deviating rises with how many
people share the convention.

---

## 2026-08-17 — The third quadrant arrives a day late

Folded in from `docs/the_third_quadrant_arrives_a_day_late_2026-08-17.md`.

Measured 2026-08-17 on 19 ladder replays in `data/seed_scripts/ladder_2026-08-17/`.
Scripts: `scripts/where_the_day_went.py`, logs under `data/logs/*_2026-08-17.log`.

### Two theories died

**"We over-water."** Dead.
We out-water every opponent on the ladder by +190 to +970 waterings in d11-d29, and we win most of
those games.

    water d11-29    us/them      result
    BeyondAnalytics  988/368     WIN +69,104
    Borys Tymchenko  971/0       WIN +84,068
    Akira Imae      1002/821     LOSS -5,508
    koren sabag     1015/821     LOSS   -158

The water count does not separate wins from losses. It is a property of our agent, not a defect.

**"The problem starts around d20."** Dead.
Cumulative plantings, us/them, against the script that beats us:

    day         4       6       8      10      12      15      20      29
    us/them  22/19   26/25   45/50   50/74   84/94   97/99  130/128  197/199

The deficit opens at d8, peaks at **d10 (50 vs 74)** and is closed by d15.
We plant the same 197 seeds all season, three to five days later each.

### What actually happens

    93839424 vs koren sabag -- quadrants owned, end of day
    day        6     7     8     9    10    11
    us         1     2     2     2     2     3
    them       2     2     2     2     3     3

We are one day behind on quadrant 2 *and* quadrant 3.

The d10 hour trace:

    d  h |     us $ usQ |   them $ themQ
    9 23 |    1,129   2 |    2,655     2
    10 1 |      986   2 |    3,064     3   <== they buy Q3
    10 23|    6,395   2 |    6,511     3
    11 1 |    6,824   3 |    7,121     3   <== we buy Q3

`LAND_PRICES = [1000, 2000, 4000]` (`reference:97`), so Q3 costs **$2,000**.
At d10 h1 we hold **$986**. We do not attempt the purchase — the only `BUY_LAND` we emit all season
is at d11 h1. `_do_buy_land` also fails **silently** on a thin bank (`reference:717-718`), so an
early attempt would leave no trace either.

The constraint is cash at d10 h1, and it is set on **d9**: we end d9 on $1,129, they end on $2,655.
Our money arrives in a lump at d10 h23 ($1,527 -> $6,395); theirs arrives smoothly across the day.
`LATE_SELL_FROM_HOUR = 16` is the obvious suspect and is **not yet tested**.

### It is our fixed schedule, not the seed and not the shops

First day each quadrant is owned, across all 19 replays:

    Q2    us: d6 in 14 games, d7 in 5        them (821-script): d6
    Q3    us: d11 in 19 of 19                them: d10
    Q4    us: never (one game, d12)          them: never

**Q3 lands on d11 in every single game.** Zero variance over seeds, shop draws and opponents, so
this is a hard-coded day in our plan rather than a board-dependent decision.

Planted tiles at d10 end, us/them, against the 821-script: 29/56, 35/56, 30/55, 35/56, 35/56,
35/56 — about half their acreage.

Two open items this raised:

- We have **never** bought quadrant 4 ($4,000), one game aside. Nor does anyone in this sample,
  so it may be correct, but it has never been tested.
- Q2 slips d6 -> d7 in 5 of 19 games. That one *is* variable and is unexplained.

### Cost

21 tiles lose a full day of growth, in every game against this opponent.

### What this is NOT

- It does not explain the MilanJoshi loss (-$7,727). There the quadrant timing is **identical**
  (both reach 3 quadrants at d11) and the difference is crop mix: at d10 we hold 19 STRAWBERRY /
  7 MELON against his 11 / 8. Different cause, still open.
- It is not sufficient to flip a game on its own. **Tom Yim runs the same script with the same
  50/74 profile and we beat him by $5,275.** The lag is a standing handicap, not the trigger.

### The opponent field

Three distinct scripts, identifiable by their d11-d29 signature:

    water/harv/plant     games                                      our record
    821 / 363 / 199      Moshel, Yan, INDRAJIT, Akira, koren,       1 W, 5 L
                         Tom Yim, Sankalp                           (+2 W at 812)
    734 / 364 / 187      MilanJoshi, Dmitry Larko                   1 W, 1 L
    715 / 327 / 174      Tita, Issac, Rheal                         3 W

The 821-script is the one to beat. We now hold seven examples of it.

### Next test, untried

Get $2,000 into the bank by d10 h1 and buy Q3 on d10 instead of d11.
Judge it on the d10 planting count (50 -> ~74) and the d11-d29 harvest count, replayed against the
821-script tape, **not** on season money.

Risk to check first: d12-d29 runs on precomputed routes, and a route is a visit ORDER over tiles.
Moving the quadrant a day earlier changes the board at the d11 handover, so stops can be dropped
silently. Prove the route survives before trusting the money.
