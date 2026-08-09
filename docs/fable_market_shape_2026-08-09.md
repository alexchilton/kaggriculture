# Market shape: Seb vs us, measured on fills — task #49

2026-08-09. Branch `shaping-potential`. Follows on from `docs/fable_the_discard_problem_2026-08-09.md`
earlier the same day. `kagg/search/schedule_agent.py` is the only file changed.

## Verdict, up front

- **LATE_SELL_BIAS is a real, substantial win.** Arena A/B, 8 held-out seeds × 3 opponents × both
  seatings (48 games/state): pool win rate **14.6% → 27.1% (+12.5pp, nearly double)**, mean money
  **$16,146 → $24,535 (+$8,389)**. Positive or flat on every individual opponent, never negative.
  This is the headline result of this task. See §4.
- **CAP_SELL_OFFER_SIZE's byte-identical A/B result is a genuine null, not a bug — checked, not
  assumed.** The coordinator flagged that an identical OFF/ON result usually means the flag never
  reached the code path (their own `still_owed` mistake earlier today). I re-verified the flag
  directly through the exact arena wiring (`make_our_agent()` + `kaggle_environments`, no
  overrides): seed 2 vs `contrarian`, OFF emits `SELL WHEAT 43`, ON caps it to exactly 30, money
  $10,268 → $10,265. The flag works. It just never binds on the 8 seeds (20-27) the A/B used against
  any of the 3 pool opponents — confirmed directly, max offer stays ≤23 there. The premise
  ("standing offer vs few/small/late") also does not cleanly explain the money gap on fills: Seb's
  realised price is far above both us and the opponent who beat us in the sample loss ($141/unit vs
  $93/unit vs $86/unit), but the opponent's own single-product orders are BIGGER than Seb's (mean
  7.8, max 31, vs Seb's mean 4.0, max 16) — what separates the three is **product mix sold**, not
  order shape. See §2 and §3.1.
- **A separate, bigger question the coordinator raised: is the 14.6% baseline a regression, or a
  harder/different pool than the historical "94.4%"?** Traced the 94.4% figure to its source
  (`schedule_agent.py` ~line 873): it is explicitly flagged IN THE SOURCE, at the time it was
  recorded, as a **saturated, uninformative** number — "94.4% with `mirror` at 50% means every
  non-mirror opponent already loses 100% of the time... the pool cannot see it." That pool included
  `mirror` and, per this project's own repeated warnings, most likely `starter`
  (`CLAUDE.md`: "never tune against starter alone... the market is never contested"). My 14.6% used
  only `heuristic`/`rancher`/`contrarian`, no mirror, no starter. **These are not the same
  measurement and the drop is not a valid before/after comparison.** What I did confirm on one seed:
  our agent is not globally broken (plays normally against Seb's tape, ~$50k by day 28, matching this
  morning's numbers); the "hands: 0" reading that looked alarming mid-check is by design (crew is
  dismissed nightly, confirmed by tracing hands rising to 7 within the first hour of every day). The
  live-pool weakness is real but its root cause is a separate, already-tracked project-level question
  (`docs/the_top_five_clusters_2026-08-09.md`: "we score 1,123.5, the field floor is ~3,117"), out of
  this task's scope. See §4.1.
- **Both candidates are implemented behind flags, default OFF, with RED-before-GREEN tests**
  (`tests/test_market_shape_candidates.py`, 9/9 passing). See §3-4 for the numbers and §5 for the
  recommendation.

## 0. What the task handed me, and the one correction to it

The stats quoted for order COUNT/SIZE/hour-distribution (Seb 244/4.9/30, 54% late; us 456/3.9/78,
40% early) are OFFER counts and were already flagged as not requiring a fills correction — a COUNT of
distinct order objects and their individual sizes doesn't need the CLAUDE.md fills warning the way a
SUMMED volume does. I did not recompute them; they are quoted as given.

What I owed on top: **fills and realised prices**, which the task explicitly said nobody had done.
That is §§1-2 below.

## 1. Method: two shed-delta techniques, one much better than the other

**First attempt — reuse `scripts/breakdown.py`'s shed-delta method directly on the recorded JSON.**
`SELL`/`BUY_PRODUCT`/`BUY_ANIMAL` settle straight against `private["shed"]`, so a turn's shed delta
is the fill — PROVIDED no `DROP`/`PICKUP`/`PLACE` also fired that turn (they touch the same field
and taint the read). Applied directly to `data/seed_scripts/top_guys/90976060.json` (Seb) and
`data/ladder/losses/91229682.json` (our loss), this recovered order-count stats that matched the
task's own numbers exactly (244 SELL offers for Seb, 455 for us) — a good cross-check that the
method and the recorded data agree. But **coverage was terrible**: only 18 of Seb's 244 SELL offers
landed on a clean turn, so total captured revenue was $13,355 against a final bank of $128,518 — a
>90% undercount, useless for a realised-price comparison. Both players' crews DROP constantly as
part of normal routing, so most turns that also carry a market order are tainted.

**Second attempt, adopted — exact revenue via money conservation, not shed reconstruction.**
`reference/kaggriculture.py` shows money moves ONLY via `SELL`/`BUY_PRODUCT`/`BUY_ANIMAL`/
`BUY_SEED`/`HIRE`/`BUY_LAND` (`_commit_unit`, `_do_hire`, `_do_buy_land`) — never by any unit-phase
op (`DROP`/`PICKUP`/`PLACE`/`HARVEST`/...). Of those six, four are FIXED cost, computable exactly
from tables and counters already in the observation (`BUY_SEED`/`BUY_ANIMAL` are flat per-item
constants; `HIRE` is `mult * fib(hires_today)`, `hires_today` read straight off the farm; `BUY_LAND`
is `LAND_PRICES[len(unlocked_quadrants) - 1]`). Only `SELL` and `BUY_PRODUCT` depend on the live
market curve. So on any turn whose market list has **no `BUY_PRODUCT`**, that turn's money delta
minus the (exactly known) fixed costs of whatever else fired IS that turn's SELL revenue, exactly —
no shed reconstruction, no DROP taint, and `_commit_unit`'s SELL branch only ever fails on an empty
shed (never a capacity limit), so a covered turn's offered quantity is also its filled quantity.

Coverage: **81% for Seb, 41% for us, 76% for the opponent** (of turns that emitted ≥1 SELL order).
Sanity check: **zero negative-revenue events** across all three (a SELL-only, no-`BUY_PRODUCT` turn
can never legitimately lose money; a negative reading would mean the accounting was wrong, and an
earlier pass of this exact script produced exactly that — see the retraction in §1.1).

### 1.1 A bug caught and fixed before trusting any number here

The first version of the money-delta script paired `steps[t]['action']` with the money change from
`steps[t]` to `steps[t+1]`, and produced physically impossible NEGATIVE "pure-SELL-turn" revenue —
e.g. `SELL WHEAT 1` alongside a **-$935** money change. `kaggle_environments`' own convention (used
correctly by `scripts/breakdown.py`'s `tape_policy`, which builds its replay list from
`d["steps"][1:]`) is that `steps[i]['action']` is the action chosen IN RESPONSE to
`steps[i]['observation']`, applied to produce `steps[i+1]` — so the action explaining a turn's money
move lives at `steps[t+1]`, not `steps[t]`. Fixed, re-run, zero negative events since. Recorded here
per this project's testing culture: a measurement that looks plausible enough to report is not the
same as one that has been checked against a physical invariant.

