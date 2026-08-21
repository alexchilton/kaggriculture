# Flag audit, 2026-08-20

Scope: `kagg/search/schedule_agent.py`, `kagg/search/cover.py`, `kagg/search/router.py`.
Base commit: `486d51c` (`kawashigi-plan`), 5762 / 1723 / 1454 lines.

**151 module-level constants found, not 145.**
The count in the brief is close but low; an AST walk over module-level `Assign` / `AnnAssign` with
an upper-case `Name` target finds 92 in `schedule_agent.py`, 25 in `cover.py` and 34 in `router.py`.

Result: **14 constants deleted, 4 lines of unreachable code deleted, 11 docstrings corrected.**
The season harness is byte-identical before and after.

## Method, and where it was not enough

Read sites were counted with an **AST walk**, not grep: every `ast.Name` in `Load` context and
every `ast.Attribute` whose `attr` matches, across every `.py` file in the repo except
`reference/`. Comments and docstrings are excluded by construction, which grep cannot do — several
constants have forty-line `#:` blocks that mention their own name and every neighbour's.

**That method missed two live readers, and the miss is the most useful thing in this audit.**
`scripts/close_package_ablation.py` drives an A/B from a dict of flag NAMES AS STRINGS through
`setattr`:

```python
DELTAS = {
    "TRIM_A_TAIL_THAT_CANNOT_COME_HOME":   ("kagg.search.cover", True, False),
    ...
}
for flag, (mod, on, off) in DELTAS.items():
    setattr(mods[mod], flag, want)
```

An AST search for a `Name` or `Attribute` finds nothing. `TRIM_A_TAIL_THAT_CANNOT_COME_HOME` was
deleted and then restored. Had it shipped deleted, the ablation would have set an attribute nothing
reads and reported a byte-identical arm — indistinguishable from a measured null, which is the exact
failure `CLAUDE.md` records. The same recovery applies to `STEAL_FROM_DAY_MARGIN`, read only by
`scripts/who_claimed_the_last_work.py:38`.

**Rule for the next pass: grep the quoted string as well as the name, and check `setattr` sites.**

## 1. The 151 constants

