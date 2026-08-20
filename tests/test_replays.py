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

from kagg.il import market_bundles as MB, replays
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

    from kagg.il import market_bundles as MB
    from kagg.rl import jax_act as A, jax_policy as P
    from kagg.sim import jax_sim as J

    heads = replays.encode_action(
        {"farmer": ["PLANT", "MELON"], "hands": [["WATER"]], "market": [["HIRE"]] * 10}, n_units=2)

    # `to_sim_actions` decodes the bundle index through the static tables, so it needs the SAME
    # vocabulary the labels were written against. A different file and every index means something
    # else, with nothing offline to show it.
    tables = {k: jnp.asarray(v)
              for k, v in MB.tables(MB.load_vocab(), pad_to=P.N_BUNDLES).items()}

    # Two seats of one game, which is the layout `to_sim_actions` unflattens.
    batched = {k: jnp.broadcast_to(jnp.asarray(v), (2,) + np.shape(v)) for k, v in heads.items()}
    sim = A.to_sim_actions(batched, batch=1, tables=tables)

    assert sim.unit_op.shape == (1, 2, J.MAX_UNITS)
    assert int(sim.unit_op[0, 0, 0]) == O.PLANT_OP
    assert int(sim.unit_crop[0, 0, 0]) == 4

    # **A COUNT, not a flag.** Ten HIRE orders must survive as ten. This is the whole reason the
    # market became one bundle: `hire = np.int32(1)` in the label path capped the teacher's most
    # common large market decision at a single hand.
    assert int(sim.hire[0, 0]) == 10, "ten hires collapsed to %d" % int(sim.hire[0, 0])


def test_market_orders_encode_to_the_right_buckets():
    """Quantities are categorical, so the label is the nearest representable bucket."""
    action = {
        "farmer": ["PASS"], "hands": [],
        "market": [["SELL", "MELON", 3], ["BUY_PRODUCT", "WHEAT", 5],
                   ["BUY_SEED", "MELON", 2], ["BUY_ANIMAL", "COW", 1],
                   ["HIRE"], ["BUY_LAND"]],
    }
    heads = replays.encode_action(action, n_units=1)

    # Exact, not nearest-rung. The quantity head's class index IS the quantity, so a teacher who
    # sold 3 is labelled 3. On the old ladders these read back as 3, 5 and 2 only by luck of which
    # rungs existed; `SELL 18` came back as 30.
    assert heads["qty_sell"][4] == 3                            # MELON is product 4
    assert heads["qty_buy_product"][0] == 5                     # WHEAT is product 0
    assert heads["qty_buy_seed"][4] == 2

    # BUY_ANIMAL, HIRE and BUY_LAND carry no quantity head at all: they are part of the BUNDLE
    # identity, so `HIRE x10` is a different symbol from `HIRE x1`. `hire = 1` was the bug this
    # whole change exists to remove -- the teacher hires ten hands in one turn, 18,666 times in
    # 920,320 turns, and a flag capped every one of them at one hand.
    assert "hire" not in heads and "buy_land" not in heads and "buy_animal" not in heads
    assert heads["bundle"] == MB.load_vocab().index(MB.bundle_of(action["market"]))

    # Only the products the bundle named are scored. Weighting every entry would train the other
    # eight toward class 0 on a turn the teacher had no opinion about them.
    assert heads["w_qty_sell"][4] == 1.0 and heads["w_qty_sell"][0] == 0.0


def test_every_label_is_in_range_for_its_head():
    """A label outside its head's class count is silently fatal.

    JAX's `take_along_axis` does **not** clip an out-of-bounds index -- it returns NaN, which
    propagates through the summed loss and shows up only as `train nan` several layers away. That
    is exactly what `buy_animal` did: the head is `N_ANIMALS x 2` and `to_sim_actions` passes it
    through as the count, so it is binary, and the teacher's real quantity of 2 or 3 was being
    written straight into the labels.
    """
    from kagg.rl import jax_policy as P
    from kagg.sim import jax_sim as J

    sizes = {"op": O.N_OPS, "crop": J.N_CROPS, "item": J.N_ITEMS,
             "qty": len(P.UNIT_QTY_BUCKETS), "qty_sell": P.MAX_QTY,
             "qty_buy_product": P.MAX_QTY, "qty_buy_seed": P.MAX_QTY,
             "bundle": P.N_BUNDLES}

    worst = {}
    for _obs, _priv, action, _seat in replays.iter_turns(REPLAY):
        for k, v in replays.encode_action(action, n_units=24).items():
            if k.startswith("w_"):
                continue          # per-product loss weights, not class indices
            worst[k] = max(worst.get(k, 0), int(np.max(v)))

    over = {k: (worst[k], sizes[k]) for k in worst if worst[k] >= sizes[k]}
    assert not over, f"labels out of range for their head (label_max, n_classes): {over}"


def test_a_pass_turn_encodes_to_all_noop():
    """The idle action must be all-zeros, the same fact the RL idle opponent relies on."""
    heads = replays.encode_action({"farmer": ["PASS"], "hands": [["PASS"]], "market": []}, 2)

    assert not heads["op"].any()
    assert not heads["qty_sell"].any() and not heads["qty_buy_product"].any()
    assert heads["bundle"] == 0, "an empty market is the empty bundle, pinned at index 0"
    # `hire` is no longer a head. It is part of the bundle identity, so an idle turn is idle by
    # being bundle 0, not by a separate flag reading zero.
    assert "hire" not in heads


def test_the_dataset_is_big_enough_to_be_worth_it():
    """One replay is 720 turns of one winner; the directory holds dozens."""
    n = sum(1 for _ in replays.iter_turns(REPLAY))

    assert n > 600, f"only {n} usable turns in a 720-step replay"
