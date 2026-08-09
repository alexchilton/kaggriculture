# Animals are still being killed off, and it is systematic, not one seed

**2026-08-09.** Diagnosis only, per instruction -- the per-death table comes before any proposal.
Does not touch production, animal buying, planting, `kagg/search/cover.py`, the herd-mix code
(`SHOP_ADAPT_HERD`, `SHOP_ADAPT_FROM_DAY`, `HERD_FLOOR_COW`, `HERD_FLOOR_SHEEP`,
`expected_future_drain`, `want_total`), or the feed-buy line.

## Method

`consecutive_unfed >= 2` deletes an animal outright and irreversibly
(`reference/kaggriculture.py:792-806`). Ran the shipped agent
(`kagg.search.schedule_agent.make_agent`, default flags, `router=True`, the real
`data/seed_scripts/top_guys/90976060/schedule.json` fixture -- the same fixture
`mirror_gate.py`/`test_reservation_sell_cap.py` already use) mirrored against itself, full 720-turn
season, on **7 seeds: 11, 13, 17, 19, 23, 29, 41**. `farms[i]["tiles"]` is public
(`reference/kaggriculture.json`), so every animal tile on BOTH farms is tracked turn by turn from
either player's own observation; `private.shed`/`private.inventories` are read from each side's own
observation. A death is detected the turn a previously-alive tile position stops carrying an
`"animal"` key. `scripts/animal_death_diag.py` is the harness; raw output at
`data/logs/animal_death_diag3.log`.

**One real bug found and fixed along the way, reported because it inverted the first result
entirely.** The first version's schedule-thinning whitelist (copied from
`tests/test_reservation_sell_cap.py`) filtered on a key called `"animals"`, which does not exist in
the schedule JSON -- the real field is `"animals_bought"`. That silently dropped every animal
purchase: peak herd size was 0 on all 7 seeds, both farms, and "0 deaths" was trivially true because
there was nothing to die. Switching to `mirror_gate.py`'s own exclusion-based thinning (already
verified live, since its own runs report real MILK/WOOL/MELON/STRAWBERRY sales) fixed it; herds then
reached 12-21 animals and deaths appeared immediately. Worth stating plainly: **a "clean" measurement
that reports zero of the thing you are looking for is the first thing to distrust, not the last.**

Mirror seating makes farm 0 and farm 1 run the identical schedule against identical logic on
identical boards, so every event below happens on BOTH farms -- the table lists 21 **distinct**
events; the raw log has 42 (21 x 2 seats).

## Result: systematic, not one seed

| seed | deaths (both seats) | distinct events | peak herd (each farm) | herd at d29 |
|---:|---:|---:|---:|---:|
| 11 | 4 | 2 | 19 | 19 |
| 13 | 6 | 3 | 20 | 18 |
| 17 | 8 | 4 | 18 | 17 |
| 19 | 0 | 0 | 21 | 21 |
| 23 | 2 | 1 | 20 | 20 |
| 29 | 22 | 11 | 12 | 10 |
| 41 | 0 | 0 | 21 | 21 |

**5 of 7 seeds lose at least one animal.** Seed 29 is not a mild case: 11 distinct animals die
across days 10, 11, 13, 14 and 16 -- a rolling loss through the whole mid-game, herd 12 -> 10 by
day 29. This is well past "rare, and I want to know whether it is rare-but-systematic or a genuine
one-off": on this measurement it is systematic on more than two-thirds of seeds tested.

This also does not match the cited baseline of "shipped loses 1 animal on seed 13" --
`docs/the_book_is_shallow_2026-08-09.md`'s own figure. Here seed 13 loses 3 distinct animals. The
two measurements were not run under identical conditions (opponent, schedule vintage, and possibly
code state all differ, and this worktree's `kagg/search/schedule_agent.py` does not contain the
`FEED_BUY_CEILING_DAYS` buy-side fix referenced in an uncommitted `docs/fable_the_wheat_churn_2026-08-09.md`
found on this machine but not on this branch -- see "What this doc does not include" below), so
the two numbers are not directly comparable, but neither reading supports "one animal, don't worry
about it."

## Per-death table

Every distinct event, in the order it occurred within its seed. `dist_to_shed` is Manhattan distance
to the nearest of the four shed-access tiles. `fresh` means placed 2 days or fewer before death.
"Wheat dawn" is shed WHEAT at the start of each of the two days whose `consecutive_unfed` tally
killed the animal, plus the death day itself.

