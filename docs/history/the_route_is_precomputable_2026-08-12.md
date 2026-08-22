# The board is fixed, so the route can be solved offline

Alex's point, 2026-08-12, and it is correct: **the map is the same in every game.**
This had been argued around for two sessions on the assumption that a day's routing depends on the
seed and the opponent. It does not.

## The proof is two functions

```python
def _initial_tile(x, y, board_size):
    return None if _quadrant_of(x, y, board_size) == "NW" else "LOCKED"
```

A pure function of coordinates. `_default_spawn` is deterministic too.
**There is exactly one RNG in `kaggriculture.py`** — `random.Random((seed * 1_000_003) ^ day)` at
line 858 — and it is used for precisely two things: the shop unlock draw and `_spawn_weeds`.

So the geometry, the depots, the shed-access tiles and every walking distance are identical in every
game ever played. The seed changes what is worth SELLING and where weeds appear; it does not change
where anyone walks. The opponent touches our *money*, not our map.

**Therefore a route solved once is reusable**, and the 1s/turn `actTimeout` stops being a constraint
on route quality — solve it offline with hours, ship the answer. This is also what the top players
are recorded as doing (`project_kaggriculture_open_loop`: fixed 720-turn scripts, deterministic
combinatorial scheduling).

The one real caveat is **weeds**: the ladder runs `weedSpawnChance` at the default 0.005, so a
handful of tiles a season turn to weed at random and add a job the precomputed plan did not expect.
That is a local-repair problem, not a structural one. Our own grids run 0.0.

## `scripts/solve_day_offline.py`

Takes a captured day fixture and runs `cover.py`'s **own** `cover()` — the same `slot`/`cost`/
`materialise` the shipped planner uses — with the LNS deadline raised and multiple restarts. A route
it reports as feasible is feasible under the real cost model, not a second model of the game that
might be optimistic about distances.

```
python -u scripts/solve_day_offline.py tests/fixtures/lns_day_12_seed11_victor.json \
    --seconds 5 --restarts 2
```

## What it found

**d12 is a real defect, now proven.**

```
  shipped planner (greedy, no LNS):   48/49 covered
      LEFT (9,1) [WATER, HARVEST, PLANT]  at_risk=False required=False
  offline:                            49/49 covered, 5s, both restarts independently
  per-unit turns: 14-21 against a budget of 24 -- slack on EVERY hand
```

The day is not full. It is an assignment failure.

**d18 is NOT a defect. The shipped planner already covers 66/66 and leaves nothing.**
The previously reported "66 of a proven 67" does not reproduce from the saved fixture, which
contains 66 jobs in total. That lead is closed; do not re-open it on the old claim.

**The existing ruin-and-recreate code already solves d12 — at 5 seconds.**
It fails at the `RUIN_AND_RECREATE_SECONDS = 0.25` it is allowed in-game. So the mechanism is
right and the budget is what is wrong, which is exactly the case for precomputing rather than for
making the greedy cleverer. At 0.25s in a full season it measured slightly WORSE than off
(work 1591 vs 1613 over 20 days), so it must not be shipped at its current budget.

## The reason to keep expectations low: capacity is not the binding constraint

Measured on the d0-d19 grid, seed 11, tape victor:

```
  days 0-19 totals    ours    tape
  work                1,613   1,556      we work MORE
  move                1,646   1,536      we move MORE
  idle                  539     692      we idle LESS
  money at d19       26,105  27,133      we bank LESS
```

We spend 57 more work turns and 110 more move turns than Victor and finish $1,028 behind.
He idles 153 turns more than us and wins anyway.

**Freeing more turns gives us more of the thing we already have a surplus of.** If 692 idle turns do
not stop him winning, our 539 are not what is stopping us. This caps how far the routing work can
compound, and it points at the *mix* rather than the *count* — consistent with the op ranking already
in CLAUDE.md, where FEED (+0.452), CARE (+0.441) and harvest/plant (+0.439) predict money while
PLANT (-0.358) and WATER (-0.276) predict less of it.

Before generalising the offline solve to all 30 days, measure the ceiling: run the season with a
long per-day deadline and see whether the money moves at all.
