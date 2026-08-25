# The sell side: the ceiling is $8k-$13k and we are already halfway up it

Fable, 2026-08-25.
Read-only pass. No repo file was changed except this one.
Scripts and raw logs are in the session scratchpad at
`/private/tmp/claude-501/-Users-alexchilton-DataspellProjects-kaggriculture/1ceba71d-ed80-4dee-9d20-d544a8b98ee0/scratchpad/`
(`book.py`, `ceiling.py`, `ceiling_700.log`, `ceiling_702.log`, `out_70{0,1,2}.txt`).

## The answer in six lines

1. This is **not** an optimal-execution problem.
   Revenue is **path-independent** in everything except the town's drain, and I prove that from the source below.
2. We are **never glutted**. Measured over three full seasons: six of seven books trade **below** `I0`, at **1.04x to 2.24x base price**. The worst glut we create all season on any product except FERTILIZER is **+6 units above `I0`**. Zero units traded at the $1 floor on seed 700.
3. The **+8%/unit at smaller lots is a mix artefact.** Dropping the 200 cheapest units of our own realised season raises $/unit by **+10.4%** while cutting revenue by **-3.9%**. Same shape, no mechanism.
4. The **measured ceiling** for a perfect sell schedule, shed cap respected, farm actions held fixed: **+$7,922 (seed 700) and +$12,805 (seed 702)** — 4.2% and 7.0% of sell revenue.
5. The **whole span** of the dimension, from "dump everything the turn it lands" to that optimum, is **$11,366 / $16,777**. We currently sit about a third of the way up. There is no $80k hiding here.
6. Two things nearby are **bigger than the entire sell schedule**: the wool/yarn-store draw (**$18,908** swing on identical production) and the dawn discard (**$10,322/season**, your own `data/logs/what_rots_by_product.log`). Both are production decisions, not sell decisions.

**Recommendation: stop optimising sell cadence.** Ship the current rule. Spend the time on the herd decision at day 3-6 and on shed headroom.

---

## 1. Four things in the brief that are wrong

Leading with these because two of them invalidate work already done.

**"It never reads the market book" — false.**
`PRICE_AWARE_SELL_CAP = True` (`kagg/search/schedule_agent.py:2468`) and `RESERVATION_SELL_CAP = True` (`:2469`) are both live.
`reservation_units` (`:3405`) reads `market.inventory` and `town.unlocked_shops` every turn and computes the remaining town drain from them.
Any arm framed as "add book-reading" is re-adding something that ships.

**`maxMarketOrdersPerTurn = 10` is 10 orders, not 10 units.**
`_parse_order` (`reference/kaggriculture.py:631`) parses `["SELL", item, n]` with `n` unbounded, and `_process_market` truncates the *list* at ten (`:560`).
There are nine products. The order channel has never been a constraint on sell volume and cannot become one.

**`reference/kaggriculture.json` is stale.**
It gives `townCenterSellInterval` a default of **12**. The installed `kaggle-environments 1.32.7` gives **24**, and 24 is what the ladder runs.
`reference/kaggriculture.py` is byte-identical to the installed module; only the JSON has drifted.
Anyone who reads `reference/` for a config default gets the town-centre drain 2x wrong. My numbers below use 24.

**The rot figure contradicts your own log.**
The brief says rot is "27.5 units / $3,716 a season, ~2.2% of bank".
`data/logs/what_rots_by_product.log`, same day, six seeds, says **78.0 units / $10,322, 6.11% of bank**.
Those cannot both be true. The second is the more detailed measurement and is the one I have used. Resolve it before quoting either.

---

## 2. The mechanism: revenue is path-independent

This is the whole theory, and it is three lines of source.

- `market_price(item, inventory)` (`:192`) is a pure function of the book.
- `_commit_unit` raises the book by exactly one per unit sold (`:660`).
- Nothing else our agent does moves it.

