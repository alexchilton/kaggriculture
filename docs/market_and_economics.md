# Market and economics

This doc merges 22 files from `docs/` on one topic: market mechanics, pricing curves, the
2026-08-15 balance/hinge change, crop-mix economics, herd/pen geometry, simulator parity and
state-leak fixes, shed/discard mechanics, and wheat churn.
Every source file is preserved in full in `docs/history/` after this consolidation.
Each claim below carries a `source:` tag naming the original file.
Where a source file already carries its own status banner (SUPERSEDED, STALE, CORRECTION,
RETRACTED), that status is carried forward here, not re-decided.
Where two files disagree, both are stated; no winner is silently picked.

---

## 1. The sell/price mechanism

`market_price(item, inventory, params)` is a **pure function** of inventory, monotone decreasing
above `I0 = 10,000`, computed from `reference/kaggriculture.py:177-191`.
`_commit_unit` raises market inventory by exactly one per unit sold.
Sales at the $1 floor do not increase market supply — the floor is an infinite sink, so a crashed
book is recoverable but its value is forfeit, not destroyed.
`_town_consume` lowers inventory by an amount depending only on the step and
`town.unlocked_shops`, and runs immediately after `_process_market` every step.
(source: the_market_2026-08-09.md)

Both `market` and `town` are `shared: True` in the observation, so both terms of the sell
decision are free to compute — no opponent order needs to be seen.
The derived (not fitted) sell rule:

```
λ_p = market_price(p, I_now + Q_rem - contest * D_rem)
offer n units now, largest n with market_price(p, I_now + n) >= max(λ_p, (1-slip)*market_price(p, I_now))
```

`contest` is the one free, game-theoretic dial: `1.0` is the single-player optimum, `0.5` the
two-player split; lower sells sooner.
(source: the_market_2026-08-09.md)

`FEED` consumes exactly 1 WHEAT per animal per day, taken from the shed
(`reference/kaggriculture.py:505-512`), so wheat is a consumable as well as a market product.
(source: market_curves_and_the_q4_branch_2026-08-15.md)

`_process_market` reads ONE market object off player 0's observation and drains it per unit in
lockstep between both seats (`reference/kaggriculture.py:544-547`).
Every unit either seat sells lowers the other's price: prices are a race, not a private resource.
(source: market_curves_and_the_q4_branch_2026-08-15.md)

### Price curve, by surplus (2026-08-15 measurement, post-hinge)

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

Three structural facts follow.
**Wheat cannot be crashed, but it can be halved**: its whole downside is $25 to $19 even at +1000
surplus, but the range actually in play is $21 (surplus) to $47 (deficit), and ~800 units are grown
into that book, so more wheat really does cost money per unit.
"Monotonically safe" is wrong; "never goes to $1" is what is true.
**TOMATO and CARROT are the only two crops with a `hinge` undersupply curve**, quadratic past
`u = x/T > 1`: tomato at -400 deficit is $300, at -800 it is $1,884, at -1200 it is $5,004.
**EGG is the only animal product that cannot be crashed**: milk decays linearly and wool
quadratically, both reaching $1 at about +100 surplus; egg decays logarithmically and holds ~$38
at +1000.
(source: market_curves_and_the_q4_branch_2026-08-15.md — this file's sections 1-6 are unaffected by
its own later note about section 7, see §3 below)

### Depth from a balanced book (pre-hinge, still correct arithmetic — pure function of `MARKET_PARAMS`)

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
not track price level.
(source: the_market_2026-08-09.md)

### Units above I0 to reach the $1 floor (a second, independent computation, same underlying curve)

```
WOOL          sq      T=105    59 units
STRAWBERRY    linear  T=100    62 units
MILK          linear  T=122    76 units
MELON         sq      T=300   158 units
WHEAT         log     T=400   effectively unfloodable
```

(source: the_book_is_shallow_2026-08-09.md)

### Depth table with drain and price-at-N, computed identically a third way

```
product      base  shops   drain     p@50    p@100    p@200     to $1
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

`drain` is the season total: instance N unlocks on day 3N so it is live for `180 - 18N` four-step
ticks (792 tick-instances over eight draws); shops are drawn **with replacement** from eight
names; a single-product shop consumes double.
Reading it: **WHEAT and EGG never floor** (log decay: 200 wheat still fetches $21 of $25 base, 200
eggs $41 of $50).
**WOOL, MILK and STRAWBERRY are shallow to the point of fragility** — 59, 76, 62 units of excess
and they hit $1; they are also the highest-value products, so they are simultaneously the best and
the easiest to destroy.
**MELON has no shop at all**; its only buyer is the town centre, 1 unit per 24 steps, 30 a season,
against a $250 base.
(source: market_depth_and_the_morning_losses_2026-08-13.md)

### A fourth, independent curve table (2026-08-15, sell-timing framing)

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

**STRAWBERRY loses 10% of its price after SIX units. MILK after eight.**
WHEAT and EGG (log curve, `atgt 0.2`) are effectively undentable.
(source: when_and_what_to_sell_2026-08-15.md — STALE, see §6 below for the banner in full)

### What the town takes back, per day

```
product     shops that buy it (units/day each)              town  max/day
WHEAT       bakery:6 pizza:6 brunch:6 ice:6 farmers:6          1       31
STRAWBERRY  brunch:6 ice:6 smoothie:6 farmers:6                1       25
CARROT      pet:12 farmers:6                                   1       19
MILK        pizza:6 ice:6 smoothie:6                            1       19
TOMATO      pizza:6 farmers:6                                   1       13
EGG         bakery:6 brunch:6                                   1       13
WOOL        yarn:12                                             1       13
MELON       — no shop stocks melon —                            1        1
```

Shops unlock one per three days, drawn with replacement, capped at `MAX_SHOP_INSTANCES = 8`.
**MELON has no shop. The town absorbs one melon a day, thirty for the whole season.**
(source: when_and_what_to_sell_2026-08-15.md, STALE)

### A day-by-day book crash, seed 3, contested, both seats shipped

```
 day    MELON   STRAWB   TOMATO   CARROT    WHEAT
   0      250      120       60       35       25
  10      271      181       61       36       36
  13       94      195       62       36       40
  20       96      216       62       37       45
  26      111      147       63       38       42
  29      118       59       63       40       41
```

**Melon is a three-day race, d11 to d14**: it climbs to $271 as the town eats it before anyone
harvests, then both farms' melon lands and it falls to $81; sell d10-d11 for $250+, sell d14 for
$81.
**Strawberry peaks at $216 on d20** — 80% over base — then collapses to $59 over the last six
days as our own harvest lands: we sell our best product in its worst week.
Melon recovers late (to $118 by d29) because its decay is `sq`.
In replay `93372504`, WOOL floored on d16 at +59 surplus and MILK on d24 at +76; our 10 cows
against their 8 changed nothing — both books died for both seats.
(source: market_curves_and_the_q4_branch_2026-08-15.md)

### Realised prices, real ladder confirmation, 12 recent games

```
product       base |  OURS-WIN units   $/u |  OURS-LOSS units   $/u |  ALL FOES units   $/u
MELON          250 |             984   150 |             247   111 |           1,050   153
WOOL           200 |           1,950   147 |             398   127 |             896   141
MILK           160 |           2,082   205 |             321    73 |           1,405   161
STRAWBERRY     120 |           2,711   182 |             562    78 |           1,366   154
WHEAT           25 |           9,115    45 |           1,693    49 |           7,124    48
```

Wins and losses share the same board — 97 tiles, same herd, same third-parcel day in every game
but one — and differ almost entirely in price realised on milk and strawberry; wheat is *better*
in the losses.
(source: the_market_2026-08-09.md)

---

## 2. Why we oversold, and the shed/eviction rules (2026-08-09, the_market file)

`schedule_agent.py:1947-2088` (pre-fix): both throttles (`rate[prod]` per-offer cap, `allow`
day-total cap) were transcribed from the tape's own schedule row, keyed to *its* production, not
ours.
We plant 77 tiles to its 45, so surplus had no row to release it.
Measured on the handover fixture (seed 11, weeds off, tape plays d0-10, agent from d11), pre-fix:

```
day    11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28
shed   14  33  35  35  45  86 100 100 100 100 100 100 100 100 100 100  90 100
lost    0   1   2   1   0  21  13  27  23  18  42  36  28  11  41   7  10  24
```

**331 units destroyed**, shed pinned at its 100 cap from day 17; the tape holds 18-36 all season
because it never stops selling.
(source: the_market_2026-08-09.md)

`PRICE_AWARE_SELL_CAP` and `RESERVATION_SELL_CAP` both ship ON (verified directly in
`kagg/search/schedule_agent.py`, lines 920 and 974 as of 2026-08-09).
`PRICE_AWARE_SELL_CAP` drops the day-total cap when the live price is at or above base; a first,
uncapped version cost ~30% of mean money against every arena opponent (seeds 500-505).
Corrected (only `allow` moves), on the handover fixture (seed 11):

```
                  final     destroyed    turns at cap
OFF             $71,976        331            12
ON              $75,866         82             2
                +$3,890        -75%
```

On the arena pool this read as neutral ($103,932 → $102,095, win 94.4% both ways) because the
pool was saturated with `mirror` at 50%.
`RESERVATION_SELL_CAP` replaces the binary `price >= base` test with the per-product depth rule;
it was nearly shipped as a widen-only rule and would have been a no-op (five seeds byte-identical)
had `rate[prod]` not already been smaller on the turns that mattered.
Measurement that shipped it:

```
              mean bank    units destroyed    land parcels
OFF             62,868        86 - 165        [4, 6, 15/16]
ON              64,667        39 - 107        [4, 6, 16]
```

+2.9% bank, a third off destroyed units.
On the handover fixture, six of nine products run at a deficit the entire season (milk peaks at
$315 against base $160, wheat at $51 against $25) — "we sell 71 wheat where the field sells 525"
there is a production ceiling, not a policy one.
(source: the_market_2026-08-09.md)

### Overselling into a book the opponent is already filling

Across 14 real ladder losses, holding the opponent's play fixed and re-pricing only our own sales
**downward**, 12 of 14 become wins (gaps $715-$4,266, recoverable revenue $7k-$33k/game):

```
recoverable money, summed over 14 losses
  WOOL            +135,250
  STRAWBERRY       +57,433
  MILK             +57,163
  MELON             +4,447
  WHEAT                  0
  FERTILIZER             0
```

Optimal fractions of the observed sell:

```
WOOL         0.7x  best in 7 of 14 games (0.6-0.8 in 11)
MILK         0.5x  best in 4, 0.6-0.7 in 5
STRAWBERRY   0.7x  best in 6, 0.9x in 4
WHEAT        1.0x  -- no gain, ever
FERTILIZER   1.0x  -- no gain, ever
```

"Less, not slower": downscaled (fewer units, same shape) gains **+254,293** total across 56 cases
(best in 16); spread (same units, even cadence) gains **+87,343** (best in 16); both gains
**+252,611** (best in 17) — cutting-plus-spreading adds nothing over cutting alone, except WOOL,
which is a volume problem: episode 91122388, $5,278 observed vs $23,794 at 0.7x volume, 4.5x
revenue from 70% of the units.
MELON is a cadence problem; MILK is both; STRAWBERRY is often already right.
(source: the_market_2026-08-09.md)

Across-lever correlation with money, 124 seats / 62 games:

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

The one lever with real headroom is `buy_product` (49th percentile against a top-quintile 1,156):
OPEN-3's buy-wheat → feed → milk conversion.
Against `vs_tapes.py` (a real top player, not the near-passive handover fixture): we lose 4/4 to
`oldleader` (margins -$8,982, -$4,268, -$8,178, -$6,811 on seeds 11/101/202/303) and beat `seb`'s
own tape by +$98,483 on seed 11.
(source: the_market_2026-08-09.md)

Two traps, caught twice: **money is not the objective; the ladder is Elo** — Seb's own sell mix
earned more money on every seed and still lost 8/8 head-to-head, because ceding wool let the
opponent earn more than we gained; and **a replayed tape does not react** — absolute money
against a tape runs 2-3x real ladder games.
(source: the_market_2026-08-09.md)

---

## 3. The 2026-08-15 hinge / balance change

Posted by the competition organisers, quoted verbatim because the percentages are the content:

> Small balance change. I'm adding a small change to eggs, tomatoes and carrots, such that their
> price will increase significantly if there is a large shop demand and no production.
> tomatoes => 50% of games; carrot => 26% of games; eggs => 22% of games.
> The intent... is to roughly preserve the existing market dynamics, but make these products
> viable in some situations, not universally... You should update to >=1.32.7.

`kaggle-environments >= 1.32.7` is now required; `CLAUDE.md` still said `>= 1.32.2`, the version
that first contained the env, not the version the ladder runs.
Every baseline in the repo before this predates the change: the 29-day kawashigi grid, the mirror
gate win rate, the build's dollar identity, the schedule rows themselves.
(source: balance_change_eggs_tomatoes_carrots_2026-08-15.md)

The three products buffed — CARROT, TOMATO, EGG — are the three this agent could not sell at all
until 2026-08-13 (`SELLABLE` omitted them).
Four carrot arms were measured and rejected while carrot revenue was structurally zero, and the
goose verdict is downstream of the same bug: geese were switched off and later deleted on evidence
gathered while EGG could never reach the market.
"Animals don't pay" has been an artifact four separate times already; this is a candidate fifth.
This is **not** a universal buff — it fires only when shop demand is high and nobody is producing,
which makes it a contention question of the same shape as `MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`
(read the opponent's board and yield the crop they're flooding), pointed at a different crop.
(source: balance_change_eggs_tomatoes_carrots_2026-08-15.md)

### Mechanism, verified against the organiser's own percentages

`market_price` below I0 (`reference/kaggriculture.py:198-201`):

```
price = base * (1 + below_target * hinge(x / T)),   x = I0 - inventory
hinge(u) = u + 8.0 * max(0, u - 1)^2                 (:68-73)
```

`_town_consume` subtracts stock unconditionally, so with no production the deficit `x` grows
linearly.
Monte Carlo over the shop draw gives P(hinge fires by d29, zero production) = CARROT 25.8%,
TOMATO 53.4%, EGG 22.4% — against the organiser's announced 26% / 50% / 22%.
The model is validated to the organiser's own numbers.
(source: fable_allocation_economics_2026-08-15.md)

Because inventory below I0 only deepens on a sale, the pure-scarcity optimal release is to hold
and dump at d29 (shed cap permitting).
Zero-production book quotes, by day (quantiles over 20k shop draws):

```
CARROT (base 35, T 450, bt 1.00)      TOMATO (base 60, T 200, bt 0.40)     EGG (base 50, T 332, bt 0.40)
day   p25  med  p75  p90   max        p25  med  p75  p90   max             p25  med  p75  p90  max
10     36   38   41   43    50         61   63   67   69    72              51   51   54   54   56
15     37   41   46   51    68         63   68   72   76    90              51   53   56   58   64
20     39   45   53   60   180         67   73   80   88   298              53   57   60   63   81
25     44   53   63   74   500         71   80  101  160   956              56   60   65   70  202
29     49   58   71  116  1068         77   86  165  317  1803              58   63   69   83  397

