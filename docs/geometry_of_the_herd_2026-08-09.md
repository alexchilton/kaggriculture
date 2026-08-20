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

---

# Consolidated herd/animal findings

The sections below fold in five more docs on herd mechanics: feeding cadence, milk timing, wool
delivery, and the geese question.
Each is dated and marked with its source file.
Numbers, tables and code excerpts are kept verbatim; only prose is reflowed to one sentence per
line.

## 2026-08-10 — How Seb feeds seven animals on day 4

Folded in from docs/how_seb_feeds_the_herd.md.

> **TARGET SUPERSEDED, added 2026-08-11.**
> Seb's tape was optimal under the OLD `townCenterSellInterval=12` economy; his median bank halved
> and he has since withdrawn from the ladder (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder
> seats).
> The route mechanics below are still an accurate reading of the recorded tape — only the choice
> to imitate this particular herd and feed cadence, rather than the field's, is now in question.

Read straight off tape 91422988, seed 11, Seb's own seat, day 4.
He scores `FEED 7`, `CARE 7`, `PLACE 1`, `COLLECT_FERTILIZER 6`.
We score `FEED 5`, `CARE 5`, `PLACE 1` from the same board.

### The shape of his day

Three pickups, all in the first two hours, on three different hands:

```
h1  u1  PICKUP WHEAT 3
h2  u2  PICKUP WHEAT 3
h2  u6  PICKUP COW 1
```

Seven drops, none of them before hour 18:

```
h18 u7 | h21 u2, u3, u6 | h22 u5 | h23 u0, u1
```

The shed runs `6 -> 3 -> 1` in the first two hours and sits on 1 until h18, when the harvest
lands.
He empties it deliberately and never goes back.

### Three roles, not one

**u1 — wheat carrier A.** Draws 3 at h1, spends them walking outward.

```
h1 (4,4) PICKUP W3   h2 (4,4) FEED   h4 (4,3) FEED   h7 (3,2) FEED
h8 (3,2) CARE  h9 (3,2) COLLECT_FERTILIZER  then crop work to dusk
```

**u2 — wheat carrier B.** Draws 3 at h2, sweeps a different arc.

```
h2 (4,4) PICKUP W3   h5 (3,3) FEED   h9 (2,2) FEED   h14 (1,3) FEED
with CARE and COLLECT_FERTILIZER at each, then south to the shed
```

**u6 — animal carrier and CARE sweeper.** Draws the COW at h2 and carries it for ten hours, doing
the ITEMLESS work at every pen it passes on the way.

```
h2 (4,4) PICKUP COW 1
h3 (4,4) CARE            h4 (4,4) COLLECT_FERTILIZER
h6 (4,3) CARE            h7 (4,3) COLLECT_FERTILIZER
h9 (3,3) COLLECT_FERTILIZER
h12 (1,3) PLACE COW      then walks on -- h13 (0,3) WEST, h14 WATER, h15 HARVEST
```

### The three rules this implies

1. **Load once, in parallel, at dawn.** Two carriers take the whole shed between them in hours 1
   and 2. There is no second trip and no mid-day `DROP`, so no wheat is ever put back into a shed
   that another hand has already emptied.

2. **The hand with no wheat does the work that needs no item.** CARE costs nothing to carry, so
   the animal carrier pays for its long walk by caring for every pen it crosses. Our herd hand
   does FEED, CARE and COLLECT at one tile and then moves.

3. **A pen's day is SPLIT ACROSS HANDS, and the feed arrives after the placement.** u6 places the
   cow at `(1,3)` at h12. It does not feed it. **u2 feeds it at h14**, two hours later, on a wheat
   drawn at h2 for a pen that had no animal in it at the time.

### Why rule 3 matters here

`crew.cover`'s docstring states the opposite as a design principle:

> **The unit of ownership is the TILE, not the op.**
> A pen's whole day -- build it, put the animal in, feed it, care for it, take the fertilizer --
> belongs to one hand.

The second justification given for it is exactly the case Seb solves differently:

> an animal placed today must be FED today, and `build_nodes` cannot emit a FEED for a tile until
> an animal is standing on it, so the feed is invisible at plan time

Seb's answer is not to give the pen to one hand.
It is to send a **second** hand, already carrying wheat, past the pen *later in the day* than the
hand that filled it.
The feed is not invisible to him because it is not planned as part of the placement at all -- it
is one stop on a wheat carrier's sweep, and the sweep is timed to arrive after the placement.

Tile ownership is not wrong -- it fixed a real pairing failure (`place 3/4`, `feed 3/4`, d3 bank
$28 against $478).
But it is what forces the placing hand to carry its own feed, which is what forces the mid-tour
re-supply `DROP`, which is what loses the wheat.

### What it costs us on day 4

Our herd hand u4 does all three roles alone:

```
h1 PICKUP COW 1   h2 PICKUP WHEAT 4   h3 FEED (4,4)   h4 CARE
h6 DROP           h7 PICKUP COW 1     h8 PICKUP WHEAT 1   <- asked 3, got 1
h10 FEED (4,3)    h11 CARE            h14 PLACE COW (3,3)   <- arrives empty
h15 walks off; the cow is never fed or cared for
```

`DROP` is all-or-nothing (`kaggriculture.py:333`), so the h6 re-supply dumps the cow too and pays
to pick it up again.
By h8 the shed holds 1 wheat, the leftover want is deleted (`schedule_agent.py:1761`), and the
shed is bare from h9 to h18 -- so `FETCH_THE_FEED_AND_RETURN` cannot fire either.

Wheat ledger, both sides: 6 in the shed at dawn, 1 bought during the day, 7 animals.
**He buys exactly what we buy.**
He is not better funded; he simply never spends a wheat on a round trip.

### Open questions from this doc

- Seb performs 7 FEEDs having drawn only 6 wheat.
  u7 feeds `(2,3)` at h7 without ever visiting the shed, so it began the day holding wheat.
  Not yet confirmed whether the midnight sweep (`_drop_inventories_to_shed`) leaves a remainder in
  hand or whether the seventh wheat comes from somewhere else.
- Between our h6 `DROP` and our h8 re-pickup, one wheat AND the collected fertilizer both
  disappear from the shed.
  Either the drop overflowed shed capacity -- overflow is discarded outright
  (`kaggriculture.py:340`) -- or another hand drew them.
  Not yet separated, and it matters: if it is capacity, the round trip is destroying goods, not
  merely costing turns.

## 2026-08-11 — The d7 tenth feed: the dawn wheat block is dropped for a full order queue

Folded in from docs/fable_the_d7_feed_2026-08-11.md.

