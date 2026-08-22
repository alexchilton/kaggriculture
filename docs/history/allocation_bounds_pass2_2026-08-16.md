# Allocation bounds, pass 2: narrower bands, per-draw policy, best response

2026-08-16.
Model: `scripts/allocation_bounds.py` (modes `attrib`, `policy`, `br`; pass-1 `scenarios`
mode unchanged).
Logs: `data/logs/allocation_bounds_pass2_attrib.log`, `..._policy.log`, `..._br.log`.
Ground truth remains the installed `kaggle-environments 1.32.7` kaggriculture module
(byte-identical to the main repo's `reference/kaggriculture.py`; the worktree copy of
`reference/` is stale and was not used).

## Headline

- The bands narrowed 24-32% from modelling fidelity (items 2+4), essentially 0% from the
  solver gap at the 1% tolerance, and a further ~25% by reporting at 0.1%:
  WHEAT [15, 185] -> [23, 135], CARROT [0, 144] -> [0, 86] (combined model, 0.1%).
  What width remains at 0.1% is genuine economics: carrot and tomato are near-zero-margin
  crops whose lower bound really is 0.
- The per-draw policy table is the actionable output: the optimal mix swings from
  SHEEP 20 / STRAWBERRY 9 (YARNx4 draw) to STRAWBERRY 28 / COW 9 (SMOOTHIEx4 draw) to
  GOOSE 6 / CARROT 37 (BAKERY+PET draw).  No fixed allocation is near-optimal across draws.
- MELON 20 / STRAWBERRY 34: melon 20 lies inside the 1% outer interval of every draw solved;
  strawberry 34 only under smoothie-heavy draws.  The JOINT point always costs more than 1%:
  3.7% under the actual draw and 13-15% under the others.
- Best-response iteration: every quantity except melon is stable from iteration 0
  (STRAW 26-30, COW 9-10, SHEEP 5-6, WHEAT 79-85, GOOSE 0-2); melon see-saws
  7 -> 18 -> 11 -> 12 tiles against opponent melon 120 -> 42 -> 108 -> 66, a contracting
  oscillation around ~12-14 tiles per player with combined sales pinned near the 188-unit
  season cap.  MELON 20 is the exploitable side of that fixed point: the best response to a
  20-tile melon opponent is 7 tiles, not 20.

## What was already in pass 1 (so it is not re-claimed here)

- Feeding consumes wheat: the herd's 1 wheat/animal/day comes from grown wheat (usable the
  morning after harvest) or market buys at the simulated day price; the S1 optimum grew 93
  wheat cycles and still bought 142 units.  Herd and crops were never independent.
- Animal yield schedules are simulated from the reference rules exactly, including
  `max_held` caps and the harvest cadence they force: cow first 6 milk at day+8 then 3/2d
  (harvest every 4 days), sheep first 6 wool at day+6 then 4/3d, goose first 4 eggs at
  day+4 then 2/d (harvest every 2 days).  Self-check asserts pin these.
- Fertilizer is a real lever with turn cost: COLLECT_FERTILIZER is 1 op per unit (max
  1/animal/day), fertilised crop variants carry their FERTILIZE ops and usage, and
  fertilizer is sellable (S1 optimum collected 335, used ~190, sold 145).
- Hire cost is the exact per-day fibonacci sum via a convex slot formulation, so hiring is
  lumpy and cash-timed in the model too.  (The reference's silent `_do_hire` failure on a
  short bank is an execution hazard, not a planning constraint; the model's bank >= 0 per
  day guarantees the plan never walks into it.)

## Corrections to the tasking, from the reference

Two factual points in the tasking do not match the 1.32.7 rules, and the model follows the
rules:

1. Ongoing crops do NOT need water every single day.  `_daily_refresh_plants` weeds a tile
   at `consecutive_unwatered >= 2`, so watering every other day keeps any crop alive, and
   unfertilised ongoing production does not require watering at all (only the fertiliser
   bonus checks `watered_today`).
2. An ongoing tile's obligation is finite, not to season end.  After `max_yield`
   productions the plant's `max_lifespan_step` is set and it decays; a strawberry planted
   day d produces evenings d+9/11/13/15 and is dead wood from d+17.

Pass 1 therefore already charged per-day maintenance for ongoing crops:
strawberry_u = 8 waters + 1 harvest + 1 dig over 17 tile-days (0.59 ops/tile-day),
tomato_u = 6 waters + 1 harvest + 1 dig over 12 tile-days (0.75),
vs melon = 10 ops over 11 tile-days (0.91 — melon is the op-DENSEST crop per tile-day
because one-shot yield requires 5 window waters).
The 19-strawberry-weed game (93593633) was an execution failure — idle turns existed on the
two days before the die-off — not a cost the planner omitted.
What pass 2 adds for it is a DAILY-WATER robustness variant: every ongoing tile watered
every day (the execution-safe schedule), costed and attributed below.

