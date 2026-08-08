# The market is a solved subproblem, and we are ceding it

2026-08-08.
Answers the three questions in `docs/brief_market_selling_2026-08-08.md`.
Everything below is either a line of the environment source or a number produced today; the scripts
that produced each table are named at the point of use.

**Status of the code: `RESERVATION_SELL_CAP` ships OFF (`kagg/search/schedule_agent.py`).**
It is derived, wired, unit-tested (12 tests, `tests/test_reservation_sell_cap.py`) and measured at
**+$2,822 mean on five handover seeds, 4 up 1 down** — which is inside this project's own ±15% seed
variance, so it is not a result yet.

**Duplicate work warning, read before doing anything with this.**
While this was being written, `kagg/economics/market.py` gained `reservation_price` and
`units_to_sell` and `tests/test_reservation_price.py` appeared alongside it (file mtimes 22:08 and
22:09 today, mid-session).
They are a second, independent implementation of the same rule, and that test file is currently
**17 failed / 1 passed** — `reservation_price` raises `TypeError: unsupported operand type(s) for -:
'dict' and 'int'` at `market.py:224`.
Nothing here touches either file.
The two implementations must be reconciled to one before anything ships; the derivation below
applies to both.

---

## Q1. The decision rule

### The exact statement the environment supports

Three facts, each from the source, and together they make the sell decision a computation rather
than a judgement.

1. `market_price(item, inventory, params)` is a pure function of inventory, monotone decreasing
   above `I0 = 10000` (`reference/kaggriculture.py:177-191`).
2. `_commit_unit` raises the market inventory by **exactly one per unit sold**, and — this is the
   sentence that matters most in the whole file — *"Sales at $1 do not increase market supply"*
   (`:626-635`). The floor is an infinite sink, so a crashed book is recoverable but its value is
   forfeited, not destroyed.
3. `_town_consume` lowers inventory by a deterministic amount that depends only on the step and
   `town.unlocked_shops` (`:696-717`), and runs immediately after `_process_market` every step
   (`:909-910`).

Put those together. Inventory only moves up by one per unit either player sells, and down by the
town's drain (and by `BUY_PRODUCT`, which only exists for WHEAT and FERTILIZER). So:

> **Units sellable at a price of at least `L`, by BOTH players, over the rest of the season:**
>
>     N(L) = max(0, I_L − I_now) + D_rem
>
> where `I_L` is the inventory at which the price is `L`, and `D_rem` is the town's remaining drain.

Every drain unit is one re-sale at that level; every level below `I_L` is reachable exactly once
without the drain's help.
Both terms are in the observation — `market` and `town` are both `shared: True`
(`reference/kaggriculture.json`) — so `N(L)` is not estimated, it is read.

### The rule

Invert `N` at our own remaining supply and the reservation price falls out with no fitted constant:

    λ_p = market_price(p, I_now + Q_rem − contest · D_rem)

    offer n units now, where n is the largest n with market_price(p, I_now + n) ≥ max(λ_p, (1−slip)·market_price(p, I_now))

**Inputs, all free, all from the observation:**

| input | where | currently read? |
|---|---|---|
| `I_now` | `obs["market"]["inventory"][p]` | **no** |
| `D_rem` | `obs["town"]["unlocked_shops"]` + `day`, `hour` | **no** |
| `Q_rem` | `obs["private"]["shed"]` + hands' inventories + `yield_units` on our tiles | shed only |
| deadline | `day` | via `LIQUIDATE_LAST_DAY` only |

**What each piece replaces.**

- `λ_p` replaces `allow` — the day total, which is `still_owed`/`carry` off one 1.32.2 schedule row.
  `allow` answers "how much did *he* sell that day"; `λ_p` answers "what will the marginal unit
  fetch if we wait".
- The `slip` term replaces `rate[prod]` — "the largest single day the schedule ever asked for".
  `rate` was standing in for a real market fact (an oversized offer walks its own size down the
  curve inside one lockstep: wool 123 → 138 units took revenue $29,041 → $21,811) and that fact is
  computable per product, per turn.
- The binary `price >= BASE_PRICE` test disappears entirely. It is one bit, and the products do not
  differ in level, they differ in **depth**.

**The deadline is already inside the formula and needs no special case.**
`D_rem` shrinks as the season shortens, so `λ_p` falls automatically toward the floor.
`LIQUIDATE_LAST_DAY` remains as a belt-and-braces override on day 29.

