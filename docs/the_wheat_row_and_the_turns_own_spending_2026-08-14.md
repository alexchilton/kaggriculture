# Day 8's wheat row: a real 12 units, and a $9,577 fix

**Status: DIAGNOSED, FIX REVERTED, DO NOT RETRY AS WRITTEN.**
Board: kawashigi, seed 11, `scripts/breakdown.py --tape kawashigi --days 17`.

## The defect is real

`_process_market` walks a turn's order slots in order, so an order pays out of what the slots ahead
of it left behind.
The market block tracks a running `money` as it builds the queue and debits it for `BUY_LAND`,
`BUY_ANIMAL` and its own `BUY_PRODUCT WHEAT` — but **not** for `HIRE` and **not** for `BUY_SEED`.
With `HIRE_FIRST` on, both of those sit ABOVE the wheat row.

So the bank is right about incoming revenue — it carries the turn's pending sells, which is exactly
what `SELLS_FUND_THE_DAWN_PARCEL` exists to do — and wrong about outgoing spend, in the direction
that over-orders.

Day 8's row asks `buys {WHEAT: 17}`.
Probed at the block itself:

    h00  money 833  live_bank 305  quote 33  owed 17  short 17   12 orders already queued;
                                                                 block refused a slot (len < 9)
    h01  money 741  live_bank 741  quote 33  owed 17  short 17   queued LAST, behind
                                                                 HIRE, HIRE,
                                                                 BUY_SEED STRAWBERRY 4,
                                                                 BUY_SEED WHEAT 5
    h02  money  15                           owed  0  short  0

The two hires cost `fib(9) + fib(10)` = $144 and the seed $400 + $50 = $450, so $594 of the bank is
already committed and roughly $147 reaches the wheat slot.
Five units fill.

**The five that fill are not the damage.**
`state["ordered"]` is credited on the order QUEUED, and a `BUY_PRODUCT` the book refuses is silent,
so `owed` drops to 0 and the row is never re-offered — and `DUSK_FEED_TOPUP` is itself bounded by
`row_buys - ordered`, so it is dead too.
Day 8 closes `buy_product 5/17`, and on an empty shed `feed 2/10` and `care 2/10`.

The tape spends comparable money on the same day and lands all seventeen by never over-committing a
single slot: nine at h00 where only a fertilizer sell is ahead of it, then 1 at h03, 2 at h05, 2 at
h07 and 3 at h10 as the day's sales land.

## The fix works on d8 and loses the season

Debiting `money` for the HIRE and BUY_SEED orders already queued this turn
(`THE_BANK_IS_DEBITED_FOR_WHAT_THE_TURN_ALREADY_ORDERED`) does exactly what it should on day 8.
It also loses **$9,577**.

    d8 alone, after the fix: buy_product 17/17, and the row drips
                             6 at h01, 1 at h09, 1 at h10, 1+6 at h18, 1 at h19, 1 at h20

    d16 money      baseline 32,419   hire+seed debit 22,842   seed debit only 23,798   (tape 32,566)

The loss is not on day 8. It is on **day 6**, and it is identical in both variants:

    d6                     baseline        after
      money                  956/957        6/957
      hands                    4/4          2/4
      pens                     8/8          6/8
      buy_product              6/6          0/6
      buy_seed               15/15        12/15
      build_pasture            2/2          0/2
      sell                   17/17        11/17

Day 6 is the day the schedule takes the $1,000 parcel.

**The seed debit alone is enough to cause it, with hires untouched** — which kills the first theory,
that the hire path was being charged twice by its own affordability guard.
The running `money` is not a private variable of the wheat row: the land buy, the hire top-up and
the `short_of_cash` routing decision all read it, and all of them were tuned against a bank that was
never debited for seed.
Lowering it by $450 on a parcel day propagates into the routing, and day 6 sells 11 where it sold
17.

## Second attempt: local sizing. Same loss, to the dollar.

The recommendation below was tried: size only the wheat order against `money` minus this turn's
earlier spend, computed at the wheat block, **without mutating `money`**
(`THE_WHEAT_ROW_IS_SIZED_ON_WHAT_THE_TURN_HAS_LEFT`).

    exact cells of 544   baseline 385   local sizing 349
    d16 money            baseline 32,419   bank debit 22,842   local sizing 22,842

**The two implementations produce the identical season.** That is the finding, and it refutes the
diagnosis above: if the loss came from the shared bank being mutated, the local version — which
leaves `money` untouched for every other reader — would not land on the same dollar.

It does. So the cause is not the plumbing, it is the **size of the row on d6**:

    d6      hands 4/4 -> 2/4    hire 4/4 -> 2/4    pens 8/8 -> 6/8
            buy_product 6/6 -> 0/6               sell 17/17 -> 11/17

At baseline d6's over-sized wheat order **fills** — `buy_product 6/6` is exact.
Sizing it to what the turn can provably pay refuses an order the market would have honoured, and d6
is the day the $1,000 parcel is taken, so the day unwinds from there.

d8 did get what it was owed: `buy_product 5/17 -> 17/17` and `place 0/3 -> 2/3`.
It cost 47 broken cells elsewhere against 11 gained.

**Why the honest size is too small.** `money` at the wheat block already carries the turn's pending
sells, which settle in earlier slots. Subtracting the queued HIRE and BUY_SEED from that figure is
right in the slot arithmetic and wrong as a forecast, because the sells are an estimate at the
row's own prices while the hire ladder and seed are exact. The pessimism lands entirely on the
purchase and none of it on the revenue, so a turn that can in fact pay is told it cannot.

## The lesson

**A running estimate with several readers is not safe to make more accurate for one of them.**
The bank being wrong was load-bearing for three other decisions.
Correcting it in isolation is not a partial fix, it is a different global tuning — the same shape as
`HARVEST_WAITS_FOR_THE_LAST_GROWING_DAYS_WATER`
(`docs/the_last_growing_days_water_2026-08-14.md`), where one unit of yield was traded for the herd.

Both attempts so far shrank the order, and shrinking the order is what loses d6.
**Do not try a third way of sizing it.**

The one shape left is the one that changes no size at all: credit `state["ordered"]` on what
actually **FILLED** rather than on what was queued, so a row the book refuses is re-offered later in
the day. d6 keeps its over-sized order and keeps filling it; d8 keeps its over-sized order, fills
five, and re-offers the other twelve as the afternoon's sales land — which is the tape's own
cadence. No bank is read and no order is made smaller.

The obstacle is measuring the fill. `obs["private"]` carries `shed`, `seeds` and `inventories`, so
wheat holdings are visible, but wheat also arrives from HARVEST and leaves via FEED, so the day's
purchases are `(shed + carried)_now + fed_today - (shed + carried)_dawn - harvested_today` — the
same shape `SEED_ROW_IS_A_FLOOR` already uses for seed (`bought = seeds_now + planted_today -
seeds_dawn`), with one extra term. Model it on that, and dawn-latch the wheat exactly as
`state["seeds_dawn"]` is latched.
