> SUPERSEDED by docs/allocation_bounds_pass2_2026-08-16.md - same day, same script, a tighter solver
> gap and a corrected cost model narrow every band in this file 24-32% and add a per-shop-draw policy
> this pass does not have.

# Allocation bounds: the near-optimal region for every crop and species

2026-08-16.
Model and solver: `scripts/allocation_bounds.py`.
Run log: `data/logs/allocation_bounds.log`.

The question answered: given the game's constraints, what RANGE must the season allocation lie in?
The deliverable is a near-optimal region per crop and per species — the interval each season total
can move over while end-of-season money stays within 1% (and 5%) of the model optimum.

## Headline

The leader's MELON 20 / STRAWBERRY 34 split is NOT inside the 1% near-optimal region in any
of the three scenarios.
Pinning it costs 1.78% of the optimum when the opponent sells nothing, 3.9% against the
leader's own supply, and 23% against double supply.
It IS inside the 5% region in the first two scenarios.
The reason is melon alone: the melon book absorbs only ~30 units of town demand a season and
its price falls as 250 − 0.01·(surplus)², so 20 melon tiles (120 melons) is near-optimal only
when the OPPONENT is not also selling melons.
His strawberry 34 sits inside the 1% interval in scenarios 1 and 2.

The herd answer is shop-draw dependent, not universal: under this game's draw (SMOOTHIE x4 =
strawberry+milk demand) the model wants 9-18 cows and his cross-game modal COW 6 is below the
1% interval, while under an average draw the optimal herd collapses to COW ~2.
His measured play IN this game (COW 10, SHEEP 4) matches the model's scenario-1 optimum
(COW 9, SHEEP 6) far better than his cross-game modal 6/8 — consistent with
"the leader re-plans on the shop draw".

## Results

All money figures are end-of-season money minus the $3000 start (Z).
Base MILP solves reached mip gaps of 0.4-0.7% at the 150 s limit (flagged in the log);
the pinned leader checks reached 0.4-2.0%, so quote their drops with that width.
Ranges are LP-relaxation OUTER bounds (see below): outside them the loss certainly exceeds
the tolerance; inside them not every point is achievable — the pinned checks close that gap
for the leader's own point.

Units: crops = tile-cycles planted over the season (a melon cycle is 1 tile for 11 days);
animals = head bought.  "leader" = his measured allocation over 51 games.

    S1  opponent = leader's per-day fills      Z* = $129,045   (bank $132,045)
    item         base       [1% range]       [5% range]   leader
    WHEAT          93        [15, 185]         [0, 229]        -
    CARROT         16         [0, 144]         [0, 194]        -
    TOMATO         22          [0, 68]          [0, 85]        -
    STRAWBERRY     29         [15, 50]          [7, 64]       34
    MELON           6          [0, 31]          [0, 45]       20
    GOOSE           2          [0, 15]          [0, 21]        0
    COW             9          [6, 17]          [5, 22]        6
    SHEEP           6          [4, 15]          [3, 20]        8
    pinned MELON=20,STRAW=34             -> Z $123,989, drop 3.92%  (>= 2.0% after gap)
    pinned MELON=20,STRAW=34,COW=6,SHEEP=8 -> Z $118,148, drop 8.44%

    S2  opponent = zero                        Z* = $190,247   (bank $193,247)
    item         base       [1% range]       [5% range]   leader
    WHEAT          65         [2, 148]         [0, 181]        -
    CARROT          7          [0, 86]         [0, 135]        -
    TOMATO          2          [0, 38]          [0, 56]        -
    STRAWBERRY     33         [20, 51]          [9, 62]       34
    MELON          27         [14, 42]          [6, 55]       20
    GOOSE           0          [0, 10]          [0, 17]        0
    COW            18         [13, 24]          [8, 30]        6
    SHEEP          10          [7, 18]          [5, 24]        8
    pinned MELON=20,STRAW=34             -> Z $186,856, drop 1.78%
    pinned MELON=20,STRAW=34,COW=6,SHEEP=8 -> Z $161,856, drop 14.92%

    S3  opponent = 2x leader's fills           Z* = $56,125    (bank $59,125)
    item         base       [1% range]       [5% range]   leader
    WHEAT         110        [47, 197]        [31, 227]        -
    CARROT         43         [0, 130]         [0, 165]        -
    TOMATO         40         [16, 64]          [6, 74]        -
    STRAWBERRY      9          [1, 20]          [0, 27]       34
    MELON           0          [0, 12]          [0, 20]       20
    GOOSE          16          [8, 22]          [5, 25]        0
    COW             0           [0, 5]           [0, 7]        6
    SHEEP           0           [0, 3]           [0, 6]        8
    pinned MELON=20,STRAW=34             -> Z $43,198, drop 23.03%
    pinned MELON=20,STRAW=34,COW=6,SHEEP=8 -> Z $31,545, drop 43.79%

