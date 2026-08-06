# Can we react to the opponent, and what else is fixable on Seb's plan

Written 2026-08-07, after two of our own leaderboard replays showed a $25,368 swing that was not the seed and not the crew.

## 1. Reacting to the opponent is not approximate — the curve is exactly computable

`market_price(item, inventory)` is a pure function of the shared book (`reference/kaggriculture.py:177`).
`MARKET_PARAMS` is a module constant, and `_new_market` writes a `params` key into the market dict **only when the params are non-default**.
A live game's observation carries `market` with keys `['inventory', 'prices']` and no `params`, so the competition runs the defaults and we know the curve exactly.

Given `obs["market"]["inventory"]`, we can compute what every successive unit of a SELL will fetch, before ordering it.

The curve above `I0` (10,000) is brutally shallow for exactly the products we live on:

| units above I0 | 0 | +20 | +50 | +100 |
|---|---|---|---|---|
| MILK | 160 | 118 | 55 | 1 |
| WOOL | 200 | 177 | 55 | 1 |
| STRAWBERRY | 120 | 82 | 24 | 1 |
| MELON | 250 | 246 | 225 | 150 |

Fifty units of milk into the book takes it from $160 to $55.
Both seats add to the same inventory, so an opponent selling what we sell taxes us without ever touching our farm.

Measured on our own two games (`scripts/why_did_that_game_go_badly.py`):

| game | opponent | our units sold | milk price d15-29 | final |
|---|---|---|---|---|
| 90534961 | Sophie | 1058 | 101.1 | $103,367 LOST |
| 90536513 | Mohit Babel | 1017 | 225.1 | $128,735 WON |

We sold **more** units in the game we lost.
Milk alone, ~135 units at a ~$124/unit worse price, is ~$16.7k of the $25.4k gap; strawberry adds ~$8.8k.

### Why the two previous attempts at smarter selling failed

Both were **static** rules against a **level** in a game whose realised price is bimodal:

| tried | measured | why it could not work |
|---|---|---|
| refuse to sell below 0.5x base | -$16,025 | 0.5x base for milk is $80, but the price is either ~$160 (book at I0) or ~$55 (book +50). The floor either blocks everything or nothing. |
| cap the quota to a day total rather than a turn | -$2,653 | Spacing by CLOCK, not by price. A standing offer collects each shop drain; a one-shot order does not. |

The rule that fits the mechanism is **marginal, not floored**: walk down the computed curve and stop at the first unit whose price falls below a reservation value.
Holding has a real, knowable value because the drain is deterministic — shops every 4 steps, town centre every 12, at 1x/2x/4x from days 10/20 (`kaggriculture.py:706-716`).

### The measurement blind spot that must be closed FIRST

`scripts/agent_ladder.py` drives seat 1 from a **fixed replay**.
The only contention it can ever measure is whatever that one tape happened to do.
Both negatives above were measured against a non-contesting opponent, so neither is evidence about a game against Sophie.

This is the project's own "never tune or evaluate against `starter` alone" lesson in a new costume, and it has now cost a measured $25k in a live game.
**Add a second, contesting opponent to the ladder before touching the sell logic.**

## 2. What else is fixable on Seb's plan

Full season, seed 11, ours minus tape (`scripts/first_two_days_all_params.py 11 --days 30 --turns 0`):

```
parameter              season ours-tape   days differing
_moves                        -588             30
PASS                          -400             28
PICKUP                        +312             28
tile:PLANT                    -238             24
_work                         +227             29
WATER                         -175             24
mkt:SELL_STRAWBERRY           -125             12
tile:WEED                     +102             17
HARVEST                        -89             16
DIG                            +47             12
FERTILIZE                      -26             14
```

**Execution capacity is no longer the problem.** We do +227 more work ops and -588 fewer moves than he does. That was the whole story a day ago and it is not the story now.

**The remaining gap is ground lost to weeds.**
This run is at `weedSpawnChance 0.0`, so every one of those +102 weed-tile-days is *our own crop* that went two days unwatered (`consecutive_unwatered >= 2`), plus 47 DIGs spent cleaning up after it.
The chain is:

    weeds  ->  -238 plant-tile-days  ->  -175 waters  ->  -89 harvests  ->  -125 strawberries sold

Strawberry is $120 base, so that last line is the expensive one and it is a consequence, not a cause.

Caution before acting: promoting the survival water into the mandatory pass was measured at **-$2,804** and reverted, and that test is pinned.
But it was measured *before* the fertilizer-reserve, thin-bank-feed and live-quote fixes, on a farm that was $10k poorer and could not keep its herd fed.
Re-measuring it is legitimate; assuming the old number still holds is not.

**`PICKUP +312` is separate and cheap.**
312 extra draws is 312 turns, roughly 13 unit-days a season, on a farm that already has spare PASS.
Worth a look purely because it is unambiguous waste.

## Ranked

1. Add a contesting opponent to the ladder. Nothing about selling can be trusted until this exists.
2. Marginal-revenue selling off the computed curve. ~$25k in one measured game.
3. The weed chain: -238 plant-tile-days on Seb's plan, at `weedSpawnChance 0`.
4. `PICKUP +312`.