| file | line | name | value | class | reads | note |
|---|---:|---|---|---|---:|---|
| `schedule_agent.py` | 65 | `DELIVER_CUTOFF_TURNS` | `99` | INERT | 2 | 99 is above any turn budget, so the closing trip is never charged (documented) |
| `schedule_agent.py` | 121 | `WALK_THE_LOAD_HOME_DAYS` | `(10, 29)` | LIVE | 1 | day set; `close_package_ablation.py` flips it by string |
| `schedule_agent.py` | 126 | `LAST_FREE_DROP_DAY` | `28` | **DELETED** | 0 | no reader; duplicate of the router copy |
| `schedule_agent.py` | 161 | `LATE_SEASON_TRIAGE` | `True` | ONE-BRANCH | 1 | no external reader; see "needs a decision" |
| `schedule_agent.py` | 164 | `LAST_DAY` | `29` | TUNING NUMBER | 3 | |
| `schedule_agent.py` | 227 | `FUND_THE_DAY_WHEN_SHORT` | `True` | ONE-BRANCH | 1 | no external reader; cover.py comments cite it |
| `schedule_agent.py` | 238 | `PLAN_THE_CREW_THAT_ARRIVES` | `True` | ONE-BRANCH | 2 | no external reader |
| `schedule_agent.py` | 240 | `HARVEST_WHAT_YOU_STAND_ON` | `True` | **DELETED** | 1 | hard True, 1 read site, no external reader; inlined |
| `schedule_agent.py` | 259 | `CARE_WHAT_YOU_STAND_ON` | `True` | ONE-BRANCH | 2 | a test asserts it is on |
| `schedule_agent.py` | 267 | `LAST_DAY_DEADLINE_WALK` | `True` | ONE-BRANCH | 1 | `close_package_ablation.py` flips it BY STRING |
| `schedule_agent.py` | 286 | `LAST_DAY_WALK_SLACK` | `3` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 639 | `TPD` | `R.TURNS_PER_DAY` | LIVE | 288 | |
| `schedule_agent.py` | 640 | `SHED` | `set(R.shed_access_tiles())` | LIVE | 109 | |
| `schedule_agent.py` | 641 | `SPAWN` | `tuple(R.SPAWN)` | LIVE | 38 | |
| `schedule_agent.py` | 642 | `STEP` | compass table | LIVE | 13 | |
| `schedule_agent.py` | 643 | `CROP` | `R.CROP_TABLE` | LIVE | 28 | |
| `schedule_agent.py` | 647 | `SHED_CAPACITY` | `100` | TUNING NUMBER | 10 | env default |
| `schedule_agent.py` | 671 | `FEED_DAYS` | `1` | TUNING NUMBER | 3 | docstring says 4 — see §2 |
| `schedule_agent.py` | 674 | `FEED_DAYS_LATE` | `1` | INERT | 2 | equal to `FEED_DAYS`, so `feed_days(day)` is constant |
| `schedule_agent.py` | 679 | `FEED_DAYS_FROM_DAY` | `16` | INERT | 5 | selects between two equal values |
| `schedule_agent.py` | 729 | `BUY_DRIP` | `1` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 754 | `FEED_TURN_CAP` | `6` | TUNING NUMBER | 4 | |
| `schedule_agent.py` | 770 | `DUSK_FEED_HOUR` | `18` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 774 | `DUSK_FROM_DAY` | `2` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 779 | `MIN_OPPORTUNISTIC_DROP` | `4` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 796 | `MIN_SELL_ROW_DROP` | `6` | **DELETED** | 0 | no reader; `cover.DELIVER_MIN` is the live threshold |
| `schedule_agent.py` | 804 | `DELIVER_FERRY_MARGIN` | `3` | **DELETED** | 0 | no reader |
| `schedule_agent.py` | 871 | `PEN_SPOTS` | 10 tiles | LIVE | 1 | docstring said it must stay empty — see §2 |
| `schedule_agent.py` | 922 | `PEN_NEAREST_DEPOT_FROM_DAY` | `11` | TUNING NUMBER | 3 | |
| `schedule_agent.py` | 925 | `ORDER_SLOTS` | `10` | TUNING NUMBER | 3 | env rule |
| `schedule_agent.py` | 1016 | `HIRE_PINNED_DAYS` | `frozenset(range(30))` | INERT | 2 | always true; the drip branch is unreachable |
| `schedule_agent.py` | 1018 | `CUMULATIVE_SELLS` | `True` | ONE-BRANCH | 2 | `scripts/breakdown.py` prints it |
| `schedule_agent.py` | 1023 | `LIQUIDATE_LAST_DAY` | `True` | ONE-BRANCH | 4 | a test reads it |
| `schedule_agent.py` | 1034 | `LIQUIDATE_FROM_HOUR` | `16` | TUNING NUMBER | 4 | |
| `schedule_agent.py` | 1059 | `HIRE_FIRST` | `True` | ONE-BRANCH | 5 | `scripts/breakdown.py` prints it |
| `schedule_agent.py` | 1079 | `URGENT_OPS` | `()` | INERT | 2 | empty, so the urgent-replan trigger is dead |
| `schedule_agent.py` | 1083 | `ANIMAL_OVER_HIRE` | `True` | **DELETED** | 2 | hard True, no external reader; inlined |
| `schedule_agent.py` | 1087 | `SELLS_FUND_THE_TURN` | `True` | **DELETED** | 1 | hard True, no external reader; inlined |
| `schedule_agent.py` | 1117 | `STEAL_FROM_DAY` | `6` | INERT | 0 | no reader at all; kept, see §4 |
| `schedule_agent.py` | 1118 | `STEAL_FROM_DAY_MARGIN` | `4` | INERT | 1 | one reader, a diagnostic script |
| `schedule_agent.py` | 1127 | `SELL_CARRY_DAYS` | `3` | TUNING NUMBER | 2 | |
| `schedule_agent.py` | 1130 | `LAND_PRICES` | `R.LAND_PRICES` | LIVE | 50 | |
| `schedule_agent.py` | 1136 | `RANK` | op priority dict | LIVE | 13 | |
| `schedule_agent.py` | 1462 | `DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND` | `True` | ONE-BRANCH | 2 | a test flips it |
| `schedule_agent.py` | 1514 | `OPENING_GEOMETRY` | 6 tiles | LIVE | 1 | |
| `schedule_agent.py` | 1520 | `OPENING_GEOMETRY_LAST_DAY` | `4` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 2479 | `PRICE_AWARE_SELL_CAP` | `True` | ONE-BRANCH | 2 | tests/scripts flip it |
| `schedule_agent.py` | 2480 | `RESERVATION_SELL_CAP` | `True` | ONE-BRANCH | 5 | tests/scripts flip it |
| `schedule_agent.py` | 2481 | `HOLD_A_FLOORED_BOOK` | `True` | ONE-BRANCH | 1 | no external reader |
| `schedule_agent.py` | 2482 | `RESERVATION_CONTEST` | `0.5` | TUNING NUMBER | 2 | |
| `schedule_agent.py` | 2483 | `RESERVATION_SLIP` | `0.1` | TUNING NUMBER | 3 | |
| `schedule_agent.py` | 2500 | `LATE_SELL_BIAS` | `True` | ONE-BRANCH | 3 | tests/scripts flip it |
| `schedule_agent.py` | 2501 | `LATE_SELL_FROM_HOUR` | `16` | TUNING NUMBER | 7 | |
| `schedule_agent.py` | 2505 | `NO_DRAIN_PRODUCTS` | `('MELON',)` | LIVE | 2 | |
| `schedule_agent.py` | 2506 | `SELL_AT_ONCE_FROM_DAY` | `18` | TUNING NUMBER | 2 | |
| `schedule_agent.py` | 2522 | `SELL_AT_ONCE_DAYS` | `(10, 11)` | LIVE | 1 | |
| `schedule_agent.py` | 2545 | `_CENTER_INTERVAL` | `24` | TUNING NUMBER | 2 | env rule |
| `schedule_agent.py` | 2612 | `SHOP_ADAPT_HERD` | `True` | ONE-BRANCH | 1 | a scratchpad diagnostic prints it |
| `schedule_agent.py` | 2633 | `SHOP_ADAPT_FROM_DAY` | `3` | TUNING NUMBER | 4 | |
| `schedule_agent.py` | 2650 | `HERD_FLOOR_COW` | `2` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 2651 | `HERD_FLOOR_SHEEP` | `3` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 2742 | `SHOP_ADAPT_CROPS` | `False` | INERT | 3 | hard False; the whole `_adapt_crops` path is dead in the agent |
| `schedule_agent.py` | 2746 | `CROP_SWAP_PAIRS` | 2 pairs | INERT | 1 | reachable only through `_adapt_crops` |
| `schedule_agent.py` | 2759 | `CROP_ADAPT_FROM_DAY` | `6` | INERT | 10 | same gate |
| `schedule_agent.py` | 2765 | `STRAWBERRY_SHOPS` | 4 shops | LIVE | 1 | |
| `schedule_agent.py` | 2790 | `STRAWBERRY_TILES_BY_DRAIN` | `(26, 26, 35, 36, 37)` | LIVE | 3 | |
| `schedule_agent.py` | 2802 | `STRAWBERRY_FLOAT_FROM_DAY` | `12` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 2853 | `WOOL_SHOP_SETS_THE_HERD` | `True` | ONE-BRANCH | 1 | a scratchpad diagnostic prints it |
| `schedule_agent.py` | 2857 | `WOOL_SHOP_COW_CAP` | `6` | TUNING NUMBER | 7 | |
| `schedule_agent.py` | 2861 | `WOOL_SHOP_DRAW_LIMIT` | `3` | TUNING NUMBER | 11 | |
| `schedule_agent.py` | 2884 | `WOOL_SHOP_NO_YARN_COW` | `10` | TUNING NUMBER | 3 | |
| `schedule_agent.py` | 2888 | `GOOSE_FROM_DAY` | `6` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 2891 | `MILK_DRAINING_SHOPS` | 3 shops | LIVE | 1 | |
| `schedule_agent.py` | 2895 | `MILK_SHOPS_FOR_A_BIG_HERD` | `2` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 2896 | `COW_ON_A_MILK_RICH_BOARD` | `12` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 2897 | `COW_ON_A_MILK_POOR_BOARD` | `7` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 2900 | `MILK_CLASSIFIER_FROM_DAY` | `9` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 3153 | `HERD_GEESE` | `0` | INERT | 7 | `swap_in_geese` never runs; a test pins it at 0 |
| `schedule_agent.py` | 3156 | `HERD_GEESE_FROM` | `('SHEEP', 'COW')` | INERT | 2 | reachable only through `swap_in_geese` |
| `schedule_agent.py` | 3174 | `HERD_GEESE_EARLIEST` | `(0, 6, 10, 21)` | INERT | 5 | same |
| `schedule_agent.py` | 3532 | `SELLABLE` | product order | LIVE | 8 | |
| `schedule_agent.py` | 3539 | `FERTILIZER_RESERVE_LOOKAHEAD_DAYS` | `1` | TUNING NUMBER | 1 | docstring says 3 — see §2 |
| `schedule_agent.py` | 3564 | `WHEAT_TILES_TO_CARROT` | `0` | INERT | 2 | documented as inert at 0 |
| `schedule_agent.py` | 3597 | `WHEAT_TILES_TO_TOMATO` | `1` | LIVE | 2 | docstring said "unconditional" — see §2 |
| `schedule_agent.py` | 3600 | `TOMATO_DRAINING_SHOPS` | 2 shops | LIVE | 1 | |
| `schedule_agent.py` | 3604 | `TOMATO_DRAIN_SHOPS_NEEDED` | `2` | TUNING NUMBER | 1 | |
| `schedule_agent.py` | 3627 | `CROP_TILE_SHIFTS` | `()` | INERT | 13 | no-op until a sweep sets it |
| `schedule_agent.py` | 3631 | `LATE_CROP_FROM_DAY` | `12` | TUNING NUMBER | 2 | |
| `schedule_agent.py` | 3703 | `REPLAY_OPENING_DAYS` | `()` | INERT | 2 | the tape replay is off; the harness asserts this |
| `schedule_agent.py` | 3708 | `EMBEDDED_OPENINGS` | `{}` | INERT | 2 | filled only by the submission builder |
| `schedule_agent.py` | 3718 | `REPLAY_OPENING_TAPE` | tape map | INERT | 3 | reachable only from the replay path |
| `schedule_agent.py` | 3760 | `_PASTURE` | derived | LIVE | 5 | |
| `cover.py` | 65 | `TPD` | `R.TURNS_PER_DAY` | LIVE | 288 | |
| `cover.py` | 66 | `SHED` | `tuple(R.shed_access_tiles())` | LIVE | 109 | |
| `cover.py` | 69 | `DRAWN` | 4 ops | LIVE | 3 | |
| `cover.py` | 72 | `YIELDING` | 2 ops | LIVE | 1 | this copy IS the one read |
| `cover.py` | 106 | `REQUIRED_OPS` | `('FEED',)` | LIVE | 1 | |
| `cover.py` | 111 | `REPAIR` | `True` | ONE-BRANCH | 1 | `tests/test_cover.py` flips it |
| `cover.py` | 125 | `COMPACT` | `True` | ONE-BRANCH | 1 | wraps a ~45-line block; no external reader |
| `cover.py` | 131 | `MAKE_ROOM_HANDS` | `3` | TUNING NUMBER | 1 | |
| `cover.py` | 132 | `MAKE_ROOM_MOVES` | `8` | TUNING NUMBER | 1 | |
| `cover.py` | 141 | `MEMOISE_SLOT` | `True` | ONE-BRANCH | 2 | a test flips it |
| `cover.py` | 165 | `AT_RISK_NOT_LAST_DAYS` | 5 days | LIVE | 1 | |
| `cover.py` | 166 | `AT_RISK_TAIL_PENALTY` | `2` | TUNING NUMBER | 1 | |
| `cover.py` | 170 | `_MISS` | `object()` | LIVE | 2 | sentinel |
| `cover.py` | 184 | `DELIVER_MIN` | `6` | TUNING NUMBER | 5 | |
| `cover.py` | 195 | `RUSH_BANK_MIN` | `4` | TUNING NUMBER | 1 | |
| `cover.py` | 232 | `_NEAREST` | `{}` | LIVE | 6 | memo |
| `cover.py` | 790 | `RESERVE_FROM_DAY` | `10` | TUNING NUMBER | 4 | |
| `cover.py` | 808 | `RESERVE_DAYS` | day set | LIVE | 1 | |
| `cover.py` | 813 | `RANK_HOME_DAYS` | `frozenset({4})` | **DELETED** | 0 | no reader; docstring claimed "days it applies" |
| `cover.py` | 817 | `TRIM_A_TAIL_THAT_CANNOT_COME_HOME` | `True` | ONE-BRANCH | 1 | ablation flips it BY STRING — nearly deleted |
| `cover.py` | 826 | `TRIM_HOME_DAYS` | `frozenset({29})` | LIVE | 1 | ablation flips it by string |
| `cover.py` | 907 | `UNSOLVE_DAYS` | `tuple(range(0, 30))` | INERT | 4 | empties `PRECOMPUTED_ROUTES` |
| `cover.py` | 909 | `PRECOMPUTED_ROUTES` | `{}` at import | INERT | 14 | live tooling, dead in the shipped agent |
| `cover.py` | 924 | `MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE` | `True` | INERT | 1 | cannot fire while routes are `{}` |
| `cover.py` | 928 | `PRECOMPUTED_MISSES` | `[]` | INERT | 10 | appended only from the precomputed path |
| `router.py` | 67 | `TPD` | `R.TURNS_PER_DAY` | LIVE | 288 | |
| `router.py` | 68 | `WORK_TURNS` | `TPD - 1` | **DELETED** | 0 | no reader; `dayplan.py` defines its own |
| `router.py` | 69 | `SHED` | `tuple(R.shed_access_tiles())` | LIVE | 109 | |
| `router.py` | 70 | `SHED_SET` | `frozenset(SHED)` | LIVE | 1 | |
| `router.py` | 71 | `CROP` | `R.CROP_TABLE` | LIVE | 28 | |
| `router.py` | 72 | `ANIMALS` | `R.ANIMALS` | LIVE | 134 | |
| `router.py` | 77 | `BASE_PRICE` | price table | LIVE | 53 | |
| `router.py` | 96 | `MANDATORY` | `100000` | TUNING NUMBER | 9 | prize tier |
| `router.py` | 112 | `CRITICAL` | `1000000` | TUNING NUMBER | 18 | prize tier |
| `router.py` | 115 | `LAST_FREE_DROP_DAY` | `R.SEASON_DAYS - 2` | **DELETED** | 0 | no reader |
| `router.py` | 121 | `HARVEST_CRITICAL_FROM_DAY` | `9` | TUNING NUMBER | 1 | |
| `router.py` | 126 | `SEED_COST` | seed price table | LIVE | 38 | read as `RT.SEED_COST` |
| `router.py` | 135 | `PLACE_DRAWS_FEED` | `True` | **DELETED** | 1 | hard True, no external reader; inlined |
| `router.py` | 206 | `PLACE_IS_MANDATORY_FROM_DAY` | `14` | TUNING NUMBER | 4 | |
| `router.py` | 208 | `CHAIN_OPS` | `()` | **DELETED** | 0 | no reader |
| `router.py` | 211 | `SERVICE_ROUND` | `10` | TUNING NUMBER | 4 | |
| `router.py` | 215 | `DRAWN` | 4 ops | LIVE | 3 | |
| `router.py` | 219 | `YIELDING` | 2 ops | **DELETED** | 0 | no reader; `cover.py` has the live copy |
| `router.py` | 241 | `HOMEWARD_DROP_TURNS` | `0` | INERT | 0 | no reader; kept as a paired record — see §4 |
| `router.py` | 263 | `DEPOT_NODE_EXTRA_SERVICE` | `0` | INERT | 1 | read, but 0 adds nothing |
| `router.py` | 274 | `_QUAD_ORDER` | derived | LIVE | 1 | |
| `router.py` | 348 | `DEPOT_RING_FIRST` | `1` | INERT | 5 | `len(unlocked) >= 1` is always true |
| `router.py` | 433 | `TOP_UP_DISCOUNT` | `8.0` | TUNING NUMBER | 2 | |
| `router.py` | 675 | `LATE_SEASON_PAIR` | `True` | **DELETED** | 3 | hard True master switch; 26/26/True inlined |
| `router.py` | 677 | `FERTILIZE_UNTIL_DAY` | `26` | TUNING NUMBER | 3 | now a plain 26 |
| `router.py` | 681 | `HARVEST_A_TRUNCATED_ONE_SHOT` | `LATE_SEASON_PAIR` | **DELETED** | 1 | alias; `True` inlined |
| `router.py` | 686 | `LATE_TRUNCATED_PLANT_DAY` | `26` | TUNING NUMBER | 3 | now a plain 26 |
| `router.py` | 820 | `ARRIVAL_FEED_REMAINING` | `0` | LIVE | 1 | genuinely written every turn by the agent |
| `router.py` | 825 | `ARRIVAL_FEED_EARLIEST_YIELD` | `None` | LIVE | 2 | genuinely written every turn |
| `router.py` | 835 | `FEED_CADENCE_FROM_DAY` | `7` | INERT | 5 | no reader in any module; only tests read it |
| `router.py` | 935 | `NO_UPKEEP_ON_THE_LAST_DAY` | `True` | ONE-BRANCH | 2 | test + ablation flip it |
| `router.py` | 1075 | `_DEPOT_TILES` | derived | LIVE | 1 | |
| `router.py` | 1141 | `PLANT_THEN_WATER` | `True` | ONE-BRANCH | 3 | a test asserts it is on |
| `router.py` | 1155 | `REPLANT_A_CLEARED_TILE` | `True` | ONE-BRANCH | 2 | `schedule_agent.py:1912` reads it |

