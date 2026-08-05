"""One unit must be able to hold a pen group *and* a crop block, and a full day must be refused.

The wall this file exists to break. Our chain model is one chain = one unit, and a unit either grows or
ranches, never both. Covering the leader's farm -- 14 pens plus ~100 tile-plantings -- therefore needs 14
chains, which forces unit 17, and the Fibonacci hire ladder resets every dawn:

     8 chains -> max unit  9 ->  9 hands = $   88/day = $  2,640/season
    12 chains -> max unit 14 -> 14 hands = $  986/day = $ 29,580/season
    14 chains -> max unit 17 -> 17 hands = $4,180/day = $125,400/season

$125,400 is more than the leader banks in total. He does the same work with **twelve** hands, because
one of his hands tends a pen and crop tiles on the same day. That is the entire difference, and it is
why the scheduler's full-mix plan banks $2,147 with 8 of 14 chains refused.

The turn budget says it is comfortably legal. A day is 24 turns, turn 0 is the market order, so 23 are
work:

    walk to the quadrant            ~4-6
    2 pens, fed every other day      ~7   (PICKUP/FEED/CARE/COLLECT/HARVEST, halved feed)
    remainder for crop tiles         ~10  at one WATER per tile with water_every=2

which is ~10 tiles a day of a 20-tile block -- against the leader's ~11 tiles per hand. So the
arithmetic was never the obstacle; the writer was.

**The defect is a silent overwrite, this project's recurring failure mode.** `Script.op` assigns
`unit_op[t, u]` directly, and both routines lay their day out from `d + 1` on the assumption that they
own the whole day. Calling both for one unit therefore does not raise, does not warn, and does not
compose -- the second one writes over the first. Measured on a 2-pen group plus a 4-tile block:

    ranch alone       327 ops
    grow alone        434 ops
    sum if composed   761
    actually written  441      -- 320 ops, 42% of the work, silently gone

A farm that quietly stops feeding its cows on the day a crop block joins the unit is exactly the
$300-$500 deterministic loss `ranch()`'s docstring promises the search can never propose.

So the fix is a per-unit, per-day **turn cursor** on the `Script`: a routine claims the turns it needs
and is told where they start, rather than assuming turn `d + 1`. Overflow then becomes a refusal the
caller can count -- honest -- instead of an overwrite nobody can see.
"""

import numpy as np
import pytest

from kagg.search import routines as R

PENS = [(4, 4), (5, 4)]                  # the shed 2x2, zero walk, cheapest pens on the board
# **Nearest-to-shed tiles, and the geometry is load-bearing.** The first fixture here used row 1
# ((3,1)...(0,1)), which costs a 4-move walk out and back every single day: 2 tiles then need 14 turns
# against the 11 a 2-pen group leaves free, and the chain is refused for distance rather than for work.
# `scripts/measure_combined_chain_capacity.py` sweeps this -- combined chains only pay adjacent to the
# shed, which is also where the leader keeps his.
BLOCK = [(4, 3), (3, 4), (4, 2), (3, 3)]


def _ops(script, unit=0):
    return int((script.unit_op[:, unit] != 0).sum())


def _ops_on_day(script, day, unit=0):
    d = day * R.TURNS_PER_DAY
    return int((script.unit_op[d:d + R.TURNS_PER_DAY, unit] != 0).sum())


def _feed_days(script, unit=0):
    return R.feed_days(script, unit)


def test_the_premise_the_hire_ladder_punishes_chain_count():
    """Why this matters in dollars, pinned so nobody has to re-derive it.

    The ladder resets at every dawn, so the cost of the *highest* unit index is paid 30 times.
    """
    ladder = R.HIRE_LADDER if hasattr(R, "HIRE_LADDER") else [1, 1, 2, 3, 5, 8, 13, 21, 34, 55,
                                                             89, 144, 233, 377, 610, 987, 1597]
    per_day = {n: sum(ladder[:n]) for n in (9, 14, 17)}
    assert per_day[9] < 200, f"9 hands should be trivial, got ${per_day[9]}/day"
    assert per_day[17] * R.SEASON_DAYS > 100_000, (
        f"17 hands must be measured as ruinous, got ${per_day[17] * R.SEASON_DAYS:,}")
    # 9 -> 14 hands is 11x; 14 -> 17 is a further 4.2x. Both cliffs matter, and the second one is
    # what a 14-chain plan walks off.
    assert per_day[14] > 10 * per_day[9] and per_day[17] > 4 * per_day[14], (
        f"the ladder's cliffs are what force combined chains: "
        f"9->${per_day[9]} 14->${per_day[14]} 17->${per_day[17]} per day")


