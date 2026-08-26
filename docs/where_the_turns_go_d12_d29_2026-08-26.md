# Where the turns go, d12-d29: ours against カワシギ

Measured 2026-08-26 on the Mac, worktree `corner`, branch `shaping-potential`.

Sources:

- **Ours:** 54 ladder replays at `data/seed_scripts/ours_2026-08-26/`, every episode of the two
  newest submissions (`carrot_only` 27 games, `d28` 25 games). Not selected by outcome, so a win
  rate from this set is meaningful -- unlike `data/seed_scripts/losses*`, which Alex downloads by
  hand and which are losses by construction.
- **カワシギ:** 76 seats across `downloads_2026-08-19/20/21`, `kawa_2026-08-24`, `leaders_2026-08-24`.
  The op histogram below is a 10-seat subsample of the same files (40 per dir) and its PASS gap
  (+281.6) agrees with the 76-seat table's (+225), so the subsample is not driving the result.

Scripts: `scripts/what_differs_from_d12.py`, `scripts/what_our_losses_look_like.py`.
Logs: `data/logs/d12_diff.log`, `data/logs/our_losses.log`, `data/logs/op_histogram.log`.

## The headline: we idle, he walks

Alex's theory was that we over-plant late and cannot then harvest it.
**The planting is identical and the theory is refuted.**
What is not identical is what the crew does with the rest of the day.

Per seat, d12-d29:

```
op                 kawa     ours     diff
WEST              736.7    555.4   -181.3
WATER             702.3    761.8    +59.5
NORTH             666.6    608.0    -58.6
EAST              596.4    438.0   -158.4
SOUTH             574.0    492.6    -81.4
HARVEST           358.5    348.5    -10.0
COLLECT_FERTILIZER 242.1    258.1    +16.0
FEED              206.1    242.4    +36.3
CARE              205.0    242.1    +37.1
PASS              200.9    482.5   +281.6
PLANT             115.8    112.0     -3.8
PICKUP             83.8    166.9    +83.1
FERTILIZE          65.5    122.3    +56.8
PLACE              27.9      4.2    -23.7
DIG                23.8     39.4    +15.6
DROP                9.0     43.7    +34.7
BUILD_PASTURE       1.2      0.9     -0.3
TOTAL            4815.6   4918.9
```

- **PLANT 112.0 vs 115.8.** Equal, and equal day by day. We do not over-plant.
- **HARVEST 348.5 vs 358.5.** Ten ops.
- **He walks 2,574 turns; we walk 2,094.** He spends 480 more turns moving.
- **He PASSes 201; we PASS 482.** We stand still for 282 more unit-turns.

The crew is identical day for day (11, 12, 9, 13, 10, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12,
11, 9), so this is not a hiring difference. The same crew is given less to do.

**This corrects an earlier reading of mine.** On 2026-08-25 I wrote that the day is full of walking
and there are no spare turns, from a d29 breakdown of one game. d29 is the single day where he
idles more than we do. Across d12-d23 the picture is the opposite.

## The idle is d12-d23 only, and it stops where the solver stops

Extra PASS turns, ours minus his, by day:

```
d12 +44.9   d15 +43.9   d18 +39.8   d17 +24.2   d19 +20.1   d13 +19.7
d20  +9.5   d16  +9.0   d22  +8.4   d21  +8.2   d14  +6.7   d23  +3.9
d24  -0.8   d25  +0.1   d26  +3.6   d27  -1.0   d28  -9.9   d29  -5.4
```

d12-d23 is the SOLVER zone. d24-d29 is the live PLANNER.
**Every extra idle turn is in the solver zone, and the effect ends exactly where the solver hands
over.** From d24 on we are as busy as he is.

The worst days -- d12, d15, d18 -- are big-crew days. d14 (crew 9) and d16 (crew 10) have almost no
excess idle. The pattern is consistent with the solver failing to use the hands it has once the crew
passes some size, though the mechanism has not been read out of the code yet.

## The standing crop is a LAG, not an accumulation

Standing units at day end, ours vs his:

```
day   d14   d16   d18   d20   d22   d24   d26   d28   d29
ours 68.8  48.1  59.9  57.0  59.3  66.1  68.9  34.2  14.0
his  49.2  42.0  47.8  38.8  43.3  43.6  56.8  14.0   2.1
```

We run ~15-20 units above him from d14 onward, every single day, with near-equal PLANT and HARVEST
flows. That is a constant offset, not a build-up: we collect the same crop later in its life.
The 14.0-vs-2.2 gap at the bell is the tail of that offset, not a separate defect.

## The second gap: a fertilizer chain he barely runs

```
PICKUP             +83.1
FERTILIZE          +56.8
DROP               +34.7
COLLECT_FERTILIZER +16.0
                  ------
                   ~191 turns per season
```

He fertilizes 65 times; we do it 122. He picks up 84 times; we do it 167.
Whether those 191 turns pay for themselves has not been measured.
`PLACE` runs the other way -- 27.9 for him against 4.2 for us -- and has not been looked at.

## The losses: three hypotheses, none survive

54 games, 41 W, 13 L, **75.9%**.