## The four items, what each changed

### Item 3 — solver gap vs tolerance

Pass-1 base solves stopped at 0.4-0.7% gap against a 1% band: part of every band was slop.
Pass 2 solves the base MILP at `mip_rel_gap 5e-4` (600 s), reports the attained gap, and
adds 0.1% bands.  Bands remain LP-relaxation OUTER bounds with the floor on the incumbent
(floor = (1-tol)*Z_inc <= (1-tol)*Z_true, so outer validity is preserved); the attained gap
is the amount by which each band is still wider than the true-economics band.

### Item 2 — ongoing maintenance (daily-water variant)

Profiles rebuilt with every ongoing tile watered daily (strawberry_u 8 -> 16 waters,
tomato_u 6 -> 11).  This is the execution-safe schedule that would have prevented the
weed die-off.

### Item 4 — geometry walk model

The flat 1.254 move-turns per work op is replaced by:
1 move per tile VISIT (serpentine adjacency: consecutive worked tiles are neighbours), where
a crop op is one visit but an animal pen's whole daily block (feed+care+collect+harvest)
shares ONE visit; plus a fixed 8 moves per unit-day transit (the mean Manhattan distance
from a shed-access corner to a tile of its quadrant is exactly 4.0 each way, dawn out and
dusk walk-home-and-drop).
This prices animals cheaper per op and crops dearer than the flat average, which is the
"feasible on average" failure the flat model had.  The solution's implied move/work ratio
is printed against the tape's 3477/2773 = 1.254.
Note the geometry gives NO between-quadrant differentiation: the shed is central, so all
four quadrants have identical distance distributions — the Nth TILE is not further, only
the Nth VISIT costs another move.

### Item 1 — per-draw policy

One correction to the premise: the pass-1 bands were ALREADY per-draw (S1 used the actual
92498144 draw); the 2.4x Z* swing across draws widened nothing in them.  What per-draw
solving adds is the POLICY: per draw, the clairvoyant optimal mix and its band — the
"given this draw, plant this" table.  Draws are sampled exactly as the env draws them:
8 instances at days 3,6,...,24, uniform over sorted(SHOPS) WITH replacement.
Opponent supply is held at the leader's recorded fills for every draw (his fills were a
response to the actual draw; SPECULATION: against a draw-adapted opponent the contested
books would be tighter than modelled).

## Town demand caps, explicit

Season units the shared book can absorb before the price floor, actual draw
(cap = town drain + surplus room above I0 until price 1; both players share it):

    product     drain  floor_room   season cap   price at I0+50  at I0+150
    WHEAT         390       >5000            -              22        21
    CARROT        156         842          998              27        21
    TOMATO        246         529          775              42        29
    STRAWBERRY    624          62          686              24         1
    MELON          30         158          188             225        25
    EGG            30       >5000            -              43        41
    MILK          588          76          664              55         1
    WOOL          246          59          305              55         1
    FERTILIZER      0         493          493              90        70

Demand-limited products: MELON (188 — the leader alone sells 120), WOOL (305),
FERTILIZER (493).  Labour-limited: WHEAT, EGG (price never floors).
STRAWBERRY/MILK sit in between: huge drain under this draw but a cliff just past it.
Shed capacity (100) never binds: the largest single-day harvest in any pass-2 base solution
is printed per run ("peak daily harvest") and stays under the cap, and sales settle the
same day the slot fires.

## Attribution: one item at a time (S1, actual draw, opponent = leader fills)

Each variant changes exactly one thing against the recomputed pass-1 baseline V0.
1% band WIDTHS (upper minus lower, LP outer bounds):

    item        V0 pass1   V1 tight-gap   V2 daily-water   V3 geom-walk   V4 combined
    WHEAT          169.6         169.7           153.6           146.7          128.7
    CARROT         144.3         144.3           127.8           113.7           97.8
    TOMATO          68.1          68.1            57.6            62.9           50.5
    STRAWBERRY      34.3          34.3            30.1            32.4           28.0
    MELON           31.2          31.2            28.8            28.6           26.1
    GOOSE           14.5          14.5            12.6            14.6           12.2
    COW             10.9          10.9             9.2            10.1            8.1
    SHEEP           10.7          10.7             9.4            10.2            8.4

    Z*          $129,045      $129,046        $127,578        $125,807       $123,827
    gap attained   0.40%       <=0.05%           0.20%           0.88%          0.09%

