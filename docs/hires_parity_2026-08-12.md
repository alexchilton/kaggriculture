# `_hires_this_turn` and the wall check -- verified, fixed, measured, and the fix is a regression

Date 2026-08-12. Investigating a claim from an earlier (unverified) analysis pass: that
`_hires_this_turn` in `kagg/search/schedule_agent_1455mh.py` never applies `_unwalled_landing_slots`,
while the market block's actual HIRE-order emission does, and that this explains a dawn-plan
phantom-crew miscount on Victor tape (seed 11) day 10 (`land=1, hands=14`).

## 1. Verification

The code-level divergence is real. Before this fix, `_hires_this_turn` (then at line 416) computed
`want = row["hands"]` and a fib-affordability loop, with no reference to `_unwalled_landing_slots`
anywhere in its body. The market block's HIRE-emission branch (`HIRE_PINNED_DAYS and hour == 0`, then
around line 3864) computes the same `want` and, when `HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS and
row["land"] > 0`, caps it with `_unwalled_landing_slots(tiles, units, want)` before emitting any HIRE
orders. `_hires_this_turn`'s own docstring states the contract this breaks: it predicts "how many
hands the market block below is about to buy" for the dawn plan to route, and "must not diverge from
what that block actually orders."

**Where it actually bites is not where the earlier pass said.** `_unwalled_landing_slots` was
instrumented across the full Victor replay, seed 11, d0-d12. It is called on exactly the two days
with `land > 0` in the schedule -- d6 and d10 -- and only reduces `want` on one of them:

    d 6   land=1  row hands=4   _unwalled_landing_slots(tiles, units, 4)  -> 2   _hires_this_turn -> 4  (WRONG, pre-fix)
    d10   land=1  row hands=14  _unwalled_landing_slots(tiles, units, 14) -> 14  _hires_this_turn -> 14 (already correct)

d10 -- the day the earlier pass cited as "exactly land=1, hands=14" -- is a false positive for this
specific bug. Its own predicted-vs-landed gap is real (14 predicted, 7 HIRE orders actually emitted)
but is caused by `ORDER_SLOTS = 10` truncating the turn's order queue (2 SELL + 7 HIRE + 1 BUY_LAND =
10 slots, exactly full), a separate, pre-existing throttle this task did not ask to be fixed and this
fix does not touch. d6 is the one clean, real instance of the reported mechanism.

## 2. Test

`tests/test_the_dawn_hire_forecast_applies_the_wall_check.py`. Plays d0-d12 of the Victor schedule
against the real replay opponent, spying on `_hires_this_turn` and `_unwalled_landing_slots` to
record, per day, the dawn forecast and the market block's own pre-`ORDER_SLOTS` `want`. Five tests:

- a guard that at least one day's `want` is actually reduced by the wall check (anchored on the raw
  schedule row, not on the prediction, so it holds regardless of the fix and isn't circular),
- `predicted <= market_want` for every day in d0-d12 (never over-predict -- the actual failure mode;
  under-prediction from the *separate*, correct fib-affordability check is not this bug and is
  explicitly allowed),
- a hardcoded check that the one day known to be wall-bound with affordability *not* binding (d6)
  predicts exactly 2, not 4.

Pre-fix: 2 of 15 fail, both on d6, both clean assertion failures (`4 == 2`, `4 <= 2`) -- confirmed by
reverting the production change and re-running with a signature-aware spy, not by a TypeError
artifact. Post-fix: 15/15 pass.

`tests/test_each_day_matches_the_tape.py`: 6/7 fail both before and after (d1-d6), identically -- the
pre-existing 1.32.2-vs-1.32.6 divergence this task was told to expect and not fix. No new failure, no
new pass, among d0-d6.

## 3. The fix

`_hires_this_turn` gained optional `tiles=None, units=None` parameters and, when both are given and
`HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS and row["land"] > 0`, applies
`want = min(want, _unwalled_landing_slots(tiles, units, want))` before the fib-affordability loop --
identical to the market block's own logic. The one call site (`make_agent`'s router branch) now
passes the `tiles`/`units` already in scope there. No other call sites exist.

