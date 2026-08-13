# Competition brief and environment rules

Everything here is quoted from the competition configuration or measured directly against
`reference/kaggriculture.py`, which is ground truth for every rule question.
Read the source rather than the README where the two disagree; that has cost this project time
more than once.

## The competition

| Field | Value |
|---|---|
| URL | https://www.kaggle.com/competitions/kaggriculture |
| Prize | $50,000 |
| Launched | 2026-07-30 |
| Final deadline | **2026-09-30** |
| Merger / new-entrant deadline | 2026-09-23 |
| Max team size | 5 |
| Submissions per day | **5** |
| Env id | `kaggriculture` (also a `kaggriculture_beginner` variant) |

Alex competes separately from a friend who is independently running MaskablePPO with an entity
transformer; they compare notes on Discord.

## The game

Two players, one 10x10 farm each, 30 days x 24 turns = **720 turns**.
Start on **$3,000** and one unlocked 5x5 quadrant.
Buy seeds and livestock, plant, water, harvest, feed and care for animals, hire day labourers,
sell into a **shared** dynamic market.
Most money in the bank at the end wins. **Unsold inventory is worth exactly zero.**

## Scoring — Elo, starting at 600

The environment hands the framework **money** as the episode reward (`s.reward` is the farm's
bank), but the competition ranks on a rating updated from match outcomes.

- **Winning matters, margin does not.** A $43k win and a $4k win score identically.
- New submissions start at **600**, not 1000. Anything judged against 1000 reads ~400 points too
  harshly — v4 at 526 was genuinely losing, v5 at 613 genuinely winning.
- Money is a good dense *training* signal and the wrong **selection** criterion.

Field movement, measured from the official episodes index:

| date | episodes | top avg | median avg |
|---|---:|---:|---:|
| 2026-07-30 | 864 | 1,152 | 670 |
| 2026-07-31 | 928 | 1,427 | 1,175 |
| 2026-08-01 | 829 | 1,581 | 1,348 |
| 2026-08-02 | 793 | 2,627 | 2,319 |

The public leaderboard on 2026-08-03 read top 2,723 / 20th 2,464 / median 819 over 615 teams,
against our best-ever submission at 600.5.
**Any target read off a leaderboard snapshot more than a few days old is stale** — confirmed again
by the next reading: the daily episode index on 2026-08-08 read `median_avg_score` **3,067.75** and
`top_avg_score` **3,192.89**, against our best-ever submission at **1,123.5** — a 15-replay sample
that is now superseded in scale by `docs/experiment_log.md`'s "the ladder is two scripts" section,
measured from 2,744 ladder
seats: the ladder top is ~3,210, our best-ever submission is 1,257.9, and the field plants 108-147
WHEAT tiles a season against our 24. Read that file before treating any older "the gap is just price
realised per unit" framing as the whole story.

## Baselines, measured locally on 1.32.2

```
starter vs starter  ->  3512 / 3512     (+$512 profit over a whole season)
starter vs pass     ->  3508 / 3000
random vs pass      ->   120 / 3000
random vs random    ->     0 / 0
```

**Never tune or evaluate against `starter` alone.** It sells almost nothing, so the market is never
contested and every number comes out roughly 2x reality. That mistake cost a submission.

## Inference budget

| Setting | Value |
|---|---|
| `actTimeout` | **1 second per turn** |
| `remainingOverageTime` | **60 seconds banked for the whole episode** |
| `runTimeout` | 1200 seconds for the whole episode |

The 60 is from `reference/kaggriculture.json:128`; an earlier note here said 12 and several
design decisions were made against that wrong figure.

No *per-turn* online search. A network forward pass (~1-5 ms) fits trivially, and 60 banked seconds
allows a planning burst at turn 0 or a shorter one every few days.

## Action space

Per unit (farmer plus each hired hand), one op per turn, 18 ops:

```
Movement:  NORTH SOUTH EAST WEST PASS
Shed:      PICKUP <item> [n]   PLACE <item> [n]   DROP
Plants:    PLANT <crop>   WATER   HARVEST   FERTILIZE
Animals:   BUILD_COOP  BUILD_PASTURE  FEED  COLLECT_FERTILIZER  CARE
Terrain:   DIG
```

