# The spawn-ring misprediction, and why routing can be solved offline

Merged 2026-08-13 from three 2026-08-12 write-ups: `spawn_ring_misprediction_2026-08-12.md` (the
discovery and a reverted fix attempt), `fable_spawn_ring_verdict_2026-08-12.md` (a follow-up review
ranking the fix options and finding a second bug), `the_route_is_precomputable_2026-08-12.md` (a
related but structurally distinct finding — the board is a deterministic constant, so routing can be
solved with a much larger offline time budget). All three source files deleted.

## The mechanism (seed 11, tape `victor`)

`_end_of_day` discharges the whole crew every night; `_arrivals` predicts landing tiles using the
spawn ring **before** the farmer's hour-0 move, but hires settle in the market phase which runs
**after** the unit phase — so every hand lands one ring slot early than planned. Worked example on
d11: predicted `(5,4)(4,5)(5,5)(4,4)...`, actual `(4,4)(5,4)(4,5)(5,5)...`.

**Cost:** u10 on d11 was priced at 23 turns against a 23-turn budget (zero slack); it woke 2 tiles
off, ended 2 tiles short at `(1,2)`, which then weeded (`consecutive_unwatered >= 2`).

## Fix attempted and REVERTED — pinning the farmer is a measured loss

Pinning the farmer on hire turns to force the prediction true was tried and reverted: 17-day grid
money@d16 baseline **17,459 → 16,044**, strawb 35/36 → 33/36, weeds 2 → 4 — `(1,2)` was saved but
three other tiles died in its place, because pinning costs a turn of the 24-turn unit on nearly
every hire day. With the pin on, d11 goes fully green and d10 improves from 14 wrong to 7, isolating
a residual second cause: later-wave hires whose h0-computed prediction goes stale by the time they
land.

**Everything else tried and ruled out on the same seed/tape:**

```
pin farmer                          LOSS      (above)
predict-walks-off-ring              breaks the d9 control (day-dependent behavior)
two-pass re-solve                   initially "doesn't fit time budget" -- see below, now viable
tour slack (START_SLACK_TURNS 1,2)  LOSS      money 26,889->27,538 only by doing less work,
                                               wrong trade on an Elo ladder
buy fertilizer ahead                NULL      order-timing mismatch, and the underlying premise
                                               had already expired (see below)
COVER_PLANNER=False                 bit-rotted, not a valid comparison
```