## 4. Measured -- and the fix is a regression

`python -u scripts/breakdown.py --module schedule_agent_1455mh --tape victor --days 20 --moves`,
baseline (bug present) vs. fixed, both seed 11:

**d6, the fix's own target day** (ours/tape):

| row          | baseline    | fixed       |
|--------------|-------------|-------------|
| pens         | 8/8 (match) | 6/8         |
| weeds        | 0/0 (match) | 1/0         |
| build_pastur | 2/2 (match) | 0/2         |
| place        | 1/1 (match) | 0/1         |
| money        | 59/28       | 7/28        |

The fix turns four rows that matched the tape into four rows that don't, on the exact day it targets.

**Season totals, d0-d19** (ours/tape):

| metric | baseline    | fixed       |
|--------|-------------|-------------|
| work   | 1606 / 1556 | 1242 / 1556 |
| move   | 1672 / 1536 | 1309 / 1536 |
| idle   | 541 / 692   | 1265 / 692  |
| mv/wk  | 1.04 / 0.99 | 1.05 / 0.99 |

d19 money: baseline 26,215 (tape 27,133, a 3.4% gap) vs. fixed 11,790 (a 56.6% gap). d10 money:
baseline 5,560/5,630 (near-exact) vs. fixed 5/5,630 -- effectively bankrupt. Weeds: baseline never
weeds a single tile in 20 days (matching the tape's 0 throughout); fixed accumulates 17 by d19.

Full tables: `data/logs/breakdown_baseline_victor_d20.log`, `data/logs/breakdown_post_fix_victor_d20.log`.

### Why: the forecast needs the day's eventual crew, not the hour-0 crew

The wall check *defers* a hire, it does not cancel it -- `HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS`'s own
comment: "Held, never cancelled: `state[\"hired\"]` is not credited, so the day still reaches its
`hands` row." The held-back hands land later the *same* day via the top-up branch, once the parcel
opens the wall. But the day is planned once, at dawn (`docs/architecture.md`,
`project_kaggriculture_plan_once.md`), with no replan and no idle top-up for routing. A dawn forecast
that reports only 2 (the hour-0-landable count) tells the router only 2 hands need jobs today; the 2
that arrive later via the top-up get hired but never assigned a route, and sit idle for the rest of
the day they arrive on. That is exactly what the idle-turn totals show (541 -> 1265, more than
double) and it compounds: d6 alone banks $52 less immediately, and every later day inherits a smaller
worked board, a thinner bank, and (from d7 on) a bank too thin for the fib-affordability check inside
`_hires_this_turn` itself to predict as many hires as the baseline could, which throttles the crew
further. One 4-to-2 delta at d6 hour 0 is the sole point of divergence between the two runs
(confirmed: every other day's `_hires_this_turn` prediction is identical between baseline and fixed,
by direct instrumentation) -- and it cascades into the season-long gap above through exactly the
"days match in order, an earlier day's failure decides every later one" mechanism this project's own
testing discipline warns about.

## Verdict

The reported code-level divergence is real, but only on d6 -- d10 was misattributed. A test,
`tests/test_the_dawn_hire_forecast_applies_the_wall_check.py`, proves it red before the fix and green
after, and confirmed red again on revert. The fix compiles, is minimal (one function gains two
optional parameters, one call site passes them), and does exactly what the theory asked.

**It should not be shipped as-is.** Measured against the tape, it turns d6 from a day that matched
the board on pens/build/place/weeds into a day that does not, and it roughly halves the season's
final bank against the same tape it was meant to track more closely. The dawn-routing consumer of
`_hires_this_turn` needs the day's *eventual* hand count (all hires that land today, whenever in the
day they land), not the hour-0-landable count the wall check produces -- so the correct fix is
probably at the call site or in `_clear_the_spawn_ring`/`_land_this_turn` (route for the full `hands`
row regardless of the wall check, since every held-back hire still shows up before midnight), not in
`_hires_this_turn` itself. That is a different, larger change than what was asked for here, and is
left for a decision rather than silently implemented.

This left in the tree as delivered code in this worktree, per instructions, for the user to review
and integrate or discard.