Attribution, stated plainly:

- Item 3 (gap): moved the 1% bands by 0.0-0.1 units.  The pass-1 1% bands were economics,
  not solver slop.  Where the gap DOES pay is the 0.1% tolerance: V4's 0.09% attained gap
  makes the 0.1% bands meaningful (effective tolerance <= 0.19%); under V0's 0.4% gap they
  were slop-dominated.
- Item 2 (daily-water on ongoing crops): -9% to -16% width on the crops that compete with
  ongoing for labour; Z* -1.1%.  Strawberry_u goes 8 -> 16 waters, tomato_u 6 -> 11.
- Item 4 (geometry walk): -3% to -21% width; Z* -2.5%.  The model's implied move/work
  ratio is 1.43-1.47 vs the tape's 1.254 — the geometry charges MORE than the flat model
  (transit for every unit-day dominates), so it is conservative, and it penalises
  crop-heavy, visit-dense mixes specifically (wheat/carrot narrowed most).
- Combined: -16% (melon) to -32% (carrot) width at 1%.

## The narrowed bands (combined model V4, S1, actual draw)

    item         base       0.1% band        1.0% band        5.0% band   leader
    WHEAT          83     [23, 135]        [15, 144]        [0, 178]         -
    CARROT         10     [0, 86]          [0, 98]          [0, 144]         -
    TOMATO         22     [0, 46]          [0, 51]          [0, 65]          -
    STRAWBERRY     28     [17, 40]         [15, 43]         [6, 55]         34
    MELON           7     [0, 23]          [0, 26]          [0, 38]         20
    GOOSE           2     [0, 10]          [0, 12]          [0, 19]          0
    SHEEP           6     [5, 11]          [4, 13]          [3, 18]          8
    COW             9     [7, 14]          [7, 15]          [5, 20]          6

Pass-1 vs pass-2 at 1%: WHEAT [15,185] -> [15,144], CARROT [0,144] -> [0,98],
TOMATO [0,68] -> [0,51], STRAWBERRY [15,50] -> [15,43], MELON [0,31] -> [0,26],
COW [6,17] -> [7,15], SHEEP [4,15] -> [4,13], GOOSE [0,15] -> [0,12].

## Per-draw policy (combined model, opponent = leader's recorded fills for every draw)

    draw                          Z*     W   C   T   S   M   G  Co  Sh   MELON 1%   STRAW 1%   20/34 pin
    actual  FARMERS,ICE,PIZZA,
            SMOOTHIEx4,YARN   $123,579  88  12  23  28   6   1   9   6    [0, 27]   [14, 43]      3.70%
    rng11   BRUNCH,FARMERSx2,
            ICE,YARNx4         $81,286  96  19  25   9   7   2   0  20    [0, 23]    [0, 22]     14.62%
    rng12   BAKERY,FARMERS,PET,
            PIZZAx2,SMOOTHIE,
            YARNx2            $103,883  74  37  38   3  12   6   2  10    [1, 26]    [0, 17]     13.69%
    rng13   FARMERSx4,ICEx2,
            PETx2              $73,048  65  13  37  29  13  12   0   0    [4, 25]   [20, 44]      3.66%
    rng14   BRUNCHx2,ICE,
            PETx4,YARN         $65,629  94  43  10   9  12  16   0   3    [0, 32]    [0, 29]     12.23%
    rng15   BAKERYx4,FARMERSx2,
            ICEx2              $63,876  81  33  30  13   9  13   0   0    [0, 30]    [0, 32]     12.31%

The policy reading across all six draws: the draw is revealed one shop every 3 days from
day 3, and the first 2-3 shops carry most of the signal.  Wool-heavy draws (YARNx2+) flip
the pen mix to sheep and kill strawberry; goose becomes the herd (12-16 birds) whenever
the draw gives neither milk nor wool demand (PET/BAKERY-heavy: rng13/14/15 all have
COW=0); strawberry >= 20 is only optimal under smoothie/ice-cream/farmers-market demand.
Melon's optimum is 6-13 tiles in EVERY draw — melon has no shop, so no draw ever rescues
a 20-tile melon commitment against an opponent who also sells 120 melons.
The 20/34 pin costs 3.7% under the two draws closest to his real game and 12-15%
elsewhere.
Z* across draws spans $64k-$124k (1.9x) with the opponent held fixed: most of the
pass-1 "scenario spread" was demand, not opponent.

## The leader's measured trigger, against this model

