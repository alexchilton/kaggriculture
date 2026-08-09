# Shop-aware market dynamics: design, what shipped, and what did not

**2026-08-09.** Scope: the SELL side and `BUY_PRODUCT` only, in `kagg/search/schedule_agent.py`.
Does not touch production, animal buying, planting, or `kagg/search/cover.py` — those are being
implemented separately (`SHOP_ADAPT_HERD`, `SHOP_ADAPT_FROM_DAY`, `HERD_FLOOR_COW`,
`HERD_FLOOR_SHEEP`, `expected_future_drain()`), and this doc does not describe or depend on that
work.

Read first: `docs/the_book_is_shallow_2026-08-09.md`.

## Summary verdict

Two candidate flags were built and measured. **Neither cleared significance and neither is
recommended to ship on.** One structural question (`BUY_PRODUCT`) was resolved by reading the
environment source rather than by measurement, and the answer is that there is no shop-aware
surface there to build on. This is a negative-results report more than a positive one, and that is
reported as the finding it is, not softened.

## 1. What was measured, with seed count and t-statistic

All numbers below are from `scripts/mirror_gate.py` (copied into this worktree from the main
checkout — it did not exist here; see "Tooling" below), which plays the candidate against the
shipped baseline in a mirror match, both seatings, and scores the **paired margin per seed**
(candidate minus baseline, both seatings summed), because a single win/loss threshold needs ~400
games to see a 5pp shift against this project's $17k-$163k seed variance, while pairing on the
seed removes that variance. `--selftest` was run first and returned 50.0% (W11 D2 L11 on a 4-seed
sample), confirming the harness is not biased before trusting any candidate number.

### 1a. `SHOP_THIN_DEPTH_RULE` — the flag this doc's design work produced

16 seeds (4001-4016), both seatings, **32 paired mirror seasons**:

    candidate  W17 D0 L15   win rate 53.1%
    candidate mean bank $67,308   baseline mean bank $68,304
    paired margin per seed: mean $-1,992   SE $7,500   t = -0.27
    -> NOT SIGNIFICANT -- inside noise, do not act on it
    seeds better for candidate: 8/16

**Split by whether WOOL was starved on that board** (YARN_STORE drawn or not — the split the brief
asked for specifically, since a starved board's wool absorption is fixed at 30 regardless of any
sell rule and mixing those seeds into one average hides both effects):

    WOOL-starved (YARN_STORE never drawn), n=9 of the 16 seeds:
      seeds: 4003, 4005, 4007, 4008, 4009, 4010, 4011, 4012, 4014
      per-seed margins: [23194, 489, -4723, -33134, 5996, -50078, -52511, 74984, 5887]
      mean $-3,322   SE $13,185   t = -0.25

    WOOL-healthy (YARN_STORE drawn), n=7 of the 16 seeds:
      seeds: 4001, 4002, 4004, 4006, 4013, 4015, 4016
      per-seed margins: [-21913, 8519, -747, 2323, 18434, -2023, -6577]
      mean $-283   SE $4,744   t = -0.06

Both subsets are individually **not significant** (|t| < 1 in both), both are negative in mean
sign, and the starved subset's per-seed spread is enormous ($75k top to bottom on n=9) — consistent
with this project's documented ~15% seed variance rather than with a real effect in either
direction. **The starved/healthy split does not rescue the flag.** It was the specific hypothesis
this design was built around (see §3) and the data does not support it at this sample size.

### 1b. `HOLD_A_FLOORED_BOOK=False` — re-run at full power, not something I designed

The brief flagged this as an open item from an underpowered n=24 run (SE only $0.8k-scale,
"treat as a hypothesis not a result"). Re-run here at 16 seeds / 32 paired seasons, same seed range
as above:

    candidate  W20 D0 L12   win rate 62.5%
    candidate mean bank $68,117   baseline mean bank $66,029
    paired margin per seed: mean $+4,175   SE $3,239   t = +1.29
    -> NOT SIGNIFICANT -- inside noise, do not act on it
    seeds better for candidate: 10/16

