# The sell side, 2026-08-25

Rewritten at 14:40 after four measurements contradicted the 13:50 version of this file.
Three claims in it were wrong. They are marked RETRACTED below rather than deleted, because each
one was wrong for a reason worth keeping.

## 1. The drain-ranked sell release is a NULL. Recommend reverting it.

Two uncommitted edits in `kagg/search/schedule_agent.py`: a shed at `SHED_TARGET`+ may release its
overflow before `LATE_SELL_FROM_HOUR` (`:4626`), ranked by a new `gain_from_waiting()` computed
live from `town["unlocked_shops"]` instead of by holding size (`:4253`).

Measured on two seeds against a replayed tape it was +$2,511 / +$441. Measured properly it is
nothing:

```
  setting                     games   win rate base   win rate change   mean money delta
  pool heuristics, 20 seeds     200          100.0%            100.0%             -1,566
  kawa's tape, 20 seeds          40           77.5%             77.5%               -284
  the two tape seeds only         2               -                 -             +1,476
```

Paired on seed, opponent and seating: the change is better in 55 of 200 pool pairs and worse in
145. **Win rate is identical in both settings**, and this project selects on win rate.

The reason it cannot do much is that the branch barely executes. `schedule_agent:4626` fires only
when `day >= SHED_HEADROOM_FROM_DAY (12)` and `sum(shed) >= SHED_TARGET (90)`; on every other turn
of the 720 the two arms are the same code. Measured turns per season where that holds:

```
  opponent        pressed (>=90, d>=12)   at the 100 cap
  wheat_only                         10                2
  strawberry                         10                3
  cow_heavy                          12                4
  carrot_hinge                       10                2
  contrarian                         16               10
  tape:kawa                          14                8

  our 35 real ladder games                ~32              ~4     (per game, from sell_shape.log)
```

So the state is real and the simulation reaches it at roughly half the ladder's rate. It is not
that the pool cannot see the change; it is that 10-16 turns of 720 is not enough to move a season.

**RETRACTED: "+$2,511 melon, +$441 straw, pool gate 95%".** The gate figure was a different metric
(the built submission against nine opponents) and the two-seed figures are two seeds against one
opponent. Neither is evidence for shipping.

## 2. His cadence loses, and it loses INSIDE the solver zone

12 seeds, `contrarian`, his fills spliced onto our board for d12-d23:

```
  arm          d24 bank    d29 bank    fill turns   units   clamped
  ours           97,884     164,670            64    1413         0
  his            58,569     128,929            88    1136       271
  his-nf         37,458     101,454            67     872       457

  arm          delta at d24   delta at d29   what the planner did
  his               -39,582        -35,741               +3,840
  his-nf            -60,426        -63,216               -2,791
```

The gap is already fully open when his cadence stops. The d24-d29 planner *narrows* it. So this is
not "the planner cannot recover"; his selling loses the money in the twelve days it runs.

The mechanism is the shed:

```
  ours    d12:50 d14:46  d16:74  d18:61  d20:82  d22:91  d24:90
  his     d12:50 d14:100 d16:100 d18:100 d20:100 d22:100 d24:100
```

Read the two arms carefully: both are OUR farm. Our own rule sells 1,413 units on 64 turns; his
schedule on the same farm sells 1,136 on 88. More often, which is the thing that looked worth
copying, and less total. **His lot sizes are sized for his farm.** We out-produce him, so his
schedule cannot clear our shed, it pins at the 100 cap for eleven days and ~250 units a season are
discarded at dawn by `_drop_inventories_to_shed`.

Neither number is a comparison with him. Head to head, 20 seeds and both seatings, we beat his tape
**31 of 40 games (78%), $102,709 to $93,963**, winning 16 of 20 seeds; the four losses are $749 to
$2,799. The premise that his selling is beating us does not survive playing him.

The transferable part is therefore lot size and frequency at OUR volume, not his quantities. That
arm has not been run.

**RETRACTED: "we sell the fertilizer the farm needs as an input".** Removing FERTILIZER from his
list makes it $20,844 WORSE at d24, not better. The claim is dead.

**RETRACTED: the $19,701 / $22,186 figures.** That harness replaced the whole `market` list, and
`_process_market` carries HIRE, BUY_LAND, BUY_SEED and BUY_PRODUCT on the same channel. It measured
a farm with hiring and purchasing switched off for twelve days. `sell_like_kawa.py` and
`his_cadence_across_seeds.py` now splice only the SELLs, at the position of our first sell so an
order funded by an earlier sale keeps its funding.

## 3. The seed recovery was void

`find_the_seeds.py` fingerprinted seeds with both players on PASS. `_end_of_day` builds one
`random.Random((seed * 1_000_003) ^ day)` per day and calls `_spawn_weeds` for both farms before
drawing the shop; `_spawn_weeds` calls `rng.random()` only where `tiles[y][x] is None`
(`reference/kaggriculture.py:836-840`, `:871`). Play moves the stream, so the draw moves with it.

```
  seed   PASS                                       REAL (live agent vs contrarian)
   700   SMOOTHIE, SMOOTHIE, SMOOTHIE               BRUNCH_SPOT, FARMERS_MARKET, ICE_CREAM
   701   FARMERS_MARKET, PET_CAFE, FARMERS_MARKET   PIZZA_SHOP, YARN_STORE, FARMERS_MARKET
   702   BAKERY, SMOOTHIE, ICE_CREAM                PET_CAFE, YARN_STORE, ICE_CREAM
   258   YARN_STORE, SMOOTHIE, BRUNCH_SPOT          PIZZA_SHOP, ICE_CREAM, ICE_CREAM
   127   SMOOTHIE, FARMERS_MARKET, FARMERS_MARKET   PIZZA_SHOP, YARN_STORE, YARN_STORE
```

