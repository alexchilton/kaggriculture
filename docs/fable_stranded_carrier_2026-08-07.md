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

---

# Second round: after Fix 2 was measured at 125 and reverted

Reported back: Fix 2 gives d0-d6 byte-identical, then d7 8 -> 11 and d11 19 -> 21.
His regression prediction was right in mechanism but landed on d7, not d0-d5 -- keeping the draw
alive pulls units back to the depot mid-tour once stock arrives, and d7 is exactly the day the
steal gate had just bought from 15 down to 8.

## His answer to "is the slack-gated retry worth running"

Second priority, not first.
The mechanism is right -- a freshly-packed tour from `STEAL_FROM_DAY` has near-zero slack by
construction, so `detour <= slack - margin` should correctly refuse there -- but it is a broader
change than it looks: it still lets *any* unit with slack divert *any* time stock appears, on
*every* day, so it has more surface area for another cross-day coupling surprise.

## His recommended one shot: clear a route that is provably dead, before walking it

Insert immediately before the walk-the-tour loop:

```python
if (any(v > 0 for v in inv.values()) and st["route"] and not st["draw"]
        and all(not _live_ops(n.tile, tiles[n.tile[1]][n.tile[0]], day, inv, pins, seeds)
                for n in st["route"])):
    st["route"].clear()
```

Three conditions, each deliberately narrow:

- **`not st["draw"]`** -- the tour's depot need has already resolved or already been abandoned.
  This is the condition B and C were missing, and it is why they revalidated live routes and
  cascaded.
- **`all(...)` over the WHOLE remaining route, not just the head** -- a route with a HARVEST or
  WATER node in it (neither gated on a drawn item) cannot satisfy this, so it fires only on the true
  dead-end shape.
- Reuses `_live_ops` exactly as the arrival check already does. No new liveness judgment, just asked
  earlier.

For u2 this is true from **h17**, not h21 -- once the melon node pops and the route is down to the
single dead pasture stop with `st["draw"]` already empty.
That is a 4-turn head start.
(1,3) is 4 steps from the depot ring; at h17 seven turns remain, so the **already-implemented** tail
at lines 1117-1127 gets home with 3 to spare instead of arriving one short.
No new DROP code, no new redirect logic.

Why he argues this is a different bet rather than a rerun: it never touches a head still covered by
a pending draw, and it never interrupts otherwise-live work for supply.
It clears only once every remaining stop is *simultaneously* proven dead.

**The risk he flags and cannot rule out without measuring:** an animal node dead only because *this*
unit lacks wheat could become servable for CARE alone if a *different* unit feeds it first
(`fed_today` flips without this unit's involvement).
If two routes ever service the same pasture, clearing early gives up a stop that would have revived.
He expects this to be rare because nodes are generally claimed by one route.

## His answer to "is this worth any more effort"

Run this one attempt. **If it also regresses, stop -- do not chain into the slack-gated retry.**

> "Five attempts is already more cycles than a $600 defect has earned, and the pattern across all
> four -- hoist regresses d0, gated hoist is inert, retry regresses d7/d11 -- is consistent with
> 'every general-purpose lever here costs more than the fertilizer it rescues'."

He agrees the arithmetic favours the seed overbuy: ~$600 season-wide against `buy_seed` +42/d6,
+33/d9 and a -$1,466 day-10 swing that costs a whole quadrant.
He holds the line at one more shot and calls strict-xfail-and-move-on fully legitimate.