WHEAT, same premise (base 25, sqrt below-curve, FIVE shops stock it):
d10 33, d15 37, d20 41, d25 45, d29 48 (medians)
```

(source: fable_allocation_economics_2026-08-15.md)

### Unconditional conversion has no edge — the paired sweep

**Wheat is itself on a starved book.** Five of eight shops stock wheat, so a zero-production wheat
book reaches $48 by d29 on its own; arm-0 games realise $45.2/unit on wheat, and the extra
carrots realise only $42-43/unit — the "premium" crop pays LESS per unit than the crop it
replaces, in the median game.
Paired re-run, `WHEAT_TILES_TO_CARROT` 0/8/28, 12 richest recorded opponents, seeds 1300-1302,
both seatings, 72 paired boards/arm:

```
arm    win     margin delta vs 0 (paired)    sign of margin delta
  0   80.6%              —                          —
  8   83.3%    mean +12, median +906         44/72 positive
 28   77.8%    mean -1,614, median -1,883    52/72 NEGATIVE  (sign test p < 0.001)
```

The arm-28 loss decomposes per game: direct swap carrot +84u ($3,524) minus wheat sold -70.8u
(-$2,616) = net +$908; gift to opponent (their wheat +$725 on unchanged units) = net -$725; feed
cascade (our MILK -18.6u, WOOL -11.1u; our str/milk/wool -$1,981, their milk/wool +$1,474) = net
~-$1,800.
Four mechanisms in order of size: wheat's own scarcity premium (the swap is a wash in the median
game, +$32/stop); the book is shared, so withdrawing supply is a price gift; the wheat buffer
feeds the herd on the margin (8 conversions: milk -0.3u, wool -0.0u, inside the buffer; 28
conversions: milk -18.6u, wool -11.1u, not inside it); three of twelve opponents already produce
the "no production" crops (tawashi 58 carrots/game, YassY 24; HoJoonYun 24 tomatoes).
(source: fable_allocation_economics_2026-08-15.md)

### The conditional play — the shop draw is public by d12

```
visible by d12     P(games)   P(tomato hinge)   tomato d29 med   carrot: P(hinge)  carrot d29 med
0 relevant           31%            4%                $70              0%              $43
1 relevant           42%           61%                $91             16%              $60
2 relevant           21%          100%               $216             68%              $81
3+ relevant           5%          100%               $546+            96%             $187+
```

(relevant = PIZZA_SHOP/FARMERS_MARKET for tomato; PET_CAFE/FARMERS_MARKET for carrot;
BAKERY/BRUNCH_SPOT for egg — egg at 2 visible fires 68% but d29 median only $72, "not worth a
goose").
Per-planting economics (unfertilized/fertilized): WHEAT 4/6 units, CARROT 3/4, TOMATO 4/8.
Measured in the sweep: 28 carrot conversions produced +84.0 sold units/game (3.0/stop) and cost
-70.8 wheat units/game (2.5/stop of wheat actually forgone).

```
one late stop (d12+)         units   $/unit realised/modelled       gross    seed     net
WHEAT (what it does today)     2.5   $45.2 measured (arm 0)          $113     $10    $103
CARROT, agent cadence          3.0   $42.2-42.8 measured             $127     $20    $107
CARROT, held to d29, median    3.0   ~$55 modelled                   $165     $20    $145
CARROT, 2+ relevant shops      3.0   $81-187 modelled                $243+    $20    $223+
TOMATO, held to d29, median    4     ~$80 modelled                   $320     $50    $270
TOMATO, 2+ relevant shops      4     $150-216 modelled               $600+    $50    $550+
```

EGG/goose: cost 300 + coop + place; median realised ~$55-60/egg late season, ~$870/goose net of
the animal in the median game, before op costs; the egg hinge needs TWO egg shops drawn early
(22% of games), and the same wheat scarcity that feeds the hinge thesis is the goose's feed bill.
Expected value of a **gated** tomato play, before cascade costs: ~26% of games x 8 stops x
(~$550 - $103) = **~$900/game mean**, concentrated as ~$3,600 in the fired games — real but
modest, not to be bought unconditionally.
(source: fable_allocation_economics_2026-08-15.md)

### Melon front-load fix, and the corrected release value

`NO_DRAIN_THRESHOLD` front-loads a no-drain product (sell on arrival) rather than trickling.
Test: `tests/test_a_no_drain_product_is_sold_the_day_it_arrives.py`, red before the fix, green
after, red again on revert.
With no opponent melon flow, trickling is harmless (book recovers at 1/day); the race exists
because recorded opponents dump 114-120 melons into the same book.
Corrected release table (seed 11, tape kawashigi):

```
product      produced  we sold  drain   ACTUAL $  OPTIMAL $  left on table
WHEAT             531      471     31     10,367     11,710         +1,343
CARROT             12        6     19        204        404           +200
STRAWBERRY        212      204     31     11,464     12,502         +1,038
MELON             114      114      1     20,285     21,638         +1,353
MILK              177      171     13     12,194     13,163           +969
WOOL              193      176     13     29,273     30,023           +750
TOTAL                                     83,787     89,440         +5,653
```

Melon leaves +$1,353 on the table, not the -$11,929 an earlier broken trickle model printed; the
shipped agent is nearly optimal on melon already.
**`docs/when_and_what_to_sell_2026-08-15.md` §3's +$12,136 "even spread" figure compared against
an infeasible baseline; the real release value for that game is +$5,653.**
No agent code was touched in producing this table — `schedule_agent.py`, `cover.py`, the router
and the schedule are byte-identical to session start, confirmed on a full 30-day grid: ours
$149,207 / tape $150,076 on seed 11.
(source: fable_allocation_economics_2026-08-15.md)

### Unresolved contradiction — flag for an owner

The root-level `RETRACTIONS.md` (outside `docs/`, not edited here) item 7 reports a 960-game
population sweep where the shipped melon-swap rule (`MELON_YIELD_OPPONENT_MELON = 7`) narrowly
**BEAT** turning it off (`= 99`): 68.1% vs 67.9% win rate.
This disagrees with `when_and_what_to_sell_2026-08-15.md`'s model and with
`work_to_be_done_2026-08-16.md` §4's direct A/B (-$17,297/game, 66.7% vs 0%), both of which say
keeping melon beats swapping.
Possible reconciliation: the small-N arms may measure a narrower trigger condition than the
population sweep's blanket rule — not checked.
Flag for an owner.

---

## 4. Saturation and absorption tables

### First local peak, CONTEST = 1.0 (opponent sells as much as we do)

```
  product       base  drain  peak units     $/u   season $  tiles/head
  WHEAT           25    553         276    25.0      6,900         6.6
  CARROT          35    317         156    35.0      5,460         4.0
  TOMATO          60    209         104    60.0      6,240         6.5
  STRAWBERRY     120    452         224   120.0     26,880        18.7
  MELON          250     30          88   179.0     15,748         7.3
  MILK (cow)     160    322         160   160.0     25,600         2.4
  WOOL (sheep)   200    204         112   192.2     21,529         2.3
  EGG (goose)     50    256         128    50.0      6,400         1.2
  FERTILIZER     100      0        4000     4.1     16,250         n/a
```

"First local peak" must be read literally: the global maximum is meaningless once `market_price`
bottoms at the $1 floor, since revenue then rises forever with volume — a first version of this
table searched globally and wrongly reported wheat, carrot, tomato, melon, egg and fertilizer all
"saturating" at 3,000 units.
(source: what_saturates_and_what_does_not_2026-08-09.md)

**Geese are NOT the exception to saturation** — an earlier claim that geese scale without limit
was retracted the same day it was written, from two compounding bugs: `revenue_rate` computed a
herd's output as `events * max_held` (`max_held` caps the unharvested buffer, not the per-event
yield — `kaggriculture.py:813`, so every herd was overstated 4-6x; `kagg/economics/production.py`
already held the true per-head numbers: EGG 26, MILK 11, WOOL 8), and `best_revenue` took the
global (not local) maximum, again running past the price crash.
Corrected, per head:

```
  animal    1      2      4      8     12     16     20     24
  COW      80    160    320    640    960   1164   1164   1164   <- flat from 16
  SHEEP    67    133    267    533    800    897    897    897   <- flat from 16
  GOOSE    50    100    200    246    246    246    246    246   <- flat from 8
```

This **brackets Seb's 9 cows and 11 sheep** rather than contradicting them.
Egg's book is the shallowest in the game (`above_func: log`, `above_target: 0.2` against wool's
`sq` at 3.2), but egg's base ($50) is far below milk's ($160) and wool's ($200): a goose herd
caps at $246/day, a cow herd at $1,164.
The superseded reading, kept because the shape of the error is the point:

```
  animal    1      2      4      6      8     12     16     20  head
  COW     480    960   1164   1164   1164   1164   1164   1164   <- flat from 4
  SHEEP   400    800    897    897    897    897    897    897   <- flat from 4
  GOOSE   200    343    652    955   1257   1845   2424   2998   <- still climbing at 20
