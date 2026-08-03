# What the public notebooks say, and what it means for the RL

**Date:** 2026-08-03, evening.
**Source:** four notebooks pulled from the competition's public code page via the Kaggle API and
saved under `reference/community_notebooks/`. Alex pointed at the page; everything below is from
those files, not from inference.

## The scale gap

| | bank |
|---|---:|
| top public agents, head-to-head, full 720-turn episodes | **$90,000 – $123,000** |
| `raykkretzschmar` c16 ladder rating | 2182 |
| `kaitofukami` v16 verified public LB | 2592.4, mean reward 123,186 |
| **our policy at update 690** | **$18,332 median, $34,127 best** |
| our best training opponent (`farm`) | $27,340 |

**We are training against a pool whose ceiling is a quarter of the field's floor.**

## The single most urgent finding: melon is the wrong crop

`romanrozen/strong-statr-baseline-agent-lb-950` measured live market prices in the current meta:

```
STRAWBERRY 280   MILK 263   WOOL 235   MELON 54   WHEAT 58
```

Base prices are 120/160/200. Strawberry, milk and wool trade **well above base** because the town
drains faster than two farms can supply. **Melon has collapsed to 22% of base** because everyone
dumps it on day 10.

**Our policy plants 77% melon** (`crop MELON:0.77` in tonight's log) and sells wheat on 29% of turns.
It has optimised into the two most crashed products in the game.

That notebook also records the same mistake costing its author ~40,000 points: *"play the `log`
products — eggs and wheat — which you cannot crash. **That is exactly backwards.**"*

## Action economy: hands are nearly free, and we have two

| hands | 6 | 8 | 10 | **12** | 14 | 16 |
|---|---|---|---|---|---|---|
| coins/day | 20 | 54 | 143 | **376** | 986 | 2583 |

Hire cost is `fib(n)`, so the first ~10 hands are cheap and 12+ gets expensive fast. Twelve hands cost
**376 coins for 288 extra actions — about 1.3 coins each**, against one in-window melon watering
worth **$250**.

We run **1.96 hands** at `hire_rate 0.067`. The leader census (`prvsiyan`, episode 89517103) and the
public agents both sit at **12 hands, `hire_rate` 0.42**.

## Value per action, measured

| action | value |
|---|---:|
| melon, in-window watering | **≈ $250** *(while price holds — it currently does not)* |
| cow, fed + cared | ≈ $95 |
| sheep, fed + cared | ≈ $86 |
| **`COLLECT_FERTILIZER`** — free, every animal, every day | **≈ $85** |
| goose, fed + cared | ≈ $32 |
| strawberry | ≈ $37 |
| wheat | ≈ $17 |

`COLLECT_FERT` costs nothing and pays $85. Our op census reads **`fert+: 0.00–0.18%`**.

## The public meta, in three clusters

From `raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta`:

- **A. Pure cow ranch** — 3-10 cows, little crop. Punishes crop-only bots.
- **B. Melon IPO** — 16 melons + 2 cows, day-10 dump. Huge if uncontested; hits the $1 floor if a
  second dumper shows up.
- **C. Staged economic herd (the C0x family)** — 3 cows + 1 sheep floor, staged 4 → 8/10 → 14/15.
  Strongest public code family.

The current common plan (c16): **8 cows, 5 sheep, 5 strawberry plots, 12 hands.**

`beicicc/kaggriculture-c04-target-herd-15` ships that as code, and its tunables are explicit:

```
MAX_HANDS = 12       TARGET_HERD = 15     CORE_HERD = 4      MID_HERD = 8
HERD_EXPANSION_DAY = 7    HERD_FINAL_DAY = 11    ANIMAL_PURCHASE_LAST_DAY = 18
FEED_STOCK_DAYS = 3       MELON_TILES_BASE = 10  MAX_EXTRA_LAND = 2   CASH_RESERVE = 250
```

We run **crew 2, herd 0**.

## Two engine facts worth checking against our sim

1. **Melon is ripe at day 10, not 12.** `max_yield_day = 12` implies the window starts at
   `ceil(12/2) = 6`, ages 6–12, cap 6 — so full water reaches max at **age 10**. Days 11 and 12 add
   nothing. Missing water on days 6–10 silently yields ~70 instead of ~96 on 16 tiles.
2. **`SELL` only sees the shed.** Harvest 90 melons and never `DROP` while shed-adjacent and the
   market cannot see them until the end-of-day auto-drop — often too late to fund same-turn land or
   animal buys.
3. **Unsold stock scores exactly zero at day 30**, hence the liquidation glide path
   `floor_q = ceil(have / max(1, days_left - 1)) if days_left <= 12 else 0`.

Fact 3 is a candidate explanation for the end-of-season bank collapse
(`docs/fable_review_animals_2026-08-03_evening.md`) that neither review could diagnose.

## What this says about self-play

**Self-play pressure is bounded by the pool it plays.** Our pool is frozen copies of an $18k policy
plus scripts topping out at $27k. Nothing in it demands $90k, and nothing in it plays cows, sheep,
strawberry, fertiliser collection or a twelve-hand crew — so those strategies are not merely
undiscovered, they are never *demonstrated*, and there is no opponent that punishes their absence.

`HANDOFF.md` already recorded the narrower version of this: *"no opponent in the pool ever uses the
animal economy"*, which is now only half-true (`jax_rancher` exists) but still true of crops,
fertiliser and crew size.

The honest read is that self-play will keep improving against *this* pool and that improvement will
increasingly fail to transfer, because the pool's strategy space is a strict subset of the field's.

## What follows

1. **Port a winner-class opponent.** `beicicc/c04` is 1,704 lines of readable Python with explicit
   constants, and `kagg/agents/homestead.py` already encodes the mixed-farm shape in numpy. A
   `jax_homestead` at 12 hands and a 15-animal herd would be the first training opponent above
   $30k.
2. **Check the crop mix against live prices.** Being 77% melon is defensible in our sandbox and
   probably wrong on the ladder. This is measurable today with `arena.evaluate` against
   `contrarian`/`converter`, which no RL script has ever run.
3. **`COLLECT_FERT` is free money we never take.** $85 per animal per day for one action, at 0.00–0.18%
   of ours.
4. **Verify the day-10 melon window and the shed-visibility rule** against our simulator. Both are
   engine facts a strong agent depends on, and if our sim differs, every number we have is measured
   in a different game.