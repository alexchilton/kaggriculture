# Question 5 — does town drain exceed player supply for premium goods?

**Status: answered by measurement, 2026-07-31.**
Every number here comes from `kagg/economics/`, whose drain model is validated against live
episodes step for step and product for product in `tests/test_market_model.py`.
Reproduce with `python scripts/answer_q5.py`.

## The answer

**Yes for every premium good except melon — and the reason is not the one the day-1 analysis gave.**

Premium prices do not inevitably collapse, because a player physically cannot grow enough to
collapse them.
The binding constraint is **tile yield**, which the day-1 desk analysis overstated by roughly
tenfold for exactly the crops the strategy hung on.

Three consequences, all measured:

1. **Selling late beats selling early for every crop, by 1.14x to 1.26x** — worth having, but
   not a strategy on its own.
2. **There is no storage**, so that gain must be captured by making crops *mature* late rather
   than by holding harvested product. 100 items overnight, overflow destroyed.
3. **The bigger prize is that the premium/volume framing was built on a broken yield table.**

## The error that mattered

`docs/economics_analysis.md` read the Object Types "Max yield / tile / DAY" column as a daily
rate.
For ongoing crops it is not.
`_daily_refresh_plants` stops producing once `production_count > max_yield`, so an ongoing tile
yields `max_yield` units **for its entire life** and then dies.

Measured season output from one tile, optimal single-farmer play, no fertilizer
(`tests/test_production.py` re-measures these on every run):

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

The `[HYPOTHESIS]` revenue-per-tile-day table in `economics_analysis.md` is therefore wrong,
and wrong in the direction that made premium crops look like the prize.

Animals are the exception in the other direction: `_daily_refresh_animals` has **no**
`production_count` cap, so an animal produces until it starves.
A goose yields 26 eggs a season against a `max_held` of 4.

## Demand side — town drain is fixed and large

Nothing either player does changes it.
Measured over a full season (seed 11; totals move only a few percent across seeds):

| Product | Shops demanding | Season drain | Price at zero player sales | x base |
|---|---|---|---|---|
| Wheat | 5 | 662 | $51 | 2.04x |
| Carrot | 2 | 410 | $42 | 1.20x |
| Tomato | 2 | 410 | $109 | 1.82x |
| Strawberry | 4 | 536 | $314 | 2.62x |
| Melon | **0** | 140 | $293 | 1.17x |
| Egg | 2 | 320 | $69 | 1.38x |
| Milk | 3 | 446 | $344 | 2.15x |
| Wool | 1 | 320 | $250 | 1.25x |

Melon appears in **no shop**; its only consumer is the town centre.
That makes melon drain the smallest and completely predictable — it does not depend on the
unlock draw at all, and is exactly 140 on every seed.

## Supply side — one quadrant against that drain

25 tiles is the free NW quadrant, so this is the commitment available without buying land.

| Crop | units/tile | 25 tiles supply | drain | supply / drain | tiles to saturate demand |
|---|---|---|---|---|---|
| Wheat | 28 | 700 | 662 | 1.06x | 23.6 |
| Carrot | 29 | 725 | 410 | 1.77x | 14.1 |
| Tomato | 8 | 200 | 410 | **0.49x** | 51.2 |
| Strawberry | 6 | 150 | 536 | **0.28x** | 89.3 |
| Melon | 12 | 300 | 140 | 2.14x | 11.7 |
| Egg | 26 | 650 | 320 | 2.03x | 12.3 |
| Milk | 11 | 275 | 446 | **0.62x** | 40.5 |
| Wool | 8 | 200 | 320 | **0.62x** | 40.0 |

**Strawberry needs 89 tiles to saturate town demand.** That is three and a half quadrants
committed to one crop, and $8,933 of seed against a $3,000 start.
Tomato needs 51 tiles, milk 40 cows, wool 40 sheep.
None of these is reachable, which is precisely why their prices hold.

Wheat and carrot and melon and egg *can* be oversupplied by a single quadrant.
Those are the goods where dumping discipline matters.