**`contest` is the only dial, and it is a game-theoretic one, not a fitted one.**
The drain is a common pool: every unit the town removes is one re-sale at a good price and whoever
offers first has it.
`contest = 1.0` is the single-player optimum; `0.5` is the two-player split; lower sells sooner.
This is the formal version of the brief's trap #1 — denying the opponent revenue is worth as much as
earning it, because the resource being contested is the *drain*, not the product.

### Why one threshold cannot work: the numbers

`scratchpad/absorb.py`, computed from `MARKET_PARAMS` and `SHOPS` directly.

**Season-total town absorption**, expected over a uniform shop-unlock order, 30 days:

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

Top 1.32.6 plans sell **305-649 wheat**; wheat's 1.32.6 absorption is **525**.
That is not a coincidence, it is the same number: the top plans are selling the town's wheat budget.
Ours sells 71.

**MELON is in no shop at all** — check `SHOPS`, it appears in none of the eight — so the town centre
is its only buyer: 30 units a season on 1.32.6.
**FERTILIZER is in no shop and is excluded from `TOWN_CENTER_PRODUCTS` (`:100`), so its drain is
exactly zero.**

**Depth from a balanced book** — units sellable before the price falls to a fraction of base:

```
product      base   ≥0.9·base   ≥0.75   ≥0.5    above_func
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

A price-neutral offer is **7 units of strawberry or 53 of fertilizer**.
A seven-fold spread, and it does not track the price level: wheat is cheap *and* deep, melon is dear
*and* deep-ish, milk is dear and paper-thin.
`rate[prod]`, a single transcribed integer per product, cannot express that in either direction, and
neither can `price >= base`.

**Dumping the whole pile at once** (mean $/unit, from a balanced book):

```
              10u      50u     100u     200u     400u
WHEAT       23.70    22.54    21.93    21.46    20.78     ← flat: 400 units cost 12% of price
MELON      249.80   241.96   217.21   132.63    66.82     ← 200 units puts the book on the $1 floor
MILK       150.60   108.60    62.05    31.52    16.26     ← 100 units puts it on the floor
STRAWBERRY 111.30    72.96    38.47    19.73    10.37
```

### What the rule is worth, measured

`scripts/handover.py --seeds 11,12,13,14,15` — Seb's own days 0-10 replayed, our agent from day 11,
weeds off, on the locally installed **1.32.2** env.
`data/logs/reservation_off.log`, `data/logs/reservation_on.log`.

```
seed      OFF        ON       delta
  11  140,455   145,608    +5,153
  12  138,003   138,183      +180
  13  151,325   156,196    +4,871
  14  151,075   158,296    +7,221
  15  149,039   145,722    -3,317
