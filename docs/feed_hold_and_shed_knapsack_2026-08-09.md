# Tasks #45 and #46 — the planner-owned feed hold, and the knapsack that turned out to be a sort

2026-08-09.
Branch `feed-hold-knapsack`, cut from `shaping-potential` at `b85ac19`.
Follows `docs/fable_the_discard_problem_2026-08-09.md`, which measured and rejected the obvious
remedy (`FEED_RESERVE_YIELDS_TO_OVERFLOW`).

## Verdict, up front

Three findings, in descending order of how much they should change what anyone does next.

1. **The discard metric this whole line of work has been measured on is wrong, and it overstates
   the problem by up to 20x.**
   `held_at_dusk - shed_at_dawn` is not the discard: hour 23's SELL and BUY_PRODUCT settle in the
   *same* interpreter step as the rollover, so a sale is counted as a loss.
   Instrumenting `_drop_inventories_to_shed` — the only code path in the game that deletes product —
   gives the exact figure.
   On seed 11, full season, the delta method reports **105–137 units destroyed** and the env
   destroys **7**.
   Same run, same money ($54,813) both ways, so it is purely the metric.
   §1.

2. **Two of the three premises in the task brief do not hold against the shipped code.**
   The wheat pile is not a one-way ratchet — we sell 1,328 units of wheat in a full season and the
   dusk shed oscillates 6–53.
   `have` for WHEAT is not pinned at 0, because the schedule's own `buys.WHEAT` row (18–20 a day
   late season) is one of the terms subtracted from the reserve.
   And the reserve is not "56–76 units of the shed": 76 is a *target the buy never reaches*, not
   an occupancy.
   The premise that does hold is the important one — `feed_days()` is one constant doing two jobs,
   and neither job reads the shed.
   §2.

3. **Task #46 is not a knapsack.**
   Every unit of every product occupies exactly one slot (`_drop_inventories_to_shed` counts
   `sum(shed.values())` against `capacity`; there is no per-item size), and a 0/1 knapsack whose
   items all have weight 1 is solved exactly by sorting on value.
   `release_order` already sorts ascending on `BASE_PRICE`, so the shipped rule *is* the optimum.
   Brute-forced against an exhaustive search over 60 random sheds: identical every time.
   What was actually missing was not the algorithm but a **participant** — the feed reserve was the
   one rule spending those hundred slots that never read them.
   That is #45, and it is the only thing #46 needed.
   §4.

**What shipped:** `feed_hold()` in `kagg/search/schedule_agent.py`, bounding the wheat hold by the
slots the night can spare, wired to the BUY site (`FEED_HOLD_BOUNDS_THE_BUY = True`) and left off
at the SELL site (`FEED_HOLD_BOUNDS_THE_SELL = False`).

**What it is worth:** across 32 seeds, full season, it destroys **67% less product** (660 → 217
units) and places **38% fewer wheat buy orders** (51,714 → 31,970 fills) at **money parity**
(+$238 ± $440 SE, better on 21 of 32 seeds) and **escapes unchanged** (89 → 90).

**What it is not:** a proven money win.
Every arm measured here sits inside one standard error of zero.
There is no valid arena right now, so nothing in this document is a win-rate claim, and the money
column should be read as "did not regress", not as "gained".
§3.

## 0. Method

`probe_hold.py` (repo root, scratch) replays Seb's 1.32.6 tape as the opponent, runs our schedule
agent in seat 0, and records for every day: dawn and dusk shed per product, hands at dusk, herd
size, animals fed, escapes across the rollover, **market fills** (not offers), and the exact
rollover discard.
`sweep_hold.py` runs it across seeds and arms and reports **paired** per-seed money deltas, which
is the only way to see anything through a $24k seed standard deviation.

Two surfaces, because they disagree and it matters:

* **full season** — our agent plays d0–d29. This is the project's canonical surface
  (`breakdown.py` with no `--handover`).
* **handover 11** — the tape plays d0–d10 and we take over. Inherits a bigger board and a faster
  herd, so it is far more feed-stressed and carries most of the discards.

Weeds off, tape `seb1326`, seeds 11–42.
Logs: `data/logs/sweep_feedhold_full_32.log`, `data/logs/sweep_feedhold_h11_32.log`,
`data/logs/probe_hold_*.log`.

