> **STALE, flagged 2026-08-22.** Two claims in this file are contradicted elsewhere and were never
> corrected in place. §"the deciding number" total `152,792 -> 164,928 (+12,136)` compares against an
> infeasible baseline; `docs/fable_allocation_economics_2026-08-15.md` gives the real release value
> as **+$5,653**. The falsifiable prediction at the end (`MELON_YIELD_OPPONENT_MELON = 99` beats the
> shipped `= 7`) was tested on 960 games and falsified — the shipped rule narrowly won, 68.1% vs
> 67.9% (root `RETRACTIONS.md`, item 7). Read the mechanics sections (market-impact curves) as
> reference; do not quote the total or the prediction from this file.

# When and what to sell — an optimisation analysis

Written 2026-08-15. Every number here is computed from `reference/kaggriculture.py` and the shipped
plan (`kagg/plan.py:SHIPPED_PLAN`), not measured in a game. **It is a model, not a result.** The
falsifiable prediction at the end is the part that can be checked.

---

## 1. The mechanics that decide everything

Selling raises market inventory, and inventory starts at `MARKET_I0 = 10000`. So a sale pushes the
book **above** `I0`, which means the `above_func` / `above_target` pair governs price impact — not
the `below_*` pair that the 2026-08-15 balance change altered.

    price(I0 + x) = base - (above_target * base / shape_above(T)) * shape_above(x)

Two knobs matter: the **shape** and the **knee `T`**. A small `T` with a convex shape is brutal.

### How far a sale moves the book

    product      base  shape  atgt    T    -10%   -50%  FLOOR   $/unit at 20 sold
    STRAWBERRY    120  linear  1.6  100       6     31     62                  82
    MILK          160  linear  1.6  122       8     38     75                 118
    WOOL          200  sq      3.2  105      19     42     59                 177
    MELON         250  sq      3.6  300      50    112    157                 246
    TOMATO         60  sqrt    0.6  200       5    135    529                  49
    CARROT         35  sqrt    0.7  450      10    230   5000                  30
    FERTILIZER    100  linear  0.4  200      48    248    488                  96
    EGG            50  log     0.2  332      13   5000   5000                  45
    WHEAT          25  log     0.2  400      20   5000   5000                  22

**STRAWBERRY loses 10% of its price after SIX units. MILK after eight.** WHEAT and EGG are
effectively undentable — a log curve with `atgt 0.2` never dies.

### What the town takes back

`_town_consume` runs every `townShopSellInterval = 4` steps (6 times a day) and every
`townCenterSellInterval = 24` steps (once a day). Each unlocked shop instance consumes one unit of
each product it stocks, doubled if the shop stocks only one product.

    product     shops that buy it (units/day each)              town  max/day
    WHEAT       bakery:6 pizza:6 brunch:6 ice:6 farmers:6          1       31
    STRAWBERRY  brunch:6 ice:6 smoothie:6 farmers:6                1       25
    CARROT      pet:12 farmers:6                                   1       19
    MILK        pizza:6 ice:6 smoothie:6                           1       19
    TOMATO      pizza:6 farmers:6                                  1       13
    EGG         bakery:6 brunch:6                                  1       13
    WOOL        yarn:12                                            1       13
    MELON       — no shop stocks melon —                           1        1

Shops unlock one per three days, drawn **with replacement**, capped at `MAX_SHOP_INSTANCES = 8`. So
the drain ramps through the season and its composition is a random draw — which is what
`SHOP_ADAPT_HERD` is reading.

**MELON has no shop. The town absorbs one melon a day, thirty for the whole season.**

## 2. Supply against absorption

The shipped plan's season sell totals:

    product      plan sells  drain/day  days to absorb  verdict
    FERTILIZER         1487          0               -  NOTHING DRAINS IT
    WHEAT               868         31            28.0  tight
    MILK                279         19            14.7  ok
    STRAWBERRY          223         25             8.9  ok
    WOOL                120         13             9.2  ok
    MELON               120          1           120.0  4x OVER THE SEASON
    CARROT               20         19             1.1  ok

Two lines break the budget: **melon at 4x season absorption**, and **fertilizer, which no shop and
no town centre ever removes.** Fertilizer is `BUYABLE`, so the only thing that restores its book is
an opponent buying it back.

## 3. What spreading is worth

