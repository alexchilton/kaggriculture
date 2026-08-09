# The delivery problem, measured exactly: it is not the problem

**2026-08-09.**
Started as a brief to explain 443 units of MILK/WOOL/MELON/STRAWBERRY sitting in hands at dusk on
seed 13, and to fix `kagg/search/cover.py`'s delivery batching if that turned out to be a discard
bug.
It is not.
`docs/the_book_is_shallow_2026-08-09.md` (main worktree, written mid-investigation by the same
coordinator running this task) reached the same conclusion independently, from a wider 36-season
study, and supersedes this doc's original framing.
**Read that doc first.**
This one records the exact instrumentation built here, the numbers it produced, why they agree with
the wider study rather than contradict it, and the two things that remain open and unfixed: a small,
real animal-loss event and the production-mix question the wider doc identifies as the actual gap.

## 1. The destroyed-vs-late split, measured exactly

`/tmp/delivery.py`, the first attempt at this split, crashed on `kg.BASE_PRICE` — that constant
does not live in the env module, it lives in `kagg/search/router.py`.
It also *guessed* at the split by sampling an observation at hour 23 (before that turn's own action)
and differencing `shedCapacity - sum(shed.values())`, the same category of error
`docs/fable_the_discard_problem_2026-08-09.md` already flagged as a 15x overstatement: a SELL or
BUY_PRODUCT at hour 23 settles in the same `env.step` as the midnight rollover, so a sale can read
as a loss.

The corrected method monkeypatches `_drop_inventories_to_shed` itself
(`reference/kaggriculture.py:830`), the exact function that performs the sweep, so the split is read
off the real call with the real per-hand `private["inventories"]` and the real `private["shed"]` —
zero inference, per product, every day:

```
held_p         units of product p summed across every hand's inventory, going INTO the real call
shed_before_p  what the shed already held of p (drops made earlier in the day)
shed_after_p   what the shed holds of p, coming OUT of the real call
landed_p       shed_after_p - shed_before_p     (<= held_p always, by construction)
destroyed_p    held_p - landed_p                (exact, not inferred)
```

`_end_of_day` (`kaggriculture.py:865`) calls this once per player, in `enumerate(obs0.farms)` order
— player 0 first, then player 1 — which is the only way to attribute a call to "us" without a
player id in the function's own signature.
There is exactly one call site in the reference, so that parity is safe.

### Measured, shipped `schedule_agent`, the `seb1326` tape opponent, seat 0, four seeds

| seed | destroyed (hi) | landed late (hi) | destroyed % of rollover-swept | destroyed % of season hi-value produced | animals lost |
|-----:|---------------:|------------------:|-------------------------------:|------------------------------------------:|-------------:|
|   13 |             22 |               410 |                           5.1% |                                      2.7% |            1 |
|   17 |             36 |               442 |                           7.5% |                                      4.2% |            0 |
|   19 |              2 |               315 |                           0.6% |                                      0.3% |            0 |
|   23 |             15 |               321 |                           4.5% |                                      2.0% |            1 |

At base price that is **$320-$6,100 a game destroyed outright**, against a season that banks
$57,658-$163,036 on these same four seeds.
**Do not add destroyed and landed-late together** — they are different losses.
Destroyed is a permanent write-off; landed-late reached the shed a day after it could have and sold
whenever the schedule's row next asked for that product, which is a price-timing question, not a
write-off.

This is a small number, and it independently reproduces the same verdict as
`the_book_is_shallow_2026-08-09.md`'s broader fills-based study: "left in shed 0, left in hands 0"
at season end, shed at capacity 2-6 hours out of 720.
The two studies used different instrumentation (this one wraps `_drop_inventories_to_shed` and
reports the *rollover*, theirs wraps `_commit_unit` via `kagg/analysis/fills.py` and reports the
*season*) and land on the same conclusion from different angles: whatever gets destroyed is a
rounding error next to the season's revenue, not the 443-unit crisis the dusk snapshot implied.

### Why 443 looked large and is not

443 was `hi_held` summed across 30 daily dusk snapshots on seed 13 — a flow (goods in transit)
counted as if it were a stock (goods lost).
Two things inflate a stock reading of a flow: sampling at the one instant of the day when the
numerator (hands) is maximal and the denominator (shed) is minimal by construction, and comparing
raw counts across agents with different herd sizes, so an agent that produces less (because it lost
more animals) automatically strands less of it and looks like the better deliverer.
Both are recorded in `the_book_is_shallow_2026-08-09.md` §"Two measurement errors" with the
`1455m` graft as the concrete example: 134 units stranded against the shipped agent's 443, on 11
animals lost against 1.

### The test this leaves behind

`tests/test_high_value_produce_reaches_the_shed.py`, `@pytest.mark.slow`, four seeds.
Asserts destroyed stays under 10% of the rollover-swept hi-value population (worst measured is
7.5%, seed 17) — a regression guard on `cover.py`'s delivery batching (`DELIVER_MIN`,
`DROP_WHERE_THE_TOUR_ALREADY_STANDS`, the closing-trip cutoff), not a target to chase.
Confirmed discriminating: tightened to 1% locally, it failed with the exact seed-17 numbers
(`36 of 478 rollover-swept hi-value units destroyed (7.5%)`), then restored to 10.0.
All four seeds pass at the shipped threshold (`23.45s` for the full parametrized run).

