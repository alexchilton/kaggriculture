# Experiment log

Append-only record of what was tried, what it scored, and what it taught. Newest last.

The point of this file is that several things in this project were "discovered" twice because a
measurement was made and then not written down. **If you measure something, put it here.**
`REGISTER.md` is the live open/closed list; this is the history.

> **Version caveat, added 2026-08-09.** The ladder moved to `kaggle-environments` 1.32.6 on
> 2026-08-07/08 (`competition_brief.md`, "version skew"). Entries below that date were scored on
> 1.32.2 and are not directly comparable to anything measured since — the town rebalance changed
> absorption by up to 4.67x on melon. Treat every dollar figure here as dated by its own entry, not
> as a current baseline. `docs/the_market_2026-08-09.md` holds the current, 1.32.6-dated market
> findings.
> **2026-08-11 addendum:** `docs/the_ladder_is_two_scripts.md` and `docs/what_the_town_will_actually_eat.md`
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

---

# Part 4 — parity, plan-once mechanics, and arena infrastructure (2026-08-09 to 2026-08-15)

## 25. The day is planned once: dawn blind spots closed, d0-d1 exact

Folded in from `docs/handoff_plan_once_2026-08-09.md` and
`docs/plan_once_and_the_dawn_blind_spots_2026-08-09.md`.

> **Target superseded, noted 2026-08-11.** "d0 and d1 are exact" means exact against Seb's tape,
> which was optimal under the OLD `townCenterSellInterval=12` economy. Seb's median bank halved and
> he withdrew from the ladder (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats). The planner
> architecture change — one plan per day, at dawn — is real and still stands. Exact-match-to-Seb is
> no longer the same thing as exact-match-to-the-field.

Branch `shaping-potential`, HEAD `f5b1e3e` at the evening handoff.

**The question.** Alex's spec: "you should do the whole plan 1 time per day no replans no urgency
and optimise it so the schedule can be implemented - when you have done that the d0 - d6 should
match." An earlier session had solved this with plans at h0, h1 and h2 and it was not accepted: the
day is deterministic, so there should be no reason to replan at all.

**What was actually replanning.** `URGENT_OPS` was empty and the idle top-up had been deleted in
`5aa233e`, so exactly one trigger was left: `state["crew"] != len(live)`.
`tests/test_the_first_seven_days_match_the_plan.py::test_the_day_is_planned_once_and_only_at_dawn`
counts `_solve` calls per day and measured d0 planning three times (h0, h1, h3) and d1-d6 twice (h0,
h1). The cause is phase order, not hiring policy: `interpreter` applies unit actions and only then
calls `_process_market` (`kaggriculture.py:922` then `:928`), so a hand bought at hour 0 does not
exist when hour 0 is planned, appears at hour 1, and the dawn plan is thrown away. What actually
covered 23 of the 24 hours was an hour-1 plan.

**Four blind spots in the dawn plan, all real, all confirmed by a red test.**

1. The crew. The dawn plan cannot see hands the same turn is about to hire. Fixed by `_arrivals` +
   `_hires_this_turn` (`PLAN_THE_CREW_THAT_ARRIVES`), which model the env exactly: hires all settle
   in one turn because the atomic block re-enters per order slot (`kaggriculture.py:550,564`),
   `_hire_cost` is `mult * fib(hires_today)` per day, and `_do_hire` fails silently when the bank is
   short (`:691`). `_spawn_hand` gives the landing square, so phantom index `len(units)+k` is the
   same unit as real index `len(units)+k` an hour later.
2. The goods. `buys` lands at the end of hour 0, so the dawn plan reads a shed without it.
3. The animals. `BUY_ANIMAL` commits to `private["shed"]` like a product (`:672`), and `build_nodes`
   gates its PLACE branch on `shed[a] > 0` — so an empty pen the day means to fill offered nothing
   at dawn. This is why d3 and d6 planned zero placements while owning the pen. 2 and 3 are fixed
   together by `PLAN_TODAYS_PURCHASES`, which credits both rows at hour 0 only.
4. The pens. `build_nodes` reaches PLACE only through `elif kind in ("PASTURE", "COOP")` — a tile
   that is already a pen. On d0 the pens are built during the day, so the entire dawn node set is
   `{BUILD: 8, PLANT: 17}` with no placement in it to route, and everything
   `SERVE_THE_ANIMAL_IT_PLACES` hangs off a placement goes with it. `feed 0/4` on a planned-once day
   0 was never a feeding defect — it was two placements that were never in the plan. Attempted fix
   `BUILD_THEN_PLACE`: a pinned BUILD carries the PLACE, FEED and CARE for the animal `_refresh_pins`
   already chose that ground for.

**The measurement — three of four diagnoses net-negative.** Work turns d0-d6, tape 339. Higher is
closer.

```
config                                             geometry OFF   geometry ON
HEAD (5aa233e), nothing added                          317            305
+ PLAN_TODAYS_PURCHASES                                290            308
+ purchases + BUILD_THEN_PLACE (merged onto build)      --            281
+ purchases + PLAN_THE_CREW_THAT_ARRIVES               239            273
full plan-once, PLACE merged onto the build node        --            276
full plan-once, PLACE as its OWN node                   --            284
```