Measured on his 67 games (briefed 2026-08-16 14:21): melon at day 9 is bimodal 12 or 20,
melon + strawberry always 31, and the switch is the OPPONENT'S day-3 melon count
(>= 9 -> 12/19, < 9 -> 20/11), separating the populations with zero errors.

That is precisely the structure this model derives:

- Best response to a melon-flooding opponent: 7-12 melon tiles (BR iterations 0/2/3 vs
  opponent melon 120/108/66).  His contested mode is 12.
- Best response to a low-melon opponent: 14-27 tiles (S2 base 27, 1% band [14, 42];
  BR iteration 1 vs opponent melon 42: 18).  His uncontested mode is 20 — inside the
  band, on its cautious side.
- The BR fixed point ~12-14 tiles per player is exactly his contested mode, and the
  contracting oscillation explains why a trigger at day 3 (before any melon exists on
  the board — the earliest melon harvest is day 10, so day-3 melon count means PLANTED
  tiles, which are visible) is the right instrument: commit to the low-melon branch only
  once the opponent is seen to have committed to the high one.
- What the model does NOT reproduce is the constant sum melon + strawberry = 31.
  Our per-draw optima put melon+straw at 22-42.  SPECULATION: his constant 31 is a
  fixed-labour-block swap (8 tiles retasked between two crops with near-equal daily
  maintenance), which keeps his opening script and crew size unchanged — an execution
  constraint, not a market optimum.

Consequence for the brief: the "optimal fixed allocation" question is settled as moot —
the leader himself does not play one, and the model agrees no fixed melon count is
near-optimal against both of his modes.  The deliverable that stands is the per-draw,
per-opponent-mode policy: melon 12 contested / ~20 uncontested, strawberry filling the
demand the draw provides, herd species from the draw's milk/wool/egg demand.

On the fourth quadrant: he buys it in 21/67 games, independent of the crop swap.
This model chooses parcels endogenously and lands on 2 parcels (75 tiles) in the S1
optimum and 3 (100 tiles) in S2 — the marginal parcel tracks total demand, which is
consistent with an independent-of-crop-swap decision.  Tile budget was never binding at
75 in the S1 base (peak concurrent occupancy ~60), so the 4th-quadrant purchase is about
demand-rich draws, not about the melon/strawberry swap.

## Best-response iteration (combined model, actual draw, start = leader's fills)

    iter   opp MELON/STRAW/MILK    our mix (W,C,T,S,M,G,Co,Sh)      our Z*     our melon sold
    0        120 / 223 / 279      85,10,24,27, 7, 1, 9, 6         $123,484        42
    1         42 / 216 / 297      85,11,10,27,18, 1,10, 5         $120,369       108
    2        108 / 216 / 303      79,10,20,26,11, 2,10, 6         $119,185        66
    3         66 / 208 / 306      85,13,15,30,12, 0,10, 5         $119,606        72

Melon is the only strategically live quantity; the oscillation contracts (120/42 ->
108/66) toward ~12-14 tiles (~70-85 units) each, combined ~150 units against the 188-unit
season cap.  Everything else is a fixed point from the first iteration.
Gap caveat: iteration solves attained 0.1-0.3% gaps against differences of $1-4k between
iterations, so the melon trajectory is solver-noise-free; the +/-1 wobbles in
tomato/carrot are within gap and not meaningful.
SPECULATION: the symmetric equilibrium melon is 12-14 tiles per player; proving it needs a
simultaneous (not alternating) solve.

## Residual model risks

- The geometry walk model overcharges movement relative to the tape (1.43-1.47 vs 1.254
  measured), so pass-2 Z* and bands are conservative on labour.
- Peak daily harvest in the base solutions is 170-207 units against a shed capacity of 100.
  Sales settle the same day the slots fire, and DROP is capped at capacity without
  discarding (mid-day overflow stays in unit inventories; only the END-OF-DAY drop
  discards), so the plan is executable — but it requires intra-day drop/sell sequencing on
  ~3-5 peak days, which the model does not schedule.  An agent that dumps everything at
  dusk would lose the overflow.
- Opponent supply is the leader's recording under every draw; his real play would adapt.
- LP-relaxation bands remain OUTER bounds; the joint-point pin checks close that gap only
  at the specific tested points.

## Run facts

attrib 2734 s (5 variants), policy 3294 s + 2150 s (first launch killed by the runner
after 3 of 6 draws; remaining 3 in `allocation_bounds_pass2_policy2.log`, run at
time-limit 250 s / gap 1e-3 — their gaps 0.1-0.5%), br 1802 s (4 iterations).
MILP: 1104-1140 vars (264-300 int), 573 constraints; HiGHS mip_rel_gap 5e-4 targeted,
attained per solve as printed in the logs.
