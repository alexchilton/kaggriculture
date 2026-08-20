"""Turn downloaded episode replays into supervised (observation, action) pairs.

**Why this rather than more self-play.** Per-turn PPO from scratch settles into a mutual draw: the
policy converges on doing nothing, an opponent that also does nothing draws with it at $3,000 each,
and the measured symptoms are exact -- `ret` 0.4925 with a standard deviation of 0.0030 over fifteen
updates, `ev_signal` undefined on 12 of 19 because every terminal reward equals 0.5, and a win rate
asymptoting on 0.5 from below because 0.5 *is* the draw value. Nothing in that loop rewards the
first step toward an economy, because the first step costs money and the policy cannot see far
enough ahead to earn it back.

Supervised learning does not have to discover anything. `data/` holds 34 replays of 720 turns and
two seats, and the teachers in 89197802 banked **$106,091 and $113,478** against our best agent's
$51k and this policy's $7. Cloning `contrarian` would inherit a $51k ceiling; cloning these does
not.

**Both seats record a full observation, including `private`.** That is checked rather than assumed
(`test_replays.py`), because a replay format that stored full state only for seat 0 would have made
the winning seat unusable and it is the seat we most want.

The features come from `adapter.state_from_obs` and the *same* `jax_obs.encode` the policy trains
on, for the reason the adapter's own docstring gives: a second encoder is a thing that must agree
forever and will not.
"""

import json
from pathlib import Path

import numpy as np

from kagg.rl import jax_policy as P
from kagg.sim import ops as O
from kagg.sim.jax_sim import MAX_UNITS
from kagg.sim.market import ITEM_INDEX
from kagg.sim.tiles import CROP_INDEX

# Name -> op code, matching `kagg.sim.ops`. Ops the replay can contain that the simulator folds into
# NOOP (PASS, and anything illegal) map to NOOP, which is what the simulator would have done anyway.
OP_CODE = {
    "PASS": O.NOOP, "NORTH": O.NORTH, "SOUTH": O.SOUTH, "EAST": O.EAST, "WEST": O.WEST,
    "WATER": O.WATER, "HARVEST": O.HARVEST, "PLANT": O.PLANT_OP, "DIG": O.DIG,
    "PICKUP": O.PICKUP, "DROP": O.DROP, "PLACE": O.PLACE, "FEED": O.FEED, "CARE": O.CARE,
    "COLLECT_FERTILIZER": O.COLLECT_FERT, "FERTILIZE": O.FERTILIZE,
    "BUILD_COOP": O.BUILD_COOP, "BUILD_PASTURE": O.BUILD_PASTURE,
}

ANIMAL_INDEX = {"GOOSE": 0, "COW": 1, "SHEEP": 2}
PRODUCTS = [k for k, v in sorted(ITEM_INDEX.items(), key=lambda kv: kv[1]) if v < 9]

_SELL = np.asarray(P.SELL_BUCKETS)
_BUY = np.asarray(P.BUY_BUCKETS)
_QTY = np.asarray(P.UNIT_QTY_BUCKETS)


def _bucket(value, buckets):
    """Nearest bucket index. The heads are categorical over fixed quantities, so an exact
    quantity the teacher used may not be representable; the closest bucket is the best label
    available and the error is bounded by the bucket spacing."""
    return int(np.argmin(np.abs(buckets - value)))


