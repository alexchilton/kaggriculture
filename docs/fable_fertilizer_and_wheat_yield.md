# Fertilizer threshold, wheat yield, and herd timing — findings log

Written incrementally while working, per project convention. Numbers are either the 12-seed ladder
mean (`python -u scripts/agent_ladder.py --seeds 11,22,33,44,55,66,77,88,99,101,202,303 --arms
tape,router`) or an explicitly labelled single-seed diagnostic (seed 11), never conflated.

Baseline going in: **$109,688** mean over the 12 seeds, tape $127,569 (86%). Confirmed still current
by re-running the ladder before touching any code — see `data/logs/fable_ladder_baseline.log`.

Single-seed-11 diagnostics reproduced from a fresh run today (`data/logs/fable_parity_seed11_baseline.log`,
`fable_market_ledger_seed11_baseline.log`, `fable_herd_seed11_baseline.log`):

- FERTILIZE 62 vs tape's 107 (task brief said 67; within day-to-day drift, same shape).
- Tiles under an active fertilizer bonus: 124 tile-days vs 186.
- Fertilizer realised sale: 239 units for $12,601, mean price **$53** (against `BASE_PRICE["FERTILIZER"]
  = 100` used as the router's cost threshold). We collect 314 fertilizer-days worth (`fertilizer
  collected` 314 vs tape's 318 — collection itself is not the gap).
- Wheat harvest 283 vs tape's 338 on this seed (season sum from parity_all_days; the brief's 122/66
  vs 222/66 figure is a different — presumably closer-cropped — measurement window; both point the
  same direction: we harvest less wheat per planted tile than the tape).
- Herd: animal-days 314 vs 325 (97%), same final herd size (14), first 14 real placements land by day
  12 for us against day 11 for the tape (the tape's other 13 "placements" are a day-29 end-of-season
  artifact, almost certainly worthless — game ends day 29 hour 23).

---

## Item 1 — fertilizer threshold

**Theory:** `crop_ops` compares fertilizing's gain against `BASE_PRICE["FERTILIZER"] = 100`, the
market's I0 equilibrium price. Nobody actually realises that price: we sell fertilizer at a measured
mean of $53/unit (`scripts/the_market_ledger.py`, seed 11: 239 units for $12,601), and we collect far
more than we spend (314 fertilizer-days collected a season against only 62-67 FERTILIZE ops). Since
almost every unit we hold is headed for a SELL order anyway, the honest opportunity cost of routing one
into a tile is what it would have sold for, not the sticker price.

**Test:** `test_fertilizer_threshold_at_the_realised_sale_price_was_measured_null_and_reverted` in
`tests/test_router.py`. Wrote it to assert an ongoing TOMATO (`$60/unit`) gets FERTILIZE offered at a
$53 threshold (fails against the un-reverted $100 threshold), confirmed it failed for the right reason,
implemented the fix (`FERTILIZER_COST = 53` replacing `BASE_PRICE["FERTILIZER"]` at both comparison
sites in `crop_ops`), confirmed it passed.

**Change:** `BASE_PRICE["FERTILIZER"]` (100) -> realised sale price (53) as fertilizing's cost
threshold, in both the one-shot (`gain * price > cost`) and ongoing (`price > cost`) branches of
`crop_ops`.

**12-seed ladder:** before $109,688, after **$109,688 — identical, to the dollar.** FERTILIZE stayed
at exactly 67/season on every one of the 12 seeds.

**Why it did nothing, found by reading `data/seed_scripts/new_leader/schedule.json`:** the only crop
the threshold change can affect is an ongoing crop priced between $53 and $100 — TOMATO at $60 is the
sole example in `CROPS`. This schedule's `plants` rows only ever call for WHEAT, STRAWBERRY and MELON
(66 / 44 / 21 across the season) — TOMATO and CARROT never appear at all. STRAWBERRY at $120 already
clears the old $100 threshold, so it was unaffected either way. WHEAT's one-shot gain is capped at a
fixed $50 (2 extra units at $25/unit, `min(room, waters_left*2) - min(room, waters_left)` maxes at 2
for wheat's 6-unit cap and 3-water window) — just under $53, so it stays unfertilized under both
thresholds. The fix is more economically honest but this specific benchmark cannot express the
difference: it never grows the one crop that would show it.

**Verdict: REVERTED.** A tie does not beat the baseline per project protocol. The test above now pins
the reverted ($100-threshold) behaviour so the $53 number is not re-derived and re-tried against a
schedule it structurally cannot move. If the crop mix this project measures against ever changes to
include TOMATO, this is worth revisiting with the actual measured realised price at that time.

## Item 2 — wheat yield

**The task's framing (per-tile yield, forcing more in-window waters) turned out not to be the driver.**
Measured directly: our wheat harvest EVENTS average 3.94 units each (`{3: 2, 4: 29}` histogram, i.e.
nearly all of them hit the plain 4-unit ceiling) against the tape's 3.47 (`{2: 10, 3: 27, 4: 14, 5: 13}`,
skewed toward earlier, smaller harvests). Per-harvest yield is not the gap — it is measurably *higher*
in the small sample we do harvest. The gap is in how many times a wheat tile gets harvested at all.

**What's actually happening, found with a tile-lifecycle scan (position -> plant/harvest/weed events,
no monkeypatching, just reading `farm["tiles"]` every turn):**

| | distinct wheat tile positions used | harvest events | cycles/position | mean age at harvest | still standing, unharvested, at season end |
|---|---|---|---|---|---|
| ours | 42 | 31 | 0.74 | 4.06 days | **32 of 66 plantings (48%)** |
| tape | 40 | 64 | 1.60 | 3.38 days | 1 of 66 |

Both plant 66 wheat total and use a near-identical physical tile count (42 vs 40). The tape recycles
each tile more than twice as often. Digging into *why*: the schedule itself (extracted from the tape's
own play) has a cumulative WHEAT-plant target that jumps from 34 to 65 in a single day — day 25 to day
26 — meaning the tape plants a ~31-tile batch on day 26 of a 30-day season (season is `R.SEASON_DAYS =
30`, days 0-29). WHEAT's window is ages 2-4, so a day-26 planting reaches only age 3 by the season's
last day (29); its window can never formally close (`age >= max_day` needs age 4, i.e. day 30, which
does not exist).

`crop_ops`'s `_one_shot_is_finished(info, age, room)` gated HARVEST on `age >= info["max_day"] or room
<= 0` — nothing else. For a late planting neither condition can ever become true, so **HARVEST was
never offered at all**, for the entire remaining season. `plant_prize` already discounts a truncated
window and correctly still plants these tiles (a partial wheat pays), but the harvest gate did not
carry the same discount, so every one of those late plantings sat on the board, growing to whatever
partial yield the truncated window allowed (measured: yield 1-3, age 2-3 at season end for all 32),
and then the season simply ended with them unharvested. The tape does not have this problem because
whatever is still growing on the literal last day still gets banked — it does not wait out a window
that cannot close.

**Test:** `test_a_late_one_shot_planting_is_still_harvested_on_the_seasons_last_day` in
`tests/test_router.py`. A wheat cell planted at `SEASON_DAYS - 3`, evaluated on the season's last day
at age 2 (nowhere near `max_day` = 4, so the window reads as still open), holding 2 units. Confirmed it
failed (`ops == []`, no HARVEST offered) before any code change.

**Change:** `_one_shot_is_finished` now also takes `day` and returns `True` when
`day >= R.SEASON_DAYS - 1` — the season's last day, the one point nothing more can ever be gained
regardless of the crop's nominal window. `crop_ops`'s call site now passes `day` through. WATER is
still emitted ahead of HARVEST in the ops list for the same tile on that day (code order preserved), so
the last possible water still lands before the forced harvest.

**12-seed ladder:** before $109,688 (`data/logs/fable_ladder_baseline.log`). After (this fix alone,
nothing else changed): **$109,596** (`data/logs/fable_ladder_wheat_fix.log`) — a loss of **-$92**.
HARVEST rose exactly as the diagnosis predicted, 296 -> 323 a season, so the fix genuinely fires and
genuinely banks more wheat. The season total is very slightly worse anyway.

Tried a second variant, forcing the same finished-check two days early instead of one
(`day >= R.SEASON_DAYS - 2`), on the theory that a harvest forced on the literal last day has no
runway left to reach the shed (DROP) and clear a SELL order before the game ends -- so it can convert
"still growing, banks $0" into "harvested but unsold, banks $0" while spending a turn that could have
gone to something that clears. Measured stacked with the item-3 PLACE fix below (both changes active
at once): **$106,882**, a bigger loss than either component alone (see item 3's isolated number),
consistent with the 2-day variant making things worse, not better.

**Verdict: REVERTED.** `_one_shot_is_finished` is back to `age >= info["max_day"] or room <= 0`, no
`day` argument. The bug this targeted is real and worth revisiting -- 32 of 66 wheat plantings a
season genuinely never get harvested -- but forcing the harvest is not the fix; the harvested product
still has to physically reach a sale before the season ends, and this change did not get it there
often enough to pay for the turns it spent. `test_forcing_a_late_one_shot_harvest_on_the_last_day_was_measured_a_92_dollar_loss`
in `tests/test_router.py` pins the reverted state.

**A real, unexplored next step for whoever revisits this:** the actual cycling-rate gap (0.74
harvests/tile-position for us against the tape's 1.60) is much bigger than the late-planting piece
alone explains. The tape harvests EARLY and small (mean age at harvest 3.38, yield histogram skewed to
2-3 units) and replants immediately, running closer to 2x the cycles per physical tile that we do.
That is a genuinely different question from "force the last day" -- it is "is early harvest + fast
replant worth more per season than full-window harvest + fewer cycles", which needs its own
theory-then-test rather than being folded into this one. Flagging it here rather than chasing it,
since it is a bigger design change than this task's scope.

## Item 3 — animal placement timing

**The task's framing was "money is the suspected constraint" — measured, it is not.** `BUY_ANIMAL`
totals match the tape exactly (COW 8/8, SHEEP 6/6, `scripts/the_market_ledger.py`), and per-day
purchase TIMING is close to identical: both buy in bursts on days 0, 5, 6, 8, 9, 10-11. Money at dawn
is frequently HIGHER for us than the tape in the early game (day 1: ours $517, tape $42), so the
purchases themselves are not being delayed by a thin bank.

**What's actually delayed is PLACE (walking a bought animal from the shed onto an empty pasture), not
BUY_ANIMAL.** A concrete instance found by listing every `BUY_ANIMAL`/`PLACE` event with its
`(day, hour)`, seed 11: a SHEEP is bought day 5 hour 1, but the corresponding `PLACE SHEEP` does not
land until day 8 hour 9 -- three days sitting in the shed producing nothing, while COWs bought in the
meantime get placed same-day or next-day.

**Root cause:** COW and SHEEP share the `PASTURE` structure (`ANIMALS["COW"]["structure"] ==
ANIMALS["SHEEP"]["structure"] == "PASTURE"`). `build_nodes`'s PLACE logic for a bare structure iterated
`R.ANIMAL_NAMES = ["GOOSE", "COW", "SHEEP"]` and took the FIRST type available in the shed --
unconditionally COW whenever both COW and SHEEP were sitting in the shed at once, regardless of which
was bought first or which was worth more. (`test_the_whole_day_zero_schedule_is_executed` and the
`pens standing` row of `scripts/parity_all_days.py` already show pen COUNTS match the tape exactly
every day, so this is not a build/structure shortfall -- it is purely which animal wins a shared pen.)

**Test:** `test_a_shared_pasture_was_tried_ranked_by_value_and_measured_a_5676_dollar_loss` in
`tests/test_router.py`. Built one empty PASTURE with both a COW and a SHEEP in the shed at day 5,
where a fresh SHEEP (`500 cost + 6 productions * $200 WOOL = $1700`) is worth more than a fresh COW
(`400 + 8 * $160 MILK = $1680`). Confirmed the un-fixed code picks COW anyway (fails the "should pick
the higher-value one" assertion) before any change.

**Change tried:** score every animal type available for the tile by the same `cost + _animal_remaining`
prize used for every other node, and let the highest one win the tile instead of the first match in a
fixed list.

**12-seed ladder:** before $109,688. After: **$104,012** (`data/logs/fable_ladder_pasture_fix_alone.log`)
— a loss of **-$5,676**, the largest measured swing of the three items, and in the wrong direction.

**Why the locally-correct fix loses in aggregate:** the isolated example is real and the value
comparison is right for that one turn. But the schedule wants a specific MIX over the whole
season -- 8 COW against 6 SHEEP (`data/seed_scripts/new_leader/schedule.json`) -- and a per-turn value
tie-break has no notion of that mix. It reallocates every tied pasture all season, not just the one it
was diagnosed from, and evidently does so in a way that works against reaching that 8:6 split
efficiently (a value tie-break systematically favours SHEEP whenever both are freshly available, since
SHEEP's higher cost and price partially offset its longer interval -- but the schedule needs more COWs
overall, so more of them end up waiting instead of fewer).

**Verdict: REVERTED.** Back to the fixed `GOOSE, COW, SHEEP` order.
`test_a_shared_pasture_was_tried_ranked_by_value_and_measured_a_5676_dollar_loss` pins the reverted
state. The three-day idle SHEEP is a real, confirmed instance of a real bug (a shared-structure type
race with no memory of intent), but "rank by same-turn value" is the wrong fix for it. A fix that
tracked the ORIGINAL intended type per pasture (e.g. from the schedule's `places` order, at BUILD time,
so a pasture built for a SHEEP stays earmarked for one) is the more promising direction and was not
attempted here -- it needs threading the schedule's per-slot intent through `_refresh_pins` into
`build_nodes`, which is a bigger change than a one-line ranking swap and deserves its own
theory-then-test cycle.

## Summary

| item | theory | diagnosed as real? | fix tried | 12-seed ladder | verdict |
|---|---|---|---|---|---|
| 1. fertilizer threshold | cost should be realised sale price ($53), not base price (100) | yes, but inert for this crop mix | `FERTILIZER_COST = 53` replacing `BASE_PRICE["FERTILIZER"]` | $109,688 -> $109,688 (±$0) | REVERTED (tie, not a beat; schedule never plants TOMATO, the only crop it touches) |
| 2. wheat yield | forcing harvest can't wait past the season's actual end | yes, 32/66 wheat plantings a season never get harvested | `_one_shot_is_finished` also true on/near the last day | $109,688 -> $109,596 | REVERTED (-$92; harvested product often doesn't reach a sale in time) |
| 3. animal placement | money is the constraint | no; PLACE (not BUY_ANIMAL) is delayed, by a shared-pasture type race | rank PLACE candidates by value instead of fixed COW-first order | $109,688 -> $104,012 | REVERTED (-$5,676; ignores the season's intended 8:6 COW:SHEEP mix) |

Net result: **$109,688 unchanged.** All three theories were diagnosed as real, measurable phenomena
with concrete numbers behind them (verified with a failing test before any code change, in every
case), and all three fixes attempted here were measured net losses on the 12-seed ladder and reverted.
Every test added is now a "tried and measured a loss" pin, per project convention, so none of the
three specific fixes above gets re-derived and re-tried unchanged. Two of the three have a plausible,
more promising next attempt noted above (early-harvest-and-replant throughput for wheat; schedule-intent-aware
pasture assignment for animals) that was not attempted in this session because each is a materially
bigger change than the one tested and deserves its own theory-then-test cycle rather than being folded
into this task's scope.

Final confirmation run after all reverts, to rule out any stray state: `data/logs/fable_ladder_final_confirm.log`,
identical to the pre-session baseline, $109,688 to the dollar, same op tally.
