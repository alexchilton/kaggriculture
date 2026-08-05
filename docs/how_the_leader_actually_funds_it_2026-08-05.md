# How the leader funds his farm, measured off the tape

The question that mattered all along was never "how many tiles" but "how does he pay for them".
Measured from `data/seed_scripts/new_leader/90016067.json`.

## His first fortnight

```
day  0  $3,000   BUY_ANIMALx4 BUY_PRODUCTx16 BUY_SEEDx4 HIREx4 SELLx12
day  1  $   42   <-- forty-two dollars
day  2  $  141
day  3  $  217
day  5  $  621
day  7  $1,719   BUY_LANDx1
day 10  $1,278   BUY_LANDx1     <-- a $2,000 parcel on a $1,278 dawn bank
day 11  $3,236
day 12  $6,828
day 13  $14,622
```

Three things follow, and none of them is about tiles.

**He goes all-in on day 0 and ends it on $42.** Four animals, ~51 wheat bought in small lots spread
across all 24 hours, 18 seeds, 4 hires. His day-0 SELL orders are speculative over-requests against an
empty shed and mostly no-op -- exactly like ours.

**His early revenue is FERTILIZER.** Day 1, hour 8: `SELL FERTILIZER x4`. The four day-0 animals produce
fertilizer every night, COLLECT_FERTILIZER costs no action, and he sells it daily from day 1 -- long
before milk arrives on day 8. Our own census: `COLLECT_FERTILIZER 83` against his **318**.

**He funds purchases from same-day sales.** The $2,000 parcel on a $1,278 dawn bank works because his
sells land earlier in the same day. He runs at the edge of insolvency the whole ramp; our plans hold a
minimum of $747 and finish at $38,948. We hoard, he compounds.

## Why our emitter cannot copy it (each one measured, in order found)

1. **`ranch()` raises one pen per day.** So one chain of 4 pens buys its first animal on day 0 and its
   fourth on day 3. That alone is why our day-1 bank was $2,301 against his $42 -- three of the four
   purchases had not happened yet. His shape is **four chains of several pens each, all starting day 0**:
   four animals bought on day 0, still only four hands.
2. **One chain per hand plus 20 chains = 19 hands.** Splitting pens into one-per-chain to fix (1) pushed
   the crew to 19 and the Fibonacci ladder ate the farm: final $7,923. Pen *groups* are the only way to
   get 14 pens onto ~5 hands.
3. **Unit-to-ground reachability is unchecked, and must be checked per DAY.** Units cycle NW/NE/SW/SE, so
   units 1, 2, 3 wake on tiles that are locked on day 0. Movement onto locked ground is ignored silently
   (`ops.py:86`), so such a chain emits a whole season of ops that act on the wrong tile. A replica of
   his ramp emitted 13 chains, 12 hands and 312 fertilizer sales -- and planted **zero** tiles.
   `chains.unit_can_reach()` now exists for this, but it is called with the season-end parcel count; it
   needs the count owned on the chain's *start day*.
4. **Distance, not count, sets the turn budget.** Pens sorted by distance-from-shed form a diagonal ring
   and each diagonal step costs two moves, so four such pens need 25 of 23 turns. Compact clusters fit;
   scattered ones are refused.

## What is NOT the problem

- **The emitter is not wasting the day.** Productive share of worked turns: ours 30.5%, his 34.9%
  (`scripts/diff_emitter_vs_leader.py`). He walks enormously too -- 4,120 movement ops against 2,438
  productive. The gap is pure quantity: 18 useful ops a day against his 81.
- **The land gate is not wrongly refusing SW.** Forcing the second parcel through was tested: `quads`
  stayed at 2 because `_do_buy_land` no-opped for want of money, and the attempt starved a pen
  ($38,948 -> $3,943). We are genuinely too poor. The flat-price fix in `PRICE_BASE` is still worth
  doing, but it is not the root cause, and an earlier claim in this project's notes that it was is wrong.
- **Market timing is not the edge.** Shifting only the sell days moves money at most +3.6% and the win
  rate not at all.
- **Wheat is not arbitrage.** He buys 967 at mean $44.96 and sells 1,131 at $46.49 -- a 3.4% spread. 319
  units go to FEED. He buys feed instead of growing it, which `ranch(buy_feed=True)` already does.

## The order to fix it

1. Make `unit_can_reach` day-aware and call it with the parcels owned on the chain's start day.
2. Let the genome express **several multi-pen chains starting on day 0**, so day 0 buys four animals on
   four hands. This is the single change that reproduces his cash curve.
3. Sell fertilizer daily from day 1 (`collect_fertilizer` + `sell_fertilizer` already exist; the search
   does not choose them -- our 83 collections against his 318).
4. Only then widen the board: more slots, second parcel, southern half.
