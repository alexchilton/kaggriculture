"""Chain-level mutation of a 720-turn tape: the unit-day is the atom, not the slot.

**Why the slot operator stalls.** `script_mutate.py` edits one `[turn, unit]` cell at a time. A tape is
a chain: change what unit 3 does at turn 300 and it is standing somewhere the next twenty turns did
not expect, so the rest of its day is walking to places that no longer matter. Almost every edit
therefore destroys more than it creates. Measured on the winner's tape
(`data/logs/optimise_from_winner.log`): 3 accepted moves in 70 iterations, +1.6%, nothing after
iteration 30. That reads as "the tape is a local maximum" and is at least partly a statement about
the operator.

This is the same argument `kagg/search/routines.py` makes for the genome search -- "a representation
in which a partial chain **cannot be expressed**" -- applied to a tape instead.

**The structural fact that makes it work.** The simulator respawns the whole crew on the shed at dawn
(`executor.py:138`, `ops.SHED_TILES`) and `n_units` resets to 1 each night. So a unit's 24 actions on
one day form a *closed* sequence from a known start position. Moving that block to another day, or
copying it onto another unit, leaves a tape that still makes sense -- the unit begins where the block
assumes it begins. That is what the slot operator can never guarantee, and it is why the unit-day is
the atom here.

Nothing in this module reasons about whether an edit is *good*. An illegal or pointless action
degrades to NOOP inside the simulator and simply scores worse, so the optimiser rejects it unaided
(the same argument `script_mutate.py` makes). What this module guarantees is only *coherence*.
"""

import numpy as np

TURNS_PER_DAY = 24

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")

UNIT_FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty")
MARKET_FIELDS = ("sell", "buy_seed", "buy_product", "buy_animal")
SCALAR_FIELDS = ("hire", "buy_land")

# Relative weights over the edit kinds. Deliberately biased toward moving *time*, because every
# strategic lever the winner's tape turns is a timing decision -- when the crew ramps, when the herd
# is stocked, when a quadrant is unlocked, when produce is dumped.
KINDS = ("shift_unit_day", "copy_unit_day", "swap_unit_days",
         "shift_market_day", "scale_market_day", "shift_hire_day", "shift_land_day")
WEIGHTS = np.array([0.26, 0.20, 0.12, 0.18, 0.10, 0.08, 0.06])


def candidates(base, n_cand):
    """`n_cand` int64 copies of `base`. Mirrors `script_mutate.candidates`, including the widening."""
    return {f: np.repeat(np.asarray(base[f])[None].astype(np.int64), n_cand, axis=0)
            for f in FIELDS}


def n_days(cand):
    return int(cand["unit_op"].shape[1]) // TURNS_PER_DAY


def _day_slice(day):
    return slice(day * TURNS_PER_DAY, (day + 1) * TURNS_PER_DAY)


def _live_unit(rng, crew, day):
    """A unit index that exists on `day`, so an edit is not written into a slot with nobody in it.

    There are up to 24 unit slots against a crew averaging about 10, so drawing uniformly would spend
    most of the budget on rows the simulator ignores -- the same waste `script_mutate` guards against.
    """
    hi = max(int(np.asarray(crew)[min(day * TURNS_PER_DAY, len(crew) - 1)]), 1)
    return int(rng.integers(0, hi))


def shift_unit_day(cand, c, rng, crew):
    """Move one unit's whole day to another day. Coherent: both days start on the shed."""
    days = n_days(cand)
    src, dst = int(rng.integers(0, days)), int(rng.integers(0, days))
    if src == dst:
        return
    u = _live_unit(rng, crew, src)
    for f in UNIT_FIELDS:
        block = cand[f][c, _day_slice(src), u].copy()
        cand[f][c, _day_slice(src), u] = 0
        cand[f][c, _day_slice(dst), u] = block


