# The conditional carrot sweep, 2026-08-22

12,096 seasons, 5h07m on the box (13:42:48 -> 18:50:08 CEST).
Raw rows: `data/logs/carrot_refine_rows_2026-08-22.csv` (pulled local), box copy at
`~/kaggriculture/data/logs/carrot_refine_rows_2026-08-22.csv`.

## What the arm changes

`kagg/search/tape_edit.py::carrot_when_it_pays(agent, drain_min, opp_tiles_max, days=(25,26,27))`.

On the first turn of day 25 it decides once, then for d25-d27 rewrites `PLANT WHEAT` to
`PLANT CARROT` and re-points that day's `BUY_SEED WHEAT` to `CARROT`.

The decision is `drain >= drain_min and theirs <= opp_tiles_max`, where `drain` counts the town's
unlocked shops that buy CARROT (2 if the shop buys only carrot, else 1) and `theirs` counts the
opponent's standing CARROT tiles.

**The grid was `drain_min` x `opp_tiles_max`, not day x anything.** The arm names read
`cond_carrot_d{3,4,5}_o{3,7,99}`, where `d` is the drain threshold. This was misread as a day
during analysis and corrected.

## Result

48 towns x 7 opponents x 3 seeds = 1008 paired seasons per arm. Pairing is exact: every arm sees
the same (town, tape, opponent, seed).

    arm                     mean ours     win%    vs ctrl   rows differing
    control                     88282     54.7         +0        0/1008
    carrot2_d25d27              88316     55.3        +34     1006/1008
    carrot4_d25d27              88539     56.2       +257     1008/1008
    cond_carrot_d3_o3           89377     60.2      +1096      630/1008
    cond_carrot_d3_o7           89377     60.2      +1096      630/1008
    cond_carrot_d3_o99          89377     60.2      +1096      630/1008
    cond_carrot_d4_o3           89412     60.1      +1130      525/1008
    cond_carrot_d4_o7           89412     60.1      +1130      525/1008
    cond_carrot_d4_o99          89412     60.1      +1130      525/1008
    cond_carrot_d5_o3           89361     60.0      +1080      441/1008
    cond_carrot_d5_o7           89361     60.0      +1080      441/1008
    cond_carrot_d5_o99          89361     60.0      +1080      441/1008

Win rate by opponent band:

    arm                  low    mid    top  mirror
    control             48.6   50.0   58.6    58.3
    carrot4_d25d27      49.3   50.3   60.2    63.2
    cond_carrot_d3_o*   54.9   54.2   63.2    68.8
    cond_carrot_d4_o*   54.9   54.2   63.0    68.8
    cond_carrot_d5_o*   54.9   54.2   63.0    68.1

Paired McNemar against control, on the win/loss flip:

    cond_carrot_d4_o3    flips +55 -0   net +55   z=7.42
    cond_carrot_d3_o3    flips +57 -1   net +56   z=7.35
    carrot4_d25d27       flips +28 -12  net +16   z=2.53

## What is real

**The town condition works and is the load-bearing half.** `drain_min` moves the arm monotonically
-- 630 / 525 / 441 rows touched as the threshold rises 3 -> 4 -> 5 -- and the win rate lifts
54.7% -> 60.1% overall, including 58.6% -> 63.0% against the top band. 55 games flip to a win and
none flips to a loss. This is a win-rate result, which is the selection criterion; the +$1,130 of
money is inside seed variance and should not be quoted as the finding.

The static `carrot4_d25d27` is much weaker (z=2.53, and it loses 12 games it used to win). Making
the decision at runtime, where it can see the board, is what the conditional buys.

## Where the win actually lives -- the aggregate was hiding it

The 60.1% headline is an average over towns the rule never touches. Cut by the town's carrot drain,
`control` against `cond_carrot_d4_o3`, same 1008 pairs:

    drain   n     control   cond    delta    fired
        0   126     73.0    73.0    +0.0     0/126
        1    84     67.9    67.9    +0.0     0/84
        2   168     54.2    54.2    +0.0     0/168
        3   105     61.0    61.0    +0.0     0/105
        4    84     42.9    44.0    +1.2    84/84
        5   231     42.0    51.1    +9.1   231/231
        6   147     57.8    71.4   +13.6   147/147
        7    63     46.0    66.7   +20.6    63/63

