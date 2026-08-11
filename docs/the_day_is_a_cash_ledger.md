> **TARGET SUPERSEDED, added 2026-08-11.** The day being diagnosed here is built to fund Seb's tape,
> which was optimal under the OLD `townCenterSellInterval=12` economy. His median bank halved and he
> has since withdrawn from the ladder (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats). The
> `short_of_cash` bug described below is still a real bug in the ledger logic — only the schedule it
> is funding is now known to be a suboptimal target.

# Step 1 is a ledger, not a flag

Alex, 2026-08-10, correcting the `sell_deadline` design I built the same day.

## What is wrong

`schedule_agent_1455mh.sell_deadline(hour, selling, short_of_cash)` returns **one hour**, and
`short_of_cash` is **one boolean** over the whole day's bill:

    short_of_cash = FUND_THE_DAY_WHEN_SHORT and any(owed_sale.values()) and _days_bill(row) > money

On day 4 that reads:

    cow    400   needed at h0    <- covered by the $480 dawn bank, needs no sale at all
    land  1000   needed at h21   <- the only thing the day's produce has to fund
    hires   33   h0
    wheat  ~28   h0
    ----------
          ~1461  vs $480         ->  short_of_cash = True  ->  due = 0, rush = True

So a purchase that is not due until h21, and a purchase that is already paid for, are added into
one number and turned into "deliver everything at hour 0". That is what forces the rush on d4.

## What the day actually is

Read off tape 91422988, day 4, Seb's own seat. Four sell waves, three buy points:

    h0    BUY_ANIMAL COW       -400      from the dawn bank
    h0    HIRE x7               -33
    h2    BUY_PRODUCT WHEAT    ~-28
    h18   SELL WHEAT 5         +165
    h21   SELL FERTILIZER 5, SELL WHEAT 12
    h21   BUY_LAND            -1000      funded by the two SELLs in EARLIER ORDER SLOTS of this turn
    h22   SELL WHEAT 12        +239
    h23   SELL WHEAT 20, SELL FERTILIZER 1

He sits on $12 from h2 to h18 and it costs him nothing, because nothing he owes is due before h21.

Ours, same day, same board:

    h0    BUY_ANIMAL COW, BUY_PRODUCT WHEAT      $480 -> $15 by h2
    h6    SELL FERTILIZER 1, SELL WHEAT 1
    h7    SELL WHEAT 1
    h14   SELL WHEAT 8
    h16   SELL WHEAT 16
    h18   BUY_PRODUCT WHEAT 5                    -$154
    h19   SELL WHEAT 5
    h21   SELL FERTILIZER 2, BUY_LAND            -> $115
    h22   --
    h23   --                                     dusk $115 against his $1115

Two differences, both caused by the scalar: we sell early and small into a book that has not
recovered, and we stop selling the moment the parcel is bought while he sells 12 more at h22 and 21
more at h23.

## The shape step 1 should have

Emit a **ledger**, at dawn, from the row and the live bank:

1. **Dated obligations.** `[(hour, cash)]`, one per thing the row buys, at the hour it is bought.
   Animals and hires are h0. Land is its own hour. Feed and seed buys are theirs.
2. **Opening balance.** The live bank, not the row's `money_dawn` (that is a different farm's).
3. **The shortfall curve.** Walk the obligations in hour order against the balance. The first hour
   the running balance goes negative is the first hour the day genuinely needs a sale, and the
   deficit at that hour is how much. Everything before it needs nothing.
4. **Delivery obligations.** Turn each deficit into "this many units of this product in the SHED by
   this hour" at the prices the row implies. That is what routing needs -- it is `cover`'s `due`,
   but as a small list, not an int.
5. **Sell waves.** Spread the sells so the book recovers between them, and keep selling after the
   last purchase. `market_price` falls as town inventory rises; measured, landing a load in two DROP
   waves banked **$542 for 54 units** where four waves banked **$774 for 41**.

Day 4 under that model asks for nothing before h21, then $1000 by h21, then sells the remainder at
h22 and h23. Which is the tape.

## Why `feed 6/7` and `care 6/7` are downstream of this

The cow lands at h0 and takes the bank to $15 by h2. The seventh animal's wheat is then unaffordable
for the rest of the morning, so it is neither fed nor cared for. That row is a cash-sequencing
failure, not a routing failure, and no amount of lane cutting will close it.

## Measured, so it is not re-derived

- Staggering the hires to keep hands off `(5,5)` is a LOSS on day 4 and the reason is in
  `_arrival_plan`'s docstring. Baseline d4 matches `water 17/17`, `harvest 14/14`, `place 1/1`;
  with staggering those go to 16/17, 12/14, 0/1. Two boxed hands cost d4 nothing measurable,
  because six seats already covered every tile.
- The tape boxes hands too: Seb's `u2` and `u6` sit on `(5,5)` doing nothing on d0, d1 and d3, and
  one of them on d2 and d4. It stops at d5, when he owns a second quadrant.
- `_days_bill` does count the cow. The bug was never a missing term; it was adding terms with
  different due dates together.