**Two retractions on the record from this investigation:** "the tape wastes turns watering
pastures" was wrong — board-state contamination from comparing against our own tiles, retracted. And
the fertilizer-starvation premise behind the "buy fertilizer ahead" arm had already expired by the
time it was tested — `FERTILIZER_RESERVE_LOOKAHEAD_DAYS=1` had already fixed supply (shed now holds
14-20 vs the tape's 12-13; u13 gets all 6 FERTILIZER it asks for vs 0 before).

### The d16 water gap, resolved into two parts

A tour probe found only 2 assigned jobs all season where the unit never stood on the tile it was
assigned (both u13 FERTILIZE) — execution is not the general problem: 39 waters offered, 0
uncovered, 50 idle turns, 96 turns of priced slack on d16. The apparent `water 53/59` gap splits:
a **counting artifact** (op-count 53/59 masks identical 45/45 tile coverage; the tape wastes 14 ops
as no-ops, we waste 8) and a **real deficiency**: weeds 3/0 — we lose `(1,2)` STRAWBERRY (d11),
`(2,0)` WHEAT (d14), `(9,0)` WHEAT (d18); the tape loses zero all season. Cadence matters most for
non-ongoing crops (WHEAT, MELON), where a missed water inside the yield window is permanently lost
yield, not just weed risk.

## The follow-up review: is the two-pass re-solve viable, and a second bug

A second review confirmed the whole prediction sequence
(`_hires_this_turn` → `_clear_the_spawn_ring` → `arriving` → `_router_acts`) runs exactly once per
day at hour 0, and tested a two-pass re-solve directly:

```
day 9    converges in 1 pass (control)
day 11   converges in 1 pass
day 10   needs 3 passes to reach a fixed point (not 1)
```

Settles within 2 corrections on every day tested, but does not converge in 1 pass always.
Wall-clock cost of the hour-0 solve: 0.000-0.002s (d0-6) → 0.075s (d8) → 0.127s (d9) → **0.372s
(d10, 14 hires)** → 0.326s (d11) → 0.426s (d16) → 0.496s (d17). **Three solves at day-10's 0.372s is
over 1.1s, exceeding the 1s `actTimeout`.**

**Recommended order: (b) first, (a) second, not (c).**

- **(b)** dock a second turn off phantom-vehicle budget at `_router_acts` line 1697-1698 — cheap, no
  extra solve cost, bounds the error to Manhattan-2 regardless of cause. Ship this first.
- **(a)** the two-pass re-solve, capped at 2 iterations with a wall-clock guard, second.
- **(c)** binding by landing tile was checked concretely on day 11: predicted per-tile counts
  `(5,4):3 (4,5):3 (5,5):2 (4,4):2` vs actual `(4,4):3 (5,4):3 (4,5):2 (5,5):2` — not the same
  multiset, so binding by landing tile doesn't fix the count mismatch. Do not pursue.

**A new, previously undocumented bug (d): `_hires_this_turn` (line 416) sizes `n` purely from bank
affordability and does not apply `_unwalled_landing_slots`, but the market block that actually emits
HIRE orders (line 3864-3865) does.** They diverge on land-buying days — confirmed live on day 10
(`hands:14, land:1` in `schedule.json`), where days 9 and 11 are `land:0`. **This is the dominant
cause of day 10 being the hard case**, not wave staleness alone.

**Framing check that survives both fix attempts:** the scheduler prices zero margin anywhere — ~20
tiles sit one missed-water from death every day by the watering cadence's own design, so any 2-turn
perturbation from any cause converts to a dead tile.

## Routing is precomputable offline — the board is a deterministic constant

`_initial_tile` and `_default_spawn` are pure functions of coordinates; the only RNG in
`kaggriculture.py` (`random.Random((seed*1_000_003)^day)` at line 858) governs only the shop-unlock
draw and `_spawn_weeds`. Geometry, depots, shed-access tiles and walking distances are therefore
identical in every game — the seed only changes what's worth selling and where weeds appear
(caveat: real-ladder `weedSpawnChance=0.005` introduces some drift; our own grids run at 0.0).

`scripts/solve_day_offline.py` reuses `cover.py`'s own cost model (not a second, possibly-optimistic
model) with a raised LNS deadline and restarts, and confirmed a real defect on seed 11/victor:

**d12 is a real defect.** The shipped greedy planner covers 48/49 (one job left uncovered:
`(9,1)` WATER/HARVEST/PLANT); the offline solve covers **49/49 in 5s, on both restarts
independently**; per-unit turns run 14-21 against a 24-turn budget — slack on every hand, i.e. an
**assignment failure, not a capacity failure.**

**d18 is NOT a defect** — a previously reported "66 of a proven 67" does not reproduce from the
saved fixture (which contains only 66 jobs total); that lead is closed.

The existing ruin-and-recreate (LNS) code already solves d12 given 5 seconds, but is capped in-game
at `RUIN_AND_RECREATE_SECONDS = 0.25`, where over a full 20-day season it measured slightly WORSE
than off (work 1591 vs 1613) — **the mechanism is right, the budget is wrong.**

**Capacity is not the binding constraint generally.** Over d0-d19, seed 11 vs victor: we work more
(1,613 vs 1,556), move more (1,646 vs 1,536) and idle less (539 vs 692) than the tape, yet still bank
less ($26,105 vs $27,133) — we already have a turn surplus, and better routing alone won't close the
gap. The lever is job mix, not turn count.