WATER / HARVEST / FERTILIZE / FEED / CARE / DIG act on the tile the unit stands on, so **routing is
a first-class cost**.

Market is a separate ordered list of up to `maxMarketOrdersPerTurn` (default **10**):

```
["BUY_SEED", crop, n]   ["BUY_PRODUCT", item, n]   ["BUY_ANIMAL", animal, n]
["SELL", item, n]       ["HIRE"]                   ["BUY_LAND"]
```

Invalid actions are **silent no-ops**. Only `WHEAT` and `FERTILIZER` are legal `BUY_PRODUCT` items.

```py
{"farmer": [op, *args], "hands": [[op, *args], ...], "market": [[op, *args], ...]}
```

An agent submits exactly one unit action per unit it owns.

## Observation

Both farms are fully visible: tiles, crops, `planted_day`, unit positions, money, unlocked
quadrants, hires today. Only the shed, seed store and unit inventories are private.
Market inventory and prices are shared and visible.

Per-turn state the env hands over for free, and which the live agent reads rather than predicting:

```
obs["farms"][me]["tiles"]     watered_today, yield_units, fed_today, cared_today,
                              fertilizer_available, consecutive_unwatered
obs["farms"][me]["farmer"]    where the farmer stands -- no dead reckoning
obs["farms"][me]["hands"]     every hand, so an op cannot go to a unit we do not own
obs["farms"][me]["money"]     so a purchase is never ordered against a bank that cannot pay
obs["private"]["shed"]        so an animal is never drawn from an empty shed
obs["private"]["seeds"]       so PLANT is never blocked by the atomic-seed rule
```

## Randomness

Deterministic given a seed except for:

- **Weed spawns** — `weedSpawnChance` 0.005 per **empty** unlocked tile, once per end-of-day.
  ~40 empty tiles gives ~0.2 spawns/day, **~6 a season**, and only those landing on ground the plan
  intends to use matter.
- **Town shop unlock order** — random selection from the remaining pool every 3 days.

Everything else, including every weed that comes from our own neglect, is deterministic.

## Configuration defaults

| Parameter | Default |
|---|---|
| `episodeSteps` | 720 |
| `boardSize` | 10 |
| `startingMoney` | 3000 |
| `maxMarketOrdersPerTurn` | 10 |
| `turnsPerDay` | 24 |
| `shedCapacity` | 100 |
| `weedSpawnChance` | 0.005 |
| `townShopUnlockInterval` | 3 |
| `townShopSellInterval` | 4 |
| `townCenterSellInterval` | 12 (1.32.2) / 24 (1.32.6) |
| `farmHandCostMult` | 1 |

## Engine rules that have each cost a day

Every one of these was, at some point, written up as our bug and turned out to be the environment.

- **`first_yield_day` gates HARVEST.** MELON's is 10. A HARVEST below it is a **no-op that still
  costs the turn** (`kaggriculture.py:395`). `router.py:243` matches the rule exactly.
- **A one-shot crop is demolished by HARVEST**, so it must not be harvested until full.
  `_one_shot_is_finished` refuses while `room > 0`, correctly. Yield comes only from WATER inside
  `[(max_day + 1) // 2, max_day]` — ages 6-12 for melon — and a fertilized water pays two units, so
  a one-shot can fill early and then sit idle. `crop_ops` only fertilizes a one-shot when
  `waters_left < room`, so that trade is already declined.
- **Ongoing crops yield `max_yield` once per LIFETIME, not per day.** Tomato is 8 units per tile per
  season, strawberry 6 — not 4.0 and 2.0 per day as the Object Types table reads. Pinned by
  `tests/test_production.py`. Do not re-derive from the published tables.
- **Animals have no `production_count` cap**, so they produce until they starve. A goose gives
  26 eggs a season against a `max_held` of 4.
- **`consecutive_unfed >= 2` removes the animal** and leaves the structure
  (`kaggriculture.py:786`). Not "a day's production forgone" — a $400-$500 asset written off plus
  every remaining day of its output.
- **`consecutive_unwatered >= 2` turns a PLANT tile into a WEED** (`kaggriculture.py:753`), and
  weeded ground refuses PLANT until DIG clears it.
- **The shed holds 100 items and `_drop_inventories_to_shed` DESTROYS the overflow** at dusk.
  Carried inventory is uncapped during a day and emptied every night.
