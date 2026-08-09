# The measured economics

Filename kept because `CLAUDE.md` and `kagg/agents/heuristic.py` point at it.
It started as the answer to verification question 5 and is now the whole measured economics of the
game: yields, drain, allocation, and selling into a shared book.

Every number here came from a measurement, and each one names what produced it.
`kagg/economics/` is validated against live episodes step for step and product for product in
`tests/test_market_model.py`; `tests/test_production.py` re-measures the yield table on every run.

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
