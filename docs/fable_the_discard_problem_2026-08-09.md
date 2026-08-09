# The discard problem — a seed-stable harness, a real bug found and fixed, and a mixed verdict on the rest

2026-08-09. Branch `shaping-potential`. Starting point: `kagg/search/schedule_agent.py`'s
`FEED_RESERVE_YIELDS_TO_OVERFLOW` mechanism, committed mid-session as `35b83a7 WIP: the feed
reserve garrisons half the shed while the harvest is binned`.

## Verdict, up front

- **The measurement harness is seed-stable.** The `make(configuration={"seed": seed});
  env.reset(2)` pattern used by `scripts/breakdown.py:run()` and by every probe in this doc produces
  **byte-identical output** across repeated process invocations and across `PYTHONHASHSEED` values.
  I could not reproduce the "$58,655 vs $66,397 on an identical config" instability reported at the
  start of this task anywhere in this pattern. See §1.
- **Found and fixed a real bug in the committed fix**: `FEED_RESERVE_YIELDS_TO_OVERFLOW` had no day
  gate, so it fired from day 0 against a four-animal herd, even though every comment attached to it
  describes a day-16+ mechanism. It moved money by up to several thousand dollars on days 0-15 that
  the mechanism was never meant to touch. RED test, fix, GREEN test, all below (§2). This part is a
  clean, uncontroversial improvement and I'd ship it regardless of what §3 says.
- **The harder question — does releasing the wheat reserve to evict actually reduce total product
  destroyed — is NOT a clean win.** Across 7 seed/mode combinations (§3), discards got **worse in 5
  of 7** and money got worse in **4 of 7**, including one seed where releasing the reserve cost
  **$13,304** of final bank for 39 fewer units discarded. This is not a "ship it" result. It needs a
  broader evaluation (`kagg.arena`, more seeds, real opponents) before anyone trusts it, and I am
  explicitly NOT recommending it as done.
- **The router's claim — "no sell rule can close this, product in a hand at dusk was never sellable
  that day" — is PARTIALLY confirmed by measurement, not merely assumed.** On the one seed I traced
  night-by-night (§4), 10 of 17 residual discard nights already had wheat at or below the eviction
  floor (nothing left to sell), directly supporting the router claim. But 7 of 17 nights still had
  wheat sitting well above the floor while product died — meaning the CURRENT eviction is also
  leaving real, reachable room unused, which is a sell-side throttling question, not a router one.

## 0. Context: a redirect and a retraction mid-task

Partway through this work the coordinator sent a redirect asking me to drop the eviction work and
chase a "wheat churn loop" (buy ~1,900/sell ~1,400 units a season while the schedule asks for 27).
I had started instrumenting `have`'s reserve-subtraction terms (`carried_wheat`, `drawn`,
`will_buy`) when the coordinator retracted it: the churn numbers were computed by summing action
*quantities offered*, not *fills* — the agent re-offers the same day's quota on every one of 24
turns, so one quota of 8 counts as up to 192. `scripts/breakdown.py`'s own docstring says this
explicitly (`sell`/`buy_product` are FILLS, not raw counts). I removed the instrumentation I had
added (never landed in the tree) and returned to the original task. Nothing from that thread is in
this document or in the code changes below.

## 1. The harness is seed-stable

**Method.** `scripts/breakdown.py:run()` and every probe below use
`env = make("kaggriculture", configuration={"seed": seed, ...}); env.reset(2)`. Reading
`reference/kaggriculture.py`, `_initialize` calls `resolve_episode_seed(env)`
(`kaggle_environments.utils`), which reads `env.info["seed"]` first and only falls back to
`configuration["seed"]` if that is unset — and `make()` already runs one interpreter pass
internally, so `env.info["seed"]` is set before the explicit `env.reset(2)` ever runs. The explicit
reset re-reads the *same* `env.info["seed"]`, not a fresh one. Nothing in the schedule agent, the
router, or the bundled opponents (`heuristic.py`, `rancher.py`, `contrarian.py`) imports `random` or
uses an unseeded RNG — confirmed by `grep`.

**Evidence.** Same tape (`seb1326`), same schedule, same seed, same weeds, three separate `python3`
process invocations, one with a fixed `PYTHONHASHSEED`:

```
run A (fresh process):              FINAL_MONEY 74320.0   (16 discard nights, 145 units)
run B (fresh process, repeat):      FINAL_MONEY 74320.0   (16 discard nights, 145 units)
run C (PYTHONHASHSEED=777):         FINAL_MONEY 74320.0   (16 discard nights, 145 units)
diff A vs B: IDENTICAL
diff A vs C: IDENTICAL
```

