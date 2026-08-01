"""Replays as supervised data, and the two assumptions that decide whether any of it is usable.

The first is that **both seats record a full observation**. Kaggle formats sometimes store complete
state only for seat 0, and the seat we most want to imitate is whichever one won -- seat 1 in
89197802, which banked $113,478. If that seat's observation were missing the whole plan collapses,
so it is checked rather than assumed.

The second is that the action encoding **round-trips**: what `encode_action` produces has to survive
`jax_act.to_sim_actions` and come back as the operation the teacher actually issued. A silent
mismatch here would train the policy on labels that mean something else, which is invisible in a
loss curve and fatal in play.
"""

import json
from pathlib import Path

import numpy as np
import pytest

from kagg.il import replays
from kagg.sim import ops as O

DATA = Path(__file__).resolve().parent.parent / "data"
REPLAY = DATA / "89197802.json"

pytestmark = pytest.mark.skipif(not REPLAY.exists(), reason="replay data not downloaded")


def test_both_seats_record_a_full_observation():
    """If only seat 0 had state, the winning seat would be unusable as a teacher."""
    steps = json.loads(REPLAY.read_text())["steps"]

    for seat in (0, 1):
        obs = steps[5][seat].get("observation") or {}
        assert obs.get("farms"), f"seat {seat} has no farms"
        assert obs.get("private"), f"seat {seat} has no private state"
        assert len(obs["farms"]) == 2


def test_the_winner_is_the_seat_we_keep():
    summary = replays.replay_summary(REPLAY)

    assert summary["rewards"] == [106091.0, 113478.0]
    assert summary["winner"] == 1

    seats = {seat for _obs, _priv, _act, seat in replays.iter_turns(REPLAY)}
    assert seats == {1}, f"kept seats {seats}, expected only the winner"


def test_unit_ops_encode_to_the_teachers_actual_operations():
    """A real turn out of 89197802, and every slot has to come back as what the teacher did."""
    action = {
        "farmer": ["WEST"],
        "hands": [["WEST"], ["BUILD_PASTURE"], ["PASS"], ["PLANT", "MELON"],
                  ["PICKUP", "SHEEP", 1], ["NORTH"]],
        "market": [["SELL", "WHEAT", 1]],
    }
    heads = replays.encode_action(action, n_units=7)

    assert list(heads["op"][:7]) == [
        O.WEST, O.WEST, O.BUILD_PASTURE, O.NOOP, O.PLANT_OP, O.PICKUP, O.NORTH]
    assert heads["crop"][4] == 4, "MELON is crop index 4"
    assert heads["item"][5] == 11, "SHEEP is item index 11"
    assert list(heads["op"][7:]) == [0] * (len(heads["op"]) - 7), "unused slots must be NOOP"


def test_encoded_heads_have_the_shapes_to_sim_actions_expects():
    """The labels have to be the same objects the policy emits, or training targets nothing real."""
    import jax.numpy as jnp

    from kagg.rl import jax_act as A
    from kagg.sim import jax_sim as J

    heads = replays.encode_action(
        {"farmer": ["PLANT", "MELON"], "hands": [["WATER"]], "market": [["HIRE"]]}, n_units=2)

    # Two seats of one game, which is the layout `to_sim_actions` unflattens.
    batched = {k: jnp.broadcast_to(jnp.asarray(v), (2,) + np.shape(v)) for k, v in heads.items()}
    sim = A.to_sim_actions(batched, batch=1)

    assert sim.unit_op.shape == (1, 2, J.MAX_UNITS)
    assert int(sim.unit_op[0, 0, 0]) == O.PLANT_OP
    assert int(sim.unit_crop[0, 0, 0]) == 4
    assert bool(sim.hire[0, 0])


def test_market_orders_encode_to_the_right_buckets():
    """Quantities are categorical, so the label is the nearest representable bucket."""
    action = {
        "farmer": ["PASS"], "hands": [],
        "market": [["SELL", "MELON", 3], ["BUY_PRODUCT", "WHEAT", 5],
                   ["BUY_SEED", "MELON", 2], ["BUY_ANIMAL", "COW", 1],
                   ["HIRE"], ["BUY_LAND"]],
    }
    heads = replays.encode_action(action, n_units=1)

    assert replays.P.SELL_BUCKETS[heads["sell"][4]] == 3        # MELON is product 4
    assert replays.P.BUY_BUCKETS[heads["buy_product"][0]] == 5  # WHEAT is product 0
    assert replays.P.BUY_BUCKETS[heads["buy_seed"][4]] == 2
    assert heads["buy_animal"][1] == 1                          # COW
    assert heads["hire"] == 1 and heads["buy_land"] == 1


def test_a_pass_turn_encodes_to_all_noop():
    """The idle action must be all-zeros, the same fact the RL idle opponent relies on."""
    heads = replays.encode_action({"farmer": ["PASS"], "hands": [["PASS"]], "market": []}, 2)

    assert not heads["op"].any()
    assert not heads["sell"].any() and not heads["buy_product"].any()
    assert heads["hire"] == 0


def test_the_dataset_is_big_enough_to_be_worth_it():
    """One replay is 720 turns of one winner; the directory holds dozens."""
    n = sum(1 for _ in replays.iter_turns(REPLAY))

    assert n > 600, f"only {n} usable turns in a 720-step replay"
