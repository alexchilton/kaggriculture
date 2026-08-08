# Small, obvious errors in the chain-search stack — review 2026-08-05

Requested by Alex: hunt for concrete, small, obvious defects in `routines.py`, `chains.py`,
`scheduler.py`, `local_search.py`, `beam_chains.py`, `allocation_calculator.py`,
`build_calculated_genome.py`.
Everything below was measured against the live code, not inferred from reading it — each item
has the script that produced the number.
Two defects were already known (fixed-stride block partition stranding tiles; the wheat feed loop
needing 3 coordinated gene changes) and are not re-reported except where a new instance of the
same *class* turned up.

Ranked by expected value: how much it would move the search's result if fixed.

---

## 1. Cross-slot tile collision — decode() never checks two chains don't claim the same ground

**This is live in the current best genome ($81,102).** `kagg/search/chains.py`'s `decode()`
(lines 374-440) iterates slots independently and calls `R.ranch()` / `R.grow()` with whatever
tiles that slot's genes name. Nothing anywhere — not `decode()`, not the beam, not local search —
tracks which physical tiles an earlier slot in the *same genome* already claimed.

`RANCH_GROUPS` (built by `_cut_pen_groups()`, `chains.py:169-198`) draws its multi-pen groups as
`block[:n]` prefixes of the exact same `NARROW_BLOCKS`/`WIDE_BLOCKS` tuples that the `grow` kind
indexes via `BLOCKS`. A ranch chain using `block[:2]` of block `B` and a grow chain using the full
block `B` in a different slot are two different genes indexing the same tile set, and `decode()`
has no cross-reference between the "ranch" and "grow" tile universes to catch it.

**Measured**, on `data/chain_search_local/best_beam_genome.npz` (the $81,102 / $81,768-held-out
genome):

```
('ranch', 'COW',    ((0, 0), (1, 0)),                                    0)
('grow',  'MELON',  ((3,3),(2,3),(1,3),(0,3),(0,4),(1,4),(2,4),(3,4)),   1)
('ranch', 'COW',    ((4, 0), (4, 1)),                                    0)
('ranch', 'COW',    ((1, 1), (0, 1)),                                    4)
('grow',  'MELON',  ((2,2),(3,2),(4,2),(4,3)),                           3)
('grow',  'WHEAT',  ((0,4),(1,4),(2,4),(3,4)),                          12)
```

`grow.MELON` (slot 1) and `grow.WHEAT` (slot 5) share all four tiles `(0,4) (1,4) (2,4) (3,4)`.
That is exactly the "18 NW tiles" figure the brief quotes (22 nominal tiles across all six chains,
minus the 4 double-booked ones) — the brief's own tile count already reflects this collision
without anyone having identified the mechanism.

Simulated the whole season (`J.step` turn by turn, `weed_chance=0.0`, opponent = all-PASS) and
inspected `state.tiles.crop` at the four contested tiles:

```
day  1..13: crop == MELON continuously (planted day 1/2, still growing)
day 14:     harvested, tile clears (crop == EMPTY)
day 15/16:  MELON's own chain replants MELON there again
```

**`WHEAT` never once appears as the tile's crop, on any of the 30 days, on any of the four
tiles.** Confirmed by scanning every day of the season: `WHEAT ever appeared on slot5's 4 tiles
across full season: False`. The wheat chain's internal bookkeeping (`planted[tile]` in
`routines.grow()`) is open-loop and has no feedback from the simulator, so it happily believes its
day-12 `PLANT` succeeded and spends the rest of the season emitting `WATER`/`HARVEST`/sell orders
for a crop that was never actually there. `WATER` and `HARVEST` are crop-agnostic in their
preconditions (they only test tile *kind*, not which crop), so the wheat unit's ops land on the
real melon crop instead — sometimes redundantly (re-watering an already-watered tile), sometimes
racing melon's own unit for the same harvest.

**The slot is not free, and it is not neutral.** Forcing slot 5 to `"off"` and re-scoring on the
same 16 games:

```
as-is:                                    16/16 wins, $81,102
slot 5 (the "wheat block") forced off:    16/16 wins, $79,792   (-$1,310)
```

So the phantom slot is currently net *positive* by $1,310 — not because it grows wheat (it
produces zero, all season), but through the accidental WATER/HARVEST interaction with melon's
own crop. That is not a strategy anyone designed or would want to rely on; it is an artifact of
two chains fighting over one tile, and its sign could flip with a different opponent mix, a
different melon start day, or any local-search step that changes melon's timing.

