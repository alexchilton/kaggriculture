# d0-d3, cell by cell

**0 of 4 exact by the grid's own count. d0 is exact in BOARD AND SHED — its three cells are two
netting artifacts and the $3 of price impact they cause. d1, d2 and d3 are diagnosed, not fixed.**

Setup: game 92498144's own d0-d12 rows, seed 11, injected shop draw, weeds 0.0, seed-first ordering
AND netting both in place. `scripts/can_the_executor_play_his_own_row.py --detail 4`.

    per-day differing cells
      d0=3  d1=3  d2=1  d3=4   (then d4=3 d5=7 d6=16 d7=13 d8=19 d9=14 d10=17 d11=17 d12=13)

## d0 — 3 cells, and the board is identical

    state  money              ours       13   tape       16   -3
    fill   SELL               ours        0   tape        3   -3
    fill   BUY_PRODUCT        ours        5   tape        8   -3

Verified rather than argued (`scripts/d0_shed_check.py`):

    end of d0, ours/tape
      shed_WHEAT         3/3
      shed_MILK          0/0
      shed_WOOL          0/0
      shed_FERTILIZER    0/0
      net wheat traded   ours +5   tape +5

**Every board and shed quantity matches.** The two op cells are exactly the round trip netting
removed: he buys 8 and sells 3 for a net of +5; we buy 5 and sell 0 for a net of +5. Op-for-op
grading scores the redundant round trip as correct and its removal as two misses.

**These two are expected-different and should not be chased.** The `money -3` is their consequence,
not a separate defect: three fewer touches of the book means a different realised price on the same
net units. It is not inherited by d1 as an error — d1's own trade matches exactly (`BUY_PRODUCT 5/5`,
`SELL 3/3`) and the -$3 simply rides along.

If d0 is wanted green on the grid, netting has to come out; it cannot be both.

## d1 — 3 cells. The defect is fertilizer cadence.

    state  money              ours      168   tape      171   -3      (inherited from d0)
    op     COLLECT_FERTILIZER ours        4   tape        3   +1
    op     PLACE              ours        3   tape        1   +2

    end of d1  shed_FERTILIZER  ours 1 / tape 0

Hour by hour, `scripts/what_the_day_did_hour_by_hour.py --day 1`:

    ours   h3  COLLECT_FERTILIZER
           h4  PLACE FERTILIZER   +  SELL FERTILIZER x1
           h9  COLLECT_FERTILIZER
          h11  PLACE FERTILIZER   +  SELL FERTILIZER x1
          h15  COLLECT_FERTILIZER
          h17  PLACE FERTILIZER   +  SELL FERTILIZER x1
          h22  COLLECT_FERTILIZER  <-- never disposed of; ends in the shed

    tape  h11  COLLECT_FERTILIZER
          h13  COLLECT_FERTILIZER
          h15  COLLECT_FERTILIZER
          h18  PLACE FERTILIZER   +  SELL FERTILIZER x3  +  BUY_PRODUCT WHEAT x5

**We dispose of fertilizer one unit at a time, as each is collected. He accumulates three and
clears them in a single PLACE and a single SELL x3 at h18.** Three PLACE ops where he spends one, so
two unit-turns are burned on drops; and the fourth collection at h22 has no turn left to dispose of
it, which is the `shed_FERTILIZER 1/0`.

`PLACE` here is the shed-drop form, not an animal placement — the same op conflation that produced
the `KeyError: 'FERTILIZER'`. `only_animals_get_placed` cleaned the ROW; these PLACEs are generated
by the executor from the live board, so the filter does not reach them.

The mechanism to name for the fix: **the drop of a collected product should be batched to one trip,
not emitted per unit.** Not fixed here.

## d2 — 1 cell

    state  money              ours       44   tape       42   +2

The cheapest diagnostic on the board, as asked. Every op, every crop, every shed level and the herd
all match. It is money only, and the sign FLIPS from d0 and d1's -$3 to +$2, so it is not simply the
d0 trail carried forward — something on d2 earns $5 more than his does, or costs $5 less.

**Not isolated.** d2 emits no SELL on either side and `BUY_PRODUCT` is 4/4, so it is not a trade
count; it is a realised price or a fill the grid aggregates. A turn-level cash trace of d2 has not
been taken and is the next cheapest thing to do in this whole problem.

## d3 — 4 cells

    state  money              ours       23   tape        1   +22
    state  crop_WHEAT         ours        0   tape        7   -7
    op     HARVEST            ours        7   tape        0   +7
    fill   BUY_SEED           ours        0   tape        1   -1

**We harvest seven wheat tiles on d3 that he leaves standing.** His board ends d3 holding 7 wheat;
ours ends holding none. That is one decision, not four cells — the harvest, the crop count, the $22
it banks and the seed he buys and we do not all follow from it.

WHEAT is `first_yield_day 2, max_yield_day 4`, so a tile planted on d0 is harvestable on d2-d4. He
waits; we take it as soon as it is ready. d3 is also the melon/strawberry split day
(`kagg/search/melon_branch.py`), so this is the wrong day to be diverging on.

Not diagnosed further — d0-d2 come first.

## What I did not do

No fix was written for d1, d2 or d3. I traced d0 and d1 to the turn, named d1's mechanism, and
reported d2 and d3's cells without isolating them. Nothing was reverted, disabled or flag-gated, and
`tests/test_each_day_matches_the_tape.py` was not run.

## Unverified

- One seed, one game, one tape.
- d2's $2 is unexplained. I have not ruled out that it is a fill the grid buckets differently rather
  than a real cash difference.
- d1's fertilizer batching is read off one day's trace. Whether the same dribble happens on other
  days is not measured, though `COLLECT_FERTILIZER` failing on 13 days of the shipped gate suggests
  it is not confined to d1.
- Whether batching the drop actually makes d1 exact, or merely removes two cells and moves the miss.
