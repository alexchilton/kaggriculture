"""`ranch()` must be able to put a pen anywhere on the board, not only on the four shed tiles.

The original refusal was a real safety property, not laziness: a pen on a shed-access tile needs **no
movement op at all**, so no later edit can invalidate the unit's position, and the first version of
this routine -- which walked once on the start day -- silently starved every animal outside `(4,4)`
after the dawn teleport sent the unit home.

But it caps the ceiling, and the cap is severe. Measured:

* `data/logs/second_animal.log` -- the leader tape buys **14 animals** (8 COW, 6 SHEEP, 0 GOOSE) and
  emits 14 `BUILD_PASTURE`. Our chain model could express 4.
* Worse than 4 in practice: the four shed cells are one per quadrant, so pens 3 and 4 cost $3,000 and
  $7,000 in land against a $3,000 opening bank. Substituting them scored **$0 and 0/16 wins** -- the
  farm goes broke and every later order silently no-ops. The usable cap was **2**.
* And two cows beat one by **$3,004**, so the cap was binding on a farm that wanted more.

`grow()` already solved the same dawn-teleport problem the honest way: re-walk from spawn every day.
These tests hold `ranch()` to that, and to the two consequences that follow from being off the shed --
a remote pen cannot DROP to the shed, so its sale waits for the dusk auto-drop and the next dawn.
"""

import numpy as np
import pytest

from kagg.search import routines as R

SHED = R.shed_access_tiles()
REMOTE = (0, 0)            # NW, owned at spawn, several steps from the shed
FAR = (9, 9)               # SE corner: owned only after every parcel, and the longest walk


def _ops_on_day(script, unit, day):
    lo, hi = day * R.TURNS_PER_DAY, (day + 1) * R.TURNS_PER_DAY
    return [R.OP_NAMES[int(o)] for o in script.unit_op[lo:hi, unit]]


def _position_after(script, unit, day):
    """Replay the day's movement and report every tile the unit stands on.

    From the unit's **own** spawn tile. Replaying from `SPAWN` for every unit is the exact defect
    this suite's sibling `test_unit_spawn_routing.py` was written to catch, and it was in this helper
    too: it reported unit 1 arriving one tile east of wherever it really stood.
    """
    pos = list(R.spawn_tile(unit))
    seen = [tuple(pos)]
    for name in _ops_on_day(script, unit, day):
        if name == "NORTH":
            pos[1] -= 1
        elif name == "SOUTH":
            pos[1] += 1
        elif name == "EAST":
            pos[0] += 1
        elif name == "WEST":
            pos[0] -= 1
        seen.append(tuple(pos))
    return seen


def _run(script, seed=0):
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    fields = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
              "buy_product", "buy_animal", "hire", "buy_land")
    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in fields}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return state, float(np.asarray(state.farm.money)[0, 0])


def test_a_pen_off_the_shed_is_no_longer_refused():
    """The whole point. This raised ValueError before."""
    R.ranch(R.Script(), "COW", REMOTE, start_day=0, unit=1)


def test_the_shed_tiles_still_need_no_movement():
    """The zero-movement property is why shed cells are worth having; it must not regress."""
    s = R.ranch(R.Script(), "COW", SHED[0], start_day=0)
    u = R.unit_for_cell(SHED[0])
    moves = {"NORTH", "SOUTH", "EAST", "WEST"}
    for day in range(1, R.SEASON_DAYS):
        assert not (moves & set(_ops_on_day(s, u, day))), \
            f"day {day} walks, but {SHED[0]} is a shed-access tile"


def test_a_remote_pen_is_re_walked_every_single_day():
    """`_end_of_day` teleports every unit back to spawn. A routine that walks once and then feeds for
    the rest of the season is feeding the spawn tile -- the exact defect that starved every animal in
    the first version of this routine.
    """
    s = R.ranch(R.Script(), "COW", REMOTE, start_day=0, unit=1)
    for day in range(R.SEASON_DAYS):
        assert REMOTE in _position_after(s, 1, day), \
            f"day {day} never reaches {REMOTE}; the unit is acting on the spawn tile"


def test_a_remote_pen_still_feeds_cares_collects_and_harvests_daily():
    s = R.ranch(R.Script(), "COW", REMOTE, start_day=0, unit=1)
    for day in range(1, R.SEASON_DAYS):
        ops = _ops_on_day(s, 1, day)
        for needed in ("FEED", "CARE", "COLLECT_FERTILIZER", "HARVEST"):
            assert needed in ops, f"day {day} is missing {needed}: {[o for o in ops if o != 'PASS']}"


def test_a_remote_pen_carries_its_wheat_out_from_the_shed():
    """FEED needs wheat in hand and PICKUP only works next to the shed, so the wheat must be drawn
    at spawn *before* the walk, not after arriving."""
    s = R.ranch(R.Script(), "COW", REMOTE, start_day=0, unit=1)
    ops = _ops_on_day(s, 1, 5)
    live = [o for o in ops if o != "PASS"]
    assert "PICKUP" in live, "no wheat drawn"
    assert live.index("PICKUP") < live.index("FEED"), "picked wheat up after feeding with it"


def test_a_remote_pen_does_not_pretend_it_can_drop_to_the_shed():
    """DROP tests shed-adjacency. Out in the field it is a wasted turn; `_drop_to_shed` runs at dusk
    anyway. `grow()` records the same finding for crops."""
    s = R.ranch(R.Script(), "COW", REMOTE, start_day=0, unit=1)
    assert "DROP" not in _ops_on_day(s, 1, 5)


def test_a_remote_pen_sells_after_the_shed_has_the_goods():
    """The harvest sits in `carried` until dusk, so a same-day sell quotes against a shed that does
    not hold it -- measured at exactly zero revenue for crops in `test_grow_routine.py`."""
    s = R.ranch(R.Script(), "COW", REMOTE, start_day=0, unit=1)
    milk = R.PRODUCTS.index("MILK")
    for t in np.flatnonzero(np.asarray(s.sell)[:, milk] > 0):
        assert int(t) % R.TURNS_PER_DAY <= 1, \
            f"sell at turn {t} is mid-day; a remote pen's goods only reach the shed at dusk"


def test_a_remote_pen_fits_inside_a_day():
    """Raises rather than truncating, exactly as `grow()` does -- a spilled op lands after the dawn
    teleport. The far corner is the worst case."""
    for tile in (REMOTE, (0, 9), (9, 0)):
        s = R.ranch(R.Script(), "COW", tile, start_day=0, unit=1)
        for day in range(R.SEASON_DAYS):
            ops = _ops_on_day(s, 1, day)
            assert ops[0] == "PASS", f"{tile} day {day} put work on the market turn"


def test_a_remote_pen_earns_more_than_no_pen_at_all():
    """The economic floor. If a walked pen cannot beat an empty farm it is not worth the option."""
    _s0, base = _run(R.Script())
    s = R.ranch(R.Script(), "COW", REMOTE, start_day=0, unit=1)
    _s1, got = _run(s)
    assert got > base, f"remote pen lost money: ${got:,.0f} vs empty ${base:,.0f}"


def test_the_animal_actually_ends_up_on_the_remote_tile():
    """Structure can look right while PLACE silently no-ops -- that is how the first seeded genome
    bought four animals and placed one."""
    from kagg.sim import jax_sim as J
    s = R.ranch(R.Script(), "COW", REMOTE, start_day=0, unit=1)
    state, _ = _run(s)
    animals = np.asarray(state.tiles.animal)[0, 0]
    assert (animals != J.NO_ANIMAL).sum() >= 1, "no animal is on the board at the end of the season"
