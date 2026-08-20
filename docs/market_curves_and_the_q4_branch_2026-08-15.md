# The market curves, and what they say about allocation

Written 2026-08-15.
Everything here is computed from `reference/kaggriculture.py` or measured with one OS process per game.
Where a claim is one seed, it says so, because a single seed turned out to be worth almost nothing.

---

## 1. The shared book is the whole game

`_process_market` reads ONE market object off player 0's observation and drains it per unit in
lockstep between both seats (`reference/kaggriculture.py:544-547`).
Every unit the opponent sells lowers our price.
Prices are therefore a race, not a private resource.

`FEED` consumes exactly 1 WHEAT per animal per day, taken from the shed
(`reference/kaggriculture.py:505-512`), so wheat is a consumable as well as a product.

## 2. Every product's price curve, computed

Price as a function of book position, where negative means the town has eaten more than both farms
grew:

```
  surplus   WHEAT  CARROT  TOMATO   STRAW   MELON   MILK   WOOL    EGG
    -1200      60     906   5,004     411     312    461    261
     -800      53     267   1,884     358     309    406    257
     -400      45      66     300     288     303    334    251
     -100      35      43      72     204     290    247    240
       +0      25      35      60     120     250    160    200     50
     +100      21      23      35       1     150      1      1     42
     +200      21      19      24       1       1      1      1
     +400      20      12       9       1       1      1      1
    +1000      19       1       1       1       1      1      1     38
```

Three structural facts fall straight out of this.

**Wheat cannot be crashed, but it can be halved.**
Its whole downside is $25 to $19 even at +1000 surplus.
But the range actually in play is $21 (surplus) to $47 (deficit), and we grow ~800 units into that
book, so growing more wheat really does cost real money per unit.
"Monotonically safe" was wrong; "never goes to $1" is what is true.

**TOMATO and CARROT are the only two crops with a `hinge` undersupply curve**, which is quadratic
past `u = x/T > 1`.
Tomato at -400 deficit is $300, at -800 it is $1,884, at -1200 it is $5,004.
That, and not yield, is why tomato is "viable in ~50% of games": the top players grow zero tomato
across 40+ recorded games, so the supply side is empty by construction and the price is whatever the
shop draw makes it.
Melon is the opposite -- `log` on the upside, so it never spikes.

**EGG is the only animal product that cannot be crashed.**
Milk decays linearly and wool decays quadratically; both reach $1 at about +100 surplus.
Egg decays logarithmically and holds ~$38 at +1000.

## 3. When the books actually crash

Seed 3, contested, both seats shipped:

```
 day    MELON   STRAWB   TOMATO   CARROT    WHEAT
   0      250      120       60       35       25
  10      271      181       61       36       36
  13       94      195       62       36       40
  20       96      216       62       37       45
  26      111      147       63       38       42
  29      118       59       63       40       41
```

**Melon is a three-day race, d11 to d14.**
It climbs to $271 because the town eats it before anyone harvests, then both farms' melon lands and
it falls to $81.
Sell on d10-d11 and get $250+; sell on d14 and get $81.

**Strawberry peaks at $216 on d20** -- 80% over base, and worth more than double melon from d15 --
then collapses to $59 over the last six days as our own harvest lands.
We sell our best product in its worst week.

Melon recovers late (to $118 by d29) because its decay is `sq`: 10 units of town drain buys back $24
a unit near the top of the surplus.

In replay `93372504`, WOOL floored on **d16** at +59 surplus and MILK on **d24** at +76.
Our 10 cows against their 8 changed nothing -- both books died for both seats.

## 4. Which seeds want which crop

Both seats grow no tomato and no geese, so these columns are the town's appetite alone.
Scanned with real agents, because the shop draw comes off the same RNG that weed spawning consumes.

```
 seed  TOMATO d29  CARROT d29  EGG d29   shops by d6
    5          83          63      120   FARMERS_MARKET,BRUNCH_SPOT
    7          64          32      305   BRUNCH_SPOT,BAKERY
   11         216          75       75   FARMERS_MARKET,BAKERY
   15         356          62       59   FARMERS_MARKET,ICE_CREAM_SHOP
   16          72          40      211   BRUNCH_SPOT,BRUNCH_SPOT
```

`YARN_STORE` unlocks by d6 on **15 of 100 seeds**: `[3, 10, 17, 18, 22, 45, 47, 53, 60, 65, 66, 73,
79, 82, 95]`.
Shop frequencies in the first 7 days: BRUNCH_SPOT 28%, BAKERY 27%, PET_CAFE 26%, ICE_CREAM_SHOP 25%,
FARMERS_MARKET 21%, PIZZA_SHOP 19%, SMOOTHIE_SHOP 19%, YARN_STORE 15%.

## 5. The season is chaotic, and single-seed deltas are worthless

The sim is deterministic -- the same baseline run twice on seed 3 gave $133,221 both times.
Deterministic is not the same as well-conditioned.

- Swapping ONE sheep for ONE goose moved our bank $82,953 -> $105,738 and the frozen opponent's
  $82,615 -> $119,462 on one seed. One sheep is ~8 wool units a season.
- In a 38-config sweep over 14 seeds, **seed 8 gave 37 of 37 configs a median +$24,368** and seed 20
  gave only 8 of 37 anything positive, median -$9,523.
  Those two seeds drove the entire table.

Any harness must therefore average many seeds, resample them, and never read one row.

After removing those two seeds, two configs survive with a consistent sign:

```
config                    mean w/o 8,20      sd    seeds up
STRAWBERRY->WHEAT x4          +$3,647     5,366     9/12
WHEAT->MELON x2               +$2,499     2,597    10/12
```

Melon up, strawberry down -- which is what the curves in section 2 predict, and what Kawashigi's own
four-quadrant games run (MELON 20 / STRAWBERRY 34 against our 12 / 41).
Neither is confirmed on win rate.

## 6. Geese are UNMEASURED, not dead

`HERD_GEESE` exists at `schedule_agent.py:3583` and is 0.
Its 2026-08-11/12 negative verdict predates the `SELLABLE` fix (`c99a8a5`, 2026-08-13) that first
allowed EGG to be sold at all, so that verdict measured birds whose product could not be sold.

Two defects in the knob, found today and unfixed:

- `HERD_GEESE >= 2` returns a herd of **13** where 0 and 1 return 14 -- the second conversion places
  its goose and loses the animal it replaced.
- It saturates at 2 geese; `HERD_GEESE = 4` is byte-identical to 3.

Eggs do now sell: one goose sold 51 eggs, and the egg book finished at **$95 with a 445-unit
deficit** -- nine more geese would not have filled it.

A pool run gave geese 0 at 89.1% win and geese 1 at 88.5%.
**That result is not evidence.**
Five of the six opponents were saturated at 100% in both arms, so the entire difference rested on 16
mirror games and amounted to half a game.
A discriminating test needs opponents we do not already beat every time.

## 7. The four-quadrant branch

Kawashigi's four-quadrant tape (`91907974`) extracted to `data/seed_scripts/kawashigi_q4/`.
Composed with our shipped tape at **d9**, the first day the two disagree, into
`data/seed_scripts/kawashigi_q4c/`.
Through d8 they are the same plan, so the opening cannot regress by construction.

```
land bought d6, d11, d12   -> quadrants unlock d7, d12, d13
herd COW 6 / SHEEP 12 = 18 -> against our COW 10 / SHEEP 4 = 14
202 tile-plantings, 12 hands
```

It runs: on seed 3 it buys the fourth quadrant on d13, builds COW 6 / SHEEP 12, and banks $148,406
against $133,221.

**Run on every seed it LOSES**: mean -$2,749, median -$5,286, 5/14 seeds up, wins 4/14 against
q3's 5/14.
That is the expected result for a branch that should fire on ~15% of games.

The unexpected finding is that `COW 6 / SHEEP 12` appeared on **only seeds 3 and 10 -- exactly the
two YARN_STORE seeds in that set**.
`WOOL_SHOP_SETS_THE_HERD` is already reading the yarn draw by itself.

Measured directly on the SHIPPED q3 arm, to pin down how much of the package already exists:

```
armed seed 17    COW 6, SHEEP 8    (14)
unarmed seed 5   COW 10, SHEEP 4   (14)
```

So the shipped agent already shifts sheep-ward on an armed seed, but only to **6/8**.
The q4 tape reaches **6/12** by buying four more animals.
What the tape adds is therefore the parcel, four extra sheep, and the plantings to fill the ground --
not the sheep-ward shift itself.

### Measured on the 15 armed seeds

```
mean +465   median +4,553   sd 11,220   8/15 seeds up
wins:  q3 10/15   q4 12/15
```

Against the same comparison run on an unselected seed set (-$2,749, 4/14 wins), the trigger is doing
its job: a $3,214 swing and the win column flips.
But on the armed set alone q4 is break-even on money -- $465 against a standard error of ~$2,900 --
and +2 wins on 15 games.
Not shippable.

Both arms ran routes live from d9.
That handicaps q4 harder, because it has 100 tiles and 18 animals against 75 and 14, and the solved
routes were built for the three-quadrant board.
A re-solve on the 100-tile board is outstanding and should move q4 only.

`kagg/search/solved_days.py` is backed up to `solved_days.py.q3_backup_2026-08-15` before any
in-place rewrite.

## Open

- q4 measured on the 15 armed seeds, with routes re-solved for 100 tiles.
- Whether the tape's MELON 20 / STRAWBERRY 34 mix survives the agent's own melon/strawberry
  adaptation, which currently overrides it.
- Geese against a field that discriminates.
- Live market prices in `router.BASE_PRICE`, which is a hardcoded table -- `grep market_price
  kagg/search/router.py` returns nothing, so the planner values melon at $250 on d20 while it trades
  at $96.

---

## 2026-08-09 — The market: mechanism, shipped status, and the open prescription

Folded in from docs/the_market_2026-08-09.md.
That file was itself a 2026-08-09 consolidation of six earlier write-ups
(`fable_market_technique`, `fable_market_selling`, `the_shed_destroys_the_harvest`,
`the_planner_prices_the_wrong_market`, `brief_market_selling`, `we_oversell_into_a_contested_book`,
`fable_plan`), all deleted at that time.
Every number below names the script or log that produced it.
**Env version matters here more than anywhere else in the project**: the ladder ran
`kaggle-environments` **1.32.6** from 2026-08-07/08 (the project is now on 1.32.7 -- see
`docs/balance_change_eggs_tomatoes_carrots_2026-08-15.md`, untouched, standalone).
Numbers explicitly marked 1.32.2 below are historical and kept only where the 1.32.6 column sits
next to them.

> **2026-08-11 addendum, as recorded in the source.** `docs/what_the_town_will_actually_eat.md`
> (folded in below, 2026-08-11 section) re-measures season absorption directly off 87 recorded
> ladder tapes' closing inventory, rather than off `MARKET_PARAMS`/`SHOPS` computed here.
> It confirms melon and fertilizer are always oversupplied and wheat's book never saturates.

### 1. The mechanism — selling is computable, not a judgement call

Three facts from `reference/kaggriculture.py`, together making the sell decision arithmetic:

1. `market_price(item, inventory, params)` is a **pure function** of inventory, monotone decreasing
   above `I0 = 10,000` (`:177-191`).
2. `_commit_unit` raises market inventory by exactly one per unit sold, and **"sales at $1 do not
   increase market supply"** (`:626-635`) — the floor is an infinite sink, so a crashed book is
   recoverable but its value is forfeited, not destroyed.
3. `_town_consume` lowers inventory by a deterministic amount depending only on the step and
   `town.unlocked_shops` (`:696-717`), and runs immediately after `_process_market` every step.

So, units sellable at price ≥ `L`, by both players, over the rest of the season:

```
N(L) = max(0, I_L - I_now) + D_rem
```

`I_L` is the inventory at which price is `L`; `D_rem` is the town's remaining drain. Both terms are
free — `market` and `town` are `shared: True` in the observation.

**The rule** (derived, no fitted constant):

```
λ_p = market_price(p, I_now + Q_rem - contest * D_rem)
offer n units now, largest n with market_price(p, I_now + n) >= max(λ_p, (1-slip)*market_price(p, I_now))
```

`λ_p` replaces `allow` (a day total transcribed off one 1.32.2 replay row — see the shed-eviction
section below).
`slip` replaces `rate[prod]` (a real fact: an oversized single offer walks its own size down the
curve inside one lockstep — see the sell-cap section below).
`contest` is the only free dial and it is game-theoretic, not fitted: `1.0` is the single-player
optimum, `0.5` the two-player split. Lower sells sooner. This formalises the core trap (see the
two-traps section below): denying the opponent revenue is worth as much as earning it, because the
contested resource is the *drain*, not the product.

### 2. Season absorption, both env versions

`scratchpad/absorb.py`, computed directly from `MARKET_PARAMS` and `SHOPS`. 1.32.6 halves the town
centre's cadence (`townCenterSellInterval` 12 → 24) and deletes its late-season demand ramp.

