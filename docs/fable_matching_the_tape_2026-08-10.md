> **TARGET SUPERSEDED, added 2026-08-11.** This doc matches the schedule against Seb's recorded
> tape, which was optimal under the OLD `townCenterSellInterval=12` economy. Seb's own median bank
> halved ($137,747 -> $77,737) when the town rebalance landed and he has since withdrawn from the
> ladder (`docs/the_ladder_is_two_scripts.md`, measured from 2,744 ladder seats). That doc says
> explicitly: "it is not the planner, the watering or the market logic; it is the target." The bugs
> found and fixed below are real bugs and still stand — read `the_ladder_is_two_scripts.md` before
> treating "matches the tape" as the goal. The field plants 108-147 WHEAT tiles a season; we plant 24.

# d4 sell shortfall and d9/d10 place 0/4 — measured 2026-08-10

Everything below is measured on `tape seb2988`, seed 11, `weeds 0.0`, module `schedule_agent`,
against `data/seed_scripts/top_guys/91422988.json` / `.../schedule.json`, on branch
`shaping-potential` at the tree as handed to me (uncommitted `docs/REGISTER.md` diff, plus
`scripts/diagnose_season.py` and `submission/main_replay11.py` untracked — neither touched).
Read-only throughout; no source file was changed.

Every measurement script is written to the session scratchpad
(`/private/tmp/claude-501/.../scratchpad/`) and its output is also saved under
`data/logs/fable_*.log` in this repo for anyone who wants the raw trace. I flag inline which claims
are **measured** (I ran it and read the output below) versus **inferred** (read from the code and
not independently executed).

**Caveat, load-bearing: the working tree was being edited by someone else while I worked, read-only,
in the same directory.** `git status` at the end of my session shows uncommitted changes to
`kagg/search/cover.py`, `kagg/search/router.py`, `kagg/search/schedule_agent.py`,
`scripts/breakdown.py`, `tests/test_the_first_seven_days_match_the_plan.py` and `docs/REGISTER.md`
that I did not make (I only ever used `Write`/`Edit` on this report and on scratchpad files under
`/private/tmp/...`). File mtimes: `cover.py`, `router.py`, `breakdown.py`, `docs/REGISTER.md` and
the test file all predate my first tool call (Aug 9 22:27-Aug 10 08:06, my session started ~09:27),
so everything I quote from those files is stable and was not moving under me.
**`kagg/search/schedule_agent.py` changed at 09:55:30, inside my session window**, and the
diff (`FEED_DAYS 2->1`, a new `WALK_THE_LOAD_HOME` flag, `CARE_WHAT_YOU_STAND_ON` False->True, a new
`day` parameter threaded into `_solve`) is squarely in the same territory as Q1/Q2 below — someone
else appears to have been actively working the d4 late-delivery/sell question at the same time I was
measuring it. I re-checked every line number I cite against the file as it stands now (all my
`grep`/`Read` calls for exact line numbers were re-run after that edit landed) and the CONTENT at
each cited location is unchanged from what I traced against — only line numbers shifted from
insertions earlier in the file. But if this file moves again before anyone reads this, the line
numbers below will drift again; the constant names and the quoted code will not.

---

## Q1 — why does d4 sell only ~41 of 55 while Seb sells 55

**Measured. Not the order book, not the price curve, not "produce not in the shed."** It is our own
`DUSK_FEED_TOPUP` block re-buying wheat the sell block just sold, same turn, from hour 18 onward.

### The baseline numbers

`python -u scripts/breakdown.py --module schedule_agent --tape seb2988 --days 7`
(full table in the session; the d4 column):

```
sell         41/55       buy_product   21/1
```

The schedule row for d4 (`data/seed_scripts/top_guys/91422988/schedule.json`, key `"4"`) is
`"sells": {"WHEAT": 49, "FERTILIZER": 6}` (= 55) and `"buys": {"WHEAT": 1}`. So the tape's `sell 55`
in the breakdown table is not an artifact of the tape column being degraded (per
`docs/the_tape_column_does_not_replay_his_game_2026-08-09.md`) — it is corroborated directly by the
schedule row Seb's own tape produced it from, and 5+12+5+12+20+1 = 55 sums exactly from his own
recorded orders (below). This IS a real target.