| seed | species @ tile | placed | died (day/hr) | dist | fresh | wheat dawn (d-2,d-1,d) | mechanism |
|---|---|---:|---|---:|---|---|---|
| 11 | SHEEP (0,4) | d13 | d15 h0 | 4 | Y | 18,14,17 | B: no hand ever on tile, day 15 |
| 11 | COW (1,4) | d0 | d15 h0 | 3 | N | 18,14,17 | B: no hand ever on tile, day 15 |
| 13 | COW (1,4) | d0 | d10 h0 | 3 | N | 1,4,8 | A: wheat dawn=1 on d8 |
| 13 | COW (2,7) | d13 | d15 h0 | 4 | Y | 16,12,7 | B: PLACE then PASS x9, never fed |
| 13 | COW (3,8) | d13 | d15 h0 | 4 | Y | 16,12,7 | B: no hand on tile d15 |
| 17 | COW (1,3) | d3 | d9 h0 | 4 | N | 3,0,4 | A: wheat dawn=0 on d8 |
| 17 | COW (2,4) | d0 | d10 h0 | 2 | N | 0,4,11 | A: wheat dawn=0 on d8 (replacement fed d10) |
| 17 | SHEEP (3,4) | d0 | d10 h0 | **1** | N | 0,4,11 | A: wheat dawn=0 on d8, despite dist=1 |
| 17 | COW (6,3) | d13 | d15 h0 | 2 | Y | 16,9,18 | B: PLACE then never fed again |
| 23 | COW (1,3) | d3 | d9 h0 | 4 | N | 3,0,4 | A: wheat dawn=0 on d8 |
| 29 | COW (2,3) | d1 | d10 h0 | 3 | N | 0,0,11 | A: wheat dawn=0 on d8 AND d9 |
| 29 | COW (0,3) | d4 | d11 h0 | 5 | N | 0,11,8 | A: wheat dawn=0 on d9 |
| 29 | COW (1,4) | d0 | d11 h0 | 3 | N | 0,11,8 | A: wheat dawn=0 on d9 |
| 29 | SHEEP (7,3) | d11 | d13 h0 | 3 | Y | 8,5,14 | B: no hand on tile d13 |
| 29 | COW (8,3) | d10 | d13 h0 | 4 | N* | 8,5,14 | B: minimal routing, 4 visits total, no FEED |
| 29 | COW (9,3) | d10 | d13 h0 | 5 | N* | 8,5,14 | B: minimal routing, 3 visits total, no FEED |
| 29 | SHEEP (3,2) | d12 | d14 h0 | 3 | Y | 5,14,6 | B: PLACE then PASS x6, never fed |
| 29 | COW (3,3) | d12 | d14 h0 | 2 | Y | 5,14,6 | B: PLACE, visited 4x, never FEED |
| 29 | COW (1,3) | d3 | d16 h0 | 4 | N | 6,1,9 | A/B mix: wheat dawn=1 on d15 |
| 29 | COW (0,4) | d13 | d16 h0 | 4 | N* | 6,1,9 | A/B mix: wheat dawn=1 on d15 |
| 29 | COW (1,4) | d13 | d16 h0 | 3 | N* | 6,1,9 | A/B mix: wheat dawn=1 on d15 (replacement fed d16) |

`*` placed 3 days before death -- one day past this doc's `<=2 day` "fresh" cutoff, but functionally
the same case: never fed even once in its short life.

**Every single death shows `consecutive_unfed == 1` at the last observed-alive snapshot** -- i.e.
every one of these is exactly two bad days back to back, not a long-neglected animal accumulating a
larger tally that this env does not even allow (the cap is 2, so this is expected, but it does mean
"neglected for a week" is not a shape that occurs -- the failure is always a tight two-day window).

## Two mechanisms, not one

**Mechanism A -- genuine early-game wheat shortage.** `shed WHEAT at dawn` is 0 or 1 on the day(s)
that seal the death: seed 13 d8=1, seed 17 d8=0, seed 23 d8=0, seed 29 d8=0/d9=0, seed 29's second
cluster d15=1. This cluster is concentrated in days 7-11 (the ramp-up window) and once more around
day 15-16. This is a buy-side timing question -- explicitly out of scope here per the "do not touch
the feed-buy line" constraint, and this worktree does not contain whatever buy-side fix (if any) is
current elsewhere; see the note above.

