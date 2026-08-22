# Animals and the herd

Merged 2026-08-22 from 5 source files. Every source file is archived, unedited, at
`docs/history/<filename>`.
This doc covers the herd (cow/sheep/goose) mix question, the geese verdict, and pen-placement
geometry.
Read `docs/geese_verdict_status_2026-08-22.md` for the current, live status of the geese question —
it postdates every file merged here and is not touched by this pass.

The geese question has been re-derived at least six times in this project.
The two files below are the last two full derivations before the 2026-08-22 status file.
Two more derivations of the same question live inside `docs/market_and_economics.md`
(`the_market_is_the_late_season_2026-08-13.md` and `the_mix_and_the_routes_are_one_artifact_2026-08-19.md`)
and are not repeated here — read them there if the two derivations below are not enough.

## 1. Geese: the money verdict (2026-08-15)

source: `the_goose_is_insurance_2026-08-15.md`, 2026-08-15.
Alex's own instruction: "do the math, not an experiment."
Computed from `reference/kaggriculture.py` directly, no agent simulation.
Opponent volumes are read off three ladder replays downloaded the same day.

**Why this was reopened.** `HERD_GEESE` was measured 2026-08-11/12 as a disaster: 0 birds won 69.4%,
2 birds won 38.9%.
That verdict is dead: commit `c99a8a5` fixed `SELLABLE` on 2026-08-13, two days later.
Before the fix, `SELLABLE` listed six of the env's nine products, and CARROT, TOMATO and EGG could
not be sold at all.
So the 08-11/12 sweep measured geese producing eggs that could never become money — pure cost, zero
revenue, on any flag, on any day.
It is not evidence about geese.
This is the third time in this project a mechanic-level negative turned out to be an artifact of our
own code, not the mechanic (`project_kaggriculture_animals_verdict`, per project memory).

**Production model**, stepped through `_daily_refresh_animals` (`reference/kaggriculture.py:805`),
one animal placed d5, fed and cared every day, harvested as it fills:

| animal | cost | structure | first_yield | interval | max_held | product | units/season (this doc) |
|---|---|---|---:|---:|---:|---|---:|
| GOOSE | $300 | COOP | 4 | 1 | 4 | EGG | 46 |
| COW | $400 | PASTURE | 8 | 2 | 6 | MILK | 30 |
| SHEEP | $500 | PASTURE | 6 | 3 | 6 | WOOL | 30 |

Validated against a real game: predicts 30 milk/cow, game `93239838` has 9 cows producing ~290 milk
— 32/cow, close enough to trust.
The goose is the cheapest animal, starts 4 days earlier than a cow, and produces every day against
the cow's every-other and the sheep's every-third.

**Revenue, opponent sharing the same book.** An earlier calculation priced our units into an empty
book and got milk at $155/unit — contradicted by every real game, where milk closes at $1-$5.
Corrected opponent season volumes at first pass: MILK 250-410, WOOL ~250, EGG 0 (ours too).

> **RETRACTED inside this same file, 2026-08-15.** Those two opponent volumes are summed sell
> OFFERS, not fills — the agent re-posts an unfilled order every turn, inflating the true number by
> roughly 6x. Measured against market inventory instead: across 26 replays a no-yarn board ends at
> `inv - I0 = +59` units of wool for BOTH herds combined; real wool supply is ~8 units per sheep per
> season, so two full herds move ~60-70 units, not 500. Milk re-checked the same way is ~200-240
> units per seat per season, realised at $37-$78/unit on a milk-poor board and $231 on a milk-rich
> one. Every number in this file's §2 that uses "theirs" is built on the wrong (offer-based) volume
> and the ranking needed re-deriving from fills. See `feedback_offers_are_not_fills` (project
> memory) — this file is the example of the mistake it warns about.

Six animals, net of purchase cost, computed on the (retracted) offer-based opponent volumes:

| | our units | their units (retracted basis) | net, 2 shops draining | net, 0 shops draining |
|---|---|---|---:|---:|
| GOOSE | 276 EGG | 0 | $11,270 | $9,818 |
| COW | 180 MILK | 300 | $10,392 | $556 |
| SHEEP | 180 WOOL | 250 | $32,910 | $1,174 |

Goose loses 11% of net revenue when its (nonexistent) drain disappears; cow loses 77%; sheep loses
88% — this asymmetry is the part of the finding that survives the retraction, because it is about
the SHAPE of each book's demand curve, not the disputed volume numbers.