```

A goose yields daily from day 4 (`interval` 1, `max_held` 4), so 20 geese make 2,080 eggs a
season, and eggs barely bend against a $50 base even at that volume.
(source: what_saturates_and_what_does_not_2026-08-09.md)

Fertilizer is species-independent and has no drain: `kaggriculture.py:818` sets
`tile["fertilizer_available"] = True` for every animal tile every day, so a $300 goose produces
the same 1 fertilizer/day as a $500 sheep; twenty animals is ~600 units a season, and its drain is
zero — `TOWN_CENTER_PRODUCTS` excludes it and no shop carries it.
(source: what_saturates_and_what_does_not_2026-08-09.md)

A superseded section of the same file initially modelled cow/sheep saturation at 4 head
(contradicting Seb's 9/11) before the `events * max_held` bug was found and fixed; resolved same
day.
Candidate explanations considered and left unmeasured at the time: CARE compounding
(`pending_care_bonus`), continuous small-parcel selling vs. one dump, and the `BUY_PRODUCT`
conversion margin (buy wheat, feed, sell milk) — the one lever `what_the_others_do.py` put us at
only the 49th percentile on.
(source: what_saturates_and_what_does_not_2026-08-09.md)

### Season absorption, both env versions (pre-hinge; 1.32.2 vs 1.32.6)

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

Melon is exact (no shop carries it: town centre only, 719/24 = 30 ticks at multiplier 1); other
rows are indicative (1.32.6 draws shops with replacement; this table used a 1.32.2
without-replacement draw for non-melon rows).
`kagg/search/chains.py`'s `DRAIN_UNITS` still held the 1.32.2 column as of 2026-08-09: against the
ladder it overstated the market 1.13x (carrot) to 4.67x (melon), and the planner believed the
market worth $308,160 against a real $207,180 — though stage 1 did not ship in
`submission/main.py` at that time (`DRAIN_UNITS 0`, `OPPONENT_SHARE 0`, `revenue_rate 0` in the
bundle grep), so this had not yet cost a ladder game.
(source: the_market_2026-08-09.md)

### What the town will actually eat — measured directly off 87 recorded ladder tapes' closing inventory (2026-08-11)

```
| product | shop types carrying it (of 8) | season appetite | closing surplus, 87 tapes |
|---|---|---|---|
| WHEAT | 5 | 745 – 1,282 | -386 to -1,356 |
| CARROT | 2 (PET_CAFE single-product, counts double) | 29 – 924 | -12 to -1,002 |
| TOMATO | 2 | 208 – 924 | -30 to -678 |
| STRAWBERRY | 4 | 387 – 1,282 | -381 to +60 |
| MILK | 3 | 566 – 1,103 | -342 to +77 |
| EGG | 2 | 208 – 566 | -624 to +108 |
| WOOL | 1 (YARN_STORE, single-product, counts double) | 29 – 387 | -424 to +59 |
| MELON | 0 | 29 on every board | +38 to +158, always positive |
| FERTILIZER | 0 | 0 on every board | +201 to +493, always positive |
```

Fertilizer pays well and then permanently stops paying: linear curve, `above_target 0.40`, `T =
200`; every unit sold knocks ~$0.40 off and nothing restores it.

```
units sold | marginal unit | cumulative | average
50 | $90 | $4,755 | $95
100 | $80 | $9,010 | $90
150 | $70 | $12,765 | $85
200 | $60 | $16,020 | $80
250 | $50 | $18,775 | $75
400 | $20 | $24,040 | $60
500 | $1 | $25,052 | $50
```

Every one of the 87 tapes closes with fertilizer between $1 and $20 against base $100 — the book
is saturated at the end of every game ever played there.
Melon: 17 tiles at ~12 units/tile is 204 units into a 29-unit appetite; all 87 tapes close with a
melon surplus (+38 to +158) — every player over-plants melon, winners included, making it a shared
inefficiency, not a losing move, and one that the shop draw cannot inform (`SHOP_ADAPT_CROPS`
deliberately excludes melon from swap pairs).
Wheat's closing surplus is negative in all 87 tapes by 386-1,356 units — price *rises*, closing at
$40-$59 against base $25; wheat is carried by five of eight shop types.
The measured wheat yield is 28/tile unfertilized, 42 fertilized (`kagg/economics/production.py`),
against a shipped comment calling wheat "a bad trade" on the grounds of a 6-unit tile yield.
(source: what_the_town_will_actually_eat.md)

### Market depth and the two 2026-08-13 losses

Both losses are near-mirrors decided in the last third of the season: we ship volume into
products the town does not drain and under-ship the one it does.
`92550780` — lost $69,881 to $77,275 (-$7,394): town drew YARN_STORE three times and PET_CAFE
twice (wanted 1,074 wool, 716 carrot over the season):

```
WOOL   closed $252  of base $200   drained 1,074   <-- ABOVE base all season
CARROT closed $ 42  of base $ 35   drained   716   <-- ABOVE base all season
MILK   closed $  5  of base $160   drained   358
STRAW  closed $  3  of base $120   drained   179
MELON  closed $ 25  of base $250   drained     0
```

We had 8 sheep to Densike's 4 and shipped a fraction of the wool they did — on the unambiguous
attribution slice, 28 units/$6,738 against 115 units/$28,158 — while putting milk and strawberry
on the floor in a game where the town drained only 358 and 179 of them.
`92562037` — lost $129,161 to $133,724 (-$4,563): a true mirror (~148 wheat, ~13 animals both
sides); the one large divergence is melon, 136 tiles to their 19, closing at $25 of $250 base.
Both losses are lost after day 18:

```
92550780   d18 -$84       d21 -$10,532     d29 -$7,394
92562037   d18 +$6,363    d21 -$1,155      d29 -$4,563   (their last day +$10,469 to our +$4,080)
```

First `SELL CARROT` is step 598 and 617 (day 25) in games where the town was draining carrot from
day 3.
(source: market_depth_and_the_morning_losses_2026-08-13.md)

The melon/strawberry answer is CONDITIONAL: `92562037` (5 strawberry-carrying instances, drained
895, closed $187, above base) says a melon tile converted to strawberry is worth several times
more; `92550780` (1 instance, drained 179, closed $3, floored) says the swap buys nothing, since
that town wanted wool and carrot instead.
The stake is 19 melon tiles against 36 strawberry tiles (corrected from an earlier hundreds-count
misreading BUY_SEED order quantities as plants — see the correction below).
`scripts/product_search.py`'s global sweep over `melon_day`/`melon_shift` averages both regimes
and reports a wash, which is the expected result of asking a global question about a conditional
quantity — the same trap that would have hidden `WOOL_SHOP_SETS_THE_HERD`.
(source: market_depth_and_the_morning_losses_2026-08-13.md)

**Correction, same day**: an earlier version read melon and carrot counts off `why_we_lost.py`'s
"crops planted (offers)" column, which is BUY_SEED order quantities re-posted every turn, not real
plants (Alex: "we have a carrot plant of 6 i dont understand how we planted 42").
Real plants, counted off tile transitions, are the same in every game: **WHEAT 138, STRAWBERRY
36, MELON 19, CARROT 6.**
The claim "we planted 136 melon to their 19" was an artifact — both sides plant 19.

```
game       MELON plants   MELON closed   EGG drained   EGG closed   geese   CARROT plants
92550780        19            $25            179          $59          0          6
92562037        19            $25            537          $67          0          6
92564858        18            $19            537          $70          0          5
92565805        19            $16            537          $70          0          6
92566708        19            $10          1,074          $88          0          6
```

Melon closed between $10 and $25 of a $250 base in every game (no shop, town absorbs 30/season, 19
plants a side already buries it).
Carrot: 6 tiles ≈ 24 units against towns draining 716, 895, 716 — closed above base every time it
was drawn, and it has the deepest glut tolerance of any crop (842 units to floor).
EGG closed above base in all five games, $59-$88, town draining up to 1,074, with zero geese run
in all five (EGG was unsellable when the goose flag was measured).
The forum claim "multiply base by shop count" is half right: shop count sets the sustainable
*rate*, not the price — milk with three shops still floors after 76 units of excess, which is why
our own milk repeatedly closed at $1-$5 despite the claim saying it "sells above 160 most of the
season."
(source: market_depth_and_the_morning_losses_2026-08-13.md)

Bare pastures and starved animals, same file: two consecutive unfed days and the animal escapes
(`kaggriculture.py:804`).
`92550780`: final herd COW 6 SHEEP 8, 1 bare structure, 0 escapes.
`92562037`: final herd COW 9 SHEEP 4, 2 bare structures, 1 escape (COW, day 24, -$400).
`92548920`: final herd COW 6 SHEEP 8, 1 bare structure, 0 escapes.
In `92550780`, `WOOL_SHOP_SETS_THE_HERD` correctly held cows at cap 6 on a three-YARN_STORE board,
but `_herd_split` is forbidden from growing `want_total` beyond the schedule's own count, so the
rule's own reference table (COW 6, SHEEP 12, total 18) landed as COW 6, SHEEP 8, total 14 — four
animals short — because the early return skips the drain-aware greedy branch below it.
`92566708` — worst of five, lost $56,006 to $109,034: twelve of fourteen animals escaped days
10-13 ($5,200 of stock plus every remaining unit of milk/wool for 17 days); the shed held zero
wheat from day 8 through day 12 while the bank sat at $1, $75, $22 — a liquidity failure
converting directly into destroyed capital.
(source: market_depth_and_the_morning_losses_2026-08-13.md)

### The book is shallow, and production ignores it (2026-08-09)

**Correction carried in the source file itself**: every absorption figure was originally measured
PASS-vs-PASS and described as "a property of the board with no agent involved" — wrong, because
`_spawn_weeds` draws from the same per-day rng before the shop unlock
(`reference/kaggriculture.py:856-878`), and weed spawning depends on which tiles are empty, so how
the agents play shifts the shop stream:

```
seed 13  PASS: YARN, BAKERY, PIZZA, YARN, ICE_CREAM, FARMERS, PIZZA, BRUNCH
         REAL: SMOOTHIE, ICE_CREAM, YARN, ICE_CREAM, FARMERS, YARN, YARN, ICE_CREAM
seed 29  PASS: PET_CAFE, FARMERS, BRUNCH, ICE_CREAM, BAKERY, BAKERY, BRUNCH, BRUNCH
         REAL: BRUNCH, FARMERS, ICE_CREAM, YARN_STORE, PET_CAFE, PET_CAFE, BAKERY, BAKERY
```

So seed 29 is NOT wool-starved under real play — it draws a YARN_STORE — and the "WOOL starved on
5 of 12 boards" claim described boards the agent never sees.
The 34% figure for P(no YARN_STORE) survives, since it comes from a uniform 8-shop draw with
replacement, which gameplay does not change.
What survives untouched: the price-curve table (verified against `kg.market_price` by
`tests/test_the_price_curve_math.py`), realised-price and two-way results (measured under real
play), the shop-count table, and the fact MELON is carried by no shop on any board.
What needed redoing: absorption per board.
(source: the_book_is_shallow_2026-08-09.md)

The claim that started the file — high-value produce sitting in workers' hands at dusk rather
than the shed (443 such units on seed 13, read as a delivery bug) — was also false.
Counting actual fills with `kagg/analysis/fills.py`:

```
seed | MILK made/sold | WOOL made/sold | MELON made/sold | STRAWBERRY made/sold | left in shed | left in hands
13 | 228 / 249 | 165 / 169 | 84 / 84 | 278 / 294 | 0 | 0
17 | 264 / 278 | 161 / 163 | 78 / 78 | 280 / 293 | 0 | 0
29 | 204 / 217 | 161 / 161 | 84 / 84 | 287 / 313 | 0 | 0
41 | 242 / 251 | 152 / 155 | 84 / 78 | 272 / 284 | 0 | 0
```

100-109% of everything produced is sold, nothing is left at season end; the shed is at capacity 2-6
hours out of 720; there is no delivery, discard, or shed-capacity problem.
Two measurement errors caused the false reading: comparing a raw count across agents with
different herd sizes (scale-free version is `hi_held / (hi_held + hi_shed)`), and sampling at
dusk, which is the flow's maximum numerator and minimum denominator by construction.
A third, smaller error: a hand-turn census reported "idle 0.0%" because the environment's idle op
is named `PASS`, not `IDLE`; the real split is 24% idle, 42% walking, ~34% working.
(source: the_book_is_shallow_2026-08-09.md)

Revenue per unit, same seasons:

```
seed | MILK $/unit | WOOL $/unit | final bank
13 | 252.66 | 229.23 | 163,036
17 | 111.51 | 236.51 | 126,151
29 | 27.90 | 219.29 | 77,254
41 | 197.71 | 39.65 | 100,464
```

Seed 29 sold *more* milk than seed 13 and banked $6,054 for it against $62,913 — same agent, same
code, same schedule, same opponent tape.
Two-way design, 6 tape opponents x 6 seeds, 36 seasons:

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
Mechanism, per opponent:

```
opponent | milk they sold | wool they sold | our milk $ | our wool $
HealthStone | 201 | 93 | 103.20 | 120.79
Mohamed | 213 | 148 | 172.78 | 40.85
Phi | 213 | 148 | 179.03 | 41.01
Seb | 176 | 58 | 157.32 | 115.69
```

WOOL is sold by one shop of eight, so its demand is thin on every board; MILK is in three of
eight, so the draw moves demand more than the opponent does.
The same agent banked between $16,888 and $163,036 across these 36 seasons with no code change —
a single-seed, single-opponent comparison is noise.
(source: the_book_is_shallow_2026-08-09.md)

What the seed controls: `rng = random.Random((seed * 1_000_003) ^ day)`, then `_spawn_weeds` and
the shop draw (`town["unlocked_shops"].append(rng.choice(sorted(SHOPS)))`) — drawn with
replacement, one every 3 days, max 8 instances.

```
product | shops selling it | P(never drawn in 8)
WHEAT | 5 of 8 | 0.2%
STRAWBERRY | 4 of 8 | 2.3%
MILK | 3 of 8 | 2.3%
WOOL | 1 of 8 | 34.4%
MELON | 0 of 8 | always
```

The numeric seed itself is deliberately hidden from agent observations (`reference/
kaggriculture.json`), but `town["unlocked_shops"]` is `shared: True` and fully observable every
turn — the cause is hidden, the part that matters is not.
The sell side already uses this (`town_drain_remaining`, `reservation_units`,
`PRICE_AWARE_SELL_CAP`/`RESERVATION_SELL_CAP`/`HOLD_A_FLOORED_BOOK` all ship ON); the production
side ignores the draw completely — the schedule commits to a fixed cow/sheep/crop target sheet
decided before the board is known.
Open, separate from the price question: animal loss — shipped loses 1 animal on seed 13, `1455`
loses 4, the `1455m` graft 8-11; `consecutive_unfed >= 2` deletes an animal irreversibly
(`kaggriculture.py:786`), and a late loss barely dents final bank while destroying an asset that
would have paid out every remaining day.
(source: the_book_is_shallow_2026-08-09.md)

---

## 5. Carrot / tomato / egg economics

### Carrot swap, measured on Victor's tape (2026-08-12) — SUPERSEDED

> This file carries a SUPERSEDED banner: superseded by `carrot_and_the_empty_book_2026-08-19.md`,
> the clean measurement its own retraction calls for.
> `CARROT_SWAP` no longer exists in the code (checked 2026-08-15).
> Kept for the method lesson (winner's curse, tape-instrument noise floor); its own retractions,
> below, are already in force.

The file carries two of its own retractions, both dated after the original write-up.
**First retraction (2026-08-12, same day)**: every arm in the file is invalid, because the
schedule's `sells` rows never mention CARROT, so nothing ever sold any carrot grown — measured
directly, 2 carrot tiles put 6 units (seed 13) and 3 units (seed 14) into the shed and 0 out of
it, all season.
Every arm therefore paid the $20 seed and banked nothing, a loss by construction on any crop.
A second, independent defect: carrot is `max_yield_day 3` against wheat's `4`, and the schedule's
harvest cadence is built for wheat, so the carrot tile is visited a day late and misses its own
yield too.
"Carrot is UNTESTED, not disproven" — a real test needs CARROT in the sells row and a harvest on
carrot's own clock.
(source: carrot_swap_2026-08-12.md)

**Second retraction (2026-08-13), "the frame was also wrong"**: every arm in the file is a SWAP
(`PLANT WHEAT -> PLANT CARROT`), replacing a crop that pays more with one that pays less at base
prices ($140/tile wheat vs $120/tile carrot) — a question with a correct "no" answer that is not
the question the leader is actually answering.
カワシギ (#1, 15-1 over 16 games) buys 8 carrot seeds on d3/d6 in all 16 games and then plants NO
carrot until d21, then plants carrot on otherwise-finished ground from d21-d26 in every game:

```
2407  d22:4 d25:4        0434  d21:3 d22:1 d25:1 d26:2
8461  d21:2 d22:1 d24:3 d25:1    8144  d21:2 d22:2 d24:2 d25:2
2932  d21:2 d22:2 d24:2 d25:1 d26:1   6371  d21:1 d22:1 d24:1 d25:1 d26:1
```

Carrot (`first_yield_day 2, max_yield_day 3`) finishes a d26 sowing; wheat (`2, 4`) would finish
d31, past the season.
**Carrot is not a competitor to wheat — it is the crop for the window in which wheat is
unplantable, additive on dead tiles, never a substitution.**
The fixture forced the wrong frame: a baked tape's sell rows, harvest cadence and seed purchases
are all fixed to wheat's clock, so the only carrot experiment such a fixture can express is
"rewrite some wheat tokens as carrot tokens," which cannot express planting into empty late tiles
(an addition, and a tape has no free slots to add to).
(source: carrot_swap_2026-08-12.md)

Original measurement (before either retraction), kept for the method lesson: rewriting
`PLANT WHEAT -> PLANT CARROT` for day >= D on Victor's tape, mirroring every `SELL WHEAT q` with
`SELL CARROT q`.
Control arm (D=99, nothing swapped) reproduces the tape at $101,917 mean over seeds 11-14.

```
D  plants  seeds  starved   mean bank  weeds     delta
99       0      0       11     101,917    1.5        +0
26      11      2       11     100,900    1.5    -1,017
23      55     34       11      93,472   29.2    -8,446
20      81     89       18      83,835   44.2   -18,082
16      97    105       33      77,726   45.2   -24,191
10     114    123       37      59,262   45.2   -42,656
 6     127    136       47      43,522   45.2   -58,395
 0     139    148       73      26,498   45.2   -75,419