The last two are the same feature implemented two ways. `Node.prize` sums its ops and `Node.service`
counts them, so folding PLACE + FEED + CARE onto the BUILD made a four-op node that outbids and
out-costs everything near it: the allocation reshuffled and `build_pasture` went 8/8 -> 6/8 and
`plant` 17/17 -> 14/17 to buy two placements. Emitting the placement as a separate node on the same
tile leaves the build untouched — the route is a visit order and `_live_ops` re-derives the work at
each stop, so the second visit reads a pen that is now standing. That is worth +8 over the merged
form and still 33 short of HEAD.

Also found and reverted: `DRAWN` contains BUILD and a pinned build carries the animal in its item
slot, though `_emit` uses it only to pick BUILD_PASTURE over BUILD_COOP and consumes nothing. While
BUILD and PLACE shared a node, `Node.needs` summed them and demanded two cows to fill one pen.
Separate nodes make the question moot.

**Nothing beats HEAD's 317.** Each diagnosis is mechanically right and each fix makes the table
worse. Recorded plainly because the temptation next session was to re-derive them.

- `PLAN_THE_CREW_THAT_ARRIVES` is the second time phantom-crew planning has been tried, and the first
  with the arrival model read off the env rather than guessed. It still loses. The two-stage plan
  with real units beats a one-stage plan with phantoms on every day. **The h1 replan is not a
  defect.**
- `BUILD_THEN_PLACE` first chained a PLACE onto every pinned pen, because `pen_for` names an animal
  for all of them — d0 pins eight pens against four bought animals and every one became a four-op
  node, so the crew built two pens instead of eight (`build_pasture` 8/8 -> 2/8). Budgeting the chain
  by animals that exist recovered it to 6/8 and 281 work turns, still under HEAD.
- `PLAN_TODAYS_PURCHASES` is the one interaction worth keeping: -27 with geometry off, +3 with
  geometry on. The two are not independent.

**Geometry.** `DEPOT_RING_FIRST` is **1 (ON)**, Alex's explicit call, twice reaffirmed. The prior OFF
verdict recorded above in Part 3 §21 is a money argument, and money is not the criterion here; it
was also measured with the idle top-up and crew replan still in place, against a planner that no
longer exists — this is a resolution of that entry, not a contradiction of it. On the cell criterion,
geometry ON alone costs 12 work turns against HEAD and breaks seven rows that were exact on d6
(`plant 14/14`, `water 17/17`, `harvest 2/2`, `sell 19/19`, `buy_product 9/9`, `buy_animal 2/2`).
With `PLAN_TODAYS_PURCHASES` on it is +18 instead. Shipped config is therefore geometry ON with
purchases on, 308. Not yet measured, at the time of writing, on the metric named for it: pen and
animal distance, via `scripts/where_the_walking_goes.py`. Work turns are the wrong lens for a siting
change.

**The real open item: delivery has no deadline.** Alex: "sometimes there are things which need to be
delivered to the shed so they can be sold before something can be bought like land or more animals -
that needs to be part of the plan too", and "if the money is going to be short the harvest or
fertilizer should be optimally sold early in the day." What exists: `owed_sale` (today's `sells` row
minus what is already in the shed, passed to `_solve` as `wanted=`); `FUND_THE_DAY_WHEN_SHORT`
(`_days_bill(row) > money` sets `fund=True`, harvesting first and delivering on sight instead of
batching — `_days_bill` counts animals, seeds, buys, hires and land); `cover.materialise` appending
the walk home when a job yields or the predicted hand is non-empty. What does not exist: any
ordering or deadline. `short_of_cash` is one boolean for the whole day. Nothing expresses "the
$2,000 parcel at hour 20 needs those 14 wheat in the shed and sold by hour 12" — a delivery has no
due hour, and sell-before-buy is not sequenced. On this tape it is what d4, d6, d8 and d10 turn on.

Two further named rules, also unbuilt: do not dig weeds that are not in the geometry plan
(`DIG_ONLY_IF_REPLANTING` gates on global `plants_left`, not per-tile); do not plant what cannot
finish (`_pointless_tiles` drops existing tiles, it does not refuse new ones).

**Tests added**, all in `tests/test_the_first_seven_days_match_the_plan.py`, all verified red before
the fix:

- `test_the_day_is_planned_once_and_only_at_dawn` — counts `_solve` per day.
- `test_the_dawn_plan_can_see_the_goods_the_day_is_about_to_buy` — spies the `supply` kwarg.
- `test_the_dawn_plan_offers_a_place_for_every_animal_the_day_buys` — spies the node set.

The first is red again with `PLAN_THE_CREW_THAT_ARRIVES = False`, which is the shipped setting. It
is kept because it is the statement of the goal, not a regression guard for it.

**Evening status (from the handoff).**

```
python -u -m pytest tests/test_each_day_matches_the_tape.py -q          # one test per day
python -u scripts/breakdown.py --module schedule_agent --days 7  # the table
```

```
d0  PASSES
d1  PASSES
d2  sell 4/5   money 561/659
d3  sell 6/5
d4  care 6/7   sell 30/32   money 126/1311   owned 50/25
d5  sell 28/26  money 860/1855  owned 50/25  pen 9/8
d6  plant 13/14  water 16/17  feed 7/8  care 7/8  place 0/1  sell 17/19
    buy_product 6/9  money 1481/2565  owned 50/25  pen 9/8
```

`d0-d6 work 334/339` at the peak; `329` as shipped with the care arm off. It was **274** when this
session's planner work began. d2's `sell 4/5` and d3's `6/5` are one unit sliding a day and
reconcile — d3's money is exact.

