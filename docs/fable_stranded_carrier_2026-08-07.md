# Fable on the stranded carrier and the wasted walk, 2026-08-07

Asked after I had measured three failing attempts and could describe the defect but not fix it.
Baseline at the time: commit `b206e06`, 120 cells,
`d0=7 d1=6 d2=4 d3=7 d4=7 d5=7 d6=11 d7=8 d8=11 d9=14 d10=19 d11=19`.

## What he rejected, and why

**(b) "let a dead-route unit walk home and DROP" is already implemented** -- `schedule_agent.py`
lines 1117-1127.
u2 *does* do this, from h21.
It fires five turns too late to matter: (1,3) is 4 steps from the depot ring with 3 turns left.
So this is not a missing feature, it is a feature that starts too late.

**(a)/(c) as a general `_live_ops` hoist is what Attempt A already was.**
The byte-identical 168 from Attempts B and C proves the item-supply narrowing *never fired*, and he
read that correctly: the regression is not coming from wheat/fertilizer-gated stops at all.
It comes from every other reason a node dies early -- a crop finishing, a PLANT stop whose
`seeds[crop]` a teammate just consumed, a WEED someone else dug.
B and C tested "is anything needed anywhere", never "is the current head specifically the
unservable one", and since seeds are never in `shed`, a PLANT stop always read as unsupplied and
popped unconditionally.
The hoist revalidates *everything*, which is the `idle +159` cascade.

## Fix 2 -- the one nobody had tried, and his first recommendation

`st["draw"].clear()` is a **permanent, one-shot abandonment, not a retry.**

`st["draw"]` is set once at `plan_routes` time and is never repopulated; the only thing that ever
happens to it afterwards is `.clear()`.
So the first turn the draw block finds the shed momentarily empty, the need is gone *forever* for
that committed route -- regardless of day 6 buying wheat nine more times afterwards
(h3, 5, 6, 7, 8, 9, 11, 13, 15).

> "This isn't a policy tradeoff, it's arguably a plain bug: 'abandon' and 'not available yet' are
> being treated identically."

`why_u2_route_dies.py` only starts logging at h14 and u2's pasture stop is already stuck at
`routelen=1` by then, so the clear plausibly happened hours before h17 -- u2 wrote off the wheat
before most of the day's nine purchases had even landed.

The fix is to retry the draw every turn rather than clear on a momentary miss, clearing only once
the associated node is popped or the need is genuinely fulfilled.

## Fix 1 -- the corrected version of B/C, to layer on only if needed

Scope the head-pop to `Node.needs` (the field already exists, `router.py:510`) rather than hoisting
`_live_ops` wholesale.
`st["draw"]` is the *whole tour's* aggregate need (`depot[u]` from `plan_routes`), not the current
head's, so clearing it wipes every future stop's draw memory too.
Narrower: before clearing, check whether `st["route"][0].needs` overlaps what is unavailable, and
only then pop that head -- leaving every other stop's draw intent alive and every non-supply-related
pop untouched.

## How Fix 2 could regress d0-d5 -- his own warning

If `st["draw"]` becomes retryable, then on any turn the shed happens to hold some needed item the
unit will divert toward a depot (lines 977-983) **mid-tour**, however far through its route it is.
Early days churn the shed hardest -- day 0 buys land, seed and several animals in one morning.

He cites the directly analogous precedent already in the repo: the `SUPPLY_LEDGER` note at
`router.py:679-687`, where extending scarcity-tracking to every drawn item cost day 0
`feed`/`care` 4/4 -> 3/4, because refusing supply on "not available right now" refuses work that
becomes fundable moments later.
A retryable draw is the mirror-image risk, and would reproduce the PICKUP/DROP thrash that the
`OPPORTUNISTIC_DROP` comment (lines 1039-1041) exists to prevent.

**So gate the depot diversion against remaining slack** the way `DELIVER_FERRY` already gates its
detour (`_route_turns`, line 602), rather than letting any nonzero shed stock trigger a walk.

## His bottom line

- Try **Fix 2 first**: untested, the most literal reading of "the draw was cleared, the stop
  remained", and needs no new judgment about when to abandon a stop.
- Layer **Fix 1** on top only if wasted walking persists.
- Do **not** pursue (a)/(c) in general form -- `idle +159` and the day-0 `SUPPLY_LEDGER` precedent
  point the same way.
- Measure exactly as Attempts A-C were measured. His closing caveat, which is fair:

> "this is a plausible read of the code and the two logs, not a certainty, and the project's own
> history (BOTH SUPPLY_LEDGER and the late-delivery arm) shows 'obviously correct' fixes here have
> flipped sign before."
