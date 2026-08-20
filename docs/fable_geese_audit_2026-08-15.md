# Geese, audited — and why the Elo framing closes them (Fable, 2026-08-15)

Asked: audit `docs/the_goose_is_insurance_2026-08-15.md`, add the missing costs, give a policy.
Method as instructed: math only, no agent runs.
Production is stepped through the real `_daily_refresh_animals`; revenue walks the real
`market_price` unit by unit; the shop draw is exact.
Scratch scripts behind every number: `goose_audit.py` / `goose_margin.py` (session scratchpad),
all reproducible from the formulas quoted here.

## Verdict

**No geese, and the number that closes it is -$11,758 of expected MARGIN per six animals.**
On the money objective the goose really is insurance (best pick in 14.8% of shop draws).
On margin — ours minus theirs, which is what an Elo ladder pays — the goose is best in **0.9%**
of draws, because leaving the flooded milk/wool books stops suppressing the opponent's fixed
300/250-unit flows, and that suppression is worth ~$10,400 (milk) / ~$9,300 (wool) to whoever
is left alone in the book. The insurance premium is paid to the opponent.

## 1. Audit of the doc's three claims

**Production stepping: one real error, -2 eggs.** Stepped through
`_daily_refresh_animals` exactly (fed+cared daily, harvested before overflow):

    animal  placed  sellable  (doc)    harvest visits forced by max_held
    GOOSE      d5      44      46            12
    COW        d5      30      30             6
    SHEEP      d5      30      30             7

The doc's 46 counts the production event at the END of day 29 (`next_day` 30).
That event fires only for the goose — interval 1 lands on every rollover; the cow's events
stop at `next_day` 29 and the sheep's at 29 — and its eggs have no day 30 to be harvested
or sold in. Sellable is 44. Cross-check: my egg revenue E is $12,094 against the doc's
$12,678, and the gap is exactly those 2 eggs x 6 birds x ~$50.
The `pending_care_bonus` handling in the doc is otherwise RIGHT, including the subtle first-event
behaviour (goose: 3 banked bonuses + base = 4, exactly `max_held`, no loss; cow: 7 banked + base
= 8, capped at 6, loses 2 — already in both our totals).

**Binomial(8, m/8): correct.** Eight draws, `next_day % 3 == 0` at next_day 3..24, uniform with
replacement over `sorted(SHOPS)`, `MAX_SHOP_INSTANCES = 8` never binds before the 9th draw
(`reference/kaggriculture.py:886-891`). P(zero): EGG (6/8)^8 = 10.0%, MILK (5/8)^8 = 2.3%,
WOOL (7/8)^8 = 34.4% — all three match the doc. One thing the count alone misses: unlock TIMING.
An instance drawn d24 drains 6 days, one drawn d3 drains 27; my revenue model carries the ramp.

**EGG undentable above I0: correct.** `log` / `above_target 0.2`: halving the price needs
`1.722 * ln(1+x) = 25`, i.e. x ~ 2 million units above I0. Same class as WHEAT's above-curve.
This is also why the two independent revenue models agree on eggs to within the 2-unit error
while disagreeing on milk and wool.

**Where the doc's revenue model is optimistic: cow and sheep E.** The doc has
COW E $21,278 ($118/unit) and SHEEP $22,590 ($125/unit). My model — same shared book, same
opponent volumes, but pro-rata drain share and the residual dumped at d29 — gets
COW $14,041 ($78/unit) and SHEEP $15,778 ($88/unit). The real seed-11 game realises milk at
**$69/unit** (171 sold, $12,194), which sides with the lower model; the ladder memory
(`milk is floored at $1-5`) points the same way. This does not rescue the goose on money —
the ordering GOOSE < COW < SHEEP survives in both models — but the "$8k per six" gap the doc
quotes shrinks to **$1.3-2.5k** under the floor-realistic release, and the goose's money-corner
widens to 14.8% of draws (median gain $2,330 over the best pasture, p90 $5,841).

## 2. The costs the doc left out, priced

**Feed: cancels.** Every animal eats 1 WHEAT/day (`FEED`, `:505-513`) — species-identical, so it
cannot move the ranking. Absolute: 6 animals x ~24 fed days ~ 145 wheat, $3.2k at the seed-11
realised $22/unit, up to $6.5k at the field's $45. Charge it to "animals at all", not to species.

