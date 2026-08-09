# The book is shallow, and our production ignores it

> **CORRECTION, same day.** Every absorption figure below was measured PASS-vs-PASS and described
> as "a property of the board with no agent involved". **That is wrong.** `_spawn_weeds` draws from
> the same per-day rng *before* the shop unlock (`reference/kaggriculture.py:856-878`), and weed
> spawning depends on which tiles are empty -- so how the agents play shifts the stream and changes
> which shop is drawn. Measured:
>
>     seed 13  PASS: YARN, BAKERY, PIZZA, YARN, ICE_CREAM, FARMERS, PIZZA, BRUNCH
>              REAL: SMOOTHIE, ICE_CREAM, YARN, ICE_CREAM, FARMERS, YARN, YARN, ICE_CREAM
>     seed 29  PASS: PET_CAFE, FARMERS, BRUNCH, ICE_CREAM, BAKERY, BAKERY, BRUNCH, BRUNCH
>              REAL: BRUNCH, FARMERS, ICE_CREAM, YARN_STORE, PET_CAFE, PET_CAFE, BAKERY, BAKERY
>
> So seed 29 is NOT wool-starved under real play -- it draws a YARN_STORE -- and the "WOOL starved
> on 5 of 12 boards" claim describes boards our agent never sees. The 34% figure for
> P(no YARN_STORE) is still correct, because it comes from the draw being uniform over 8 shops with
> replacement, which no gameplay changes.
>
> What survives untouched: the price-curve table (verified against `kg.market_price` itself by
> `tests/test_the_price_curve_math.py`), the realised-price and two-way results (measured under real
> play throughout), the shop-count table, and the fact that MELON is carried by no shop on any board.
>
> What must be redone: absorption per board, computed from the shop timeline observed during real
> play rather than from a PASS game. It also means a seed cannot be catalogued by constellation --
> the mapping is agent-dependent, so a sweep must dictate `unlocked_shops` rather than search seeds.

**2026-08-09.**
Supersedes the "delivery problem" framing from earlier the same day.
That framing was wrong and the measurements behind it were wrong in two separate ways; both are
recorded here because the mistakes recur.

## The claim that started it, and why it was false

High-value produce (MILK, WOOL, MELON, STRAWBERRY) appeared to sit in workers' hands at dusk
rather than in the shed, where `SELL` can see it.
The shipped agent showed **443 such units on seed 13**, and that was read as a delivery bug.

Counting actual fills with `kagg/analysis/fills.py` instead of snapshots:

| seed | MILK made/sold | WOOL made/sold | MELON made/sold | STRAWBERRY made/sold | left in shed | left in hands |
| --- | --- | --- | --- | --- | --- | --- |
| 13 | 228 / 249 | 165 / 169 | 84 / 84 | 278 / 294 | 0 | 0 |
| 17 | 264 / 278 | 161 / 163 | 78 / 78 | 280 / 293 | 0 | 0 |
| 29 | 204 / 217 | 161 / 161 | 84 / 84 | 287 / 313 | 0 | 0 |
| 41 | 242 / 251 | 152 / 155 | 84 / 78 | 272 / 284 | 0 | 0 |

We sell 100-109% of everything produced, nothing is left on the farm at season end, and the shed is
at capacity on 2-6 hours out of 720.
(Sold exceeds made because the production counter samples at turn start, so a unit harvested and
sold inside one `env.step` is never observed.
Production is undercounted; sales are not inflated.)

**There is no delivery problem, no discard problem and no shed-capacity problem.**

### Two measurement errors, both a snapshot standing in for a flow

1. **A raw count compared across agents with different herd sizes.**
   The `1455m` graft stranded 134 units against the shipped agent's 443 and looked like the better
   deliverer. It had lost 11 animals to the shipped agent's 1, so it made less milk and wool and
   therefore stranded less of it.
   The scale-free version is `hi_held / (hi_held + hi_shed)` at one instant.

2. **Sampling at dusk.**
   Dusk falls *after* the day's harvest has accumulated in hands and *after* the day's selling has
   drained the shed, so the numerator is at its maximum and the denominator at its minimum by
   construction.
   Produce in a hand at dusk is a pipeline in flight.

A third, smaller one: the hand-turn census reported `idle 0.0%` and "the crew is saturated".
The environment's idle op is named **`PASS`**, not `IDLE`, so the bucket caught nothing.
The real split is **24% idle, 42% walking, ~34% working** — there is slack, and herd work and
harvest work are not competing for a fixed budget.

## Where the money actually goes

The same seasons, read as revenue per unit:

| seed | MILK $/unit | WOOL $/unit | final bank |
| --- | --- | --- | --- |
| 13 | 252.66 | 229.23 | 163,036 |
| 17 | 111.51 | 236.51 | 126,151 |
| 29 | **27.90** | 219.29 | 77,254 |
| 41 | 197.71 | **39.65** | 100,464 |

Seed 29 sold *more* milk than seed 13 and banked **$6,054** for it against **$62,913**.
Same agent, same code, same schedule, same opponent tape.

### The curve is far steeper than the melon case everyone has curved

`market_price` (`reference/kaggriculture.py:179`) is a pure function of the book's inventory
relative to `I0 = 10,000`:

    price = base - (above_target * base / shape(above_func, T)) * shape(above_func, inventory - I0)

Inverting for the surplus that reaches the `$1` floor:

| product | above_func | T | units above I0 to floor |
| --- | --- | ---: | ---: |
| WOOL | sq | 105 | **59** |
| STRAWBERRY | linear | 100 | 62 |
| MILK | linear | 122 | **76** |
| MELON | sq | 300 | 158 |
| WHEAT | log | 400 | effectively unfloodable |