**The two biggest single fixes, both from watching rather than reasoning.**

- The feed was drawn twice per pen. `DRAWN` contains FEED whose item IS "WHEAT", so once the FEED
  sat on the placement node `PLACE_DRAWS_FEED` added a second unit for a feed that eats one. A hand
  sat at the shed hoovering the drip while another placed cows empty-handed.
- Hands walked over hungry animals carrying eight wheat. The route is a visit order and `_live_ops`
  is consulted at stops only. `underfoot()` in the tour walker now feeds the ground a hand is
  standing on, out of surplus, from both the depot and travel branches.

**THE TAPE COLUMN IS NOT SEB'S GAME — this cost half a session.** `breakdown.py` replays Seb's
actions on seed 11 with weeds 0.0. The replay's own `configuration` records `seed: None` and
`weedSpawnChance: 0.005`, so he never played this board. Consequence: `tiles 50/25` on d4 is not our
defect. Seb's own replay shows his tiles going 25 -> 50 at d4 h23; he buys that parcel, and on our
board his plan cannot pay for it. We match his real play and the tape column is the artifact. The
money column from d4 onward inherits it, so `d10 2203/6397` measures nothing clean. Before treating
any tape row as a target, check the raw replay: `data/seed_scripts/top_guys/90494364.json` holds
both the actions and the observations.

**Open, in the order to take them (as of the handoff).**

1. d6 is the worst real day: `place 0/1`, `plant 13/14`, `water 16/17`, `buy_product 6/9`,
   `feed 7/8`. It is the last day before the tape's own economy diverges, so it is worth more than
   d4's single care.
2. d4 `care 6/7`. One care. `CARE_WHAT_YOU_STAND_ON` buys it and spends nine others — measured,
   shipped OFF, test xfail(strict). A rule that fires only where the hand has slack is a different
   arm and has not been tried.
3. The closing shed trip is uncharged, so a hand can end the day in the far corner holding produce
   the row wants. Four fixes tried, all null or net-negative; the working version needs a per-tour
   reserve, not a per-day one.
4. Label the tape column in `breakdown.py` for what it is. Every conclusion from it inherits the
   caveat above.
5. Never built: don't dig weeds outside the geometry plan (`DIG_ONLY_IF_REPLANTING` gates on global
   `plants_left`, not per-tile); don't plant what cannot finish before season end (`_pointless_tiles`
   drops existing tiles, it does not refuse new ones).

Everything else that was in the CLI task list at the time became `OPEN-CLI` in `REGISTER.md`.

**Measured nulls — do not re-derive these.**

- `RESERVATION_SLIP` 0.10 -> 0: whole grid byte-identical. The sell bunching is delivery, not the
  cap.
- `CHAIN_OPS`: byte-identical. `COVER_PLANNER = True`, so `router.plan_routes` never runs.
- "deliver a finished row" and "deliver a finished product" in `materialise` rule 2: never fire. Rule
  2 inserts before a later job and the fertilizer is collected by the tour's last jobs.
- `SELL_ROW_PRODUCE_GOES_FIRST` (drop the `fund` gate on `Job.funds`): no change.
- `END_NEAR_THE_SHED` ranking tie-break: null on d4, a real loss on d6.
- Phantom-crew planning without the other three fixes: 317 -> 273. It only pays as a set.

**Housekeeping.** Five `while pgrep -f pytest; do sleep N; done` waiters from earlier sessions were
found spinning forever and killed — never write one. `data/logs` and `data/seed_scripts` are
excluded in `.idea/kaggriculture.iml`; do not delete `data/logs` — it is gitignored, so deletion is
permanent, and at the time 92 log paths were cited as evidence in 84 files. `.claude/` and `.idea/`
are both gitignored, so the skill and the exclusion are on disk only.

## 26. Parity restored against `kaggle-environments` 1.32.6

Folded in from `docs/parity_restored_on_1326_2026-08-09.md`.

2026-08-09. Both simulators exact against the installed environment again. The eight failures
handed to this session closed, and eleven others already red went green with them.

`python3 -c "import kaggle_environments; print(kaggle_environments.__version__)"` -> **1.32.6**, and
`reference/kaggriculture.py` is byte-identical to the installed
`kaggle_environments/envs/kaggriculture/kaggriculture.py`. The reference in this repo was ground
truth and already current; what had not moved was the simulator.

**The verdict.** It was the encoding of 1.32.2 rules, as suspected — but verified rather than
assumed, and the list is longer than the town drain. Diffing the 1.32.2 env source
(`git show 909e5f6^:reference/kaggriculture.py`) against 1.32.6 gives a closed list: everything in
that diff is either a comment or one of six behavioural changes. Two of the six
(`townCenterSellInterval` 12 -> 24, and the deletion of `TOWN_CENTER_DEMAND_SCHEDULE`) had already
been handled in `kagg/sim/town.py` by commit 909e5f6. The other four had not, and they are what this
session fixed.

