# Melon reality check: does day 6's batch ever land, and where does land money come from

Seed 11, weeds off, `tape=seb`, days 0-11 (turn resolution, `turnsPerDay=24`).
Our agent is `kagg.search.schedule_agent.make_agent(thin, 0, router=True)`, seat 0, against
Seb's real opponent tape in seat 1 (`tape_policy(replay, team, 1)`), the same harness as
`scripts/breakdown.py` and `scripts/the_seed_row_reoffer.py`.

Probe scripts used (not committed, kept in the session scratchpad since this task was
investigate-only):

- `melon_probe.py` — per-day MELON seed/plant/harvest/sell tally for both our agent and Seb's own
  recorded seat-0 tape, against the identical seat-1 opponent.
- `melon_day6_hourly.py` — hour-by-hour trace of day 6 only.
- `melon_tile_trace.py` — raw tile dump (`planted_day`, `yield_units`) for every standing MELON
  tile at the dawn of days 9, 10, 11, and at the end of the run.
- `land_funding_probe.py` — money and per-product shed delta at every turn a `BUY_LAND` order is
  emitted, plus per-day sold/harvested totals for all nine products.
- `day11_turn0_probe.py` — the exact market order list emitted at day 11 turn 0, since that is
  where the picture changed.

Logs: `data/logs/melon_probe.log`, `data/logs/melon_day6_hourly.log`,
`data/logs/melon_tile_trace.log`, `data/logs/melon_land_funding.log`,
`data/logs/melon_day11_turn0.log`.

## Fill logic, not order logic

Every number below labelled a **fill** comes from an observation-state delta that the env commits,
never from the order list. `scripts/breakdown.py` tallies `ops[day][o[0]] += int(o[2])` — the
quantity of every order **emitted**, every turn — and our BUY_SEED row is deliberately re-offered
every turn until it lands (`schedule_agent.py`), so an unfunded re-offer inflates that tally
without buying anything. That trap is specifically avoided here.

Two deltas turned out to be exact and cheap to compute, read directly off
`reference/kaggriculture.py`:

- `private["seeds"][MELON]` only increases in `_commit_unit` on a filled `BUY_SEED` (line ~647),
  and only decreases on a successful `PLANT` (line ~369; a blocked plant is a silent no-op that
  spends no seed). So a turn-over-turn delta in seed count is exactly "bought" (positive) or
  "planted" (negative).
- `HARVEST` adds units to the acting unit's **carried inventory**
  (`private["inventories"][idx]`), not directly to the shed (line ~408). The shed only gains units
  once a day, via `_drop_inventories_to_shed` at end-of-day (line ~812), and only loses units via a
  filled `SELL` (line ~630). Defining `total = shed[MELON] + sum(carried MELON across all
  inventories)` gives a quantity that the day-end auto-drop cannot move (it is purely an internal
  carried→shed transfer), so a turn-over-turn delta in `total` is exactly "harvested" (positive) or
  "sold" (negative) — including across the turn-23 day boundary, where a drop and a sell can land
  in the same `env.step`.

## Verdict on the original claim

**"We never plant day 6's six melons" is FALSE.**
We buy exactly 6 MELON seeds and plant exactly 6 MELON tiles on day 6, both numbers exact at turn
resolution (`melon_probe.py`: `bought=6, planted=6, plant_melon_emitted=6` for day 6, and every
`PLANT MELON` action emitted that day succeeds — emitted count equals accepted count all season).

The hour-by-hour trace (`melon_day6_hourly.py`) shows exactly what happens:

```
h 0 money 869->15    (a STRAWBERRY seed buy spends most of the day's dawn cash)
h 1..h 7  money stuck at 15, MELON seed count stuck at 0, BUY_SEED MELON 6 re-offered every hour
h 8 money 15->0, MELON seeds 0->6   <-- lands: SELL WOOL 6 + SELL FERTILIZER 1 fund it in the same turn
h 9, h12, h14, h16, h19, h22:  one PLANT MELON accepted each hour, 6 total
h23 MELON seeds back to 0 (all 6 spent on planting)
```

The original evidence in `data/logs/d6_seed_orders.log` (bank pinned at $15, MELON seeds at 0
through hour 8) is factually correct for hours 0-7. The claim built on it was wrong because the
diagnostic script only prints a line when an order is present, and once the order lands at hour 8
the schedule agent stops re-emitting it — so the log simply goes quiet, and quiet reads
indistinguishably from "still blocked." Money pinned at $15 for seven hours plus a seed count that
stays at 0 through the last printed line is not evidence of failure to buy; it is evidence of
"blocked until hour 8, funded by an animal-product sale, then immediately spent on planting."
"Seeds held at day 6 dusk = 0" is also true, but because all 6 were bought **and** fully planted
the same day, not because none were ever bought.

## Is day 6's batch ever harvested or sold, within days 0-11?

