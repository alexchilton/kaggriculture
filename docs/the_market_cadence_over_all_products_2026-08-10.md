> **TARGET SUPERSEDED, added 2026-08-11.** Measured against Seb's tape (`91422988`), optimal under
> the OLD `townCenterSellInterval=12` economy. His median bank halved and he has since withdrawn from
> the ladder (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats). The hour-cadence mismatch
> found below is still real — the target it is measured against is now known to be suboptimal.

# The market cadence, over all products

Measured 2026-08-10, seed 11, tape `91422988`, crew planner on d0-d6.
Ours is **exact fills** diffed out of `record_fills` after every step — what committed, not what was
offered.
His is the `orders` field of the derived schedule, `[hour, op, item, qty]`, read straight off his
replay.
Raw log: `data/logs/cadence_all.log`.

Both sides trade roughly the right quantities.
The hours are wrong, and they are wrong in the same direction on every product.

## The table

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

## Three defects, all general, none product-specific

### 1. The carry dumps at hour 0

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

### 2. Sells fire in the morning; his fire in the evening

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

### 3. Buys are front-loaded into a block; his drip

d0 is the extreme case — identical quantity, opposite distribution:

```
  ours  h01 h02 h03 h04 h05 h06 h07 h08     eight consecutive turns
  seb   h05 h07 h09 h11 h12 h14 h17 h19     spread across fifteen
```

`BUY_DRIP` exists for this and meters one unit per turn, but it starts at h00 and runs out by h08.
The shops restock every 4 steps, so his spacing buys each unit into a restocked book and ours
buys the second half into a book its own first half has already lifted.

## What it costs, where it has been priced

- **The d6 land parcel.** He sells `WOOL 6` at h09 and `WOOL 6` at h13, taking his bank
  $5 → $1,349, and buys the parcel at h13.
  We sell `WOOL 1` at h07 and `WOOL 5` at h19, hold $47 at h13, and do not reach $1,400 until h23.
  Same twelve units, ten hours late, and `buy_land 0/1` on d6 follows from it.
  This is why the crew planner reads as costing the parcel; it does not.
- **d4's wheat.** `h16x25` in one order against his `h18x5 h21x12 h22x12 h23x20`.
  `market_price` falls per unit *inside* a single order, so a 25-lump clears at a materially worse
  mean than four blocks across four turns with restocks between them.

## What has NOT been measured

Whether moving our sells later is worth it in money.
Every number above is a timing observation.
The obvious experiment — a `SELL_AFTER_HOUR` floor, and denying the carry hour 0 — is unrun.
Note that `docs/` already records two occasions where a cadence change that looked obviously right
measured as a loss, so this gets a grid before it gets an opinion.
