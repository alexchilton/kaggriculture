# Does herd placement geometry cost us turns? Measured, not restated.

Two fresh loss episodes, both never analysed before this doc: `91229682` (seed 73957860, us seat
0 vs `Shivam_2212`, final money 61,427 vs 94,412) and `91231728` (seed 1153474158, us seat 1 vs
`As Wasti`, final money 89,433 vs 98,581).
We lose both.

**Answer up front: geometry is not a lever here either.** It replicates the existing verdict in
`docs/REGISTER.md` C-21 and `experiment_log.md` §21 on two episodes nobody had looked at before.
The shape difference (smeared vs compact) is real and confirmed below.
The cost it was assumed to carry is not there: on both episodes our walk-per-work-op ratio is
*better* than the opponent's despite our *worse* geometry, and total realized walking is
comparable to or lower than theirs.

All numbers below come from `/private/tmp/claude-501/-Users-alexchilton-DataspellProjects-kaggriculture/5fb520ea-bfb5-460d-aaa7-d7f197a84d9e/scratchpad/geom_analysis.py`,
run directly against the two episode JSONs.
Positions and rules are cross-checked against `reference/kaggriculture.py`
(`_shed_access_tiles`, `_apply_unit_action`, `FARMER_MOVES`).

## 1. Per-op action counts, both seats, both episodes

Classification: the four cardinal ops (`NORTH`/`SOUTH`/`EAST`/`WEST`) are folded into `MOVE`;
every other op (including `PASS`) is counted under its own name.
Counts are **submitted** actions (farmer + all hands, every turn of the 720-step episode), not
actions that resolved legally — that matches how the rest of this project's docs count ops.

### Episode 91229682 (us = seat 0 `alex chilton`, opp = seat 1 `Shivam_2212`)

| op | us | opp |
|---|---:|---:|
| BUILD_PASTURE | 21 | 14 |
| CARE | 457 | 308 |
| COLLECT_FERTILIZER | 471 | 296 |
| DIG | 33 | 27 |
| DROP | 162 | 56 |
| FEED | 442 | 300 |
| FERTILIZE | 77 | 84 |
| HARVEST | 346 | 361 |
| MOVE | 3011 | 2940 |
| PASS | 1512 | 1005 |
| PICKUP | 357 | 145 |
| PLACE | 21 | 14 |
| PLANT | 81 | 174 |
| WATER | 578 | 930 |
| **TOTAL** | **7569** | **6654** |

MOVE share: us 3011/7569 = **39.8%**, opp 2940/6654 = **44.2%**.
**Our MOVE share is lower, not higher**, despite worse pen geometry (below).

### Episode 91231728 (us = seat 1 `alex chilton`, opp = seat 0 `As Wasti`)

| op | us | opp |
|---|---:|---:|
| BUILD_COOP | 0 | 4 |
| BUILD_PASTURE | 21 | 10 |
| CARE | 342 | 274 |
| COLLECT_FERTILIZER | 365 | 289 |
| DIG | 28 | 21 |
| DROP | 189 | 49 |
| FEED | 323 | 289 |
| FERTILIZE | 78 | 76 |
| HARVEST | 313 | 372 |
| MOVE | 3134 | 4189 |
| PASS | 1746 | 354 |
| PICKUP | 301 | 161 |
| PLACE | 20 | 14 |
| PLANT | 81 | 163 |
| WATER | 590 | 1133 |
| **TOTAL** | **7531** | **7398** |

MOVE share: us 3134/7531 = **41.6%**, opp 4189/7398 = **56.6%**.
Here the opponent's MOVE share is dramatically *higher* than ours, and the opponent has the
*better* pen geometry (below) — the exact opposite of what "geometry drives MOVE share" predicts.

**Note on `alex chilton`'s seat.** In `91229682` we are seat 0; in `91231728` we are seat 1
(`As Wasti` is seat 0). An earlier pass of this script labelled columns "us(0)/opp(1)" unconditionally
and would have silently reported `As Wasti`'s numbers as "us" for the second episode. Fixed by
resolving the seat from `info.TeamNames.index("alex chilton")` before printing anything; every
table above is seat-corrected.

