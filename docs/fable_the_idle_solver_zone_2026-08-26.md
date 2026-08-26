# Fable on the d12-d23 idle: why the solver parks hands next to ripe crop

Run 2026-08-26 against `docs/where_the_turns_go_d12_d29_2026-08-26.md`.
Fable read `kagg/search/cover.py`, `kagg/search/schedule_agent.py` and the docs; it ran no jobs and
changed no code.

**Line numbers below are Fable's and have not been independently re-checked by me.**
Verify before acting on any of them.

---

## 1. Why the solver idles next to reachable ripe crop, d12-d23 only

The zone boundary is not "solver vs planner" in the abstract -- it is
`UNSOLVE_DAYS = tuple(range(24, 30))` at `kagg/search/cover.py:967`.
d12-d23 are seated from `PRECOMPUTED_ROUTES`; d24-d29 run the live greedy.
**The idle stops exactly at the day the fixture routes stop being used.**

The mechanism is a chain, and every link is in the code:

**Link 1 -- the fixture routes park hands by design.**
The offline solve's objective is "cover every job, ties broken on fewer turns" (cover.py:6, :84-88).
Minimizing turns after coverage concentrates work: the d12 solve "seats 47/47 in 169 turns with TWO
hands never leaving the shed" (cover.py:907-909).
d12 crew is 11 hands x ~23 turns ~= 253 unit-turns; the plan spends 169.
On the fixture board that surplus is free.
Fixture stops-per-hand confirm the shape: d15/d17/d18 (crew 13) carry 4.5-4.8 stops/hand vs d14
(crew 9) at 6.6 -- measured from `solved_days.py`.
That is why big-crew days idle worst and d14/d16 barely idle: small-crew days have no surplus to
park.

**Link 2 -- the live board has more work than the fixture board, and the surplus grows itself.**
A stop is seated only on an exact `(tile, ops)` key match (`_apply_precomputed`, cover.py:1020,
:1026).
Ladder boards drift from the fixture (opponent-dependent shed/market, and -- the feedback loop --
our own standing-crop lag of 15-20 units means today's board holds ripe tiles the fixture board
never had at this date).
Drifted jobs fall to `left`.

**Link 3 -- on a solved day, `left` gets one chance and the failures are silent.**
`cover()` at cover.py:1160-1162 does `pre = _apply_precomputed(...); if pre is not None: return pre`.
**The greedy passes, COMPACT, REPAIR and MAKE_ROOM never run on a solved day.**
Leftovers go through a single cheapest-insertion pass (`_insert_leftovers`, cover.py:1119-1146);
whatever does not fit is returned as `over` -- and `_solve` discards it:
`out, _uncovered = DP.plan(...)` at schedule_agent.py:635, `_uncovered` never read.
COMPACT exists precisely because "sixteen spare unit-turns across thirteen hands is 1.2 each, and
nothing costs 1.2 turns" (cover.py:120-131) -- and it is unreachable in the exact zone that idles.

**Link 4 -- insertion is priced against an inflated cost model.**
`deliver = max(budget) > DELIVER_CUTOFF_TURNS` with the cutoff at 99 (schedule_agent.py:66, :633),
so `deliver=False` on every ordinary day, and `materialise` under `deliver=False` fires the
`stranded` rule (cover.py:762-766): each yielding leftover whose product is in the sell row buys its
own mid-tour shed round trip.
The recorded example: the same work sequence priced 21 turns with `deliver=True` and 29 with
`deliver=False` (cover.py:1208-1213).
So a parked hand with 23 free turns "fills up" after two or three harvest insertions.

**Link 5 -- the executor cannot recover any of it.**
Once `st["route"]` is empty the hand PASSes to dusk; the only fallback is walk-home-if-carrying
(schedule_agent.py:2512-2522).
`thirsty_claimed` at schedule_agent.py:2091 is initialized and **never read** -- grep count 1 -- the
idle-pull it was for does not exist.
`underfoot()` fires only while walking a non-empty route.

### Discriminating measurements, cheapest first

1. Patch a print into `_solve` (schedule_agent.py:635) logging `day, len(jobs), len(_uncovered)` and
   rerun one recorded seed.
   If `_uncovered` is ~0 on d12-d23, links 2-4 are wrong and the idle is pure link-1 parking
   (fixture never offered the work to those hands); if it spikes on d12/d15/d18, links 3-4 carry it.
2. Log `PRECOMPUTED_MISSES` (cover.py:988) per day on the same run -- sizes link 2 (drift).
3. Sum `budget[u] - cost` over hands per day at dawn -- sizes link 1 (parked capacity) against the
   measured PASS excess (+44.9 on d12).

## 2. Fixes that do not require replanning

All dawn-plan or per-turn-local; none re-solves mid-day.