## 2. What actually differs, on fills

Money-delta method, `data/seed_scripts/top_guys/90976060.json` (Seb) and
`data/ladder/losses/91229682.json` (us seat 0 / opponent Shivam_2212 seat 1, the loss this task
names). All figures below are from **covered** (SELL, no `BUY_PRODUCT`) turns only; totals are a
sample, not the season total, at 41-81% coverage as noted.

```
                        events  covered qty   revenue    mean $/unit   single-order size (mean/max)
Seb (allegedly)            113          1064   $150,395      $141.35             4.0 / 16
us (the loss, seat 0)      130          1053    $98,072       $93.14             2.0 / 6
opponent (seat 1, won)      79          1209   $103,777       $85.84             7.8 / 31
```

By hour bucket (mean $/unit):

```
                h0-7      h8-15     h16-23
Seb            $149.17    $130.35    $138.68     -- flat-to-slightly-DOWN late, not up
us             $108.66     $60.62     $86.89     -- mid-day is the bad hour, not early
opponent        $76.65    $150.42     $95.68     -- no consistent pattern either
```

Per-product, single-product covered turns (the part of the sample with a clean per-item price):

```
Seb:        WOOL 55u@$38   FERTILIZER 52u@$73   STRAWBERRY 34u@$183   MELON 28u@$133
            WHEAT 21u@$36  MILK 6u@$276
us:         FERTILIZER 66u@$65   WHEAT 49u@$42   MELON 6u@$232   MILK 6u@$107
            STRAWBERRY 5u@$174   WOOL 3u@$181
opponent:   STRAWBERRY 190u@$161(!)   MILK 31u@$115   MELON 24u@$95
            FERTILIZER 20u@$86   WHEAT 7u@$40
```