def encode_action(action, n_units):
    """One turn's action dict -> the head labels the policy would have had to emit.

    Returns a dict of arrays shaped like the policy's heads for a single seat. Unit slots beyond
    the crew's size are NOOP, which is what `to_sim_actions` feeds the simulator for them too.
    """
    op = np.zeros(MAX_UNITS, dtype=np.int32)
    crop = np.zeros(MAX_UNITS, dtype=np.int32)
    item = np.zeros(MAX_UNITS, dtype=np.int32)
    qty = np.zeros(MAX_UNITS, dtype=np.int32)

    units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
    for i, act in enumerate(units[:MAX_UNITS]):
        if not act:
            continue
        name = act[0]
        op[i] = OP_CODE.get(name, O.NOOP)
        if name == "PLANT" and len(act) > 1:
            crop[i] = CROP_INDEX.get(act[1], 0)
        elif name in ("PICKUP", "DROP", "PLACE"):
            if len(act) > 1:
                item[i] = ITEM_INDEX.get(act[1], 0)
            if len(act) > 2:
                qty[i] = _bucket(act[2], _QTY)

    sell = np.zeros(len(PRODUCTS), dtype=np.int32)
    buy_product = np.zeros(len(PRODUCTS), dtype=np.int32)
    buy_seed = np.zeros(len(CROP_INDEX), dtype=np.int32)
    buy_animal = np.zeros(len(ANIMAL_INDEX), dtype=np.int32)

    for order in action.get("market") or []:
        kind = order[0]
        if kind == "SELL" and len(order) > 2 and order[1] in ITEM_INDEX:
            idx = ITEM_INDEX[order[1]]
            if idx < len(PRODUCTS):
                sell[idx] = _bucket(order[2], _SELL)
        elif kind == "BUY_PRODUCT" and len(order) > 2 and order[1] in ITEM_INDEX:
            idx = ITEM_INDEX[order[1]]
            if idx < len(PRODUCTS):
                buy_product[idx] = _bucket(order[2], _BUY)
        elif kind == "BUY_SEED" and len(order) > 2 and order[1] in CROP_INDEX:
            buy_seed[CROP_INDEX[order[1]]] = _bucket(order[2], _BUY)
        elif kind == "BUY_ANIMAL" and len(order) > 1 and order[1] in ANIMAL_INDEX:
            # **Binary, not a quantity.** The `buy_animal` head is `N_ANIMALS x 2` and
            # `to_sim_actions` passes it through as the count, so the only values it can express are
            # 0 and 1. Writing the teacher's actual quantity here put 2s and 3s in the labels, and
            # JAX does *not* clip an out-of-range index in `take_along_axis` -- it returns NaN,
            # which propagated through the total loss and printed as `train nan`.
            buy_animal[ANIMAL_INDEX[order[1]]] = 1
        # HIRE and BUY_LAND carry no quantity head. They are part of the BUNDLE identity now --
        # `HIRE x10` is a different symbol from `HIRE x1` -- so reading them here would only
        # reintroduce the flag that lost the count.

    # **The market is one bundle, not six marginals -- and `hire` is a COUNT.**
    #
    # The loop above accumulated per-product quantity buckets, which are still the right labels for
    # the `qty_*` heads. What it CANNOT express is the bundle: which orders went out together. And
    # The `hire` flag this used to write was the exact defect this change removes -- `jax_sim` reads
    # `hire` as "COUNT of hands to hire this turn, not a flag" (:258) and warns that casting to bool
    # "would collapse 'hire twice' to 'hire once'" (:315), while the teacher's second most common
    # market decision is ten hires in a single turn.
    #
    # So the bundle is read straight off the order list, where the multiplicity survives, and the
    # per-product buckets are kept as the conditioned quantity labels.
    from kagg.il import market_bundles as _MB

    vocab = _MB.load_vocab()
    bundle = np.int32(vocab.index(_MB.bundle_of(orders)))

    # A quantity is only a decision where the bundle asked for one. Without these weights the
    # 78.9% of turns that send nothing train every quantity head toward bucket 0 -- the padding
    # mistake `bc.py` already warns about three times for the unit heads.
    w_sell = np.zeros(len(PRODUCTS), dtype=np.float32)
    w_buy_product = np.zeros(len(PRODUCTS), dtype=np.float32)
    w_buy_seed = np.zeros(len(CROP_INDEX), dtype=np.float32)
    for order in orders:
        if not order:
            continue
        kind = order[0]
        if kind == "SELL" and len(order) > 1 and order[1] in ITEM_INDEX:
            i = ITEM_INDEX[order[1]]
            if i < len(PRODUCTS):
                w_sell[i] = 1.0
        elif kind == "BUY_PRODUCT" and len(order) > 1 and order[1] in ITEM_INDEX:
            i = ITEM_INDEX[order[1]]
            if i < len(PRODUCTS):
                w_buy_product[i] = 1.0
        elif kind == "BUY_SEED" and len(order) > 1 and order[1] in CROP_INDEX:
            w_buy_seed[CROP_INDEX[order[1]]] = 1.0

    return {"op": op, "crop": crop, "item": item, "qty": qty,
            "bundle": bundle,
            "qty_sell": sell, "qty_buy_product": buy_product, "qty_buy_seed": buy_seed,
            "w_qty_sell": w_sell, "w_qty_buy_product": w_buy_product,
            "w_qty_buy_seed": w_buy_seed}