Base solution details, scenario 1: hands 8.1/day mean (leader measured 9.6 units/day incl.
farmer), 2 land parcels, wheat bought 142, fertilizer collected 335 and sold 145
(the leader sold 249), sold MELON 36 / STRAWBERRY 232 / MILK 294 / WOOL 164.

### What holds in all three scenarios

- Some strawberry is always in (min never 0 at 1% in S1/S2; 1.5 in S3), and 34 tiles is
  never harmful by more than ~2% except under a double-supply flood.
- Melon is the contested resource: its 1% interval slides from [14, 42] (empty market)
  to [0, 31] (leader present) to [0, 12] (flooded).  There is no melon count that is
  near-optimal in all three scenarios — melon allocation is a bet on what the opponent sells,
  not a fixed constant.  20 is the S2 answer played unconditionally.
- Wheat is wide everywhere ([15-47 min, 148-197 max @1%]): dozens of wheat cycles are
  interchangeable with bought wheat at a few dollars margin.  A wide range is a real finding:
  wheat count is nearly a free parameter.
- Geese are never obligatory below double supply, but become the SAFE HAVEN when everything
  else floods (egg price is log-flat above I0): S3 forces 8-22 geese.  This is the first
  measured case where geese are the right play — against a flooder, not against the field.
- The herd (cow+sheep) tracks milk/wool demand from the shop draw, from 0 to 28 head.

### Shop-draw sensitivity (scenario-1 economics)

    draw            Z*        WHEAT CARROT TOMATO STRAW MELON  GOOSE COW SHEEP
    actual (SMOOTHIEx4) $129,045   93    16    22     29     6      2   9    6
    expected (avg shop) $93,073    85    42    29     16    11     10   2    5
    no shops            $53,038   141    46    23      0    13     17   0    0

The draw moves Z* by a factor of 2.4 and reallocates the whole farm: strawberry 29 -> 0,
cows 9 -> 0, geese 2 -> 17.  Melon moves only 6 -> 13 because melon has no shop —
its demand is the town center's 1/day regardless of the draw.
Any fixed season allocation is therefore an average over draws; the measured leader behaviour
(fixed 74-turn opening, then adapt to the draw) is what this table predicts a good player
must do.

## Ground truth and inputs

- Rules, prices, growth data: imported at runtime from the installed
  `kaggle-environments 1.32.7` kaggriculture module, which is byte-identical to the main repo's
  `reference/kaggriculture.py`.
  The worktree copy of `reference/kaggriculture.py` in this branch is STALE
  (pre-hinge, pre town-drain change); it was not used.
- Opponent supply: episode 92498144 (カワシギ $149,998 vs Yusuke Hayashi $143,436, seed 1240813987),
  re-run through the real engine with the recorded actions and seed, logging every `_commit_unit`
  fill.
  The recorded rewards reproduce to +$78/+$0 (0.05%); the drift is the 1.32.7 repricing of
  CARROT/TOMATO/EGG (the episode was recorded on module 1.32.6).
  Fills are exact, not inferred from the action stream (offers are not fills).
- Leader's measured season, from those fills:
  sold WHEAT 522 / STRAWBERRY 223 / MELON 120 / MILK 279 / WOOL 120 / FERTILIZER 249 / CARROT 20;
  bought WHEAT 423;
  seed buys WHEAT 144 / MELON 20 / STRAWBERRY 34 / CARROT 16; animal buys COW 10 / SHEEP 4.
  The MELON 20 / STRAWBERRY 34 seed buys equal the reference allocation measured over 51 games.
