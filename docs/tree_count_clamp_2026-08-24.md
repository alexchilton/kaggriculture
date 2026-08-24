# The d13-d18 tree clamp: the window gains, the season pays for it

Measured 2026-08-24, branch `tree-clamp`, six seeds, kawashigi tape opponent, shop draw injected
from the recording, weeds 0.005. Harness: `scripts/tree_clamp_ab.py` (pattern copied from
`scripts/breakdown.py`; identical seeds and identical shop draw both arms).

Implements the proposal at the end of
`docs/history/the_opening_is_a_tape_the_middle_is_two_regimes_2026-08-21.md` ("Whether feeding the
tree's count to the planner actually fixes the 158-vs-112 over-planting. Proposed, not measured.")
-- now measured, and the answer is **no**.

## What shipped

`kagg/search/tree_clamp.py`: the fitted depth-3 tree read off four dawn-board features
(`my_empty`, `my_shed_WHEAT`, `my_shed_FERTILIZER`, `my_crop_STRAWBERRY`), hard-gated to
13 <= day <= 18, applied as a CAP on the plan's `plants` row in the day-change block of
`schedule_agent.make_agent`, after every other row-rewriting branch. Budgets per leaf are his own
d13-d18 rows filtered to the leaf's crop family. Crops already in the ground are never touched;
a row already under budget passes through unchanged. Tests:
`tests/test_the_dawn_tree_clamps_the_planting_window.py` (17, written RED first; red -> green ->
revert -> red -> green all confirmed).

## The verdict: NEGATIVE on the season, and it ships OFF

    seed   banked d13-18   plants cut   crops@d18   FINAL SEASON
    11        +4,674          -25          -26        -8,811
    12        +6,432          -24          -24        -1,984
    13        +6,501          -26          -25        -3,974
    14        +5,809          -25          -25        -2,810
    15        +5,809          -25          -25        -2,810
    16        +5,764          -24          -24        -6,585
    mean      +5,832                                  -4,496

Every seed: banking during the window improves (less seed and water spend, fewer chained turns),
and every seed ends the season WORSE. The tiles the cap keeps out of the ground on d15-d18 were
going to pay later; the window saves spending and loses more harvest than it saves. This is the
same shape as the old per-day seed cap -- "byte-identical early, -$2,682 by d16" --
reproduced one layer up.

Per the discipline: written down and stopped. **No softer budget was swept** -- tuning the caps
until the negative goes away would be selecting on the noise.

## What the tree actually reads on our boards

On all six seeds the dawn features landed in `straw+wheat` on five of the six days and `straw`
on d15 only (dawn shed WHEAT past 34.5 behind a nearly full board). So almost all of the cut
comes from the BUDGET half ({8,4,3,2,1,0} against rows asking {2-3,2-3,8-9,6-9,4-6,7-10}), not
from the regime half. The tree was fitted on tape-game boards; our board reaches d13 with a
different feature distribution and nearly always takes the same leaf. A tree that fires one
leaf 5/6 of the time is carrying one bit of information, not five days of decisions.

## Measurement notes, so nobody re-reads these wrong

- **Seeds are weaker diversity than they look.** Seeds 14 and 15 produced byte-identical seasons
  in BOTH arms, and 11/12/16 differ only from d14 onward. The recorded shop draw is injected from
  the replay and is therefore the SAME for every seed; what varies is the weed RNG only.
  Six seeds here carry perhaps four independent draws.
- **A reporting bug that cost nothing but could have.** The first print truncated the leaf label
  to 5 characters -- `'straw+wheat'[:5] == 'straw'` -- which made five straw+wheat days read as
  straw. Caught by re-driving one seed with full feature logging; fixed before any number above
  was read off it.
- **Suite churn, none of it a regression.** With the clamp armed, ~19 cells of the full-season
  sim gates flip to failing and ~19 others flip to passing (`test_each_day_matches_the_tape`,
  harvest/shed gates) -- downstream chaos of a changed mid-season board, both directions. With
  the switch shipping OFF, a serial run of every affected file is cell-for-cell identical to
  clean `9ffda3c`.
- The `-89 standing wheat / +171 idle` season grid in the source doc was OUR SHIPPED agent against
  the tape's own game; this A/B measures the same pairing, so the two are comparable.

## State

`TREE_CLAMP = False` ships. The machinery, the budgets and the tests stay; arming it is one
constant. What would have to change for a retry: evidence that a LATER window (the count signal
is dead after d18, but the cost shows up as missing standing crops at d19+) or a cap that
reschedules rather than cancels the deferred plantings into d19-d21 spare ground. Neither was
tested here; do not re-arm on the window numbers alone.
