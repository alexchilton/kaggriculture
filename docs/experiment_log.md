# Experiment log

Append-only record of what was tried, what it scored, and what it taught. Newest last.

The point of this file is that several things in this project were "discovered" twice because a
measurement was made and then not written down. **If you measure something, put it here.**
`REGISTER.md` is the live open/closed list; this is the history.

> **Version caveat, added 2026-08-09.** The ladder moved to `kaggle-environments` 1.32.6 on
> 2026-08-07/08 (`competition_brief.md`, "version skew"). Entries below that date were scored on
> 1.32.2 and are not directly comparable to anything measured since — the town rebalance changed
> absorption by up to 4.67x on melon. Treat every dollar figure here as dated by its own entry, not
> as a current baseline. **"The market" and "the ladder is two scripts" sections below (added
> 2026-08-13, folded in from `the_market.md` and `the_ladder_is_two_scripts.md`) hold the current,
> 1.32.6-dated market and strategy findings** — read them before treating any numbered entry above
> as a current baseline.
> **SELLABLE caveat, added 2026-08-13.** `SELLABLE` excluded CARROT, TOMATO and EGG from every SELL
> our own agent could emit until commit `c99a8a5`. Any entry below concluding something about those
> products not selling, or about geese/eggs being unprofitable, was measured with that revenue line
> disconnected — flagged inline wherever it recurs in the sections added this pass; older numbered
> entries are not individually re-audited for it, so treat any pre-2026-08-13 carrot/egg/goose
> verdict as suspect until re-checked.

Rules for reading it: a score is mean final bank, seat-swapped, on held-out seeds never used for
tuning, against the named opponent. **Seed variance is ~15%** — identical parameters score $11.5k on
one 8-seed set and $13.3k on another. Always quote the seed range.

---

# Part 1 — the heuristic era (2026-07-31 to 2026-08-01)

| # | What | Score | Ladder |
|---|---|---|---|
| 0 | `starter` built-in baseline | $3,512 | — |
| 1 | v1 wheat only, timid hiring | $8,641 | — |
| 2 | v2 fixed hiring and land timing | $11,296 | — |
| 3 | v3 ES-tuned parameters | $13,486 | — |
| 4 | v4 melon quadrant + wheat | $43,540 | **429.9 — lost** |
| 5 | v5 opponent-pool tuned, price-aware | $35,544 | **613.5** |
| 6 | v6 deferred selling, 8-strategy pool | $37,060 | ~546-622, unsettled |
| 7 | v7 `contrarian`, opponent-reading crop choice | $45,769 | — |
| 8 | v8 ES-tuned `converter` | — | **712** |
| 9 | v9 `shepherd` | — | 548.4 |

The $20k kill criterion cleared at v4, so the economics model is vindicated rather than falsified.

## 1-3. Parameters, and the two methodological failures

`scripts/tune_heuristic.py`, a (1+lambda) hill-climbing ES over seven parameters. It refuted a doc
claim the agent had inherited — that aggressive hiring is "close to free money". Hire cost is
Fibonacci **and resets every morning**, so it is paid 30 times: 8 hands is $54/day (~$1.6k a
season), 14 is $986/day (~$29.6k, more than the extra labour earns). Search moved hiring **down**
from 17 hands to 8.

1. **Seed overfitting.** Three fixed tuning seeds reported **+40%**; held-out seeds said **+12.8%**.
   The baseline's tuning-vs-held-out gap was 8% and the tuned config's was 35% — that gap *is* the
   overfitting signature. Fixed by resampling seeds every generation and re-scoring the incumbent on
   the same fresh seeds.
2. **Winner's curse.** After that fix the search still "moved" 11 times in 14 generations for +1.6%
   total. Fixed by re-evaluating the winner on a fresh draw before accepting.

**The parameter layer is exhausted.** ES tunes numbers; it cannot invent structure.

## 4. Melon quadrant — the economics model's prediction, cashed in

Melon is the only product no shop demands, so its price is set purely by town-centre drain, which is
identical on every seed. Swept tile count on held-out seeds:

| melon tiles | 0 | 6 | 12 | 18 | 25 | 40 | 60 |
|---|---|---|---|---|---|---|---|
| mean bank | 13,218 | 26,656 | 39,085 | 39,087 | **43,602** | 39,572 | 37,912 |

Peak at 25 tiles — a full quadrant — matching the offline model. Beyond that, melon's shallow market
(~113 units at half base against a season drain of 140) costs more than the extra tiles earn.

## 5. The submission that lost, and what it cost to learn

v4 scored **$43,540** locally and **429.9** on the ladder. Both downloaded replays were losses:
$27,119 vs $33,520 and $27,640 vs $41,595. Not a crash, not a timeout — max turn latency was 18.9 ms
against a 1000 ms limit. **The measurement was wrong.**

| Opponent | v4 bank |
|---|---|
| `starter`, which we tuned against | $43,636 |
| a copy of itself | $21,200 |

`starter` sells almost nothing, so the market was never contested and every number was roughly
**twice reality**.

The replays showed the winner farming strawberry at $310/unit while we crashed melon to $7, owning
all 100 tiles to our 50, and leaving 54 tiles as weeds and still winning — the win came from crop
choice, not execution.

### Four reversals worth remembering

1. **The opponent pool must be frozen.** The first version built pool members from the candidate's
   own parameters, so changing the candidate changed the opposition. That produced a confounded
   result — cows appeared to lift win rate 62% → 81% — which fully reversed once fixed.
2. **Price-aware selling** (hold below 55% of base, refuse seed below 45%, dump from day 28) is
   roughly neutral on score, because the shed fills and forces the sale anyway. Kept as insurance
   against the $7 dumping.
3. **Animals: measured, and switched off — and this was WRONG, see #10.** Per-tile arithmetic said
   cows were the best tile in the game ($725, or $2,116 with CARE, against wheat's $452). Against
   the frozen pool: **70% win / $33.3k with none, 62% / $23.0k with ten, total collapse to $467 at
   sixteen.** The gap is **routing**: a cow needs 4-6 actions a day plus a walk to the shed for
   feed, against wheat's ~1.5 per tile. **Per-tile revenue rankings that ignore action cost are not
   decision-ready.**
4. **Melon 25 → 12 → 25.** Against `starter`, 25 looked best. In mirror matches 12 looked best.
   Against the frozen pool on win rate, 25 is best again (77% vs 67%). **A mirror match optimises
   the symmetric case, which is not what an Elo ladder rewards.**

## 6. Deferred selling — the money-versus-winning result

192 games (12 seeds x 2 seats x 8 opponents):

| hold_days | win rate | draws | mean money |
|---|---|---|---|
| 0 | 81.2% | 12.5% | $36,996 |
| **10** | **90.6%** | 6.2% | $37,060 |
| 14 | 77.6% | 7.3% | $37,505 |

**Money barely moves; win rate moves 9 points**, and `hold_days=14` banks the *most* money while
winning the *least*. Had we selected on mean bank, as v1-v4 did, we would have picked the worst of
the three.

Tested head-to-head against `melon_heavy`, varying **both** sides (12 seeds x 2 seats): whoever
holds beats whoever does not, **100% to 0%**; when both hold it returns to the symmetric baseline.
So it is a genuine best response, not a pool artifact — and its edge decays if the field adopts it.

*Methodological note:* the first version of that test reported identical numbers for both opponent
settings, which is what exposed it as broken — `evaluate` runs matches in worker processes that
re-import the module, so mutating `pool.BASELINE` in the parent never reached them. **Ask what a
passing test would look like if the mechanism were broken.**

## 7 & 11. The pool was one strategy in eight hats

Section 7 widened the pool from five to eight and called it "eight competing strategies". It was
not: every member was `heuristic.make_agent()` with different dials — identical tile ordering,
hiring curve, job priorities, sell cadence. It tested robustness to **crop mix** and nothing else,
which is precisely the axis the ladder losses were *not* on.

`kagg/agents/contrarian.py` is one genuinely different agent: it reads the opponent's board (both
farms are fully visible; nothing else in the pool looks), routes compactly by distance to the
nearest shed-access tile, waters before it harvests on the last day of the window, and uses
per-product sell floors read off the curve shape.

12 seeds x 2 seatings, held out, then re-run on a second independent draw:

| | seeds 300-311 | seeds 500-511 |
|---|---|---|
| heuristic vs the old 8-member pool | 92.2% | 93.2% |
| **heuristic vs the pool with `contrarian` in it** | **81.9%** | **82.9%** |
| `contrarian` vs the 8 heuristic-based members | 92.2%, $45,769 | 90.1%, $45,920 |
| `contrarian` head to head vs the heuristic | **100.0%** | **100.0%** |

**Adding one opponent cost the heuristic 10.3 points of measured win rate.** The pool was hiding a
weakness exactly as the ladder results implied.

Ablation — the case for reading the opponent (same 8 opponents, seeds 300-311):

| variant | win rate | mean bank |
|---|---|---|
| reads the opponent's board | **92.2%** | $45,769 |
| hard-wired to melon | 90.1% | $41,087 |
| hard-wired to strawberry | 74.5% | $26,306 |

### Two bugs that produced plausible scores

- **Buying land silently abandoned ten growing tiles.** Unlocking a quadrant makes *closer* tiles
  available, so a plain nearest-N set drops crops already in the ground; they go unwatered and weed
  two days later. Land bought day 7, ten weeds day 9, **$9,052**. Keeping any tile already growing
  took the same agent to **$42,460** against the same opponent.
- **The agent quit melon because it had successfully sold melon.** The contested test read market
  inventory on the theory that inventory is a durable record of a rival's sales. It is not: melon's
  `max_yield_day` is 12, so inside the window where the decision is live an above-`I0` melon
  inventory is **always our own**. Cost $5,884 of mean bank at an identical win rate.

## 9 & 12. The simulators, and a throughput figure that was wrong

Built numpy-batched rather than JAX, on the grounds that the hard part is one-unit-at-a-time market
settlement and that is far easier to make exact with ordinary control flow. JAX ported after.

| Workload, B=512 | numpy | JAX (scan) |
|---|---|---|
| farmer (1 live unit) | 95k | 434k (4.6x) |
| full crew (24 units) | 15k | 151k (10.0x) |
| full crew, B=16384 | 11k | 470k (**42x**) |

**The real speedup over the reference is 30-200x on realistic workloads, not the 1,032x first
recorded.** That figure (and a later 752k) was measured with one live unit on an empty board issuing
WATER against nothing, so nearly every masked update hit its `if not active.any(): continue`
shortcut. **It benchmarked the shortcut.** The headline was repeated in commit messages, the README
and two docs before being caught.

Absolute throughput moves by up to 2x with machine load. **Only ratios against a same-time control
are trustworthy, and the workload must be stated next to the number.**

### The bug only the end-to-end gate caught

The first run of the gate scored **0 out of 40** while all 136 component tests passed and a 200-step
end-to-end check passed. `ops.plant` only plants on an empty tile but the game loop spent a seed
regardless. A PLANT onto an occupied tile is a free no-op in the reference; in the sim it silently
burned a seed. The farm starved gradually, so the divergence did not surface until step 130-320 —
past the length of the short check.

**Unit tests verify components; only the gate verifies composition. A short parity check is not a
weak version of a long one, it is a different test.**

## 14. Parity closed — and the harness was the thing that was broken

Recorded as "8/12 under hiring" and blocking training. Now **300/300 full-length episodes exact**
across five configurations. Five things were wrong; only three were in the simulator.

**Hiring was a red herring**, and isolating before theorising took ten minutes:

| configuration | result |
|---|---|
| one unit driven, hiring **and** market on | 8/8 exact |
| six units driven, **no hiring**, no market | **1/8** |
| six units driven, no hiring, market on | 5/8 |

`parity.py` filled six unit actions per player whether or not the farm owned six units. The
reference ignores a surplus action for movement and work but computes the atomic-PLANT block over
the actions **submitted**, so a PLANT request from a hand that does not exist cancelled the farmer's
plant. No real game can reach that — every agent builds its action from `[farmer, *farm["hands"]]`.
**When the gate and the product disagree about the calling convention, suspect the gate.**

Also fixed: both seats are paid the same price on a contested unit (the sim re-quoted after seat 0
committed, docking seat 1 a dollar a unit; a green test had asserted the *wrong* behaviour under a
docstring whose own premise contradicted its conclusion), and the JAX sim was 3 tests red on a clean
checkout with **no atomic-PLANT rule at all**.

**Three of the five fixes were covered by nothing** — the suite stayed green with them backed out:

| fix | suite with it backed out |
|---|---|
| JAX atomic PLANT | 14/14 green |
| JAX same-price quoting | 15/15 green |
| numpy `_process_market` same-price quoting | 237/237 green |

These rules only *discriminate* in a narrow window random play almost never enters. Atomic PLANT
differs from greedy spending only when `0 < seeds < demand`, a window that opened **twice in 2,400
player-turns** and never landed a plant. **After fixing, revert the fix and confirm the test goes
red.**

## 15. The simulator was half a game

Reading episode 89197802 (the top two agents head to head) exposed that the simulator implemented
**9 of the environment's 18 unit ops and 4 of its 6 market orders**, and the missing half was the
entire animal economy. Both agents banked ~$110k against `contrarian`'s $38k and **neither strategy
was expressible**: one drew ~83% of revenue from milk and wool by converting bought wheat into
animal products; the other traded wheat with `BUY_PRODUCT`.

**Parity does not imply coverage.** `parity.py` built its scripts from `SCRIPT_OPS`, which listed
only the ops the simulator already had, so the gate could not emit `FEED` and therefore could not
fail on `FEED`.

Order slotting had been deferred as unreachable — every pairing of our own agents gave $0 of error,
because agents emit sells in a canonical product order. `BUY_PRODUCT` made it reachable, since a buy
quotes at `inventory - 1` against a book the sells have already lifted. `Game._order_book` now
compacts a turn's orders into ten slots and `_process_market` walks them in lockstep, verified by a
400-turn randomised differential test of the market phase alone.

## 10. Animals are viable — our conclusion was an artifact of our own routing

Three of the largest ladder losses ($104k, $93k, $84k) were all **small 8-15 tile farms built almost
entirely on pasture animals, two with zero hired hands**, contradicting #5.

The contradiction resolves cleanly: #5 measured animals **inside our heuristic**, which spreads over
50-100 tiles and hires 8-14 hands. In that layout an animal costs a walk to the shed for feed every
day and the routing swamps the return. **It was never a fact about animals.**

`kagg/agents/rancher.py` inverts every choice: six animals, zero hired hands, ~six tiles, all
adjacent to the shed.

| | rancher | heuristic |
|---|---|---|
| vs `starter` | $44,614 | $43,575 |
| head to head, 12 games | **$42,362, 41.7% win** | $43,575 |

Herd size has a sharp optimum — 4 gives $31.6k, **6 gives $45.7k**, 10 gives $15.9k — and the
binding constraint is the **action budget**, not money.

**Three bugs, each of which pinned the herd at exactly one animal**, and each looked like a strategy
result: three of the four shed-access tiles start locked; an occupied pasture keeps
`kind == "PASTURE"` so the "needs work" check matched the farmer's own tile at distance zero; and
PLACE draws from carried inventory, not the shed. Each produced a flat, plausible score curve across
herd sizes. **"Changing the parameter does nothing" is a bug signature, not a finding.**

