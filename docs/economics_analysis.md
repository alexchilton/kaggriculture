# Kaggriculture — Economics Analysis

> [!WARNING]
> **Superseded in part on 2026-07-31 by `docs/economics_q5_findings.md`.**
>
> The "Revenue per tile-day" table below is **wrong**.
> It reads the Object Types "Max yield / tile / DAY" column as a daily rate, but for ongoing
> crops that column is a *lifetime* total: `_daily_refresh_plants` stops producing once
> `production_count > max_yield`.
> Tomato is overstated 15x and strawberry 10x.
> Measured per-tile yields are in the findings document, and pinned by
> `tests/test_production.py`.
>
> Question 5 is **answered**. The rest of this document is kept as the day-1 reasoning, since
> its four-constraints framing and its PvP section still stand.

**Status: day-1 desk analysis. Arithmetic off the published tables, not yet simulated.**

Everything marked `[HYPOTHESIS]` needs confirming against the simulator before any of it is
built into an agent.
This file exists so that work starts from a quantitative prior instead of from intuition,
and so that a wrong prior is falsifiable rather than invisible.

The one thing that is **measured**, not inferred: the `starter` baseline finishes on
**$3512 from a $3000 start**. Any serious agent should be multiples of that.

## The four constraints

Ranked by how likely each is to be the binding one.

1. **Market absorption** — how much product the market will take before the price collapses.
2. **Routing / action budget** — units act on the tile they stand on, and movement costs an action.
3. **Capital in the first few days** — $3000 start, land costs $1k / $2k / $4k.
4. **Shed capacity** — 100 non-seed items, end-of-day overflow is **discarded**.

Land and labour are almost certainly *not* binding. See below.

## Labour is nearly free, and the field will underuse it

Hire cost is `farmHandCostMult * fib(n)` where `n` is hires already made that day,
resetting each morning. With the default multiplier:

| Hands hired in a day | Total cost | Extra actions bought |
|---|---|---|
| 5 | $12 | 120 |
| 8 | $54 | 192 |
| 10 | $143 | 240 |
| 12 | $376 | 288 |
| 15 | $1596 | 360 |

Twelve hands cost **$376 per day** and buy **288 extra actions per day**.
That is roughly **$1.30 per action**, against actions that move $20+ of product.

> **PARTLY REFUTED 2026-07-31 by measurement.**
> The per-day arithmetic above is right, but "close to free" ignores that you pay it **every one
> of the 30 days**. Twelve hands is $376/day = **$11,280 a season**; fourteen is $986/day =
> **$29,580**, which is more than the extra labour earns.
> Parameter search on the heuristic agent moved hiring *down* from 17 hands to 8 and gained
> ~13% on held-out seeds.
> Eight hands ($54/day, ~$1.6k a season) is close to free. Fourteen is ruinous.
> The cliff is steep because the cost is Fibonacci: hires 13 and 14 alone cost $610/day.

`[HYPOTHESIS]` Aggressive hiring is close to free money and most competitors will underhire.
The real cost of a hand is not the fee, it is that you must **route** it.
Movement is an action, and WATER / HARVEST / FEED / CARE only apply to the tile the unit occupies.

To water 100 tiles you need ~100 WATER actions plus ~100+ movement actions, so
**~250-300 actions per day**, which is ~10-12 hands.
Affordable. The hard part is the routing, which makes this a
**multi-agent vehicle-routing problem on a 10x10 grid with a 24-step horizon**.

`[HYPOTHESIS]` Routing quality, not crop choice, is where the leaderboard is won.

## Revenue per tile-day

> [!CAUTION]
> **This table is wrong — see the warning at the top.**
> The `Units/tile/day` column below is a misreading for ongoing crops.
> Measured values: wheat 0.93, carrot 0.97, tomato **0.27** (not 4.0), strawberry **0.20**
> (not 2.0), melon 0.40, egg 0.87, milk 0.37, wool 0.27.
> Kept here only so the error is visible rather than quietly deleted.

From the Object Types table (`Max yield / tile / DAY`) times price:

| Crop | Units/tile/day | At base price | At P(I0+T) | At P(I0+2T) |
|---|---|---|---|---|
| Wheat | 1.5 | $37.50 | **$30.00** | **$28.50** |
| Carrot | 1.333 | $46.70 | $13.30 | $1.30 |
| Tomato | 4.0 | $240.00 | **$96.00** | $36.00 |
| Strawberry | 2.0 | $240.00 | $2.00 | $2.00 |
| Melon | 0.5 | $125.00 | $0.50 | $0.50 |
| Egg | 2.0 | $100.00 | **$80.00** | **$78.00** |
| Milk | 1.0 | $160.00 | $1.00 | $1.00 |
| Wool | 0.67 | $134.00 | $0.67 | $0.67 |

Read the last two columns. **Wheat, Egg and Tomato are the glut-tolerant goods.**
Everything premium goes to the $1 floor on modest volume because they carry `above_target > 1`.