Fable, 2026-08-11.
Worktree `agent-a3a2da1c905101655`, branch reset to `9bc5a6d` ("Do not queue the day's ration
behind the parcel"), plus the one uncommitted fix described below in
`kagg/search/schedule_agent.py`.
Everything measured on seed 11, Victor tape, via `python -u scripts/breakdown.py --module
schedule_agent --tape victor --days 12`.

### Verdict in one paragraph

Alex's hypothesis was right: the answer is the market cadence, not a wait at the depot.
The dawn plan sizes the h00 wheat order at the whole 14-unit row (`BUY_THE_ROW_AT_DAWN`), the bank
covers it ($2,512 with the same turn's wool pending), and the order is then **dropped on the
floor** because d7's h00 queue already holds ten orders — `SELL WOOL`, `SELL FERTILIZER`, seven
`HIRE`s and the `BUY_ANIMAL COW 2` — and the append is gated on `len(orders) < 9`.
`state["ordered"]` is honest here (nothing was credited), but from h01 the boost is gone (`hour ==
0`), so the row falls back to `BUY_DRIP = 1` per turn and fourteen wheat arrive one an hour
through h15.
The crew's depot draws at h02-h05 outpace that drip, u4's want is deleted against a momentarily
empty shed, and the day closes `feed 9/10`, `care 9/10`, `collect_fert 6/7`.
The fix keeps the dawn boost live until the block is actually queued; it goes out whole at h01 —
which is byte-for-byte the tape's own cadence, since Victor's h01 queue is also exactly ten and he
ships `BUY_PRODUCT WHEAT 6` as a block at h02, his first turn with a free slot.
d7 now matches on every op row this investigation owns; d0-d6 are **byte-identical** to baseline.

### 1. The traced mechanism

Instrumented buy block, d7 hour by hour (`data/logs/fable_d7_buytrace.log`):

```
FABLEBUY d7 h00 money=2512.0 quote=33 owed=14 herd=-12 short=14 shedW=2 ordered_buys=0 norders=10   <- refused: no slot
FABLEBUY d7 h01 money=2207.0 quote=34 owed=14 herd=-12 short=1  shedW=2 ordered_buys=0 norders=2
FABLEBUY d7 h02 money=1343.0 quote=34 owed=13 herd=-14 short=1  shedW=0 ordered_buys=1
... one wheat per hour ...
FABLEBUY d7 h15 money=892.0  quote=35 owed=0  short=0  shedW=10 ordered_buys=14
```

`short=14` at h00 says the sizing and the funding were both correct; `norders=10` says the append
gate `len(orders) < 9` refused it.
Note `money=2512` at h00 — `SELLS_FUND_THE_TURN` had already credited the wool, so "the bank was
thin" is NOT the story; the queue was full.

The crew side (`data/logs/fable_d7_deltrace.log`, `fable_d7_day_ops.log`):

```
h00  u0 draws WHEAT 3 (dawn shed 5 -> 2)
h01  buy drip 1 fills end of turn -> shed 3 at h02
h02  u1 (earlier in unit order) takes 3 of its 4 -> shed 0
h02  FABLEDEL u4 item=WHEAT want=3 shed=0 critical=False        <- the whole want, deleted
h02-h04  u4 walks its tour wheatless; its first pen still offers COLLECT_FERTILIZER,
         so `_live_ops` is non-empty and `FETCH_THE_FEED_AND_RETURN` (which fires only on
         an EMPTY ops list) never triggers there -- that pen's FEED is dropped silently
h05  at the next pen the fetch DOES fire, sizes its draw off FEEDs still in the route
     (1 underfoot + 1 ahead = 2, not 3), takes 2, feeds two pens
net  feed 9/10; care 9/10 because `router.animal_ops` offers CARE only on a pen it feeds;
     collect_fert 6/7 because the unplanned round trip eats the tour's tail
```

Two corrections to the working framing in the task brief, both from the trace:

- The deletion is at **h02, and it is the whole want (3), not a post-draw remainder of 1**.
  u4's h05 `PICKUP WHEAT 2` is not the planned depot stop short-changed; it is
  `FETCH_THE_FEED_AND_RETURN` inserting a new stop, correctly sized for the two FEEDs still
  visible in the route.
  The third FEED was already lost at h02-h04, before the fetch could see it.
- The reverted attempts extending `WAIT_FOR_THE_MORNING_DELIVERY` never touched `feed 9/10`
  because waiting at the depot only helps if the wheat comes; at 1/turn against three drawing
  units it does not come in time whatever the hand does.
  The defect is upstream of the depot.

### 2. Where else the same drop fires (`data/logs/fable_allday_h00_trace.log`)

```
d0  h00 norders=8   sent (11 wheat, one block)      d7  h00 norders=10  DROPPED
d1  h00 owed=0      nothing to send                 d8  h00 norders=9   DROPPED (gate is < 9)
d2  h00 norders=3   sent                            d9  h00 norders=10  DROPPED
d3  h00 norders=5   sent (money-shrunk to 3)         d10 h00 norders=15  short=0 (land-turn skip)
d4  h00 norders=4   sent                             d11 h00 norders=10  DROPPED
d5  h00 norders=8   sent                             d12 h00 norders=10  DROPPED
d6  h00 norders=6   sent (money-shrunk to 3)
```

Every day from d7 with a big hire row drops its dawn block, and d8/d9's `feed 11/12`, `care 11/12`
carry the same signature.
A second `FABLEDEL` fires on d10 (u12, want 1).
Those days are beyond this investigation's frontier and were not chased; the fix reaches them by
construction, and the measured d8-d11 movement is toward the tape (below).

### 3. The fix

`kagg/search/schedule_agent.py`, two lines of logic plus the daily reset:

- The `BUY_THE_ROW_AT_DAWN` boost condition `hour == 0` becomes `not
  state.get("dawn_row_sent", False)` — the boost stays live until the block is queued.
- `state["dawn_row_sent"] = True` is set at the append — even for a partial send shrunk by the
  money guard (today's thin-bank behaviour, unchanged), never by the slot gate refusing it.
- `dawn_row_sent=False` joins the daily `state.update(...)` reset.

Deliberately narrow: a day whose h00 block goes out (all of d0-d6) is bit-identical, because the
h00 append sets the flag exactly where `hour == 0` used to expire.
Only a day refused for a full queue changes, and it changes into the tape's own shape: the block
goes out whole on the first turn with a free slot.
On d10 the land-turn skip zeroes `short` before the append, so the flag stays unset and the row
now goes out as a block once the parcel's turn is over — previously it dripped; this is the one
behavioural change beyond the refused-queue days, and it moved d10 toward the tape (`harvest 5/6
-> 6/6`, `money 3719 -> 5230` against 5630).

Test: `tests/test_the_dawn_row_survives_a_full_queue.py` — asserts the d7 row is fully queued by
the end of h01.
Red at baseline (`queued only 1 of the 14-wheat row ... per hour {h1..h14: 1 each}`), green with
the fix, and red again with the fix reverted to `hour == 0` (checked both directions).
The assertion is on the ORDERS deliberately: the defect is on the offer side, one line before any
fill exists, and the fill follows from a $2,207 bank against a ~$480 order.

### 4. The grid, before and after

Baseline (`data/logs/fable_d7_baseline_grid.log`):

```
                       d0           d1           d2           d3           d4           d5           d6           d7           d8           d9          d10          d11
money               15/15        14/14      188/182      203/196      560/554      529/528        57/28      892/766       224/97    4139/1980    3719/5630    5933/6856
tiles               25/25        25/25        25/25        25/25        25/25        25/25        50/50        50/50        50/50        50/50        75/75        75/75
pens                  5/5          5/5          5/5          5/5          5/5          6/6          8/8        10/10        12/12        12/12        12/12        12/12
weeds                 0/0          0/0          0/0          0/0          0/0          0/0          0/0          0/0          0/0          1/0          2/0          2/0
wheat                 5/5          5/5          5/5          6/6          6/6          7/7          7/7        10/10        15/13        13/13        12/13        13/13
strawb                0/0          0/0          0/0          3/3          3/3          7/7          8/8        18/18        18/20        19/20        30/31        32/36
melon                 5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5         4/12        12/14
cow                   1/1          1/1          1/1          1/1          1/1          2/2          3/3          6/6          7/8          7/8          8/8          8/8
sheep                 4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4

plant               10/10          0/0          0/0          4/4          5/5          5/5          1/1        14/14         8/10          3/1        14/23        14/11
water               10/10          0/0        10/10          9/9        15/15          9/9        12/12        33/33        16/22        29/28        31/43        43/41
harvest               0/0          0/0          0/0          0/0          5/5          0/0          4/4          1/1          4/6          5/5          5/6          3/4
feed                  5/5          0/0          5/5          5/5          5/5          6/6          7/7         9/10        11/12        11/12        11/12        12/12
care                  5/5          0/5          5/5          5/5          5/5          6/6          7/7         9/10        11/12        11/12        11/12        12/12
collect_fert          0/0          5/5          5/5          5/5          5/5          5/5          6/6          6/7        10/10        11/12        11/12        12/12
dig                   0/0          0/0          0/0          0/0          0/0          0/1          0/0          0/1          0/0          2/0          0/0          0/1
build_pastur          5/5          0/0          0/0          0/0          0/0          1/1          2/2          2/2          2/2          0/0          0/0          0/0
place                 5/5          0/0          0/0          0/0          0/0          1/1          1/1          3/3          1/2          0/0          1/0          0/0
pickup                5/4          0/0          2/2          2/2          2/2          3/3          8/4          6/5          7/5          6/4          6/4          6/4
drop                  0/0          3/0          2/0          2/0          1/0          2/0          4/1          2/0          4/0          5/0          6/5          4/0
pass                44/48        31/28        12/21        31/27         2/18        12/27         12/5        23/22         8/23        17/44        84/78        16/57
sell                  6/6          0/0          5/5          5/5          5/5        22/22        13/13        18/18          9/9        42/29        30/55        21/18
buy_seed            10/10          0/0          0/0          4/4          5/5          5/5          4/4        11/12        10/10          1/1        31/31          3/4
buy_product         11/11          0/0        11/11          5/5          2/2          7/7          5/5        14/14          7/7        10/10        12/12          6/6
buy_animal            5/5          0/0          0/0          0/0          0/0          1/1          2/2          2/2          2/2          0/0          0/0          0/0
buy_land              0/0          0/0          0/0          0/0          0/0          0/0          1/1          0/0          0/0          0/0          1/1          0/0
hire                  4/4          1/1          2/2          3/3          3/3          3/3          4/4          7/7          6/6          7/7        14/14        10/10
```

With the fix (`data/logs/fable_d7_fixed_grid.log`, reproduced byte-identically by the cleaned tree
in `fable_d7_final_grid.log`):

```
                       d0           d1           d2           d3           d4           d5           d6           d7           d8           d9          d10          d11
money               15/15        14/14      188/182      203/196      560/554      529/528        57/28      896/766       229/97    4155/1980    5230/5630    7497/6856
tiles               25/25        25/25        25/25        25/25        25/25        25/25        50/50        50/50        50/50        50/50        75/75        75/75
pens                  5/5          5/5          5/5          5/5          5/5          6/6          8/8        10/10        12/12        12/12        12/12        12/12
weeds                 0/0          0/0          0/0          0/0          0/0          0/0          0/0          0/0          0/0          1/0          2/0          2/0
wheat                 5/5          5/5          5/5          6/6          6/6          7/7          7/7        10/10        15/13        13/13        12/13        12/13
strawb                0/0          0/0          0/0          3/3          3/3          7/7          8/8        18/18        18/20        19/20        30/31        33/36
melon                 5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5          5/5         4/12        11/14
cow                   1/1          1/1          1/1          1/1          1/1          2/2          3/3          6/6          7/8          7/8          8/8          8/8
sheep                 4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4          4/4

plant               10/10          0/0          0/0          4/4          5/5          5/5          1/1        14/14         8/10          3/1        15/23        13/11
water               10/10          0/0        10/10          9/9        15/15          9/9        12/12        33/33        18/22        29/28        32/43        42/41
harvest               0/0          0/0          0/0          0/0          5/5          0/0          4/4          1/1          4/6          5/5          6/6          3/4
feed                  5/5          0/0          5/5          5/5          5/5          6/6          7/7        10/10        11/12        11/12        11/12        12/12
care                  5/5          0/5          5/5          5/5          5/5          6/6          7/7        10/10        11/12        11/12        11/12        12/12
collect_fert          0/0          5/5          5/5          5/5          5/5          5/5          6/6          7/7        10/10        11/12        11/12        12/12
dig                   0/0          0/0          0/0          0/0          0/0          0/1          0/0          0/1          0/0          2/0          0/0          0/1
build_pastur          5/5          0/0          0/0          0/0          0/0          1/1          2/2          2/2          2/2          0/0          0/0          0/0
place                 5/5          0/0          0/0          0/0          0/0          1/1          1/1          3/3          1/2          0/0          1/0          0/0
pickup                5/4          0/0          2/2          2/2          2/2          3/3          8/4          5/5          5/5          4/4          6/4          6/4
drop                  0/0          3/0          2/0          2/0          1/0          2/0          4/1          2/0          2/0          4/0          7/5          4/0
pass                44/48        31/28        12/21        31/27         2/18        12/27         12/5        21/22         6/23        20/44        79/78        19/57
sell                  6/6          0/0          5/5          5/5          5/5        22/22        13/13        18/18          9/9        42/29        37/55        22/18
buy_seed            10/10          0/0          0/0          4/4          5/5          5/5          4/4        11/12        10/10          1/1        31/31          3/4
buy_product         11/11          0/0        11/11          5/5          2/2          7/7          5/5        14/14          7/7        10/10        12/12          6/6
buy_animal            5/5          0/0          0/0          0/0          0/0          1/1          2/2          2/2          2/2          0/0          0/0          0/0
buy_land              0/0          0/0          0/0          0/0          0/0          0/0          1/1          0/0          0/0          0/0          1/1          0/0
hire                  4/4          1/1          2/2          3/3          3/3          3/3          4/4          7/7          6/6          7/7        14/14        10/10
```

Reading the diff (`diff fable_d7_baseline_grid.log fable_d7_fixed_grid.log`):

- **d0-d6: byte-identical**, every row, both tables.
- **d7: feed 9/10 -> 10/10, care 9/10 -> 10/10, collect_fert 6/7 -> 7/7.**
  `pickup 6/5 -> 5/5` and `pass 23 -> 21/22` come along (both exempt rows); money 892 -> 896/766.
- d8-d10 move toward the tape everywhere they move: d8 `water 16 -> 18/22`, d10 `harvest 5/6 ->
  6/6`, `money 3719 -> 5230` against 5630, d11 `plant 14 -> 13/11`, `water 43 -> 42/41`, `strawb 32
  -> 33/36`.
- Three cells past the frontier move away by one: d11 `sell 21 -> 22/18`, d11 board `wheat 13/13
  -> 12/13`, `melon 12 -> 11/14`.
  d11 sits behind d8's `feed 11/12` and d10's `plant 15/23`, so by the days-in-order rule these are
  inherited noise on a diverged board, not regressions of matched ground.

### 5. The new frontier

In order: d1 `care 0/5` (we are right — the reference banks the care bonus only on a fed animal,
`kaggriculture.py:816`), the no-op digs (d5/d7/d11, tape digs an empty tile), then **d7 `buy_seed
11/12`** — present at baseline, untouched here, and now the first live op divergence — then d8
(`plant 8/10`, `water 18/22`, `harvest 4/6`, `feed 11/12`, `care 11/12`, `place 1/2`).
d8/d9 still drop their dawn blocks' SIBLING signature (`feed 11/12`) for what the h00 trace says
is at least partly the same class — d8's h00 queue holds 9 — but their remaining gap survives this
fix, so something else is also owed there.

### 6. What was NOT the answer, for the register

- **A wait at the depot** (the two reverted `WAIT_FOR_THE_MORNING_DELIVERY` extensions): the wheat
  does not arrive inside the window a waiting hand has, because the drip is 1/turn against three
  drawing units.
  Upstream cadence, not downstream patience.
- **Marking the FEED draw critical**: would have stood u4 at the shed from h02 collecting the drip
  one unit at a time, deforming the tour the same way the measured d4/d5 regressions did.
  Not attempted once the h00 trace showed the block was affordable and refused.
- **Re-slotting the queue** (wheat ahead of the cow or a hire): the tape itself does not do this
  — Victor's h01 queue is the same ten orders ours is, and his wheat waits for h02.

### Artifacts

- Fix: `kagg/search/schedule_agent.py` (uncommitted; the `dawn_row_sent` flag, three edit sites,
  comment block at the boost).
- Test: `tests/test_the_dawn_row_survives_a_full_queue.py` (red at `9bc5a6d`, green with the fix,
  red again on revert — verified in both directions).
- Guards run: `test_the_dusk_topup_stays_inside_the_days_row.py`,
  `test_a_hire_waits_for_the_ground_that_frees_it.py`,
  `test_the_dawn_plan_owns_the_land_it_buys_today.py` — 31 passed, 34 skipped, 0 failed
  (`data/logs/fable_d7_guard_tests.log`).
- Logs: `data/logs/fable_d7_baseline_grid.log`, `fable_d7_fixed_grid.log`,
  `fable_d7_final_grid.log` (byte-identical to the previous — the cleaned tree reproduces its own
  measurement), `fable_d7_buytrace.log`, `fable_d7_deltrace.log`, `fable_allday_h00_trace.log`,
  `fable_d7_day_ops.log`, `fable_d7_sell_day.log`.
- Worktree housekeeping: this worktree was created at a stale 2026-08-03 commit and was reset to
  the task's stated `9bc5a6d`; `data/seed_scripts` is a symlink to the main repo's copy, and
  `scripts/day_ops.py` (untracked in the main repo) was copied in for the hour-by-hour trace.

## 2026-08-13 — Day 6: the stranded wool, found and fixed

Folded in from docs/d6_stranded_wool_2026-08-13.md.

Seed 11, kawashigi grid, weeds 0, recorded shop draw injected.
The d6 row asks `sells={'FERTILIZER': 5, 'WOOL': 12}` and the board produces 9 wool across two
shear jobs.
Baseline sold 10 of 17: the 5 fertilizer at h00 plus the 5 wool one hand dropped at h09.
The other 4 wool rode in a hand from h09 to dusk and reached the shed only via the overnight
sweep, after the market had closed.

### Why that hand's tour contained no shed stop

The hinted theory — a pen whose `yield_units` is 0 at dawn producing an empty `gives` — is NOT
what happens here.
Both sheep pens carry their wool on the board at dawn: (4,3) reads `yield_units 4` and (4,4) reads
`yield_units 5`, so both shear jobs predict their load (`predict_yield`) and `held` in
`materialise` is correct.

The plan (`cover.plan`, day 6, `deliver=False`, `rush=True`, `wanted={'WOOL': 12}`) gives the
shear at (4,3) to the hand that then feeds the cows at (0,0) and (1,0).
Every delivery rule in `materialise` declined that hand, each for its own documented reason:

- Rule 0 (`RUSH_BANK_MIN`) fires only on a hand that STARTS the tour loaded; this one starts
  empty.
- The free drop (`DROP_WHERE_THE_TOUR_ALREADY_STANDS`) and the re-draw
  (`REDRAW_RATHER_THAN_CARRY`) fire only at a zero-detour depot, and neither (4,3) nor anything
  after it is one — (4,3) is not a shed-access tile, and the shed-access set is
  `{(4,4),(4,5),(5,4),(5,5)}`.
- Rule 2 refused on quantity: with `DELIVER_SURPLUS_NOT_THE_ROW = False` the load counts only the
  row's items, so WOOL 4 sat under `DELIVER_MIN = 6`.
- Rule 3, the closing trip, is never charged (`DELIVER_CUTOFF_TURNS = 99` makes `deliver` False on
  every 24-turn day).

The last two interlock, and that interlock is the defect.
`DELIVER_MIN`'s own docstring defers a small load to "the end of the tour, which ends at the shed
anyway" — and with `deliver` False that clause is false.
This also explains mechanically why the `DELIVER_CUTOFF_TURNS = 12` arm was a measured null: this
tour costs 21 of its 23-turn budget and the walk home from (1,0) costs 8 more, so `plan()` prices
the `deliver=True` route at 29, refuses it as over budget, and keeps the tour without the closing
drop.
No setting of the cutoff can deliver this wool; the tour has no later delivery at all.

### The fix: batch only for a delivery that exists

`SHIP_WHAT_NO_LATER_STOP_CAN_BANK = True` in `kagg/search/cover.py`, one new clause in rule 2.
When the closing trip is uncharged (`deliver` False) and neither the current position nor any
remaining stop stands on a depot tile, a positive load of the ROW's produce ships now,
`DELIVER_MIN` notwithstanding.
The ferry re-draws whatever the rest of the tour still needs on the same stop, exactly as the
existing rule-2 ferry does, so the pens ahead still eat.
Tours that still touch a depot are untouched: the zero-detour rules own those, and their refusals
(`REDRAW_ONLY_WHAT_THE_MARKET_WONT_TAKE`) are measured.
The `due` clock is not consulted for a stranded load, because `tail` prices a closing drop that
`deliver=False` never plans.

The greedy prices the ferry like any other stop (`slot` -> `materialise` -> `turns`), so
assignment rebalances instead of shipping an over-budget tour.
On d6 the planner now routes the wool through a shed stop at h08 and the SELL lands while the
market is open.

Test: `tests/test_a_load_the_tour_can_never_deliver_is_ferried_not_batched.py`.
Red on HEAD, green with the fix, red again with the flag backed out (`-n0`), restored green.
A second test in the same file pins the guard: a tour whose remaining stops touch a depot buys no
walking ferry.

### Measured, before -> after (ours/tape, `--tape kawashigi --days 17`)

d0-d5: byte-identical, every row.

d6, the target day:

| row | before | after |
|---|---|---|
| sell | 10/17 | **14/17** |
| sh:wool (end of day) | 4/0 | **0/0** |
| buy_seed | 7/15 | **15/15** |
| money | 3/957 | 358/957 |
| tiles | 50/50 | 50/50 |
| buy_land | 1/1 | 1/1 |
| plant / water / harvest | 2/2, 17/19, 2/2 | 2/2, 17/19, 2/2 |
| feed / care / collect | 6/6, 6/6, 6/6 | 6/6, 6/6, 6/6 |

14/17 is the ceiling of this fix by construction: the row asks WOOL 12 and the board only grows 9.
The last 3 need more sheep and remain a separate open item.

d7 reconciles to exact: `sell 10/6 -> 6/6` (the baseline was selling yesterday's swept wool a day
late) and `buy_seed 5/4 -> 4/4`.
d4 `harvest 7/7` holds.

Downstream of d7 the board diverges as any d6 change makes it: the herd ends BIGGER (d16 cow+sheep
11 vs 10 baseline, d9 9/12 vs 8/12), d8 `feed 0/10 -> 1/10`, and d16 money closes 22,246 vs 19,067.
Two rows move the other way and are noted rather than hidden: the second sheep is lost on d8 (0/4
vs 1/4 baseline; both runs lose sheep inside the pre-existing d8 feed collapse, `feed 1/10`), and
the weed row's timing shifts (weeds appear d12-d13 and are dug by d14/d16, against d14/d16
appearances in baseline; both runs end d16 within one weed).
Days match in order: d0-d6 strictly improved or identical, d7 exact, so the later jitter is
inherited board state, not a gate.

### The two named gates are stale at this working state

`tests/test_each_day_matches_the_tape.py` errors at setup on every day: it asks for
`breakdown.TAPES["seb"]`, and the seb tapes were removed from that dict on 2026-08-13.
`tests/test_the_first_seven_days_match_the_plan.py` drives the retired Seb schedule (90494364) and
fails 7 of 15 with the fix OFF.
With the fix ON it fails 6 of 15 — `test_no_pen_stands_empty_at_dusk_beside_a_shed_holding_its_animal`
goes green — so the fix strictly reduces that gate's failures and introduces none.
Both gates need rebasing onto the kawashigi tape; that is not this change.

### Environment note for reproduction

Commit `2ddffb6` alone does not run: `schedule_agent` calls `router.crop_ops(..., tile=tile)`,
which only exists in the UNCOMMITTED `kagg/search/router.py` in the main checkout (the
`WATER_ROTATION` work), and `scripts/breakdown.py` needs the untracked `kagg/plan.py`.
Both were mirrored into this worktree unchanged; they are not part of this fix.

## 2026-08-14 — Day 8: the milk must be in the shed by h05, and the pen IS the shed

Folded in from docs/the_milk_must_be_in_the_shed_by_h05_2026-08-14.md.

Board: kawashigi, seed 11, `scripts/breakdown.py --tape kawashigi --days 17`.
Supersedes the "first milk day" section of
`the_wheat_row_and_the_turns_own_spending_2026-08-14.md`, which was right that d8 is the first
milk day and wrong about what to do with that.

### The decisive measurement

Forcing the tape's EXACT d8 orders -- buys and sells together -- with the milk banked six hours
earlier than baseline changes **nothing**:

```
d8                forced + early milk    forced (before the fix)    baseline
sell                    6/18                    6/18                 18/18
buy_product            10/17                   10/17                  5/17
feed                    9/10                    9/10                  2/10
care                    9/10                    9/10                  2/10
+ sold              $524/$3,177             $524/$3,177          $3,220/$3,177
```

Byte-identical.
His `SELL MILK 12` is at **h05**; the fix put our milk in the shed at **h07**.
Two hours late fills exactly as much as thirteen hours late: zero.

**"Earlier" is not the requirement. "By h05" is the requirement.**

### His plan, read off the raw replay

Positions come from the replay observations at seat 0, not inferred from the action stream.
His two ripe cows at d8 dawn are `CO@4,3 y6` and `CO@4,4 y6`; the other seven animals hold
nothing.

```
u4  <== STARTS ON A RIPE PEN
    h02 (4,4) PICKUP/WHEAT   h03 (4,4) FEED   h04 (4,4) CARE
    h05 (4,4) HARVEST        h06 (4,4) PLACE/MILK
u0  <== STARTS ON A RIPE PEN
    h01 (4,4) PICKUP/WHEAT   h03 (4,3) FEED   h04 (4,3) CARE   h05 (4,3) COLLECT_FERTILIZER
u2  h04 HARVEST              h06 (4,4) PLACE/MILK
```

Three things, and the third is the one that matters:

1. **The ripe pens are the day's FIRST work** for two units, not work they reach mid-tour.
2. **Every op on a pen happens in consecutive turns on that tile** -- PICKUP, FEED, CARE, HARVEST,
   PLACE, one after another, no revisit.
3. **He banks from the pen tile itself.** `_refresh_pins` sites pens ON shed-access tiles, so
   `PLACE/MILK` at (4,4) costs one turn and zero walking.
   He never makes a trip.
   The pen IS the depot.

### Ours, the same day

```
u4  FEED h02   CARE h03   COLLECT_FERT h04   HARVEST h05   ...   DROP h07
u1  ...                                      HARVEST h11         DROP h12
```

We have his shape on the first pen and then lose two turns delivering, and eight turns reaching
the second pen.
The second cow is the bigger half.

### Why the delivery flag was not enough

`BANK_THE_ROWS_PRODUCE_WHILE_REAPING` (`kagg/search/cover.py`) lets a hand bank produce the row is
selling at a zero-detour depot while harvests remain, gated on `rush` AND on the hand carrying
what `wanted` names.
Measured on the 17-day grid:

```
exact cells   447 -> 465  (+18)      d16 money   32,419 -> 31,321  (-$1,098)
animals d10-d16   13/14 -> 14/14     feed/care d11-d16  13/14 -> 14/14
d9 sell 22/25 -> 17/25               d10 sell 78/91 -> 69/91
d8 buy_product 5/17, feed 2/10, care 2/10   -- UNCHANGED
```

It moves the milk h17 -> h07 and four wheat buys out of h18 into h08-h11, which is a real timing
gain, and it makes the herd exact from d10.
It does not reach h05 and it does not move d8's target cells, so it is shipped **False** pending
the two changes below.

### Timing is the thing that is not matched

Daily fill COUNTS hide this completely -- d8 reads `sell 18/18` in the baseline with the orders
thirteen hours out of place.
Fills stamped with the hour, ours vs his hour-stamped asks:

```
d8   h00  OURS S-FERTx6                  TAPE B+WHEAx9 S-FERTx6
     h05  OURS -                         TAPE B+WHEAx2 S-MILKx12
     h08  OURS B+WHEAx1 S-MILKx6         TAPE B+WHEAx2
     h13  OURS S-MILKx6                  TAPE -

d9   OURS h01 B+WHEAx11 S-FERTx9   h02 S-WHEAx8   h18 S-WOOLx5
     TAPE h00 S-FERTx6 S-WHEAx8  h01 S-FERTx3  h03 B+WHEAx2  h06 B+WHEAx2 S-WOOLx4
          h07 S-WOOLx4  h10 B+WHEAx2  h12 B+WHEAx3  h17 B+WHEAx2

d10  OURS h01 B+WHEAx33  h02 S-FERTx10 S-WHEAx22  then nothing until h16
     TAPE h03 B+WHEAx7  h10-h19 S-FERT in blocks of 18, B+WHEA at h14/h17
```

**We transact in one early block and then go quiet; he trickles all day.** That is systemic and
bigger than d8.

Two separate causes on d8, both visible above:

- `HIRE_FIRST` puts NINE hires in the h00 block ahead of the wheat, so we buy 0 wheat at h00 where
  he buys 9 -- funded on a $5 bank by the `SELL FERTILIZER 6` sitting in an earlier slot of that
  same turn.
  He hires 11 too, but 5 at h00, 5 at h01, 1 at h05.
- `state["ordered"]` is credited when an order is QUEUED, so the twelve units the book refused at
  h01 drive `owed` to 0 and the row is never re-offered, however much money lands later.

### One hand per ripe pen: `ONE_HAND_PER_FUNDING_PEN`

The tour ORDER was never the defect, and neither was the flag.
Reading the work sequence `cover` hands each unit on d8 -- remembering that
`schedule_agent:3809` builds task tiles as `(x, y)` while the board is `(y, x)`, which cost one
wrong diagnosis in this session:

```
u4  0. (4,4) [FEED, CARE, COLLECT_FERTILIZER, HARVEST]  4t  funds   <== ripe cow
    1. (4,3) [FEED, CARE, COLLECT_FERTILIZER, HARVEST]  4t  funds   <== the OTHER ripe cow
```

Both ripe pens correctly flagged `funds`, both at the FRONT of the tour -- and BOTH ON ONE HAND.
Eight turns of work back to back, so the second cow cannot be banked before ~h08.
The tape puts one hand on each.
`greedy` ranks on `(added turns, unit, tile, index)`, pure cheapest-insertion, so appending the
second cow to the hand already standing on the first always wins.

The fix is a preference inside that ranking, never a refusal.
**It also has to be repeated in `COMPACT`**, which accepts any relocation that lowers total turns
and silently stacked them back -- the spread survived `greedy` and vanished before the tour was
built.

```
baseline      exact 447/697   d16 32,419
bank only     exact 465 (+18) d16 31,321 (-1,098)
split only    exact 468 (+21) d16 31,888 (-531)
split + bank  exact 465 (+18) d16 31,321 (-1,098)   BYTE-IDENTICAL to bank alone
```

**The two are not complementary.** With the banking flag on, the split is a no-op: once each
funding pen needs its own depot stop, stacking them is already the expensive option and `greedy`
separates them without being asked.
Two routes to the same assignment.

d0-d7 are byte-identical to baseline across all 41 rows, so nothing regresses in order.
The herd goes exact from d10 (`animals 13/14 -> 14/14`, d10-d16) and the first cow's harvest moves
h05 -> h03.

**d8's target cells do not move in ANY arm**: `buy_product 5/17`, `feed 2/10`, `care 2/10` are
identical in all four.
The milk is still not in the shed by h05 -- u1's cow is job 1 on its tour, behind an at-risk pen
it must feed to keep the animal alive, so it harvests at h10.

### Next

1. The remaining d8 gap is the WHEAT ROW, not the milk -- `HIRE_FIRST` puts nine hires ahead of it
   at h00, and `state["ordered"]` is credited on the QUEUE so a refused order is never re-offered.
   Fix the credit first; it is the only one of the three that changes `buy_product 5/17`.
2. Only then is it worth asking whether a `funds` pen should outrank an at-risk pen on the same
   hand -- that trade is an animal's life against the day's cash and must not be guessed at.

Do NOT reopen: the herd mix, d8's routing/job list (`crew.cover` covers 39/39), or sizing the
wheat row.

### The milk lands: `BANK_ON_THE_PEN_THAT_FUNDS_THE_DAY`

**Every delivery path in `materialise` banks on the way to the NEXT job.** All of them compute `d
= nearest(depots, pos, j.tile)` for the TRANSITION, so the stop is part of moving on and is gated
on that move being free.
Standing still is not a move, so none of them could express "bank here, now" -- which is the only
thing his plan does.
He harvests at (4,4) and PLACEs on that same tile the next turn, because `_refresh_pins` sites
pens on shed-access tiles.

Appending the bank stop directly after a funding pen, on the pen:

```
h02  u4 HARVEST          h03  u4 PLACE + SELL MILK 6      h04  bank $610
                                                               (every other arm: $13)
```

Gated on the PEN'S OWN yield being in `wanted`, not on what the hand carries -- a test caught the
looser version banking at every pen on a day whose row sells the wheat the herd is eating.

```
d8            baseline    on-pen
feed             2/10       6/10
care             2/10       6/10
pass           122/36     107/36
buy_product      5/17       5/17
season exact  447/697    467/697  (+20)      d16 money  32,419 -> 31,816  (-603)
```

**First movement in d8's target cells all session.** Half the milk is on time; the second cow is
still harvested at h11 because it is job 1 on its hand, behind an at-risk pen.

### What is binding NOW

`buy_product 5/17`, and for a reason that has changed.
The money IS there at h04 and the row never asks again: `state["ordered"]` is credited when an
order is QUEUED, so the twelve units the book refused at h01 drove `owed` to 0.
Before the milk landed this fix was worthless -- the forced-order run re-offered at his own
cadence and still failed on cash.
Now the cash exists and the ask is missing, so credit the FILL instead of the queue.

Then: `HIRE_FIRST` puts nine hires ahead of the wheat at h00, where he hires five and buys nine
wheat behind the fertilizer sale in the same turn.
That is worth the other 5 of the 17.

## 2026-08-15 — The goose is insurance (SUPERSEDED)

Folded in from docs/the_goose_is_insurance_2026-08-15.md.

> **SUPERSEDED, flagged 2026-08-15.**
> The verdict below ("geese are insurance in 14.8% of shop draws") was computed from opponent
> volumes that were later found to be summed sell OFFERS, not fills — see the RETRACTED note
> embedded in section 2 below, which is part of the original doc and kept in place.
> A same-day audit (`docs/fable_geese_audit_2026-08-15.md`, folded in immediately below this
> section) redid the arithmetic on the SELLABLE fix (commit `c99a8a5`, 2026-08-13, which added
> CARROT/TOMATO/EGG to the sellable set) and on fills instead of offers, and reached the opposite
> policy: **zero geese**, margin-best in only 0.9% of draws.
> Kept here for the traceable history of how the number moved; do not cite this doc's "14.8%
> insurance" figure without reading the audit that follows it.

Written 2026-08-15, at Alex's instruction to *do the math, not an experiment*.
Everything here is computed from `reference/kaggriculture.py`, with opponent volumes read off the
three ladder replays downloaded the same day.
**No simulation of our agent is involved**, deliberately: whether our planner can currently
execute a plan is a separate question from whether the plan is right.

### 0. Why this was reopened

`HERD_GEESE` was measured on 2026-08-11/12 as a disaster — 0 birds 69.4% win, 2 birds 38.9%.
That verdict is **dead**, and the dates say so:

```
2026-08-11/12   HERD_GEESE measured
2026-08-13      c99a8a5 fixes SELLABLE
```

`SELLABLE` listed six of the env's nine products and is the iteration domain of the only loop that
emits a SELL.
CARROT, TOMATO and **EGG could not be sold at all**.
So the sweep measured geese that produced eggs which could never be turned into money: pure cost,
zero revenue, on any flag, on any day.
It is not evidence about geese.

This is the third time in this project that a mechanic-level negative turned out to be an
artifact.
See `project_kaggriculture_animals_verdict`.

### 1. Production, from the env's own loop

`_daily_refresh_animals` (`reference/kaggriculture.py:805`), stepped exactly, one animal placed
d5, fed and cared every day, harvested as it fills:

```
animal   cost  structure  first_yield  interval  max_held  product   units/season
GOOSE    $300  COOP                 4         1         4  EGG                 46
COW      $400  PASTURE              8         2         6  MILK                30
SHEEP    $500  PASTURE              6         3         6  WOOL                30
```

**The model is validated against a real game**: it predicts 30 milk per cow, and game `93239838`
has 9 cows producing ~290 milk — 32 per cow.
Close enough to trust the rest.

The goose is the cheapest animal, starts four days earlier than a cow, and produces **every day**
against the cow's every-other and the sheep's every-third.

### 2. Revenue, with the opponent in the same book

The first version of this calculation priced our units into an empty book and reported milk at
$155/unit.
Every real game contradicts that — milk closes at $1-$5.
The error was leaving out the **opponent's flow**, and correcting it is what produces the finding.

Both seats settle into ONE inventory.
Measured opponent season volumes:

```
MILK  250-410      WOOL  ~250      EGG  0    -- and ours is 0 too
```

> **RETRACTED 2026-08-15. These two volumes are summed sell OFFERS, not fills.**
> The agent re-posts an unfilled order every turn, so they are inflated by roughly 6x.
> Measured against market inventory instead: across 26 replays a no-yarn board ends at
> `inv - I0 = +59` units of wool for **both herds combined**, and `93240733` lands at +59 with the
> opponent running zero sheep.
> Real wool supply is ~8 units per sheep per season, so two full herds move ~60-70 units, not 500.
> Milk was checked the same way and is ~200-240 units per seat per season, realised at $37-$78 a
> unit on a milk-poor board and $231 on a milk-rich one.
> **Every number below that uses `theirs` is therefore wrong and the ranking must be re-derived
> from fills before this doc is used again.**
> See `feedback_offers_are_not_fills`, which this document violated.

Six animals, net of purchase cost:

```
                          2 shops draining it    ZERO shops draining it
GOOSE   276 EGG,   0 theirs       $11,270                $9,818
COW     180 MILK, 300 theirs      $10,392                  $556
SHEEP   180 WOOL, 250 theirs      $32,910                $1,174
```

The goose loses **11%** when its drain disappears.
The cow loses 77%, the sheep 88%.

### 3. Expectation over the real shop draw

Shops unlock one per three days on days 3..24 — eight draws, uniform over the eight types, with
replacement.
So instances carrying a product is `Binomial(8, m/8)` for `m` carrier types.
Exact:

```
animal  product  types  P(zero)   E[revenue]  worst 10%    net E
GOOSE   EGG          2    10.0%       12,678     11,618   10,878
COW     MILK         3     2.3%       21,278      5,575   18,878
SHEEP   WOOL         1    34.4%       22,590      4,174   19,590
```

**The math does NOT say switch to geese.** On expectation a cow or sheep beats a goose by about
$8,000 per six animals.
Anyone quoting this doc for "geese are better" is misreading it.

What it says is that the goose is the only animal whose floor is close to its mean.
Its worst-decile revenue is more than double either alternative's, and the sheep — the highest
expectation of the three — returns $1,174 net on the **34.4%** of draws with no YARN_STORE.

Two structural reasons the egg book does not move:

1. EGG's curve is `log` with `above_target 0.2`, which is effectively undentable — the fragility
   table in `docs/when_and_what_to_sell_2026-08-15.md` puts EGG and WHEAT alone in that class.
2. **The opponents submit fixed 720-turn scripts.** They cannot start producing eggs in response.
   The egg book stays uncontested in every game, all season, by construction — which is a much
   stronger guarantee than any of our own price modelling.

### 4. What follows, and what does not

**Follows:** the herd choice should be conditional on the draw, and geese belong in the option set
as insurance against the egg-rich / yarn-poor corner.
`SHOP_ADAPT_HERD` cannot express this — it floats COW against SHEEP only.

**Does not follow:** a blanket switch to geese. The expectation says that loses money.

**The real cost of building it**, stated plainly because it is the reason this is not a flag flip:
`SHOP_ADAPT_HERD`'s swap is free *because COW and SHEEP both build a PASTURE*, so nothing in the
build schedule, the pen geometry or the routing changes.
**A goose builds a COOP.** Adding it means changing what gets built and where, which is a real
change to the opening, and the opening is matched to the tape.

### 5. Caveats a reader should hold

- `theirs` is three games. It is the right order of magnitude and the EGG=0 term is structural,
  but MILK 300 and WOOL 250 are estimates.
- Even production spreading is assumed. Real release is lumpier, which hurts the fragile products
  (milk, wool) more than the robust one (egg), so this if anything **understates** the goose's edge
  on the tail.
- Feed cost is not netted. Every animal eats one wheat a day, so it is close to a constant across
  the three and does not move the ranking, but the absolute nets are optimistic.
- No op-cost is charged. A goose fills at 4 units against the cow's 6, so it needs collecting more
  often — more HARVEST stops for the same crew. That is a real cost and it is NOT in these numbers.

## 2026-08-15 — Geese, audited — and why the Elo framing closes them

Folded in from docs/fable_geese_audit_2026-08-15.md.
Fable, 2026-08-15. **This audit supersedes the goose verdict above.**

Asked: audit `docs/the_goose_is_insurance_2026-08-15.md`, add the missing costs, give a policy.
Method as instructed: math only, no agent runs.
Production is stepped through the real `_daily_refresh_animals`; revenue walks the real
`market_price` unit by unit; the shop draw is exact.
Scratch scripts behind every number: `goose_audit.py` / `goose_margin.py` (session scratchpad),
all reproducible from the formulas quoted here.

### Verdict

**No geese, and the number that closes it is -$11,758 of expected MARGIN per six animals.**
On the money objective the goose really is insurance (best pick in 14.8% of shop draws).
On margin — ours minus theirs, which is what an Elo ladder pays — the goose is best in **0.9%** of
draws, because leaving the flooded milk/wool books stops suppressing the opponent's fixed
300/250-unit flows, and that suppression is worth ~$10,400 (milk) / ~$9,300 (wool) to whoever is
left alone in the book.
The insurance premium is paid to the opponent.

### 1. Audit of the doc's three claims

**Production stepping: one real error, -2 eggs.** Stepped through `_daily_refresh_animals`
exactly (fed+cared daily, harvested before overflow):

```
animal  placed  sellable  (doc)    harvest visits forced by max_held
GOOSE      d5      44      46            12
COW        d5      30      30             6
SHEEP      d5      30      30             7
```

The doc's 46 counts the production event at the END of day 29 (`next_day` 30).
That event fires only for the goose — interval 1 lands on every rollover; the cow's events stop at
`next_day` 29 and the sheep's at 29 — and its eggs have no day 30 to be harvested or sold in.
Sellable is 44.
Cross-check: my egg revenue E is $12,094 against the doc's $12,678, and the gap is exactly those 2
eggs x 6 birds x ~$50.
The `pending_care_bonus` handling in the doc is otherwise RIGHT, including the subtle first-event
behaviour (goose: 3 banked bonuses + base = 4, exactly `max_held`, no loss; cow: 7 banked + base =
8, capped at 6, loses 2 — already in both our totals).

**Binomial(8, m/8): correct.** Eight draws, `next_day % 3 == 0` at next_day 3..24, uniform with
replacement over `sorted(SHOPS)`, `MAX_SHOP_INSTANCES = 8` never binds before the 9th draw
(`reference/kaggriculture.py:886-891`).
P(zero): EGG (6/8)^8 = 10.0%, MILK (5/8)^8 = 2.3%, WOOL (7/8)^8 = 34.4% — all three match the doc.
One thing the count alone misses: unlock TIMING.
An instance drawn d24 drains 6 days, one drawn d3 drains 27; my revenue model carries the ramp.

**EGG undentable above I0: correct.** `log` / `above_target 0.2`: halving the price needs `1.722 *
ln(1+x) = 25`, i.e. x ~ 2 million units above I0.
Same class as WHEAT's above-curve.
This is also why the two independent revenue models agree on eggs to within the 2-unit error
while disagreeing on milk and wool.

**Where the doc's revenue model is optimistic: cow and sheep E.** The doc has COW E $21,278
($118/unit) and SHEEP $22,590 ($125/unit).
My model — same shared book, same opponent volumes, but pro-rata drain share and the residual
dumped at d29 — gets COW $14,041 ($78/unit) and SHEEP $15,778 ($88/unit).
The real seed-11 game realises milk at **$69/unit** (171 sold, $12,194), which sides with the
lower model; the ladder memory (`milk is floored at $1-5`) points the same way.
This does not rescue the goose on money — the ordering GOOSE < COW < SHEEP survives in both models
— but the "$8k per six" gap the doc quotes shrinks to **$1.3-2.5k** under the floor-realistic
release, and the goose's money-corner widens to 14.8% of draws (median gain $2,330 over the best
pasture, p90 $5,841).

### 2. The costs the doc left out, priced

**Feed: cancels.** Every animal eats 1 WHEAT/day (`FEED`, `:505-513`) — species-identical, so it
cannot move the ranking.
Absolute: 6 animals x ~24 fed days ~ 145 wheat, $3.2k at the seed-11 realised $22/unit, up to $6.5k
at the field's $45.
Charge it to "animals at all", not to species.

**Op cost: bounded, does NOT reverse anything.** The goose's cap forces 12 harvest visits against
the cow's 6 and the sheep's 7 — but every animal already receives a daily FEED+CARE visit, so the
extra HARVEST is one op at a tile the route already stands on.
Marginal: ~5-6 unit-turns per goose-SEASON.
Even priced at a panic $50/turn that is < $300 against ranking gaps in the thousands.
The goose actually SAVES ops elsewhere: an undentable book makes release timing worthless, so eggs
can ride the automatic end-of-day inventory drop (`_drop_inventories_to_shed`, `:878`) — no h05
shed race, which milk does need.

**Coop vs pasture: the tile cancels, the build is one op.** Any animal occupies a tile, so tile
opportunity cost is common to all three species.
The differential cost of a goose is one `BUILD_COOP` op (money-free, `:493`) plus the
pen-geometry/opening perturbation — which the question's framing says to ignore (the agent gets
adapted).
Called: ~zero in this arithmetic.
The doc's point that `SHOP_ADAPT_HERD`'s cow<->sheep float is free BECAUSE both build PASTURE
stands.