**Mechanism B -- freshly-placed or lightly-visited animals, wheat abundant, simply never fed.**
`shed WHEAT at dawn` is in the teens (12-18) and the log line is literally
`no hand/farmer ever stood on (x,y) this day`, or the tile gets 1-4 drive-by visits across three
days with every logged action being `PASS`, `COLLECT_FERTILIZER`, or plain movement -- never `FEED`.
Nine of the 21 events are a clean instance of this (11 x2, 13 x2, 17 x1, 29 x4), and a further four
are ambiguous mixes (29's day-16 cluster: wheat is thin AND the tile is barely visited). This is a
routing/priority miss, not a supply problem, and it hits BOTH freshly-placed animals (the schedule's
own `PLACE` order, never followed up) and animals sitting on distant tiles that fall off the crew's
priority list once other work exists.

**Distance to shed is not the discriminator.** Seed 17's `SHEEP (3,4)` sits at distance 1 -- as close
to the shed as a tile can be -- and still starves (mechanism A there: the shed itself was empty).
Deaths occur at distances 1 through 5 with no visible trend; whatever the driver is, it is not "too
far to reach."

## One hypothesis tested, and it failed

`URGENT_OPS = ()` (`kagg/search/schedule_agent.py:1127`) is not a hunch pulled out of thin air --
its own docstring describes mechanism B exactly: *"PLACE is the whole list because what follows it
is time-critical: an animal must be fed and cared for on the day it lands... Placed at hour 18 it
simply cannot be served,"* and a comment directly above the value says *"Re-enabled 2026-08-07, and
the reason it was off has expired."* The shipped value is the empty tuple -- still disabled, despite
the comment. This looked like exactly the mechanism-B fix, wired into `_router_acts`
(`kagg/search/schedule_agent.py:1923`, unconditionally on the live path whenever `router=True`, which
this diagnosis and every other test/gate in this codebase uses).

**Tested directly, seeds 11/13/17, mirror, full season:**

    URGENT_OPS = ()            (shipped)   18 deaths
    URGENT_OPS = ("PLACE",)                18 deaths

**Zero measured difference.** The mechanism the flag targets is real and the flag is genuinely on
the live code path (confirmed by reading `_router_acts`'s call site, not assumed), but flipping it
does not move a single death. Root cause of *why* it does not help is still open -- candidates not
yet investigated: the "urgent" trigger may fire a replan that still does not prioritize FEED over
whatever else is queued; `state["seen_urgent"]` may already be swallowing the trigger for reasons
unrelated to the fix in its own docstring (that docstring already records ONE such swallowing bug,
fixed by keying on `(tile, op)` instead of `tile` alone -- there may be a second one); or the replan
may fire correctly but the solver's own cost function still does not rank a FEED trip highly enough
against everything else competing for the same hand's time.

This is reported as a negative result and pinned as `tests/test_animals_still_die.py` (marked
`@pytest.mark.xfail`, `@pytest.mark.slow`), not because URGENT_OPS is being recommended, but because
"the obvious fix does not work" is itself the finding, and a future session should not re-derive it
by re-trying the same flag.

## Is it worth fixing

Yes, on the numbers here: 5 of 7 seeds, up to 11 animals in a single season, systematic rather than
rare. It was explicitly separated in `docs/the_book_is_shallow_2026-08-09.md` from the price-collapse
work as "not the same defect... must not be traded against it," and this measurement does not change
that verdict -- if anything it strengthens it, since the loss rate measured here (up to ~50% of a
12-animal herd on seed 29) is larger than the one-animal figure it was filed under.

## What this doc does not include

- **A fix.** Explicitly diagnosis-first per instruction. One candidate (`URGENT_OPS`) was tested and
  ruled out; no other candidate was tried, and none should be read as implied or recommended from
  this doc alone.
- **The buy-side (mechanism A) shortage.** Off limits per the feed-buy-line constraint. A separate,
  uncommitted `docs/fable_the_wheat_churn_2026-08-09.md` exists elsewhere on this machine describing
  a related buy-side day-budget defect and fix (`FEED_BUY_CEILING_DAYS`) with its own anti-starvation
  measurement, but that code is not present on this branch/worktree and this doc does not depend on
  it, borrow its numbers, or assume its fix is or is not already shipped anywhere else.
- **Any run against a real (non-mirror) opponent.** Mirror was used because it is what this
  project's other market/behaviour diagnostics already validate as reproducing contested conditions
  (`scripts/mirror_gate.py`'s own docstring), and because both seats running the SAME code gives two
  independent samples per seed for free. A real-opponent run was not attempted; if the opponent's own
  animal-product selling pressures the schedule's timing differently, that is unmeasured here.

## Artifacts

- `scripts/animal_death_diag.py` -- the harness, reusable for any future seed/flag sweep.
- `data/logs/animal_death_diag3.log` -- full raw output, all 42 death records with per-day wheat
  and hand-action detail (this doc's table is a condensed read of it).
- `tests/test_animals_still_die.py` -- xfail pin, `@pytest.mark.slow`.