Totals: **TUNING NUMBER 48, LIVE 40, INERT 27, ONE-BRANCH 22, DELETED 14.**

Read again: **27 of 151 constants are INERT and 22 more have a branch that never executes.** A third
of the module-level surface of these three files does not discriminate anything at runtime.

## 2. Docstrings that contradict their code

Eleven. All eleven had their prose corrected; **no code was changed to match prose.**

**1. `router.py:838` `will_be_fed` — an unconditional `return True` in front of the rule.**
The known one, and it is worse than a stale comment: the code below it was unreachable.

```
896        return (ARRIVAL_FEED_REMAINING > 0 ...)
900    return True
901    if cell.get("consecutive_unfed", 0) >= 1:
902        return True
903    a = ANIMALS[cell["animal"]]
904    return ((day + 1) - int(cell.get("placed_day", 0)) - a["first_yield_day"]) >= 0
```

Lines 901-904 deleted. The function's own docstring now states the two rules it actually has.

**2. `router.py:827-835` `FEED_CADENCE_FROM_DAY = 7`** — "First day the cadence applies."
There is no cadence. The rule it gated is the block above, which was unreachable. **No module reads
this constant.** Two test files do, and one of them —
`tests/test_we_feed_on_alternate_days_like_the_tape.py::test_a_pen_that_has_not_started_producing_is_not_fed_unless_it_is_hungry`
— **FAILS on this branch at the base commit**, before any of my changes, for exactly this reason.
That is a test recording a rule the shipped code does not implement.

