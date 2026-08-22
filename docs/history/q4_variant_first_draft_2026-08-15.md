# A four-quadrant variant, first draft and first measurement (2026-08-15)

Worktree: `/Users/alexchilton/DataspellProjects/kaggriculture/.claude/worktrees/agent-aba114beb8852f9e4`.
Nothing here is committed and nothing in the main tree was touched.

Files added:

- `kagg/search/q4_agent.py` — the variant.
- `scripts/q4_probe.py` — the measurement, one OS process per cell.
- `tests/test_the_fourth_quadrant_branch_leaves_the_opening_alone.py` — 7 fast tests, 11 slow.

Logs: `data/logs/q4_probe.log`, `data/logs/q4_probe.json`, `data/logs/q4_shopscan.log`,
`data/logs/q4_opening_test.log`.

## What was built

The shipped agent is not edited and its behaviour is unchanged.
`q4_agent.make_agent` wraps `schedule_agent.make_agent` and the whole branch is an edit to ONE ROW
of the schedule, day 12.

That works because `schedule_agent` reads its schedule live rather than latching it at
construction: the land block walks `sched[d]["land"]` every turn to find the next parcel due,
`want_total` re-accumulates `animals_bought` every turn, and `_refresh_pins` re-reads `builds` and
`places` every turn.
`schedule_agent.make_agent` also shallow-copies the outer schedule dict and shares every row object
with its caller, which is what lets the wrapper arm the day-12 row at day 6 and have the agent see
it at day 12.

The trigger is `q4_agent.the_town_promised_wool_early(obs)`.
It reads `observation["town"]["unlocked_shops"]` and tests for `YARN_STORE` among the first two
draws.
`YARN_STORE` is pinned against `reference.kaggriculture.SHOPS` by a test, because a predicate keyed
on a misspelled shop never fires and reads exactly like a measured null.
Shops unlock every `townShopUnlockInterval = 3` days (`reference/kaggriculture.py:867,886`), so d6
hour 0 has seen exactly the d3 and d6 draws and "a yarn store by d3-d6" is exactly the first two
entries of the list.

When the trigger fires the branch writes four things onto the day-12 row — `land: 1`,
`animals_bought: {SHEEP: 4}`, `builds: 4`, `places: ["SHEEP"] * 4` — and drops the solved routes
from d12 onward.
`_do_buy_land` takes `LAND_ORDER[len(unlocked) - 1]` (`reference/kaggriculture.py:712-725`), so
owning NW, NE and SW makes the third parcel SE deterministically; it is not a choice the branch
makes.
The four extra animals take the schedule's herd from 14 to 18, and on an early-yarn board
`_herd_split` already caps cows at six, so the split spends all four on sheep and returns
COW 6 / SHEEP 12.

Refusals are reported rather than swallowed.
`_do_buy_land` returns silently on a short bank and so does `_do_hire`, so a run that quietly
stayed on three quadrants would otherwise be measured and written up as "the parcel does not pay".
Every refusal is printed to stderr once and recorded in `agent.q4_report`.

## The opening is action-for-action what ships, and the test that says so is not vacuous

`test_the_opening_is_action_for_action_what_ships` plays the shipped agent against the environment,
hands the q4 agent the identical observation every turn, and compares the two actions.
11 seeds, 11 passed, no divergence before d12.

Arming at d12 is not obviously inert before d12 and this was the one real risk in the design.
`_pens_due_before_more_land(sched, day)` scans days AFTER today for the next parcel and counts the
pens due before it, so adding `builds: 4` at d12 alone would change what d11 believes about its own
pens from 0 to 4, and adding `land: 1` at d12 cuts the scan short and returns it to 0.
Neither edit is safe on its own; the pair is.

Two checks were run against the test itself.
Moving the package from d12 to d10 makes all three probed seeds diverge at exactly d10h0, so the
comparison discriminates.
More importantly, the first version of the test was **vacuous and passed**: it picked its seed by
stepping a PASS-only game, and the shop draw comes off the environment's own `rng`, which the weed
spawn and everything else also consume — so a game where nobody plants anything draws a different
shop stream from the game the agents play.
The pre-scan said seed 0 had an early yarn store; the real game shows `['BAKERY', 'PET_CAFE']`.
Every identity assertion passed while the branch under test never armed.
The seed list is now measured from real games (`data/logs/q4_shopscan.log`) and the test asserts
`armed` at the end.

Early-yarn boards are 11 of seeds 0-69, a base rate of 15.7% against a theoretical
1 - (7/8)**2 = 23.4%.

## The measurement

Three arms, because two would not have been interpretable.
`cover._apply_precomputed` keys a stop on `(tile, ops)` against routes solved for a 75-tile board,
so the q4 arm has to plan d12-29 live, and live routing costs real money on its own.
`shipped_live` is the shipped agent paying that same handicap and nothing else, which is what makes
`q4 - shipped_live` a statement about the parcel rather than about the router.