### 2.1 Reading it: this is a product-mix gap dressed as a price gap

Seb's realised price is 51% above us and 65% above the opponent who beat us — that part of the
premise holds. But the mechanism the task set out to test — small, late, deliberate orders command
a better price than a large, early, standing offer — **does not survive the opponent row**. The
opponent's own single-product orders are *bigger* than Seb's (mean 7.8 vs 4.0, max 31 vs 16, both
comfortably over "30" and over our 6), and the opponent still realises a materially LOWER average
price than Seb ($86 vs $141) and is not clearly ahead of us on price either ($86 vs our $93 — we are
nominally *higher*, on this sample).

What the per-product table shows instead: **we sold 115 of 135 single-product covered units (85%)
in WHEAT and FERTILIZER, both under $75/unit; the opponent sold 190 of 272 (70%) in STRAWBERRY at
$161/unit, and moved that volume without collapsing the price** (which is consistent with the
project's own earlier finding in `scripts/measure_sell_timing_impact.py`: seven of eight products
are in a "thick" market regime where a big offer barely moves the price — melon is the one thin
exception). Seb's mix is the most balanced of the three, with real STRAWBERRY, MELON and MILK
volume alongside wheat/fertilizer/wool. The opponent's win in this game reads as **produce more of
the expensive thing and sell it in bulk into a market that can absorb it**, not as **place smaller,
later orders**.

This does not mean order shape is worthless — a 51-65% price gap against Seb specifically is real
and worth keeping on the table — but it means **the loss to Shivam_2212 specifically is not
explained by sell shape on this evidence**, and a fix aimed at shape (§3) should not be expected to
close a gap that is actually about what got planted and harvested.

**Caveat with teeth:** one loss game, one Seb tape, 41-81% coverage. This is a real, exact-on-its-
subset measurement, not a full-season census. A different loss, or the full uncovered 19-59% of
sell-turns, could tell a different story. Treat §2.1 as the strongest reading of the evidence
gathered, not a closed case.

## 3. The candidates: implemented, RED-before-GREEN, both OFF by default

`kagg/search/schedule_agent.py`, new flags near `RESERVATION_SLIP` (~line 997):

```python
CAP_SELL_OFFER_SIZE = False
SELL_OFFER_CAP = 30

LATE_SELL_BIAS = False
LATE_SELL_FROM_HOUR = 16
```

Enforcement sits right after the `LIQUIDATE_LAST_DAY` override in the per-product sell loop
(~line 2720), so neither candidate can touch the last-day liquidation window every other cap in that
loop already exempts:

```python
last_day_liquidating = LIQUIDATE_LAST_DAY and day >= last_day and hour >= LIQUIDATE_FROM_HOUR
if CAP_SELL_OFFER_SIZE and not last_day_liquidating:
    n = min(n, SELL_OFFER_CAP)
if LATE_SELL_BIAS and hour < LATE_SELL_FROM_HOUR and not last_day_liquidating:
    n = 0
```

Tests: `tests/test_market_shape_candidates.py`, 9/9 passing
(`data/logs/market_shape_final_2026-08-09.log`). Existing suite checked for regressions:
`tests/test_router.py` is unchanged at 8 failed / 62 passed / 6 skipped, the same pre-existing
failures left by the day-gating fix earlier today (`docs/fable_the_discard_problem_2026-08-09.md`
§2), confirmed via the byte-identical-when-off rail (`test_both_flags_off_is_byte_identical_to_the_
shipped_agent`) rather than assumed.

