# Experiment log

Append-only record of what was tried, what it scored, and what it taught. Newest last.

The point of this file is that several things in this project were "discovered" twice because a
measurement was made and then not written down. **If you measure something, put it here.**
`REGISTER.md` is the live open/closed list; this is the history.

> **Version caveat, added 2026-08-09.** The ladder moved to `kaggle-environments` 1.32.6 on
> 2026-08-07/08 (`competition_brief.md`, "version skew"). Entries below that date were scored on
> 1.32.2 and are not directly comparable to anything measured since — the town rebalance changed
> absorption by up to 4.67x on melon. Treat every dollar figure here as dated by its own entry, not
> as a current baseline. `docs/the_market.md` holds the current, 1.32.6-dated market
> findings.
> **2026-08-11 addendum:** `docs/the_ladder_is_two_scripts.md` and `docs/the_market.md`
> are newer still — the current position on strategy and market economics.

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

See `the_field.md` for the measurement. The consequence for this log:

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
  evidence says needs no reactivity at all. See `rl_feasibility.md`.

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
now itself superseded by `docs/the_ladder_is_two_scripts.md`'s rebase recommendation (Dmitry Belan or
Efe Can Celiksoy, `REGISTER.md` OPEN-10) — `chains.py`/`scheduler.py` are independently known to be
dead code, not part of the shipped submission.

## 26. The wheat-buying day budget — see `docs/fertilizer_and_wheat_supply.md`

A closed, shipped fix (`FEED_BUY_CEILING_DAYS=2`) for a purchase-side defect that had us buying
1,099 wheat/season against the field's 266-392. Full write-up, including the swept constant and the
routing/labor bottleneck it exposed at the tighter setting, lives in
`docs/fertilizer_and_wheat_supply.md` (merged there from `fable_the_wheat_churn_2026-08-09.md`,
2026-08-13).
