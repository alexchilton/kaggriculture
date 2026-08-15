# Spawn-ring misprediction: is it worth fixing, and how

2026-08-12, seed 11, tape `victor`. Answering the question in
`docs/spawn_ring_misprediction_2026-08-12.md`: analysis only, no code changed.
Two read-only scripts were run to get real numbers instead of guessing; both are described below
so the run can be repeated.

## Direct recommendation

Do (b) first. It is cheap, has no solve cost, is reachable at a line that already exists, and it
is the only one of the four that also hardens the schedule against causes of a 1-2 turn slip that
are not this bug. Do (a) second, as a precision improvement, but capped at two extra solves and
gated on wall-clock, because of a real timing risk this review measured and the source doc did
not. Do not pursue (c) as scoped -- it does not dodge the prediction problem, it only relocates it,
and on the one day this review checked in detail it would still orphan a route. (d): there is a
second, previously undocumented bug under the "residual second cause" label -- see below -- and it,
not "wave staleness," is most of what makes day 10 the hard case.

## Reachability check

Both mechanisms under discussion sit inside `agent()`'s `if router:` block in
`kagg/search/schedule_agent.py`, specifically the sequence at lines 2982-2992
(`_hires_this_turn` -> `_clear_the_spawn_ring` -> `arriving`) feeding the ONE solve at
`_router_acts` lines 1837-1844, gated by `if not routes` (line 1816). `state["routes"]` is reset to
`{}` on every day change (line 2958) and never rebuilt after ("NO REPLAN, NO TOP-UP", line 1845),
so this whole sequence runs exactly once per day, on the first `agent()` call at hour 0 -- confirmed
by instrumenting it directly (below), not inferred from reading. Any fix to either the prediction
(a) or the tour-budget slack (b) lands inside this exact, single, per-day call. Verified reachable.

## What was measured, not assumed

### Experiment 1: does one extra solve converge?

Script: monkeypatches `SA._router_acts` to snapshot (deep-copy) `state` at every hour-0 call while
replaying seed 11 / tape `victor` for real through day 11, then off-line re-runs `_router_acts`
from each snapshot with (pass 1) today's prediction and (pass 2) a prediction rebuilt from pass 1's
own farmer action. Log: `data/logs/two_pass_experiment_2026-08-12.log`. Script kept at
`/private/tmp/.../scratchpad/two_pass_experiment.py` (scratchpad, not committed).

Result, all three days that were checked:

| day | pass 1 farmer act | pass 2 farmer act | converged in 1? | ring slots pass1 vs pass2 differ |
|---|---|---|---|---|
| 9 (control, `land=0`) | `PICKUP WHEAT 3` (stays (4,4)) | same | yes | 0/7 |
| 10 (`land=1, hands=14`) | `NORTH` -> (4,3) | `SOUTH` -> (4,5) | **no** | 14/14 |
| 11 (`land=0, hands=10`) | `NORTH` -> (4,3) | `NORTH` -> (4,3) | yes | 10/10 |

Day 10 needed a third pass to settle: pass 2 and pass 3 both land the farmer on `(4,5)`, so it is a
fixed point reached after **two** corrections, not one, on the one day it was checked that needed
more than one. This directly answers the stated concern: **one iteration is not always enough, but
it did not diverge or oscillate on any day tested -- it settled within two.** Day 9 is the control
from the source doc and reproduces exactly ("all eight/seven predictions exact"), which cross-checks
that this harness reproduces the real mechanism rather than a harness artifact.

On days 10 and 11, *every* ring slot in the naive prediction was wrong (10/10, 14/14) -- this
matches the doc's own finding almost exactly and is not a sampling fluke; the naive predictor is
wrong on essentially 100% of hires on any day the farmer's first action is a move.

### Experiment 2: what does the extra solve cost, in wall clock

Timed `agent()`'s hour-0 call across days 0-17, same tape/seed, no monkeypatching:

| day | crew size context | hour-0 solve time |
|---|---|---|
| 0-6 | 1-7 units | 0.000-0.002 s |
| 8 | | 0.075 s |
| 9 | | 0.127 s |
| 10 | 14 hires that day | 0.372 s |
| 11 | | 0.326 s |
| 16 | | 0.426 s |
| 17 | | 0.496 s |

`docs/competition_brief.md`: `actTimeout` is **1 second per turn**, `remainingOverageTime` is
**60 seconds banked for the whole 720-turn episode**. A single solve already costs roughly half the
per-turn budget by day 16-17. Experiment 1 showed day 10 -- a fourteen-hire land-buying day, exactly
the kind of day this fix targets -- needs *three* solves to reach its fixed point. Three solves at
day 10's measured 0.372s each is over 1.1s, which **exceeds `actTimeout` on the solve alone**,
before the rest of the turn's work. This is a real, previously unmeasured cost that the source doc's
"one extra solve and no game turn" did not price in, because it assumed one iteration would suffice.