def test_ranch_and_grow_on_one_unit_must_not_silently_lose_work():
    """The defect itself. Composing two routines on one unit must keep both, or refuse loudly.

    Deliberately asserts on *op count* rather than on any particular op, because the failure is
    quantitative: the second routine overwrites the first and nothing anywhere reports it.
    """
    s_pen = R.Script()
    R.ranch(s_pen, "COW", PENS, 0, unit=0, buy_land=False)
    s_crop = R.Script()
    R.grow(s_crop, "MELON", BLOCK, 1, unit=0, buy_land=False, water_every=2)
    alone = _ops(s_pen) + _ops(s_crop)

    both = R.Script()
    R.ranch(both, "COW", PENS, 0, unit=0, buy_land=False)
    R.grow(both, "MELON", BLOCK, 1, unit=0, buy_land=False, water_every=2)

    assert _ops(both) >= alone, (
        f"composed {alone} ops of work onto one unit and only {_ops(both)} survived -- "
        f"{alone - _ops(both)} silently overwritten")


def test_the_animals_keep_being_fed_after_a_crop_block_joins_the_unit():
    """The consequence that actually costs money, stated on its own.

    An animal escapes after two consecutive missed feeds (`jax_sim.py:1243`). If the crop block
    overwrites the feed loop, the herd walks off the farm and the pen cost is pure loss -- and no test
    on op counts alone would necessarily catch it.
    """
    pen_only = R.Script()
    R.ranch(pen_only, "COW", PENS, 0, unit=0, buy_land=False)
    expected = _feed_days(pen_only)
    assert expected, "the pen-only chain must feed at all, or this test proves nothing"

    both = R.Script()
    R.ranch(both, "COW", PENS, 0, unit=0, buy_land=False)
    R.grow(both, "MELON", BLOCK, 1, unit=0, buy_land=False, water_every=2)
    got = _feed_days(both)

    missing = sorted(expected - got)
    assert not missing, (
        f"adding a crop block to the same unit deleted feeding on {len(missing)} days "
        f"{missing[:8]}...; two consecutive missed feeds and the herd escapes")


def test_a_combined_day_stays_inside_the_turn_budget():
    """The arithmetic claim: pens plus tiles fit 23 work turns, so this is worth doing at all."""
    both = R.Script()
    R.ranch(both, "COW", PENS, 0, unit=0, buy_land=False)
    R.grow(both, "MELON", BLOCK, 1, unit=0, buy_land=False, water_every=2)
    for day in range(2, R.SEASON_DAYS):
        n = _ops_on_day(both, day)
        assert n <= R.TURNS_PER_DAY - 1, (
            f"day {day} wrote {n} ops into {R.TURNS_PER_DAY - 1} work turns; the cursor is not "
            f"enforcing the budget")


def test_an_overfull_day_is_refused_not_silently_dropped():
    """A unit asked to do more than a day holds must fail loudly.

    This is the property that distinguishes the fix from the bug. The old behaviour and a broken fix
    both 'work'; only this separates them, because silently dropping the overflow is precisely what
    made 42% of the work vanish without a trace.
    """
    wide = [(x, y) for y in range(4) for x in range(4)][:12]     # 12 tiles, watered daily
    s = R.Script()
    R.ranch(s, "COW", PENS, 0, unit=0, buy_land=False)
    with pytest.raises(ValueError, match="turn|day|budget|full"):
        R.grow(s, "MELON", wide, 1, unit=0, buy_land=False, water_every=1)


def test_two_crop_blocks_on_one_unit_compose_too():
    """The same cursor must make any pair compose, not just the pen/crop pair we set out to fix.

    A fix special-cased to ranch-then-grow would leave the next composition broken the same way.
    """
    a, b = [(0, 1), (1, 1)], [(2, 1), (3, 1)]
    one = R.Script()
    R.grow(one, "MELON", a, 1, unit=0, buy_land=False)
    n_a = _ops(one)
    two = R.Script()
    R.grow(two, "MELON", a, 1, unit=0, buy_land=False)
    R.grow(two, "WHEAT", b, 1, unit=0, buy_land=False)
    assert _ops(two) > n_a, (
        f"a second crop block added {_ops(two) - n_a} ops to the unit; it was overwritten")