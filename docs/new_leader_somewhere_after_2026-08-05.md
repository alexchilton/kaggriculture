# The new leader: `somewhere after`

Four replays pulled 2026-08-05 (`~/Downloads/new/9001*.json`, `90023239`), analysed by
`scripts/analyse_new_leader.py`, raw output in `data/logs/new_leader.log`.

## He wins every game, by two to four percent

| episode | seat | opponent | his bank | theirs | margin | % |
|---|---|---|---|---|---|---|
| 90016067 | 1 | haoran huang430 | 160,593 | 157,959 | +2,634 | +1.7% |
| 90018004 | 1 | manual player | 134,780 | 130,777 | +4,003 | +3.1% |
| 90020633 | 1 | Savko | 137,667 | 133,335 | +4,332 | +3.2% |
| 90023239 | 0 | Savko | 123,443 | 118,437 | +5,006 | +4.2% |

4/4, mean bank **$139,121**, mean margin **+3.1%**.

The margin is the point.
Everyone at the top banks $120k-160k and the leader edges it by a few thousand dollars.
On an Elo ladder a $2,634 win scores exactly what a $50,000 win scores, so the top of this
leaderboard is a knife-edge contest between several near-equal fixed scripts, not a blowout.
Our best is $67,535 (`data/logs/arena_gate.log`), which is not yet in the same conversation.

## It is a fixed open-loop script, and this is the hardest evidence yet

Every derived quantity below is **byte-identical across all four replays** -- same land days, same
herd, same seed counts, same fertilizer flows, same crew ramp -- in **seat 0 and seat 1**, against
**four different opponents**.
The only variation anywhere in the four tapes is 107 vs 106 `FERTILIZE` ops.

That closes any remaining doubt about the project thesis in
[`project_kaggriculture_open_loop`]: the top of this leaderboard submits a fixed 720-turn sequence
and does not react to the opponent at all.

## His farm against ours

| | `somewhere after` | us (2026-08-05) |
|---|---|---|
| land | days **7 and 10**, two parcels, never SE | day 0, hardcoded |
| herd | **8 COW + 6 SHEEP = 14 pens** | 4 COW |
| crops | WHEAT 66 (50%), STRAWBERRY 44 (34%), MELON 21 (16%) | near-monoculture MELON |
| fertilizer | 318 collected, **107 applied**, 0 bought, 445 offered | 0 collected until 2026-08-04 |
| crew | 4 hands on day 0, ramping 4-6-5-5-6-6-6-8-10-11-12, flat 12 from day 10 | `max(unit index)` |
| bank | $139,121 mean | $67,535 |

## Five things this changes

1. **Land on days 7 and 10 is confirmed, independently, in four fresh tapes.**
   Our catalog hardcoded `LAND_DAY_CHOICES.index(0)` for every land-needing chain, so the forward
   pass -- where the crop/animal mix is decided -- could only ever propose day 0.
   Widening the grid to 30 days achieved nothing while that `.index(0)` stood.

2. **He does BOTH with the fertilizer.**
   107 units onto crops, the surplus offered to market, none bought.
   This vindicates making `fert_trade` a per-chain gene rather than one global switch, and it
   deflates the "selling beats applying 6:1" measurement, which used one 4-tile block and two cows.
   With 14 pens making 318 units a season he can afford to do both; we could not.

3. **`DIG` is in the op vocabulary and `routines.py` never emits it.**
   He digs 103 times. A weeded tile is dead for the season -- `WATER` needs `kind == PLANT` and
   `PLANT` needs `EMPTY` -- while the chain keeps buying seed for it.
   Every chain measurement in this project ran `weed_chance=0.0`, which is exactly why this never
   surfaced. This is a new defect, not a tuning gap.

4. **Sell cadence is worth much less than task #24 claims.**
   His mean gap between sell days is 1.0 (wheat, fertilizer) to 1.4 (wool) days.
   He sells nearly daily, like us. #24 should be downgraded.

5. **56% of his ops are movement** (N 16.8%, W 15.0%, S 12.7%, E 11.7%), and `PASS` is only 4.9%.
   His units are spread across the board rather than working compact adjacent blocks.
   Our `BLOCK_SIZE = 4` serpentine blocks minimise walking by construction, which looks efficient
   and may be the wrong objective: he spends the turns to reach better tiles.

## Full op census, four replays aggregated

```
NORTH 4,943 16.8%   WEST 4,392 15.0%   SOUTH 3,716 12.7%   EAST 3,428 11.7%
WATER 3,404 11.6%   PASS 1,427 4.9%    PICKUP 1,356 4.6%   HARVEST 1,352 4.6%
FEED 1,276 4.3%     COLLECT_FERTILIZER 1,272 4.3%          CARE 1,232 4.2%
PLANT 524 1.8%      FERTILIZE 427 1.5%  DROP 320 1.1%      PLACE 108 0.4%
DIG 103 0.4%        BUILD_PASTURE 56 0.2%
```

`PLANT` 524 across four replays is 131 per replay, matching 66 + 44 + 21 = 131 seeds exactly.