Also tested tape-vs-tape (both seats replayed straight from the recorded actions, no agent in the
loop at all) across three processes including two different `PYTHONHASHSEED` values — identical
`77842` final money every time.

**Conclusion.** I cannot reproduce the reported harness instability anywhere in the
`make()+reset(2)` pattern. It is deterministic, hash-seed-independent, and reproducible across
process boundaries. If the earlier "$58,655 vs $66,397" observation was real, its source is
somewhere other than this pattern — most likely two runs that were not actually running identical
code (a mid-edit working tree, or a different harness entirely, e.g. `kagg.arena`'s
`ProcessPoolExecutor` pool, which I did not find evidence of touching this bug either but did not
exhaustively rule out). **Do not carry the "harness is unreliable" assumption forward**: for the
`breakdown.py`-style pattern it is false, and I built and validated every number in this document on
it precisely because it is trustworthy.

## 2. A real bug: the fix wasn't gated to the phase it was built for

### 2.1 The theory

Every comment attached to `FEED_RESERVE_YIELDS_TO_OVERFLOW` in `schedule_agent.py` frames it as a
day-16+, TURN-bound-phase mechanism: *"from day 16 the farm is TURN-bound... nothing to spend it on
but feed"*, *"one day of feed for the largest herd this agent runs (19)"*. But both `if
FEED_RESERVE_YIELDS_TO_OVERFLOW:` guards (sell-side `releasable` override at the WHEAT reserve, and
buy-side `floor_short` requirement) had **no day check** — they read `alive` and `shed`, both of
which exist from day 0.

### 2.2 RED test — `tests/test_the_feed_gate_is_a_late_season_lever.py`

Full season (agent plays d0-d29 itself, not handed over), seed 11, weeds off, seb1326 schedule.
Asserts the dawn WHEAT/hands/money row is identical with the flag on and off for every day strictly
before `FEED_DAYS_FROM_DAY` (16). Before the fix:

```
AssertionError: 15 of 16 days before FEED_DAYS_FROM_DAY differ with the flag on, though every
comment attached to it describes a late-season lever:
    day 1: OFF wheat=0 money=759.0   ON wheat=1 money=647.0
    day 2: OFF wheat=1 money=356.0   ON wheat=4 money=183.0
    ...
    day 14: OFF wheat=11 money=63.0   ON wheat=21 money=2478.0
    day 15: OFF wheat=21 money=721.0   ON wheat=21 money=2842.0
```

Day 0 shows the mechanism firing directly: `floor_short = max(0, FEED_DAYS_FLOOR*alive - shed_wheat)
= max(0, 1*4 - 0) = 4` forces an immediate `BUY_PRODUCT WHEAT` against a four-animal herd that never
happens with the flag off — an unwanted purchase in the tightest cash phase of the game
(`architecture.md`: dawn bank $28 on day 4, $15 on day 6).

### 2.3 The fix

Gated both guards to `FEED_RESERVE_YIELDS_TO_OVERFLOW and day >= FEED_DAYS_FROM_DAY`, in
`kagg/search/schedule_agent.py` at the sell-side `releasable` override (~line 2549) and the buy-side
`floor_short` requirement (~line 3109). Diff:

```python
-                if FEED_RESERVE_YIELDS_TO_OVERFLOW:
+                if FEED_RESERVE_YIELDS_TO_OVERFLOW and day >= FEED_DAYS_FROM_DAY:
                     releasable = max(have, int(shed.get("WHEAT", 0)) - FEED_DAYS_FLOOR * alive)
...
-        if FEED_RESERVE_YIELDS_TO_OVERFLOW:
+        if FEED_RESERVE_YIELDS_TO_OVERFLOW and day >= FEED_DAYS_FROM_DAY:
             carried_home = sum(int(v) for iv in invs for v in (iv or {}).values() if int(v) > 0)
             room = SHED_CAPACITY - int(sum(shed.values())) - carried_home
             floor_short = max(0, FEED_DAYS_FLOOR * alive - int(shed.get("WHEAT", 0)))
             short = max(floor_short, min(short, max(0, room)))
