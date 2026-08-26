# `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE` measured as an arm — 2026-08-25

**Verdict: NEGATIVE, and the arm never did the thing it was supposed to do.**
Win rate 15% against the 54% seat-0 baseline, 48 games each.
The herd TOTAL reached twelve in **0 of 48 games**.

## Two things you must read before the table

**1. This was NOT run in the `corner` worktree.**
I was spawned isolated in `.claude/worktrees/agent-a63df8cab88b0a862`, whose `schedule_agent.py`
does not contain `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE` at all — that branch **deleted** the
flag and its four constants on 2026-08-19 and left the finding as a comment at `:2900-2926`.
Writes into `.claude/worktrees/corner` are refused by the isolation guard, so
`scripts/the_herd_against_the_drain.py` **in `corner` is unmodified**; the arm was added to a copy
of the corner tree in the scratchpad and run there. The patch is at the bottom of this file and has
to be applied by hand.

**2. The arm changed the split, not the total.** Details in the mechanism section. Every conclusion
below is a conclusion about COW 8 / SHEEP 6, not about COW 6 / SHEEP 6.

## The run

    python -u scripts/the_herd_against_the_drain.py --range 700 8 --workers 3 --out data/logs/total12.csv

Seeds 700-707. `ARMS = ("ship", "total12")`. Mirror match, seat 1 is always the SHIPPED agent, shops
forced and revealed on the real cadence (first at d3, one every third day). Exit code 0.

    log  /Users/alexchilton/DataspellProjects/kaggriculture/.claude/worktrees/agent-a63df8cab88b0a862/data/logs/total12_2026-08-25.log
    rows /Users/alexchilton/DataspellProjects/kaggriculture/.claude/worktrees/agent-a63df8cab88b0a862/data/logs/total12_2026-08-25.csv

## Result, as the script printed it

```
world           wool  milk           arm     win   herd C/S   mean ours  mean theirs
wool2_milk4        2     4          ship     25%   6.0/11.9      96,910       97,175
wool2_milk4        2     4       total12     38%   8.0/6.0      109,672      110,774

wool6_milk0        6     0          ship     75%   6.0/12.0      81,017       80,220
wool6_milk0        6     0       total12      0%   8.0/6.0       61,960       81,887

wool2_milk0        2     0          ship     38%   6.0/12.0      63,365       64,252
wool2_milk0        2     0       total12      0%   8.0/6.0       64,930       78,783

wool6_milk4        6     4          ship     62%   6.0/12.0      97,009       96,713
wool6_milk4        6     4       total12      0%   8.0/6.0       74,444       91,507

wool0_milk4        0     4          ship     50%  10.0/4.0      110,334      110,430
wool0_milk4        0     4       total12     50%  10.0/4.0      110,334      110,430

wool4_milk2        4     2          ship     75%   6.0/11.9      98,047       97,847
wool4_milk2        4     2       total12      0%   8.0/6.0       78,282       94,056

arm                win   games   mean ours
ship               54%      48      91,114
total12            15%      48      83,270
```

## The herd control, with the TOTAL spelled out

`==12` counts the games in which cow+sheep on the final board was twelve.

```
world                arm    win   n   cow  sheep   TOTAL  min  max  ==12   mean ours  mean theirs
wool2_milk4         ship    25%   8   6.0   11.9    17.9   17   18     0      96,910       97,175
wool2_milk4      total12    38%   8   8.0    6.0    14.0   14   14     0     109,672      110,774

wool6_milk0         ship    75%   8   6.0   12.0    18.0   18   18     0      81,017       80,220
wool6_milk0      total12     0%   8   8.0    6.0    14.0   14   14     0      61,960       81,887

wool2_milk0         ship    38%   8   6.0   12.0    18.0   18   18     0      63,365       64,252
wool2_milk0      total12     0%   8   8.0    6.0    14.0   14   14     0      64,930       78,783

wool6_milk4         ship    62%   8   6.0   12.0    18.0   18   18     0      97,009       96,713
wool6_milk4      total12     0%   8   8.0    6.0    14.0   14   14     0      74,444       91,507

wool0_milk4         ship    50%   8  10.0    4.0    14.0   14   14     0     110,334      110,430
wool0_milk4      total12    50%   8  10.0    4.0    14.0   14   14     0     110,334      110,430

wool4_milk2         ship    75%   8   6.0   11.9    17.9   17   18     0      98,047       97,847
wool4_milk2      total12     0%   8   8.0    6.0    14.0   14   14     0      78,282       94,056

arm           win    n  TOTAL herd  games at 12   mean ours  mean theirs
ship          54%   48        17.3            0      91,114       91,106
total12       15%   48        14.0            0      83,270       94,573
```

### `wool0_milk4` is a NULL ROW — its money column means nothing

`total12` and `ship` both play COW 10 / SHEEP 4 there. The money is identical **to the dollar** on
both sides (110,334 / 110,430) and the win rate is identical at 50%. The arm did not fire: that
world has no YARN_STORE and four milk shops, so the flag's `else` branch and the shipped rule give
the same answer. Read it as a correctness check that the module copy is isolated, nothing more.

The other five worlds all fired: herd 18 -> 14.

## The herd TOTAL never reached 12 — the mechanism

The comment at `:2935` promises COW 6 / SHEEP 6. It cannot deliver it from `unlocked_shops`, because
`_herd_split` is called from day 0 and **the first shop does not land until d3**.

With the flag on and `unlocked_shops` empty, `_early` is False, `"YARN_STORE" not in []` is True and
`_milk` is 0, so the `MILK_POOR` branch fires and asks for **COW 8 / SHEEP 6**. Those eight cows get
bought during d0-d2. From d3 the early-yarn branch does ask for COW 6, but `bought` floors the count
and `max()` cannot take a bought cow back.