| # | Rule in 1.32.6 | Was | Site |
|---|---|---|---|
| 1 | Movement onto a `LOCKED` tile is allowed | blocked | `ops.move`, `jax_sim` movement |
| 2 | `DROP`/`PICKUP`/`PLACE` resolve **before** the `LOCKED` guard | after | `ops.shed_adjacent`, `jax_sim` `on_shed` |
| 3 | `BUY_PRODUCT`/`BUY_ANIMAL` fail once the shed is full | uncapped | `game._commit`, `jax_sim` market commit |
| 4 | Shops unlock **with replacement**, capped at `MAX_SHOP_INSTANCES` | all distinct | `town.drain_at`, `Game.unlocked_shops`, `jax_sim` unlock arrays, `parity.run_reference` |

Every one was measured against the installed environment before a line of simulator changed, and
each has a test that goes red when the fix is backed out (`tests/test_parity_1326_rules.py`).

**Why #4 mattered most.** The env's own comment reads like an edge case: "`unlocked_shops` may list
the same shop more than once (shops are drawn with replacement); each instance consumes
independently." It is not an edge case: eight instances drawn from eight shops are all distinct with
probability 8!/8⁸ = **0.24%**, so a duplicate is the norm. Every seed the parity gate uses duplicates
— 700, 701, 800, 1500, 1501, 1502 — and `observe_unlocks(11)` opens YARN_STORE on days 12, 15 and
21. A simulator holding unlocks as a set of booleans therefore under-drains essentially every game.

This had spread further than the simulator. `kagg/economics/market.py` already modelled instances
correctly, which is why
`tests/test_sim_town.py::test_drain_matches_the_validated_economics_model_at_every_step` had been
failing at "step 360, WOOL: 3 != 5" — three being one YARN_STORE plus the centre, five being two
YARN_STOREs plus the centre. The bool-mask assumption was in the simulator and its test helper, not
the economics model.

`Game.unlocked_shops` is now instance counts rather than flags, recomputed each step rather than
accumulated. `jax_sim` moved from a shop-indexed `unlock_day [B, N_SHOPS]` — a shape that cannot
express a duplicate at all — to an instance-indexed pair, `unlock_day` and `unlock_shop`, each
`[B, MAX_INSTANCES]`. All existing input forms still work: a `{day: shop}` dict, the new
`{day: [shop, ...]}` list, and a `[B, N_SHOPS]` day array from `random_unlock_days` / `boards.unlock_array`.

**The harness could not see it — the recurring lesson.** `parity.run_reference` recorded unlocks as
`unlocks.setdefault(shop, day)`, keyed by shop name, which collapses a duplicate before the
simulator is ever asked about it — the gate handed our sim half the drain and then compared the two.
It now records `day -> [shop names appended that day]`, matching the env's actual list.

This failure mode recurred twice in this session alone. The second instance would otherwise have
shipped untested: rule #3 (buying stops at `shedCapacity`) is unreachable by the existing 719-step
scripts. Measured across all five, the shed peaks at **8 to 11 items in a 100-item shed** — a
simulator ignoring the rule entirely passes every one of them. Confirmed directly: backing rule #3
out leaves all five original full-length tests green. `random_script` gained `buy_rate` / `buy_max`,
`run_reference` / `run_sim` gained `starting_money`, and `tests/test_sim_parity.py` gained
`test_full_length_episode_against_a_full_shed_is_exact`, which holds both farms at the 100-item cap
for **1,429 of 1,438 player-steps**. Backing rule #3 out now fails exactly those two cases and
nothing else — proof the gate works and proof the old gate never could.

**The tape fixture was testing a game that no longer exists.** `tests/test_tape_parity.py` had
flagged the numpy sim as failing, with a warning not to chase JAX while its reference was wrong. It
was not a numpy bug: the episode's own recorded configuration says
`data/episodes/89873723.json -> "module_version": "1.32.3", "townCenterSellInterval": 12`. The
fixture pinned `EXPECTED_BANK = 147_178`, the bank that action tape produced on the ladder that
recorded it. Driving the identical tape into the installed environment banks **$92,313**. The
recorded number is not reachable under 1.32.6, and a simulator that reproduced it today would be
wrong. Corroborating detail: that recording opens eight distinct shops, the 0.24% event under 1.32.6
and the guaranteed outcome under 1.32.2.

The test now gates the claim it always actually made — given these actions, our simulator equals the
environment — by replaying the tape into the installed env and comparing against that, rather than a
stale recording. Costs about four seconds and is version-proof. Result: exact, all 719 turns, both
simulators, $92,313. `test_the_recorded_bank_is_a_1_32_3_number_and_is_not_the_target` was added so
nobody restores the old constant; it goes red if a future release ever makes $147,178 reachable
again, which would itself be the correct signal that the town rebalance had been reverted.

One trap re-confirmed: the unlock schedule must be read out of the env run being compared against,
never hard-coded. `_spawn_weeds` consumes a draw per empty tile before `rng.choice` picks the shop,
so the same seed with weeds on and off produces different shops.

**Verification — each fix reverted individually, per CLAUDE.md.** None covered by nothing:

| Fix reverted | Goes red |
|---|---|
| 1 movement onto LOCKED | its own test + 8 full-length parity cases |
| 2 shed ops on a LOCKED tile | its own test + 7 full-length parity cases |
| 3 shed capacity on buys | its own test + only the 2 new full-shed cases |
| 4 duplicate shop instances | its own test + 7 parity cases + the tape test |

Rule #2's test passed before rule #1 was fixed, for a confounded reason: the farmer could not walk
onto the locked tile, so `PICKUP` ran from the unlocked one and succeeded. It only discriminates once
movement is correct.