1. **Fall through after `_apply_precomputed` instead of returning** (cover.py:1160-1162): treat the
   seated fixture routes as the greedy's initial state, then run the existing COMPACT + greedy-top-up
   + REPAIR passes on `left`.
   The code is all already below that line; the change is control flow.
   Risk is wall time -- the full greedy from scratch on d12-16 is what disqualified 55352401
   (cover.py:1289-1294) -- but this runs the passes only over the leftover residue with routes
   mostly pre-seated, and `MEMOISE_SLOT` has landed since.
   Measure dawn-solve wall time on the densest day before shipping.
2. **An executor-level harvest scavenger for route-empty hands.**
   The prior top-up failed because a rebuilt PLACE/FEED/CARE route never got a walk home
   (schedule_agent.py:2072-2078).
   A scavenger restricted to HARVEST does not have that defect: a hand that harvests is then
   carrying, and the existing carrying-fallback at schedule_agent.py:2512-2522 already walks it home
   and DROPs.
   Claim coordination already exists (`_claimed_tiles`, schedule_agent.py:1479).
   Targets the measured 191 unclaimed-ripe turns and touches nothing about planning.
3. **Re-solve the fixtures with a capacity-using objective** -- offline only.
   Keep "cover every job" but break ties toward spreading stops across all hands (the greedy's own
   fair-share cap, cover.py:1360-1378, is the argument: parked capacity is not free when the board
   can drift).
   Every hand then has slack where leftovers land. No runtime change at all.
4. **Charge leftover insertion at the cost the day will pay** -- the `deliver=False` inflation
   (link 4) makes `_insert_leftovers` refuse work the day could do.
   Narrow change: price insertions on solved days without the `stranded` round trip (the overnight
   sweep banks d12-d23 loads free, `kaggriculture.py:812` per cover.py:547-549).
   SPECULATION on size; measure with discriminator 1 first.
5. **Extending `UNSOLVE_DAYS` down to d12** is the blunt A/B and worth one run for calibration, but
   it is not the fix: the solved days exist because the greedy both under-covered (45/47 vs 47/47,
   cover.py:907-909) and overran the time budget.
   Use it as a measurement arm, not a ship candidate.

## 3. Win big / lose small on Elo -- Fable's blunt answer

The shape itself is a distraction; the asymmetry it implies is not.
A $106k win and a $94 win are identical to the ladder, so **any surplus in won games is worthless,
and every change should be judged only on whether it moves the ~$2k band** -- 6 of 13 losses are
under $2,000.
The idle fix is exactly that kind of change: 191 unit-turns beside ripe crop plus 14 units left at
the bell is plausibly $1-3k of floor in a contested game, which is the loss median.
Do not build anything that targets the shape directly (no "play safe when ahead" logic -- you cannot
see the opponent's bank reliably anyway).

One open thread worth a look before dismissing: wool 70.7 in losses vs 103.3 in wins with the
confirmed we-flood-our-own-book mechanism (WOOL $239 -> $11 on 57 units).
If the sell cadence dumps into contested books, that is floor lost in exactly the close games.
Unmeasured; not yet a cause.

## 4. Under-weighted op deltas

- **PLACE 27.9 vs 4.2 is the mirror of PICKUP +83 and DROP +35, and together they are a
  ~118-turn/season tax that is bigger than the harvest gap.**
  `DROP` is all-or-nothing (`kaggriculture.py:333` per cover.py:388); a hand banking produce with
  DROP dumps its feed wheat and pays a PICKUP per item to take it back (cover.py:389-393).
  `PLACE <item> <n>` beside the shed banks n of one item and keeps the ration
  (`kaggriculture.py:381-395`).
  Kawa's pattern is PLACE-and-keep; ours is DROP-all-and-redraw.
  The machinery exists (`_bank`, cover.py:455-479) but the branches that would use it aggressively
  ship off after whole-detour measurements (`DELIVER_SURPLUS_NOT_THE_ROW`, cover.py:240;
  `BANK_THE_ROWS_PRODUCE_WHILE_REAPING`, cover.py:274) -- the un-tried variant is the zero-detour
  PLACE at pens, which cover.py:236-239 itself names as "the version worth trying next".
  Discriminator for his side: classify kawa's PLACE args in the replays -- animal vs product -- one
  script pass.
- **The fertilizer chain: we FERTILIZE 122 vs his 65 while collecting the same (258 vs 242), so he
  sells ~175 fertilizer a season and we sell ~135 and spend ~57 extra turns (plus draws) spreading
  ours on tiles.**
  At $100 base per unit (cover.py:374) that is ~$4k of direct sales he takes that we forgo, before
  pricing whether the yield-doubling pays it back.
  Unmeasured and cheap to measure: per-tile revenue of fertilized vs unfertilized same-crop tiles
  across the 54 replays.
- **WATER +59.5 may already be partly fixed:** the safe-tile alternate-day parity term was only put
  into the condition on 2026-08-18 (router.py:747-757).
  Check whether the two submissions behind the 54 replays predate it before spending anything on
  WATER.
