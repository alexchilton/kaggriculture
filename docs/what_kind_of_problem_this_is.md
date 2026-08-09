# What kind of problem kaggriculture is

Written 2026-08-05, after a day in which every result that looked like a fact about the game turned
out to be a limitation of our own code. The purpose is to name the problem class precisely, so the
next session reaches for the right tool instead of rediscovering the wrong one.

## The short version

**It is a deterministic, open-loop, multi-dimensional knapsack with a time-phased budget, played as
a best response against a fixed field.**

Every clause is load-bearing and each rules out a family of approaches. Measured rather than argued:

- **the allocation is computable** — closed form from the town's drains reproduces the leader's farm;
- **the schedule genuinely needs search** — greedy-by-payback under a cash simulation recovers only
  23% of what a beam finds, so this half is not reducible to a rule;
- **the simulator is the verifier**, never the search engine.

We spent weeks treating all three as one undifferentiated search problem.

## Why it is not a reinforcement learning problem

Not because RL is weak, but because the problem has no property RL is for.

**There is nothing to react to.** The top of the leaderboard submits a fixed 720-turn tape, and four
fresh replays of the leader are byte-identical in every derived quantity across four opponents and
both seats. A policy mapping observations to actions is solving a harder problem than the one being
scored.

**The environment is deterministic given the tape.** `Q(s, a) = V(s')` can be *computed* by
simulation rather than estimated. Fitted-Q, TD learning and replay buffers all exist to approximate
a value function we can evaluate exactly.

**The horizon is 30 decisions, not 720.** A season is a bag of chains, one per unit. Credit
assignment over 720 steps was the motivating difficulty for the RL framing and is an artifact of the
wrong decision granularity.

**And the reward is terminal.** The ladder is Elo, so a $43k win and a $4k win score identically.
That is a *ranking* objective over a fixed field — a best-response computation, not a control
problem.

RL becomes right again if the field turns adaptive, or if the state space grows past what exhaustive
evaluation can reach. Neither is true today. See `rl_feasibility.md`.

## The structure, formally

Choose a set of **chains** (a crop block or a pen group, with a start day and options) to maximise
the final bank, subject to:

| constraint | value | notes |
|---|---|---|
| tiles | 100, non-overlapping | 25 owned at spawn; 75 after two parcels |
| units (slots) | one chain per unit | a unit's position is a cumulative sum, so two chains on one unit interleave and both fail |
| turns | 23 work turns per unit-day | the binding constraint on tiles per chain |
| market drain | 8 products, 2,086 crop + 1,122 animal units | how much the town removes before the price floors |
| cash | $3,000 at dawn on day 0 | **a flow, not a stock** |
| land | $1,000 / $2,000 / $4,000 in fixed order | `_do_buy_land` ignores which quadrant you ask for |
| hires | Fibonacci in the day's hire count, resets daily | 12 hands is $376/day; 17 is $4,180/day |

The objective is **nearly additive**: chains interact through exactly three channels — the shared
price curve per product, cash timing, and tile/slot exclusivity. Nothing else couples them.

That near-additivity plus the *concavity* of the price curve is what makes the **allocation**
tractable: with a concave objective and linear constraints, ranking by marginal-value-per-resource is
near-optimal rather than a heuristic. See `economics_q5_findings.md` §4 for the arithmetic that
recovers the leader's farm.

**But cash timing is not a mild coupling, and this is where the naive reading goes wrong.** Cash is a
flow, so "chain B is unaffordable until chain A has sold" is a precedence constraint that compounds
over thirty days: which chain to fund first, and whether a given dollar buys land or seeds, changes
what is affordable for the rest of the season. Measured, that coupling is worth roughly **four times
the allocation itself**. Additivity buys you the mix. It does not buy you the schedule.

## What genuinely needs search

**1. The schedule.** The leader's own timeline is a dependency chain:

```
melon + wheat in NW, day 0-2   ->  revenue by day 3
revenue                        ->  NE parcel day 7, SW parcel day 10
parcels                        ->  strawberry on 41 tiles, days 7-14
```

A hand-built farm cannot test it, because every configuration either has the land or does not —
which is choosing the answer. Measured: asking for 6 wide strawberry blocks with no revenue first
ends with 75 tiles still locked and a starved pen.

