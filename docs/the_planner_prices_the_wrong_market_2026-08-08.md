# The planner prices a market 49% bigger than the one we play in

2026-08-08, on `shaping-potential`.
Measurement: `data/logs/prices_recent.log`, `data/logs/revenue_danu.log`, `data/logs/whichagent.log`.

## The environment we test on is not the environment we play in

`kaggle_environments` as installed on this machine is **1.32.2**:

```
townCenterSellInterval default = 12
TOWN_CENTER_DEMAND_SCHEDULE = [(20, 4), (10, 2), (0, 1)]     # the post-day-10/20 ramp
MAX_SHOP_INSTANCES          -- absent
```

The ladder is **1.32.6**. Read straight off the `configuration` block of downloaded episode
91122388:

```
townCenterSellInterval = 24
townShopSellInterval   = 4
townShopUnlockInterval = 3
```

So the town centre drains **half as often** on the ladder, and 1.32.6 also deleted the demand ramp
that quadruples centre demand from day 20. Every local fixture in this project — the handover
harness, the arena pool, the +35% plan rebase, both sell-cap flags — was measured on a game with
roughly **1.5x the town demand of the real one**.

`reference/kaggriculture.py` is the 1.32.6 source and is correct. The *installed package* is not,
and it is the installed package that every script imports. Checking `reference/` and concluding
"we are on 1.32.6" is how this was missed; the check that matters is
`kg.__file__` and the JSON config next to it.

## What that does to the planner's market model

`kagg/search/scheduler.py:150` is the whole of stage 1's market awareness:

```python
units = min(y * n_tiles, C.DRAIN_UNITS[what] * OPPONENT_SHARE)
return units * base * 0.5 / R.SEASON_DAYS
```

`C.DRAIN_UNITS` (`kagg/search/chains.py:63`) is a hard-coded season absorption per product. Against
the ladder's configuration:

```
  product      DRAIN_UNITS  local 1.32.2  LADDER 1.32.6  overstated    $ ladder
  WHEAT                662           662            552       1.20x      13,800
  STRAWBERRY           572           536            426       1.34x      51,120
  MILK                 500           446            336       1.49x      53,760
  TOMATO               374           410            300       1.25x      18,000
  CARROT               338           410            300       1.13x      10,500
  EGG                  338           320            210       1.61x      10,500
  WOOL                 284           320            210       1.35x      42,000
  MELON                140           140             30       4.67x       7,500
  TOTAL                                                                 207,180

  planner believes the market is worth $308,160 ; on the ladder it is $207,180
```

**Melon is the extreme case and it is exact.** No shop carries melon, so its only drain is the town
centre: 719 steps / 24 = 30 ticks at a flat multiplier of 1, i.e. **30 units a season**. The 140 in
`DRAIN_UNITS` is 60 ticks at the old interval, ramped 1/2/4 across the season. Because melon has no
shop, this figure does not depend on the unlock draw at all.

The other seven rows *do* depend on the draw, and the ladder column above uses a 1.32.2 unlock
sequence (eight distinct shops, drawn without replacement) with a 1.32.6 centre interval. 1.32.6
draws shops **with replacement**, so a product's shop count can repeat and its true drain will move.
Treat the non-melon rows as indicative and the melon row as exact.

## The chain this completes

We sell roughly **110 melon a season** into a book that absorbs 30, which is why melon quotes at the
$1 floor on 462 of 719 turns. The same argument runs, less violently, through wool and milk.

The failure is not in the sell rule. It is upstream: stage 1 sizes production against an absorption
figure calibrated on a different game, the surplus has to go somewhere, and the sell rule's only
remaining choice is which day to dump it.

## What the ladder games say the surplus costs

Twelve recent ladder games, same agent, price actually achieved per unit:

```
  product       base |  OURS-WIN units   $/u |  OURS-LOSS units   $/u |  ALL FOES units   $/u
  MELON          250 |             984   150 |             247   111 |           1,050   153
  WOOL           200 |           1,950   147 |             398   127 |             896   141
  MILK           160 |           2,082   205 |             321    73 |           1,405   161
  STRAWBERRY     120 |           2,711   182 |             562    78 |           1,366   154
  FERTILIZER     100 |           2,837    64 |             513    48 |           1,453    51
  WHEAT           25 |           9,115    45 |           1,693    49 |           7,124    48
```

Wins and losses are indistinguishable in board state — same tiles, same herd, same land day — and
differ almost entirely in the price we realise on **milk and strawberry**. Wheat is *better* in the
losses. Caveat: the loss column is two games and one of them is a mirror, where by construction an
identical seller contests every book. Episode 91120630 (Danu A.) shows the effect on its own, with
milk at $53/unit.

## The missing term

`schedule_agent.py:2487` reads the live book, but reads it as though we were the only seller:

```python
n = min(have, reservation_units(
    prod, market_inv.get(prod, ...), day * TPD + hour, unlocked_shops, have + standing[prod]))
```

There is no term for rival supply. A heavy opponent collapses our milk price without ever deciding
to, and the rule cannot see it coming. `OPPONENT_SHARE = 0.5` in `scheduler.py:107` is the same
quantity as a fixed dial, and Fable's `contest` term
(`λ_p = market_price(p, I_now + Q_rem − contest·D_rem)`, `docs/fable_market_technique_2026-08-08.md`)
is the same quantity again, also as a dial. Three places, one unmeasured number.

Separately, no cap in `schedule_agent.py` compares two *different* products, so the shared 100-slot
shed — wheat holding 41-45 slots at $25 base while milk holds 0-9 at $160 — is not expressible in
the sell rule at all.

## Scope correction: stage 1 does not ship

Grepping the bundle rather than the repo:

```
  DRAIN_UNITS          0
  OPPONENT_SHARE       0
  revenue_rate         0
  reservation_units    3
  cover              101
  _PLAN_JSON           2
```

**`scheduler.py` is not in `submission/main.py`.** The drain table above describes a component that
has never played a ladder game. What ships is a production mix copied wholesale from a recorded
tape (`_PLAN_JSON`), a covering day planner that optimises a movement tour with no price term in
its objective, and `reservation_units` — the only place a price enters the agent at all.

So the corrected drain figures are a *precondition* for wiring stage 1 in, not an explanation of
current losses. Wiring it in first would size the farm against a market 40% too large.

## What the upgrade costs, measured

Same suite, same invocation, both versions:

```
  1.32.2   14 failed, 909 passed, 70 skipped, 5 xfailed
  1.32.6   30 failed, 893 passed, 70 skipped, 5 xfailed
```

18 new failures, 2 fixed, 12 unchanged. The new ones are not random — they are three real groups:

- **`test_shop_unlocks.py` (7)** — these hard-code 1.32.2 drain and price measurements as
  expectations. They are old measurements written down as tests and must be re-baselined.
- **`test_sim_ops.py` movement (3) + `test_pens_do_not_block_the_depot_ring` (1)** — 1.32.6 allows
  movement onto LOCKED tiles and our `kagg/sim/` still blocks it. A genuine parity divergence.
- **`test_sim_town.py` (2)** — our town drain model is the 1.32.2 one. Genuine divergence.
- **`test_storage.py` (3)** and **`test_water_cadence.py` (1)** — shed-cap and melon behaviour,
  not yet diagnosed.

The two that the upgrade **fixed** are the confirmation that this direction is right. One of them is
`test_unlocks_land_every_third_day_until_eight_shop_INSTANCES_are_open`, written tonight to assert
`kg.MAX_SHOP_INSTANCES` — a constant 1.32.2 does not have. It was red because the environment was
wrong, not because the test was.

## What must happen before any of this is tuned

Fixing `DRAIN_UNITS` against the wrong environment would bake the error in. Either pin the local env
to the ladder's configuration explicitly, or pass `townCenterSellInterval: 24` into every harness.
Until then a local number and a ladder number are answers to different questions.