The community meta notebook
(`reference/community_notebooks/kaggriculture-findings-from-zero-to-top-meta/`, cell 6) already
walks this curve — **for melon only**, which at 158 units is the *shallowest-sloped* of the
premium products. Wool floors at roughly a third of that, and a season produces 150-280 units of
each.

WHEAT's `log` shape is why it behaves nothing like the rest of the table and why volume there is
nearly free. That is a property of the price parameters, not of anything we do.

## Board versus opponent: both, and it splits by product

Two-way design, 6 tape opponents x 6 seeds, 36 seasons (`data/logs/price_two_way.log`).
A tape is open-loop, so an opponent emits the same order sequence whatever the seed, which makes
the opponent factor genuinely fixed down a column.

    ===== MILK $/unit =====                    ===== WOOL $/unit =====
    opponent          13     17     29     41     53     67        13     17     29     41     53     67
    HealthStone   238.74  69.85  26.64  75.06  88.20 216.17     85.77  21.20  21.44 237.29  59.94 114.78
    Mohamed       254.98  98.55  33.21 200.38 232.10 217.47     38.62  45.63  55.55  38.63  31.23  35.46
    Phi           255.15 114.49  36.12 203.77 246.75 217.89     38.62  40.83  34.78  63.17  33.23  35.46
    Seb           252.66 111.51  27.90 197.71 247.49 258.22    229.23 236.51 219.29  39.65  62.94  62.60

    mean spread ACROSS SEEDS, opponent fixed :  88.5 (milk)    49.0 (wool)
    mean spread ACROSS OPPONENTS, seed fixed :  54.1 (milk)    73.1 (wool)

**MILK is board-driven. WOOL is opponent-driven.**
Seed 29 floors milk against every opponent ($26-36); seed 13 holds it against every opponent
($238-255).
Wool inverts: on seed 13 it is $229 against Seb and $39 against Phi.

The mechanism is the shop table:

| opponent | milk they sold | wool they sold | our milk $ | our wool $ |
| --- | ---: | ---: | ---: | ---: |
| HealthStone | 201 | 93 | 103.20 | 120.79 |
| Mohamed | 213 | 148 | 172.78 | 40.85 |
| Phi | 213 | 148 | 179.03 | 41.01 |
| Seb | 176 | 58 | 157.32 | 115.69 |

WOOL is sold by **one shop of eight** (`YARN_STORE`), so its demand is thin on every board and
whoever else dumps it sets the price.
MILK is in three of eight, so the *draw* moves its demand more than the opponent does.

The same agent banks between **$16,888 and $163,036** across these 36 seasons with no code change.
A single-seed, single-opponent comparison is therefore noise, and a $30k difference between two
variants sits well inside one variant's spread against itself.

## What the seed controls, and what we can see

The seed touches exactly two things (`reference/kaggriculture.py:856-878`):

    rng = random.Random((seed * 1_000_003) ^ day)
    ...  _spawn_weeds(farm, board_size, weed_chance, rng)           # weeds
    ...  town["unlocked_shops"].append(rng.choice(sorted(SHOPS)))    # which shops unlock

Shops are the demand side: `_town_consume` removes stock per unlocked shop instance, per product
that shop sells, every 4 turns, against the town centre's 1 unit per product per 24 turns.
Drawn **with replacement**, one every 3 days, maximum 8 instances.

| product | shops selling it | P(never drawn in 8) |
| --- | ---: | ---: |
| WHEAT | 5 of 8 | 0.2% |
| STRAWBERRY | 4 of 8 | 2.3% |
| MILK | 3 of 8 | 2.3% |
| WOOL | **1 of 8** | **34.4%** |
| MELON | **0 of 8** | always |

**The seed itself is deliberately hidden.** `reference/kaggriculture.json` states that the
interpreter clears `seed` from the configuration and stores it on `env.info['seed']`
"so it stays out of agent observations".

**The shop draw is not.** `town` is `shared: True`, so `town["unlocked_shops"]` is readable every
turn. The cause is hidden; the part that matters is fully observable.

## The actual gap

The **sell** side already uses all of this and is not the problem.
`town_drain_remaining` (`kagg/search/schedule_agent.py:1228`) mirrors `_town_consume` exactly,
`reservation_units` prices against the book's remaining absorption, and `PRICE_AWARE_SELL_CAP`,
`RESERVATION_SELL_CAP` and `HOLD_A_FLOORED_BOOK` all ship ON.
The per-product depth numbers were derived there already.

The **production** side ignores the draw completely.
The schedule commits to cows, sheep and crops from a fixed target sheet decided before the board
is known, and nothing in that path consults `town["unlocked_shops"]`.
On a board that never draws `YARN_STORE` we still buy sheep, and their wool is worth a fraction of
base however well it is later sold.
Shops unlock one every three days, so two or three are known by day 6-9, while most animal buying
is still ahead.

The community notebook reached the same place from replays rather than from the price table:

- cluster D, the adaptive leaders: "Dynamic cow/sheep/goose mix — **rebalances when milk is
  contested**";
- its own bug table: "Fixed 10 cows forever → mirror banks collapse toward ~40k → **fix: add
  sheep/strawberry/opponent routing**".

## Open, and separate

**Animal loss.** Shipped loses 1 animal on seed 13, `1455` loses 4, the `1455m` graft 8-11.
`consecutive_unfed >= 2` deletes the animal outright (`reference/kaggriculture.py:786`), so it is
irreversible, and a final bank cannot show it — a late loss barely dents the total while
destroying an asset that pays out every remaining day.
This is not the same defect as the price collapse and must not be traded against it.

## Method note

Both wrong turns were a snapshot substituted for a flow, and both were caught by instrumenting the
one function that moves goods and money together.
`kagg/analysis/fills.py` documents three earlier versions of the same mistake.
Start there before building a fourth proxy.
