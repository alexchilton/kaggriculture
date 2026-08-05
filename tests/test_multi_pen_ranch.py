"""One chain must be able to hold several pens, and feed them every other day.

This is the animal mirror of the two crop fixes in 78b4753, and both halves are the same mechanic:

    crops:    wide blocks (8 tiles/chain)   +  water_every=2   (2-strike dry death)
    animals:  several pens per chain        +  feed_every=2    (2-strike unfed escape)

`jax_sim.py:1243` -- "Unfed twice and the animal escapes" -- is the identical two-strike rule as
`tiles.py:157` for watering, so feeding every other day is legal. Our `ranch()` feeds 30 times per
animal per season. The leader feeds **319 times across 14 animals = 22.8 each**, so he is not feeding
daily either.

The cost of one-pen-per-chain is the whole shape of our farm. 1 chain = 1 pen = 1 unit = 1 slot, so
five pens eat five of eight slots and leave three for crops = 12 crop tiles. That is the direct reason
strawberry never competes: its market is the largest in the game, $68,640 against melon's $35,000, and
filling it needs ~48 tiles.

The arithmetic that makes multi-pen fit. The four shed cells are a 2x2 block, so one unit walks all
four in four moves. Per animal per day the loop is PICKUP, FEED, CARE, COLLECT_FERTILIZER, HARVEST =
five turns:

    4 moves + 4 animals x 5 turns = 24    just over the 23 available work turns
    feeding every other day:  4 + 4 x 3.5 = 18    comfortable

So four pens on one chain frees three slots and cuts the hire bill, because fewer distinct units are
needed at dawn.

Measured context: leader 14 pens / 12 hands / 60-75 worked tiles / $139,121. Us 5 pens / 6 hands /
12-16 tiles / $64,349.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")
SHED = R.shed_access_tiles()
# The four shed cells are one per quadrant, so reaching all four costs $7,000 of land. A group of four
# pens *inside* NW is owned at spawn, which is the group worth testing the mechanics on.
NW_FOUR = [t for t in R.serpentine([(x, y) for y in range(5) for x in range(5)
                                    if (x, y) not in SHED])][:4]


def _day_ops(script, unit, day):
    lo, hi = day * R.TURNS_PER_DAY, (day + 1) * R.TURNS_PER_DAY
    return [R.OP_NAMES[int(o)] for o in np.asarray(script.unit_op)[lo:hi, unit]]


def _fed_tiles(script, unit, day):
    """Replay the day and report which tiles a FEED actually lands on."""
    pos = list(R.spawn_tile(unit))
    moves = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
    out = []
    for name in _day_ops(script, unit, day):
        if name in moves:
            dx, dy = moves[name]
            pos = [pos[0] + dx, pos[1] + dy]
        elif name == "FEED":
            out.append(tuple(pos))
    return out


def _run(script, seed=0):
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in FIELDS}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return state


def _alive(state):
    from kagg.sim import jax_sim as J
    return int((np.asarray(state.tiles.animal)[0, 0] != J.NO_ANIMAL).sum())


def test_the_premise_an_animal_escapes_on_the_second_missed_feed():
    """The whole approach rests on this being a two-strike rule, exactly like watering."""
    import inspect
    from kagg.sim import jax_sim as J

    src = inspect.getsource(J)
    assert "consecutive_unfed" in src
    i = src.index("Unfed twice")
    assert "escapes" in src[i:i + 120], "the escape rule has changed; alternate-day feeding is unsafe"


def test_a_single_tile_call_is_unchanged():
    """Every animal measurement in this project used the one-pen form. It must be byte-identical."""
    old = R.ranch(R.Script(), "COW", SHED[0], start_day=0, land_day=0)
    new = R.ranch(R.Script(), "COW", [SHED[0]], start_day=0, land_day=0)
    for f in FIELDS:
        assert np.array_equal(np.asarray(getattr(old, f)), np.asarray(getattr(new, f))), \
            f"{f} differs between the scalar and one-element-list forms"


# How many pens fit one chain depends on the walk, so the vocabulary is validated rather than assumed
# -- the far NW corner is eight moves from the shed and fits three, nearer ground fits four. These
# tests therefore use the largest group the vocabulary actually offers on owned land.
GROUP = max((g for g in C.RANCH_GROUPS if all(R.land_purchases_for(t) == 0 for t in g)),
            key=len)


def test_one_chain_can_hold_several_pens():
    """The point of the exercise: several animals, one unit, one slot."""
    assert len(GROUP) >= 3, f"the vocabulary's best rent-free group is only {len(GROUP)} pens"
    s = R.ranch(R.Script(), "COW", list(GROUP), start_day=0, land_day=0, unit=0)
    assert int(np.asarray(s.buy_animal).sum()) == len(GROUP), "one animal per pen must be ordered"
    builds = sum(1 for day in range(R.SEASON_DAYS)
                 for o in _day_ops(s, 0, day) if o == "BUILD_PASTURE")
    assert builds == len(GROUP), f"{builds} pastures built for {len(GROUP)} pens"


def test_a_multi_pen_day_fits_inside_the_day():
    """`ranch()` must raise rather than truncate -- a spilled op lands after the dawn teleport."""
    s = R.ranch(R.Script(), "COW", list(GROUP), start_day=0, land_day=0, unit=0)
    for day in range(R.SEASON_DAYS):
        ops = _day_ops(s, 0, day)
        assert ops[0] == "PASS", f"day {day} put work on the market turn"


def test_every_animal_is_fed_at_least_every_second_day():
    """The safety property, and the only failure that really matters: two missed feeds in a row is a
    deterministic $300-$500 escape, which is the loss `routines.py` exists to make inexpressible."""
    s = R.ranch(R.Script(), "COW", list(GROUP), start_day=0, land_day=0, unit=0)
    last = {tuple(t): 0 for t in GROUP}
    for day in range(1, R.SEASON_DAYS):
        fed = set(_fed_tiles(s, 0, day))
        for t in list(last):
            if t in fed:
                last[t] = day
            else:
                assert day - last[t] <= 2, (
                    f"{t} went unfed from day {last[t]} to day {day}; two consecutive missed feeds "
                    f"and the animal escapes")


def test_the_quadrant_rule_does_not_reject_the_shed_cells():
    """The four shed cells are contiguous -- `(4,4)` to `(5,4)` is one EAST step -- so the
    one-quadrant rule must not refuse them for *spanning quadrants*, which it would by construction
    since they are one per quadrant.

    Fitting the day is a separate constraint and all four genuinely do not: three moves plus four pens
    of work is 25 turns of 24, so `RANCH_GROUPS` excludes the full 2x2 and keeps the triples. Two
    different limits, and only the second one should bite.
    """
    R.ranch(R.Script(), "COW", SHED[:3], start_day=8, land_day=4, unit=0)
    with pytest.raises(ValueError, match="turns"):
        R.ranch(R.Script(), "COW", SHED, start_day=8, land_day=4, unit=0)


def test_the_animals_actually_survive_the_season():
    """Structure can look right while the herd quietly starves. NW only, so land never confounds it."""
    s = R.ranch(R.Script(), "COW", list(GROUP), start_day=0, land_day=0, unit=0)
    assert _alive(_run(s)) == len(GROUP), "the herd did not survive on the shared chain"


def test_four_pens_on_one_chain_beat_four_chains_on_four_units():
    """The economic claim. Same four animals either way; the shared chain pays fewer hires and, more
    importantly, leaves three slots free -- which is what the crop side needs."""
    owned = [t for t in SHED if R.land_purchases_for(t) == 0]
    if len(owned) < 2:
        pytest.skip("needs at least two rent-free shed cells")
    shared = R.ranch(R.Script(), "COW", owned, start_day=0, land_day=0, unit=0)
    separate = R.Script()
    for t in owned:
        R.ranch(separate, "COW", t, start_day=0, land_day=0)
    a = float(np.asarray(_run(shared).farm.money)[0, 0])
    b = float(np.asarray(_run(separate).farm.money)[0, 0])
    assert a >= b * 0.95, f"the shared chain banks ${a:,.0f} against ${b:,.0f} for separate chains"


def test_the_genome_can_reach_a_multi_pen_chain():
    """Reachability. A routine parameter no genome can set is not a capability -- the lesson of
    `tests/test_catalog_covers_every_gene.py`, learned three times."""
    assert hasattr(C, "RANCH_GROUPS"), "no multi-pen vocabulary for the block gene to select"
    assert any(len(g) > 1 for g in C.RANCH_GROUPS), "every ranch entry is still a single pen"
    # And every group in the vocabulary must decode without raising: a group that does not fit would
    # be swallowed by `decode()` as a skipped slot and read as a weak strategy.
    for g in C.RANCH_GROUPS:
        R.ranch(R.Script(), "COW", list(g), start_day=8, land_day=4, unit=0)
