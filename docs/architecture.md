# The agent, as it actually is

Current as of 2026-08-08, branch `shaping-potential`.
`CLAUDE.md`'s "read these first" list points here for the design; the 2026-07-31 spec it used to
point at described an RL pipeline that is not what ships and has been deleted.

> **Version caveat, added 2026-08-09.** The ladder runs `kaggle-environments` 1.32.6. The
> economics figures below (the emitter 48%/100% table, the $ figures in "the flags that ship
> OFF") were measured on 1.32.2 or an early 1.32.6 fixture that has since moved. The architecture
> (schedule -> `schedule_agent.py` -> `router.py`/`cover.py`) is unchanged; do not quote the dollar
> figures here as current without re-measuring. See `docs/experiment_log.md`'s "the market" section
> for the current market picture and `docs/REGISTER.md` for the version caveat that also applies to
> its STATE block.
> **2026-08-11 addendum:** `docs/experiment_log.md`'s "the ladder is two scripts" section is the
> current position on strategy and market economics, measured from 2,744 ladder seats — read it
> before treating anything below as a target to hit.
> **PARITY CORRECTION, same day 2026-08-09.** The "8 failures on 1.32.6" statement below was true
> only briefly: **both simulators were made exact against 1.32.6 again the same day**, four
> behavioural rule changes fixed (locked-tile movement now allowed; DROP/PICKUP/PLACE resolve before
> the LOCKED guard; `BUY_PRODUCT`/`BUY_ANIMAL` now fail once the shed is full; shop unlock draws
> **with replacement**, capped at `MAX_SHOP_INSTANCES` — a duplicate-free draw of 8 from 8 shops has
> probability 0.24%, so duplicates are the norm and every parity seed hit one). The stale tape
> fixture (`tests/test_tape_parity.py`) was also found to be comparing against a recorded 1.32.3
> constant ($147,178) rather than the live env; replaying the identical tape into installed 1.32.6
> banks $92,313, and the fixture now compares against the live env at test time. One regression
> surfaced and was left open: `test_locked_chain_relocates::test_two_different_far_tiles_are_not_the_same_farm`
> — an unreachable chain now silently "builds nowhere" instead of relocating, which weakens the
> beam's ability to distinguish candidates. **`tests/test_shop_unlocks.py`'s price-literal table
> still quotes 1.32.2 numbers and needs re-checking against the corrected 1.32.6 table** (frozen-town
> vs test-pinned, reference-schedule vs test-pinned, for WHEAT/TOMATO/EGG/MILK/STRAWBERRY) — flagged,
> not yet done as of 2026-08-09.

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

The winners submit fixed 720-turn tapes (see `docs/experiment_log.md` §27, "what the opponents
actually do"), and this project built an emitter to do the same. It measured **48% of emitted ops
landing**, against the tape's ~100%:

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

**2026-08-09: both simulators were restored to exact parity on the installed 1.32.6 env** — see the
PARITY CORRECTION at the top of this file. The 8-failure state existed only briefly earlier the same
day. The figures immediately below are the 1.32.2 result and are kept for the method, not as
a current status claim; the fix commit did not re-measure the 300/300 figure on 1.32.6 explicitly,
but the parity suite (`tests/test_parity_1326_rules.py`, `test_full_length_episode_against_a_full_shed_is_exact`)
passes on the current tree.

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

## What the shipped agent actually scores against the pool

`scripts/gate_pool.py`, 9-member `COMPETITIVE` pool, seeds 700-705, both seatings, weeds ON, 108
games (2026-08-09): **win 94.4%, draw 0%, mean $108,180.** Per-opponent: mirror 50%/$59,271;
wheat_only, melon_heavy, cow_heavy, carrot_25, small_farm, straw_small, contrarian all 100%;
strawberry 100%/$86,213. This confirms the shipped artifact (`submission/main.py`, `gate_pool.py`)
was never on the `run_arena` state-leak path described below — it reads `obs["player"]` rather than
baking in a seat, and its pool opponents are freshly constructed per match. **There is no
pool-composition gap left to explain from that harness**; `docs/REGISTER.md`'s OPEN-CLI notes on
`LATE_SELL_BIAS` come from a *different*, separately-diagnosed contaminated harness (see below), not
this one.

**A state-leak bug, found and fixed 2026-08-09**: `run_arena` was passing the *same* agent object
into every match while `kagg.search.schedule_agent.make_agent` builds its `state` dict once in a
closure, so a finished season's state carried into the next match and killed the agent — one
`make_agent` object through 3 matches vs `pass` (seed 40) scored $114,028 / $0 / $0. `gate_pool.py`
(the submission gate, via `kagg.arena.pool.evaluate`) and `scripts/arena_gate.py` were never
affected; the original `LATE_SELL_BIAS` §4 figures ($16,146/14.6%, first measured in
`fable_market_shape_2026-08-09.md`) **were** measured on the contaminated path and are superseded by
the honest re-measurement now in `docs/experiment_log.md`'s "the market" section §4
($24,535/27.1%, later reconfirmed as $102,886/100% when
Fable's exact §4 configuration was re-run on the fixed harness — 17.8x on money, 6.2%→100% on win
rate). `run_arena` now requires an `AgentFactory` and refuses a bare callable. A second, unrelated
seat-swap defect for agents with a baked-in seat is tracked as `docs/REGISTER.md` OPEN-13.

## Herd sizing — the count is a floor now, not the schedule's fixed number

Added 2026-08-13, commit `1f7d457` ("Size the herd to the drain, not to the schedule's count"),
`kagg/search/schedule_agent_1455mh.py`. Four defects, one mechanism, measured on five ladder games
of 2026-08-13 (92550780, 92566708, 92565805, 92548920, and one more). **Any doc or comment saying
the herd is fixed at the schedule's count, or that `SHOP_ADAPT_FROM_DAY = 3`, predates this and is
stale.**

**The wool branch used to `return` early**, so the headroom greedy below it — the only allocator
that counts shop INSTANCES rather than shop presence — never ran in the games where the drain is
most extreme. `92550780` drew YARN_STORE three times; the town absorbed 1,074 wool against the ~100
that eight sheep make; wool closed at $252 on a $200 base. Above base means supply never caught
demand — every extra unit that season was worth about $250, and the branch was refusing to buy more.
It no longer returns; a bought-past-cap cow path (`split["COW"] <= WOOL_SHOP_COW_CAP` failing, which
is the *normal* case — the schedule buys eight cows by day 8 and draw #3 lands on day 9, so
`WOOL_SHOP_DRAW_LIMIT = 3` was dead as written) now routes the remaining budget to sheep instead of
falling through with nothing done.

**`want_total` was a ceiling; it is now a floor.** Everything above only ever redistributed the
schedule's fixed count between COW and SHEEP — a town draining 1,074 wool got the same 14-animal
herd as one draining 228. The leader's own tapes say a yarn store by d6 takes him to EIGHTEEN
animals, not eighteen split differently (21 of his 24 yarn games). `HERD_GROWS_WITH_THE_DRAIN = True`
lets the same headroom greedy that picks the species also grow the count, capped by
`HERD_GROWTH_CAP = 4` (takes the schedule's 14 to the leader's observed ceiling of 18, no further)
and gated by `HERD_GROWTH_MIN_YIELDS = 2` (an animal must be able to reach at least two production
events before season end, or it is a pure loss — a sheep bought day 27 first yields day 33).

**The cap is set by the feed bill, not by demand.** At a herd of 16 sheep on day 9, even a
one-instance yarn town still shows 252 units of remaining wool drain against 64 units of production
— the greedy alone would keep buying past what is safe. Every animal eats one WHEAT a day and
escapes after two missed feeds (`kaggriculture.py:804`). `92566708` is what unbounded growth looks
like: the shed held zero wheat from d8 to d12, twelve of fourteen animals walked, and the game ended
$56,006 to $109,034. `HERD_GROWTH_CAP` exists specifically to bound that exposure.

**`SHOP_ADAPT_FROM_DAY` moved 3 → 0.** Day 0 was buying `COW 1 + SHEEP 4` before any shop draw
exists (the first draw lands day 3), which is the single largest uninformed commitment of the
season, kept purely because it matched the reference tape's mix. `_herd_split` already gets this
right when asked — the floors alone turn `COW 1 + SHEEP 4` into `COW 4 + SHEEP 1`, the direction the
expectation wants, since MILK is carried by three of the eight shops and WOOL by one. `92565805`
drew no yarn store at all and the pre-fix code bought four sheep on day 0 regardless. The defect was
purely that the caller was not asking early enough — the day-0 buy is now floor-driven from the
start rather than a fixed opening.

`test_an_early_yarn_store_also_raises_the_herd_total` was `xfail(strict)` with the reason "it cannot
raise it, by design" — written to fail loudly the day it could. That day was 2026-08-13; the marker
was removed, not the test. Each of the four fixes was confirmed red on revert.

**Not yet measured in the arena as of this writing. Unit-tested only** — the commit that landed this
says so explicitly, and no pool or ladder score should be quoted for it yet.

## Matching the tape — planner mechanisms found by diffing against a reference

Folded in 2026-08-13 from `matching_the_tape_mechanisms.md` (itself a 2026-08-13 merge of ten
2026-08-09/-10/-11 write-ups). Every number carried across; source file deleted.

> **Two different tapes appear below — read the subsection headers.** "Seb's tape" sections have
> since been shown to be optimal only under the OLD `townCenterSellInterval=12` economy — his median
> bank halved when the town rebalanced and he has withdrawn from the ladder (`experiment_log.md`,
> "the ladder is two scripts"). **The target is superseded; the mechanism findings are not** — every
> bug found this way is a real planner defect, independent of which tape exposed it. The "Victor's
> tape" subsection is measured against the field's #2-rated player and the currently-active
> submission target — referenced live in `cover.py`, `schedule_agent_1455mh.py`,
> `build_planner_submission.py` and current tests. It carries no target-supersession caveat: it is
> live, current work.

### What a good planner looks like — Seb's route architecture

Reconstructed directly from recorded observation/action pairs across four independent tapes (seeds
`1012428555`/`231975074`/`658760367`/`1440180345`, four different opponents, both seats, both
`townCenterSellInterval` economies), confirmed by replay on five of our own seeds.

**The opening is byte-identical across all four tapes through day 3** (units 24/24, market 24/24 or
near it) and diverges starting day 4 — the first day after `townShopUnlockInterval=3` gives the
agent its first live information.

**Each hand is assigned one of four fixed roles for the whole day** (waterer/feeder/collector/
builder) and **owns a contiguous tile block, walked once, never revisited.** Our own global
re-ranking is measured to cost **16 plants lost to thirst** (14 strawberry, 2 melon) in a season
where Seb's equivalent loses exactly one animal. A worked d0 example: unit 6 sweeps column y=4, then
row x=0, PLANT/WATER on consecutive turns at the same tile — a literal lawnmower.

**Idle time is deliberate, not filled**: 707 idle turns over d0-d16 (124 on d1 alone), work at only
32.7% of all turns season-wide (14.0%-43.3% by day), against 49.1% spent walking — a finished hand
is never reassigned.

**Feed routing splits a pen's day across hands, contradicting our own `crew.cover` design
principle** ("the unit of ownership is the TILE, not the op... a pen's whole day belongs to one
hand"). Read directly off tape `91422988` day 4: Seb scores FEED 7 / CARE 7 / COLLECT_FERTILIZER 6
against our FEED 5 / CARE 5 on the identical board. His day uses three roles — two wheat carriers
that load their whole draw once at dawn (h1, h2) and never return to the shed, plus one animal
carrier that carries the COW for ten hours doing the zero-carry-cost ops (CARE, COLLECT_FERTILIZER)
at every pen it passes. The animal carrier places the cow at (1,3) h12 *without* feeding it; a wheat
carrier already mid-sweep feeds it two hours later at h14 — Seb solves "feed is invisible until the
animal is placed" with a second hand's timed sweep, not by giving the pen to one hand.

Traced identically on our side: one herd hand (u4) carries cow, wheat, feed and care alone, mid-tour
DROPs at h6 (all-or-nothing per `kaggriculture.py:333`, so it dumps the cow too), re-picks up only 1
of 3 wheat requested, and the second cow it places at h14 is never fed or cared for at all. The
wheat ledger is identical both sides (6 dawn + 1 bought = 7 animals) — **we are not underfunded, we
spend a wheat unit on a round trip Seb's design never requires.** Two threads left open: the source
of Seb's seventh FEED against only 6 drawn wheat, and whether our h6-h8 loss of 1 wheat + fertilizer
is shed-capacity overflow or a different hand drawing it first.

Implications for a future planner, not yet built: assign role + contiguous block per hand at dawn,
no global re-rank; emit PLANT+WATER as one owned tile; let a finished hand idle rather than force
work; d0-d3 need no board reading at all (constant); d4+ input is just the shop unlock plus bank.

### The tape-column harness bug — the reason several money/state columns are unreliable

**Proved the `breakdown.py` "tape" column does not reproduce Seb's actual recorded game.** Pushing
his own recorded actions for both seats through a fresh env on seed 11 diverges from his real
recorded bank starting **turn 32 (day 1, hour 8)** by exactly one dollar ($29 charged vs $30
recorded for the same WHEAT purchase) and compounds to a final simulated bank of $10,264-$11,711
against his real $110,820 — roughly 9% reproduction. Root cause: his replay predates the 2026-08-08
kaggle-environments 1.32.6 switch, which re-priced wheat, so his recorded game is fundamentally not
reproducible under the currently-installed engine at all; `weedSpawnChance` (0.0 vs 0.005) makes no
difference to the divergence point. **This closes a disagreement that had recurred "roughly ten
times across sessions."**

Verified clean by the same pass: the starting board is exact (seed 11 reproduces his step-0 board
cell-for-cell) and the schedule derivation is exact (builds/places match his tape every day across 17
days, 19/19, zero mismatches).

**What this invalidates:** every "tape column" state/fill/money figure quoted from
`breakdown.py --tape seb...` after day 1 — melon, pastures, sells, and money are all measuring an
environment that stopped being his game on day 1, not a real target. Two illustrative false
positives: `melon 7/6` and `pens 9/8` at d5 both looked like *our* over-buying but are actually the
*column* being short — the schedule's cumulative counts (7 melon, 9 builds by d5) match our actual
play exactly. This also corrects two specific wrong prior beliefs (recorded in
`.claude/skills/matching-the-tape`) that the contamination was money-only and started at d4 — it is
state+fills+money, and starts day 1 hour 8.

**The ruling that follows: the schedule (build/place/plant/buy/sell counts per day) remains the
valid target; money and realized fill prices are not portable across env versions and should never
be tuned against.**

#### The mechanical fix: repointing the tape

Repointed the test harness's tape fixture (`TAPE_REPLAY`/`TAPE_SCHEDULE`/`TAPE_TEAM`) from Seb's
1.32.2-played tape (`90494364`) to a 1.32.6-played one (`90976060`, "seb1326") and re-derived every
day-specific asserted number from scratch via a ground-truth replay script, because the two tapes
differ structurally (land-buy days 5/9/11 vs 4/6/10, ~19 vs 21 pens, herd flipped MILK 179→303/WOOL
230→104/MELON 132→96), not just numerically. A sanity check reproduced the pre-existing day-6
dawn-bank figure of $1,855 exactly by replaying the old tape under the current env, validating the
method.

The repoint revealed that **days 0-3, previously asserted "already exact," are NOT exact under the
new tape** (day 0 FEED 1/4 CARE 1/4 SELL 7/0, day 3 FEED 4/6 CARE 4/6 SELL 7/5) — so day 4's known
shortfall inherits upstream drift rather than being a standalone day-4 defect. Of 76 tests, 4 were
deleted outright because the economic conditions they measured (a day-5 wheat-reserve race, a
day-6 $800 seed bill, a day-6 wool-sale geometry) simply don't occur in the new tape's schedule
rows, 2 were re-derived and now pass, and 5 remain failing — all pre-existing gaps re-measured
against the corrected target, none newly discovered, including day 4's `HARVEST 11/14, WATER 12/17,
SELL 22/55` and day 6's plant count flipping from under- to over-planting (6 planted against a
target of 4, was 14). **`seb1326` is itself flagged as still the stale interval-12-economy build —
the further recommended repoint is onto Dmitry Belan or Efe Can Celiksoy (`REGISTER.md` OPEN-10).**

### The plan-once architecture and its dawn blind spots

Diagnosed four blind spots in a single-dawn-plan architecture, all traced to `interpreter` applying
unit actions before `_process_market` (`kaggriculture.py:922` then `:928`), all confirmed by a
red-then-green test in `tests/test_the_first_seven_days_match_the_plan.py`:

1. **The crew** — the dawn plan can't see hands hired that same turn. Fixed by
   `PLAN_THE_CREW_THAT_ARRIVES`, modeling hire cost and silent-failure-when-short exactly.
2. **The goods** — a `buy` lands at the end of hour 0, invisible to the dawn plan.
3. **The animals** — `BUY_ANIMAL` commits to shed like a product; `build_nodes` gates PLACE on
   `shed[a]>0`, so an empty pen offers nothing at dawn. Caused d3 and d6 to plan **zero**
   placements despite owning the pen.
4. **The pens** — `build_nodes` only reaches PLACE through an *already-built* pen tile; on d0 pens
   are built during the day, so the whole dawn node set that day is `{BUILD:8, PLANT:17}` with zero
   placements. **"`feed 0/4` on a planned-once day 0 was never a feeding defect — it was two
   placements that were never in the plan."**

**Measured on work-turns-to-tape-339 (d0-d6, against the OLD pre-repoint Seb tape `90494364` — treat
these numbers as target-stale even by the standard of the other sections here):**

```
config                                              geom OFF   geom ON
HEAD (5aa233e)                                          317        305
+ PLAN_TODAYS_PURCHASES                                 290        308
+ purchases + BUILD_THEN_PLACE (merged)                   —        281
+ purchases + PLAN_THE_CREW_THAT_ARRIVES                239        273
full plan-once, PLACE merged onto build                   —        276
full plan-once, PLACE as own node                          —        284
```

**Nothing beats HEAD's 317.** `PLAN_THE_CREW_THAT_ARRIVES` (an env-accurate phantom-crew model)
still loses to the existing two-stage plan-then-replan-at-h1 approach — "the h1 replan is not a
defect." `BUILD_THEN_PLACE` initially collapsed `build_pasture` from 8/8→2/8 by chaining PLACE onto
every pinned pen regardless of whether an animal existed; recovered to 6/8 (281) by budgeting
against actual animal count, still under HEAD. **Only `PLAN_TODAYS_PURCHASES` is kept**: −27 with
geometry off, **+3** with geometry on (interaction-dependent, not independent). Shipped config:
geometry ON + purchases ON = 308.

`DEPOT_RING_FIRST` (the geometry flag) stays ON — Alex's explicit call, twice reaffirmed — despite
costing 12 work turns alone against HEAD and breaking 7 previously-exact d6 rows; the prior OFF
verdict was money-based (money isn't the criterion) and measured against an obsolete planner.

**Two further fixes, found by direct observation:** FEED was being drawn twice per pen because
`PLACE_DRAWS_FEED` added a second wheat unit on top of one already implicit in the placement node's
own `DRAWN` set; and hands were walking straight past hungry animals while carrying 8 wheat because
`_live_ops` was only consulted at tour stops — `underfoot()` now feeds the ground under a moving
hand from both the depot and travel branches.

**Measured nulls, recorded so they are not re-derived:** `RESERVATION_SLIP` 0.10→0 byte-identical;
`CHAIN_OPS` byte-identical (dead code, `COVER_PLANNER=True` means `router.plan_routes` never runs);
several `materialise` delivery rules never fire; `SELL_ROW_PRODUCE_GOES_FIRST` no change;
`END_NEAR_THE_SHED` null on d4, real loss on d6; phantom-crew planning alone (without the other 3
fixes) 317→273 — "it only pays as a set."

**Open items still handed off:** d6 as the worst real day (`place 0/1, plant 13/14, water 16/17,
buy_product 6/9, feed 7/8`); d4's single unfed `care 6/7` (`CARE_WHAT_YOU_STAND_ON` tried and shipped
OFF, xfail strict, because it buys 1 care at the cost of 9 others); the closing shed trip uncharged
(4 fixes tried, all null/negative, needs a per-TOUR not per-day reserve); two never-built rules —
don't dig weeds outside the geometry plan, don't plant what can't finish before season end.

### The cash-ledger / funding-sequencing bug

`schedule_agent_1455mh.sell_deadline`'s `short_of_cash` flag collapses an entire day's bill into one
boolean, ignoring when each obligation is actually due. On day 4 this sums a $400 cow (due h0,
already covered by the dawn bank), a $1000 land parcel (due h21 — the only item genuinely needing
sale revenue), $33 hires and ~$28 wheat into ~$1461 against $480 cash, forcing the whole day into an
h0 sell-everything rush. Seb's actual day 4, read off tape `91422988`, sits idle on $12 from h2 to
h18 at zero cost — nothing is due before h21 — then sells in four waves (h18/21/22/23, summing to 55
wheat+fertilizer) and buys land at h21 funded by earlier order slots the same turn; our agent
rushes selling by h2, dribbles small sells from h6, and stops selling entirely once the land purchase
clears, missing the two biggest waves (his h22 sells 12 more, h23 sells 21 more, ours sells nothing
either hour). `feed 6/7`/`care 6/7` on d4 are downstream of the same bug: the h0 cow purchase drops
the bank to $15 by h2, so the seventh animal's wheat is unaffordable that morning — a
cash-sequencing failure, not a routing one.

**Proposed (unbuilt) fix**: a dated-obligations ledger — walk `[(hour, cash)]` against the live
opening balance to find the first hour the running balance actually goes negative, turn each deficit
into a "N units in shed by hour H" delivery obligation for routing, and space sell waves to let the
book recover between them. A related measurement found landing a load in two waves banked $542 for
54 units against four waves' $774 for 41.

**Ruled out**: staggering hire arrivals off tile (5,5) to avoid crowding — measured LOSS on d4
(water 17/17→16/17, harvest 14/14→12/14, place 1/1→0/1) — because Seb's own tape boxes two hands
doing nothing on that exact tile through d0-d4 with zero cost. `_days_bill` counts the cow correctly
— the bug was never a missing term, it was summing terms with different due dates.

This is the same "no delivery deadline" gap the plan-once section above independently named one day
earlier — this section goes further with a concrete ledger design.

### d4 sell shortfall and d9/d10 placement failures

**d4 — we sell only 41 of the 55 wheat units Seb's tape sells** (5+12+12+20 vs our 39, both matching
their respective breakdown rows exactly), while `buy_product` reads 21/1 — a mirror-image wash
trade. Traced hour-by-hour, HARVEST and delivery timing match exactly on both sides (14/14); the
defect is entirely `DUSK_FEED_TOPUP` (`schedule_agent_1455mh.py:3606-3634`) recomputing the same
feed-reserve quantity (`feed_days(day)*alive` = 7 on d4) independently of the sell-side reserve at
`:2909-2933`, so from hour 18 the agent sells wheat down to the reserve floor then immediately rebuys
toward the same floor, every turn, for the rest of the day. End-of-day wheat is 0/0 both sides, so
nothing is lost — the cost is a spread paid twice on ~20 units/day, contributing to a ~$289 d4 money
gap not fully isolated. No fix was written (read-only pass); the shape needed is unifying the two
reserve computations.

**d9 and d10 both read `place 0/4`** — three chained causes, all directly instrumented:
`router.build_nodes`'s species tie-break types every open pen "PLACE COW" (never SHEEP) whenever
both have nonzero supply — only 2 of 10 identical COW claims are ever affordable against
`plan_supply`'s `stock[COW]=2`; `SHOP_ADAPT_HERD` (active from day 6) buys 4 SHEEP and 0 COW on both
days because it re-derives species from live market headroom rather than the schedule's day mix (all
4 buys both days are SHEEP — already logged in `REGISTER.md`'s OPEN-CLI-2); and the 2 routed COW
claims draw against a shed that genuinely never holds a COW, fail silently (non-critical, no
replan), and strand all 4 real SHEEP purchased that day with no pen ever typed to receive them.

### Victor's tape — current work, not superseded

**Measured against Victor's tape — the field's #2-rated, currently-active submission target, not
Seb's.** No target-supersession caveat applies to this subsection.

#### The spawn-ring step-off drops the depot draw

Found and fixed a bug where the farmer's hour-0 spawn-ring step-off overwrites the planned action
*after* the route has already consumed that hour's real action (a WHEAT pickup on days 3-5), so the
route believes wheat was drawn that never was. This costs 6 unpriced turns (2 for the wasted round
trip, 4 for a triggered fetch-recovery), which on day 4 drops the tour's final stop
`(0,4)[WATER,HARVEST]` — measured as `water 14/15, harvest 4/5` — and cascades to day 5's
`plant 4/5, strawb 6/7`.

The fix ("defer, don't delete," `hold_farmer` + `farmer_start`) makes `_router_acts` skip walking
the farmer's route on an overwritten turn rather than deleting the step, so the real pickup lands
one turn later instead of being lost. Two other fix shapes were tried and rejected: removing the
step-off entirely re-strands a second hand for 23 idle turns; guarding to "only overwrite a MOVE"
silently reduces to the same removal on exactly the days that matter (PICKUP days). Verified with a
test red-at-baseline, green-with-fix, red-on-revert; days 4 and 5 now match on every non-exempt row.

**The fix exposes a genuine, previously-latent router defect**: a newly planted tile starts with
`consecutive_unwatered:1` and weeds at 2, so any plant not watered the same day becomes a weed —
measured directly on tile (5,3), planted day 6 hour 13, weeded day 7 hour 23, never watered once —
because the router prices WATER as a prize rather than a hard co-requisite of PLANT. Stated rule for
future work: "a PLANT whose same-day WATER cannot also be executed is worth LESS than nothing."

Also surfaced: an earlier, still-uninvestigated divergence at day 1 (`care 0/5`), predating and
unrelated to this fix — by the project's days-in-order rule this is technically the first open day
and was not chased in this pass.

A retracted "replant the harvested tile" idea (code-read only, not re-measured) necessarily fails
regardless of router-side fixes, because the pinned-tile gate exists in TWO places
(`router.build_nodes:956` and `schedule_agent_1455mh.py`'s `_live_ops:1349-1352`) and any future
attempt must patch both.

#### The d7 order-queue starvation

The dawn plan correctly sizes and funds day 7's whole 14-unit wheat order at hour 0 ($2,512 bank
against a $480ish order), but the order is silently dropped because the h00 queue already holds ten
other orders (wool/fertilizer sells, seven hires, two cow buys) and the append is gated
`len(orders) < 9` — traced directly to `norders=10, REFUSED`. The agent then falls back to a
1-unit/turn drip through hour 15, which the crew's depot draws (h02-h05) outpace; one hand's 3-unit
want is deleted entirely against a momentarily-empty shed at h02, and a later recovery mechanism
only restores 2 of it. This produces `feed 9/10, care 9/10, collect_fert 6/7` on day 7, and the same
signature (`norders>=9` at h0) recurs on days 8, 9, 11 and 12 — 5 of 13 days measured, only day 7 was
fixed in this pass.

**The fix** keeps the dawn boost live (via a `dawn_row_sent` flag) until the block is actually queued
rather than expiring it at `hour==0`, so a refused block goes out whole at the first turn with a free
slot instead of dripping — which matches Victor's own cadence exactly (his h01 queue is also ten
orders deep, and his wheat block also waits for h02). Result: day 7 now matches on
feed/care/collect_fert (9/10→10/10, 9/10→10/10, 6/7→7/7), d0-d6 are byte-identical, and days 8-10
move toward the tape wherever they move (d10 harvest 5/6→6/6, money 3719→5230 against a 5630 target),
with three cells past the frontier drifting by one, explained as noise inherited from already-
diverged ground rather than a regression.

**Explicitly ruled out as fixes**: waiting longer at the depot (the wheat supply rate itself is the
bottleneck, not patience); marking the feed draw critical (deforms the tour the same way as the
d4/d5 regressions above); re-slotting wheat ahead of hires in the queue (Victor's own tape doesn't do
this either — his h01 queue is also exactly ten orders, and his wheat also waits for a free slot at
h02).

**Open frontier after this fix**: d1 `care 0/5` (explained as us being *correct* — the reference only
banks the care bonus on a fed animal, `kaggriculture.py:816`); no-op digs on empty tiles (tape digs
unconditionally); d7's own pre-existing `buy_seed 11/12` (untouched, now the first live divergence);
then d8 (`plant 8/10, water 18/22, harvest 4/6, feed 11/12, care 11/12, place 1/2`) — d8/d9 still
show a residual `feed 11/12` signature suggesting a related but distinct remaining cause, not chased.

## The spawn-ring misprediction, and why routing can be solved offline

Folded in 2026-08-13 from `spawn_ring_and_routing.md` (itself a merge of three 2026-08-12 write-ups:
`spawn_ring_misprediction_2026-08-12.md`, `fable_spawn_ring_verdict_2026-08-12.md`,
`the_route_is_precomputable_2026-08-12.md`). Every number carried across; source file deleted.

### The mechanism (seed 11, tape `victor`)

`_end_of_day` discharges the whole crew every night; `_arrivals` predicts landing tiles using the
spawn ring **before** the farmer's hour-0 move, but hires settle in the market phase which runs
**after** the unit phase — so every hand lands one ring slot early than planned. Worked example on
d11: predicted `(5,4)(4,5)(5,5)(4,4)...`, actual `(4,4)(5,4)(4,5)(5,5)...`.

**Cost:** u10 on d11 was priced at 23 turns against a 23-turn budget (zero slack); it woke 2 tiles
off, ended 2 tiles short at `(1,2)`, which then weeded (`consecutive_unwatered >= 2`).

### Fix attempted and REVERTED — pinning the farmer is a measured loss

Pinning the farmer on hire turns to force the prediction true was tried and reverted: 17-day grid
money@d16 baseline **17,459 → 16,044**, strawb 35/36 → 33/36, weeds 2 → 4 — `(1,2)` was saved but
three other tiles died in its place, because pinning costs a turn of the 24-turn unit on nearly
every hire day. With the pin on, d11 goes fully green and d10 improves from 14 wrong to 7, isolating
a residual second cause: later-wave hires whose h0-computed prediction goes stale by the time they
land.

**Everything else tried and ruled out on the same seed/tape:**

```
pin farmer                          LOSS      (above)
predict-walks-off-ring              breaks the d9 control (day-dependent behavior)
two-pass re-solve                   initially "doesn't fit time budget" -- see below, now viable
tour slack (START_SLACK_TURNS 1,2)  LOSS      money 26,889->27,538 only by doing less work,
                                               wrong trade on an Elo ladder
buy fertilizer ahead                NULL      order-timing mismatch, and the underlying premise
                                               had already expired (see below)
COVER_PLANNER=False                 bit-rotted, not a valid comparison
```

**Two retractions on the record from this investigation:** "the tape wastes turns watering
pastures" was wrong — board-state contamination from comparing against our own tiles, retracted. And
the fertilizer-starvation premise behind the "buy fertilizer ahead" arm had already expired by the
time it was tested — `FERTILIZER_RESERVE_LOOKAHEAD_DAYS=1` had already fixed supply (shed now holds
14-20 vs the tape's 12-13; u13 gets all 6 FERTILIZER it asks for vs 0 before).

#### The d16 water gap, resolved into two parts

A tour probe found only 2 assigned jobs all season where the unit never stood on the tile it was
assigned (both u13 FERTILIZE) — execution is not the general problem: 39 waters offered, 0
uncovered, 50 idle turns, 96 turns of priced slack on d16. The apparent `water 53/59` gap splits:
a **counting artifact** (op-count 53/59 masks identical 45/45 tile coverage; the tape wastes 14 ops
as no-ops, we waste 8) and a **real deficiency**: weeds 3/0 — we lose `(1,2)` STRAWBERRY (d11),
`(2,0)` WHEAT (d14), `(9,0)` WHEAT (d18); the tape loses zero all season. Cadence matters most for
non-ongoing crops (WHEAT, MELON), where a missed water inside the yield window is permanently lost
yield, not just weed risk.

### The follow-up review: is the two-pass re-solve viable, and a second bug

A second review confirmed the whole prediction sequence
(`_hires_this_turn` → `_clear_the_spawn_ring` → `arriving` → `_router_acts`) runs exactly once per
day at hour 0, and tested a two-pass re-solve directly:

```
day 9    converges in 1 pass (control)
day 11   converges in 1 pass
day 10   needs 3 passes to reach a fixed point (not 1)
```

Settles within 2 corrections on every day tested, but does not converge in 1 pass always.
Wall-clock cost of the hour-0 solve: 0.000-0.002s (d0-6) → 0.075s (d8) → 0.127s (d9) → **0.372s
(d10, 14 hires)** → 0.326s (d11) → 0.426s (d16) → 0.496s (d17). **Three solves at day-10's 0.372s is
over 1.1s, exceeding the 1s `actTimeout`.**

**Recommended order: (b) first, (a) second, not (c).**

- **(b)** dock a second turn off phantom-vehicle budget at `_router_acts` line 1697-1698 — cheap, no
  extra solve cost, bounds the error to Manhattan-2 regardless of cause. Ship this first.
- **(a)** the two-pass re-solve, capped at 2 iterations with a wall-clock guard, second.
- **(c)** binding by landing tile was checked concretely on day 11: predicted per-tile counts
  `(5,4):3 (4,5):3 (5,5):2 (4,4):2` vs actual `(4,4):3 (5,4):3 (4,5):2 (5,5):2` — not the same
  multiset, so binding by landing tile doesn't fix the count mismatch. Do not pursue.

**A new, previously undocumented bug (d): `_hires_this_turn` (line 416) sizes `n` purely from bank
affordability and does not apply `_unwalled_landing_slots`, but the market block that actually emits
HIRE orders (line 3864-3865) does.** They diverge on land-buying days — confirmed live on day 10
(`hands:14, land:1` in `schedule.json`), where days 9 and 11 are `land:0`. **This is the dominant
cause of day 10 being the hard case**, not wave staleness alone.

**Framing check that survives both fix attempts:** the scheduler prices zero margin anywhere — ~20
tiles sit one missed-water from death every day by the watering cadence's own design, so any 2-turn
perturbation from any cause converts to a dead tile.

### Routing is precomputable offline — the board is a deterministic constant

`_initial_tile` and `_default_spawn` are pure functions of coordinates; the only RNG in
`kaggriculture.py` (`random.Random((seed*1_000_003)^day)` at line 858) governs only the shop-unlock
draw and `_spawn_weeds`. Geometry, depots, shed-access tiles and walking distances are therefore
identical in every game — the seed only changes what's worth selling and where weeds appear
(caveat: real-ladder `weedSpawnChance=0.005` introduces some drift; our own grids run at 0.0).

`scripts/solve_day_offline.py` reuses `cover.py`'s own cost model (not a second, possibly-optimistic
model) with a raised LNS deadline and restarts, and confirmed a real defect on seed 11/victor:

**d12 is a real defect.** The shipped greedy planner covers 48/49 (one job left uncovered:
`(9,1)` WATER/HARVEST/PLANT); the offline solve covers **49/49 in 5s, on both restarts
independently**; per-unit turns run 14-21 against a 24-turn budget — slack on every hand, i.e. an
**assignment failure, not a capacity failure.**

**d18 is NOT a defect** — a previously reported "66 of a proven 67" does not reproduce from the
saved fixture (which contains only 66 jobs total); that lead is closed.

The existing ruin-and-recreate (LNS) code already solves d12 given 5 seconds, but is capped in-game
at `RUIN_AND_RECREATE_SECONDS = 0.25`, where over a full 20-day season it measured slightly WORSE
than off (work 1591 vs 1613) — **the mechanism is right, the budget is wrong.**

**Capacity is not the binding constraint generally.** Over d0-d19, seed 11 vs victor: we work more
(1,613 vs 1,556), move more (1,646 vs 1,536) and idle less (539 vs 692) than the tape, yet still bank
less ($26,105 vs $27,133) — we already have a turn surplus, and better routing alone won't close the
gap. The lever is job mix, not turn count.

## Supply-management defects in the market emission block: fertilizer and wheat

Folded in 2026-08-13 from `fertilizer_and_wheat_supply.md` (itself a merge of two write-ups on the
same class of bug — a day-level purchase/reservation budget missing from the market emission block
in `schedule_agent.py`, so a sell row or a per-turn cap drains a shed stock that a same-day work stop
still needs). Every number carried across; source file deleted. Both dated after the 2026-08-08
`townCenterSellInterval` switch (current economy); neither touches CARROT/TOMATO/EGG.

### Fertilizer: sold out from under its own fertilize stops (OPEN)

**d16 (seed 11, tape victor): FERTILIZE offered 12, emitted only 6** (tape: 13); WATER offered 39,
emitted 50 (tape 59); 0 uncovered jobs, 96 turns of priced slack — the crew wasn't busy, the *work
wasn't doable*.

**Mechanism:** `_apply_unit_action` fails FERTILIZE silently on an empty hand (`kaggriculture.py:465`)
— the plan and the walk happen, but the fertilize op never fires and nothing reports it. Per-unit d16
table: u8 got all 3 planned FERTILIZER; u3 got 1 of 2; u12 got 0 of 1 (recovered 1 via COLLECT);
**u13 planned a 6-unit FERTILIZER draw and got 0 of 6.**

**Root cause is 4 days earlier, not a d16 routing defect.** Dawn shed fertilizer tracks the tape
exactly through d10 (`5/5, 5/5, ... 15/15`), then diverges and never recovers (d11 `10/12`, d12
`4/9`, d13 `4/12`, d14 `1/12`, d16 `10/12`). `collect_fert` production is identical to the tape every
day d9-d16 (12/12) — it's not produced differently, it's **spent** differently: the sell rows ask for
`FERTILIZER: 24` (d11), `14` (d12), `8` (d14) out of the same stock the day's own fertilizing needs.
`fertilize` first goes wrong at d12 (2/3), the day after stock first diverges.

**Worth noting:** FERTILIZE sets `fertilized_until_day = day+2`, doubling WATER's yield for 3 days —
a missed fertilize costs 3 days of half-value watering on that tile, part of why `water 50/59` also
trails without any routing defect involved.

**Landmine flagged: `SUPPLY_LIMITS_EVERY_DRAW` (refuse jobs whose supply is short) is OFF** because
it measured worse three times (work down, idle up, d16 money 7,293→3,280→0). Do not re-enable
without pairing it with a purchase-triggering rule.

**Three candidate fixes, ranked:**

1. **Don't sell fertilizer the day's own plan is going to spend** — reserve the planned draw before
   filling the sell quota. This is where the divergence is created and is the top candidate.
2. **Buy the shortfall via `BUY_PRODUCT`** (base price $100) — we hold $14,407 at dawn on d16 with 96
   idle turns, so the precondition is already met.
3. Cap the planned depot pick at real shed stock, and give surplus stops to units whose tour already
   includes COLLECT_FERTILIZER.

**Status note:** the most recent commit on this branch as of this pass ("Hold back the fertilizer
the field is about to ask for") is very likely candidate (1) implemented — check
`schedule_agent.py`'s current fertilizer sell-reservation logic before re-diagnosing this as still
open.

**Two side findings from the same run:** d18 has exactly one uncovered job (`(0,0)`
WATER/FERTILIZE/HARVEST) and that tile dies (weeds 2→4, strawb 35→33 at d18); **d19 is where the
season turns** — leading $23,454/$22,551 at d18, trailing $26,215/$27,133 at d19.

### Wheat: a purchase-budget defect, not a selling one (CLOSED, fix shipped)

**Reframing evidence, 66 of our own 1.32.6 ladder replays** (`townCenterSellInterval=24` only): we
buy **1,099 wheat units/season** against the field's 266-392 (Rayk 266, Lester 266, kakuteki 266,
Syed 323, HealthStone 293, Seb 392). Selling is downstream of over-buying, not the primary anomaly —
money outcomes across the same replays show no clean correlation with sell volume (Rayk/Lester sell
only 305, bank $125-130k; Syed sells 649, banks $101k; Seb sells only 84, banks $74,264),
undermining a pure sell-side framing.

**Mechanism:** the feed-buy sizing term `herd = feed_days(day)*alive - fed_today - on_hand` in
`schedule_agent.py` had **no day-level purchase budget**, bounded only by the per-turn
`FEED_TURN_CAP=6` (a 144/day theoretical ceiling), and dominated the emission formula from ~day 12
onward. Measured on seed 11 vs Seb's tape via `kagg.analysis.fills.record_fills` ground truth:
unfixed bought 1,800, sold 1,456, banked $45,797 — herd path hit `FEED_TURN_CAP` on 20-24 of 24
turns every day from d17-29.

**Shipped fix: `FEED_BUY_CEILING_DAYS=2`** — adds a `herd_ceiling` (credited on asks, via
`state["ordered"][("feed","WHEAT")]`) and a `herd_floor` (credited on arrivals,
`alive - fed_today - on_hand`, so a real shortfall is never silenced). Swept at 1/2/4:

```
FEED_BUY_CEILING_DAYS=1  bought unchanged-tight, causes REAL herd starvation:
                          day 16->17 herd drops 20->14 with zero recovery, wheat sitting idle in
                          the shed (16-19 units) while only 7/20 animals get fed -- under tight
                          supply the bottleneck is crew/routing capacity to physically deliver
                          wheat, not wheat supply itself.
FEED_BUY_CEILING_DAYS=2  SHIPPED. bought 797 (-56%), sold 458, bank $46,370 (+$573 vs unfixed),
                          zero herd drops across all 30 days.
FEED_BUY_CEILING_DAYS=4  bought 1,328 (-26%, barely bends the curve), bank $46,834,
                          zero herd drops.
```

`=2` cuts purchases 56% at bank parity (+$573) with the same zero-herd-drop safety record as
unfixed — the shipped value. **The deeper routing/labor constraint the `=1` experiment exposed —
crew can't physically reach 20 animals in one day even with abundant wheat in the shed — is
explicitly NOT fixed here**, a separate, deeper bug flagged for future investigation.

**Two false leads recorded, so they are not repeated:** `PYTHONHASHSEED` was ruled out directly
(pinned 0/1/2 and default all gave identical 373); a run-to-run discrepancy (1,800 vs 373) turned out
to be caused by a second, concurrent session editing the shared main checkout mid-investigation,
silently injecting an unrelated in-flight fix (`FEED_BUY_TURNS_PER_DAY`) — resolved by reconstructing
the true "before" state via reversing the investigation's own diff. General warning: do not re-read
a shared checkout mid-session from an isolated worktree.

Tests: `tests/test_the_herd_buy_has_a_day_budget.py`, two tests, revert-and-confirm done per
`CLAUDE.md` discipline (reverting turns the budget test red again while the anti-starvation test
correctly stays green on unfixed code too, confirming it isn't accidentally carrying the whole
signal).

## Kill criteria, as they stand

| Gate | Criterion | Status |
|---|---|---|
| Economics | heuristic clears **$20k** final bank | **cleared at v4** ($43,540) |
| Sim | parity exact over 1000 random action sequences | **passing on 1.32.2** (300/300); **restored to passing on 1.32.6** as of 2026-08-09 (four rule fixes — see PARITY CORRECTION above); one search-layer regression left open (`test_two_different_far_tiles_are_not_the_same_farm`) |
| RL | explained variance passes **0.5** early | see `docs/experiment_log.md` §32; the RL track is parked |