def copy_unit_day(cand, c, rng, crew):
    """Duplicate a unit-day onto another unit, optionally on another day.

    The single most useful edit available: an idle unit inherits a sequence already known to do
    something. The winner's tape spends 44% of unit-turns on real work against our executor's 7%
    (`data/logs/teacher_forced_diff.log`), so replicating a working day is a large, coherent step.
    """
    days = n_days(cand)
    src, dst = int(rng.integers(0, days)), int(rng.integers(0, days))
    u = _live_unit(rng, crew, src)
    v = _live_unit(rng, crew, dst)
    if (u, src) == (v, dst):
        return
    for f in UNIT_FIELDS:
        cand[f][c, _day_slice(dst), v] = cand[f][c, _day_slice(src), u]


def swap_unit_days(cand, c, rng, crew):
    """Exchange two unit-days. Reorders the season without changing what work exists in it."""
    days = n_days(cand)
    a, b = int(rng.integers(0, days)), int(rng.integers(0, days))
    if a == b:
        return
    u, v = _live_unit(rng, crew, a), _live_unit(rng, crew, b)
    for f in UNIT_FIELDS:
        pa, pb = cand[f][c, _day_slice(a), u].copy(), cand[f][c, _day_slice(b), v].copy()
        cand[f][c, _day_slice(a), u] = pb
        cand[f][c, _day_slice(b), v] = pa


def shift_market_day(cand, c, rng, crew):
    """Move a whole day of market orders. Selling a day earlier or later is a real strategic lever."""
    days = n_days(cand)
    src, dst = int(rng.integers(0, days)), int(rng.integers(0, days))
    if src == dst:
        return
    for f in MARKET_FIELDS:
        block = cand[f][c, _day_slice(src)].copy()
        cand[f][c, _day_slice(src)] = 0
        cand[f][c, _day_slice(dst)] += block


def scale_market_day(cand, c, rng, crew):
    """Scale one day's order quantities. Volume, holding the schedule fixed."""
    day = int(rng.integers(0, n_days(cand)))
    factor = float(rng.choice([0.0, 0.5, 1.5, 2.0]))
    f = MARKET_FIELDS[int(rng.integers(0, len(MARKET_FIELDS)))]
    block = cand[f][c, _day_slice(day)]
    cand[f][c, _day_slice(day)] = np.maximum(np.rint(block * factor), 0).astype(np.int64)


def shift_hire_day(cand, c, rng, crew):
    """Move a day's hiring earlier or later, preserving the count.

    `HIRE_COST` is Fibonacci in `hires_today` and resets each dawn, so *when* a hand is taken changes
    both its price and how many hours it works. The winner ramps 5 -> 13 over ten days rather than
    hiring the crew on day 0; encoding that as a flat target is what bankrupted our own plan.
    """
    days = n_days(cand)
    src, dst = int(rng.integers(0, days)), int(rng.integers(0, days))
    if src == dst:
        return
    block = cand["hire"][c, _day_slice(src)].copy()
    cand["hire"][c, _day_slice(src)] = 0
    cand["hire"][c, _day_slice(dst)] += block


def shift_land_day(cand, c, rng, crew):
    """Move the next land purchase. Two parcels in a season, so this is a coarse, high-leverage knob."""
    turns = np.flatnonzero(cand["buy_land"][c] > 0)
    if not len(turns):
        turn = int(rng.integers(0, cand["buy_land"].shape[1]))
        cand["buy_land"][c, turn] = 1
        return
    src = int(rng.choice(turns))
    dst = int(rng.integers(0, cand["buy_land"].shape[1]))
    cand["buy_land"][c, src] = 0
    cand["buy_land"][c, dst] = 1


_OPS = dict(zip(KINDS, (shift_unit_day, copy_unit_day, swap_unit_days, shift_market_day,
                        scale_market_day, shift_hire_day, shift_land_day)))


def mutate(base, rng, n_cand, n_edits, crew):
    """`n_cand` copies of `base`, each with `n_edits` chain-level edits.

    Signature matches `script_mutate.mutate` so the two can be swapped in an optimiser and compared
    on equal budget -- which is the experiment this module exists to make possible.
    """
    cand = candidates(base, n_cand)
    probs = WEIGHTS / WEIGHTS.sum()
    for c in range(n_cand):
        for _ in range(n_edits):
            kind = KINDS[int(rng.choice(len(KINDS), p=probs))]
            _OPS[kind](cand, c, rng, crew)
    return cand
