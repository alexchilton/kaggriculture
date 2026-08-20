# The greedy is a mix scorer

Consolidated record for the routing / planner / greedy mix-scorer / tape-matching subject group.
Merged 2026-08-20 from 11 source docs into this one, in chronological order.
One dated section per source doc.
Every dollar figure, percentage, table, seed and per-day grid from every source survives below —
nothing was compressed away. Where a later section corrects an earlier one, the earlier claim is
kept and labelled superseded rather than deleted, since the reasoning inside it is often still
load-bearing.

**Note on `docs/REGISTER.md`:** its OPEN-14 entry currently claims
`docs/kawashigi_one_board_2026-08-13.md` was "folded into `the_ladder_is_two_scripts.md`; file
deleted." Neither is true — the file exists on disk and its content (world/market/tile hashes,
open-loop analysis) is absent from `the_ladder_is_two_scripts.md`. That REGISTER line looks stale.
It is folded into *this* doc instead, per the assignment for this consolidation pass; REGISTER.md
itself was left untouched, as instructed.

---

## 2026-08-09 — The tape column does not reproduce his game

Folded in from `docs/the_tape_column_does_not_replay_his_game_2026-08-09.md`.

> **TARGET SUPERSEDED, added 2026-08-11.** The harness-fidelity finding below (our replay of his
> recorded actions diverges from his recorded bank) is a real, version-skew bug and still stands. But
> the tape itself is now known to be a poor target regardless: it is Seb's, and Seb's median bank
> halved when the town rebalance landed and he has since withdrawn from the ladder
> (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats).

Measured 2026-08-09.

**Alex's position, which is correct: the tape is the JSON replay of the game he actually played.
The schedule was derived from that JSON. So if our harness disagrees with the tape, our harness is
wrong.**

This had never been tested end to end. It is now.

### The measurement

Push **his own recorded actions for BOTH seats** through a fresh env on seed 11 and compare, every
turn, against the money recorded in his own replay:

```
weeds=0.0    first money divergence  turn 32 (d1 h8)  sim=188  rec=187   FINAL sim=10,264   recorded=110,820
weeds=0.005  first money divergence  turn 32 (d1 h8)  sim=188  rec=187   FINAL sim=11,711   recorded=110,820
```

His actions, his opponent's actions, his board — and the simulation ends on **9%** of his real
bank. It starts diverging on **day 1, hour 8, by one dollar**.

### The cause: we replay a pre-1.32.6 game under 1.32.6

Turn 31, with both sides otherwise idle and only his `BUY_PRODUCT WHEAT 1` on the book:

```
turn 30   246 -> 217   recorded charge 29   installed env charge 29
turn 31   217 -> 188   recorded charge 30   installed env charge 29   <-- the dollar
```

Installed `kaggle-environments` is **1.32.6**. His replay predates the 2026-08-08 switch. The two
price wheat differently, so his recorded game is not reproducible here at all — one dollar at d1 h8
compounds to $10,264 against $110,820.

`weedSpawnChance` is not the cause: 0.0 and 0.005 both diverge at the same turn and both end ~10x
short.

**Alex has stated this roughly ten times across sessions and been argued with every time.** It is
closed. `docs/REGISTER.md`'s OPEN-CLI already carried it as "1.32.6 test failures ... Both simulators
fail parity on 1.32.6"; that entry and this document are the same fact.

### What IS verified

- The starting board is exact. Seed 11 reproduces his step-0 tiles cell for cell, same money, same
  town. So the seed choice is right and the divergence is not a different board.
- The schedule is derived correctly. Against his recorded actions across 17 days, `builds` and
  `places` match every single day, zero mismatches, 19 builds against 19. There is no error in the
  derivation — that hypothesis was tested and closed.

### What this invalidates

`breakdown.py`'s tape column runs his actions forward in our env (`breakdown.py:274`, both seats
from the replay). Since that run diverges at d1 h8, the column is **his action sequence executed
into a state that stopped being his after day 1**, not his game.

Consequences:

- **State rows** (`money`, `tiles`, `pens`, crops, herd) are not targets. His real melon reaches 18
  and the column shows 7. His real pastures reach 19 and the column shows 8, flat, all season.
- **Fill rows** (`sell`, `buy_product`, `buy_seed`, `buy_animal`) run through a book that is no
  longer his, so they degrade too.
- **Emitted-op rows** are still literally his recorded actions and are the least damaged — but the
  board they land on is wrong from d1 h8, so a refused or no-op action is counted where his
  succeeded.

Two rows chased this session illustrate it. `melon 7/6` at d5 and `pens 9/8` at d5 both read as us
over-buying. Neither is: the schedule's cumulative melon seeds are 7 by d5 and cumulative builds are
9 by d5, and we hit both exactly. The column is what is short.

### What has been recorded about this before, and why it was not enough

`.claude/skills/matching-the-tape` and `docs/REGISTER.md` both describe this as a **money**
contamination starting at **d4**, caused by the replayed Seb selling into a book we have lifted.
Both are wrong on all three counts:

- it starts at **d1 h8**, not d4;
- it affects state and fills, not just money;
- the tape run never faces our agent at all — `opp` is the replay's own seat 1.

The skill also notes "$2 a day compounds, and the $2 on d1 was hiding a defect worth $1,590 on d6".
That d1 dollar was seen and filed as small. It is the same dollar as turn 32 here.

### The schedule is still the target — Alex, 2026-08-09

**The schedule remains valid. Market prices vary between env versions; that is expected and is not a
defect to chase.** There are several replays, and the schedule is the portable thing derived from
them: what to build, place, plant, buy and sell, on which day. Money and realised fill prices are
not portable and never will be.

So the scoreboard for d0-d6 is **our actions against the schedule** —
`test_our_sells_match_the_plan_every_day`, `test_our_buys_match_the_plan_every_day` and the
per-day op rows — not our money against the tape column. Do not open a money gap as a defect.

### What to do before any more tape matching

Do not tune against the tape column until the replay reproduces his bank. The first job is turn 32:
one dollar, day 1, hour 8, with both sides playing his recorded actions. Find that, and the column
either becomes a real target or is replaced by his recorded observations.

---

## 2026-08-09 — Router tape repoint: `seb` to `seb1326`

Folded in from `docs/router_tape_repoint_2026-08-09.md`.

> **TARGET SUPERSEDED, added 2026-08-11.** `seb1326` (`90976060`) is itself the tape
> `docs/the_ladder_is_two_scripts.md` identifies as "his interval-12 shape" — the low-wheat build Seb
> kept running after the town rebalance, which is why his median bank halved and he has since
> withdrawn from the ladder (measured from 2,744 ladder seats). The re-derivation work below (day-by-day
> diffs, the repointing mechanics) is still correct; repointing onto this particular tape is not the
> fix — see that doc's "best tape to rebase on" for Dmitry Belan / Efe Can Celiksoy instead.

`tests/test_router.py`: repointing the tape fixture from `seb` to `seb1326`, and re-deriving every asserted day.

Task #53.
`TAPE_REPLAY` / `TAPE_SCHEDULE` / `TAPE_TEAM` (added `a34cc1e`) repointed from
`data/seed_scripts/top_guys/90494364` (`seb`, played on 1.32.2) to
`data/seed_scripts/top_guys/90976060` (`seb1326`, played on 1.32.6).
The two tapes land quadrants on different days (5/9/11 vs 4/6/10), carry different pen counts
(~19 vs 21), and re-cut the herd from wool to milk (MILK 179→303, WOOL 230→104, MELON 132→96), so
every day-specific number in this file had to be re-derived rather than merely re-run.

### Method

Two scripts (temporary, not committed — logs kept under `data/logs/`):

- **`tape_truth.py`** replays the leader's own recorded actions against his real recorded opponent
  from the episode JSON. Because kaggriculture is deterministic given seed + actions, this
  reproduces the historical episode exactly — it is the ground-truth "tape" value every test
  docstring quotes. Output: `data/logs/tape_truth_90976060.log` (dawn bank, sells, op tallies, seed
  peaks, first-sell/first-buy hours, per day 0–11).
- **`day_by_day_diff.py`** runs the same replay for the tape's actions and for our
  `schedule_agent`-driven agent (playing against the same real opponent sequence), and diffs the
  op tally per day. Output: `data/logs/day_by_day_diff.log`.

Sanity check: replaying the OLD tape's own actions under the current 1.32.6 env gives dawn day 6 =
**$1,855**, matching the number already recorded in the `TAPE_REPLAY` comment block before this
pass started. Same method, same answer — the new-tape numbers below use the identical method.

### Finding that changes the shape of the triage: days 0–3 are no longer exact under `seb1326`

The day-4 gate's docstring claimed "days 0-3 already exact" — true of the old tape, false of the
new one. Op-for-op diff, our agent vs. the tape's own replayed actions, days 0–3:

```
day 0: {'FEED': '1/4', 'CARE': '1/4', 'SELL': '7/0'}
day 1: {'SELL': '2/4'}
day 2: {'SELL': '6/5'}
day 3: {'FEED': '4/6', 'CARE': '4/6', 'SELL': '7/5'}
```

