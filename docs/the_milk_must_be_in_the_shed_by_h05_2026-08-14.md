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

## One hand per ripe pen: `ONE_HAND_PER_FUNDING_PEN`

The tour ORDER was never the defect, and neither was the flag. Reading the work sequence `cover`
hands each unit on d8 -- remembering that `schedule_agent_1455mh:3809` builds task tiles as `(x, y)`
while the board is `(y, x)`, which cost one wrong diagnosis in this session:

    u4  0. (4,4) [FEED, CARE, COLLECT_FERTILIZER, HARVEST]  4t  funds   <== ripe cow
        1. (4,3) [FEED, CARE, COLLECT_FERTILIZER, HARVEST]  4t  funds   <== the OTHER ripe cow

Both ripe pens correctly flagged `funds`, both at the FRONT of the tour -- and BOTH ON ONE HAND.
Eight turns of work back to back, so the second cow cannot be banked before ~h08. The tape puts one
hand on each. `greedy` ranks on `(added turns, unit, tile, index)`, pure cheapest-insertion, so
appending the second cow to the hand already standing on the first always wins.

The fix is a preference inside that ranking, never a refusal. **It also has to be repeated in
`COMPACT`**, which accepts any relocation that lowers total turns and silently stacked them back --
the spread survived `greedy` and vanished before the tour was built.

    baseline      exact 447/697   d16 32,419
    bank only     exact 465 (+18) d16 31,321 (-1,098)
    split only    exact 468 (+21) d16 31,888 (-531)
    split + bank  exact 465 (+18) d16 31,321 (-1,098)   BYTE-IDENTICAL to bank alone

**The two are not complementary.** With the banking flag on, the split is a no-op: once each funding
pen needs its own depot stop, stacking them is already the expensive option and `greedy` separates
them without being asked. Two routes to the same assignment.

d0-d7 are byte-identical to baseline across all 41 rows, so nothing regresses in order. The herd
goes exact from d10 (`animals 13/14 -> 14/14`, d10-d16) and the first cow's harvest moves h05 -> h03.

**d8's target cells do not move in ANY arm**: `buy_product 5/17`, `feed 2/10`, `care 2/10` are
identical in all four. The milk is still not in the shed by h05 -- u1's cow is job 1 on its tour,
behind an at-risk pen it must feed to keep the animal alive, so it harvests at h10.

## Next

1. The remaining d8 gap is the WHEAT ROW, not the milk -- `HIRE_FIRST` puts nine hires ahead of it
   at h00, and `state["ordered"]` is credited on the QUEUE so a refused order is never re-offered.
   Fix the credit first; it is the only one of the three that changes `buy_product 5/17`.
2. Only then is it worth asking whether a `funds` pen should outrank an at-risk pen on the same
   hand -- that trade is an animal's life against the day's cash and must not be guessed at.

Do NOT reopen: the herd mix, d8's routing/job list (`crew.cover` covers 39/39), or sizing the
wheat row.