So if we sell `N` units of product `p` over a season, the revenue is

    R = sum over k = 0 .. N-1 of  market_price(p, I0 + k - d(t_k))

where `d(t)` is the **exogenous** book movement by time `t` — the town's drain, the opponent's flow, and our own `BUY_PRODUCT`.
`k` is the unit's rank in **our own** sell sequence and does not depend on the schedule at all.

Three consequences follow immediately, and every one of them is checkable:

**(a) Lot size within a turn is worth exactly zero.**
Splitting one turn's 22-unit order into three smaller orders on the same turn cannot change a cent: the same 22 rungs of the curve get walked in the same order.
Any measured effect of lot size is the drain harvested *between* turns, or it is an artefact.

**(b) Selling later is weakly better, always.**
`d(t)` is non-decreasing and `market_price` is non-increasing in the book, so delaying any unit weakly raises its price. There is no execution-risk term, no variance penalty, no reason to hurry.
The only cost of delay is a shed slot.

**(c) Volume is always weakly good — never refuse a sale to protect a price.**
`_commit_unit:658-660` does not raise the book when `price == 1`. The floor is **absorbing**.
Marginal revenue is therefore never below $1/unit and `R(N)` is strictly increasing in `N`.
An arm that sells 897 units instead of 1,442 loses money by construction. That result needed no experiment.