```
product        1.32.2    1.32.6     per-day, all 8 shops live
WHEAT             635       525            31
STRAWBERRY        536       426            25
CARROT            437       327            19
MILK              437       327            19
TOMATO            338       228            13
EGG               338       228            13
WOOL              338       228            13
MELON             140        30             1
FERTILIZER          0         0             0
```

**Melon is exact** — no shop carries it, so its only buyer is the town centre: 719 steps / 24 = 30
ticks at a flat multiplier of 1. The other rows depend on the shop-unlock draw and are indicative,
not exact (1.32.6 draws shops *with replacement*; the table above uses a 1.32.2 without-replacement
draw for the non-melon rows).

`kagg/search/chains.py`'s `DRAIN_UNITS` — the constant stage 1's `revenue_rate` prices production
against — still holds the 1.32.2 column. Against the ladder it overstates the market by **1.13x
(carrot) to 4.67x (melon)**, and the planner believes the market is worth $308,160 against a real
$207,180. Stage 1 does not currently ship in `submission/main.py` (grep the bundle: `DRAIN_UNITS 0`,
`OPPONENT_SHARE 0`, `revenue_rate 0`), so this overstatement has not cost a ladder game directly —
but it would be baked in on day one of wiring stage 1 back in. See `fable_stage1_review_2026-08-09.md`
for why stage 1 in its current form should not be revived as-is.

For per-head animal saturation and the corrected 1.32.6 "first local peak" table (which supersedes
the season-drain figures above for the *production-sizing* question), see
`what_saturates_and_what_does_not_2026-08-09.md`.

**Depth from a balanced book** — units sellable before price falls to a fraction of base (pure
function of `MARKET_PARAMS`, unaffected by the version change):

```
product      base   >=0.9*base   >=0.75   >=0.5    above_func
WHEAT          25          20    2421  ~inf     log
EGG            50          24    1422  ~inf     log
FERTILIZER    100          53     128   253     linear
MELON         250          51      80   113     sq
CARROT         35          10      55   230     sqrt
WOOL          200          19      30    42     sq
TOMATO         60           7      38   144     sqrt
MILK          160           8      20    39     linear
STRAWBERRY   120           7      16    32     linear
```

A price-neutral offer is 7 units of strawberry or 53 of fertilizer — a seven-fold spread that does
not track price level. `rate[prod]`, a single transcribed integer per product, cannot express this.

### 3. Why we stopped selling — the shed destroys the harvest

`schedule_agent.py:1947-2088` (pre-fix logic, mechanism unchanged):

```python
for d in sorted(sched):
    for p, q in (sched[d].get("sells") or {}).items():
        if d <= day:       rate[p] = max(rate[p], int(q))   # per-OFFER cap
        elif d <= horizon: still_owed[p] += int(q)          # rest of season
allow = max(today + carry, have - still_owed[prod])
n     = min(have, allow, rate[prod])
```

Both throttles were transcribed from the tape's own schedule row, keyed to *its* production, not
ours. We plant 77 tiles to its 45, so the surplus has no row anywhere to release it. Measured on the
handover fixture (seed 11, weeds off, tape plays d0-10, our agent from d11), pre-fix:

```
day    11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28
shed   14  33  35  35  45  86 100 100 100 100 100 100 100 100 100 100  90 100
lost    0   1   2   1   0  21  13  27  23  18  42  36  28  11  41   7  10  24
```

**331 units destroyed**, shed pinned at its 100 cap from day 17. The tape holds 18-36 all season
because it never stops selling.

### 4. `PRICE_AWARE_SELL_CAP` and `RESERVATION_SELL_CAP` — both are now ON, verified live in code

Both flags are read directly from `kagg/search/schedule_agent.py` as of this 2026-08-09
consolidation (`grep PRICE_AWARE_SELL_CAP\|RESERVATION_SELL_CAP`):

```
PRICE_AWARE_SELL_CAP  = True   (line 920)
RESERVATION_SELL_CAP  = True   (line 974)
```

This **superseded** both flags' original 2026-08-08 write-ups, which reported `PRICE_AWARE_SELL_CAP`
shipping OFF and `RESERVATION_SELL_CAP` "derived, tested, not yet measured wide enough to ship." The
measurements that justified turning them on, kept because they show the traps that nearly sank both:

**`PRICE_AWARE_SELL_CAP`** drops the day-total cap (`allow`) when the live price is at or above base;
`rate[prod]` — the per-offer cap — is untouched. A first version dropped *both* (`n = have`,
uncapped) and cost **~30% of mean money** against every arena opponent (seeds 500-505): a large
`have` right after a harvest lands walks its whole size down the price curve in one lockstep, instead
of spreading across turns the way `rate[prod]` always has (the same dump shape as wool going 123→138
units for $29,041→$21,811 in `LIQUIDATE_FROM_HOUR`'s own docstring). Corrected (only `allow` moves):

```
                  final     destroyed    turns at cap   (handover fixture, seed 11)
OFF             $71,976        331            12
ON              $75,866         82             2
                +$3,890        -75%
```

On the arena pool it read as neutral ($103,932 → $102,095, win 94.4% both ways) — **the pool is
saturated**: 94.4% with `mirror` at 50% means every non-mirror opponent already loses 100% of the
time either way, so mean money is the only channel left and it says nothing happened there. The
handover fixture, against an opponent that actually beats us, is the instrument that discriminated.

**`RESERVATION_SELL_CAP`** replaces the binary `price >= base` test with the per-product depth rule
from §1 above. It was nearly shipped as `max(rate[prod], reservation)` — reasoning that a rule which
can only *widen* an offer cannot regress — and was a **no-op**: five seeds came back byte-identical,
because `rate[prod]` was already the larger number every turn that mattered.
`tests/test_reservation_sell_cap.py::test_turning_the_flag_on_actually_changes_what_is_ordered`
exists so this cannot recur. The measurement that shipped it, from the flag's own current docstring
in `schedule_agent.py`:

```
              mean bank    units destroyed    land parcels
OFF             62,868        86 - 165        [4, 6, 15/16]
ON              64,667        39 - 107        [4, 6, 16]
```

+2.9% bank, a third off destroyed units, land a day later on some seeds — accepted because both
fixtures move the same way on money while waste falls on every seed, and because the arena pool
cannot discriminate any sell rule at all.

Fixture note that still applies: on the handover fixture (seed 11, weeds off), **six of nine
products run at a deficit for the entire season** — milk peaks at $315 against base $160, wheat at
$51 against $25, neither ever crosses `I0`. Glut protection is exercised only on melon, wool and
fertilizer there. "We sell 71 wheat where the field sells 525" on that fixture is a **production**
ceiling, not a policy one — see the "we oversell" section below for the real, contested-ladder
picture, which differs.

### 5. The current, most important finding as of 2026-08-09 — we oversell into a book the opponent is already filling

Across **14 real ladder losses** (`data/ladder/losses/`), holding the opponent exactly as they
played and re-pricing only our own sales **downward**, **12 of 14 become wins**
(`scripts/what_we_should_have_sold.py`, `data/logs/what_we_should_have_sold.log`). Gaps were tiny —
$715 to $4,266 — recoverable revenue $7k-$33k per game.

```
recoverable money, summed over 14 losses
  WOOL            +135,250
  STRAWBERRY       +57,433
  MILK             +57,163
  MELON             +4,447
  WHEAT                  0
  FERTILIZER             0
```

Consistent enough to be a rule:

```
WOOL         0.7x  best in 7 of 14 games (0.6-0.8 in 11)
MILK         0.5x  best in 4, 0.6-0.7 in 5
STRAWBERRY   0.7x  best in 6, 0.9x in 4
WHEAT        1.0x  -- no gain, ever
FERTILIZER   1.0x  -- no gain, ever
```

Wheat and fertilizer are the two products we sell most by volume, and they are correctly sized —
their books are deep enough that our volume alone does not move price. Everything recoverable is in
the three thin, steep books.

**It is genuinely LESS, not slower.** `scripts/less_or_slower.py` separates volume from cadence by
reconstructing the counterfactual book each schedule would have faced:

```
total gain over observed, summed across every game and product
  downscaled  (fewer units, same shape)   +254,293   best in 16 of 56 cases
  spread      (same units, even cadence)   +87,343   best in 16 of 56 cases
  both        (fewer units, even cadence) +252,611   best in 17 of 56 cases
```

Spreading alone recovers about a third of what cutting recovers; cutting-plus-spreading adds nothing
over cutting alone. Exception: **WOOL is a volume problem and severe** (episode 91122388: $5,278
observed vs **$23,794** at 0.7x, 4.5x the revenue from 70% of the units — `above_func: sq`,
`above_target: 3.2`, floor at 59 units above `I0`; the town removes only 204 wool a season against
our ~200 + opponent's 140-255 into the same book). MELON is a cadence problem (spreading wins it in
most games). MILK is both. STRAWBERRY is often already right.

**We can see their play without seeing their orders.** `market.inventory` is shared and visible
every turn, so their selling is visible as the book rising even though their intent (and shed) is
not:

```
opponent_net_trade(p, t) = delta_inventory(p) - our_sales(p) + drain(p, t)
```

This is the free measurement that turns `contest` (§1 above) from an assumed 0.5 into an actual
per-product number. `schedule_agent.py`'s reservation call site (`:2487`) still did not read it, as
of 2026-08-09 — the same missing quantity appears three times in this project (`OPPONENT_SHARE =
0.5` in `scheduler.py`, the `contest` dial in §1, and here) and had never been measured as of this
write-up.

**Real ladder confirmation**, 12 recent games:

```
product       base |  OURS-WIN units   $/u |  OURS-LOSS units   $/u |  ALL FOES units   $/u
MELON          250 |             984   150 |             247   111 |           1,050   153
WOOL           200 |           1,950   147 |             398   127 |             896   141
MILK           160 |           2,082   205 |             321    73 |           1,405   161
STRAWBERRY     120 |           2,711   182 |             562    78 |           1,366   154
WHEAT           25 |           9,115    45 |           1,693    49 |           7,124    48
```

Wins and losses share the same board — 97 tiles, same herd, same third-parcel day in every game but
one — and differ almost entirely in the price realised on milk and strawberry. Wheat is *better* in
the losses.

**On every lever that correlates with money we already match or beat the top quintile.**
124 seats, 62 games (`scripts/what_the_others_do.py`):

```
lever          corr w/ money   top 20%  bottom 20%  OURS mean  our percentile
sell_orders           +0.384       542         300        546             65%
feed                  +0.359       376         268        391             62%
harvest               +0.334       324         253        328             48%
care                  +0.327       385         268        406             63%
hires                 +0.301        12          11         12             14%
buy_product           +0.255      1156         750       1068             49%
herd                  +0.258        17          13         18             69%
tiles                 +0.149        92          80         99             42%
plant                 -0.050        95         105         85             24%

money: ours $73,977   field $68,091   top-20% $116,407
```

There is no missing activity. **The whole gap is price realised per unit.** The one lever with real
headroom is `buy_product` (49th percentile against a top-quintile 1,156) — OPEN-3's buy-wheat →
feed → milk conversion.

**The opening is not the problem.** Six seeds, weeds 0.005: our own planner driving from day 0 wins
0/6 (mean $47,756); the tape opening followed by our agent from day 11 wins 4/6 (mean $67,181). Keep
the tape opening.

#### Two corrections on the 2026-08-09 record

- The first pass of this analysis scaled sales **up to 1.5x** and reported wheat as the single
  biggest recoverable line (+$165,070) — nonsense, since selling up means selling goods we never
  held and nothing checked inventory. The sound version only scales down.
- Market orders in a replay are **offers, not fills** (one replay records a 21,216-unit MILK offer).
  The corrected method perturbs the *observed* path rather than reconstructing the opponent's
  quantities from their orders.

#### Addendum — the contested instrument, and what it said as of 2026-08-09

Every number above used `scripts/handover.py`, whose seat-1 opponent barely sells, so no book floors
and glut-protection numbers had nothing real to act on. `scripts/vs_tapes.py` — a real top player's
own play in seat 1 — was run partially:

```
tape        seed        ours        tape  result   margin
oldleader     11      48,827      57,809  LOSS     -8,982
oldleader    101      55,159      59,427  LOSS     -4,268
oldleader    202      67,241      75,419  LOSS     -8,178
oldleader    303      65,177      71,988  LOSS     -6,811
seb           11     116,500      18,017  WIN     +98,483
```

**We lose 4/4 to `oldleader` and beat `seb`'s own tape by $98k.** The schedule we ship is copied
from Seb, so beating his tape measures execution on a board we were built for; `oldleader` is a
genuinely different opponent and beats us every seed. This was the discriminating fixture proposed
to gate every future selling change — the arena pool (94.4% saturated) and the handover fixture
(10/10 wins) cannot.

### 6. Two traps already caught, twice (as of 2026-08-09)

1. **Money is not the objective; the ladder is Elo.** Seb's own 1.32.6 sell mix earned us more money
   on *every* seed and still lost **8/8** head-to-head, because ceding wool let the opponent earn
   more than we gained. Denying the opponent revenue is worth as much as earning it.
2. **A replayed tape does not react.** Absolute money against a tape runs 2-3x what real ladder
   games produce. Use a tape for per-day fidelity; use `vs_tapes.py` or a reacting arena pool for
   anything about strategy.

### 7. Prescriptions, in the order they were derived on 2026-08-09 (not all shipped as of that date)

1. **Sell fertilizer from day 0, hard.** Non-recovering book (`D_rem = 0`, price only falls,
   linear), and we are four days behind the tape into a book that never recovers: first 200 units
   worth $16,020 against the last 200's $8,020.
2. **Sell far more milk, at the corrected §5 rate (0.5x of what looked natural), spread not
   dumped.** The single largest recoverable line.
3. **Wool at ~0.7x volume — a volume fix, not a cadence one.** Melon is the cadence exception;
   spread it, do not cut it, since its drain (30/season) makes no volume level "right."
4. **Wire the opponent's inferred net trade (§5's `opponent_net_trade`) into the reservation call
   site** — the one free measurement none of the three places that needed it (`OPPONENT_SHARE`,
   `contest`, the sell block) read as of 2026-08-09.