**No — and this is expected, not a bug.**
MELON's `first_yield_day` is 10 (`reference/kaggriculture.py` CROPS table: `"MELON": {...,
"first_yield_day": 10, "max_yield_day": 12, "ongoing": False}`), counted from `planted_day`. A
tile planted on day 6 cannot be harvested before day 16.

Direct tile inspection (`melon_tile_trace.py`) confirms this rather than deriving it from the
constants table alone: at the dawn of day 9, day 10, and day 11, and at the very end of the
12-day run, the six `planted_day: 6` MELON tiles are present, standing, `yield_units` still at 1
(barely into the watering window, which for a non-ongoing crop like melon opens at age 6), and
never harvested. Day 7's and day 8's smaller batches (3 and 2 tiles) are in the same state.

Seb's own tape plants an identical 6-unit MELON batch on day 6 (`bought=6, planted=6`, same as
ours, from the `seb-tape` run in `melon_probe.py`) and it is equally unharvested by day 11 in
Seb's own replay. This is the environment's maturity rule acting the same way on both sides, not
an agent defect on ours.

## Is MELON sold at all in days 0-11?

**Yes — 18 units, on day 11 — but none of it is day 6's batch.**
All 18 units trace to a different, earlier batch: 3 MELON seeds bought and planted on **day 0**.
Those 3 tiles reach age 10 exactly at day 10 (the maturity threshold), get watered up to the
6-unit cap that same day, and are harvested for 3 × 6 = 18 units on day 10
(`melon_tile_trace.py`: the three `planted_day: 0` tiles are present with `yield_units: 5` at dawn
day 10 and are gone — replaced by nothing, i.e. harvested — by dawn day 11). The 18 units sit in
the shed overnight and are sold at day 11, turn 0.

Seb's own tape does the same thing one day faster: harvest and sale both land on day 10 in Seb's
replay (`harv=18, sold=18` same day), while ours carries the harvest to day 10 and sells it on day
11 — a one-day lag in selling cadence, worth noting but separate from the melon question asked
here.

## Where does land-purchase money actually come from?

Our agent buys land three times in days 0-11 (`land_funding_probe.py`, cross-checked against
`melon_probe.py`'s independently-collected `buy_land_emitted_turns` column — same three turns in
both). List prices are fixed per `LAND_PRICES = [1000, 2000, 4000]` in
`reference/kaggriculture.py`; the money deltas below are net of everything else that same turn
(other buys, hires, and that turn's own sells), not the list price in isolation.

| day | turn | tiles unlocked | list price | money before → after | funded by |
|---|---|---|---|---|---|
| 4  | 22 | 25 → 50  | $1,000 | $283 → $225 (net -$58)   | WHEAT + FERTILIZER — no MELON exists in the shed yet at this point (0 units harvested to date) |
| 8  | 13 | 50 → 75  | $2,000 | $1,487 → $1,104 (net -$383) | FERTILIZER + WHEAT + MILK — MELON on hand is still 0 |
| 11 | 0  | 75 → 100 | $4,000 | $3,273 → $2,883 (net -$390) | **MELON** — see below |

The first two are unambiguous: at day 4 and day 8, zero MELON has ever been harvested
(`melon_probe.py`'s `dawn_total_melon` column reads 0 through day 10), so neither purchase can be
melon-funded regardless of turn order. Both are paid for out of the season's running wheat and
fertilizer sale cycle (wheat and fertilizer are sold in small amounts on nearly every day of the
window; see the per-day SOLD table in `melon_land_funding.log`).

Day 11 turn 0 is different, and checking it directly overturned an assumption I made mid-probe. My
first pass reasoned that since day 11's melon sale happens "later in the day," it couldn't have
funded a turn-0 land purchase. `day11_turn0_probe.py` checked this directly instead of trusting
that reasoning, and it's wrong: the full market order list our agent emits at day 11, turn 0, in
one shot, is

```
[SELL MELON 18, SELL FERTILIZER 3, HIRE, HIRE, HIRE, HIRE, HIRE, BUY_LAND, BUY_ANIMAL SHEEP, BUY_ANIMAL SHEEP]
```

shed MELON goes from 18 to 0 in that single `env.step`. Per the project's documented per-turn
commit order (SELL, HIRE, BUY_LAND, BUY_ANIMAL, BUY_SEED — see `schedule_agent.py`'s ordering
comments), the MELON sale settles before the land purchase in the same turn. So the day-11 land
purchase — the largest of the three, at $4,000 — **is** genuinely, same-turn funded in significant
part by melon revenue.

## Answering the user's pushback directly

The pushback was: melon must be getting sold at some point, or there'd be no money for land at
all. That's half right and half wrong, now that it's checked rather than assumed:

- Melon **is** sold in this window (18 units, day 11), and it **does** directly fund a land
  purchase — the last and biggest one, $4,000 on day 11.
- But the first two land purchases ($1,000 on day 4, $2,000 on day 8) predate any melon harvest
  entirely and are funded by wheat, fertilizer, and milk instead.
- And critically, the melon that funds day 11's purchase is **day 0's** three-tile batch, not
  **day 6's** six-tile batch. Day 6's batch is still standing in the ground, unharvested, at the
  end of the probed window — not because anything failed, but because MELON needs 10 days from
  planting and day 6 + 10 = day 16, outside days 0-11. Seb's own tape leaves its own day-6 batch in
  exactly the same unharvested state by day 11.

## Caveats

- This only covers days 0-11, the window asked for. Day 6's batch would first become harvestable
  around day 16; whether it eventually gets harvested/sold, and whether it funds anything later,
  is not answered here and would need the run extended.
- "Funded by X" above is read off the net money delta at the purchase turn plus the order list
  emitted that turn, not from re-deriving exact market prices; I did not import
  `reference/kaggriculture.py`'s `market_price` function to reconstruct exact per-unit sale prices,
  since the delta/order-list evidence was already unambiguous for all three purchases.
- The one-day selling lag (harvest day 10, sell day 11, versus Seb's same-day day 10 harvest+sell)
  is noted but not investigated further here — it wasn't the question asked, but it's the kind of
  gap that's worth a separate look if selling cadence becomes the topic.
