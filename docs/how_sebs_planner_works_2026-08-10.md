# How Seb's planner works

Measured 2026-08-10 off the four tapes we hold, by reconstructing positions out of the recorded
observations and pairing each with the action emitted from it.
Not inferred from op counts — every claim below is a route.

## 1. The opening is open-loop, and it stops the day the shop speaks

Every farmer action and every hand action is **identical across all four tapes** for the first 96
turns:

```
  per-day agreement across all four tapes (turns of 24 with an identical unit action)
    d0  units 24/24   market 24/24
    d1  units 24/24   market 24/24
    d2  units 24/24   market 24/24
    d3  units 24/24   market 22/24
    d4  units  1/24   market 17/24
    d5  units  1/24   market 10/24
    d6+ units  0-1/24
```

Four different seeds (`1012428555`, `231975074`, `658760367`, `1440180345`), four different
opponents (Valmorlee, Pranshu Ghori, kakuteki, Leon Christians), both seats, and **both economies**
(`townCenterSellInterval` 12 and 24), all with `weedSpawnChance 0.005`.

Confirmed independently by replaying those 96 turns on seeds 11, 7, 123, 999 and 20260810: the
board and the crew size come out identical every time.

It stops at d3/d4 because `townShopUnlockInterval = 3` — d3 is the first day a shop unlocks
(`91422988` d3 opens with `shops ['ICE_CREAM_SHOP']`), and that is the first information the agent
has. Before it, there is nothing to plan against, so the opening is a constant.

The unit streams part at t97 (d4 h01), and the tape that parts first parts for one reason:
`90494364` has an **eighth hand** there. It is the richer `sellInterval 12` economy, so it could
afford one more hire, so the crew is a different size, so every route after it differs. The other
three stay identical for 121 turns — through d5 h00.

**So the only closed loop in the opening is `market -> money -> hire count -> crew size`, and the
crew size sizes the plan.**

## 2. A hand is given a role for the day, and it keeps it

Work ops only (moves and passes dropped), `91422988`:

```
  d11  u1  PURE crop  7/7    WATERx6 PLANTx1
       u6  PURE crop  9/9    WATERx6 PLANTx3
       u9  PURE crop  8/8    WATERx6 HARVESTx1 PLANTx1
       u11 PURE crop  9/9    WATERx6 PLANTx3
       u12 domi herd  8/10   CAREx3 COLLECT_FERTILIZERx3 FEEDx2 BUILD_PASTUREx1 PICKUPx1
       u3       herd  7/11   CAREx3 FEEDx2 COLLECT_FERTILIZERx2 PICKUPx1 BUILD_PASTUREx1 PLANTx1 WATERx1
       u8       haul  5/12   DROPx3 FEEDx3 PICKUPx2 HARVESTx2 CAREx1 COLLECT_FERTILIZERx1
```

Four roles, and the mixing is almost entirely *within* a role:

| role | ops | note |
|---|---|---|
| **waterer** | `WATER`, `PLANT`, `HARVEST` | never touches an animal |
| **feeder** | `PICKUP WHEAT` → `FEED` → `CARE` | the `PICKUP`/`DROP` is the wheat it carries, not a second job |
| **collector** | `CARE` → `COLLECT_FERTILIZER` → `DROP` | one round trip of the pens |
| **builder** | `BUILD_PASTURE`, `PLACE` | day 0 and land days |

`PICKUP`/`DROP`/`PLACE` on a herd hand are not a second assignment — they are the load that role
carries out and the fertilizer it carries back.

## 3. A hand owns a tile end to end, and a contiguous run of them

`PLANT` and `WATER` are emitted on **consecutive turns at the same position**, every time. The tile
is never revisited.

```
  d0  u6  spawn(4,5)  h03(3,4)PLANT[WHEAT] h04(3,4)WATER  h06(2,4)PLANT h07(2,4)WATER
                      h09(1,4)PLANT h10(1,4)WATER  h12(0,4)PLANT h13(0,4)WATER
                      h15(0,3)PLANT h16(0,3)WATER  h18(0,2)PLANT h19(0,2)WATER
```

That is a lawnmower sweep down the column `y=4` and along the row `x=0` — a contiguous block handed
to one hand at dawn, walked in order. Same shape on every crop hand:

```
  d0  u2  (4,1)MELON (4,0)WHEAT (2,0)WHEAT (0,0)WHEAT
  d0  u4  builds (4,3)(3,3)(3,2)(2,2) then plants (2,1)(1,1)(0,1)
  d0  u5  (3,1)MELON (3,0)WHEAT (1,0)WHEAT then builds (1,2)(2,3)
```

The farmer (`u0`) never leaves the shed's 3×3 on d0: `BUILD_PASTURE`, `PICKUP`, `PLACE`, `CARE`.

**This is the difference from ours.** We hold one global priority queue, every hand eligible for
every op, re-ranked at every stop. That is why a waterer gets pulled onto a critical feed and
`consecutive_unwatered` climbs: measured over a full season our agent loses **16 plants to thirst**
(14 strawberry, 2 melon), every one after d9, while losing exactly **one** animal.

## 4. He does not fill the turns, and that is deliberate

```
   day  crew  slots  turns  work  move  pass  idle-all-day  work%
     0     7      8    178    60    60    58             2  33.7%
     1     7      8    178    25    29   124             2  14.0%
     2     7      8    178    38    64    76             1  21.3%
     3     7      8    178    37    47    94             2  20.8%
     4     7      8    178    61    88    29             1  34.3%
     5     7      8    178    51    98    29             0  28.7%
    ...
    11    12     13    286   122   158     6             0  42.7%
    15    12     13    284   123   161     0             0  43.3%

  d0-d16 totals: work 1277 (32.7%)  move 1917 (49.1%)  pass 707 (18.1%)
```

Two hands stand still for the whole of d0 and d3. Day 1 is 124 PASS turns out of 178 — the crew
does 25 work ops all day, because everything planted on d0 was watered on d0 and
`consecutive_unwatered >= 2` means d1 can simply be skipped.

A hand that finishes its block idles. It is not reassigned.

## 5. Where the headroom is

- **707 idle turns over d0-d16**, 124 of them on d1 alone.
- **49.1% of all turns are walking.** Work is 32.7%.
- The early days are the loosest: d1-d3 run at 14-21% work against 40%+ from d11.

None of that is an argument that his plan is bad — it wins. It is an argument that the *ceiling*
above this plan is high, and that a planner built the same way (role per hand, contiguous block,
idle when done) has room to beat it without needing to be cleverer per turn.

## What this implies for our planner

1. Assign a **role** and a **contiguous block** to each hand at dawn. Do not re-rank globally.
2. Emit `PLANT`+`WATER` as one owned tile, not two independent jobs.
3. Let a hand idle when its block is done. Filling turns is what drags waterers onto feeds.
4. d0-d3 needs no board reading at all — it is a constant, and the crew size is the only output
   that matters to d4.
5. From d4 the input is the shop unlock and the bank: which animal is buyable, and whether the
   extra hire is affordable.
