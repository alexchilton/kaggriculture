# The wheat churn is a buy-side day-budget defect, not a sell-side one

Started from a sell-side framing (the shed carries a 42-44 unit reserve while offering 51-123 WHEAT
a day from day 17).
That framing was superseded mid-investigation by new evidence, and this doc follows the corrected
one: **the field disagrees on how much to sell and agrees closely on how much to buy.**

## The reframing evidence

66 of our own 1.32.6 ladder replays (`townCenterSellInterval=24` only), wheat units offered per
game, grouped by team:

```
team                     games  wheat_buy  wheat_sell  mean_bank
alex chilton                66      1,099         764    $73,827
Seb (allegedly)             10        392          84    $74,264
Rayk Kretzschmar             1        266         305   $129,906
Lester Leong                 1        266         305   $125,255
Syed Muhammad Gillani        4        323         649   $101,153
HealthStone                  5        293         436    $80,237
kakuteki                     1        266         350    $70,886
```

Syed sells 649 and banks $101k; Rayk and Lester sell 305 and bank $125-130k.
Seb's 84 is the low outlier, not the field's norm.
The whole field buys 266-392; we buy 1,099.
Selling is downstream of having bought too much, not the anomaly itself.

## The mechanism, measured

`kagg/search/schedule_agent.py`, the feed-buy emission site (originally ~line 3194, now ~3208 after
the fix's comments were added):

```python
herd = feed_days(day) * alive - fed_today - on_hand
short = min(max(herd, min(max(0, owed), BUY_DRIP)), FEED_TURN_CAP)
```

`owed` is the schedule row's own target, credited every turn via
`state["ordered"][("buys", "WHEAT")]`.
It self-limits: once the day's row has been asked for, `owed` goes to (and stays at) zero or below,
and the row stops contributing.

`herd` (`feed_days(day) * alive - fed_today - on_hand`) has **no day-level credit at all.**
`feed_days(day)` is 2 early, 4 from day 16 (`FEED_DAYS_FROM_DAY`) — a 2-4 DAY **stock buffer**, not
a purchase budget.
The only thing that ever bounded it was the per-turn `FEED_TURN_CAP` (6), giving a theoretical
ceiling of 6 × 24 = 144 units a day.
`max(herd, ...)` means whichever term is bigger wins, and from around day 12 that is `herd` on
almost every turn.

### Measured, own instrumentation, seed 11, Seb's tape at seat 1

Full 30-day season, ground truth via `kagg.analysis.fills.record_fills` (never offers off the
action stream, never a holdings delta — see `fills.py`'s own docstring for the three ways those
proxies previously lied):

| | bought | sold | final bank |
|---|---:|---:|---:|
| unfixed | 1,800 | 1,456 | $45,797 |

Per-day trace confirming the mechanism (`data/logs/herd_diag_seed11.log`, an earlier run with a
different opponent-seat argument, same qualitative shape): the herd path hits its `FEED_TURN_CAP`
ceiling on 20-24 of 24 turns on days 17 through 29, for 1,668 herd-path units asked that run.
The two "unfixed" numbers (1,668 vs 1,800) differ because of a real methodology bug caught along the
way, see **Two false leads** below — 1,800 is the one to trust, since it uses
`build_tape_agent(TAPE, 1)`, the convention every other test in this repo (`test_fills.py`) already
uses for "Seb's tape as the opponent."

## The fix

Two additions right after `herd` is computed, both inside `kagg/search/schedule_agent.py`:

```python
herd_ceiling = max(0, max(wanted, FEED_BUY_CEILING_DAYS * alive) - state["ordered"][("feed", "WHEAT")])
herd_floor = max(0, alive - fed_today - on_hand)
herd_capped = max(min(herd, herd_ceiling), herd_floor)
short = min(max(herd_capped, min(max(0, owed), BUY_DRIP)), FEED_TURN_CAP)
```

**The ceiling is credited on ASKS**, reusing `state["ordered"][("feed", "WHEAT")]` — the row and the
herd already share that exact counter (both increment it at the emission site), so it already totals
everything asked today from either path.
No new bookkeeping was needed.

**The floor is credited on ARRIVALS.**
`alive - fed_today - on_hand` is what is *still* needed today regardless of the ceiling, and
`on_hand` only moves when stock genuinely lands (buy fills, harvest) or leaves (feed, sell) — an
order that fails to fill leaves it untouched, so the floor asks again next turn.
`max()` always lets the floor through, so a real shortfall is never silenced by the budget; only the
*excess* chasing of the multi-day buffer is bounded.

This mirrors the exact shape of the historical starvation bug this repo already carries scar tissue
for (`d124359`: subtracting *asks* from a target already sized at one day's need, so a single ask
could zero it out for the day whether or not it filled) — the difference is that here the thing being
credited on asks is a **ceiling with headroom**, not the **target** itself, and a separate
**arrival-based floor** exists specifically to survive an ask that failed.

### Why `FEED_BUY_CEILING_DAYS = 2`, not 1

The first version sized the ceiling at `max(wanted, alive)` — one day's true consumption, the
tightest defensible number.
It passed the churn measurement outright: 1,800 → 393 bought.

It then failed the anti-starvation check on a **second, independent run**: seed 11, day 15, the shed
held 16-19 idle WHEAT the entire day (visible in `sh_wht` below) while only 7 of 20 animals got fed,
and by day 17's rollover six animals had starved (`consecutive_unfed >= 2`,
`reference/kaggriculture.py:786`, herd 20 → 14 with **zero** recovery):

