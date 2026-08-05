"""The hire ladder is Fibonacci and it RESETS EVERY DAWN, so crew size is the dominant running cost.

This is the bug found on 2026-08-05 after four mixes -- his measured one included -- all banked under
$310 in the real environment. The mix was never the problem. The farm was paying its staff more than
it could ever earn, from day 0.

`reference/kaggriculture.py:666`:

    def _hire_cost(n_already_today, mult=FARM_HAND_COST_MULT):
        return mult * _fib(n_already_today)          # fib: 1, 1, 2, 3, 5, 8, 13, ...

and `farm["hires_today"] = 0` at every dawn (`:850`). So the cost of *running* a crew of N is the
whole partial sum, every single day:

        hands   $/day    $/season (30 days)
            6      20         600
            8      54       1,620
           10     143       4,290
           12     376      11,280      <- his crew, all 12 used
           14     986      29,580
           16   2,583      77,490      <- ours, for the SAME farm
           17   4,180     125,400

$77,490 is more than half the leader's entire season bank, spent on hands. And it is charged from day 0
against a $3,000 opening balance, so the farm is insolvent before a single animal produces anything --
which is exactly what the measurement showed: 14 pens and 58 tiles across 15-16 chains banked $205-$309
no matter which crop mix it used.

**The cause is one thing per unit.** `routines.py` writes a chain onto a unit and every pen group and
every crop block took a fresh one. He runs 14 pens and ~61 crop tiles on **12 hands** by putting more
than one job on a hand. `Script.claim` was built for that on 2026-08-05 and nothing was using it:
`mix_plan` in `scripts/measure_bank_curve_and_fertilizer.py` walked `range(16)` skipping every busy
unit, so a farm his size necessarily reached unit 15 and the $2,583 rung.

These tests are about the *cost of the layout*, not about money banked, so they need no environment and
run in under a second.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

# `_fib(0)=1, _fib(1)=1, _fib(2)=2, ...` -- the n-th hire of the day costs `_fib(n)`.
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]

# Measured off `data/seed_scripts/new_leader/90016067.json`.
HIS_HANDS = 12
HIS_PENS = 14
HIS_CROP_TILES = 61          # PLANT ops: MELON 21 + STRAWBERRY 44 - replants; ~61 distinct tiles
HIS_CREW_SEASON = 11_280


def crew_cost_per_day(hands):
    """What a crew of `hands` costs to bring into existence, once. Charged again every dawn."""
    return sum(FIB[:hands])


def crew_cost_season(hands):
    return crew_cost_per_day(hands) * R.SEASON_DAYS


# ------------------------------------------------------------------ the ladder itself, pinned
def test_the_ladder_is_the_partial_sum_not_the_last_rung():
    """Stated because getting this wrong makes 16 hands look like $987 a day instead of $2,583.

    Hiring the 16th hand costs `_fib(15)` = $987, but you cannot have a 16th without the previous
    fifteen, and the whole crew is dismissed and re-hired every dawn.
    """
    assert crew_cost_per_day(12) == 376
    assert crew_cost_per_day(16) == 2583
    assert crew_cost_season(12) == HIS_CREW_SEASON


def test_four_extra_hands_cost_more_than_the_leader_banks_all_season():
    """Why this is the dominant term and not a rounding error."""
    delta = crew_cost_season(16) - crew_cost_season(12)
    assert delta > 60_000, f"16 hands vs 12 is only ${delta:,}/season"


# ------------------------------------------------------------------ the layout must fit his crew
def test_his_farm_fits_in_his_crew():
    """The contract. 14 pens and ~61 crop tiles on at most 12 hands.

    Deliberately stated as *his* farm and *his* crew, because both halves are measured and the whole
    question is whether our emitter can hold them together. A layout that needs 16 hands for this farm
    is not a more expensive version of his plan, it is a losing one.
    """
    script = R.Script()
    taken, hands_used = set(), set()

    def cluster(quadrant, n):
        pool = [t for t in [(x, y) for y in range(R.BOARD_SIZE) for x in range(R.BOARD_SIZE)]
                if R.quadrant_of(*t) == quadrant and t not in R.shed_access_tiles()
                and t not in taken]
        pool.sort(key=lambda t: abs(t[0] - 4) + abs(t[1] - 4))
        if not pool:
            return []
        out = [pool[0]]
        while len(out) < n:
            nxt = min((t for t in pool if t not in out
                       and any(abs(t[0] - o[0]) + abs(t[1] - o[1]) == 1 for o in out)),
                      key=lambda t: abs(t[0] - 4) + abs(t[1] - 4), default=None)
            if nxt is None:
                break
            out.append(nxt)
        return R.serpentine(out)

    def place(fn, *fnargs, **kw):
        """Lowest unit that accepts the job, sharing a unit wherever the day still has room."""
        import copy
        for unit in sorted(hands_used) + [u for u in range(20) if u not in hands_used]:
            probe = copy.deepcopy(script)
            try:
                fn(probe, *fnargs, unit=unit, **kw)
            except ValueError:
                continue
            fn(script, *fnargs, unit=unit, **kw)
            hands_used.add(unit)
            return unit
        return None

    # **Group size has to shrink with distance from the shed, and only the emitter knows by how much.**
    # Four adjacent pens fit beside the shed at 22 of 23 turns; the same four one ring further out need
    # 25 and `ranch()` refuses them. Insisting on fours placed 8 pens and then gave up, which measured
    # the fixture rather than the crew. So try the largest group that fits and fall back.
    # The farm owns all three quadrants here -- this test prices the LAYOUT, and land is a separate
    # question with its own tests. `start_day` follows the parcel order so nothing builds on locked
    # ground.
    start_for = {"NW": 0, "NE": 8, "SW": 11}

    def fill(want, place_one):
        got = 0
        for quadrant in ("NW", "NE", "SW"):
            while got < want:
                for size in range(min(8, want - got), 0, -1):
                    group = cluster(quadrant, size)
                    if len(group) < size:
                        continue
                    if place_one(quadrant, group) is None:
                        continue
                    taken.update(group)
                    got += len(group)
                    break
                else:
                    break                      # nothing of any size fits here; next quadrant
        return got

    pens = fill(HIS_PENS, lambda q, g: place(
        R.ranch, "COW" if len(hands_used) < 3 else "SHEEP", g,
        start_day=start_for[q], buy_land=False, feed_every=2, build_every=3))
    tiles = fill(HIS_CROP_TILES, lambda q, g: place(
        R.grow, "STRAWBERRY", g, plant_day=start_for[q] + 1, buy_land=False, water_every=2))

    needed = max(hands_used) if hands_used else 0
    assert pens >= HIS_PENS, f"only placed {pens} of {HIS_PENS} pens"
    assert tiles >= HIS_CROP_TILES - 8, f"only placed {tiles} of {HIS_CROP_TILES} crop tiles"
    assert needed <= HIS_HANDS, (
        f"{pens} pens and {tiles} tiles needed {needed} hands = "
        f"${crew_cost_season(needed):,}/season against his {HIS_HANDS} hands at "
        f"${HIS_CREW_SEASON:,}")
