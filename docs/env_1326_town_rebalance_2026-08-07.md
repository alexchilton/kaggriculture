# The env changed under us on 2026-08-07, and the ladder has not taken it yet

`kaggle-environments` 1.32.6 ships PR #1394, "Kaggriculture town rebalance", merged 2026-08-07.
We were pinned on 1.32.2.
Both facts matter, and the second one is the reason this file exists.

## What changed

    townCenterSellInterval        12 -> 24      the centre buys once a day, not twice
    TOWN_CENTER_DEMAND_SCHEDULE   [(20,4),(10,2),(0,1)] -> DELETED, flat 1 all season
    MAX_SHOP_INSTANCES = 8        each unlocked shop gets its own town slot,
                                  shops drawn WITH REPLACEMENT so this caps count, not variety
    movement onto LOCKED          blocked -> ALLOWED

Late-season town-centre drawdown therefore falls **8x**: from four units twice daily to one unit
once daily, from day 20 onward.
Every "hold it and dump it late" argument in this repo was priced against the old ramp.

The movement change is separate from the town and is easy to miss.
1.32.2 has `if farm["tiles"][ny][nx] == "LOCKED": return`.
1.32.6 removes it, with the comment *"a hand can spawn on a locked shed-access tile, and blocking
movement would strand it there forever"*.
Tile operations still no-op on LOCKED; only movement is freed.

## The ladder is still on the OLD rules

The replay downloaded 2026-08-07 21:16 (`90751101`, Seb beating Leon Christians 143,772 to 127,114)
records `townCenterSellInterval = 12` in its own `configuration` block.
So as of that evening the competition servers had not picked up 1.32.6.

**Check that field on every future download before trusting a comparison against it.**
It is the only reliable statement of which economy a given tape was played under, and it is one line:

```python
json.loads(pathlib.Path(replay).read_text())["configuration"]["townCenterSellInterval"]
```

We upgraded to 1.32.6, measured, found the tape damaged, and pinned back to 1.32.2 within the hour.
Measuring on 1.32.6 while the ladder runs 1.32.2 optimises for a game nobody is playing.

## What it did to the day-matching, while we were briefly on 1.32.6

Seed 11, weeds off, Seb's tape `90494364`, days 0-11:

    on 1.32.2   d0=7 d1=6 d2=4 d3=7 d4=7 d5=7 d6=11 d7=15 d8=13 d9=14 d10=19 d11=20   130 cells
    on 1.32.6   d0=7 d1=6 d2=4 d3=8 d4=7 d5=8 d6=15 d7=19 d8=18 d9=18 d10=22 d11=27   159 cells

d0-d2 are untouched because nothing has been sold yet.

**The tape itself is damaged by the change**, which matters more than the cells.
It emits `BUY_LAND` on the same turns either way -- `1/1` at d4, d8, d10 -- and under 1.32.6 the
purchases FAIL.
It finishes d11 on 75 tiles against our 100 and 8 pens against our 15, sitting on $6,397 it cannot
spend.
With the town drawing 1 unit a day instead of 8, its sells crash the book further and return less,
so at the turn its script fires `BUY_LAND` the cash is not there -- and a fixed 720-turn script
cannot wait for a better price.

That is a general warning about tape-following, not just about this tape.

## How the code handles both

Nothing reads a remembered literal any more.

- `kagg/sim/town.py` reads `CENTER_INTERVAL` from the installed env's own JSON spec, and
  `CENTER_SCHEDULE` via `getattr(kg, "TOWN_CENTER_DEMAND_SCHEDULE", [(0, 1)])`.
- `kagg/economics/market.py` and `kagg/sim/jax_sim.py` both defer to those.
- `tests/test_sim_town.py::test_center_multiplier_matches_the_schedule` asserted `1,1,2,2,4,4` and
  now asserts the SHAPE the env declares. A rule change should not read as our bug.

## Still outstanding on 1.32.6

19 tests fail there and are NOT fixed:

| suite | count | why |
|---|---|---|
| `test_shop_unlocks` | 8 | slot/instance model changed |
| `test_market_model` | 4 | drain schedule and interval |
| `test_storage` | 3 | bank thresholds baked from old prices |
| `test_sim_ops` | 3 | our sim blocks a move the reference now permits |
| `test_water_cadence` | 1 | same, a bank threshold |

The three `test_sim_ops` failures are the movement change and are a **real divergence in our
simulator**, not a stale expectation. `kagg/sim/ops.py` still blocks LOCKED.

And when the ladder does move to 1.32.6 there is a routing gain sitting there: `_step_towards` and
`_mobile` in `schedule_agent.py` both refuse locked tiles, so every tour currently detours around a
quadrant it would be allowed to cross.
