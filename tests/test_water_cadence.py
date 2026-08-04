"""A unit that waters every tile every day can only hold four tiles. That is a choice, not a rule.

`grow()` visited and watered every tile on every day, which costs about three turns per tile -- one
WATER plus the walk -- so a 24-turn day caps a block at **four** tiles. Six needs 26 turns and raises.
That is why our whole farm is 12-16 crop tiles while the leader works 60-75.

The game does not require it. Two mechanics, read off `kagg/sim/tiles.py`:

* **Death needs two *consecutive* dry days** (`tiles.py:157`, `consecutive_unwatered >= 2`). One dry day
  leaves the streak at 1 and the next watering resets it to 0. So visiting a tile every *other* day is
  survivable indefinitely.
* **Base production never tests watering.** `produces` depends only on the crop's schedule; watering
  gates the *fertilizer doubling* alone (`tiles.py:178`, `gain = 2 if fertilized and was_watered`).

So half the tiles each day is legal, and it doubles the land one unit can hold: eight tiles fit a
24-turn day where daily watering caps at four.

Measured, one unit, NW tiles, whole season:

    STRAWBERRY   4 tiles daily   $6,182
    STRAWBERRY   8 tiles alt     $9,395    +$3,213  (+52%)
    MELON        4 tiles daily  $15,575
    MELON        8 tiles alt    $11,167    -$4,408  (-28%)

**It must therefore be per chain, never a default.** Strawberry is an ongoing crop producing on a
fixed interval, so it does not care which days it is visited. Melon is one-shot with a harvest window
that closes at `max_day` 12, and an every-other-day visit can miss it -- after which `decay_plants`
eats the yield.

Why this matters beyond +52%: strawberry is the **largest market in the game**, $68,640 against
melon's $35,000 (drain 572 at base 120, versus 140 at 250), and filling it needs ~48 tiles. At four
tiles a unit that is twelve slots and unreachable; at eight it is six.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")
NW = R.serpentine([(x, y) for y in range(5) for x in range(5)
                   if (x, y) not in R.shed_access_tiles()])


def _day_ops(script, unit, day):
    lo, hi = day * R.TURNS_PER_DAY, (day + 1) * R.TURNS_PER_DAY
    return [R.OP_NAMES[int(o)] for o in np.asarray(script.unit_op)[lo:hi, unit]]


def _tiles_touched(script, unit, day):
    """Replay the day and report which tiles the unit actually works."""
    pos = list(R.spawn_tile(unit))
    moves = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
    out = []
    for name in _day_ops(script, unit, day):
        if name in moves:
            dx, dy = moves[name]
            pos = [pos[0] + dx, pos[1] + dy]
        elif name in ("PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG"):
            out.append(tuple(pos))
    return out


def _bank(script, seed=0):
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in FIELDS}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return float(np.asarray(state.farm.money)[0, 0])


def test_the_premise_one_dry_day_does_not_kill_a_plant():
    """Read straight from the simulator, because the whole approach rests on it."""
    import inspect
    from kagg.sim import tiles as T

    src = inspect.getsource(T.daily_refresh_plants if hasattr(T, "daily_refresh_plants")
                            else T.refresh_plants)
    assert "consecutive_unwatered >= 2" in src, \
        "death is not on a two-day streak any more; this whole cadence is unsafe"


def test_base_production_does_not_require_watering():
    """Watering gates the fertilizer doubling only. If it gated production, alternate days would
    halve the yield and the trade would be a wash."""
    import inspect
    from kagg.sim import tiles as T

    src = inspect.getsource(T.daily_refresh_plants if hasattr(T, "daily_refresh_plants")
                            else T.refresh_plants)
    i_prod = src.index("produces = ")
    line = src[i_prod:src.index("\n", i_prod)]
    assert "was_watered" not in line, f"production now tests watering: {line}"


def test_a_daily_block_is_still_capped_at_four():
    """The default must not move -- every crop measurement in the project used it."""
    R.grow(R.Script(), "STRAWBERRY", list(NW[:4]), plant_day=0, unit=0)
    with pytest.raises(ValueError):
        R.grow(R.Script(), "STRAWBERRY", list(NW[:6]), plant_day=0, unit=0)


def test_alternate_day_fits_eight_tiles():
    """The point of the exercise: twice the land in the same 24 turns."""
    s = R.grow(R.Script(), "STRAWBERRY", list(NW[:8]), plant_day=0, unit=0, water_every=2)
    for day in range(R.SEASON_DAYS):
        ops = _day_ops(s, 0, day)
        assert ops[0] == "PASS", f"day {day} put work on the market turn"


def test_every_tile_is_visited_at_least_every_second_day():
    """The safety property. A tile skipped twice running becomes a WEED and is dead for the season,
    which is exactly the failure the daily cadence was protecting against."""
    block = list(NW[:8])
    s = R.grow(R.Script(), "STRAWBERRY", block, plant_day=0, unit=0, water_every=2)
    last_seen = {tuple(t): 0 for t in block}
    for day in range(R.SEASON_DAYS):
        touched = set(_tiles_touched(s, 0, day))
        for t in list(last_seen):
            if t in touched:
                last_seen[t] = day
            else:
                assert day - last_seen[t] <= 2, (
                    f"{t} went unvisited from day {last_seen[t]} to day {day}; two consecutive dry "
                    f"days turn it into a WEED")


def test_no_tile_is_walked_to_twice_in_one_day():
    """A revisit is a wasted walk, and the extra tiles are paid for out of walk turns.

    Several work ops on one tile in a row (PLANT then WATER) is one visit, not two -- so this collapses
    runs before checking, rather than counting ops.
    """
    s = R.grow(R.Script(), "STRAWBERRY", list(NW[:8]), plant_day=0, unit=0, water_every=2)
    for day in range(R.SEASON_DAYS):
        visits = [t for i, t in enumerate(_tiles_touched(s, 0, day))
                  if i == 0 or t != _tiles_touched(s, 0, day)[i - 1]]
        assert len(visits) == len(set(visits)), f"day {day} walks back to a tile: {visits}"


def test_strawberry_earns_more_on_the_wider_block():
    """The money form, and the reason to bother: +52% measured."""
    narrow = R.grow(R.Script(), "STRAWBERRY", list(NW[:4]), plant_day=0, unit=0)
    wide = R.grow(R.Script(), "STRAWBERRY", list(NW[:8]), plant_day=0, unit=0, water_every=2)
    a, b = _bank(narrow), _bank(wide)
    assert b > a * 1.2, (
        f"eight alternate-day strawberry tiles bank ${b:,.0f} against four daily tiles' ${a:,.0f}; "
        f"the extra land is not paying")


def test_melon_is_left_alone_by_default():
    """Alternate days cost melon 28% -- its harvest window closes at max_day 12 and an every-other-day
    visit can miss it. So the cadence is opt-in per chain, and `water_every=1` must be untouched."""
    s = R.grow(R.Script(), "MELON", list(NW[:4]), plant_day=0, unit=0)
    assert _bank(s) > 15_000, "the default melon chain has regressed"


def test_the_genome_can_reach_the_wider_blocks():
    """Reachability, which is the failure this project keeps repeating: a routine parameter no genome
    can set is not a capability. See `tests/test_catalog_covers_every_gene.py`.

    `water_every` is deliberately **not** a gene. It is a property of the block: an eight-tile block
    only fits a 24-turn day on the alternate cadence, and a four-tile block gains nothing from it. As a
    free gene, half the combinations would decode to a raise. So the block gene carries it, via
    `WATER_EVERY_FOR_BLOCK`, and what the genome chooses is the block.
    """
    assert C.WIDE_BLOCKS, "no eight-tile blocks were cut; the wider cadence is unreachable"
    assert set(C.WIDE_BLOCKS) <= set(C.BLOCKS), "wide blocks are not in the gene's vocabulary"
    assert all(C.WATER_EVERY_FOR_BLOCK[b] == 2 for b in C.WIDE_BLOCKS)
    assert all(C.WATER_EVERY_FOR_BLOCK[b] == 1 for b in C.NARROW_BLOCKS)


def test_every_block_in_the_vocabulary_decodes_without_raising():
    """The hazard of two block sizes: a wide block handed a daily chain does not fit and raises, which
    `decode()` would swallow as a skipped slot. `WATER_EVERY_FOR_BLOCK` must prevent it for every block,
    not just the ones a test happened to pick."""
    for b in C.BLOCKS:
        R.grow(R.Script(), "STRAWBERRY", list(b), plant_day=0, unit=0,
               water_every=C.WATER_EVERY_FOR_BLOCK[b])
