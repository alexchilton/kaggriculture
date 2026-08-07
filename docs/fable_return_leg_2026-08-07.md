# The return-leg defect is real, but "stale budget" is the wrong name for it

Investigated 2026-08-07, seed 11, weeds off, tape `seb`, days 3-4 only.
Scope: the day-by-day tape match, per `CLAUDE.md`'s testing discipline.
No code in the tracked working tree was changed.
All experiments ran in a scratch git worktree at `/tmp/kagg-attempt3`, seeded from the current (attempt-1) `router.py` and `schedule_agent.py`, since those files carry uncommitted changes not present at `HEAD`.
The worktree was removed after the investigation; the tracked tree is exactly as it was handed over.

## Verdict on the stated hypothesis

**Killed, not confirmed — but its intuition was pointing at a real neighbour of the actual bug.**

The stated hypothesis was: `budget = TPD - hour - 1` is computed once per replan, only idle units get topped up, so a unit committed early keeps a tour costed against a budget that "no longer exists" by the time it walks it.

I instrumented `RT.plan_routes` to log, on every call during day 3, the hour, the budget passed in, and the `used[u]` cost each committed route was accepted at (log: `day3_replans.log` for attempt 1, `day3_replans_attempt3.log` for a reproduced attempt 3).
Every commitment I traced was accepted at a cost `<=` the budget that was live at that exact call.
Turn accounting is 1:1: every hour that passes, the unit either walks one route step or the step gets popped for free (a stale no-op node costs zero turns, it just shortens the day).
I could not find a single case where a unit's realised turn spend exceeded what its budget allowed at commit time, under either attempt 1 or my reproduction of attempt 3.
`budget` itself is never wrong about what it claims to model (turns remaining today) and it is recomputed fresh, correctly, on every call — full replan or top-up.

So the turn-budget bookkeeping is not stale.

## What is actually happening: a phantom prize, not a stale number

Traced `RT.build_nodes` directly (script logic below) on day 3 and day 4.
Day 3, hours 1 through 17, with exactly **one** COW sitting in the shed (later carried by whichever unit drew it):

```
hr1  shed_COW=1  PLACE-candidate tiles: [(0,3), (1,3), (0,4)]   each priced $1840
hr3  shed_COW=0  carried_COW=1   PLACE-candidate tiles: [(0,3), (1,3), (0,4)]   still all three, still $1840 each
```

Day 4, hours 10 through 23, with one COW in the shed all day:

```
hr10 shed_COW=1  n_candidates=2  tiles=[(0,3), (0,4)]
hr23 shed_COW=1  n_candidates=2  tiles=[(0,3), (0,4)]   -- never placed all day under the closed-tour variant
```

`(0,3)` and `(0,4)` are two pens built on an earlier day that a shortfall of animal purchases left permanently empty — that backlog is a pre-existing fact of this tape/schedule pairing, not something introduced here, and it is not the bug.

The bug is in `RT.build_nodes`'s PASTURE/COOP branch (`kagg/search/router.py`, the `elif kind in ("PASTURE", "COOP")` block, currently around line 439-476):

```python
for a in R.ANIMAL_NAMES:
    ...
    if shed.get(a, 0) > 0 or carried.get(a, 0) > 0:
        ...
        ops = [("PLACE", a, max(1.0, served))]
        break
```

This is evaluated **once per empty pasture tile**, independently, and it only checks that the shed holds `> 0` of the animal — never how many empty pastures are simultaneously making the same claim.
With one COW and three empty pastures, `build_nodes` hands back three separate `Node` objects each worth the full $1840, as if three cows were available.
`plan_routes` has no mechanism to notice this: `held` (`kagg/search/router.py:546`) and `depot`/`depot_at` are **per-unit** counters, there is no cross-unit ledger of how much of a `DRAWN` item is actually left in the shed once other units in the same planning pass have already claimed it.
So cheapest-insertion can and does commit **two or three different units** to "the" COW in the same pass, each with `needs = {"COW": 1}`, each believing it alone will collect it.

The conflict is only ever resolved for real at execution time, in `schedule_agent._router_acts`'s draw loop (`kagg/search/schedule_agent.py`, currently around line 478-489):

```python
for item, qty in st["draw"].items():
    short = qty - inv.get(item, 0)
    if short > 0 and shed.get(item, 0) > 0:
        draw = (item, min(short, shed[item]))
        break
```

This reads the **live** shed, which is correctly scarce — the first unit to reach a depot with the item still in stock gets it, `shed[item]` goes to zero, and every later claimant's `PICKUP` silently draws nothing.
That loser then walks all the way to its assigned empty pasture, finds `inv.get(a, 0) == 0`, gets `[]` from `_live_ops`, pops the dead stop, and only then discovers it is carrying nothing useful and has to walk home — with however much of the day happens to be left.

This is present in **every attempt**, including the currently-exact attempt 1. Confirmed directly: under the current tracked code, day 3 sends **two** separate units on this exact wasted trip.

```
attempt 1, day 3 (current/tracked code, day 3 is EXACT)
  u7  hr11 walks south into (0,3), hr12 already turning back east -- no op found, arrived and left same-ish hour
  u1  hr14-18 walks west through the placed (1,3) pen and on to (0,3)/(0,4), hr19 turns back
```

Both losers recover: `u7`'s round trip is short and early, `u1` turns back at hour 19 with four hours of daylight left, comfortably enough to walk home and drop.
Day 3 still comes out exact not because the phantom-node bug is fixed, but because under attempt 1's costing this particular waste happens to land early enough in the day to be free.