Monotone in drain, and **drain 4 is a wash**. The recommended `drain_min=4` buys one bucket worth
+1.2 points on 84 seasons. Everything of value is at drain >= 5.

Note also that drain 4-5 towns are where the unedited agent is *weakest* (control 42.9% and 42.0%,
against 73.0% at drain 0). The rule rescues our worst towns rather than padding our best.

Town drain distribution over the 48 sampled towns:

    drain    0   1   2   3   4   5   6   7
    towns    6   4   8   5   4  11   7   3

So **44% of towns are drain >= 5**, where the rule pays.

`drain_min=6` was never tested and the trend is still rising at 7. 5 is the best TESTED value, not
established as the best value.

## How much carrot the opponents actually plant

Measured 2026-08-22 from `data/seed_scripts/top_guys/`: 85 replays read, 170 player-seats, counting
standing CARROT tiles at step 600 (day 25, the decision turn) and the season peak.

    CARROT AT DAY 25              PEAK CARROT OVER THE SEASON
        0 tiles  160 (94%)            0 tiles  145 (85%)
      >=4 tiles    7 (4%)           >=4 tiles   13 (8%)
      >=8 tiles    4 (2.4%)         >=8 tiles   11 (6%)
     >=13 tiles    3 (2%)          >=13 tiles    5 (3%)

94% of seats hold no carrot at the decision point and 85% never plant one all season. That is the
mechanism behind the byte-identical `o3`/`o7`/`o99`: the guard had nothing to guard against.

Keep `opp_tiles_max=7` regardless. It costs nothing, and `carrot_when_it_pays`'s own prior measured
the `opp CA 15+` bucket at **-$510, 28% improved** -- a real tail that ~1-2% of seats reach.

Two limits on this sample, both real:

- These replays are **downloaded losses** (Alex's standing rule). Acceptable for a crop-mix
  statistic, not for anything rate-like.
- Their game IDs are 90.4M-91.2M, **older than the tape teacher's games** (91.9M-92.5M). The
  2026-08-15 balance change put CARROT on the `hinge` price curve, so if these predate it the
  field's carrot appetite may have shifted since. Not checked.

## Recommendation

Ship it at **`drain_min=5, opp_tiles_max=7`**, not the docstring's 4.

`carrot_when_it_pays` lives in `kagg/search/tape_edit.py`, which is NOT in
`scripts/build_planner_submission.py::MODULES`. The shipped agent is
`kagg/search/schedule_agent.py`. Inlining the rule there is preferable to adding a module to the
bundle.

Open first: whether `drain_min=6` beats 5. One arm, control plus two thresholds, ~2,000 seasons.

## What the sweep did NOT measure

**`opp_tiles_max` never binds on this opponent field.** `o3`, `o7` and `o99` are byte-identical in
every band, at every drain threshold. The field is 7 leaderboard agents, all melon openers
(`melon@d3` 11-12), so `theirs` -- their standing carrot at d25 -- is always <= 3 and all three
thresholds pass.

Six of the nine conditional arms were therefore a wash **by construction**, and it was predictable
before launch: `carrot_when_it_pays`'s own docstring says the opponent test "only removes the 15+
bucket", and the log header at 13:42 lists an opponent field with nobody in it.

So this run cost 12,096 seasons to answer a question 4,032 would have: control plus three drain
thresholds. The opponent half of the rule is still untested and needs a field containing a carrot
player.

`mean drain_CARROT` is 3.5 for every arm including control, which is correct and not a bug: it is a
property of the town draw, and the arms share towns by design.

## Process failure

The run finished at 18:50 and was not looked at until 20:11, on Alex asking. There was no waiter on
it and it was not checked once in five hours, though it printed a progress line every 200 seasons.

The arm was analysed only after the numbers were in hand, and a McNemar z was quoted before anyone
had read what the arm does. The standing rule -- state in one sentence what the arm changes and what
would have to be true for it to win, BEFORE the sweep -- would have caught the inert `o` axis from
the log header alone.