- **`SELL` sees only the shed.** Harvest 90 melons and never DROP and the market cannot see them
  until the overnight sweep, which is usually too late to fund a same-day land or animal buy.
  `BUY_PRODUCT` and `BUY_ANIMAL` also settle only against the shed; FEED, HARVEST and
  COLLECT_FERTILIZER only touch the acting unit's own inventory.
- **`PLACE` and `FEED` draw from the unit's CARRIED inventory, not the shed.**
- **Atomic PLANT.** The reference drops *every* PLANT for a crop when a turn's requests exceed the
  seeds held, counting the actions **submitted**, not the units that exist.
- **Market orders pair by slot.** `_process_market` pairs the two players' *i*-th order and quotes
  both from the same pre-commit inventory, so both seats pay the same price on a contested unit.
  Orders past the tenth slot are dropped.
- **Hire cost is `mult * fib(n)` in the day's hire count and RESETS EVERY MORNING**, so it is paid
  30 times. 8 hands is $54/day; 12 is $376/day; 14 is $986/day; 17 is $4,180/day.
- **`_do_buy_land` ignores which quadrant you ask for.** Prices are $1,000 / $2,000 / $4,000 in a
  fixed order.
- **Three of the four shed-access tiles start LOCKED** (NE, SW, SE), and hands can spawn on them.
- **A pasture or coop sitting on a shed-access tile does NOT block DROP/PICKUP or movement.**
  `_is_shed_adjacent` is pure coordinate membership; the only tile state that blocks anything is
  `"LOCKED"`. Confirmed by `tests/test_pens_do_not_block_the_depot_ring.py` (7 cases), including a
  positive control that LOCKED *does* block.
- **An unaffordable or unfillable order is refused silently.** There is no rejection signal in the
  observation, which is why our agent re-offers every turn and why any metric counting *offers*
  rather than *fills* over-reads by up to 11x.

## Version skew — 1.32.2 vs 1.32.6

`kaggle-environments` 1.32.6 shipped a "town rebalance" on 2026-08-07:

```
townCenterSellInterval        12 -> 24      the centre buys once a day, not twice
TOWN_CENTER_DEMAND_SCHEDULE   [(20,4),(10,2),(0,1)] -> DELETED, flat 1 all season
MAX_SHOP_INSTANCES = 8        each unlocked shop gets its own town slot
movement onto LOCKED          blocked -> ALLOWED
```

Late-season town-centre drawdown falls **8x**, so every "hold it and dump it late" argument in this
repo was priced against the old ramp.

**The ladder was still on 1.32.2 as of 2026-08-07 evening**: replay `90751101` records
`townCenterSellInterval = 12` in its own configuration block. We upgraded, measured, found the
reference tape damaged (its `BUY_LAND` orders fail under the new economy because a fixed script
cannot wait for a better price), and pinned back within the hour.
Measuring on 1.32.6 while the ladder runs 1.32.2 optimises for a game nobody is playing.

**Check that field on every replay you download:**

```python
json.loads(pathlib.Path(replay).read_text())["configuration"]["townCenterSellInterval"]
```

Nothing in our code reads a remembered literal: `kagg/sim/town.py` reads `CENTER_INTERVAL` from the
installed env's JSON spec and `CENTER_SCHEDULE` via `getattr(kg, "TOWN_CENTER_DEMAND_SCHEDULE", ...)`.
19 tests still fail on 1.32.6 and are not fixed; three of those (`test_sim_ops`) are a real
divergence — `kagg/sim/ops.py` still blocks movement onto LOCKED.
When the ladder does move, there is a free routing gain: `_step_towards` and `_mobile` both refuse
locked tiles, so every tour currently detours around ground it would be allowed to cross.

## Economics — measured yields, drain, allocation, storage and the price curve

