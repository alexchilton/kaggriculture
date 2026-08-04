"""Carrying an item through dawn, and selling it at hour 0. The one boundary nothing exercised.

**Why this file exists.** `tests/test_sim_parity.py` passes 719-step full-length episodes and is
genuinely exact -- but until 2026-08-04 `compare` looked only at money, the *market's* inventory, and a
tile census. An item moving between a unit's hands and the shed changes none of those, so the entire
dawn-drop phase was uncompared. `shed` and `carried` are now in the trace, and they are clean.

They are clean partly because the random scripts do not reach this case. Measured on the seed the
parity suite uses:

    ref[23] carried=[[{}], [{}]]     <- step 23->24 is the day boundary, and nothing is being carried

`random_script` picks ops independently per step, so a unit holding something at hour 23 *and* an order
against that item at hour 0 is vanishingly rare. That is the CLAUDE.md rule about gates only testing
what they exercise, so this asks for it directly instead of hoping a random draw wanders in.

The case matters because replaying a real tape first broke at a dawn boundary -- episode 89873723 seat 0,
turn 48 (day 2, hour 0), selling one FERTILIZER that the previous day's `COLLECT_FERTILIZER` ops had put
in a unit's hands, worth $99.

**That turned out not to be a phase-order bug.** These tests establish that both implementations drop
carried inventory inside the hour-23 step, so an hour-0 order sees it in the shed. The coverage gap they
close is real regardless: nothing previously compared `shed` or `carried` at all, let alone across dawn.
The turn-48 divergence has another cause and is still open.
"""

import numpy as np
import pytest

from kagg.sim import ops as O
from kagg.sim import parity as PA
from kagg.sim.market import ITEM_INDEX

TURNS_PER_DAY = 24


def _blank_entry(n_units=1):
    return {
        "units": [([O.NOOP] * n_units, [0] * n_units, [0] * n_units, [1] * n_units)
                  for _ in range(2)],
        "sell": [{}, {}],
        "buy_seed": [{}, {}],
        "hire": [False, False],
        "buy_land": [False, False],
        "buy_product": [{}, {}],
        "buy_animal": [{}, {}],
    }


def _script_carrying_wheat_through_dawn(sell_hour):
    """Buy wheat, PICKUP into a unit's hands late on day 0, then SELL at `sell_hour` of day 1.

    The unit spawns on the shed at dawn, so a PICKUP needs no walking. Selling on the far side of the
    boundary is the whole point: the wheat is in hands, not the shed, when the day turns over.
    """
    steps = TURNS_PER_DAY + sell_hour + 2
    script = [_blank_entry() for _ in range(steps)]

    # Hour 0 of day 0: buy wheat into the shed for both seats, so there is something to carry.
    for seat in range(2):
        script[0]["buy_product"][seat] = {"WHEAT": 3}

    # Hour 22 of day 0: pick it up, so it is in hands when the day ends.
    for seat in range(2):
        script[22]["units"][seat] = ([O.PICKUP], [0], [ITEM_INDEX["WHEAT"]], [3])

    # The sell, on the other side of dawn.
    t = TURNS_PER_DAY + sell_hour
    for seat in range(2):
        script[t]["sell"][seat] = {"WHEAT": 3}
    return script


@pytest.mark.parametrize("sell_hour", [0, 1])
def test_an_item_carried_through_dawn_settles_as_the_reference_settles_it(sell_hour):
    """**The uncovered boundary.** Sell at hour 0 and at hour 1, since only one of them is ambiguous.

    Hour 1 is a control: by then the drop has certainly happened in both implementations, so a failure
    there would mean something broader than a phase-order error.
    """
    script = _script_carrying_wheat_through_dawn(sell_hour)
    ref, unlocks = PA.run_reference(script, seed=0)
    sim = PA.run_sim([script], seed=0, unlocks=unlocks)[0]

    problems = PA.compare(sim, ref, label=f"sell_hour={sell_hour} ")
    assert not problems, problems[0]


def test_the_carry_actually_happens_so_the_test_is_not_vacuous():
    """A gate that exercises nothing passes for the wrong reason. Prove the wheat is in hands at dawn."""
    script = _script_carrying_wheat_through_dawn(sell_hour=0)
    ref, _ = PA.run_reference(script, seed=0)

    # Hour 22, not 23: the drop fires *within* the hour-23 step in both implementations, so the
    # hour-23 snapshot already shows the wheat back in the shed. Checking there is how this assertion
    # first failed against a fixture that was working correctly.
    at_hour_22 = ref[22]["carried"][0]
    assert any(inv.get("WHEAT", 0) > 0 for inv in at_hour_22), (
        f"no wheat in hand at hour 22, so this test cannot see the dawn drop: {at_hour_22}")
    # And it is back in the shed by the end of hour 23, which is the phase order being pinned.
    assert ref[TURNS_PER_DAY - 1]["shed"][0].get("WHEAT", 0) >= 3


def test_the_reference_and_our_sim_agree_on_when_the_shed_receives_it():
    """Pins the phase order itself, as a fact about both implementations rather than a guess.

    Recorded rather than asserted in one direction: whichever turn the shed gains the wheat, both must
    agree, and the test says which turn that is so a future change is visible in the diff.
    """
    script = _script_carrying_wheat_through_dawn(sell_hour=1)
    ref, unlocks = PA.run_reference(script, seed=0)
    sim = PA.run_sim([script], seed=0, unlocks=unlocks)[0]

    def first_shed_turn(trace):
        for i, entry in enumerate(trace):
            if i >= TURNS_PER_DAY - 1 and entry["shed"][0].get("WHEAT", 0) >= 3:
                return i
        return None

    theirs, ours = first_shed_turn(ref), first_shed_turn(sim)
    assert theirs == ours, (
        f"the shed receives the carried wheat at turn {ours} in our sim and turn {theirs} in the "
        f"reference -- a one-turn phase-order difference, which is worth real money for any order "
        f"placed on that boundary")
