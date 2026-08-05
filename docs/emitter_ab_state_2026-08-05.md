# Emitter A/B state, 2026-08-05

## The loop

    tape A  --extract-->  schedule  --emit-->  tape B

If B were A, B would score what A scores.
It does not, so every difference between the two tapes is an emitter defect.
Money is the outcome and not the target: it swings +/-40% run to run on weed and shop-unlock RNG,
and a money-scored sweep will happily pick a tape that is wrong in a profitable direction.

Scoreboards: `scripts/ab.py` (money, identical opponent and configuration) and
`scripts/tape_match.py` (per-day, per-op fidelity, which is the one being driven).

## Where it stands

    market orders   98.41%     every total exact: SELL 4427, BUY_PRODUCT 967, HIRE 306,
                               BUY_SEED 131, BUY_ANIMAL 14, BUY_LAND 2
    unit ops        72.28%
    level 1         100.00%    encode/decode
    round trip      100.00%    emit -> extract -> emit
    level 2          90.42%    router, against a tape whose own router is not shortest-path

## The remaining defect, named

**Our hands are as busy as the tape's. We use fewer of them.**

    day   A hands  B hands   A turns/hand  B turns/hand
      3        6        2         17.7         18.0
      9       12        7         21.4         19.7
     15       13       11         21.4         22.2
     24       13        9         21.5         22.3

The crew is no longer the problem -- HIRE is exact at 306/306, so B hires exactly what A hires.
The packer runs out of *tasks* before it runs out of hands, and 2-4 hired hands stand idle every day.
`_tasks_for_day` generates ~200-240 turns of work a day where the tape generates ~280.

Residual per op:

    WATER   A 851  B 713   -138
    PICKUP  A 339  B 301    -38
    DROP    A  80  B  39    -41
    HARVEST A 338  B 318    -20
    DIG     A  25  B   7    -18
    PLANT   A 131  B 115    -16
    CARE    A 308  B 354    +46
    FEED    A 319  B 356    +37

CARE and FEED are the only ops we over-produce, and they are the herd loop -- serviced on a fixed
daily cadence rather than when the animal needs it.

## Ruled out, with the measurement

- **Routing is not the gap.** 1.49 walk turns per work turn against the tape's 1.44, and level 2 is
  90.42% against a ceiling that is not ours to move: 3774 of the tape's 3775 moves changed position,
  so its detours are its own policy and not blocked ground.
- ~~**Tile placement is free.**~~ **RETRACTED 2026-08-05, later the same day.** The original
  measurement -- tape tiles $1,484 against our own $11,215 -- was taken while the emitter was
  building three of four day-0 pens on locked ground, inventing its own market book, and letting
  crops die of thirst. Re-measured after those fixes: **tape tiles $11,638 (12,669/11,097/11,149),
  ours $6,794 (10,211/10,168/2)**, with 2 refusals against our 17. The tape's tiles now win and ours
  is unstable. `_nearest_free` hands each planting the closest free tile, which scatters work across
  quadrants; it is the weak part and it is worth replacing.
- **The mix is not the gap.** His 44/21 strawberry/melon, the calculator's 48/12 and both crosses all
  banked $15-$309 at our scale.
- **Day 26 is capacity, not a bug.** 62 crop tiles and 14 pens against the 75 the farm owns on two
  parcels, 44 of them holding ongoing STRAWBERRY. We land 14 of the tape's 31-tile wheat wave.
  Making one-shot crops prefer a clearing tile over fresh ground was tried and measured: 72.28% ->
  72.24%, no change to the refusal count. Reverted.

## Defects fixed getting here, all previously silent

- `hire` written to all 24 turns emitted 96 hires on day 0 instead of 4, walked the Fibonacci ladder
  inside the day, drained $3,000 to $76, and banked $0 with an empty crew all season.
- Crew size derived from our own `want_turns`, which under-generates: 2-3 hands on days 4-7 against
  the tape's 6-8. That closes a loop -- generate too little work, hire fewer, do less.
- The whole market book was invented rather than read off the schedule: 320 units of SELL a day
  against the tape's 17-55, a third of its wheat, 23 seeds short.
- All market orders written to turn 0, past the ten-order cap (`kaggriculture.py:534`).
- `build_plan` maps unit 0 to the farmer, so `hands: 4` is five workers; reading it as four cost a
  worker every day.
- No DIG ever emitted: weeds 9 -> 17 -> 20 by day 12 while PLANT fell 9 -> 2 -> 1.
- Extracted tile positions were shifted one move (`steps[t].observation` is post-action), and again
  at every dawn boundary (`_end_of_day` teleports units home). Both were poisoning every number taken
  before they were found.
- `_axis_ops` moved X before Y; the tape moves Y first, 220 walks to 18.
- The SPAWN detour fired on routes that were never blocked, because `_path_ops` did not know which
  quadrants the farm owned.
- Draws batched into one trip out of SPAWN, where the tape draws at the shed cell it is already
  standing on -- the herd lives on those four cells, so its pickups are free.

## Next

Task generation. Not seven cadence knobs -- the tape does not run a cadence, it services whatever is
ready, and every one of our cadences was read off a season average.