Folded in 2026-08-13 from `economics_q5_findings.md` (whole) and the analytical, environment-facts
half of `the_market.md` (the rest of that file's findings-about-us are in `experiment_log.md`).
Filenames referenced below (`docs/the_market.md`, `docs/what_saturates_and_what_does_not_2026-08-09.md`,
etc.) are historical — the content is here now.

Every number below came from a measurement or a direct computation off `reference/kaggriculture.py`,
and each one names what produced it. `kagg/economics/` is validated against live episodes step for
step and product for product in `tests/test_market_model.py`; `tests/test_production.py` re-measures
the yield table on every run.

> **Version and SELLABLE caveats.** §1 (yields) and §3-5 (supply, allocation, storage) below are
> version-independent — they come from per-tile production rules and `MARKET_PARAMS`, neither of
> which changed in 1.32.6. §2's original 1.32.2 town-drain table is superseded by the direct 87-tape
> measurement in `experiment_log.md`'s "the market" section, and by the corrected per-head animal
> saturation table further down this section (which fixed a bug that overstated every herd 4-6x).
> **The EGG-related saturation figures below are VOID pending re-measurement**: SELLABLE excluded
> EGG from every sale until `c99a8a5` (2026-08-13), so any `market_price`-based EGG revenue number
> computed before that date was pricing a product our own agent could never actually sell. Only the
> underlying egg *production-count* table (a yield fact, independent of sellability) survives intact.

### 1. Yields — the table in the competition docs is wrong

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

### 2. Town drain — fixed, large, and randomly scheduled (1.32.2 table; see the 87-tape correction below)

Nothing either player does changes the drain. Measured over a full season on 1.32.2 (seed 11; totals
move only a few percent across seeds) — **superseded for absolute size by the 1.32.6 rebalance, kept
for the mechanism**:

| Product | Shops | Season drain (1.32.2) | Price at zero player sales | x base |
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
is exactly 140 on every 1.32.2 seed, and never grows.

**The direct 1.32.6 measurement** (87 real ladder tapes, reading each game's closing
`market.inventory` against its own `town.unlocked_shops` — no simulation) is in `experiment_log.md`'s
"the market" section §2. Headline: WHEAT closes negative (undersupplied) on all 87 tapes; MELON and
FERTILIZER close positive (oversupplied) on all 87.

#### The drain does not exist from day 0, and this is the largest correction to the model

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

### 3. Supply — one quadrant against that drain

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

### 4. The allocation is arithmetic, not search

`scripts/allocation_calculator.py` computes the target allocation from `chains.DRAIN_UNITS` and
`economics/production.py` with no fitted constants. Fill each market to its drain, ranked by
revenue per unit-day (1.32.2 sizing):

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

### 5. Storage caps the timing prize

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

### 6. Selling into a shared book — the price curve, exactly

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

**The derived sell rule** (shipped, `PRICE_AWARE_SELL_CAP`/`RESERVATION_SELL_CAP` in
`schedule_agent.py`; measured impact in `experiment_log.md`): offer the largest `n` such that
`market_price(p, I_now+n) ≥ max(λ_p, (1−slip)·market_price_now)`, where
`λ_p = market_price(p, I_now + Q_rem − contest·D_rem)` and `contest` (1.0 solo-optimal, 0.5
two-player-split) replaces a hardcoded day-total `allow`. This is the marginal rule that follows
directly from the two rejected static rules below.

A finer-grained, version-invariant depth table — units above `I0` needed to reach 0.9x/0.75x/0.5x of
base, computed directly from the price curve (cross-checked against the season-absorption drain
numbers in `experiment_log.md`'s "market depth" section and found identical):

```
product      to 0.9x base   to 0.75x   to 0.5x
WHEAT              20          2421      ~inf
EGG                24          1422      ~inf      <- EGG figures VOID, see caveat above
FERTILIZER         53           128       253
MELON              51            80       113
CARROT             10            55       230
WOOL               19            30        42
TOMATO              7            38       144
MILK                 8            20        39
STRAWBERRY           7            16        32
```

#### Two rejected arms, and why both had to fail

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

#### Market manipulation and timing are not where the money is

`scripts/measure_true_drain.py` on a real leader replay: the town inventory never saturates, so the
"everyone sells wheat on day 28 and the price crashes" tragedy-of-the-commons does not occur.
Shifting only the sell days moves money at most **+3.6% and the win rate not at all**.
Market timing, front-running and withholding together are ~3% of money and 0% of wins.
The leader's own gaps between sell days are 1.0 (wheat, fertilizer) to 1.4 (wool) days — he sells
nearly daily, because **a fixed tape cannot wait for a demand event it cannot observe**.
Daily is the robust choice, not the lazy one.

### 7. Where each product's revenue actually saturates

First-local-peak table under `CONTEST=1.0` (splitting season demand with one other seller). **Read
"first local peak" literally** — a naive global maximum returns nonsense once price has crashed
through the $1 floor (revenue then rises forever with volume); an earlier pass made exactly this
mistake:

```
product           peak units   price     season $    tiles/head-equiv
WHEAT                 276      $25.0      $6,900       6.6
CARROT                 156     $35.0      $5,460       4.0
TOMATO                 104     $60.0      $6,240       6.5
STRAWBERRY              224    $120.0    $26,880      18.7
MELON                    88    $179.0    $15,748       7.3
MILK (cow)              160    $160.0    $25,600       2.4
WOOL (sheep)             112    $192.2    $21,529       2.3
EGG (goose)              128     $50.0     $6,400       1.2   -- VOID, see caveat above
FERTILIZER             4,000      $4.1    $16,250        --
```

Corrected per-head animal production (fixing a bug that computed herd output as `events × max_held`
when an animal makes one unit per event — every herd had been overstated 4-6x). This table is a
yield fact and is NOT subject to the SELLABLE correction:

```
head        1     2     4     8    12    16    20    24
COW        80   160   320   640   960  1164  1164  1164   (flat from 16)
SHEEP      67   133   267   533   800   897   897   897   (flat from 16)
GOOSE      50   100   200   246   246   246   246   246   (flat from 8)
```

This brackets rank-1 Seb's observed 9 cows / 11 sheep — an earlier, buggy model had wrongly
predicted saturation at only 4 head and contradicted him.

Fertilizer production is species-independent: `tile["fertilizer_available"]=True` for every animal
tile every day regardless of species (`kaggriculture.py:818`) — a $300 goose makes fertilizer at the
same rate as a $500 sheep.

### 8. What this changes

- The strategy is neither "wheat volume" nor "premium timing". It is *pick crops by revenue per
  tile-day against measured yields, size each to its drain, and weight by how early its shop is
  likely to open.*
- **Animals are the only uncapped producer**, and they convert wheat into a product worth 4-8x the
  wheat. Milk at $344 with zero player sales is the strongest premium position on the board.
  See `experiment_log.md` for the five separate times "animals do not pay" turned out to be a
  limitation of our own code.
- **Melon is the least scalable product in the game** — no shop, fixed 140 units — and our own
  searches built a monoculture on it three times.
- There is no large untapped market left to discover. The whole market is $302,380 (1.32.2 sizing),
  "1.0x if split evenly between two players", and the leader banks $139,121 — he captures nearly his
  entire share. The remaining edge is efficiency and robustness.

### Still not verified

- **Intra-day throughput.** The deferred schedules in §5 sell up to 150 units in one day, which is
  legal only because carried inventory is uncapped and selling from the shed frees room to drop
  more. Whether those instalments are routable inside the action budget is untested, so every
  deferred figure is an upper bound.
- **The CARE bonus** is excluded from every yield above, so they are floors rather than ceilings.

## Kaggle API

Credentials at `~/.kaggle/kaggle.json`. Never print or commit them.

```bash
pip install -U "kaggle-environments>=1.32.2"    # earlier versions lack the env
kaggle competitions submit kaggriculture -f main.py -m "v1"
kaggle competitions submissions kaggriculture
kaggle competitions episodes <SUBMISSION_ID>
kaggle competitions replay <EPISODE_ID>
kaggle competitions leaderboard kaggriculture -s
```

Submission needs `main.py` at the root exposing an `agent` function.
Build it with `scripts/build_planner_submission.py`, which inlines the four `kagg/search` modules
plus the schedule into one self-contained file and verifies the result imports and runs — a
hand-rolled `main.py` once spliced a docstring over line 1, failed to import, and banked exactly
the $3,000 start.

The older `scripts/build_submission.py` was deleted on 2026-08-09. It copied a *single*
dependency-free agent file verbatim, which fits `kagg/agents/contrarian.py` and cannot express the
planner, so building the old way silently shipped contrarian while reporting "submission verified".
Its gate was "beats `starter`", which this project's own notes call worthless — `starter` sells
almost nothing, so the market is never contested. Use `scripts/gate_pool.py` for a real gate.
