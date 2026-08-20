# CARROT_SWAP — plant carrot instead of wheat when the shop draw favours it

## The prior art this task did not know about

Before writing any code, `docs/REGISTER.md` C-23 and its docstring in
`kagg/search/schedule_agent_1455mh.py` (`SHOP_ADAPT_CROPS`) were read, because CLAUDE.md's own
rule says to check whether a doc already answers the question. It very nearly does.

`SHOP_ADAPT_CROPS`'s `("WHEAT", "CARROT")` cadence pair is a board-conditional wheat<->carrot
substitution, already built, already gated behind a module constant, already OFF, with its own
test (`tests/test_the_field_follows_the_shop_draw.py::test_the_crop_swap_is_disabled_and_stays_disabled`)
asserting it stays off. It was measured — together with `("TOMATO", "STRAWBERRY")` — at **0.806
against HEAD's 0.871 over 232 matched games**, and independently on the 2,744-seat ladder sample:
carrot growers bank **below the field median** ($79,847 vs $82,136). The docstring says plainly:
"Do not switch it back on with these pairs."

That is strong prior evidence against carrot as a crop, full stop. It is not, however, a complete
answer to what this task asked for, for two reasons:

1. **The 232-game measurement was never isolated to `WHEAT<->CARROT` alone** — it always ran
   together with `TOMATO<->STRAWBERRY`, so the carrot-specific contribution to that loss is not
   separated out.
2. **The mechanism is different.** `_adapt_crops` scores in dollars through a season-long
   headroom model (`town_drain_remaining` + `expected_future_drain`, priced per tile per cycle).
   This task specifically asked for the plainer instrument — a raw shop-instance count — which
   has never been tried on its own.

So this is a narrower, previously-untested question sitting inside a much better-supported "no."
Both numbers are reported below, honestly, against each other.

## What was built

`CARROT_SWAP` (module constant, default `False`, `kagg/search/schedule_agent_1455mh.py`), plus
`CARROT_SWAP_FROM_DAY = 6` and two functions:

- `_carrot_shop_weights(unlocked_shops)` — sums unlocked shop INSTANCES from `kaggriculture.SHOPS`
  that buy CARROT and that buy WHEAT, weighting a single-product shop (`PET_CAFE`) double — the
  same convention `town_drain_remaining` already uses, because a shop that buys only one thing
  drains it twice as fast as a shop with three. Duplicates count: two `PET_CAFE` draws score 4,
  not 2.
- `_carrot_swap(want, planted, live, day, unlocked_shops)` — from day 6, if carrot's weighted
  count **strictly exceeds** wheat's, moves the schedule's still-**unplanted** WHEAT to CARROT,
  tile for tile. Ground already committed (`planted + live`) is never re-labelled — the same
  anchor rule `_adapt_crops` uses one field over, for the same reason (a target recomputed from
  scratch every turn against a monotonically-growing `planted` counter can overshoot both crops at
  once if the anchor is dropped).

Growth profiles checked against `reference/kaggriculture.py` / `router.CROP_TABLE` before assuming
any substitution, per CLAUDE.md's warning that the published Object Types table is misleading:

```
WHEAT    first_yield_day 2   max_yield_day 4   max_yield 6   seed $10   base $25
CARROT   first_yield_day 2   max_yield_day 3   max_yield 4   seed $20   base $35
```

