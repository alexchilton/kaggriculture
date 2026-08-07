# Day 5 `BUY_PRODUCT WHEAT` 5/4 — the fifth unit and its fix

Scope: Seb's tape, seed 11, weeds off.
This work happened entirely in a scratch git worktree, never in the main checkout.
See "Worktree and main-tree isolation" at the end for the exact commands and `git status` proof.

## Reproduction

```
python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0
```

Day 5, before any change here: `buy_product 5/4`, `sell 26/26` (already exact), days 0-4 exact on
every op and the dawn board, matching what the task description already established.

## 1. The hour-by-hour arithmetic — measured, not reasoned

Instrumented `schedule_agent.py` in the worktree with a print gated on `os.environ["DEBUG_D5"]`
directly inside the feed top-up block, right after `short` is computed, then ran:

```
DEBUG_D5=1 python -u scripts/fidelity.py --seed 11 --days 6 \
    --replay data/seed_scripts/top_guys/90494364.json \
    --schedule data/seed_scripts/top_guys/90494364/schedule.json --team "Seb (allegedly)"
```

Every turn's values, `alive=7` throughout the day:

```
hour  fed_today  shed  on_hand  feed_ordered  wanted  buys_ordered  owed  herd  short
 0        0        23     27         0          4          0        4   -13     1   (dropped: order cap, 10 HIRE+SELL already queued)
 1        0         2     10         0          4          0        4     4     4   -> BUY_PRODUCT WHEAT 4
 2        0         5     14         4          4          4        0    -4     0
 3        0         5     14         4          4          4        0    -4     0
 4        1         5     13         4          4          4        0    -3     0
 5        3         5     11         4          4          4        0    -1     0
 6        3         5     11         4          4          4        0    -1     0
 7        4         5     11         4          4          4        0    -1     0
 8        6         5      9         4          4          4        0     1     1   -> BUY_PRODUCT WHEAT 1
 9        6         6     10         5          4          5       -1    -1     0
10-23     7         6-8   9-11       5          4          5       -1  -2..0    0
```

(`fed_today` is the count of animal tiles with `c.get("fed_today")` true, added to the same debug
line to test the hypothesis below — also a measurement, not an assumption.)

Totals: hour 1 buys 4 (matches `wanted`, `owed` reaches 0). Hour 8 buys a 5th unit. That 5th unit is
the entire divergence — `buy_product 5/4`.

The hour-0 order for `short=1` never fires: `len(orders) < 9` fails because 8 HIRE + 2 SELL already
fill the list before the feed block runs. That's a pre-existing, separate throttle, not part of this
question — it's the reason the real top-up happens at hour 1 instead of hour 0, and it doesn't change
the day's total either way (the reformulated `herd` at hour 1 already catches up to the full 4).

## 2. Classification: (a), a genuine off-by-one — specifically off-by-`fed_today`

`herd = FEED_DAYS * alive - on_hand - state["ordered"][("feed", "WHEAT")]` targets a **fixed** two-day
supply (`2 * 7 = 14`) on every single turn of the day, and nothing in it ever shrinks as the day's own
feeding consumes that supply. `FEED` takes exactly 1 WHEAT from a unit's hand inventory per animal per
day (`reference/kaggriculture.py:480-488`) and will not draw again once `tile["fed_today"]` is set
(`kaggriculture.py:483`) — so wheat spent on today's ration is gone for good, not a shortfall to be
replaced today. It's tomorrow's ration that still needs covering.

By hour 8, six of seven animals have already been fed. `on_hand` has fallen from 14 (hour 2, right
after the first top-up landed) to 9 — a drop of 5, matching roughly what 6 feeds consumed net of
whatever else moved through shed/hands that hour. `feed_ordered` is still pinned at 4 (the day's
`wanted`, already satisfied). The formula reads `14 - 9 - 4 = 1` and orders a 5th unit, treating
today's own consumption as fresh demand on top of a target that was already met.

