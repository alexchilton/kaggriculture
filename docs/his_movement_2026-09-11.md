# His movement, read off the tape, 2026-09-11

## Method

`scripts/walk_pattern.py` is the measurement this doc is built on.
For every unit, every day, it takes the tiles that unit actually WORKED (stood on and issued a working op, not merely passed through), in the order it worked them.
The tile SET is held fixed — this measures the ORDER only, which tiles a unit gets is a separate question (see "what is not resolved" below).
Seven candidate generators are tried against that same tile set, each starting from the unit's own dawn square: `nearest` (greedy nearest-neighbour), `dist_from_shed` (sorted by distance from shed, ties broken by tile), `serp_row`/`serp_row_x`/`serp_col` (row- or column-major boustrophedon, with or without opening at the shed's own x), `lawnmower_row`/`lawnmower_col` (same axes, no alternation — carriage return instead).
Scored three ways: `exact` (candidate order equals observed order), `adjacent` (fraction of his consecutive steps that are also consecutive in the candidate), `kendall` (rank agreement between the two orderings).

Corpus: the 9 SpaTaro arm replays already curated in `scripts/breakdown.py::TAPES` (one per world), days 3-20, seat identified by team name.
1,665 unit-days, mean worked-tile bounding box 15.4 tiles.
Full log: `data/logs/walk_pattern.log`.

A second, supplementary pass (`scripts/spataro_walk_shape.py`, this session) scans the wider corpus (`data/replays_spa_sub/`, `data/replays_2026-09-07/08/09`) and classifies RAW position sequences — every hour a unit stands somewhere, not only worked tiles — into straight runs along x or y, to check whether the local shape corroborates the order-only result independently. 20 seasons, days 3/5/7/9/11, 858 unit-days.

## The result

    candidate           exact   adjacent   kendall
    nearest            43.4%     80.5%    84.2%     <- his walk
    dist_from_shed     27.3%     68.1%    83.5%
    serp_row_x         17.9%     67.0%    74.6%
    serp_col           15.7%     68.1%    74.0%
    lawnmower_col      13.3%     63.3%    71.3%
    serp_row           12.9%     66.1%    70.6%     <- what our planner did before this session
    lawnmower_row      11.0%     61.8%    68.4%

**His walk is greedy nearest-neighbour, not a lawnmower and not a row- or column-major serpentine.**
It wins on all three scores, against every alternative tried.
Our planner's row-major boustrophedon (`serp_row`) is the second-worst fit of the seven — 12.9% exact against his 43.4%, 70.6% Kendall against his 84.2%.
That gap is not noise: a serpentine walks the long way between two tiles that merely happen to share a row, and a nearest-neighbour walk never does.

**It is not the whole story.** 43.4% exact means more than half his unit-days do not match a pure nearest-neighbour chain exactly, and `dist_from_shed` alone — a much simpler rule, sort by distance and nothing else — still reaches 83.5% Kendall, only 0.7 points under `nearest`'s 84.2%.
So there is a real outward-from-the-shed component sitting alongside the local nearest-neighbour choice, and this measurement does not isolate it.
Do not read 43.4%/84.2% as "solved" — read it as "the best single-mechanism fit found, with a known residual."

## Supplementary check: local run shape

Independent of tile order, does the raw walk (all positions, not just worked tiles) look like short alternating runs — consistent with nearest-neighbour zig-zagging inside a compact block — or long single-axis sweeps?

    day    n unit-days   mean bbox w   mean bbox h   mean runs   row-major : col-major
      3         121          4.18          4.01         3.99        34 : 87
      5         132          4.02          3.92         3.89        41 : 91
      7         172          4.67          4.16         5.52        51 : 121
      9         213          4.62          4.48         5.57        89 : 124
     11         220          4.69          4.50         5.63        93 : 127

