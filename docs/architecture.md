# The agent, as it actually is

Current as of 2026-08-08, branch `shaping-potential`.
`CLAUDE.md`'s "read these first" list points here for the design; the 2026-07-31 spec it used to
point at described an RL pipeline that is not what ships and has been deleted.

> **Version caveat, added 2026-08-09.** The ladder runs `kaggle-environments` 1.32.6. The parity
> and economics figures below (the emitter 48%/100% table, the $ figures in "the flags that ship
> OFF") were measured on 1.32.2 or an early 1.32.6 fixture that has since moved. **"The simulators"
> section's "300/300 exact, 16/16 fields" is a 1.32.2 statement — both `kagg/sim/` simulators now
> fail parity on 1.32.6 (8 failures), not just the JAX one.** The architecture (schedule ->
> `schedule_agent.py` -> `router.py`/`cover.py`) is unchanged; do not quote the dollar figures here
> as current without re-measuring. See `docs/the_market_2026-08-09.md` for the current market
> picture and `docs/REGISTER.md` for the version caveat that also applies to its STATE block.
> **2026-08-11 addendum:** `docs/the_ladder_is_two_scripts.md` and `docs/what_the_town_will_actually_eat.md`
> are the current position on strategy and market economics, measured from 2,744 ladder seats and 87
> tapes respectively — read them before treating anything below as a target to hit.

## What ships

```
schedule (per-day counts)      what to buy, plant, hire and sell on each of 30 days
        |
        v
kagg/search/schedule_agent.py  a closed-loop agent. Reads obs every turn. No emitter,
        |                      no dead reckoning, no model.
        |  build_nodes         router.py decides WHICH jobs the board offers today
        |  cover.plan          cover.py decides WHO does what, in what order
        |  cover.materialise   inserts the shed trips as real stops
        v
submission/main.py             built by scripts/build_planner_submission.py
```

`scripts/build_schedule.py` generates a schedule; `scripts/schedule_ladder.py` scores one.
`scripts/breakdown.py` is the day-by-day diff against a reference tape and is the metric that
counts.

## Why closed-loop, when the winners are open-loop

The winners submit fixed 720-turn tapes (see `the_field.md`), and this project built an emitter to
do the same. It measured **48% of emitted ops landing**, against the tape's ~100%:

```
                    ours emit/land    tape emit/land
CARE                     312 / 150         308 / 308
FEED                     312 / 142         319 / 319
WATER                    766 / 455         851 / 846
COLLECT_FERTILIZER       297 / 143         318 / 318
HARVEST                  286 / 149         338 / 337
```

Eight separate silent bugs were fixed in one day — a hand waking on the locked `(5,5)` corner, ops
written to an unhired slot, a tour truncated past the end of the day, two parcels ordered against a
bank the day's own purchases had already spent, animals drawn from a shed before the purchase
settled — and every one is the same bug: **emitting an op without checking the state it lands in.**

Reading `obs` every turn makes that whole failure class unrepresentable rather than fixable one bug
at a time. Seven of the nine emitter defects simply cannot occur:

```
op landing        emitter 48%      agent 100%
tape's tile list  worth $23,470    worth $0
tape's order book required          not needed
BUY_LAND          fixed hour, lost the $2,000 parcel   fires when the bank covers it
BUY_ANIMAL        silently no-oped on a thin bank      only ordered when affordable
```

**This is a delivery-mechanism choice, not a rejection of offline optimisation.** The offline
half is still the right direction; see "the agreed architecture" below.

## The day is a covering problem, not a prize auction

`kagg/search/cover.py`, `COVER_PLANNER = True`.

```
resources     k hands, each with `budget` turns (TURNS_PER_DAY - hour)
stops         a tile and the work done standing on it -- SHED TRIPS INCLUDED
travel        Manhattan distance, paid between consecutive stops
objective     COVER EVERY JOB. Ties broken on fewer turns.
```

**There is no price table in it, and that is the point.** The board is known in advance and Seb's
tape proves a day of it is coverable, so the question a day poses is not "which job is worth most",
it is "can thirteen hands cover forty-six jobs in twenty-three turns each". Every job counts 1.

Three moves, and no more — GREEDY cheapest feasible insertion, COMPACT relocation accepted only on
a strict fall, REPAIR that takes one job off a unit and re-homes the displaced one, accepted only
if coverage rises. Deterministic by construction: every tie breaks on a total order, no randomness,
no wall-clock cutoff.

`FEED` is a **constraint**, not a candidate: `consecutive_unfed >= 2` removes the animal outright,
which is a fact about the rules rather than an estimate, so it can live in a file with no prices.

### What it replaced, and the number that justified it

`router.plan_routes` ranked candidates by `prize / marginal cost` out of a derived price table, with
MANDATORY (100,000) and CRITICAL (1,000,000) tiers layered on to stop the ratio misbehaving.
Measured over 12 seasons, **a local search that got BETTER at that objective lost $34,816**
(`data/logs/planner_ab3.log`), and the arm restricted to the mandatory tier alone lost most of all —
because "reach this pen" is priced as lexicographically infinite while a $400 animal yielding
~$160/day plainly is not, so it displaces four real jobs to serve one.

`router.build_nodes` is kept: deciding *which jobs exist* is derived from the reference's own
mechanics. What was dropped is `prize`, `MANDATORY` and `CRITICAL`.
`COVER_PLANNER = False` restores `plan_routes` exactly.

### A shed trip is a stop

The first version of `cover.py` modelled a tour as a list of tiles to work and charged shed trips
inside the cost function — one notional draw at the front, one notional walk home at the back. Both
numbers were right. Neither was a stop, so nothing in a route ever said "be at the shed at this
point" and the executor had nothing to walk to. Getting produce to market was left to four
opportunistic mechanisms plus a `draw` side-channel outside the route entirely.

Seed 11 day 6 is the bill. The row reads `WOOL: 12` and buys two COWs out of the proceeds. The tape
harvests at h0, sells six at h2, harvests again at h2, sells the last six at h5; both cows funded by
hour five. We harvested at h4 and h10, carried ten wool through h11-h18, dropped four at h19 and
took six into the night. The bank sat on $20 all day and the second cow slipped.

Everything needed to plan that was on the board at dawn. `materialise` now derives the shed trips
from the work sequence deterministically and inserts them as real stops, costed where they happen —
which is also what makes the search honest, since it was previously optimising a number no tour
matched.

## The flags that ship OFF, with the number that turned them off

Both target real defects. Both cures measured worse than the disease. **Do not rebuild either
without beating these numbers.**

**`cover.DELIVER_SURPLUS_NOT_THE_ROW = False`** — deliver whatever the unit is carrying rather than
only what today's sell row still owes. The broad version measured **-$15,272 over twelve seeds**.
The defect it targets is real: the 12 melons stranded in hands on day 10 are surplus the row never
names, and that day's `sell` is 35/35 exact.

**`schedule_agent.STAND_AT_A_DRY_SHED = False`** — a unit whose CRITICAL draw finds the shed empty
stands and retries next turn instead of dropping the attempt and walking on.

```
                money@d16   cows   work   idle       (seed 11, weeds off, d0-d16)
  off              23,483    8/8   1412   1300
  on               16,363    5/8   1273   1381
```

A blocked hand is 139 work ops over seventeen days, and work ops are feeds. The animal it saves on
day 12 is real; so are the three cows it costs by day 16. The non-destructive `node.pick` handling
around it is free and stays on unconditionally.
The right fix for the underlying defect — `materialise` plans each tour independently and cannot see
the shed drain from the sell block or another unit's draw in the same replan — is to make the
**draw see the contention at plan time**, not to make the hand wait at execution time.

## Harness warnings that have each mis-scored an arm

- **`scripts/matched_days.py` runs 29 INDEPENDENT days off Seb's board and CANNOT see compounding.**
  It replays the tape to each dawn, so the board, the water debt and everything else resets to a
  well-managed state before every comparison. It has now mis-scored two arms as free
  (`STAND_AT_A_DRY_SHED` was one). **It is not a season verdict.** A planner can be strictly better
  on all 29 sampled days and worse over 29 *consecutive* days.
- **`scripts/breakdown.py --diff`'s `money` row is an AREA, not a deficit.** It sums the per-day
  difference between two bank curves. Read the **d29 column**, or the day the arm targets.
  Misreading it as a deficit drove several wrong conclusions for a whole day.
- **Market rows (`sell`, `buy_product`, `buy_animal`, `buy_seed`) are FILLS; everything else,
  including `hire` and `buy_land`, is an OFFER.** Fills are read off the shed/seed delta on turns
  clean of DROP/PICKUP/PLACE, so they are a **lower bound**. Before the fix, `SELL` over-read 11x
  (165 offers, 15 fills) and `BUY_PRODUCT` 3.4x.
- **`d2`'s residual cells are a churn detector, not a defect.** Its entire remainder is walk
  geometry plus one pickup; `east 0` / `west 0` are coincidences of the current assignment
  permutation, so *any* change to any insertion cost re-permutes it and the coincidence dissolves.
  A change that leaves d2 at 4 has left the dawn permutation alone.

## The agreed architecture — offline basis, checked per day, repaired on deviation

Alex, 2026-08-08. This is the direction, not what ships today.

The runtime planner shrinks from "solve a Team Orienteering Problem 720 times a season under a
one-second budget" to "confirm the board matches the plan, and repair it if a weed landed".

**Why the split works: money and routing decouple at d16.** Read off the schedule's own
`money_dawn`:

```
d0 1,807 -> d4 28 -> d6 15 -> d10 2,220 -> d15 1,076 -> d16 10,448 -> d29 108,153
land bought d4, d8, d10   animals all bought by d14   seeds essentially done by d11
```

| | d0-d15 | d16-d29 |
|---|---|---|
| binding constraint | **cash** — a dollar is a parcel or an animal | **unit-turns** — cash is free |
| what to optimise | selling: timing, price, what to hold | routing: whose hands do what, when |
| coupling | land d4/d8/d10, animals to d14, seeds to d11 | none |

**Every failure measured on 2026-08-08 is in the d16+ half** — sheep starve d16/d17/d18,
strawberries die from d21, the shed overflows d21/d23/d24, idle peaks d19-d28. That is the half
with a fixed crew, a deterministic board, no purchases and no cash constraint: the most obviously
solvable-offline part of the game is where we lose the most.

**Deviation is rare enough to enumerate.** Weeds spawn on empty tiles only, ~6 a season, and only
those landing on ground the plan intends to use matter. Realistically the repair path fires one to
three times a season, and three firings can be unit-tested. A planner firing 720 times cannot.

Three parts: a **money plan** for d0-d15 (needs cash SLACK as a constraint, not a point estimate,
because the opponent contests it), a **physical plan** for the whole season solved offline against
`jax_sim`, and a **day repair** for a weed on planned ground or a purchase refused for cash.

**Why offline is trustworthy:** `jax_sim` reproduces `senkin13`'s real $145k season to **0.2%**,
livestock included, and the residual is a *deterministic* order-book bias so candidate-vs-candidate
comparisons stay self-consistent. At `weed_chance=0` one perturbation's effect is an **exact finite
difference**, not a noisy estimate — the quantity PPO spends a critic and 719 steps of credit
assignment approximating. No legality machinery is needed: an illegal op degrades to NOOP, wastes
the unit-turn and scores worse, so the optimiser rejects it unaided.

Machinery already in the repo: `scripts/optimise_script.py`,
`kagg/search/{plan,scheduler,script_mutate,replay_plan}.py`,
`scripts/build_script_submission.py`, `kagg/search/best_plan.json`.

**Caveat with teeth:** the optimiser's opponents are our OWN recorded agents with weeds off. Any
winner must be scored against the real pool and across weed seeds before it is believed. On
2026-08-08 the uncontested number said we finished $4,586 ahead of Seb and the contested
head-to-head said we lose both seatings on the valid seed.

Keep the starvation floor as scaffolding with an expiry: a dead herd is wrong today whatever
replaces the planner.

## The magic constants are compensation, not design

The comment in `_router_acts` justifying the adaptive design — *"hands are hired through the
morning, so the dawn plan genuinely cannot know how many vehicles it has"* — is **stale**. Measured
on seed 11, all 29 days, the crew resets to 1 each dawn and is final by **h2, h3 at worst**:

```
d0    h0:1  h1:6  h2:7  h3:8
d10   h0:1  h1:7  h2:13
d28   h0:1  h1:8  h2:13
```

From h2 there are 13 known vehicles, 21 known turns each and a fully known board: **273 unit-turns
of complete information**, of which 35-46 go unspent.

`CRITICAL` exists only because greedy cheapest-insertion ranks by `prize / cost` and division
destroys ordering, so "this animal dies tonight" cannot be expressed except as a tier. In a real
solve it is a **constraint**: a plan that starves a pen is infeasible and is rejected.
`PLACE_IS_MANDATORY_FROM_DAY = 14` is a day number fitted to one seed, and generalising it cost
$15,882 on another — a curve fit, not a rule.

**What survives a rewrite is the measurements, not the mechanisms.** The melon water pricing, the
repeated unfed pen, the 101 binned units, the unspent turns beside unserved work — those are facts
about the domain and become constraints and objective terms in any solver. The tiers and the magic
constants must not be inherited as design.

## The simulators

`kagg/sim/` holds a numpy-batched simulator and a JAX port, both parity-gated against
`reference/kaggriculture.py`.

**2026-08-09: both simulators FAIL parity on the installed 1.32.6 env — 8 failures, not just the
JAX one.** The figures immediately below are the 1.32.2 result and are kept for the method, not as
a current status claim.

- **300/300 full-length episodes exact** (on 1.32.2), five configurations from one unit to
  twelve-unit crews with land buying; JAX matches numpy field for field, 16/16 (on 1.32.2).
- **All 18 unit ops and all 6 market orders** are modelled. Until 2026-08-01 it was 9 and 4, and
  the missing half was the entire animal economy.
- Two deliberate divergences, both neutralised in the gate: the weed spawn sequence (an exact port
  costs ~3M Python RNG calls per batch) and the shop unlock order (supplied by the caller).

**Adding an op means adding it to `SCRIPT_OPS` and to `_dense_actions` in `tests/test_jax_sim.py`
in the same commit**, or it is untested by construction and the suite will say so in green.
`parity.py` built its random scripts from `SCRIPT_OPS`, so a harness that could not emit `FEED`
could not fail on `FEED`, and "300/300 exact" was a true statement about a subset.

## Kill criteria, as they stand

| Gate | Criterion | Status |
|---|---|---|
| Economics | heuristic clears **$20k** final bank | **cleared at v4** ($43,540) |
| Sim | parity exact over 1000 random action sequences | **passing on 1.32.2** (300/300); **failing on 1.32.6**, 8 failures, unfixed as of 2026-08-09 |
| RL | explained variance passes **0.5** early | see `rl_feasibility.md`; the RL track is parked |

## 2026-08-09 — Stage-1 review: the $2,484 is a decode veto, not a pricing error

Folded in from docs/fable_stage1_review_2026-08-09.md.
Fable, 2026-08-09.
This reviews **stage 1** — the `chains.py`/`scheduler.py` genome machinery listed above as
"Machinery already in the repo" for the offline-basis architecture — and answers: is the
`revenue_rate` cap the binding problem, why land lands on days 11/15, should stage 1 exist, and
what closes the ~2,000-point gap.
Everything below was verified against the actual saved artifact
(`data/chain_search_scheduled/best_beam_genome.npz`, money $2,484, land days 11/15 — the exact run
in question) and `data/logs/run_scheduler_v7.log`.
Installed env was 1.32.6 (`kg.__version__` checked) at review time, so that version landmine was
closed as of this review.
See also `docs/the_market_2026-08-09.md` §2 for the 1.32.6 `DRAIN_UNITS` overstatement this review
references, and `docs/the_top_five_clusters_2026-08-09.md` for why "get into the v23 band first"
(below) was rated the higher-priority move over reviving stage 1 at all.

### The headline: (b) is not a scheduling bug, it is a decode veto, and it is measured

Decoding the saved genome:

```
reachable_quadrants(g, 12) = 0
land_schedule(g, 12)       = [11, 15]
decode -> used 7, skipped 5
```

The five skipped chains are **every chain that needs land**: the melon block, all three
strawberry blocks, and the fourth wheat block — the entire revenue expansion.
What actually plays is 2 cow pens, 2 sheep pens, and 12 wheat tiles in NW.
That farm banks $2,484 and wins 0/16.
The schedule was never the thing being scored.

Worse: `decode` (`chains.py:687-691`) emits the `buy_land` orders from `land_schedule`
**unconditionally**, while `reachable_quadrants` gates only the *chains*.
So the tape spends $3,000 on parcels on days 11 and 15 and then refuses every chain that would
have used them.
Ground with no crop on it, bought — the exact failure the module's own docstring calls "worse
than no ground".
That is a straight bug independent of everything else.

#### Why the gate says 0 parcels: three cash models that disagree by 10x

- `scheduler.schedule()` (line 241-245) walks a bank that charges seed/animals/feed but **no crew
  at all** — `daily_burn` is feed only, and hires never appear.
  Its day-11 bank for this plan: ~$742-$1,963 depending on reserve.
- `chains.cash_curve()` (line 591-593) charges the **full crew from day 0** —
  `hc[:max_unit].sum()` = $232/day for 11 hands here — even though half the slots start on days
  9-15 and no hand is needed before its chain runs.
  Its curve for the same genome: `[1823, 741, -366, ..., 188, 108, 76, ...]` — **$108 on day 11**.
- The jax sim is the truth, in between.

`reachable_quadrants` breaks at `spent + follow_on > curve[day]` (`chains.py:480`), i.e. it needs
~$1,040 on day 11 and sees $108, so parcel 0 is refused and everything behind it dies.
The comment at `chains.py:458` — "Same rule as `scheduler.schedule`, so the gate and the
scheduler agree" — is false in the one way that matters: same *rule*, different *bank*.
The optimistic model proposes days; the pessimistic model holds a veto; the plan is guaranteed to
be gutted whenever they straddle the affordability line, which is exactly where an aggressive
plan lives.

#### Why days 11/15 and not the tape's 5/9/11

Secondary, but answerable.
Inside `schedule()`:

1. **The inflow is a trickle, not a harvest** (line 242-244).
   `revenue_rate` spreads a drain-capped, price-halved, share-halved season total evenly over 30
   days: a wheat block credits $140/day from day ~5.
   Real wheat cash is chunky — the leaders are buying land on day 5 out of day-3-4 harvests the
   trickle model cannot represent.
2. **Chains before land** (lines 255-265 before 276-287): every affordable pending chain drains
   the bank to below `cost + reserve` *before* land is considered each day, so the bank pins near
   `reserve` and land waits for the trickle to accumulate `price + follow_on + reserve` in one
   day's residual.
   With the v7 mix (3 cow + 2 sheep groups up front, $1,200-1,700 each) that crossing happens on
   day 11-12 for parcel 0 and 15-20 for parcel 1.
3. `reserve` is double-counted: chain placement already holds it back, and the land condition adds
   it again.

Re-running `schedule()` on the reproduced mix: reserves 0/300/800/1500 give parcel days
7/11, 8/11, 5/13, 7/14.
The days move ±4 with an arbitrary dial.
The scheduler does not know when money arrives, so the land day is noise around the
trickle-crossing, not a decision.

### Answer to (1): no, the cap fix is not the binding problem

The cap is real, and the flat melon estimate is exactly as bad as
`test_the_planner_prices_volume.py` says.
But fix it and the pipeline still scores $2,484-class results, because the decode veto guts the
plan downstream of any pricing.
Order of binding:

1. decode vetoes the plan (`reachable_quadrants` vs `schedule()` disagreement) — fatal today;
2. decode buys land for chains it refuses — pays for the veto twice;
3. the trickle inflow mistimes land by ±5 days;
4. the cap flattens the melon/milk/wool estimates — the original (a) question.

And a marginal-revenue curve with a contest term is **still a proxy**, which is the deeper
objection: `run_scheduler.py` already runs the full jitted jax sim per reserve arm to *score* the
result.
The sim is cheap enough to be the objective.
Every hand cash model in this pipeline (`revenue_rate`, `schedule()`'s bank, `cash_curve`,
`_bank_estimate`) has a documented wrong answer in its own comments — the file is a museum of
them.
Do not build a fifth model.
If stage 1 survives at all, replace "propose days from a cash model" with coordinate descent on
`start_day`/`land_day` genes scored directly by the sim.
The scheduler's only irreplaceable output is an *ordering* heuristic, and payback order survives
as a search initialisation.

### Answer to (3): stage 1 in its current role should not exist

Blunt version: stage 1 optimises a proxy (`revenue_rate`) inside a proxy (genome → decode, with
decode holding an independent veto) against a phantom field
(`heuristic,rancher,homestead,carrot` tapes — a pool that predates the cluster data and contains
zero of the three real archetypes).
Three layers of indirection — the memory note "optimise the artifact, not a proxy" names this
exact shape.
It has never shipped and its best output loses 16/16 to its own sibling.

What the cluster doc changes: **the floor of the top five is a public agent we have locally.**
Three of five run kaitofukami v23 byte-identical at 3,117-3,131, and v23 was verified to run
locally.
We are at 1,123.5.
The highest-EV sequence identified by this review:

1. **Put v23 in the arena as the opponent.** Every number in this project is currently measured
   against a field that no longer exists.
   Our shipped agent vs v23, 16+ seeds, win rate — that one measurement reframes everything and
   costs an afternoon.
2. **Get into the v23 band first.** Hand-build the opening from the cluster signatures (or study
   v23's own action stream — it is public and deterministic).
   This is not "give up on search"; it is the same move the field made, and it is worth ~2,000
   points before any originality.
3. **Then search for the counter, which is where the sim is a real edge.** Seb is rank 1 *while
   banking the least money* because he beats the v23 cluster consistently.
   Beating a known, fixed, public opponent is precisely what an exact simulator plus search is
   for — score candidate openings by wins vs v23 in the jax sim, terminal win/loss, exactly as
   `CLAUDE.md` already prescribes.
   In that loop no revenue proxy exists to be wrong.

So: keep the chains/decode/sim machinery — it is the asset.
Retire the scheduler-as-cash-simulator and the drain-capped revenue model.
Stage 1's question ("what mix, what days") stays; its answer method (hand cash models feeding a
genome the decoder second-guesses) goes.

### (4) Everything else found, in this review

- **`decode` buys land its own gate refused** (`chains.py:687-691` vs `674`).
  Fix regardless of any other decision: land orders must be gated by the same affordability the
  chains are.
- **`to_genome` silently truncates** (`scheduler.py:319`): v7 scheduled 14 chains into 12 slots;
  the last two strawberry blocks vanished without a count.
  Skips are counted everywhere else on principle; this one isn't.
- **The per-chain drain cap is not shared.** `revenue_rate` applies `min(units, DRAIN*share)` per
  *chain*, so four melon chains "sell" 4x15 units into a 30-unit drain.
  The model is not even internally consistent about the drain it believes in.
- **`OPPONENT_SHARE = 0.5` vs `--share 1.0`**: `run_scheduler`'s mix deliberately un-halves the
  drain (with a comment explaining why halving is wrong) while `revenue_rate` still halves it two
  calls later.
  The mix and the cash model disagree about the market size by 2x.
- **CARE does not exist in the model.** HealthStone (rank 2) is built on CARE compounding from
  sheep (+3/yield at interval 3).
  No term in `revenue_rate`, `cash_curve`, or the mix targets knows CARE exists, so no stage-1
  variant can ever find or price the rank-2 strategy.
  Same pattern as the animals verdict: ask what the code cannot express before trusting its
  negative.
- **`expected_first_demand_day` draws shops without replacement** (`scheduler.py:99`); 1.32.6
  draws with replacement (per `chains.py`'s own 2026-08-08 comment), so payback ordering is
  computed on 1.32.2 unlock statistics.
  Minor next to the above, noted for when payback order is kept as an initialiser.
- **The opponent pool is the pre-cluster world.** Any stage-1 "wins" number, even after all
  fixes, is a statement about four of our own old tapes.
  Selecting on it repeats the frozen-opponents / wrong-field lesson already in `CLAUDE.md`.

### What the review did not do

No files were modified by this review, other than the source doc it produced.
No long jobs — the two `schedule()` traces and the genome decode each ran in seconds.
The (then) 3-of-5-red test file pinning stage 1's current shape was flagged to hold rather than
fix, because if the cash models are retired in favour of sim-scored day search, `revenue_rate` is
deleted rather than fixed and the tests would pin a corpse.