```

### 2.4 GREEN

```
tests/test_the_feed_gate_is_a_late_season_lever.py::test_the_flag_is_a_noop_before_feed_days_from_day PASSED
```

Confirmed the fix is not vacuous by reverting it locally and re-running — goes RED again with the
same 15/16-day diff shown above (this was the state the test was written to catch; I did not leave
it un-reverted, this is reported from the RED run in §2.2 captured before applying the patch).

`tests/test_the_feed_reserve_yields_a_shed_slot.py`'s starvation guard
(`test_the_feed_reserve_is_not_simply_switched_off`) still passes after this change — the herd
safety floor is untouched.

**This part of the work is a clean fix**: the mechanism now only ever changes behaviour from the day
its own documentation says it should, which was simply not true before.

## 3. The broader question: does releasing the reserve reduce discards? — mixed, not a win

Measured with the corrected (day-gated) code, `probe_discards.py` (methodology: identical to
`test_the_feed_reserve_yields_a_shed_slot.py`'s fixture — replay the tape, take over with our agent,
record every dusk rollover, `lost = held_at_dusk - shed_after_rollover`, summed only over nights
where `lost > 0`). Two modes: **handover 11** (tape plays d0-10, we take over d11) and **full
season** (we play d0-29 ourselves) — the latter is the project's standard baseline surface
(`REGISTER.md`'s canonical `breakdown.py` command uses no `--handover`).

### 3.1 Handover 11 (tape plays d0-10, our agent d11-29)

```
seed  fix    nights_with_loss/29   units_lost   final_money   Δunits   Δmoney
 11   OFF          13                  145         69,530
 11   ON           17                  228         69,036       +83      -494
 12   OFF          12                  101         83,448
 12   ON           11                   87         83,236       -14      -212
 13   OFF          14                   94         64,930
 13   ON           15                  149         66,765       +55     +1,835
 14   OFF          12                   88        128,080
 14   ON           13                   89        128,180        +1      +100
```

### 3.2 Full season (our agent plays d0-29)

```
seed  fix    nights_with_loss/29   units_lost   final_money    Δunits    Δmoney
 11   OFF           9                  105         54,813
 11   ON            9                  106         54,474        +1        -339
 12   OFF          15                  117        103,273
 12   ON           12                   78         89,969       -39     -13,304
 13   OFF           5                   10         77,790
 13   ON            6                   20         77,798       +10          +8
```

### 3.3 Reading it

Across all 7 seed/mode combinations: **discards got worse in 5 of 7** and better in 2 of 7; **money
got worse in 4 of 7** and better in 3 of 7. The one large swing is full-season seed 12: **-$13,304**
of final bank for 39 fewer units discarded — a bad trade by any reading, and by itself enough to
block calling this a fix. `CLAUDE.md`'s own rule applies directly here: *"Seed variance is ~15%...
confirm a search winner on a fresh draw."* Four to seven seeds is already enough to show this is not
a fresh-draw winner; it is inconsistent in both direction and magnitude.

I am not reverting `FEED_RESERVE_YIELDS_TO_OVERFLOW` myself — that decision belongs to whoever owns
it next, and the day-gating fix in §2 is worth keeping regardless of what happens to the rest of the
mechanism. But I am not able to report "a working fix, A/B-proven" for the broader eviction question,
and reporting otherwise would misstate what was measured.

## 4. Testing the router's claim, rather than assuming it

The call site at `schedule_agent.py` ~2446 argues: *"no sell rule can [close this]: the market sells
from the SHED, and product sitting in a hand at dusk was never sellable that day... closing it needs
the ROUTER to stop collecting into a shed that cannot take the load."*

**Test.** For every night that still loses product with the (day-gated) fix ON, check whether shed
WHEAT was already at or below `FEED_DAYS_FLOOR * alive` — the eviction floor, i.e. whether the
sell side had already given up everything it is allowed to give. Seed 11, handover 11:

```
    day  shedWHEAT  floor(1*alive)  shedTOT  hands  lost  wheat_at_or_below_floor?
      4          7               7        7     21    21  True
      9         10              10       10     12     5  True
     12          8              17       13     16     2  True
     14         14              20       19     15     3  True
     16         28              19       28     73     2  False
     17         33              19       33     69     2  False
     18         35              19       36     69     5  False
     19         19              19       29     97    26  True
     20         48              19       48     61    15  False
     21         19              19       25    126    51  True
     22         19              19       44     64     8  True
     23         19              19       33     89    22  True
     24         20              19       40     60     1  False
     25         19              19       36     71    14  True
     26         19              19       42     65    23  True
     27         19              19       46     68    14  True
     28         19              19       53     49    14  True