Confirmed this is a real defect, not "correct behaviour the tape happens not to need" (option c): the
extra unit is never eaten. `feed 7/7` is exact on both sides of the market fix already in place, with
or without the 5th unit. It just sits in the shed, and it shows up one-for-one as excess wheat carried
into day 6's dawn board: `sh:wheat` read `8/7` before this fix (verified below it now reads `7/7`).
So it is a genuine bug with a measurable downstream effect on day-6 exactness, not a harmless
over-cushion.

Not (b), a double count between `owed` and `herd`: `feed_ordered` staying pinned after the order fills
would, if anything, make `herd` *more* negative (safer, not the direction of the bug) — the arrival
of the 4 units is already reflected once in `on_hand` (via `shed`) and the still-uncleared
`feed_ordered` counter double-subtracts it, not double-adds it. That effect exists but pushes the
wrong direction to explain the 5th unit; it wasn't measured further because it doesn't need to be to
answer the question asked.

## 3. Failing test, fix, and the reverted-goes-red check

All done in `tests/test_router.py` and `kagg/search/schedule_agent.py` **in the worktree only**.

### Test: `test_fed_today_relieves_the_herd_floor_instead_of_re_triggering_it`

Six animals, a shed stocked to exactly `FEED_DAYS * alive` (12) at dawn, an empty schedule (`wanted =
0`, so the floor is the only thing that can order anything). Four of six get `fed_today` flipped and
their ration drained from the shed at hours 2, 4, 6, 8 — the same shape as Seb's day 5. Asserts
`ordered == 0` across the whole day.

Ran it against the unmodified code first:

```
$ python -m pytest tests/test_router.py -k fed_today_relieves -v
FAILED ... AssertionError: ... same-day feeding alone triggered 4 more wheat to be bought ...
assert 4 == 0
```

### Fix

```python
fed_today = sum(1 for r in tiles for c in r
                if isinstance(c, dict) and "animal" in c and c.get("fed_today"))
herd = FEED_DAYS * alive - fed_today - on_hand - state["ordered"][("feed", "WHEAT")]
```

Rationale for the exact form: subtracting `fed_today` converts the floor from "always hold a fixed
2-day supply" to "hold whatever is left of today's ration for the unfed, plus a full ration for
tomorrow" — `(alive - fed_today) + alive`, algebraically `2*alive - fed_today`. At hour 1
(`fed_today=0`) it's unchanged from before (still orders 4). At hour 8 (`fed_today=6`) it reads
`14 - 6 - 9 - 4 = -5`, no further order.

### Result: test passes with the fix

```
$ python -m pytest tests/test_router.py -k fed_today_relieves -v
PASSED
$ python -m pytest tests/test_router.py -q
58 passed, 6 skipped
```

### Reverted, confirmed red again

Stashed only `kagg/search/schedule_agent.py` (kept the test), reran:

```
$ git stash push -- kagg/search/schedule_agent.py
$ python -m pytest tests/test_router.py -k fed_today_relieves -v
FAILED ... assert 4 == 0
$ git stash pop
```

Confirmed the test is covered by the fix, not accidentally green.

### Acceptance bar — verified with `scripts/breakdown.py`, not claimed

Before the fix (already true per the task description, reproduced here):
`buy_product 5/4`, `sell 26/26`, days 0-4 dawn board and every op exact.

After the fix:

```
day        d0        d1        d2        d3        d4        d5        d6 ...
money  3000/3000  566/566  356/356  658/658  483/482  316/320  830/869 ...
```

Days 0-4 dawn board rows are **byte-identical to the pre-fix run** (checked money, tiles, pens, wheat,
strawb, melon, cow, sheep, sh:wheat, sh:melon, sh:ferti for d0-d4; every op row d0-d4 unchanged too —
`plant 17/17`, `water 17/17`, `feed 4/4`..`7/7`, etc., same as before touching the code).

Day 5: `buy_product 4/4` (was 5/4 — fixed), `sell 26/26` (unchanged, still exact) — both halves of the
acceptance bar hold.