5. **Gate every future selling change on `vs_tapes.py` against a reacting opponent (`oldleader`,
   not just `seb`), not the arena pool or the handover fixture** — both proven unable to
   discriminate a real change.
6. Shed-slot eviction by value density (wheat is the deepest book in the game and the one product
   that least needs shed room) was proposed but not built as of 2026-08-09; `SELL_TO_MAKE_ROOM` only
   reserved room for tonight's drop reactively and did not decide which product should hold the
   buffer.

### What this did not settle, as of 2026-08-09

- The opponent was held fixed in §5's counterfactual. A real one reacts, and cutting our supply
  raises their price, which may raise their volume — read §5 as an upper bound on the easy win.
- "Sell 0.7x" means the other 30% was grown and then wasted; the selling half is cheap, the
  production half (`revenue_rate` in `scheduler.py`) is a separate, unshipped fix.
- The duplicate implementation flagged on 2026-08-08 (`kagg/economics/market.py:reservation_price`
  vs `schedule_agent.reservation_units`) was resolved by omission: `market.py` no longer defines
  `reservation_price`/`units_to_sell` (checked 2026-08-09) and `tests/test_reservation_price.py`
  did not exist. `schedule_agent.reservation_units` was the sole implementation as of that date.

---

## 2026-08-09 — The book is shallow, and our production ignores it

Folded in from docs/the_book_is_shallow_2026-08-09.md.

> **CORRECTION recorded in the source, same day.** Every absorption figure in an earlier pass of
> this document was measured PASS-vs-PASS and described as "a property of the board with no agent
> involved." **That is wrong.** `_spawn_weeds` draws from the same per-day rng *before* the shop
> unlock (`reference/kaggriculture.py:856-878`), and weed spawning depends on which tiles are empty
> — so how the agents play shifts the stream and changes which shop is drawn. Measured:
>
> ```
> seed 13  PASS: YARN, BAKERY, PIZZA, YARN, ICE_CREAM, FARMERS, PIZZA, BRUNCH
>          REAL: SMOOTHIE, ICE_CREAM, YARN, ICE_CREAM, FARMERS, YARN, YARN, ICE_CREAM
> seed 29  PASS: PET_CAFE, FARMERS, BRUNCH, ICE_CREAM, BAKERY, BAKERY, BRUNCH, BRUNCH
>          REAL: BRUNCH, FARMERS, ICE_CREAM, YARN_STORE, PET_CAFE, PET_CAFE, BAKERY, BAKERY
> ```
>
> So seed 29 is NOT wool-starved under real play — it draws a YARN_STORE — and the "WOOL starved on
> 5 of 12 boards" claim described boards our agent never sees. The 34% figure for P(no YARN_STORE)
> is still correct, because it comes from the draw being uniform over 8 shops with replacement,
> which no gameplay changes.
>
> What survives untouched: the price-curve table (verified against `kg.market_price` itself by
> `tests/test_the_price_curve_math.py`), the realised-price and two-way results (measured under real
> play throughout), the shop-count table, and the fact that MELON is carried by no shop on any board.
>
> What needed redoing: absorption per board, computed from the shop timeline observed during real
> play rather than from a PASS game. It also means a seed cannot be catalogued by constellation —
> the mapping is agent-dependent, so a sweep must dictate `unlocked_shops` rather than search seeds.

This 2026-08-09 write-up superseded a "delivery problem" framing from earlier the same day.
That framing was wrong and the measurements behind it were wrong in two separate ways; both are
recorded here because the mistakes recur.

### The claim that started it, and why it was false

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

**There is no delivery problem, no discard problem and no shed-capacity problem**, per this
2026-08-09 measurement. (Shed capacity and harvest-discard questions were later revisited from the
production/routing side in `docs/fable_the_discard_problem_2026-08-09.md`, which belongs to the
crops/watering/harvest group, not here — see the note at the end of this file.)

#### Two measurement errors, both a snapshot standing in for a flow

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

### Where the money actually goes

The same seasons, read as revenue per unit:

| seed | MILK $/unit | WOOL $/unit | final bank |
| --- | --- | --- | --- |
| 13 | 252.66 | 229.23 | 163,036 |
| 17 | 111.51 | 236.51 | 126,151 |
| 29 | **27.90** | 219.29 | 77,254 |
| 41 | 197.71 | **39.65** | 100,464 |

Seed 29 sold *more* milk than seed 13 and banked **$6,054** for it against **$62,913**.
Same agent, same code, same schedule, same opponent tape.

#### The curve is far steeper than the melon case everyone has curved

`market_price` (`reference/kaggriculture.py:179`) is a pure function of the book's inventory
relative to `I0 = 10,000`:

```
price = base - (above_target * base / shape(above_func, T)) * shape(above_func, inventory - I0)
```

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
walked this curve — **for melon only**, which at 158 units is the *shallowest-sloped* of the
premium products. Wool floors at roughly a third of that, and a season produces 150-280 units of
each.

WHEAT's `log` shape is why it behaves nothing like the rest of the table and why volume there is
nearly free. That is a property of the price parameters, not of anything we do.

### Board versus opponent: both, and it splits by product

Two-way design, 6 tape opponents x 6 seeds, 36 seasons (`data/logs/price_two_way.log`).
A tape is open-loop, so an opponent emits the same order sequence whatever the seed, which makes
the opponent factor genuinely fixed down a column.

```
===== MILK $/unit =====                    ===== WOOL $/unit =====
opponent          13     17     29     41     53     67        13     17     29     41     53     67
HealthStone   238.74  69.85  26.64  75.06  88.20 216.17     85.77  21.20  21.44 237.29  59.94 114.78
Mohamed       254.98  98.55  33.21 200.38 232.10 217.47     38.62  45.63  55.55  38.63  31.23  35.46
Phi           255.15 114.49  36.12 203.77 246.75 217.89     38.62  40.83  34.78  63.17  33.23  35.46
Seb           252.66 111.51  27.90 197.71 247.49 258.22    229.23 236.51 219.29  39.65  62.94  62.60

mean spread ACROSS SEEDS, opponent fixed :  88.5 (milk)    49.0 (wool)
mean spread ACROSS OPPONENTS, seed fixed :  54.1 (milk)    73.1 (wool)
```

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

### What the seed controls, and what we can see

The seed touches exactly two things (`reference/kaggriculture.py:856-878`):

```
rng = random.Random((seed * 1_000_003) ^ day)
...  _spawn_weeds(farm, board_size, weed_chance, rng)           # weeds
...  town["unlocked_shops"].append(rng.choice(sorted(SHOPS)))    # which shops unlock
```

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

### The actual gap, as of 2026-08-09

The **sell** side already used all of this and was not the problem.
`town_drain_remaining` (`kagg/search/schedule_agent.py:1228`) mirrors `_town_consume` exactly,
`reservation_units` prices against the book's remaining absorption, and `PRICE_AWARE_SELL_CAP`,
`RESERVATION_SELL_CAP` and `HOLD_A_FLOORED_BOOK` all shipped ON.
The per-product depth numbers were derived there already.

The **production** side ignored the draw completely, as of 2026-08-09.
The schedule commits to cows, sheep and crops from a fixed target sheet decided before the board
is known, and nothing in that path consulted `town["unlocked_shops"]`.
On a board that never draws `YARN_STORE` we still buy sheep, and their wool is worth a fraction of
base however well it is later sold.
Shops unlock one every three days, so two or three are known by day 6-9, while most animal buying
is still ahead.

The community notebook reached the same place from replays rather than from the price table:

- cluster D, the adaptive leaders: "Dynamic cow/sheep/goose mix — **rebalances when milk is
  contested**";
- its own bug table: "Fixed 10 cows forever → mirror banks collapse toward ~40k → **fix: add
  sheep/strawberry/opponent routing**".

### Open as of 2026-08-09, and separate from the price question

**Animal loss.** Shipped loses 1 animal on seed 13, `1455` loses 4, the `1455m` graft 8-11.
`consecutive_unfed >= 2` deletes the animal outright (`reference/kaggriculture.py:786`), so it is
irreversible, and a final bank cannot show it — a late loss barely dents the total while
destroying an asset that pays out every remaining day.
This is not the same defect as the price collapse and must not be traded against it.

### Method note

Both wrong turns were a snapshot substituted for a flow, and both were caught by instrumenting the
one function that moves goods and money together.
`kagg/analysis/fills.py` documents three earlier versions of the same mistake.
Start there before building a fourth proxy.

---

## 2026-08-09 — Market shape: Seb vs us, measured on fills (task #49)

Folded in from docs/fable_market_shape_2026-08-09.md.
Branch `shaping-potential`, follow-on from `docs/fable_the_discard_problem_2026-08-09.md` earlier
the same day (that file belongs to the crops/watering/harvest group — see the note at the end of
this document). `kagg/search/schedule_agent.py` was the only file changed.

### Verdict, up front, as recorded 2026-08-09

- **LATE_SELL_BIAS is a real, substantial win.** Arena A/B, 8 held-out seeds × 3 opponents × both
  seatings (48 games/state): pool win rate **14.6% → 27.1% (+12.5pp, nearly double)**, mean money
  **$16,146 → $24,535 (+$8,389)**. Positive or flat on every individual opponent, never negative.
  This was the headline result of this task. See §4 below.