**Expectation over the real shop draw.** Shops unlock 1-per-3-days on days 3..24 — 8 draws, uniform
with replacement over 8 shop types. Instances carrying a product is `Binomial(8, m/8)` for `m`
carrier types:

| animal | product | carrier types | P(zero carriers) | E[revenue] | worst-10% | net E |
|---|---|---:|---:|---:|---:|---:|
| GOOSE | EGG | 2 | 10.0% | $12,678 | $11,618 | $10,878 |
| COW | MILK | 3 | 2.3% | $21,278 | $5,575 | $18,878 |
| SHEEP | WOOL | 1 | 34.4% | $22,590 | $4,174 | $19,590 |

**On this file's own (later-retracted) expectation table, a cow or sheep beats a goose by about
$8,000 per six animals** — the file states plainly: "the math does NOT say switch to geese. Anyone
quoting this doc for 'geese are better' is misreading it."
What DOES follow: the goose's worst-decile revenue is more than double either alternative's — it is
the only animal whose floor is close to its mean, because EGG's price curve is `log` with
`above_target 0.2`, effectively undentable (needs ~2 million units above I0 to halve the price — same
class as WHEAT), and because opponents run fixed 720-turn scripts that cannot start producing eggs
in response, so the egg book stays uncontested in every game, all season, by construction.

**Caveats stated in the file:** "theirs" is three games (order-of-magnitude only, EGG=0 is
structural but MILK 300/WOOL 250 are estimates); even production spreading is assumed, so real
lumpier release likely understates the goose's tail edge; feed cost (1 wheat/animal/day) is not
netted and is roughly constant across species so it doesn't move the ranking, but makes all absolute
nets optimistic; op-cost is not charged, and the goose needs collecting more often (fills at 4
against the cow's 6).

## 2. Geese: the Elo (margin) verdict that supersedes §1 (2026-08-15)

source: `fable_geese_audit_2026-08-15.md`, 2026-08-15 — commissioned as an audit of §1's own file,
math only, no agent runs; scratch scripts `goose_audit.py`/`goose_margin.py` behind every number.

**This is the file that closes the geese question, on the objective that matters.**
Money maximisation and margin (Elo) maximisation disagree here, and margin is what the ladder pays.

**Audit findings on §1's own numbers:**
- Production: one real error, -2 eggs. §1's 46 counts a production event at the end of day 29 that
  fires for the goose (interval 1 hits every rollover) but not the cow (stops at next_day 29) or
  sheep (also 29) — corrected sellable is 44, not 46. Egg revenue recomputed at $12,094 against §1's
  $12,678 — the gap is exactly 2 eggs x 6 birds x ~$50.
- Binomial(8, m/8) model: correct. P(zero): EGG (6/8)^8 = 10.0%, MILK (5/8)^8 = 2.3%, WOOL (7/8)^8 =
  34.4% — all match §1.
- EGG undentable above I0: correct (same math as §1).
- Cow/sheep revenue in §1 is optimistic: this audit's model (same shared book, same opponent
  volumes, but pro-rata drain share and residual dumped at d29) gets COW $14,041 ($78/unit, not
  $118) and SHEEP $15,778 ($88/unit, not $125). The real seed-11 game realises milk at $69/unit (171
  sold, $12,194) — closer to this audit's lower model. Ordering (GOOSE < COW < SHEEP on money)
  survives either way; the "$8k per six" gap in §1 shrinks to $1.3-2.5k under the floor-realistic
  release, and the goose's money-corner widens to 14.8% of shop draws (median gain $2,330 over the
  best pasture alternative, p90 $5,841).

**Costs §1 left out, priced here:** feed cancels (species-identical, ~$3.2k-$6.5k for 6 animals
across a season, charged to "having animals at all" not to species choice); op cost for the goose's
extra harvest visits (12 against cow's 6, sheep's 7) is bounded at under $300 even at a panic
$50/turn, and the goose actually SAVES ops elsewhere because its undentable book makes release
timing worthless (no h05 shed race, unlike milk); coop-vs-pasture tile cost cancels across species,
differential cost of a goose is one `BUILD_COOP` op (money-free) plus an opening perturbation the
question explicitly says to ignore.

**The margin (Elo) verdict — this is what closes it.** The opponent's flow is open-loop and fixed:
MILK ~300 from d13, WOOL ~250 from d11, EGG 0. Species choice decides which book we co-occupy.
Suppression value of our 180 units on their flow (their revenue GAIN if we exit that book), over
4,000 draws:

