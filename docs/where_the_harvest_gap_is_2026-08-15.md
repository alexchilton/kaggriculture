# Where `harvest -19` against the tape comes from — a hypothesis, not yet measured

Written 2026-08-15, after the packing and melon fixes.
**Nothing here is an A/B result.** The grid it is read off was measured while the solved routes were
72% seated, so the per-day numbers are contaminated. It names a candidate and the experiment.

---

## The shape

Seed 11, kawashigi tape, `--days 30`. From d15 to the end it is the same trade every day:

     day   harvest   gap     water   gap      idle      work
      15     17/18    -1     47/41    +6     68/18   124/118
      19     23/24    -1     48/41    +7     21/22   142/121
      21     34/36    -2     40/34    +6      20/0   151/133
      23     31/30    +1     41/31   +10       9/0   144/128
      24     23/26    -3     53/44    +9       2/0   158/138
      25     28/29    -1     39/33    +6       8/0   144/124
      27     32/35    -3     47/36   +11       1/0   150/135

We do **more** total work than the tape — 150-160 turns against 130-140 — and convert less of it
into produce. Idle is at or near zero on those days, so the crew is saturated and every extra WATER
is a HARVEST not taken.

Season d9-d29: water +65, harvest -19, and the market fills row is also down (1378/1455).

## The candidate

`router.WATER_ROTATION`, emitted at `kagg/search/router.py:692`:

```python
elif (WATER_ROTATION and tile is not None and not cell["watered_today"]
      and (tile[0] + tile[1] + day) % 2 == 0):
    out.append(("WATER", None, _crop_remaining(cell, day) / TOP_UP_DISCOUNT))
```

It waters half the SAFE one-shot tiles — tiles that cannot weed tonight, because they were watered
yesterday — on alternating parity. It ships `True` with **no day gate at all**.

Its own docstring gives its whole evidence base, and it is one day:

> Measured off カワシギ's own d3, seed 11: his board at dawn is 19 tiles ... and he emits **14**
> waters. We emitted 7 ... His extra seven are melon: he is not watering all twelve, he waters
> about half and takes the rest tomorrow.

That is a d3 measurement applied to all thirty days. It is the same shape as two defects already
found today: `DELIVER_CUTOFF_TURNS = 99`, tuned on the victor grid and applied everywhere, and the
solved routes, solved against one plan and shipped against another.

`TOP_UP_SAFE_TILES`, which occupies the same slot, ships `False` and has `TOP_UP_FROM_DAY = 7`.
So the flag that IS day-gated is off and the one that is not is on.

## What makes this only a hypothesis

**Watering a one-shot crop is productive, not overhead.** Wheat and melon are `ongoing: false` with
`max_yield 6`, so each water raises the tile's eventual yield. More water can mean fewer harvest
OPS carrying more units each, and the grid's `harvest` row counts ops, not units. A harvest count
below the tape's is therefore not by itself a loss.

Two things argue it is a loss anyway, and neither is conclusive:

1. The market FILLS row is down as well (1378/1455), and that one counts units.
2. Late in the season a tile has fewer days left to use the yield it is being topped up toward,
   while the harvest it displaces is banked today.

## The experiment

One delta, on a clean board — i.e. **after** the d12-d29 re-solve finishes, because the current
grid's late days are exactly the ones whose routes are stale.

Add a day gate to `WATER_ROTATION` and sweep it: off from d15, d20, d25, and never. Judge on the
per-day grid at the target days, not on season money, and require d0-d8 to be byte-identical —
which a gate at d15 or later gives by construction.

The prediction to write down first, so it can be wrong: gating from d20 raises `harvest` toward the
tape and lowers `water`, and does **not** raise weeds, because the rule only ever waters tiles that
were watered yesterday and so cannot weed tonight.