## 13. Offline plan search on the fast simulator — a tie from a worse starting point

CEM over a 277-gene closed-loop farm plan, interpreted by `kagg/search/executor.py`. Real
environment, `COMPETITIVE` pool, both seatings, 216 games per cell:

| agent | seeds 400-411 | seeds 500-511 | ex-mirror |
|---|---|---|---|
| heuristic | 81.5% / $36,227 | 82.9% / $36,247 | 87.5% / 87.0% |
| **searched plan** | 80.1% / $45,583 | 78.2% / $45,562 | 87.5% / 87.5% |
| `melon_wheat`, the search's starting point | 69.9% / $28,498 | — | 75.0% |

**Read it as a tie.** Against the eight non-self opponents the two are identical: both beat every
pool member 100% and both lose to `contrarian` 100%. The whole headline gap is the mirror column,
and a mirror is not a best response. Money is 26% higher, which counts for nothing on Elo.

What the search found and where it disagrees with the heuristic: wheat nearly abandoned (5 of 50
tiles against 25), **nine of fifty owned tiles left fallow on purpose**, NE bought on day 0 and SW/SE
never, tomato never sold before the dump day, melon's floor at 0.0, planting stops day 20 and
everything dumped from day 24, headcount ~8. Only the melon gene carries a strong signal
(`p(MELON) = 0.33` against uniform 0.167) — **the crop mix is the finding, the tile map is not.**

Structural handicaps, stated: the plan language cannot express DROP or PICKUP, so a searched plan
can only get produce into the shed at the nightly drop; animals were absent for the same reason; and
selection degenerates to money once win rate saturates against a small pool.

---

# Part 2 — the reframe (2026-08-04 onwards)

## 16. The winners are open-loop, and both tracks were optimising proxies

See §27 below ("what the opponents actually do") for the measurement. The consequence for this log:

**Both tracks optimised parameters of hand-written heuristics rather than the artifact that gets
submitted.** Every layer of indirection between the search space and the submission costs you, and
we had two.

- **The CEM/plan track** searched 283 genes that `executor.py` then interprets, so the ceiling is
  the executor's expressiveness. Measured: **the leaders' own allocation, run through our executor,
  banks $0 and loses 3/3**, ordering 29 animals against a specified 14 and 15 units of feed against
  their 967. Three defects — no cumulative cap on purchases, feed never bought, the stake consumed
  and never recovered — compounding into animals dying and being re-bought.
  This also explained the seeded CEM's bad start (`pop mean 0.03` seeded at the leaders' genome was
  our executor failing on every livestock sample, not evidence against their plan) and retired the
  task "find out why the policy never buys animals": livestock lost money **in our implementation**,
  so not buying animals was the *correct* behaviour.
- **The RL track** paid the full price of credit assignment over 719 steps to learn a behaviour the
  evidence says needs no reactivity at all. See §32 below.

**The validating experiment PASSED.** `senkin13`'s exact 720-turn sequence replayed through our own
simulator reproduces his season to **0.2%**, livestock included:

```
turn  day |  recorded p0      ours p0  | recorded p1      ours p1
 480   20 |       50,796       50,887  |      50,509       50,343
 718   29 |      145,018      144,743  |     143,571      143,884
```

The first attempt returned $0/$0 with a $2 divergence at turn 2: `Actions.hire` was a **boolean**,
so at most one hire per turn was expressible while `senkin13` batches hires on 106 of 720 turns.
Once crew size differed, every subsequent slot-indexed unit action landed on the wrong farmer.
`Actions.hire` and `Actions.buy_land` are integer counts as of 2026-08-04.

The residual ~0.2% is a **deterministic** order-book bias — our `_order_book` lays orders out
canonically while `senkin13` emits HIRE first, and `_process_market` pairs the two players' i-th
orders — so candidate-vs-candidate comparisons stay self-consistent.

## 17. Layer 3 is not plumbing

| layer | question | method | status |
|---|---|---|---|
| genome | what mix of crops and animals | deterministic constrained optimisation | largely done |
| schedule | how many of what, on which day | search on win rate | not started properly |
| **agent** | which tile, which unit, in what order | assignment + routing | **the bottleneck** |

Driving the **same** schedule on the **same** five seeds, execution alone moved the bank from
**$10,134 to $59,716** — 8% of the winner's $127,266 to 47%. No schedule change was involved.

The gate that made it measurable is **the winner's schedule through our agent**: the only input that
cannot be tuned against. Adopting it immediately exposed that a day of "improvements" had been
measured on a schedule that was simultaneously being tuned to route around the agent's faults — 46%
on our plan against 8% on theirs. That spread was the size of the self-deception.

**Every dollar figure needs a fixed, matched seed list.** `env.reset()` draws a fresh seed each
call, and one identical tape banked **$48,144-$59,199 across four runs**. An unseeded figure is not
a rough measurement, it is no measurement.

The four components of layer 3, in the order their absence cost money: **tile uniqueness** (a
schedule-derived task has no stable identity until something pins it), **tour commitment** (the
agent re-picked from the whole pool every turn, so there was no plan to perturb and every priority
tweak made it worse), **tile placement** (adjacency dominates distance; five adjacent tiles is a
four-step tour, five round a ring is twelve), and **zoning** (FEED landed on 81% of animal-days, and
at 81% a herd does not survive — it built to 8 by day 13 and decayed to 3 by day 16 while the bank
climbed $9,273 → $43,938).

### Hypotheses that died to measurement, so they are not retried

- sell orders 60-90% unfilled — the tape's own orders measure identically; the replay observation is
  post-market
- fertilizer lost to the 100-unit shed cap — we bin 27 units a season, the tape bins 7
- ongoing crops wasting production at their yield cap — `atcap` is 0 for both sides all season
- wheat as an appreciating store of value — tried twice; FEED went *down* as more was bought,
  because wheat bought is animals not bought
- crop deaths as the cause of a small farm — watering every tile every day cut deaths 39 → 31 and
  raised peak crops 30 → 37, and **cost $18,569**
- BFS routing — correct on a non-convex board, zero measurable effect
- market timing, front-running, withholding — ~3% of money and 0% of wins

### The failure mode that recurred six times in one day

Every one of these was reported as a fact about the game and was a limitation of the chain builder:

| looked like | actually was |
|---|---|
| "animals do not pay" | `ranch()` never collected fertilizer; then capped the herd at 4 |
| "fertilizer does not help" | `grow()` emitted `FERTILIZE` and never *ordered* any, so every op was refused |
| "day 0 is the right time to buy land" | the catalog hardcoded `LAND_DAY_CHOICES.index(0)` |
| "strawberry loses to melon" | `BLOCK_SIZE = 4`, because `grow()` watered every tile every day |
| "four pens is the right herd" | 1 pen = 1 chain = 1 slot, so five pens ate five of eight slots |
| "weeds cost nothing" | true on our farms, false on a farm that replants — carrot +$2,055 with DIG |

**Before believing a measurement about a mechanic, ask what the code could not express.**
`tests/test_catalog_covers_every_gene.py` enforces the catalog half automatically and caught a live
instance on its first run.

### The chain-search pipeline, run end to end

| stage | what it decides | result |
|---|---|---|
| 1 | the mix (`allocation_calculator.py`) | **$13,479** |
| 1 + 2 | mix and days (`+ scheduler.py`) | **$17,653** |
| beam | mix and days together (`beam_chains.py`) | **$76,169** |

Stage 1 reproduces the leader's mix from arithmetic and still dies, because it ordered four cows and
three sheep on day 5 — $3,100 against a $3,000 bank. Stage 2 adds greedy-by-payback under a cash
simulation and recovers only **23%** of what the beam finds. **The mix is arithmetic; the schedule
is not solvable by a simple greedy rule.**

Beam's structural weakness: greedy forward selection commits slot by slot and `--refine` sweeps
timing only, so it can re-time a genome but not restructure one. Measured consequence — **widening
the catalog made the answer worse** ($64,349 pinned to day-7 land against $62,695 with `{0, 7}`
offered), because more options means more ways to commit early to something locally good and
globally wrong.

---

# Part 3 — the day-matching era (2026-08-06 to 2026-08-08)

Metric: `python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff --no-moves`,
counting **differing fields per day** against Seb's tape. See `architecture.md` for the harness
caveats — every one of them has mis-scored an arm at least once.

## 18. The covering planner replaced the prize auction

`router.plan_routes` ranked candidates by `prize / marginal cost`. Measured over 12 seasons, **a
local search that got BETTER at that objective lost $34,816**, and the arm restricted to the
mandatory tier alone lost most of all. Replaced by `cover.py`, which covers the day's job list with
no price table at all. Detail in `architecture.md`.

## 19. Seven arms against "the harvest reaches the shed too late", all reverted

The symptom was real and traced: day 10, seed 11, the same eighteen melons on both sides.

```
SEB   h6 HARVEST, h9 x2, h12, h14  ->  SELL 12 @h13, SELL 6 @h15   melon in shed at d11 dawn: 0
OURS  h17 HARVEST, h19, h20        ->  hands reach 18 at h21, never dropped;  d11 dawn: 18
```

Six labels — melon timing, the stranded carrier, the return leg, the delivery node, the sell-row
delivery, "shed to shop" — and seven arms, every one reverted. **All seven were judged on season
totals, which is the wrong metric**, and none checked field-by-field whether the arm moved the field
it targeted.

**It was none of them. The WATER ran seven hours late.**

```
hour each ripe MELON tile first fills 6/6 and becomes harvestable at all
SEB   (4,2) h6    (3,1) h9    (4,1) h9
OURS  (2,0) h15   (1,0) h16   (0,0) h18
```

Both sides wake with the same three tiles at 5/6. MELON is a one-shot and `_one_shot_is_finished`
refuses HARVEST while `room > 0` — correctly, since HARVEST demolishes the tile. **Neither side
could harvest before the fill**, and our harvests at h17/h19/h20 land one to three turns *after*
ours. The harvest was always prompt; the drop was always prompt behind it.

`crop_ops` priced an in-window one-shot water at the single unit it adds, **$250**, while an
out-of-window survival water on an *immature* melon priced at `_crop_remaining` — the whole tile,
**$1,250-$1,500**. The planner ranked insurance on a tile that could not yield for two more days at
**six-to-one** over the one water that unlocks same-day cash.

`FILLING_WATER` (`router.py`): when a water fills the tile, the node also offers the HARVEST it
unlocks. Day 10 `money -3082 → -1548`, `sh:melon +12 → 0`, fills `h15/h16/h18 → h10/h15/never`,
**d0-d9 byte-identical**.

**Rejected arm, recorded at the emission site:** pricing the harvest at `held` rather than
`held + gain` is the strictly correct marginal and **gives back the entire gain** (d10 money back to
-3,082), because an immature melon's survival water prices at *exactly* $1,500 too and the surplus
$250 is the only thing breaking the tie.

**Lesson:** every one of the six labels described a symptom at a *later leg*. The question that
cracked it was asked about the **tile**, not the unit, the route or the shed.

## 20. Four attempts at dropping the harvest earlier, all negative

Baseline: 12 seeds, `weedSpawnChance 0.005`, **$119,281** on our schedule and $96,064 on Seb's.

| # | rule | result |
|---|---|---|
| 1 | at a depot, DROP if inventory exceeds `sum(n.needs)` over the remaining route | $119,281 → **$104,009** |
| 2 | same, per-item, route recomputed and re-booked for a same-depot redraw | broke the same test |
| 3 | farm-wide `FEED_DAYS * alive` threshold, no per-unit awareness | endless PICKUP/DROP loop, FEED 0 |
| 4 | both gates plus a `MIN_OPPORTUNISTIC_DROP = 4` floor, firing only on an already-chosen MOVE | tests green, **mechanism worked**, $119,281 → **$110,989** |

**Attempt 4 is the informative one.** It did exactly what it set out to do — the first DROP of the
day moved from h19 to h5 and the day-4 cow was placed — and still lost $8,292, because
`DROP 116 → 137` bought `HARVEST 300 → 294`. **Twenty-one extra shed trips bought six fewer
harvests.**

**The finding: a late harvest is not free money left on the table — it is already priced.** A unit
standing at a depot is one step into its next job, and pens sit ON depot tiles by design, so a unit
servicing the herd passes a depot constantly and every one of those moments costs a turn if taken.

## 21. Pen geometry is not a lever

Handing ourselves Seb's exact eight day-0 pen tiles, taken off his own board:

```
          d0  d1  d2  d3  d4  d5  d6  d7  d8  d9 d10 d11   total
baseline   7   6   4   7   7   7  14  21  15  16  23  23    150
his tiles  6   7   7   6   8   7  14  21  15  14  25  18    148
```

Two cells out of 150, with d1 and d2 going backwards. Our day-0 pens sit on y=3,4 and his on y=2,3,
which reads like a real difference and is not one: **the Manhattan sum from (4,4) is 22 for both
blocks**, and 23 for both on day 6.

A related arm — honour the schedule's `places` order so a SHEEP lands on the depot pen — measured
**59 cells against 52**, and an arm honouring intent *only* on the four depot tiles measured
identically to the cell. Three different mechanisms (value ranking, load ranking, schedule intent)
all landing on the same 59-cell line: **the occupant IS the variable, and every route to it costs
the same.** The regression is that the resequenced draws leave the feed wheat in the shed, so two
day-0 FEEDs are skipped and `sh:wheat +2` persists all season.

`DEPOT_RING_FIRST` (site tiles by distance to the nearest owned depot) ships **`None`, off**:

| arm | money sum | valid wins |
|---|---|---|
| always on, 6 seeds | **-33,133** | 2/6 → 1/6 |
| from the SW purchase, tuning seeds | +20,526 | 2/6 → 2/6 |
| from the SW purchase, **held out** | **-11,111** | 1/6 → **3/6** |

The money sign **reversed on the fresh draw** — the winner's curse this repo has been bitten by
before. Two unconfirmed halves pointing opposite ways is a null.

**The reusable finding is not the flag, it is the measurement underneath it.** Nineteen pens absorb
**63% of all our work turns**; a pen is worth five to nine times more on the depot ring than a crop
tile is. But season totals read `work 2,814 / 2,703` and `move 3,460 / 4,025` against the tape —
**we already do more work than the tape with less walking, and 427 more idle turns, and still lose**.
Walking is not the binding constraint; the money is dominated by herd trajectory (one animal either
way is worth $15-23k of season).

## 22. Correcting the cost model makes day-matching worse, on purpose

`Node.service` is `len(ops)` fixed at plan time, and the executor re-derives ops on arrival, so a
stop planned as one WATER can offer WATER *and* HARVEST. Restricted to stops actually reached:

| | visited stops | planned | actual | overrun |
|---|---|---|---|---|
| depot cells | 30 | 77 | 114 | **63%** |
| field tiles | 260 | 410 | 454 | **27%** |

`Node.service` never contains PICKUP or DROP, so a depot stop is priced at zero-to-one turn and
routinely takes five to seven.

