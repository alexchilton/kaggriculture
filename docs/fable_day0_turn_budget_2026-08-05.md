# Fable on the day-0 turn budget, 2026-08-05

Asked why our emitter needs 123 turns for the identical day-0 placements the tape does in 106, given
the schedule now carries the tape's own tile coordinates.

**My framing was partly wrong and the headline finding is a bug neither of us had seen.**

## Finding 0 (new) — a duplicate pen task on every build day. HIGH impact, one line.

`dayplan.py:480` inserts a newly built pen into `farm.pens` **before** `_tasks_for_day` runs at
`dayplan.py:527`. Inside, the standing-pens loop (`dayplan.py:136-145`) iterates `farm.pens` and
emits FEED/CARE/COLLECT_FERTILIZER for every pen it finds -- including the ones built *that same
day* -- while the `build_orders` loop (`dayplan.py:206-208`) separately emits
BUILD_PASTURE/PLACE/FEED/CARE for the same tile.

So a new pen gets **two task entries for the same tile on its first day**. Instrumented: on day 0 the
tiles (4,4), (4,3), (3,4), (4,2) each carry both. Across the season it fires on every build day
-- (0,4), (5,2), (6,1), (8,4), (9,1), (10,3) -- for **15 phantom tasks**, which matches
BUILD_PASTURE at 14-15 almost exactly.

**This is almost certainly what the earlier Finding 2 was reaching for and got backwards.** The
season residual CARE +47 / FEED +36 is not a cadence that is too generous; it is these duplicates
actually landing. Cutting the cadence was the wrong fix for a real symptom.

It also answers the walk question. Hands fill strictly sequentially (`dayplan.py:273`), and the
duplicate is rank 3 against the build's rank 0 (`dayplan.py:240`), so the hand that did the build has
usually moved on before its own duplicate becomes the cheapest option. Traced on day 0: hand 4
finishes two distant plantings at (0,4)/(0,3) and then walks **back across the board** to (4,3) and
(4,2) -- tiles hand 0 and hand 1 had built pens on earlier -- purely to service a phantom.

Fix, in the pens loop:

    for tile, pen in sorted(farm.pens.items()):
        if pen["placed"] == day:
            continue        # covered by the build task today

`pen["placed"]` is set to exactly `day` at `dayplan.py:480`, and HARVEST is unaffected (`age >= 2`
is never true on the build day).

## Why both tour-ordering experiments destroyed the money

Distance-first sends a hand to whatever is cheapest and nearest -- and a phantom FEED/CARE sitting on
the tile it is standing on is exactly that. A distance-first policy does not avoid the duplicate bug,
it **routes into it preferentially**, spending turns on ops that produce nothing
(`kaggriculture.py:786`/`:794` -- production is not gated on feeding) instead of on PLANT/WATER.

Second, independent reason: rank exists to protect work that is unrecoverable if skipped
(`dayplan.py:225-239`), and distance-first defeats that directly.

**Both experiments were judged in the presence of the duplicate bug, so they were not judged fairly.**
Worth re-running once Finding 0 is fixed.

## The packer's shape is fine

Day 0 measured fresh: 107 of 115 turns used, moves 42, work 65, one refusal of 3 turns -- and that
refusal is the phantom. The "20 extra moves" story traces to a data bug, not an algorithmic one. Do
not redesign `_assign` into a joint/global assignment for this.

## Plant-day watering is LOAD BEARING -- do not remove it

My framing asked whether watering on the planting day is 17 wasted turns, since `age_days == 0` is
outside every one-shot window. **It is not.** `_new_plant` (`kaggriculture.py:200-211`) sets
`consecutive_unwatered: 1` with the comment "planting day counts as unwatered", and
`_daily_refresh_plants` weeds anything reaching 2 at the next dusk.

Verified directly against the live engine, not read: a WHEAT tile planted on day 0 and left unwatered
**becomes a WEED at the first day-1 observation, every time.** Total loss of the planting.
`dayplan.py:223` always pairs WATER with PLANT and must keep doing so.

**Unresolved caveat, flagged not fixed:** the tape appears to show 4 of A's 17 day-0 wheat tiles
unwatered same-day yet surviving to harvest on day 4. The raw replay shows `consecutive_unwatered`
going 1 -> 0 across the day boundary with no WATER op nearby, which contradicts both the code as
read and the direct engine reproduction. Could be a step-indexing artifact in how the replay bundles
pre/post-action state, or `extract_tape.py`'s position attribution on the last turn of a day. Given
the controlled counter-test, do NOT treat "A waters 13 of 17" as licence to skip planting-day water.

## Also noted, unscored

DIG is 0 of the tape's 25: `dayplan.py:161` only emits it in the replant branch, never for an
existing crop tile.

## Ranked

1. Finding 0, the duplicate guard. Confirmed, structural, season-wide, one line. Test first.
2. Re-run the rank/distance tour experiment AFTER Finding 0 -- the earlier result was measured while
   a bug was inflating exactly the kind of cheap-nearby task distance-first would chase.
3. Leave `_assign`'s sequential shape alone.
4. Leave the plant-day WATER alone.