```

Weeds go 1.5 -> 45 because wheat's harvest/water cadence is baked into the tape and a carrot tile
(shorter lifecycle) rots before it is reached, plus a seed-matching shortfall at the boundary.
Neutralising the lifecycle (giving CARROT wheat's yield days) held weeds flat but did **not**
recover the money (D=20: -$18,135 against -$18,082 unneutralised) — the dead tiles were never what
cost the money.
D=20 is the clean arm: 81 tiles swapped, weeds flat, starvation +7/299 FEEDs, **-$224/tile**.
Sixteen towns tested at D=20: the trend runs the hypothesized direction (more carrot-shop drain =
smaller loss) and never crosses zero — the best of sixteen still loses $9,196 (seed 18, PET_CAFE
x3).
The hole is five times the base-price yield-table gap ($20/tile = $1,620 over 81 tiles measured;
actual best case -$9,196) because **wheat is also the feed supply**: growing it holds its own
price down and feeds the herd; swapping it out raises the feed bill at the same time crop revenue
falls (isolation of the two effects not run).
A tiny genuine sweet spot exists at D=20, N=2-4, worth ~$300/game, found by pairing swapped
plants to specific unclaimed wheat-seed units so starvation cannot contaminate the read
(earlier tiles are the herd's feed — swapping the first 2 wheat tiles cost $26,405 and drove
starvation 11->34).
But at a FIXED setting across sixteen towns it loses (fixed N=1: -$486; fixed N=2: -$573;
per-seed argmax over 7 arms: +$284, flagged explicitly as winner's curse, not a result — 10/16
positive but the argmax does not track the town's carrot drain and cannot be predicted in
advance).
Generalizing to the pocket-value question across products, town seed 18 (most carrot-favourable
of sixteen):

```
product       drain   pocket$    p1   base   half@   glut     yield/op  seed$  fyd
STRAWBERRY      300    29,172   265    120     226   linear          4    100   10
MILK            210    17,696   286    160     157   linear          -      -    -
WHEAT           696    12,246    51     25     514   log             6     10    2
EGG             516     8,035    81     50     259   log             -      -    -
CARROT          570     3,502    42     35     550   sqrt            4     20    2
TOMATO           84       428    70     60      39   sqrt            4     50    8
```

Carrot drains 570 units and the price only reaches $42 (log/0.20 curve, the flattest of any crop);
wheat is the inverse and the best book in the game to dump into (log/0.20 on the glut side, still
above base after 500+ units).
The pocket ceiling ($3,502 on the best of sixteen towns, $91 on the worst) is planner-independent.
**The deciding measurement — our agent, the real pool, win rate**: seeds 1300-1303, 24 recorded
ladder opponents, both seatings, 192 games/arm:

```
seeds 1300-1303, 24 recorded ladder opponents, both seatings, 192 games per arm
   value  games     win   mean ours  mean theirs  mean margin
       0    192  65.1%     130,168      109,698       20,470
       1    192  54.7%     124,304      111,341       12,963

seeds 1306-1309 (chosen because the flag fires on 3 of 4), 192 games per arm
       0    192  67.2%     131,387      108,988       22,399
       1    192  59.4%     127,108      109,569       17,539