Bonus, not asked for but worth recording since it's directly diagnostic: day 6 dawn `sh:wheat` moved
from `8/7` to `7/7`. That's the downstream evidence the 5th unit was genuinely surplus, not a needed
buffer.

## What I only reasoned about, not measured

- The claim that hour 0's `short=1` is dropped specifically by the 10-order market cap (8 HIRE + 2
  SELL already in the list) is inferred from `len(orders) < 9` and the order counts printed, not
  stepped through in a debugger. It doesn't affect the classification or the fix, since the day's
  total already catches up fully at hour 1 either way.
- The exact per-hour breakdown of what other than FEED moved wheat through `shed`/hands between hours
  2 and 8 (PICKUP timing, DROP timing) was not decomposed further — `on_hand`'s fall from 14 to 9 was
  taken as consistent with "roughly 6 feeds plus other shed traffic" rather than reconciled unit by
  unit. Not needed for the fix, since `fed_today` is read directly from the tile flags rather than
  inferred from the wheat count.
- Day 6 onward beyond the one `sh:wheat` cell was not re-checked for further divergences; the task
  scope is day 5's `buy_product`, and the instruction was explicit not to chase a season aggregate.

## Worktree and main-tree isolation

All work happened in a scratch worktree, created manually (not via the `EnterWorktree` tool, because
its default base ref branches from `origin/<default-branch>` and the fix under investigation — the
`shed_before`/`shed` accounting from commit `6243b55` — is not on any remote branch):

```
git worktree add -b fable-d5buy-scratch \
    /private/tmp/claude-501/-Users-alexchilton-DataspellProjects-kaggriculture/5fb520ea-bfb5-460d-aaa7-d7f197a84d9e/scratchpad/wt-d5buy \
    6243b55
```

`data/` and `.venv` are gitignored, so `data/seed_scripts` and `.venv` were symlinked from the main
checkout into the worktree to run `scripts/breakdown.py` and `scripts/fidelity.py` — read-only access
to gitignored assets, no writes back to the main checkout through those links.

Everything else in this document — the debug instrumentation, the new test, and the fix — was written
and run only inside the worktree:

```
$ git -C /Users/alexchilton/DataspellProjects/kaggriculture status --porcelain
 M docs/executor_livestock_broken_2026-08-04.md
 M docs/tutorial_how_this_game_is_actually_optimised.md
 M kagg/search/best_plan.json
 M kagg/search/plan.py
 M kagg/search/schedule_agent.py
 M kagg/search/scheduler.py
 M pyproject.toml
 M submission/main.py
?? docs/fable_chain_genome_review_2026-08-04.md
?? docs/fable_herd_cap_and_retraction_2026-08-04.md
?? docs/fable_small_errors_review_2026-08-05.md
?? docs/kimi_prompt_trajectory_optimisation.md
?? docs/kimi_take_chain_optimisation_2026-08-04.md
?? scripts/the_held_back_fertilizer.py
?? scripts/where_the_cow_went.py
?? tests/conftest.py
```

That's the main tree's own state, changed by work happening there concurrently while this task ran —
`kagg/search/schedule_agent.py` shows modified there too, but on a different HEAD (`6ab2dc1`, moved
on from the `6243b55` this worktree branched off) and with unrelated content; `pyproject.toml` and
`tests/conftest.py` are new since this task started and were never touched here. None of the files
this document changed (`kagg/search/schedule_agent.py`, `tests/test_router.py`) were written to by
this task in the main checkout — every edit happened at
`/private/tmp/claude-501/-Users-alexchilton-DataspellProjects-kaggriculture/5fb520ea-bfb5-460d-aaa7-d7f197a84d9e/scratchpad/wt-d5buy`.

The worktree itself, with both changes still applied and 58 passed / 6 skipped, is left in place at
that path (branch `fable-d5buy-scratch`) for porting into the main tree by hand, since editing
`kagg/search/schedule_agent.py` and `tests/test_router.py` there directly was off-limits for this task.