| product | mean | p10 | p90 |
|---|---:|---:|---:|
| milk | $10,411 | $5,513 | $14,240 |
| wool | $9,275 | $2,611 | $18,145 |

Margin objective (ours minus theirs, net of purchase cost), best pick over 4,000 draws:

| species | share of draws it is margin-best |
|---|---:|
| COW | 43.6% |
| SHEEP | 55.5% |
| GOOSE | 0.9% |

**Goose margin expectation is $11,758 WORSE than cow/sheep.**
Mechanism: our marginal milk/wool units were heading for the floor anyway (small loss to us), but
their presence forces pro-rata floor-sharing onto the opponent's larger flow (large loss to them —
1.7x our volume for milk). Eggs are the mirror image: uncontested and undentable means our egg
revenue is safe AND harmless — nothing we sell there costs the opponent a dollar. **Safe-and-harmless
is exactly what a zero-sum ladder does not pay for.**
Even conditioned on the single best observable corner (no YARN_STORE and no milk carrier among the
first three shop draws visible by d9 — 12.8% of games), P(goose margin-best) is still only 7.0%.
No observable rescues it.

This reframes the older "milk is floored, we flood our own book, this is where the $11k gap is"
finding (project memory: `project_kaggriculture_milk_is_floored`): partially true for our own bank,
but the flood is SIMULTANEOUSLY holding the opponent's 300 units down. Any fix that WITHDRAWS milk
supply gifts back up to ~$10k of the opponent's revenue. The margin-aware fix is release TIMING
within the book, not exit from it.

**Policy, stated by this file:**
- **Zero geese.** Closing number: -$11,758 margin expectation per six animals; goose margin-best in
  0.9% of draws, 7.0% at its single best observable corner.
- `SHOP_ADAPT_HERD` (the cow<->sheep float) stays and is near-optimal: margin split COW 43.6% /
  SHEEP 55.5% of draws.
- The `HERD_GEESE` deletion (commit `7a88d30`) was right, but by accident — the sweep it rested on
  measured unsellable eggs (the SELLABLE bug), and the corrected arithmetic reaches the same end
  state by a different, now-verified route.

