"""A turn may contain several HIRE orders, and our action interface cannot express that.

**Where the wrong reading is written down.** `kagg/rl/jax_carrot.py:27` states:

    `jax_sim.Actions.hire` is one boolean per seat per turn, because the reference rule
    makes HIRE atomic -- "handle once, in player order" -- so several hires in one turn
    is not expressible here.

That inference is wrong. The reference comment it quotes sits inside a loop over *order slots*
(`reference/kaggriculture.py:538`):

    max_len = max((len(q) for q in queues), default=0)
    for i in range(max_len):                      # <-- over ORDER SLOTS
        order_states = [_parse_order(q[i]) ...]
        # Atomic orders (HIRE, BUY_LAND): handle once, in player order.
        for player_id, ostate in enumerate(order_states):
            if op == "HIRE":
                _do_hire(...)
                order_states[player_id] = None    # the slot is spent

"Atomic" means *this slot's* order resolves once and is then cleared so the per-unit SELL/BUY
lockstep below skips it. It does not mean one hire per turn. Our own `kagg/sim/game.py:364` carries
the correct reading -- "Atomic orders resolve once, in seat order, and then the slot is spent".

**And the leaders rely on it.** In `data/episodes/89541819.json`, turn 1 of `senkin13`:

    {"farmer": ["PASS"], "hands": [],
     "market": [["HIRE"], ["HIRE"], ["BUY_ANIMAL","COW",1],
                ["BUY_SEED","MELON",6], ["BUY_SEED","WHEAT",6], ["SELL","WHEAT",1]]}

and the observation recorded immediately after shows `hires_today: 2` with `hands` of length 2
(three units including the farmer). Two hires, one turn.

Hiring is close to free: `_hire_cost` is `mult * fib(hires_today)` with `FARM_HAND_COST_MULT = 1`
and `hires_today` reset every morning (`reference/kaggriculture.py:850`), so the ladder is
$1, $1, $2, $3, $5, $8, ... Five hands in a day costs $12.

**Why this matters even though the cap is not economically binding.** There are 24 turns in a day
and `MAX_UNITS` is 24, so one hire per turn still reaches a full crew -- this is NOT the cause of the
project's training failures, and it should not be reported as one. What it does break is *exact
replay fidelity*: the replay addresses units by slot index, so the moment our crew size differs from
the recorded one, every subsequent unit action lands on the wrong farmer. Measured consequence in
`data/logs/replay_diag.log` -- positions track exactly for 209 turns and then diverge, and the season
ends at $0 against a recorded $145,034.
"""

import json
import pathlib

import numpy as np
import pytest

from kagg.sim.game import Actions, Game

EPISODE = pathlib.Path("data/episodes/89541819.json")


def test_the_reference_charges_a_fibonacci_ladder_that_resets_daily():
    """Pins the economics that make many hires per day rational, so a future reader does not
    'optimise' hiring down on the assumption that hands are expensive."""
    ref = pathlib.Path("reference/kaggriculture.py").read_text()
    assert "return mult * _fib(n_already_today)" in ref, "hire cost is no longer fib(hires_today)"
    assert "FARM_HAND_COST_MULT = 1" in ref, "the multiplier changed; the ladder is not $1,$1,$2,$3"
    assert 'farm["hires_today"] = 0' in ref, "hires_today no longer resets, so the ladder never resets"


def test_the_atomic_comment_sits_inside_a_loop_over_order_slots():
    """**The refutation of `jax_carrot.py:27`, pinned against the source.** If the atomic-order block
    were executed once per turn, one hire per turn would be right. It is inside `for i in
    range(max_len)`, which walks the order slots."""
    lines = pathlib.Path("reference/kaggriculture.py").read_text().splitlines()
    atomic = next(i for i, l in enumerate(lines) if "Atomic orders (HIRE, BUY_LAND)" in l)
    preceding = "\n".join(lines[max(0, atomic - 12):atomic])
    assert "for i in range(max_len)" in preceding, (
        "the atomic-order block is no longer inside the per-slot loop; re-derive the rule")


@pytest.mark.skipif(not EPISODE.exists(), reason="replay not downloaded")
def test_a_real_leader_issues_two_hires_in_one_turn():
    """Ground truth from the leaderboard, not from reading the rules."""
    steps = json.loads(EPISODE.read_text())["steps"]
    market = steps[1][0]["action"]["market"]
    hires = [o for o in market if o and o[0] == "HIRE"]
    assert len(hires) == 2, f"expected two HIRE orders on turn 1, found {len(hires)}: {market}"

    after = steps[1][0]["observation"]["farms"][0]
    assert after["hires_today"] == 2, f"recorded hires_today {after['hires_today']}, expected 2"
    assert len(after["hands"]) == 2, (
        f"recorded {len(after['hands'])} hands after two hires, expected 2")


@pytest.mark.skipif(not EPISODE.exists(), reason="replay not downloaded")
def test_our_simulator_reproduces_two_hires_in_one_turn():
    """**The failing assertion this file exists for.** Ask for two hires on the first turn and the
    crew must reach three units, as the recorded episode does. `Actions.hire` is a bool, so the
    request cannot even be written down: the closest expressible thing is one hire."""
    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(0))
    actions = Actions(1)
    # The intent is "hire twice this turn". A bool cannot carry it.
    assert actions.hire.dtype != bool, (
        "Actions.hire is still boolean, so several hires in one turn cannot be requested -- "
        "see reference/kaggriculture.py:538 and data/episodes/89541819.json turn 1")
    actions.hire[0, 0] = 2
    game.step(actions)
    assert int(game.farms[0].n_units[0]) == 3, (
        f"asked for two hires, crew is {int(game.farms[0].n_units[0])} units, expected 3 "
        f"(farmer + 2 hands)")


@pytest.mark.skipif(not EPISODE.exists(), reason="replay not downloaded")
def test_buy_land_has_the_same_shape_of_limit():
    """`buy_land` is a bool for the same reason and is wrong for the same reason -- BUY_LAND is in the
    same atomic block. Kept as one assertion so the two are fixed together rather than one being
    found again in a month."""
    actions = Actions(1)
    assert actions.buy_land.dtype != bool, (
        "Actions.buy_land is still boolean; BUY_LAND sits in the same per-slot atomic block as HIRE "
        "(reference/kaggriculture.py:553) so more than one per turn is legal")
