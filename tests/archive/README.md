# Archived: the day-planner test surface

**Nothing here is deleted, and nothing here is broken.**
These 35 files test `crew.cover`, `router.plan_routes` and the per-tile op pricing that feeds them.
They are not collected, because the component they test does not decide anything in the shipped
artifact.

Switch them back on by deleting `--ignore=tests/archive` from `addopts` in `pyproject.toml`.
That is the only thing holding them off.

## Why

Measured 2026-08-22, `data/logs/planner_coverage_2026-08-22.log`:

    latch key             steps     of 720    planner decides
    (False, False)          719      99.9%          1
    (False, True)           719      99.9%          1
    (True, False)           719      99.9%          1
    (True, True)            719      99.9%          1

`REPLAY_OPENING_DAYS` is `tuple(range(30))` and all four recordings in `REPLAY_OPENING_TAPE` are
full 720-step seasons.
`make_agent` wraps the planner in `replayed()`, which calls `agent(obs)` on every turn and then
returns the tape's actions instead whenever `step in opening`.
That is true for 719 of 720 steps.

Alex, 2026-08-22: *"the planner gets 0 days - its all tape baby. different tapes but tape - the
animals and some of the other stuff is swapped out but all tape."*

## What our code still decides

This is the whole live surface, and its tests stay in `tests/`:

1. **Which tape plays** — the two latches, `_MB` (melon, d3) and `_Q4` (yarn store, `DECIDE_BY_DAY`).
2. **The animal species relabel** on `PICKUP` / `PLACE` / `BUY_ANIMAL`, driven by
   `state["herd_split"]`. The count and the turn stay the tape's; only COW-vs-SHEEP is ours.
3. **A `BUY_SEED` count trim**, melon-q3 arm only.
4. One turn — step 719, the last hour of d29.

## What this cost, honestly

Two things were true at once and only one of them was recorded anywhere.

**The suite was measuring a component with no vote.** Most of the red in this repo lived here.
`test_router.py` alone was 29 failed / 29 passed, and with the replay switched off it is 21 failed /
37 passed in 3.2s instead of 20.9s — the tape was overriding the scenario each test had built, so
eight of those failures were the harness, not the code.

**Four shipped constants lose their only guard.** Said plainly rather than left to be discovered:

    RT.FEED_CADENCE_FROM_DAY >= 7     test_we_feed_on_alternate_days_like_the_tape.py
    RT.PLANT_THEN_WATER               (chain-on precondition)
    SA.SHOP_ADAPT_CROPS is False      test_the_field_follows_the_shop_draw.py
    schedule_agent.FEED_DAYS == 2

All four are planner-side, so flipping one moves an answer that is discarded — but nothing will now
say so out loud. `CARE_ON_THE_WAY_PAST` is in the same position and is noted at its own definition
in `schedule_agent.py`.

## The three that needed a different argument

`test_every_seat_the_day_owns_is_given_work.py`, `test_a_unit_walks_the_route_it_was_given.py` and
`test_the_dusk_topup_stays_inside_the_days_row.py` came in second, on 2026-08-22, and they are worth
a note because the obvious reasoning would have got them wrong.

They build a real env, so the first classifier kept them.
And unlike `test_router.py`, switching the replay off does not rescue them — it makes them worse,
and it changes *which* tests fail:

    replay ON  (shipped)   20 failed, 57 passed
    replay OFF (planner)   25 failed, 52 passed

`test_no_hand_passes_the_whole_day` passes with the tape and fails 8 times with the planner.
So "the replay is swamping them" is false here; each mode fails a different real thing.

What settles it is what they compare, not how they fail.
`test_the_first_stop_walked_is_the_first_stop_planned` asserts `route[0] == first tile worked` --
the planner's route against what the unit did.
With the tape playing, the route is the discarded answer and the mismatch is guaranteed by
construction.
The `buys` row tests compare against a schedule the tape does not use.
And `test_every_seat_the_day_owns_is_given_work.py:156` says it outright in its own docstring:
*"Every assertion in this file is about what the PLANNER did."*

The lesson is the one already in `CLAUDE.md` about `farm:0.445` -- ask what unit an assertion is
over before trusting how it fails.
A test can fail differently in two modes and still be measuring nothing in the one that ships.

## What would make this matter again

Any of these, and the archive should come back:

- `REPLAY_OPENING_DAYS` stops covering all 30 days.
- A tape shorter than 720 steps is registered in `REPLAY_OPENING_TAPE`, leaving real days unplanned.
- `EMBEDDED_OPENINGS` ships empty in a bundle, so `_replay_opening` returns `{}` and the planner
  plays the whole season. **This is the dangerous one** — it degrades silently by design, so the
  artifact would fall back to 35 files' worth of untested code with no error.

The third case is worth a live test in `tests/` rather than a note here.
