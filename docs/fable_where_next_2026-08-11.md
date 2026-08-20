# Where next: prioritised directions, with today's new measurements

Fable, 2026-08-11, worktree `agent-a29a0f4eb7054c852` reset to `898b81b`.
All new numbers below are seed 11, Victor tape, `townCenterSellInterval 24`, `weeds 0.0`, measured this session with `kagg/analysis/fills.py` wrapped around full-season runs.
Logs: `data/logs/fable_reconcile_money.log`, `fable_ours_fills.log`, `fable_tape_meldetail.log`, `fable_quadrants.log`, `fable_parity_check.log` (all in this worktree).
Scripts that produced them are in the session scratchpad; each is ~60 lines on top of `scripts/breakdown.py`'s own `run` loop and can be reconstituted from the log headers.

## 0. The "arithmetically impossible" money gap is CLOSED — the instruments are fine

I replayed Victor's game (both real seats, him vs Efe) and separately our agent vs the same Efe seat, and checked the money identity **per turn**:
`money = 3000 + sell_revenue − buy_costs − hire_costs − land_costs` — the only income in the reference is SELL inside `_commit_unit`, the only spends are the three buy ops, `_do_hire` and `_do_buy_land` (read directly off `reference/kaggriculture.py:639-708`).

| | Victor replayed | ours |
|---|---|---|
| sell fills | 1,434 units, $112,925 | 1,159 units, $93,298 |
| BUY_PRODUCT / SEED / ANIMAL | $9,810 / $6,700 / $6,100 | $9,234 / $6,230 / $6,100 |
| net trade | **$90,315** | **$71,734** |
| hires + land (identity residual) | −$10,004 | −$10,004 |
| final bank | **$83,311 = 3000 + 90,315 − 10,004, to the dollar** | **$64,730 = 3000 + 71,734 − 10,004, to the dollar** |

Zero turns had a positive residual; `fills.unattributed = 0`; every per-day residual decomposes into that day's hire fib-sums plus the d6 $1,000 and d10 $2,000 parcels.
So `fills.py` and `breakdown.py`'s money snapshot are **both exact**.
The briefing's "tape net trade $76,308" and "tape fills 1228" do not reproduce on this game — our side's numbers (1,159 / $64,730 / $83,311) reproduce exactly.
The impossible triple was two different games' numbers put in one equation (most plausibly: bank from the tape-vs-Efe replay, net trade from a tape-vs-**us** run, where Victor's fills are contested by our selling).
Action: find and delete whatever script produced 1228/$76,308, or stamp it with the game it measures. Nothing else is owed here.

Also settled in passing: hands do not persist overnight (`_end_of_day` sets `farm["hands"] = []`, `kaggriculture.py:867`), so the crew is re-hired daily and hire spend is a real season cost — ~$7,000 of Victor's $10,004 residual, 9–14 hires a day at fib prices.

## 1. The $18.6k net-trade gap, decomposed per product — this is the ranking that should drive the next week