0 of 5. **RETRACTED: "24 of 35 games matched to a seed" and "127 of 400 seeds draw a yarn store".**
Seeds 258, 302, 127, 294, 128, 123, 112 and 241 are not the losing games' seeds; they are seeds.

`scripts/find_the_yarn_seeds.py` records this exact hazard in its own docstring and was not read.

The method that would work: a recorded game contains BOTH action streams, so replay both under a
candidate seed and compare the unlock sequence. One full season per (seed, game). Not implemented.

**RETRACTED: "died with BrokenProcessPool under memory pressure".** `/tmp/run_losing.py` had no
`if __name__ == "__main__"` guard, so every spawned worker re-executed the whole script. Not memory.

## 4. What is actually worth chasing

From `data/logs/sell_shape.log`, our 35 real ladder games, d12-d23:

```
  turns with the shed AT the cap (100)   137     a SELL was emitted on  17     units FILLED  0
  turns with the shed at 90-99           969     a SELL was emitted on   8     units FILLED  0
```

On the ladder we spend 1,106 solver-zone turns pinned at or near the cap, emit a sell on 25 of
them, and fill **nothing**. Kawashigi moves 797 units in the same window.

The simulated games do not reproduce this: they fill 720-798 units across d12-d23. So the ladder
failure is not currently reachable in any harness here, which is why an arm aimed at it measures
null. **Find out why a real ladder game fills zero units at the cap before tuning the release
again.** That is the open question this file ends on.

## Open

- Why the ladder games fill zero at the cap when the simulations do not.
- Our volume at his lot size and frequency (~10 units, ~90 turns) -- the transferable half of §2.
- The carrot sweep (running, started by Alex).
- Whether to revert §1. Recommendation: revert. Nothing is committed.

## 5. The rot question, and eight arms that all lose (2026-08-25, late)

Alex's question: if WOOL is $240 and WHEAT is $40, selling a wheat so a wool does not rot must pay.

**The rot is real and WOOL is the biggest part of it.** Measured over 6 seasons, destroyed at dawn
by `_drop_inventories_to_shed`, valued at that dusk's book price:

```
  product      units/season   value $   $/unit
  WOOL                 10.8     2,458       227
  MILK                 10.2     2,375       234
  MELON                 8.0     1,824       228
  STRAWBERRY            7.2     1,586       221
  WHEAT                29.5     1,209        41
  FERTILIZER           11.8       822        70
  TOTAL                78.0    10,322   = 6.11% of bank
```

**And one unit really does move nothing.** `market_price` at `MARKET_I0 + k`:

```
  k                    +0    +1    +2    +5   +10   +20   +50
  WOOL                200   200   200   199   194   177    55
  WHEAT                25    24    24    24    23    22    22
  MILK                160   158   156   150   139   118    55
```

So the premise holds: the trade is free at k=1 and the damage is all at k>=20, where WOOL falls off
a cliff.

**Every arm built to exploit it still loses.** Two seeds, `contrarian`, as-drawn and a forced
wool-8 town:

```
  arm            rot $ as_drawn   bank as_drawn   rot $ wool8   bank wool8
  ours                   9,078              +0         3,315           +0
  dusk_swap              9,062          -1,004         3,204          +32
  opt_dusk               9,528          -2,984         2,384         -407
  cheap_first            7,454          -3,433         3,091       -1,239
  foresight              7,550         -12,726         2,252       -5,755
  opt_season             9,596         -39,672         3,692      -10,666
```

The ordering is the finding: **the harder an arm suppresses rot, the more money it loses.**
`foresight` sells MORE units than the control (1,492 vs 1,459) and banks $12,726 less.

### What the arms are still missing

Alex, closing: *"selling it at any price is a gain -- not necessarily if it crashes a different
market by making lots of sales necessary."*

That is the term none of these have. The greedy prices a unit against its own future price, so when
rot forces a sale it treats the future value as 0 and sells at any price. But the real cost of
selling unit `k` of product `p` is not that unit's price -- it is the reduction it causes in the
revenue of **every later sale of `p` for the rest of the season**. Suppressing 10 units of wool rot
can cost more than 10 units of wool if it drags the wool book down for the 100 units still to come.

Until the opportunity cost is "lost revenue on all remaining units of that product", not "this
unit's later price", these arms are optimising the wrong objective, and the monotone loss above is
what that looks like from the outside.

### Harness notes worth keeping

- Every arm now reports `fired`, the count of turns on which it changed the orders sent, and the
  table refuses to interpret any cell with `fired == 0`. Three arms today produced clean tables
  while changing nothing.
- Rot is measured directly as `(shed + carried at dusk) - (shed at dawn)`, never inferred from
  money. Bank alone cannot separate "prevented the rot and lost on price" from "did nothing".
- Sell at h22, not h23: an hour-23 SELL settles in the same `env.step` as the shed rollover, and
  `dusk_swap` at h23 made rot WORSE (82 units against 74).
- `scripts/force_the_shops.py` pins `town["unlocked_shops"]` so the drain is an axis, verified
  against the measured book. Seed-hunting for a shop draw is no longer necessary for anything.