Simulating each product's season — walk `n` units down the curve each day, then let the town remove
its drain — for the plan's own day-by-day schedule against a flat spread of the same total:

    product      units    plan $    even $     delta   $/unit plan   even
    MELON          120    24,968    26,763    +1,795           208    223
    MILK           279    38,146    42,219    +4,073           137    151
    WOOL           120    23,886    23,970       +84           199    200
    STRAWBERRY     223    20,810    25,331    +4,521            93    114
    WHEAT          868    18,272    19,906    +1,634            21     23
    FERTILIZER    1487    26,039    26,039        +0            18     18
    CARROT          20       671       700       +29            34     35
    TOTAL                152,792   164,928   +12,136

**About $12k of pure scheduling gain**, concentrated in STRAWBERRY (+4,521) and MILK (+4,073) — the
two products with a linear above-curve and a knee under 125.

Caveat: an even spread is not always feasible. Melon is a one-shot crop with `first_yield_day 10`,
so it cannot be sold before d10 — but it can be held later at no cost beyond shed space. Milk and
strawberry accrue continuously and are genuinely spreadable.

## 4. The melon branch — the rule may be backwards

`MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT` swaps our melon rows to strawberry when the opponent holds
`>= MELON_YIELD_OPPONENT_MELON = 7` melon at d5. It fires in about 68% of games and shipped on
2026-08-15 on tape evidence alone.

The plan front-loads **60 melons on d10** and trickles the rest (d11 +12, d16 +6, d17 +30, d18 +12).
Into a 1/day drain that is a race: whoever loads the book first gets the good prices.

Simulating a shared book, both seats interleaved one unit at a time as `_process_market` does:

    case                                          melon $   straw $   OUR TOTAL
    A  keep melon   | opponent sells NO melon      24,968     9,909     34,877
    B  keep melon   | opponent sells the SAME 120  13,549     9,909     23,458
    C  swap→straw   | opponent sells NO melon           0    15,296     15,296
    D  swap→straw   | opponent sells the SAME 120       0    15,296     15,296

**Even in the melon-heavy case the rule exists for, keeping melon beats swapping by $8,162.**

The reason is that strawberry is already saturated. 223 units into a 25/day drain is near the limit;
adding 120 melon units on top returns only **+$5,387, or $45/unit**, while contested melon still
pays **$113/unit**. Melon's base is $250 against strawberry's $120, so a crushed melon outsells a
crushed strawberry.

Model limits, stated plainly: melon units are converted to strawberry **1:1**, which flatters the
swap (melon yields 6/tile against ongoing strawberry's 4); the swap shifts revenue from d10–d18 to
d15–d29, which interacts with land purchases and is not modelled; and the opponent's melon flow is
assumed to follow the schedule's shape.

## 5. The policy this implies

1. **Classify by drain, not by price.** A product is either drain-limited (sell at the drain rate,
   spread) or robust (sell whenever convenient). WHEAT, EGG and CARROT are robust — their timing is
   worth almost nothing. STRAWBERRY, MILK, WOOL and MELON are drain-limited and timing is worth
   thousands.
2. **For drain-limited products, target the drain rate, and compute it from the LIVE shop draw.**
   `town_drain_remaining` already exists in `schedule_agent.py` and mirrors `_town_consume`, so this
   is readable from the observation rather than estimated. The current sell rule uses `rate[prod]` —
   the largest single day one recorded replay asked for — which is a fact about his production, not
   about the market.
3. **Front-load only where the book is a race.** Melon's 1/day drain means the book never recovers,
   so first mover takes the price. That is what his d10 sixty-melon dump is, and it is correct.
4. **Never let a fragile product accumulate.** Milk hits −10% after eight units; a shed holding 60
   milk cannot be liquidated at any decent price. This is the mechanism behind the observed ladder
   losses where milk cleared at $1–$7.

## 6. The experiment worth running

Opponents run fixed or near-fixed tapes, so their sell flow is exogenous and knowable. That makes
our problem a **best response to a known flow**, and it is searchable:

1. Extract each recorded ladder opponent's per-day sell vector per product from their replays.
   This is a read, not a simulation.
2. Perturb it — shift each product's sell days by ±1, ±2, ±3 — to model the variants of a fixed
   tape that the field actually contains.
3. For our own production, search the release schedule that maximises revenue against that
   distribution of opponents, subject to production availability and shed capacity.
4. Because the price curve is convex and the drain is linear, the interior optimum equalises
   marginal revenue across days. The search only has to handle the boundaries: production not yet
   available, shed capacity, and the melon race.

## 7. Falsifiable prediction

Made **before** the data landed, on 960 games against 24 recorded ladder opponents:

> `MELON_YIELD_OPPONENT_MELON = 99` (rule off) should beat `= 7` (rule as shipped).

If the sweep comes back the other way, this model is wrong and the reason is worth more than the
model was.
