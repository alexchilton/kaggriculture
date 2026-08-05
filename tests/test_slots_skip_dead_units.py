"""A slot must not be assigned a unit that cannot move.

Hands spawn on the four shed-access tiles in NWSE order and the cycle repeats every four, so units 3,
7, 11 ... all wake on `(5,5)` in SE. `(5,5)`'s only two neighbours are `(4,5)` in SW and `(5,4)` in NE,
and `ops.py:86` silently ignores a move onto LOCKED ground. So an SE-spawn unit cannot take a single
step until the farm owns SE -- which costs all three parcels, **$7,000** against a $3,000 opening bank.

The leader tape buys exactly two parcels (day 7 NE, day 10 SW) and never buys SE at all. Under that
plan, and under every plan our own search has ever found, units 3 and 7 are inert for the whole season.

Measured on one identical melon block, changing only the unit:

    unit 0  (4,4)  $15,575        unit 4  (4,4)  $15,365
    unit 1  (5,4)  $15,545        unit 5  (5,4)  $15,215
    unit 2  (4,5)  $15,515        unit 6  (4,5)  $14,975
    unit 3  (5,5)  $ 1,920        unit 7  (5,5)  $ 1,050

`decode()` mapped slot `k` to unit `k`, so an 8-slot genome spent two of its eight slots on units that
do nothing while still paying to hire them. The fix maps slots onto the units that can actually work:
`[0, 1, 2, 4, 5, 6, 8, 9]`.

The cost is hires, and it is small. Hands are dismissed and re-hired every dawn on a Fibonacci ladder
that resets daily, so reaching unit 9 instead of unit 7 is a few dollars a day against a recovered
unit worth roughly $15,000 a season.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

SE = (5, 5)


def test_the_premise_the_se_spawn_is_locked_without_every_parcel():
    """Guard the setup: if the board or land order changes, this suite must fail loudly."""
    assert R.shed_access_tiles()[3] == SE
    assert R.spawn_tile(3) == SE and R.spawn_tile(7) == SE
    assert R.land_purchases_for(SE) == 3
    assert sum(R.LAND_PRICES) == 7000 > C.OPENING_BANK



# ---------------------------------------------------------------------------------------------------
# SUPERSEDED 2026-08-05. The three tests that stood here asserted a property of `working_units()` --
# that it must exclude SE-spawn units -- and that mechanism is gone.
#
# The fact they measured is real and is kept below: unit 3 wakes on `(5,5)` in SE, and driven onto a NW
# block it banks $2,408 against unit 0's $9,331, because a move onto locked ground is silently ignored
# and its walk stops at the border. What was wrong was the conclusion drawn from it -- "those units are
# inert for the season" -- and the fix chosen. Skipping them left them **hired and idle**: hands are
# hired in sequence, so reaching unit 14 pays for hands 1-14, and 14 chains then needed 17 hands at
# $4,180/day, i.e. $125,400 a season against the leader's $7,916 for twelve.
#
# They are not inert. One NORTH step from `(5,5)` lands on `(5,4)`, which is NE -- the first $1,000
# parcel -- and a full-season melon chain there emits 247 ops at 15 of 23 turns.
#
# So `decode()` now **assigns** the lowest-numbered free unit that can actually reach a chain's ground
# on that chain's start day, instead of looking up a static slot -> unit map. The tests below state that
# contract, which is strictly stronger: it fixes the money, keeps the hire count at one hand per chain,
# and refuses the unreachable combinations that the old map emitted as phantoms.
# ---------------------------------------------------------------------------------------------------


def test_decode_never_puts_a_chain_on_a_unit_that_cannot_reach_its_ground():
    """The contract. A chain is emitted on a reachable unit or it is refused and counted."""
    rng = np.random.default_rng(0)
    for _ in range(40):
        genome = rng.integers(0, 6, size=C.n_genes(8), dtype=np.int64)
        script, used, skipped = C.decode(genome, 8)
        land_days = sorted(C.land_schedule(genome, 8))
        for u in range(script.U):
            turns = np.flatnonzero(np.asarray(script.unit_op)[:, u] != 0)
            if not len(turns):
                continue
            start_day = int(turns[0]) // R.TURNS_PER_DAY
            parcels = sum(1 for d in land_days if d <= start_day)
            spawn = tuple(R.spawn_tile(u))
            if R.land_purchases_for(spawn) <= parcels:
                continue
            x, y = spawn
            escapes = any(0 <= nx < R.BOARD_SIZE and 0 <= ny < R.BOARD_SIZE
                          and R.land_purchases_for((nx, ny)) <= parcels
                          for nx, ny in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)))
            assert escapes, (
                f"unit {u} starts work on day {start_day} from {spawn}, which needs "
                f"{R.land_purchases_for(spawn)} parcels against {parcels} owned, and cannot step onto "
                f"owned ground -- every op it emits lands on the wrong tile")


def test_one_chain_costs_the_same_whichever_slot_holds_it():
    """Slot index must not be a price. It was: slot 3 drove unit 3 and banked an eighth of slot 2.

    With assignment by reachability the cheapest free unit is taken, so a lone chain is identical in
    every slot and only the *number* of chains drives the hire ladder.
    """
    block = [b for b in C.BLOCKS if C.land_cost(b[0]) == 0][0]
    bi = C.BLOCKS.index(block)

    def tape(slot):
        g = np.zeros((8, len(C.GENES)), dtype=np.int64)
        g[slot] = [C.KINDS.index("grow"), R.CROPS.index("MELON"), bi,
                   C.START_DAY_CHOICES.index(2), C.LAND_DAY_CHOICES.index(0), 0, 0, 0]
        script, _used, skipped = C.decode(g.reshape(-1), 8)
        return int((np.asarray(script.unit_op) != 0).sum()), int(np.asarray(script.hire).max()), skipped

    first = tape(0)
    for slot in range(1, 8):
        assert tape(slot) == first, (
            f"slot {slot} decodes to {tape(slot)} against slot 0's {first}; the slot index is still "
            f"pricing the chain")


def test_n_chains_never_need_more_than_n_hands():
    """No idle paid hands. This is the whole reason the skip was wrong."""
    rng = np.random.default_rng(1)
    for _ in range(30):
        genome = rng.integers(0, 6, size=C.n_genes(8), dtype=np.int64)
        script, used, _skipped = C.decode(genome, 8)
        busy = sum(1 for u in range(script.U)
                   if (np.asarray(script.unit_op)[:, u] != 0).any())
        hired = int(np.asarray(script.hire).max())
        assert hired <= busy, (
            f"{busy} units do work but {hired} hands are hired; {hired - busy} are paid and idle")