### Hour-by-hour, both sides, direct from `_process_market`

Script: `scratchpad/d4_trace.py` (this file was subsequently overwritten by something else in the
scratchpad between my run and now — the log at `data/logs/fable_d4_trace.log` is the surviving
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

### The mechanism, proved from the code

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

### End-of-day wheat is 0/0 both sides

The breakdown table's d4 `wheat` row reads `0/0` — neither side is left holding stranded wheat. The
14-unit shortfall (55 sold vs 41) is wheat that got bought back and then fed to animals rather than
sold, not wheat that vanished. So the cost of this defect is not a stranded-goods loss; it is the
**spread**, paid twice on roughly 20 units a day from h18 on — sell low, buy back higher, repeat —
plus every one of those round trips occupies an order slot and a market-lockstep iteration that buys
nothing. Money at d4 end: 774/1063 (ours/tape), a ~$289 gap, consistent with a repeated wash trade
though I have not isolated exactly how much of that gap is this mechanism versus everything else
that differs by dusk. **Money is downstream evidence here, not the target** — the target is the op
count, and `sell 41/55`, `buy_product 21/1` are both directly this mechanism.

---

## Q2 — is the fix to match the WORK ORDER (harvest early, deliver, sell in bursts), not the sell block

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

So this is squarely in "tune the sell/buy interaction," not "match the day's work order." I did not
design or test a fix (out of scope, read-only), but the shape one would need is: make
`DUSK_FEED_TOPUP`'s floor agree with what the sell-side reserve (`:2909-2933`) already believes is
reserved, rather than two independent computations of the same `feed_days(day) * alive` quantity.

---

## Q3 — why cover leaves 8 of 10 d9 placements unassigned, and why the 2 it does route emit nothing

**Measured, in three layers, and they chain into one cause.** `place` reads `0/4` on both d9 and
d10 (breakdown table). This is not a turn-budget problem — d9 measured 277 unit-turns of budget
against 155 used by other work, i.e. 122 turns free (`scratchpad/d9_place_trace.py`,
`data/logs/fable_d9_place_trace.log`).

### Layer 1 — all 10 open pens are typed "PLACE COW", none "PLACE SHEEP"

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

### Layer 2 — the animals the model expects were never bought

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
(`docs/REGISTER.md` OPEN-CLI: "Shop-adaptive herd shipped and measured; floors still open") — what I
am adding here is the specific causal link from it to `place 0/4`.

So the dawn plan is built against a purchase that never happens: 10 pens get typed and routed on the
assumption of 2 COWs arriving; 0 COWs ever arrive; the 4 SHEEP that *do* arrive all day are never
offered as a placement target at all, because no node was ever typed SHEEP.

### Layer 3 — the 2 routed jobs draw against an empty shed and are abandoned, silently

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

---

## What I did not verify

- I did not independently re-derive that the "101 idle unit-turns" figure quoted in the prompt is
  exact — my own instrumentation measured **122** idle turns on d9 (277 budget − 155 used before any
  closing trips), a different number in the same direction (large free capacity, ruling out a
  turn-budget explanation). I did not reconcile the two figures; both support the same conclusion.
- I did not check whether `SHOP_ADAPT_HERD`'s species reallocation is itself a good idea in
  aggregate (REGISTER already logs it as shipped-and-measured, floors still open) — only that it is
  the direct, provable cause of `place 0/4` on d9 and d10 via the plan/purchase mismatch above.
- I did not test or write a fix for either Q1 or Q3, per the read-only instruction. The mechanism
  for each is pinned to specific line numbers above so a fix can be scoped without re-deriving this.
- The d4 hour-by-hour trace script (`scratchpad/d4_trace.py`) was overwritten by something else in
  the scratchpad after I ran it; the numbers quoted above come from the saved log
  (`data/logs/fable_d4_trace.log`), not a re-run against the current file on disk.