**3. `schedule_agent.py:244` `CARE_WHAT_YOU_STAND_ON`** — the block opens
"**OFF, and measured.**" and the value is `True`. `tests/test_the_first_seven_days_match_the_plan.py:910`
asserts it is ON. The measurement table below it (which argues for OFF) is kept; the verdict word
is corrected.

**4. `schedule_agent.py:831-833` `PEN_SPOTS`** — "Empty is the shipping behaviour and **must stay
empty on main**". It ships as ten tiles. A later paragraph in the same block ("That verdict
expired") overrode it and the opening sentence was never updated.

**5. `schedule_agent.py:3536` `FERTILIZER_RESERVE_LOOKAHEAD_DAYS`** — "**Three**, because
`FERTILIZE` sets `fertilized_until_day = day + 2` ... covers a three-day window". The value is `1`.

**6. `schedule_agent.py:~653` `FEED_DAYS`** — headline "**RAISED 2 -> 4 on 2026-08-08**". The value
is `1`, and a note 16 lines *below* the constant is the one that reverted it: "the board-read
target at `FEED_DAYS = 1` is the measured best". Two contradictory verdicts in one block, with the
live one placed after the assignment where it reads as unrelated.

**7. `schedule_agent.py:984-986`** — `CUMULATIVE_SELLS`'s docstring ("Whether `sells` is read as a
CUMULATIVE target...") was stranded at the TOP of `HIRE_PINNED_DAYS`'s own 20-line block, and
`CUMULATIVE_SELLS = True` two lines later had no docstring at all. Moved.