Ours minus Victor-replayed, identical opponent (Efe's recorded seat), identical seed and economy:

| product | ours | Victor replayed | delta |
|---|---|---|---|
| STRAWBERRY | 213 u, $24,107 ($113/u) | 274 u, $46,430 ($170/u) | **−$22,323** |
| WHEAT | 313 u, $14,009 ($45/u) | 446 u, $18,957 ($42/u) | **−$4,948** |
| MELON | 102 u, $13,376 ($131/u) | 114 u, $16,542 ($145/u) | −$3,166 |
| FERTILIZER | 201 u, $12,903 ($64/u) | 237 u, $13,772 ($58/u) | −$869 |
| WOOL | 134 u, $22,244 ($166/u) | 138 u, $12,098 ($88/u) | **+$10,146** |
| MILK | 196 u, $6,659 ($34/u) | 225 u, $5,126 ($23/u) | +$1,533 |

(−$19,627 on sells, +$1,046 on buys = the −$18,581 net-trade gap exactly.)

Three things in this table override several standing assumptions:

- **Strawberry is the whole game right now.** It is bigger than everything else combined.
  Two halves: volume (−61 units = the production/watering gap) and price ($113 vs $170).
  The price half is a **late dump**: our fills go 30u@$168 d20 → 29u@$68 d22 → 12u@$20 d23 → 28u@$7 d24, while Victor sells *more* volume on the same days at $182/$162/$114.
  Selling 40 units for $27 combined while `HOLD_A_FLOORED_BOOK = True` is on means some path overrides the reservation logic on those days — prime suspects `SELL_TO_MAKE_ROOM` (shed pressure from produce arriving late, OPEN-1's shape) and the schedule row's own cumulative carry.
- **The tape is beatable on its own terms and we already do it on wool.** Victor's script dumps ~48 wool units at $1–2 on d12–d19; we hold and take $166/u average, +$10k over him.
  This is the concrete proof that "the tape is a diagnostic, not the goal" now has a measured win attached.
- **Milk is nearly worthless after d15 in Victor's own game** — his 225 units fetch $5,126 because the book floors at $1–5 from d16.
  The marginal late cow earns fertilizer and little else.
  This reframes the cow/sheep question (see D5) and caps what any herd-split cleverness can be worth.

## 2. Directions, ranked by expected value per unit of effort

### D1 — Stop the late-season strawberry/melon dump (do this first)

**Mechanism.** Produce arrives at the shed late (production oscillation, OPEN-1 delivery shape), stock piles up, and from d22 something sells 40+ units into a floored book at $7–68 despite `HOLD_A_FLOORED_BOOK`/`RESERVATION_SELL_CAP` being ON.
Victor books $114–182 on the same days.
Melon is the same shape smaller: his second flush goes out d20 60u@$151; ours goes d21 24u@$142 then d22 48u@$57 — one to two days late into a book his 60 units just crushed.

**Worth.** Order $10k+: the price half of strawberry's −$22.3k plus melon's −$3.2k. Even half-capture beats every other line on this page.

**Cheapest experiment.** Diagnostic before any fix, one run with a per-sell trace: for each d21–d25 strawberry fill, which code path emitted the offer (`SELL_TO_MAKE_ROOM`? the schedule row via `CUMULATIVE_SELLS`? `LIQUIDATE_LAST_DAY` is h16 d29 only, so it is not this).
Then one flag-level A/B judged on d20–d29 strawberry fills and W/L vs the Efe and Victor seats, 3 seeds.
Instrument: the fills-by-day table from `fable_ours_fills.log`'s script — it is exactly the right granularity and costs one season per arm.

**Dead-end risk.** Withholding only pays if the town's drain lifts the book before season end — strawberry appetite is 387–1,282 (board-dependent) and d22+ leaves ≤7 days of drain.
If the diagnostic shows the dump is *forced* (shed physically full because 60 units arrived in one evening), the fix is delivery pacing (OPEN-1), not sell logic, and the sell-side A/B will read null.
Both outcomes are cheap and informative.

### D2 — The parameter sweep on the Windows box (yes, but rebuild the space; the JAX sim is NOT the tool)

**Is the JAX sim usable today?** For *this* sweep, no — and not because of parity.
Parity is green (`tests/test_parity_1326_rules.py` + `tests/test_tape_parity.py`: 5 passed, re-run this session; `docs/parity_restored_on_1326_2026-08-09.md` for the full restoration).
It is that the candidate being swept is `schedule_agent_1455mh`, a Python planner that cannot run inside JAX, so the env must be `kaggle_environments` (or the numpy sim) driven per-step from Python, and the GPU buys nothing.
The register's "CMA-ES on the JAX sim over a direct market policy" is a different, parked project; do not conflate them.
This sweep is a **CPU farm job**: measured today ~2–4 min per full season on the Mac; the box is ~2.2x slower per core with 16 workers (`docs/throughput_measurements.md`).

**The scaffolding already exists**: `scripts/es_market.py` — paired seeds, blend fitness (win rate primary, margin as tiebreak), per-generation baseline re-scoring, `--holdout` re-scoring of the champion on unseen seeds.
Three repoints before it is honest for today's baseline:

1. `PLAN` → `data/seed_scripts/victor/schedule.json` (it still points at Seb's `90976060`).
2. Agent module → `schedule_agent_1455mh` (it imports `schedule_agent`).
3. **Rebuild `SPACE` from 1455mh's actual constants.** Five of its fourteen names (`SELL_OFFER_CAP`, `CAP_SELL_OFFER_SIZE`, `SELL_EVERY_N_HOURS`, `SELL_ON_DRAIN_CADENCE`, `FEED_DAYS_FLOOR`) do not exist as module constants on 1455mh — `setattr` would create dead attributes nothing reads, i.e. silent null dimensions, the exact `feedback_no_silent_disable` trap.
   Assert `hasattr` for every SPACE key at startup.

**The space that actually matters on 1455mh** (every one exists, is read, and has a measured comment):

| group | constants | why in the space |
|---|---|---|
| sell shape | `RESERVATION_CONTEST` (0–1), `RESERVATION_SLIP` (0–0.35), `LATE_SELL_FROM_HOUR` (0–20), `LATE_SELL_BIAS` (b), `SELL_CARRY_DAYS` (1–5), `SELL_BIGGEST_FIRST` (b), `LIQUIDATE_FROM_HOUR` (8–22) | D1's neighbourhood; the $22k row |
| feed cadence | `FEED_TURN_CAP` (1–12), `FEED_DAYS` (1–4), `FEED_DAYS_LATE` (1–6), `FEED_DAYS_FROM_DAY` (8–22), `BUY_DRIP` (1–4), `DUSK_FEED_HOUR` (14–22) | feed correlates +0.452 with money; OPEN-5's cadence |
| herd split | `HERD_FLOOR_COW` (0–6), `HERD_FLOOR_SHEEP` (0–4), `SHOP_ADAPT_FROM_DAY` (3–12) | settles D5 empirically instead of by hand |
| planner | `crew.ACTIVE_UNTIL_DAY` (0–30) — **different module**, the harness must set `kagg.search.crew` too | D3's knob; current 8+{10} was tuned on 17 days |

Deliberately NOT in the space: schedule quantities (wheat/melon/strawberry tile counts) — those live in `schedule.json`, not module constants, and need a schedule-transformer to sweep; that is phase 2 and only worth building if phase 1 moves.

**Objective.** Win rate against a **frozen** panel of interval-24 recorded seats, margin only as tiebreak (`blend`), exactly as `es_market.py` already does.
Panel: the 20 seats in `data/seed_scripts/top2/` (Victor ×7, THUNDER, Efe, Ueddy, Dmitry Larko, …) plus non-`alex chilton` interval-24 seats from `top_guys`.
This panel discriminates: we currently **lose** to the Efe seat on seed 11 ($64,730 vs $69,160), so win rate is not saturated the way the old arena pool was.
Money is logged, never selected on.

**Winner's-curse protocol** (the fixed-3-seed +40%-vs-+12.8% lesson, all four parts):
paired seeds per opponent; holdout seeds AND holdout opponent games the search never sees; champion re-confirmed on a fresh draw before anything ships; accept only improvements clearing one SE on the holdout.
`es_market.py` implements the first and third; add the opponent split.

**Cost.** pop 16 × 20 opponents = 320 games/gen ≈ 2–4 h/gen on the box at 14 workers; 10–15 generations is one to two nights.
Run in `~/kagg/.venv-kagg` (1.32.6) — NOT `.venv`/`.venv-cuda`, which carry the dead economy — with vLLM stopped, log tee'd on the box.

**Dead-end risk.** The sweep may un-match d0–d7 to buy wins — that is allowed (winning is the goal), but decide up front that its output is a *separate candidate* judged on the panel, not on the tape grid, or the two acceptance criteria will fight.
Second risk: 14 knobs × 320 games/gen is thin coverage; if nothing clears the SE by gen ~8, stop and narrow to the sell-shape group alone.

### D3 — The production oscillation: crew-planner day range, and the plant-that-cannot-be-watered rule

**Mechanism.** The volume halves of strawberry (−61 u) and wheat (−133 u sold) plus all 13 weeds are one failure: `cover.cover` oscillates after d10 — idle unit-turns 128, 11, 66, 12, 100, 8, 101 across d10–d16 against the tape's 78, 57, 39, 48, 38, 23, 49, watering swinging in antiphase (`kagg/search/crew.py` header, measured on the Victor grid).
Two days unwatered = weed; every weed is ours.
Separately, the router permits a PLANT so late its same-day WATER cannot happen, which converts a seed into a weed by rule (`consecutive_unwatered` starts at 1; mechanism traced at tile (5,3), `docs/fable_the_d4_d5_planner_2026-08-11.md` §5).

**Worth.** Order $5–15k gross: 61 strawberries at his $170 is ~$10k alone if both halves (grow it, then don't dump it) land; the weed tiles also cost DIGs and replants.

**Cheapest experiment.** `ACTIVE_UNTIL_DAY` ∈ {8, 11, 15, 20, 30} × {with/without d10 extra} on the Victor grid — five configs, judged on weeds, strawberry board tiles at d16/d29, strawberry fills d14+, and W/L vs the Efe seat.
~30 games ≈ an afternoon on the Mac.
The crew docstring itself says the old 0.427-at-11 sweep was measured against Seb-era opponents and must be re-measured here.
The late-PLANT rule is a one-test-one-fix item on the existing grid harness.

**Dead-end risk.** The lawnmower was never tuned past d10 and may genuinely be worse late (that is what the 30-vs-11 sweep said on the old target); if so the answer is a d11+ anti-oscillation term in `cover.cover`'s pricing (a tile watered yesterday should not price at zero tomorrow), which is more work.

### D4 — Keep grinding the d8+ frontier (the geometry item lives here, not as a program)

Today's method — trace the day, prove the code path, one test one fix — closed thirteen defects and moved the exact-match frontier to d8.
The next known items: d7 `buy_seed 11/12`, d8 `feed 11/12`/`care 11/12` (the dawn-block fix's siblings, partially reached), d8 `place 1/2` — which is the briefing's geometry observation in concrete form: pens and crops draw from one free-tile pool and nothing reserves near-shed ground for pens the schedule still owes, so by d8 the placement wants ground that is gone.
Fix it as that one defect (reserve the schedule's owed pen tiles from the plant pool), not as a geometry program — pen geometry as a money lever is measured dead (C-21, `docs/geometry_of_the_herd_2026-08-09.md`).

**Worth.** Each item is small ($100s to low $1,000s) but they compound, and this is the only line of work with a demonstrated 13-defects-per-day close rate.
It also keeps the baseline honest for D1–D3's measurements.

### D5 — The cow/sheep/goose split: fold into D2, and here is the evidence to carry

- `SHOP_ADAPT_HERD` barely discriminates (9/5, 10/4, 10/4, 10/4 across seeds 11/13/29/41, seed 13 having no YARN_STORE) because `expected_future_drain` keeps P(YARN_STORE still coming) material deep into the season and the floor+already-bought anchoring leaves ~1 animal of actual freedom.
  That is visible in the code (`schedule_agent_1455mh.py:3770-3834`); it is working as designed, and the design has almost no float.
- The milk-collapse measurement above caps the stakes: his 225 milk units earn $5,126.
  Late cows are fertilizer engines, wool recovers late ($109–181 d24–28), and the whole cow-vs-sheep revenue question is worth low thousands, not tens.
  Let the sweep set the floors and `SHOP_ADAPT_FROM_DAY`; do not hand-tune further.
- **GOOSE: both a schedule fact and an agent limitation, and leave it that way.**
  The schedule has no goose rows; `SHOP_ADAPT_HERD` floats only COW/SHEEP; and the swap is NOT free the way cow↔sheep is — a goose needs a COOP, not a PASTURE, so it touches the build schedule and routing.
  Field evidence: zero geese across all 16 top players in 2,744 seats.
  Nothing here is worth a COOP implementation.

### D6 — The fourth quadrant: a measured "not now"

New measurement this session (`data/logs/fable_quadrants.log`): **every one of the 20 seats in the current top-of-ladder sample (`top2/`: Victor, THUNDER, Efe, Ueddy, Dmitry Larko, …) finishes with exactly 3 quadrants.**
Four-quadrant play was the old economy (Seb) and us.
The economics of the fourth parcel: $4,000 (`LAND_PRICES[2]`), and — the real wall — the crew to work it is priced in fib: the 15th daily hire costs $610, the 16th $987, *per day*, forever (hands are re-hired daily, §0).
25 tiles of wheat from ~d12 is roughly 350–500 extra unit-turns over the remaining season ≈ 1–2 extra hands/day ≈ $8–15k of hires against ~$14–20k gross — marginal at best, negative if the sell book or the watering slips.
Wheat being the one unsaturated product is the only argument *for*, and it is a real one.
**Verdict: park it behind D1–D3.** Revisit only if, after the oscillation fix, the late-season idle rows still show 50+ surplus turns/day — then the marginal crew is already paid for and the arithmetic flips.
The honest test (a schedule arm with land d11–d12 + wheat lawnmower rows) is days of work; do not spend them yet.

## 3. Plainly not worth doing

- **Goose / COOPs.** See D5. Zero field evidence, real build cost, thin EGG book.
- **Pen geometry as a program.** Closed twice with artifacts (C-21, `geometry_of_the_herd_2026-08-09.md`). The d8 `place 1/2` defect is real but is a reservation bug, not geometry.
- **Movement as its own direction.** mv/wk 1.09 vs 1.01 is ~229 extra moves ≈ a ceiling of a few $k gross, and most of it is the D3 oscillation wearing its walking shoes. Fixing D3 is fixing this; polishing routes on an oscillating plan is polishing the symptom.
- **Rebuilding the agent in JAX to sweep on GPU.** Weeks of work to accelerate a search whose CPU cost is one or two nights. The JAX sim stays what it is: parity-green infrastructure for the parked RL/direct-policy track.
- **Re-deriving watering rules.** Measured: ~4% of the tape's 415 waters are top-ups of safe tiles; the vocabulary already exists. The gap is scheduling (D3), not rules.
- **Melon tile-count re-derivation from appetite/headroom models.** Withdrawn once already (the drain-cliff-vs-price-slope error, `the_ladder_is_two_scripts.md`). If melon quantity is ever revisited, it goes through the phase-2 schedule sweep with W/L as the judge, or through the marginal-unit `market_price` rule — never through another appetite model.
- **Trusting the $76,308 / 1,228 aggregates anywhere.** They mix games (§0). Ours-side numbers reproduce; those two do not.

## 4. Suggested order of play

1. **D1 diagnostic** (one traced run, same afternoon) → D1 A/B.
2. **D3 crew sweep** on the Victor grid (an afternoon, runs while D1 is being read).
3. **D2 repoint + launch** on the box overnight — it industrialises D1/D3/D5's knobs together.
4. **D4 frontier grind** as the steady background, including the d8 pen-reservation fix.
5. D6 re-priced only after 1–3 land.