```
   episode          arm    margin      ours    theirs  cow  shp  stand  tiles   wool   milk  opponent
  99856433  carrot_only   -14,310    72,698    87,008    6   12     25     45     43      9  kaggle Osaka
  99858484          d28   -12,003   110,704   122,707    6   12     12     40     31    124  Debmalya
  99856181  carrot_only    -7,878    99,641   107,519   10    4     18     26      1     53  ömer kiraz
  99860770  carrot_only    -7,204   101,103   108,307   10    4     12     28      5      1  Yusei Ito
  99872241          d28    -5,837    95,474   101,311   10    4      3     20    148      3  Joanna C.
  99840121          d28    -2,945    63,364    66,309   10    4     18     31      5      3  Gebreab K. Zewdie
  99849273          d28    -2,258    68,991    71,249   10    4     14     33      1      1  Stefano Blando
  99851573          d28    -1,661    84,833    86,494   10    3     22     31    158      1  uitsnf
  99842398  carrot_only    -1,528   119,177   120,705    6   12     15     34    232    124  HaniJezo
  99869955  carrot_only    -1,360   131,982   133,342   10    4     23     29      5    122  dunky su
  99851574  carrot_only      -675    87,599    88,274   10    4     19     31    148      1  ra5anchor
  99876816          d28      -292    73,136    73,428   10    4      4     23    141      1  rupsa roy
  99867553  carrot_only      -230    69,969    70,199   10    4     10     26      1      1  Kaggs
```

- **Not a match-up.** 13 losses, 13 distinct opponents, zero repeats.
- **Not the herd.** 10c/4s loses 9 and wins 28; 6c/12s loses 3 and wins 6. Same rate.
- **Not standing crop, within our own games.** 15.0 units in losses vs 13.6 in wins -- worth roughly
  $300 against a median loss of $2,258. The standing-crop gap is real against カワシギ and is not
  what decides a ladder game.

What IS true is the shape:

```
LOSS  n=13  median $2,258   under $2,000: 6   under $10,000: 11   max $14,310
WIN   n=41  median $12,541  under $2,000: 7   under $10,000: 16   max $106,296
```

**We win big and lose small.** On an Elo ladder a $106,296 win and a $94 win score identically, so
the surplus in the blowouts is worth nothing. Converting a $1,500 loss into a $500 win is worth more
than adding $20,000 to a game already won.

One unresolved correlate: `wool` at the bell averages 70.7 in losses against 103.3 in wins, and
`milk` 34.2 against 70.1. **This is not yet a cause** -- the bell price is downstream of our own
selling, so a dead book may be a symptom of a close contested game rather than the reason we lost
it.

## Two thirds of those idle turns had reachable work

`scripts/what_the_idle_units_could_have_done.py`, 54 seats, d12-d23, log `data/logs/idle_ours.log`.

For every PASS turn: was there a crop tile carrying `yield_units > 0` close enough that this unit
could walk there, HARVEST, and still reach a shed access tile before the bell --
`cheb(unit, tile) + dist_to_shed(tile) + 1 <= turns_left`? And was that tile left uncollected by
every other unit of ours that day?

```
  day     PASS  reach ripe  UNCLAIMED  thirsty  correct
   12     45.6        31.4       31.4     35.4     10.2
   13     61.5        41.4       41.4     45.5     15.9
   14     10.5         2.4        2.4      3.7      6.9
   15     50.9        33.9       29.4     38.2     12.3
   16     12.4         3.1        3.1      4.3      8.1
   17     33.9        20.2       20.2     23.6     10.3
   18     51.5        31.7       31.7     35.6     15.8
   19     28.3        16.2       14.7     19.2      9.1
   20     13.6         5.3        5.3      4.6      8.2
   21     10.7         4.4        4.4      5.1      5.4
   22     12.0         4.7        4.7      4.0      7.1
   23      7.5         2.5        2.3      3.4      4.1

   PASS turns per seat                          338.5
   ... with a reachable ripe tile               197.3
   ... with an UNCLAIMED reachable ripe tile    191.1
   ... with a reachable thirsty tile            222.5
   ... nothing reachable: a CORRECT pass        113.3
```

**Only 113 of 338 idle turns are correct.** 191 of them are spent standing next to ripe crop that no
other unit collects that day.

Two caveats, both making the bound generous rather than tight:

- The reachability test is what ONE unit could do alone. It ignores that the unit may already be
  mid-tour with a load, and it ignores carrying capacity.
- `watered_today` was confirmed as a real tile key before trusting the `thirsty` column
  (`{"consecutive_unwatered": 1, "crop": "STRAWBERRY", ..., "watered_today": false}`).

## What the idle turns actually are -- three corrections to the number above

The 191 figure above was measured on the 54 ladder replays with a wrong predicate, and it moved
twice more before it settled. Recording the whole chain because the corrections are the useful part.

| version | harvest turns | what was wrong |
|---|---|---|
| 54 replays, `yield_units > 0` | 191 | ripeness is not harvestability |
| seed 11, real `crop_ops` | 75 | -- |
| water column, unfiltered | 163 | did not exclude tiles another hand waters later |
| water column, filtered | 128 | mixed brink waters with optional parity waters |
| water column, split | **58 brink** | -- |