## Timing — late beats early, but storage caps the prize

**There is no long-term storage in this game.**
Overnight carry is 100 items total and `_drop_inventories_to_shed` **destroys** the overflow.
Carried inventory has no cap during a day, but it is emptied every night.
Ongoing crop tiles hold at most `max_yield` (4 units) and only for about a day before decay.
All pinned in `tests/test_storage.py`.

So a season's harvest cannot be banked and released at the end.
Comparing an even daily drip against the latest schedule that storage actually permits — where
anything that would not survive the night must be sold that day:

| Crop | qty | drip revenue | $/unit | deferred revenue | $/unit | gain | forced out early | held to end |
|---|---|---|---|---|---|---|---|---|
| Wheat | 700 | $15,185 | 21.7 | $19,208 | 27.4 | 1.26x | 600 | 100 |
| Carrot | 725 | $14,214 | 19.6 | $16,218 | 22.4 | 1.14x | 575 | 150 |
| Tomato | 200 | $15,412 | 77.1 | $18,012 | 90.1 | 1.17x | 100 | 100 |
| Strawberry | 150 | $38,579 | 257.2 | $45,039 | 300.3 | 1.17x | **0** | 150 |
| Melon | 300 | $52,646 | 175.5 | $60,970 | 203.2 | 1.16x | 200 | 100 |

The mechanism is real: town drain runs all season whether or not you sell, so an untouched
market drifts into scarcity and price rises well above base.
Selling early spends that premium; deferring banks it.
But the gain is a **uniform 1.14x-1.26x**, not the 1.5-1.75x an unlimited-storage model
suggests, because 600 of wheat's 700 units have to leave the barn before the end regardless.

> **Correction.** An earlier version of this document claimed 1.75x for wheat and called wheat
> the biggest timing win. That was computed with a schedule that held 700 units, which no shed
> can do. Wheat's real gain is 1.26x and it is the crop *most* forced into drip selling.
> The claim in `economics_analysis.md` that wheat is timing-insensitive is closer to right than
> what replaced it.

**The lever is production timing, not sale timing.**
Since product cannot be stored, the way to sell into a scarce market is to have it *mature*
late.
Strawberry shows this cleanly: its 150 units arrive on days 16 and 29 only, nothing is forced
out early, and it captures the full deferred price.
A crop that matures in the last week needs no storage at all.

## What this changes

- **The strategy is neither "wheat volume" nor "premium timing" as posed.** It is
  *"sell late, and pick crops by revenue per tile-day against measured yields."*
- **Premium crops are safe from self-inflicted collapse** but are also far less productive per
  tile than the doc assumed. Strawberry at 6 units/tile/season is a poor use of a tile despite
  the high unit price.
- **Melon is the standout on these numbers** — 25 tiles, $65k, and demand that is identical on
  every seed. It is also the least contested, since no shop wants it.
- **Animals are the only uncapped source** and convert wheat into a product worth 4-8x the
  wheat. Milk at $344 with zero player sales, and 40 cows needed to saturate, is the strongest
  premium position on the board.

## What is still unverified

- **Intra-day throughput.** The deferred schedules above sell up to 150 units in a single day,
  which is legal only because carried inventory is uncapped and selling from the shed frees room
  to drop more. It costs HARVEST, DROP and SELL actions and requires standing on a shed-access
  tile. Whether those instalments are routable inside the action budget is **not tested**, so
  every deferred figure is an upper bound.
- **Feed cost.** `FEED` consumes 1 wheat per animal per day, so animal revenue is net of a
  wheat operation sized to the herd. Not yet modelled.
- **Action and routing budget.** Every figure here assumes the harvest actually gets harvested.
  Routing is the constraint the day-1 analysis flagged as decisive and it remains unmeasured.
- **Fertilizer and the CARE bonus** are excluded, so all yields are floors rather than ceilings.

## Questions this retires and raises

Retires question 5.
Raises: *what is the revenue-per-tile-day ranking once routing cost is charged against each
crop?* — which is question 3 on the original list, now the highest-value unknown.
