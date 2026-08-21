# BRANCH B: the executor cannot play a row it was handed, and it misses from d0

Measured 2026-08-21. Answers Alex: *"strange that it cant match the d3 -12..."*

He was right to be suspicious, and the modal-row run could not answer him. That run played the MODAL
row every day, and game 92498144 is only the modal season on d0, d1, d2 and d4 -- so "d3-d12 does
not match" meant "we chose a different plan", and nobody had tested whether the executor could play
*his* plan if handed it.

**It cannot. Not one of the thirteen days is exact, and the first divergence is d0.**

    scripts/can_the_executor_play_his_own_row.py --seed 11 --days 13
    scripts/what_the_day_did_hour_by_hour.py     --day 0  --seed 11

Setup: game 92498144's own d0-d12 target rows fed to the same executor, same seed 11, same injected
shop draw, `townCenterSellInterval 24`, weeds 0.0. His rows go through
`kawa_rows.only_animals_get_placed` exactly as the modal rows do, so this is not the `places`
extractor defect firing.

**This is NOT the op replay.** Replaying his ACTIONS reproduces his board exactly to d11; that is
established and it is a different test. An action is a 24-turn op tape carrying hours, coordinates,
movement and WATER. A target row has none of those and our router regenerates all of them. The op
replay passing said nothing about whether the ROW round-trips, and it does not.

## The grade

    per-day differing cells (exempt: DROP, EAST, NORTH, PASS, PICKUP, SOUTH, WEST)
      d0=6  d1=5  d2=2  d3=4  d4=4  d5=7  d6=10  d7=12  d8=19  d9=15  d10=18  d11=16  d12=14
    0/13 days exact

Days are graded IN ORDER, so **d0 is the day to fix**. Everything after it inherits d0's board and
d0's bank, and the divergence grows monotonically from d5 on.

## d0, hour by hour. The defect is one turn.

     h0   ours  $3000 -> BUY_PRODUCT WHEAT x9  +  five HIREs
          tape  $3000 -> five HIREs  +  all nineteen seeds
     h1   ours  $7    -> SELL WHEAT x3, BUY_SEED MELON x1, BUY_SEED WHEAT x1
          tape  $13   -> SELL WHEAT x3
     h2   ours  $6                                tape  $100
     h6   ours  $6                                tape  $100 -> BUY_PRODUCT WHEAT x2
     h12  ours  $6                                tape  $44  -> BUY_PRODUCT WHEAT x1
     h23  ours  $6                                tape  $16

**From h2 to h23 -- twenty-two consecutive turns -- we emit `BUY_SEED WHEAT x1` and it never fills,
because a WHEAT seed costs $10 and the bank holds $6.**

The row's `buys` is a **day total with no cadence in it**. A target row has no hours, so the executor
chooses the turn, and it chooses the first one -- putting a nine-unit product order in front of the
seed the ground is waiting for. Kawashigi buys his seed at h0 and spreads the product over h6 and
h12.

Every field that differs on d0:

    state  money            ours        6   tape       16   -10
    state  crop_WHEAT       ours        6   tape        7    -1
    op     PLANT            ours       18   tape       19    -1
    op     WATER            ours       18   tape       19    -1
    fill   BUY_PRODUCT      ours        9   tape        8    +1
    fill   BUY_SEED         ours       18   tape       19    -1

One plant short, and $10 short -- exactly one wheat seed.

## This is a known failure family

`schedule_agent.py:4860` already documents the same shape with a different competitor for the same
dollars: BUY_ANIMAL outranking BUY_SEED, answered by `SEED_BEFORE_LIVESTOCK`.

> "ours h1 BUY_SEED MELON 6, BUY_SEED STRAWBERRY 8 -> four melon, no strawberry at all ... A
> BUY_SEED fills only what the bank covers ... He defers the cows himself, to hour 2. This does not
> say animals are a bad buy; it says the seed is due first on the day the ground is waiting for it."

Same argument. BUY_PRODUCT is simply not in that ordering.

Pinned by `tests/test_the_seed_order_outranks_the_product_order_at_dawn.py`, `xfail(strict=True)` --
recorded and unfixed, and it flips the moment somebody fixes it. **Not fixed here**: the fix is a
change to dawn market-order priority, which is a different piece of work from the run that found it.

## What the $10 becomes

    d0   one plant short, $6 against $16
    d5   sell 13 against 23
    d6   money $16 against $957
    d8   crew 3 against 11 -- `_do_hire` fails SILENTLY on a thin bank
    d10  crew 5 against 11, water 3 against 32, unit-turns 139 against 270
    d11  thirteen weeds against his zero

The weeds are the tell the previous block-agent attempt also showed, but the cause is different:
there it was a literal op tape watering the wrong tiles, here it is a crew that could not be hired
because the bank was stranded on turn one. `reference/kaggriculture.py:771` -- two days unwatered
makes a WEED, and `weedSpawnChance` is 0.0 on this run, so all thirteen are our own missed waterings.

Never call the d0 gap small. $10 on turn one is thirteen weeds and half a crew by d11.

## The fork, resolved

**BRANCH B.** The executor does not reproduce a row it was handed.

**Do NOT build the d7-d13 selector.** A selector chooses which row to play; it cannot make the
executor play one. The 17-25% modal coverage measured yesterday is real, and it is not the binding
problem -- feeding the *perfect* row for d0-d12 still produces 0/13 exact days and leaves us $8,415
behind at d12 ($7,150 against $15,565). Selection was worth $4,644 by d13; execution is worth more
than that on its own.

The order is: fix d0, re-grade, then the next divergent day, and only reopen selection when the
executor round-trips a row it is given.

## Unverified

- One seed, one game, one tape. d0's defect is arithmetic and seed-independent, but the size of its
  consequences at d8-d11 is measured once.
- Whether fixing dawn order priority makes d0 exact, or merely closer. The $10 and the one plant are
  what the trace shows; whether `WATER 18/19` follows from the missing plant or is separate is not
  established.
- d1-d12 have their own defects on top of d0's inheritance. `d2=2` is the smallest and may be the
  cheapest second target, but nothing here separates a day's own fault from what it inherited.
- Weeds 0.0 throughout. The ladder runs 0.005.