**Correction 1: ripe is not harvestable.** `router.py:759-760` offers HARVEST on a one-shot crop only
once `_one_shot_is_finished` -- the window has shut or the tile is full. HARVEST sets a one-shot tile
to `None` (`reference/kaggriculture.py:409`), so taking it early is a demolition that forfeits the
units still owed. Seed 11 lost five tiles on day 3 to exactly that bug. On d12-d23, **394 ripe tiles
produce 147 HARVEST offers, with 0 pinned out and 0 locked out** (`data/logs/ripe_offered.log`).
Most of the 247 declines are the router being right.

**Correction 2: the router is not dropping routed work.** Fable's links 3 and 4 -- leftovers refused
by `_insert_leftovers` and then discarded unread at `schedule_agent.py:635` -- are refuted.
`data/logs/solver_drops.log`: **9 dropped jobs out of 748** across d12-d23.
Falling through at `cover.py:1160` to reach COMPACT/REPAIR would recover 9 jobs a season.
The cap is not in `cover` at all; the day's job LIST is simply shorter than the crew.

**Correction 3: a parity water is not a missed water.** `crop_ops` offers a safe tile a water on
`(x + y + day) % 2 == 0` at `_crop_remaining / TOP_UP_DISCOUNT`, and skipping it is what the
alternation is FOR -- the tile is offered again tomorrow. `TOP_UP_SAFE_TILES` watered every safe
tile every day and measured **$79,905 -> $63,645**. Counting those as opportunities would have
rebuilt that flag by hand.

### What survives, seed 11, `data/logs/idle_offered3.log`

```
  day    PASS  HARVEST avail  WATER avail  of which BRINK  correct
   12      51             30           30               8       19
   13      78              0           50              23       28
   15      48             19           20              14       27
   18      47             16           14              13       30

d12-d23 (solver): PASS 319   harvest available 75   water available 128 (BRINK 58)   correct 183
d24-d29 (planner): PASS 61   harvest available 19   water available 16 (BRINK 14)   correct 42
```

**58 idle unit-turns in the solver zone had a reachable tile at `consecutive_unwatered >= 1` that no
other hand watered that day.** A second dry night weeds it (`kaggriculture.py:771`), which is why
`crop_ops` prices that water at the whole tile rather than the one unit a water adds.
Not the optional parity water, so filling it is not `TOP_UP_SAFE_TILES` again.

Caveat: 58 is a count of TURNS, not of distinct tiles -- two idle hands in reach of the same tile in
the same turn count twice. The distinct-tile count has not been measured.

The outcome test is the weed count, since the op histogram already shows **DIG 39.4 ours vs 23.8
his** (`scripts/how_many_weeds_are_our_own.py`, `data/logs/weeds.log`).

## The standing-crop gap is 3.6 points of efficiency, not a 6x failure

`scripts/how_full_is_each_harvest.py`, log `data/logs/harvest_size.log`.

```
                     units taken/seat    left standing
KAWASHIGI (15)                  232.0    1.5 units on 1.1 tiles
OURS      (54)                  323.0   14.0 units on 6.6 tiles
```

**We out-produce him by 39%.** So the standing crop has to be read as a share of production, not as a
raw count:

- ours 14.0 of 323 taken = **4.2%** left on the field
- his   1.5 of 232 taken = **0.6%**

A ~3.6-point gap, worth roughly $3-4k on a $100k season. Real, and the same order as the median loss
($2,258) -- but "14.0 against 2.2" was a ratio between two small numbers, and quoting it as a 6x
failure overstated it all day.

### A measurement caveat that took three checks to pin down

A HARVEST op carries no target (`['HARVEST']`), so the tile has to come from the acting unit's
position. Of 338 harvests in one replay:

```
crop tiles   221      a crop harvest
animal pens   80      HARVEST on a pen collects milk/wool/eggs -- the pen has `animal`, not `crop`
non-dict      36      unattributed: the position maps to a tile that is not a dict
```

**89.1% attributed, 10.7% not.** The per-crop rows below are good to about that, not exact. The
`units taken` and `left standing` figures above do NOT depend on the position mapping -- they are
read off the final board -- so they are unaffected.

Per crop, both sides:

```
   crop        ops/seat     units/op his   units/op ours
   STRAWBERRY     ~110           0.33            0.22
   WHEAT           ~85           1.75            2.35
```

**Both of us spend ~110 harvest ops a season on strawberry for 24-36 units** -- 3 to 5 ops per unit
on the most-harvested crop on the board. He is ~50% better at it than we are. Neither of us is good
at it, and it is 110 turns either way. Not yet investigated.

## Open, in order of size

1. **Why does the solver decline reachable work on 191 unit-turns in d12-d23?** Not yet read out of
   the code. The days it happens on are the big-crew days, and it ends exactly at d24.
2. Do the 191 fertilizer-chain turns pay?
3. What is `PLACE` 27.9 vs 4.2?
4. Are the six sub-$2,000 losses winnable, and by what?