**Caveats stated in the file:** opponent volumes are 3 replays; magnitudes scale roughly linearly
with their volume and the sign is robust to +/-50% on them; EGG=0 for the opponent is structural
(fixed scripts can't respond) — this part is not a volume estimate, it's a property of the field.
Fill-sharing is modelled pro-rata within a day (the env's real interleave is per order slot, but
pro-rata is the right first-order model and applies symmetrically to both sides of every
comparison). Only 6-of-one-species portfolios are compared; mixed herds interpolate and nothing here
rewards mixing geese in.

## 3. Real ladder losses, animal books flooring (2026-08-15)

source: `three_ladder_games_2026-08-15.md`, 2026-08-15.
Read off downloaded replays only — no simulation for market numbers.
**Alex downloads losses, so nothing in this section is a win rate** (per project memory: downloaded
games are SELECTED).

Three games:

| game | result | our money | opponent | opponent money | seat | seed |
|---|---|---:|---|---:|---:|---:|
| 93237183 | WIN | $117,976 | Farfadet | — | 0 | 1158229392 |
| 93239838 | LOSS | $87,726 | mashBrian254 | — | 1 | 702042888 |
| 93242536 | LOSS | $111,741 | Alexandre008 | — | 1 | 195279982 |

All three: `weedSpawnChance 0.005`, `townCenterSellInterval 24`.

**Solver seating does not predict the result.** Replayed each game on its own `info.seed`, read
`cover.PRECOMPUTED_MISSES`:

| game | result | stops offered | skipped | seated % |
|---|---|---:|---:|---:|
| 93237183 | WIN | 1115 | 471 | 58% |
| 93239838 | LOSS | 1115 | 373 | 67% |
| 93242536 | LOSS | 1115 | 366 | 67% |
| seed 11 vs kawashigi tape (what it was solved on) | — | 1115 | 0 | 100% |

The WIN has the worst seating of the three. This closes `RETRACTIONS.md` item (b)4 ("that the
regenerated routes generalise off seed 11") — they partly do: 100% on the solving seed against
58-67% on a ladder board is the overfit, measured. On 93239838, seating decays through the season
from 82% (d12) to as low as 50% (d18), averaging 67% overall across days 12-29.

**Melon sells late because of delivery, not the sell gate.** On d10, melon sits in HANDS (not the
shed) for 7 hours while its book price holds at $272 — the sell rule only sees the shed. First offer
lands h19-h21 in both loss games. Realised on 93239838: 60 units at ~$218/unit average; selling the
same 60 units from h12 instead, walking the book down from a $272 start, would have averaged ~$250 —
a real, ~$1,900 prize, not the reason either game was lost. `SELL_AT_ONCE_DAYS = (10, 11)` (shipped
that morning) does not bind on d10 here (every sale is already past `LATE_SELL_FROM_HOUR = 16`), but
it DOES bind on d11 (93239838 sells at h00/h01 instead of waiting to h16 while the opponent walks the
book down). Open work identified: a mid-day DROP at the shed on the melon flush.

**What actually lost these games: shop draw decides what the town absorbs, and we produce the same
mix regardless.**

93239838 — town wanted eggs and strawberry, we made milk and wool:

| product | season drain | closing price | base price | status |
|---|---:|---:|---:|---|
| WHEAT | 1,253 | $49 | $25 | starved |
| STRAWBERRY | 1,253 | $268 | $120 | starved |
| EGG | 1,074 | $154 | $50 | starved, nobody produced any |
| MILK | 179 | $3 | $160 | FLOORED |
| CARROT | 179 | $46 | $35 | — |
| TOMATO | 179 | $79 | $60 | — |
| WOOL | 0 | $1 | $200 | FLOORED, no YARN_STORE all season |

Our herd both games: 9 COW, 4 SHEEP (same as the game we won). Whole-season wool on 93239838: ~130
units for $1,940 against 4 sheep at $500 each plus a season of FEED/CARE — the book floors between
d13 and d14 ($144 -> $1) and never moves again. Milk floors at d19 the same way (drain 179 against
~290 units produced). **MILK floored in all three games: $3, $5, $1.** The file states: "that is not
a seed, it is 9-10 cows."

93242536 — different draw, same failure on a different product: CARROT drained 895 units at $77
(base $35, "starved," we planted only 63 tiles); WOOL fine here (YARN_STORE drawn twice, closed
$236); MILK floored anyway at $1 despite 537 units drained.

**A cow starves on d11, and we pay $400 to replace it.** Across 18 downloaded games of this agent,
herd totals cluster at (COW,SHEEP) = (6,8) in 9 games, (10,4) in 5, (9,4) in 4 — total 14 in 14
games, 13 in 4 games. The shipped plan asks for COW 10 / SHEEP 4 = 14
(`kagg/plan.py:SHIPPED_PLAN`). The four 13-animal games are exactly the four games with an animal
escape:

| game | result | escapes | where |
|---|---|---:|---|
| 93182759 | WIN | 1 | d16 (3,5) COW |
| 93186363 | LOSS | 1 | d11 (6,4) COW |
| 93237183 | WIN | 1 | d11 (6,4) COW |
| 93239838 | LOSS | 1 | d11 (6,4) COW |

`_daily_refresh_animals` (`reference/kaggriculture.py:817`): two consecutive unfed days removes the
animal (structure stays standing) — the only way an animal is removed. Tile (6,4) in 93239838,
traced turn by turn: fed d8 h5, never fed d9, never fed d10 (`consecutive_unfed` reaches 2), gone at
d11 h00, replacement cow placed d11 h7. The original cow was placed d7 with `first_yield_day` 8 — its
first milk would have been d15. **It starved before producing a single unit**, and the "d11 herd
growth" purchase is actually re-paying $400 for a cow already owned. Same tile, same day, in 3 of 4
cases — the file states this is reproducible, not bad luck: a FEED scheduling miss on d9/d10, and
FEED is the op with the highest measured correlation to money in this project (+0.452, per project
`SUPER_IMPORTANT_READ_THIS_FIRST.md`/decision-point audits).

**What this points at, not proposed as a change here and not measured:** on 93239838 the right herd
was the floor (`HERD_FLOOR_COW = 4`, `HERD_FLOOR_SHEEP = 1`); we ran 9/4 into a town that absorbed
179 milk and 0 wool. `SHOP_ADAPT_HERD` floats the cow/sheep split but keeps the total COUNT fixed by
its own design comment ("The COUNT the schedule asks for is kept exactly; only the species is
re-decided") — the next candidate arm is the COUNT, not the split, and needs the same A/B discipline
the melon rule got. Second, cheaper thread: STRAWBERRY, CARROT, WHEAT and EGG books were starved in
every one of the three games, several closing at 2-3x base — nothing we grow is worth less for
growing more of it in those four.

## 4. Two more losses, feed fix confirmed, sheep still floored (2026-08-15)

source: `two_losses_2026-08-15b.md`, 2026-08-15.
Read off recordings only; volumes are fills (shed decreases), never offers.

| game | result | our money | opponent | opponent money | margin | seat |
|---|---|---:|---|---:|---:|---:|
| 93286476 | LOSS | $78,254 | Light | $79,216 | -$962 | 0 |
| 93285579 | LOSS | $56,805 | Mutte1904 | $63,697 | -$6,892 | 1 |

Two different losses; the file says explicitly they must not be pooled.

**The d9/d10 stranded-FEED defect (§3 above) is closed in live play.** Zero animal starvations on
our side in either game (opponent lost 1 sheep in each, both d29 h00).

**Sheep/wool problem confirmed again, but did not decide either game.** WOOL closed at the $1.00
floor in both games, zero YARN_STORE unlocked on either board, and we ran 4 sheep anyway. Price
trace on one game: d6 inventory 9,994 / $217 -> d9 10,009/$195 -> d12 10,021/$174 -> d15 10,058/$5 ->
d18 onward 10,059/$1. 65 units of net supply took wool from $217 to $1 in 9 days and it never
recovered. Not the differentiator here because BOTH seats ran the mistake (one ran 5 sheep to our
4, into the same dead book) — `SHOP_ADAPT_HERD` stays the right fix (4 sheep = $2,000 purchase plus
a season of FEED/CARE for a $1 product) but these two games are not its evidence.

**Melon: we sell faster, we simply have less of it.** In 93286476 we clear our whole melon stock at
d11-d12 (the two best prices of the season) then sell none for 17 days; the opponent dribbles theirs
out to the last day at falling prices. Our timing is better but our production is the gap: 12 melon
fills against the opponent's 62 in 93285579 — at their realised prices that's roughly $3,700, over
half the $6,892 total loss margin.

**TOMATO closed at 11x base in 93285579 and neither seat grew it**: closed $660 (base $60), drained
895 units, on the `hinge` below-curve added in 1.32.7 (steep: inventory 10,000 -> $60, 9,800 -> $84,
9,600 -> $300, 9,400 -> $900, 9,200 -> $1,884, 9,000 -> $3,252). This is the conditional play Fable
recommended elsewhere (2+ tomato-stocking shop instances visible by d12, ~26% of draws) and the
payoff here was far above base-price arithmetic. Caveat stated: the curve is this steep in both
directions, so oversupplying it collapses it fast too — sizing is not established here.

**We led on bank+field value at d28 in 93286476 and lost anyway.** Total value (bank + standing
produce + shed, both priced at live market): our lead was +$5,311 at d28, decayed to +$2,631 at d29
dawn, and finished at -$962. A second game (93281072, referenced for comparison) shows the identical
shape: +$4,503 at d28 decaying to +$872 at d29 dawn, finishing -$1,562. Neither is a d29 routing
miss — both boards finish with negligible standing stock (2 WHEAT each) and the opponent simply had
more to harvest on the final day (25 vs 38 HARVEST ops in one game, 26 vs 38 in the other). The file
states: "we convert standing value into cash worse than they do over the last two days." (93285579
does not have this shape — behind on total value from d24 onward, -$6,889, never led; that one is
the melon/tomato production game, not a conversion problem.)

**Killed: "we dump sales in one hour and they spread theirs."** We post SELL orders in 68 hours
across the season against the opponent's 319 (~2/day vs ~15/day in the back half). Priced on a real
d29 order: spreading 35 WHEAT over 12 hours instead of 1 gains +$3; MILK +$42; STRAWBERRY +$19;
CARROT/WOOL/FERTILIZER +$0 each. **Null — do not re-derive.** `_process_market` quotes per unit at
live inventory, so the walk-down is identical whether posted in 1 hour or 12; the only recovery
between hours is town drain, negligible at these volumes.

## 5. Pen-placement geometry — confirmed not a lever, a third time (2026-08-09)

source: `geometry_of_the_herd_2026-08-09.md`, 2026-08-09.
Two fresh loss episodes never analysed before this file: `91229682` (seed 73957860, us seat 0 vs
Shivam_2212, final $61,427 vs $94,412) and `91231728` (seed 1153474158, us seat 1 vs As Wasti, final
$89,433 vs $98,581). We lose both.

**Answer: geometry is not a lever here either** — replicates the existing verdict in `REGISTER.md`
C-21 and `experiment_log.md` §21 on two episodes nobody had looked at before. The shape difference
(our pens smeared, opponent's compact) is real and confirmed, but the assumed cost is not there.

Per-op action counts (submitted actions, both seats, both episodes) — MOVE share:

| episode | us MOVE share | opp MOVE share | our geometry vs theirs |
|---|---:|---:|---|
| 91229682 | 39.8% | 44.2% | ours worse, our share still lower |
| 91231728 | 41.6% | 56.6% | theirs worse, their share still higher |

Walk-per-work-op (realized Manhattan walking / work-ops, position-diffed from observations, not
submitted-move counts):

| episode | us | opp |
|---|---:|---:|
| 91229682 | 1.028 | 1.118 |
| 91231728 | 1.210 | 1.445 |

Total realized walking: 3131 (us) vs 3029 (opp) in 91229682 (+3.4%, roughly level); 3208 (us) vs
4125 (opp) in 91231728 (-22%, LOWER for us — in the episode with the bigger geometry gap).

Pen geometry at final state (ring-depth = mean Manhattan distance of a pen from its own herd's
centroid):

| episode | side | pens | ring-depth | mean shed-dist | shed-dist range |
|---|---|---:|---:|---:|---|
| 91229682 | us | 21 | 3.25 | 2.86 | [0,7] |
| 91229682 | opp | 14 | 1.90 | 1.21 | [0,2] |
| 91231728 | us | 16 | 2.74 | 2.19 | [0,4] |
| 91231728 | opp | 14 | 1.93 | 1.57 | [0,3] |

Shed-access tiles verified from source: `(4,4),(5,4),(4,5),(5,5)` for `boardSize=10`, farmer spawns
`(4,4)` — matches both episodes at step 0. Pens are fixed early (stabilised by day 16 in 91229682)
and never move again once built.

**Correction to a pre-existing figure**: an older "1.86 vs 2.93" ring-depth pair does not reproduce
under either Manhattan or Euclidean centroid-distance metrics, tried independently at every 2-day
checkpoint from day 0 to day 30. Closest reproduction is 3.25/1.90 (Manhattan) or 2.69/1.50
(Euclidean) — same DIRECTION (we are more spread out) but different magnitude. This file's numbers
(3.25/1.90) are the ones to cite going forward; the 1.86/2.93 pair should not be.

**Verdict:** MOVE share is lower for us in both episodes despite worse geometry; walk-per-work-op is
better for us in both episodes despite worse geometry; total realized walking is level or lower for
us. We lose both games regardless. What actually separates the two sides is production volume and
idle time — PASS (1512 vs 1005, and 1746 vs 354) and WATER (578 vs 930, and 590 vs 1133) and PLANT
(81 vs 174, and 81 vs 163) — not where the pens sit.

Where pen placement IS decided (`kagg/search/schedule_agent.py`, `_refresh_pins`, ~line 1672-1710):
falls through `PEN_SPOTS` (line 634, currently `()` — empty, shipped off; docstring records a
2-cell-out-of-150 measured difference, not worth carrying) -> shed-access tiles if free -> nearest-
depot search only if `PEN_NEAREST_DEPOT` is True (it is `False`, line 668) or day >=
`PEN_NEAREST_DEPOT_FROM_DAY` (currently 11, line 717) -> otherwise the same quadrant-major
boustrophedon sweep crops use, which is why early pens smear to the tail of the sweep.
`PEN_NEAREST_DEPOT = True` (always-nearest) was tried and reverted: it achieves no pen beyond 5
steps at day 11, but was penalised by the project's cell-count-resemblance-to-tape metric at the
time, not by a bank/win-rate test — its own docstring flags this as unresolved and asks for a
bank/win-rate re-test, which this file states has never been done. `PEN_NEAREST_DEPOT_FROM_DAY = 11`
ships because early-game distance already matches the tape exactly (22 vs 22) through day 8, and the
benefit of switching earlier is small given §5's own finding that walking isn't the binding cost.
`router.DEPOT_RING_FIRST` (the field-order-level twin, covering crops too) ships `None`/off because
it reversed sign between tuning seeds (+$20,526) and held-out seeds (-$11,111) — a winner's-curse
null, not a proven loss.
This file explicitly does not recommend spending time re-testing `PEN_NEAREST_DEPOT`, given its own
finding that geometry is not the binding cost even under the current, worse layout.