**Biggest divergence in both episodes is not MOVE — it's PASS and WATER.** We pass 1.5-1.7x more
than the opponent (1512 vs 1005, and 1746 vs 354 — the second one is enormous), and the opponent
waters 1.6-1.9x more than us (930 vs 578, 1133 vs 590) and plants more (174 vs 81, 163 vs 81).
That is a production/idle story, not a walking story, and it is outside this task's scope — flagged
here only because it is where the real gap visibly sits.

## 2. Realized walking distance and shed distance

### Shed position, verified against source

`reference/kaggriculture.py` `_shed_access_tiles(board_size)`: for `boardSize=10` (the configured
value in both episodes — `d["configuration"]["boardSize"] == 10`, asserted in the script), the four
shed-access tiles are `(4,4), (5,4), (4,5), (5,5)`. `farmer` spawns at `(4,4)`
(`_default_spawn`), which matches both episodes' step-0 observation. Shed distance for a pen is
the Manhattan distance to the *nearest* of these four tiles — this is a real, non-degenerate
number in every table below (ranges below are `[0,7]`, `[0,2]`, `[0,4]`, `[0,3]`, never all-zero).
This directly answers the "verify sheds aren't 0" instruction: they are not; the earlier sheds=0
run was a different bug, not present here.

### Pen geometry at final state (day 30)

| episode | side | pens | centroid | ring-depth (Manhattan) | mean shed-dist | shed-dist range | sum shed-dist |
|---|---|---:|---|---:|---:|---|---:|
| 91229682 | us | 21 | (3.43, 3.90) | 3.25 | 2.86 | [0,7] | 60 |
| 91229682 | opp | 14 | (4.36, 3.57) | 1.90 | 1.21 | [0,2] | 17 |
| 91231728 | us | 16 | (3.44, 4.25) | 2.74 | 2.19 | [0,4] | 35 |
| 91231728 | opp | 14 | (4.50, 3.00) | 1.93 | 1.57 | [0,3] | 22 |

Our pens: `91229682` tiles = `(0,1),(0,3),(0,4),(1,3),(1,4),(2,3),(2,4),(2,7),(3,2),(3,3),(3,4),
(3,8),(4,4),(4,5),(4,8),(5,3),(5,4),(6,3),(7,3),(8,3),(9,3)` — the row-3 smear from x=0 to x=9 the
task described is confirmed exactly, and the "stray pen" reads as `(2,7)`/`(4,8)`/`(3,8)` rather
than literally `(7,2)`, likely a transposition in the earlier note; same phenomenon either way.
Opponent tiles = `(2,4),(3,3),(3,4),(3,5),(4,2),(4,3),(4,4),(4,5),(5,2),(5,3),(5,4),(6,3),(6,4),
(7,4)` — the compact x:2-7, y:2-5 block, also confirmed.

Pen geometry is fixed early and never revisited: sweeping the pen count/ring-depth every 2 days
from day 0 to day 30 on `91229682` shows the ring stabilises at 3.25 (us) / 1.90 (opp) by day 16
and does not move again — pens, once built, don't move, so whatever the sweep handed out in the
first ten days is locked in for the rest of the season.