**On Almgren-Chriss.** It does not apply and adopting its language will mislead you.
A-C trades a temporary-impact cost against inventory *risk* over a stochastic price. Here there is no temporary impact (every unit's impact is permanent), no price risk, and no risk aversion.
The correct analogue is a **deterministic reservoir release problem**: an exogenous inflow (the town's drain) refills a reservoir at a known rate, storage is capped, and you release to maximise a concave value. The optimum is bang-bang: hold to the cap, release the overflow, as late as the cap permits.

---

## 3. Where our book actually sits

Measured, not modelled. `_commit_unit` was wrapped to record the book at every fill, seat 0, shipped agent vs `contrarian`.

    seed 700, bank $152,354

    product      units       rev$  $/unit  base  xbase  book@1st  median  book@last  worst
    MILK           222     55,537     250   160   1.56       -25    -102       -205    -15
    STRAWBERRY     249     55,097     221   120   1.84      -145    -146       -142   -110
    WOOL           131     30,936     236   200   1.18        -7    -118       -296     +6
    WHEAT          625     24,351      39    25   1.56       -42    -207       -157    -25
    FERTILIZER     199     15,960      80   100   0.80         0     +99       +198   +198
    MELON           18      4,675     260   250   1.04       -11      -2         +5     +5
    CARROT          14        570      41    35   1.16       -46     -80        -89    -44

    "book" = market inventory minus MARKET_I0 at the instant that unit traded.
    negative = scarcity, price ABOVE base.   units at the $1 floor: none.

**Read the `worst` column.** Excluding FERTILIZER, the deepest glut we create in 720 turns is **+6 units**.
We are not walking down a convex curve. We are selling into a hole the town dug for us.

The reason is a rate mismatch that has nothing to do with execution. At eight shop instances the town removes, per day:

    WHEAT 31   STRAWBERRY 25   CARROT 19   MILK 19   TOMATO 13   EGG 13   WOOL 13   MELON 1   FERTILIZER 0

Over a whole season (132 shop-instance-days plus 30 town-centre ticks) the town absorbs **2,319 units**.
We sell ~1,460. On strawberry we produce 8.3/day into a 25/day drain.

**This is the second-order effect you asked about, and it is bigger than the first.**
The steep, convex part of every price curve is *above* `I0`. Below `I0` the shapes are `sqrt` and `log` and they are nearly flat.
The value of one extra day of delay, at the book depth we actually occupy versus at `I0`:

    product      median book   $/unit/day here   $/unit/day at I0
    STRAWBERRY          -146                 9                 42
    MILK                -102                 8                 38
    MELON                 -2                 2                  6
    CARROT               -80                 2                  1
    WOOL                -118                 1                 23
    WHEAT               -207                 1                  6
    FERTILIZER           +99                 0                  0

Per **turn** that is $0.33-$0.38 on milk and strawberry and $0.04 on everything else.
`LATE_SELL_FROM_HOUR = 16` delays a unit by at most 16 turns, so its entire theoretical upside is about **$6/unit on milk and strawberry and near zero elsewhere** — roughly **$2,700 a season** if every unit got the full delay.
Your own `data/logs/what_to_sell.log` computed the same thing independently: +$0.62 wheat, +$7.38 strawberry, +$14.00 milk.

A dawn discard costs **$221-$234/unit** (`what_rots_by_product.log`).
**The gate's best case is $6/unit and its failure mode costs $230/unit.** That is the trade, and it is 38:1 against holding whenever the shed is near the cap.

---

## 4. The +8% is a mix artefact

Take our own realised season and drop the cheapest units, keeping every product's own price path:

    drop cheapest    units    revenue     $/unit    $/unit change    revenue change
    none              1541   $203,577     $132.1                -                 -
    200               1341   $195,612     $145.9           +10.4%             -3.9%
    400               1141   $187,648     $164.5           +24.5%             -7.8%
    545                996   $181,873     $182.6           +38.2%            -10.7%

**+10.4% $/unit for free, purely by selling less.**
Your capped arm reported +8% at lot 8 vs lot 22 and sold 897 units instead of 1,442. That is exactly this curve.
The mechanism is Simpson's paradox: WHEAT is 43% of our units at $39 and 13% of our revenue. Any cap that binds unevenly drops wheat first and lifts the mean.

**How to check it in one command.** Report $/unit **per product** and the terminal book **per product**.
If $/unit rose inside every product *and* each product's final book is unchanged, the effect is real.
If the product shares moved, it is mix. Section 2(a) says a same-turn split cannot be real, so the prior should be strongly on mix.

---

## 5. The ceiling, measured

`scratchpad/ceiling.py`. Play the real season. Record per turn: our shed per product (which reconstructs the arrival stream), and the book per product minus our own cumulative sales (which gives the exogenous book `d(t)`).
Then re-solve offline under the only two real constraints — a unit cannot be sold before it reaches the shed, and shed occupancy must stay under the cap — by delaying every unit maximally. By section 2(b) that is the optimum.

    seed 700   product      N   actual$      cap0     cap20     cap50    cap100
               MILK       222    55,537    54,556    57,885    61,473    65,716
               STRAWBERRY 249    55,097    54,065    55,722    57,709    60,112
               WOOL       131    30,936    30,693    31,792    32,411    32,761
               WHEAT      625    24,351    23,168    23,927    24,821    25,907
               FERTILIZER 199    15,960    15,960    15,960    15,960    15,960
               MELON       18     4,675     4,675       634       634       634
               CARROT      14       570       565       594       594       594
               TOTAL     1458   187,126   183,682   186,514   193,602   201,684
               vs actual                   -3,444      -612    +6,476   +14,558

    best split of the 100-slot shed: MILK 85, STRAWBERRY 15, everything else 0
    ceiling $195,048   actual $187,126   headroom +$7,922  (+4.2% sell side, +5.2% bank)

    seed 702   best split: WOOL 45, MILK 30, STRAWBERRY 25
               ceiling $196,353   actual $183,548   headroom +$12,805 (+7.0%, +8.5% bank)

Four things to read out of this:

- **`cap0` is only $3,444 below what we do now.** Selling every unit the turn it lands, with no storage and no cleverness at all, costs 1.8% of the sell side. The entire dimension is narrow.
- **FERTILIZER is $15,960 in every column.** Its drain is zero (`TOWN_CENTER_PRODUCTS`, `:114`, excludes it and no shop carries it), so `d(t) = 0` and timing is *provably* worthless. Stop testing fertilizer sell rules. The only fertilizer question is whether to sell it at all — we get $80/unit against a base of $100 and the book never comes back.
- **MELON prefers `cap0`**, and by a lot: $4,675 held, $634 delayed. `contrarian` dumps 207 melons and crashes the book, so waiting is walking into someone else's sale. `NO_DRAIN_PRODUCTS = ("MELON",)` (`kagg/search/schedule_agent.py:2494`) is correct and should stay.
- **The headroom is all MILK, STRAWBERRY and WOOL**, and it needs 85 shed slots of one product. That is not compatible with also storing wheat, fertilizer and the day's un-tipped harvest, so **$7,922 is an over-estimate of what is reachable**, not a target.

### Caveats on this number, stated plainly

- Three seeds, one opponent (`contrarian`), one arm. Seed variance on this project is ~15%.
- The per-product cap treats the 100 slots as separable. They are one shared pool drained at one dawn (`_drop_inventories_to_shed`, `:843`, called `:878`), so the true joint optimum is **lower** than the greedy split shown.
- The arrival stream for WHEAT is approximate: `PICKUP` removes wheat from the shed for `FEED`, so I force the reconstructed arrivals to be monotone. MILK, STRAWBERRY and WOOL never leave the shed except by sale, so their rows are exact.
- The re-solve holds the opponent's actions fixed. Selling differently would change their book slightly.

---

## 6. What is actually big, and it is not the sell schedule

**WOOL is the largest single number on the sell side, and no sell rule can touch it.**
Identical production, three seeds:

    seed   wool units   wool revenue   $/unit   exogenous wool drained all season   units at $1 floor
    700           131        $30,936     $236                                 419                   0
    701           131        $16,555     $126                                 101                   6
    702           132        $12,028      $91                                  65                  44

`YARN_STORE` is the only shop that eats wool, at 2 per tick — 12/day per instance.
Without one, wool's entire season absorption is the town centre's 30 units. Seed 700 drew a yarn store; 701 and 702 did not.
**$18,908 of revenue swing on the same 131 sheep-days, decided by a random draw at `_end_of_day:891`.**
The herd size is committed on days 3-6; the first shop unlocks on day 3. The decision that matters is whether to buy sheep *at all* before the draw is known, and how fast to switch when it is.
`docs/` already records `WOOL_SHOP_SETS_THE_HERD` as a count rule that never reads the book. That is the open item, and it is worth more than everything in section 5.

**The dawn discard is second.** $10,322/season, 78 units, at $221-$234/unit for the four expensive products.
`docs/the_shed_is_the_bottleneck_2026-08-25.md` measures us at 90+ shed occupancy on 2,505 turns across 35 games against the opponents' 488. That is the constraint that is actually binding, and it is a routing and headroom problem.

**Third, and this inverts the question.** Six of seven books trade above base because the town wants more than we grow: strawberry at 2.18x base with 15/day of unmet demand, milk at 1.34x with 10/day.
The market is not telling us to sell better. It is telling us to grow more strawberry and milk, and less wool.

---

## 7. The optimal policy, stated exactly

If you ship anything, ship this. It is the argmax of section 2 under the shed constraint.

1. **Sell at dusk, down to `shedCapacity - (units your hands will tip in at dawn)`.**
   Not to a fixed target, and never below it. The binding instant is `_drop_inventories_to_shed` at the end of hour 23; anything above the cap at that moment is destroyed and anything below it is a wasted slot.
2. **Allocate the slots by marginal delay value**, computed live: `market_price(p, book_p - drain_p) - market_price(p, book_p)`, where `drain_p` comes from `town.unlocked_shops` — both fields are `shared: True` in the observation. Fill from the top. This is a knapsack over 100 slots, not a per-product rule.
3. **Zero slots for any product the town barely eats.** FERTILIZER is exactly zero — no shop carries it and `TOWN_CENTER_PRODUCTS` (`:114`) excludes it, so its book never recovers at all. MELON is 1/day (town centre only; no shop carries it). WOOL drops to 1/day in any season with no `YARN_STORE`, which is the seed-702 case above. Rule 2 already produces this if the drain is read live; the point is that it must be read live, because it is a draw and not a constant.
4. **The hour matters only through the six drain ticks.** `_town_consume` fires on `step % 4 == 0` and runs *after* `_process_market` in the same step (`:941-942`). Selling at hour 20 captures five of the day's six ticks. Hours 21-23 add nothing over hour 20.
5. **Never cap a lot to protect a price.** Section 2(c). The floor is absorbing; the marginal unit is always worth at least $1 and the units already sold are already sold.
6. **Lot size within a turn is a no-op.** Delete any rule whose only effect is to split an order on one turn.

Against that list, the current agent's two defects are: the `hour < 16` gate compresses the day into 8 selling turns, which is what pins the shed at 100 (`:4719`); and `SHED_TARGET = 90` (`:665`) / `SHED_HEADROOM_FROM_DAY = 12` (`:670`) make the release conditional on day >= 12 and shed >= 90, which by your own measurement is 10-16 turns of 720.
Both are worth low single-digit thousands. Fixing them will not show up over 15% seed variance without ~100 paired seeds.

---

## 8. The one experiment, if you run one more

`scratchpad/ceiling.py` is it, and it is already written and validated. To make it decision-grade:

- Run it on **20 seeds x both arms x the competitive pool**, not 3 seeds x `contrarian`.
- Replace the greedy per-product split with a **joint** solve over the shared 100 slots at the dawn instant. That is the only place the current version is optimistic.
- Report **one number**: `ceiling - actual`, per seed, as a share of bank.

The stopping rule, agreed in advance: **if the median headroom is under 5% of bank, close the sell side and do not reopen it.** Seeds 700 and 702 give 5.2% and 8.5% with an optimistic solver, so I expect the joint solve to land under 5% and for the answer to be "close it".

**Why the existing `data/logs/the_sell_ceiling.log` could not settle this.**
Its `feasible$` is **$22,668 below** its own `actual$`. A ceiling below the measured floor is a broken model, and its own validation note says as much before the columns are read anyway.
The three causes, all fixable: it used a fixed **14-slot-per-product** shed share instead of the real shared pool; its `model$` misses MELON by **-87.7%** and WHEAT by **-41.5%**, which is our 439 `BUY_PRODUCT` wheat units (`:671` decrements the book, and that is why wheat sells at 1.56x base) plus the opponent's 207 melons; and it used an *expected* shop draw rather than the season's actual `unlocked_shops`, which as section 6 shows is a 6x error on wool.
The version I ran takes the exogenous book straight off the live episode, so none of the three can occur.

---
---

# REVISION 1 — 2026-08-25, later the same day

**Everything above section 8 was measured against `contrarian`, which does not compete for the book.
The headline claim "we are never glutted" is WITHDRAWN, and with it the recommendation to close the
sell side. Re-derived against a competing seller the ceiling is +$19,579 to +$32,148 a season —
17% to 37% of bank — against the +$7,922 / +$12,805 reported above. Keep working on this.**

The superseded reasoning is left in place above. Sections 2(a), 2(c), 4, 6 and the section-1
framing corrections survive unchanged; everything that depended on the measured book depth does not.

## R0. The error was mine, and my own table contained the counterexample

I wrote "excluding FERTILIZER, the deepest glut we create in 720 turns is +6 units" from the
**seed 700 row**, and then generalised it across three seeds in the headline.
Two screens further down, in the same run, my own output says:

    seed 700   units that traded at the $1-$2 FLOOR: none
    seed 701   units that traded at the $1-$2 FLOOR: {'WOOL': 6}     worst book +59
    seed 702   units that traded at the $1-$2 FLOOR: {'WOOL': 44}    worst book +59

Seed 702 sold 132 wool for $12,028 — **$91/unit against a $200 base**, with a third of the units at
the floor. That is a glut. I had it, tabulated it in section 6, and still wrote a headline that
contradicted it. A claim that does not survive checking against my own output two paragraphs up is
the exact failure mode the project rules name. It cost the coordinator a corpus scan to overturn.

## R1. Does path-independence survive a glutted book?

**Partly, and the part that dies is the one my recommendation rested on. The coordinator's
conclusion is right; the route is not quite, and the difference is what tells you which products
invert.**

**The $1 floor does NOT break path-independence.** This is worth getting right because it is the
premise of the coordinator's question. With no exogenous book movement, revenue is still exactly
order-independent even when the floor is reached: the book walks the same rungs in the same order
and every surplus unit gets $1, whatever sequence you sell them in.
Measured directly (`scratchpad/slots.py`, real env, one turn, balanced WOOL book, opponent selling
nothing):

    me: one order of 20    -> $3,856
    me: two orders of 10   -> $3,856      byte-identical

**What breaks is that the exogenous book path `e(t)` is no longer monotone.**
Against `contrarian`, `e(t)` only ever fell: `_town_consume` (`:728`) is the only thing moving it,
and it removes units every 4 steps. Monotone decreasing `e(t)` is exactly the premise of my
theorem 2(b), "selling later is weakly better, always".
Put a real second seller in and `e(t)` rises whenever they dump. **Theorem 2(b) is false in the
competitive regime and must not be used.** Timing becomes a genuine optimisation with an interior
optimum, not a boundary one, and the direction of the optimum is now per-product.

This is why the re-derived ceiling can be 4x larger while none of the source-level facts changed.

**Theorem 2(c) survives untouched.** `_commit_unit:658-660` does not raise the book when
`price == 1`, so marginal revenue is never below $1 and total revenue is still non-decreasing in
volume. This is opponent-independent. An arm that sells fewer units still loses by construction.

**Theorem 2(a) — "lot size within a turn is a no-op" — was wrong, and the correction is worth
money.** `_process_market` loops over **order slots** (`:562`, `for i in range(max_len)`) and runs
the per-unit lockstep loop only over the players who have an order in **that same slot index**
(`:585-620`). Two players interleave rung-by-rung only if their SELLs sit at the same index.
Same test, opponent now selling 20 WOOL in slot 0:

    me: one order of 20         ->  me $3,428   them $3,428
    me: two orders of 10        ->  me $3,240   them $3,581     -$188  (-5.5%)
    me: BUY_SEED then SELL 20   ->  me $2,943   them $3,856     -$485  (-14.2%)

**One non-sell order ahead of a SELL costs 14.2% of that turn's sell revenue and hands the
difference to the opponent.** This is invisible against a non-selling opponent — which is why it
survived — and it is free to fix.

`_order_sells` (`kagg/search/schedule_agent.py:950`) ranks SELLs *within the slots they already
occupy* and deliberately does not move them: "SELLs are deliberately not moved" (`:979`).
`_wheat_row_first` (`:966`) moves hour 0's `BUY_PRODUCT WHEAT` in front of everything, which on a
measured +6-wheat argument pushes any hour-0 SELL back a slot.
The funding argument at `:979-980` only forbids moving SELLs *later*; moving them **earlier** still
lets a SELL settle before every atomic order behind it. So sells-first is compatible with it.
Caveat: one turn, one product, both sides selling the same 20 units into a balanced book. The
magnitude scales with the overlap and I have not measured it over a season. It is a cheap A/B.

## R2. The ceiling, re-derived against a seller that competes

Same solver as section 5 (`scratchpad/ceiling.py`), same seeds, only the opponent changed.
`mirror` is our own agent in seat 1; `tape` is the Kawashigi replay.
Logs: `scratchpad/ceil_mirror_{700,702}.log`, `scratchpad/ceil_tape_{700,702}.log`.

The mirror reproduces the ladder shape the coordinator measured:

    seed 700 mirror   peak book above I0: FERTILIZER +493, MELON +130, WOOL +60, WHEAT +26
                      our units at the $1 floor: WOOL 158, FERTILIZER 72
                      turns with the book <=25% of base: WOOL 271, FERTILIZER 169

    seed 700, mirror   product      N   actual$      cap0     cap20     cap50    cap100
                       STRAWBERRY 270    63,098    62,017    63,787    66,008    68,993
                       MILK       219    44,303    42,998    46,808    50,054    53,157
                       MELON       72    14,718    14,869    13,479    12,336    11,925
                       FERTILIZER 318    12,552    12,923    12,185    11,346    10,288
                       WOOL       200     5,944     6,008    14,184    32,122    40,265
                       WHEAT      123     4,528     3,749     4,461     5,557     6,968
                       TOTAL     1202   145,143   142,564   154,904   177,423   191,596

    opponent   seed   actual$    ceiling$    headroom$   % sell side   % bank
    contrarian  700   187,126     195,048       +7,922          +4.2     +5.2
    contrarian  702   183,548     196,353      +12,805          +7.0     +8.5
    mirror      700   145,143     172,089      +26,946         +18.6    +26.7
    mirror      702   131,171     163,319      +32,148         +24.5    +36.5
    tape        700   125,969     145,548      +19,579         +15.5    +22.1
    tape        702   159,554     180,445      +20,891         +13.1    +16.9

My proposed stopping rule was "close it if median headroom is under 5% of bank". Against a real
seller it is **16.9% to 36.5%**. The rule is failed by a factor of three to seven.

**Nearly all of it is WOOL.** $5,944 realised against $40,265 at cap 100 and $32,122 at cap 50, and
wool takes 40-80 of the 100 shed slots in every competitive best-split. Under `contrarian` wool's
headroom was $1,879.

The structural reason: the town absorbs **2,319 units a season** across all products (section 3),
and that figure is for the town, not per player. Two real farms bring ~2,400 units. On wool
specifically the town takes 228 with a yarn store and 30 without, against ~400 units of combined
supply. **The book is guaranteed to floor.** `contrarian` banks $15,900 and brings almost no supply,
so it never happened in my measurement.

## R3. The right policy

The direction of the optimum is **per-product**, and one already-computed quantity decides it:
`town_drain_remaining` versus remaining supply (`schedule_agent.py:3453`, gated at `:3461`).

- **Book recovers (`d_rem` large): HOLD HARD.** WOOL with a `YARN_STORE` drains 13/day and its
  above-`I0` curve is `sq` (`reference/kaggriculture.py:49`), so recovery from the floor is worth
  ~$200/unit. cap 40-80 in every competitive split. This is the whole $20-32k.
- **Book never recovers (`d_rem` ~ 0): SELL EARLY, ahead of the glut.** FERTILIZER's drain is
  exactly zero — no shop carries it and `TOWN_CENTER_PRODUCTS` (`:114`) excludes it — and cap0 beats
  cap100 by $2,635 (mirror 700). MELON drains 1/day and cap0 beats cap100 by $2,944.
  For these two the coordinator's "get ahead of the glut" is exactly right.

**Do not race, and do not crash a book deliberately.** We are 66% of the combined flow (1,574 to
~800), so a unit pushed into a contested book costs us roughly twice what it costs them. The
measured $3,692-to-$1,161 arm is the textbook result for the larger supplier in a common pool. It
should not be retried.

**The $1 floor is a free release valve, and this resolves the glut -> refusal -> jam chain.**
`_commit_unit:658-660` does not move the book when `price == 1`. A sale at exactly $1 therefore does
**zero** further price damage — it costs only the option value of a later recovery. Selling at $2-$50
into a crashed book is the genuinely harmful case, because that does move the book and pins it there;
that is precisely what `HOLD_A_FLOORED_BOOK`'s own evidence describes (`:3466-3480`, episode
91122388, 140 units at $1-$5).

So `RESERVATION_SELL_CAP` is **right on price and wrong on priority**. The correct order is:

1. Never let the dawn drop discard. `_drop_inventories_to_shed` (`:843`, called `:878`) destroys the
   overflow, at $221-$234/unit for the expensive products.
2. Then never sell *above* the floor into a crashed book. This is the existing rule and it is sound.
3. Then delay for the drain.

Today (1) sits below (2), and the coordinator's 1,106 solver-zone turns at shed 90-100 with zero
fills are exactly that inversion.

**The rule that fixes it, stated so it can be implemented and tested:** a shed slot has a shadow
price equal to the value of the unit it will displace — $221-$234 — *if and only if* the shed is
projected to overflow at the next dawn drop, and $0 otherwise. Hold floored stock when the shadow
price is $0. Dump it when it is not. Wool's maximum recovery gain is $198/unit by the code's own
table (`:3475-3480`), so **wool loses that comparison whenever overflow is projected**, and dumping
it at $1 to free a slot for a $234 strawberry is +$233 net and costs the market nothing.

**And cut wool production when no yarn store draws.** Section 6 stands and is strengthened: the
draw at `_end_of_day:891` is worth an $18,908 revenue swing on identical production, and no sell
rule reaches it.

## R4. What else was conditioned on the weak opponent

**Superseded — do not use:**
- The book-depth table (section 3). Those depths are a `contrarian` artefact.
- The delay-value table ($0.04-$0.38/unit/turn). At a floored book the value of waiting is the gap
  between $1 and base — up to $199/unit on wool — not $9/unit/day.
- Theorem 2(b), "later is weakly better". False against a seller. See R1.
- The $7,922 / $12,805 ceiling and the 5%-of-bank stopping rule.
- Section 7 rule 6, "lot size within a turn is a no-op". Corrected in R1; it inverts to
  "put SELLs in the earliest slots, one order per product".

**Survives, opponent-independent:**
- The section 1 framing corrections. All four are facts about source and config.
- Theorem 2(a) *as restated*, 2(c).
- Section 4, the +8% mix artefact. It is an arithmetic identity about averages and does not depend
  on the opponent at all. Still check $/unit per product, not in aggregate.
- Section 6 on wool and the yarn-store draw — strengthened.
- Section 7 rules 1-5. Rule 2's ranking must now handle both regimes: rank by
  `market_price(p, book - drain) - market_price(p, book)` still works, because for a floored
  recovering book that difference is large and for fertilizer it is exactly zero.
- The critique of `data/logs/the_sell_ceiling.log` in section 8. Its three defects are unchanged,
  and the expected-shop-draw one is now clearly the worst of them.

**Newly open, and I have not measured it:** how much of the 17-37% headroom survives a *joint*
solve over the shared 100 slots. Wool wants 40-80 of them and the day's harvest also has to fit.
That is the one number still missing, and it is the same joint-solve gap I flagged in section 5.

## R5. Corrected recommendation

Do not close the sell side. In priority order:

1. **Subordinate `HOLD_A_FLOORED_BOOK` to the dawn-overflow projection.** Highest value per line
   changed, and it is the mechanism behind the 1,106 zero-fill turns.
2. **Move SELLs to the earliest order slots.** Measured 5.5-14.2% of a turn's sell revenue,
   free, and compatible with the funding argument at `:979`.
3. **Re-run every sell arm from today against `mirror` and the tape, not `contrarian`.** Eight arms
   producing nothing is the expected result of testing them in a regime where the effect they target
   does not occur. That is a harness fault, not eight null results, and any of the eight may be live.
4. Then the joint-slot solve, to size what is left.

Every number above is 2-4 seeds against one opponent each. Seed variance on this project is ~15%
and I have not run the pool.
