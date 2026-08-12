# The late season is one defect in two halves, and neither half pays alone

2026-08-12. Measured, seed 11, tape victor. **Both halves are currently UNFIXED** — the first was
written, measured as a loss on its own, and reverted. Do not re-derive either from scratch.

## What the season looks like

State rows match the tape all the way to d24 — same land, same pens, same herd. Then:

    weeds    d24 1/1   d25 6/0   d26 7/0   d27 14/0   d28 17/1
    wheat    d24 43/44           d26 38/54          d28 17/23

Cumulative flow rows, where each stops reconciling:

    fertilize  127/71   +56   breaks at d23   <- the only row where we do MORE
    harvest    322/360  -38   breaks at d25
    plant      182/194  -12   breaks at d26
    water      906/965  -59   breaks at d26

## Half one: a DIG clears ground and nothing plants on it

`DIG` sets the cell to `None` (`kaggriculture.py:477`) exactly as a one-shot HARVEST does
(`:454-455`), and it is how `DIG_A_SPENT_ONGOING_CROP` clears a finished strawberry.
`REPLANT_A_CLEARED_TILE` chains a planting onto the HARVEST case and **not** onto the DIG case, so a
day that demolishes ground plants nothing on it — `_refresh_pins` only sites a PLANT on ground empty
at DAWN, and this ground does not exist until the day makes it.

Seed 11, d26, with d12-d25 solved: the schedule row asks for eleven WHEAT, the pool contains
`HARVEST/DIG x 11`, and PLANT ops offered = **0**. Live on the ladder in episode 92433651 the same
day dug 13 tiles and planted none.

This is the fourth instance of a pattern already fixed three times — `BUILD_THEN_PLACE`,
`PLANT_THEN_WATER`, `REPLANT_A_CLEARED_TILE` — all with the same one-line statement:
**the board the plan reasons about must be the board the day will have.**

**Fixed, measured, REVERTED.** Extending `REPLANT_A_CLEARED_TILE`'s condition to
`any(o == "DIG" ...) or (not ongoing and HARVEST in ops)` passed a four-test unit suite and went red
on revert. On the grid, routes off both sides, control -> fixed:

    money    d24 53031->51523   d26 56453->55259   d28 62743->59845   -$2,898
    weeds    d26  9/0 -> 2/0    d27 13/0 -> 7/0    d28 13/1 -> 7/1
    harvest  d23 23/25->18/25   d27 24/28->21/28
    plant    d26 0/11 -> 0/11   THE TARGET CELL DID NOT MOVE

Fewer weeds, less money, and the day it was written for is untouched — because of half two.

## Half two: `plant_prize` is zero from d26, so nothing is eligible to chain

    plant_prize('WHEAT', 25) = 75.0
    plant_prize('WHEAT', 26) =  0.0

`plant_prize` returns 0 when `days_left < info["max_day"]`, and the docstring is explicit about why:
a one-shot pays only through a HARVEST, and `_one_shot_is_finished` only offers one **once the yield
window has SHUT**. A wheat planted d26 reaches age 4 on d30, past the end, so under our own harvest
rule it can never be collected and is correctly priced at nothing.

**Victor does not play that way.** From his own recorded game (`data/seed_scripts/top2/91854176.json`):

    day  PLANT  HARVEST  WATER  DIG
    d25     12       25     50    1
    d26     11       14     42   10
    d27      0       28     39    0
    d28      0       20     39    6
    d29      0       26     21    0
    final crops: {'WHEAT': 2}

He plants eleven on d26 and harvests **26 on d29**, taking them PARTIALLY at age 2-3, and finishes
with two wheat standing. The env allows it: `HARVEST` takes whatever `yield_units` holds once
`day - planted_day >= first_yield_day` (`:441`), and clears the tile.

Note this is crop-specific and NOT a general "harvest early" rule. Measured on the same tape, every
MELON he harvests is `held 6 / max 6` at age exactly 10 — never partial. The 135 partial harvests in
his season are all WHEAT at age 4, `held 4 / max 6`, which is its last legal day anyway.

## The order to do them in

Half one alone plants tiles we then cannot collect: -$2,898.
Half two alone makes late plantings valuable with nothing clearing ground for them to go on.

So the pair is: teach the harvest rule to take a partial one-shot when the season is about to end,
which makes `plant_prize` non-zero at d26; THEN chain the planting onto the DIG. Measure the pair,
not the halves.

The eight solved routes are keyed to exact job lists, so either change invalidates all of them and
they must be re-solved IN DAY ORDER.
