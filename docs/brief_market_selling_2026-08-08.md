# Brief: when to sell, on the 1.32.6 economy

Written 2026-08-08 for Fable.
Everything here is measured today unless marked otherwise.

## The one-line ask

**Decide when to sell each unit, rather than how much per day.**
Focus on **day 10 onward** — before that the farm is cash-bound and the rows are nearly forced.

## Why this is open

Our `sells` are a fixed per-day row transcribed from a replay: day 12 sells 19 strawberry because
the tape sold 19 strawberry.
It does not look at the price, at the market inventory, or at what the opponent has just dumped.

That row came off a **1.32.2** replay, and the ladder moved to **1.32.6** overnight on 2026-08-08.
So it is a fixed quantity schedule priced against an economy that no longer exists.

## What changed in 1.32.6 (verified in the installed env, not remembered)

```
townCenterSellInterval        12 -> 24        the centre buys once a day, not twice
TOWN_CENTER_DEMAND_SCHEDULE   [(20,4),(10,2),(0,1)] -> DELETED, flat 1 all season
MAX_SHOP_INSTANCES = 8        each unlocked shop gets its own town slot
movement onto LOCKED          blocked -> ALLOWED
```

Confirmed live from our own episode `91023699`: `configuration.townCenterSellInterval = 24`.
Late-season town drawdown falls roughly 8x.

## The mechanics you can rely on

- `market_price(item, inventory, params)` in the env source is a **pure function** of inventory.
  Monotone decreasing above `I0`, increasing below it. Floor at `PRICE_FLOOR`.
- The drain is deterministic: shops every `townShopSellInterval` (4) turns, each unlocked shop
  consuming 1 per product (2 if the shop has a single product); the town centre every 24 turns,
  1 per product in `TOWN_CENTER_PRODUCTS`.
- **The observation gives you everything**: `market.inventory`, `market.prices`,
  `town.unlocked_shops`, and the opponent's whole board (`farms[1].tiles`, money, quadrants).
  You do NOT see their shed — only ours is in `private`.
- Orders settle per unit slot in lockstep; both players are quoted against the same pre-commit
  inventory for a given slot. Max 10 market orders per player per turn.
- A SELL only funds a BUY that sits in a **later slot** of the same turn.

So: the revenue of selling now is exactly computable. The value of holding is a forecast, but a
**bounded** one — the drain is a guaranteed floor on improvement, and the opponent can only push
inventory the other way.

## The live signal we are currently blind to

From a real ladder game, day 17:

```
WHEAT    inventory 9,494   price 47   base  25     trading at ~2x base, scarcest product
MELON   inventory 10,079   price 188  base 250     flooded
WOOL    inventory 10,048   price 66   base 200
MILK     inventory 9,993   price 183  base 160
```

Every top 1.32.6 plan sells **305-649 wheat**. Ours sells **71**.

## Data you have

- `data/seed_scripts/v1326/` — ten schedules extracted from 1.32.6 top seats, plus the raw
  replays. Best seats: `healthstone_130k`, `rayk_130k`, `lester_125k`, `syed_125k`,
  `mohamed_107k`. Top games reach $125-130k.
- `data/seed_scripts/top_guys/90976060/schedule.json` — Seb on 1.32.6, banked $128,518.
- `scripts/breakdown.py --tape seb1326 --days 30` — day-by-day ours/tape, every field.
  `--diff` for the delta view.
- `scripts/extract_leader_schedule.py` — replay -> schedule.
- `kagg/arena` — `evaluate(agent, seeds, opponents=COMPETITIVE)` plays a **reacting** pool.

## Two traps that have already caught us today

1. **Money is not the objective.** The ladder is Elo; margin does not count.
   Measured today: Seb's own 1.32.6 sell mix earned us **more money on every seed** and lost
   **8/8** head-to-head, because ceding wool let the opponent earn more than we gained.
   Denying the opponent revenue is worth as much as earning it.
2. **A replayed tape does not react.** Absolute money against a tape runs 2-3x what real ladder
   games produce (live games settle around $30k vs $10k). Use the tape for per-day fidelity;
   use the arena pool for anything about strategy.

## Constraints

- The season ends at day 29. Stock unsold then is worth zero — holding has a hard deadline, and
  we currently lose to one opponent **entirely on d29**.
- Shed capacity is 100 and the overnight sweep dumps every hand into it; what will not fit is
  destroyed.
- Wheat is also FEED: 1 per animal per day, and `consecutive_unfed >= 2` evicts the animal.
  Never release wheat the herd needs — that failure has cost this project a day already.
- `SELL_SURPLUS_HORIZON` in `schedule_agent.py` has an existing sweep in its docstring showing
  short horizons are much worse. Read it before proposing one.

## What a good answer looks like

A rule that, given the observation, decides for each product how many units to offer this turn —
justified against the price curve and the drain, not tuned. Plus the measurement that shows it
beats the fixed row on **pool win rate**, with the money as context.

Write findings to `docs/fable_market_selling_2026-08-08.md`.
