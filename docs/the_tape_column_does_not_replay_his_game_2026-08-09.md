> **TARGET SUPERSEDED, added 2026-08-11.** The harness-fidelity finding below (our replay of his
> recorded actions diverges from his recorded bank) is a real, version-skew bug and still stands. But
> the tape itself is now known to be a poor target regardless: it is Seb's, and Seb's median bank
> halved when the town rebalance landed and he has since withdrawn from the ladder
> (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats).

# The tape column does not reproduce his game — measured 2026-08-09

**Alex's position, which is correct: the tape is the JSON replay of the game he actually played.
The schedule was derived from that JSON. So if our harness disagrees with the tape, our harness is
wrong.**

This had never been tested end to end. It is now.

## The measurement

Push **his own recorded actions for BOTH seats** through a fresh env on seed 11 and compare, every
turn, against the money recorded in his own replay:

```
weeds=0.0    first money divergence  turn 32 (d1 h8)  sim=188  rec=187   FINAL sim=10,264   recorded=110,820
weeds=0.005  first money divergence  turn 32 (d1 h8)  sim=188  rec=187   FINAL sim=11,711   recorded=110,820
```

His actions, his opponent's actions, his board — and the simulation ends on **9%** of his real
bank. It starts diverging on **day 1, hour 8, by one dollar**.

## The cause: we replay a pre-1.32.6 game under 1.32.6

Turn 31, with both sides otherwise idle and only his `BUY_PRODUCT WHEAT 1` on the book:

```
turn 30   246 -> 217   recorded charge 29   installed env charge 29
turn 31   217 -> 188   recorded charge 30   installed env charge 29   <-- the dollar
```

Installed `kaggle-environments` is **1.32.6**. His replay predates the 2026-08-08 switch. The two
price wheat differently, so his recorded game is not reproducible here at all — one dollar at d1 h8
compounds to $10,264 against $110,820.

`weedSpawnChance` is not the cause: 0.0 and 0.005 both diverge at the same turn and both end ~10x
short.

**Alex has stated this roughly ten times across sessions and been argued with every time.** It is
closed. `docs/REGISTER.md`'s OPEN-CLI already carried it as "1.32.6 test failures ... Both simulators
fail parity on 1.32.6"; that entry and this document are the same fact.

## What IS verified

- The starting board is exact. Seed 11 reproduces his step-0 tiles cell for cell, same money, same
  town. So the seed choice is right and the divergence is not a different board.
- The schedule is derived correctly. Against his recorded actions across 17 days, `builds` and
  `places` match every single day, zero mismatches, 19 builds against 19. There is no error in the
  derivation — that hypothesis was tested and closed.

## What this invalidates

`breakdown.py`'s tape column runs his actions forward in our env (`breakdown.py:274`, both seats
from the replay). Since that run diverges at d1 h8, the column is **his action sequence executed
into a state that stopped being his after day 1**, not his game.

Consequences:

- **State rows** (`money`, `tiles`, `pens`, crops, herd) are not targets. His real melon reaches 18
  and the column shows 7. His real pastures reach 19 and the column shows 8, flat, all season.
- **Fill rows** (`sell`, `buy_product`, `buy_seed`, `buy_animal`) run through a book that is no
  longer his, so they degrade too.
- **Emitted-op rows** are still literally his recorded actions and are the least damaged — but the
  board they land on is wrong from d1 h8, so a refused or no-op action is counted where his
  succeeded.

Two rows chased this session illustrate it. `melon 7/6` at d5 and `pens 9/8` at d5 both read as us
over-buying. Neither is: the schedule's cumulative melon seeds are 7 by d5 and cumulative builds are
9 by d5, and we hit both exactly. The column is what is short.

## What has been recorded about this before, and why it was not enough

`.claude/skills/matching-the-tape` and `docs/REGISTER.md` both describe this as a **money**
contamination starting at **d4**, caused by the replayed Seb selling into a book we have lifted.
Both are wrong on all three counts:

- it starts at **d1 h8**, not d4;
- it affects state and fills, not just money;
- the tape run never faces our agent at all — `opp` is the replay's own seat 1.

The skill also notes "$2 a day compounds, and the $2 on d1 was hiding a defect worth $1,590 on d6".
That d1 dollar was seen and filed as small. It is the same dollar as turn 32 here.

## The schedule is still the target — Alex, 2026-08-09

**The schedule remains valid. Market prices vary between env versions; that is expected and is not a
defect to chase.** There are several replays, and the schedule is the portable thing derived from
them: what to build, place, plant, buy and sell, on which day. Money and realised fill prices are
not portable and never will be.

So the scoreboard for d0-d6 is **our actions against the schedule** —
`test_our_sells_match_the_plan_every_day`, `test_our_buys_match_the_plan_every_day` and the
per-day op rows — not our money against the tape column. Do not open a money gap as a defect.

## What to do before any more tape matching

Do not tune against the tape column until the replay reproduces his bank. The first job is turn 32:
one dollar, day 1, hour 8, with both sides playing his recorded actions. Find that, and the column
either becomes a real target or is replaced by his recorded observations.