```
day  hr  herd  ceil floor capd owed on_hand alive fed_td sh_wht short ordrd
 15  16    14     0    0    0    0      22    20      4     16     0    20
 15  21    14     0    0    0    0      19    20      7     16     0    20   <- day ends, 7/20 fed
 16  19    39     0    0    0   -2      27    20     14     15     0    20   <- day ends, 14/20 fed
 17   0    30    18    0   18   18      26    14      0     21     6     0   <- herd is now 14
```

The bottleneck is **not wheat supply** — the shed is sitting on it — it is **delivery**: FEED needs a
hand to physically carry a unit of wheat to a tile, and with a herd of 20 that is a real
routing/labor constraint.
The old code's gross over-buying had been masking that constraint with sheer surplus; tightening
supply to exactly the daily need removed the slack the crew needed to catch up on a day it fell
behind.

Three ceiling sizes were measured on the identical fixture (seed 11, `build_tape_agent(TAPE, 1)`):

| `FEED_BUY_CEILING_DAYS` | bought | sold | final bank | herd drops |
|---:|---:|---:|---:|---|
| unfixed (no ceiling) | 1,800 | 1,456 | $45,797 | none |
| 1 (`= alive`) | 393 | 253 | $53,421† | **day 16→17: 20 → 14** |
| 2 (shipped) | 797 | 458 | $46,370 | none |
| 4 (`= feed_days(day)*alive`, the full buffer) | 1,328 | 985 | $46,834 | none |

† This bank figure is not comparable to the others — it was measured with a stale, differently-tuned
`schedule_agent.py` before the data-contamination issue below was caught and corrected; the *herd
drop* it produced, independently reproduced on the clean fixture, is the actual finding that mattered.

**`FEED_BUY_CEILING_DAYS = 2` is the shipped value**: it cuts the season's wheat purchases by 56%
(1,800 → 797), keeps the bank at parity with the unfixed baseline (+$573), and produces **zero herd
drops across the full 30-day season** — the same safety record as the unfixed baseline, at less than
half the spend. `4` (the full existing buffer) is safe too but barely bends the curve (1,328, a 26%
cut) because it is close enough to the multi-day target that the day rarely exhausts it. `1` cuts the
hardest and is the one that is unsafe.

**The routing/labor limit itself is a separate, deeper bug and is explicitly NOT fixed here.** It
is flagged for a future investigation: even with abundant wheat sitting in the shed, the crew could
not reach all 20 animals on a single day at this herd size. `FEED_BUY_CEILING_DAYS = 2` works around
it by keeping enough buffer that the crew has a spare day to catch up; it does not explain why the
crew falls behind in the first place.

## Two false leads, corrected in-flight

Both cost real time and are recorded so they are not re-walked.

### 1. `PYTHONHASHSEED` was not the cause of a run-to-run discrepancy

An early measurement gave 1,800 bought; a later one, on what looked like the identical setup, gave
373.
`PYTHONHASHSEED` was the first suspect (`hash("WHEAT")` genuinely differs between unseeded Python
processes), but pinning it to 0, 1, and 2 all reproduced **373** identically, and reverting to the
default unseeded process also gave 373 on six separate runs. The environment is deterministic given
a seed exactly as CLAUDE.md says; this was a red herring.

