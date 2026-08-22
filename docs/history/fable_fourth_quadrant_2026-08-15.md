> SUPERSEDED by docs/fable_fourth_quadrant_reopened_2026-08-15.md - same day. Real ladder seats show
> a 100-tile quadrant is worked with the SAME hire count as a 75-tile one (277 season hires either
> way), so this file's closing argument - a ~$21,960 marginal-crew cost - prices a plan nobody plays
> and is retracted by the reopened file, section 1.

# Is there a narrow path to a fourth quadrant? (Fable, 2026-08-15)

Verdict up front: **no path at quadrant scale — closed by the fibonacci hire curve, not by the
bank.** Crewing 25 new tiles costs ~$21,960 in marginal hires over d12-29 against a measured
marginal crop value of $6,039 (wheat) or $15,298 (tomato, best realistic conditional case).
One arithmetic sliver survives — a conditional PARTIAL planting of ~8 tomato tiles, ~5-26% of
games — and it is operationally unreachable while cover.py cannot seat the harvest jobs it
already builds. Numbers below; nothing in agent code was changed for this.

## 1. Cost and timing — the bank does not close this

- The fourth parcel is the THIRD purchase: `LAND_ORDER = ["NE", "SW", "SE"]`,
  `LAND_PRICES = [1000, 2000, 4000]` (`reference/kaggriculture.py:96-97`). **$4,000, SE.**
- Purchases are sequential but nothing stops two in one day. Earliest covered turn: **d11**,
  alongside the third parcel — d11 currently closes at $12,699 after seeds $2,380, animal $800,
  hires $376 and the $2,000 parcel; adding $4,000 still closes ~$8,700, and every later day
  closes higher (d12 $16,246, d14 $21,799). No scheduled seed/animal/hire purchase is starved.
- So affordability is not the question. The crew is.

## 2. Can the crew work it — the closer

Working 25 wheat tiles in steady state needs ~35 work ops/day (25 water + ~5 plant + ~5
harvest) plus ~25-28 moves to snake the quadrant from the shed spawn: **~60-65 unit-turns/day,
i.e. ~2.6 dedicated hands.**

The schedule already hires 12 hands/day at $376 = sum(fib(0..11)) exactly — confirmed against
the grid's hire row. The hire curve is `cost = fib(n_already_today)`
(`reference/kaggriculture.py:698`), so the marginal hands cost:

    13th hand  $233/day
    14th hand  $377/day
    15th hand  $610/day     -> 3 extra hands = $1,220/day
    over d12-29 (18 days)   -> ~$21,960

Against that, the crop side (section 3): $6,039 for wheat, $15,298 for the best realistic
tomato case. **The crew costs 1.4-3.6x everything the quadrant can grow.**

The "use the idle instead" escape is refuted by Alex's own measurement, not by a model:
d9-29 idle is 979 turn-slots against the tape's 383, and yet 16 tiles a season die holding
units, 11 of them with a HARVEST job built on their one safe day that was not seated — and
`cover.py` contains zero references to `max_lifespan_step`, so the visit order cannot even see
the deadline. Idle turn-slots are positional; they are demonstrably not fungible into located,
deadline-day work in the quadrants we already own. A 26th-through-50th tile only multiplies the
population exposed to that mechanism: **an unreachable one-shot tile is worth negative** (seed
paid, ops spent, unit decayed to WEED), and wheat/carrot — the only crops with spare-tile-scale
economics — are exactly the crops with the one-day window.

## 3. What it would grow, measured on the real books

**Wheat** (+25 tiles from d12 = 3 cycles x 4u = +300 units), marginal revenue on the REAL
seed-11 book — recorded arrivals and both seats' sells, optimal release, via
`scripts/optimal_release.py`'s own season model:

    baseline optimal   531u -> $11,710   ($22.1/u)
    with +300u         831u -> $17,749   marginal $6,039 = $20.1/u

    net: $6,039 - $750 seeds - $4,000 land - $21,960 crew  =  ~ -$20,700   CLOSED

(The $45/u wheat realised against the ladder field does not rescue it: even at $45/u the 300
units gross $13.5k against $26.7k of costs.)

**Tomato, conditional on the d12-visible shop draw** (the only play my allocation work left
open) — exact d29 dump revenue at the median deficit of each visibility bucket, zero
production premise, premium decay included:

    visible by d12    P(games)    32u        100u        200u (fertilized)
    0                  31.3%     $2,183     $6,324     $10,324
    1                  42.2%     $2,773     $8,179     $15,121
    2                  21.4%     $6,178    $15,298     $24,012
    3+                  5.0%    $16,043    $41,423     $62,588

A FULL quadrant of tomato (100u unfert / 200u fert): at 2-visible it grosses $15-24k against
~$27k of land+seeds+crew — still negative. Only the 3+-visible bucket (5% of games) covers the
costs, and two things eat that tail: the shed caps at 100 items TOTAL so a 200u hold-to-d29
dump is infeasible (the release must spill early into a shallower deficit), and the number
assumes flawless daily watering of 25 far tiles for 18 days by a router that today drops
seated jobs in the quadrants it knows.

## 4. The sliver that survives arithmetic, and why it still fails

Conditional partial use: buy the parcel at d12 ONLY when 2+ tomato-stocking instances are
visible (26.4% of games), plant ~8 tomato tiles, crew them from existing idle (no 13th hand),
hold and release late:

    2-visible:  32u -> $6,178 - $4,000 land - $400 seeds  =  +$1,778   (21.4% of games)
    3+-visible: 32u -> $16,043 - $4,400                   =  +$11,643  ( 5.0% of games)
    unconditional EV                                      ~  +$960/game

Tomato is `ongoing: true` — no one-day harvest window, so the crop-death mechanism does not
apply to it; the risk is two missed waters = WEED. That is the same seating problem in a
different costume: ~10 SE unit-turns/day for 18 days with a no-miss-twice constraint, from a
planner that currently leaves 11 built jobs unseated per season. It also requires agent code
that does not exist (a conditional BUY_LAND, SE routing), and ~$1k/game EV is under the
seed-noise floor (~15%) — it could not even be measured cleanly today.

## 5. Bottom line

    marginal crew for a workable quadrant      -$21,960
    best full-quadrant crop value (realistic)  +$6,039 wheat / +$15,298 tomato 2-visible
    -> full quadrant                            NO, in every bucket except a 5% tail the
                                                shed cap and the seating defect both bite
    -> conditional 8-tile sliver                +$960/game EV on paper, unreachable until
                                                the router can seat deadline-day jobs

The same crew-seating defect that kills the fourth quadrant is already costing 16 dying tiles
a season in the three we own. Fixing the seating pays there first, with no land, no hires and
no new code path — and only after that fix would the sliver above even be measurable.