```
attempt 3 reproduction (closed-tour-in-ratio), day 3
  u6  hr17-20 walks WEST from the depot to (0,4), arriving hr21, no op found (COW already placed by u4 at hr14)
      hr21-23: only 3 hours left, needs 4 to walk home -- still walking at day's end, carrying an
      uncollected fertilizer picked up at hour 12 that never reaches the shed
  bank at day-3 dusk: $291 (attempt 3) vs $483 (attempt 1) vs $482 (tape)
```

Same bug, same tiles, same single COW. What differs is **when** the wasted trip gets scheduled, and that difference is a direct, and in this instance correct, consequence of the return-leg fix doing its job: a correctly-priced closed-tour ratio ranks a phantom, low-marginal-value node behind genuinely productive work, so it gets deferred to whatever's left of the day — which on day 3 turns out to be too little to survive discovering it was fake. Attempt 1's cruder, order-independent reserve happens to schedule the same waste earlier purely as a side effect of being a worse approximation, not because it defends against the failure mode.

Day 4 confirms the same mechanism drives the animal-chain loss under attempt 3 (`place` 1/1 -> 0/1, `feed`/`care` 7/7 -> 6/7): the trace above shows the identical two-candidate ((0,3), (0,4)) oversubscription for the identical single COW, present from hour 10 to hour 23, with `PLACE` never landing at all that day under the closed-tour variant.

## Answering the three questions

**1. Is the stale-budget hypothesis right?**
No. Turn-budget accounting is internally consistent in every variant tested; I could not produce a case where a committed route's realised cost exceeded the budget it was accepted under. The hypothesis's *shape* — something committed early becomes invalid by the time it is executed — is correct, but the thing that goes stale is not a turn-count, it is the **truthfulness of a node's prize**, which was never true for more than one claimant in the first place. `plan_routes` recomputing `budget` correctly every call was never the weak link.

**2. If not the whole story, what is, and why does attempt 3 lose day-3 fertilizer and day-4's animal chain?**
`RT.build_nodes` prices scarce, `DRAWN`-item nodes (currently: PLACE and BUILD, both gated on an animal in the shed) per **destination tile**, not per **unit of the resource actually available**. With one physical animal and several empty pastures, it manufactures one full-prize `Node` per pasture, and `plan_routes` has no cross-unit ledger to catch the oversubscription — only the live shed at `PICKUP` time enforces scarcity, and by then a unit may already have committed its whole remaining-day budget to reaching a tile that has nothing for it. This bug predates and is independent of all three return-leg attempts. It happens to be harmless under attempt 1 only because attempt 1's costing (not by design) schedules the resulting wasted trips early enough in the day to recover from. The closed-tour-exact marginal in attempt 3 is not what breaks day 3 or day 4 — it is what correctly reprioritises a fake node to the tail of the day, which is exactly where a real oversubscription bug does maximum damage, because the tail is where there is no slack left to absorb discovering the waste.

**3. What should the fix actually be?**
Two separate, orthogonal fixes, not one:

- **Keep (or re-adopt) the closed-tour-exact marginal from attempt 3.** `cdelta = delta(u, n, i) + homeward(u, n, i) - homeward(u)`, used for both scoring and acceptance, is the textbook closed-tour insertion cost and — confirmed by direct calculation during this investigation — it is exact at every insertion position, not only when a node happens to land at the current end of the route. It is what correctly rescues the day-4 far-corner tile and it should not be abandoned in favour of the cruder flat reserve, which is only "working" on day 3 by accident of timing.

- **Give the router a genuine scarce-resource budget, the same shape it already gives turns.** Right now `TPD - hour - 1` is a real, shared, decrementing budget that every acceptance test checks. The shed's stock of a `DRAWN` item has no equivalent: `held` and `depot` are per-unit, and nothing stops two different units, in the same planning pass, from each being told "yes, you can have the one COW." The fix is structural, not a threshold tweak: introduce a **cross-unit remaining-supply counter** for each `DRAWN` item, seeded from the true shed count (plus whatever is already `carried`), decremented the moment `commit()` books a `short` draw for that item against *any* unit — and gate a node's eligibility on that shared counter, not merely on the per-unit `_uncovered` check. Once the one COW is claimed by whichever unit's insertion wins the greedy pass, the *other* pasture nodes for COW must drop out of `left`/`remaining` (or their needed quantity must read as unavailable) for the rest of that same `plan_routes` call, not just get discovered wrong three hours later at the shed. This is the same fix in spirit whether it is enforced in `plan_routes` (a `reserved = collections.Counter()` checked against `shed`/`carried` totals passed in alongside `carry`) or upstream in `build_nodes`/`_refresh_pins` (cap the number of PLACE/BUILD candidate tiles emitted to the actual animal count on hand). The former is more general — it also protects `BUILD`, and anything else `DRAWN` that becomes scarce in the future — and matches the pattern the router already trusts for turns.

Doing only the first (closed-tour marginal) without the second is what produced attempts 2 and 3's regressions: it is not that the return-leg math needs to be softened, it is that it exposes a pre-existing hole in resource accounting that the cruder costing was accidentally papering over. Doing both together should let day 4's far-corner rescue stand without re-breaking day 3, since the thing that actually stranded day 3 — a unit chasing a COW that had already gone to someone else — stops being schedulable at all once the second unit's candidate node is correctly retired the moment the first unit's claim is committed.

## What I did not do

Per scope: did not measure or optimise season-long bank, did not touch tracked files, did not implement the fix (this was requested as diagnosis plus the shape of the solution, not a patch). The two check scripts used for the `build_nodes` tracing (`/tmp/check_place_nodes.py`, `/tmp/check_place_nodes_d4.py`) and the scratch worktree (`/tmp/kagg-attempt3`) are outside the repo and were not left behind as part of it.