**8. `router.py:128-134` `PLACE_DRAWS_FEED`** — carried THREE stacked `#:` paragraphs. The first
described a turns threshold that no longer exists ("Below this many turns left, a placement banks no
product today"); the second described `CHAIN_OPS`, defined 73 lines later with its own comment; only
the third was its own. Deleted with the flag.

**9. `router.py:670-675` `LATE_SEASON_PAIR = True`** — the `#:` block above the boolean is entirely
about the NUMBER below it, ending "which is why **this sits at 26**". Fixed by deleting the boolean,
which leaves the prose sitting correctly on `FERTILIZE_UNTIL_DAY = 26`.

**10. `cover.py:811-813` `RANK_HOME_DAYS`** — "Days it **applies**." Nothing reads it. Deleted.

**11. `schedule_agent.py:3565` `WHEAT_TILES_TO_TOMATO`** — headline "ONE tile, **unconditional**",
and a second "**Unconditional**, because the shop condition was tried and refuted". A 2026-08-19
paragraph at the FOOT of the same block already retracts both — "The word 'unconditional' was also
never true of the code. Two conditions already applied at the use site" — but a reader who stops at
the headline gets the wrong answer, which is how a test came to assert on a name the branch does not
read. Headline now points at the retraction.

Also noted, not a contradiction but the same hazard: **`cover.py:924`
`MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE`** describes behaviour that cannot occur on this branch —
`UNSOLVE_DAYS = range(0, 30)` makes `PRECOMPUTED_ROUTES == {}`, so `_apply_precomputed` seats
nothing on any day. A note saying so was added.

## 3. What was deleted, and the evidence

**14 constants and 4 lines of unreachable code.** Every deletion is either zero-reader (proved by an
AST walk over the repo, plus a literal-string grep, plus a `setattr` audit) or a hard-`True` flag
with no reader outside its own module.

| deleted | file:line | evidence |
|---|---|---|
| `LAST_FREE_DROP_DAY` (both copies) | `router.py:115`, `schedule_agent.py:126` | 0 AST loads. `tests/test_the_second_to_last_day_banks_the_field.py:37` computes its own from `R.SEASON_DAYS - 2` and imports neither |
| `WORK_TURNS` | `router.py:68` | 0 AST loads. `dayplan.py:46` has its own |
| `CHAIN_OPS` | `router.py:208` | 0 AST loads, 0 string hits. Its lesson is already recorded in `cover.py:1678` |
| `YIELDING` | `router.py:219` | 0 AST loads. `cover.py:72` defines the copy that `cover.py:307` reads |
| `MIN_SELL_ROW_DROP` | `schedule_agent.py:796` | 0 AST loads; only prose mentions |
| `DELIVER_FERRY_MARGIN` | `schedule_agent.py:804` | 0 AST loads; the one prose reference at `_route_turns` was rewritten |
| `RANK_HOME_DAYS` | `cover.py:813` | 0 AST loads, 0 string hits |
| `PLACE_DRAWS_FEED` | `router.py:135` | `True`, one read site (`router.py:1127`), no store anywhere, no string hit. Inlined |
| `LATE_SEASON_PAIR` | `router.py:675` | `True`, read only by the three lines under it. `26 if X else 99` → `26`; inlined |
| `HARVEST_A_TRUNCATED_ONE_SHOT` | `router.py:681` | pure alias of the above; `True` inlined at `router.py:772` |
| `HARVEST_WHAT_YOU_STAND_ON` | `schedule_agent.py:240` | `True`, one read site, no docstring at all, no store, no string hit |
| `ANIMAL_OVER_HIRE` | `schedule_agent.py:1083` | `True`, two read sites in one `if`, no store, no string hit |
| `SELLS_FUND_THE_TURN` | `schedule_agent.py:1087` | `True`, one read site, no store, no string hit |
| `will_be_fed` lines 901-904 | `router.py` | proved unreachable by an AST pass for statements after an unconditional `Return` in the same block; it was the only such site in all three files |

Line counts: 5762 → 5742, 1723 → 1730 (cover gains from added correction prose), 1454 → 1443.

**Two deletions were made and then REVERTED during this audit** — see §4.

## 4. Needs a decision

Nothing below was deleted. Each is dead or one-branch, and each has a reason not to touch it
without Alex.

**a. `TRIM_A_TAIL_THAT_CANNOT_COME_HOME` (`cover.py`) and `LAST_DAY_DEADLINE_WALK`,
`WALK_THE_LOAD_HOME_DAYS`, `NO_UPKEEP_ON_THE_LAST_DAY`, `MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE`,
`TRIM_HOME_DAYS`.** All six are the arms of `scripts/close_package_ablation.py`, which flips them by
STRING through `setattr`. The first was deleted and restored. **None of these may be deleted while
that script exists**, and any future audit has to grep the quoted name.

**b. `STEAL_FROM_DAY = 6` / `STEAL_FROM_DAY_MARGIN = 4`.** Deleted and restored.
`STEAL_FROM_DAY` genuinely has zero readers; `STEAL_FROM_DAY_MARGIN` has exactly one, at
`scripts/who_claimed_the_last_work.py:38`, which is a diagnostic and not on any play path. So the
stealing rule they gate is not running. Deleting them means deleting or rewriting that script — a
decision, not a cleanup. Their docstring now says so, and preserves the measurement (d7 15 cells → 8,
the largest single-day gain recorded here).

**c. `FEED_CADENCE_FROM_DAY = 7` (`router.py`) — and the failing test that goes with it.**
No module reads it. Two test files do, and
`test_a_pen_that_has_not_started_producing_is_not_fed_unless_it_is_hungry` **fails at the base
commit**. Three ways out and they are not equivalent: delete the constant and the test (a test
change), re-enable the cadence (a behaviour change that must be measured on the grid), or leave it
red as a recorded defect. I left it red and documented it.

**d. Nine hard-`True` flags with no external reader that were NOT deleted.**
`LATE_SEASON_TRIAGE`, `FUND_THE_DAY_WHEN_SHORT`, `PLAN_THE_CREW_THAT_ARRIVES`,
`HOLD_A_FLOORED_BOOK`, `COMPACT` (cover). Each is provably one-branch. Reasons for holding off:
`COMPACT` wraps a ~45-line block whose removal is a dedent, which is where a silent error would
come from; the other four carry long measurement blocks that other files' comments cite by name, so
deleting them scatters dangling references. All are safe to inline, individually, with the harness
as the gate.

**e. Flags a TEST asserts or flips:** `CARE_WHAT_YOU_STAND_ON`, `REPAIR`, `MEMOISE_SLOT`,
`PLANT_THEN_WATER`, `LIQUIDATE_LAST_DAY`, `DIG_A_WEED_...`, `PRICE_AWARE_SELL_CAP`,
`RESERVATION_SELL_CAP`, `LATE_SELL_BIAS`, `SHOP_ADAPT_CROPS`. Deleting any of these is a test
change, which was out of scope by instruction.

**f. `HOMEWARD_DROP_TURNS = 0` (`router.py:241`) — zero readers, deliberately kept.**
It qualifies as UNREAD and I did not delete it, because the block below it
(`DEPOT_NODE_EXTRA_SERVICE`) explicitly records the joint decision: "the two constants stay at 0 as
documentation of a measured dead end". Deleting it would delete half of a recorded measurement pair
that someone chose to keep. Alex's call.

**g. The whole precomputed-route mechanism is off in the shipped agent.**
`UNSOLVE_DAYS = tuple(range(0, 30))` ⇒ `PRECOMPUTED_ROUTES == {}` ⇒ `_apply_precomputed`,
`PRECOMPUTED_MISSES` and `MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE` cannot fire. This is intended on
this branch (the docstring says "the greedy lawnmower plays the whole season") and three scripts
rebuild the table, so it is live tooling. Worth knowing that the d29 landmine those constants
describe cannot currently occur.

**h. `HIRE_PINNED_DAYS = frozenset(range(30))` is always true**, so the hire *drip* branch at
`schedule_agent.py:~4934` is unreachable. Its own docstring records that pinning all thirty days
measured identically to pinning 0-3. Narrowing or removing it is a behaviour question.

**i. `FEED_DAYS == FEED_DAYS_LATE == 1`**, so `feed_days(day)` is a constant function and
`FEED_DAYS_FROM_DAY = 16` selects between two equal values. Three tuning numbers, one live value.
Left alone under "do not touch numbers", but the hinge they encode is not doing anything.

## 5. Proof of no behaviour change

Harness: `KAGG_CODE=<worktree> python -u .../tets_grid3.py`, seed 959074148, tetsuya's own tape,
his seat, his recorded opponent.

Before (`data/logs/baseline_grid.log`) and after (`data/logs/final_grid.log`) are **byte-identical**;
`diff` returns empty. The required figures:

```
season  PLANT 212/212  BUILD 15/15  PLACE 30/15  FEED 309/353  CARE 310/353  BUY_ANIMAL 10/15
        HARVEST 393  WATER 1031  PASS 1373
        herd at close {'SHEEP': 5, 'COW': 6, 'GOOSE': 3}   (his was COW 8 SHEEP 2 GOOSE 3)

 crop        ours   row
 CARROT         8     8
 MELON          8     8
 STRAWBERRY    32    32
 WHEAT        164   164

 placed by species  {'COW': 7, 'SHEEP': 5, 'FERTILIZER': 15, 'GOOSE': 3}
```

Matches the required baseline: `PLANT 212/212 BUILD 15/15`, `WHEAT 164 STRAWBERRY 32 MELON 8
CARROT 8`, herd `COW 6 SHEEP 5 GOOSE 3`.

Tests. `tests/test_the_herd_split_answers_tetsuyas_shop_draws.py` is 4 skipped in this worktree
(its data files are not committed), so it is not a gate here. The real comparison is a wider suite
run twice — once with `git checkout --` on the three files, once with the edits restored:

```
baseline  (data/logs/audit_tests_wide_BASELINE.log)   28 failed, 107 passed, 4 skipped
after     (data/logs/audit_tests_wide.log)            28 failed, 107 passed, 4 skipped
```

`diff` of the sorted `FAILED` lines is **empty** — the same 28 tests, pre-existing at the base
commit (18 of them `FileNotFoundError` on uncommitted `data/seed_scripts/` fixtures). The final run
adds `test_the_herd_split...` and `test_we_feed_on_alternate_days...`, giving
`29 failed, 116 passed, 8 skipped`; the extra failure is the pre-existing `will_be_fed` one
described in §2.

Logs, all under `data/logs/` in this worktree:
`baseline_grid.log`, `after_grid.log`, `after_grid2.log`, `final_grid.log`,
`audit_tests_before.log`, `audit_tests_wide_BASELINE.log`, `audit_tests_wide.log`,
`audit_tests_final.log`.