- **CAP_SELL_OFFER_SIZE's byte-identical A/B result is a genuine null, not a bug — checked, not
  assumed.** The coordinator flagged that an identical OFF/ON result usually means the flag never
  reached the code path (their own `still_owed` mistake earlier that day). Re-verified the flag
  directly through the exact arena wiring (`make_our_agent()` + `kaggle_environments`, no
  overrides): seed 2 vs `contrarian`, OFF emits `SELL WHEAT 43`, ON caps it to exactly 30, money
  $10,268 → $10,265. The flag works. It just never binds on the 8 seeds (20-27) the A/B used against
  any of the 3 pool opponents — confirmed directly, max offer stays ≤23 there. The premise
  ("standing offer vs few/small/late") also does not cleanly explain the money gap on fills: Seb's
  realised price is far above both us and the opponent who beat us in the sample loss ($141/unit vs
  $93/unit vs $86/unit), but the opponent's own single-product orders are BIGGER than Seb's (mean
  7.8, max 31, vs Seb's mean 4.0, max 16) — what separates the three is **product mix sold**, not
  order shape. See §2 and §3.1 below.
- **A separate, bigger question the coordinator raised: is the 14.6% baseline a regression, or a
  harder/different pool than the historical "94.4%"?** Traced the 94.4% figure to its source
  (`schedule_agent.py` ~line 873, quoted in full above under the 2026-08-09 mechanism section): it
  is explicitly flagged IN THE SOURCE, at the time it was recorded, as a **saturated, uninformative**
  number. That pool included `mirror` and, per this project's own repeated warnings, most likely
  `starter`. The 14.6% used only `heuristic`/`rancher`/`contrarian`, no mirror, no starter. **These
  are not the same measurement and the drop is not a valid before/after comparison.** Confirmed
  separately on one seed: our agent is not globally broken (plays normally against Seb's tape, ~$50k
  by day 28, matching the mechanism section's numbers); the "hands: 0" reading that looked alarming
  mid-check is by design (crew is dismissed nightly, hands rise to 7 within the first hour of every
  day). The live-pool weakness is real but its root cause is a separate, already-tracked
  project-level question (`docs/the_top_five_clusters_2026-08-09.md`: "we score 1,123.5, the field
  floor is ~3,117"), out of this task's scope. See §4.1 below.
- **Both candidates were implemented behind flags, default OFF, with RED-before-GREEN tests**
  (`tests/test_market_shape_candidates.py`, 9/9 passing). See §3-4 for the numbers and §5 for the
  recommendation.

### 1. Method: two shed-delta techniques, one much better than the other

**First attempt — reuse `scripts/breakdown.py`'s shed-delta method directly on the recorded JSON.**
`SELL`/`BUY_PRODUCT`/`BUY_ANIMAL` settle straight against `private["shed"]`, so a turn's shed delta
is the fill — PROVIDED no `DROP`/`PICKUP`/`PLACE` also fired that turn (they touch the same field
and taint the read). Applied directly to `data/seed_scripts/top_guys/90976060.json` (Seb) and
`data/ladder/losses/91229682.json` (our loss), this recovered order-count stats that matched the
task's own numbers exactly (244 SELL offers for Seb, 455 for us) — a good cross-check that the
method and the recorded data agree. But **coverage was terrible**: only 18 of Seb's 244 SELL offers
landed on a clean turn, so total captured revenue was $13,355 against a final bank of $128,518 — a
>90% undercount, useless for a realised-price comparison. Both players' crews DROP constantly as
part of normal routing, so most turns that also carry a market order are tainted.

**Second attempt, adopted — exact revenue via money conservation, not shed reconstruction.**
`reference/kaggriculture.py` shows money moves ONLY via `SELL`/`BUY_PRODUCT`/`BUY_ANIMAL`/
`BUY_SEED`/`HIRE`/`BUY_LAND` (`_commit_unit`, `_do_hire`, `_do_buy_land`) — never by any unit-phase
op (`DROP`/`PICKUP`/`PLACE`/`HARVEST`/...). Of those six, four are FIXED cost, computable exactly
from tables and counters already in the observation (`BUY_SEED`/`BUY_ANIMAL` are flat per-item
constants; `HIRE` is `mult * fib(hires_today)`, `hires_today` read straight off the farm; `BUY_LAND`
is `LAND_PRICES[len(unlocked_quadrants) - 1]`). Only `SELL` and `BUY_PRODUCT` depend on the live
market curve. So on any turn whose market list has **no `BUY_PRODUCT`**, that turn's money delta
minus the (exactly known) fixed costs of whatever else fired IS that turn's SELL revenue, exactly —
no shed reconstruction, no DROP taint, and `_commit_unit`'s SELL branch only ever fails on an empty
shed (never a capacity limit), so a covered turn's offered quantity is also its filled quantity.

Coverage: **81% for Seb, 41% for us, 76% for the opponent** (of turns that emitted ≥1 SELL order).
Sanity check: **zero negative-revenue events** across all three (a SELL-only, no-`BUY_PRODUCT` turn
can never legitimately lose money; a negative reading would mean the accounting was wrong, and an
earlier pass of this exact script produced exactly that — see the retraction in §1.1).

#### 1.1 A bug caught and fixed before trusting any number here

The first version of the money-delta script paired `steps[t]['action']` with the money change from
`steps[t]` to `steps[t+1]`, and produced physically impossible NEGATIVE "pure-SELL-turn" revenue —
e.g. `SELL WHEAT 1` alongside a **-$935** money change. `kaggle_environments`' own convention (used
correctly by `scripts/breakdown.py`'s `tape_policy`, which builds its replay list from
`d["steps"][1:]`) is that `steps[i]['action']` is the action chosen IN RESPONSE to
`steps[i]['observation']`, applied to produce `steps[i+1]` — so the action explaining a turn's money
move lives at `steps[t+1]`, not `steps[t]`. Fixed, re-run, zero negative events since. Recorded here
per this project's testing culture: a measurement that looks plausible enough to report is not the
same as one that has been checked against a physical invariant.

### 2. What actually differs, on fills

Money-delta method, `data/seed_scripts/top_guys/90976060.json` (Seb) and
`data/ladder/losses/91229682.json` (us seat 0 / opponent Shivam_2212 seat 1, the loss this task
names). All figures below are from **covered** (SELL, no `BUY_PRODUCT`) turns only; totals are a
sample, not the season total, at 41-81% coverage as noted.

```
                        events  covered qty   revenue    mean $/unit   single-order size (mean/max)
Seb (allegedly)            113          1064   $150,395      $141.35             4.0 / 16
us (the loss, seat 0)      130          1053    $98,072       $93.14             2.0 / 6
opponent (seat 1, won)      79          1209   $103,777       $85.84             7.8 / 31
```

By hour bucket (mean $/unit):

```
                h0-7      h8-15     h16-23
Seb            $149.17    $130.35    $138.68     -- flat-to-slightly-DOWN late, not up
us             $108.66     $60.62     $86.89     -- mid-day is the bad hour, not early
opponent        $76.65    $150.42     $95.68     -- no consistent pattern either
```

Per-product, single-product covered turns (the part of the sample with a clean per-item price):

```
Seb:        WOOL 55u@$38   FERTILIZER 52u@$73   STRAWBERRY 34u@$183   MELON 28u@$133
            WHEAT 21u@$36  MILK 6u@$276
us:         FERTILIZER 66u@$65   WHEAT 49u@$42   MELON 6u@$232   MILK 6u@$107
            STRAWBERRY 5u@$174   WOOL 3u@$181
opponent:   STRAWBERRY 190u@$161(!)   MILK 31u@$115   MELON 24u@$95
            FERTILIZER 20u@$86   WHEAT 7u@$40
```

#### 2.1 Reading it: this is a product-mix gap dressed as a price gap

Seb's realised price is 51% above us and 65% above the opponent who beat us — that part of the
premise holds. But the mechanism the task set out to test — small, late, deliberate orders command
a better price than a large, early, standing offer — **does not survive the opponent row**. The
opponent's own single-product orders are *bigger* than Seb's (mean 7.8 vs 4.0, max 31 vs 16, both
comfortably over "30" and over our 6), and the opponent still realises a materially LOWER average
price than Seb ($86 vs $141) and is not clearly ahead of us on price either ($86 vs our $93 — we are
nominally *higher*, on this sample).

What the per-product table shows instead: **we sold 115 of 135 single-product covered units (85%)
in WHEAT and FERTILIZER, both under $75/unit; the opponent sold 190 of 272 (70%) in STRAWBERRY at
$161/unit, and moved that volume without collapsing the price** (consistent with
`scripts/measure_sell_timing_impact.py`'s own earlier finding: seven of eight products are in a
"thick" market regime where a big offer barely moves the price — melon is the one thin exception).
Seb's mix is the most balanced of the three, with real STRAWBERRY, MELON and MILK volume alongside
wheat/fertilizer/wool. The opponent's win in this game reads as **produce more of the expensive
thing and sell it in bulk into a market that can absorb it**, not as **place smaller, later
orders**.

This does not mean order shape is worthless — a 51-65% price gap against Seb specifically is real
and worth keeping on the table — but it means **the loss to Shivam_2212 specifically is not
explained by sell shape on this evidence**, and a fix aimed at shape should not be expected to
close a gap that is actually about what got planted and harvested.

**Caveat with teeth:** one loss game, one Seb tape, 41-81% coverage. This is a real, exact-on-its-
subset measurement, not a full-season census. A different loss, or the full uncovered 19-59% of
sell-turns, could tell a different story. Treat §2.1 as the strongest reading of the evidence
gathered, not a closed case.

### 3. The candidates: implemented, RED-before-GREEN, both OFF by default (2026-08-09)

`kagg/search/schedule_agent.py`, new flags near `RESERVATION_SLIP` (~line 997):

```python
CAP_SELL_OFFER_SIZE = False
SELL_OFFER_CAP = 30

LATE_SELL_BIAS = False
LATE_SELL_FROM_HOUR = 16
```

Enforcement sits right after the `LIQUIDATE_LAST_DAY` override in the per-product sell loop
(~line 2720), so neither candidate can touch the last-day liquidation window every other cap in that
loop already exempts:

```python
last_day_liquidating = LIQUIDATE_LAST_DAY and day >= last_day and hour >= LIQUIDATE_FROM_HOUR
if CAP_SELL_OFFER_SIZE and not last_day_liquidating:
    n = min(n, SELL_OFFER_CAP)
if LATE_SELL_BIAS and hour < LATE_SELL_FROM_HOUR and not last_day_liquidating:
    n = 0
```

Tests: `tests/test_market_shape_candidates.py`, 9/9 passing
(`data/logs/market_shape_final_2026-08-09.log`). Existing suite checked for regressions:
`tests/test_router.py` was unchanged at 8 failed / 62 passed / 6 skipped, the same pre-existing
failures left by the day-gating fix earlier that day (`docs/fable_the_discard_problem_2026-08-09.md`
§2 — crops/harvest group, see note at end of this file), confirmed via the byte-identical-when-off
rail (`test_both_flags_off_is_byte_identical_to_the_shipped_agent`) rather than assumed.

#### 3.1 CAP_SELL_OFFER_SIZE

RED scenario, found by measurement rather than assumed: a solo replay against a dummy opponent never
produces an over-30 offer on any seed tried. A **24 seed×opponent sweep** (`heuristic`, `rancher`,
`contrarian`; 8 seeds each; `data/logs/market_shape_offer_sweep_2026-08-09.log`) found exactly two
over-30 offers, both `SELL WHEAT 43` on day 29 hour 0, both against `contrarian` (seeds 2 and 6).
Against `heuristic`/`rancher` the ceiling never even reaches 25. So the flag is real but the surface
it acts on is narrow: most of the historical "78-unit offer" gap already closed on its own once
`RESERVATION_SELL_CAP` / `PRICE_AWARE_SELL_CAP` / `HOLD_A_FLOORED_BOOK` shipped.

RED (`CAP_SELL_OFFER_SIZE=False`, seed 2 vs `contrarian`): `SELL WHEAT 43` on day 29.
GREEN (`CAP_SELL_OFFER_SIZE=True`, same seed/opponent): capped to exactly 30, no offer over the cap
anywhere in the season. `tests/test_market_shape_candidates.py::test_the_cap_reproduces_and_then_
fixes_an_over_thirty_offer`.

**Post-sweep re-check, prompted by the coordinator.** The arena A/B in §4 came back byte-identical
between OFF and ON on all three pool opponents across seeds 20-27 — exactly the signature of a flag
that never reaches the code path. Checked rather than trusted: ran the EXACT arena wiring
(`make_our_agent()`'s seat-agnostic wrapper, `kaggle_environments.make("kaggriculture",
configuration={"seed": 2})` with no overrides, matching `kagg.arena.run_arena`'s own config) on the
one seed/opponent pair already known to trigger the cap. Result: `CAP_SELL_OFFER_SIZE=False` → max
SELL offer 43, final money $10,268; `CAP_SELL_OFFER_SIZE=True` → max SELL offer exactly 30, final
money $10,265. The flag reaches the code path and does what it says. Then re-swept seeds 20-27
against `contrarian` specifically (the only opponent that ever triggered it) with the flag off: max
offer across all 8 held-out seeds is 23 — never above the cap. **The byte-identical A/B result is a
genuine null: the held-out seeds simply never exercise this candidate, on any of the 3 pool
opponents.** It is not evidence the cap is harmless or useless, only that this A/B has no
statistical power to say either way. A wider seed sweep specifically against `contrarian` (where
the trigger lives) would be needed to get a real answer; not run given the time already spent and
LATE_SELL_BIAS's much larger, unambiguous signal in §4.

#### 3.2 LATE_SELL_BIAS

This one is unambiguously wired and unambiguously live: `test_without_the_bias_orders_fire_before_
hour_sixteen` shows early offers firing under default settings on every seed tried, and `test_late_
sell_bias_actually_suppresses_early_offers` shows the flag removing every one of them (last-day
liquidation excepted). Unlike the cap, this candidate is not narrow — it changes roughly two-thirds
of the day's selling window (hours 0-15 of 24) to zero SELL orders, every day, all season.

The code's own prior evidence should be read as a warning before trusting this without a number:
`SELLS_FUND_THE_TURN` is a load-bearing mechanism that funds same-turn `BUY_LAND`/`BUY_SEED`/
`BUY_ANIMAL` from that turn's SELL proceeds, and the file's own day-6 example
(schedule_agent.py ~line 2820) shows Seb buying `BUY_ANIMAL COW 2` and `BUY_SEED MELON 6` on a bank
of $15, funded by a same-turn `SELL WOOL 6` at hour 2 — inside the window this flag would zero out.
Blocking all selling before hour 16 is a strictly blunter instrument than that funding mechanism
needs; it was implemented and tested as literally specified ("biasing sells toward h16-23") rather
than pre-softened, on the view that the A/B should say whether it costs money, not have the answer
assumed into the design.

### 4. Does it cost win rate — the A/B (2026-08-09)

`kagg.arena.run_arena`, workers=1 (closures from `make_agent` are not picklable across
`ProcessPoolExecutor`'s macOS spawn — the same constraint `scripts/arena_gate.py` documents).
Opponent pool: `heuristic`, `rancher`, `contrarian` (the diverse-crop-mix, same-play-style pool
`CLAUDE.md` describes). 8 seeds (20-27), both seatings via `run_arena`'s built-in swap = 16 games per
opponent per state. Seeds held out from the seeds used to find/verify the candidates (2, 11).
Selection criterion is **win rate**, per `CLAUDE.md` — the ladder is Elo, and money is a dense
training signal, not the verdict.

Full log: `data/logs/market_shape_arena_ab_2026-08-09.log`.

```
CAP_SELL_OFFER_SIZE                    win rate    mean money      opponent breakdown (money, win%)
  OFF                                    14.6%       $16,146        heuristic 8,672/12.5%  rancher 21,450/6.2%  contrarian 18,317/25.0%
  ON                                     14.6%       $16,146        heuristic 8,672/12.5%  rancher 21,450/6.2%  contrarian 18,317/25.0%
  delta                                  +0.0pp           +0        byte-identical on every opponent -- see §3.1, verified a real null

LATE_SELL_BIAS                         win rate    mean money      opponent breakdown (money, win%)
  OFF                                    14.6%       $16,146        heuristic 8,672/12.5%   rancher 21,450/6.2%   contrarian 18,317/25.0%
  ON                                     27.1%       $24,535        heuristic 23,196/25.0%  rancher 28,612/31.2%  contrarian 21,798/25.0%
  delta                                 +12.5pp      +$8,389        UP or flat on every single opponent, never down
```

**Verdict as recorded 2026-08-09: LATE_SELL_BIAS is a real, substantial, consistent win on this
evidence.** Pool win rate nearly doubles (14.6% → 27.1%), mean money rises 52% ($16,146 → $24,535),
and the effect is positive-or-flat on all three opponents individually — `rancher` alone goes from a
near-shutout (6.2%) to a real contest (31.2%). This was a much larger and cleaner signal than
anything else measured in this task, including the price-per-unit gap in §2 that motivated the whole
investigation. The mechanism this task set out to test — the design note's own claim that
`SELLS_FUND_THE_TURN` makes blocking early selling dangerous — did not materialise as a downside in
this A/B: money went up, not down, on every opponent. That does not mean the risk is zero (48 games
is not proof against a rare, expensive failure mode), only that it did not show up here.

#### 4.1 The 94.4% vs 14.6% question

Traced per the coordinator's instruction, on one seed (20), before writing anything else:

- **Not the same measurement.** The 94.4% figure (`schedule_agent.py` PRICE_AWARE_SELL_CAP
  docstring, ~line 873) is explicitly flagged in the source, AT THE TIME it was recorded, as
  uninformative. Whatever pool produced that number included `mirror` (which can only ever read
  50%) and, going by every other reference to "the arena pool" in this project, most likely
  `starter` — which `CLAUDE.md` names by itself as inflating results ~2x because it barely sells.
  The 14.6% used `heuristic`/`rancher`/`contrarian` only: no mirror, no starter, no seed overlap
  (theirs was 500-505, this run's was 20-27). A saturated-pool number from a different era compared
  to a deliberately harder, unsaturated one is not a before/after pair.
- **Our agent is not globally broken.** Re-ran `scripts/breakdown.py --tape seb1326 --seed 11 --days
  29` (the exact fixture used all morning): money $49,942 by day 28 against the tape's $75,556 —
  the same shape of gap already documented, not a collapse. Whatever is happening against the live
  pool is not "the agent stopped working."
- **A red herring, resolved rather than reported.** A first diagnostic pass showed "hands: 0" at the
  start of every single day against `heuristic`, seed 20 — alarming at a glance, as if hiring were
  silently broken. Traced turn-by-turn: hands go 0 → 5 → 6 → 7 within the first three hours of every
  day. `schedule_agent.py`'s own comment says why: *"hands are dismissed nightly, so every claim is
  stale."* Dawn is the one instant hands are legitimately always 0; not a bug.
- **What was real and in scope on 2026-08-09:** the pool win rate against
  `heuristic`/`rancher`/`contrarian` really was low (14.6%), and §4's result shows sell TIMING is a
  real, substantial part of why — closing nearly half the gap to a coin flip with one flag. What was
  real and OUT of scope: why the remaining gap existed. `docs/the_top_five_clusters_2026-08-09.md`
  already tracked a large, independent competitiveness gap under 1.32.6, consistent with what was
  measured here but a project-level question, not a market-shape one.

### 5. Recommendation, as of 2026-08-09

1. **LATE_SELL_BIAS is the strongest result in this task and should go to a wider confirmatory
   sweep before flipping the default.** 8 seeds is a real signal (consistent direction on 3/3
   opponents, effect size far larger than the ~15% seed variance) but not yet the "twelve seeds" bar
   this project has used elsewhere before shipping a sell-rule change. Next step: the same A/B on a
   second, disjoint seed block, plus `homestead`/`shepherd` added to the opponent pool, before
   considering `LATE_SELL_BIAS = True` by default.
2. **Do not ship CAP_SELL_OFFER_SIZE on the strength of anything measured here.** Its A/B is a
   genuine null on the seeds tried — real, checked, not a bug — but a null from an under-powered
   test is not evidence of "no effect," only "not measured." If it is picked up again, test it
   specifically against `contrarian` (the only opponent shown to trigger it) on a wider seed range.
3. **Do not chase the 94.4%-vs-14.6% framing as a regression.** It is not a valid comparison. The
   live-pool weakness it pointed at is real, tracked elsewhere, and only partially explained by what
   this task covers.
4. **The product-mix finding in §2.1 is worth a follow-up task of its own**, separate from sell
   shape: on the one loss traced, the opponent who beat us won by producing and selling far more
   STRAWBERRY (190 units at $161/unit) than we did (5 units), not by a different order shape. If that
   generalises, it points at what gets planted, not how it gets sold.

### 6. What was in the tree as of 2026-08-09

- `kagg/search/schedule_agent.py`: `CAP_SELL_OFFER_SIZE` / `SELL_OFFER_CAP` and `LATE_SELL_BIAS` /
  `LATE_SELL_FROM_HOUR`, both flags OFF by default, plus the two-line enforcement in the per-product
  sell loop. No default behaviour changed with both flags off (pinned by
  `test_both_flags_off_is_byte_identical_to_the_shipped_agent`).
- `tests/test_market_shape_candidates.py`: new, 9 tests, RED-before-GREEN for both candidates plus
  the wiring and no-op rails this codebase's other sell-cap tests use as their pattern
  (`tests/test_reservation_sell_cap.py`).
- Scratch analysis scripts (`fills_analysis.py`, `fills_money_delta.py`, `fills_exact.py`,
  `arena_ab_market_shape.py`) lived in the session scratchpad, not the repo, matching this project's
  convention for one-off probes.
- Logs: `data/logs/market_shape_red_2026-08-09.log`, `data/logs/market_shape_green_2026-08-09.log`,
  `data/logs/market_shape_final_2026-08-09.log`, `data/logs/market_shape_offer_sweep_2026-08-09.log`,
  `data/logs/market_shape_arena_ab_2026-08-09.log`.
- Not touched: `kagg/sim/`, `tests/test_sim_*.py`, `tests/test_tape_parity.py`, per instruction.

---

## 2026-08-10 — The market cadence, over all products

Folded in from docs/the_market_cadence_over_all_products_2026-08-10.md.

> **TARGET SUPERSEDED, addendum recorded 2026-08-11 in the source.** Measured against Seb's tape
> (`91422988`), optimal under the OLD `townCenterSellInterval=12` economy. His median bank halved
> and he has since withdrawn from the ladder (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder
> seats). The hour-cadence mismatch found below is still real — the target it is measured against
> is now known to be suboptimal.

Measured 2026-08-10, seed 11, tape `91422988`, crew planner on d0-d6.
Ours is **exact fills** diffed out of `record_fills` after every step — what committed, not what was
offered.
His is the `orders` field of the derived schedule, `[hour, op, item, qty]`, read straight off his
replay.
Raw log: `data/logs/cadence_all.log`.

Both sides trade roughly the right quantities.
The hours are wrong, and they are wrong in the same direction on every product.

### The table

```
--- day 0 ---
  BUY_PRODUCT  WHEAT   ours h01x1 h02x1 h03x1 h04x1 h05x1 h06x1 h07x1 h08x1
                       seb  h05x1 h07x1 h09x1 h11x1 h12x1 h14x1 h17x1 h19x1

--- day 1 ---
  BUY_PRODUCT  WHEAT   ours h00x1 h01x1 h02x1 h06x1 h07x1 h08x1
                       seb  h01x1 h04x2 h06x1 h07x1 h12x1
  SELL         FERT    ours h06x1 h08x1 h09x1 h10x1        seb h04x2 h10x1 h12x1

--- day 2 ---
  BUY_PRODUCT  WHEAT   ours h00x1 h01x1 h02x1 h03x1 h04x1  seb h02x1 h04x1 h06x1 h08x2
  SELL         FERT    ours h07x1 h08x1 h12x1 h13x2        seb h15x3 h19x2

--- day 3 ---
  BUY_PRODUCT  WHEAT   ours h00x1 h01x1 h02x1 h03x1 h04x1 h05x1 h07x1
                       seb  h01x1 h03x1 h05x1 h06x1 h07x1 h08x1 h15x1
  SELL         FERT    ours h07x1 h12x1 h13x2 h14x1        seb h15x4 h18x1

--- day 4 ---
  BUY_PRODUCT  WHEAT   ours h00x1 h22x4                    seb h02x1
  SELL         FERT    ours h16x3 h18x3                    seb h21x5 h23x1
  SELL         WHEAT   ours h16x25 h21x8 h23x1             seb h18x5 h21x12 h22x12 h23x20

--- day 5 ---
  BUY_PRODUCT  WHEAT   ours h13x1 h18x4                    seb h17x2 h21x1
  SELL         FERT    ours h04x2 h13x2 h14x1 h18x2        seb h17x1 h19x3 h20x3
  SELL         WHEAT   ours h00x7                          seb  (none)

--- day 6 ---
  BUY_PRODUCT  WHEAT   ours h08x1 h12x1 h14x1 h16x1 h17x1 h18x3 h19x1
                       seb  h09x4 h11x1 h13x1 h15x1 h19x1
  SELL         FERT    ours h07x1 h12x1 h13x2 h19x1 h20x2  seb h09x2 h13x2 h14x2 h16x1
  SELL         WHEAT   ours h00x2 h07x1                    seb  (none)
  SELL         WOOL    ours h07x1 h19x5                    seb h09x6 h13x6

--- day 7 ---
  BUY_PRODUCT  WHEAT   ours h01x1 h02x1 h03x1 h18x5        seb h17x2 h22x1
  SELL         FERT    ours h05x1 h19x2                    seb h17x1 h22x3 h23x3
  SELL         WHEAT   ours h00x5                          seb  (none)
```

### Three defects, all general, none product-specific

#### 1. The carry dumps at hour 0

`SELL WHEAT h00x7` on d5, `h00x2` on d6, `h00x5` on d7 — fourteen units at dawn across three days,
against a schedule that asks for **no wheat sale at all** on any of them.

It is `CUMULATIVE_SELLS` recovering d4's unfilled row.
d4 asks for 49 and we fill 34, so 15 carry forward and go out on the next three dawns.

Hour 0 is the worst hour available for it, for three separate reasons at once:

- the day's harvest has not happened, so the only stock is the herd's feed;
- the town has not drained the book, so the price is at its lowest;
- it is the same hour our own `BUY_PRODUCT WHEAT` fires, so we pay the spread on both legs.

The reserve fix in `b52e210` stops this on d4, where the row places an animal.
It does not stop it on d5-d7, because the carry is a different code path from the row.

#### 2. Sells fire in the morning; his fire in the evening

FERTILIZER is the clearest, because both sides trade it every day:

```
       ours                          seb
  d2   h07 h08 h12 h13               h15 h19
  d3   h07 h12 h13 h14               h15 h18
  d5   h04 h13 h14 h18               h17 h19 h20
  d7   h05 h19                       h17 h22 h23
```

`townCenterSellInterval = 24` on this economy: the town drains the book once a day.
Selling into an undrained book is selling into the bottom of the price curve.
He sells after the drain, we sell before it.

#### 3. Buys are front-loaded into a block; his drip

d0 is the extreme case — identical quantity, opposite distribution:

```
  ours  h01 h02 h03 h04 h05 h06 h07 h08     eight consecutive turns
  seb   h05 h07 h09 h11 h12 h14 h17 h19     spread across fifteen
```

`BUY_DRIP` exists for this and meters one unit per turn, but it starts at h00 and runs out by h08.
The shops restock every 4 steps, so his spacing buys each unit into a restocked book and ours
buys the second half into a book its own first half has already lifted.

### What it costs, where it has been priced

- **The d6 land parcel.** He sells `WOOL 6` at h09 and `WOOL 6` at h13, taking his bank
  $5 → $1,349, and buys the parcel at h13.
  We sell `WOOL 1` at h07 and `WOOL 5` at h19, hold $47 at h13, and do not reach $1,400 until h23.
  Same twelve units, ten hours late, and `buy_land 0/1` on d6 follows from it.
  This is why the crew planner reads as costing the parcel; it does not.
- **d4's wheat.** `h16x25` in one order against his `h18x5 h21x12 h22x12 h23x20`.
  `market_price` falls per unit *inside* a single order, so a 25-lump clears at a materially worse
  mean than four blocks across four turns with restocks between them.

### What has NOT been measured (as of 2026-08-10)

Whether moving our sells later is worth it in money.
Every number above is a timing observation.
The obvious experiment — a `SELL_AFTER_HOUR` floor, and denying the carry hour 0 — was unrun as of
this write-up.
Note that `docs/` already records two occasions where a cadence change that looked obviously right
measured as a loss, so this gets a grid before it gets an opinion.

(`LATE_SELL_BIAS`, folded in above under the 2026-08-09 fable-market-shape section, is exactly that
experiment for the second defect — "sells fire in the morning" — measured one day earlier and shown
as a real win on the seeds tried there. The two documents were written independently on adjacent
days and agree on the direction of the fix.)

---

## 2026-08-11 — What the town will actually eat

Folded in from docs/what_the_town_will_actually_eat.md.

Measured 2026-08-11 off the 87 recorded ladder games in `data/seed_scripts/top_guys`, by reading
each game's closing `market.inventory` against its own `town.unlocked_shops`.
No simulation and no agent is involved: the book and the shop list are both `shared: True` in the
observation, so these are facts the game hands us.

Two numbers per product.
**Appetite** is what the town removes over a season, from `_town_consume`: every
`townShopSellInterval` (4) steps each shop instance takes one of each product it sells, doubled if
it sells only one, and every `townCenterSellInterval` (24) steps the town centre takes one of
everything except fertilizer.
Over 719 steps that is 179 shop ticks and 29 centre ticks.
**Surplus** is `closing inventory - 10000`: units that were sold and never eaten, which is what a
floored price is made of.

### The shop table

| product | shop types carrying it (of 8) | season appetite | closing surplus, 87 tapes |
|---|---|---|---|
| WHEAT | 5 | 745 – 1,282 | **−386 to −1,356** |
| CARROT | 2 (PET_CAFE single-product, counts double) | 29 – 924 | −12 to −1,002 |
| TOMATO | 2 | 208 – 924 | −30 to −678 |
| STRAWBERRY | 4 | 387 – 1,282 | −381 to +60 |
| MILK | 3 | 566 – 1,103 | −342 to +77 |
| EGG | 2 | 208 – 566 | −624 to +108 |
| WOOL | 1 (YARN_STORE, single-product, counts double) | 29 – 387 | −424 to +59 |
| MELON | **0** | **29 on every board** | **+38 to +158, always positive** |
| FERTILIZER | **0** | **0 on every board** | **+201 to +493, always positive** |

### Fertilizer pays well and then stops paying, permanently

`reference/kaggriculture.py:101` builds the town centre's list as `[p for p in PRODUCTS if p !=
"FERTILIZER"]`, and no shop lists it either.
So fertilizer demand is zero on every board there is — this is not a property of one town seed, it
is a property of the rules.

The price curve is `linear` with `above_target 0.40` and `T = 200`, so every unit sold knocks about
$0.40 off and nothing ever puts it back.
Every other product's book gets drained back down; fertilizer's only ratchets one way.

| units sold | marginal unit | cumulative | average |
|---|---|---|---|
| 50 | $90 | $4,755 | $95 |
| 100 | $80 | $9,010 | $90 |
| 150 | $70 | $12,765 | $85 |
| 200 | $60 | $16,020 | $80 |
| 250 | $50 | $18,775 | $75 |
| 400 | $20 | $24,040 | $60 |
| 500 | $1 | $25,052 | $50 |

So the first hundred units are excellent — $9,010, better per unit than anything else on the board —
and units 250 to 500 fetch $6,277 between them, less than the first seventy earned.

**Every one of the 87 tapes closes with fertilizer between $1 and $20**, against a base of $100.
The book is saturated at the end of every game that has ever been played here.
Both farms sell into it, so the question is never "is fertilizer worth selling" but "did we get
there before the other farm did".

### Melon is the same shape, and we plant 17 tiles of it

No shop carries melon, so the town centre's 29 units a season is the entire market, on every board.
17 tiles at a measured 12 units a tile is 204 units into an appetite of 29, and the melon price is
`sq` with `above_target 3.60` — it reaches $1 about 190 units above I0.

All 87 tapes close with a melon surplus, +38 to +158, so **every player over-plants melon**, the
winners included.
That makes it a shared inefficiency rather than a losing move, and therefore an edge available to
whoever fixes it first.
It is also **not a decision the shop draw can inform**, which is why `SHOP_ADAPT_CROPS` deliberately
leaves melon out of every swap pair: how much melon to plant is a fixed-quantity question and a
separate one.

### Wheat is the scarcest thing on the board

Wheat's closing surplus is negative in all 87 tapes, by 386 to 1,356 units — the town eats far more
than both farms together produce, so the price *rises*, closing at $40–$59 against a base of $25.
It is carried by five of the eight shop types, more than anything else.

That is worth holding next to the shipped comment in `schedule_agent.py` that calls growing
wheat "a bad trade" on the grounds that a tile yields six units.
The measured figure in `kagg/economics/production.py` is 28, or 42 fertilized.

### What this does not say

Appetite is a ceiling on what the town removes, not a prediction of what we will sell.
Both farms sell into one book, and none of this models turns, walking, watering, or the fact that a
tile has to be reached before it can be harvested.
These rank products; they do not price a season.

---

## 2026-08-13 — How deep each market is, and why two losses happened

Folded in from docs/market_depth_and_the_morning_losses_2026-08-13.md.

Both losses are near-mirrors decided in the last third of the season, and both point at the same
thing: **we ship volume into products the town does not drain, and under-ship the one it does.**

### The depth table (computed from `reference/kaggriculture.py`, not from play)

`market_price` depends on **market inventory only**. Shops move the price solely by draining that
inventory, so exactly two numbers matter per product: how much the town absorbs over a season
(= the sustainable sell rate) and how much net excess takes the price to $1.

```
product      base  shops   drain     p@50    p@100    p@200     to $1
------------------------------------------------------------------------
WHEAT          25      5     525       22       21       21     never
CARROT         35      2     327       27       23       19       842
TOMATO         60      2     228       42       35       24       529
STRAWBERRY    120      4     426       24        1        1        62
MELON         250      0      30      225      150        1       158
EGG            50      2     228       43       42       41     never
MILK          160      3     327       55        1        1        76
WOOL          200      1     228       55        1        1        59
FERTILIZER    100      0       0       90       80       60       493
```

`drain` is the expected season total: instance N unlocks on day 3N so it is live for `180 - 18N`
four-step ticks (792 tick-instances over eight draws), shops are drawn **with replacement** from the
eight names, and a single-product shop consumes double (`_town_consume`).
`p@N` is the price after N units of net excess sit in the book.

Read off it:

- **WHEAT and EGG never floor.** Both decay as `log`, so the price is essentially flat: 200 wheat
  still fetches $21 of a $25 base, and 200 eggs $41 of $50. These are the two bottomless markets.
- **WOOL, MILK and STRAWBERRY are shallow to the point of fragility** — 59, 76 and 62 units of
  excess and they are at $1. Wool and milk are also the two highest-value products, so they are
  simultaneously the best and the easiest to destroy.
- **MELON has no shop at all.** Its only buyer is the town centre, 1 unit per 24 steps, 30 a season.
  A $250 base with a 30-unit season of real demand.

**The EGG line matters for the goose axis.** Egg is one of the two products that cannot be flooded,
and it was unsellable until `c99a8a5` — so every previous goose measurement was taken with the
revenue line disconnected. That was, as of 2026-08-13, in the running sweep as a live axis. (See the
2026-08-13 "late season" section below for what a direct re-measurement of geese with the fix live
then found: zero eggs sold.)

### `92550780` — lost $69,881 to $77,275 (-$7,394)

The town drew `YARN_STORE` **three times** and `PET_CAFE` twice, so it wanted **1,074 wool** and
**716 carrot** over the season.

```
WOOL   closed $252  of base $200   drained 1,074   <-- ABOVE base all season
CARROT closed $ 42  of base $ 35   drained   716   <-- ABOVE base all season
MILK   closed $  5  of base $160   drained   358
STRAW  closed $  3  of base $120   drained   179
MELON  closed $ 25  of base $250   drained     0
```

Wool closing **above** its base means total supply never caught the drain: every additional wool
unit that season was worth about $250 and there was room for it. We had **8 sheep to Densike's 4**
and shipped a fraction of the wool they did — on the slice of turns where attribution is
unambiguous, 28 units / $6,738 against 115 units / $28,158.

At the same time we put milk and strawberry on the floor, in a game where the town drained only 358
and 179 of them.

### `92562037` — lost $129,161 to $133,724 (-$4,563)

A true mirror: both sides ~148 wheat, both ~13 animals, near-identical sell cadence.
The one large divergence is **melon — we planted 136 to their 19**, into the product with zero
shops. It closed at **$25 of a $250 base**.

(This melon-plant figure was corrected below, in the same source document, after `why_we_lost.py`
was found to be printing BUY_SEED order quantities rather than real plants — see the correction in
the "five games" table further down.)

### Both losses are lost after day 18

```
92550780   d18 -$84       d21 -$10,532     d29 -$7,394
92562037   d18 +$6,363    d21 -$1,155      d29 -$4,563   (their last day +$10,469 to our +$4,080)
```

The opening is not the problem in either game. The late season is.
The first `SELL CARROT` is step **598** and **617** — day 25 — in games where the town was draining
carrot from day 3.

### Attribution caveat

Per-seat units are computed from the shared market ledger,
`inv(t) - inv(t-1) = sold_us + sold_them - bought - town_drain`, which is exact only on turns where
one side alone trades that product. Most volume lands in a `shared` bucket (1,260 and 1,803 units)
and is **not** split by a guess. The wool ratio above is the unambiguous slice, not the season total.

### The melon/strawberry answer is CONDITIONAL, and the running sweep cannot find it

Strawberry floors after **62 units** of excess, and its drain swings from 179 to 895 units a season
purely on how many strawberry-carrying shops the town draws.
That makes the melon/strawberry split a *conditional* answer, not a constant one:

```
92562037   5 instances carry STRAWBERRY   drained 895   closed $187 (above base)
           -> a melon tile converted to strawberry was worth several times more
92550780   1 instance  carries STRAWBERRY  drained 179   closed $  3 (floored)
           -> the swap buys nothing; that town wanted WOOL and CARROT
```

The stake is 19 melon tiles against 36 strawberry tiles, not the hundreds an earlier draft of this
doc claimed — see the correction below. The per-unit gap is real (strawberry realised about $211 a
unit in `92562037` against melon's $25 close); the tile count it applies to is small.

**`scripts/product_search.py` varies `melon_day` and `melon_shift` globally**, across whatever shop
draws the seeds happen to produce. If the truth is "strawberry when the town draws strawberry shops,
melon otherwise", then a global axis averages the two regimes together and reports a **wash** — the
arm that wins on one draw loses on the other, and the marginal comes out flat.

A flat marginal on that axis is therefore **not** evidence that the split does not matter. It is the
expected result of asking a global question about a conditional quantity. The same trap would have
hidden `WOOL_SHOP_SETS_THE_HERD`, which only reads as a rule once the games are split by the draw.

The fix is to slice the dump by shop draw rather than to add another axis — `--analyse` already
keeps every game, and the shop list is recoverable per seed.

### The closing days: a bare pasture, and one starved cow

Alex spotted an empty pasture. It is real, it is in every game checked, and there are two separate
causes behind it.

`kaggriculture.py:804`: **two consecutive unfed days and the animal escapes, leaving the structure.**

```
92550780   final herd COW 6 SHEEP  8   bare structures 1   escapes 0
92562037   final herd COW 9 SHEEP  4   bare structures 2   escapes 1  (COW, day 24, -$400)
92548920   final herd COW 6 SHEEP  8   bare structures 1   escapes 0
```

So one bare pasture per game is a pen **built and never stocked**, and in `92562037` a second one is
a cow that starved on day 24 — $400 of stock plus five days of milk, in a game lost by $4,563.

The bare pen appears on day 24 and is still bare on day 29 in both losses. We were holding $53k and
$95k at that point; a sheep costs $500.

### Why the herd was too small in `92550780`, specifically

The town drew **`YARN_STORE` three times** — at draw #1 (d3), #4 (d12) and #6 (d18). Three
instances is 6 wool a tick, 1,074 a season. Eight sheep produce roughly 100 units in a season (first
yield day 6, one unit every 3 days). The town wanted ten times what we could make, which is why wool
closed **above** base at $252 and never came down.

**The split rule fired correctly and the COUNT is what failed.** Every `BUY_ANIMAL` we issued:

```
d0  COW 1, SHEEP 4     d4 COW 1   d5 COW 1   d6 COW 1   d7 COW 2
d8  SHEEP 2            d12 SHEEP 1          d18 SHEEP 1
------------------------------------------------------------------
total requested        COW 6, SHEEP 8   =  14 animals
```

`WOOL_SHOP_SETS_THE_HERD` did exactly what it is written to do: yarn was in the first three draws,
so cows were held at `WOOL_SHOP_COW_CAP = 6` and every remaining animal went to sheep. But the
rule's own reference table says a draw-#1 yarn store means **COW 6, SHEEP 12, total 18**, and we
ran a total of **14**. `_herd_split` re-splits a `want_total` it is handed and is explicitly
forbidden from growing it ("capped at the schedule's own count"), so the sheep-heavy half of the
rule landed and the extra four animals never did. `92548920` — yarn at draw #2 — is the same:
COW 6, SHEEP 8, total 14, where the table says 18.

**And the early return skips the one branch that does count instances.** Below the wool rule,
`_herd_split` runs a greedy over `town_drain_remaining(...) + expected_future_drain(...)`, which is
genuinely instance-aware and would have seen three yarn stores. The wool rule `return`s before it.
So the code's drain-aware allocation is bypassed in precisely the case where the drain is extreme.

**The bare pen is the same story from the other end.** Fifteen `BUILD_PASTURE` ops, and pens are
still being built on d21 (2) and d24 (1) — after the last animal purchase on **d18**. Fifteen pens,
fourteen animals.

### `92566708` — the herd starved to death on day 12

Lost $56,006 to $109,034, the worst of the five. **Twelve of fourteen animals escaped on days 10-13**
— $5,200 of stock, plus every unit of milk and wool for the remaining seventeen days. The agent
never rebuilt: it finished with **2 cows and 13 bare pens**, feeding exactly 2 animals a day from
day 20 to the close.

```
day  feeds  harv  wheat_shed  money  hands
  8      9     1           0    137      6
  9     10     4           0  1,377      7
 10      1     1           0      1     14     <-- first escape
 11      0     0           0     75     10
 12      0    13           0     22     10     <-- eight escape in one day
 13      0     0           7    167      8
```

`FEED` takes one WHEAT from the acting hand's inventory (`kaggriculture.py:496`), and two consecutive
unfed days releases the animal (`:804`). The shed held **zero wheat from day 8 through day 12** while
the bank sat at $1, $75 and $22 — so neither the stock nor the cash to buy it existed, and a herd of
fourteen needs fourteen wheat every single day.

This is a **liquidity failure that converts directly into destroyed capital**, and nothing in the
agent treats the feed bill as a committed liability the way `RESERVE_THE_SEED_BILL` treats seeds.

### Five games, one repeated waste

Across all five games downloaded on 2026-08-13:

> **CORRECTION, same day.** An earlier version of this table read melon and carrot counts out of
> `why_we_lost.py`'s `crops planted (offers)` column, which prints **BUY_SEED order quantities**, not
> plants. The agent re-posts a standing order every turn, so those numbers are re-offers. Alex caught
> it: *"we have a carrot plant of 6 i dont understand how we planted 42"*. Real plants, counted off
> tile transitions, are the same in every game: **WHEAT 138, STRAWBERRY 36, MELON 19, CARROT 6.**
> The claim "we planted 136 melon to their 19" was an artifact — both sides plant 19.

```
game       MELON plants   MELON closed   EGG drained   EGG closed   geese   CARROT plants
92550780        19            $25            179          $59          0          6
92562037        19            $25            537          $67          0          6
92564858        18            $19            537          $70          0          5
92565805        19            $16            537          $70          0          6
92566708        19            $10          1,074          $88          0          6
```

**Melon closed between $10 and $25 of a $250 base in every single game.** It has no shop and the town
absorbs 30 units a season, so nineteen plants a side is already enough to bury it.

**Carrot is the sharper number.** Six tiles at 4 units each is about 24 units of carrot, against
towns draining **716, 895 and 716** — and carrot closed ABOVE base every time it was drawn. Carrot
also has the deepest glut tolerance of any crop (842 units to the floor), so there is no price risk
in growing far more of it.

**EGG closed ABOVE base in all five**, between $59 and $88, with the town draining up to 1,074 units
— and we ran zero geese in all five, because EGG was unsellable when the goose flag was measured.

### On the forum claim ("multiply base by shop count")

Half right, and the half that is wrong is the half that matters. Shop count sets the **sustainable
rate**, not the price: the price is a pure function of inventory. Milk with three shops still floors
after 76 units of excess, which is why our own milk has repeatedly closed at $1-$5 while the claim
says it "sells above 160 most of the season". Both statements are true at different volumes — the
drain is about 327 milk a season, roughly 11 a day, and a herd that produces faster than that puts
its own price on the floor no matter how many shops are open.

---

## 2026-08-13 — The late season is a market problem, not a turns problem or a routing problem

Folded in from docs/the_market_is_the_late_season_2026-08-13.md.
Seed 11, tape victor, measured on `scripts/breakdown.py` and `scripts/sell_when.py`.

Three explanations for the late-season gap were tested and killed in one session.
Recording them together because each was believed at the time and each cost a run.

### Turns are not the constraint

Raising the schedule's `hands` row from 10 to 14 on d26-d29 cost **-$3,350** and bought nothing:

```
hire     d26 10->14   d27 10->14   d28 10->14   d29 9->14
pass     d26 36->124  d27  1->89   d28  8->50   d29 27->123
water    d26 36->36   d27 43->43   d28 26->27   d29 13->13
```

The extra hands stood still and drew wages.
This should have been predicted rather than measured: the control already idled 36 turns on d26,
which is the direct disproof of "the crew is 80 turns a day short".

The season totals say the same thing from the other side.
Ours against the tape: **work 2,978 / 2,800** and **idle 862 / 935**.
We already do 178 more ops than Victor and idle less, and finish $11k behind him.

Spare capacity is also the wrong SHAPE, which is the more useful half of the finding.
Idle turns per unit, by day: d20 0.1, d24 0.1, d21 0.4, d25 0.8, d22 1.1, d17 1.2.
One or two turns per unit at dusk cannot absorb a trip; work only fits where a unit already stands.
The only real slack is d28 (56 turns), d29 (89) and, earlier, d10 (98), d18 (73), d16 (63).

### Routing is not the constraint either

The late-season pair below changes the job pool, so d26-d29 were re-solved in day order
(`scripts/solve_day.py`, fixtures dumped from inside `breakdown.py`'s own harness).
Against the new pool the shipped greedy already covers almost everything:

```
d26  60 jobs   greedy 60/60      d28  51 jobs   greedy 48/51 -> 51/51
d27  61 jobs   greedy 61/61      d29  25 jobs   greedy 25/25
```

**But coverage is not the product.** Dropping d26/d27/d29 from `SOLVED_DAYS` on the reasoning that
"the greedy already covers them" cost **-$2,277** and put weeds back to 5 a day.
The solver also minimises turns and fixes the visit ORDER, and `_live_ops` re-derives work at each
stop, so a better order does strictly more work at identical coverage.
Coverage and order are two different claims; do not read one as the other.

### What the late-season pair is, and what it measured

Three changes, all gated to d26 and later, in `kagg/search/router.py` behind `LATE_SEASON_PAIR`:

- `FERTILIZE_UNTIL_DAY = 26` -- no tile is offered a FERTILIZE from d26. Ours ran 9/11/5 against the
  tape's 2/0/0 on d26-d28.
- `LATE_TRUNCATED_PLANT_DAY = 26` -- `plant_prize` stops returning 0 for a window the season cannot
  finish, so a wheat sown d26 prices at the two waters it can actually reach.
- `HARVEST_A_TRUNCATED_ONE_SHOT` -- `_one_shot_is_finished` takes a partial once the window cannot
  close before d29. Victor takes 26 wheat on d29 at `held 4 / max 6`.

They are a pair by construction and were measured as one, per
`docs/the_late_season_is_one_defect_in_two_halves_2026-08-12.md`.
Half one alone plants tiles nothing can collect; half two alone makes late plantings valuable with
no ground cleared for them.

Measured, control -> arm, season money:

```
stale routes          72,184 -> 70,321   -1,863
re-solved routes      72,184 -> 71,814     -370
routes dropped        72,184 -> 69,537   -2,647
```

With the routes re-solved the rows land on the tape almost exactly:

```
plant    d26  0 -> 12   (tape 11)
weeds    d27  0 ->  1   d28 0 -> 1   d29 0 -> 1   (tape 0/1/1)
water    d28 26 -> 38   (tape 39)
harvest  d28 17 -> 30   (tape 20)
```

**-$370 on one seed is undecided, not a win.** It is well inside the ~15% seed variance, and the
ladder is an Elo rating, so the decider is `scripts/field_sweep.py` against recorded opponents, not
this grid. Note the grid CANNOT see the thing that matters: `breakdown.py` runs our agent and the
tape as separate seat-0 runs against their own recorded adversaries, so our sells never move the
tape column and a change that starves an opponent looks identical to one that does not.

### CORRECTION, same day: the milk floor is a HARNESS artefact

Three ladder episodes downloaded 2026-08-13 (92450417, 92443929, 92442061) carry the market price at
each day's close. MILK never floors on the ladder in this sample:

```
92450417   169 -> 279 over the season
92443929   169 -> 258
92442061   169 -> 154   (and WOOL dips to 82 on d10, then recovers to 245)
```

`breakdown.py` seats our agent against a REPLAYED tape, and both sell into one book. A tape that
sold 303 milk in its own game sells it again next to us, so the harness gluts a book no real game
gluts. That is the identical failure `7a88d30` warned about for the mirror sweep.

The section below is therefore true OF THE HARNESS and unproven on the ladder by this source's own
account. Re-measure it from a ladder replay before acting on it. `SHOP_ADAPT_HERD` reading shops
rather than prices is still a real gap, but the evidence that it is COSTING anything was, as of this
correction, withdrawn.

**UNRESOLVED CONTRADICTION — needs a measurement.**
This correction states MILK never floors on the real ladder, based on 3 episodes
(92450417, 92443929, 92442061).
The 2026-08-13 "How deep each market is" section above, folded in from
`docs/market_depth_and_the_morning_losses_2026-08-13.md`, reads 5 *different* real downloaded
ladder episodes (92550780, 92562037, 92564858, 92565805, 92566708) the same day and finds MILK
closing at $5, $1-$5 repeatedly, floored well below base in multiple real ladder games — not a
`breakdown.py` harness replay.
Both sets are described in their source documents as real ladder tapes, not harness constructions.
The two documents disagree on whether MILK floors on the actual ladder.
Neither source reconciles the other set of episodes.
This needs a wider, single-method sweep across all recorded episodes before either claim is trusted.

### Where the money actually is: we flood our own book

`scripts/sell_when.py` prints exact per-product SELL fills per day, per unit price, via
`kagg/analysis/fills.py`. Ours, d18-d29:

```
MILK   units   18   3  14  21   3  12  21  11   3  12  15  26
       $/unit   4   1   3   1   1   2   3   5   2   5   3   3

WOOL   units    0  16   0  16   0   0  12   4   0  18   4   0
       $/unit   0   1   0  25   0   0 160 109   0 181 146   0

MELON  d20 60 units at $151, then d21 12 at $5 and d22 12 at $1
```

**159 units of milk at $1-$5.** Realised milk was $223.81 a unit in episode 92077611.
Wool is the control that proves the mechanism: $1 on d19, then $160/$109/$181/$146 on d24-d28 when
it goes out in smaller lots. The town's demand refills; we do not let it.

Total sell revenue is $214,385 against a final bank of $71,814. The revenue exists. The price we
accept for it does not.

This corroborates what `7a88d30` already recorded and nobody carried forward: across the eleven
newest ladder losses, every game where `SHOP_ADAPT_HERD` cut us to six cows closed MILK above base
($169, $235, $249) and every game at eight or nine floored it at $1. **The cow COUNT is causal.**

And `SHOP_ADAPT_HERD` cannot see any of it. It floats the cow/sheep split on which SHOPS exist --
three of eight carry milk, so it reads "well supported" and buys cows -- and never reads a realised
price. We run COW 10 / SHEEP 4 against every recorded opponent's COW 8 / SHEEP 6: heavy in the
floored product, light in the one paying $180.

Two pens also stand empty from d24 to the end. Pens 15, animals 13, tape 14.

### The geese verdict was measuring our own bug

`c9c1c18` and `7a88d30` killed geese on two sweeps, both **outcome-only** -- win rate and mean money.
An outcome test cannot separate "geese are bad" from "we play geese badly", and the fills were never
read.

Restored the machinery from `7a88d30` and ran `HERD_GEESE = 2` through `sell_when.py`:

```
EGG fills, whole season          0
animals                     10 (13 without geese)
season money                48,196 (71,814 without)
sell revenue               188,908 (214,385 without)
```

**Not one egg is ever sold.** The birds are bought, fed and cared for over thirty days and produce
nothing that reaches a sale. The -42 points of win rate is the cost of three animals' worth of turns
and money against zero revenue; it says nothing about whether a goose is worth owning.

The stale baked routes cost part of that $23k -- `SOLVED_DAYS` was solved on a goose-free pool -- but
stale routing cannot produce zero egg sales.

This is the fifth time an animal verdict here has turned out to be an artefact. The rule in CLAUDE.md
already covers it: ask what the code could not express before trusting a mechanic-level negative.
The addition this time is narrower and mechanical: **an outcome-only sweep is not a test of a
mechanic.** Before believing one, read the fills for the product the mechanic is supposed to produce.

(The main survivor-file section above, "Geese are UNMEASURED, not dead", records the later
2026-08-15 state: the `SELLABLE` fix landed and one goose did sell 51 eggs with the egg book
finishing at $95 with a 445-unit deficit. That is consistent with, not contradicting, this finding —
this section's zero-egg-sales measurement predates the `SELLABLE` fix reaching the code path being
tested here specifically through `sell_when.py`, and is recorded because it is the direct proof that
an outcome-only win-rate sweep cannot see a mechanic producing zero revenue.)

### Open, in priority order, as of 2026-08-13

1. Meter the milk sell rate, or cut the cow count. This is where the $11k is.
2. Re-capture the tape side of `sell_when.py` -- the split-on-turn-wrap only caught one env, so
   whether Victor sells the same units in smaller lots is still unmeasured.
3. Re-run the geese properly: re-solve the routes for a goose pool, and require an EGG row with
   units before reading any money at all.
4. Field-sweep `LATE_SEASON_PAIR`. It needs a second route set so the off-arm is not seated with
   routes solved for the on-arm's job pool.
5. Fill the last two pens.

---

## 2026-08-15 — When and what to sell: an optimisation analysis

Folded in from docs/when_and_what_to_sell_2026-08-15.md.
Every number here is computed from `reference/kaggriculture.py` and the shipped plan
(`kagg/plan.py:SHIPPED_PLAN`), not measured in a game. **It is a model, not a result.** The
falsifiable prediction at the end is the part that can be checked.

### 1. The mechanics that decide everything

Selling raises market inventory, and inventory starts at `MARKET_I0 = 10000`. So a sale pushes the
book **above** `I0`, which means the `above_func` / `above_target` pair governs price impact — not
the `below_*` pair that the 2026-08-15 balance change altered.

```
price(I0 + x) = base - (above_target * base / shape_above(T)) * shape_above(x)
```

Two knobs matter: the **shape** and the **knee `T`**. A small `T` with a convex shape is brutal.

#### How far a sale moves the book

```
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
```

**STRAWBERRY loses 10% of its price after SIX units. MILK after eight.** WHEAT and EGG are
effectively undentable — a log curve with `atgt 0.2` never dies.

#### What the town takes back

`_town_consume` runs every `townShopSellInterval = 4` steps (6 times a day) and every
`townCenterSellInterval = 24` steps (once a day). Each unlocked shop instance consumes one unit of
each product it stocks, doubled if the shop stocks only one product.

```
product     shops that buy it (units/day each)              town  max/day
WHEAT       bakery:6 pizza:6 brunch:6 ice:6 farmers:6          1       31
STRAWBERRY  brunch:6 ice:6 smoothie:6 farmers:6                1       25
CARROT      pet:12 farmers:6                                   1       19
MILK        pizza:6 ice:6 smoothie:6                            1       19
TOMATO      pizza:6 farmers:6                                  1       13
EGG         bakery:6 brunch:6                                  1       13
WOOL        yarn:12                                             1       13
MELON       — no shop stocks melon —                            1        1
```

Shops unlock one per three days, drawn **with replacement**, capped at `MAX_SHOP_INSTANCES = 8`. So
the drain ramps through the season and its composition is a random draw — which is what
`SHOP_ADAPT_HERD` is reading.

**MELON has no shop. The town absorbs one melon a day, thirty for the whole season.**

### 2. Supply against absorption

The shipped plan's season sell totals:

```
product      plan sells  drain/day  days to absorb  verdict
FERTILIZER         1487          0               -  NOTHING DRAINS IT
WHEAT               868         31            28.0  tight
MILK                279         19            14.7  ok
STRAWBERRY          223         25             8.9  ok
WOOL                120         13             9.2  ok
MELON                120          1           120.0  4x OVER THE SEASON
CARROT                20         19             1.1  ok
```

Two lines break the budget: **melon at 4x season absorption**, and **fertilizer, which no shop and
no town centre ever removes.** Fertilizer is `BUYABLE`, so the only thing that restores its book is
an opponent buying it back.

### 3. What spreading is worth

Simulating each product's season — walk `n` units down the curve each day, then let the town remove
its drain — for the plan's own day-by-day schedule against a flat spread of the same total:

```
product      units    plan $    even $     delta   $/unit plan   even
MELON          120    24,968    26,763    +1,795           208    223
MILK           279    38,146    42,219    +4,073           137    151
WOOL           120    23,886    23,970       +84           199    200
STRAWBERRY     223    20,810    25,331    +4,521            93    114
WHEAT          868    18,272    19,906    +1,634            21     23
FERTILIZER    1487    26,039    26,039        +0            18     18
CARROT          20       671       700       +29            34     35
TOTAL                152,792   164,928   +12,136
```

**About $12k of pure scheduling gain**, concentrated in STRAWBERRY (+4,521) and MILK (+4,073) — the
two products with a linear above-curve and a knee under 125.

Caveat: an even spread is not always feasible. Melon is a one-shot crop with `first_yield_day 10`,
so it cannot be sold before d10 — but it can be held later at no cost beyond shed space. Milk and
strawberry accrue continuously and are genuinely spreadable.

### 4. The melon branch — the rule may be backwards

`MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT` swaps our melon rows to strawberry when the opponent holds
`>= MELON_YIELD_OPPONENT_MELON = 7` melon at d5. It fires in about 68% of games and shipped on
2026-08-15 on tape evidence alone.

The plan front-loads **60 melons on d10** and trickles the rest (d11 +12, d16 +6, d17 +30, d18 +12).
Into a 1/day drain that is a race: whoever loads the book first gets the good prices.

Simulating a shared book, both seats interleaved one unit at a time as `_process_market` does:

```
case                                          melon $   straw $   OUR TOTAL
A  keep melon   | opponent sells NO melon      24,968     9,909     34,877
B  keep melon   | opponent sells the SAME 120  13,549     9,909     23,458
C  swap→straw   | opponent sells NO melon           0    15,296     15,296
D  swap→straw   | opponent sells the SAME 120       0    15,296     15,296
```

**Even in the melon-heavy case the rule exists for, keeping melon beats swapping by $8,162.**

The reason is that strawberry is already saturated. 223 units into a 25/day drain is near the limit;
adding 120 melon units on top returns only **+$5,387, or $45/unit**, while contested melon still
pays **$113/unit**. Melon's base is $250 against strawberry's $120, so a crushed melon outsells a
crushed strawberry.

Model limits, stated plainly: melon units are converted to strawberry **1:1**, which flatters the
swap (melon yields 6/tile against ongoing strawberry's 4); the swap shifts revenue from d10–d18 to
d15–d29, which interacts with land purchases and is not modelled; and the opponent's melon flow is
assumed to follow the schedule's shape.

**UNRESOLVED CONTRADICTION — needs a measurement.**
This section's model concludes keeping melon beats swapping to strawberry, even in the melon-heavy
case, by $8,162 in its own simulation.
The 2026-08-13 "How deep each market is" section above (folded in from
`docs/market_depth_and_the_morning_losses_2026-08-13.md`) reads a real ladder loss, `92562037`,
where melon planted 19-to-19 still closed at $25 of a $250 base and is flagged there as the one
large divergence in a lost mirror game — read in that source as evidence melon overplanting is
costly, not neutral-to-good.
Neither source directly refutes the other (one is a scheduling model holding the opponent's flow
fixed to the plan's own shape, the other is a single real game with an unknown opponent flow), but
they point opposite directions on whether melon volume is the problem or the schedule's melon
*timing* is the fix.
Section 7's own falsifiable prediction below is the proposed way to settle this.

### 5. The policy this implies

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

### 6. The experiment worth running

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

### 7. Falsifiable prediction

Made **before** the data landed, on 960 games against 24 recorded ladder opponents:

> `MELON_YIELD_OPPONENT_MELON = 99` (rule off) should beat `= 7` (rule as shipped).

If the sweep comes back the other way, this model is wrong and the reason is worth more than the
model was.

---

## 2026-08-15 — The season ends with the crew holding the margin

Folded in from docs/the_stranded_load_is_the_loss_2026-08-15.md.
Measured 2026-08-15 off three downloaded ladder replays, at the final step of d29.
Read from the recordings, not simulated.

```
episode     our stranded          their stranded     result
93318573    81 units  ~$3,264      4 units  ~$19     lost by   $645
93323101    55 units  ~$3,526      0 units    $0     lost by $3,919
93286476    70 units  ~$2,238      0 units    $0     lost by   $962
```

**In all three the stranded value exceeds the losing margin.** Two of the three are wins if that
produce reaches the shed. Our shed is EMPTY at the close in all three; the goods are in hands.

### Why it happens

`_end_of_day` calls `_drop_inventories_to_shed`, so on any ordinary day a carried load reaches the
shed for free. That is why カワシギ emits **five** DROP ops in the whole of `92498144` against 389
harvests -- he almost never needs one.

On d29 that drop still runs, but it runs after the final turn, and `_commit_unit` refuses a SELL
unless the goods are already in `private["shed"]`:

```
if op == "SELL":
    if private["shed"].get(item, 0) <= 0:
        return False
```

So the pipeline is **one day delayed**: harvest on day N, banked free at the N/N+1 rollover, sold on
day N+1. Anything harvested on d29 has no day N+1.

The tape solves it by spending **9 DROPs on d29** against our 2.

### The consequence that makes this cheap

A d29 harvest that is not delivered is worth **exactly zero -- the same as not harvesting it.**
So turns spent walking to the shed on d29 cost nothing real. There is no trade-off to balance.

### Three fixes tried, all measured, all recorded so they are not re-tried blind

1. `WALK_THE_LOAD_HOME_DAYS = (10, 29)` -- recovered 7 units of 58. A solved route stores work stops
   only; `materialise` appends the shed trip out of slack, and d29 has none.
2. `NO_UPKEEP_ON_THE_LAST_DAY` -- frees 28 turns (FEED and CARE on d29 pay out at a rollover into a
   day 30 that does not exist; the tape does zero of both). **Regressed** the grid: harvest
   396 -> 389, sell 1489 -> 1474, and d29 HARVEST fell 27 -> 20 while gaining 28 turns, because
   `cover._apply_precomputed` keys a stop on `(tile, ops)` -- change the ops and the stop leaves the
   route rather than getting cheaper.
3. `UNSOLVE_DAYS = (29,)` -- greedy plans d29 with `deliver=True`. Sell 1489 -> 1502, d29 sell
   93 -> 106, +$256, harvest 396 -> 393. Stranded rose 51 -> 78: the greedy harvests more than it
   walks in.

### Also measured and NOT the cause

- **d28 is not under-prioritising.** Its solved route seats every job with slack and two hands idle;
  only 7 ripe units remain unharvested at dusk. Promoting d28 harvests by prize, by `at_risk`, and
  by `at_risk` plus a d28 re-solve were all three byte-identical on the grid.
- **Planting dates are identical to the tape** -- d25 9/9, d26 9/9, d27 11/11 -- so his crops do not
  ripen earlier than ours.
- Shed overflow discards only 5 units a season.
- Spreading the sell across hours instead of one is worth $64.

So what gives him d28 harvest 32 to our 27, and d29 19 to our 27, is still unexplained. It is
neither ranking nor planting date.

### Where the fix has to go

`RESERVE_DAYS` already covers d29 and `cover.cost` already knows how to price a tour that ends at
the shed. Two things block it: the reserve is gated behind `deliver=True`
(`PRICE_THE_TOUR_THE_CALLER_WILL_WALK`), which only d10 sets, and d29 is precomputed so `cover.cost`
never runs at all. A fix needs the delivery to be a **planned stop** -- either stored in the solved
route, or budgeted before the work is seated -- rather than appended from slack that does not exist.

---

## Note on a source file left untouched

`docs/fable_the_discard_problem_2026-08-09.md` was checked in full during this consolidation and
**does not belong in this file.** Its subject is `FEED_RESERVE_YIELDS_TO_OVERFLOW`, the wheat-reserve
shed-eviction mechanism, and whether releasing it reduces harvest lost to shed overflow (discards
measured in units destroyed per night, day-gating bug fix, router "hands were never sellable" claim).
It touches SELL only as the mechanism it argues cannot fix the discard on its own — the market price
curve, depth, or sell timing are not its subject. It belongs with the crops/watering/harvest-discard
group, not this one. Left untouched, per instruction.