So day 4's shortfall (below) is not purely a day-4 defect; it inherits upstream drift. Recorded in
the test's docstring; not separately gated, since no day-0/1/2/3 op-for-op test exists in this file
(day 0 and day 1's own gates are `@pytest.mark.skip`d for an unrelated reason — tour shape, not ops).

### Per-test table

| Test | Verdict | Number / finding | Source |
|---|---|---|---|
| `test_a_carried_sell_row_never_offers_more_than_the_biggest_day_ever_asked` | **real gap** (untouched) | Hand-built harness, no tape reference at all. `sched[0]["sells"]={"MELON":5}` twice, shed holds 20; agent offers `SELL MELON 20` instead of capping the carry at 5. | Pre-existing bug in `schedule_agent.py`'s carry-cap logic, independent of the tape. Out of scope — `schedule_agent.py` is owned by another agent. |
| `test_a_hand_full_of_the_days_sell_row_walks_it_in_when_there_are_turns_to_spare` | **real gap** (untouched) | Hand-built harness (`_mid_tour_state`), no tape reference. Unit holding MELON 12 with 12 turns of slack and a 5-turn detour home emits `NORTH` instead of `EAST`/`SOUTH` — it never triggers `DELIVER_FERRY`. | Pre-existing bug in `schedule_agent.py`'s deliver-ferry trigger, independent of the tape. Out of scope. |
| `test_the_sells_row_is_a_day_total_not_a_per_turn_quota` | **re-derived, still a real gap** | Day 4 target changed `{WHEAT:28, FERTILIZER:4}` → `{WHEAT:49, FERTILIZER:6}`. Our agent currently delivers `{FERTILIZER:3, WHEAT:19}` — well under, not over. | Target: `data/seed_scripts/top_guys/90976060/schedule.json` key `"4"`, `sells` field; cross-checked against `tape_truth_90976060.log` ("day 4: {'WHEAT': 49, 'FERTILIZER': 6}"). Gap traced to `test_day_four_matches_seb_on_every_op_it_works`'s HARVEST/WATER shortfall — less produce exists to sell. |
| `test_the_feed_top_up_counts_wheat_already_standing_ripe_in_the_field` | **re-derived, now passes** | Day 4 target changed `bought == 0` → `bought == 1`. Our agent already buys exactly 1. | Target: `schedule.json` key `"4"`, `buys` field = `{WHEAT: 1}` (was `{}` under the old tape); cross-checked against `tape_truth_90976060.log` ("day 4: ... 'BUY_PRODUCT': 1"). |
| `test_day_four_matches_seb_on_every_op_it_works` | **real gap** (docstring corrected, assertion untouched — it's a structural diff, not a number) | `HARVEST 11/14`, `WATER 12/17`, `SELL 22/55` (ours/tape). Also corrected the false "days 0-3 already exact" premise — see above. | `data/logs/day_by_day_diff.log`, day 4 row. |
| `test_the_biggest_sale_takes_the_earliest_slot` | **re-derived (assertion dropped), now passes** | Kept the slot-order invariant (still passes unmodified). Dropped `dawn6 >= 860` — its premise (day 6 needs $854 for an $800 strawberry order) no longer exists: day 6's seed row is `{}` under `seb1326`. The tape's own dawn-day-6 bank, replayed, is **$0**; ours is $26 — already ahead of the tape on this metric, so there is no gap to threshold. | `schedule.json` key `"6"` (`seeds: {}`); `tape_truth_90976060.log` dawn bank table (`day 6: 0`). |
| `test_wheat_drawn_this_turn_is_the_herds_reserve_not_extra_to_it` | **deleted** | Day 5's row is `sells: {FERTILIZER: 5}` under `seb1326` — no WHEAT key at all, so the wheat-reserve race this test measured on day 5 doesn't occur. Our agent still sells 10 unrequested wheat that day, possibly the same carry-logic family as the first row of this table, but that's a different, unopened question. | `schedule.json` key `"5"`; `tape_truth_90976060.log` ("day 5: {'FERTILIZER': 5}"). |
| `test_day_six_gets_a_load_to_the_shed_early_enough_to_fund_the_strawberry` | **deleted** | Day 6 has neither `animals_bought` nor `seeds` under `seb1326` (both `{}`) — no $800 bill to fund by hour 2. Was `xfail(strict=True)`, had started silently XPASSing from an unrelated hour-0 FERTILIZER carryover sale, not from anything the test's routing narrative describes. | `schedule.json` key `"6"`. |
| `test_day_six_sells_the_wool_as_soon_as_the_walk_allows` | **deleted** | Same day-6 board change as above; the specific sheep-pen geometry (`(1,4)`/`(3,4)` vs tape's `(4,4)`/`(4,3)`) this test traced belongs to the old tape's day 6, which no longer exists in this shape. Also spuriously XPASSing for the same unrelated reason. | `schedule.json` key `"6"`. |
| `test_day_six_plants_every_tile_the_row_asks_for` | **re-derived, still a real gap** | Day 6 target changed `planted == 14` → `planted == 4`. Our agent plants 6 — **over**-planting, not the under-planting (stuck-seed-order) bug the old test caught. | Target: `schedule.json` key `"6"`, `plants` list (4 entries: `MELON, MELON, STRAWBERRY, MELON`); cross-checked against `tape_truth_90976060.log` ("day 6: ... 'PLANT': 4"). |
| `test_the_days_seed_is_bought_before_the_days_livestock` | **deleted** | Day 6 has neither `animals_bought` nor `seeds` under `seb1326` — the livestock-vs-seed funding race this test measured doesn't occur that day. The mechanism (HIRE/LAND/ANIMAL settle before SEED, so livestock takes the bank first) still exists in the code; days 9 and 11 both carry simultaneous `animals_bought` + `seeds` rows and could host a rebuilt version, but that needs a fresh hour-by-hour trace this pass did not do. | `schedule.json` keys `"6"`, `"9"`, `"11"`. |

### Result

72 tests collected (was 76; 4 deleted).
**5 failing, all real gaps, none newly discovered by this pass** — they were already-known
divergences that the repoint re-measured against the correct target instead of a stale one:

```
FAILED test_a_hand_full_of_the_days_sell_row_walks_it_in_when_there_are_turns_to_spare
FAILED test_a_carried_sell_row_never_offers_more_than_the_biggest_day_ever_asked
FAILED test_the_sells_row_is_a_day_total_not_a_per_turn_quota
FAILED test_day_four_matches_seb_on_every_op_it_works
FAILED test_day_six_plants_every_tile_the_row_asks_for
```

61 passed, 6 skipped (unrelated, pre-existing `@pytest.mark.skip`s on tour-shape gates).
Confirmed by deselecting the 5 known-red tests and re-running the rest clean.

None of the fixes moved a threshold to whatever the code currently produces — every changed number
traces to `schedule.json`'s own row for that day, cross-checked against a full replay of the tape's
own recorded actions against its real recorded opponent (`tape_truth_90976060.log`).

---

## 2026-08-10 — How Seb's planner works

Folded in from `docs/how_sebs_planner_works_2026-08-10.md`.

> **TARGET SUPERSEDED, added 2026-08-11.** Seb's tape was optimal under the OLD
> `townCenterSellInterval=12` economy. His own median bank halved ($137,747 -> $77,737) when the town
> rebalance landed and he has since withdrawn from the ladder (`docs/the_ladder_is_two_scripts.md`,
> measured from 2,744 ladder seats). The route-reconstruction findings below are still correct — the
> doc reads real recorded actions, not opinion — but the ladder now plants 108-147 WHEAT a season
> against our 24, and matching Seb's planner exactly no longer means matching the field.

Measured 2026-08-10 off the four tapes we hold, by reconstructing positions out of the recorded
observations and pairing each with the action emitted from it.
Not inferred from op counts — every claim below is a route.

### 1. The opening is open-loop, and it stops the day the shop speaks

Every farmer action and every hand action is **identical across all four tapes** for the first 96
turns:

```
  per-day agreement across all four tapes (turns of 24 with an identical unit action)
    d0  units 24/24   market 24/24
    d1  units 24/24   market 24/24
    d2  units 24/24   market 24/24
    d3  units 24/24   market 22/24
    d4  units  1/24   market 17/24
    d5  units  1/24   market 10/24
    d6+ units  0-1/24
```

Four different seeds (`1012428555`, `231975074`, `658760367`, `1440180345`), four different
opponents (Valmorlee, Pranshu Ghori, kakuteki, Leon Christians), both seats, and **both economies**
(`townCenterSellInterval` 12 and 24), all with `weedSpawnChance 0.005`.

Confirmed independently by replaying those 96 turns on seeds 11, 7, 123, 999 and 20260810: the
board and the crew size come out identical every time.

It stops at d3/d4 because `townShopUnlockInterval = 3` — d3 is the first day a shop unlocks
(`91422988` d3 opens with `shops ['ICE_CREAM_SHOP']`), and that is the first information the agent
has. Before it, there is nothing to plan against, so the opening is a constant.

The unit streams part at t97 (d4 h01), and the tape that parts first parts for one reason:
`90494364` has an **eighth hand** there. It is the richer `sellInterval 12` economy, so it could
afford one more hire, so the crew is a different size, so every route after it differs. The other
three stay identical for 121 turns — through d5 h00.

**So the only closed loop in the opening is `market -> money -> hire count -> crew size`, and the
crew size sizes the plan.**

### 2. A hand is given a role for the day, and it keeps it

Work ops only (moves and passes dropped), `91422988`:

```
  d11  u1  PURE crop  7/7    WATERx6 PLANTx1
       u6  PURE crop  9/9    WATERx6 PLANTx3
       u9  PURE crop  8/8    WATERx6 HARVESTx1 PLANTx1
       u11 PURE crop  9/9    WATERx6 PLANTx3
       u12 domi herd  8/10   CAREx3 COLLECT_FERTILIZERx3 FEEDx2 BUILD_PASTUREx1 PICKUPx1
       u3       herd  7/11   CAREx3 FEEDx2 COLLECT_FERTILIZERx2 PICKUPx1 BUILD_PASTUREx1 PLANTx1 WATERx1
       u8       haul  5/12   DROPx3 FEEDx3 PICKUPx2 HARVESTx2 CAREx1 COLLECT_FERTILIZERx1
```

Four roles, and the mixing is almost entirely *within* a role:

| role | ops | note |
|---|---|---|
| **waterer** | `WATER`, `PLANT`, `HARVEST` | never touches an animal |
| **feeder** | `PICKUP WHEAT` → `FEED` → `CARE` | the `PICKUP`/`DROP` is the wheat it carries, not a second job |
| **collector** | `CARE` → `COLLECT_FERTILIZER` → `DROP` | one round trip of the pens |
| **builder** | `BUILD_PASTURE`, `PLACE` | day 0 and land days |

`PICKUP`/`DROP`/`PLACE` on a herd hand are not a second assignment — they are the load that role
carries out and the fertilizer it carries back.

### 3. A hand owns a tile end to end, and a contiguous run of them

`PLANT` and `WATER` are emitted on **consecutive turns at the same position**, every time. The tile
is never revisited.

```
  d0  u6  spawn(4,5)  h03(3,4)PLANT[WHEAT] h04(3,4)WATER  h06(2,4)PLANT h07(2,4)WATER
                      h09(1,4)PLANT h10(1,4)WATER  h12(0,4)PLANT h13(0,4)WATER
                      h15(0,3)PLANT h16(0,3)WATER  h18(0,2)PLANT h19(0,2)WATER
```

That is a lawnmower sweep down the column `y=4` and along the row `x=0` — a contiguous block handed
to one hand at dawn, walked in order. Same shape on every crop hand:

```
  d0  u2  (4,1)MELON (4,0)WHEAT (2,0)WHEAT (0,0)WHEAT
  d0  u4  builds (4,3)(3,3)(3,2)(2,2) then plants (2,1)(1,1)(0,1)
  d0  u5  (3,1)MELON (3,0)WHEAT (1,0)WHEAT then builds (1,2)(2,3)
```

The farmer (`u0`) never leaves the shed's 3×3 on d0: `BUILD_PASTURE`, `PICKUP`, `PLACE`, `CARE`.

**This is the difference from ours.** We hold one global priority queue, every hand eligible for
every op, re-ranked at every stop. That is why a waterer gets pulled onto a critical feed and
`consecutive_unwatered` climbs: measured over a full season our agent loses **16 plants to thirst**
(14 strawberry, 2 melon), every one after d9, while losing exactly **one** animal.

### 4. He does not fill the turns, and that is deliberate

```
   day  crew  slots  turns  work  move  pass  idle-all-day  work%
     0     7      8    178    60    60    58             2  33.7%
     1     7      8    178    25    29   124             2  14.0%
     2     7      8    178    38    64    76             1  21.3%
     3     7      8    178    37    47    94             2  20.8%
     4     7      8    178    61    88    29             1  34.3%
     5     7      8    178    51    98    29             0  28.7%
    ...
    11    12     13    286   122   158     6             0  42.7%
    15    12     13    284   123   161     0             0  43.3%

  d0-d16 totals: work 1277 (32.7%)  move 1917 (49.1%)  pass 707 (18.1%)
```

Two hands stand still for the whole of d0 and d3. Day 1 is 124 PASS turns out of 178 — the crew
does 25 work ops all day, because everything planted on d0 was watered on d0 and
`consecutive_unwatered >= 2` means d1 can simply be skipped.

A hand that finishes its block idles. It is not reassigned.

### 5. Where the headroom is

- **707 idle turns over d0-d16**, 124 of them on d1 alone.
- **49.1% of all turns are walking.** Work is 32.7%.
- The early days are the loosest: d1-d3 run at 14-21% work against 40%+ from d11.

None of that is an argument that his plan is bad — it wins. It is an argument that the *ceiling*
above this plan is high, and that a planner built the same way (role per hand, contiguous block,
idle when done) has room to beat it without needing to be cleverer per turn.

### What this implies for our planner

1. Assign a **role** and a **contiguous block** to each hand at dawn. Do not re-rank globally.
2. Emit `PLANT`+`WATER` as one owned tile, not two independent jobs.
3. Let a hand idle when its block is done. Filling turns is what drags waterers onto feeds.
4. d0-d3 needs no board reading at all — it is a constant, and the crew size is the only output
   that matters to d4.
5. From d4 the input is the shop unlock and the bank: which animal is buyable, and whether the
   extra hire is affordable.

---

## 2026-08-10 — Fable: d4 sell shortfall and d9/d10 place 0/4

Folded in from `docs/fable_matching_the_tape_2026-08-10.md`.

> **TARGET SUPERSEDED, added 2026-08-11.** This doc matches the schedule against Seb's recorded
> tape, which was optimal under the OLD `townCenterSellInterval=12` economy. Seb's own median bank
> halved ($137,747 -> $77,737) when the town rebalance landed and he has since withdrawn from the
> ladder (`docs/the_ladder_is_two_scripts.md`, measured from 2,744 ladder seats). That doc says
> explicitly: "it is not the planner, the watering or the market logic; it is the target." The bugs
> found and fixed below are real bugs and still stand — read `the_ladder_is_two_scripts.md` before
> treating "matches the tape" as the goal. The field plants 108-147 WHEAT tiles a season; we plant 24.

Measured 2026-08-10.
Everything below is measured on `tape seb2988`, seed 11, `weeds 0.0`, module `schedule_agent`,
against `data/seed_scripts/top_guys/91422988.json` / `.../schedule.json`, on branch
`shaping-potential` at the tree as handed to Fable (uncommitted `docs/REGISTER.md` diff, plus
`scripts/diagnose_season.py` and `submission/main_replay11.py` untracked — neither touched).
Read-only throughout; no source file was changed.

Every measurement script is written to the session scratchpad
(`/private/tmp/claude-501/.../scratchpad/`) and its output is also saved under
`data/logs/fable_*.log` in this repo for anyone who wants the raw trace. Claims are flagged inline
as **measured** (run and read) versus **inferred** (read from the code and not independently
executed).

**Caveat, load-bearing: the working tree was being edited by someone else while Fable worked,
read-only, in the same directory.** `git status` at the end of the session shows uncommitted changes
to `kagg/search/cover.py`, `kagg/search/router.py`, `kagg/search/schedule_agent.py`,
`scripts/breakdown.py`, `tests/test_the_first_seven_days_match_the_plan.py` and `docs/REGISTER.md`
that Fable did not make (only `Write`/`Edit` on the report and on scratchpad files under
`/private/tmp/...`). File mtimes: `cover.py`, `router.py`, `breakdown.py`, `docs/REGISTER.md` and
the test file all predate the first tool call (Aug 9 22:27-Aug 10 08:06, session started ~09:27),
so everything quoted from those files is stable and was not moving under Fable.
**`kagg/search/schedule_agent.py` changed at 09:55:30, inside the session window**, and the
diff (`FEED_DAYS 2->1`, a new `WALK_THE_LOAD_HOME` flag, `CARE_WHAT_YOU_STAND_ON` False->True, a new
`day` parameter threaded into `_solve`) is squarely in the same territory as Q1/Q2 below — someone
else appears to have been actively working the d4 late-delivery/sell question at the same time.
Every line number cited was re-checked against the file as it stands now (all `grep`/`Read` calls
for exact line numbers were re-run after that edit landed) and the CONTENT at each cited location is
unchanged from what was traced against — only line numbers shifted from insertions earlier in the
file. But if this file moves again before anyone reads this, the line numbers below will drift
again; the constant names and the quoted code will not.

### Q1 — why does d4 sell only ~41 of 55 while Seb sells 55

**Measured. Not the order book, not the price curve, not "produce not in the shed."** It is our own
`DUSK_FEED_TOPUP` block re-buying wheat the sell block just sold, same turn, from hour 18 onward.

#### The baseline numbers

`python -u scripts/breakdown.py --module schedule_agent --tape seb2988 --days 7`
(full table in the session; the d4 column):

```
sell         41/55       buy_product   21/1
```

The schedule row for d4 (`data/seed_scripts/top_guys/91422988/schedule.json`, key `"4"`) is
`"sells": {"WHEAT": 49, "FERTILIZER": 6}` (= 55) and `"buys": {"WHEAT": 1}`. So the tape's `sell 55`
in the breakdown table is not an artifact of the tape column being degraded (per
`docs/the_tape_column_does_not_replay_his_game_2026-08-09.md`, folded in above) — it is corroborated
directly by the schedule row Seb's own tape produced it from, and 5+12+5+12+20+1 = 55 sums exactly
from his own recorded orders (below). This IS a real target.

#### Hour-by-hour, both sides, direct from `_process_market`

Script: `scratchpad/d4_trace.py` (this file was subsequently overwritten by something else in the
scratchpad between the run and now — the log at `data/logs/fable_d4_trace.log` is the surviving
record of the run and is what the numbers below are read from).

**HIS d4** (tape replayed both seats, `data/logs/fable_d4_trace.log`):

```
d4h18  shed WHEAT=1        orders=[SELL WHEAT 5]              -> FILLED SELL 5
d4h21  shed WHEAT=7        orders=[SELL FERTILIZER 5, SELL WHEAT 12, BUY_LAND]  -> FILLED SELL 17
d4h22  shed WHEAT=7        orders=[SELL WHEAT 12]              -> FILLED SELL 12
d4h23  shed WHEAT=7        orders=[SELL WHEAT 20, SELL FERTILIZER 1]  -> FILLED SELL 21
```
WHEAT sold: 5+12+12+20 = 49. FERTILIZER: 5+1 = 6. Total 55, exact match to the schedule row.
**No BUY_PRODUCT after h2.** He sells everything from h18 on and does not rebuy that day.

**OURS d4** (`schedule_agent` seat 0 vs the same tape opponent, same log):

```
d4h14  SELL WHEAT 8                      -> FILLED SELL 8
d4h17  SELL WHEAT 8, SELL FERTILIZER 1   -> FILLED SELL 9
d4h18  BUY_PRODUCT WHEAT 6               -> FILLED BUY_PRODUCT 6
d4h19  SELL WHEAT 6, BUY_PRODUCT WHEAT 1 -> FILLED SELL 6, FILLED BUY_PRODUCT 1
d4h20  SELL WHEAT 8                      -> FILLED SELL 8
d4h21  BUY_PRODUCT WHEAT 6               -> FILLED BUY_PRODUCT 6
d4h22  SELL WHEAT 6, BUY_PRODUCT WHEAT 1 -> FILLED SELL 6, FILLED BUY_PRODUCT 1
d4h23  SELL WHEAT 1, BUY_PRODUCT WHEAT 6 -> FILLED SELL 1, FILLED BUY_PRODUCT 6
```
WHEAT sold: 2(h0)+8+8+6+8+6+1 = 39, FERTILIZER 1+1 = 2, total **41** — matches the breakdown row
exactly. BUY_PRODUCT WHEAT total: 1(h1)+6+1+6+1+6 = **21** — also matches the breakdown row
(`buy_product 21/1`) exactly.

#### The mechanism, proved from the code

From hour 18 on, every turn we both sell wheat AND buy it straight back, in that order, inside the
*same* turn. That is not a coincidence of two independent blocks firing near each other — it is
`DUSK_FEED_TOPUP` (`kagg/search/schedule_agent.py:3606-3634`), re-evaluated every turn:

```python
if (DUSK_FEED_TOPUP and day >= DUSK_FROM_DAY and hour >= DUSK_FEED_HOUR
        and len(orders) < 9):
    arriving = len((sched.get(day + 1, {}) or {}).get("places") or [])
    gap = (alive + arriving) - int(shed.get("WHEAT", 0))
    gap = min(gap, FEED_TURN_CAP, int(money // quote))
    if gap > 0:
        orders.append(["BUY_PRODUCT", "WHEAT", gap])
```

`DUSK_FEED_HOUR = 18`, `DUSK_FROM_DAY = 2` (`:576`, `:580`), `FEED_TURN_CAP = 6` (`:546`). On d4,
`alive` = 7 (cow 5 + sheep 2, matching the end-of-day herd row), d5's schedule row has `"places": []`
so `arriving = 0`. `gap = 7 - shed["WHEAT"]`, evaluated fresh every hour from h18. The SELL order is
appended earlier in the same turn's order list (the day's plan block, before this feed block runs),
so within one turn slot-processing order (`_process_market`, `reference/kaggriculture.py:550`,
`for i in range(max_len)` walks order *slots* — SELL is slot 0, BUY_PRODUCT a later slot — so SELL
settles completely before BUY_PRODUCT is even quoted, `reference/kaggriculture.py:570-613`): the
sell drains the shed toward zero, then the SAME turn's dusk topup sees `shed=0`, computes
`gap=7`, caps at `FEED_TURN_CAP=6`, and buys 6 straight back. h18: buy 6. Next turn (h19) the sell
block sells 6 of it right back down (plus whatever fresh harvest lands), gap recomputes to 1, and a
1-unit topup fires again. This repeats at h21-h23. **Every `BUY_PRODUCT` this measurement logged for
d4 lands in exactly this window (h18, h19, h21, h22, h23)** — five of the six buy events — plus one
feed-drip buy at h1 from a separate block (`:3566-3604`).

The sell block itself already tries to hold back a feed reserve before offering wheat
(`:2909-2933`):

```python
have = max(0, have - max(0, feed_days(day) * alive - carried_wheat - drawn - will_buy))
```

`feed_days(day) * alive` = `1 * 7` = 7 for d4 — the **same** floor `DUSK_FEED_TOPUP` targets. But
the sell-side reserve nets off `carried_wheat` (wheat currently in a hand) and `will_buy`
(this-turn commitments), while `DUSK_FEED_TOPUP`'s own comment (`:3610-3615`) argues the opposite —
that hand-carried wheat should *not* count, because it may be drawn for a pen before the overnight
rollover ever returns it to the shed, and its own change note there records exactly this failure
mode ("d4 we harvest 14 wheat, it is still in hands at h18, and the top-up ordered 21 units against
a tape that buys 1"). Two blocks target the identical number (7 = `alive`) from two different bases,
each one blind to what the other has already reserved, and the result is the sell-then-rebuy churn
above.

**Not the order book / slot mechanics.** Every turn in the trace carries 1-2 market orders, nowhere
close to `maxMarketOrdersPerTurn = 10` (`reference/kaggriculture.py:538`) or the `len(orders) < 9`
gate on the topup itself. Ruled out by direct count, not inferred.

**Not "produce not in the shed."** Both sides show the identical mechanism: shed reads 0 or low
*before* the turn (dawn snapshot), and a SELL for 5-8 units still fills, because the unit phase
(HARVEST + DROP) runs before the market phase *within the same turn*
(`reference/kaggriculture.py:922` then `:928`, restated in the matching-the-tape skill) and refills
the shed in time for that turn's SELL to clear. This is true for us exactly as it is true for him —
harvest counts match 14/14 on d4 in the breakdown table. The gap is not delivery timing.

#### End-of-day wheat is 0/0 both sides

The breakdown table's d4 `wheat` row reads `0/0` — neither side is left holding stranded wheat. The
14-unit shortfall (55 sold vs 41) is wheat that got bought back and then fed to animals rather than
sold, not wheat that vanished. So the cost of this defect is not a stranded-goods loss; it is the
**spread**, paid twice on roughly 20 units a day from h18 on — sell low, buy back higher, repeat —
plus every one of those round trips occupies an order slot and a market-lockstep iteration that buys
nothing. Money at d4 end: 774/1063 (ours/tape), a ~$289 gap, consistent with a repeated wash trade
though the exact split of that gap between this mechanism and everything else that differs by dusk
was not isolated. **Money is downstream evidence here, not the target** — the target is the op
count, and `sell 41/55`, `buy_product 21/1` are both directly this mechanism.

### Q2 — is the fix to match the WORK ORDER (harvest early, deliver, sell in bursts), not the sell block

**Measured evidence says no, reordering harvest/delivery would not close this gap.**

- HARVEST counts already match exactly, d4: `harvest 14/14` (breakdown table).
- Wheat already reaches the shed in the same turn a SELL clears it, on both sides — proven directly
  above (his h18 sells 5 against a *pre-turn* shed reading of 1; ours sells 8 at h14 against a
  pre-turn reading of 0). The intra-turn unit-phase-then-market-phase ordering already gets the
  produce to market the same hour it is picked up, for both agents. There is no late-delivery gap to
  close by resequencing work.
- The defect measured above is entirely on the **market-order side**: a feed-reserve rule computed
  twice, on two different bases, competing with the sell block from h18 onward. Reordering *what the
  crew does on the tiles* does not touch either of those two blocks — they run in the market-order
  construction, independent of tour order.

So this is squarely in "tune the sell/buy interaction," not "match the day's work order." No fix
was designed or tested (out of scope, read-only), but the shape one would need is: make
`DUSK_FEED_TOPUP`'s floor agree with what the sell-side reserve (`:2909-2933`) already believes is
reserved, rather than two independent computations of the same `feed_days(day) * alive` quantity.

### Q3 — why cover leaves 8 of 10 d9 placements unassigned, and why the 2 it does route emit nothing

**Measured, in three layers, and they chain into one cause.** `place` reads `0/4` on both d9 and
d10 (breakdown table). This is not a turn-budget problem — d9 measured 277 unit-turns of budget
against 155 used by other work, i.e. 122 turns free (`scratchpad/d9_place_trace.py`,
`data/logs/fable_d9_place_trace.log`).

#### Layer 1 — all 10 open pens are typed "PLACE COW", none "PLACE SHEEP"

Instrumented `cover.cover()` directly for the day-9 dawn solve (monkeypatch, not inference):

```
total jobs offered=53   PLACE jobs among them=10
  PLACE job: tile=(4,1) ops=[('PLACE','COW'),('FEED','WHEAT'),('CARE',None)] ...
  ... (all 10, every one COW) ...
supply given to cover()={..., 'COW': 2, 'SHEEP': 2, ...}
PLACE jobs routed: 2 / 10
```
(`data/logs/fable_d9_place_trace.log`). The schedule's own d9 row asks for `['COW','COW','SHEEP',
'SHEEP']` — two of each — but **zero of the ten offered nodes are typed SHEEP**. This comes from
`router.build_nodes`'s PASTURE/COOP tie-break (`kagg/search/router.py:836-865`): an open pen with no
specific reservation (`pen_for`) iterates `R.ANIMAL_NAMES = ["GOOSE","COW","SHEEP"]` and takes the
first species with nonzero shed/supply, which is COW whenever both are present — a behaviour the
code's own comment (`:836-850`) already documents as measured and accepted in isolation. Combined
with `cover()`'s supply gate (`affordable()`, `kagg/search/cover.py:812-816`, `stock[COW] = 2` from
`plan_supply`), only 2 of the 10 identically-typed COW claims can ever be affordable — **not because
turns are scarce, but because the model believes only 2 COWs exist and none of the ten nodes is
typed as the SHEEP that will actually be available.**

#### Layer 2 — the animals the model expects were never bought

`plan_supply` (`schedule_agent.py:1562-1568`) credits `sched[day]["animals_bought"]` — the
**schedule's** row, `{COW:2, SHEEP:2}` on d9 — into the dawn plan's supply, under
`PLAN_TODAYS_PURCHASES = True` (`:260`). But the actual `BUY_ANIMAL` orders our agent emits are
decided by a separate, later block, `SHOP_ADAPT_HERD` (`:2067`, on from `SHOP_ADAPT_FROM_DAY = 6`,
`:2088` — active on both d9 and d10), which re-derives the COW/SHEEP split from live market headroom
(shop unlocks, remaining town drain for MILK vs WOOL) rather than reading the schedule's per-day
species mix (`:3317-3404`). Measured directly, both days:

```
d9h 0  BUY_ANIMAL SHEEP 1     d9h7  BUY_ANIMAL SHEEP 1, SHEEP 1     d9h12 BUY_ANIMAL SHEEP 1
d10h0  BUY_ANIMAL SHEEP 1, SHEEP 1     d10h16  BUY_ANIMAL SHEEP 1, SHEEP 1
```
(`data/logs/fable_d9_shed_cow.log`, `fable_d10_shed_cow.log`). **Zero `BUY_ANIMAL COW` orders fire
on either day.** Shed `COW` reads 0 every single hour of d9 (`data/logs/fable_d9_shed_cow.log`,
every printed row). `buy_animal` fills still read 4/4 both days in the breakdown table because the
*count* matches Seb's — only the *species* differs, exactly what `SHOP_ADAPT_HERD`'s own docstring
says it is designed to do ("The COUNT the schedule asks for is kept exactly; only the species is
re-decided," `:3317-3318`). This is a known, already-flagged feature
(`docs/REGISTER.md` OPEN-CLI: "Shop-adaptive herd shipped and measured; floors still open") — what
this adds is the specific causal link from it to `place 0/4`.

So the dawn plan is built against a purchase that never happens: 10 pens get typed and routed on the
assumption of 2 COWs arriving; 0 COWs ever arrive; the 4 SHEEP that *do* arrive all day are never
offered as a placement target at all, because no node was ever typed SHEEP.

#### Layer 3 — the 2 routed jobs draw against an empty shed and are abandoned, silently

The 2 jobs `cover()` *does* route are planned correctly at the routing layer — instrumented
`_solve()`'s materialised route directly (`scratchpad/d9_solve_trace.py`,
`data/logs/fable_d9_solve_trace.log`):

```
LOCAL unit 1  start=(5,4)
    Shed(5,4)[COWx1+WHEATx2]
    Job(5,4)['PLACE','FEED','CARE']  needs=Counter({'COW': 1, 'WHEAT': 1})
    Job(4,4)['FEED','CARE','COLLECT_FERTILIZER','HARVEST']
    Shed(4,4)[DROP]
```

This route correctly asks for a COW at the first depot stop. But cross-referenced against the
turn-by-turn execution trace at the same tile (`data/logs/fable_d9_place_execute_trace.log`), the
unit that actually stands at `(5,4)` at hour 1 emits `PICKUP WHEAT 2` and never once picks up a COW
— and a season-wide scan of every hand on d9 (`data/logs/fable_d9_all_units_trace.log`) confirms
**COW and SHEEP never enter any hand's inventory, and PLACE never fires, at any point on d9**, even
though real SHEEP are sitting in the shed by hour 1. The COW half of the depot draw fails because
the shed genuinely never holds a COW (Layer 2), and the executor does not retry or reroute around a
failed draw unless the job is `critical` — `Depot.critical` is set only when `at_risk and required`
(`cover.py:330-335`, `:585-587`); the PLACE job here is `required=True` (it bundles a `FEED`) but
`at_risk=False`, so `critical=False`, and per the documented executor behaviour the stop is one "not
worth standing at and retrying... worth walking away from." Combined with "the day is planned once,
no replan" (project-wide rule, and this file's own comments at `:1601-1630`), the fixed route never
revisits `build_nodes` later in the day even though the shed does fill with SHEEP — so the 4 real
animals purchased that day are never routed to a pen either.

**Net chain:** `SHOP_ADAPT_HERD` buys the wrong species (by design, reading only live market
headroom) → `plan_supply` and `build_nodes`'s tie-break still assume the schedule's species mix, so
every open pen is typed for the species that will not arrive → `cover()`'s supply gate caps routing
at the phantom count → the 2 it does route chase a COW that is never in the shed and get silently
abandoned, non-critical → 0 PLACE ops fire, 8 of 10 jobs are never even attempted, and the 4 real
SHEEP purchased that day are stranded with no node ever typed to receive them.

### What was not verified in this pass

- The "101 idle unit-turns" figure quoted elsewhere was not independently re-derived — this pass's
  own instrumentation measured **122** idle turns on d9 (277 budget − 155 used before any closing
  trips), a different number in the same direction (large free capacity, ruling out a turn-budget
  explanation). The two figures were not reconciled; both support the same conclusion.
- Whether `SHOP_ADAPT_HERD`'s species reallocation is itself a good idea in aggregate (REGISTER
  already logs it as shipped-and-measured, floors still open) was not assessed — only that it is
  the direct, provable cause of `place 0/4` on d9 and d10 via the plan/purchase mismatch above.
- Neither Q1 nor Q3 got a fix or a test, per the read-only instruction. The mechanism for each is
  pinned to specific line numbers above so a fix can be scoped without re-deriving this.
- The d4 hour-by-hour trace script (`scratchpad/d4_trace.py`) was overwritten by something else in
  the scratchpad after it ran; the numbers quoted above come from the saved log
  (`data/logs/fable_d4_trace.log`), not a re-run against the current file on disk.

---

## 2026-08-11 — Fable: the d4/d5 planner chain — the spawn-ring step deletes the depot draw

Folded in from `docs/fable_the_d4_d5_planner_2026-08-11.md`.

Fable, 2026-08-11.
Worktree `agent-abcebcdbb11b26b7e`, detached at `f847e7d` ("Day zero matches"), plus the two experimental edits described below (uncommitted, in `kagg/search/schedule_agent.py`).
Everything here is measured on seed 11, Victor tape, `townCenterSellInterval 24`, `weeds 0.0`, via `python -u scripts/breakdown.py --module schedule_agent --tape victor --days 12`.

### Verdict in one paragraph

The cost model is right and the executor is wrong.
u0's d4 tour is costed at 21 turns against a budget of 24 and that plan is achievable.
The executor spends 27, because `acts[0] = [step_off]` (line ~2777) overwrites the farmer's hour-0 action AFTER `_router_acts` has already walked the route for that hour — and on d4 that hour's action was `PICKUP WHEAT 2`, which the walk had already CONSUMED from the route state (`node.pick` emptied at `:1837-1841`, the local `shed` counter decremented).
The route then believes wheat is in hand that was never drawn.
Six unpriced turns follow — 2 for the step-off round trip, 4 for the recovery — and the tour's tail stop `(0,4)[WATER, HARVEST]` is 3 turns out of reach.
That one dropped stop is `water 14/15` and `harvest 4/5` on d4; the un-freed tile is d5's `plant 4/5` and `strawb 6/7` (confirming Alex's own dawn instrumentation: d5 needs six tiles and has five).
Deferring the walk instead of deleting the draw fixes d4 and d5 exactly and moves the first divergence to d6.

### 1. The traced mechanism (d4, hour by hour)

Full trace: `data/logs/fable_trace_d4.log` (route state, computed act, and emitted act per hour).
The plan: `Shed(4,4)[pick WHEAT 2] -> (2,4)[FEED,CARE,COLLECT] -> (3,4)[FEED,CARE,COLLECT] -> (1,4)[WATER] -> (2,3)[WATER] -> (0,4)[WATER,HARVEST]`, cost 21, budget 24.

```
    h00  (4,4)  computed PICKUP WHEAT 2 -- route consumes it (pick={}), shed 6->4 locally
                EMITTED NORTH (the overwrite).  Wheat never drawn; route thinks it was.
    h01  (4,3)  SOUTH -- walking back to the depot stop it believes is exhausted
    h02  (4,4)  depot pick empty -> stop POPPED -> WEST.  Standing ON the shed, draws nothing.
    h03-h04     WEST WEST to (2,4); COLLECT_FERTILIZER (planned)
    h05         `_live_ops` offered no FEED (no wheat in inventory);
                `FETCH_THE_FEED_AND_RETURN` inserts an UNPLANNED depot stop: EAST
    h06-h07     EAST; PICKUP WHEAT 2 at the shed -- the planned draw, taken 7 hours late
    h08-h09     WEST WEST back to (2,4)
    h10-h15     FEED CARE (2,4), EAST, FEED CARE COLLECT (3,4)
    h16-h21     the tour continues: WATER (1,4), WATER (2,3)
    h22-h23     SOUTH, WEST -- still 1 move + WATER + HARVEST short of (0,4) when the day ends
```

Waste, quantified: 2 turns (h00 step off + h01 walk back, never budgeted) + 4 turns (h05, h06, h08, h09 — the fetch round trip that exists only because of the phantom draw).
21 + 6 = 27 > 24, over by 3, which is exactly the walk+work remaining to `(0,4)` at midnight.

So, to Alex's direct question: the model under-charges only the 2 step-off turns; the other 4 are the executor wasting turns the model correctly never priced, because the work they redo was already done on paper at h00.

### 2. Where else it fires

The overwrite only matters when the farmer's h0 computed action MUTATES state.
A computed MOVE or PASS overwritten by the step costs nothing (the route was not touched).
Traced d0-d6 (`data/logs/fable_trace_d0_d5.log`, `fable_trace_d6_defer.log`):

```
    d0  h0 computed PASS  (WAIT_FOR_THE_MORNING_DELIVERY; shed empty)   no overwrite fired
    d1  h0 computed WEST                                                 no overwrite fired
    d2  h0 computed PASS                                                 no overwrite fired
    d3  h0 computed PICKUP WHEAT 2 -> OVERWRITTEN   6 wasted turns, absorbed by slack (only `pass` moves)
    d4  h0 computed PICKUP WHEAT 2 -> OVERWRITTEN   tail dropped: water 14/15, harvest 4/5
    d5  h0 computed PICKUP WHEAT 3 -> OVERWRITTEN   a water lost: 8/9
    d6  step_off is None all day (farmer works a clean 24-turn tour)
```

`step_off` can only ever fire at hour 0: `_hires_this_turn` returns 0 for `hour != 0`, so `_clear_the_spawn_ring` gets `n=0`, `lost=0`, and returns `None` on every later hour.

### 3. The fix that keeps BOTH the step and the draw: defer, don't delete

Alex's suspicion was right: the fix lives in how the route advances when the emitted action is overridden, not in the overwrite itself.
Delta 1 (`hold_farmer`): when the call site is going to overwrite the farmer's action, `_router_acts` must not walk u0's route at all that turn — emit a placeholder, leave the depot stop unconsumed.
The tour then starts one turn late instead of one stop short: the farmer steps NORTH at h00, walks back at h01, takes the REAL pickup at h02, and the whole tour fits (21 + 2 = 23 ≤ 24).

Why the two reverted attempts had to lose, for the record:

- Removing the step-off entirely re-ran the spawn rotation: on d3-d5 the farmer's h0 act is a PICKUP that keeps it ON `(4,4)` as the hires settle, so a second hand lands on the dead `(5,5)` corner and idles 23 turns (`_clear_the_spawn_ring`'s own measured table). d3 `water 4/9` is that hand's whole route, gone.
- "Only overwrite a MOVE" is the same change wearing a guard: on exactly the days the bug fires (d3-d5, PICKUP days), the guard suppresses the step, which is the removal case above. That is why it left d4 `harvest 4/5` untouched AND wrecked d3.

Delta 2 (`farmer_start`): additionally cut u0's tour from the tile the step lands on, one turn poorer, so the plan charges the step.
Measured on top of delta 1: byte-identical grid except d4 `pass 2 -> 1` (one idle turn becomes a move; both exempt rows).
A near-null here — the trigger (a farmer tour planned tighter than 22) never occurs on this tape — but it is the honest cost model and the insurance against a tight day.
Alex's call whether it stays; the project's revert-a-null rule argues against, the plan-once doctrine ("crew arrival is planned for, not discovered") argues for.

Both edits are in the worktree, flagged as EXPERIMENT with Fable's name on them.
Test: `tests/test_the_spawn_step_defers_the_depot_draw.py` — red at `f847e7d` (`d4 water 14/15 -- the tour tail was dropped`), green with delta 1, verified in both directions.

### 4. The grid, before and after

Baseline (`f847e7d`, `data/logs/fable_baseline_grid.log`) — first non-exempt op divergences: d1 `care 0/5`, then d4:

```
    plant               10/10  0/0  0/0  4/4  5/5  4/5  1/1   9/14  11/10   6/1  17/23  13/11
    water               10/10  0/0 10/10 9/9 14/15  8/9 12/12 26/33  22/22 27/28 36/43  45/41
    harvest              0/0   0/0  0/0  0/0  4/5   0/0  4/4   1/1    6/6   5/5   4/6    4/4
    strawb (board)       0/0   0/0  0/0  3/3  3/3   6/7  7/8  14/18  16/20 20/20 31/31  32/36
    weeds                0/0 throughout
```

With the fix (`data/logs/fable_defer_plus_charge_grid.log`, reproduced by the final tree in `fable_final_grid.log`):

```
    plant               10/10  0/0  0/0  4/4  5/5  5/5  0/1  15/14   7/10   3/1  15/23  17/11
    water               10/10  0/0 10/10 9/9 15/15  9/9 11/12 33/33  17/22 29/28 31/43  47/41
    harvest              0/0   0/0  0/0  0/0  5/5   0/0  4/4   1/1    6/6   5/5   5/6    4/4
    strawb (board)       0/0   0/0  0/0  3/3  3/3   7/7  7/8  17/18  17/20 17/20 29/31  30/36
    weeds                0/0   0/0  0/0  0/0  0/0   0/0  0/0   1/0    1/0   2/0   2/0    3/0
```

d4 and d5 now match on every non-exempt row except d5 `dig 0/1` and the sell shortfall that predates the fix (d5 `sell 15/22`, baseline 14/22).
On the d5 dig: Victor's tape digs on d5/d7/d11 as unconditional open-loop script actions; our fixed board has no weed on d5, so there is nothing to dig and `0/1` is the honest state.
Baseline's `1/1` was our agent digging SOMETHING on its own diverged board — not traced further, and should not be read as a matched behaviour.

The stale Seb gates (`test_each_day_matches_the_tape.py` 6F/1P, `test_the_first_seven_days_match_the_plan.py` 7F/7P/1x — both still target tape `90494364`) fail IDENTICALLY with the fix on and off.
No pinned test regresses.

### 5. The new frontier: d6, and the weeds

The fix moves the first divergence (after d1 `care 0/5`, see §7) from d4 to d6, and d6 was never clean: baseline already had `build 0/2`, `place 0/1`, `pens 6/8`, `cow 2/3`, `buy_seed 1/4` there.
Under the fix d6 also slips `water 12->11 (/12)` and `plant 1->0 (/1)`, because d5 now ends with the NW quadrant FULL (19 crops + 6 pens = 25/25; baseline had 24) — the tape's own board is identical, so this is ground Victor handles and we do not.
The step-off is NOT involved: it never fires on d6, and the farmer's d6 tour executes cleanly to h23 (`data/logs/fable_trace_d6_defer.log`).
d6's `idle 42/5` with uncovered work on the board says plan gap, not executor waste — a separate investigation.

**The weeds are a latent router defect the fix made reachable, with a measured mechanism.**
`reference/kaggriculture.py:209`: a new plant is created with `consecutive_unwatered: 1` — "planting day counts as unwatered".
The nightly refresh (`:766-771`) increments and weeds at 2.
So ANY plant not watered the same day becomes a weed that night, seed burned, dig owed.
Measured: tile `(5,3)` went `LOCKED -> None (d6 h13, the parcel purchase) -> WEED (d7 h23)` without ever being sampled as a plant (`data/logs/fable_trace_cell53.log`) — one of d7's 15 plants landed in the day's FINAL hour and was weeded by the same step's refresh.
The router pairs a pinned PLANT with its WATER (`PLANT_THEN_WATER`) but prices the water as a prize, not a co-requisite, and nothing forbids a PLANT so late it cannot be watered.
Baseline never tripped this only because its d7 planted fewer (9 vs 15).
The rule to encode, when this is picked up: a PLANT whose same-day WATER cannot also be executed is worth LESS than nothing — it converts a seed into a weed.

### 6. The retracted replant line — why attempt 3 could not have worked (code-read, not measured)

Alex retracted "replant the tile you just harvested", so Fable did not re-run those attempts; but the code answers why attempt 3 failed even with `HARVEST_THEN_PLANT` in `build_nodes`.
The pinned-tile gate exists in TWO places:

- `router.build_nodes:956`: `if tile in pinned or not isinstance(cell, dict): continue` — the planner side that was patched.
- `_live_ops:1349-1352` (`schedule_agent.py`): a pinned tile whose cell is not `None` returns `[]` — the EXECUTOR side.

The route is a visit order and `_live_ops` re-derives the work at each stop, so even a correctly emitted HARVEST+PLANT node on a pinned occupied tile is dropped silently at execution.
Any future variant of this idea must patch both, or it is deleted at the second gate it never saw.

### 7. Loose ends, stated so they are not lost

- **d1 `care 0/5` is an op divergence EARLIER than d4** and was absent from the working summary.
  The tape cares its 5 animals on d1 while feeding none; we do neither.
  Present at baseline and unchanged by this fix.
  By the days-match-in-order rule it is technically the first open day.
- d5 `sell 15/22` (baseline 14/22) and the money drift from d5 on predate the fix and are the sell chain, not this chain.
- Delta 2's cost model charges 1 turn (plan cut from the stepped tile); the true round trip is 2 when the tour's first stop is the shed itself.
  If a future day plans the farmer at exactly 23, this halves the safety margin — worth revisiting if a tail ever drops again on a step-off day.

### Artifacts

- Experimental edits: `kagg/search/schedule_agent.py` (uncommitted; `hold_farmer` + `farmer_start`, both flagged EXPERIMENT).
- Test: `tests/test_the_spawn_step_defers_the_depot_draw.py` (red on `f847e7d`, green with delta 1).
- Logs: `data/logs/fable_baseline_grid.log`, `fable_defer_grid.log` (delta 1 alone), `fable_defer_plus_charge_grid.log` (delta 1+2), `fable_final_grid.log` (byte-identical to the previous — the tree reproduces its own measurement), `fable_trace_d4.log`, `fable_trace_d0_d5.log`, `fable_trace_d6_defer.log`, `fable_trace_weed.log`, `fable_trace_cell53.log`.

---

## 2026-08-12 — The board is fixed, so the route can be solved offline

Folded in from `docs/the_route_is_precomputable_2026-08-12.md`.

Alex's point, 2026-08-12, and it is correct: **the map is the same in every game.**
This had been argued around for two sessions on the assumption that a day's routing depends on the
seed and the opponent. It does not.

### The proof is two functions

```python
def _initial_tile(x, y, board_size):
    return None if _quadrant_of(x, y, board_size) == "NW" else "LOCKED"
```

A pure function of coordinates. `_default_spawn` is deterministic too.
**There is exactly one RNG in `kaggriculture.py`** — `random.Random((seed * 1_000_003) ^ day)` at
line 858 — and it is used for precisely two things: the shop unlock draw and `_spawn_weeds`.

So the geometry, the depots, the shed-access tiles and every walking distance are identical in every
game ever played. The seed changes what is worth SELLING and where weeds appear; it does not change
where anyone walks. The opponent touches our *money*, not our map.

**Therefore a route solved once is reusable**, and the 1s/turn `actTimeout` stops being a constraint
on route quality — solve it offline with hours, ship the answer. This is also what the top players
are recorded as doing (`project_kaggriculture_open_loop`: fixed 720-turn scripts, deterministic
combinatorial scheduling).

The one real caveat is **weeds**: the ladder runs `weedSpawnChance` at the default 0.005, so a
handful of tiles a season turn to weed at random and add a job the precomputed plan did not expect.
That is a local-repair problem, not a structural one. Our own grids run 0.0.

### `scripts/solve_day_offline.py`

Takes a captured day fixture and runs `cover.py`'s **own** `cover()` — the same `slot`/`cost`/
`materialise` the shipped planner uses — with the LNS deadline raised and multiple restarts. A route
it reports as feasible is feasible under the real cost model, not a second model of the game that
might be optimistic about distances.

```
python -u scripts/solve_day_offline.py tests/fixtures/lns_day_12_seed11_victor.json \
    --seconds 5 --restarts 2
```

### What it found

**d12 is a real defect, now proven.**

```
  shipped planner (greedy, no LNS):   48/49 covered
      LEFT (9,1) [WATER, HARVEST, PLANT]  at_risk=False required=False
  offline:                            49/49 covered, 5s, both restarts independently
  per-unit turns: 14-21 against a budget of 24 -- slack on EVERY hand
```

The day is not full. It is an assignment failure.

**d18 is NOT a defect. The shipped planner already covers 66/66 and leaves nothing.**
The previously reported "66 of a proven 67" does not reproduce from the saved fixture, which
contains 66 jobs in total. That lead is closed; do not re-open it on the old claim.

**The existing ruin-and-recreate code already solves d12 — at 5 seconds.**
It fails at the `RUIN_AND_RECREATE_SECONDS = 0.25` it is allowed in-game. So the mechanism is
right and the budget is what is wrong, which is exactly the case for precomputing rather than for
making the greedy cleverer. At 0.25s in a full season it measured slightly WORSE than off
(work 1591 vs 1613 over 20 days), so it must not be shipped at its current budget.

### The reason to keep expectations low: capacity is not the binding constraint

Measured on the d0-d19 grid, seed 11, tape victor:

```
  days 0-19 totals    ours    tape
  work                1,613   1,556      we work MORE
  move                1,646   1,536      we move MORE
  idle                  539     692      we idle LESS
  money at d19       26,105  27,133      we bank LESS
```

We spend 57 more work turns and 110 more move turns than Victor and finish $1,028 behind.
He idles 153 turns more than us and wins anyway.

**Freeing more turns gives us more of the thing we already have a surplus of.** If 692 idle turns do
not stop him winning, our 539 are not what is stopping us. This caps how far the routing work can
compound, and it points at the *mix* rather than the *count* — consistent with the op ranking already
in CLAUDE.md, where FEED (+0.452), CARE (+0.441) and harvest/plant (+0.439) predict money while
PLANT (-0.358) and WATER (-0.276) predict less of it.

Before generalising the offline solve to all 30 days, measure the ceiling: run the season with a
long per-day deadline and see whether the money moves at all.

---

## 2026-08-12 — Spawn-ring misprediction: every hand is routed from a tile it does not wake on

Folded in from `docs/spawn_ring_misprediction_2026-08-12.md`.

2026-08-12, seed 11, tape `victor`.
Found while chasing why `(1, 2)` weeds at the end of d11 and costs `strawb 35/36` for the rest of the season.

### The finding

`_end_of_day` discharges the whole crew — `farm["hands"] = []` (`kaggriculture.py:867`).
Every hand is therefore a fresh `_spawn_hand` every morning, and the dawn plan can only *predict* where they land.

`_arrivals` (`schedule_agent.py:343`) is that prediction: least-occupied shed-access tile, ties in NWSE ring order `[(4,4), (5,4), (4,5), (5,5)]`, counting `[farmer] + hands` at the moment the HIRE settles.

The hires settle in the **market** phase, which runs **after** the unit phase (`kaggriculture.py:922` then `:928`).
So the ring the hires see is the ring *after* the farmer has taken its hour-0 action.

`_clear_the_spawn_ring` knows this, and handles the case where the farmer is stepped off **deliberately** — but it only steps off when the step saves a hand from the dead `(5,5)` corner.
Once the board is fully unlocked nothing is dead, so it returns `step_off=None` and predicts the ring with the farmer still on `(4,4)`.
The farmer's own routed tour then walks it off `(4,4)` at hour 0 anyway.

`(4,4)` reads empty when hire 1 settles, and **every hand of the day lands one ring slot early**:

```
    d11, seed 11, 11 units
      predicted  (5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5)
      actual     (4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5) (4,4) (5,4)
```

The prediction and the farmer's hour-0 move are **two separate decisions that disagree**.

### What it cost, exactly

u10 on d11, priced at 23 turns against a budget of 23 — zero slack:

```
    PLANNED   start (4,5)
      (4,5) PLANT                       2 turns
      (7,3) WATER HARVEST PLANT   5 mv + 4 = 9
      (6,2) WATER HARVEST PLANT   2 mv + 4 = 6
      (1,2) WATER                 5 mv + 1 = 6
                                        -- 23, fits to the turn

    ACTUAL    woke on (5,4), two turns away
      h01 WEST  h02 SOUTH   <- the two turns
      h03 (4,5) PLANT/WATER ... h19 (6,2) done, on schedule from there
      h20-h23 WEST x4 -> ends at (3,2), two tiles short of (1,2)
```

`(1,2)` weeded that night at `consecutive_unwatered >= 2` (`kaggriculture.py:770`).

### What is NOT the cause — all excluded with evidence

The job was **offered** (`crop_ops` emitted it), **covered** (`uncovered` empty), and **assigned** (to u10).
So it is not the node set, not triage, not priority, and not the assignment.
There is no DIG anywhere in u10's day; all 25 turns are accounted for.

Four earlier hypotheses were excluded the same day and are recorded in `REGISTER.md`: mid-day ferrying, pen siting, brink-water pricing, and the closing walk home.

### The obvious fix is a measured LOSS

Pin the farmer on a hire turn while it stands on the ring, reusing the `hold_farmer` machinery that already exists for the deliberate step.
That makes the prediction true by force, and the force is a turn of the 24-turn unit on nearly every hire day.

17-day grid, seed 11, `--tape victor`:

| | baseline | pinned |
|---|---|---|
| money @ d16 | **17,459**/15,759 | 16,044/15,759 |
| strawb from d11 | **35**/36 | 33/36 |
| weeds | **2**/0 | 4/0 |
| d11 move | 128/99 | **109**/99 |
| d11 idle | 23/57 | 40/57 |

`(1,2)` lived and `(0,2)`, `(1,4)` and `(2,1)` died in its place.
Reverted.

### The second cause, not yet chased

With the pin on, d11 went **fully green** and d10 from 14 wrong to 7.
The residual is a different mechanism: hands that arrive in a **later wave** (d10 hires across h0/h1/h2), by which time the h0 wave has walked off the ring, so the h0-computed `arriving` list is stale for them.
`_arrivals` predicts all of a turn's hires at once from the h0 ring.

### The untried direction

Fix the **prediction**, not reality: re-plan once after the farmer's hour-0 move is known.
Costs one extra solve on a hire turn and **no game turn**.
Risk is that the second solve moves the farmer somewhere else again — it is a fixed point with no convergence guarantee, so it would need a cap and a measurement.

### Artifacts

- `tests/test_a_hand_starts_the_day_on_the_tile_it_was_routed_from.py` — red on the mechanism, **green on the d9 control** (8 units, farmer parked, all eight predictions exact). Marked `xfail` because the defect is open.
- `data/logs/is_it_assigned_2026-08-12.log` — the offered/uncovered/assigned/walk trace.
- `data/logs/grid_baseline_2026-08-12.log`, `data/logs/grid_pin_farmer_2026-08-12.log` — the A/B.
- `data/logs/which_tile_dies_2026-08-12.log`, `..._pinned_...`, `..._baseline_...` — which tile weeds.

### Standing context this sits in

The alternate-day watering cadence (`router.crop_ops:650`) waters only tiles at `consecutive_unwatered >= 1`.
The counter starts at 1 on the planting day and weeds at 2, so a tile watered yesterday is safe tonight — which means **~20 tiles sit one miss from death every day, all season**.
There is zero margin, so any day that loses turns converts directly into a permanent tile loss.
That is the reason a 2-turn misprediction is worth a season of `strawb 35/36`.

### Everything ruled out on 2026-08-12, with the measurement

All on seed 11, tape `victor`, 20-day grid. Do not re-derive any of these.

| attempt | result |
|---|---|
| Pin the farmer on hire turns (`hold_farmer`) | **LOSS.** money@d16 17,459 -> 16,044; weeds 2 -> 4. `(1,2)` lived, `(0,2)`/`(1,4)`/`(2,1)` died. Costs a turn of the 24-turn unit nearly every day. |
| Predict the farmer walks off the ring | **BREAKS THE CONTROL.** d9 goes red — the farmer *stays* on d9 and *leaves* on d0/d1/d6/d10/d11. Its hour-0 behaviour is day-dependent, so no constant prediction is right. |
| Two-pass re-solve | **DOES NOT FIT.** A full hour-0 solve is 0.37-0.5s by d10-d17 against a 1s `actTimeout`; d10 would need three. Measured, not assumed. |
| Tour slack (`START_SLACK_TURNS` 1 and 2) | **LOSS on the farm.** d19 weeds 3 -> 7, strawb 33/33 -> 30/33, work 149 -> 126. Money rises (26,889 -> 27,538) only because we sell instead of tending — the wrong trade on an Elo ladder. It does not redistribute; it just does less work, and the dropped jobs are the brink waters. |
| Buy fertilizer (today's demand, and tomorrow's) | **NULL both ways.** `fertilize` d16 stays 10/13 at 0, today and tomorrow. Buying for today is too late by construction: `_process_market` runs after the unit phase, so stock lands after the crew drew at h1-h3. And the premise had already expired — see below. |
| `COVER_PLANNER = False` (the "old planner") | **BIT-ROTTED, not slower.** money d19 0/27,133, work 0/145, 18 weeds. It banks the $15 start and flatlines from d12. There is no comparison to be had. It is a stale runnable artifact and a trap. |

### Two corrections to earlier claims in this document's neighbourhood

- **"The tape wastes turns watering pastures" is WRONG and was my methodology.** The script compared
  the tape's watered tiles against *our* board state. Our pen placement differs from his, so a tile
  that reads PASTURE for us may well be planted for him. Nothing can be concluded about his tiles
  from our board. Retracted. The consequence runs against us: d16's water gap is the full 6 tiles.

- **The fertilizer starvation premise expired.** It was real when written (shed 1-4 against the
  tape's 12) and `FERTILIZER_RESERVE_LOOKAHEAD_DAYS = 1` fixed it: we now hold **14-20 against the
  tape's 12-13**, i.e. more than he does, and still fertilize less. Verified per-unit — u13 asks the
  shed for 6 FERTILIZER and now **gets all 6**, where it got 0 before. Supply is solved.

### What the tour probe actually found on d16

Comparing our plan against our own execution — no tape involved, so no board-state contamination:

```
    day 16: only 2 assigned jobs whose unit never stood on the tile
      u13  (5,0)  ['FERTILIZE']
      u13  (6,0)  ['FERTILIZE']
    u13: start=(5,4) budget=23 priced_cost=20  SLACK=3
         actual walk begins h02 at (4,4)     <- wrong tile AND a turn late
```

So **execution is not the problem**. 39 waters offered, nothing uncovered, all executed; 50 idle
turns and 96 turns of priced slack left over. The water row is a difference in what gets OFFERED,
and with the boards diverged by d16 that cannot be attributed to a defect from our side alone.

### The open question, restated

`cover.cover` is a **greedy insertion heuristic** — insertion positions per unit, cheapest that fits,
plus displace-and-rehome and `_make_room`. No global search, no restarts, no backtracking, no
optimality guarantee. How far its output sits from feasible-best has never been measured, and that
number decides the next move: near the frontier means the lever is the node set and the schedule;
well short means the planner itself is the lever. d18 is the day to measure it on — we spend 263 of
275 unit-turns, Victor spends 235 of 272 and does more.

### The d16 water gap: PARTLY a counting artifact, but we DO lose tiles he does not

Settled by replaying both sides and reading **each side's own board** — the earlier attempt read his
actions against *our* tiles, which is invalid once the boards diverge.

```
    day 16   ours: 53 water ops on 45 distinct tiles
             tape: 59 water ops on 45 distinct tiles
```

**Identical tile coverage.** The `water 53/59` row counts OPS, not tiles.

`_apply_unit_action` makes a repeat water a no-op — `if tile["watered_today"]: return`
(`kaggriculture.py`, WATER branch) — and a water on a non-PLANT returns immediately. So:

- his 59 ops on 45 tiles are **14 wasted turns**, plus two spent on PASTURE cells on his own board
- ours are **8 wasted turns**

We are *more* efficient per tile than the tape. Of the 14 tiles he waters and we do not, **12 are
non-comparable** — his board genuinely differs by d16 (he holds `WHEAT planted_d12 yield=3` where we
hold `STRAWBERRY planted_d5`; two are PASTURE for him too).

**DO NOT read the above as "nothing to fix" — that conclusion was wrong and is retracted.**

Matching tile COUNTS is not matching tile SETS. Of the 45 each side waters, only **31 overlap**:
14 he waters that we do not, 14 we water that he does not. Nearly a third of the day's watering is
different tiles.

And the decisive row was on screen the whole time: **weeds 3/0**. He loses ZERO tiles all season.
We lose three:

```
    (1,2)  STRAWBERRY  dead end of d11
    (2,0)  WHEAT       dead end of d14
    (9,0)  WHEAT       dead end of d18
```

So the water cadence IS deficient. What the board-vs-board harness legitimately establishes is only
the narrower claim that the raw `water 53/59` op-count gap is not itself the deficiency — six of his
extra ops are no-ops. The deficiency is which tiles we skip, and it costs three tiles.

**The cadence question is crop-dependent and was not being treated that way.** From `CROPS`:

```
    WHEAT       ongoing False  max_yield_day 4   max_yield 6   window = age 2..4
    MELON       ongoing False  max_yield_day 12  max_yield 6   window = age 6..12
    STRAWBERRY  ongoing True   interval 2
    TOMATO      ongoing True   interval 1
```

The WATER branch adds yield ONLY for `ongoing: False` crops, inside `window_start =
(max_yield_day + 1) // 2`. So for WHEAT and MELON every missed day inside the window is yield gone
permanently, not merely weed risk — a melon has 7 days to bank 6 units. For STRAWBERRY and TOMATO
water adds NO yield at all and buys only survival. Two of our three dead tiles are WHEAT.

Caveats worth re-checking before leaning hard on it: the exact 45-45 equality is striking (plausible
— both farms hold 75 tiles under the same cadence, so ~45 on the brink is an equilibrium — but not
verified twice), and tile attribution reads the previous turn's positions, which can be off by one.
That noise applies equally to both sides, so the comparison survives it.

**The one actionable thing this found is ours:** we spend ~8 turns a day watering tiles that are
already watered. Small, free, and the opposite of the problem being hunted.

Harness: `scratchpad/board_vs_board.py`.

---

## 2026-08-12 — Spawn-ring misprediction: is it worth fixing, and how (Fable's review)

Folded in from `docs/fable_spawn_ring_verdict_2026-08-12.md`.

2026-08-12, seed 11, tape `victor`. Answering the question in the spawn-ring misprediction doc
folded in above: analysis only, no code changed.
Two read-only scripts were run to get real numbers instead of guessing; both are described below
so the run can be repeated.

### Direct recommendation

Do (b) first. It is cheap, has no solve cost, is reachable at a line that already exists, and it
is the only one of the four that also hardens the schedule against causes of a 1-2 turn slip that
are not this bug. Do (a) second, as a precision improvement, but capped at two extra solves and
gated on wall-clock, because of a real timing risk this review measured and the source doc did
not. Do not pursue (c) as scoped -- it does not dodge the prediction problem, it only relocates it,
and on the one day this review checked in detail it would still orphan a route. (d): there is a
second, previously undocumented bug under the "residual second cause" label -- see below -- and it,
not "wave staleness," is most of what makes day 10 the hard case.

### Reachability check

Both mechanisms under discussion sit inside `agent()`'s `if router:` block in
`kagg/search/schedule_agent.py`, specifically the sequence at lines 2982-2992
(`_hires_this_turn` -> `_clear_the_spawn_ring` -> `arriving`) feeding the ONE solve at
`_router_acts` lines 1837-1844, gated by `if not routes` (line 1816). `state["routes"]` is reset to
`{}` on every day change (line 2958) and never rebuilt after ("NO REPLAN, NO TOP-UP", line 1845),
so this whole sequence runs exactly once per day, on the first `agent()` call at hour 0 -- confirmed
by instrumenting it directly (below), not inferred from reading. Any fix to either the prediction
(a) or the tour-budget slack (b) lands inside this exact, single, per-day call. Verified reachable.

### What was measured, not assumed

#### Experiment 1: does one extra solve converge?

Script: monkeypatches `SA._router_acts` to snapshot (deep-copy) `state` at every hour-0 call while
replaying seed 11 / tape `victor` for real through day 11, then off-line re-runs `_router_acts`
from each snapshot with (pass 1) today's prediction and (pass 2) a prediction rebuilt from pass 1's
own farmer action. Log: `data/logs/two_pass_experiment_2026-08-12.log`. Script kept at
`/private/tmp/.../scratchpad/two_pass_experiment.py` (scratchpad, not committed).

Result, all three days that were checked:

| day | pass 1 farmer act | pass 2 farmer act | converged in 1? | ring slots pass1 vs pass2 differ |
|---|---|---|---|---|
| 9 (control, `land=0`) | `PICKUP WHEAT 3` (stays (4,4)) | same | yes | 0/7 |
| 10 (`land=1, hands=14`) | `NORTH` -> (4,3) | `SOUTH` -> (4,5) | **no** | 14/14 |
| 11 (`land=0, hands=10`) | `NORTH` -> (4,3) | `NORTH` -> (4,3) | yes | 10/10 |

Day 10 needed a third pass to settle: pass 2 and pass 3 both land the farmer on `(4,5)`, so it is a
fixed point reached after **two** corrections, not one, on the one day it was checked that needed
more than one. This directly answers the stated concern: **one iteration is not always enough, but
it did not diverge or oscillate on any day tested -- it settled within two.** Day 9 is the control
from the source doc and reproduces exactly ("all eight/seven predictions exact"), which cross-checks
that this harness reproduces the real mechanism rather than a harness artifact.

On days 10 and 11, *every* ring slot in the naive prediction was wrong (10/10, 14/14) -- this
matches the doc's own finding almost exactly and is not a sampling fluke; the naive predictor is
wrong on essentially 100% of hires on any day the farmer's first action is a move.

#### Experiment 2: what does the extra solve cost, in wall clock

Timed `agent()`'s hour-0 call across days 0-17, same tape/seed, no monkeypatching:

| day | crew size context | hour-0 solve time |
|---|---|---|
| 0-6 | 1-7 units | 0.000-0.002 s |
| 8 | | 0.075 s |
| 9 | | 0.127 s |
| 10 | 14 hires that day | 0.372 s |
| 11 | | 0.326 s |
| 16 | | 0.426 s |
| 17 | | 0.496 s |

`docs/competition_brief.md`: `actTimeout` is **1 second per turn**, `remainingOverageTime` is
**60 seconds banked for the whole 720-turn episode**. A single solve already costs roughly half the
per-turn budget by day 16-17. Experiment 1 showed day 10 -- a fourteen-hire land-buying day, exactly
the kind of day this fix targets -- needs *three* solves to reach its fixed point. Three solves at
day 10's measured 0.372s each is over 1.1s, which **exceeds `actTimeout` on the solve alone**,
before the rest of the turn's work. This is a real, previously unmeasured cost that the source doc's
"one extra solve and no game turn" did not price in, because it assumed one iteration would suffice.

### Ranking

**(b) — do this.** Reachable at the exact line that already docks phantom-vehicle budget for a
different reason: `_router_acts` line 1697-1698,
`for k in range(len(units), len(plan_units)): budget[k] = max(0, budget[k] - 1)`. The four ring
tiles are mutually within Manhattan 2 of each other and `_spawn_hand`/`_arrivals` can only ever
return one of those four tiles -- so the walking-distance error between *any* predicted landing tile
and *any* actual one is bounded by 2, regardless of whether the mismatch is a clean rotation (day 9,
11 pattern) or a count-per-tile mismatch (see the second cause below). A second turn docked off
every phantom vehicle's budget at this line is a direct, bounded, no-solve-cost hedge against
*all* of it, not just the rotation case. It also protects against sources of a 1-2 turn slip that
are not this bug at all -- which is the point, given the "Standing fact" above. Two caveats, both
unverified because verifying them is a code change: whether -2 flat is too conservative (wastes
slack on days the tour was never going to be short, the same failure mode that sank the pin
experiment) is an empirical question that needs the same A/B the doc already ran for the pin, and
a more surgical version -- reserve margin only on a tour's *last* stop rather than off the whole
budget -- looked more promising on inspection but its implementation locus (inside `_solve` /
`router.py`'s acceptance check) was not read this session.

**(a) — do this too, capped.** Experiment 1 shows it is not a runaway fixed point: it settled within
two corrections on every day tested. It is correct in direction and the untried-fix note in the
source doc undersold its cost. Cap iterations at 2 (matches the worst case measured), and gate on a
wall-clock budget with a hard fallback to the pass-1 (current) prediction if the accumulated solve
time for the day is getting close to `actTimeout` -- day 10's 3-solve worst case already crosses
1 second at day-10-sized crews, and crew/board size only grows later in the season, so this is not
a corner that stays small. This makes (a) strictly an improvement in prediction *accuracy* over
today, conditioned on a budget guard that does not exist in the source doc's proposal. Also: (a) as
scoped (correcting the ring-slot prediction) does **not** fix the residual on day 10 -- see below --
so shipping (a) alone and expecting day 10 to go green would repeat the doc's own measured surprise
("14 wrong to 7", not to 0) under the pin experiment.

**(c) — do not pursue as scoped.** It looked like a clean sidestep ("price the tour from whichever
tile it lands on, permutation stops mattering") but does not survive contact with the actual
mechanism. Checked concretely on day 11 (10 hires, 4-tile ring): predicted per-tile counts are
`(5,4):3 (4,5):3 (5,5):2 (4,4):2`; actual are `(4,4):3 (5,4):3 (4,5):2 (5,5):2`. These are not the
same multiset -- `(4,4)` gets **one more** hand than planned and `(4,5)` gets **one fewer**. Binding
tours to landing tiles rather than arrival order fixes the *ordering* problem but not this: a tile
that gets an extra, unplanned visit still has no tour waiting for it (an orphaned real hand), and a
tile that gets one fewer visit than planned leaves a planned tour with no vehicle. Getting the counts
right requires the same accurate start-position prediction that (a) is already trying to solve, so
(c) is not an independent alternative -- it is, at best, a complementary change to how the executor
binds a real hand to a planned route, layered on top of (a) rather than instead of it. Whether the
executor can even express "route bound to tile, not index" was not checked -- the binding is
currently by index identity (`_router_acts` line 1690-1692: "index here is the index they will
occupy in `farm['hands']`"), and rebinding it by position would touch whatever reads
`state["routes"]` every subsequent hour, which was not located this session.

**(d) — a genuinely new finding, not previously in the register.**

### The residual second cause is not (only) wave staleness

The source doc's account -- "d10 hires in waves across h0/h1/h2, by which time the h0 wave has
walked off the ring, so an h0-computed prediction is stale for later waves" -- is true as far as it
goes but is not the whole mechanism, and reading the code that actually decides *how many* hires
happen at h0 shows a second, sharper bug.

`_hires_this_turn` (line 416, this is what the dawn plan calls to size `arriving`) computes `n`
purely from bank affordability against the schedule row's `hands` want. It does **not** apply
`_unwalled_landing_slots` (line 456). But the market block that actually **emits** the HIRE orders
(line 3864-3865) does: `if HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS and land>0: want = min(want,
_unwalled_landing_slots(...))`. That is exactly the `_hires_this_turn` docstring's own warning,
unheeded by its own author: *"Read by the DAWN PLAN, which has to route them, so it must not
diverge from what that block actually orders."* It diverges. On a land-buying day, the dawn plan's
`arriving` list can contain more phantom hands than actually get hired at hour 0 -- the rest are
genuinely held back and trickle in later via the `elif HIRE_FIRST` drip (line 3869), some of them
plausibly not until the parcel itself settles (comment at line 3872-3874 mentions a deadline of
`TPD` on a land day, i.e. as late as dusk). A phantom routed as if it has ~23 turns from hour 1 but
that does not actually exist until, say, hour 13, is a much larger error than 2 Manhattan tiles --
it is a route built for a vehicle that is unavailable for over half the day.

Confirmed this is live on day 10: `data/seed_scripts/victor/schedule.json` day 10 is `hands: 14,
land: 1`; days 9 and 11 are both `land: 0`. Day 10 is exactly the day both the source doc's pin
experiment (14 wrong -> 7, not 0) and this review's two-pass experiment (needs 3 solves, not 2) flag
as the hard case, and it is exactly the day `HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS` is live.

**This changes the answer to "does the second cause change which of (a)-(d) is right."** Yes: (a)'s
two-pass mechanism, scoped to correcting ring-slot prediction, cannot fix this by construction --
the phantom crew *count* is already wrong before ring rotation is even computed. The actual fix for
day 10's residual is to give `_hires_this_turn` the same `_unwalled_landing_slots` cap the market
block already applies (so `n` at hour 0 matches what will actually be ordered), and -- harder, not
attempted here -- extend the dawn plan to also model the later-hour drip hires as phantom vehicles
with a correspondingly later, shorter budget rather than not modelling them at all. This is a
parity bug of the same shape the project's CLAUDE.md already warns about repeatedly ("a gate only
tests what it exercises" / "check whether a doc already answers the question") -- two functions that
must agree, stated as needing to agree in one of their own docstrings, that do not.

### Framing check: is the ring misprediction even the right thing to fix

The prompt's own framing challenge is right and should be taken at face value, not politely hedged.
The worked example in the source doc is a tour priced at *exactly* 23 turns against a 23-turn
budget. The watering cadence weeds a tile at `consecutive_unwatered >= 2` with the counter starting
at 1 on the planting day -- so, by the doc's own count, roughly 20 tiles sit exactly one miss from
death every day, all season, by design. Given that, a 2-turn shift from *any* cause -- this bug, a
different bug, a future rule change, an off-by-one in some other function -- converts directly into
a dead tile whenever it lands on a tour that was priced with zero margin. The spawn-ring
misprediction is real, deterministic, and proven (Experiment 1 above independently reproduces it),
so it is not a phantom cause. But it is a *trigger*, not the vulnerability. The vulnerability is
that nothing in the scheduler ever prices a margin, anywhere, for anything -- confirmed by reading
`_router_acts`'s budget construction, which computes exact turn budgets and hands them to a solver
with no slack term of any kind visible in what was read this session. Fixing the prediction (a)
closes this one instance. It does not touch the underlying zero-margin architecture, which will
present the identical symptom -- a tile weeded because a tour finished two tiles short -- under the
next cause that perturbs a tour by even one turn. That is the argument for ranking (b) above (a):
it is the fix that generalizes, and the fix aimed at the symptom the prompt itself flagged as
possibly the real defect.

### What could not be verified this session

- Whether a flat -2 budget haircut on phantom vehicles (b) nets positive on the 17-day grid, or
  repeats the pin experiment's failure mode (forced margin spent on days that did not need it). This
  needs the same seed-11 A/B the source doc ran for the pin fix, and running it requires a code
  change, which was out of scope here.
- Whether the more surgical form of (b) -- slack only on a tour's last stop, inside the `_solve` /
  `router.py` acceptance check -- is actually where that check lives; `router.py` was not read this
  session.
- Whether the executor (whatever reads `state["routes"]` every hour after the dawn solve) could be
  changed to bind by landing tile rather than index for (c); the binding code past
  `_router_acts` line 1843 was not located.
- Whether `_hires_this_turn` gaining the `_unwalled_landing_slots` cap, by itself, closes day 10's
  gap or only shrinks it further (there may be a third layer under this one); not measured.
- Experiment 1 covered three days (9, 10, 11) of one seed on one tape. The claim "settles within two
  corrections" is well short of a season-wide guarantee; it is what was observed, not a proof.

### Artifacts

- `data/logs/two_pass_experiment_2026-08-12.log` -- Experiment 1's full output.
- Experiment 1 and 2 scripts: read-only, run from repo root, not committed (scratchpad only, per
  the no-code-change constraint). Reproducible from the snippets embedded in this doc's tables plus
  `scripts/breakdown.py`'s `TAPES["victor"]` / `env_config` / `tape_policy` helpers, which is all
  either script imports beyond the schedule agent module itself.

---

## 2026-08-13 — Kawashigi: one board, and the leader is not open-loop

Folded in from `docs/kawashigi_one_board_2026-08-13.md`.

2026-08-13.
16 episodes of **カワシギ** (current #1) downloaded and cached to `data/seed_scripts/kawashigi/`,
plus four of our own games from 2026-08-12.

### 1. Every ladder game starts from the identical world

Hashing the opening observation with `farms`, `step`, `remainingOverageTime` stripped:

```
    world  dc0d81c5   1 distinct across all 16 Kawashigi games
    market a7e792b0   1 distinct
    tiles  bb3b18da   1 distinct, AND identical for seat 0 and seat 1
```

Our own games carry the same three hashes:

```
    92433651  alex chilton vs Benjamin Beaujard   world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
    92450417  alex chilton vs Agzam               world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
    92443929  Bang sion vs alex chilton           world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
    92439273  Jonathan Roy vs alex chilton        world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
    92498144  カワシギ vs Yusuke Hayashi            world=dc0d81c5 mkt=a7e792b0 tiles=bb3b18da/bb3b18da
```

Terrain, land parcels, town positions and opening prices are constants of the competition, and the
two seats are mirror-identical. **The seed's only job is the shop unlock draw** (section 2), which
first fires on d3. So a ladder game has exactly two variables: the shop sequence and the opponent.

This retires the framing that has driven a lot of work here. "Seed variance is ~15%" (CLAUDE.md) is
a fact about `kagg.arena`'s randomly drawn *boards*, **not** about the ladder. Held-out seeds there
measure robustness to a board we will never be dealt. Offline solving against this one board is not
overfitting; it is the whole problem. The thing that genuinely needs generalising is the shop draw.

### 2. He is NOT replaying a tape

If he were open-loop, 16 games on one board would be 16 identical action streams. They are not.
Pairwise identity over the 720-turn action vector runs 26%-82%.

Distinct action-vectors per hour, across the 16 games (1 = all sixteen played the same thing):

```
    d00 : 111111111111111111111111   modal 16.0/16
    d01 : 111111111111111111111111   modal 16.0/16
    d02 : 111111111111111111111111   modal 16.0/16
    d03 : 112222222222222221111111   modal 12.2/16
    d04 : 111111111111111111111111   modal 16.0/16
    d05 : 111111111111111222111111   modal 15.9/16
    d06 : 111111111111111111121121   modal 15.5/16
    d07 : 111222222222333333444555   modal  9.8/16
    d08 : 332223333333444444456566   modal 10.6/16
    d09 : 511133655545555544442111   modal 10.0/16
    d10 : 112333235335565556666666   modal  8.3/16
    d11 : 511244436446755777777776   modal  7.2/16
    d12 : 612445456667667777777777   modal  6.7/16
    d13 : 712233355666666677778888   modal  7.0/16
    d14 : 913445556466666666666677   modal  7.0/16
    d15 : 714565566666666678877888   modal  6.0/16
    d16 : 713977888888888899999999   modal  5.0/16
    d17 : 913597799999999999999999   modal  4.0/16
    d18 : 917989999999999999999999   modal  3.0/16
    d19 : 912988899999999999999999   modal  4.3/16
    d20 : 913999999999999999999999   modal  3.4/16
    d21 : 913988999999999999999999   modal  3.6/16
    d22 : 914999999999999999999999   modal  3.0/16
    d23 : 912699999999999999999999   modal  3.4/16
    d24 : 919999999999999999999999   modal  1.9/16
    d25 : 914999999999999999999999   modal  2.6/16
    d26 : 918999999999999999999999   modal  2.3/16
    d27 : 913999999999999999999999   modal  2.2/16
    d28 : 916999999999999999999999   modal  2.8/16
    d29 : 814999999999999999999999   modal  2.8/16
```

**All 16 games are byte-identical for the first 74 turns — d0 through d3 h1.**
d0-d2, d4 and most of d5-d6 are 16/16 at every hour. From d7 the fan-out starts, and by d24 the
modal action is shared by fewer than 2 of 16 games. That is a fixed opening followed by live play.

**The 74 turns are the deterministic prefix, and they end at the first shop unlock.**
`_advance_day` draws a shop every `townShopUnlockInterval = 3` days with replacement
(`kaggriculture.py:854,878`), so the first draw lands on d3 — and d3 h2 is exactly where the 16
games stop agreeing. All 16 drew a different sequence:

```
    2407  ICE_CREAM_SHOP | BAKERY         | YARN_STORE       0434  SMOOTHIE_SHOP  | ICE_CREAM_SHOP | FARMERS_MARKET
    7234  BAKERY         | YARN_STORE     | YARN_STORE       8785  YARN_STORE     | PET_CAFE       | PIZZA_SHOP
    8461  PIZZA_SHOP     | PIZZA_SHOP     | YARN_STORE       8144  SMOOTHIE_SHOP  | ICE_CREAM_SHOP | FARMERS_MARKET
    2932  BAKERY         | BAKERY         | PIZZA_SHOP       8348  SMOOTHIE_SHOP  | YARN_STORE     | FARMERS_MARKET
    1493  PET_CAFE       | BRUNCH_SPOT    | BRUNCH_SPOT      1336  ICE_CREAM_SHOP | YARN_STORE     | YARN_STORE
    5172  FARMERS_MARKET | PIZZA_SHOP     | FARMERS_MARKET   9904  BRUNCH_SPOT    | BAKERY         | PIZZA_SHOP
    2538  PIZZA_SHOP     | PET_CAFE       | SMOOTHIE_SHOP    9908  PIZZA_SHOP     | BAKERY         | SMOOTHIE_SHOP
    6371  SMOOTHIE_SHOP  | ICE_CREAM_SHOP | BRUNCH_SPOT      2865  PIZZA_SHOP     | ICE_CREAM_SHOP | ICE_CREAM_SHOP
```

16 distinct sequences over 16 games. So the divergence is **the shop draw, not the opponent** —
same-opponent pairs diverge as early as d5 h15 and different-opponent pairs stay identical to d9 h6,
because opponent identity is not what is driving it.

That is the finding that matters. The seed's only job is the shop draw, and **the leader re-plans
around it from the moment it lands.** `SHOP_ADAPT_HERD` is our one attempt at the same thing, it
starts at d6, and it reads only shop *presence* to float a cow/sheep split. His response begins on
d3 and reaches the whole plan.

### 3. Two structural constants worth chasing

- **Hour 1 is identical in all 16 games right through to d23** (the `1` in column 1 of every row
  from d16 to d23) while hour 0 and hours 3+ are fully divergent. Something at h1 is unconditional.
- **Hour 0 is the most divergent hour of the day from d14 on** (leading 9s). A dawn decision that
  reads state, then a walk that is much more stable. Structurally our own architecture: plan once
  at h0, execute.

### 4. Record

15-1 across the 16. The single loss is 92445172, $88,448 to Yusuke Hayashi's $89,993 — $1,545.
Money range $44.9k to $150.0k on an identical board, which is the size of the swing the opponent
alone produces.

### Open

- Diff his fixed 74-turn opening against ours, op for op. It is a solved plan on a board we also
  own, and it is the cheapest thing in this project to copy.
- Find what he does at h1 every day.
- Re-check whether `kagg.arena`'s multi-seed evaluation is measuring anything we are graded on.

---

## 2026-08-19 — The crop mix, the herd and the routes are ONE artifact

Folded in from `docs/the_mix_and_the_routes_are_one_artifact_2026-08-19.md`.

2026-08-19.
The single most expensive lesson of the day, confirmed independently four times.

`_apply_precomputed` keys every stop on `(tile, tuple(op_names))`.
A day whose work has changed no longer matches the route solved for it, the stop is demoted to
`_insert_leftovers`, and `_insert_leftovers` needs slack the day has not got.
So **any change to what the units DO must be measured against routes re-solved for it**, or the number
is measuring the mismatch and not the change.

The tell is an implausible magnitude.
No single tile and no single animal is worth $10,000, so a swing that size is a mismatch, not a
finding.
The second tell is the PLANTS column moving when only the shed should have.

### What it cost, and what it was worth once matched

| change | against old routes | against re-solved routes |
| --- | --- | --- |
| strawberry cap, straw arm | **-$10,553** | **+$4,022** |
| melon arm, no crop change at all | -- | **+$5,615** |
| 1 tomato tile, straw arm | -$1,117 | included above |
| 1 tomato tile, melon arm | -$3,880 | still negative, tile removed there |
| 2 geese, straw arm | -$62,866 | **-$63,417** (NOT rescued -- see below) |

The melon row is the important one: **its crop mix did not change at all**.
Strawberry stayed at 34, no tomato, cap never binds (3 drains -> cap 36, it plants 34).
The whole +$5,615 is route staleness -- the tables had been solved against an older schedule and had
drifted.
Any arm carrying stale routes is paying this silently.

### Route seating, measured

`cover.PRECOMPUTED_MISSES` counts stops that did not seat.
Straw arm after re-solving d12-d23: **19 skipped over twelve days**, with d12, d16 and d21 perfect.
q4_melon before its closing days were re-solved: **0 skipped in d12-d22 and 138 in d24-d29**, which is
where its -$12,308 came from -- `q4_branch.install` resets `cover.UNSOLVE_DAYS` to `()`, so the
four-quadrant arms run precomputed routes right through d29 while the three-quadrant arms hand the
close to the greedy.

### Shipped, and why the four-quadrant arms were left alone

Each arm uses a different end of tetsuya's drain-keyed strawberry table, and only the high end survived:

```
 arm        quads  straw-drains  cap  row   delta      verdict
 straw_q3     3         4         37   42   +4,022     binds, GOOD
 melon_q3     3         3         36   34   +5,615     never binds
 q4_straw     4         0         26   42     -214     binds hard
 q4_melon     4         0         26   34   -9,560     binds hard, worst arm
```

Both four-quadrant boards draw ZERO strawberry shops and so take the table's low end, where cutting
costs about $2,400 a tile.
tetsuya's 25.5 tiles at zero drains is HIS optimum for HIS season; ours has more ground and cannot go
there.
**A flat ceiling near 37 fits every row above** -- it reproduces straw and melon exactly and never
binds on q4 -- and is the next thing to test, with the q4 tables re-solved for it.

### `q4_armed`, not `len(unlocked)`

Both the cap and the tomato tile key on `state["q4_armed"]`, which `Q4Branch` decides at d6.
A live quadrant count is wrong here: **d12 is the very turn the fourth quadrant is bought**, so the
count reads 3 at dawn and 4 from d13.
A per-day test and a once-only test therefore disagree on exactly that day, which let the tomato tile
fire on the q4 board for -$1,031 while the cap looked correct.

### Seed at the close

Two separate leaks, one fixed and one not.

- **The replayed opening buys his seed counts.** d11 h0 issues `BUY_SEED STRAWBERRY 23`, sized for his
  42-tile season; the cap plants 37 and five sit in the shed to the final bell. Trimmed in the replay's
  order loop -- the same place `BUY_ANIMAL` is already re-labelled for the herd split. **+$560**, seed
  at close $590 -> $30, plants identical.
  **Three-quadrant boards only**: on a q4 board `q4_branch` installs its planting rows AFTER that turn,
  so the season total is short at d11 and the trim UNDER-buys -- **-$8,582 on q4_melon to save $170**.
- **Wheat, 2-4 at the close, ~$30, UNEXPLAINED.** Reached 0 on the pre-cap mix. Bounding `_later` by
  `RT.plant_prize(crop, day) > 0` was tried and did **not** move it, so rows past the crop's last useful
  day are not the cause. `test_no_wheat_seed_is_left_in_the_shed` is relaxed to `<= 3` and this is
  recorded there as an open regression, not a tidy-up.

### Stage 1 vs stage 2 -- the spike that separates them

Alex's original design, stated correctly (an earlier draft of this file had the two inverted):

- **Stage 1 -- the optimum animal and plant MIX, derived from the maths.** How many cows, sheep and
  geese; how many tiles of each crop. Decided from drains, price curves, yields per tile and the action
  cost of working them. Not copied off a leader.
- **Stage 2 -- the schedule.** The day-by-day plan that realises that mix: what is bought when, what is
  planted when, what is built when.
- Routing -- the lawnmower -- is downstream of both, and turns a day's rows into 24 turns of work.

Today's evidence is that stage 1 is where the gap to the #1 player is.

Our planner was handed tetsuya's schedule, on his own board, seat and seed (`94345389`, seed
959074148), against his own recorded opponent, with `REPLAY_OPENING_DAYS = ()` and
`cover.UNSOLVE_DAYS = range(0, 30)` -- so no taped opening and **no precomputed routes at all**:

```
  our planner on his schedule   $62,365
  his own recorded result       $55,330
                                +$7,035
  herd   COW 8  SHEEP 2  GOOSE 3
  plants WHEAT 161  STRAWBERRY 32  MELON 8  CARROT 8
```

**Our routing beats his, on his own schedule, with the worst routing we can give it.**
So the gap to the #1 player is not execution. It is stage 1 -- the mix itself.

Corroborated by utilisation, counting `NORTH/SOUTH/EAST/WEST` as movement and `PASS` as idle:

```
        tetsuya                     kawashigi
 day   work  move  PASS  idle%     work  move  PASS  idle%
 d14  107.2 142.3  45.7  15.5%     94.5 110.0   0.5   0.2%
 d20  147.8 116.2  30.6  10.4%    136.0 146.0   9.0   3.1%
 d23  131.8 123.5  39.4  13.4%    128.5 162.5   0.0   0.0%
```

kawa runs at the limit -- 0.0% idle at d23 -- and tetsuya never drops below 10%, while doing MORE work
with FEWER moves.
The tape we replay for d4-d11 is therefore one with no headroom, and any inefficiency downstream has
nothing to hide in.

**Stage 1 has never been built.** We inherit a leader's schedule wholesale -- Victor, then kawa -- which
is stage 2 handed to us with stage 1 already baked in and unavailable. Every crop and animal experiment
of 2026-08-19 (cap, tomato, geese, cow count) was a hand-poke at a stage-1 quantity through a stage-2
artifact, and each needed a two-hour route re-solve merely to be measurable.

The obstacle to searching stage 1 is that it is coupled to the routes through stage 2: every candidate
mix costs an hour of solving before it can be scored. Making it searchable needs either a much faster
solve, or a way to score a mix that does not require exact routes -- which is what deriving the mix from
the maths was for in the first place.

### His schedule does NOT transplant -- measured on 14 boards

One schedule, extracted from `94345389`, run on 14 of his other games: his seat, his seed, his recorded
opponent, no taped opening and no precomputed routes.

```
  record vs his opponents   7W - 7L   (0.50)
  mean vs his own bank      -$13,912
  our mean bank             $100,565     his $114,477
```

On the board the schedule came FROM, our routing beat his by +$7,035. On the other fourteen it is a
coin flip and $14k a game worse. His stage-2 rows carry that board's shop draw baked into them, so a
copy loses exactly the adaptation that makes him #1.

**So there is no shortcut through his schedule.** The thing worth having is the stage-1 logic that
GENERATES a mix from a board, not any schedule it happened to produce.

### Geese: the defect is `swap_in_geese`, not the bird

Fifth attempt at a goose verdict, and the first with a working instrument.

```
  2 geese via swap_in_geese, cow-solved routes      $97,317   seed at close $2,100
  2 geese via swap_in_geese, GEESE-solved routes    $96,766   seed at close $2,100
  no geese,                  geese-solved routes   $156,083   seed at close    $40
  no geese,                  cow-solved routes     $160,183   seed at close    $30
```

A matched re-solve did **not** rescue geese -- 96,766 against 97,317 -- while a cow season on the
geese-solved routes still banks $156,083. So the routes are fine and `swap_in_geese` is broken: it
reshapes the whole schedule (the d12 fixture goes WATER 38 -> 21, COLLECT_FERTILIZER 14 -> 6) and
inflates seed purchases by ~$2,000 in a way no route mismatch explains.

Geese from a schedule that natively contains coops are harmless: built on 9 of the 14 boards above,
one to three birds, no collapse and no seed explosion. Those boards went 6W-3L against 1W-4L without,
and averaged $8.7k better -- suggestive, but confounded, since a goose board is also an egg-shop board.

Previous goose verdicts were void for a different reason each time: `SELLABLE` omitted EGG so it could
never be sold, then cow-solved routes, now `swap_in_geese`. **Do not accept a goose measurement without
first stating which instrument produced it.**

---

## 2026-08-19 — The greedy is a mix scorer, and that makes stage 1 searchable

Folded in from `docs/the_greedy_is_a_mix_scorer_2026-08-19.md`.

2026-08-19, evening session.
Everything here is measured on each arm's own tape and seed, replaying d4-d11 then playing our planner.

### The finding

Turning off every solved route from d12 onward costs a flat ~4% on the three-quadrant arms and
**gains** money on one four-quadrant arm:

```
 arm        solved routes   greedy from d12    delta      mix change
 straw_q3      160,183         154,277        -5,906      wheat 120 -> 123, rest identical
 melon_q3      145,068         137,529        -7,539      wheat 135 -> 134, rest identical
 q4_melon       93,929          81,834       -12,095      wheat 133 -> 130, rest identical
 q4_straw       78,305          79,527        +1,222      wheat 128 -> 127, rest identical
```

Two things matter more than the deltas.

**The mix is preserved.** The herd is identical on every arm and the crop counts move by at most
three wheat tiles. So the greedy plays the same season, slightly worse -- it does not play a
different season.

**A season takes 8-25 seconds.** The solve it replaces takes about two hours per arm.

That combination makes the greedy a usable RANKER for a stage-1 mix. It is not a substitute for the
final number -- confirm any winner against re-solved routes before shipping -- but it removes the
coupling that made every stage-1 experiment cost a solve, which is what the "mix and the routes are
one artifact" section above recorded as the obstacle.

### The q4 tables are actively harmful

`q4_straw` banks **more** with no routes than with its solved table. A table you beat by deleting it
is doing damage, not merely drifting. Those two tables are the only ones never re-solved during the
day's mix work, and `q4_branch.install` runs them right through d29 (`q4_branch.py:294` resets
`cover.UNSOLVE_DAYS` to `()`), so the drift reaches the closing days where there is no slack.

`scripts/resolve_q4_full.sh` re-solves both, d12-d29. Until it has run, **no q4 experiment measures
the idea being tested -- it measures the table.**

### A comparison that measured nothing, and how to spot it

`scripts/q4_vs_q3.py` patched to unsolve both arms returned delta **exactly +$0 on all 12 seeds**,
with matching quadrant counts. Two different schedules cannot produce identical money to the dollar
twelve times. The harness is not applying the q4 plan.

The tell is the one this project keeps re-learning: an implausible number is a broken instrument, not
a finding. Here it is implausible in the other direction -- a PERFECT null across independent seeds
is as suspect as a $10,000 swing. **q4 remains untested.**

### Hires are NOT being lost -- corrected

Three mechanisms can in principle shrink the crew below the schedule row: affordability in
`_hires_this_turn`, the `_fit_slots` cut when a turn's orders exceed `ORDER_SLOTS = 10` (the env's
own `maxMarketOrdersPerTurn`), and `_do_hire` failing silently on a thin bank.

Measured per day on both q3 arms, none of them does:

```
 straw_q3   row 277   landed 277   short +0 on EVERY day   slotcut 32
 melon_q3   row 277   landed 277   short +0 on EVERY day   slotcut 33
```

`_fit_slots` does cut ~32 hires a season, and every one is re-issued on a later hour and lands. It is
a deferral, not a leak.

So the "we hire 11, tetsuya hires 6" gap is not a defect. **We hire 11 because kawa's schedule row
says 11, and we get all 11.** It is another stage-1 quantity inherited wholesale through a stage-2
artifact. The ladder is `mult * fib(n)`, so 11 costs $232 a day against 6 at $20 -- roughly $4,000
across d8-d27, buying hands that then `PASS` 124 times against his 16.

The hand count changes the unit set and therefore desyncs every route, so it can only be swept with
routes off. That is the correct instrument, not a workaround.

### Why the schedule's "harvest 10" never reaches the router

The row's counts are not carried anywhere. Pins hold only `PLANT` and `BUILD`
(`schedule_agent.py:1298`, `:1313`) -- **there is no harvest pin.** `_live_ops` (`:1282`) re-derives
the work from the live cell at every stop:

> "The route fixes *which tiles* a unit visits and in what order... What it does when it gets there
> is read off the cell, so a stop whose work another unit already did, or whose crop weeded
> overnight, simply returns nothing and the stop is dropped."

If three tiles are ripe you get three harvests, whatever the row says. Nothing checks the row's
number and nothing reports the shortfall.

So `harvest 0/10` on d3 is not a planner failure and no flag is blocking it -- the crop was not
ripe. The lever is WHEN a tile becomes harvestable, and it lives in `router.crop_ops`, not in the
schedule. WHEAT is `first_yield 2, max_day 4`: tetsuya harvests at d3 and turns the ground over, we
wait for `max_day` and take more units per tile while the tile stays occupied. That is what leaves us
full at d7 with zero empty squares, which is what stalls our pens at 9 while his reach 15.

**Untested.** It is the same trade as the strawberry cap -- less per tile, more throughput -- and it
is the tetsuya-tracking change most worth measuring next.

### Flags deleted, verified byte-identical

Ten flags and five orphaned constants, removed in a worktree and checked on all four arms:

```
 arm        money      baseline    herd            seed   plants
 straw_q3   160,183    160,183 ok  COW10 SHEEP4    $30    W120 M12 S37 T1 C5
 melon_q3   145,068    145,068 ok  COW10 SHEEP4    $10    W135 M20 S34 C8
 q4_melon    93,929     93,929 ok  COW6  SHEEP12   $180   W133 M20 S34 C7
 q4_straw    78,305     78,305 ok  COW6  SHEEP12   $130   W128 M12 S42 C7
```

`cover`: `AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP`, `SUPPLY_LIMITS_EVERY_DRAW`,
`SUPPLY_CHECKED_OPS`, `DELIVER_SURPLUS_NOT_THE_ROW`, `BANK_THE_ROWS_PRODUCE_WHILE_REAPING`.
`router`: `TOP_UP_SAFE_TILES`, `TOP_UP_FROM_DAY`, `BRINK_WATER_IS_WORTH_THE_TILE_FROM_DAY`
(INERT -- it only reached the board through `min(LATE_TRUNCATED_PLANT_DAY, 99)`), `CLOSED_TOUR`.
`schedule_agent`: `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE` with `EARLY_WOOL_SHEEP`,
`MILK_POOR_SHOP_COUNT`, `MILK_POOR_COW`, `MILK_POOR_SHEEP`, and `SEED_BEFORE_LIVESTOCK`.

**`SHOP_ADAPT_CROPS` was deliberately NOT removed.** Its dead branch, `_adapt_crops`, is 83 lines
that pick a crop from town-drain headroom, priced per tile and costed over re-sow cycles. That is
stage-1 logic, and our strawberry cap is a hand-rolled special case of it. It belongs in the sweep as
a config to measure, not in the bin.

### Correction, 2026-08-19: three of the four "holes" were the harness, not the planner

The first grid read `BUILD 0/15`, `PLACE 29/15` and `BUY_ANIMAL 10/15` and all three were counting
errors in `tets_grid3.py`. Corrected on tetsuya's own board (`94345389.json`, seed 959074148, seat 0):

- **`BUILD 0/15` -> 15/15, exact every day.** The env has no `BUILD` op. It has `BUILD_COOP` and
  `BUILD_PASTURE` (`reference/kaggriculture.py:493,499`), and `schedule_agent.py:1274` emits those
  names. The grid counted the string `"BUILD"` and matched nothing.
- **`PLACE 29/15` -> 15/15, exact.** `PLACE` is not animals-only. 14 of the 29 are
  `PLACE FERTILIZER`. Animal placements are COW 6, SHEEP 6, GOOSE 3 -- the row exactly.
- **`BUY_ANIMAL 10/15` -> all 15 heads bought.** The row asks 15 HEADS; `schedule_agent.py:4901`
  emits one order per SPECIES (`["BUY_ANIMAL", a, want]`), so 15 heads leave in 10 orders. Orders
  were being counted against heads. Same shape as `feedback_offers_are_not_fills`, one field over.

A whole session's worth of "missing planner methods" was three unit mismatches in the instrument.
Before implementing against a grid cell, check the op NAME the env actually uses and the UNIT the
column counts.

### What actually tracks, and what does not

Following tetsuya's schedule, on his own board and seed:

```
    hands      exact every day except d12 (9/11)
    plants     212/212 season
    crop mix   WHEAT 164/164  STRAWBERRY 32/32  MELON 8/8  CARROT 8/8
    builds     15/15
    places     15/15 animals
    animals    15/15 heads
    FEED       314/353
    CARE       316/353
    herd       14 standing, COW 5 SHEEP 6 GOOSE 3
```

The herd climbs monotonically 5 -> 14 by d12 and never drops -- nothing dies. But 15 placements
leave 14 animals standing, so one COW placement lands on ground that already holds one. One cow's
FEED and CARE across the back of the season is the shape of the 39-op shortfall. That is the next
thing to fix, and it is one defect, not two.

### TOMATO is not in ANY schedule, and the adapt rule did not fire

Alex's challenge, 2026-08-19: "tetsuya plants no tomato at all - that is against your original
evidence, that's why we added tomato to kawa because on some seeds he does."

Correct, and broader than one player. No schedule file in the repo carries a TOMATO row:

```
    tetsuya           WHEAT 164  STRAWBERRY 32  MELON  8  CARROT 8
    tetsuya_93866112  WHEAT 135  STRAWBERRY 37  MELON 15
    kawashigi         WHEAT 136  STRAWBERRY 34  MELON 20  CARROT 8
    kawashigi_b3      WHEAT 124  STRAWBERRY 42  MELON 12  CARROT 5
    victor            WHEAT 139  STRAWBERRY 36  MELON 19  CARROT 6
```

Tomato reaches the board ONLY through `WHEAT_TILES_TO_TOMATO = 1` (`schedule_agent.py:3461`), which
converts wheat tiles at run time on the shop draw. Tetsuya's own two games disagree with each other
-- carrot 8 on one draw, none on the other -- which is the seed-dependence the rule exists for.

So "our crop mix matches his to the unit" is a WEAKER statement than it looks: WHEAT came out at
164, identical to the row, with TOMATO 0. The conversion never ran on this seed. A column that
matches because a rule did not fire is not evidence the rule is right. `WHEAT_TILES_TO_TOMATO`
is armed and unexercised here, and needs a draw that unlocks tomato before anything can be said
about it.

### 2026-08-19, later: the one-schedule approach is wrong, measured on 78 games

Alex: "if you only read 1 schedule how the hell can you make a bloody adaptable dynamic rule" and
"you will fit the 1 schedule and it will be broken everywhere."

Correct. The tetsuya schedule was extracted from ONE replay (94345389) and followed all night. We
hold **78 tetsuya replays**. Against them, the game we fitted is an outlier on nearly every axis:

```
    field         94345389      across 78 games
    WHEAT              164      99-187   mean 135
    STRAWBERRY          32      24-50    mean  37
    MELON                8      8-19     mean  13    <- the MINIMUM he ever plants
    CARROT               8      0-65     present in  9/78 games
    TOMATO                0      0-22     present in  4/78 games
```

#### The invariant, and the response

```
    TOTALS                       min  max   mean    sd    cv
      herd total                  15   18   15.2   0.5  0.03
      straw + melon               32   65   49.8   5.8  0.12
      tiles planted              160  246  187.7  17.8  0.09
    SPLITS
      COW                          4   12    7.6   2.8  0.37
      SHEEP                        3   11    6.4   2.7  0.43
      GOOSE                        0    5    1.2   1.4  1.16
      CARROT                       0   65    2.2   8.8  4.07
      TOMATO                       0   22    0.7   3.3  4.64
```

**His herd total is 15, cv 0.03.** The cow share of the pasture moves 0.29 -> 0.80 and CLUSTERS --
18 games at 0.80, 13 at 0.50, 16 near 0.30. Clusters are the signature of a shop draw, not noise.

So the rule is: pin the total, adapt the split.

  - pin: herd total ~15, straw+melon ~50
  - adapt on the draw: cow/sheep split, goose count, carrot, tomato
  - scale with land: total tiles planted

#### The change this reverses

`SHOP_ADAPT_HERD` -- 47 lines re-splitting cow/sheep on the shop draw -- was DELETED earlier the
same day so that the geese would come out 3/3 on game 94345389. The 78-game spread says the split
is exactly the quantity that must stay adaptive, and that a 3/3 goose match on one replay is
fitting to a draw that 35 of his 78 games do not have at all (goose is absent in 35).

That deletion should come back. Matching one tape's herd exactly is the failure mode, not the goal.

### The pivot lands: `_herd_split` now follows tetsuya

Two test files were added, both scoring at HIS DECISIONS rather than at the final board:

  - `tests/test_the_herd_split_answers_tetsuyas_shop_draws.py`
  - `tests/test_the_crop_mix_answers_tetsuyas_shop_draws.py`

**Scoring at the decision, not the census, is the whole method.** Reading the end-of-season herd and
asking the rule about it hands the rule a day-29 shop list nobody had on day 4. Each animal he put
in a pen is one question, asked with the day and the shops unlocked at that turn. That change alone
moved the measured baseline from 11.5% to 55.8% without touching a line of the rule -- the old number
was measuring the instrument.

#### What changed in `kagg/search/schedule_agent.py`

```
    1  the opening       floors to SHEEP 3 / COW 2, applied sheep-first; an EMPTY `unlocked_shops`
                         returns before the wool branch
    2  the goose         `_herd_split` carries a GOOSE bucket from the schedule row
    3  the gradient      COW = CAP - (LIMIT - draw) for draws #1-#3, replacing the two-valued step
    4  the milk line     REVERTED, -16 points
```

Placement match against his 78 games: **55.8% -> 65.6%** (779/1187).

**(1) is the biggest single defect and it was a category error.** On day 0 `unlocked_shops` is EMPTY,
and the wool branch read that as "this board has no yarn store" and committed ten cows before a
single shop had landed. An undrawn deck is not a known deck. His first five animals are
`SHEEP SHEEP SHEEP COW COW` in 78 of 78 games -- unanimous, no exceptions -- and ours were cows.

**(4) failed for a reason worth keeping.** The milk covariate is real: over his 50 late/no-yarn games
the cow count is linear in the number of milk-draining shops, 6.0 / 7.5 / 8.6 / 9.8 / 10.9 / 12.0 for
one through six of them. But it is fitted on the FINAL board and was applied to the draw SO FAR. At
day 3 two shops have landed, the milk count is near zero, and the line asks for 6 cows on a board
that ends at 12. It needs the count he could have EXPECTED, not the count visible yet. Same
census-vs-decision error as above, one level down, made an hour after correcting it.

#### カワシギ's tests: broken on purpose, xfail(strict), not deleted

One function cannot be two players. Four tests went red and Alex approved the breakage.

```
    test_the_herd_follows_the_wool_shop.py   draws #1 and #2 params -> xfail(strict)
    test_the_herd_split_answers_the_recorded_shop_draw.py
                                             ..._the_leaders_cow_count... -> xfail(strict)
```

`strict` on purpose: if the rule is ever pointed back at カワシギ these turn green and fail the suite,
which is the signal that the pivot has been undone.

`test_the_total_is_never_exceeded` was NOT xfailed. Its ceiling is a real invariant and still holds
on every input; only its `>= 12` FLOOR was wrong for the empty draw, so the empty case now asserts
the opening and every other assertion stays live.

#### Still open

  - 65.6% -> 80%. The residual is largely ORDER, not mix: he exhausts all three sheep before the
    first cow, and `_herd_split` returns counts while ordering lives in the caller's pen siting.
  - the milk covariate, re-fitted on EXPECTED final shops rather than visible ones.
  - the crop side, untouched: `WHEAT_TILES_TO_TOMATO = 1` fires on 78/78 boards where he plants
    tomato in 4/78, and `SHOP_ADAPT_CROPS = False` leaves nothing connecting the draw to the crop
    choice while his carrot ranges 0-65 tiles.

### Where the herd rule actually fails, and why the milk line could not fix it

#### Scoring per DAY, order-free inside it

`_herd_split` returns COUNTS. Which pen a hand reaches first comes from the schedule row via
`_outstanding_places`, so charging the split for his sheep-first opening scores it for something it
does not control. Order-free per-day scoring: **65.6% -> 77.9%**. Twelve points of the apparent gap
was the instrument again.

#### The failure is entirely in the back half

```
     day   placed   right    rate    shops drawn by then
       0      390     344   88.2%    ~0
       3       78      70   89.7%    ~1
       4      148     139   93.9%    ~1
       7      124     110   88.7%    ~2
       9       98      66   67.3%    ~3
      10       99      63   63.6%    ~3
      11      143      86   60.1%    ~3
      12       67      32   47.8%    ~4
      13       29      12   41.4%    ~4
     season  925/1187 = 77.9%
```

d0-d7 is ~90%. It collapses from d9. The opening and the first two draws are solved; every remaining
error is late, which is Alex's read exactly -- "d0-d3 we know and then it gets more than 1 decision
d6 d9 d12".

#### The milk line: measured twice, negative twice, and the second run explains the first

```
    visible milk count, fitted on the final board      65.6% -> 46.4%
    expected final milk, undrawn at 3/8 each            65.6% -> 63.0%
    flat WOOL_SHOP_NO_YARN_COW                          65.6%
```

The expectation correction recovered thirteen of sixteen lost points, so reading a partial draw as
final WAS a real defect -- but not the only one. **A linear fit to a bimodal response lands between
both modes and matches neither.** His late/no-yarn boards cluster at COW 6 and COW 12; the per-milk
means of 6.0 ... 12.0 are averages OVER that split, not a trend within it. At three milk shops nine
boards go low and eight go high, so the fitted 8.6 is a value he essentially never plays. Both
reverted, both recorded in place.

A rule that beats the flat number must CLASSIFY, not interpolate.

#### The classifier is probably the OPPONENT -- Alex's call, and it survives a control

```
     yarn store in draws 1-3       n     his sheep share
       opponent sheep <= 4        59          0.97
       opponent sheep >= 5        86          0.99      no opponent effect
     yarn store late or absent     n     his sheep share
       opponent sheep <= 4       198          0.41
       opponent sheep >= 5        15          0.07      strong, crowding direction
```

Uncontrolled, the opponent's sheep count predicts his choice in the WRONG direction -- both players
go sheep together, which is the signature of a common cause, and the common cause is the shared shop
draw. Controlled for the draw the picture inverts and sharpens: where the draw is informative the
opponent is irrelevant (0.97 vs 0.99); where the draw says nothing the opponent decides, and a
sheep-heavy opponent pushes him to cows.

That is a candidate for the bimodality the milk line could not reach. **n=15 in the deciding cell.**
One thin cell carrying the claim: a lead, not a result. It needs more late-yarn games before any
code is written against it.

**This "opponent lead" claim is superseded by the 2026-08-20 finding below** — re-measured at the
game level (not the placement level) it disappears. See the 2026-08-20 section.

### The herd clears the bar: 81.9%

Two more fixes after the first commit (`2b28fe1`):

  - **the goose is held to `GOOSE_FROM_DAY = 6`.** Offered at day 0 the bucket was spent on the
    opening and displaced a sheep -- a miss twice over, the goose early and the sheep missing. He
    places his first bird on d6 and nothing at all on d0-d5: d6:3 d7:8 d8:3 d9:9 d10:8 d11:28 d12:23
    d13:13. **Day 0 went from 88.2% to 100.0%, 390/390.**
  - **the tomato tile is gated on the draw.** See below.

```
     day   placed   right    rate
       0      390     390   100.0%
       4      148     140    94.6%
       7      124     110    88.7%
       9       98      66    67.3%
      11      143      86    60.1%
      13       29      12    41.4%
     season 972/1187 = 81.9%
```

The whole remaining error is d9 onward, and the opponent lead above is the only candidate that
reaches it.

### The plant side

#### Tomato is a shop response and is now gated on one

```
    tomato-draining shops    0    1    2    3    4    5
    games                   10   24   25    9    7    3
    games with tomato        0    0    1    0    1    2
```

Not one tile across all 34 games with fewer than two draining shops. `TOMATO_DRAIN_SHOPS_NEEDED = 2`
is added to the existing `melon_armed and not q4_armed` conditions. A GATE, not a size -- the tile
count is untouched, so the only change is which boards get it.

#### Three false premises in one session, all the same mistake

This is the one worth carrying forward. Three assertions were written against a NAME instead of the
BRANCH that reads it, and all three were wrong:

  1. "`WHEAT_TILES_TO_TOMATO` fires on every board, unconditionally" -- taken from its own docstring.
     The use site has gated it on `melon_armed and not q4_armed` all along.
  2. "`SHOP_ADAPT_CROPS = False`, so nothing connects the draw to the crop choice" --
     `STRAWBERRY_TILES_BY_DRAIN` caps strawberry on the draw and runs OUTSIDE that flag.
  3. "`_herd_through_day` re-labels every head, so a goose cannot survive" -- it iterates COW and
     SHEEP only and leaves other species alone.

And a fourth was caught before it shipped: the tomato gate was first written against the local
`unlocked`, which is `unlocked_quadrants`. Quadrant names never match shop names, so it would have
scored 0 on every board and switched the tile permanently off while reading like a working gate --
a silent null. `CLAUDE.md` already says "print the name the code actually reads before any A/B";
the docstring is not the name.

#### Carrot has no predictor and no gate was invented for it

Carrot's nine games sit at drain counts 1,1,1,2,2,2,3,3,3 -- evenly spread -- and the five games
with FOUR draining shops have none. Non-monotone, so drain count is the wrong variable. Its
first-planted day splits into two clusters, d6-d10 and d25-d27, so the late one is end-of-season
opportunism on leftover ground rather than a crop plan at all.

`test_carrot_is_the_crop_with_no_predictor_yet` pins the non-monotonicity so nobody fits a line to
it -- which is exactly what cost sixteen points on the herd side -- and says to replace itself when
a predictor is found.

---

## 2026-08-20 — The milk classifier, and the death of the opponent lead

Folded in from `docs/the_greedy_is_a_mix_scorer_2026-08-20.md` (this document's own prior content;
continues the section immediately above).

Herd placement match against tetsuya's 78 recorded games: **81.9% -> 88.5%** (1051/1187).

### The opponent lead is DEAD, killed by using the right unit

2026-08-19 reported that on late/no-yarn boards a sheep-heavy opponent pushes him to cows, 0.41 ->
0.07 sheep share (see "The classifier is probably the OPPONENT" above). That was measured over 213
PLACEMENTS. Those come from ~50 games, and a game contributing twelve animals is one decision
repeated twelve times, not twelve independent observations -- textbook pseudo-replication. A handful
of games with sheep-heavy opponents each contributed a dozen rows and carried the whole effect.

Re-measured at the GAME level, 50 late/no-yarn games:

```
    variable                his COW<=7   his COW>=8      gap
      opp COW at d9             6.05         6.00       -0.05
      opp SHEEP at d9           3.95         3.77       -0.17
      opp COW final             9.42         9.10       -0.32
      opp SHEEP final           3.84         3.55       -0.29
```

Nothing. The reason is visible in the per-game rows: his opponents sit at COW 6-8 / SHEEP 4 in
almost every game, because the ladder pool plays alike. **A variable with no variance cannot explain
a response.** The lead was raised and killed inside two messages.

**This is the correction to 2026-08-19's "opponent lead" section above: the placement-level n=15
result does not survive re-measurement at the game level. The 2026-08-19 finding is kept in place,
labelled superseded, because the pseudo-replication mistake it embodies is itself worth keeping on
record.**

### It was the milk count all along -- as a THRESHOLD, read at the DECISION

Same 50 games, every other candidate flat to three digits:

```
    quadrants @d9      2.00 vs 2.00        shops drawn @d9   3.00 vs 3.00
    money @d9       2760.58 vs 2693.94     yarn stores @d9   0.00 vs 0.00
    milk shops @d9     0.68 vs 1.81   <--
    milk shops @d12    0.95 vs 2.23   <--
```

As a classifier rather than a slope:

```
    milk@d9 >= 1  -> high cow    37/50 = 74.0%   (fp 13, fn 0)
    milk@d9 >= 2  -> high cow    40/50 = 80.0%   (fp  0, fn 10)
    always-high baseline         31/50 = 62.0%
    milk@d9 <  2: n=29 mean COW  7.21
    milk@d9 >= 2: n=21 mean COW 11.33
```

**Twenty-one of twenty-one games with two milk shops by d9 go high-cow. Zero false positives.**
"Two milk shops implies a big herd" holds without exception; the converse does not, and does not
need to.

`MILK_SHOPS_FOR_A_BIG_HERD = 2`, `COW_ON_A_MILK_RICH_BOARD = 12`, `COW_ON_A_MILK_POOR_BOARD = 7`,
gated from `MILK_CLASSIFIER_FROM_DAY = 9`.

#### The same variable failed twice before this

```
    visible milk count, LINE fitted on the final board     65.6% -> 46.4%
    expected final milk count, LINE, undrawn at 3/8        65.6% -> 63.0%
    milk count at d9, THRESHOLD                            81.9% -> 88.5%
```

Three attempts, same variable, and the first two were negative. The variable was never the problem.
**A linear fit to a bimodal response lands between both modes and matches neither** -- his boards
cluster at COW 6 and COW 12, so the per-milk-count means of 6.0 ... 12.0 are averages OVER a split,
not a trend within it, and the fitted 8.6 at three milk shops is a value he essentially never plays.

The lesson is not "milk shops don't work". It is: **before fitting, ask whether the response is a
gradient or a mixture.** A gradient wants a line; a mixture wants a classifier, and the mean is the
worst single guess for a mixture.

### Where the season now stands

```
     day    before    after
       9     67.3%    73.5%
      10     63.6%    79.8%
      11     60.1%    82.5%
      12     47.8%    76.1%
      13     41.4%    55.2%
     season  81.9%    88.5%
```

d13 at 55.2% is the weakest day left, on 29 placements.

### カワシギ: four more xfail(strict), still nothing deleted

`test_a_late_yarn_store_still_leaves_the_herd_cow_heavy`,
`test_the_split_matches_the_leader_on_three_quadrants[shops4/shops5]`,
`test_the_common_board_is_untouched`. All four assert HIS numbers -- the "common board" is his 42 of
51 seats, and its board carries two milk shops, which the classifier now reads as milk-rich. Suite:
21 passed, 16 xfailed.

## 2026-08-10 — Step 1 is a ledger, not a flag

Folded in from `docs/the_day_is_a_cash_ledger.md`.

> TARGET SUPERSEDED, noted 2026-08-11 in the source. The day being diagnosed here funds Seb's tape,
> which was optimal under the old `townCenterSellInterval=12` economy. His median bank halved and he
> withdrew from the ladder (2,744 ladder seats, see the ladder-strategy document). The `short_of_cash`
> bug described below is still a real bug in the ledger logic. Only the schedule it funds is now a
> suboptimal target.

Alex, 2026-08-10, correcting the `sell_deadline` design built the same day.

**What is wrong.** `schedule_agent.sell_deadline(hour, selling, short_of_cash)` returns one hour, and
`short_of_cash` is one boolean over the whole day's bill:

    short_of_cash = FUND_THE_DAY_WHEN_SHORT and any(owed_sale.values()) and _days_bill(row) > money

On day 4 that reads:

    cow    400   needed at h0    <- covered by the $480 dawn bank, needs no sale at all
    land  1000   needed at h21   <- the only thing the day's produce has to fund
    hires   33   h0
    wheat  ~28   h0
    ----------
          ~1461  vs $480         ->  short_of_cash = True  ->  due = 0, rush = True

A purchase not due until h21, and a purchase already paid for, are added into one number and turned
into "deliver everything at hour 0." That forces the rush on d4.

**What the day actually is.** Read off tape 91422988, day 4, Seb's own seat. Four sell waves, three
buy points:

    h0    BUY_ANIMAL COW       -400      from the dawn bank
    h0    HIRE x7               -33
    h2    BUY_PRODUCT WHEAT    ~-28
    h18   SELL WHEAT 5         +165
    h21   SELL FERTILIZER 5, SELL WHEAT 12
    h21   BUY_LAND            -1000      funded by the two SELLs in EARLIER ORDER SLOTS of this turn
    h22   SELL WHEAT 12        +239
    h23   SELL WHEAT 20, SELL FERTILIZER 1

He sits on $12 from h2 to h18 and it costs him nothing, because nothing he owes is due before h21.

Ours, same day, same board:

    h0    BUY_ANIMAL COW, BUY_PRODUCT WHEAT      $480 -> $15 by h2
    h6    SELL FERTILIZER 1, SELL WHEAT 1
    h7    SELL WHEAT 1
    h14   SELL WHEAT 8
    h16   SELL WHEAT 16
    h18   BUY_PRODUCT WHEAT 5                    -$154
    h19   SELL WHEAT 5
    h21   SELL FERTILIZER 2, BUY_LAND            -> $115
    h22   --
    h23   --                                     dusk $115 against his $1115

Two differences, both caused by the scalar: we sell early and small into a book that has not
recovered, and we stop selling the moment the parcel is bought while he sells 12 more at h22 and 21
more at h23.

**The shape step 1 should have.** Emit a ledger, at dawn, from the row and the live bank:

1. Dated obligations: `[(hour, cash)]`, one per thing the row buys, at the hour it is bought.
   Animals and hires are h0. Land is its own hour. Feed and seed buys are theirs.
2. Opening balance: the live bank, not the row's `money_dawn` (a different farm's).
3. The shortfall curve: walk the obligations in hour order against the balance. The first hour the
   running balance goes negative is the first hour the day genuinely needs a sale, and the deficit at
   that hour is how much. Everything before it needs nothing.
4. Delivery obligations: turn each deficit into "this many units of this product in the SHED by this
   hour" at the prices the row implies -- `cover`'s `due`, as a small list, not an int.
5. Sell waves: spread the sells so the book recovers between them, and keep selling after the last
   purchase. `market_price` falls as town inventory rises; measured, landing a load in two DROP waves
   banked **$542 for 54 units** where four waves banked **$774 for 41**.

Day 4 under that model asks for nothing before h21, then $1000 by h21, then sells the remainder at
h22 and h23 -- which is the tape.

**Why `feed 6/7` and `care 6/7` are downstream of this.** The cow lands at h0 and takes the bank to
$15 by h2. The seventh animal's wheat is then unaffordable for the rest of the morning, so it is
neither fed nor cared for. That row is a cash-sequencing failure, not a routing failure, and no
amount of lane cutting closes it.

**Measured, so it is not re-derived.**
- Staggering the hires to keep hands off `(5,5)` is a LOSS on day 4, per `_arrival_plan`'s docstring.
  Baseline d4 matches `water 17/17`, `harvest 14/14`, `place 1/1`; with staggering those go to
  16/17, 12/14, 0/1. Two boxed hands cost d4 nothing measurable, because six seats already covered
  every tile.
- The tape boxes hands too: Seb's `u2` and `u6` sit on `(5,5)` doing nothing on d0, d1 and d3, and
  one of them on d2 and d4. It stops at d5, when he owns a second quadrant.
- `_days_bill` does count the cow. The bug was never a missing term; it was adding terms with
  different due dates together.

## 2026-08-17 — Why the d5-d11 tape replay cannot converge on his board

Folded in from `docs/replay_window_cannot_converge_2026-08-17.md`.

Measured 2026-08-17, seed 11, weeds 0.0, `REPLAY_OPENING_DAYS = (5, 6, 7, 8, 9, 10, 11)`. Both
three-quadrant tapes. Logs: `data/logs/replay_q3_both_tapes_fixed_2026-08-17.log`,
`data/logs/replay_failed_ops_2026-08-17.log`, `data/logs/his_three_tiles_2026-08-17.log`.

**The argument that made this measurable.** Inside the replay window the actions are his. If the
tape is his and the replay is faithful, the two boards must converge day for day. Any mismatch
inside the window is a defect, not a strategy difference. That turned a vague "we are behind" into
three named tiles.

**What the grid said.** Every cell is ours/tape of the same quantity, at the end of that day.

```
=== --tape kawashigi (his MELON season)        d6      d7      d8      d9     d10     d11     d12
melon                                       14/14   20/20   20/20   20/20    11/8    11/8    13/8
strawb                                        2/4     5/7    9/11    9/11    9/11   25/27   28/34
weeds                                         0/0     0/0     0/0     1/0     1/0     1/0     0/0
money  d6 959/957   d8 1433/1431   d10 12374/16162

=== --tape kawashigi_b3 (his STRAWBERRY season)
melon                                       12/12   12/12   12/12   12/12     3/0     3/0     0/0
strawb                                        4/6     6/8   17/19   17/19   17/19   35/37   36/39
weeds                                         0/0     0/0     0/0     1/0     1/0     1/0     0/0
money  d6 1570/1566   d8 1227/1223   d10 13020/16403
```

Strawberry is exactly **-2** every day from d6, in both arms, constant rather than compounding.
Melon is exactly **+3** at d10, in both arms. Money tracks him to within $4 at d6 and d8, then loses
$3.4k at d10 -- the same day as the melon gap.

**The three tiles.** Replaying the window and resolving each PLANT and HARVEST against the board it
landed on gives 5 failures out of 71-73 watched ops, identical in both arms:

```
day  h   op       item        tile     before        after
  5 14  PLANT    STRAWBERRY  (0,0)    MELON         MELON      refused
  5 14  PLANT    STRAWBERRY  (1,1)    MELON         MELON      refused
  8 11  HARVEST  -           (3,0)    MELON         MELON      refused
  8 12  PLANT    WHEAT       (3,0)    MELON         MELON      refused
 10 19  PLANT    WHEAT       (3,2)    empty         empty      refused
```

His own board on the same tiles, read from the raw replay at each dawn:

```
 day  (0,0)        (1,1)        (3,0)     (3,2)
   1  WHEAT        WHEAT        WHEAT     MELON
   4  WHEAT        WHEAT        WHEAT     MELON
   5  None         None         WHEAT     MELON
   6  STRAWBERRY   STRAWBERRY   WHEAT     MELON
  11  STRAWBERRY   STRAWBERRY   WHEAT     WHEAT
```

**Our d0-d4 plants MELON on (0,0), (1,1) and (3,0); his plants WHEAT.** Wheat planted on d1 is ripe
and cleared by d5, freeing the tile for his d5 h14 strawberry. Melon planted on d1 stands until about
d10. So his d5 strawberry and his d8 wheat both land on an occupied tile and are refused -- the
divergence is permanent from d5.

One root cause explains both numbers: melon `+3` is these three tiles still standing; strawb `-2` is
two of them that should have become strawberry at d5 h14; the third, (3,0), should have become wheat
at d8. (3,2) is separate and smaller -- the tile is EMPTY on our board when his d10 wheat plant
arrives, so the refusal is not an occupancy problem; not diagnosed, seeds are the first thing to
check.

**The fix, and what it measured.** `OPENING_GEOMETRY` in `schedule_agent.py` pins the six squares to
the crop he sows, seated before the sweep. Each pin spends its own crop's outstanding count, so the
day's totals are untouched -- a permutation of the same plantings. `OPENING_GEOMETRY_LAST_DAY = 4`
keeps it out of mid-season. Test:
`tests/test_the_opening_sows_the_fast_crop_where_the_strawberry_goes.py`, red before, green after.

Replay window d5-d11, both arms, seed 11:

```
                          BEFORE (ours/tape)          AFTER (ours/tape)
=== MELON arm            d10     d11    d12         d10     d11    d12
melon                   11/8    11/8   13/8         8/8     8/8   11/8
strawb                  9/11   25/27  28/34       10/11   26/27  28/34
money d10             12374/16162                16242/16162

=== STRAWBERRY arm
melon                    3/0     3/0    0/0         0/0     0/0    0/0
strawb                 17/19   35/37  36/39       18/19   36/37  38/39
money d10             13020/16403                16486/16403
```

Melon is now EXACT at d10 and d11 in both arms; the `+3` is gone. Strawberry closed from `-2` to
`-1`. Money at d10 moved from $3.4k-$3.8k behind to level. Refusals inside the window fell from 5 to
**1**, the same one in both arms:

```
 day  h   op      item        tile     before   after
   5 14  PLANT   STRAWBERRY  (0,0)    WHEAT    WHEAT    refused
```

The wheat is in the right place now and is not cleared in time. His (0,0) is already empty at dawn on
d5 -- he harvests it during d4, our own day. That d4 harvest is the next defect, worth exactly the
remaining strawb `-1`.

Season money is not measurable yet: `solved_days*.py` was solved on the old geometry and
`_apply_precomputed` keys a stop on `(tile, ops)`, so the swapped squares' stops now drop rather than
adapt. d12-d29 needs re-solving on all four arms before any season total means anything.

**What this does and does not say.** It does **not** say the replay is broken -- 71 of 76 of his
watched ops succeed. It does say the replay's ceiling is set by our own **d0-d4 crop assignment**,
which the window does not touch. Taping earlier days is the mechanical fix and was measured worse
(`tape d4-d11` and `tape d3-d11` both 127,185 against 143,454 for d5-d11). The interesting, unmeasured
fix is the other direction: put wheat rather than melon on (0,0), (1,1) and (3,0) in our own d0-d4
rows, so a fast crop frees the tile the way his does.

**Season money, for the record.** Every replay variant still loses on seed 11. Our own d0-d29 banks
**153,492**; the best replay window (d5-d11) banks **143,454**. The replay is a diagnostic here, not
a candidate.

**Two bugs found on the way.**
- `replayed` keyed its tape lookup on `state["branch_armed"]`. Nothing writes that name --
  `MelonBranch.armed_key` is `"melon_armed"` -- so the melon latch was pinned False and the
  strawberry tape was unreachable by construction. The strawberry arm silently replayed his MELON
  season, which is what made the first `kawashigi_b3` grid read `melon 20/12`. Now read through
  `_MB.BRANCH.armed_key` so it cannot go stale again.
- `state["bought"]` kept the discarded planner's purchase increments on replayed turns, handing d12 a
  herd nobody ordered. Snapshotted and restored, then advanced by what the tape actually orders.

**The COW/SHEEP substitution.** Built. On a replayed turn the species token in `BUY_ANIMAL`,
`PICKUP` and `PLACE` is re-decided by `_herd_split`, keeping the tape's count, hour and pen. Both
species live on a PASTURE, so no pen, walk or route stop moves; only the bill does, $400 against
$500. On seed 11 it is a no-op by agreement: the live branch targets `WOOL_SHOP_NO_YARN_COW = 10`
cows and the season herd is 14, giving COW 10 / SHEEP 4, exactly what the tape buys. Forcing the
target to 6 cows relabels d9 and d11 and lands COW 6 / SHEEP 8 with pens and herd size unchanged --
`tests/test_a_replayed_day_buys_the_species_the_shops_ask_for.py`, and two of its three tests go red
when the substitution is disabled.

**Caveat that matters:** `breakdown.run` forces the tape's RECORDED shop draw onto both columns, so
under that harness the herd target is pinned by the tape on every seed. The substitution is
structurally invisible in every grid in this document. Measuring it needs a harness with a free town
draw.