**2. Inputs versus outputs.** Wheat's own market is seventh of eight and the leader plants 40 tiles
of it, because it is an **input**: 14 pens eat ~420 units a season and wheat is the only crop
returning cash by day 3. A revenue ranking scores it last. This is the one coupling a purely additive
model cannot represent — the calculator computes 0 wheat tiles against his 40.

**3. The opponent shares the drain.** Both players sell into the same town inventory. Against a fixed
field this is still tractable — it is a best response, and the leaderboard *is* fixed since everyone
submits static tapes — but it is a game, not a solitaire optimisation.

## The tool ordering

1. **Compute the allocation** (`scripts/allocation_calculator.py`). A target, not a starting point.
2. **Beam over chains for the basin** (`scripts/beam_chains.py`) — one exact joint max per slot, the
   simulator as the model, beam width for the interactions. Cheap and deterministic.
   Its weakness is structural: greedy forward selection commits slot by slot and `--refine` sweeps
   *timing only*, so it can re-time a genome but not restructure one.
3. **CEM/ES to restructure out of the basin** (`scripts/search_chains.py --seed-genome`). An ES
   mutates whole genomes, so it can move a slot from melon to strawberry *and* fix that slot's land
   day in one proposal. The beam structurally cannot.
4. **Verify on held-out seeds, in the real environment** (`scripts/arena_gate.py`) — fresh seeds,
   weeds on, live pool. Not optional, and not the same as the in-search score.

> **Status note, 2026-08-08.** The chain-search stack above is the *offline* half and is currently
> parked; what ships is the closed-loop schedule agent in `architecture.md`. The problem
> classification is unchanged and the agreed direction ("offline basis, checked per day, repaired on
> deviation") comes straight from it. Dollar figures produced by that stack are from a codebase that
> has since moved; treat them as evidence about *method*, not as current scores.

## The trap that has cost the most: overfitting the objective

Recorded twice in `CLAUDE.md` — *"a fixed 3-seed objective reported +40% where held-out seeds said
+12.8%"* and *"11 accepted moves in 14 generations for +1.6%"* — and `search_chains.py` had the
defect built in until 2026-08-05: the board draw was cached on one seed, so thirty generations of
five hundred candidates all fit the same sixteen games, and the incumbent kept whatever score its
lucky draw gave it and could never be displaced.

Both fixed: a new draw every generation, the incumbent re-scored alongside its challengers on that
same draw, and a `--holdout` pass that prints the in-search versus held-out gap so the curse is
measured rather than assumed.

**Seed variance is ~15%. Always quote the range.**

## The failure mode to watch for, because it recurred six times in one day

Every one of these was reported by the search as a fact about the game and was actually a limitation
of the chain builder:

| looked like | actually was |
|---|---|
| "animals do not pay" | `ranch()` never collected fertilizer; then capped the herd at 4 |
| "fertilizer does not help" | `grow()` emitted `FERTILIZE` and never *ordered* any, so every op was refused |
| "day 0 is the right time to buy land" | the catalog hardcoded `LAND_DAY_CHOICES.index(0)` |
| "strawberry loses to melon" | `BLOCK_SIZE = 4`, because `grow()` watered every tile every day |
| "four pens is the right herd" | 1 pen = 1 chain = 1 slot, so five pens ate five of eight slots |
| "weeds cost nothing" | true on our farms, false on a farm that replants — carrot +$2,055 with DIG |

**Before believing a measurement about a mechanic, ask what the code could not express.** List what
the action space, the routine and the catalog can each emit.
`tests/test_catalog_covers_every_gene.py` enforces the catalog half automatically — it asserts every
gene `decode()` reads takes more than one value somewhere in the catalog — and it caught a live
instance on its first run.

## The shape of the target

The top of the board is a knife-edge: everyone banks $120k-160k and the leader edges it by ~3%. On
an Elo ladder a $2,634 win scores what a $50,000 win scores, so the target is a **small consistent
edge over several near-equal fixed scripts** — and because they are fixed, they cannot punish
anything. They are a stationary target to compute a best response against.
