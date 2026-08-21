# The tape beats our planner, and three bugs were hiding it

Measured 2026-08-21. Commits `1be532f`, `032254c`, `b105d05`.

## 1. The headline

Playing カワシギ's recorded season all the way to d29 finishes **+$240 ahead of him** on seed 11,
with **zero differing cells on every one of the 30 days** up to d20 and 1-2 a day after.

The $240 is not luck and not a different plan.
It is the same ops, same turns, minus the seed he buys and never sows.

## 2. Every dollar we lose is the handover

`scripts/breakdown.py --tape kawashigi --seed 11 --diff --replay-days N`, only the boundary moving.
Money is a LEVEL -- our bank minus his at the end of that day.

```
                  d21  d22  d23   d24    d25   d26    d27   d28    d29
replay d0-d23     +40  +80  +80  -1160  -4117  -543  -3872  -280  -7713
replay d0-d27     +40  +80  +80  +120   +160   +160  +240    +29  -1615
replay d0-d29     +40  +80  +80  +120   +160   +160  +240   +240   +240
```

```
handover   season money vs tape   cells d24-d29
  d24            -$7,713          13 14 15 16 14 8
  d28            -$1,615           2  2  1  2 12 10
  none            +$240            2  2  1  2  1  1
```

The planner turns 2 differing cells a day into 13-16 the moment it takes over, wherever that is.
`REPLAY_OPENING_DAYS` stays at `range(24)` on Alex's instruction -- the planner keeps d24-d29.
The number is recorded because it says the loss is ours, not the tape's.

## 3. Three bugs, each found by measurement and each one line

### Only one tape was ever played

`_MB.arm` and `_Q4.arm` were deleted on 2026-08-20 for a tetsuya reason that no longer applies.
Nothing wrote `melon_armed` or `q4_armed`, so `_replay_opening` read `(False, False)` on every turn
of every seed and all four entries of `REPLAY_OPENING_TAPE` resolved to the melon tape.
Three of the four tapes were unreachable by construction while the docs claimed four branches.

### The yarn store was read a day after the tapes split

`SPLIT_DAY = 9` is correct about the schedule ROWS and was read as if it covered the branch.
The replay sends the tape's own ops, and the q3 and q4 tapes part company at **d5**.
`DECIDE_BY_DAY` 6 -> 5.

### Our seed saving bought a hand he could not afford

The `BUY_SEED` trim leaves us richer than he was on the same turn.
`_do_hire` fails **silently** on a thin bank (`reference/kaggriculture.py:691`), cost
`mult * fib(hires_today)`.
So $60 saved at d6 buys a hand at d8 the tape was refused.

```
d6   money +60  buy_seed -3                                the trim
d8   money -29  hands +1  hire +1  plant +2  water +1      9 cells
     our hands 11, tape 10
d9+  weed, WHEAT and STRAWBERRY diverge for the season
```

Trim dropped on the strawberry arm, **kept on the melon arm** where it is the entire +$240.
Per-arm plan content, the same distinction `WHEAT_TILES_TO_CARROT`'s tomato tile draws.

## 4. Where it stands, 16 seed-drawn towns, d0-d29

`scripts/seed_tape_grid.py --vs-all --live-shops`. Cells against the tape the latches chose.

```
arm                        seeds   before      after
q4, yarn store by d3         6     23-35           0
q4, yarn store at d6         3        69          43   now declines the q4 plan
melon, no yarn store         7     34-41       34-43
strawberry                   5    60-132           0
strawberry                  10    130-132         25
strawberry                   1        40          40
```

Eleven of the thirty-two arm/seed combinations are now exact for a whole season.
The residual on the clean arms is `money x19  sell x6` -- **our sell cadence, not his field ops.**

## 5. What was disproved

- **The herd re-label.** `animals x16` was present in all ten bad strawberry seeds and absent from
  all five good ones, and d8 is the day the tape places a SHEEP. Removing the re-label came back
  **byte-identical**: d8 buys no animal at all, its PLACE is a head bought on d7. Reverted, not left
  runnable.
- **"Verified on seeds 11-14".** `breakdown.recorded_shops` injects the tape's own town into both
  columns, and both latches plus the schedule are functions of that draw. With it on, every seed
  plays the same town and arms the same branch. Four seeds was one measurement repeated four times.
- **"200 different plans by d20".** Three quantities were quoted as one: ~174 distinct whole ROWS at
  d18 (nearly one per game, and mostly executor-generated fields), 25 distinct crop MULTISETS, and 4
  replay branches. The middle is one plan with a wobbling tile count, not 200 strategies.

## 6. Geese are closed; tomato is open

`scripts/who_plays_tomato_or_geese.py`, 4,022 seats across the replay tree.

```
      bank  team                 game                            TOMATO  GOOSE
    162943  Subramanya N         downloads_2026-08-20/94469635      105      0
    153367  tetsuya              downloads_2026-08-19/93870141        0      3
    133308  Ryo Hasegawa         ryo/94413334                         9      0
    132585  Crop Dusta           downloads_2026-08-20/94559597       45      0
    130906  Crop Dusta           downloads_2026-08-20/94557806       61      4

302 of 4022 seats touch either at all
best bank among them            162,943
best bank touching neither      185,263
```

**Geese: closed by absence.** The best goose seat plays 3-4 in a season. Nobody builds around them.

**Tomato: one real candidate.** `94469635` banks **$162,943** with 105 tomato ops -- $13k above the
tape we currently play. `Crop Dusta` has three seasons at 45-61 ops. But the archive's best bank
touches neither token, at $185,263, so tomato is not where the top of the distribution lives.

## 7. Not established

- The melon/strawberry latch has been exercised with exactly two opponents. It was 16/16 correct
  both ways, but that is two values of one variable.
- **How often a melon opponent appears on the ladder.** The strawberry arm only fires on 9+ opponent
  melon tiles at d3. Never counted, and it scales everything in section 4.
- Everything in section 2 is ONE seed on the tape's own recorded game.
- Whether `94469635`'s opening is a fixed script, which is what would make it a fifth tape.