- Shop draw in that game (with replacement, active-from-day):
  d3 SMOOTHIE, d6 ICE_CREAM, d9 FARMERS_MARKET, d12 YARN, d15 PIZZA, d18/21/24 SMOOTHIE.
  Season town drain under that draw: WHEAT 390, CARROT 156, TOMATO 246, STRAWBERRY 624, MELON 30,
  EGG 30, MILK 588, WOOL 246, FERTILIZER 0.

## The model (MILP over days 0..29)

Decision variables (all per day):

- `x[c,fert,d]` int — tiles starting a crop cycle of variant (crop, fertilised?) on day d.
  Variants: WHEAT_u/f, CARROT_u/f, MELON_u, TOMATO_u/f, STRAWBERRY_u/f.
- `y[a,d]` int — animals of species a bought, penned and placed on day d.
- `h[d]` int — hands hired that day (hands are per-day in this game; the crew resets at dawn).
- `land[k,d]` bin — k-th parcel bought on day d (ordered, prices 1000/2000/4000).
- `u[p,k]` cont — units of product p sold in sell-slot k (see Revenue).
- `wbuy[d], g[d]` — wheat bought / own-grown wheat diverted to feed.
- `fbuy[d], fcol[d]` — fertilizer bought / collected from animals (1 op per unit).

Every cycle/placement expands to an exact per-day profile of work ops, yields, feed and
fertilizer use, simulated directly from the env rules (watering windows, `consecutive_unwatered`,
care-bonus accrual, held-unit caps, harvest cadence, decay + DIG).
Self-checked anchors: wheat_u 4 units/6 ops, melon 6 units/10 ops/11 tile-days,
tomato_f 8 units, strawberry_f 8 units with 2 fertilizer, goose first 4 eggs at day+4 then 2/day,
cow first 6 milk at day+8 then 3 per 2 days, sheep first 6 wool at day+6 then 4 per 3 days.

Constraints, all linear:

- Tiles: sum of active cycles + pens <= 25 + 25 * parcels bought by day d (max 100).
- Labour: (1 + lambda) * work_ops_d <= 24 * (1 + h_d), lambda = 3477/2773 = 1.254 —
  the leader's measured move/work ratio over a full season (seed 11 tape:
  work 2773, move 3477, idle 660 of 6910 unit-turns).
  Movement is charged on every work op; market orders (SELL/BUY/HIRE/BUY_LAND) cost no turns.
- Cash: running bank >= 0 every day, from $3000.
  HIRE cost is the exact per-day fibonacci sum (convex slot formulation).
- Growth: encoded in the cycle profiles; a cycle with no harvest before day 29 does not exist.
- Feed: 1 wheat per animal per day (fed through day 28); grown wheat usable the morning
  after harvest, bought wheat the same day at the simulated market price.
- Fertilizer: collected (1 op) from any live animal, at most 1/animal/day, or bought;
  used by fertilised cycle variants; sellable.
- Sales availability: cumulative units sold by a slot's day <= cumulative harvested by then.

Objective: end-of-season money = sum of slot revenues minus seeds, animals, land, hires,
wheat and fertilizer purchases.

### Revenue (the hard part)

Price is the env's own `market_price` (hinge shapes included) on a per-product book:

    book(d) = I0 + own_sales(price>1) + opponent_net(d) − town_drain(d)

Each product gets K=30 sell slots of fixed width with FIXED assumed sell days:
slot k is sold on the earliest day where cumulative book room (town drain minus opponent
supply, made monotone) reaches k*width — i.e. the model sells unit-for-unit into demand as it
materialises, which is what the leader's cadence does.  Units beyond total season room sell at
day 29 (surplus tail); products with no demand regime (melon) spread uniformly over their window.

