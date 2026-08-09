# The market — mechanism, shipped status, and the open prescription

Consolidated 2026-08-09 from six overlapping 2026-08-08/09 write-ups (`fable_market_technique`,
`fable_market_selling`, `the_shed_destroys_the_harvest`, `the_planner_prices_the_wrong_market`,
`brief_market_selling`, `we_oversell_into_a_contested_book`, `fable_plan`), all now deleted.
Every number below names the script or log that produced it.
**Env version matters here more than anywhere else in the project**: the ladder has run
`kaggle-environments` **1.32.6** since 2026-08-07/08.
Numbers explicitly marked 1.32.2 are historical and are kept only where the 1.32.6 column sits
next to them.

## 1. The mechanism — selling is computable, not a judgement call

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

`λ_p` replaces `allow` (a day total transcribed off one 1.32.2 replay row — see §3).
`slip` replaces `rate[prod]` (a real fact: an oversized single offer walks its own size down the
curve inside one lockstep — see §4).
`contest` is the only free dial and it is game-theoretic, not fitted: `1.0` is the single-player
optimum, `0.5` the two-player split. Lower sells sooner. This formalises the core trap (§6): denying
the opponent revenue is worth as much as earning it, because the contested resource is the *drain*,
not the product.

## 2. Season absorption, both env versions

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

## 3. Why we stopped selling — the shed destroys the harvest

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

## 4. `PRICE_AWARE_SELL_CAP` and `RESERVATION_SELL_CAP` — both are now ON, verified live in code

Both flags are read directly from `kagg/search/schedule_agent.py` as of this consolidation
(`grep PRICE_AWARE_SELL_CAP\|RESERVATION_SELL_CAP`, 2026-08-09):

```
PRICE_AWARE_SELL_CAP  = True   (line 920)
RESERVATION_SELL_CAP  = True   (line 974)
```

This **supersedes** both flags' original 2026-08-08 write-ups, which reported `PRICE_AWARE_SELL_CAP`
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
from §1. It was nearly shipped as `max(rate[prod], reservation)` — reasoning that a rule which can
only *widen* an offer cannot regress — and was a **no-op**: five seeds came back byte-identical,
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
ceiling, not a policy one — see §5 for the real, contested-ladder picture, which differs.

## 5. The current, most important finding — we oversell into a book the opponent is already filling

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

This is the free measurement that turns `contest` (§1) from an assumed 0.5 into an actual per-product
number. `schedule_agent.py`'s reservation call site (`:2487`) still does not read it — the same
missing quantity appears three times in this project (`OPPONENT_SHARE = 0.5` in `scheduler.py`, the
`contest` dial in §1, and here) and has never been measured.

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

### Two corrections on the record

- The first pass of this analysis scaled sales **up to 1.5x** and reported wheat as the single
  biggest recoverable line (+$165,070) — nonsense, since selling up means selling goods we never
  held and nothing checked inventory. The sound version only scales down.
- Market orders in a replay are **offers, not fills** (one replay records a 21,216-unit MILK offer).
  The corrected method perturbs the *observed* path rather than reconstructing the opponent's
  quantities from their orders.

### Addendum — the contested instrument, and what it says so far

Every number above and in §2-4 used `scripts/handover.py`, whose seat-1 opponent barely sells, so no
book floors and glut-protection numbers have nothing real to act on. `scripts/vs_tapes.py` — a real
top player's own play in seat 1 — was run partially:

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
genuinely different opponent and beats us every seed. This is the discriminating fixture that should
gate every future selling change — the arena pool (94.4% saturated) and the handover fixture (10/10
wins) cannot.

## 6. Two traps already caught, twice

1. **Money is not the objective; the ladder is Elo.** Seb's own 1.32.6 sell mix earned us more money
   on *every* seed and still lost **8/8** head-to-head, because ceding wool let the opponent earn
   more than we gained. Denying the opponent revenue is worth as much as earning it.
2. **A replayed tape does not react.** Absolute money against a tape runs 2-3x what real ladder
   games produce. Use a tape for per-day fidelity; use `vs_tapes.py` or a reacting arena pool for
   anything about strategy.

## 7. Prescriptions, in the order they were derived (fold into next work, not yet all shipped)

1. **Sell fertilizer from day 0, hard.** Non-recovering book (`D_rem = 0`, price only falls,
   linear), and we are four days behind the tape into a book that never recovers: first 200 units
   worth $16,020 against the last 200's $8,020.
2. **Sell far more milk, at the corrected §5 rate (0.5x of what looked natural), spread not
   dumped.** The single largest recoverable line.
3. **Wool at ~0.7x volume — a volume fix, not a cadence one.** Melon is the cadence exception;
   spread it, do not cut it, since its drain (30/season) makes no volume level "right."
4. **Wire the opponent's inferred net trade (§5's `opponent_net_trade`) into the reservation call
   site** — the one free measurement none of the three places that need it (`OPPONENT_SHARE`,
   `contest`, the sell block) currently reads.
5. **Gate every future selling change on `vs_tapes.py` against a reacting opponent (`oldleader`,
   not just `seb`), not the arena pool or the handover fixture** — both are proven unable to
   discriminate a real change (§4, §5 addendum).
6. Shed-slot eviction by value density (wheat is the deepest book in the game and the one product
   that least needs shed room) was proposed but not built; `SELL_TO_MAKE_ROOM` only reserves room
   for tonight's drop reactively and does not decide which product should hold the buffer.

## What this does not settle

- The opponent is held fixed in §5's counterfactual. A real one reacts, and cutting our supply
  raises their price, which may raise their volume — read §5 as an upper bound on the easy win.
- "Sell 0.7x" means the other 30% was grown and then wasted; the selling half is cheap, the
  production half (`revenue_rate` in `scheduler.py`) is a separate, unshipped fix.
- The duplicate implementation flagged on 2026-08-08 (`kagg/economics/market.py:reservation_price`
  vs `schedule_agent.reservation_units`) is resolved by omission: `market.py` no longer defines
  `reservation_price`/`units_to_sell` (checked 2026-08-09) and `tests/test_reservation_price.py`
  does not exist. `schedule_agent.reservation_units` is the sole implementation now.