### 3. The Elo framing — this is what closes it

Money maximisation and margin maximisation disagree here, and the margin is what the ladder pays.
The opponent's flow is open-loop and fixed: MILK ~300 from d13, WOOL ~250 from d11, EGG 0.
Our species choice decides which book we co-occupy.
Computed per draw, real curve walk, their revenue with and without our flow in the book:

```
suppression value of OUR 180 units on THEIR flow (their gain if we exit):
  milk: mean $10,411   p10 $5,513   p90 $14,240
  wool: mean  $9,275   p10 $2,611   p90 $18,145

margin objective (ours - theirs, net of purchase), best pick over 4,000 draws:
  COW    43.6%      SHEEP  55.5%      GOOSE  0.9%
  goose margin E is $11,758 WORSE than cow/sheep
```

Mechanism: our marginal milk units were heading for the floor anyway (small loss to us), but their
presence forces pro-rata floor-sharing on the opponent's 1.7x larger flow (large loss to them).
Eggs are the mirror image: an uncontested, undentable book means our egg revenue is safe AND
harmless — nothing we sell there costs the opponent a dollar.
Safe-and-harmless is exactly what a zero-sum ladder does not pay for.

Even conditioned on the best observable corner — no YARN_STORE and no milk carrier among the three
draws visible by d9 (their money-corner detector, 12.8% of games) — P(goose margin-best) is
**7.0%**. There is no observable that rescues it.