### 3.1 CAP_SELL_OFFER_SIZE

RED scenario, found by measurement rather than assumed: a solo replay against a dummy opponent never
produces an over-30 offer on any seed tried. A **24 seed×opponent sweep** (`heuristic`, `rancher`,
`contrarian`; 8 seeds each; `data/logs/market_shape_offer_sweep_2026-08-09.log`) found exactly two
over-30 offers, both `SELL WHEAT 43` on day 29 hour 0, both against `contrarian` (seeds 2 and 6).
Against `heuristic`/`rancher` the ceiling never even reaches 25. So the flag is real but the surface
it acts on is narrow: most of the historical "78-unit offer" gap already closed on its own once
`RESERVATION_SELL_CAP` / `PRICE_AWARE_SELL_CAP` / `HOLD_A_FLOORED_BOOK` shipped.

RED (`CAP_SELL_OFFER_SIZE=False`, seed 2 vs `contrarian`): `SELL WHEAT 43` on day 29.
GREEN (`CAP_SELL_OFFER_SIZE=True`, same seed/opponent): capped to exactly 30, no offer over the cap
anywhere in the season. `tests/test_market_shape_candidates.py::test_the_cap_reproduces_and_then_
fixes_an_over_thirty_offer`.

**Post-sweep re-check, prompted by the coordinator.** The arena A/B in §4 came back byte-identical
between OFF and ON on all three pool opponents across seeds 20-27 — exactly the signature of a flag
that never reaches the code path (the coordinator's own `still_owed`/`max()` mistake earlier today).
Checked rather than trusted: ran the EXACT arena wiring (`make_our_agent()`'s seat-agnostic wrapper,
`kaggle_environments.make("kaggriculture", configuration={"seed": 2})` with no overrides, matching
`kagg.arena.run_arena`'s own config) on the one seed/opponent pair already known to trigger the cap.
Result: `CAP_SELL_OFFER_SIZE=False` → max SELL offer 43, final money $10,268;
`CAP_SELL_OFFER_SIZE=True` → max SELL offer exactly 30, final money $10,265. The flag reaches the
code path and does what it says. Then re-swept seeds 20-27 against `contrarian` specifically (the
only opponent that ever triggered it) with the flag off: max offer across all 8 held-out seeds is
23 — never above the cap. **The byte-identical A/B result is a genuine null: the held-out seeds
simply never exercise this candidate, on any of the 3 pool opponents.** It is not evidence the cap
is harmless or useless, only that this A/B has no statistical power to say either way. A wider seed
sweep specifically against `contrarian` (where the trigger lives) would be needed to get a real
answer; not run here given the time already spent and LATE_SELL_BIAS's much larger, unambiguous
signal in §4.

### 3.2 LATE_SELL_BIAS

This one is unambiguously wired and unambiguously live: `test_without_the_bias_orders_fire_before_
hour_sixteen` shows early offers firing under default settings on every seed tried, and `test_late_
sell_bias_actually_suppresses_early_offers` shows the flag removing every one of them (last-day
liquidation excepted). Unlike the cap, this candidate is not narrow — it changes roughly two-thirds
of the day's selling window (hours 0-15 of 24) to zero SELL orders, every day, all season.

The code's own prior evidence should be read as a warning before trusting this without a number:
`SELLS_FUND_THE_TURN` is a load-bearing mechanism that funds same-turn `BUY_LAND`/`BUY_SEED`/
`BUY_ANIMAL` from that turn's SELL proceeds, and the file's own day-6 example
(schedule_agent.py ~line 2820) shows Seb buying `BUY_ANIMAL COW 2` and `BUY_SEED MELON 6` on a bank
of $15, funded by a same-turn `SELL WOOL 6` at hour 2 — inside the window this flag would zero out.
Blocking all selling before hour 16 is a strictly blunter instrument than that funding mechanism
needs; it was implemented and tested as literally specified ("biasing sells toward h16-23") rather
than pre-softened, on the view that the A/B should say whether it costs money, not have the answer
assumed into the design.

## 4. Does it cost win rate — the A/B

`kagg.arena.run_arena`, workers=1 (closures from `make_agent` are not picklable across
`ProcessPoolExecutor`'s macOS spawn — the same constraint `scripts/arena_gate.py` documents).
Opponent pool: `heuristic`, `rancher`, `contrarian` (the diverse-crop-mix, same-play-style pool
`CLAUDE.md` describes). 8 seeds (20-27), both seatings via `run_arena`'s built-in swap = 16 games per
opponent per state. Seeds held out from the seeds used to find/verify the candidates (2, 11).
Selection criterion is **win rate**, per `CLAUDE.md` — the ladder is Elo, and money is a dense
training signal, not the verdict.

Full log: `data/logs/market_shape_arena_ab_2026-08-09.log`.

```
CAP_SELL_OFFER_SIZE                    win rate    mean money      opponent breakdown (money, win%)
  OFF                                    14.6%       $16,146        heuristic 8,672/12.5%  rancher 21,450/6.2%  contrarian 18,317/25.0%
  ON                                     14.6%       $16,146        heuristic 8,672/12.5%  rancher 21,450/6.2%  contrarian 18,317/25.0%
  delta                                  +0.0pp           +0        byte-identical on every opponent -- see §3.1, verified a real null

LATE_SELL_BIAS                         win rate    mean money      opponent breakdown (money, win%)
  OFF                                    14.6%       $16,146        heuristic 8,672/12.5%   rancher 21,450/6.2%   contrarian 18,317/25.0%
  ON                                     27.1%       $24,535        heuristic 23,196/25.0%  rancher 28,612/31.2%  contrarian 21,798/25.0%
  delta                                 +12.5pp      +$8,389        UP or flat on every single opponent, never down
```

**Verdict: LATE_SELL_BIAS is a real, substantial, consistent win on this evidence.** Pool win rate
nearly doubles (14.6% → 27.1%), mean money rises 52% ($16,146 → $24,535), and the effect is
positive-or-flat on all three opponents individually — `rancher` alone goes from a near-shutout
(6.2%) to a real contest (31.2%). This is a much larger and cleaner signal than anything else
measured in this task, including the price-per-unit gap in §2 that motivated the whole investigation.
The mechanism this task set out to test — the design note's own claim that `SELLS_FUND_THE_TURN`
makes blocking early selling dangerous — did not materialise as a downside in this A/B: money went
up, not down, on every opponent. That does not mean the risk is zero (48 games is not proof against
a rare, expensive failure mode), only that it did not show up here.

### 4.1 The 94.4% vs 14.6% question

Traced per the coordinator's instruction, on one seed (20), before writing anything else:

- **Not the same measurement.** The 94.4% figure (`schedule_agent.py` PRICE_AWARE_SELL_CAP
  docstring, ~line 873) is explicitly flagged in the source, AT THE TIME it was recorded, as
  uninformative: *"94.4% with `mirror` at 50% means every non-mirror opponent already loses 100% of
  the time... the pool cannot see it."* Whatever pool produced that number included `mirror` (which
  can only ever read 50%) and, going by every other reference to "the arena pool" in this project,
  most likely `starter` — which `CLAUDE.md` names by itself as inflating results ~2x because it
  barely sells. My 14.6% used `heuristic`/`rancher`/`contrarian` only: no mirror, no starter, no
  seed overlap (theirs was 500-505, mine 20-27). A saturated-pool number from a different era
  compared to a deliberately harder, unsaturated one is not a before/after pair.
- **Our agent is not globally broken.** Re-ran `scripts/breakdown.py --tape seb1326 --seed 11 --days
  29` (the exact fixture used all morning): money $49,942 by day 28 against the tape's $75,556 —
  the same shape of gap documented in `fable_the_discard_problem_2026-08-09.md` earlier today, not a
  collapse. Whatever is happening against the live pool is not "the agent stopped working."
- **A red herring, resolved rather than reported.** A first diagnostic pass showed "hands: 0" at the
  start of every single day against `heuristic`, seed 20 — alarming at a glance, as if hiring were
  silently broken. Traced turn-by-turn: hands go 0 → 5 → 6 → 7 within the first three hours of every
  day. `schedule_agent.py`'s own comment says why: *"hands are dismissed nightly, so every claim is
  stale."* Dawn is the one instant hands are legitimately always 0; not a bug.
- **What is real and in scope:** the pool win rate against `heuristic`/`rancher`/`contrarian` really
  is low (14.6%), and §4's result shows sell TIMING is a real, substantial part of why — closing
  nearly half the gap to a coin flip with one flag. What is real and OUT of scope: why the remaining
  gap exists. `docs/the_top_five_clusters_2026-08-09.md` already tracks a large, independent
  competitiveness gap under 1.32.6 ("we score 1,123.5, the field floor is ~3,117"), which is
  consistent with what I measured here but is a project-level question, not a market-shape one. I am
  not claiming to have resolved it, and flagging it rather than chasing it further, per the
  instruction to stay on the market-shape task.

## 5. Recommendation

1. **LATE_SELL_BIAS is the strongest result in this task and should go to a wider confirmatory
   sweep before flipping the default.** `CLAUDE.md`: "confirm a search winner on a fresh draw" and
   "seed variance is ~15%." 8 seeds is a real signal (consistent direction on 3/3 opponents, effect
   size far larger than 15%) but is not yet the "twelve seeds" bar this project has used elsewhere
   before shipping a sell-rule change. Next step: the same A/B on a second, disjoint seed block, plus
   `homestead`/`shepherd` added to the opponent pool, before considering `LATE_SELL_BIAS = True` by
   default.
2. **Do not ship CAP_SELL_OFFER_SIZE on the strength of anything measured here.** Its A/B is a
   genuine null on the seeds tried — real, checked, not a bug — but a null from an under-powered
   test is not evidence of "no effect," only "not measured." If it is picked up again, test it
   specifically against `contrarian` (the only opponent shown to trigger it) on a wider seed range.
3. **Do not chase the 94.4%-vs-14.6% framing as a regression.** It is not a valid comparison (§4.1).
   The live-pool weakness it pointed at is real, tracked elsewhere, and only partially explained by
   what this task covers.
4. **The product-mix finding in §2.1 is worth a follow-up task of its own**, separate from sell
   shape: on the one loss traced, the opponent who beat us won by producing and selling far more
   STRAWBERRY (190 units at $161/unit) than we did (5 units), not by a different order shape. If that
   generalises, it points at what gets planted, not how it gets sold.

## 6. What's in the tree

- `kagg/search/schedule_agent.py`: `CAP_SELL_OFFER_SIZE` / `SELL_OFFER_CAP` and `LATE_SELL_BIAS` /
  `LATE_SELL_FROM_HOUR`, both flags OFF by default, plus the two-line enforcement in the per-product
  sell loop. No default behaviour changes with both flags off (pinned by
  `test_both_flags_off_is_byte_identical_to_the_shipped_agent`).
- `tests/test_market_shape_candidates.py`: new, 9 tests, RED-before-GREEN for both candidates plus
  the wiring and no-op rails this codebase's other sell-cap tests use as their pattern
  (`tests/test_reservation_sell_cap.py`).
- Scratch analysis scripts (`fills_analysis.py`, the abandoned shed-delta attempt;
  `fills_money_delta.py`, its SELL-only-turn refinement; `fills_exact.py`, the wider-coverage
  fixed-cost version actually quoted in §2; `arena_ab_market_shape.py`, the A/B harness) live in the
  session scratchpad, not the repo, matching this project's convention for one-off probes.
- Logs: `data/logs/market_shape_red_2026-08-09.log` (initial RED run), `data/logs/market_shape_
  green_2026-08-09.log` (post-wiring, still 2 failing on the vacuous premise test),
  `data/logs/market_shape_final_2026-08-09.log` (9/9 after fixing the RED scenario to use a live
  opponent), `data/logs/market_shape_offer_sweep_2026-08-09.log` (24-combination offer-size sweep),
  `data/logs/market_shape_arena_ab_2026-08-09.log` (the win-rate A/B).
- Not touched: `kagg/sim/`, `tests/test_sim_*.py`, `tests/test_tape_parity.py`, per instruction.