**This reframes the already-known defect (b).** "The wheat feed loop needs 3 coordinated gene
changes and every intermediate step is worse" is true, but it understates the problem: slot 5's
block is not a working wheat chain that needs tuning, it is squatting on ground slot 1 already
owns. No amount of adjusting `fertilize`/`feed_loop`/`fert_trade` on slot 5 can ever produce real
wheat while `block` still points at melon's tiles — the gene that actually needs to move is
`block`, to any of the many free NW/NE tiles, and *then* the feed-loop coordination becomes
reachable.

**What would confirm/fix it:** add a tile-overlap check to `decode()` — track a `used_tiles: set`
across slots (exactly as `build_calculated_genome.py`'s `pick()` helper already does, line 145-153,
which shows the author was aware this needed guarding in that one script but never ported the
check into the actual search path) and mark a colliding slot `skipped` rather than `used`. Re-run
local search after the fix; the wheat chain should either relocate to free ground or the search
should drop it, and the $81,102 number will move (very likely up, since a *working* wheat chain —
one that actually feeds the cow ranches, which is the entire point of task-today's "wheat feed
loop" work — is worth much more than $1,310 of incidental melon assistance).

**Verification script**: `PYTHONPATH=. python3` snippet loading
`data/chain_search_local/best_beam_genome.npz`, calling `C.decode`, and intersecting the tile sets
of the returned `used` list — reproduced above, three lines of Python, no simulator needed to see
the collision; the simulator run above only confirms the mechanical consequence.

---

## 2. Land-timing gate lets a genome believe it bought land it never actually got

**File:** `kagg/search/chains.py`, `_affordable()` (360-371), `land_schedule()` (312-337),
`_land_requests()` (340-357), used by `reachable_quadrants()` and `decode()`.

`_affordable()`'s only safety check is:

```python
if first_order[j] < EARLIEST_REVENUE_DAY and spent > OPENING_BANK:
    break
```

i.e. a parcel requested **on or after day 3** is treated as unconditionally affordable, no matter
how large cumulative spend is by that point, and with zero knowledge of whether any revenue has
actually landed by then for *this* genome. It is explicitly documented as "not a cash-flow model"
(`reachable_quadrants`'s docstring), which is a reasonable simplification in principle — but the
consequence is that `decode()` will mark a multi-parcel chain as `used` (not `skipped`) even when
its own land will silently fail to arrive in the real simulator.

**Compounding cause:** `_land_requests()` records the *same* `land_day` value for every parcel
index a chain needs (`for j in range(need): first_order[j] = min(..., day)` — no `+k` offset),
while `land_schedule()` then spaces the actual purchases one parcel per day
(`prev = max(prev + 1, first_order[j])`). So a chain needing 2 parcels (an SW tile) with
`land_day = 7` is recorded as wanting *both* parcels "by day 7", but the farm-level schedule can
only buy the first on day 7 and is forced to the second on day 8 — one day later than the chain's
own gene implies, with no mechanism checking that the chain's `start_day` accounts for that.

**Measured**, with a synthetic genome (one `grow WHEAT` chain on an SW block, `start_day = 7`,
`land_day = 7` — satisfies every existing guard, including the beam's own
`land_day <= start_day` refine check):

```
_land_requests:        {0: 7, 1: 7}                 # both parcels "wanted by day 7"
land_schedule():       [7, 8]                        # but actually bought day 7 and day 8
reachable_quadrants(): 2                             # "both are affordable" -- WRONG
decode(): used=[('grow','WHEAT', SW-block, start=7)] # NOT skipped
```

Simulated turn by turn:

```
day 7:  money 3000 -> 1960   (NE parcel $1000 + 4 wheat seeds $40)   n_land: 0 -> 1
day 8:  money stays 1960                                             n_land: 1 (unchanged!)
day 9, 10: money 1960, n_land 1                                      unit stuck at spawn (4,4)
```

The day-8 SW purchase ($2,000) silently no-ops (`_do_buy_land`'s documented behaviour) because
only $1,960 remains after day 7's spend — a spend `_affordable()` never modelled, since it only
ever reasons about land prices, not the chain's own seed cost or any other slot's spend on the
same days. **The farm never owns SW for the rest of the game.** The chain that "needed" it
continues to try to plant there every day, wasting its seed orders and hire cost, and `decode()`
still reports it as a working chain rather than a skipped one.

**Why this matters beyond the synthetic example:** the current $81,102 best genome uses land
inside NW *only* — zero `buy_land` orders anywhere (verified: all six chains' tiles have
`x < 5, y < 5`). The leader banks $139,121 partly by buying NE and SW on days 7 and 10 and growing
41 tiles of strawberry on the new ground. If every attempt the search makes to reach outside NW
runs into this failure mode — a chain that *looks* affordable by the static gate but silently
loses its own land race against its own seed spend — the search would learn "land doesn't pay",
which is exactly the illusory-fact-from-code-limitation pattern `what_kind_of_problem_this_is.md`
already lists six instances of. This is very plausibly a seventh, and it sits directly on the path
to closing the $58k gap to the leader.

**What would confirm/fix it:** either (a) make `reachable_quadrants`/`_affordable` account for the
chain's own opening cost (seeds/animals) alongside the land price when judging affordability past
day 3, or (b) — cheaper — verify post-hoc: after `decode()` builds the script, check `n_land`
reached by each chain's `land_day + land_purchases_for(tile) - 1` in a quick simulated prefix, and
mark it skipped if the parcel never actually unlocks. Re-run the beam with SW/SE offered more
freely once fixed, and check whether it starts finding land-based strategies instead of always
retreating to NW.

**Verification script:** the two Python snippets above (`_land_requests`/`land_schedule` sanity
check, then a turn-by-turn `J.step` loop reading `state.farm.n_land` and `state.farm.money`) —
both under 20 lines, no long job.

---

## 3. `allocation_calculator.turns_per_tile()` drops the recurring HARVEST turn for ongoing crops

**File:** `scripts/allocation_calculator.py:35-45`.

```python
def turns_per_tile(crop, water_every):
    info = R.CROP_TABLE[crop]
    cycles = 1 if info["ongoing"] else max(1, DAYS // max(info["max_day"], 1))
    per_visit = 1 + 1                       # WATER + one step of walk
    return per_visit / water_every + (2 * cycles) / DAYS
```

For an ongoing crop (`STRAWBERRY`, `TOMATO`), `routines.grow()`'s own job assignment is:

```python
if info["ongoing"]:
    jobs[tile] = ["WATER"] + (["HARVEST"] if age >= info["first"] else [])
```

Once the tile starts producing (`age >= first`, day 10 for strawberry) it needs **`WATER` +
`HARVEST`** on every visited day, not just `WATER` — for the ~20 remaining days of a 30-day
season, i.e. roughly two thirds of the crop's life. `turns_per_tile()`'s `per_visit = 1 + 1` bakes
in only "WATER + one step of walk" and never adds the harvest op; the `(2*cycles)/DAYS` term with
`cycles = 1` was clearly meant to amortise "one PLANT, ever" but ends up standing in for the
*entire* recurring harvest cost too, which it cannot do because harvest recurs on ~20 days, not
once.

**Measured directly** by running `R.grow()` on a real 8-tile `WIDE_BLOCK` nearest to spawn
(minimising walk-distance bias) for a full season:

```
STRAWBERRY, water_every=2, nearest wide block: measured 2.179 turns/tile/day
TOMATO,     water_every=2, same block:          measured 2.212 turns/tile/day
calculator's formula for both:                  1.067 turns/tile/day
```

**The calculator understates the true turn cost by roughly 2x** for the two ongoing crops.
Since `value_per_unit = drain * base / (tiles_to_fill * tpt / TURNS)`, an understated `tpt`
directly **overstates** `value_per_unit` — the exact "revenue per unit-day" ranking that decides
the greedy fill order in `THE ALLOCATION` section of the script's own printed output. Strawberry
is the second-largest market in the whole game by the doc's own numbers ($66,586-$68,640), so this
bug runs in favour of exactly the crop the whole "the mix is arithmetic" thesis leans on, and the
"reproduces the leader's farm" claim is riding on a ~2x-wrong number for it. This does not change
the *tiles allocated* to strawberry (that's capped by `tiles_to_fill` and the 75-tile budget,
neither touched by `tpt`), but it does change strawberry's rank against every other crop when
tiles are scarce, and it changes the "slots to fill" column that determines whether the
recommended mix is even physically buildable in the number of chain-slots available.

**What would confirm/fix it:** for ongoing crops, `per_visit` needs to become a day-weighted
average — roughly `(pre_production_days * 2 + producing_days * 3) / DAYS` per water_every, rather
than a flat 2. A quick patch: replace the ongoing branch's amortisation with a term that adds one
extra op for every day from `first` to `DAYS`, divided by `water_every`.

**Verification script:** `R.grow(Script(), "STRAWBERRY", list(nearest_wide_block), plant_day=0,
water_every=2, sell=False, buy_land=False, unit=0)`, count non-`PASS` ops, divide by
`len(block) * 30` — five lines, no simulator needed.

---

## 4. `allocation_calculator.turns_per_tile()`'s cycle count is off by one for non-ongoing crops

**Same function**, the `else` branch: `cycles = max(1, DAYS // max(info["max_day"], 1))`.

`routines.grow()`'s actual cycle length for a non-ongoing crop is `max_day + 1` days, not
`max_day`: the tile is harvested and cleared on day `p + max_day`, and can only be replanted the
*following* day, `p + max_day + 1`. Dividing by the bare `max_day` overcounts how many cycles fit
in a season.

**Measured** via actual `PLANT`/`HARVEST` op counts from `R.grow()` on a real 4-tile
`NARROW_BLOCK` nearest to spawn, full season:

```
crop      measured harvest-cycles/tile   formula's DAYS//max_day   corrected DAYS//(max_day+1)
WHEAT     6  (24 HARVEST ops / 4 tiles)  7  (30//4)                 6  (30//5)   <- matches measured
CARROT    7  (28 HARVEST ops / 4 tiles)  10 (30//3)                 7  (30//4)   <- matches measured
MELON     2  (8 HARVEST ops / 4 tiles)   2  (30//12)                2  (30//13)  <- same by floor coincidence
```

(`CARROT` also shows one extra `PLANT` per tile beyond the harvested cycles — a final planting
near season end that never completes, matching `production.py`'s own documented caveat about a
"final cycle that cannot finish before day 29" — that's a separate, already-known wrinkle and not
part of this bug.)

This is the opposite-direction, smaller-magnitude sibling of finding #3: it makes `WHEAT`/`CARROT`
tiles cost *more* estimated turns than they really do, understating `tiles_per_unit` for them.
Effect size: ~3% for `WHEAT` (minor — wheat is grown for cash-flow/feed reasons anyway, not
market-rank), ~30% for `CARROT` (irrelevant in practice since the leader and every measured genome
run zero carrot tiles).

**Fix:** `cycles = max(1, DAYS // max(info["max_day"] + 1, 1))`.

**Verification script:** the `PLANT`/`HARVEST` `Counter` over `unit_op`, shown above — same
pattern as finding #3's check, five extra lines.

---

## 5. `working_units()`'s comment understates the real cost of skipping units 3, 7, 11...

**File:** `kagg/search/chains.py:212-234`. The docstring's claim:

> "Skipping costs hires and the cost is small: hands are re-hired every dawn on a Fibonacci ladder
> that resets daily, so reaching unit 9 rather than unit 7 is a few dollars a day."

**Measured** against `kagg/sim/farm.py`'s actual `HIRE_COST` table
(`[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...]`, cumulative cost of hiring exactly `N` hands is
`sum(HIRE_COST[:N])`):

```
hands needed    daily hire cost
6               $20
7               $33
8               $54
9               $88
```

For an 8-slot farm, `working_units(8)` maps slots to units `[0,1,2,4,5,6,8,9]` (skipping 3 and 7,
the SE-spawns). Slot 6 therefore needs unit **8** (`$54/day`) instead of the naive unit **6**
(`$20/day`) — an extra **$34/day**, not "a few dollars". Slot 7 needs unit **9** (`$88/day`)
instead of unit **7** (`$33/day`) — an extra **$55/day**. Over even a two-week working window
that's **$500-$1,500** across the season, roughly 10-20x the comment's claimed magnitude.

**This does not corrupt any actual search result** — the JAX simulator applies the real Fibonacci
cost regardless of what the comment says, so every measured `$` figure in the logs already accounts
for it correctly. It is purely a documentation-accuracy issue: anyone reasoning about slot
economics from the comment alone (e.g. "is it worth adding a 9th or 10th slot?") would be off by an
order of magnitude. Worth fixing the comment, low priority otherwise.

**Verification:** `kagg.sim.farm.HIRE_COST`, `sum(HIRE_COST[:n])` for `n` in `{6,7,8,9}` — one line.

---

## Checked and found correct (per Alex's explicit request to verify, not just re-report)

- **`scheduler.expected_first_demand_day()`** — the formula (`mean of min(combo)` over
  `itertools.combinations(UNLOCK_DAYS, k)`) is exactly `E[min of a uniform random k-subset of the
  8 unlock days]`, which is the correct statistic given the unlock-day-to-shop assignment is a
  random permutation (so a random *subset* of k shops' days is genuinely uniform over all
  `C(8,k)` subsets). Confirmed correct, both as arithmetic and as "the right statistic to schedule
  on" — no bug.
- **`local_search.gene_values()`** — correctly reads the *current* `kind` for the slot being
  mutated before choosing the arity for `what`/`block`, matching `decode()`'s own kind-dependent
  modulo indexing. No cross-kind mismatch found. One inefficiency worth noting: for a slot whose
  `kind` is currently `"off"`, `gene_values()` still enumerates the full arity for `what`, `block`,
  `start_day`, `land_day`, `fertilize`, `fert_trade`, `feed_loop` — all of which `decode()` ignores
  for an off slot, so every one of those "neighbours" decodes to an *identical* script. This wastes
  a meaningful fraction of each sweep's evaluation budget on genomes indistinguishable from the
  current best (does not change the answer, just the time to reach it) — not worth fixing under
  deadline pressure, but easy: skip enumerating anything but `kind` when the slot is off.
- **`NARROW_BLOCKS`/`WIDE_BLOCKS` fit-validation using `WHEAT` as the probe crop for every block**
  (`chains.py:114-128`) — theoretically a mismatch, since ongoing crops need more turns/day once
  producing (see finding #3). Checked empirically: ran `STRAWBERRY` and `TOMATO` through every
  single wide and narrow block for a full season — **zero** raise a `ValueError`. So this
  mismatch does not currently exclude or wrongly admit any block from the catalog. Worth knowing
  it's a latent fragility (a future block geometry or crop could hit it) but it is not live today.
- **Ranch/grow sell-quantity multipliers** (`info["max_held"] * len(live)` for pens,
  `info["max_yield"] * n_harvested` for crops) and their timing relative to the dusk auto-drop —
  read through carefully; the same-day-vs-next-dawn logic is internally consistent with where
  `DROP` can actually reach the shed. No defect found here.
- **`land_schedule()`'s spacing rule itself** (`prev = max(prev + 1, first_order[j])`) is correct
  in isolation — parcel `j` is never bought before parcel `j-1`, and never on the same day. The bug
  in finding #2 is in what feeds it (`_land_requests`'s same-day-for-every-parcel-index recording)
  and in what gates it (`_affordable`'s day-3 cliff), not in the spacing arithmetic itself.

---

## Summary table

| # | file:function | class of error | measured effect | confidence |
|---|---|---|---|---|
| 1 | `chains.py` `decode()` | silent cross-slot tile double-booking | best genome's "1 wheat block" produces **zero** wheat all season; net effect currently +$1,310 by accident, sign not guaranteed | confirmed live, in the current best genome |
| 2 | `chains.py` `_affordable`/`land_schedule` | land-purchase gate doesn't model the chain's own cash flow | a legally-gated multi-parcel chain can silently never get its 2nd/3rd parcel; `decode()` reports it as used, not skipped | confirmed via synthetic genome + full turn-by-turn sim |
| 3 | `allocation_calculator.py` `turns_per_tile()` | missing op in the per-visit turn model | ~2x understates turn cost for STRAWBERRY/TOMATO, inflating their allocation rank | confirmed via direct `R.grow()` measurement |
| 4 | `allocation_calculator.py` `turns_per_tile()` | off-by-one cycle divisor | WHEAT +16%, CARROT +43% overcounted cycles, understating their tiles/unit | confirmed via `PLANT`/`HARVEST` op counts |
| 5 | `chains.py` `working_units()` docstring | wrong order-of-magnitude cost estimate | claimed "a few dollars/day", actually $34-55/day extra | confirmed via `HIRE_COST` table; no scoring impact |

Findings 1 and 2 are both plausible direct contributors to the $58k gap between the current best
($81,102) and the leader ($139,121): the leader's edge is substantially "buys land on day 7/10 and
grows 41 tiles of strawberry there, runs a working wheat-feeds-cattle loop" — both of exactly the
moves this review found the search's own code silently sabotaging.