**Op cost: bounded, does NOT reverse anything.** The goose's cap forces 12 harvest visits against
the cow's 6 and the sheep's 7 — but every animal already receives a daily FEED+CARE visit, so the
extra HARVEST is one op at a tile the route already stands on. Marginal: ~5-6 unit-turns per
goose-SEASON. Even priced at a panic $50/turn that is < $300 against ranking gaps in the
thousands. The goose actually SAVES ops elsewhere: an undentable book makes release timing
worthless, so eggs can ride the automatic end-of-day inventory drop
(`_drop_inventories_to_shed`, `:878`) — no h05 shed race, which milk does need.

**Coop vs pasture: the tile cancels, the build is one op.** Any animal occupies a tile, so tile
opportunity cost is common to all three species. The differential cost of a goose is one
`BUILD_COOP` op (money-free, `:493`) plus the pen-geometry/opening perturbation — which the
question's framing says to ignore (the agent gets adapted). Called: ~zero in this arithmetic.
The doc's point that `SHOP_ADAPT_HERD`'s cow<->sheep float is free BECAUSE both build PASTURE
stands.

## 3. The Elo framing — this is what closes it

Money maximisation and margin maximisation disagree here, and the margin is what the ladder pays.
The opponent's flow is open-loop and fixed: MILK ~300 from d13, WOOL ~250 from d11, EGG 0.
Our species choice decides which book we co-occupy. Computed per draw, real curve walk,
their revenue with and without our flow in the book:

    suppression value of OUR 180 units on THEIR flow (their gain if we exit):
      milk: mean $10,411   p10 $5,513   p90 $14,240
      wool: mean  $9,275   p10 $2,611   p90 $18,145

    margin objective (ours - theirs, net of purchase), best pick over 4,000 draws:
      COW    43.6%      SHEEP  55.5%      GOOSE  0.9%
      goose margin E is $11,758 WORSE than cow/sheep

Mechanism: our marginal milk units were heading for the floor anyway (small loss to us), but
their presence forces pro-rata floor-sharing on the opponent's 1.7x larger flow (large loss to
them). Eggs are the mirror image: an uncontested, undentable book means our egg revenue is safe
AND harmless — nothing we sell there costs the opponent a dollar. Safe-and-harmless is exactly
what a zero-sum ladder does not pay for.

Even conditioned on the best observable corner — no YARN_STORE and no milk carrier among the
three draws visible by d9 (their money-corner detector, 12.8% of games) — P(goose margin-best)
is **7.0%**. There is no observable that rescues it.

This also reframes `project_kaggriculture_milk_is_floored` ("we flood our own book, this is
where the $11k gap is"): partially true for our bank, but the flood is simultaneously holding
the opponent's 300 units down. Any fix that WITHDRAWS milk supply gifts back up to ~$10k of
their revenue; the margin-aware fix is release timing within the book, not exit from it.

## 4. Policy

- **Zero geese.** Closing number: -$11,758 margin E per six animals; goose margin-best in 0.9%
  of draws, 7.0% in its best observable corner.
- The cow<->sheep float (`SHOP_ADAPT_HERD`) is the right lever and stays; on the margin
  objective the split is COW 43.6% / SHEEP 55.5% of draws, so the adaptive pasture herd is
  near-optimal already.
- The HERD_GEESE deletion (7a88d30) was right by accident: the sweep it rested on measured
  unsellable eggs, but the corrected arithmetic reaches the same end state.

## 5. Caveats, stated plainly

- Opponent volumes are three replays (MILK 300, WOOL 250). The suppression magnitudes scale
  roughly linearly with their volume; the SIGN of the margin result is robust to +/-50% on them,
  and the EGG 0 term is structural (fixed scripts cannot respond).
- Fill sharing is modelled pro-rata within each day. The env's real interleave is per order
  slot; either seat can front-run within a turn, but over a season of daily flows pro-rata is
  the right first-order model, and it is the SAME assumption on both sides of every comparison.
- Only 6-of-one-species portfolios were compared, matching the doc. Mixed herds interpolate;
  nothing in the margin table rewards mixing geese in.
- Margin E levels (-49k etc.) include their fixed wool+milk revenue as an offset; only
  DIFFERENCES across our choices are meaningful, and those are what is quoted.
