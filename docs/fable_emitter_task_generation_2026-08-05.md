# Fable on the emitter's task generation, 2026-08-05

Asked: is "cadence vs demand-driven" the right diagnosis for a `-138 WATER / +46 CARE` split, does the
open-loop constraint force a forward simulator, is the packer itself leaving work on the table, and is
anything in the reference provably unexploited.

Verdict: **the framing is half right.** The axis is correct but it is *two* independent wrong
cadences sharing one turn budget, which is why WATER and CARE move in opposite directions. Neither
fix needs a forward simulator; both are static functions of `(type, age)` we already track.

## Finding 1 - one-shot WATER is not insurance, it IS the yield (highest impact, cheap)

`reference/kaggriculture.py:373-386`: WATER on a NON-ongoing crop (WHEAT/CARROT/MELON), inside the
age window `[(max_yield_day+1)//2, max_yield_day]`, directly adds 1 to `yield_units` -- 2 if
fertilized -- capped at `max_yield`. Outside that window it only resets `consecutive_unwatered`.

This is categorically different from ongoing crops (TOMATO/STRAWBERRY), where
`_daily_refresh_plants` (`kaggriculture.py:738-771`) grows yield on a fixed schedule *regardless* of
`watered_today`. There, water only prevents death and gates the fertilizer bonus.

`dayplan.py:166-167` applies one rule to both:

    if day - c["last_water"] >= 2: WATER

Correct for ongoing crops. For one-shot crops it throttles the actual production mechanism to about
half its legal rate inside a short window -- melon's window is 7 days (6-12), wheat's is 3 (2-4).

**This was already measured in this repo and never wired into `dayplan.py`.**
`kagg/search/routines.py:708-771` records the exact split under `water_every`:

    melon (one-shot)      daily $15,575   every-other-day $11,167    -28%
    strawberry (ongoing)  daily  $6,182   every-other-day  $9,395    +52%
    wheat: "worse still at 2-4 days"

So the uniform cadence is the wrong rule for three of five crops.

Fix: gate the cadence on `info["ongoing"]`. Keep every-2-days for ongoing crops and for pre-window
one-shot crops; water EVERY DAY once `age >= (info["max_day"]+1)//2` on a one-shot crop. No new state.

Corollary flagged, not in scope: `FERTILIZE` is gated to ongoing crops only (`dayplan.py:182`), but
the same one-shot branch DOUBLES the water bonus when fertilized (`kaggriculture.py:384`). For
wheat's 3-day window, unfertilized watering tops out at 4 of 6 `max_yield` -- fertilizer is the only
way to reach the cap.

## Finding 2 - the packer's static priority starves WATER for pen upkeep (high impact, cheap)

**This is the explanation for the opposite signs, which I had not accounted for.**

`dayplan.py:215`: `RANK = {"build":0, "plant":1, "replant":2, "pen":3, "crop":4}` -- every pen task
outranks every crop task. And pen tasks are generated unconditionally, daily, for every pen
(`dayplan.py:136-145`), even though `kaggriculture.py:774-802` shows feeding and caring do NOT gate
production: production runs on schedule regardless of `fed_today`. Feeding only prevents the
two-consecutive-miss escape and banks a bonus consumed on a later fed production day.

So on any day where generated work exceeds capacity, `_assign`'s greedy pick
(`key = (task["_rank"], add)`, `dayplan.py:280-282`) drains the budget on guaranteed, low-value,
over-generated pen upkeep before it ever reaches crop WATER -- which per Finding 1 is where the yield
actually is. One structural cause, both signs of the residual.

Fix: drop pen FEED/CARE to the same every-2-day floor already used for crops, mirroring
`kaggriculture.py:786`'s two-miss escape rule exactly. Frees ~83 turns a season (46+37). Optionally
also rank in-window one-shot crop tasks above pen tasks -- the file's own rank comment
(`dayplan.py:209-214`) ranks by "what is unrecoverable if skipped", and a missed in-window watering
IS unrecoverable because the window closes, while a redundant CARE visit is not.

## Finding 3 - the 14-task tour cap is an unmeasured magic number (medium, very cheap to test)

`dayplan.py:268`: `while len(take) < 14:`. Every other constant in that file cites the measurement
that produced it; this one does not. On a day of cheap clustered tasks a hand can hit 14 tasks well
under its 20-23 turn budget and stop, silently dropping pending WATER the budget would have allowed.

## Q4 - unexploited in the reference

Nothing beyond Finding 1 and its fertilizer corollary. Minor, low confidence: `dayplan.py:170`
harvests ongoing crops every 3rd day regardless of each crop's own `interval` (TOMATO=1,
STRAWBERRY=2, `kaggriculture.py:14-15`). Mostly harmless because production accumulates to
`max_yield` and only decays after the cap, so at most a small part of the -20 HARVEST residual.

## OUTCOMES -- all three tested, one delta at a time

    Finding 1  one-shot water window     74.69%  from 72.28%   ACCEPTED  (+2.41)
    Finding 2  cut pen FEED/CARE         66.42%  from 74.69%   REVERTED  (-8.27)
    Finding 3  the 14-task tour cap      74.69%  unchanged     INERT

**Finding 1 was right and is the largest single fix of the session.** WATER went 713 -> 817 against
the tape's 851. Pinned by `tests/test_one_shot_crops_are_watered_every_day_in_window.py`, which
asserts the RULE (one-shot crops watered every window day, ongoing crops NOT watered daily) rather
than the cadence.

**Finding 2 was wrong, and the reasoning is the instructive part.** The mechanism argument is correct
-- `kaggriculture.py:791` really does produce regardless of `fed_today`, so a daily visit to every pen
really is mostly redundant work. But the tape feeds **319 times across roughly 343 animal-days**: it
feeds daily anyway. Cutting to "every other day plus production days" dropped FEED to 122 and CARE to
122, and cost eight points of fidelity to reclaim a +47/+36 over-production. The mechanism said the
work was unnecessary; the winner does it regardless, and the winner is the target.

Kept as `tests/test_the_herd_is_serviced_when_it_pays.py`, inverted, with the failed argument written
into the docstring -- it looked sound and will look sound again. Its two safety assertions are
genuinely useful and stay: an animal is never unfed two days running (`:786`, escape is
unrecoverable), and a production day is always a fed day (`:794`, an unfed production day discards
every care turn banked since the last one).

**Finding 3 is inert.** Swept the cap at 10, 14, 20 and 30: identical output at every value. The turn
budget binds first and the cap is never reached, so it is not a magic number doing hidden damage --
it is dead code.

## Test order (as advised)

One delta at a time, re-running `scripts/tape_match.py` after each:
1. Finding 1 alone (isolates the water-supply fix)
2. Finding 2 (isolates the packer-priority fix)
3. Finding 3 (cheapest check)
