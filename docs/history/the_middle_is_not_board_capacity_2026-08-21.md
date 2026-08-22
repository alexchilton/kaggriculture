# The mid-season wheat count is not board capacity

Measured 2026-08-21 against `docs/kawashigi_algorithm_2026-08-21.md`, which states:

> The middle is not a plan at all — it is "plant wheat on every tile you can reach today", and the
> number of tiles is a property of the board, not a decision.

and flags it as "the single most load-bearing unverified claim in this document".

**It is false.** Kawashigi ends 85.7% of his mid-season days with unlocked, empty, affordable ground
on the board. He is not filling it.

The task that commissioned this measurement said to stop and report if the claim failed rather than
build on it. No agent was built. What follows is the measurement and what it does and does not kill.

Scripts: `scripts/is_the_middle_capacity.py`, `scripts/did_he_have_the_turns.py`,
`scripts/what_sets_the_mid_wheat_count.py`, `scripts/dusk_bias_check.py`.
Logs: `data/logs/is_the_middle_capacity_v2_2026-08-21.log`,
`data/logs/did_he_have_the_turns_2026-08-21.log`,
`data/logs/what_sets_the_mid_wheat_count_2026-08-21.log`,
`data/logs/dusk_bias_check_2026-08-21.log`.

Every number below is read out of a recorded observation in the raw replays. Nothing is simulated,
so no model of the game can be wrong in it. 2,982 day-rows, d14-d27.

## The count against the board

`free_dawn` is `tiles[y][x] is None` at hour 0 — the only plantable tile state
(`kaggriculture.py:425`). `everfree` is the union over all 24 hourly observations, so it includes
every tile a HARVEST opened mid-day; WHEAT is `ongoing: False`, so harvesting one clears its tile
and it can be replanted the same day. `dusk` is the empty count in the h23 observation.

     day     n planted    wheat    dawn everfree     h12    dusk  seedcap    money
      14   213    2.11     2.11    5.76    10.16    5.76    8.06    10.10    14949
      15   213    7.54     7.54    8.15    15.18    9.42    7.65    14.56    17863
      16   213    6.56     6.56    8.20    13.97    9.37    7.41    15.07    21462
      17   213    3.73     3.73    7.47    11.43    8.39    7.67    11.48    27087
      18   213    6.43     6.43    7.75    10.62    8.06    4.19    15.04    31495
      19   213    5.48     5.48    4.23    11.13    4.92    5.65    12.76    37294
      20   213    5.35     5.35    5.90    12.17    6.89    6.82    13.63    43391
      21   213    4.63     3.26    7.07    11.88    7.60    7.24    11.72    48797
      22   213    8.38     7.25    7.59    16.20    8.95    7.83    14.76    55408
      23   213    7.11     6.75    8.31    15.23    8.99    8.12    14.58    61593
      24   213    6.54     5.77    8.53    16.17    9.23    9.63    13.74    67684
      25   213   11.25     9.80   10.27    19.52   11.37    8.27    17.73    71740
      26   213    9.59     8.81    8.78    17.63   10.00    8.04    16.86    75895
      27   213   11.52    11.52    8.46    19.66    9.99    8.14    19.23    78660

    POOLED d14-d27, 2982 day-rows
      planted == ever_free         8.2%   (planted EVERY tile the board offered)
      wheat   == ever_free         6.9%
      wheat   == free_dawn         7.9%
      dusk    == 0                 8.2%   (board full overnight)
      dusk    >= 3                72.7%   (three or more tiles left empty)
      mean tiles left empty at dusk   7.48
      corr(wheat, free_dawn  )   0.274
      corr(wheat, ever_free  )   0.507
      corr(wheat, free_by_h12)   0.327
      corr(wheat, seed_cap   )   0.921
      corr(wheat, units      )  -0.273
      corr(wheat, money_dawn )   0.388
      corr(wheat, unlocked   )   0.078

`corr(wheat, seed_cap) = 0.921` is the one large number and it is not evidence of anything. The doc
already established that he buys the seed he is about to plant, so the seed purchase is downstream
of the decision, not a constraint on it.

Money is not the constraint either. A WHEAT seed is $10 and his mid-season bank runs $15k to $79k:

    2738 rows left a tile empty overnight; 2738 (100.0%) could have afforded the seed for
    every one of them at dawn.

## The h23 read is biased, and correcting it does not save the claim

The h23 observation is the board *before* that turn's PLANT lands, and his planting is heavily
back-loaded — 16.4% of all mid-season PLANT ops fire at h23, and 68.7% at h18 or later. So `dusk`
overstates the empty count.

The bias-free version is the *minimum* free-tile count over all 24 hourly observations. If the board
is ever full, this is 0 whatever hour the last plant landed.

    POOLED  mean min_free 6.18   mean h23_free 7.48
      min_free == 0 (board full at SOME hour)  14.3%
      min_free >= 3                            58.0%