**Repaying that debt was swept and every arm was worse.** Seb's own days overpack any honest
per-stop estimate — his d10 spends 43 more moves than us to buy 8 more work ops — and the executor's
stay-until-`_live_ops`-is-empty behaviour is exactly what makes an overpacked plan executable.
`service = len(ops)` is wrong about the quantity it names and right about the quantity that matters.
Both correction constants ship at 0. **This is the model, not a fix deferred**, and a future session
reading the probe numbers and "fixing" the constants will re-run the dead end.

## 23. The metrics that were themselves wrong

- **`buy_seed +42` and `+33` were phantom.** `breakdown.py` counted offers; we re-offer every turn.
  Day 6 offers 48 units of melon seed (six units, eight times) and fills 6.
- **`sell` was overstated 11x** — 165 offers, 15 fills. Every number taken before 2026-08-08 used
  the wrong yardstick.
- **`weeds -174` does not mean we beat the tape; it means the opposite.** Seb finishes with **42
  weeds standing** and we finish with **8**, because we DIG ours (`dig +35`) and he leaves his
  alone. Weeded ground he was never going to replant costs him nothing; clearing it costs us 35
  unit-turns. Final board: ours `WEED=8 empty=72`, his `WEED=42 empty=37`.
- **Thirst deaths are identical.** 41 STRAWBERRY on each side (ours +2 wheat, his +1). We are not
  losing crops he keeps alive — we lose ours **eleven days early**, from d11 while he loses his
  entirely from d22, which is deliberate end-of-season abandonment.
- **`sh:wheat -139` from d8 is not a defect.** The HARVEST count is identical, the net market delta
  is identical, and the -1 lives entirely in the DROP / dusk-sweep / PICKUP mix — the opposite way
  round from the assumption. Verified by an exact accounting identity holding every day for both
  sides. No fix written, deliberately: forcing our order to match would be cloning the tape.
- **`tiles -25` at d10 is a one-day delay, not a lost quadrant.** `tiles` is a dawn snapshot at the
  window edge.
- **The tape idling 0 turns on day 1** was a harness artifact: the tape was replayed into seat 1
  with truncated hands. Real figures 144/131.

## 24. Where it stands

HEAD, seed 11, weeds off, full 30 days, against Seb's tape:

```
bank      OURS 120,424    TAPE 116,635
work      3,092 / 2,703
move      2,782 / 4,025
tiles     100 both sides    pens 19 both sides    cows 8    sheep 11
animals lost in our own season: 0
```

The uncontested number says we finish ahead. **The contested head-to-head says we lose both seatings
on the valid seed**, so this is not yet a ladder result. Open defects, with their evidence, are in
`REGISTER.md`.

## 25. Why the offline chain-search stack (stage 1) was abandoned — 2026-08-09

Folded in from `docs/fable_stage1_review_2026-08-09.md` (file deleted). Verified against the saved
artifact `data/chain_search_scheduled/best_beam_genome.npz` (money $2,484, land days 11/15) and
`data/logs/run_scheduler_v7.log`, on the installed 1.32.6 env.

**The $2,484 result is a decode veto, not a pricing bug.** `reachable_quadrants(g,12) = 0`; decode
uses 7 of 12 chains and skips the 5 that need land — the melon block, all 3 strawberry blocks, and a
4th wheat block, i.e. the entire revenue expansion. What actually plays: 2 cow pens, 2 sheep pens, 12
wheat tiles NW. Banks $2,484, wins 0/16.

**A separate, unconditional bug**: `decode` (`chains.py:687-691`) emits `buy_land` orders from
`land_schedule` unconditionally even though `reachable_quadrants` gates only the chains — so the
tape spends $3,000 on parcels on days 11/15 and then refuses every chain that would use them.

**Root cause of the veto: three cash models disagree by ~10x.** `scheduler.schedule()` charges no
crew at all (day-11 bank estimate ~$742-$1,963); `chains.cash_curve()` charges full crew from day 0
($232/day for 11 hands), giving **$108 on day 11**; `reachable_quadrants` needs ~$1,040 on day 11,
sees $108, refuses the parcel, and everything behind it dies. A comment at `chains.py:458` claiming
the gate and scheduler "agree" is false.

Order of what actually binds, most to least important: (1) the decode veto — fatal; (2) decode
buying land for chains it then refuses; (3) trickle-inflow mistiming land purchase days by up to ±5
(re-running `schedule()` with reserves 0/300/800/1500 gives parcel days 7/11, 8/11, 5/13, 7/14 —
noise around the trickle-crossing, not a decision); (4) the originally-suspected `revenue_rate` cap
is **not** binding, and is 4th and least important.