The direction is positive (mean money up, win rate up) and the SE is tighter than the earlier
underpowered run, but `t = +1.29` is still under this project's own bar of `|t| >= 2.0`. **This
does not confirm the hypothesis from the brief and does not refute it either** — it moves the
question from "underpowered" to "measured, inconclusive." Realised per-unit prices moved in mixed
directions relative to the same-seed-range `SHOP_THIN_DEPTH_RULE` baseline run (§1a's candidate
run, which itself has the shipped `HOLD_A_FLOORED_BOOK=True`): MILK $116.87 -> $123.06 (up, same
direction as the brief's own report), WOOL $133.86 -> $128.10 (down, opposite direction to the
brief's $107.81 -> $123.53), MELON $193.32 -> $194.78 (flat), STRAWBERRY $114.89 -> $103.77 (down).
The milk direction replicates; the wool direction does not. **Recommendation: leave
`HOLD_A_FLOORED_BOOK` at its shipped default (`True`).** No code change was made here — this is a
re-measurement of an existing flag, not a new one, and it is reported because the brief asked for
it and because "not significant" is itself the deliverable, not a reason to omit the section.

### 1c. Harness validation

    scripts/mirror_gate.py --selftest --seeds 4   (8 seasons)
    -> 50.0% (W3 D2 L3), paired margin mean $0 exactly, SE $0
    -> OK: an unchanged mirror is a coin flip, as the harness's own contract requires

## 2. `tests/test_shop_thin_depth_rule.py` — what it asserts, and its current state

**State as this doc is written: GREEN.** `PYTHONPATH=. python3 -m pytest
tests/test_shop_thin_depth_rule.py -q` (default addopts, `-m 'not slow'`) passes 7/7 in ~3s. The
two `@pytest.mark.slow` composition tests also pass (`-m slow`, ~21s) — run separately because they
drive a real 720-step `kaggle_environments` mirror match rather than a pure-function call.

What it would take to make it RED again: **revert the two new functions and the new flag from
`kagg/search/schedule_agent.py`** (`shop_thin`, `below_base_sell_units`, `SHOP_THIN_DEPTH_RULE`,
and the call-site change in the below-base sell branch). This was actually done and confirmed
during development, not asserted from memory:

    git stash push -- kagg/search/schedule_agent.py
    PYTHONPATH=. python3 -m pytest tests/test_shop_thin_depth_rule.py -q -m "not slow"
    -> 7 failed (AttributeError: module 'kagg.search.schedule_agent' has no attribute
       'SHOP_THIN_DEPTH_RULE')
    git stash pop
    -> 7 passed again

Per-claim breakdown:

1. **`shop_thin(prod, unlocked_shops)` classification** (4 tests) — pure function, no env
   simulation. Pins: MELON is thin on every board (no shop ever carries it); WOOL is thin until
   `YARN_STORE` unlocks and not thin the instant it does; MILK needs any ONE of its three shops;
   FERTILIZER is always thin (cross-checked against the existing
   `test_fertilizer_has_no_town_drain_at_all` from a different angle).
2. **`below_base_sell_units(...)` sizing** (3 tests) — pure function. Pins: flag off reproduces the
   exact pre-flag arithmetic (`min(have, allow, rate_cap)`, day-trimmed); flag on but the product's
   shop IS open leaves the old sizing untouched (this is the whole content of the gate — the test
   that would fail if the gate were silently dropped and the flag reproduced the blanket version
   that lost 32-season, `t=+2.90`, per the brief); flag on AND shop-thin produces a DIFFERENT number
   from the day-total cap (a direct test against the exact failure mode `RESERVATION_SELL_CAP`'s
   own history warns about — a wiring that looks live and is a no-op).
3. **Composition, `@pytest.mark.slow`** (2 tests) — drives `make_agent` + a real
   `kaggle_environments` mirror match (both seats active, contested book) rather than a single
   agent against an empty `{}` opponent. This distinction mattered and is recorded in the test's
   own docstring: **a lone agent against an empty opponent never contests its own book**, so `have`
   never exceeds the old cap and the flag is a provable no-op measured against the wrong fixture —
   confirmed directly during development (301 below-base MELON calls over a full season, single
   agent, seed 11: zero of them differing with the flag on vs off). Mirrored, seed 11 alone produces
   13 differing turns in the same window. The two tests: OFF is byte-identical across two runs
   (determinism rail every flag in this file carries); ON changes at least one action in the
   candidate seat's own stream over a full season, seed 11.

## 3. What changed in `kagg/search/schedule_agent.py`, flag by flag

Two new pure functions and one new flag, inserted after `reservation_units` (~line 1412) and wired
into the existing below-base sell branch (previously `else: n = min(have, allow, rate[prod]); n =
min(n, allow - state["ordered"][("sold", prod)])`, now calls `below_base_sell_units(...)` with the
same inputs plus `unlocked_shops`).

- **`shop_thin(prod, unlocked_shops)`** — pure function, no flag, always live. Returns whether the
  town currently has NO unlocked shop that sells `prod`. Reads `_KG.SHOPS`, the fixed product table,
  against the live `town.unlocked_shops` list. **Not itself a behavioural change** — it does
  nothing unless `SHOP_THIN_DEPTH_RULE` reads it. Tested, GREEN, not separately measured on an
  arena because it changes nothing on its own.

- **`below_base_sell_units(...)`** — pure function replacing two inline lines at the below-base sell
  call site. With the new flag OFF (the shipped default) it is a byte-identical refactor of the
  prior inline code — this is pinned by `test_below_base_sizing_is_unchanged_with_the_flag_off` and
  by the mirror-composition byte-identical test. **Not itself measured as a behaviour change**,
  because with the flag off there is no behaviour change to measure — it is a pure refactor for
  testability, the same reason `reservation_units` and `town_drain_remaining` were factored out
  before it.

- **`SHOP_THIN_DEPTH_RULE = False`** — the actual behavioural lever. **Implemented, unit- and
  composition-tested (GREEN), measured (§1a: 32 mirror seasons, t=-0.27, not significant, and the
  starved/healthy split does not rescue it), and left OFF.** This is a designed-and-tested,
  measured-and-rejected flag, following the exact convention this file already uses for
  `STEAL_MARGIN = None` and `FEED_RESERVE_YIELDS_TO_OVERFLOW = False` — implemented so the next
  session does not have to re-derive it, documented with the measurement that killed it, off by
  default because the measurement did not clear the bar.

No other line in `kagg/search/schedule_agent.py` was touched. `git diff --stat` for that file:
`94 insertions(+), 2 deletions(-)`, entirely the block described above plus its docstrings.

## 4. What did NOT work, and why

**`SHOP_THIN_DEPTH_RULE` itself is the main negative result of this piece of work.** The design
hypothesis (from the brief, and the reason this flag exists at all) was: the blanket version of
"hold below-base stock back" measured net negative (32 seasons, `t=+2.90` FOR turning it off) because
holding hands the town's absorption to a contesting opponent, but MELON's sub-base volume was
reported unchanged either way, and MELON is the one product with zero shops on every board — so
gating the below-base hold on `shop_thin` (no shop currently open for that specific product) should
recover the win where it is genuinely uncontested and avoid the loss where it is not.

That hypothesis does not survive measurement here. `t=-0.27` overall, and splitting by the
mechanism's own target variable (WOOL-starved vs WOOL-healthy boards) gives `t=-0.25` and `t=-0.06`
respectively — both indistinguishable from zero, both nominally negative. Two candidate
explanations, neither separately confirmed:

- The "no shop currently open" definition may not track the right kind of contestation. Re-reading
  `docs/the_book_is_shallow_2026-08-09.md`'s own two-way table: **MILK is board-driven, WOOL is
  OPPONENT-driven** — wool's price spread is larger across opponents at a fixed seed (73.1) than
  across seeds at a fixed opponent (49.0). `shop_thin` is entirely a function of the shop draw
  (seed-driven, observable), not of how much the opponent is actually selling into the book
  (opponent-driven, only inferable from the inventory trend). It is plausible the flag is gating on
  the wrong axis of contestation for exactly the product (WOOL) the brief's own MELON evidence
  suggested it should help most.
- Sample size. n=9 and n=7 per starved/healthy subset, against this project's documented ~15% seed
  variance and per-seed spreads up to $75k inside a single subset (§1a), is not enough to rule out a
  real but small effect. `t=-0.25`/`t=-0.06` say "not detected here," not "proven zero."

**This is reported as the negative result it is.** The flag ships OFF, matching the measurement,
and is left in the codebase implemented and tested rather than deleted, so a future session with
more compute does not have to redo the design work — only the measurement, ideally on more seeds
and/or with a better definition of "contested" than shop-draw alone.

**A separate thing that was considered and NOT built at all: `BUY_PRODUCT` arbitrage on high-value
products.** The brief's scope explicitly includes "whether to `BUY_PRODUCT`." Reading
`reference/kaggriculture.py:585` (`_process_market`'s per-unit quoting loop) directly settles this
rather than requiring a measurement:

    elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
        quoted[player_id] = (...)
    ...
    else:
        order_states[player_id] = None  # malformed sub-op; abort

**`BUY_PRODUCT` is only legal for WHEAT and FERTILIZER.** Any `BUY_PRODUCT` order for MILK, WOOL,
MELON or STRAWBERRY is a no-op by construction — the env aborts it as malformed before it is ever
quoted. This closes off any "buy the opponent's dumped high-value stock back cheap, let the price
recover, keep selling into a healthier book" idea before it can be designed: the mechanic that
would make it possible does not exist for the products where it would matter. Of the two products
it IS legal for: WHEAT's `BUY_PRODUCT` line is the existing feed-purchase logic, explicitly off
limits per this task's instructions ("do not touch the feed-buy line"). FERTILIZER has **zero**
shops (`_KG.SHOPS` has no FERTILIZER entry) and is excluded from `TOWN_CENTER_PRODUCTS`
(`reference/kaggriculture.py:101`), so its town drain is permanently zero — there is no shop-unlock
signal to key anything off for fertilizer at all, and it is additionally producible directly via
`COLLECT_FERTILIZER` from an animal tile, which is production-adjacent and out of this task's scope.
**Conclusion: there is no shop-aware `BUY_PRODUCT` surface to build.** This is a structural finding
from the environment source, not a measured A/B — no test or arena run was needed or run for it,
and none should be read as implied.

## 5. Believed but NOT measured — do not treat as findings

- The "wrong axis of contestation" explanation in §4 for why `SHOP_THIN_DEPTH_RULE` failed
  (shop-draw-based thinness vs opponent-selling-based contestation) is a plausible read of the null
  result, not something separately tested. An opponent-inventory-trend-based contestation signal
  (e.g. rate of rise in `market.inventory` for a product over the last N turns, which is visible
  today via `market["inventory"]`, `shared: True`) was NOT built or measured. It is a candidate next
  step, not a recommendation.
- `HOLD_A_FLOORED_BOOK=False`'s positive-but-not-significant direction (§1b, `t=+1.29`) is
  consistent with the brief's original underpowered hint being real and this run still being
  underpowered, OR with it being noise that happened to land positive twice. 32 seeds did not
  settle it. More seeds (48-64) would be the direct way to find out; none were run here per the
  explicit instruction to stop measuring.
- Whether `SHOP_THIN_DEPTH_RULE` would look different sized on FERTILIZER specifically (always
  `shop_thin`, and per `reservation_units`'s own docstring its below-base regime already behaves
  close to a no-hold rule since its town drain is always zero) was not isolated per-product in the
  arena data collected — the 32-season numbers are whole-season bank totals, not decomposed by
  which product's below-base branch fired. This would need per-product fills accounting
  (`kagg/analysis/fills.py`) layered onto the mirror harness, which was not built.

## 6. Tooling notes (not a finding, but needed to reproduce any of the above)

This worktree started without `scripts/mirror_gate.py`, `scripts/board_demand.py`, or
`data/seed_scripts/top_guys/90976060/schedule.json` — all three exist in the main checkout's
working tree but are either uncommitted (`git status` in this worktree showed a clean tree at commit
`5cfaf78`) or gitignored (`data/*` is ignored except `data/README.md`). They were copied in
read-only from the main checkout to run the measurements this task explicitly required
(`scripts/mirror_gate.py`'s own docstring: "USE `scripts/mirror_gate.py`... DO NOT use
`scripts/tape_gate.py`"). No production code was copied or touched. `data/logs/` in this worktree
did not exist and was created fresh; the raw logs backing every number above are at:

    data/logs/mirror_shop_thin_depth_rule.log
    data/logs/mirror_hold_a_floored_book_false.log
    data/logs/split_starved_shop_thin.log
    data/logs/test_shop_thin_composition2.log   (the two slow composition tests, passing)
    data/logs/full_suite_after_edit.log         (full non-slow suite with this change)
    data/logs/full_suite_baseline.log           (same suite with the change stashed out)

**Pre-existing test failures, unrelated to this work:** the full non-slow suite shows 14 failures
plus 5 errors both WITH and WITHOUT this change (`test_router.py` x9, `test_stock_the_schedule_never_names.py`
x2, `test_a_stranded_feed_survives_a_dry_shed.py` x1, `test_locked_chain_relocates.py` x1,
`test_replay_plan.py` x5 errors). Identical failure set before and after this diff — confirmed by
running the suite with `kagg/search/schedule_agent.py` stashed out and comparing. Most plausibly
explained by this worktree missing data fixtures that are gitignored and present only in the main
checkout (the same reason `mirror_gate.py`/`board_demand.py`/the schedule fixture were missing).
Not investigated further — `test_router.py` is explicitly out of this task's scope, and none of
these failures are in `test_shop_thin_depth_rule.py` or caused by it.