The bias is 1.3 tiles. **The board is never full at any hour of the day on 85.7% of his mid-season
days**, and on 58.0% of them it never gets below three empty tiles.

## He was not idle, and that is the interesting part

The obvious objection is reachability: empty and affordable is not the same as reachable. It does
not hold up as a general explanation, but it points at the mechanism that does.

     day     n   budget     idle   travel     work   plant   water      dusk
      14   213    208.0     10.0    105.0     93.0    2.11   30.44      8.06
      15   213    287.0      5.0    160.0    122.0    7.54   45.85      7.65
      16   213    230.0      7.5    120.1    102.3    6.56   32.92      7.41
      17   213    288.0      6.6    159.4    121.9    3.73   45.16      7.67
      18   213    291.0     14.4    158.6    118.0    6.43   39.94      4.19
      19   213    291.0      9.6    159.8    121.6    5.48   43.51      5.65
      20   213    291.0      6.6    151.3    133.1    5.35   45.56      6.82
      21   213    291.0      3.2    161.0    126.7    4.63   31.79      7.24
      22   213    291.0      1.0    153.3    136.7    8.38   45.61      7.83
      23   213    291.0      2.7    160.9    127.4    7.11   32.95      8.12
      24   213    271.0      0.3    143.3    127.4    6.54   38.18      9.63
      25   213    270.0      0.3    142.8    126.9   11.25   31.89      8.27
      26   213    269.9      0.7    138.8    130.4    9.59   47.33      8.04
      27   213    270.0      2.2    142.6    125.1   11.52   36.02      8.14

    POOLED d14-d27, 2982 day-rows
      mean idle unit-turns per day        5.01
      days with ZERO idle turns           43.4%
      idle share of budget                 1.8%
      travel share of budget              53.6%
      WATER share of all work             31.9%
      PLANT share of all work              5.6%

His day is turn-saturated: 1.8% idle, and 43.4% of days have no idle turn at all. More than half the
budget is walking, and a third of the work is watering. Planting is 5.6% of what he does.

So the count is bounded by the **turn budget**, not by the tile count. That is a property of his
routing, not of the board, and it is not something an agent can read off the dawn observation.

## What actually predicts the count — nothing well

    corr(wheat, tiles freed today   )   0.598    exact match 15.7%
    corr(wheat, HARVEST ops today   )   0.277    exact match  1.2%
    corr(wheat, WHEAT tiles at dawn )   0.197    exact match  0.2%
    corr(wheat, wheat planted d-1   )   0.181    exact match  9.7%

"Replant what you just harvested" is the best of the four and still only r=0.598 with a 15.7% exact
match. It is not a rule.

Nor is the count a per-season constant:

    IS THE COUNT A PER-SEASON SCALAR?  213 seasons
      grand mean wheat/day        6.45
      between-season SD of means  0.71
      mean within-season SD       3.57
      -> within/between ratio     5.03

The day-to-day spread inside one season is five times the spread between seasons. One number per
season does not describe the middle.

## What this kills and what it does not

**Killed:** "the number of tiles is a property of the board". The wheat count is not free tiles, not
free tiles plus mid-day frees, not harvests, not yesterday's plant, and not a per-season scalar.
Every board-side quantity tried tops out at r=0.6.

**Killed:** "plant wheat on every tile you can reach today" as a *specification*. Applied literally
it would roughly double his plant count — mean 6.45 wheat against a mean `everfree` of 14.4 — and
there are no turns for it. His day is already 98.2% committed with a third of the work going to
WATER, and every extra tile planted is a watering obligation on every following day.

**Not killed, and still unverified:** the design conclusion that d14-d27 needs no row library. The
count is turn-bounded rather than menu-selected, which is consistent with a planner producing it. But
it would be *our* router's turn budget setting the number, not his, and nothing here measures whether
those agree. Treat "the greedy planner already produces it" as an open question, not a finding.

**Holds:** the crop-mix half of the claim. `planted == wheat` exactly on d14-d20 and d27; d21-d26
carry 1-2 CARROT and nothing else. No melon, no tomato, no potato in the middle, as the doc says.

## A correction to the source doc's n

`data/target_rows_kawa_norm.json` has 6,840 day-rows and 228 rows per day, but only **213 distinct
game-seats**. Fifteen game-seats appear twice, because the same game id was downloaded into two
directories under `data/seed_scripts/`. Every "228 seasons" in
`docs/kawashigi_algorithm_2026-08-21.md` is 213 independent observations, and the duplicated fifteen
are counted twice in every distinct-row and coverage figure in it. The effect on those tables is
small but they are not measured on 228 independent seasons.

## Unverified

- Whether **our** planner's turn budget produces a wheat count near his. Not measured.
- Why he leaves 6+ tiles empty. The turn saturation is consistent with it but is not proof of
  intent — a routing that never reaches those tiles and a decision not to plant them look identical
  in a replay.
- Everything here is Kawashigi alone. The source doc's own caveat about Ryo Hasegawa and tetsuya
  applies unchanged.