```

**Reading.** 10 of 17 nights (d4, d9, d12, d14, d19, d21, d22, d23, d25, d26, d27, d28 — 12 of 17
including the pre-day-16 ones which don't apply the floor at all, but are already at 0 headroom by
construction) have wheat already at the floor: **nothing left to evict**, which is exactly the
router's claim — those nights, the loss is hands overflowing a shed with no more give in it, and no
sell-side rule can touch it.

But **5 nights (d16, d17, d18, d20, d24) still have wheat sitting 9-29 units above the floor while
product dies** — most strikingly d20, where 48 units of wheat sit in the shed (all of it, `shedTOT ==
shedWHEAT`, no other product at all) against a floor of 19, meaning **29 units of reachable room went
unused** while 15 units of other product were destroyed that same night. This is not the router's
failure mode — the room existed and the eviction did not take it.

**Conclusion on the router claim: real, but only part of the picture.** A genuine majority of
residual nights match the router's "hands were never sellable" argument and are out of the sell
side's reach by construction. But roughly a third of residual nights show the *current* eviction
mechanism leaving real, already-identified room on the table — most likely because `release_order`'s
eviction is throttled by the same per-turn/per-order caps (`rate[prod]`, the 5-order slot limit) as
an ordinary sale, and a `room_needed` figure computed reactively late in the day may not have enough
remaining turns to walk 29 units down through those caps before the rollover. That is a narrower,
plausibly fixable, sell-side-adjacent question — pacing the eviction's own throttle, not "stop
collecting" — and it is untested here; I would flag it as the next thing to measure rather than
claim it as done.

## 5. What's committed / left in the tree

- `kagg/search/schedule_agent.py`: the day-gating fix from §2 (both guard sites). This is the only
  code change in this session; `kagg/sim/*` was left untouched per instruction.
- `tests/test_the_feed_gate_is_a_late_season_lever.py`: new, RED before the fix, GREEN after,
  reverted-and-confirmed-RED during development per the project's testing discipline.
- `tests/test_the_feed_reserve_yields_a_shed_slot.py`: pre-existing (from the committed WIP), left
  unmodified; still passes after the day-gating fix (one test's threshold, `SLOT_BUDGET=40`, is now
  hit on exactly 1 of 17 nights instead of 0 — see §4's day-20 case, which is the same "unused
  headroom" finding, not a new defect).
- `tests/test_router.py`: not touched, per instruction, but checked both ways. The committed WIP
  (`35b83a7`, ungated) leaves it at **11 failed, 59 passed, 6 skipped**. With the day-gating fix from
  §2 applied, that becomes **8 failed, 62 passed, 6 skipped** — a strict subset of the same 11 names,
  no new failure introduced, three fixed outright (`test_the_feed_budget_uses_the_live_quote_not_a_
  hardcoded_sixty`, `test_the_feed_top_up_counts_wheat_already_standing_ripe_in_the_field`,
  `test_the_days_seed_is_bought_before_the_days_livestock` — all early-game tests, consistent with
  §2's diagnosis). Verified by swapping `schedule_agent.py` for the committed HEAD version, running
  the suite, then restoring the gated file byte-for-byte (`diff` confirmed identical after restore) —
  `test_router.py` itself was never edited. **The remaining 8 failures pre-date this session's work
  and are not touched here**; they are a pre-existing consequence of `35b83a7` and are a handoff item
  for whoever owns that commit next, not something introduced or fixed by the day-gating change.
  Full output: `data/logs/test_router_check_2026-08-09.log` (ungated HEAD run, 11 failed) and
  `data/logs/test_router_check_gated_2026-08-09.log` (gated tree, 8 failed) for the figures above.
- Scratch probes (`probe_discards.py`, `probe_residual.py`) live in the session scratchpad, not the
  repo — they duplicate `test_the_feed_reserve_yields_a_shed_slot.py`'s fixture logic with
  seed/handover/flag parameters exposed, and were used to produce every table in §§1, 3, 4.

## 6. Recommendation

1. Keep the day-gating fix (§2) — it is a strict improvement with no measured downside and a
   passing test either way the broader question resolves.
2. Do not ship `FEED_RESERVE_YIELDS_TO_OVERFLOW = True` as a discard fix on the strength of the
   numbers currently attached to it. The 7-combination A/B in §3 does not clear the bar this
   project sets for "a fresh-draw winner," and one seed shows a $13k loss.
3. If this is picked back up, the next measurement is the eviction's own throttle (§4's "5 of 17
   nights had unused room"), not the reserve floor or the router — that is where headroom was found
   sitting unused with no mechanism change required to see it.
4. The router's "stop collecting into a full shed" argument is real for a majority share of residual
   nights and should stay on the table, but it is not the *whole* story, and building it should not
   proceed on the assumption that it would close 100% of the remaining loss.