**Correction to the pre-existing "1.86 vs 2.93" figure.** Recomputing ring-depth (mean Manhattan
distance of a pen from its own herd's centroid, exactly as defined in the task) from the final
board state, and independently at every 2-day checkpoint from day 0 to day 30, never produces
1.86 for us or 2.93 for them — the closest values found are 3.25 (us) / 1.90 (opp), which is the
**same direction** as the qualitative claim (we are more spread out) but **opposite magnitude
ordering** from the quoted numbers. A Euclidean version of the same metric gives 2.69 (us) / 1.50
(opp) — still the same direction, still not 1.86/2.93. The qualitative shape claim (smear vs
block) holds up; the specific "1.86 vs 2.93" pair does not reproduce under either metric tried and
should not be cited going forward. This doc's numbers (3.25/1.90 Manhattan) are the ones to use.

### Realized walking distance (Manhattan, farmer + all hands, position-diffed from observations — not submitted-MOVE counts, so blocked/no-op moves don't inflate it)

| | 91229682 us | 91229682 opp | 91231728 us | 91231728 opp |
|---|---:|---:|---:|---:|
| total realized walk | 3131 | 3029 | 3208 | 4125 |
| work-ops (everything except MOVE/PASS) | 3046 | 2709 | 2651 | 2855 |
| **walk per work-op** | **1.028** | 1.118 | **1.210** | 1.445 |

Per-day breakdown (both episodes, day 0-30) and the full per-hand-per-day walking table for our
side are in the raw script output, reproduced at the bottom of this doc for the record.

**This is the decisive number.** Walk-per-work-op normalises out the fact that we simply submit
more total actions than the opponent (7569 vs 6654 in episode 1, "we take more total actions than
they do but produce less" per the task's own framing). If geometry were costing us turns, this
ratio should be *worse* for us, given our pens sit measurably farther from the shed (mean 2.86 vs
1.21, and 2.19 vs 1.57). It is **better** for us in both episodes: 1.028 vs 1.118, and 1.210 vs
1.445. In episode 91231728 the opponent — who has the *better* geometry — walks *more* in both
absolute (4125 vs 3208) and normalised (1.445 vs 1.210) terms. That is the opposite sign from
what the geometry-cost hypothesis needs.

## 3. Verdict: real lever or pretty picture?

**Pretty picture. A correct no, on two fresh episodes that replicate the existing closed finding.**

- MOVE share is lower for us in both episodes despite worse geometry (39.8% vs 44.2%; 41.6% vs
  56.6%).
- Walk-per-work-op is better for us in both episodes despite worse geometry (1.028 vs 1.118;
  1.210 vs 1.445).
- Total realized walking is roughly level in episode 1 (3131 vs 3029, +3.4%) and *lower* for us in
  episode 2 (3208 vs 4125, -22%) — in the episode with the bigger geometry gap.
- We lose both games regardless.

This is the same conclusion `docs/REGISTER.md` C-21 already recorded ("His exact tiles buy 2 cells
of 150... FALSE") and the same one `router.py`'s `DEPOT_RING_FIRST` docstring recorded from a
season-long measurement: *"we already walked 3,460 turns against the tape's 4,025 and idled 1,426
against its 999, so the crew was never turn-starved by distance... The season's money rides on one
or two animals, and shuffling the ground moves that in both directions for reasons that have
nothing to do with walking."* Two independent episodes, a different metric (walk-per-work-op
instead of season cell counts), and the same answer.

What actually separates the two sides in these episodes is production volume and idle time — PASS
1512 vs 1005 and 1746 vs 354, WATER 578 vs 930 and 590 vs 1133, PLANT 81 vs 174 and 81 vs 163 — not
where the pens sit. That is outside this task's scope but is where a follow-up should look if the
goal is closing the money gap, not the shape gap.

## 4. Where pen placement is actually decided, and what would have to change

Pen siting happens in `kagg/search/schedule_agent.py`, function `_refresh_pins` (~line 1672-1710),
in the `while have < want_pens:` loop. For each pen the schedule calls for, the site is chosen by
falling through, in order:

1. `PEN_SPOTS` (line 634) — a fixed priority list of tiles to fill before anything else.
   **Currently `PEN_SPOTS = ()`** — empty, shipped off. The docstring above it records that filling
   it with the opponent's own day-0 tiles measured a 2-cell difference out of 150 and is not worth
   carrying.
2. `R.shed_access_tiles()` — the four tiles literally touching the shed (`(4,4),(5,4),(4,5),(5,5)`)
   if one is free.
3. **Only if `PEN_NEAREST_DEPOT` is `True` (it is `False`, line 668) or the current day is
   `>= PEN_NEAREST_DEPOT_FROM_DAY` (currently `11`, line 717)** — `_nearest_ground(order, tiles,
   taken, unlocked)`, which picks the free tile closest to any owned depot across the whole board
   (line 1484).
4. Otherwise, `_next_ground(order, tiles, taken)` (line 1463) — the next free tile in
   `router.field_order`'s **quadrant-major boustrophedon sweep**, the same order crops are placed
   in. This is the fallback that actually fires for every pen built before day 11, and it is why
   the smear happens: the sweep fills a quadrant's near rows with crops first, so a pen requested
   once the near ground is already planted lands at the tail of the sweep — which is how our herd
   ends up walking out to `(7,3),(8,3),(9,3)` while `PEN_NEAREST_DEPOT_FROM_DAY` hasn't kicked in
   yet.

This is not a new mechanism — it is `router.DEPOT_RING_FIRST` (line 472, for crop/field-tile
ordering) and its pen-specific sibling `PEN_NEAREST_DEPOT` / `PEN_NEAREST_DEPOT_FROM_DAY`
(schedule_agent.py lines 668/717), both already tried and both already shipped in their current
state for measured reasons — not oversights:

- `PEN_NEAREST_DEPOT = True` (always nearest-first) was tried and reverted: it *does* what it
  claims — no pen beyond 5 steps at day 11 — but the project's own scoring metric at the time
  (cell-count resemblance to the opponent's tape) penalised it, because the opponent's own day-0
  block happens to sum to less distance under nearest-first than under our current sweep. The
  docstring explicitly flags this as unresolved: *"this is the first arm in the project that is
  plausibly right and is refused by the objective rather than by the board. It should be
  re-measured on BANK, head to head, before it is written off."* — i.e. nobody has actually checked
  whether it wins money or games; it was killed by a proxy metric, not a bank/win-rate test.
- `PEN_NEAREST_DEPOT_FROM_DAY = 11` (nearest-first, but only from day 11 onward) is what currently
  ships. It was chosen because the damage from switching earlier lands on days 0-8, where our
  layout already matches the tape's distance exactly (22 vs 22), while the benefit only shows up
  from day 8-10 onward once crop tiles have already eaten the near ground.
- `router.DEPOT_RING_FIRST` (the field-order-level version, applying to crops too) is `None`
  (off) for a different, already-settled reason: turning it on always reversed sign between tuning
  seeds (+20,526) and held-out seeds (-11,111) — a winner's-curse null, not a proven loss.

**What would have to change, concretely, to test this properly:** set `PEN_NEAREST_DEPOT = True`
(or lower `PEN_NEAREST_DEPOT_FROM_DAY` toward 0) and re-run the arena/ladder evaluation on
**bank and win rate**, not the cell-count-vs-tape proxy that killed it originally — that re-test is
explicitly still open per the docstring's own words. Given what section 3 measured here (walking is
not the binding cost even with the current worse geometry), the expected effect of doing this is
small to nil on money, and this doc does not recommend spending time on it: the existing
season-long measurement (`experiment_log.md` §21) already found the two arms that moved pens
nearest-first cost a win in one seed and reversed sign on a held-out draw, i.e. it is not free even
if it is not clearly harmful either. Task #32 ("a pen keeps the animal it was built for",
`router.PEN_KEEPS_ITS_ANIMAL`) is unrelated — it fixes which *animal* a built pen receives, not
*where* the pen is built, and nothing in this investigation touched it.

## Appendix: raw per-day walking tables

### Episode 91229682 — realized walking distance by day (Manhattan, farmer+hands)

```
day        us     opp
0          42      53
1          20       8
2          43      34
3          55      19
4          80      54
5          81      19
6          86      35
7         107     100
8         123      64
9         140      93
10        120      93
11        138     133
12        138      79
13        105     119
14        127      67
15        124     119
16        132     115
17        134     146
18        130     115
19        134     144
20        117     145
21        130     130
22        115     139
23        131     165
24        111     164
25        117     137
26        124     109
27        106     147
28        111     112
29         10     172
30          0       0
TOT      3131    3029
```

### Episode 91231728 — realized walking distance by day (Manhattan, farmer+hands)

```
day        us     opp
0          42      49
1          20      62
2          43     137
3          55     123
4          80     128
5          67     124
6         114     131
7         102     140
8         122     137
9         124     156
10        117     132
11         95     158
12        169     166
13        157     143
14        139     153
15        150     149
16        141     155
17        128     142
18        133     141
19        136     154
20        112     144
21        127     142
22        120     126
23        120     145
24        118     146
25        111     140
26        120     132
27        129     150
28        113     155
29          4     165
30          0       0
TOT      3208    4125
```

Per-hand-per-day walking distance (our side, both episodes) is in the script output; omitted here
for length since the season totals and work-ratio above already carry the finding — available by
re-running `geom_analysis.py` if a specific hand/day needs auditing.