**Other findings (not fixed, not chased further):** `to_genome` silently truncates (14 chains into
12 slots, the last two strawberry blocks vanish uncounted); the per-chain drain cap is not shared
across chains (4 melon chains each independently "sell" 15 units into a single 30-unit season drain,
double-counting 60 units of headroom that doesn't exist); `OPPONENT_SHARE=0.5` vs `--share 1.0`
disagree, a 2x market-size mismatch; CARE is not modeled at all in `revenue_rate`/`cash_curve`, so a
CARE-compounding strategy (like rank-2 HealthStone's) can never be found by this search;
`expected_first_demand_day` draws shops without replacement but 1.32.6 draws with replacement.

**Verdict: not worth continuing in its current role** — "three layers of indirection," optimizing a
proxy inside a proxy against a phantom field (its tape opponents predate the 2,744-seat cluster data
and contain zero real archetypes). Never shipped; its own best output loses 16/16 to its sibling.
Its originally-recommended next step (target `kaitofukami v23` via the 15-replay cluster sample) is
now itself superseded by this file's "the ladder is two scripts" section below, and its rebase
recommendation (Dmitry Belan or Efe Can Celiksoy, `REGISTER.md` OPEN-10) —
`chains.py`/`scheduler.py` are independently known to be dead code, not part of the shipped
submission.

## 26. The wheat-buying day budget — see `docs/architecture.md`

A closed, shipped fix (`FEED_BUY_CEILING_DAYS=2`) for a purchase-side defect that had us buying
1,099 wheat/season against the field's 266-392. Full write-up, including the swept constant and the
routing/labor bottleneck it exposed at the tighter setting, lives in `docs/architecture.md`'s
"supply-management defects" section (originally merged from `fable_the_wheat_churn_2026-08-09.md`,
then folded from `fertilizer_and_wheat_supply.md` into `architecture.md` on 2026-08-13).

# Part 4 — population-scale and mechanism studies, folded in from their own files, 2026-08-13

Everything below was originally a standalone doc. Each is now one section, kept close to its
original text — headers renumbered as subsections rather than as further `##` entries, since these
are not single dated experiments but whole studies. No number was re-derived; every figure below is
copied from the source file, not recomputed.

## 27. What the opponents actually do

Folded in from `the_field.md`. Measured from leaderboard replay JSON, not inferred from notebooks or
forum posts.

> **Version and currency caveat.** The replays analysed below predate the 2026-08-07/08 move to
> `kaggle-environments` 1.32.6, so absolute dollar figures (bank totals, revenue splits) are not
> directly comparable to a 1.32.6 game. The structural finding — winners submit fixed 720-turn
> open-loop scripts — is a claim about *behaviour*, not price level, and is independently
> reconfirmed on 1.32.6, at population scale, by §28 below.
>
> §28 also reconfirms the open-loop finding at population scale: most of the field is scripted, two
> shared scripts dominate, and the one clearly reactive top player (#1, at the time §28 was measured)
> beats the fixed scripts by ~110 rating points through an adaptive herd, not a different opening.

### The winners submit fixed 720-turn scripts

Six replays, five distinct players. For each player appearing in more than one replay, every turn's
action was split into `units` (`farmer` + `hands`) and `market` (trading orders) and compared
turn-by-turn between episodes:

```
senkin13        4 episodes, 6 pairwise comparisons, different opponents AND swapped seats
                units  identical 720/720  (100.0%)  in all six
                market identical 720/720  (100.0%)  in all six
                banks $121,538 - $145,034

syouya tobita   units  identical 720/720       (100.0%)  in all six
                market identical 716-720/720   ( 99.4-100.0%)

Dmitry Larko    units  701/720 (97.4%)   market 689/720 (95.7%)
```

Independently confirmed on the later leader `somewhere after` (four replays, 2026-08-05): every
derived quantity — land days, herd, seed counts, fertilizer flows, crew ramp — is **byte-identical
across all four**, in both seats, against four different opponents. The only variation anywhere is
107 vs 106 `FERTILIZE` ops.

**Reactivity is worth approximately nothing at the top of this leaderboard.** Two design questions
close on it: no opponent model, no market policy.

**But the artifact is a genuine 720-step program, not a repeated routine.** Every player shows
**30/30 distinct daily unit-routines**. There is seasonal phase structure; "one routine, repeated"
cannot express what they play.

**Open-loop does not mean unoptimised.** Reactivity is conditioning on state at play time, which
they have none of. Optimisation is searching for a good sequence before play time, which they
clearly did a great deal of.

#### Caveats that must travel with the claim

- **`senkin13` and `syouya tobita` are not confirmed top-ranked** — a strong mid-field agent at
  ~$145k — and they are a **mirror match**: 536/720 identical action dicts between the two of them.
  `CLAUDE.md`: a mirror match is not a best response.
- The only confirmed top-tier games are the `Dmitry Larko` pair, which is the *weakest* open-loop
  evidence in the table. Our own docs disagreed on that figure (97.4% here, 93.5% elsewhere for the
  same pair).
- **Zero `WEED` tiles across all 720 turns of all six replays**, despite `weedSpawnChance: 0.005`.
  "The winners ignore weeds" is untested, not proven harmless. Validate any open-loop script across
  many fresh seeds before submitting.
- The claim that survives independently of rank: **"manual player" ranked #3 at 2,911.8.** A human
  cannot compute reactive per-turn decisions across 720 turns under a one-second clock.

### The mixed economy, torn down

`senkin13`, episode 89541819, final reward **$145,034**, gross sales **$220,542**:

| product | revenue | share | units |
|---|---:|---:|---:|
| MILK | $58,505 | 26.5% | 235 |
| STRAWBERRY | $42,942 | 19.5% | 309 |
| WOOL | $40,112 | 18.2% | 190 |
| WHEAT | $38,632 | 17.5% | 855 |
| MELON | $24,489 | 11.1% | 123 |
| FERTILIZER | $14,698 | 6.7% | 271 |
| EGG | $769 | 0.3% | 12 |
| CARROT | $395 | 0.2% | 10 |

**Animal products 45.1% · crops 48.3% · fertiliser 6.7%.** Three crops carrying real weight, two
animal species, a fertiliser side-business. Not the "83% from milk and wool" single-episode figure
that circulated for a while, which was one agent in one episode. (This game's own CARROT/EGG revenue
is a real opponent's real sale, not ours — not subject to the SELLABLE caveat, which is about our
own agent's inability to emit those SELL orders, not about whether the product can be sold at all.)

Four things this contradicted:

1. **Melon is not the meta crop.** Strawberry out-earns it nearly 2:1 on 309 units against 123.
   Seeds bought: `STRAWBERRY 44, WHEAT 34, MELON 21`.
2. **Wheat is an input.** They buy 1,055 units for $47,594 and sell 855 for $38,632. Net cash on
   wheat is negative; the return arrives as milk and wool.
3. **Fertiliser is a revenue stream**, not an expense — 271 units for $14,698, from
   `COLLECT_FERTILIZER`, which costs one action and is available only if you own animals.
4. **Cows and sheep, no geese.** `COW 8, SHEEP 6, GOOSE 0`, `BUILD_PASTURE 14, BUILD_COOP 0`, plus
   **304 hires** and 2 land purchases. Goose is the cheapest animal and the one our agents reach
   for first; the measured meta skips it entirely.

### The leader `somewhere after`, four replays 2026-08-05

| episode | seat | opponent | his | theirs | margin |
|---|---|---|---|---|---|
| 90016067 | 1 | haoran huang430 | 160,593 | 157,959 | +1.7% |
| 90018004 | 1 | manual player | 134,780 | 130,777 | +3.1% |
| 90020633 | 1 | Savko | 137,667 | 133,335 | +3.2% |
| 90023239 | 0 | Savko | 123,443 | 118,437 | +4.2% |

4/4, mean bank **$139,121**, mean margin **+3.1%**.

**The margin is the point.** Everyone at the top banks $120k-160k and the leader edges it by a few
thousand. On an Elo ladder a $2,634 win scores what a $50,000 win scores, so the top of this board
is a knife-edge contest between several near-equal fixed scripts — and because they are fixed, they
cannot punish anything. They are a stationary target to compute a best response against.

His farm: land on **days 7 and 10**, two parcels, never SE. **8 COW + 6 SHEEP = 14 pens.**
WHEAT 66 (50%), STRAWBERRY 44 (34%), MELON 21 (16%). 318 fertilizer collected, **107 applied**,
0 bought, 445 offered. Crew 4 on day 0 ramping 4-6-5-5-6-6-6-8-10-11-12, flat 12 from day 10.
`DIG` 103 times.

Op census, four replays aggregated:

```
NORTH 4,943 16.8%   WEST 4,392 15.0%   SOUTH 3,716 12.7%   EAST 3,428 11.7%
WATER 3,404 11.6%   PASS 1,427 4.9%    PICKUP 1,356 4.6%   HARVEST 1,352 4.6%
FEED 1,276 4.3%     COLLECT_FERTILIZER 1,272 4.3%          CARE 1,232 4.2%
PLANT 524 1.8%      FERTILIZE 427 1.5%  DROP 320 1.1%      PLACE 108 0.4%
DIG 103 0.4%        BUILD_PASTURE 56 0.2%
```

**56% of his ops are movement and `PASS` is only 4.9%.** His units are spread across the board
rather than working compact adjacent blocks — he spends the turns to reach better tiles. Our own
serpentine blocks minimise walking by construction, which looks efficient and may be the wrong
objective.

`PLANT` 524 across four replays is 131 per replay, matching 66 + 44 + 21 = 131 seeds exactly.

### How he funds it

From `data/seed_scripts/new_leader/90016067.json`:

```
day  0  $3,000   BUY_ANIMALx4 BUY_PRODUCTx16 BUY_SEEDx4 HIREx4 SELLx12
day  1  $   42   <-- forty-two dollars
day  2  $  141
day  3  $  217
day  5  $  621
day  7  $1,719   BUY_LANDx1
day 10  $1,278   BUY_LANDx1     <-- a $2,000 parcel on a $1,278 dawn bank
day 11  $3,236
day 12  $6,828
day 13  $14,622
```

- **He goes all-in on day 0 and ends it on $42.** Four animals, ~51 wheat bought in small lots
  across all 24 hours, 18 seeds, 4 hires. His day-0 SELL orders are speculative over-requests
  against an empty shed and mostly no-op — exactly like ours.
- **His early revenue is FERTILIZER.** Day 1 hour 8: `SELL FERTILIZER x4`. Four day-0 animals
  produce it nightly, collecting costs no action, and he sells it daily from day 1 — long before
  milk arrives on day 8. Our census: 83 collections against his 318.
- **He funds purchases from same-day sales.** The $2,000 parcel on a $1,278 dawn bank works because
  his sells land earlier in the same day. He runs at the edge of insolvency the whole ramp.
  **We hoard, he compounds.**
- Wheat is **not** arbitrage: he buys 967 at mean $44.96 and sells 1,131 at $46.49, a 3.4% spread,
  with 319 units going to FEED. He buys feed instead of growing it.

### The public meta (2026-08-03 notebooks, `reference/community_notebooks/`)

Live market prices in that meta: `STRAWBERRY 280 · MILK 263 · WOOL 235 · MELON 54 · WHEAT 58`
against bases of 120/160/200. Strawberry, milk and wool trade **well above base** because the town
drains faster than two farms can supply; **melon collapsed to 22% of base** because everyone dumps
it on day 10.

Three clusters: pure cow ranch (3-10 cows), melon IPO (16 melons + 2 cows, day-10 dump), and the
staged economic herd (`C0x` family), which is the strongest public code. The common plan (c16) is
**8 cows, 5 sheep, 5 strawberry plots, 12 hands**.

Hands are nearly free at the bottom of the Fibonacci ladder and expensive fast at the top:

| hands | 6 | 8 | 10 | **12** | 14 | 16 |
|---|---|---|---|---|---|---|
| coins/day | 20 | 54 | 143 | **376** | 986 | 2583 |

Twelve hands is 376 coins for 288 extra actions — about **1.3 coins each**, against one in-window
melon watering worth $250.

Value per action, measured:

| action | value |
|---|---:|
| melon, in-window watering | ~$250 (while price holds) |
| cow, fed + cared | ~$95 |
| sheep, fed + cared | ~$86 |
| **`COLLECT_FERTILIZER`** — free, every animal, every day | **~$85** |
| goose, fed + cared | ~$32 |
| strawberry | ~$37 |
| wheat | ~$17 |

### Our own reference tape: Seb

`data/seed_scripts/top_guys/90494364.json` is the tape `scripts/breakdown.py --tape seb` diffs
against, day by day, on seed 11 with weeds off. It is a **diagnostic, not the goal** — beating it
is the goal, so "the tape doesn't do this" is never an argument against a change.

Its own metadata is not trustworthy: `build_tiles` day 0 says `[[4,4] COW]` while a SHEEP stands
there all season. The ordered `places` list is the good metadata; `build_tiles` labels are not.

### What the field says about our own numbers

- Ladder targets go stale in days. A field that reached 2,700 in four days keeps climbing.
- **Imitation learning off the daily top-episodes datasets was checked and rejected**: those are
  ordered by *current* rating, so on 2026-07-31 they contained agents near the $3,512 baseline while
  we banked $43k. Their value is an opponent pool and scouting. Re-check only once leaderboard
  scores exceed our own.
- **Self-play pressure is bounded by the pool it plays.** A pool of frozen copies of an $18k policy
  plus scripts topping out at $27k demands nothing, and nothing in it plays cows, sheep, strawberry,
  fertiliser collection or a twelve-hand crew — so those strategies are not merely undiscovered,
  they are never *demonstrated*.

## 28. The top of the ladder is two shared scripts, and we are not playing either

Folded in from `the_ladder_is_two_scripts.md`. Measured 2026-08-11 from the official episode
datasets, `kaggle/kaggriculture-episodes-2026-08-09` and `-08-10`: 1,372 episodes, 2,744 seats, 40 GB
of replays. Extracted by `scripts/episode_index.py` (parallel, one JSONL row per seat) into
`data/episodes_2026-08-09.jsonl` and `data/episodes_2026-08-10.jsonl`.

> **Addendum 2026-08-13: the ladder is one fixed board, and the current #1 is not open-loop.**
> 16 downloaded games of the ladder's then-current #1 (カワシギ, 15-1, bank range $44.9k-$150.0k)
> plus 4 of our own games are hash-identical on world/market/tiles observation across all 20 games
> and both seats — terrain, land parcels, town positions and opening prices are constants of the
> ladder itself, not a per-seed draw. **The "seed variance ~15%" figure describes `kagg.arena`'s
> randomly drawn boards and does not apply to the ladder.** カワシギ is also, contrary to the general
> open-loop finding in §27, reactive from day 3: all 16 of its games are byte-identical for exactly
> the first 74 turns (through the moment before the first shop-unlock draw,
> `townShopUnlockInterval=3`), then pairwise action-vector identity drops to 26%-82% and divergence
> tracks the shop draw, not the opponent. Hour 1 stays identical across all 16 games through d23;
> hour 0 is the most divergent hour from d14 on. **Correction, 2026-08-13 (`1f7d457`):**
> `SHOP_ADAPT_HERD` used to start on day 6; it now floats from day 0 (`SHOP_ADAPT_FROM_DAY = 0`), so
> the gap to カワシギ's day-3 responsiveness is now about *which* draw the code reacts to, not
> whether it reacts before day 6. Diffing its fixed 74-turn opening op-for-op against ours is cheap
> and unexplored. Full detail: `docs/REGISTER.md` OPEN-14.
>
> Two smaller, older field-description studies were folded in here, both explicitly superseded in
> scale by the 2,744-seat sample below but each carrying one detail not otherwise recorded — see
> "Prior, smaller-scale field evidence" below.

### Where we actually stand

| | rating |
|---|---|
| THUNDER THUNDER (#1) | 3,210.9 |
| Victor @ Tufa Labs (#2) | 3,149.8 |
| median episode in the dataset | ~3,079 |
| **our best submission ever** | **1,257.9** |
| our submission of 2026-08-11 | 845.1 |

**None of our games appear in the two-day sample at all** — 0 of 2,744 seats.
This is not a tuning gap. The field is at ~3,000 and we are at ~1,000, and the ladder starts at 600.

### The field is running two scripts

Median values per player, players with 5+ games in the sample:

| player | n | bank | WHEAT | STRAW | MELON | COW | SHEEP | GOOSE | buy wheat | sell wheat |
|---|---|---|---|---|---|---|---|---|---|---|
| Haramball forever! | 5 | 97,828 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| Natalia Mawyin | 16 | 94,116 | 147 | 38 | 17 | 9 | 6 | 0 | 257 | 446 |
| Mohammed Nomaan | 23 | 94,006 | 147 | 38 | 17 | 9 | 6 | 0 | 257 | 446 |
| Dmitry Belan | 35 | 93,921 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| Ueddy | 25 | 90,219 | 143 | 37 | 19 | 9 | 4 | 0 | 212 | 455 |
| THUNDER THUNDER | 111 | 90,112 | 144 | 36 | 19 | 9 | 5 | 0 | 245 | 430 |
| Efe Can Celiksoy | 53 | 87,378 | 146 | 37 | 19 | 10 | 4 | 0 | 234 | 459 |
| Changyuan Chen | 11 | 93,674 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| Mohamed abdelrazik | 32 | 91,682 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 397 |
| CemBas | 13 | 89,846 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| SHAURYA SHARMA | 32 | 89,262 | 108 | 42 | 24 | 8 | 6 | 0 | 267 | 302 |
| janson | 24 | 88,990 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |
| tao wu11 | 10 | 88,462 | 108 | 42 | 24 | 8 | 6 | 0 | 266 | 305 |

Nine separate accounts report **WHEAT 108 / STRAW 42 / MELON 24 / COW 8 / SHEEP 6 / buy 266 / sell 305**
to the unit.
Seven more report **WHEAT ~144 / STRAW ~37 / MELON ~19 / COW 9 / SHEEP 4-6**.
That is not convergent evolution, it is two shared scripts.

### Timing

**Script A** (wheat ~144): 1 COW + 4 SHEEP on d0, the bulk of the cows on **d5-d8**, then a trickle
to d19. First PLANT at d0 turn 6. First SELL on d2, median sell day 21.

**Script B** (wheat 108): ~2 COW + 2 SHEEP on d0, cows on **d7-d10**, sheep on **d10-d11**.
First PLANT at d0 turn 8. First SELL on d0, median sell day 21.

### What separates us from all of them

- **Wheat.** They plant it 108-147 times a season; our schedule plants **24**. Wheat's book is
  starved in all 87 recorded tapes and closes at $40-59 against a $25 base, so it is the one product
  the market never saturates. They grow their own feed and sell the surplus; we buy 505 units.
- **Herd size and mix.** They run 13-16 head, cow-heavy (COW 8-10, SHEEP 4-6). Our schedule ran 21
  before `1f7d457`, and on the analysed loss `SHOP_ADAPT_HERD` bought **16 sheep and 5 cows**. Herd
  count is now a floor sized by drain and capped by feed capacity (`architecture.md`, "herd sizing")
  rather than fixed at the schedule's number — not yet re-measured against this comparison.
- **Geese.** Nobody in the top 16 owns a single goose.
- **Re-posting.** Measured by whether a SELL repeats the same `(item, qty)` on the next turn:
  the field is at **3-7%**. Ours re-posts its quota on all 24 turns of a day. We are the only agent
  in the sample that does this.

### Open-loop

Per-day action hashes, compared between games by the same player. One differing turn kills a whole
day, so this is a strict lower bound on similarity.

    Haramball forever!   24/30 days identical      Efe Can Celiksoy   18/30
    janson               21/30                     Mohamed abdelrazik 17/30
    Dmitry Belan         21/30                     SHAURYA SHARMA     11/30
    CemBas               21/30                     THUNDER THUNDER     7/30
    Mohammed Nomaan      19/30                     Ueddy               5/30

Most of the field is scripted. **THUNDER THUNDER, the #1, is the most reactive of the lot** — and on
a separate turn-by-turn diff, two of its same-seat games were only 1.2% identical, diverging at
d0h3. Victor @ Tufa Labs is the opposite extreme: 97-99% of turns identical across seven games on
both seats, with byte-identical season SELL totals.

So the top two are a reactive agent and a fixed script, at 3,210 and 3,149. Both work.

### Does the field adapt to the board? Mostly no — and the one that does, leads

Range across each player's own games. Every game is a distinct shop draw.

| player | n | COW | SHEEP | WHEAT | distinct draws |
|---|---|---|---|---|---|
| Dmitry Belan | 35 | 9..9 | 4..4 | 142..143 | 35/35 |
| Mohamed abdelrazik | 32 | 8..8 | 6..6 | 108..108 | 32/32 |
| janson | 24 | 8..8 | 6..6 | 108..108 | 24/24 |
| **THUNDER THUNDER** | 111 | **6..11** | **4..12** | **132..152** | 108/111 |
| Ueddy | 25 | 6..10 | 4..11 | 142..150 | 25/25 |
| Raiden.B | 27 | 1..15 | 5..19 | 55..120 | 27/27 |

Mohamed abdelrazik played 32 games on 32 different boards and bought exactly 8 cows and 6 sheep and
planted exactly 108 wheat in every one.
The fixed scripts sit at ~3,100; THUNDER, which floats cow/sheep, is #1 at 3,210.

**So adaptive herd is real and worth roughly 110 rating points. The gap from us to a fixed script is
2,255.** Do the base plan first.

### Why our schedule is the wrong target: Seb was optimal under the OLD economy

`townCenterSellInterval` went 12 -> 24 on 2026-08-08, cutting the town's drain ~8x.
Seb's 16 recorded games, split by the economy they were played under:

| | games | median bank | COW | SHEEP | WHEAT | STRAW | MELON |
|---|---|---|---|---|---|---|---|
| interval 12 (old) | 5 | **$137,747** | 5..9 | 10..15 | 19..28 | 41..45 | 18..24 |
| interval 24 (now) | 11 | **$77,737** | 5..13 | 5..20 | 20..36 | 38..43 | 14..25 |

His bank halved while he kept the same low-wheat shape, and he has since withdrawn from the ladder.
The field's answer to the new economy is the thing he does not do: plant 108-147 wheat.

**`data/seed_scripts/top_guys/90976060/schedule.json` — the plan this repo matches op-for-op — is
his interval-12 shape, asking for WHEAT 24 / STRAWBERRY 41 / MELON 17.**
That is the 845-vs-3,100 gap. It is not the planner, the watering or the market logic; it is the
target. Note also that Seb floats COW 5..13 and SHEEP 5..20 — he adapts more than the current field.

### Best tape to rebase on

**Dmitry Belan** (35 games, `COW 9..9 SHEEP 4..4 WHEAT 142..143 STRAW 36..37`) — near-zero variance
makes it a pure script, so the plan reads noise-free.
**Efe Can Celiksoy** (53 games, WHEAT 143..146) is an equally clean second source for cross-checking.
Not THUNDER: it is reactive (7/30 days identical; 1.2% on one same-seat pair), so there is no fixed
plan to extract — it is a sparring opponent and the evidence that adaptive cow/sheep pays.

### What was tried on the crop dynamic, and why all of it is off

`SHOP_ADAPT_CROPS` in `kagg/search/schedule_agent_1455mh.py` carries the full record. Summary:

- **`WHEAT<->CARROT` and `TOMATO<->STRAWBERRY`** — shipped, measured 0.806 vs HEAD's 0.871 over 232
  matched games. They swap toward crops the ladder plants 0.2% and 0.0% of the time.
- **`STRAWBERRY<->MELON`** — produces an identical 54/4 split on every board tested. No shop carries
  melon, so its drain is 29 everywhere; a pair with one board-independent member cannot adapt.
- The shared cause: **the headroom model treats the town's drain as a cliff when the price curve is
  a slope.** A melon past its drain still fetches $229 at +50 and $166 at +100. Any rule scoring on
  "units the town will eat" under-plants every steep-curve, low-drain product. The fix is to price
  the marginal unit off `market_price`, and it is unbuilt.
- **Correction, 2026-08-13: the `WHEAT<->CARROT` 0.806 figure above was measured before the
  SELLABLE fix (`c99a8a5`) — our own agent could not sell CARROT at all at measurement time, so the
  swap's carrot side banked $0 by construction.** Treat as UNVERIFIED, not re-affirmed. See
  `docs/REGISTER.md` C-23 and §29 below for the carrot pool-verdict-void flag more generally.

### Prior, smaller-scale field evidence (superseded in scale, not fully redundant)

**A public Kaggle notebook** (shared 2026-08-09, 3 replays per top-5 team, opening-cluster analysis)
found three day-0 signatures: `v23_fork` (3 teams, 3,117-3,131, a byte-identical clone of the public
`kaitofukami v23` reference), `sheep_first_hybrid` (HealthStone, 3,132.9, front-loads to $14 cash
held days 1-4 on sheep CARE compounding), and `counter_meta` (Seb, 3,201.1, keeps a $500+ cushion
days 1-5, funds 4 land quadrants and 20 animals by season end). Seb banked the least money of the
three sampled builds (~$57k vs ~$100k for the other two) yet ranked 1 — an early external
confirmation that money is not the selection criterion.

**20 real leader episodes** from `data/ladder/leaders_0808` (2026-08-08, the day of the
`townCenterSellInterval` switch — treat dollar figures as possibly-old-economy) plus our two losses
showed **18 of 20 episodes are one public reference script (`kaitofukami`-shaped) mirroring itself**,
identical signature WHEAT~103-109/STRAW42/MELON24/COW8/SHEEP6, identical hire ramp — reconfirming
that most of the visible "field" is one script. Only Seb (2 rows) diverged, running sheep-heavy
(SHEEP15/COW7 and SHEEP10/COW9). Two op-census findings not carried elsewhere: our PASS share is
21.6% against the leader average 15.0%, and our WATER share is 7.7% against 13.2% — idle capacity,
not a crop-mix problem. Neither of our two actual losses (Shivam_2212, an exact mirror-baseline
signature, 34% margin; As Wasti, a CARROT/TOMATO five-crop build appearing in zero of the 40 leader
rows, 9% margin) resembled Seb, so beating Seb's tape never implied beating the field.

### Loss forensics: given a loss, why, and how big

**MELON is a fixed pot won by whoever sells first, not a per-tile yield.** 10 downloaded ladder
losses (2026-08-11, `kaggle_environments 1.32.6`, `weedSpawnChance=0.005`) found MELON is drained by
zero of the 8 town shops (closes $4-$25 against a $250 base in 10/10 games). On episode `92077611`
(lost by $1,386) our second melon wave (9 tiles, d10-d20, 66 units for $4,758, ~$72/unit) denied the
opponent's later wave but they still out-volumed us 138 units to 96 and the game was lost anyway —
the fix is ripening earlier (plant d8, not d10), not planting less. We plant MELON 69 on every one of
6 sampled seeds regardless of town composition, because `router.py`'s crop list is copied off one
leader's schedule rather than being town-responsive. **We never plant CARROT or TOMATO despite both
closing above base in 10/10 games** (CARROT $40-42/base $35, TOMATO $77-118/base $60) — this
recommendation predates the 2026-08-13 SELLABLE fix (`c99a8a5`) which had been blocking
CARROT/TOMATO/EGG sales entirely; the price observation is sound, the recommendation was not
actionable when written and should be re-evaluated now that SELLABLE is fixed. On `92077611` we
spent $4,424 more than the opponent despite outselling them by $3,038 in revenue, in a game lost by
only $1,386 — an unmeasured lead (closing-week buy counts run 15-67/day for the opponent against our
fixed 4).

**Given a loss, how big is it — and don't compute a win rate from a losses-only sample.** 60
downloaded games of our own ladder agent (`data/seed_scripts/ours_ladder/`, 2026-08-13) were
downloaded *because* they were losses; an earlier pass computed a win rate from them ("0.085",
"5-54") and that figure was removed as worthless selection bias, per the project's `farm:0.445`
lesson (`CLAUDE.md`). What's unbiased **within** the loss-only sample: 54 losses have median -$8,900,
mean -$11,600, with 6 inside $600, 11 inside $2,100, 23 inside $6,000, 31 inside $10,000 — two losses
were inside $150 (-$70 and -$135). Ruled out as causes: stranded unsold stock (shed empty at season
end) and a single bad matchup (54 distinct opponents, no repeats). Separately, one self-play
validation episode (`91304798`, seed 0) timed out at step 531/720 — flagged as an unquantified
failure mode with no current per-turn latency measurement.

## 29. The market — findings about us: cadence, fills, the late season, and carrot

Folded in from `the_market.md`. The environment-mechanics half of that file (the derived-rule depth
table and the per-product/per-head saturation table) moved to `competition_brief.md`'s Economics
section instead, since those are facts about the environment, not about us; this section keeps
everything that required watching our own play to measure.

> **SELLABLE correction.** `SELLABLE` excluded CARROT, TOMATO and EGG until commit `c99a8a5`. Every
> dollar figure below involving those three products, or geese/eggs, was measured with that revenue
> line disconnected and is flagged VOID inline, subsection by subsection.

### The sell rule, shipped

Both `PRICE_AWARE_SELL_CAP` and `RESERVATION_SELL_CAP` ship ON (formula in `competition_brief.md`
§6). The handover fixture went from $71,976 / 331 units destroyed / 12 turns at cap to $75,866 / 82
destroyed / 2 (+$3,890, −75% waste). A second fixture went from $62,868 / 86-165 destroyed / land
days [4,6,15/16] to $64,667 / 39-107 destroyed / land [4,6,16] (+2.9% bank).

### What the town actually eats — 87 real tapes, not simulation

Measured 2026-08-11 off 87 recorded ladder games (`data/seed_scripts/top_guys`), reading each game's
closing `market.inventory` against its own `town.unlocked_shops` directly — no simulation.

```
product      shops   appetite range   closing surplus range
WHEAT          5      745-1,282        -386 to -1,356    (negative on ALL 87)
CARROT         2       29-924           -12 to -1,002
TOMATO         2      208-924           -30 to -678
STRAWBERRY     4      387-1,282        -381 to +60
MILK           3      566-1,103        -342 to +77
EGG            2      208-566          -624 to +108
WOOL           1       29-387          -424 to +59
MELON          0       29 (fixed)       +38 to +158      (positive on ALL 87)
FERTILIZER     0        0 (fixed)      +201 to +493      (positive on ALL 87)
```

**WHEAT closes negative on every single one of 87 tapes** — the town eats more than both farms
together produce, and price *rises* to $40-$59 against a $25 base. This directly rebuts a shipped
comment in `schedule_agent_1455mh.py` calling wheat "a bad trade" on a 6-unit yield assumption; the
measured `production.py` yield is 28 (42 fertilized).

**MELON and FERTILIZER close positive on every one of 87 tapes without exception.** Melon's only
consumer is the town centre (29 units/season, fixed by rule); 17 tiles at ~12 units/tile is 204
units into a 29-unit appetite — every player over-plants melon, winners included, so it is a shared
inefficiency, not a losing move relative to the field. Fertilizer demand is zero on every board by
rule (`kaggriculture.py:101` excludes it from the town-centre list, no shop carries it), not by seed
draw. Marginal price: 50u→$90 (cum $4,755), 100u→$80 ($9,010), 150u→$70 ($12,765), 200u→$60
($16,020), 250u→$50 ($18,775), 400u→$20 ($24,040), 500u→$1 ($25,052) — every one of the 87 tapes
closes fertilizer at $1-$20 against its $100 base, i.e. the book is saturated by season's end in
every game ever recorded here.

CARROT/TOMATO/STRAWBERRY/MILK/EGG/WOOL show mixed positive/negative surplus across the 87-tape
range, reflecting shop-draw variance. This measurement reads **other players'** closing inventory
from real games, not our own agent's sell behaviour — it is not filtered by our own SELLABLE list
and is not subject to the SELLABLE correction.

Appetite is a ceiling, not a prediction: this table models neither turns, walking, watering nor
reachability.

### Fills vs offers: what really moved the price

A fill-level (not offer-level) comparison of Seb's tape, our loss, and the opponent who beat us in
that same loss found Seb's realized price 51-65% above both — but the small/late-order theory does
**not** explain it: the winning opponent's own single-product orders were *larger* than Seb's (mean
7.8 vs 4.0 units, max 31 vs 16) while realizing a *lower* average price ($85.84/unit vs Seb's
$141.35). Our own losing game sold 85% of its single-product covered volume in wheat and fertilizer
(both under $75/unit) while the winning opponent sold 70% of its volume in strawberry at $161/unit
without collapsing the price. **The gap reads as product mix, not order shape.**

Full per-source numbers: coverage of SELL-emitting turns 81% Seb / 41% us / 76% opponent (money-
conservation method; shed-delta only caught 18/244 clean turns for Seb, a >90% undercount). Revenue:
Seb 113 events / 1,064 qty / $150,395 / $141.35 mean / order size 4.0 mean, 16 max. Us: 130 events /
1,053 qty / $98,072 / $93.14 mean / 2.0 mean, 6 max. Opponent (won): 79 events / 1,209 qty / $103,777
/ $85.84 mean / 7.8 mean, 31 max. By hour bucket ($/unit, h0-7/h8-15/h16-23): Seb $149.17/$130.35/
$138.68 (flat-to-down late); us $108.66/$60.62/$86.89 (mid-day worst); opponent $76.65/$150.42/
$95.68 (no pattern).

**`LATE_SELL_BIAS`** (block all sells before hour 16, last-day liquidation exempted) was confirmed:
8-seed × 3-opponent × both-seatings arena A/B (48 games/state) took pool win rate 14.6%→27.1%
(+12.5pp), mean money $16,146→$24,535 (+$8,389). Per-opponent: heuristic 8,672/12.5%→23,196/25.0%;
rancher 21,450/6.2%→28,612/31.2%; contrarian 18,317/25.0%→21,798/25.0% — positive or flat on every
individual opponent. **This measurement was later found to have been taken on `run_arena`'s
state-leak path** (`architecture.md`, "what the shipped agent actually scores") and superseded by a
re-run on the fixed harness — $102,886/100%, 17.8x on money, 6.2%→100% on win rate.

**`CAP_SELL_OFFER_SIZE`** (cap any single offer at 30 units) was verified to work correctly when
triggered (seed 2 vs contrarian: 43-unit offer capped to exactly 30, $10,268→$10,265) but came back
byte-identical on the 8 held-out A/B seeds because none of them produced an over-30 offer — a genuine
null from an under-powered test, not evidence the cap is useless. A wider 24-seed×opponent sweep
found exactly two over-30 offers, both `SELL WHEAT 43` on d29 h0 against contrarian only.

Two false leads retracted the same day they were raised: a "delivery problem" (443 units apparently
stranded in hands at dusk on seed 13) dissolved once fills were counted properly — 100-109% of
everything produced gets sold, 0 units left in shed or hands at season end across four seeds; the
apparent gap was comparing agents with different herd sizes plus sampling only at the single worst
instant (dusk). And a claimed "board property" for shop-draw absorption was wrong because
`_spawn_weeds` consumes the same per-day RNG stream *before* the shop draw, so which shops unlock is
agent-play-dependent, not seed-pure — seed 29 looked wool-starved under a PASS-only game and draws
YARN_STORE under real play.

**Same agent, same code, same schedule, same opponent tape banked $16,888-$163,036 across 36
seed×opponent seasons** (6 tapes × 6 seeds) with milk realizing $27.90-$252.66/unit purely from board
variance. MILK is board-driven (spread 88.5 holding opponent fixed) because it sits in 3 of 8 shops
(P(never drawn in 8) = 2.3%); WOOL is opponent-driven (spread 73.1 holding seed fixed) because it
sits in exactly 1 of 8 (YARN_STORE, P(never drawn) = 34.4%) — whoever else dumps wool sets its
price. `town["unlocked_shops"]` is fully observable every turn (`shared: True`) even though the
underlying seed is hidden, yet the production side of the agent — animal and crop targets — is fixed
before the board is known and never consults the draw: a board with no YARN_STORE still buys full-
price sheep. **Correction, 2026-08-13:** this specific gap — the herd not consulting the draw — is
what `1f7d457` (`architecture.md`, "herd sizing") set out to fix.

Shop-draw probability (never drawn in 8): WHEAT 5/8 shops, 0.2%; STRAWBERRY 4/8, 2.3%; MILK 3/8,
2.3%; WOOL 1/8, **34.4%**; MELON 0/8, always.

Separately: animal loss from two consecutive unfed days is irreversible and invisible in final-bank
terms — shipped agent loses 1 animal on seed 13, one variant loses 4, another 8-11. A distinct
defect from price collapse, not to be traded against it.

Across 14 real ladder losses, re-pricing only our own sales downward turns 12/14 into wins.
Recoverable money by product at the optimal multiplier: WOOL +$135,250 (0.7x), STRAWBERRY +$57,433
(0.7x), MILK +$57,163 (0.5x), MELON +$4,447, WHEAT $0 (1.0x — no gain), FERTILIZER $0 (1.0x). Wool
is specifically a volume problem, not a cadence one (episode 91122388: $5,278 observed vs $23,794 at
0.7x). Cutting dominates over spreading: downscaled-only +$254,293 (best 16/56), spread-only
+$87,343 (best 16/56), both together +$252,611 (best 17/56) — spreading adds little once cutting is
already applied.

### Intra-day cadence: when we sell, not just how much

Comparing exact committed fills against Seb's own schedule orders hour-by-hour across d0-d7 (seed
11, tape `91422988`) found quantities roughly match but hours are systematically wrong in the same
direction on every product:

1. **Unfilled sell quotas carry forward and dump at hour 0.** 14 wheat units dumped at dawn across
   d5-d7 recovering an unfilled d4 row. Hour 0 is triply the worst hour: no harvest yet, town hasn't
   drained yet, and it's the same hour `BUY_PRODUCT` fires, paying the spread twice.
2. **Our sells fire in the morning, Seb's fire in the evening.** With the town draining once a day,
   selling before the drain sells at the bottom of the curve every time. FERTILIZER shown day-by-day:
   ours d2 h07/08/12/13 vs his h15/19; d3 ours h07/12/13/14 vs his h15/18; d5 ours h04/13/14/18 vs
   his h17/19/20; d7 ours h05/19 vs his h17/22/23.
3. **Our buys front-load into a block; Seb's drip.** d0 identical quantity, opposite distribution:
   ours h01-h08 (8 consecutive turns) vs his h05/07/09/11/12/14/17/19 (spread across 15). Shops
   restock every 4 steps, so his spacing buys into a restocked book while ours buys the second half
   into a book its own first half already lifted.

Priced concretely: on d6 Seb funds a land parcel by hour 13 from two wool sells at h09/h13 (bank $5
→ $1,349); our equivalent wool sale timing leaves us $47 short until h23, missing the same-day land
purchase by ten hours. Also d4: our single 25-unit wheat lump at h16 clears at a materially worse
mean than Seb's four smaller blocks (h18/21/22/23, 5/12/12/20) with restocks between.

**Caveat carried forward: the tape this was measured against (Seb, `91422988`) is now known to be
tuned for the pre-1.32.6 economy** (his median bank has since halved and he has withdrawn from the
ladder) — the target is superseded, but the hour-shape mechanism (sell-after-drain, drip not
block-buy) is argued to still generalize and is untested against a current target. Whether moving
sells later is worth it in money was explicitly left unmeasured.

#### The d16-d19 reconciliation: why daily deltas often look worse than they are

A fill-by-fill reconciliation (seed 11, tape victor) found most apparent day-level deficits are
phase-shift artefacts. `harvest 11/14` on d18 is not three missed harvests — they were taken a day
early on d17 (cumulative d16-d18 harvest reconciles exactly, 46/46). `sell 35/61` on d18 is the exact
mirror of a `90/39` surplus on d17 (cumulative sells at end of d18: ours 499 vs tape 489, and we're
$3,045 ahead in money at that point) — caused by our own `LATE_SELL_FROM_HOUR=16` policy: the tape
posts its sell row at dawn against yesterday's still-unsold shed, while we sell late the same day and
sweep our own same-day production as it lands, so our dawn-d18 shed genuinely only holds what we
then offer, and every unit offered that day fills.

**One deficit does NOT reconcile: FERTILIZER 0/8 on d18, still −8 by end of d19.** The shed held
9-13 fertilizer all day but `FERTILIZER_RESERVE_LOOKAHEAD_DAYS=1` computed a 12-tile reservation need
against a 9-unit shed and withheld the entire offer. The reserve exists because an earlier incident
(d16) fired only 6 of 12 scheduled FERTILIZE ops when the shed ran dry — relaxing it is not
established as safe on this evidence alone. See `architecture.md`'s fertilizer section for the
follow-on investigation.

### The late season specifically

Three candidate explanations for the late-season gap were tested and killed in one session (seed 11,
tape victor):

- **More crew hands is not the answer.** +4 hands on d26-d29 cost −$3,350; the extra hands idled
  (hire d26 10→14, pass 36→124, water unchanged 36→36).
- **We already do more ops than the tape and still lose.** 2,978 vs 2,800 work ops, 862 vs 935 idle
  ops, and we finish $11k behind.
- **Routing is not the constraint either.** The greedy solver already covers 60/60, 61/61, 48/51→
  51/51, 25/25 on d26-d29, but dropping days from `SOLVED_DAYS` on "coverage looks fine" reasoning
  cost −$2,277 and returned weeds to 5/day — coverage and visit order are different claims.

**`LATE_SEASON_PAIR`** (`FERTILIZE_UNTIL_DAY=26`, `LATE_TRUNCATED_PLANT_DAY=26`,
`HARVEST_A_TRUNCATED_ONE_SHOT`, gated to d26+) measured as a pair: stale routes −$1,863, re-solved
routes **−$370**, routes dropped −$2,647 (control $72,184 both times). With routes re-solved, per-op
rows land almost exactly on tape (plant d26 0→12 vs tape 11; water d28 26→38 vs tape 39; harvest d28
17→30 vs tape 20). **−$370 is explicitly undecided, not a win** — inside the ~15% seed-variance
band; the decider is `field_sweep.py` against recorded opponents.

#### The DIG/PLANT/HARVEST chaining defect behind it

The late-season plant/harvest gap is one defect needing two changes together, neither of which pays
alone. Half one: `DIG` clears ground exactly like a one-shot HARVEST does, but the replant-chaining
rule only fires on the HARVEST case — ground DIG clears stays empty for the rest of the season (seed
11 d26: 11 DIGs, 0 PLANTs offered; confirmed live on ladder episode `92433651`, 13 tiles dug and 0
planted the same day). This is the fourth instance of a recurring pattern already fixed three times
(`BUILD_THEN_PLACE`, `PLANT_THEN_WATER`, `REPLANT_A_CLEARED_TILE` itself). Implementing the DIG chain
alone was measured and **reverted**: it cost −$2,898 and the target d26 plant count did not move at
all, because half two blocks it independently.

Half two: `plant_prize('WHEAT', 25)=75.0` but `plant_prize('WHEAT', 26)=0.0` — correctly zeroed under
the rule that a one-shot only pays through a full-window HARVEST, since a d26 planting can't reach
its harvest day before season end. But Victor's own recorded play (`91854176.json`) plants 11 wheat
on d26 and takes a genuinely **partial** harvest on d29 (26 units at age 2-3, not the full 4-day
window) — the environment allows this, and it is wheat-specific: every melon Victor harvests is a
full `held 6/max 6` at exactly age 10, never partial.

**Fix order matters:** teach the harvest rule to accept a partial one-shot near season end first
(which makes late `plant_prize` non-zero), then chain the DIG-to-replant fix on top. Measuring
either half alone will misread as a loss or a no-op. Route note: the 8 pre-solved routes are keyed
to exact job lists, so either change invalidates all of them and requires re-solving in day order.

### The milk-floor correction, and where the SELLABLE bug hid inside it

**Correction, 2026-08-13: "the milk floor is partly a harness artefact."** Three real downloaded
ladder episodes (`92450417`, `92443929`, `92442061`) carry market price at each day's close: MILK
does not floor in these three — 169→279, 169→258, 169→154 (WOOL dips to 82 on d10 in one, then
recovers to 245). `breakdown.py` seats our agent against a *replayed* tape, and both sides sell into
one shared book, so a tape that sold 303 milk in its own real game sells it *again* next to us in the
harness — glutting a book no real game gluts. **§30 below's own two real ladder losses show MILK
closing at $5 and $3** — both real ladder data, both post this correction. Not a strict contradiction
(milk floors in some real games and not others, consistent with "cow count is causal" below) but
"never floors" is too strong; read as **"milk does not always floor on the ladder; whether it does
depends on cow count relative to the opponent's."**

What does replicate across 11 real ladder losses: **every game where `SHOP_ADAPT_HERD` cut cows to 6
closed MILK above base ($169/$235/$249); every game running 8-9 cows floored it at $1. The cow COUNT
is causal.** `SHOP_ADAPT_HERD` floats the cow/sheep split on which shops *exist*, never reads
realized price — we run COW 10/SHEEP 4 against every recorded opponent's COW 8/SHEEP 6.

**RETRACTED, SELLABLE correction:** the same 2026-08-13 file also claimed "not one egg is ever sold"
across a full season with `HERD_GEESE=2` (animals 10, season money $48,196 vs $71,814 without geese,
sell revenue $188,908 vs $214,385) and concluded "the geese verdict was measuring our own bug" —
diagnosing the zero-egg-sales as a routing/outcome-only-sweep artefact. **This diagnosis is itself
almost certainly wrong: §30 below confirms EGG was unsellable by our own agent until commit
`c99a8a5`, landed the same day.** The true cause of zero egg sales was that the agent could not emit
a SELL EGG order at all, not a routing artefact. **This is the fifth time an animal verdict in this
project has turned out to be an artefact of our own code** (see `docs/REGISTER.md`'s SELLABLE
caveat). Geese/eggs are a live, re-openable axis in the running product-mix sweep now that the fix
has landed.

### Carrot economics — pool verdict VOID, needs re-run

`carrot_swap_2026-08-12.md`'s own investigation independently discovered, one day before the official
fix, that the schedule's `sells` rows never emitted CARROT — every tape-mutation arm in that file
banked $0 of carrot revenue by construction. It also found the framing itself was wrong: real leader
play (カワシギ's tapes) plants carrot d21-d26 as an **addition** to otherwise-idle late-season ground
(wheat can no longer finish there; carrot's `first_yield_day=2` still can), never as a wheat
substitute.

**Because `SELLABLE` excluded CARROT entirely until `c99a8a5` (2026-08-13), the file's pool-level
"deciding measurement" was also run against the real game engine before the fix landed, and must be
treated as void alongside the tape arms until re-run:**

```
CARROT_SWAP=1     seeds 1300-1303 (192 games/arm)  win rate 65.1% -> 54.7%   (-10.4pts)
                   seeds 1306-1309                  win rate 67.2% -> 59.4%   (-7.8pts)
CARROT_TILES=4     768 games                        win rate 72.2% -> 71.1%  (-1.1pt, null)
```

`CARROT_SWAP` shipped OFF on this evidence; that verdict is now unsafe to rely on. If SELLABLE
blocked carrot sales throughout the measurement, a negative win-rate result is unsurprising and
uninformative — it may simply re-measure "carrot revenue is zero because the engine blocks it," not
"carrot is uneconomical."

**The one plausibly-durable number, because it's planner-independent price-curve arithmetic rather
than a played-out measurement:** carrot's market book tops out at **$3,502 on the best of 16 towns
and $91 on the worst** (vs strawberry's $29,172 and wheat's $12,246 on the same town) — the flattest,
shallowest book of any crop measured, which caps how much even a perfect planner could ever extract
from it as a wheat substitute.

Whether carrot pays as a **late-season addition** on otherwise-idle ground (the real question, opened
above) remains genuinely untested and is the live open question, not "does carrot substitute for
wheat."

### Validated levers, ranked

A 124-seat/62-game lever-correlation table: sell_orders +0.384, feed +0.359, harvest +0.334, care
+0.327, hires +0.301, buy_product +0.255, herd +0.258, tiles +0.149, plant −0.050. Money: ours
$73,977, field $68,091, top-20% $116,407. `buy_product` (feed conversion) is the one lever still at
only the 49th percentile against a top-quintile value of 1,156 — everything else is already matched
or beaten against the field.

**`vs_tapes.py` against `oldleader`, not the arena pool, is the discriminating fixture.** We lose 4/4
to `oldleader` (a real top player who reacts, margins −$4,268 to −$8,982) but beat Seb's own tape by
+$98,483 on one seed — the tape we copied our schedule from is not a hard opponent. The 94.4%
arena-pool figure and the non-discriminating handover fixture should never be read as "we're close";
gate future selling changes on `vs_tapes.py`/`oldleader`.

Opening-vs-tape test: our planner from day 0 wins 0/6 (mean $47,756); tape opening + our agent from
day 11 wins 4/6 (mean $67,181).

### Still-open items from this section

- Re-confirm `LATE_SELL_BIAS` on a wider seed set (the 12.5pp win-rate gain is real on 8 seeds, not
  yet reconfirmed against a current pool, beyond the single fixed-harness re-run above).
- Re-test `CAP_SELL_OFFER_SIZE` specifically against contrarian, the only opponent that produced an
  over-30 offer in the wider sweep.
- Wire `opponent_net_trade` into the reservation-price call site (`competition_brief.md` §6).
- **Re-run the carrot pool verdict and the geese/EGG measurement now that `c99a8a5` has landed** —
  both were void under SELLABLE.
- Meter milk sell rate or cut cow count toward the field's COW 8/SHEEP 6 — "this is where the ~$11k
  gap is" per the cow-count-is-causal finding above. Partially addressed by `1f7d457`'s herd-sizing
  fix; not yet re-measured against this specific comparison.
- `FERTILIZER_RESERVE_LOOKAHEAD_DAYS` relaxation is not established as safe; the d16 incident it
  guards against (6/12 FERTILIZE fired) has not been re-tested with a smarter reserve.
- Field-sweep `LATE_SEASON_PAIR` (currently −$370 on one seed, inside seed variance) to a decision.
- Fill the DIG-to-replant chain, but only after the partial-one-shot-harvest fix lands first.

## 30. How deep each market is, and why the two losses of 2026-08-13 happened

Folded in from `market_depth_and_the_morning_losses_2026-08-13.md`. Both losses are near-mirrors
decided in the last third of the season, and both point at the same thing: **we ship volume into
products the town does not drain, and under-ship the one it does.**

> **Correction to §29 and to this section's own §"why the herd was too small," 2026-08-13.** The
> commit these sections describe as an open defect — `_herd_split`'s `want_total` "forbidden from
> growing it," "capped at the schedule's own count" — was fixed the same day this file was written,
> by `1f7d457` (`architecture.md`, "herd sizing"). `HERD_GROWS_WITH_THE_DRAIN` now lets the count
> grow, and the wool branch no longer returns early. The `92550780` analysis below is the exact
> measurement that motivated that fix, not an independent, still-open finding.
>
> **A separate correction, on reading `scripts/why_we_lost.py`'s output.** Its per-product summary
> prints seed ORDER quantities in a column a reader can easily mistake for plants. Real plant
> counts are constant across all five ladder games analysed for the herd-sizing fix — WHEAT 138,
> STRAWBERRY 36, MELON 19, CARROT 6 — because our own schedule is deterministic; a seed-order figure
> that looks like a plant count and varies game to game is the tell that it is not one.

### The depth table (computed from `reference/kaggriculture.py`, not from play)

`market_price` depends on **market inventory only**. Shops move the price solely by draining that
inventory, so exactly two numbers matter per product: how much the town absorbs over a season
(= the sustainable sell rate) and how much net excess takes the price to $1.

    product      base  shops   drain     p@50    p@100    p@200     to $1
    ------------------------------------------------------------------------
    WHEAT          25      5     525       22       21       21     never
    CARROT         35      2     327       27       23       19       842
    TOMATO         60      2     228       42       35       24       529
    STRAWBERRY    120      4     426       24        1        1        62
    MELON         250      0      30      225      150        1       158
    EGG            50      2     228       43       42       41     never
    MILK          160      3     327       55        1        1        76
    WOOL          200      1     228       55        1        1        59
    FERTILIZER    100      0       0       90       80       60       493

`drain` is the expected season total: instance N unlocks on day 3N so it is live for `180 - 18N`
four-step ticks (792 tick-instances over eight draws), shops are drawn **with replacement** from the
eight names, and a single-product shop consumes double (`_town_consume`).
`p@N` is the price after N units of net excess sit in the book.

Read off it:

- **WHEAT and EGG never floor.** Both decay as `log`, so the price is essentially flat: 200 wheat
  still fetches $21 of a $25 base, and 200 eggs $41 of $50. These are the two bottomless markets.
- **WOOL, MILK and STRAWBERRY are shallow to the point of fragility** — 59, 76 and 62 units of
  excess and they are at $1. Wool and milk are also the two highest-value products, so they are
  simultaneously the best and the easiest to destroy.
- **MELON has no shop at all.** Its only buyer is the town centre, 1 unit per 24 steps, 30 a season.
  A $250 base with a 30-unit season of real demand.

**The EGG line matters for the goose axis.** Egg is one of the two products that cannot be flooded,
and it was unsellable until `c99a8a5` — so every previous goose measurement was taken with the
revenue line disconnected. That is now in the running sweep as a live axis.

### `92550780` — lost $69,881 to $77,275 (-$7,394)

The town drew `YARN_STORE` **three times** and `PET_CAFE` twice, so it wanted **1,074 wool** and
**716 carrot** over the season.

    WOOL   closed $252  of base $200   drained 1,074   <-- ABOVE base all season
    CARROT closed $ 42  of base $ 35   drained   716   <-- ABOVE base all season
    MILK   closed $  5  of base $160   drained   358
    STRAW  closed $  3  of base $120   drained   179
    MELON  closed $ 25  of base $250   drained     0

Wool closing **above** its base means total supply never caught the drain: every additional wool
unit that season was worth about $250 and there was room for it. We had **8 sheep to Densike's 4**
and shipped a fraction of the wool they did — on the slice of turns where attribution is
unambiguous, 28 units / $6,738 against 115 units / $28,158.

At the same time we put milk and strawberry on the floor, in a game where the town drained only 358
and 179 of them.

### `92562037` — lost $129,161 to $133,724 (-$4,563)

A true mirror: both sides ~148 wheat, both ~13 animals, near-identical sell cadence.
The one large divergence is **melon — we planted 136 to their 19**, into the product with zero
shops. It closed at **$25 of a $250 base**.

### Both losses are lost after day 18

    92550780   d18 -$84       d21 -$10,532     d29 -$7,394
    92562037   d18 +$6,363    d21 -$1,155      d29 -$4,563   (their last day +$10,469 to our +$4,080)

The opening is not the problem in either game. The late season is.
The first `SELL CARROT` is step **598** and **617** — day 25 — in games where the town was draining
carrot from day 3.

### Attribution caveat

Per-seat units are computed from the shared market ledger,
`inv(t) - inv(t-1) = sold_us + sold_them - bought - town_drain`, which is exact only on turns where
one side alone trades that product. Most volume lands in a `shared` bucket (1,260 and 1,803 units)
and is **not** split by a guess. The wool ratio above is the unambiguous slice, not the season total.

### The melon/strawberry answer is CONDITIONAL, and the running sweep cannot find it

Strawberry floors after **62 units** of excess, and its drain swings from 179 to 895 units a season
purely on how many strawberry-carrying shops the town draws.
That makes the melon/strawberry split a *conditional* answer, not a constant one:

    92562037   5 instances carry STRAWBERRY   drained 895   closed $187 (above base)
               -> melon land was worth roughly 8x more as strawberry
    92550780   1 instance  carries STRAWBERRY  drained 179   closed $  3 (floored)
               -> the swap buys nothing; that town wanted WOOL and CARROT

**`scripts/product_search.py` varies `melon_day` and `melon_shift` globally**, across whatever shop
draws the seeds happen to produce. If the truth is "strawberry when the town draws strawberry shops,
melon otherwise", then a global axis averages the two regimes together and reports a **wash** — the
arm that wins on one draw loses on the other, and the marginal comes out flat.

A flat marginal on that axis is therefore **not** evidence that the split does not matter. It is the
expected result of asking a global question about a conditional quantity. The same trap would have
hidden `WOOL_SHOP_SETS_THE_HERD`, which only reads as a rule once the games are split by the draw.

The fix is to slice the dump by shop draw rather than to add another axis — `--analyse` already
keeps every game, and the shop list is recoverable per seed.

### The closing days: a bare pasture, and one starved cow

Alex spotted an empty pasture. It is real, it is in every game checked, and there are two separate
causes behind it.

`kaggriculture.py:804`: **two consecutive unfed days and the animal escapes, leaving the structure.**

    92550780   final herd COW 6 SHEEP  8   bare structures 1   escapes 0
    92562037   final herd COW 9 SHEEP  4   bare structures 2   escapes 1  (COW, day 24, -$400)
    92548920   final herd COW 6 SHEEP  8   bare structures 1   escapes 0

So one bare pasture per game is a pen **built and never stocked**, and in `92562037` a second one is
a cow that starved on day 24 — $400 of stock plus five days of milk, in a game lost by $4,563.

The bare pen appears on day 24 and is still bare on day 29 in both losses. We were holding $53k and
$95k at that point; a sheep costs $500.

### Why the herd was too small in `92550780`, specifically — the finding behind `1f7d457`

The town drew **`YARN_STORE` three times** — at draw #1 (d3), #4 (d12) and #6 (d18). Three
instances is 6 wool a tick, 1,074 a season. Eight sheep produce roughly 100 units in a season (first
yield day 6, one unit every 3 days). The town wanted ten times what we could make, which is why wool
closed **above** base at $252 and never came down.

**The split rule fired correctly and the COUNT is what failed — this is the exact defect `1f7d457`
fixed the same day.** Every `BUY_ANIMAL` we issued (pre-fix):

    d0  COW 1, SHEEP 4     d4 COW 1   d5 COW 1   d6 COW 1   d7 COW 2
    d8  SHEEP 2            d12 SHEEP 1          d18 SHEEP 1
    ------------------------------------------------------------------
    total requested        COW 6, SHEEP 8   =  14 animals

`WOOL_SHOP_SETS_THE_HERD` did exactly what it is written to do: yarn was in the first three draws,
so cows were held at `WOOL_SHOP_COW_CAP = 6` and every remaining animal went to sheep. But the
rule's own reference table says a draw-#1 yarn store means **COW 6, SHEEP 12, total 18**, and we
ran a total of **14**. `_herd_split` re-split a `want_total` it was handed and was, pre-fix,
explicitly forbidden from growing it ("capped at the schedule's own count"), so the sheep-heavy half
of the rule landed and the extra four animals never did. `92548920` — yarn at draw #2 — was the
same: COW 6, SHEEP 8, total 14, where the table says 18. **`want_total` is now a floor, not a
ceiling; see `architecture.md`.**

**And the early return used to skip the one branch that does count instances.** Below the wool rule,
`_herd_split` runs a greedy over `town_drain_remaining(...) + expected_future_drain(...)`, which is
genuinely instance-aware and would have seen three yarn stores. The wool rule used to `return` before
it. So the code's drain-aware allocation was bypassed in precisely the case where the drain is
extreme. **Fixed: the branch no longer returns.**

**The bare pen is the same story from the other end.** Fifteen `BUILD_PASTURE` ops, and pens are
still being built on d21 (2) and d24 (1) — after the last animal purchase on **d18**. Fifteen pens,
fourteen animals.

### On the forum claim ("multiply base by shop count")

Half right, and the half that is wrong is the half that matters. Shop count sets the **sustainable
rate**, not the price: the price is a pure function of inventory. Milk with three shops still floors
after 76 units of excess, which is why our own milk has repeatedly closed at $1-$5 while the claim
says it "sells above 160 most of the season". Both statements are true at different volumes — the
drain is about 327 milk a season, roughly 11 a day, and a herd that produces faster than that puts
its own price on the floor no matter how many shops are open.

## 31. Lessons carried over from Orbit Wars

Folded in from `lessons_carried_over.md`. Source material lives at
`~/DataspellProjects/orbit_wars/orbit_wars_jax/docs/` — in particular
`rl_postmortem_and_fix_plan.md` and the five competitor write-ups
(`rl_lessons_isaiah_pressman.md`, `rl_lessons_simjeg.md`,
`rl_lessons_billy_bradley_ender.md`, `rl_lessons_felix_neumann.md`,
`rl_lessons_lin_myat_ko.md`).

Read the post-mortem in full before any serious RL work.
This section is the distillation, not a replacement.

Note: the oldest memory file credits Lin Myat Ko as 1st place.
The corrected standings are Isaiah Pressman 1st, simjeg 2nd, Felix Neumann 3rd,
Billy Bradley 8th.

### The short version of what went wrong last time

RL was never impossible — 1st and 2nd place were existence proofs, and 2nd place did it with a
4.3M model barely larger than ours.
The collapses were **structural**: a wrong action parameterization and the wrong *kind* of prior.

Concretely:

- The action was one categorical over ~480 candidates plus NOOP, where NOOP was ~95% of labels.
  The loss was minimised by always predicting NOOP.
- The candidate menu was filtered to the top 192 by heuristic *quality* score, which pinned the
  ceiling to the heuristic's taste and censored the interesting expert moves out of the IL labels.
- Dense per-step shaping rewards optimised a proxy, producing ~50% against random and 0% against
  strong heuristics.
- No-op became a genuine self-play equilibrium that nothing in the setup punished.
- Total experience was **~500 complete games**. The winners ran 2-50 million.
  "Never beat random" was the *expected* outcome, not a failure mode.

### What transfers directly

**Process, mostly. These are the expensive ones.**

1. **Measure before theorising.**
   Log explained variance and return mean/std every update, from the first run.
   `ret=0.00±0.00` means the reward is not reaching the algorithm — stop everything.
   Half the Orbit Wars diagnoses were guesses because nothing was tracked.

2. **Read the logs before building a narrative.**
   The tidy single-cause story in the post-mortem was constructed without reading the logs and was
   mostly wrong. Real RL projects die of a scatter of mundane failures — plumbing bugs, missing
   normalization, KL death, entropy collapse — not one elegant villain.

3. **When every config fails the same way, the problem is what they share: the pipeline.**
   Orbit Wars treated a pipeline-bug signature as a hyperparameter signature and kept restarting
   into the same broken plumbing.

4. **Entropy going down is learning. Entropy crashing to ~0 while win rate is still random is a bug.**
   Kill losers fast, but run winners *long*. Felix killed 3x more runs than he kept and ran the
   survivors 8.4B steps. Both halves are required; Orbit Wars only ever did the first.

5. **One delta at a time, ablation-driven.**
   A stupider architecture that trains beats a smarter one that does not.

6. **Commit to a kill criterion up front**, before the sunk cost accumulates.
   See `CLAUDE.md` for this project's three.

7. **Validate priors with the cheap signal** — supervised ablation and a fast local arena —
   not with full RL runs. Orbit Wars used the most expensive possible signal on the least compute,
   which is why every ablation was inconclusive and every diagnosis a guess.

8. **Near-total ban on "it can't be done."**
   The honest form is "our current setup isn't learning it, and I don't yet know whether that's the
   frame or the game" — then go measure explained variance and find out.

### What does NOT transfer

Do not cargo-cult these. They were correct answers to a different problem.
The reasoning is in §32 below.

- **"Masking backfires."** That was about masking no-op to force action. Legality masking is
  explicitly safe.
- **"Self-play is essential."** The opponent coupling here is weak — market prices only.
- **"Collapse the action space to all-in."** That fixed a 480-way categorical.
  This action space is already 18 ops.

> **A correction, because this section used to argue the opposite.**
> It said "never shape the reward" does not transfer, on the grounds that a per-step bank delta is
> an exact decomposition of the true objective rather than a proxy. The arithmetic is right and the
> conclusion was overruled: **the ladder is Elo, so bank is itself a proxy for the score.**
> The reward is terminal — win 1, loss 0, gamma 1.0 — for every policy in this project.
> The Orbit Wars ban does transfer, for a reason Orbit Wars did not have.

### The prior taxonomy — the crux, and it still applies

A prior either **shapes the learning problem** or **is the policy**.

- **Shapes the problem (safe):** constrains inputs or action space, learner chooses within it.
  If slightly wrong, the learner routes around it.
- **Is the policy (brittle):** the rule makes the decision. Every imperfection is a permanent ceiling,
  because there is no learner underneath to compensate.

The test: **safe if it only removes moves that are never optimal (a legality fact);
dangerous if it removes moves based on a guess about which move is good (a quality judgment).**

You can stack many safe priors. The problem is never the count, it is the *kind*, or an unvalidated one.
Assertion is not validation — simjeg ablated every prior with cheap IL before touching RL.

**Applied here:** legality masks are safe and encouraged.
A "sensible actions only" filter would be the Orbit Wars mistake repeating itself. Do not build one.

### The right use of a heuristic agent

This is the lesson that cost the most and is easiest to get wrong again.

In Orbit Wars the hand-built v131 heuristic became the policy, then became a candidate filter.
Both capped the ceiling.
The post-mortem's verdict:

> Our whole heuristic effort was the wrong tool for BEING the policy but the perfect tool for
> TEACHING the policy.

**In this project the heuristic agent is, from day one and explicitly:**

- a leaderboard placeholder from week 1,
- the sparring and evaluation opponent,
- the IL bootstrap and offline-search seed.

It is **never** the final policy and **never** a filter on what the learner may consider.

### How to drive the advisor

Verbatim from the post-mortem, because it is about working with Claude and applies to this project too.

> Claude is a better critic than collaborator: fast at finding flaws when given a finished thing
> plus an answer key; prone to helping you walk confidently in a plausible wrong direction
> mid-build unless forced to challenge the frame.

Counters that worked:

- Ask the strategic question explicitly: *"is this collapse telling us the FRAME is wrong? argue that it is."*
- Force the null hypothesis: *"give me three reasons this whole approach is doomed."*
- Demand an existence proof on **day one**: *"has anyone done RL on a game like this, what was their action space?"*
- Commit to a kill criterion up front so the conversation cannot drift into endless tactical tweaks.
- Distrust confident impossibility claims. Make Claude produce the evidence before accepting "can't".

A live example from this project: the first read of Kaggriculture confidently concluded
"RL is the wrong tool, build a planner."
That was overcorrection from the previous competition, and it was overturned by two facts
(`actTimeout`, action-space size) that had not been checked when the claim was made.
Alex pushed back; the claim did not survive contact with the environment source.
**Check the source before forming the opinion.**

### Standing feedback from memory

These are recorded preferences that apply here.

- Never silently change model architecture — ask first.
- Always inspect actual observation data before using field indices. Do not assume the format.
- Test locally before submitting. This competition allows 5 submissions/day.
- `ent_coef`: Orbit Wars used 0.02, which may have been far too high.
  Alex's friend uses 0.0005 for large MultiDiscrete spaces.
- Do not declare things impossible. Check explained variance first.
  Suspect the frame and the parameterization before the model capacity.

## 32. The RL track: what it measured, and why it is parked

Folded in from `rl_feasibility.md`.

> **IMPORTANT — do not read this section in isolation and reintroduce the per-step reward it
> overrules.** This section used to argue for RL as the primary tool and for a per-step bank-delta
> reward. Both were overruled, and the arguments have been replaced below with the measurements that
> overruled them. `CLAUDE.md` carries a bullet warning that a future session might read this section
> alone and "restore" the per-step reward from it — that bullet exists because the arithmetic in the
> original argument (final bank minus starting bank is *exactly* the sum of per-step deltas) is
> genuinely correct, and only wrong once you add the fact that the ladder is Elo. Read the ruling
> below, not just the argument; the ruling is what stands.
>
> The path (`rl_feasibility.md`) that used to hold this content is unchanged, because `CLAUDE.md` and
> several modules point at it; the content itself now lives here.

### The ruling on reward, and it applies to every policy in the project

**The reward is terminal: win 1, loss 0 (or -1/+1), gamma 1.0. Never per step.**
Alex's call, made explicitly, 2026-08-01.

The original argument for per-step bank delta was that final bank minus starting bank is *exactly*
the sum of per-step deltas, so it is reward **decomposition**, not shaping. That is arithmetically
true and strategically wrong: **the ladder is an Elo rating, so margin does not count.** A $43k win
and a $4k win are the same result, and a per-step money reward trains a margin maximiser.

It is also what the evidence says. Of the top finishers in the comparable competition whose
write-ups we have, four used a terminal signal — Felix Neumann -1/+1, simjeg terminal with
gamma 0.995, Isaiah Pressman terminal, Billy Bradley's `ender` positive-only 0/1/2 with gamma
0.998 — and **none** used a per-step bank delta.

If credit assignment over 720 steps stalls, the agreed next move is a **per-game-day** signal, not
a per-step one, and only after `explained_variance` has been checked.

Potential-based shaping is a separate question and is not banned by the above: Ng, Harada & Russell
1999 leaves the optimal policy provably unchanged, and at gamma 1.0 the per-turn terms telescope so
an episode's total shaping is exactly `PHI(end) - PHI(start)` whatever route was taken.
`kagg/rl/money_potential.py` implements one (floored at the $3,000 stake, scaled to $100k, squared)
with 16 tests. `coef` defaults to 0.0 and it was **never wired into `train_jax_rl.py`**.
`kagg/rl/net_worth.py` sketches a balance-sheet potential that would stop FEED and FERTILIZE reading
as pure loss. Neither was built out; both are recorded here rather than in a separate ideas file.

### Why the track is parked

The problem does not have the property RL is for. See §33 below for the full argument; the short
version:

- **There is nothing to react to.** The top of the leaderboard submits byte-identical 720-turn
  tapes across seats and opponents (§27 above).
- **The environment is deterministic given the tape**, so `Q(s, a) = V(s')` can be *computed* by
  simulation rather than estimated. One perturbation's effect is an **exact finite difference** —
  the quantity a critic, GAE and 719 steps of credit assignment exist to approximate.
- **The reward is terminal and the objective is a ranking against a fixed field**, which is a
  best-response computation.

RL becomes right again if the field turns adaptive, or if the state space outgrows exhaustive
evaluation. Neither is true today.

### What the track measured, and it is worth keeping

Every item below is a measurement that cost real time to obtain. Several are about *measurement*
rather than about RL and generalise to anything this project does next.

#### The failures were temporal, not architectural

`jax_sim._end_of_day` returns every unit to spawn, **dismisses every hired hand** and **empties
every unit's inventory**. So every *maintenance* op — which needs a walk back to a tile on a later
turn — is re-motivated from scratch each dawn: four independent draws that must all land, for a
payoff days away, under a critic at `ev_signal < 0.3`.

Over 412,992 owned-unit actions the policy placed 4,591 animals and **fed 12**; planted 13,439
crops and **harvested 98**. Setup ops (PLANT, PLACE — one action, on the tile you already occupy)
it did *more* than the teacher. **It did not fail to learn farming; it learned exactly the subset of
farming that survives a one-step credit horizon.**

That killed the "it can't do them" theory outright: on day-25 seeded boards, COLLECT_FERTILIZER is
legal on 15.1% of unit-slots and CARE on 11.2%, and the policy had chosen COLLECT_FERTILIZER **zero
times in 23,684 episodes**. Legal often, never taken.

`kagg/rl/commit.py` fixes it: a `COMMIT_*` token in the same categorical as every primitive op
freezes a target, the unit walks it and fires the arrival op on contact, and intermediate turns are
**excluded from the PPO density** (not scored as probability 1). After **11 updates**:

| op | before | with commitments |
|---|---|---|
| COLLFERT / FERTIL | **0.00%** | 2.01% |
| CARE | 0.07% | 1.98% |
| PICKUP | 0.63% | 3.58% |
| HARVEST | 0.44% | 1.14% |
| harv/plant | 0.18 | 0.63 (teacher 2.28) |

#### The decode destroys the behaviour, not the network

`play_checkpoint.py` defaulted to per-head argmax. Same checkpoint, same 32 games:

| | greedy | **sampled** |
|---|---|---|
| WATER | 0% | **5.62%** |
| PLANT | 0% | **2.50%** |
| raw FEED | **0** | **18** |
| bank | $2,998, zero variance | $1,305 (min 54, max 3,534) |
| W/D/L | 0/0/16 | 0/0/16 |

**The marginals contain the behaviour; argmax over independent per-head marginals destroys it.**
Nine independent "probably not sell" decisions compose into "never sell". `condition_on_trade` —
drawing the op first and scoring the argument heads on the slice it selects — is the fix, and it
shipped for the **market** heads where the marginals discriminate 12:1.

`condition_on_op`, the same technique on the **unit** heads, was built and measured as **no
detectable difference** (effect changes sign between seeds; within-architecture seed spread is as
large as the effect). It is inert by construction there: `crop` is read by PLANT alone and was
already `p(crop | PLANT)`, and only PICKUP and PLACE share `item`/`qty`, at 7.8:1.
**Do not read that null on the unit heads as a verdict on the market ones.**

The durable value from that work is the scaffolding: the `ratio == 1.0` gate catches a silently
corrupted PPO update, and `migrate_params` means an architecture change no longer costs every
checkpoint and the KL anchor.

#### Metrics that measured the setup, not the policy

This is the most expensive recurring lesson in the whole track.

- **`vs farm 0.659` was entirely an artifact of the seeded start.** From turn 0 the same checkpoint
  went 0/0/32, banking $2,998 against the scripted farmer's $30,292, with 100% movement and zero
  productive actions over a whole season. **Prefer a replay to an aggregate.** The reward pays 0.5
  for a draw, so two policies that both bank $0 draw with certainty — `money == money` is exact.
- **The per-opponent win rate measured nothing** even though it was computed on exactly the right
  rows: the opponent was re-drawn every update while a game spans ~22.5 of them, so a game faced a
  mean of 4.9 distinct opponents and the label recorded whoever held the seat at the end.
  **Ask what unit an aggregate is aggregating over, and whether the label is constant across it.**
- **The curriculum mix was specified in slots and spent in episodes.** `0:0.1` asked for 10% of
  slots and delivered ~3% of finished episodes, because day-0 episodes are ~6x longer. Day 25
  supplied ~83% of terminal episodes, so the aggregate `wr` was a day-25 number wearing a mix's
  name — and it was carrying four rungs sitting at chance (day20 0.523, day15 0.491, day10 0.484,
  day0 0.528).
- **`ev_signal` and the animal gap are structurally uninformative under symmetric starts.** With
  identical seats the true value is 0.5 on every board at t=0, so there is nothing to explain from
  the state. **The >0.5 explained-variance kill criterion does not apply to a symmetric run.**
- **`best.pkl` is selected on cumulative win rate and therefore favours early updates** — update 38
  on one run whose settled rate came much later. Prefer `latest.pkl` unless you have checked.
- **After any configuration change, check whether a metric still measures what it was calibrated
  on.** Four numbers in one session were read as findings when the setup had changed what they
  measured.

#### The scale gap was the real story

| | bank |
|---|---:|
| top public agents, head to head | **$90,000 – $123,000** |
| our policy at update 690 | $18,332 median, $34,127 best |
| our best training opponent (`farm`) | $27,340 |

**We trained against a pool whose ceiling was a quarter of the field's floor**, and no opponent in
it used the animal economy, crops beyond melon, fertiliser or a twelve-hand crew.
Meanwhile total experience across the whole track never approached the 1B-15B env steps the
competitors in the comparable competition used — Billy Bradley ~1B on a single 3080, simjeg 10B,
Isaiah Pressman 15B.

**We were step-bound by roughly two orders of magnitude, not capacity-bound.** `kagg/rl/jax_policy.py`
defaults to `d_model=128, n_layers=3, n_heads=4`; simjeg took 2nd in the comparable competition with
4.3M parameters and Felix Neumann 3rd with 6.2M. Scaling the model was measured as the wrong lever.

Throughput is in §34 below. VRAM was never the constraint.

#### Hardware

The 3080 had been running at **210 MHz of 2100** under `SwThermalSlowdown` at 90 C, drawing 41-64 W.
Every throughput figure in the RL era was measured on a throttled card and the "1B steps is about a
month" estimate was 3x pessimistic. Cold it does ~1,100 turns/s and decays to ~370 within two
minutes.
**This is closed and ruled on. Do not re-rank cooling into any review.**

### The Orbit Wars killers, and which transferred

Kept from the original file because the table is still the right analysis of *this* environment.

| Orbit Wars killer | Applies here? | Why |
|---|---|---|
| No-op became a stable self-play equilibrium | **No** | PASS buys you $3,000 while the opponent banks $50k. The environment punishes passivity directly. |
| Masking was a quality judgment | **No** | Masking here is pure legality. The thing that burned us was masking *no-op* to force action. |
| Reward shaping optimised a proxy | **Partly** | Money is not a proxy for bank, but bank is a proxy for the Elo score. Hence the terminal ruling above. |
| Exploration shattered across ~480 options | **No** | 18 ops per unit. |
| Self-play instability | **Largely no** | The opponent couples only through market prices. |
| Candidate filter capped the ceiling | **Avoidable** | There is no candidate-generation step to poison. Keep it that way. |

The genuinely transferable warning is the death spiral: RL not learning → "help" it with heuristics
→ the help starves the learner → conclude RL cannot do this. The defence is the kill criteria in
`CLAUDE.md`, committed before any code was written.

**Scope note on the explained-variance gate.** It was written for the per-turn, 720-step,
full-action-space policy. `kagg/rl/env.py`'s strategy env clears 0.89 easily, but that is a 30-step
problem with 9 discrete heads and hand-built features. Clearing it there is *not* evidence the hard
frame works.

### Two corrections this track made to its own record

- **A decision to skip a fix can expire when the problem changes.** `hand_prior_heads` declined to
  shape the market heads for a stated and correct reason: their failure was *under*-firing from a
  broken joint decode, and a flat prior would not fix a missing correlation. The autoregressive
  decode landed and the failure inverted to over-firing — `buy_seed` on 29.1% of turns, bank at $0
  by day five. Same code, same argument, opposite problem.
- **Evaluate a technique against the problem its author built it for.** Ender's autoregressive
  micro-steps were assessed here against the spawn deadlock — correctly answered *no*, twice, and
  struck off. He built them for **action-space explosion**, which we independently had and had
  measured three times. A correct *no* to the wrong question is indistinguishable from a dead end.

## 33. What kind of problem kaggriculture is

Folded in from `what_kind_of_problem_this_is.md`. Written 2026-08-05, after a day in which every
result that looked like a fact about the game turned out to be a limitation of our own code. The
purpose is to name the problem class precisely, so the next session reaches for the right tool
instead of rediscovering the wrong one.

### The short version

**It is a deterministic, open-loop, multi-dimensional knapsack with a time-phased budget, played as
a best response against a fixed field.**

Every clause is load-bearing and each rules out a family of approaches. Measured rather than argued:

- **the allocation is computable** — closed form from the town's drains reproduces the leader's farm;
- **the schedule genuinely needs search** — greedy-by-payback under a cash simulation recovers only
  23% of what a beam finds, so this half is not reducible to a rule;
- **the simulator is the verifier**, never the search engine.

We spent weeks treating all three as one undifferentiated search problem.

### Why it is not a reinforcement learning problem

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
evaluation can reach. Neither is true today. See §32 above.

### The structure, formally

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
near-optimal rather than a heuristic. See `competition_brief.md`'s Economics section §4 for the
arithmetic that recovers the leader's farm.

**But cash timing is not a mild coupling, and this is where the naive reading goes wrong.** Cash is a
flow, so "chain B is unaffordable until chain A has sold" is a precedence constraint that compounds
over thirty days: which chain to fund first, and whether a given dollar buys land or seeds, changes
what is affordable for the rest of the season. Measured, that coupling is worth roughly **four times
the allocation itself**. Additivity buys you the mix. It does not buy you the schedule.

### What genuinely needs search

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

### The tool ordering

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
> has since moved; treat them as evidence about *method*, not as current scores. See §25 above for
> why that stack was fully abandoned.

### The trap that has cost the most: overfitting the objective

Recorded twice in `CLAUDE.md` — *"a fixed 3-seed objective reported +40% where held-out seeds said
+12.8%"* and *"11 accepted moves in 14 generations for +1.6%"* — and `search_chains.py` had the
defect built in until 2026-08-05: the board draw was cached on one seed, so thirty generations of
five hundred candidates all fit the same sixteen games, and the incumbent kept whatever score its
lucky draw gave it and could never be displaced.

Both fixed: a new draw every generation, the incumbent re-scored alongside its challengers on that
same draw, and a `--holdout` pass that prints the in-search versus held-out gap so the curse is
measured rather than assumed.

**Seed variance is ~15%. Always quote the range.**

### The failure mode to watch for, because it recurred six times in one day

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

### The shape of the target

The top of the board is a knife-edge: everyone banks $120k-160k and the leader edges it by ~3%. On
an Elo ladder a $2,634 win scores what a $50,000 win scores, so the target is a **small consistent
edge over several near-equal fixed scripts** — and because they are fixed, they cannot punish
anything. They are a stationary target to compute a best response against.

## 34. Env throughput — measured

Folded in from `throughput_measurements.md`.

**Measured 2026-07-31.** Reproduce with `python scripts/bench_arena.py`.
This decides whether the vectorized simulator is optional. It is not.

### Numbers

`starter` vs `pass`, 100 games per row (worker startup amortised), 719 steps per game.

| Machine | CPU | 1 worker | best multiprocess | 1B steps | 10B steps |
|---|---|---|---|---|---|
| Mac (dev) | 14-core Apple Silicon | 1,054 steps/s | 8,009 (12 workers) | 35 h | 347 h |
| **Windows box (training)** | **AMD Ryzen 9 5900HX, 8c/16t** | **484 steps/s** | **4,221 (16 workers)** | **66 h** | **658 h** |

The training box is **2.2x slower per core** than the dev Mac and 1.9x slower in aggregate.
Every throughput figure that matters is therefore the Windows row, not the Mac row.

Scaling is poor: 16 workers gives only 8.7x over one worker on an 8-core/16-thread part.
SMT contributes little and the Python interpreter dominates.

### Correction to a previously recorded fact

`README.md` recorded **1163 steps/sec single-threaded** as a measured fact.
That figure is roughly the *Mac* rate and is 2.4x optimistic for the machine that will actually
train.
The training box does 484.

### What this means for the plan

Competitive runs in the comparable previous competition used **8-15B env steps**
(8th place ~1B on a single 3080; 2nd place 10B; 1st place 15B).

- 1B steps on the training box: **66 hours**. Viable once, far too slow to iterate.
- 10B steps: **658 hours, 27 days**. Not viable.
- To reach 10B in 24 hours the sim must sustain **~116,000 steps/sec**, about **27x** the
  Python env's best multiprocess rate.

These are also *optimistic* numbers, for two reasons:

1. They use `starter`, a trivial random policy. No policy forward pass is included.
2. **`env.run()` cannot feed a GPU.** It plays a whole episode with per-step agent callbacks
   inside a worker process, so policy inference cannot be batched across environments. The
   options with this harness are a CPU policy copy per worker, or shuttling observations to the
   main process over IPC every step. Both are bad, and neither is what the throughput above
   measures.

A vectorized on-device sim removes that entire class of overhead as a side effect, which is a
second, independent argument for it beyond raw speed.

### Consequence

The vectorized simulator is **required, not optional**, and its target is set by the 10B figure:
**~100k+ steps/sec**.
Renting GPU time should be considered rather than assumed away — one 3080 Laptop may not be
enough to be competitive even with a fast sim.

What multiprocessing *does* buy is a **proof-of-life run**: 100M steps in ~6.6 hours on the
training box, enough to test the RL frame against the explained-variance kill criterion in
`CLAUDE.md` before committing to the sim build.

### Correction: the "1,032x" sim figure was an idle-profile measurement

**Recorded 2026-07-31, after a JAX port measured the same code and could not reproduce it.**

The 499,543 steps/sec (and a later 752k) quoted for the numpy sim were measured with **one live
unit per player on an empty board**, issuing WATER against nothing. Almost every masked update hit
its `if not active.any(): continue` shortcut. That is the sim's best case, not its working case.

Measured again on the same machine, at B=512, with units actually planting:

| live units per player | steps/sec |
|---|---|
| 1 (the original figure's shape) | 818,000 |
| 8 | 571,000 |
| 24 | 356,000 |

And even that 24-unit figure is optimistic, because the units all start stacked on the spawn tile,
so after the first one plants the rest hit the occupied-tile early exit. An independent measurement
with units genuinely spread out and hiring each turn put the numpy sim at **~15,000 steps/sec** at
B=512 -- though that run was taken while the machine was at load 200, which the same benchmark
showed can move absolute numbers by up to 2x.

**What to trust:** ratios, not absolutes. Absolute throughput on this Mac varies with machine load
by up to 2x, so any single figure is only meaningful next to a control measured at the same time.
The speedup over the reference environment is somewhere between **30x and 200x on realistic
workloads**, not the 1,032x first recorded. That is still transformative -- a 1B-step run goes from
66 hours to somewhere between 20 minutes and 2 hours -- but the headline number was wrong and was
repeated in several places before being caught.

**The lesson:** a benchmark whose workload does nothing measures the shortcut, not the code. State
the workload alongside the number, always.