One OS process per cell, per the 2026-08-15 finding that the first run in a process differs.
There is a second reason here: `q4_agent` mutates `cover.PRECOMPUTED_ROUTES`, which is
process-global, so two arms in one process would contaminate each other's routing.

Opponent `data/sweep/frozen_1186_opponent.py`.
Seeds 3, 10, 17, 18, 22, 45, 47, 53, 60, 65, 66 — every seed under 70 whose town draws a yarn store
in its first two draws.
All eleven arm the branch, so this is the CONDITIONAL effect, not the season average.

```
 seed arm                 bank        opp  R  quad  COW  SHP    CARRO  MELON  STRAW  WHEAT
    3 shipped          133,082    131,472  W     3    6    8     100%   100%   100%    97%
    3 shipped_live     133,221    125,186  W     3    6    8     100%   100%    98%    95%
    3 q4               127,806    123,072  W     4    6   12     100%   100%    99%    95%

   10 shipped           93,307     90,274  W     3    6    8     100%   100%    99%    95%
   10 shipped_live      94,620     90,051  W     3    6    8     100%   100%    97%    96%
   10 q4                86,025     81,800  W     4    6   12     100%   100%    99%    97%

   17 shipped           77,707     75,923  W     3    6    8      91%   100%    97%    97%
   17 shipped_live      78,855     79,568  L     3    6    8      88%   100%    98%    92%
   17 q4                70,734     66,509  W     4    6   12      91%   100%    99%    94%

   18 shipped           89,266     89,051  W     3    6    8     100%   100%    99%    95%
   18 shipped_live      82,258     81,723  W     3    6    8      96%   100%    99%    93%
   18 q4                81,682     81,063  W     4    6   12     100%   100%    99%    96%

   22 shipped          117,959    107,563  W     3    6    8      96%   100%   100%    97%
   22 shipped_live     108,441    104,525  W     3    6    8     100%   100%    98%    95%
   22 q4                97,011     87,855  W     4    6   12      91%   100%   100%    95%

   45 shipped          106,157    100,507  W     3    6    8     100%   100%   100%    97%
   45 shipped_live     101,878     98,330  W     3    6    8     100%   100%    98%    94%
   45 q4               100,182     97,762  W     4    6   11      96%   100%   100%    96%

   47 shipped          106,923    104,961  W     3    6    8     100%   100%    97%    94%
   47 shipped_live     107,848    105,359  W     3    6    8      86%   100%    98%    94%
   47 q4               106,351    102,464  W     4    6   12     100%   100%   100%    96%

   53 shipped           70,506     69,593  W     3    6    8      91%   100%    97%    96%
   53 shipped_live      69,385     69,814  L     3    6    8      89%   100%    97%    93%
   53 q4                75,169     69,702  W     4    6   12     100%   100%    98%    97%

   60 shipped          103,693    101,640  W     3    6    8     100%   100%    97%    94%
   60 shipped_live     104,443    101,406  W     3    6    8      86%   100%    98%    94%
   60 q4               108,889    104,082  W     4    6   12     100%   100%   100%    94%

   65 shipped          112,169    112,382  L     3    6    8     100%   100%    97%    94%
   65 shipped_live     112,971    110,258  W     3    6    8      86%   100%    98%    94%
   65 q4               109,401    104,574  W     4    6   12      91%   100%   100%    94%

   66 shipped          116,568    114,236  W     3    6    8      96%   100%    95%    96%
   66 shipped_live     112,813    116,243  L     3    6    8     100%   100%    98%    92%
   66 q4               135,609    134,737  W     4    6   12      87%   100%    98%    97%

arm               mean bank      median    wins  mean quads  mean herd  collect
shipped             102,485     106,157   10/11        3.00      14.00      97%
shipped_live        100,612     104,443    8/11        3.00      14.00      95%
q4                   99,896     100,182   11/11        4.00      17.91      97%

comparison                              mean d    median d  seeds better  W/L swing
shipped_live - shipped                  -1,873        +139       6/11         -2   the LIVE-ROUTE handicap alone
q4 - shipped_live                         -716      -1,696       3/11         +3   the PARCEL + herd, handicap paid by both
q4 - shipped                            -2,589      -5,276       3/11         +1   what actually ships vs the variant, all-in

q4 armed on 11/11 seeds; SE actually unlocked on 11/11. Buy days: [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
refusals: ['herd short at d20: COW 6 / SHEEP 11 against target COW 6 / SHEEP 12, bank $41,689']
animals standing in SE at d29: [4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4] of [18, 18, 18, 18, 18, 17, 18, 18, 18, 18, 18] total
SE tiles still carrying a crop at d29: [0, 0, 0, 1, 3, 0, 0, 0, 4, 0, 1] (of 25)
```

