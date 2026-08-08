# Do pastures on the shed-access tiles block delivery? A clean negative.

## The question

The depot ring is exactly `(4,4)`, `(5,4)`, `(4,5)`, `(5,5)` -- `kg._shed_access_tiles(10)`.
Rendering the board at the end of day 11 showed all four carrying `PASTURE`, in two different
pen-siting configurations, so it wasn't caused by the siting flag. If a structure sitting on a
shed-access tile blocks `DROP` or `PICKUP` there, that would sit upstream of a great deal of recent
work: a delivery investigation where seven separate fixes all regressed, and the finding that the
day-10 melon harvest never reaches the shed. Those regressions would then be explained by a masked
defect, not by the fixes being wrong.

## The answer: no, it does not block. Confirmed by test, not just by reading.

Read off `reference/kaggriculture.py` (`_apply_unit_action`), `DROP` and `PICKUP` gate on
`_is_shed_adjacent`, which is a pure `(x, y)` set-membership check against the four coordinates
(`kaggriculture.py:117-124`) -- it does not look at what, if anything, occupies the tile. The shared
prefix that runs before every op only rejects `tile == "LOCKED"` (`kaggriculture.py:321-323`); a
`PASTURE` or `COOP` dict is not `"LOCKED"`, so it doesn't trip that gate either. Movement is gated
the same way (`kaggriculture.py:308-316`, blocks only `"LOCKED"`), and there is no unit-collision or
structure-occupancy check anywhere in `_apply_unit_action` -- so a unit can walk onto and stand on an
occupied shed-access tile in the first place, which `DROP`/`PICKUP` presuppose.

`tests/test_pens_do_not_block_the_depot_ring.py` demonstrates this directly against
`kg._apply_unit_action`, rather than resting on the reasoning above:

- a `PASTURE` on a shed-access tile does not block `DROP`
- a `PASTURE` on a shed-access tile does not block `PICKUP`
- a `COOP` on a shed-access tile does not block `DROP` (the other pen-siting structure the day-11
  render showed)
- a unit can walk onto and stand on an occupied shed-access tile at all
- an empty shed-access tile behaves identically (control)
- a genuinely blocking tile state, `"LOCKED"`, **does** block `DROP` -- confirming the gate is a
  real check and not a no-op that happens to always pass

All 7 pass:

```
tests/test_pens_do_not_block_the_depot_ring.py .......                 [100%]
7 passed in 2.73s
```

## What this means for the rest of the investigation

This mechanism is ruled out. Pastures/coops sitting on the depot ring are not why delivery has
failed, and are not why the seven fix attempts regressed, and are not why the day-10 melon harvest
never reaches the shed. Those need a different explanation -- this result does not supply one, it
removes one candidate. The user's framing asked explicitly not to soften an inconvenient answer; the
honest report here is the reverse of inconvenient -- the hypothesis that would have implicated a
large amount of prior work turned out not to hold, and that is worth stating as plainly as the
alternative would have been.

## What was NOT checked

This only covers `DROP`/`PICKUP`/movement, the three things the question named. It does not check
whether siting a pasture on the depot ring has *some other* cost (e.g. crowding four units trying to
use the same four tiles for both delivery and animal care in the same turns, or the pasture reducing
the number of siteable pens elsewhere) -- that's a routing/throughput question, not a legality
question, and out of scope for "does it block."

## Files

- `tests/test_pens_do_not_block_the_depot_ring.py` -- the new test, 7 cases, all passing.
