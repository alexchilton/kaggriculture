# The shed jams at 100, and that is why we harvest more and sell less

Measured 2026-08-25 over **35 of our own ladder games** downloaded from the two submissions built
that day, plus the ours/tape grid on both arms' own seeds.

## The chain

`reference/kaggriculture.py` decides all of this, and every step is in the source:

    HARVEST  puts the yield in the UNIT'S OWN inventory          :466  _inv_add(inv, crop, units)
    SELL     is refused unless the goods are already in the shed  _commit_unit
    DROP     empties a unit's whole inventory into the shed       :343
    PLACE    puts a named item and quantity into the shed         :377
    DAWN     _drop_inventories_to_shed(private, shed_cap)         :878

`shedCapacity` is **100** (`:553`), and it is a hard ceiling on everything held.
`_drop_inventories_to_shed` says what happens when it is reached:

> Drop every per-farmer inventory into the shed up to `capacity`; **overflow is discarded**.

So once the shed is full, two things happen at once: incoming produce is destroyed at dawn, and
every further harvest has nowhere to go.

## The measurement

    35 games, shed capacity 100, all 720 turns each
      turns OUR shed at 100/100    :   306   (9 a game)
      turns THEIR shed at 100/100  :    91   (3 a game)
      turns ours   >= 90           : 2,505
      turns theirs >= 90           :   488

**We sit within ten units of the cap five times as often as our opponents.**
Worst games, `(episode, our turns at cap, theirs, our peak, their peak)`:

    99114898  30 / 0   100 / 99      <- the Koba loss, -$26,277
    99153763  29 / 0   100 / 95
    99067358  25 / 17  100 / 100
    99144625  11 / 0   100 / 75

## Why it matters: we grow more and bank less

From the ours/tape grid, strawberry arm, own seed 468411728, totals over the twelve solver days
d12-d23:

    plant          63 / 64     -1
    harvest       211 / 201   +10
    feed          168 / 115   +53
    care          168 / 115   +53
    water         521 / 494   +27
    pickup        104 / 55    +49
    drop           28 / 0     +28
    place           1 / 17    -16
    sell (units)  737 / 914  -177
    money at d23  331,133 / 342,206   -11,073

**Ten more harvests, 177 fewer units sold.**
The produce is grown and it is picked up. It cannot be banked.

The melon arm on its own seed does not have this problem -- `sell 728/727`, dead level -- which is
why melon games are won by a mean of $20,434 and strawberry games by $3,213.

## What this is NOT

- **Not the routes.** Mid-route PASS gaps (a stop dropped by `_apply_precomputed`, which keys on
  `(tile, ops)` and sheds silently) total **2 on melon and 0 on strawberry** across the whole solver
  zone. The routes the solver emits are gap-free.
- **Not idleness in the ordinary sense.** The idle turns are whole days where a hand was parked --
  227 unit-turns on melon, 319 on strawberry -- but the tape hires the SAME crew every day
  (`hire` row is identical, `10/10 11/11 8/8 12/12 ...`) and spends its surplus WALKING:
  season `work 3062/2773`, `move 3117/3477`. Its hands are not more productive, they are in transit.
- **Not the walk to the shed.** We DROP 1,425 times across 35 games. We reach the shed.

## The likely connection to the wool collapse

`docs/where_99114898_went_2026-08-25.md` records WOOL going $239 -> $11 on an overshoot of 57 units
above `I0`. A jammed shed forces exactly that behaviour: you dump whatever you can whenever you can,
rather than metering sales to the price. Kawa keeps headroom -- 488 turns at 90+ against our 2,505 --
so he can hold and sell into a better book.

## Open, and deliberately not guessed

**How many units are actually destroyed.** That needs the unit-index to `private["inventories"]`
mapping, and two attempts at it produced contradictory answers -- one pass reported 43/89/94 units in
hand at DROP turns by summing all inventories, a second reported 0 for the acting unit at the same
turns. The index mapping is wrong and the number is unknown. Do not quote a figure for this until it
is measured properly; the shed-occupancy numbers above need no such mapping and stand on their own.

## What to try

Sell cadence, not routing. The hypothesis this measurement supports is that the shipped agent sells
too late and too rarely, so production outruns storage. The test is whether raising sell frequency
in d12-d23 lowers turns-at-cap and raises units sold, on the strawberry arm first, where the gap is.
