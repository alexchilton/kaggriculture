# What kind of problem kaggriculture is, and how to actually solve it

Written 2026-08-05, after a day in which every result that looked like a fact about the game turned out
to be a limitation of our own code.
The purpose of this document is to name the problem class precisely, so the next session reaches for
the right tool instead of rediscovering the wrong one.

## The short version

**It is a deterministic, open-loop, multi-dimensional knapsack with a time-phased budget, played as a
best response against a fixed field.**

Every clause in that sentence is load-bearing, and each one rules out a family of approaches.
Unpacked below.

The practical consequence: **the allocation is computable, the schedule needs search, and the
simulator is the verifier rather than the search engine.**
We spent weeks treating all three as one search problem.

## Why it is not a reinforcement learning problem

Not because RL is weak, but because the problem has no property that RL is for.

**There is nothing to react to.**
The top of the leaderboard submits a fixed 720-turn action tape.
This is not inference: four fresh replays of the current leader (`somewhere after`) are **byte-identical
in every derived quantity** -- same land days, same herd, same seed counts, same crew ramp -- across
four different opponents and both seats.
The only variation in four tapes is 107 versus 106 `FERTILIZE` ops.
A policy that maps observations to actions is solving a harder problem than the one being scored.

**The environment is deterministic given the tape.**
`Q(s, a) = V(s')` can be *computed* by simulation rather than estimated.
Fitted-Q, TD learning and replay buffers all exist to approximate a value function we can evaluate
exactly.
`scripts/beam_chains.py` is a Bellman recursion with the simulator as the model, and it needs no
network.

**The horizon is 30 decisions, not 720.**
A season is a bag of chains, one per unit.
Credit assignment over 720 steps was the motivating difficulty for the RL framing and it is an artifact
of the wrong decision granularity.

**And the reward is terminal.**
The ladder is Elo, so a $43k win and a $4k win score identically.
That is a *ranking* objective over a fixed field, which is a best-response computation, not a control
problem.

RL remains the right tool if the field ever becomes adaptive, or if the state space grows past what
exhaustive evaluation can reach.
Neither is true today.
See `docs/rl_feasibility.md` for the original argument and CLAUDE.md for what was overruled.

## The structure, formally

Choose a set of **chains** (a crop block or a pen group, with a start day and options) to maximise the
final bank, subject to:

| constraint | value | notes |
|---|---|---|
| tiles | 100, non-overlapping | 25 owned at spawn; 75 after two parcels |
| units (slots) | one chain per unit | a unit's position is a cumulative sum, so two chains on one unit interleave and both fail |
| turns | 23 work turns per unit-day | the binding constraint on tiles per chain |
| market drain | 8 products, 2,086 crop + 1,122 animal units | how much the town removes before the price floors |
| cash | $3,000 at dawn on day 0 | **a flow, not a stock** -- see below |
| land | $1,000 / $2,000 / $4,000 in fixed order | `_do_buy_land` ignores which quadrant you asked for |
| hires | Fibonacci in the day's hire count, resets daily | 12 hands is $376/day; 17 hands is $4,180/day |

The objective is **nearly additive**: chains interact through exactly three channels.

1. **The shared price curve per product.** `price = base - amp * shape(inventory - I0)`, floored at 1.
2. **Cash timing.** Chain B may be unaffordable until chain A has sold.
3. **Tile and slot exclusivity.**

Nothing else couples them.
That near-additivity plus the *concavity* of the price curve is what makes the problem tractable:
with a concave objective and linear constraints, ranking by marginal-value-per-resource is near-optimal
rather than a heuristic.

## What is computable in closed form

`scripts/allocation_calculator.py` computes the target allocation from two measured tables --
`chains.DRAIN_UNITS` and `economics/production.py` -- with no fitted constants, and checks it against
the leader's measured season.

Fill each market to its drain, ranked by revenue per unit-day:

```
     product   base   drain      market $
        MILK    160     500        78,432   <- the biggest market in the game
  STRAWBERRY    120     572        66,586
        WOOL    200     284        56,736
       MELON    250     140        35,000
      TOMATO     60     374        21,574
         EGG     50     338        16,582
       WHEAT     25     662        15,986   <- seventh of eight
      CARROT     35     338        11,484
       TOTAL                      302,380
```

Divide each drain by the per-season yield and the answer is the leader's farm:

| | computed | leader actually runs |
|---|---|---|
| cows | 500 milk / 66 per cow = **7.6** | **8** |
| sheep | 284 wool / 48 per sheep = **5.9** | **6** |
| geese | worst pen, smallest animal market | **0** |
| strawberry | 572 / 12 = **47.7 tiles** | **41** |
| melon | 140 / 12 = **11.7 tiles** | **20** |

None of that needed searching.
It is drain divided by yield.

**Why we never saw it:** `DRAIN_UNITS` contained the five crops only until 2026-08-05, so **$151,750 of
demand was invisible** -- including milk, the largest single market.
Every allocation argument this project made was made with half the game missing.
The numbers were in `data/logs/market_ceiling.log` the whole time.

## What genuinely needs search

Three things resist closed form.

**1. The schedule.**
Cash is a *flow*.
You cannot buy strawberry's ground until the wheat has paid, so the plan is a dependency chain:

```
melon + wheat in NW, day 0-2   ->  revenue by day 3
revenue                        ->  NE parcel day 7, SW parcel day 10
parcels                        ->  strawberry on 41 tiles, days 7-14
```

That is the leader's timeline exactly.
A hand-built farm cannot test it, because every configuration either has the land or does not -- which
is choosing the answer.
Measured: asking for 6 wide strawberry blocks with no revenue first ends with 75 tiles still locked and
a starved pen.

**2. Inputs versus outputs.**
Wheat's own market is seventh of eight, and the leader plants 40 tiles of it.
It is an **input**: 14 pens eat ~420 units a season ($10,500 of feed) and wheat is the only crop
returning cash by day 3.
A revenue ranking scores it last.
This is the one coupling the calculator gets badly wrong (it computes 0 tiles against his 40), and it
names what a purely additive model cannot represent.

**3. The opponent shares the drain.**
Both players sell into the same town inventory, so "melon's 140 units" is contested.
Against a fixed field this is still tractable -- it is a best response, and the leaderboard *is* fixed
since everyone submits static tapes -- but it is a game, not a solitaire optimisation.
`data/logs/market_ceiling.log` notes the drain is "1.0x if split evenly between two players".

## How to search it: the tool ordering

**1. Compute the allocation.**
`scripts/allocation_calculator.py`.
This gives a target, not a starting point to explore from.

**2. Beam over chains for the basin.**
`scripts/beam_chains.py` -- one exact joint max per slot, the simulator as the model, beam width for
the interactions.
Cheap, deterministic, and it finds a good basin fast.

Its weakness is structural and worth stating: greedy forward selection commits slot by slot, and
`--refine` sweeps *timing only*.
It cannot restructure a genome, only re-time one.
Measured consequence: widening the catalog made the answer **worse** ($64,349 pinned to day-7 land
versus $62,695 with `{0, 7}` offered), because more options means more ways to commit early to
something locally good and globally wrong.

**3. CEM/ES to restructure out of the basin.**
`scripts/search_chains.py`, seeded from the beam's genome via `--seed-genome`.
An ES mutates whole genomes, so it can move a slot from melon to strawberry *and* fix that slot's land
day in one proposal.
The beam structurally cannot.

Three properties make it viable here: the evaluator is batched (1,024 genomes per GPU call, ~8x CPU),
`decode()` never raises (illegal proposals return as `skipped` and score worse), and the genome is 64
small categoricals.

**4. Verify on held-out seeds, in the real environment.**
`scripts/arena_gate.py` runs a genome through `kaggle_environments` on fresh seeds with weeds, against
the live pool.
This is not optional and it is not the same as the in-search score.

## The trap that has cost the most: overfitting the objective

CLAUDE.md records it twice -- *"a fixed 3-seed objective reported +40% where held-out seeds said
+12.8%"* and *"11 accepted moves in 14 generations for +1.6%"* -- and `search_chains.py` had the defect
built in until 2026-08-05: the board draw was cached on one seed, so thirty generations of five hundred
candidates all fit the same sixteen games.
The incumbent also kept whatever score its lucky draw gave it and could never be displaced.

Both are fixed: a new draw every generation, the incumbent re-scored alongside its challengers on that
same draw, and a `--holdout` pass that prints the in-search versus held-out gap so the curse is
measured rather than assumed.

**Seed variance is ~15%.** Always quote the range.

## The failure mode to watch for, because it recurred six times in one day

Every one of these was reported by the search as a fact about the game and was actually a limitation of
the chain builder:

| looked like | actually was |
|---|---|
| "animals do not pay" | `ranch()` never collected fertilizer; then capped the herd at 4 |
| "fertilizer does not help" | `grow()` emitted `FERTILIZE` and never *ordered* any fertilizer, so every op was refused |
| "day 0 is the right time to buy land" | the catalog hardcoded `LAND_DAY_CHOICES.index(0)`, so no other day was ever proposed |
| "strawberry loses to melon" | `BLOCK_SIZE = 4`, because `grow()` watered every tile every day |
| "four pens is the right herd" | 1 pen = 1 chain = 1 slot, so five pens consumed five of eight slots |
| "weeds cost nothing" | true on our farms, and false on a farm that replants -- carrot +$2,055 with DIG |

The diagnostic that would have caught all six: **before believing a measurement about a mechanic, ask
what the code could not express.**
List what the action space, the routine and the catalog can each emit.
`tests/test_catalog_covers_every_gene.py` now enforces the catalog half of that automatically -- it
asserts every gene `decode()` reads takes more than one value somewhere in the catalog, and it caught a
live instance on its first run.

## Where the numbers stand

| run | result |
|---|---|
| starter baseline | $3,512 |
| melon monoculture, pre-fix | $58,755 |
| day-7 land pinned | $64,349 (4 cows + 1 sheep) |
| wide blocks + pen groups | **$69,690 at slot 4 of 8**, still running |
| real environment, weeds on, 20 seeds | 240/240 wins, $51k-$67k against the pool |
| the leader | $139,121 mean, wins 4/4 by 1.7%-4.2% |

The top of the board is a knife-edge: everyone banks $120k-160k and the leader edges it by ~3%.
On an Elo ladder a $2,634 win scores what a $50,000 win scores, so the target is a small consistent
edge over several near-equal fixed scripts -- and because they are fixed, they cannot punish anything.
They are a stationary target to compute a best response against.