mean  145,979   148,801    +2,822   (+1.9%)
```

All ten arms WIN, so the fixture gives no win-rate signal either — this is a money-only reading, and
+1.9% is inside the ±15% seed variance `CLAUDE.md` records.
`destroyed` rises (102/110/102/104/124 → 121/128/185/107/104), which is the expected cost of
narrowing offers on shallow books and is the thing to watch if this is pushed further.

**It stays OFF.**

### The trap this hit, recorded because it nearly shipped

The first wiring was `max(rate[prod], reservation)` — reasoning that a rule which can only *widen* an
offer cannot regress, so it is safe to ship.
It was a **no-op**: five seeds came back byte-identical with the flag on and off, because
`rate[prod]` was already the larger number on every turn that mattered.
Eleven unit tests were green throughout.

The whole content of the rule is in the direction that *shrinks* an offer, and "only ever raises" is
exactly the property that removes it.
`tests/test_reservation_sell_cap.py::test_turning_the_flag_on_actually_changes_what_is_ordered`
exists so this cannot recur — it fails if the composition is inert even when every helper is right.

### The bigger finding: on our fixture the market is not glutted at all

Measured every turn of the handover fixture, seed 11 (min/max inventory reached, and the price
there):

```
product      base  min_inv  max_inv    p@min   p@max   ever above I0?
WHEAT          25     9317     9995       51      27   no
CARROT         35     9536     9999       42      36   no
TOMATO         60     9626     9999      105      60   no
STRAWBERRY    120     9867     9999      217     128   no
MILK          160     9683     9999      315     169   no
EGG            50     9662     9999       70      50   no
MELON         250     9978    10103      277     144   YES
WOOL          200     9912    10001      239     200   YES
FERTILIZER    100    10000    10269      100      46   YES
```

**Six of nine products run at a deficit for the entire season**, trading at up to twice base —
milk peaks at $315 against a base of $160, wheat at $51 against $25.
Both players together sell *less than the town drains*, all season.

This changes what the open problem is.
Glut protection is nearly unexercised on this fixture, so a sell rule can only be measured on three
products here, and the honest reading of "we sell 71 wheat where the field sells 525" is that the
binding constraint on wheat is **production, not policy**.
It is also a coverage warning of exactly the shape `CLAUDE.md` already carries three times: a gate
only tests what it exercises, and this fixture cannot exercise a glut.

### FERTILIZER is a different game and we are losing it outright

`D_rem(FERTILIZER) = 0` — no shop carries it and the town centre excludes it.
Its inventory therefore **only ever ratchets up**, and its price only ever falls: linear, 0.2 per
unit, so 500 units takes it from $100 to the floor.
Holding fertilizer has **zero option value**; the only reason to keep a unit is that FERTILIZE
doubles a tile's yield.

On the fixture the book ends at 10,269 and $46, its worst point of the season — and the units that
put it there were not ours.
Counting product leaving each shed over the season, seed 11:

```
product      ours   tape
WHEAT         417    497
FERTILIZER    114    167     first day it moves:  ours d6,  tape d2
MELON          96     29
MILK           16     68
STRAWBERRY     84     52
WOOL           37     47
```

He is four days ahead of us into a book that never recovers, and the first 200 units of that book
are worth $16,020 against the last 200's $8,020.
Meanwhile **we** are the ones glutting melon — 96 units of the 125 that crash it to $144, against an
absorption of 140 on 1.32.2 and 30 on 1.32.6 — and we sell **16 units of milk** into a book that
never dropped below $169 and touched $315.

Three concrete, derived prescriptions, in the order I would take them:

1. **Sell fertilizer from day 0, hard.** Non-recovering book, finite total value, and a race we are
   losing by four days. This is also the missing half of Seb's working-capital cycle already
   recorded in `docs/the_shed_destroys_the_harvest_2026-08-08.md` §6.
2. **Sell far more milk.** 16 units into a two-times-base book is the largest single number in the
   table above. Whether that is a market rule or the router never getting milk into the shed needs
   one probe to separate — the shed number will say which.
3. **Sell much less melon.** Its whole-season absorption on the ladder's 1.32.6 is 30 units.

None of the three is a tuning question.

---

## Q2. Should we train on downloaded 1.32.6 games?

**No. The hand-derived rule dominates, and it is not close.** Plainly, with reasons.

**(a) Behavioural cloning of sell decisions — no, and the label does not exist.**

The winners submit **fixed open-loop 720-turn scripts** (recorded in memory as
`project_kaggriculture_open_loop`, and `data/seed_scripts/top_guys/90976060/schedule.json` is one).
A script's `SELL WHEAT 28` on day 4 is not a decision conditioned on a state; it is a constant that
was optimised against *that author's own board*.
Cloning it learns a quantity schedule for somebody else's farm — which is precisely the defect
already diagnosed and named: "the sell row is a proxy for a board that is not ours"
(`docs/the_shed_destroys_the_harvest_2026-08-08.md` §4), and it is the
`feedback_optimise_the_artifact` failure mode by construction.
Downloading a thousand more of them makes a better *average* of other people's boards.
We plant 77 tiles where the tape plants 45; no amount of data fixes a label that was never about us.

There is also no counterfactual in the data.
A replay shows what was sold, never what the alternative would have fetched — and the alternative is
the entire content of the decision.

**(b) CMA-ES / evolution over a small parameter vector — defensible, but not yet, and not on this
signal.**

The derived rule has exactly two free scalars, `contest` and `slip`, and searching two scalars is a
reasonable thing to do.
The problem is the objective:

- The arena pool is **saturated at 94.4%** with `mirror` at 50%, so every non-mirror opponent already
  loses 100% of the time and no sell rule can move the win rate there. It cannot discriminate.
- The handover fixture wins 10/10 arms, so it gives no win-rate signal either.
- That leaves money, which this project has already measured as **anti-correlated with the result**
  in exactly this domain: Seb's own 1.32.6 sell mix earned more money on every seed and lost 8/8
  head to head (`brief_market_selling_2026-08-08.md`, trap 1).
- Seed variance is ~15%, and this project has already been burned once by a fixed-seed objective
  reporting +40% where held-out seeds said +12.8%.

So a search would be optimising a proxy that is known to point the wrong way, at a resolution the
noise floor does not support.
Fix the discriminating fixture first — an opponent that can beat us, on 1.32.6 — and *then* a
two-parameter CMA-ES over a held-out seed split is cheap and sane.

**(c) The thing that actually dominates both: solve it, do not learn it.**

There is no unknown function on the revenue side.
`market_price` is a pure function we can call; the drain is deterministic and observable; the
revenue of any offer is exact (`kagg/economics/market.py:sell_revenue`).
Fitting a black box to approximate a function you can already evaluate exactly is strictly worse
than evaluating it.

The one genuinely unknown quantity is the opponent's future supply — and that is **observed, not
forecast** (see Q3, item 5). It does not need a model either.

If more compute is worth spending, spend it on a **dynamic program over the market subproblem**,
which our parity-verified simulator already supports: per product it is one-dimensional in inventory
with a deterministic drain and a few hundred reachable states, so the optimal liquidation schedule is
a shortest path, not a fit.
That gives the exact answer this rule approximates, and it gives it as a *benchmark* the heuristic
can be scored against.

---

## Q3. Free information the sell block ignores

The sell block reads exactly one thing from the market: `market.prices`
(`schedule_agent.py`, `prices = (obs.get("market") or {}).get("prices") or {}`).
Everything below is in the same observation and was untouched before today.

1. **`market.inventory` — the position on the curve.**
   `prices` is one scalar and throws away the depth: it cannot distinguish 400 wheat clearing at a
   mean $20.78 from 200 melon putting the book on the $1 floor. With inventory, the revenue of any
   candidate offer size is exact, not estimated. *Now read by `RESERVATION_SELL_CAP`.*

2. **`town.unlocked_shops` — the exact remaining absorption.**
   Which shops are live determines the per-tick pull per product exactly, and therefore `D_rem`.
   A product's whole strategic character is in this number: wheat 525 a season, melon 30, fertilizer
   0. *Now read by `RESERVATION_SELL_CAP`.*

3. **The drain phase within the day.**
   Shop ticks land on steps divisible by `townShopSellInterval` (4) and the centre on
   `townCenterSellInterval` (12 on 1.32.2, 24 on 1.32.6), and `_town_consume` runs *after*
   `_process_market` in the same step. So the book is refreshed once per four steps, and a second
   offer inside the same four-step window sells into a book nobody has restocked.
   The natural sell cadence is therefore **six offers a day, phase-aligned**, not one every turn.
   Untested — and note that two previous attempts to move off "re-offer every turn" both lost money,
   so this needs a measurement rather than an argument. Flagged, not claimed.

4. **`farms[opponent]` — their whole board.**
   Their pens, animals, crops and standing `yield_units` are visible, so their *supply* per product
   is forecastable — which is the one term in `N(L)` we are currently guessing with a constant
   (`contest = 0.5`). Counting their sheep tells you the wool that is coming. Their `money` tells you
   when they can and cannot buy land or hire.

5. **The strongest one: the opponent's trades are exactly inferable, every turn, for every product.**
   We know our own sales, and the town drain is deterministic. So

       opponent_net_trade(p, t) = Δinventory(p) − our_sales(p) + drain(p, t)

   recovers their sales minus their buys, per product, per turn — including products where we cannot
   see their shed, because `private` is the only unshared field.
   That turns `contest` from a dial into a measurement, and it is free.

6. **Our own standing supply.**
   `yield_units` on our tiles and pens, plus what the crew is carrying, is stock the season must
   clear. The block nets only `ripe_wheat`, and only as a feed reserve. Understating supply
   understates the glut, which is the direction that already cost 331 destroyed units.
   *Now counted by `standing` in the sell block.*

---

## Open

- **Reconcile the two implementations.** `kagg/economics/market.py:reservation_price` /
  `units_to_sell` and `schedule_agent.reservation_units` are the same idea written twice today. The
  economics one has the better property-test suite (`tests/test_reservation_price.py`) and is
  currently 17/18 red on a `TypeError`; the schedule_agent one is the one the submission can reach.
  One of them should go.
- **The fixture cannot see a glut.** Six of nine products run at a deficit all season on the
  handover fixture, so glut protection — the whole point of the rule — is measured on melon, wool
  and fertilizer only. A fixture with a *reacting* 1.32.6 opponent is needed before any of this is
  trustworthy. `scripts/vs_tapes.py` was not run for lack of time and is the obvious next arm.
- **Everything here was measured on the installed 1.32.2 env.** The absorption tables give both
  columns, and `town_drain_remaining` reads the interval from the env's own spec so it follows the
  ladder automatically — but the handover deltas are 1.32.2 numbers and the melon/fertilizer effects
  are roughly **4.7x sharper** on the 1.32.6 the ladder runs, because the centre halves its cadence
  and loses its late-season ramp.
- **Fertilizer, milk and melon** (the three prescriptions above) are each worth more than the rule
  that surfaced them, and none needs the rule to act on.
