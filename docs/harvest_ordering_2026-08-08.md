# The day-10 melon was never a delivery problem. The tile is not ripe until dusk.

Closed 2026-08-08, after seven prior arms on the delivery leg were reverted.

## The question that had not been asked

The evidence everyone worked from is `data/logs/melon_d10_side_by_side.log`: seed 11, day 10, weeds
off, the same eighteen melons on both sides.

```
SEB   h6 HARVEST, h9 HARVEST x2, h12, h14 -> SELL 12 @h13, SELL 6 @h15   melon in shed at d11 dawn: 0
OURS  h17 HARVEST, h19, h20                                              melon in shed at d11 dawn: 18
```

Read as "we deliver late", that is a delivery defect and it was attacked seven times.
Read as "we harvest late", it is an ordering defect.
It is neither.
`scripts/when_the_melon_fills.py` prints the third possibility, which nobody had measured: what the
**tile** was doing.

## The measurement

`python -u scripts/when_the_melon_fills.py 10` — both seats, same board, `yield_units` per ripe
MELON tile per hour, and the hour each tile first becomes harvestable at all
(`data/logs/melon_d10_fill.log`):

```
                                  h0    ...   fills at
SEB    (4,2)                     5/6            h6
       (3,1)                     5/6            h9
       (4,1)                     5/6            h9

OURS   (2,0)                     5/6            h15
       (1,0)                     5/6            h16
       (0,0)                     5/6            h18
```

**Both sides wake on day 10 with three MELON tiles at 5/6.**
MELON is a one-shot (`max_yield` 6, `max_yield_day` 12), and `router._one_shot_is_finished` refuses
HARVEST while `room > 0` — correctly, because HARVEST sets the tile to `None`
(`kaggriculture.py:409`), so on a one-shot it is a demolition and not a collection.
So neither side could have harvested before the tile filled.

Ours fill at h15/h16/h18 and are harvested at h17/h19/h20 — **one to three turns later**.
The HARVEST is prompt.
The DROP is prompt behind it.
The **WATER** is what runs seven hours late, and both the harvest leg and the delivery leg are
downstream of it.
Every one of the seven prior arms was moving a leg two steps below the cause.

`tests/test_the_filling_water_carries_the_harvest.py::test_the_pair_actually_executes_back_to_back_on_one_stop`
passes with the fix reverted, which is the same finding stated as a test: the WATER→HARVEST pair was
always executable, because `_live_ops` re-derives at the tile and the stop is not popped. Nothing was
ever stuck.

## The cause: the last water is priced as if it were the first

`crop_ops` prices an in-window one-shot water at the single unit of yield it adds:

```python
out.append(("WATER", None, price * (2 if fertilized else 1)))      # $250
```

That is right for a water with room to spare.
It is wrong for the **last** one, which is the only thing standing between the tile and its whole
harvest.
Meanwhile an out-of-window survival water on an immature melon is priced at `_crop_remaining` — the
whole tile, $1,250–$1,500 — because skipping it can weed the tile.

So the planner ranked insurance on a tile that cannot yield for two more days **five to six times
above** the one water that unlocks same-day cash.
`plan_routes` sorts by prize and scores by `prize / cost`, so it put them at dusk. From the
day-10 dawn plan (`scripts/when_the_melon_is_scheduled.py`, `data/logs/melon_d10_routes.log`):

```
before   u3   (2,0)WATER@h14$250        u11  (1,0)WATER@h15$250       u5   (0,0)WATER@h22$250
         u2   (3,0)WATER@h13$1250       u11  (1,1)WATER@h13$1250      u3   (2,1)WATER@h11$1250
```

The three $250 stops are the ripe melons. Everything beating them to the morning is an immature one.

## The fix — `FILLING_WATER`, `kagg/search/router.py`

When an in-window one-shot water fills the tile (`gain >= room`) and the crop is at or past its
`first_yield_day`, the node offers the HARVEST it unlocks as well.
No new mechanism: `_live_ops` already emits WATER, then HARVEST at the same stop on the next turn.
This only makes the planner see it coming.

```
after    u6   (2,0)WATER,HARVEST@h9$1750       u10  (1,0)WATER,HARVEST@h14$1750
```

## Day 10, the day it targets, field by field

`python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 12 --diff --no-moves`
(ours minus tape; blank = identical to the tape):

| d10 field | baseline | arm 1 | arm 2 |
|---|---|---|---|
| **money** | **-3082** | **-1548** | -3082 |
| **sh:melon** | **+12** | **0** | +6 |
| sell | +7 | +7 | +7 |
| harvest | 0 | -1 | -1 |
| water | 0 | -1 | -1 |
| drop | -8 | -6 | -7 |

The target field moved: the twelve melons that used to sit in the shed at day-10 dusk are gone, and
half the day's money gap closed, **+$1,534**.
Tile fill hours went `h15/h16/h18` → `h10/h15/never`: (2,0) five hours earlier, (1,0) one hour, and
(0,0) — the far corner, eight steps out — is no longer routed at all.