## Ranking

**(b) — do this.** Reachable at the exact line that already docks phantom-vehicle budget for a
different reason: `_router_acts` line 1697-1698,
`for k in range(len(units), len(plan_units)): budget[k] = max(0, budget[k] - 1)`. The four ring
tiles are mutually within Manhattan 2 of each other and `_spawn_hand`/`_arrivals` can only ever
return one of those four tiles -- so the walking-distance error between *any* predicted landing tile
and *any* actual one is bounded by 2, regardless of whether the mismatch is a clean rotation (day 9,
11 pattern) or a count-per-tile mismatch (see the second cause below). A second turn docked off
every phantom vehicle's budget at this line is a direct, bounded, no-solve-cost hedge against
*all* of it, not just the rotation case. It also protects against sources of a 1-2 turn slip that
are not this bug at all -- which is the point, given the "Standing fact" below. Two caveats, both
unverified because verifying them is a code change: whether -2 flat is too conservative (wastes
slack on days the tour was never going to be short, the same failure mode that sank the pin
experiment) is an empirical question that needs the same A/B the doc already ran for the pin, and
a more surgical version -- reserve margin only on a tour's *last* stop rather than off the whole
budget -- looked more promising on inspection but its implementation locus (inside `_solve` /
`router.py`'s acceptance check) was not read this session.

**(a) — do this too, capped.** Experiment 1 shows it is not a runaway fixed point: it settled within
two corrections on every day tested. It is correct in direction and the untried-fix note in the
source doc undersold its cost. Cap iterations at 2 (matches the worst case measured), and gate on a
wall-clock budget with a hard fallback to the pass-1 (current) prediction if the accumulated solve
time for the day is getting close to `actTimeout` -- day 10's 3-solve worst case already crosses
1 second at day-10-sized crews, and crew/board size only grows later in the season, so this is not
a corner that stays small. This makes (a) strictly an improvement in prediction *accuracy* over
today, conditioned on a budget guard that does not exist in the source doc's proposal. Also: (a) as
scoped (correcting the ring-slot prediction) does **not** fix the residual on day 10 -- see below --
so shipping (a) alone and expecting day 10 to go green would repeat the doc's own measured surprise
("14 wrong to 7", not to 0) under the pin experiment.

**(c) — do not pursue as scoped.** It looked like a clean sidestep ("price the tour from whichever
tile it lands on, permutation stops mattering") but does not survive contact with the actual
mechanism. Checked concretely on day 11 (10 hires, 4-tile ring): predicted per-tile counts are
`(5,4):3 (4,5):3 (5,5):2 (4,4):2`; actual are `(4,4):3 (5,4):3 (4,5):2 (5,5):2`. These are not the
same multiset -- `(4,4)` gets **one more** hand than planned and `(4,5)` gets **one fewer**. Binding
tours to landing tiles rather than arrival order fixes the *ordering* problem but not this: a tile
that gets an extra, unplanned visit still has no tour waiting for it (an orphaned real hand), and a
tile that gets one fewer visit than planned leaves a planned tour with no vehicle. Getting the counts
right requires the same accurate start-position prediction that (a) is already trying to solve, so
(c) is not an independent alternative -- it is, at best, a complementary change to how the executor
binds a real hand to a planned route, layered on top of (a) rather than instead of it. Whether the
executor can even express "route bound to tile, not index" was not checked -- the binding is
currently by index identity (`_router_acts` line 1690-1692: "index here is the index they will
occupy in `farm['hands']`"), and rebinding it by position would touch whatever reads
`state["routes"]` every subsequent hour, which was not located this session.

**(d) — a genuinely new finding, not previously in the register.**

## The residual second cause is not (only) wave staleness

The source doc's account -- "d10 hires in waves across h0/h1/h2, by which time the h0 wave has
walked off the ring, so an h0-computed prediction is stale for later waves" -- is true as far as it
goes but is not the whole mechanism, and reading the code that actually decides *how many* hires
happen at h0 shows a second, sharper bug.

`_hires_this_turn` (line 416, this is what the dawn plan calls to size `arriving`) computes `n`
purely from bank affordability against the schedule row's `hands` want. It does **not** apply
`_unwalled_landing_slots` (line 456). But the market block that actually **emits** the HIRE orders
(line 3864-3865) does: `if HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS and land>0: want = min(want,
_unwalled_landing_slots(...))`. That is exactly the `_hires_this_turn` docstring's own warning,
unheeded by its own author: *"Read by the DAWN PLAN, which has to route them, so it must not
diverge from what that block actually orders."* It diverges. On a land-buying day, the dawn plan's
`arriving` list can contain more phantom hands than actually get hired at hour 0 -- the rest are
genuinely held back and trickle in later via the `elif HIRE_FIRST` drip (line 3869), some of them
plausibly not until the parcel itself settles (comment at line 3872-3874 mentions a deadline of
`TPD` on a land day, i.e. as late as dusk). A phantom routed as if it has ~23 turns from hour 1 but
that does not actually exist until, say, hour 13, is a much larger error than 2 Manhattan tiles --
it is a route built for a vehicle that is unavailable for over half the day.

Confirmed this is live on day 10: `data/seed_scripts/victor/schedule.json` day 10 is `hands: 14,
land: 1`; days 9 and 11 are both `land: 0`. Day 10 is exactly the day both the source doc's pin
experiment (14 wrong -> 7, not 0) and this review's two-pass experiment (needs 3 solves, not 2) flag
as the hard case, and it is exactly the day `HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS` is live.

**This changes the answer to "does the second cause change which of (a)-(d) is right."** Yes: (a)'s
two-pass mechanism, scoped to correcting ring-slot prediction, cannot fix this by construction --
the phantom crew *count* is already wrong before ring rotation is even computed. The actual fix for
day 10's residual is to give `_hires_this_turn` the same `_unwalled_landing_slots` cap the market
block already applies (so `n` at hour 0 matches what will actually be ordered), and -- harder, not
attempted here -- extend the dawn plan to also model the later-hour drip hires as phantom vehicles
with a correspondingly later, shorter budget rather than not modelling them at all. This is a
parity bug of the same shape the project's CLAUDE.md already warns about repeatedly ("a gate only
tests what it exercises" / "check whether a doc already answers the question") -- two functions that
must agree, stated as needing to agree in one of their own docstrings, that do not.

## Framing check: is the ring misprediction even the right thing to fix

The prompt's own framing challenge is right and should be taken at face value, not politely hedged.
The worked example in the source doc is a tour priced at *exactly* 23 turns against a 23-turn
budget. The watering cadence weeds a tile at `consecutive_unwatered >= 2` with the counter starting
at 1 on the planting day -- so, by the doc's own count, roughly 20 tiles sit exactly one miss from
death every day, all season, by design. Given that, a 2-turn shift from *any* cause -- this bug, a
different bug, a future rule change, an off-by-one in some other function -- converts directly into
a dead tile whenever it lands on a tour that was priced with zero margin. The spawn-ring
misprediction is real, deterministic, and proven (Experiment 1 above independently reproduces it),
so it is not a phantom cause. But it is a *trigger*, not the vulnerability. The vulnerability is
that nothing in the scheduler ever prices a margin, anywhere, for anything -- confirmed by reading
`_router_acts`'s budget construction, which computes exact turn budgets and hands them to a solver
with no slack term of any kind visible in what was read this session. Fixing the prediction (a)
closes this one instance. It does not touch the underlying zero-margin architecture, which will
present the identical symptom -- a tile weeded because a tour finished two tiles short -- under the
next cause that perturbs a tour by even one turn. That is the argument for ranking (b) above (a):
it is the fix that generalizes, and the fix aimed at the symptom the prompt itself flagged as
possibly the real defect.

## What could not be verified this session

- Whether a flat -2 budget haircut on phantom vehicles (b) nets positive on the 17-day grid, or
  repeats the pin experiment's failure mode (forced margin spent on days that did not need it). This
  needs the same seed-11 A/B the source doc ran for the pin fix, and running it requires a code
  change, which was out of scope here.
- Whether the more surgical form of (b) -- slack only on a tour's last stop, inside the `_solve` /
  `router.py` acceptance check -- is actually where that check lives; `router.py` was not read this
  session.
- Whether the executor (whatever reads `state["routes"]` every hour after the dawn solve) could be
  changed to bind by landing tile rather than index for (c); the binding code past
  `_router_acts` line 1843 was not located.
- Whether `_hires_this_turn` gaining the `_unwalled_landing_slots` cap, by itself, closes day 10's
  gap or only shrinks it further (there may be a third layer under this one); not measured.
- Experiment 1 covered three days (9, 10, 11) of one seed on one tape. The claim "settles within two
  corrections" is well short of a season-wide guarantee; it is what was observed, not a proof.

## Artifacts

- `data/logs/two_pass_experiment_2026-08-12.log` -- Experiment 1's full output.
- Experiment 1 and 2 scripts: read-only, run from repo root, not committed (scratchpad only, per
  the no-code-change constraint). Reproducible from the snippets embedded in this doc's tables plus
  `scripts/breakdown.py`'s `TAPES["victor"]` / `env_config` / `tape_policy` helpers, which is all
  either script imports beyond the schedule agent module itself.
