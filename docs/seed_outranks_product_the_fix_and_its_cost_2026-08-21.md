# BUY_SEED now outranks BUY_PRODUCT — and it costs 38 cells on the standing tape gate

**Read this first: the fix regresses `tests/test_each_day_matches_the_tape.py` from 263 failing
cells to 301.** It was asked for, it does what it was asked to do, and it makes the shipped agent's
own gate worse. That is a decision for Alex, not for me, and nothing is reverted or disabled.

## The change

`schedule_agent._wheat_row_first` moved hour 0's `BUY_PRODUCT WHEAT` in front of the first
`HIRE`/`BUY_ANIMAL`/`BUY_SEED`. It now clamps that insertion point to sit **after the last
`BUY_SEED` in the same turn**. Days with no seed order that turn are untouched, so the Victor
measurement in that function's own docstring still holds wherever seed is not competing.

The ten slots at d0 h0, seed 11, on game 92498144's own row:

    ours (before)  PRODUCT WHEAT 9  HIRE x5  COW 2  SHEEP 2  SEED MELON 12  SEED WHEAT 7
    tape           HIRE x5  COW 2  SHEEP 2  SEED WHEAT 7  SEED MELON 12  PRODUCT WHEAT 6

$3,000 does not cover $225 of product, $1,800 of livestock and $1,030 of seed together, and
`_do_buy_product` re-checks the bank per unit, so whichever slot runs first is paid in full.

`tests/test_the_seed_order_outranks_the_product_order_at_dawn.py`: xfail marker removed, 2 passed.
Confirmed red on revert — the same test xfailed (i.e. failed) against the stashed file.

## What it bought, d0-d12 on his own rows

    per-day differing cells      total
    before  d0=6 d1=5 d2=2 d3=4 d4=4 d5=7 d6=10 d7=12 d8=19 d9=15 d10=18 d11=16 d12=14   132
    after   d0=2 d1=5 d2=1 d3=6 d4=3 d5=4 d6=13 d7=11 d8=16 d9= 9 d10=16 d11=10 d12=10   106

    money at d12   before  7150/15565      after  12666/15565     +$5,516
    weeds at d11   before    13/0          after      6/0
    d0 PLANT       before    18/19         after     19/19
    d0 BUY_SEED    before    18/19         after     19/19

**d0 is still NOT exact.** Two cells remain, and they are the opposite sign to the original defect:

    state  money        ours  100   tape  16   +84
    fill   BUY_PRODUCT  ours    5   tape   8    -3

Having stopped the product order from eating the seed money, it now under-fills by three units and
the day closes $84 rich. The $10 was necessary and not sufficient, exactly as anticipated. The
product order is last in the slot list and takes only what the seeds and livestock leave.

**Next divergent day: d1, 5 cells.** Its own trace was not taken — d0 is still not exact, and days
grade in order.

## The cost

    tests/test_each_day_matches_the_tape.py    baseline  263 failed / 517 passed
                                               with fix  301 failed / 479 passed

Thirty-eight cells flipped from pass to fail. That gate drives the SHIPPED agent —
`schedule_agent` on `kagg/plan.py`'s schedule, which is a *different* Kawashigi season from
92498144. So the ordering that rescues one recorded row costs the season we currently ship.

Baseline was measured once, by stashing only `kagg/search/schedule_agent.py` and re-running the same
file; the post-fix number was measured twice (301 both times, once alone and once alongside the
other suites). The gate was already 263-red before any of this work.

Two readings, and this measurement does not separate them:

1. The ordering is right and the shipped season's grid was passing for the wrong reason — it was
   tuned against an executor that front-loads the product order.
2. The ordering is player-specific. Victor puts the product first, Kawashigi puts it last, and there
   is no single answer that serves both.

Reading 2 is what the two docstring measurements literally say, and it is the more likely one.

## Recommendation

Do not ship this as it stands. The options, none of which I took:

- Keep it, and re-tune the shipped grid against the new ordering. The $5,516 at d12 says the
  ordering is worth something; 38 cells says something else was resting on the old one.
- Revert it, and accept that the executor cannot round-trip a row whose player orders seed first.
- Neither is a flag. If both orderings are genuinely needed, the honest form is a property of the
  ROW (whose season it came from), not a boolean on the module.

## Part 2 is NOT started

The instruction was: do not rebuild the library smaller until the executor round-trips a row.
**It still does not — 0 of 13 days are exact.** d0 is two cells away and d6-d12 are 9-16 cells
each. Measuring a 2-3 row library on this executor would tell us nothing, which is the reason the
precondition was set.

## Unverified

- One seed, one game, one tape, for both the gain and the regression.
- Whether the 38 regressed cells are concentrated on one day or spread. Not broken down.
- Whether d0's remaining `BUY_PRODUCT 5/8` is a slot problem or a quantity problem. The row asks
  for 9; he filled 8; we fill 5.
- The gate baseline (263) was measured once.