Both one-shots, cadence-compatible (the swap doesn't disturb the tour shape), but **not** value-
equal: WHEAT nets $140/tile ($150 gross − $10 seed), CARROT nets $120/tile ($140 gross − $20
seed) before any market saturation. The swap has to be earned by the shop draw, not free.

Hook point: `_refresh_pins`, immediately after the (disabled) `SHOP_ADAPT_CROPS` call, so with the
flag off the two mechanisms are simply both skipped.

## Testing discipline

`tests/test_carrot_swap_follows_shop_instance_count.py`, 8 tests, one theory each:

1. `test_carrot_swap_ships_off_by_default` — the gate.
2. `test_carrot_shop_weights_counts_instances_and_doubles_single_product_shops` — the counting
   primitive: 2×PET_CAFE + FARMERS_MARKET = carrot weight 5, not 3; PET_CAFE doubles.
3. `test_carrot_swap_moves_unplanted_wheat_when_carrot_shops_outweigh_wheat_shops` — the core
   mechanism, both directions.
4. `test_carrot_swap_requires_carrot_to_strictly_outweigh_wheat` — a tie does not swap.
5. `test_carrot_swap_never_relabels_ground_already_planted` — the anchor rule.
6. `test_carrot_swap_keeps_the_pair_total_tile_count_unchanged` — end-to-end through
   `_refresh_pins`, count conserved on four different boards.
7. `test_carrot_swap_before_its_start_day_keeps_the_schedules_own_crop` — the day gate.
8. `test_carrot_swap_off_does_not_touch_refresh_pins_at_all` — flag off, a carrot-heavy board and
   a wheat-heavy board plant identically.

All 8 written first, run, confirmed **RED** (`_carrot_swap`/`_carrot_shop_weights`/`CARROT_SWAP`
did not exist yet — 8 `AttributeError`s, log `data/logs/carrot_swap_test_pre_2026-08-12.log`).
Implemented; all 8 **GREEN** (`data/logs/carrot_swap_test_post_2026-08-12.log`, after fixing one
test-data bug of my own — a board list had 8 entries where the comment said 5).

**Revert-and-confirm-red**, per CLAUDE.md: `git stash`d the implementation with the tests still in
place. All 8 went red again (`AttributeError`, same as the pre-implementation run). Un-stashed;
all 8 green again. The suite genuinely exercises the change.

`tests/test_each_day_matches_the_tape.py`: 1 passed (d0), 6 failed (d1-d6) — **identical pattern
to what the task specified as already-red on `main` for unrelated reasons** (the 1.32.2→1.32.6
version skew). `CARROT_SWAP` defaults `False` and is not on this code path in any way that
changes it; this run establishes that the flag did not make the pre-existing failures worse, not
that it fixed them.

## Local measurement: `breakdown.py`, seed 11, victor tape, d0-d19

**Flag OFF vs flag ON on seed 11 are byte-identical** — not just close, `diff` returns nothing
(`data/logs/carrot_swap_baseline_grid_2026-08-12.log` vs `carrot_swap_on_grid_2026-08-12.log`).

This is not merely the required "OFF restores current behaviour exactly" check — it is also
uninformative about the flag's effect, and it is important to say why before trusting it either
way: **debugged directly** (`_carrot_shop_weights` printed at every shop-unlock step for seed 11),
carrot's weighted count never exceeds wheat's across the whole 20-day window on this seed:

```
day  3: shops=(FARMERS_MARKET,)                                                   carrot=1 wheat=1
day  6: + BRUNCH_SPOT                                                             carrot=1 wheat=2
day  9: + ICE_CREAM_SHOP                                                          carrot=1 wheat=3
day 12: + YARN_STORE                                                              carrot=1 wheat=3
day 15: + YARN_STORE                                                              carrot=1 wheat=3
day 18: + SMOOTHIE_SHOP                                                           carrot=1 wheat=3
```

Seed 11's draw is wheat-favourable throughout, so the local grid check proves the gate is inert,
not that the rule does nothing useful. This is exactly the "a gate only tests what it exercises"
trap CLAUDE.md names — a single-seed check cannot discriminate a board-conditional rule from a
board that never triggers it.

## Does the flag even fire on the seeds the box sweep was told to use?

Checked before spending box time (`_carrot_shop_weights` at every shop-unlock step, seeds
1300-1323, `CARROT_SWAP_FROM_DAY=6` gate applied):

```
seed  fires by day     seed  fires by day     seed  fires by day
1300  18                1308  never            1316  never
1301  never              1309  6                1317  never
1302  never              1310  9                1318  never
1303  never              1311  6                1319  6
1304  never              1312  24               1320  never
1305  never              1313  never            1321  6
1306  9                  1314  21               1322  never
1307  24                 1315  6                1323  6
```

**In the task's literal spec — seeds 1300-1303 — the flag fires in exactly 1 of 4 seeds, and only
from day 18**, four-fifths of the way through the season, leaving almost no time for the swap to
matter. Seeds 1301-1303 never see carrot lead at all. A sweep run only on 1300-1303 would report a
number close to the flag-off baseline regardless of whether carrot substitution is good or bad,
because the mechanism barely engages — the same "instrument can't discriminate" trap the melon
work hit with the arena pool.

So two sweeps were run on the box, both against the same 24-opponent field, same harness
(`scripts/field_sweep.py`), same `--seeds 4 --opponents 24`, only `--first-seed` differs:

- **1300-1303** — the task's literal spec, comparable to the existing `CARROT_LATE` (65.1%/64.1%)
  and `HERD_CAP_COW` numbers in `data/logs/exp_cow_carrot_2026-08-12.log`.
- **1306-1309** — chosen from the table above because 3 of its 4 seeds actually fire (1306 d9,
  1307 d24, 1309 d6), against 1308 which never does — a sweep with the mechanism actually engaged
  most of the time, to separate "carrot doesn't help" from "the board never asked the question."

## Box sweep results

<!-- FILLED IN BELOW ONCE THE SWEEP COMPLETES -->

## Verdict

<!-- FILLED IN BELOW ONCE THE SWEEP COMPLETES -->