## 2. What was tried and abandoned mid-investigation: chasing the price collapse directly

Before `the_book_is_shallow_2026-08-09.md` landed, this session was redirected toward "we crash our
own price" and independently found the same seed-13-vs-seed-29 MILK divergence the wider doc later
explained structurally.
Recorded here because the trace is a useful concrete artifact, not because it adds anything the
wider doc does not already cover more rigorously.

Instrumenting every MILK fill (extending `kagg/analysis/fills.py`'s `_commit_unit` wrap with a turn
number and the live `market["inventory"]`) on seed 29: our own agent pushes `market["inventory"]`
for MILK through `I0` (10,000) at turn 204 (day 8, hour 12), selling `$169 -> $160 -> $158 -> $156`
in the same short burst without pausing at the crossing, while the opponent sells in the same turns
alongside it (turn 216: six alternating `us`/`them` fills in one turn).
By contrast, on seed 13, MILK's `market["inventory"]` never reaches `I0` at all across the whole
season — it ends at 9,839, i.e. *below* baseline, which is why the price sits at $252-271/unit
instead of the floor.

That is a real, concrete data point, and it is also exactly the shape `the_book_is_shallow`'s wider
study explains: MILK is board-driven (spread across seeds 88.5, across opponents 54.1), so which
seed floors milk is mostly a fact about *that seed's shop draw and weed layout*, not about a
turn-by-turn sell-order-shaping bug on our side.
`HOLD_A_FLOORED_BOOK`, `PRICE_AWARE_SELL_CAP` and `RESERVATION_SELL_CAP` already ship ON and already
price against `town_drain_remaining` — the wider doc's own conclusion, "the sell side already does
all of this and is not where the gap is," matches what a day-8 trace on one seed also suggested
before the fuller study arrived: the sell side is reacting correctly to a book whose future
absorption is already thin by the time selling starts, and no amount of order-shaping recovers a
book that eight shop draws never gave WOOL or MILK enough demand to hold.
**Do not re-open this; read `the_book_is_shallow_2026-08-09.md` instead**, which answers it properly
with a paired 36-season design this single-seed trace cannot match.

## 3. Animal loss on the shipped agent: characterized, not fixed

Explicitly flagged by the coordinator as real, separate from the price question, and not to be
traded against it.
On the four seeds measured here the shipped agent already loses very little: 1 animal on seed 13,
0 on seed 17, 0 on seed 19, 1 on seed 23 (`tests/test_high_value_produce_reaches_the_shed.py`'s own
fixture measures the same seasons).
Seed 13's loss happens on day 9, herd 7 -> 6, early in the game while the herd is still small.

This was not chased further.
`cover.py` already carries substantial, measured machinery specifically for this
(`REQUIRED_OPS = ("FEED",)`, the `at_risk` discrimination between an animal that slipped once and
one that will die tonight, `DROP_WHERE_THE_TOUR_ALREADY_STANDS`), and the file's own comments record
that a day-9-scale single loss on a small early herd is a materially different problem from the
20-head-herd routing constraint already measured and left open in `cover.py`'s own docstring ("even
with abundant wheat sitting in the shed, the crew could not reach all 20 animals on a single day at
this herd size").
A one-animal, day-9 loss on a 7-head herd needs its own board-specific trace before touching
anything, and the **hard constraint on this task is to not touch the feed-buy line**, which is where
most of `cover.py`'s FEED-related machinery ultimately connects.
Flagged as open rather than guessed at.

## 4. What was implemented

- `tests/test_high_value_produce_reaches_the_shed.py` — new. The corrected destroyed-vs-late
  instrumentation, as a regression guard (§1).
- This doc.

**Nothing in `kagg/search/cover.py` or `kagg/search/schedule_agent.py` was changed.**
The testing discipline this project runs on is "no code change without a failing test that proves
the problem first," and after exact measurement, twice, from two different angles, there is no
delivery/discard/shed-capacity problem to fix here — forcing a change in against that finding would
be exactly the failure mode `CLAUDE.md` warns about ("patching my own component instead of
questioning it is the tell").

## 5. What is still open, and belongs to a different investigation

`the_book_is_shallow_2026-08-09.md` §"The actual gap": the schedule commits to a cow/sheep/crop mix
from a fixed target sheet decided before the board is known, and nothing in that path reads
`town["unlocked_shops"]` — which is `shared: True` and readable every turn, with 2-3 shops already
known by day 6-9 while most animal buying is still ahead.
WOOL is sold by one shop of eight (34% chance it never unlocks); MELON by none.
That is a production-mix question, not a delivery one, is a materially larger change (it touches
the schedule/target-sheet selection logic, not `cover.py`'s routing), and the coordinator's own
measurement constraint applies to any candidate: paired across seeds *and* opponents, because the
same shipped agent already banks anywhere from $16,888 to $163,036 across 36 seasons with no code
change at all.
Not attempted here — flagged as the next investigation, per the superseding doc.

## Files touched

- `tests/test_high_value_produce_reaches_the_shed.py` (new)
- `docs/fable_the_delivery_problem_2026-08-09.md` (this file)
- `data/seed_scripts/top_guys/` copied into this worktree from the shared checkout (gitignored,
  needed for the tape fixture; not a tracked change)

No changes to `kagg/search/cover.py`, `kagg/search/schedule_agent.py`, or any other production code.