```

-10.4 and -7.8 points, two independent seed sets, 384 games, degrading in every named opponent and
improving in none. **`CARROT_SWAP = False` stayed False.**
A small, count-based version (`CARROT_TILES = 4` from day 20, on otherwise-idle ground) was also
tested and was also a null: seeds 1300-1303 +1.6pp, seeds 1306-1309 -3.7pp, mean over 768 games
-1.1pp; the flag was deleted, not left at 0.
Three things the tape work got wrong, recorded because the sequence is the lesson: "net negative
at any fixed setting" was computed on arms silently killing a sheep (a swapped wheat tile starves
the herd's SELL-sized shed); the sweet-spot numbers were per-seed argmaxes, winner's curse exactly
as `CLAUDE.md` warns; and the reserve fix that "cured" starvation made the instrument unusable
(the tape has a ±$40k noise floor on a ±$400 signal, because suppressing a sell order realigns
every order slot after it).
(source: carrot_swap_2026-08-12.md)

### Carrot and the empty book (2026-08-19) — the clean measurement, supersedes carrot_swap

**Verdict: no general increase.**
Carrot's book is not empty (94% of strong players already sell some), and on a season-long,
tile-for-tile basis WHEAT nets more per tile-day and per action than CARROT, because carrot's seed
costs twice as much for similar raw yield.
The one thing worth doing (and that top players already do): plant carrot as an
**end-of-season closer** on tiles a longer crop cannot finish, and lean into it only when
`town.unlocked_shops` has drawn PET_CAFE or FARMERS_MARKET.
(source: carrot_and_the_empty_book_2026-08-19.md)

A correction to the task's own premise: game `ladder_2026-08-17b/94282682.json` was cited as
CARROT rising while STRAWBERRY also floored to $1; replayed directly, STRAWBERRY closed at $219
(up from $120), not $1 — only MILK floored; STRAWBERRY, not CARROT, was the big winner (287 units,
$65,059 revenue).
Method: both seats' recorded actions replayed verbatim through a fresh env with `record_fills()`,
using the game's own recorded shop draw, reproducing exact fills (not offers).
Corpora: `leaders_2026-08-19` (60 games/120 seats, unbiased, winner bank >= $110k),
`ladder_2026-08-17b` (43 games/86 seats, our selected losses, behavior-only, never win rate),
`kawashigi/*.json` (19 of 20 files), `downloads_2026-08-13/91907974.json` (1 tape).
(source: carrot_and_the_empty_book_2026-08-19.md)

Is the carrot book empty? No — CARROT is the second-most universally sold crop after
WHEAT/STRAWBERRY/MELON/MILK/WOOL/FERTILIZER (all sold by every seat):

```
product | seats selling (n=120) | % seats | total units | median units/seller
WHEAT | 120 | 100.0% | 84,396 | 601
CARROT | 113 | 94.2% | 1,476 | 15
STRAWBERRY | 120 | 100.0% | 29,797 | 246
MELON | 120 | 100.0% | 12,364 | 120
MILK | 120 | 100.0% | 28,800 | 259
WOOL | 120 | 100.0% | 17,935 | 120
FERTILIZER | 120 | 100.0% | 29,283 | 242
TOMATO | 0 | 0.0% | 0 | —
EGG | 0 | 0.0% | 0 | —
```

TOMATO and EGG are the genuinely empty books — literally zero seats sold either, zero board tiles
showed TOMATO at d10/d20/d28 across all 120 seats.
Carrot sellers cluster tightly: units-sold-per-seller quartiles 10/15/15, max 88 — everybody who
touches carrot does roughly the same small amount, the signature of a garnish crop.
(source: carrot_and_the_empty_book_2026-08-19.md)

Median dawn-open vs close, 60 games:

```
product | median open | median close | close/open | n games
WHEAT | 25 | 48 | 1.92x | 60
STRAWBERRY | 120 | 171 | 1.43x | 60
TOMATO | 60 | 80 | 1.32x | 60
CARROT | 35 | 46 | 1.31x | 60
EGG | 50 | 58 | 1.16x | 60
WOOL | 200 | 156 | 0.78x | 60
MILK | 160 | 117 | 0.73x | 60
MELON | 250 | 31 | 0.12x | 60
FERTILIZER | 100 | 7 | 0.07x | 60
```

Carrot is the fourth-biggest appreciator, behind wheat, strawberry and tomato (the last on zero
sellers, pure shop-drain).
What actually drives the CARROT close is the number of PET_CAFE/FARMERS_MARKET instances drawn:

```
carrot-shop instances (PET_CAFE + FARMERS_MARKET) | n games | closing price range
0 | 8 | 33-37
1 | 30 | 38-55
2 | 10 | 47-61
3 | 10 | 56-69
4 | 1 | 65
```

Correlation (shop instances vs closing price): **r = 0.90**.
Correlation (total units sold vs closing price): **r = 0.42**, positive — more selling goes with a
higher close, because both are driven by the same demand draw; this flatly contradicts a
"sellers are scarce so price runs" story.
No shop is required to *sell* carrot (`_process_market` quotes/fills any product regardless of
`unlocked_shops`); a shop only gates *demand*.
(source: carrot_and_the_empty_book_2026-08-19.md)

```
shop | products | n games it ever unlocked (of 60) | median first day
ICE_CREAM_SHOP | STRAWBERRY, MILK, WHEAT | 54 | 6
SMOOTHIE_SHOP | STRAWBERRY, MILK | 49 | 6
YARN_STORE | WOOL | 42 | 9
BRUNCH_SPOT | EGG, WHEAT, STRAWBERRY | 41 | 12
FARMERS_MARKET | WHEAT, CARROT, TOMATO, STRAWBERRY | 37 | 12
PIZZA_SHOP | MILK, TOMATO, WHEAT | 34 | 12
BAKERY | EGG, WHEAT | 30 | 16.5
PET_CAFE | CARROT | 26 | 16.5
```

PET_CAFE is carrot's only dedicated shop and both the rarest (26/60) and latest (median day 16.5)
to unlock; FARMERS_MARKET is a second, earlier route (median day 12, 37/60) but shares the
instance with WHEAT/TOMATO/STRAWBERRY draw-down.
Carrot demand is gated by luck of the draw, tending to land in the second half of the season if at
all (8/60 games never drew either shop).
(source: carrot_and_the_empty_book_2026-08-19.md)

Per-cycle mechanics, confirmed against `reference/kaggriculture.py` and matching
`kagg/economics/production.py`'s constants exactly:

```
| | WHEAT | CARROT |
| seed cost | $10 | $20 |
| cycle length (plant to harvest) | 4 days | 3 days |
| units/cycle, unfertilized | 4 | 3 |
| units/cycle, fertilized | up to 6 | up to 4 |
| plantings/season (measured, 30-day) | 8 | 11 |
| season yield/tile, unfertilized (measured) | 28 | 29 |
| season yield/tile, fertilized (measured) | 42 | 39 |
```

Raw season yield/tile is nearly identical (28 vs 29), but CARROT needs 38% more plant/harvest
cycles (11 vs 8) and costs 2x per planting.
Using median season-average dawn price (WHEAT $39.1, CARROT $38.4):

```
| | WHEAT | CARROT |
| season revenue/tile (unfertilized) | $1,094.80 | $1,113.60 |
| less season seed cost | -$80 (8x$10) | -$220 (11x$20) |
| net/tile, season | $1,014.80 | $893.60 |
| net revenue per tile-day (÷30) | $33.83 | $29.79 |
| unit-actions/season (plant+harvest+water, no travel) | ~40 | ~44 |
| net revenue per unit-action | $25.37 | $20.31 |
```

WHEAT nets ~13-25% more per tile-day and per action than CARROT run as a season-long staple.
Fertilizer widens this gap: fertilized WHEAT nets $52.06/tile-day vs CARROT's $42.59/tile-day
(+22% edge instead of +14%).
Travel cost is not modeled and would very likely favour CARROT even less (more plantings/season =
more trips).
The one real edge CARROT has: it fits a shorter window — a tile freed on day 27 can still finish
one carrot cycle (day 30) but not a wheat cycle (day 31, past season end).
(source: carrot_and_the_empty_book_2026-08-19.md)

Board crop-tile counts, summed across all 120 leader-seats:

```
day | CARROT tiles (sum) | seats with any CARROT | WHEAT (sum) | STRAWBERRY (sum) | MELON (sum)
10 | 4 | 4/120 | 676 | 1,587 | 1,971
20 | 0 | 0/120 | 2,993 | 4,033 | 91
28 | 198 | 113/120 | 4,258 | 1,889 | 0
```

Nobody runs a carrot-heavy board mid-season; at day 20 not a single one of 120 seats has a live
CARROT tile; by day 28, 113/120 have picked some up — an end-of-season "plant something rather
than leave idle" move, done almost universally, at small scale.
One outlier: game `93804040`, seat 0 (Thomas Tschinkel, winner, $110,194 vs opponent's $103,173)
ran 35 CARROT tiles by day 28, the only genuinely carrot-heavy board in the sample; that game drew
3 carrot-shop instances, CARROT closed at $75 (second-highest in sample), he sold 88 CARROT units
for $6,264 (opponent sold 15 for $1,033, a $5,231 swing against a $7,021 final margin) — but CARROT
was still only 5.7% of his total sold revenue ($6,264 of $110,194); STRAWBERRY ($42,732) and MILK
($54,015) did the heavy lifting.
(source: carrot_and_the_empty_book_2026-08-19.md)

Verdict, in full: do not blanket-increase carrot tile allocation.
Keep, and make more systematic, the end-of-season closer (any tile freeing with 3-4 days left that
cannot finish a wheat/melon cycle should get carrot rather than sit idle); scale carrot
specifically when PET_CAFE or FARMERS_MARKET is drawn (r=0.90 with closing price); do not treat
game 94282682 as the general case.
What would falsify this: routing/travel cost priced in and found to favour carrot's shorter cycle
materially more than assumed here (untested); a larger, fresher sample weakening the shop-instance
correlation; longer games simply drawing more shop instances and scoring higher for unrelated
reasons (a confound not controlled here).
(source: carrot_and_the_empty_book_2026-08-19.md)

### Allocation economics conflict with the above — see §3

`fable_allocation_economics_2026-08-15.md`'s conditional-gate numbers (§3 above) and
`carrot_and_the_empty_book_2026-08-19.md`'s "no general increase, closer-only" verdict are
consistent in direction (both reject an unconditional carrot increase, both point at a gated,
shop-draw-conditional play) but were derived independently on different corpora
(model/Monte-Carlo vs 120-seat replay) and are not cross-referenced in either source file.
No contradiction found between them, but flagged here as not yet reconciled into one number.

---

## 6. When and what to sell — STALE

> **STALE, flagged 2026-08-22 (banner as it appears in the source file).**
> Two claims in this file are contradicted elsewhere and were never corrected in place.
> §"the deciding number" total `152,792 -> 164,928 (+12,136)` compares against an infeasible
> baseline; `docs/fable_allocation_economics_2026-08-15.md` gives the real release value as
> **+$5,653** (see §3 above).
> The falsifiable prediction at the end (`MELON_YIELD_OPPONENT_MELON = 99` beats the shipped `= 7`)
> was tested on 960 games and falsified — the shipped rule narrowly won, 68.1% vs 67.9% (root
> `RETRACTIONS.md`, item 7 — see the unresolved-contradiction callout in §3 above).
> Read the mechanics sections (market-impact curves) as reference; do not quote the total or the
> prediction from this file.

Written 2026-08-15, a model, not a measured result.
Mechanics: selling pushes the book above `I0` (`price(I0+x) = base - (above_target*base/
shape_above(T)) * shape_above(x)`), so the `above_func`/`above_target` pair governs price impact
after a sale.
The full price-curve and town-drain tables from this file are reproduced in §1 above (they are
unaffected by the STALE banner).
Supply against absorption, the shipped plan's season sell totals:

```
product      plan sells  drain/day  days to absorb  verdict
FERTILIZER         1487          0               -  NOTHING DRAINS IT
WHEAT               868         31            28.0  tight
MILK                279         19            14.7  ok
STRAWBERRY          223         25             8.9  ok
WOOL                120         13             9.2  ok
MELON                120          1           120.0  4x OVER THE SEASON
CARROT               20         19             1.1  ok
```

Melon at 4x season absorption and fertilizer (nothing ever removes it) are the two lines that
break the budget.
(source: when_and_what_to_sell_2026-08-15.md, STALE)

**The "spreading is worth $12,136" total is the STALE figure — see the +$5,653 correction in §3.**
Reproduced here for completeness, with the correction attached:

```
product      units    plan $    even $     delta   $/unit plan   even
MELON          120    24,968    26,763    +1,795           208    223
MILK           279    38,146    42,219    +4,073           137    151
WOOL           120    23,886    23,970       +84           199    200
STRAWBERRY     223    20,810    25,331    +4,521            93    114
WHEAT          868    18,272    19,906    +1,634            21     23
FERTILIZER    1487    26,039    26,039        +0            18     18
CARROT          20       671       700       +29            34     35
TOTAL                152,792   164,928   +12,136  <-- STALE, see fable_allocation_economics_2026-08-15.md: real value +$5,653
```

The melon branch section modelled `MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`
(`MELON_YIELD_OPPONENT_MELON = 7`, fires ~68% of games) against a shared-book simulation:

```
case                                          melon $   straw $   OUR TOTAL
A  keep melon   | opponent sells NO melon      24,968     9,909     34,877
B  keep melon   | opponent sells the SAME 120  13,549     9,909     23,458
C  swap→straw   | opponent sells NO melon           0    15,296     15,296
D  swap→straw   | opponent sells the SAME 120       0    15,296     15,296
```

Even in the melon-heavy case the rule exists for, keeping melon beat swapping by $8,162 in this
model, because strawberry is already near-saturated (223 units into a 25/day drain) while
contested melon still paid $113/unit against strawberry's crushed $45/unit.
**The falsifiable prediction this section staked itself on — `MELON_YIELD_OPPONENT_MELON = 99`
should beat `= 7` on 960 games — was tested and falsified; see the STALE banner above and the
unresolved-contradiction callout in §3.**
The policy this file recommended: classify by drain not price (WHEAT/EGG/CARROT robust, timing
worth little; STRAWBERRY/MILK/WOOL/MELON drain-limited, timing worth thousands); target the live
shop draw for drain-limited products via `town_drain_remaining`, not `rate[prod]` (a fact about
his production, not the market); front-load only where the book is a genuine race (melon); never
let a fragile product accumulate (milk hits -10% after eight units).
(source: when_and_what_to_sell_2026-08-15.md, STALE)

---

## 7. The `LATE_SELL_BIAS` / `CAP_SELL_OFFER_SIZE` investigation — CONTAMINATED, per a later file

`fable_market_shape_2026-08-09.md` reported that `LATE_SELL_BIAS` (bias sells to hour 16-23) is "a
real, substantial win": pool win rate 14.6% -> 27.1% (+12.5pp), mean money $16,146 -> $24,535
(+$8,389), positive-or-flat on every opponent.
`CAP_SELL_OFFER_SIZE`'s A/B (offer cap 30) came back byte-identical OFF vs ON and was verified,
not assumed, to be a genuine null on the seeds tried (the flag works — verified directly: seed 2
vs `contrarian`, OFF emits `SELL WHEAT 43`, ON caps to exactly 30, money $10,268 -> $10,265 — the
8 held-out seeds simply never trigger the cap against any of the 3 pool opponents; max offer there
stays <=23).
The file also traced fills directly: Seb's realised price ($141.35/unit) was far above both our
own ($93.14/unit, the loss traced) and the opponent who beat us ($85.84/unit), but the mechanism
tested (small/late/deliberate orders beat large/early/standing ones) did not survive the opponent
row — the opponent's own single-product orders were BIGGER than Seb's (mean 7.8 vs 4.0, max 31 vs
16) yet realised a lower price than Seb; what separated the three was **product mix sold**, not
order shape (we sold 85% of covered units in WHEAT/FERTILIZER under $75; the opponent sold 70% in
STRAWBERRY at $161, moving that volume without collapsing price).
(source: fable_market_shape_2026-08-09.md)

**`arena_state_leak_2026-08-09.md` (dated the same day) subsequently found this entire A/B
contaminated, and flags it explicitly for re-reading.**
`run_arena` was driving one agent *object* through every match, so a finished season carried state
into the next match and killed the agent outright — every contaminated number understates us,
never overstates.
Re-running §4's exact configuration (seeds 20-27, both seatings, heuristic/rancher/contrarian,
`LATE_SELL_BIAS` at its default False) both ways:

```
arm       opponent          mean $   win rate
shared    heuristic         4,534       6.2%
shared    rancher           6,001       6.2%
shared    contrarian        6,788       6.2%
shared    POOL              5,774       6.2%

fresh     heuristic        97,101     100.0%
fresh     rancher         102,850     100.0%
fresh     contrarian      108,707     100.0%
fresh     POOL            102,886     100.0%
```

`shared` reproduces the pre-fix `run_arena` (one `make_agent` object driven through all 16
matches per opponent); `fresh` builds one agent per match, seat-corrected — what
`scripts/confirm_late_sell_bias.py` already does.
$5,774 against $102,886, 6.2% against 100% — a 17.8x gap on money.
`fable_market_shape_2026-08-09.md`'s published $16,146/14.6% (and $24,535/27.1% with
`LATE_SELL_BIAS` on) sit between the two arms above, and **this does not reproduce Fable's exact
figures — the point is that both were measured on games our agent mostly did not play, not that
the direction of `LATE_SELL_BIAS` is refuted.**
The shipped artifact itself was never on the contaminated path: `scripts/gate_pool.py` builds the
candidate inside the job and was re-measured clean at win 94.4% (draw 0.0%), mean $108,180 against
the 9-member `COMPETITIVE` pool, seeds 700-705, both seatings, 108 games —

```
opponent          win       ours
mirror           50%     59,271
wheat_only      100%    137,876
melon_heavy     100%    111,038
strawberry      100%     86,213
cow_heavy       100%    102,514
carrot_25       100%    118,715
small_farm      100%    124,491
straw_small     100%    123,299
contrarian      100%    110,199
```

`fable_market_shape_2026-08-09.md` §4.1's own resolution of "94.4% vs 14.6%" (different-era,
different-pool-composition, not a valid before/after) is **partly right and misses the larger
term**: the 14.6% figure came off a harness that killed the agent in 15 of every 16 games.
**Net: `LATE_SELL_BIAS`'s direction may still hold (per-fills, product-mix evidence is
independent of the state-leak bug), but its measured magnitudes (14.6% -> 27.1%, $16,146 ->
$24,535) are not trustworthy as stated and need a re-run on the fixed harness.**
Not re-run within either source file; flagged as open.
(source: arena_state_leak_2026-08-09.md, correcting fable_market_shape_2026-08-09.md)

---

## 8. Crop-mix and route scoring

### The greedy is a mix scorer, and stage 1 becomes searchable (2026-08-19)

Turning off every solved route from d12 onward costs ~4% flat on three-quadrant arms and *gains*
money on one four-quadrant arm:

```
arm        solved routes   greedy from d12    delta      mix change
straw_q3      160,183         154,277        -5,906      wheat 120 -> 123, rest identical
melon_q3      145,068         137,529        -7,539      wheat 135 -> 134, rest identical
q4_melon       93,929          81,834       -12,095      wheat 133 -> 130, rest identical
q4_straw       78,305          79,527        +1,222      wheat 128 -> 127, rest identical
```

The mix is preserved (herd identical, crop counts move by at most 3 wheat tiles); a season takes
8-25 seconds against ~2 hours for the solve it replaces, which makes the greedy usable as a
stage-1 mix RANKER (not a substitute for the final number).
The q4 tables were actively harmful: `q4_straw` banks *more* with no routes than with its solved
table, because those two tables were never re-solved during the day's mix work and
`q4_branch.install` runs them through d29 (resets `cover.UNSOLVE_DAYS` to `()`); until re-solved
"no q4 experiment measures the idea being tested — it measures the table."
A comparison harness (`scripts/q4_vs_q3.py`) patched wrong returned delta exactly +$0 on all 12
seeds — an implausible PERFECT null, as suspect as a $10,000 swing; the harness was not applying
the q4 plan at all, so q4 remained untested at that point.
(source: the_greedy_is_a_mix_scorer_2026-08-19.md)

Hires are NOT being lost (corrected): measured per day on both q3 arms, `_fit_slots` defers ~32
hires/season but every one is re-issued and lands (straw_q3: row 277, landed 277, short +0 every
day, slotcut 32; melon_q3: row 277, landed 277, short +0 every day, slotcut 33) — we hire 11
because the schedule row says 11 and we get all 11, costing ~$4,000 across d8-d27 via `mult *
fib(n)` against a leader's 6.
Schedule counts are not carried to the router: pins hold only PLANT and BUILD, not harvest;
`_live_ops` re-derives work from the live cell every stop, so "harvest 0/10" on a day the crop
was not yet ripe is not a planner failure.
Ten flags and five orphaned constants were deleted in a worktree and checked byte-identical on all
four arms (straw_q3 $160,183, melon_q3 $145,068, q4_melon $93,929, q4_straw $78,305, all matching
baseline).
(source: the_greedy_is_a_mix_scorer_2026-08-19.md)

A grid-counting correction: "BUILD 0/15", "PLACE 29/15" and "BUY_ANIMAL 10/15" were all instrument
bugs (the env has no `BUILD` op, only `BUILD_COOP`/`BUILD_PASTURE`; `PLACE` counts fertilizer
placements too; `BUY_ANIMAL` emits one order per species, so 15 heads come in 10 orders) —
corrected, all three read 15/15 exact on tetsuya's own board.
Following tetsuya's schedule on his own board/seed: hands exact every day except d12 (9/11);
plants 212/212 season, WHEAT 164/164, STRAWBERRY 32/32, MELON 8/8, CARROT 8/8; builds 15/15;
places 15/15 animals; animals 15/15 heads bought; FEED 314/353; CARE 316/353; herd 14 standing
(COW 5 SHEEP 6 GOOSE 3) — one COW placement landed on already-occupied ground.
(source: the_greedy_is_a_mix_scorer_2026-08-19.md)

TOMATO is not in any schedule file in the repo (tetsuya WHEAT 164/STRAW 32/MELON 8/CARROT 8;
tetsuya_93866112 WHEAT 135/STRAW 37/MELON 15; kawashigi WHEAT 136/STRAW 34/MELON 20/CARROT 8;
kawashigi_b3 WHEAT 124/STRAW 42/MELON 12/CARROT 5; victor WHEAT 139/STRAW 36/MELON 19/CARROT 6);
tomato only reaches the board through `WHEAT_TILES_TO_TOMATO = 1`, run-time-conditional on the
shop draw and unexercised on the fitted seed.
The one-schedule approach was rejected on 78 games: the fitted game (94345389) is an outlier on
nearly every axis.

```
field         94345389      across 78 games
WHEAT              164      99-187   mean 135
STRAWBERRY          32      24-50    mean  37
MELON                8      8-19     mean  13    <- the MINIMUM he ever plants
CARROT               8      0-65     present in  9/78 games
TOMATO               0      0-22     present in  4/78 games
```

The invariant: herd total 15 (cv 0.03), straw+melon 49.8 (cv 0.12), tiles planted 187.7 (cv 0.09);
the split (cow/sheep, goose, carrot, tomato) is what varies and clusters by shop draw (cow share
0.29/0.50/0.80 in three clusters of 16/13/18 games).
`SHOP_ADAPT_HERD` (47 lines re-splitting cow/sheep on the draw) had been deleted earlier the same
day to fit one game's 3/3 goose match; the 78-game spread said the split is exactly what must stay
adaptive, and that deletion was reversed.
(source: the_greedy_is_a_mix_scorer_2026-08-19.md)

`_herd_split` rework, scored at HIS DECISIONS (not the final census): moved the baseline from
11.5% to 55.8% (779/1187) without touching a line of the rule, purely by fixing the scoring
method.
Fixes: the opening floors to SHEEP 3/COW 2 sheep-first (an empty `unlocked_shops` at day 0 had
been read as "no yarn store" and committed ten cows immediately — his first five animals are
SHEEP SHEEP SHEEP COW COW in 78/78 games, unanimous); `_herd_split` carries a GOOSE bucket from
the schedule row; the milk-count gradient uses `COW = CAP - (LIMIT - draw)` for draws #1-#3; a
milk-covariate fit that was reverted (-16 points, see below).
Placement match: 55.8% -> 65.6% (779->? / 1187, exact figure given as 65.6%).
Order-free per-day scoring (charging the split only for counts, not pen-visit order) recovered a
further 12 points: 65.6% -> 77.9%.
Per-day breakdown:

```
day   placed   right    rate    shops drawn by then
  0      390     344   88.2%    ~0
  3       78      70   89.7%    ~1
  4      148     139   93.9%    ~1
  7      124     110   88.7%    ~2
  9       98      66   67.3%    ~3
 10       99      63   63.6%    ~3
 11      143      86   60.1%    ~3
 12       67      32   47.8%    ~4
 13       29      12   41.4%    ~4
season 925/1187 = 77.9%
```

The milk covariate measured three times: visible milk count fit on the FINAL board (65.6% ->
46.4%, worse); expected final milk, undrawn at 3/8 each (65.6% -> 63.0%); flat
`WOOL_SHOP_NO_YARN_COW` (65.6%, no change) — a linear fit to a bimodal response (his boards cluster
at COW 6 and COW 12) lands between both modes and matches neither.
The opponent-sheep-count lead was tested and survived a control at first (yarn-store boards:
opponent sheep <=4 -> 0.97 his sheep share, opponent sheep >=5 -> 0.99, no effect; late/no-yarn
boards: opponent sheep <=4 -> 0.41, opponent sheep >=5 -> 0.07, a strong crowding-direction
effect) but the deciding cell has n=15 — "a lead, not a result."
(source: the_greedy_is_a_mix_scorer_2026-08-19.md)

Two more fixes brought the herd to 81.9%: goose held to `GOOSE_FROM_DAY = 6` (day 0 went 88.2% ->
100.0%, 390/390) and the tomato tile gated on the draw (`TOMATO_DRAIN_SHOPS_NEEDED = 2` — not a
single tile across 34 games with fewer than two draining shops:

```
tomato-draining shops    0    1    2    3    4    5
games                   10   24   25    9    7    3
games with tomato        0    0    1    0    1    2
```

).
Carrot has no predictor found yet (nine games at drain counts 1,1,1,2,2,2,3,3,3, evenly spread,
non-monotone; first-planted day splits into two clusters, d6-d10 and d25-d27, the late one being
end-of-season opportunism).
Three false premises in one session, all from asserting against a NAME rather than the branch that
reads it: "`WHEAT_TILES_TO_TOMATO` fires unconditionally" (it is gated on `melon_armed and not
q4_armed`); "`SHOP_ADAPT_CROPS = False` so nothing connects draw to crop" (`STRAWBERRY_TILES_
BY_DRAIN` caps strawberry on the draw outside that flag); "`_herd_through_day` re-labels every
head" (it iterates COW/SHEEP only).
A fourth was caught before shipping: an early tomato-gate draft read the local `unlocked` variable
(`unlocked_quadrants`, not shop names) and would have silently scored 0 on every board.
(source: the_greedy_is_a_mix_scorer_2026-08-19.md)

### The milk classifier, and the death of the opponent lead (2026-08-20)

Herd placement match: 81.9% -> 88.5% (1051/1187).
The opponent-sheep-count "lead" from the prior file is DEAD: it was measured over 213 placements
(pseudo-replication — ~50 games, 12 animals/game each repeating one decision).
Re-measured at the game level over 50 late/no-yarn games:

```
variable                his COW<=7   his COW>=8      gap
  opp COW at d9             6.05         6.00         -0.05
  opp SHEEP at d9           3.95         3.77         -0.17
  opp COW final             9.42         9.10         -0.32
  opp SHEEP final           3.84         3.55         -0.29
```

Nothing — the ladder pool plays alike, so the opponent variable has no variance.
The real classifier was the milk count all along, read as a threshold at the decision, not a
linear fit:

```
quadrants @d9      2.00 vs 2.00        shops drawn @d9   3.00 vs 3.00
money @d9       2760.58 vs 2693.94     yarn stores @d9   0.00 vs 0.00
milk shops @d9     0.68 vs 1.81   <--
milk shops @d12    0.95 vs 2.23   <--
```

```
milk@d9 >= 1  -> high cow    37/50 = 74.0%   (fp 13, fn 0)
milk@d9 >= 2  -> high cow    40/50 = 80.0%   (fp  0, fn 10)
always-high baseline         31/50 = 62.0%
milk@d9 <  2: n=29 mean COW  7.21
milk@d9 >= 2: n=21 mean COW 11.33
```

21 of 21 games with two milk shops by d9 go high-cow, zero false positives.
`MILK_SHOPS_FOR_A_BIG_HERD = 2`, `COW_ON_A_MILK_RICH_BOARD = 12`, `COW_ON_A_MILK_POOR_BOARD = 7`,
gated from `MILK_CLASSIFIER_FROM_DAY = 9`.
The same variable had failed twice before as a linear fit (visible milk, final board: 65.6% ->
46.4%; expected final milk, undrawn at 3/8: 65.6% -> 63.0%) before succeeding as a threshold
(81.9% -> 88.5%) — a gradient wants a line, a mixture wants a classifier.
Per-day standing:

```
day    before    after
  9     67.3%    73.5%
 10     63.6%    79.8%
 11     60.1%    82.5%
 12     47.8%    76.1%
 13     41.4%    55.2%
season  81.9%    88.5%
```

d13 at 55.2% (29 placements) is the weakest day remaining.
(source: the_greedy_is_a_mix_scorer_2026-08-20.md)

### The crop mix, the herd and the routes are ONE artifact (2026-08-19)

`_apply_precomputed` keys every stop on `(tile, tuple(op_names))`; any change to what units DO
must be measured against routes re-solved for it, or the number measures the mismatch, not the
change.
Tells: an implausible magnitude (no single tile/animal is worth $10,000), and the PLANTS column
moving when only the shed should have.

```
change | against old routes | against re-solved routes
strawberry cap, straw arm | -$10,553 | +$4,022
melon arm, no crop change at all | -- | +$5,615
1 tomato tile, straw arm | -$1,117 | included above
1 tomato tile, melon arm | -$3,880 | still negative, tile removed there
2 geese, straw arm | -$62,866 | -$63,417 (NOT rescued)
```

The melon row's whole +$5,615 is route staleness — the crop mix did not change at all
(strawberry stayed at 34, no tomato, cap never binds) — any arm carrying stale routes pays this
silently.
Route seating measured directly (`cover.PRECOMPUTED_MISSES`): straw arm after re-solving d12-d23,
19 skipped over twelve days (d12/d16/d21 perfect); q4_melon before its closing days were
re-solved, 0 skipped in d12-d22 and 138 skipped in d24-d29 (where its -$12,308 came from, because
`q4_branch.install` runs precomputed routes through d29 while three-quadrant arms hand the close
to the greedy).
Shipped arms and why the four-quadrant ones were left alone:

```
arm        quads  straw-drains  cap  row   delta      verdict
straw_q3     3         4         37   42   +4,022     binds, GOOD
melon_q3     3         3         36   34   +5,615     never binds
q4_straw     4         0         26   42     -214     binds hard
q4_melon     4         0         26   34   -9,560     binds hard, worst arm
```

Both four-quadrant boards draw zero strawberry shops (tetsuya's 25.5 tiles at zero drains is his
optimum for his season; ours has more ground); a flat ceiling near 37 fits every row above and is
the next thing to test, with q4 tables re-solved.
Seed leak at the close: the replayed opening buys his seed counts (`BUY_SEED STRAWBERRY 23` sized
for a 42-tile season when the cap plants 37) — trimming gained +$560 on three-quadrant boards but
cost -$8,582 on q4_melon (to save $170), because the q4 planting rows install after that turn.
A wheat 2-4-unit close-of-season residue (~$30) is unexplained and left recorded as an open
regression (`test_no_wheat_seed_is_left_in_the_shed` relaxed to `<= 3`).
(source: the_mix_and_the_routes_are_one_artifact_2026-08-19.md)

Stage 1 (optimum animal/plant mix, derived from the maths) vs stage 2 (the day-by-day schedule
realising it) vs routing (downstream of both): our planner handed tetsuya's exact schedule, on his
own board/seat/seed, no taped opening, no precomputed routes at all, banked **$62,365 against his
own recorded $55,330 (+$7,035)** — our routing beats his, on his own schedule, with the worst
routing we can give it, so the gap to #1 is stage 1 (the mix), not execution.
Utilisation corroborates: tetsuya idles 10.4-15.5%, kawa runs 0.0-3.1% idle while doing MORE work
with fewer moves at points.
His schedule does NOT transplant: run on 14 of his other games (his seat/seed/opponent, no taped
opening, no precomputed routes), record 7W-7L (0.50), mean vs his own bank -$13,912, our mean
$100,565 against his $114,477 — his stage-2 rows carry that one board's shop draw baked in, so a
copy loses exactly the adaptation that makes him #1.
(source: the_mix_and_the_routes_are_one_artifact_2026-08-19.md)

Geese, fifth attempt at a verdict, first with a working instrument:

```
2 geese via swap_in_geese, cow-solved routes      $97,317   seed at close $2,100
2 geese via swap_in_geese, GEESE-solved routes    $96,766   seed at close $2,100
no geese,                  geese-solved routes   $156,083   seed at close    $40
no geese,                  cow-solved routes     $160,183   seed at close    $30
```

A matched re-solve did NOT rescue geese (96,766 vs 97,317); the routes are fine and
`swap_in_geese` itself is broken (reshapes the whole schedule — d12 WATER 38 -> 21,
COLLECT_FERTILIZER 14 -> 6 — and inflates seed purchases ~$2,000).
Geese from a schedule that natively contains coops are harmless (built on 9/14 boards, 1-3 birds,
no collapse, no seed explosion; those boards went 6W-3L against 1W-4L without, ~$8.7k better,
suggestive but confounded since a goose board is also an egg-shop board).
Each of the four prior goose verdicts was void for a different instrument reason: `SELLABLE`
omitting EGG, then cow-solved routes, now `swap_in_geese`.
(source: the_mix_and_the_routes_are_one_artifact_2026-08-19.md)

### The four-quadrant branch (2026-08-15, in `market_curves_and_the_q4_branch_2026-08-15.md`)

> Note in the source: section 7's q4-branch number (+$465 mean, "not shippable") is a rougher
> precursor to `q4_variant_first_draft_2026-08-15.md`, which isolates the routing handicap from the
> parcel+herd cost on a proper `shipped_live` baseline and gets **-$716 mean, not distinguishable
> from zero**. Prefer that file's number (below) for this question.

Kawashigi's four-quadrant tape (`91907974`), composed with our shipped tape at d9 (the first day
they disagree), buys the fourth quadrant d13, builds COW 6/SHEEP 12=18 against our COW 10/SHEEP
4=14, 202 tile-plantings, 12 hands.
On seed 3 it banks $148,406 against $133,221.
Run on every seed it LOSES: mean -$2,749, median -$5,286, 5/14 seeds up, 4/14 wins against q3's
5/14 — expected for a branch meant to fire on ~15% of games.
`COW 6/SHEEP 12` appeared only on seeds 3 and 10, exactly the two YARN_STORE seeds in that set —
`WOOL_SHOP_SETS_THE_HERD` was already reading the yarn draw by itself; measured on the shipped q3
arm, an armed seed already shifts to COW 6/SHEEP 8, and the q4 tape reaches 6/12 by buying four
more animals.
On the 15 armed seeds: mean +465, median +4,553, sd 11,220, 8/15 seeds up; wins q3 10/15, q4 12/15
— break-even on money against a standard error of ~$2,900, +2 wins on 15 games — **not shippable**.
Both arms ran routes live from d9, which handicaps q4 harder (100 tiles/18 animals against 75/14,
solved routes built for the three-quadrant board) — a re-solve on the 100-tile board was flagged as
outstanding.
(source: market_curves_and_the_q4_branch_2026-08-15.md)

### A four-quadrant variant, first draft and measurement (2026-08-15) — the corrected number

`q4_agent.make_agent` wraps `schedule_agent.make_agent`; the whole branch edits ONE ROW of the
schedule at day 12, arming when `the_town_promised_wool_early(obs)` (a YARN_STORE among the first
two draws, pinned to `reference.kaggriculture.SHOPS` by a test).
The opening is action-for-action what ships through d11 (11 seeds, 11 passed, no divergence).
Early-yarn boards are 11 of seeds 0-69 (15.7%) against a theoretical 23.4%.
Three arms: `shipped` (production), `shipped_live` (shipped agent paying the live-routing
handicap alone, since q4 must plan d12-29 live), `q4` (the variant).
One OS process per cell (the first run in a process differs, and `q4_agent` mutates
`cover.PRECOMPUTED_ROUTES`, which is process-global).
Opponent `frozen_1186_opponent.py`; seeds 3, 10, 17, 18, 22, 45, 47, 53, 60, 65, 66 — every seed
under 70 that draws a yarn store in its first two draws (the CONDITIONAL effect, not the season
average).

```
arm               mean bank      median    wins  mean quads  mean herd  collect
shipped             102,485     106,157   10/11        3.00      14.00      97%
shipped_live        100,612     104,443    8/11        3.00      14.00      95%
q4                   99,896     100,182   11/11        4.00      17.91      97%

comparison                              mean d    median d  seeds better  W/L swing
shipped_live - shipped                  -1,873        +139       6/11         -2   the LIVE-ROUTE handicap alone
q4 - shipped_live                         -716      -1,696       3/11         +3   the PARCEL + herd, handicap paid by both
q4 - shipped                            -2,589      -5,276       3/11         +1   what actually ships vs the variant, all-in
```

Collection rates are 94-100% on every arm/crop, so no money figure is a routing failure wearing a
crop's name.
q4 armed on 11/11 seeds, SE unlocked 11/11, buy days all d12; one refusal recorded (herd short at
d20, COW 6/SHEEP 11 against target 12, bank $41,689); animals standing in SE at d29: [4,4,4,4,4,
3,4,4,4,4,4] of totals [18x11]; SE tiles still carrying a crop at d29: [0,0,0,1,3,0,0,0,4,0,1] of
25.
**The money result is a null with a wide error bar, not a loss**: `q4 - shipped_live` is -$716,
per-seed sd $9,408, standard error $2,837, spread -$11,430 to +$22,796; `q4 - shipped` is -$2,589,
se $3,026 — neither distinguishable from zero on 11 seeds.
The routing handicap is the larger, separable effect: `shipped_live - shipped` is -$1,873 and
costs two wins, nothing to do with the parcel.
The win rate moves opposite the money and the reason is measurable: q4 wins 11/11 against
shipped's 10/11 and shipped_live's 8/11, mean margin +$4,113 (q4) vs +$2,703 (shipped), because the
opponent's mean bank falls further (-$3,998) than ours (-$2,589) — four extra sheep flood a shared
wool book, and against an opponent selling the same products that hurts the opponent more.
**This is a near-mirror result (frozen copy of our own agent family) and must not be read as a
ladder result.**
The fourth quadrant is bought and then left empty: four of eighteen animals stand in SE (exactly
the +4 sheep added), and the SE crop count at d29 is 0 on seven of eleven seeds — the direct
outlay is $4,000 (parcel) + 4x$500 (sheep) = $6,000, measured return -$716 +/- $2,837.
`docs/fable_fourth_quadrant_reopened_2026-08-15.md` measures the 2026-08-14 field and finds
100-tile seats run 277 season hires (same as 75-tile seats) and work the quadrant by RELOCATING
~8 wheat plantings onto it (SE crop is wheat in all three games) — this draft implements the herd
half of that package and none of the crop half.
One contested number: the brief specifies COW 6/SHEEP 12=18 and the code implements it, but
`WOOL_SHOP_SETS_THE_HERD` records a 2026-08-15 measurement over 74 Kawashigi seats where his
four-quadrant herds run 13-16 and never 18 (max 16 of 74), while `fable_fourth_quadrant_reopened_
2026-08-15.md` records 18 for the 2026-08-14 field's 100-tile seats — both can be true (different
players), but 18 is the field's number, not the leader's.
(source: q4_variant_first_draft_2026-08-15.md)

---

## 9. The market is one token, not nine heads

Measured 2026-08-20 over tetsuya's 78 downloaded games, 56,082 seat-turns.
Treating each turn's whole `market` list as one symbol (op+item set, quantities ignored): 346
distinct market bundles.

```
count   cum%   bundle
45231   80.7  (empty)
 1504   83.3  SELL FERTILIZER
 1180   85.4  SELL WHEAT
 1057   87.3  SELL FERTILIZER, SELL MILK
  448   88.1  SELL STRAWBERRY
  400   88.8  SELL FERTILIZER, SELL WOOL
  271   89.3  HIRE x7, SELL MILK, SELL STRAWBERRY, SELL WHEAT
  268   89.8  BUY_SEED WHEAT, HIRE x5
  232   90.2  BUY_PRODUCT WHEAT
  231   90.6  BUY_PRODUCT WHEAT, HIRE x7
  217   91.0  BUY_SEED WHEAT, HIRE x6
  206   91.4  SELL STRAWBERRY, SELL WHEAT

top 20  bundles cover 93.5% of turns
top 50  bundles cover 96.5% of turns
top 100 bundles cover 98.5% of turns
```

80.7% of turns carry no market action at all, so every marginal head's base rate is overwhelmingly
"no," and nine independent "probably no" decisions multiply into "certainly no" — the arithmetic
behind greedy argmax over per-head marginals emitting zero market orders while the marginals
themselves discriminate 12:1 on `buy_product`.
The bundle `HIRE x7, SELL MILK, SELL STRAWBERRY, SELL WHEAT` (271 turns) is the coordination that
independent heads lose: sells occupy earlier order slots and settle first, funding the hires in
the same turn.
Implication for the BC track: replace nine market heads with one categorical over observed
bundles (~100 classes covers 98.5% of turns, 346 covers all of it); quantities still need a head,
conditioned on the drawn bundle.
The 80.7% empty rate also explains the parked BC track's absorbing state (`P(move) = 6e-5 per
unit-turn`, a checkpoint banking exactly its $3,000 start).
Caveats: quantities are ignored (346 is a lower bound on the full joint); this is tetsuya only, a
second player's vocabulary is unmeasured; tetsuya is no longer #1 as of 2026-08-20 (Ryo Hasegawa
3153.4 against his 3101.4), and zero games of the current leader are held.
(source: the_market_is_one_token_not_nine_heads_2026-08-20.md)

Addendum, held-out (leave-one-game-out, 25 games, 17,975 turns): market prediction (non-empty)
generalises on drain features (67.6%) better than raw shop multiset (39.0%, near-duplicate
retrieval) or a clock-only baseline (58.6%).
Unit-op prediction is NOT demonstrated by either figure: the farmer-op distribution is flat (PASS
19.7%, FEED 14.8%, CARE 14.8%, COLLECT_FERTILIZER 14.5%, MOVES 22.4%, PICKUP 4.5%, HARVEST 4.2%)
and depends on board state that no shop key encodes; the 65.3% farmer-op figure from raw shops is
near-duplicate retrieval (42.5% exact key hits), not knowledge.
(source: the_market_is_one_token_not_nine_heads_2026-08-20.md)

---

## 10. Simulator parity and state-leak fixes

### `run_arena` drove one agent object through every match (task #54, 2026-08-09)

`run_arena` took an agent *value*, not a factory, and passed the same object into every job —
every seed, both seatings — while `schedule_agent.make_agent` builds its `state` dict once in the
closure; a finished season walked into the next match and killed the agent outright.
Only `fable_market_shape_2026-08-09.md` §4 was contaminated by this among all paths checked;
`scripts/gate_pool.py`, `submission/main.py`, `scripts/arena_gate.py`,
`scripts/bench_agents.py`/`bench_arena.py`/`build_script_submission.py`, and
`scripts/confirm_late_sell_bias.py` were all checked clean (either by construction or by
verification).
The pool opponents (`heuristic`, `rancher`, `contrarian`) are stateless — three consecutive
matches through one object gave identical results each time (e.g. `heuristic` seed 40 vs `pass`:
$33,188.0 all three games) — so **only our side was ever contaminated, and only downward.**
Raw damage, one `make_agent(thin, me=0)` object, three matches, seed 40 vs `pass`: game 1
$114,028 (13.7s), game 2 $0 (1.0s), game 3 $0 (0.9s) — not degradation, invalidation.
Through `run_arena`'s seat-agnostic wrapper: `seeds=[40]` (2 games) mean $115,237; `seeds=[40,
40]` (4 games) mean $57,618 — exactly half, matches three and four bank $0.
(source: arena_state_leak_2026-08-09.md)

Fix: `AgentFactory(build, *args, **kwargs)`, a picklable "build me a fresh agent" instruction,
invoked once per match inside the worker; `run_arena` now raises `TypeError` on a bare callable
rather than risk silent reuse.
This also lifts the `workers=1` constraint that `ProcessPoolExecutor`'s macOS spawn semantics had
forced on `scripts/arena_gate.py`.
Revert check per `CLAUDE.md`: with `_resolve` returning its argument unchanged, all three original
tests go red, including a money test that would otherwise have passed vacuously (an unresolved
`AgentFactory` called directly dies and both arms report the $3,000 opening stake, equal and
meaningless) — the liveness guard (`assert once.mean_money[0] > 3000.0`) exists only because the
revert was actually performed.
A second, unfixed defect flagged: `run_arena`'s seat swap is wrong for any agent with a baked-in
seat (`make_agent(schedule, me=0)` placed in seat 1 still believes it is seat 0);
`submission/main.py` is immune because it reads `obs["player"]`.
Full suite on this worktree: 32 failed, 1077 passed, 202 skipped, 14 xfailed, 26 errors (all 26
errors are `FileNotFoundError` on gitignored fixtures; the 32 failures pre-existing, none in
modules importing `kagg.arena`).
(source: arena_state_leak_2026-08-09.md)

### Parity restored against kaggle-environments 1.32.6 (2026-08-09)

`reference/kaggriculture.py` was confirmed byte-identical to the installed
`kaggle_environments` 1.32.6 source; four behavioural rules (of six total 1.32.2->1.32.6 changes,
two already handled) were fixed in the simulators:

```
# | Rule in 1.32.6 | Was | Site
1 | Movement onto a LOCKED tile is allowed | blocked | ops.move, jax_sim movement
2 | DROP/PICKUP/PLACE resolve before the LOCKED guard | after | ops.shed_adjacent, jax_sim on_shed
3 | BUY_PRODUCT/BUY_ANIMAL fail once the shed is full | uncapped | game._commit, jax_sim market commit
4 | Shops unlock with replacement, capped at MAX_SHOP_INSTANCES | all distinct | town.drain_at, Game.unlocked_shops, jax_sim unlock arrays, parity.run_reference
```

Rule #4 mattered most: eight instances drawn from eight shops are all distinct with probability
8!/8⁸ = **0.24%**, so a duplicate is the norm, not an edge case — every parity-gate seed (700,
701, 800, 1500, 1501, 1502) duplicates, and `observe_unlocks(11)` opens YARN_STORE on days 12, 15
AND 21.
`kagg/economics/market.py` already modelled instances correctly; the bool-mask assumption was
confined to the simulator and its test helper.
`Game.unlocked_shops` moved to instance counts; `jax_sim` moved from a shop-indexed `unlock_day
[B, N_SHOPS]` (cannot express a duplicate) to instance-indexed `unlock_day`/`unlock_shop` pairs
`[B, MAX_INSTANCES]`.
(source: parity_restored_on_1326_2026-08-09.md)

Rule #3 (shed-capacity on buys) is unreachable by the five existing 719-step scripts — measured
shed peaks at 8-11 of 100 items in all five — so a simulator ignoring the rule entirely passed
every one of them; `test_full_length_episode_against_a_full_shed_is_exact` now holds both farms at
the 100-item cap for 1,429 of 1,438 player-steps, and backing rule #3 out fails exactly those two
new cases and nothing else.
The tape fixture `tests/test_tape_parity.py` was found to be testing a game that no longer exists:
`data/episodes/89873723.json` records `"module_version": "1.32.3"`,
`"townCenterSellInterval": 12`, and `EXPECTED_BANK = 147,178`; driving the identical tape into the
installed 1.32.6 environment banks **$92,313** — the recorded number is not reachable under 1.32.6
and a simulator reproducing it today would be wrong.
The test now replays the tape into the installed env and compares against that, live, rather than
a stale recording: exact, all 719 turns, both simulators, $92,313.
Suite movement from these four fixes: slow suite 24 failed -> 13 failed (zero regressions); fast
suite 26 failed -> 21 failed (one regression, a search-layer degeneracy issue in
`test_locked_chain_relocates`, deliberately left for its own issue owner).
Eight `test_shop_unlocks.py` failures (stale 1.32.2 price literals) were closed concurrently by
other work in the same session; the measured 1.32.6 table:

```
product | frozen town | test pins | reference schedule | test pins
WHEAT | 30 | 37 | 49 | 51
TOMATO | 64 | 77 | 85 | 98
EGG | 52 | 58 | 69 | 76
MILK | 208 | 263 | 315 | 340
STRAWBERRY | 166 | 219 | 274 | 297
```

— flagged as the numbers other docs' 1.32.2-era figures should be re-checked against, a piece of
work not done in this file.
Each of the four fixes was reverted individually and reconfirmed to fail its own test plus a named
set of parity cases, per `CLAUDE.md`'s testing discipline.
(source: parity_restored_on_1326_2026-08-09.md)

---

## 11. Herd pen geometry

Two fresh loss episodes analysed: `91229682` (seed 73957860, us seat 0 vs `Shivam_2212`, 61,427
vs 94,412) and `91231728` (seed 1153474158, us seat 1 vs `As Wasti`, 89,433 vs 98,581).
**Answer up front: geometry is not a lever here** — replicates the existing `docs/REGISTER.md`
C-21 verdict on two episodes nobody had looked at before.
The shape difference (smeared vs compact) is real, but the walking cost it was assumed to carry
is not: on both episodes our walk-per-work-op ratio is *better* than the opponent's despite worse
geometry.
(source: geometry_of_the_herd_2026-08-09.md)

Per-op action counts (submitted, not resolved), episode `91229682`: MOVE share us 39.8%
(3011/7569), opponent 44.2% (2940/6654) — our MOVE share is lower despite worse pen geometry.
Episode `91231728`: MOVE share us 41.6% (3134/7531), opponent 56.6% (4189/7398) — here the
opponent's MOVE share is dramatically higher and the opponent has the *better* geometry, the
opposite of what "geometry drives MOVE share" predicts.
Biggest divergence in both episodes is PASS and WATER, not MOVE: we pass 1.5-1.7x more (1512 vs
1005; 1746 vs 354) and the opponent waters 1.6-1.9x more (930 vs 578; 1133 vs 590) and plants more
(174 vs 81; 163 vs 81) — a production/idle story, not a walking story.
(source: geometry_of_the_herd_2026-08-09.md)

Pen geometry at final state (day 30), verified against `_shed_access_tiles(board_size=10)` ->
`(4,4),(5,4),(4,5),(5,5)`:

```
episode | side | pens | centroid | ring-depth (Manhattan) | mean shed-dist | shed-dist range | sum shed-dist
91229682 | us | 21 | (3.43, 3.90) | 3.25 | 2.86 | [0,7] | 60
91229682 | opp | 14 | (4.36, 3.57) | 1.90 | 1.21 | [0,2] | 17
91231728 | us | 16 | (3.44, 4.25) | 2.74 | 2.19 | [0,4] | 35
91231728 | opp | 14 | (4.50, 3.00) | 1.93 | 1.57 | [0,3] | 22
```

Our pens in `91229682` confirm the described row-3 smear (x=0 to x=9); pen geometry is fixed early
and never revisited (ring stabilises by day 16 and does not move again).
**Correction to a pre-existing "1.86 vs 2.93" figure**: recomputed from final board state and at
every 2-day checkpoint, ring-depth never reproduces 1.86/2.93 under either Manhattan (3.25/1.90)
or Euclidean (2.69/1.50) metrics — same direction (we are more spread out), different magnitude;
the 1.86/2.93 pair should not be cited going forward.
(source: geometry_of_the_herd_2026-08-09.md)

Realised walking distance (position-diffed, not submitted-MOVE counts):

```
| 91229682 us | 91229682 opp | 91231728 us | 91231728 opp
total realized walk | 3131 | 3029 | 3208 | 4125
work-ops (everything except MOVE/PASS) | 3046 | 2709 | 2651 | 2855
walk per work-op | 1.028 | 1.118 | 1.210 | 1.445
```

This is the decisive number: if geometry cost us turns, walk-per-work-op should be worse for us
given our pens sit measurably farther from the shed (mean 2.86 vs 1.21; 2.19 vs 1.57) — it is
better in both episodes.
In `91231728`, the opponent with the *better* geometry walks *more*, both absolutely (4125 vs
3208) and normalised (1.445 vs 1.210) — the opposite sign from what the geometry-cost hypothesis
needs.
Total realized walking: roughly level in episode 1 (3131 vs 3029, +3.4%) and lower for us in
episode 2 (3208 vs 4125, -22%) — in the episode with the bigger geometry gap.
We lose both games regardless; the gap is production volume and idle time (PASS, WATER, PLANT
counts above), not pen location.
(source: geometry_of_the_herd_2026-08-09.md)

Pen siting mechanism (`_refresh_pins`, `schedule_agent.py` ~1672-1710): `PEN_SPOTS` (a fixed
priority list) is currently `()`, empty and shipped off (a docstring records that filling it with
the opponent's day-0 tiles measured a 2-cell difference out of 150, not worth carrying);
`R.shed_access_tiles()` is tried next; `PEN_NEAREST_DEPOT` is `False` and
`PEN_NEAREST_DEPOT_FROM_DAY = 11`, so before day 11 pens fall through to `_next_ground`, the
quadrant-major boustrophedon sweep that also places crops — which is why a pen requested once
near ground is already planted lands at the tail of the sweep.
`PEN_NEAREST_DEPOT = True` (always nearest-first) was tried and reverted for a measured reason
that its own docstring flags as unresolved: it was refused by a cell-count-resemblance-to-tape
proxy metric, not by a bank/win-rate test — "this is the first arm in the project that is
plausibly right and is refused by the objective rather than by the board."
`router.DEPOT_RING_FIRST` (the field-order-level sibling) is off for a separately-settled reason:
it reversed sign between tuning seeds (+20,526) and held-out seeds (-11,111), a winner's-curse
null.
Given walking is not the binding cost even with the current worse geometry, re-testing this
properly (on bank/win-rate, not the proxy) is flagged as low-expected-value but not free of risk
either, per the existing season-long measurement in `experiment_log.md` §21.
(source: geometry_of_the_herd_2026-08-09.md)

---

## 12. Shed discard and wheat churn

### The discard problem — a corrected 15x overstatement (2026-08-09)

> **CORRECTION carried in the source file, added the same day.** Every discard quantity in the
> original write-up is wrong, overstating the loss by roughly 15x on the surface that matters.
> The metric used throughout, `held_at_dusk - shed_at_dawn`, is not the discard: hour 23's SELL and
> BUY_PRODUCT settle in the same `env.step` as the shed rollover, so a sale was counted as a loss.
> Instrumenting `_drop_inventories_to_shed` (the only path that actually deletes product) gives:
>
> ```
> seed 11 | this doc's delta method | env, exact
> full season | 105 (§3.2) / 137 | 7
> handover 11 | 145 (§3.1) | 123
> ```
>
> Final money is identical under both methods (same runs, measured two ways).
> **Consequence: on the canonical full-season surface the discard problem is ~20 units a season
> against a $55,837 bank.** It is real and large only on the handover-11 fixture, which is not the
> surface the agent is scored on. Any figure below — including the ladder-loss "263 units" and
> `SELL_TO_MAKE_ROOM`'s "101 units" elsewhere in the project — needs re-reading with this 15x in
> mind. What survives unaffected: the seed-stability finding (§1 below) and the
> `FEED_RESERVE_YIELDS_TO_OVERFLOW` day-gate bug (§2 below), a logic error, not a measurement.

(source: fable_the_discard_problem_2026-08-09.md)

**Harness seed-stability**: the `make(configuration={"seed": seed}); env.reset(2)` pattern is
byte-identical across repeated process invocations and `PYTHONHASHSEED` values (three separate
process runs, tape `seb1326`, seed 11: FINAL_MONEY 74320.0, 16 discard nights, 145 units, all
three identical, including one with `PYTHONHASHSEED=777`).
A previously reported "$58,655 vs $66,397 on an identical config" instability could not be
reproduced anywhere in this pattern.
(source: fable_the_discard_problem_2026-08-09.md)

**Real bug found and fixed**: `FEED_RESERVE_YIELDS_TO_OVERFLOW` had no day gate, firing from day 0
against a four-animal herd though every comment describes a day-16+ mechanism.
RED test showed 15 of 16 days before `FEED_DAYS_FROM_DAY` (16) differing with the flag on (e.g.
day 14: OFF wheat=11 money=$63.0, ON wheat=21 money=$2,478.0).
Fixed by gating both guards to `day >= FEED_DAYS_FROM_DAY`; GREEN after, confirmed RED again on
revert.
(source: fable_the_discard_problem_2026-08-09.md)

**The broader question (does releasing the reserve reduce discards) is NOT a clean win**, measured
with the corrected, day-gated code across 7 seed/mode combinations:

```
handover 11 (tape d0-10, agent d11-29)
seed  fix    nights_with_loss/29   units_lost   final_money   Δunits   Δmoney
 11   OFF          13                  145         69,530
 11   ON           17                  228         69,036       +83      -494
 12   OFF          12                  101         83,448
 12   ON           11                   87         83,236       -14      -212
 13   OFF          14                   94         64,930
 13   ON           15                  149         66,765       +55     +1,835
 14   OFF          12                   88        128,080
 14   ON           13                   89        128,180        +1      +100

full season (agent d0-29)
seed  fix    nights_with_loss/29   units_lost   final_money    Δunits    Δmoney
 11   OFF           9                  105         54,813
 11   ON            9                  106         54,474        +1        -339
 12   OFF          15                  117        103,273
 12   ON           12                   78         89,969       -39     -13,304
 13   OFF           5                   10         77,790
 13   ON            6                   20         77,798       +10          +8
```

Discards got worse in 5 of 7, money worse in 4 of 7, including full-season seed 12: -$13,304 of
final bank for 39 fewer units discarded — not a "ship it" result.
(source: fable_the_discard_problem_2026-08-09.md)

**Testing the router's own claim** ("no sell rule can close this; product in a hand at dusk was
never sellable that day") rather than assuming it, seed 11 handover: of 17 residual discard
nights, 10 already had wheat at or below the eviction floor (nothing left to sell, supporting the
router claim), but **5 nights (d16, d17, d18, d20, d24) had wheat sitting 9-29 units above the
floor while product still died** — most strikingly d20, 48 units of wheat in the shed (all of it)
against a floor of 19, with 15 units of other product destroyed the same night.
Conclusion: the router's claim is real for a majority of residual nights but not the whole
picture; roughly a third show the eviction mechanism itself leaving already-identified room
unused, plausibly because `release_order`'s eviction is throttled by the same per-turn/per-order
caps as an ordinary sale.
(source: fable_the_discard_problem_2026-08-09.md)

### The wheat churn is a buy-side day-budget defect, not a sell-side one (2026-08-09)

Reframed mid-investigation from a sell-side theory (the shed carries a 42-44 unit reserve while
offering 51-123 WHEAT/day from day 17) to a buy-side one, on new evidence: **the field disagrees
on how much to sell and agrees closely on how much to buy.**
66 of our own 1.32.6 ladder replays, wheat units offered per game, grouped by team:

```
team                     games  wheat_buy  wheat_sell  mean_bank
alex chilton                66      1,099         764    $73,827
Seb (allegedly)             10        392          84    $74,264
Rayk Kretzschmar             1        266         305   $129,906
Lester Leong                 1        266         305   $125,255
Syed Muhammad Gillani        4        323         649   $101,153
HealthStone                  5        293         436    $80,237
kakuteki                     1        266         350    $70,886
```

Syed sells 649 and banks $101k; Rayk and Lester sell 305 and bank $125-130k; Seb's 84 is the low
outlier, not the field's norm.
The whole field buys 266-392; we buy 1,099 — selling is downstream of having bought too much.
(source: fable_the_wheat_churn_2026-08-09.md)

Mechanism (`schedule_agent.py`, feed-buy emission site): `herd = feed_days(day) * alive -
fed_today - on_hand; short = min(max(herd, min(max(0, owed), BUY_DRIP)), FEED_TURN_CAP)`.
`owed` (the schedule row's own target) self-limits via `state["ordered"][("buys", "WHEAT")]`, but
`herd` (`feed_days(day) * alive - fed_today - on_hand`) had no day-level credit at all —
`feed_days(day)` is a 2-4 day STOCK BUFFER, not a purchase budget, bounded only by the per-turn
`FEED_TURN_CAP` (6), a theoretical ceiling of 144/day.
Measured (ground truth via `kagg.analysis.fills.record_fills`, seed 11, Seb's tape at seat 1):
unfixed, bought 1,800, sold 1,456, final bank $45,797.
The herd path hit its `FEED_TURN_CAP` ceiling on 20-24 of 24 turns on days 17-29 (1,668 herd-path
units asked in a comparable trace).
(source: fable_the_wheat_churn_2026-08-09.md)

Fix: `herd_ceiling = max(0, max(wanted, FEED_BUY_CEILING_DAYS * alive) - state["ordered"][("feed",
"WHEAT")])`, `herd_floor = max(0, alive - fed_today - on_hand)`, `herd_capped = max(min(herd,
herd_ceiling), herd_floor)` — the ceiling credited on asks (reusing the existing counter), the
floor credited on arrivals so a real shortfall is never silenced by the budget.
`FEED_BUY_CEILING_DAYS = 2`, not 1: the first version (`= alive`, one day's true consumption) cut
1,800 -> 393 bought but caused a second, independent failure — seed 11 day 15, the shed held
16-19 idle wheat all day while only 7 of 20 animals got fed, and by day 17 six animals had starved
(herd 20 -> 14, zero recovery) — the bottleneck was delivery (a hand physically carrying wheat to
a tile), not supply, and the old over-buying had been masking that routing/labor constraint with
sheer surplus.
Three ceiling sizes measured on the identical fixture:

```
FEED_BUY_CEILING_DAYS | bought | sold | final bank | herd drops
unfixed (no ceiling) | 1,800 | 1,456 | $45,797 | none
1 (= alive) | 393 | 253 | $53,421† | day 16->17: 20 -> 14
2 (shipped) | 797 | 458 | $46,370 | none
4 (= feed_days(day)*alive, full buffer) | 1,328 | 985 | $46,834 | none
```

(†not comparable to the others — measured on a stale, differently-tuned agent before a
data-contamination issue was caught; the herd-drop finding it produced was independently
reproduced on the clean fixture).
`FEED_BUY_CEILING_DAYS = 2` cuts season wheat purchases 56% (1,800 -> 797), keeps bank at parity
(+$573 vs unfixed), and produces zero herd drops across the full 30-day season — the same safety
record as unfixed, at less than half the spend.
The underlying routing/labor limit (the crew cannot reach all 20 animals in one day even with
abundant wheat in the shed) is explicitly NOT fixed here and is flagged as a separate, deeper bug.
(source: fable_the_wheat_churn_2026-08-09.md)

Two false leads recorded: `PYTHONHASHSEED` was not the cause of a 1,800-vs-373 run discrepancy
(pinning it to 0/1/2 all reproduced 373 identically); the actual cause was a second, concurrent
session editing the shared uncommitted main checkout mid-investigation, which silently swapped in
an unrelated in-flight fix (`FEED_BUY_TURNS_PER_DAY`) on a later re-read — resolved by
reconstructing the true "before" state by reversing this investigation's own diff rather than
re-reading the shared checkout.
(source: fable_the_wheat_churn_2026-08-09.md)

---

## Files merged (22)

1. `docs/the_market_2026-08-09.md`
2. `docs/what_the_town_will_actually_eat.md`
3. `docs/what_saturates_and_what_does_not_2026-08-09.md`
4. `docs/market_curves_and_the_q4_branch_2026-08-15.md`
5. `docs/q4_variant_first_draft_2026-08-15.md`
6. `docs/market_depth_and_the_morning_losses_2026-08-13.md`
7. `docs/when_and_what_to_sell_2026-08-15.md` (STALE)
8. `docs/the_book_is_shallow_2026-08-09.md`
9. `docs/carrot_and_the_empty_book_2026-08-19.md`
10. `docs/carrot_swap_2026-08-12.md` (SUPERSEDED)
11. `docs/fable_allocation_economics_2026-08-15.md`
12. `docs/fable_market_shape_2026-08-09.md` (CONTAMINATED — see §7)
13. `docs/balance_change_eggs_tomatoes_carrots_2026-08-15.md`
14. `docs/the_greedy_is_a_mix_scorer_2026-08-19.md`
15. `docs/the_greedy_is_a_mix_scorer_2026-08-20.md`
16. `docs/the_mix_and_the_routes_are_one_artifact_2026-08-19.md`
17. `docs/the_market_is_one_token_not_nine_heads_2026-08-20.md`
18. `docs/arena_state_leak_2026-08-09.md`
19. `docs/parity_restored_on_1326_2026-08-09.md`
20. `docs/fable_the_discard_problem_2026-08-09.md` (CORRECTION, 15x overstatement)
21. `docs/fable_the_wheat_churn_2026-08-09.md`
22. `docs/geometry_of_the_herd_2026-08-09.md`