Measured directly against the module (`kaggriculture/.claude/worktrees/corner` tree, schedule total
18, which is what these worlds row):

```
flag ON, total 18, NO bought floor, d3 with YARN_STORE visible: {'COW': 6, 'SHEEP': 6}   <- the promise
flag ON, total 18, bought COW 8,    d3 with YARN_STORE visible: {'COW': 8, 'SHEEP': 6}   <- what happens
flag ON, total 18, NO bought floor, d0 with NO shops          : {'COW': 8, 'SHEEP': 6}   <- why
```

Season trace with the buy emulated, world `wool2_milk4`:

```
ship      d0..d15  target COW 10 SHEEP 8  total 18   (every day)
total12   d0..d15  target COW  8 SHEEP 6  total 14   (every day)
```

Two consequences.

- **The 49/51 = 96.1% fit figure does not describe this code path.** It was fitted on kawa's FINAL
  boards. The live path is decided on day 0 against an undrawn deck and then frozen by `bought`.
  This is the census-vs-decision error that `WOOL_SHOP_NO_YARN_COW` already recorded costing -16
  points, in a second place.
- **The other branch of the repo already fixed exactly this.** `agent-a63df8cab88b0a862`'s
  `_herd_split` opens with `if not unlocked_shops: return split` under the heading "An undrawn deck
  is not a known deck", and its comment says the same failure — "ten cows, decided before a single
  shop had landed" — was the single biggest source of disagreement with the leader. The `corner`
  branch does not have that guard.

## What was actually measured, and what it does and does not say

The arm as run is "COW 8 / SHEEP 6, decided on day 0". It loses at **15% against a 54% baseline**,
39 points down, and it is not close: it wins 0 of 8 in four of the six worlds.

What is worth noticing, because it argues against the freed-capacity theory rather than for it:
`mean theirs` **rises** in four of the five worlds where the arm fires (wool6_milk0 80,220 ->
81,887; wool2_milk0 64,252 -> 78,783). Seat 1 is a fixed shipped agent, so the only way its bank
moves is through the shared market. Withdrawing sheep un-floors the WOOL book, and the opponent
collects most of that. Our own bank falls in three of five (wool6_milk0 81,017 -> 61,960 is a
$19,057 drop) and rises in two.

So the freed FEED/CARE turns did **not** visibly become crop money at this herd size. That is the
question the 21-31 standing harvestable units motivated, and on this evidence the answer is no — but
see the limits below before treating it as settled.

## Limits — do not over-read this

- **A mirror match is not a best response.** This measures a symmetric equilibrium against one fixed
  opponent, and the Elo ladder rewards beating a field. The melon sweep reversed 25 -> 12 -> 25 on
  exactly this shape. A negative here is stronger than a positive would be, but it is still one
  opponent.
- **8 seeds. Seed variance on this project is ~15%.** The money deltas are inside or near that; the
  **win-rate** delta (54% -> 15%, 48 games each) is what carries the verdict, not the dollars.
- **The COW 6 / SHEEP 6 hypothesis is UNTESTED.** This run refutes COW 8 / SHEEP 6. Testing the real
  thing needs the day-0 branch suppressed — either the `if not unlocked_shops: return split` guard
  from the other branch, or a `cow6`-style pinned arm with the total held at 12. The existing
  `cow6` arm in this script pins cows at 6 and gives every remaining head to sheep, so it is COW 6 /
  SHEEP 12 = 18 and is NOT the same experiment.
- The run shared the machine with the 432-game `herd_cow_sweep` already in flight. Seeds are fixed,
  so this affects wall time only.

## Recommendation

Leave `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE = False`. Do not flip it.

If the total-12 idea is worth another run, the next arm must pin the total, not the flag — because
the flag, as written, cannot produce a total of 12 on a board where shops arrive at d3.

## The patch (NOT applied to `corner` — the isolation guard refused the write)

Against `.claude/worktrees/corner/scripts/the_herd_against_the_drain.py`:

```diff
@@ -54,8 +54,16 @@
 TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
 #: `cowN` pins the cow count to N and gives every remaining head to sheep. Sweeping N per shop
 #: world answers the question the rules only approximate: what mix actually WINS in this town.
-ARMS = ("ship", "greedy", "proportional",
-        "cow4", "cow6", "cow8", "cow10", "cow12", "cow14")
+#:
+#: `total12` switches on `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE`, parked OFF at
+#: `kagg/search/schedule_agent.py:2955`. On the early-yarn branch it returns COW 6 / SHEEP 6 -- a
+#: herd TOTAL of twelve where the shipped rule spends fourteen. It fits the leader's three-quadrant
+#: seats at 49/51 = 96.1% against the shipped rule's 42/51 = 82.4%, and was parked because the freed
+#: FEED/CARE turns had nowhere to go.
+#:
+#: RESTRICTED 2026-08-25 to the pair under test, so the run is small. The full list is
+#: ("ship", "greedy", "proportional", "cow4", "cow6", "cow8", "cow10", "cow12", "cow14", "total12").
+ARMS = ("ship", "total12")
 
 #: (label, shops). YARN_STORE first wherever it appears, because `_early` slices the first three
 #: draws and the lost game drew it first. MILK is carried by PIZZA_SHOP, ICE_CREAM_SHOP and
@@ -161,6 +169,8 @@
     mine = _fresh_module()
     if arm == "greedy":
         mine.WOOL_SHOP_SETS_THE_HERD = False
+    elif arm == "total12":
+        mine.HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE = True
     elif arm == "proportional":
         _proportional(mine, shops)
     elif arm.startswith("cow"):
```

`kagg/search/schedule_agent.py` was **not** edited, in either tree.