Collection rates are 94-100% on every arm and every crop, so no money figure in this table is a
routing failure wearing a crop's name.
The mechanism landed on 11 of 11 seeds: SE unlocked on d12 every time, and the herd finished at
COW 6 / SHEEP 12 on 10 of 11.
Seed 45 finished one sheep short with a bank of $41,689, so that is a placement failure and not an
affordability one; the refusal reporter caught it.

## What the numbers say

**The money result is a null with a wide error bar, not a loss.**
`q4 - shipped_live` is -$716 with a per-seed standard deviation of $9,408, so the standard error on
that mean is $2,837 and the spread runs from -$11,430 to +$22,796.
`q4 - shipped` is -$2,589 with a standard error of $3,026.
Neither is distinguishable from zero on 11 seeds.
The median deltas are more negative than the means (-$1,696 and -$5,276) because two seeds carry
large positive tails, which is worth stating rather than smoothing away.

**The routing handicap is the larger of the two effects and it is separable.**
`shipped_live - shipped` is -$1,873 and costs two wins.
That is the cost of dropping solved routes from d12, paid by both live arms, and it has nothing to
do with the parcel.
Most of what `q4 - shipped` measures is therefore the router, not the fourth quadrant.

**The win rate moves the other way from the money, and the reason is measurable.**
q4 wins 11/11 against shipped's 10/11 and shipped_live's 8/11.
Mean margin over the opponent is +$4,113 for q4 against +$2,703 for shipped, because the
opponent's mean bank falls further (-$3,998) than ours (-$2,589).
The four extra sheep flood a shared wool book, and against an opponent selling the same products
that hurts the opponent more than us.
**This is a near-mirror result and must not be read as a ladder result.**
`frozen_1186_opponent.py` is a frozen copy of our own agent family, so the suppression works
because both sides sell the same things; a field with a different crop mix need not respond the
same way.
And 11/11 against 10/11 is one seed.

**The fourth quadrant is bought and then left empty.**
Four of the eighteen animals stand in SE, which is exactly the +4 sheep the package added, and that
is the whole use the branch makes of 25 tiles.
The SE crop count at d29 is 0 on seven of eleven seeds.
That number is a floor — a tile harvested before d29 reads empty — but the direction is not in
doubt, because nothing in this draft relocates any planting onto the new ground.
The direct outlay is $4,000 for the parcel plus 4 x $500 for the sheep; pastures are free.
So $6,000 buys four pen sites, and the measured return on that is -$716 +/- $2,837.

This is the gap the module docstring flags in advance and it is the gap against the field.
`docs/fable_fourth_quadrant_reopened_2026-08-15.md` measures the 2026-08-14 field and finds the
100-tile seats run 277 season hires — exactly what the 75-tile seats run — and work the quadrant by
RELOCATING roughly eight wheat plantings onto it, with the SE crop being wheat in all three games.
This draft implements the herd half of that package and none of the crop half.

## One contested number, left visible

The brief specifies COW 6 / SHEEP 12 = 18 and the code implements it.
`schedule_agent.WOOL_SHOP_SETS_THE_HERD` records a 2026-08-15 measurement over 74 Kawashigi seats
in which his four-quadrant herds run 13-16 and never 18, with a maximum of 16 over all 74.
`docs/fable_fourth_quadrant_reopened_2026-08-15.md` records 18 for the 2026-08-14 field's 100-tile
seats.
Both can be true — they are different players — but 18 is the field's number and not the leader's,
and it is one of the two places to look if this is retried.

## Verdict

Four quadrants is worth pursuing, but not in this form, and the reason is specific rather than a
hedge.
The branch does what it was asked to do — it fires on the right boards, takes SE on d12 on 11 of 11
seeds, and lands COW 6 / SHEEP 12 on 10 of 11 — and buying 25 tiles to stand four sheep on is
measurably worth about nothing: -$716 against the arm that pays the same routing handicap, with a
standard error four times that.
The two things standing between this draft and a real test of the idea are both identified and
neither is the parcel.
First, the solved routes are solved for 75 tiles, and dropping them costs -$1,873 and two wins
before the fourth quadrant does anything at all; re-solving the day routes for a 100-tile board
would remove that confound entirely and is a bounded piece of work.
Second, and more important, the field's package is land plus sheep plus roughly eight relocated
wheat plantings, and this draft ships the first two and none of the third — so the honest summary
is that the parcel has not yet been given a job.
The one genuinely encouraging signal, that q4 wins 11/11 and widens the mean margin over the
opponent by $1,410, is a market-suppression effect measured in a near-mirror against a frozen copy
of ourselves, and should be re-run against the real pool before anyone believes it.