Two things corroborate the order-only result:
- **100% of direction changes between same-axis runs are flips, never carriage-return repeats** (508/508 measured) — whenever the walk does hold an axis for more than one step, it alternates, the way a nearest-neighbour walk naturally does inside a small block, not the way a scanline-with-reset would.
- **Bounding boxes are consistently near-square** (mean w 4.0-4.7 vs h 3.9-4.5 through day 11), so "row-major vs column-major" is not really a meaningful axis choice for his blocks — they are not long-and-thin in either direction, which is exactly the regime where a single fixed sweep axis (what `serp_row` assumed) stops being a good model and a locally-greedy walk should win, matching the headline result.

This was not built to independently re-derive "nearest-neighbour" — `walk_pattern.py` already establishes that on the metric that matters (order against worked tiles). It is here to confirm the raw walk doesn't secretly look like a disciplined sweep that the order-only test missed.

## Answering the five questions

**1. What decides which tiles a unit visits — stable partition or daily reassignment?**
Not resolved this session. `walk_pattern.py` takes the tile SET as given (from the tape) and only tests order; it says nothing about which unit gets which tiles or whether that changes day to day. This is flagged, not answered — a real gap, not a fitted claim.

**2. Does a unit's route have a recognisable shape?**
Yes: nearest-neighbour, with an unexplained ~15% residual and an outward-from-shed correlation that `dist_from_shed` catches most but not all of. Not a fixed tile order repeated across days — that was never tested, and days 3 vs 11 above show growing bounding boxes and run counts, i.e. the block itself changes shape as the board fills, which a "fixed order" story would not predict.

**3. What ends the outward leg and sends a unit back to the shed?**
Not resolved this session — out of scope for `walk_pattern.py` (order-only, no return-to-shed detection) and not reached by the supplementary pass either. This is the same deposit-shape question the earlier (reverted) `cover.py` work was chasing from our own rules rather than his data; it remains open from his side too.

**4. Does the pattern depend on day, world, or hand count?**
Partially resolved. Mean bbox and mean run count both grow from day 3 to day 11 (bbox tiles 7.66→9.75, runs 3.89→5.63 in the supplementary pass) — the shape is not day-invariant, it tracks the board filling in. Whether it depends on WORLD (crop mix) or HAND COUNT specifically, as opposed to just "later day, bigger board," was not isolated — `walk_pattern.py`'s per-candidate scores are pooled across all 9 worlds and all days 3-20, not broken out either way. Flagged as unresolved rather than assumed away.

**5. Is the per-unit assignment predictable from the dawn board?**
Not resolved this session. This is the same gap as question 1, restated as a planning question: nothing measured here says whether the day's tile-to-unit assignment could be reproduced from dawn state alone, or depends on the day's own decisions (what to plant, what to build) in a way only known once the day starts.

## What is regular enough to copy, and what is not

**Copy:** the order in which a hand visits the tiles once it has some — greedy nearest-neighbour from wherever the hand currently stands. This is the one clean, decisive, corpus-wide result, and it directly explains part of the excess `move`/`idle` gap against his tape: our old row-major sweep was the second-worst-fitting shape of seven tried.

**Do not yet claim:** which tiles a hand gets in the first place (question 1/5), what triggers the return-to-shed (question 3), or whether the shape is genuinely day/world/hand-count-invariant (question 4) beyond "it grows as the board fills." These are real open questions, not settled by today's measurement, and a rule fitted to close them without more data would be exactly the kind of unsupported claim this file is trying to avoid.

## Change made from this

`kagg/search/crew.py::serpentine()` — replaced the row-major boustrophedon with a greedy nearest-neighbour chain, matching the measured shape. `far_first` (the crop crew's "reach the far edge first" mode) used to be a `.reverse()` of the shed-first sweep; a reversed nearest-neighbour chain is not itself a nearest-neighbour chain from its new start, so it now starts the chain at the tile farthest from the shed instead of reversing after the fact. See the function's docstring for the exact numbers and the `d7_all_worlds.py --days 13` measurement in `docs/tour_shape_2026-09-11.md` (or its own dated follow-up) for whether it holds up on the full board.