Wheat is the standout sink: `above_func=log, above_target=0.20` means
P(I0+400)=$20 and P(I0+800)=**$19**.
You can dump wheat effectively forever at ~$19-20 against a $10 seed that yields up to 6 units.
Eggs behave the same way (P(I0+664)=$39 against a base of $50).

## The correction to the naive read

The obvious day-1 conclusion is "premium goods always crash, so grow wheat".
That is **too simple**, and the reason matters.

Price is set by **cumulative net flow**: player sales *minus* town consumption.
Town consumption is not static — it ramps hard:

- Town centre consumes 1 of each non-fertilizer product every 12 turns = **2/day**,
  rising to **4/day after day 10** and **8/day after day 20**.
- Each unlocked shop consumes 1 of every product it demands every 4 turns = **6/day**
  (single-product shops 2x = 12/day).
- Shops unlock every 3 days from a pool of 8, so by day 24 **all eight are active**.

Worked example for strawberry, demanded by Brunch Spot, Ice Cream Shop, Smoothie Shop
and Farmers Market:

- Late-game drain: 4 shops x 6/day + town centre 8/day = **~32 units/day**.
- Supply: `T = 100` is one 5x5 field over 24 days, i.e. ~4/day.
  A player on all four quadrants makes ~16/day. Both players flat-out: ~32/day.

`[HYPOTHESIS]` **Supply and demand are roughly balanced at full commitment**, which means
premium prices do not inevitably collapse — they collapse only if you sell *faster than the
town drinks*, and the town drinks far more late than early.

> **RESOLVED 2026-07-31 — conclusion right, arithmetic wrong.**
> Premium prices do not collapse, but not because supply and demand balance.
> Measured drain is 536 strawberry a season against **6 units per tile**, so saturating
> strawberry demand needs 89 tiles and $8,933 of seed from a $3,000 start.
> Supply cannot reach demand, so the price is safe by impossibility rather than by balance.
> The `T = 100` reading above was right; the "~4/day" and "16/day" figures were not.

The strategic consequence, if this holds:

- **Selling premium goods early crashes them.** Few shops are unlocked, drain is ~2/day.
- **Selling premium goods late may fetch above base**, because drain has quadrupled and
  scarcity pushes price up (P(I0-100) = $204 for strawberry against a $120 base).
- **Wheat and eggs are timing-insensitive** and can be dumped whenever.

`[HYPOTHESIS]` The optimal shape is: wheat/eggs for baseline cashflow and animal feed,
premium crops harvested but **held**, then released into late-game demand.

## Storage is the plant, not the shed

The shed caps at 100 items and end-of-day overflow is destroyed, so you cannot stockpile
produce for a late dump in the obvious way.

But **ongoing crops and animals accumulate `yield_units` on the tile** up to their `max_yield`
(4-6 depending on type), and you choose when to HARVEST.
The tile is the warehouse.

The limit is decay: once a plant passes max lifespan, `yield_units` drops by 1 every other turn
until the tile becomes a weed.
For ongoing crops that clock starts one day after cumulative production hits `max_yield`.

`[HYPOTHESIS]` There is a real optimisation here — delay harvest to sell into late-game demand,
but not past the decay cliff. This is exactly the kind of thing offline search should solve
and a heuristic will get wrong.

## The one real player-versus-player lever

Both farms are **fully visible**: every tile, every crop, every `planted_day`.
You can compute precisely what the opponent will harvest and when.

Combine with the fact that premium goods floor at $1 on small volume, and there is a genuine attack:

> **Dump the good they are about to harvest, immediately before they harvest it.**

If they have committed 20 tiles to strawberry, flooring that price costs you very little and
destroys a large fraction of their season.
The defensive corollary: **hiding in wheat and eggs makes you attack-proof**, because those
curves do not crash.

`[HYPOTHESIS]` Almost nobody will be doing this early, and it may be the decisive differentiator
late in the competition.
Deliberately scoped **out of v1** — it is worthless until the base economy is strong.

## Things to verify first, in order

1. What does the `starter` agent actually do, and where does its $512 come from?
2. Sustainable revenue per tile-day under realistic price decay, simulated rather than
   read off a table.
3. What fraction of the action budget does movement consume at 25 / 50 / 100 tiles?
4. Does the opponent's selling measurably change your bank at all?
   Run two identical agents against each other, then one solo against `pass`, and diff.
   This tells us how much the two-player framing matters and whether self-play is needed at all.
5. ~~Does the town drain genuinely exceed player supply for premium goods, as hypothesised
   above?~~ **ANSWERED — see `docs/economics_q5_findings.md`.**
   Yes for every premium good except melon, because tile yield is the binding constraint and it
   is ~10x lower than this document assumed.
   Selling late beats selling early for *every* crop by 1.16x-1.75x.

Question 3 — the action-budget share consumed by movement — is now the highest-value unknown,
because every revenue figure in the findings document assumes the harvest actually gets
harvested.