Suite movement, diffed against a copy of the working tree with only these files reverted: **slow
suite 24 failed -> 13 failed, zero regressions. Fast suite 26 failed -> 21 failed, one regression**
(below).

**What was still red, and why none of it was a parity divergence.**

1. `test_locked_chain_relocates::test_two_different_far_tiles_are_not_the_same_farm` — the one
   regression, and a real finding for issue #26, deliberately not touched here. That module
   documents a search-layer bug: a chain aimed at ground the farm never unlocks walks to the border,
   stops, and builds somewhere else, so the plan is fiction. Its docstring said `ops.py:86` ignores a
   move onto a LOCKED tile — true before this session, false after. Under 1.32.6 the unit walks onto
   the locked tile and the tile ops no-op there, so no pen is built at all, which fixes the
   relocation half of #26 for free
   (`test_a_pen_on_unaffordable_ground_does_not_appear_somewhere_else` now passes,
   `test_the_border_tile_is_where_it_actually_lands` self-skips — "relocation no longer happens; this
   mechanism test has served its purpose"). But it makes the degeneracy half worse: every unreachable
   SE tile used to collapse onto a different border row, and now all collapse onto the identical
   empty farm, so the beam cannot tell any of them apart. The remedy — reject the chain in `decode()`
   so it reads as `skipped` — is a search decision, not a simulator one.
2. Eight `test_shop_unlocks.py` failures, stale 1.32.2 price literals. Closed during this session by
   concurrent work; green as of `560b95b`. The measured table against 1.32.6, worth checking docs
   against:

| product | frozen town | test pins | reference schedule | test pins |
|---|---|---|---|---|
| WHEAT | 30 | 37 | 49 | 51 |
| TOMATO | 64 | 77 | 85 | 98 |
| EGG | 52 | 58 | 69 | 76 |
| MILK | 208 | 263 | 315 | 340 |
| STRAWBERRY | 166 | 219 | 274 | 297 |

   `test_frozen_town_baseline_is_what_the_bug_was_measured_at` documents itself as "Guard. If this
   moves, every figure quoted in the bug report is stale." Going red was the signal it exists to
   raise; the figures quoted in other docs at the time were still the 1.32.2 ones and needed
   re-checking against this table — a separate piece of work, not done as part of this session.
3. The remaining ~13 failures (router, planner, feed-reserve, water-cadence, stock rows) were
   pre-existing and untouched, in the search layer another agent was working in at the time.

**Collateral fixed on the way.** Adding `unlock_shop` to the JAX `State` broke two constructors, both
corrected: `kagg/rl/adapter.py` (missing field, a hard `TypeError`), and `kagg/rl/curriculum.py`
(three sites — one a `TypeError`, the other two would have been silent: `_replace(unlock_day=...)`
without its companion would have inherited the adapter's all-zero array and read as eight instances
of shop 0, and the shuffle permuted `unlock_day` without `unlock_shop`, pairing one game's days with
another's shops). `jax_sim.shop_ids_for_days(batch)` exists so that pairing is explicit at the call
site rather than implicit, because both failures were wrong drains, not crashes. One dtype trap:
`jnp.sum` with x64 enabled accumulates int32 into int64, and `rollout`'s `lax.scan` rejects a carry
whose dtype changed; `_drain` now passes `dtype=_I` explicitly.

## 27. `run_arena` drove one agent object through every match (Task #54)

Folded in from `docs/arena_state_leak_2026-08-09.md`.

Date 2026-08-09. Base commit `b85ac19` (`shaping-potential`). Environment `kaggle-environments`
1.32.6, macOS, Python 3.12.

**The one-line finding.** `run_arena` took an agent value and passed that same object into every job
— every seed, both seatings — while `kagg.search.schedule_agent.make_agent` builds its `state` dict
once in the closure. A finished season therefore walked into the next match and killed the agent
outright. `run_arena` now takes an `AgentFactory` and refuses a bare callable.

**What was and was not affected.** The hypothesis handed to this task named `scripts/gate_pool.py`
(the submission gate) as affected. It is not, and neither is `scripts/arena_gate.py`. Both were
checked in source and by measurement.

| Path | Verdict | Why |
|---|---|---|
| `docs/fable_market_shape_2026-08-09.md` §4 | **CONTAMINATED** | §4 states its own harness: "`kagg.arena.run_arena`, workers=1 (closures from `make_agent` …)". This is the only measurement found that put a `make_agent` closure through `run_arena`. |
| `scripts/gate_pool.py` | clean | Calls `kagg.arena.pool.evaluate`, not `run_arena`. `pool._play` builds the candidate inside the job. The candidate is the path `submission/main.py`, and `kaggle_environments.agent.build_agent` re-`exec`s a path into a fresh namespace for each `Agent`, one `Agent` per `env.run`. |
| `submission/main.py` | clean | Already rebuilds its agent at `day == 0 and hour == 0`, with a docstring saying why: "a process that plays more than one episode does not carry a season of pins and pen reservations into the next one." Fix (b) shipped in the artifact and was never applied to the harness. |
| `scripts/arena_gate.py` | clean, but by luck | Did pass live callables to `run_arena`. Its own agent is a pure tape replay keyed on `obs["step"]`, and its opponents are the module-level `kagg.agents.*.agent` functions, all stateless — nothing to carry. Updated to the factory API anyway. |
| `scripts/bench_agents.py`, `bench_arena.py`, `build_script_submission.py` | clean | Pass names and paths only. |
| `scripts/confirm_late_sell_bias.py` | clean by construction | Walks `run_match` itself and rebuilds the agent per match. Its docstring already documented the trap in both directions. |

**The pool opponents are stateless — the bias has a known direction.** `heuristic.agent`,
`rancher.agent` and `contrarian.agent` are pure functions of the observation. Measured, three
consecutive matches through one object, seed 40 vs `pass`:

```
heuristic    [33188.0, 33188.0, 33188.0]
rancher      [37121.0, 37121.0, 37121.0]
contrarian   [33163.0, 33163.0, 33163.0]
```

`heuristic.make_agent` only binds a parameter dict; there is no per-game state to carry. So only our
side was ever contaminated, and only downward — a carried season makes our agent bank less, never
more. Every contaminated number understates us.

**The measurement.**

Raw damage: one `make_agent(thin, me=0)` object, three matches, seed 40 vs `pass`:

```
game 1   $114,028    13.7s
game 2         $0     1.0s
game 3         $0     0.9s
```

Not a degradation — the second game dies in the first seconds (1.0s against 13.7s) and banks $0,
below the $3,000 opening stake, so the agent is being invalidated rather than playing badly.

Through `run_arena`, seat-agnostic wrapper (the shape `submission/main.py` had before its day-0
rebuild):

```
seeds=[40]        2 games    mean $115,237
seeds=[40, 40]    4 games    mean  $57,618
```

Exactly half — matches three and four bank $0. This is the assertion in
`tests/test_arena_state_leak.py::test_run_arena_does_not_carry_a_season_into_the_next_match`;
comparing `[S]` against `[S, S]` rather than against a single `run_match` makes the seat effect
cancel, so only carried state can move the number.

Fable's §4 configuration, re-run both ways: seeds 20-27, both seatings,
`heuristic`/`rancher`/`contrarian`, `LATE_SELL_BIAS` at its default `False`, 48 games per arm.
`shared` reproduces the pre-fix `run_arena` — one `make_agent` object per opponent, driven through
all 16 of its matches. `fresh` builds one agent per match with `me` set to the seat it actually
occupies, matching `scripts/confirm_late_sell_bias.py`. Logs: `data/logs/task54_damage_shared.log`,
`data/logs/task54_damage_fresh.log`.

```
arm       opponent          mean $   win rate
shared    heuristic         4,534       6.2%
shared    rancher           6,001       6.2%
shared    contrarian        6,788       6.2%
shared    POOL              5,774       6.2%

fresh     heuristic        97,101     100.0%
fresh     rancher         102,850     100.0%
fresh     contrarian      108,707     100.0%
fresh     POOL            102,886     100.0%
```

**$5,774 against $102,886, and 6.2% against 100%.** 17.8x on money, and a pool the harness reported
as a near-shutout against us is in fact a clean sweep by us. 6.2% is 1 win in 16 — the first,
unswapped, still-clean match of each opponent, and nothing else.

For comparison, `docs/fable_market_shape_2026-08-09.md` §4 published $16,146 / 14.6% for this
configuration, and $24,535 / 27.1% with `LATE_SELL_BIAS` on — both sit between the two arms above.
This does not reproduce Fable's exact figures, and no attempt was made to: §4 does not record the
precise call, so `shared` is the pre-fix `run_arena` semantics rather than a byte-reconstruction of
that run. It reproduces the failure mode, at the same order of magnitude and in the same direction.

The `shared` arm conflates two defects and cannot separate them: a `make_agent(schedule, me=0)`
object placed in seat 1 by `run_arena`'s swap also believes it is still seat 0 (see below), so half
of `shared`'s games are wrong for that reason alone. The 6.2% win rate is 1 win in 16 — exactly the
first, unswapped, still-clean match — what both defects together predict.

**The shipped artifact, measured properly.** `scripts/gate_pool.py --seeds 6 --workers 6`,
`submission/main.py` against the 9-member `COMPETITIVE` pool, seeds 700-705, both seatings, weeds
ON, 108 games:

```
win 94.4% (draw 0.0%) mean $108,180

opponent          win       ours
mirror           50%     59,271
wheat_only      100%    137,876
melon_heavy     100%    111,038
strawberry      100%     86,213
cow_heavy       100%    102,514
carrot_25       100%    118,715
small_farm      100%    124,491
straw_small     100%    123,299
contrarian      100%    110,199
```

This is not a new number and it is not "the fix helped" — `gate_pool.py` was never on the broken
path. It answers §4.1 of `fable_market_shape_2026-08-09.md`, which spent a section on the "94.4% vs
14.6% question" and resolved it as "not the same measurement" — different pool composition,
different era, `mirror` and `starter` inflating the high figure. That explanation is partly right and
misses the larger term: the 14.6% came off a harness that killed our agent in 15 of every 16 games.
The 94.4% is the honest one, and the fresh re-run above reaches 100% against the exact three
opponents §4 used, on §4's own seeds. There was no pool-composition gap left to explain. **The
shipped agent's honest score was, and always had been, 94.4% / $108,180 against the 9-member pool on
seeds 700-705.** The submission was never gated on contaminated numbers; what was contaminated was
the market-shape investigation running beside it.

**The fix**, in `kagg/arena/arena.py`:

- `AgentFactory(build, *args, **kwargs)` — a picklable "build me a fresh agent" instruction, invoked
  once per match, inside the worker.
- `run_match` resolves a factory but still accepts a bare callable: one match cannot leak into a next
  one that does not exist, and `confirm_late_sell_bias.py` depends on that.
- `run_arena` resolves factories and **raises `TypeError` on a bare callable**. Chosen over silently
  reusing it — there is no way to rebuild an agent from an instance of one, and from outside a
  stateless callable is indistinguishable from a stateful one. The module docstring already claimed
  "Callables are deliberately not supported"; now it is enforced rather than asserted.

This also closes the `workers=1` constraint. `scripts/arena_gate.py` had pinned `--workers 1` because
`ProcessPoolExecutor` on macOS spawns rather than forks, so its `_GENOME` global arrived unset and
`make_agent` closures raised "Can't pickle local object." A factory ships the recipe — a module-level
function plus picklable arguments — and builds on the far side. `test_a_factory_survives_the_worker_pool`
pins it.

**Tests**, in `tests/test_arena_state_leak.py` (added to `SLOW_MODULES` in `tests/conftest.py`, so
`-m slow`):

| Test | What it pins |
|---|---|
| `test_run_arena_gives_each_match_its_own_agent` | Two matches, two agent objects, one game each. |
| `test_a_factory_survives_the_worker_pool` | `workers=2` with an in-process build. |
| `test_run_arena_refuses_a_live_agent` | The trap is loud, not merely discouraged. |
| `test_run_arena_does_not_carry_a_season_into_the_next_match` | The money, on the real schedule agent. |
| `test_a_path_spec_was_never_contaminated` | The shipped artifact's freshness, so a regression in either mechanism shows. |

**The revert check.** Per CLAUDE.md — three of five past fixes were, at first, covered by nothing.
With `_resolve` returning its argument unchanged and `_check_spec`'s guard forced to `False`, all
three of the original tests go red:

```
FAILED test_run_arena_gives_each_match_its_own_agent           - 0 agents built for 2 matches
FAILED test_run_arena_refuses_a_live_agent                     - DID NOT RAISE <class 'TypeError'>
FAILED test_run_arena_does_not_carry_a_season_into_the_next_match
        AssertionError: the agent banked $3,000; it did not play a season, so the comparison
        below would be vacuous
```

The revert check earned its keep immediately. The money test as first written would have PASSED with
the fix backed out: an unresolved `AgentFactory` is called as `factory(observation, configuration)`,
dies, and both arms report the $3,000 opening stake — equal, and meaningless. The liveness guard
(`assert once.mean_money[0] > 3000.0`) exists only because the revert was actually performed. A green
suite after a fix says the fix broke nothing, not that anything checks it.

**A second defect, not fixed here.** `run_arena`'s seat swap is wrong for any agent that has its
seat baked in. `make_agent(schedule, me=0)` placed in seat 1 by the swap still believes it is seat 0.
`confirm_late_sell_bias.py` handles it (`_ours(..., 1 if swapped else 0)`); `run_arena` cannot,
because it has no way to tell the agent which seat it is in. `submission/main.py` is immune because
it reads `obs["player"]`. Anything else driven through `run_arena` with a baked seat is wrong in half
its games independently of this bug. Not in scope for #54; flagged rather than chased.

**What to re-read.** `docs/fable_market_shape_2026-08-09.md` §4, §4.1 and §5 rest on the contaminated
harness. The direction of `LATE_SELL_BIAS` may well survive — `scripts/confirm_late_sell_bias.py`
re-measures it on the honest path and on a disjoint seed block — but the magnitudes ($16,146 ->
$24,535, 14.6% -> 27.1%) are measured on games our agent mostly did not play. §4.1's resolution of
the "94.4% vs 14.6% question" should be reopened.

**Suite status.** Full suite on this worktree, `pytest -m ''`: 32 failed, 1077 passed, 202 skipped,
14 xfailed, 26 errors. All 26 errors are `FileNotFoundError` on gitignored `data/` fixtures absent
from a fresh worktree. The 32 failures were pre-existing on `b85ac19` — 21 in `tests/test_router.py`,
whose fix was uncommitted work in the main tree at the time — and none of the failing modules import
`kagg.arena`. Arena suites specifically: `tests/test_arena.py` + `tests/test_arena_state_leak.py`, 10
passed.

`scripts/arena_gate.py --seeds 2 --slots 6 --workers 4` was run as a live check that the factory
lifts the `workers=1` constraint in the real script: it banks $14,708 against `starter` and $7,888
against `heuristic`, rather than the flat $3,000 / 0.000 the spawn failure used to produce. Log:
`data/logs/task54_arena_gate_workers.log`.

## 28. Handoff, 2026-08-15 — the shipped plan changed and the precomputed routes did not follow

Folded in from `docs/handoff_2026-08-15.md`.

Built only from measured results at the time. Everything asserted and later corrected, and
everything still unmeasured as of this handoff, was tracked in `RETRACTIONS.md`.

**The state of the ladder.**

```
2026-08-13 03:39   1890.2   LATE_SEASON_PAIR + re-solved d26-d29 routes
2026-08-13 05:21   1428.4   carrot reaches the market (SELLABLE fix) + pins + wool rule
2026-08-15 02:50   1030.0   d8 sheep placed + melon yields to a melon-heavy opponent
```

Two submissions in a row went backwards. The instruction at the time: do not submit again until the
route regeneration and the melon A/B have both reported.

**1. The precomputed routes were solved for a plan no longer played.** `kagg/search/solved_days.py`
was solved on seed 11 against the victor tape. `kagg/plan.py:SHIPPED_PLAN` had been kawashigi since
2026-08-13. Measured, `--tape kawashigi --days 30`:

```
precomputed ON (shipped)     d29 $139,025    work 2979  move 3036  idle 987
PRECOMPUTED_ROUTES = {}      d29 $118,660    work 2895  move 3150  idle 957
```

`cover.PRECOMPUTED_MISSES` — only **143 of 571 stops** were seated:

```
day    stops   skipped   SEATED   % used
 12       50        37       13      26%
 16       64        46       18      28%
 18       69        54       15      22%
 23       74        65        9      12%
 24       58        45       13      22%
 25       59        41       18      31%
 26       60        39       21      35%
 27       61        44       17      28%
 28       51        41       10      20%
 29       25        16        9      36%
tot      571       428      143      25%
```

A quarter of a stale artifact was worth $20,365, because the board is identical in every game:
`_initial_tile(x, y, board_size)` returns `None if quadrant == "NW" else "LOCKED"`, a pure function
of coordinates, and the env's only two `random.Random` calls drive the weed spawn and the shop draw.
What a different plan moves is the job pool — where pens were sited, what was planted where — not
the map.

Action taken: `scripts/resolve_days.py` re-solves d12-d29 in day order against the shipped plan. Day
order is a correctness requirement, since each solved day changes the next day's board, so the
driver installs each route before dumping the next fixture. Every day so far seated 100% with zero
uncovered. **Not yet verified at the time: that this closes the gap.** Measure with
`PYTHONPATH=. python -u scripts/breakdown.py --days 30` and watch `harvest` toward 375, `place` back
to ~35, `dig` down toward 25.

**2. The harvest gap is coverage, not job creation.** Over d19-d29 the board offers 335 HARVEST jobs.
We take 247. The tape takes 280.

```
 day  OFFERED   ours   tape  unseated
  20       26     11     16        15
  22       37     17     19        20
  24       32     19     26        13
  28       37     24     32        13
 tot      335    247    280        88
```

88 offered harvests go unseated; 33 of them would match him. The worst days are the ones that never
had a route at all: the old precomputed set was 12, 16, 18, 23-29, so d20, d21 and d22 ran pure
greedy and alone account for 44 of the 88. Nothing needed adding upstream in `build_nodes`. Routing
alone, with only the stale quarter applying, already moved harvest 276 -> 335 (+59).

**3. Watering is not the problem.**

```
water d9-d29    ours 798 / tape 795
```

We water three more times than he does. The per-day cells that look short (d10 25/32, d12 30/40) are
cancelled by days we over-water (d13 47/41, d23 41/31). A preventive-watering rule built against the
opposite belief measured **−$1,051** and killed one extra tile by displacing a rescue. Full write-up:
`docs/fable_watering_post_d8_2026-08-15.md`.

Also ruled out with numbers, in `docs/fable_production_decay_d19_2026-08-15.md`: we dig no crops he
keeps (zero live-crop digs either side), fertilize is not stealing harvest turns (1.85 vs his 1.97
bonus units per op), and cap discards are zero on both farms across all 30 days. The surviving
mechanism is standing-producer attrition: only **13 of our strawberry tiles complete their lifecycle
against his 31**.

**4. Three flags confirmed as losses on the ladder field.** 12 recorded opponents, both seatings,
env-default weeds, seeds 1300-1305:

```
HERD_GEESE             0 → 69.4% win, +$15,502 margin
                       2 → 38.9% win,  −$2,432
                       4 → 41.7% win,  −$1,338
WHEAT_TILES_TO_CARROT  0 → 69.4%   8 → 61.1%   16 → 63.9%   28 → 66.0%
WHEAT_TILES_TO_TOMATO  0 → 69.4%   8 → 61.1%   16 → 63.9%   28 → 68.1%
```

Carrot raises mean money (88,810 -> 90,080) while lowering win rate. On an Elo ladder that is
strictly worse. All three stayed at 0.

**5. One agent, one name (commit `fa96ace`).** `schedule_agent.py` was a dead 3,610-line
predecessor; the shipped agent was `schedule_agent_1455mh.py`, which the bundler renamed to
`kagg.search.schedule_agent`. **75 scripts imported the dead one**, including `probe_sell.py`,
`probe_shed_target.py` and `replay_the_new_sell_rule.py` — all three sell diagnostics. Any conclusion
drawn from those scripts before this commit describes a different agent. 22,777 lines deleted. Build
gate passed: `env.run` $141,449 against starter's $3,660.

**Commits at the time of this handoff.**

```
fa96ace  One agent, under the name it actually ships as
bebf5ae  The grid compares against the plan we ship, not the one we used to
d56d1be  Keep the rules that bind, move the record that does not
```

**Next, in order, as of the handoff.**

1. Finish the regeneration, rebuild, run the 30-day grid. Judge on `harvest`, `place`, `dig`.
2. Read the melon A/B (`data/logs/sweep2_melon_2026-08-15.log` on the training box).
3. Check `PRECOMPUTED_MISSES` against ladder opponents, not just the tape — the regenerated routes
   are solved on seed 11 and could be overfit to it.
4. Only then submit.