## Every day

| | d0 | d1 | d2 | d3 | d4 | d5 | d6 | d7 | d8 | d9 | d10 | d11 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| money, baseline | | | | +1 | -1 | | -137 | -128 | +30 | -858 | **-3082** | -422 | -4597 |
| money, arm 1 | | | | +1 | -1 | | -137 | -128 | +30 | -858 | **-1548** | -1516 | -4157 |
| cells, baseline | 3 | 3 | 3 | 5 | 3 | 3 | 8 | 6 | 8 | 13 | 14 | 14 | 83 |
| cells, arm 1 | 3 | 3 | 3 | 5 | 3 | 3 | 8 | 6 | 8 | 13 | 16 | 16 | 87 |

**d0–d5 are byte-identical to baseline**, which was the hard constraint.
d6–d9 are byte-identical too — the first ripe one-shot of the season is on day 10, so there is
nothing for the flag to change before it.

## The day-11 regression, reported not reverted

d11 money goes **-422 → -1516**, with `weeds +3`, `strawb -3`, `water -3`.
Three strawberry tiles on the brink went unwatered and weeded, because a filling water now outbids a
survival water — which is the trade the flag makes, taken at face value.
It has its own origin and is a separate problem: the honest reading is that `_crop_remaining` prices
a survival water as the whole tile whether the tile is one day or six days from yielding, so an
immature tile's insurance is not discounted for how long the farm has to wait for it.
Nothing here fixes that, and it should not be fixed by weakening `FILLING_WATER`, which is what
arm 2 amounted to.

Net over twelve days the change is still positive, **-4597 → -4157**, but that is not the selection
criterion and is recorded only for completeness.

## Arm 2, tried and measured worse

Arm 1 prices the unlocked HARVEST at `(held + gain) * price` = $1,500, on top of the WATER's $250, so
the node reads **$1,750 for a visit that banks $1,500**.
That is a real double count — the WATER already carries the unit it adds — and `held * price` is what
every other HARVEST in `crop_ops` is priced at.
Correcting it **gave back the entire gain**: d10 money -1,548 → **-3,082**, `sh:melon` 0 → **+6**.

The reason is a tie.
An immature melon's survival water is `_crop_remaining` = exactly $1,500 too, and at $1,500 against
$1,500 the filling water stops outranking it.
`test_a_filling_water_outranks_survival_water_on_a_tile_that_cannot_yield_yet` goes red on precisely
that assertion, which is how the mechanism was identified rather than guessed.
The surplus $250 is doing real work: certain money today and contingent value tomorrow are not the
same $1,500, and this node is the only place that difference is currently expressible.
Reverted, with the numbers recorded at the emission site so it is not re-derived.

## Tests

`tests/test_the_filling_water_carries_the_harvest.py`, 3 cases.
With `FILLING_WATER = False` two of the three go red — the pricing assert and the ranking assert.
The third (the pair executing back to back) passes either way **on purpose**, and says so in its
docstring: it documents that execution was never the defect, and must not be read as cover for the
flag.

`tests/test_router.py` and the router-adjacent suite: 113 passed, 6 skipped, 2 xfailed.

## What was NOT checked

- **One seed, one tape, twelve days.** Everything here is seed 11 against `seb` with weeds off. No
  12-seed ladder run, no win rate, no arena. The project's own rule is that seed variance is ~15% and
  that selection is on win rate, not money — this is a day-10 diagnosis, not a ladder result.
- **Days 12–29.** The flag fires on every one-shot crop from its `first_yield_day`, so it will act on
  wheat and carrot too, on every later day, and none of that is measured here.
- **Why (0,0) is now unrouted.** It is eight steps out, and adding a HARVEST makes the node YIELDING,
  which under `CLOSED_TOUR`/`RETURN_LEG` charges the walk home as well. That is a plausible reason and
  it is not confirmed — no test distinguishes "priced out by the return leg" from "lost the auction".
- **The day-11 weeds.** Traced only as far as `water -3` / `strawb -3` / `weeds +3` in the breakdown.
  Which three tiles, and to which unit's re-ordered tour, was not established.
- **Whether the $250 tie-break generalises.** It was measured on this one day. That the two prices
  collide at exactly $1,500 is a coincidence of MELON's numbers, not a principle.

## Files

- `kagg/search/router.py` — `FILLING_WATER` and the emission site in `crop_ops`.
- `tests/test_the_filling_water_carries_the_harvest.py` — the three tests.
- `scripts/when_the_melon_fills.py` — the measurement that found the cause.
- `scripts/when_the_melon_is_scheduled.py` — the committed day-10 tours, with each stop's ETA.
- `data/logs/melon_d10_fill.log`, `melon_d10_fill_arm1.log`, `melon_d10_routes.log`,
  `melon_d10_routes_arm1.log`, `harvest_baseline.log`, `harvest_arm1.log`, `harvest_arm2.log`.