This also reframes `project_kaggriculture_milk_is_floored` ("we flood our own book, this is where
the $11k gap is"): partially true for our bank, but the flood is simultaneously holding the
opponent's 300 units down.
Any fix that WITHDRAWS milk supply gifts back up to ~$10k of their revenue; the margin-aware fix
is release timing within the book, not exit from it.

### 4. Policy

- **Zero geese.** Closing number: -$11,758 margin E per six animals; goose margin-best in 0.9% of
  draws, 7.0% in its best observable corner.
- The cow<->sheep float (`SHOP_ADAPT_HERD`) is the right lever and stays; on the margin objective
  the split is COW 43.6% / SHEEP 55.5% of draws, so the adaptive pasture herd is near-optimal
  already.
- The HERD_GEESE deletion (7a88d30) was right by accident: the sweep it rested on measured
  unsellable eggs, but the corrected arithmetic reaches the same end state.

### 5. Caveats, stated plainly

- Opponent volumes are three replays (MILK 300, WOOL 250). The suppression magnitudes scale
  roughly linearly with their volume; the SIGN of the margin result is robust to +/-50% on them,
  and the EGG 0 term is structural (fixed scripts cannot respond).
- Fill sharing is modelled pro-rata within each day. The env's real interleave is per order slot;
  either seat can front-run within a turn, but over a season of daily flows pro-rata is the right
  first-order model, and it is the SAME assumption on both sides of every comparison.
- Only 6-of-one-species portfolios were compared, matching the doc. Mixed herds interpolate;
  nothing in the margin table rewards mixing geese in.
- Margin E levels (-49k etc.) include their fixed wool+milk revenue as an offset; only DIFFERENCES
  across our choices are meaningful, and those are what is quoted.

## 2026-08-14 — Day 8's wheat row: a real 12 units, a $9,577 near-fix, and what d8 actually is

Folded in from `docs/the_wheat_row_and_the_turns_own_spending_2026-08-14.md`.

Status: DIAGNOSED, FIX REVERTED, DO NOT RETRY AS WRITTEN. Board: kawashigi, seed 11,
`scripts/breakdown.py --tape kawashigi --days 17`.

**The defect is real.** `_process_market` walks a turn's order slots in order, so an order pays out
of what the slots ahead of it left behind. The market block tracks a running `money` and debits it
for `BUY_LAND`, `BUY_ANIMAL` and its own `BUY_PRODUCT WHEAT` -- but not for `HIRE` and not for
`BUY_SEED`. With `HIRE_FIRST` on, both sit above the wheat row.

Day 8's row asks `buys {WHEAT: 17}`. Probed at the block:

    h00  money 833  live_bank 305  quote 33  owed 17  short 17   12 orders already queued; block refused a slot (len < 9)
    h01  money 741  live_bank 741  quote 33  owed 17  short 17   queued LAST, behind HIRE, HIRE, BUY_SEED STRAWBERRY 4, BUY_SEED WHEAT 5
    h02  money  15                           owed  0  short  0

Two hires cost `fib(9) + fib(10)` = $144 and the seed $400 + $50 = $450 -- $594 of the bank already
committed, roughly $147 reaches the wheat slot. Five units fill.

The five that fill are not the damage: `state["ordered"]` is credited on the order QUEUED, and a
`BUY_PRODUCT` the book refuses is silent, so `owed` drops to 0 and the row is never re-offered -- and
`DUSK_FEED_TOPUP`, bounded by `row_buys - ordered`, is dead too. Day 8 closes `buy_product 5/17`, and
on an empty shed `feed 2/10` and `care 2/10`. The tape spends comparable money the same day and lands
all seventeen by never over-committing a single slot: nine at h00 where only a fertilizer sell is
ahead of it, then 1/h03, 2/h05, 2/h07, 3/h10 as sales land.

**The fix works on d8 and loses the season.** Debiting `money` for the HIRE and BUY_SEED orders
already queued this turn (`THE_BANK_IS_DEBITED_FOR_WHAT_THE_TURN_ALREADY_ORDERED`) fixes d8 --
`buy_product 17/17`, dripping 6@h01, 1@h09, 1@h10, 1+6@h18, 1@h19, 1@h20 -- and loses **$9,577**.

    d16 money      baseline 32,419   hire+seed debit 22,842   seed debit only 23,798   (tape 32,566)

The loss is on day 6, identical in both variants:

    d6                     baseline        after
      money                  956/957        6/957
      hands                    4/4          2/4
      pens                     8/8          6/8
      buy_product              6/6          0/6
      buy_seed               15/15        12/15
      build_pasture            2/2          0/2
      sell                   17/17        11/17

Day 6 is the day the schedule takes the $1,000 parcel. The seed debit alone is enough to cause it,
with hires untouched -- killing the theory that the hire path was being charged twice. The running
`money` is read by the land buy, the hire top-up and the `short_of_cash` routing decision, all tuned
against a bank never debited for seed; lowering it by $450 on a parcel day propagates into routing,
and day 6 sells 11 where it sold 17.

**Second attempt: local sizing. Same loss, to the dollar.** Sizing only the wheat order against
`money` minus this turn's earlier spend, computed at the wheat block, without mutating `money`
(`THE_WHEAT_ROW_IS_SIZED_ON_WHAT_THE_TURN_HAS_LEFT`):

    exact cells of 544   baseline 385   local sizing 349
    d16 money            baseline 32,419   bank debit 22,842   local sizing 22,842

The two implementations produce the identical season -- refuting the shared-mutation diagnosis; the
local version leaves `money` untouched for every other reader and still lands on the same dollar.
Cause: the size of the row on d6.

    d6      hands 4/4 -> 2/4    hire 4/4 -> 2/4    pens 8/8 -> 6/8
            buy_product 6/6 -> 0/6               sell 17/17 -> 11/17

At baseline d6's over-sized wheat order fills -- `buy_product 6/6` is exact. Sizing it to what the
turn can provably pay refuses an order the market would have honoured, and d6 is the day the $1,000
parcel is taken, so the day unwinds from there. d8 did get what it was owed (`buy_product 5/17 ->
17/17`, `place 0/3 -> 2/3`): it cost 47 broken cells elsewhere against 11 gained.

Why the honest size is too small: `money` at the wheat block already carries the turn's pending
sells, an estimate at the row's own prices, while the hire ladder and seed are exact. Subtracting the
queued HIRE and BUY_SEED pessimism lands entirely on the purchase and none on the revenue, so a turn
that can in fact pay is told it cannot.

**The lesson.** A running estimate with several readers is not safe to make more accurate for one of
them. The bank being wrong was load-bearing for three other decisions; correcting it in isolation is
a different global tuning -- the same shape as `HARVEST_WAITS_FOR_THE_LAST_GROWING_DAYS_WATER` (see
`docs/strawberry_watering_2026-08-16.md`), where one unit of yield was traded for the herd. Both
attempts shrank the order, and shrinking the order is what loses d6. Do not try a third way of sizing
it.

The shape left: credit `state["ordered"]` on what actually FILLED rather than on what was queued, so
a row the book refuses is re-offered later in the day. d6 keeps its over-sized order and keeps
filling it; d8 keeps its over-sized order, fills five, and re-offers the other twelve as the
afternoon's sales land -- the tape's own cadence. No bank read, no order made smaller. The obstacle is
measuring the fill: wheat also arrives from HARVEST and leaves via FEED, so the day's purchases are
`(shed + carried)_now + fed_today - (shed + carried)_dawn - harvested_today` -- the same shape
`SEED_ROW_IS_A_FLOOR` already uses for seed, with one extra term. Model it on that, dawn-latching
wheat exactly as `state["seeds_dawn"]` is latched.

**What d8 actually is: the first milk day.** Established after both fixes above were reverted;
supersedes the framing of the whole document -- the wheat row is a symptom.

Forcing the tape's exact d8 market does not reproduce his d8 market. Replaying his hour-stamped
orders verbatim (buys and sells together):

    d8            ours/tape       baseline was
    feed             9/10             2/10
    care             9/10             2/10
    sell             6/18            18/18
    buy_product     10/17             5/17
    + sold        $524/$3,177     $3,220/$3,177

6 units sold -- exactly `SELL FERTILIZER 6`. His `SELL MILK 12` filled zero, because we hold no milk.
`buy_product` cannot match until sells match, and sells cannot match until the goods exist -- every
order-logic fix was downstream of the binding constraint. With his market forced, `feed 2/10 -> 9/10`
and `care 2/10 -> 9/10`: the d8 unit plan is right, the day is starved, not misrouted. `crew.cover`
also covers d8 completely (39/39 jobs, nothing dropped), so the "19 jobs left uncovered on day 8"
note at `crew.py:120` is STALE.

The herd mix is not the cause -- ours matches the tape animal for animal at every dawn:

    day     COW    SHEEP   GOOSE
    d1      2/2     2/2     0/0
    d4      3/3     2/2     0/0
    d6      4/4     2/2     0/0
    d8      6/6     3/3     0/0

Why d8 specifically: COW is `first_yield_day 8, interval 2, max_held 6, product MILK`. Cows placed on
d0 first yield on d8, holding up to 6 each -- two early cows is 12 milk, exactly his `SELL MILK 12`.
His shed holds 0 milk at d8 dawn, same as ours: the 12 units are collected during d8. d8 is the day
the cows first pay out, not a poor day.

The capability we do not use: `PLACE` is overloaded (`kaggriculture.py:363`) -- placing an animal on
a structure-matching empty tile, or (if shed-adjacent) a targeted shed deposit of n units of a named
product. His `u2:PLACE/MILK` and `u4:PLACE/MILK` at h05 are milk deposits, not animal placements, and
`SELL MILK 12` is in that same h05 order block -- the unit phase runs before `_process_market` (:922
then :928), so it lands and sells in one turn. This also corrects the reading of d8 `place 0/3`: two
of the three are shed deposits, not animals.

`PLACE <product> <n>` deposits a named quantity; `DROP` dumps a unit's whole inventory with no amount
and no choice of item. The agent only ever emits `DROP`, and on d8 it drops at h07, h17, h18 and h23
-- all after his h05 sell. The milk cannot reach the shed before the turn meant to sell it.

    cows placed early -> first_yield_day 8 -> collect on d8 -> PLACE 12 MILK into the shed at h05
                      -> SELL MILK 12 in the same turn      -> funds BUY_PRODUCT WHEAT -> feed 10/10

**Next step, stated as a measurement, not a flag.** Does the agent emit any milk collection on d8,
and if so why does it not reach the shed before h05? `PLACE <product> <n>` as a shed deposit appears
unused anywhere in the agent. Do NOT reopen: the herd mix, d8's routing/job list, or sizing the wheat
row.

## 2026-08-09 — The wheat churn is a buy-side day-budget defect, not a sell-side one

Folded in from `docs/fable_the_wheat_churn_2026-08-09.md`.

Started from a sell-side framing (the shed carries a 42-44 unit reserve while offering 51-123 WHEAT a
day from day 17). Superseded mid-investigation: the field disagrees on how much to sell and agrees
closely on how much to buy.

**The reframing evidence.** 66 of our own 1.32.6 ladder replays (`townCenterSellInterval=24` only),
wheat units offered per game, grouped by team:

    team                     games  wheat_buy  wheat_sell  mean_bank
    alex chilton                66      1,099         764    $73,827
    Seb (allegedly)             10        392          84    $74,264
    Rayk Kretzschmar             1        266         305   $129,906
    Lester Leong                 1        266         305   $125,255
    Syed Muhammad Gillani        4        323         649   $101,153
    HealthStone                  5        293         436    $80,237
    kakuteki                     1        266         350    $70,886

Syed sells 649 and banks $101k; Rayk and Lester sell 305 and bank $125-130k. Seb's 84 is the low
outlier, not the field's norm. The field buys 266-392; we buy 1,099. Selling is downstream of having
bought too much.

**The mechanism, measured.** `schedule_agent.py`, the feed-buy emission site (~line 3194/3208):

    herd = feed_days(day) * alive - fed_today - on_hand
    short = min(max(herd, min(max(0, owed), BUY_DRIP)), FEED_TURN_CAP)

`owed` is the schedule row's own target, credited every turn via
`state["ordered"][("buys", "WHEAT")]`; it self-limits to zero once asked. `herd`
(`feed_days(day) * alive - fed_today - on_hand`) has no day-level credit at all -- `feed_days(day)` is
2 early, 4 from day 16 (`FEED_DAYS_FROM_DAY`), a 2-4 day stock buffer, not a purchase budget. The only
bound was the per-turn `FEED_TURN_CAP` (6), a theoretical ceiling of 6 x 24 = 144 units a day.
`max(herd, ...)` means the bigger term wins, and from around day 12 that is `herd` on almost every
turn.

Measured, seed 11, Seb's tape at seat 1, full 30-day season, ground truth via
`kagg.analysis.fills.record_fills`:

    |         | bought | sold  | final bank |
    | unfixed | 1,800  | 1,456 | $45,797    |

Per-day trace (`data/logs/herd_diag_seed11.log`): the herd path hits `FEED_TURN_CAP` on 20-24 of 24
turns on days 17-29, 1,668 herd-path units asked that run. The two "unfixed" numbers (1,668 vs 1,800)
differ because of a methodology bug (see Two false leads below) -- 1,800 is the one to trust, using
`build_tape_agent(TAPE, 1)`, the convention `test_fills.py` already uses.

**The fix.** Two additions right after `herd` is computed:

    herd_ceiling = max(0, max(wanted, FEED_BUY_CEILING_DAYS * alive) - state["ordered"][("feed", "WHEAT")])
    herd_floor = max(0, alive - fed_today - on_hand)
    herd_capped = max(min(herd, herd_ceiling), herd_floor)
    short = min(max(herd_capped, min(max(0, owed), BUY_DRIP)), FEED_TURN_CAP)

The ceiling is credited on ASKS, reusing `state["ordered"][("feed", "WHEAT")]` -- the row and the
herd already share that counter. The floor is credited on ARRIVALS: `alive - fed_today - on_hand` is
what is still needed today regardless of the ceiling; `on_hand` only moves when stock genuinely lands
or leaves, so an order that fails to fill leaves it untouched and the floor asks again next turn.
`max()` always lets the floor through, so a real shortfall is never silenced; only the excess chasing
of the multi-day buffer is bounded. This mirrors the shape of the historical starvation bug `d124359`
(subtracting asks from a target sized at one day's need), except here the thing credited on asks is a
ceiling with headroom, not the target itself, with a separate arrival-based floor to survive a failed
ask.

**Why `FEED_BUY_CEILING_DAYS = 2`, not 1.** The first version sized the ceiling at
`max(wanted, alive)` -- one day's true consumption. It passed the churn measurement outright, 1,800
-> 393 bought, but failed the anti-starvation check on a second, independent run: seed 11, day 15,
the shed held 16-19 idle WHEAT the entire day while only 7 of 20 animals got fed, and by day 17's
rollover six animals had starved (`consecutive_unfed >= 2`, herd 20 -> 14, zero recovery):

    day  hr  herd  ceil floor capd owed on_hand alive fed_td sh_wht short ordrd
     15  16    14     0    0    0    0      22    20      4     16     0    20
     15  21    14     0    0    0    0      19    20      7     16     0    20   <- day ends, 7/20 fed
     16  19    39     0    0    0   -2      27    20     14     15     0    20   <- day ends, 14/20 fed
     17   0    30    18    0   18   18      26    14      0     21     6     0   <- herd is now 14

The bottleneck is not wheat supply -- the shed is sitting on it -- it is delivery: FEED needs a hand
to physically carry a unit of wheat to a tile, and with a herd of 20 that is a real routing/labor
constraint. The old code's gross over-buying had been masking that constraint with surplus;
tightening supply to the exact daily need removed the slack the crew needed to catch up.

Three ceiling sizes measured on the identical fixture:

    FEED_BUY_CEILING_DAYS | bought | sold  | final bank | herd drops
    unfixed (no ceiling)  | 1,800  | 1,456 | $45,797    | none
    1 (= alive)           |   393  |   253 | $53,421†   | day 16->17: 20 -> 14
    2 (shipped)            |   797  |   458 | $46,370    | none
    4 (full buffer)        | 1,328  |   985 | $46,834    | none

† Measured with a stale, differently-tuned `schedule_agent.py` before a data-contamination issue
(below) was caught; the herd drop it produced, independently reproduced on the clean fixture, is the
finding that mattered -- the bank figure is not comparable to the others.

`FEED_BUY_CEILING_DAYS = 2` is shipped: cuts season wheat purchases 56% (1,800 -> 797), keeps the
bank at parity with the unfixed baseline (+$573), zero herd drops across the full 30-day season -- the
same safety record as the unfixed baseline at less than half the spend. 4 is safe but barely bends
the curve (1,328, a 26% cut). 1 cuts hardest and is unsafe.

The routing/labor limit itself is a separate, deeper bug, explicitly NOT fixed here: even with
abundant wheat in the shed, the crew could not reach all 20 animals in a single day at this herd
size. `FEED_BUY_CEILING_DAYS = 2` works around it with buffer; it does not explain why the crew falls
behind.

**Two false leads, corrected in-flight.**
1. `PYTHONHASHSEED` was not the cause of a run-to-run discrepancy (1,800 vs a later 373). Pinning it
   to 0, 1, 2 all reproduced 373 identically, and the default unseeded process also gave 373 on six
   separate runs -- a red herring.
2. The actual cause: a second session was concurrently editing the shared, uncommitted main checkout.
   This worktree needed `kagg/analysis/fills.py`, seed-script replay data and parts of
   `schedule_agent.py` copied in by hand from the main checkout as uncommitted work. A later re-read
   of the main checkout (to build a before/after backup) picked up a different, unrelated fix
   (`FEED_BUY_TURNS_PER_DAY`) that had landed there meanwhile from another concurrent session -- that
   was the accidental source of the 373 figure, not this investigation's code. Fixed by reconstructing
   the true "before" state by reversing this investigation's own diff against its own first synced
   copy, reproducing 1,800 exactly, repeatably, independent of hash seed. Lesson for anyone touching
   this repo from a worktree while the main checkout is live: once a file is copied in, do not copy it
   again mid-session.

**Tests.** `tests/test_the_herd_buy_has_a_day_budget.py`:
`test_wheat_bought_stays_within_a_days_budget_of_the_herds_need` (RED before, 1,800 vs a ceiling of
1,100; GREEN after, 797) and `test_the_herd_never_shrinks_across_the_season` (the anti-starvation
guard, passes on both unfixed and fixed code -- it is what would have caught the
`FEED_BUY_CEILING_DAYS = 1` regression). Revert-and-confirm per CLAUDE.md: reverting turns the first
test red again while the second correctly stays green on unfixed code too.

**What changed.** `schedule_agent.py`: new constant `FEED_BUY_CEILING_DAYS = 2`, `herd_ceiling` /
`herd_floor` / `herd_capped` added at the feed-buy emission site. `tests/test_the_herd_buy_has_a_day_budget.py`:
new, two tests. Diagnostics: `data/logs/herd_diag_seed11.log`, `data/logs/starvation_diag.log`.

**What this does not touch.** The sell side (`SELL_TO_MAKE_ROOM`, the shed feed-reserve formula,
`CAP_SELL_OFFER_SIZE`, `LATE_SELL_BIAS`, `SELL_ON_DRAIN_CADENCE`) -- untouched, since buying not
selling is the anomaly. The routing/labor limit exposed by the DAYS=1 experiment -- flagged as a
distinct, deeper bug. `FEED_ORDER_CAP`, `BUY_DRIP`, `FEED_TURN_CAP` -- left at existing,
separately-measured values.
