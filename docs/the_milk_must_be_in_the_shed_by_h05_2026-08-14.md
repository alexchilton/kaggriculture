# Day 8: the milk must be in the shed by h05, and the pen IS the shed

Board: kawashigi, seed 11, `scripts/breakdown.py --tape kawashigi --days 17`.
Supersedes the "first milk day" section of `the_wheat_row_and_the_turns_own_spending_2026-08-14.md`,
which was right that d8 is the first milk day and wrong about what to do with that.

## The decisive measurement

Forcing the tape's EXACT d8 orders -- buys and sells together -- with the milk banked six hours
earlier than baseline changes **nothing**:

    d8                forced + early milk    forced (before the fix)    baseline
    sell                    6/18                    6/18                 18/18
    buy_product            10/17                   10/17                  5/17
    feed                    9/10                    9/10                  2/10
    care                    9/10                    9/10                  2/10
    + sold              $524/$3,177             $524/$3,177          $3,220/$3,177

Byte-identical. His `SELL MILK 12` is at **h05**; the fix put our milk in the shed at **h07**.
Two hours late fills exactly as much as thirteen hours late: zero.

**"Earlier" is not the requirement. "By h05" is the requirement.**

## His plan, read off the raw replay

Positions come from the replay observations at seat 0, not inferred from the action stream.
His two ripe cows at d8 dawn are `CO@4,3 y6` and `CO@4,4 y6`; the other seven animals hold nothing.

    u4  <== STARTS ON A RIPE PEN
        h02 (4,4) PICKUP/WHEAT   h03 (4,4) FEED   h04 (4,4) CARE
        h05 (4,4) HARVEST        h06 (4,4) PLACE/MILK
    u0  <== STARTS ON A RIPE PEN
        h01 (4,4) PICKUP/WHEAT   h03 (4,3) FEED   h04 (4,3) CARE   h05 (4,3) COLLECT_FERTILIZER
    u2  h04 HARVEST              h06 (4,4) PLACE/MILK

Three things, and the third is the one that matters:

1. **The ripe pens are the day's FIRST work** for two units, not work they reach mid-tour.
2. **Every op on a pen happens in consecutive turns on that tile** -- PICKUP, FEED, CARE, HARVEST,
   PLACE, one after another, no revisit.
3. **He banks from the pen tile itself.** `_refresh_pins` sites pens ON shed-access tiles, so
   `PLACE/MILK` at (4,4) costs one turn and zero walking. He never makes a trip. The pen IS the
   depot.

## Ours, the same day

    u4  FEED h02   CARE h03   COLLECT_FERT h04   HARVEST h05   ...   DROP h07
    u1  ...                                      HARVEST h11         DROP h12

We have his shape on the first pen and then lose two turns delivering, and eight turns reaching the
second pen. The second cow is the bigger half.

## Why the delivery flag was not enough

`BANK_THE_ROWS_PRODUCE_WHILE_REAPING` (`kagg/search/cover.py`) lets a hand bank produce the row is
selling at a zero-detour depot while harvests remain, gated on `rush` AND on the hand carrying what
`wanted` names. Measured on the 17-day grid:

    exact cells   447 -> 465  (+18)      d16 money   32,419 -> 31,321  (-$1,098)
    animals d10-d16   13/14 -> 14/14     feed/care d11-d16  13/14 -> 14/14
    d9 sell 22/25 -> 17/25               d10 sell 78/91 -> 69/91
    d8 buy_product 5/17, feed 2/10, care 2/10   -- UNCHANGED

It moves the milk h17 -> h07 and four wheat buys out of h18 into h08-h11, which is a real timing
gain, and it makes the herd exact from d10. It does not reach h05 and it does not move d8's target
cells, so it is shipped **False** pending the two changes below.

## Timing is the thing that is not matched

Daily fill COUNTS hide this completely -- d8 reads `sell 18/18` in the baseline with the orders
thirteen hours out of place. Fills stamped with the hour, ours vs his hour-stamped asks:

    d8   h00  OURS S-FERTx6                  TAPE B+WHEAx9 S-FERTx6
         h05  OURS -                         TAPE B+WHEAx2 S-MILKx12
         h08  OURS B+WHEAx1 S-MILKx6         TAPE B+WHEAx2
         h13  OURS S-MILKx6                  TAPE -

    d9   OURS h01 B+WHEAx11 S-FERTx9   h02 S-WHEAx8   h18 S-WOOLx5
         TAPE h00 S-FERTx6 S-WHEAx8  h01 S-FERTx3  h03 B+WHEAx2  h06 B+WHEAx2 S-WOOLx4
              h07 S-WOOLx4  h10 B+WHEAx2  h12 B+WHEAx3  h17 B+WHEAx2

    d10  OURS h01 B+WHEAx33  h02 S-FERTx10 S-WHEAx22  then nothing until h16
         TAPE h03 B+WHEAx7  h10-h19 S-FERT in blocks of 18, B+WHEA at h14/h17

**We transact in one early block and then go quiet; he trickles all day.** That is systemic and
bigger than d8.

Two separate causes on d8, both visible above:

- `HIRE_FIRST` puts NINE hires in the h00 block ahead of the wheat, so we buy 0 wheat at h00 where
  he buys 9 -- funded on a $5 bank by the `SELL FERTILIZER 6` sitting in an earlier slot of that
  same turn. He hires 11 too, but 5 at h00, 5 at h01, 1 at h05.
- `state["ordered"]` is credited when an order is QUEUED, so the twelve units the book refused at
  h01 drive `owed` to 0 and the row is never re-offered, however much money lands later.

## Next

1. **Both ripe pens are the first stop for two units, all ops in one visit, bank on the tile.**
   `Job.funds` already marks them (`rush` is True on d8 and the row owes MILK) but it orders the
   ASSIGNMENT, not the position within each unit's tour -- which is why u1 reaches its cow at h11.
2. Then credit `state["ordered"]` on the FILL, so the wheat row re-offers as the milk money lands.
3. Then re-measure `BANK_THE_ROWS_PRODUCE_WHILE_REAPING` on top of both.

Do NOT reopen: the herd mix, d8's routing/job list (`crew.cover` covers 39/39), or sizing the
wheat row.