def iter_turns(path, winners_only=True, min_bank=None, hide_opponent=True, seats=None,
               with_index=False):
    """Yield `(shared_obs, privates, action, seat)` for each recorded turn of one replay.

    `with_index` appends the observation's **recorded step index** to each tuple. It is needed
    because `obs["step"]` is `None` in some replays -- `adapter.state_from_obs` then defaults it to
    0, and a caller that seeds an episode from a mid-season board would get day-15 tile contents
    carrying a day-0 counter. Every crop and animal rule reads `step_index // TURNS_PER_DAY`, so
    that board would be run under the wrong rules with nothing to indicate it. Pinned by
    `tests/test_curriculum.py::test_the_step_index_matches_the_day_it_claims`.

    `winners_only` keeps the seat that finished with more money. `min_bank` keeps any seat that
    finished above a threshold instead, which is usually the better filter: in 89197802 the *losing*
    seat still banked $106,091, and discarding it throws away a teacher because of who it happened
    to be drawn against.

    `seats` names the seats to keep outright, for a caller that has already ranked every seat in
    every replay and wants exactly the ones it chose (`kagg.il.bc.rank_seats`). It overrides both
    filters above.

    **`hide_opponent` blanks the other seat's private state, and it must stay on.** A replay records
    both players' sheds, seeds and carried inventory, but a real agent only ever sees its own -- the
    environment hands it `agent_private_stub()` for the opponent. Training on the full pair and then
    playing with the stub is a distribution shift that flatters every offline number and shows up
    only on the ladder, which is exactly the failure mode `adapter.py` warns about in its own
    docstring.
    """
    replay = json.loads(Path(path).read_text())
    steps = replay["steps"]
    rewards = [p.get("reward") or 0.0 for p in steps[-1]]
    best = int(np.argmax(rewards))

    def wanted(seat):
        if seats is not None:
            return seat in seats
        if min_bank is not None:
            return rewards[seat] >= min_bank
        return seat == best if winners_only else True

    blank = {"shed": {}, "seeds": {}, "inventories": [{}]}

    # **`steps[t]["observation"]` is the state that `steps[t]["action"]` already produced**, so the
    # state a teacher decided from is the one recorded at `t - 1`. Pairing them at the same index --
    # which this did -- puts the label's own effect in its features.
    #
    # It is not a mild leak. WATER, PLANT, FEED, CARE and COLLECT_FERTILIZER all act on the tile the
    # unit is standing on, and the recorded observation shows that tile *already watered, already
    # planted, already fed*. Measured over 18,000 rows of the top 25 seats, the teacher's own label
    # was illegal under the rebuilt masks on 100% of WATER (0 of 14,009), PLANT (0 of 2,297) and
    # FEED (0 of 9,097) rows, while NOOP read 100% legal and movement 90%. Those ops were dropped
    # from the loss entirely, which is why a run could report a falling loss and predict FEED on
    # 0.00% of slots against a teacher rate of 7.78%.
    #
    # It is also the most likely explanation for the parked BC track's headline symptom. From a
    # post-action observation "what did you do?" is largely readable off the state, so offline
    # accuracy flatters and on-policy play collapses -- and at spawn a PASS leaves the state
    # unchanged, which is the `P(noop) = 0.9920` that gated it.
    #
    # Verified two independent ways over 9,166 moves and 11,504 turns in `tests/test_bc_replay.py`:
    # a MOVE at `t` explains `obs[t-1] -> obs[t]` on 100% of turns away from the nightly respawn
    # (against 27.9% the other way), and the number of hand actions matches the crew in `obs[t-1]`
    # on 100% of turns (against 87.4%).
    #
    # `steps[0]`'s action is dropped: the state it was chosen from is before the recording starts.
    for t, (prev, step) in enumerate(zip(steps, steps[1:])):
        if len(step) < 2 or len(prev) < 2:
            continue
        for seat in range(2):
            if not wanted(seat):
                continue
            obs = prev[seat].get("observation")
            action = step[seat].get("action")
            if not obs or not action or not obs.get("farms"):
                continue
            mine = obs.get("private") or dict(blank)
            privates = [mine if p == seat else dict(blank) for p in range(2)] if hide_opponent \
                else [prev[p].get("observation", {}).get("private") or dict(blank)
                      for p in range(2)]
            # `t` indexes `prev`, which is the state the action was decided from.
            yield (obs, privates, action, seat, t) if with_index else (obs, privates, action, seat)


def replay_summary(path):
    """Final rewards and the winning seat, without walking every turn."""
    replay = json.loads(Path(path).read_text())
    rewards = [p.get("reward") or 0.0 for p in replay["steps"][-1]]
    return {"path": str(path), "rewards": rewards, "winner": int(np.argmax(rewards)),
            "turns": len(replay["steps"])}