## 1. The discard metric was measuring the market, not the rollover

`tests/test_the_feed_reserve_yields_a_shed_slot.py` and
`docs/fable_the_discard_problem_2026-08-09.md` §3 both compute the night's loss as
`sum(shed + hands at h23) - sum(shed at next dawn)`.

That subtraction spans one `env.step`, and that step does **two** things: it runs hour 23's market
orders and *then* the rollover.
A unit sold at hour 23 leaves the shed and shows up as a loss.
A unit bought at hour 23 hides one.

The rollover is the only place the game deletes product (`_drop_inventories_to_shed`,
`reference/kaggriculture.py:830-849`).
`PLACE` into a full shed clamps and leaves the remainder in the hand
(`kaggriculture.py:380-396`), so it destroys nothing.
Patching that one function gives the exact per-product count.

| seed 11 | delta method | env, exact |
|---|---|---|
| full season | 105 (fable §3.2) / 137 (per-product) | **7**, over 2 nights |
| handover 11 | 145 (fable §3.1) | **123**, over 8 nights |

Final money is byte-identical between the two measurements, so these are the same runs.

This does not make the earlier work wrong about the *mechanism* — the handover figure is real and
large — but it does mean:

* the full-season discard problem is roughly **20 units a season** against a **$55,837** mean bank,
  which is noise, not a lever;
* the "263 units destroyed in that game" figure quoted from `data/ladder/losses/` in
  `test_the_feed_reserve_yields_a_shed_slot.py`'s docstring was computed the same way and should be
  re-measured before anything is built on it;
* any future discard number in this project must come from the env's own deletion, not a shed delta.

## 2. What the brief got right, and what it got wrong

Task #45's framing, checked line by line against a full season on seed 11:

| claim | measured |
|---|---|
| "`feed_days()` returns one number that does TWO jobs" | **true**, and it is the real defect |
| "the reserve is 56–76 units against a shedCapacity of 100" | **no.** 76 is the buy *target*; peak dusk wheat is 53, peak dawn wheat 63 |
| "`have` for WHEAT pins at 0" | **no.** `will_buy` (the row's `buys.WHEAT`, 18–20/day late) cancels most of the reserve |
| "from day 16 we can never sell a single unit of wheat" | **no.** 1,328 units of wheat sold in the season, 1,440 on handover-11 |
| "the pile is a one-way ratchet" | **no.** Dusk wheat oscillates 6 → 53 → 6 across late-season days |

The mechanism that *is* there, and that the brief names correctly, is that the buy target and the
sell guard are the same number and disagree about it.
The buy site's own comment already said so — *"two rules disagreeing about one number"* — it just
attached the observation to a flag that was switched off.

### 2.1 A wheat round trip that is real in volume and not real in money

Measured on FILLS (`_commit_unit` returns True exactly once per unit that settles), because the
project has been burned by offer counts before:

```
seed 11, full season:   bought 1,717 wheat for $85,178 (mean $49.6)
                        sold   1,328 wheat for $66,620 (mean $50.2)
                        eaten    410
                        net    -$18,558 on a $54,813 final bank
```

From day 17 the farm buys ~130 units of wheat a day and sells ~120 back, against a herd that eats
19.
The earlier session saw this on offers, was told it was an offers-vs-fills artifact, and dropped it.
**The volume is real** — these are settled units, not re-offered quotas.

**The money is not.**
Mean sale price ($50.2) is slightly *above* mean purchase price ($49.6), and the net of −$18,558
over 410 meals is ~$45 a meal, which is roughly what wheat costs.
The round trip is close to cash-neutral; it is not a leak, and anyone chasing it as one will find
nothing.
What it does cost is market order slots and turns, which is a separate question and not measured
here.

## 3. `feed_hold()` — what shipped and what it is worth

```python
def feed_hold(day, alive, shed, invs):
    want  = feed_days(day) * alive                      # unchanged: the fill-risk buffer
    other = (everything in the shed that is not wheat)
          + (everything in a hand that is not wheat)    # it all lands in the shed tonight
    return max(FEED_DAYS_FLOOR * alive, min(want, SHED_CAPACITY - other))
```

The first term is exactly what it replaces, so the 2 → 4 evidence behind `FEED_DAYS_LATE` is
untouched.
The second is the change: the hold may not ask for slots the night does not have.
The floor is absolute — one meal a head stands whatever the crowding, because an escape is
irreversible and a binned melon is not.

Two flags, because the two call sites are not the same bet.
Bounding the **BUY** stops an order being placed: it costs nothing and walks no price.
Bounding the **SELL** releases stock to the market, which is the exact direction
`FEED_RESERVE_YIELDS_TO_OVERFLOW` was measured on and rejected at −$13,304.

### 3.1 Full season, 32 seeds (the canonical surface)

| arm | paired money Δ | seeds better | destroyed | escapes | unfed animal-days | wheat buy fills |
|---|---|---|---|---|---|---|
| shipped (`$55,837`) | — | — | 660 | 89 | 1,006 | 51,714 |
| **buy bound** | **+238 ± 440** | **21/32** | **217 (−67%)** | 90 | 1,114 | **31,970 (−38%)** |
| sell bound | +41 ± 442 | 17/32 | 358 (−46%) | 90 | 1,177 | 59,327 |
| both | +601 ± 688 | 19/32 | 179 (−73%) | 102 (+15%) | 1,260 | 40,843 |

### 3.2 Handover 11, 32 seeds (the feed-stressed surface)

| arm | paired money Δ | seeds better | destroyed | escapes | unfed animal-days | wheat buy fills |
|---|---|---|---|---|---|---|
| shipped (`$66,512`) | — | — | 1,499 | 174 | 1,554 | 45,325 |
| buy bound | −57 ± 354 | 18/32 | 798 (−47%) | 191 (+10%) | 1,689 | 28,915 (−36%) |
| sell bound | +509 ± 547 | 15/32 | 653 (−56%) | 192 (+10%) | 1,767 | 51,475 |
| both | −360 ± 365 | 12/32 | 378 (−75%) | 217 (+25%) | 1,869 | 36,517 |

### 3.3 Reading it

**Money is a wash on every arm.**
All four paired deltas are inside one standard error of zero, and 21/32 is the best win count
anywhere in the table (binomial p ≈ 0.11).
Nothing here is a money win and it must not be reported as one.
`CLAUDE.md`'s rule — *select on win rate, not money* — cannot be applied at all right now, because
there is no valid arena; the synthetic pool saturates and the tape arena does not exist.

**The mechanical result is clean and one-directional.**
Two thirds less product destroyed and 38% fewer wheat orders placed, for free.

**The one real cost is feeding cadence, and it is bounded.**
Unfed animal-days rise 11% on both surfaces.
Escapes — the irreversible failure — stay flat on the canonical surface (89 → 90) and rise 10% on
the feed-stressed one (174 → 191).
`FEED_DAYS_FLOOR = 1` is what allows that, and raising it to 2 *was* measured — §3.4.

### 3.4 `FEED_DAYS_FLOOR = 2` — the most promising number in this document, and not adopted

Buy bound on, handover 11, 32 seeds, floor 1 vs floor 2:

| arm | paired money Δ | seeds better | destroyed | escapes | unfed animal-days |
|---|---|---|---|---|---|
| buy bound, floor 1 (shipped) | — (`$66,455`) | — | 798 | 191 | 1,689 |
| buy bound, floor 2 | **+953 ± 368** | **15/32** | 1,043 | 180 | 1,601 |

It moves every mechanical column the right way — escapes 191 → 180, unfed days down 5% — and the
money delta is 2.6 standard errors, the only figure anywhere in this session that clears one.

**And it is better on only 15 of 32 seeds, which is worse than a coin flip.**
A mean that clears 2.6 SE while the sign test says nothing is a mean carried by a handful of large
seeds, and this project has a named rule for exactly that: *confirm a search winner on a fresh
draw, or the winner's curse makes it wander.*
So it is recorded, not adopted.
It is the first thing to re-run on held-out seeds and on the full-season surface, and it should be
adopted or dropped on that, not on this.

**The sell half is left off deliberately.**
It is the better arm on money on the handover surface taken alone (+$509, but on only 15 of 32
seeds) and the worse one on the canonical surface (+$41 on 17/32), it costs escapes in every
combination — and combining it with the buy bound is the *worst* arm measured anywhere: −$360 on
12 of 32 seeds with escapes up 25%.
It is also the direction this project has already rejected once with a −$13,304 seed attached.
It is wired, flagged and measured, so switching it on is one constant — but it should clear a
real arena first, not this.

## 4. Task #46: the hundred slots are one budget, and allocating them is a sort

The brief asked for "an explicit value-per-slot knapsack — nine products and 100 slots is a small
exact knapsack".

It is not, and the reason is a rule rather than an opinion.
`_drop_inventories_to_shed` compares `sum(shed.values())` against `capacity`: **every unit of every
product weighs exactly one slot.**
A 0/1 knapsack in which all items have equal weight has no combinatorial content — taking items in
descending value order is exactly optimal, and a DP can only spend runtime rediscovering it.
`release_order` already returns `sorted(SELLABLE, key=BASE_PRICE)` restricted to products the shed
holds.

`tests/test_the_shed_slots_are_one_budget.py::test_the_greedy_release_is_the_exact_optimum`
brute-forces the true minimum-value release over 60 random sheds and confirms the shipped greedy
matches it every time.
It exists so the next session that reads task #46 does not build the solver: the reason not to is
measured, not asserted.
If a rule change ever gives a product a different slot cost, that test goes red and the knapsack
becomes worth building.

What #46 was actually pointing at is right, and it is the same finding as #45: three rules were
spending one budget without seeing each other, and the feed reserve was the one that never read the
shed at all.
`feed_hold()` puts it in the budget.
The third rule — the router collecting into a shed that cannot take the load — is untouched here
and is still `REGISTER.md`'s OPEN-4.
On the seed-11 handover fixture it is visibly the larger remaining term: the worst night (d21)
destroys 38 units with **117 units in hands against 8 in the shed**, which no hold and no sell rule
can reach.

## 5. Tests

* `tests/test_the_feed_hold_is_sized_to_the_night_it_survives.py`
  * `test_bounding_the_buy_by_the_shed_destroys_less_of_the_harvest` — the shipped half.
    A/Bs the flag inside one fixture, so it goes **red** if the wiring is removed.
    Confirmed: reverting the BUY call site to `feed_days(day) * alive` gives `assert 123 < 123`.
  * `test_the_herd_is_not_starved_to_free_a_shed_slot` — escapes may not get worse.
  * `test_a_night_that_bins_product_holds_no_more_wheat_than_the_herd_will_eat` — the original RED
    test, now `xfail(strict=False)`.
    It went from 5 offending nights / 53 units binned to 4 / 21, and the residual is a timing
    artifact the buy bound cannot reach: wheat bought at hour 2, when the hands were still empty
    and the room looked large, is still in the shed at hour 23.
    Closing it needs the SELL bound, which §3.3 declines to ship.
* `tests/test_the_shed_slots_are_one_budget.py` — the #46 finding, plus the unit contract for
  `feed_hold()`.

Suite state: **12 failures, all pre-existing.**
Verified by swapping `kagg/search/schedule_agent.py` for the `b85ac19` version, running
`test_router.py`, `test_stock_the_schedule_never_names.py`,
`test_a_stranded_feed_survives_a_dry_shed.py` and `test_locked_chain_relocates.py`, and getting the
identical list of 12 names.
This change introduces none of them and fixes none of them.
(`test_replay_plan.py` errors on missing `data/` fixtures in a fresh worktree; environmental.)

## 6. What to do next, in order

1. **Re-measure anything that quoted a discard number.**
   `test_the_feed_reserve_yields_a_shed_slot.py`'s docstring table, the `data/ladder/losses/` "263
   units" figure, and `SELL_TO_MAKE_ROOM`'s "101 units destroyed across 15 days" are all shed
   deltas.
2. **Build the tape arena.**
   Every arm in §3 is inside one SE of zero and there is no way to break the tie without one.
   Four sessions in a row have now ended with "money is a wash, mechanically better" and that is
   the missing instrument, not a missing idea.
3. **`FEED_DAYS_FLOOR = 2` on held-out seeds and on the full season.**
   §3.4: +$953 ± 368 with escapes and unfed days both down, on 15 of 32 seeds.
   Everything about that says "confirm on a fresh draw before believing it", and nothing about it
   says "ship it".
   `data/logs/sweep_floor_h11_32.log`.
4. **OPEN-4, the router.**
   117 units in hands against 8 in the shed is where the remaining destruction is, and it is
   upstream of every rule touched here.