### 2. The actual cause: a second session was concurrently editing the shared, uncommitted main checkout

This worktree is isolated (`.claude/worktrees/agent-a55450e9e63e30647`), but the data and code it
needed (`kagg/analysis/fills.py`, the seed-script replay data, parts of `kagg/search/schedule_agent.py`
itself) exist only as **uncommitted** work in the shared main checkout, so they had to be copied in
by hand at the start of this session.
That copy captured one snapshot in time.
By the time a *second* comparison script re-read the main checkout later in the session (to build a
before/after backup), **a different, unrelated fix had already landed there** — a
`FEED_BUY_TURNS_PER_DAY` throttle, a different mechanism aimed at the same bug, evidently applied by
another concurrent session working the same problem.
That second snapshot was the accidental source of the 373 measurement: it was not this investigation's
code at all.

The fix was to stop re-reading the main checkout entirely and reconstruct the true "before" state by
reversing this investigation's own diff against its own first synced copy
(`schedule_agent_TRUE_BEFORE.py`, built by undoing the exact text this fix inserted, in
`/private/tmp/.../scratchpad/`), which reproduces the original 1,800 finding exactly, repeatably,
independent of hash seed.

**Lesson for anyone else touching this repo from a worktree while the main checkout is live:** once
a file is copied in from the shared checkout, do not copy it again mid-session — the source is a
moving target with other agents' uncommitted work on it, and a second read can silently swap in a
different, unrelated in-flight fix.

## Tests

`tests/test_the_herd_buy_has_a_day_budget.py`, two tests, both using
`kagg.analysis.fills.record_fills` for ground truth:

- `test_wheat_bought_stays_within_a_days_budget_of_the_herds_need` — RED before the fix (1,800 vs a
  ceiling of 1,100), GREEN after (797).
- `test_the_herd_never_shrinks_across_the_season` — the anti-starvation guard. Passes on both the
  unfixed and fixed code (the unfixed code does not starve anyone either; it only overspends), so its
  job is forward-looking: it is what would have caught the `FEED_BUY_CEILING_DAYS = 1` regression
  automatically, and it is what must stay green if this constant, or anything else on this path,
  moves again.

**Revert-and-confirm, per CLAUDE.md**: reverting the fix (restoring the pre-fix `short = min(max(herd,
...), FEED_TURN_CAP)` one-liner) turns `test_wheat_bought_stays_within_a_days_budget_of_the_herds_need`
red again (`1800 <= 1100` fails) while `test_the_herd_never_shrinks_across_the_season` correctly stays
green on the unfixed code too — confirming the second test is not accidentally the one carrying the
whole fix's signal.

## What changed

- `kagg/search/schedule_agent.py`: new constant `FEED_BUY_CEILING_DAYS = 2` (near `FEED_TURN_CAP`),
  and `herd_ceiling` / `herd_floor` / `herd_capped` added at the feed-buy emission site, replacing the
  bare `short = min(max(herd, min(max(0, owed), BUY_DRIP)), FEED_TURN_CAP)` with the same line fed by
  `herd_capped` instead of `herd`.
- `tests/test_the_herd_buy_has_a_day_budget.py`: new, two tests as above.
- This doc.

Diagnostics left behind for future reference: `data/logs/herd_diag_seed11.log` (per-turn trace of the
mechanism), `data/logs/starvation_diag.log` (the day 14-18 trace that caught the `FEED_BUY_CEILING_DAYS
= 1` regression). Both are under the gitignored `data/` scratch directory per this repo's own
convention.

## What this does not touch

- The sell side (`SELL_TO_MAKE_ROOM`, the shed feed-reserve formula, `CAP_SELL_OFFER_SIZE`,
  `LATE_SELL_BIAS`, `SELL_ON_DRAIN_CADENCE`) — all untouched. The reframing evidence says buying, not
  selling, is the anomaly, so the sell-side investigation this doc superseded is not resumed here.
- The routing/labor limit that the `FEED_BUY_CEILING_DAYS = 1` experiment exposed. Flagged above as
  a distinct, deeper bug.
- `FEED_ORDER_CAP`, `BUY_DRIP`, `FEED_TURN_CAP` — all left at their existing, separately-measured
  values.
