# Supply-management defects in the market emission block: fertilizer and wheat

Merged 2026-08-13 from two write-ups on the same class of bug — a day-level purchase/reservation
budget missing from the market emission block in `schedule_agent.py`, so a sell row or a per-turn cap
drains a shed stock that a same-day work stop still needs. Source files deleted:
`d16_fertilizer_starvation_2026-08-12.md` (open, three ranked fix candidates) and
`fable_the_wheat_churn_2026-08-09.md` (closed, fix shipped).

Both dated after the 2026-08-08 `townCenterSellInterval` switch (current economy); neither touches
CARROT/TOMATO/EGG.

## Fertilizer: sold out from under its own fertilize stops (OPEN)

**d16 (seed 11, tape victor): FERTILIZE offered 12, emitted only 6** (tape: 13); WATER offered 39,
emitted 50 (tape 59); 0 uncovered jobs, 96 turns of priced slack — the crew wasn't busy, the *work
wasn't doable*.

**Mechanism:** `_apply_unit_action` fails FERTILIZE silently on an empty hand (`kaggriculture.py:465`)
— the plan and the walk happen, but the fertilize op never fires and nothing reports it. Per-unit d16
table: u8 got all 3 planned FERTILIZER; u3 got 1 of 2; u12 got 0 of 1 (recovered 1 via COLLECT);
**u13 planned a 6-unit FERTILIZER draw and got 0 of 6.**

**Root cause is 4 days earlier, not a d16 routing defect.** Dawn shed fertilizer tracks the tape
exactly through d10 (`5/5, 5/5, ... 15/15`), then diverges and never recovers (d11 `10/12`, d12
`4/9`, d13 `4/12`, d14 `1/12`, d16 `10/12`). `collect_fert` production is identical to the tape every
day d9-d16 (12/12) — it's not produced differently, it's **spent** differently: the sell rows ask for
`FERTILIZER: 24` (d11), `14` (d12), `8` (d14) out of the same stock the day's own fertilizing needs.
`fertilize` first goes wrong at d12 (2/3), the day after stock first diverges.

**Worth noting:** FERTILIZE sets `fertilized_until_day = day+2`, doubling WATER's yield for 3 days —
a missed fertilize costs 3 days of half-value watering on that tile, part of why `water 50/59` also
trails without any routing defect involved.

**Landmine flagged: `SUPPLY_LIMITS_EVERY_DRAW` (refuse jobs whose supply is short) is OFF** because
it measured worse three times (work down, idle up, d16 money 7,293→3,280→0). Do not re-enable
without pairing it with a purchase-triggering rule.

**Three candidate fixes, ranked:**

1. **Don't sell fertilizer the day's own plan is going to spend** — reserve the planned draw before
   filling the sell quota. This is where the divergence is created and is the top candidate.
2. **Buy the shortfall via `BUY_PRODUCT`** (base price $100) — we hold $14,407 at dawn on d16 with 96
   idle turns, so the precondition is already met.
3. Cap the planned depot pick at real shed stock, and give surplus stops to units whose tour already
   includes COLLECT_FERTILIZER.

**Status note:** the most recent commit on this branch as of this pass ("Hold back the fertilizer
the field is about to ask for") is very likely candidate (1) implemented — check
`schedule_agent.py`'s current fertilizer sell-reservation logic before re-diagnosing this as still
open.

**Two side findings from the same run:** d18 has exactly one uncovered job (`(0,0)`
WATER/FERTILIZE/HARVEST) and that tile dies (weeds 2→4, strawb 35→33 at d18); **d19 is where the
season turns** — leading $23,454/$22,551 at d18, trailing $26,215/$27,133 at d19.

## Wheat: a purchase-budget defect, not a selling one (CLOSED, fix shipped)

**Reframing evidence, 66 of our own 1.32.6 ladder replays** (`townCenterSellInterval=24` only): we
buy **1,099 wheat units/season** against the field's 266-392 (Rayk 266, Lester 266, kakuteki 266,
Syed 323, HealthStone 293, Seb 392). Selling is downstream of over-buying, not the primary anomaly —
money outcomes across the same replays show no clean correlation with sell volume (Rayk/Lester sell
only 305, bank $125-130k; Syed sells 649, banks $101k; Seb sells only 84, banks $74,264),
undermining a pure sell-side framing.

**Mechanism:** the feed-buy sizing term `herd = feed_days(day)*alive - fed_today - on_hand` in
`schedule_agent.py` had **no day-level purchase budget**, bounded only by the per-turn
`FEED_TURN_CAP=6` (a 144/day theoretical ceiling), and dominated the emission formula from ~day 12
onward. Measured on seed 11 vs Seb's tape via `kagg.analysis.fills.record_fills` ground truth:
unfixed bought 1,800, sold 1,456, banked $45,797 — herd path hit `FEED_TURN_CAP` on 20-24 of 24
turns every day from d17-29.

**Shipped fix: `FEED_BUY_CEILING_DAYS=2`** — adds a `herd_ceiling` (credited on asks, via
`state["ordered"][("feed","WHEAT")]`) and a `herd_floor` (credited on arrivals,
`alive - fed_today - on_hand`, so a real shortfall is never silenced). Swept at 1/2/4:

```
FEED_BUY_CEILING_DAYS=1  bought unchanged-tight, causes REAL herd starvation:
                          day 16->17 herd drops 20->14 with zero recovery, wheat sitting idle in
                          the shed (16-19 units) while only 7/20 animals get fed -- under tight
                          supply the bottleneck is crew/routing capacity to physically deliver
                          wheat, not wheat supply itself.
FEED_BUY_CEILING_DAYS=2  SHIPPED. bought 797 (-56%), sold 458, bank $46,370 (+$573 vs unfixed),
                          zero herd drops across all 30 days.
FEED_BUY_CEILING_DAYS=4  bought 1,328 (-26%, barely bends the curve), bank $46,834,
                          zero herd drops.
```

`=2` cuts purchases 56% at bank parity (+$573) with the same zero-herd-drop safety record as
unfixed — the shipped value. **The deeper routing/labor constraint the `=1` experiment exposed —
crew can't physically reach 20 animals in one day even with abundant wheat in the shed — is
explicitly NOT fixed here**, a separate, deeper bug flagged for future investigation.

**Two false leads recorded, so they are not repeated:** `PYTHONHASHSEED` was ruled out directly
(pinned 0/1/2 and default all gave identical 373); a run-to-run discrepancy (1,800 vs 373) turned out
to be caused by a second, concurrent session editing the shared main checkout mid-investigation,
silently injecting an unrelated in-flight fix (`FEED_BUY_TURNS_PER_DAY`) — resolved by reconstructing
the true "before" state via reversing the investigation's own diff. General warning: do not re-read
a shared checkout mid-session from an isolated worktree.

Tests: `tests/test_the_herd_buy_has_a_day_budget.py`, two tests, revert-and-confirm done per
`CLAUDE.md` discipline (reverting turns the budget test red again while the anti-starvation test
correctly stays green on unfixed code too, confirming it isn't accidentally carrying the whole
signal).