Slot k's value is simulated unit-by-unit with slots 1..k-1 already sold — the maximum possible
prior own supply — so every slot value is a LOWER bound on the realised price of those units for
any fill pattern the MILP chooses.  This makes the piecewise revenue LP-safe with no SOS2 or
binaries: skipping early slots and filling late ones only under-prices the late ones.
MELON's `sq` above-threshold shape (price 250 − 0.01*(inv−I0)^2, floor $1, floor sales do not
move the book) is priced exactly by this unit-level simulation.

### How the ranges are computed

The base optimum Z* is a MILP solve (HiGHS via scipy, mip_rel_gap 2e-3, incumbents at the
time limit flagged in the log).
Each range endpoint is then min / max of the item's season total subject to all constraints
plus objective >= (1 - tol) * Z*, solved on the **LP relaxation**.
Every integer-feasible point is LP-feasible, so these are valid OUTER bounds on the true
integer range: outside the reported interval the objective certainly drops more than tol;
inside it, not every point need be achievable.
(Hard-floor integer range solves were tried first and are not tractable here: HiGHS needs
~150 s to find any integer point within 1% of Z*, and 96 such solves do not fit a day.)

Because an outer bound could make the leader's point look inside when it is not, the
leader's reference allocation is ALSO checked directly: MELON=20 and STRAWBERRY=34 (and
separately +COW=6, SHEEP=8) are pinned as equality constraints and the full MILP re-solved;
the realised objective drop is reported per scenario.

### Assumptions, stated plainly

1. Walk cost is an average: 1.254 move-turns per work op, calibrated on the leader's own season.
   No per-quadrant term — the shed is central, so all four quadrants have the same distance
   distribution (mean Manhattan distance 4.0 from the shed corner to a quadrant tile).
2. Sell timing is an assumption, not a decision variable: sales follow the demand curve
   (surplus tail at day 29).  Slot values are conservative (max-prior-own-supply).
3. Within-day cash ordering is ignored (a day's revenue can fund that day's purchases);
   the leader's own play does sell-then-buy within a day.
4. Our own wheat BUY volume does not move the wheat book in the base solve; one feedback
   iteration re-prices wheat buys with the chosen volume folded in and re-solves
   (triggered above 100 units).  Fertilizer buys are priced the same way, without iteration.
5. Full husbandry on animals (daily feed + care, harvest at cap) and full watering on crops;
   weeds from missed watering and the 0.5% random weed spawn are not modelled.
   CARE is skipped when the bonus cannot land (cap or season end) — e.g. a cow placed day p
   is cared only 5 of its 8 pre-production days.
6. Shed capacity (100) and the 10-orders-per-turn cap are not binding at these volumes
   and are ignored.
7. Animals never escape and are never sold; pens hold one animal for the rest of the season.
8. GOOSE/COOP is modelled (nothing forbids it); the ranges answer whether it should exist.
9. Opponent behaviour is FIXED per scenario (the three opponent-supply scenarios);
   the market book is the only interaction channel modelled.  No Elo/win-rate objective —
   this is a money-maximising planning bound, as specified.

### Known biases

- Revenue is a lower bound under the fixed sell schedule; a solver free to choose timing
  could do slightly better (melon especially: selling before the opponent floods the book).
- Labour is charged at the leader's realised walk ratio; a better router lowers it, a worse
  one raises it.  The leader also idled 9.6% of unit-turns which the model does not charge.
- Prices are conservative for high-volume products (max-prior-fill assumption), so
  high-volume items (milk, strawberry, wheat) are if anything UNDER-allocated by the model.

## Run facts

Full run 1975 s on 2026-08-16, log `data/logs/allocation_bounds.log`.
MILP sizes: 1140 variables (300 integer), 573 constraints; HiGHS via scipy 1.16.
Wheat-buy price feedback triggered in all three scenarios
(S1 bought 142, end price $42→$46; S2 bought 466, $45→$54; S3 bought 101, $39→$42);
the tables above are the post-feedback solves.
Sanity anchor: the model's S1 bank ($132k) sits between the leader's real $150k (a better
seller than the model's conservative slot pricing) and half of it, and the model's implied
play mirrors his measured season: hands 8.1 vs 9.6 units/day, cows 9 vs 10, sheep 6 vs 4,
strawberry 29 vs 34, fertilizer sold 145 vs 249, wheat grown-and-bought in both.
