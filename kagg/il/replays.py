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

from kagg.il import market_bundles as MB
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

def fold_illegal_ops_to_noop(op_labels, op_mask, n_units):
    """Teach NOOP wherever the mask forbids the teacher's op -- what the simulator did anyway.

    The header above has claimed this since it was written, and `OP_CODE` only ever folded PASS:
    `encode_action` never sees the board, so it cannot test legality. `ops.py:41` says the same
    thing about the code itself -- "NOOP covers both PASS and any action that turns out to be
    illegal" -- so this is the fold both files already describe, applied where the mask exists.

    Measured over the four tapes, whole season: **104 DIG labels, 97 legal, 7 on an already-empty
    tile**, where `reference/kaggriculture.py:484` returns without touching anything.

    Left as `O.DIG` those 7 are blocked twice over -- `-1e9` under `greedy_action`'s argmax over
    `_masked_logits`, and weight zero from `bc.py:232` -- so they are invisible in the loss AND in
    sampled agreement. DIG's ceiling is `97/104 = 0.933` and a converged net sits exactly there.

    The cost is not the agreement figure, it is what the net emits when asked a question it cannot
    answer. Round 27, greedy decode, full season, first pure model error on each of the four tapes
    was one of these digs:

        tape          on-tape    off-tape       gap   substitute
        92498144      150,316     149,599      -717   PLANT   (in place, hand stays)
        91906088      128,471     126,541    -1,930   SOUTH   (hand walks off)
        91907974       88,882      46,839   -42,043   WEST    (hand walks off)
        92466371      147,036         372  -146,664   PLANT

    `op_mask` is this seat's slice, `(units, ops)`. NOOP is never masked (`jax_masks.py:117`), so
    the fold cannot move the problem to another op.
    """
    out = np.array(op_labels)
    for u in range(min(int(n_units), len(out))):
        if not bool(op_mask[u, int(out[u])]):
            out[u] = O.NOOP
    return out


def seat_op_mask(masks, seat):
    """This seat's `(units, ops)` slice of a two-seat op mask."""
    flat = np.asarray(masks["op"])
    return flat.reshape(2, -1, flat.shape[-1])[seat]


def encode_action_legal(action, n_units, vocab, op_mask):
    """`encode_action`, with every op the mask forbids folded to NOOP.

    The one entry point for producing training labels. Both the trainer and
    `tests/test_a_label_the_mask_forbids_is_taught_as_doing_nothing.py` go through it, so the test
    covers the path that actually trains rather than a re-implementation of it.
    """
    labels = encode_action(action, n_units, vocab=vocab)
    labels["op"] = fold_illegal_ops_to_noop(labels["op"], op_mask, n_units)
    return labels


ANIMAL_INDEX = {"GOOSE": 0, "COW": 1, "SHEEP": 2}
PRODUCTS = [k for k, v in sorted(ITEM_INDEX.items(), key=lambda kv: kv[1]) if v < 9]

_QTY = np.asarray(P.UNIT_QTY_BUCKETS)


def _bucket(value, buckets):
    """Nearest bucket index, for the UNIT quantity ladder only.

    The market quantity heads no longer use one: their class index is the quantity itself, via
    `market_bundles.clamp_qty`. The rungs cost a measured 27.2% on SELL and 35.3% on BUY_PRODUCT
    against a teacher whose numbers are known exactly, which in imitation is pure waste.
    """
    return int(np.argmin(np.abs(buckets - value)))


def encode_action(action, n_units, vocab=None):
    """One turn's action dict -> the head labels the policy would have had to emit.

    Returns a dict of arrays shaped like the policy's heads for a single seat. Unit slots beyond
    the crew's size are NOOP, which is what `to_sim_actions` feeds the simulator for them too.

    `vocab` is the bundle vocabulary to label against. **Pass it.** This function used to read
    `MB.load_vocab()` with no argument while `dagger_tape` passed `--vocab` to build the head
    tables; they were the same file by luck and nothing made them so. `load_vocab`'s own docstring
    warns that two disagreeing vocabularies show up nowhere offline, because every index is still a
    valid index.
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

    orders = action.get("market") or []

    for order in orders:
        kind = order[0]
        if kind == "SELL" and len(order) > 2 and order[1] in ITEM_INDEX:
            idx = ITEM_INDEX[order[1]]
            if idx < len(PRODUCTS):
                sell[idx] = MB.clamp_qty(order[2])
        elif kind == "BUY_PRODUCT" and len(order) > 2 and order[1] in ITEM_INDEX:
            idx = ITEM_INDEX[order[1]]
            if idx < len(PRODUCTS):
                buy_product[idx] = MB.clamp_qty(order[2])
        elif kind == "BUY_SEED" and len(order) > 2 and order[1] in CROP_INDEX:
            buy_seed[CROP_INDEX[order[1]]] = MB.clamp_qty(order[2])
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
    vocab = MB.load_vocab() if vocab is None else vocab
    shape = MB.bundle_of(orders)
    bundle = np.int32(vocab.index(shape))
    # **A silent fallback to EMPTY is fine at play time and is a defect at LABEL time.**
    #
    # `Vocabulary.index` returns 0 for an unknown bundle, and 0 means "place no orders". So a
    # teacher turn the vocabulary cannot express is taught to the student as "do nothing", and
    # bundle agreement then SCORES IT AS A HIT because the student obediently emits nothing too.
    # Measured 2026-08-22 over the four tape teachers: 179 of 1451 traded turns, 12.3%, containing
    # 512 HIRE and 444 SELL orders -- the whole opening, every crew hire, the land-buy day.
    # `docs/the_vocabulary_labels_the_opening_as_nothing_2026-08-22.md`.
    #
    # The fallback stays -- it is pinned by `test_a_market_bundle_survives_the_round_trip.py` and it
    # is the right behaviour where an unknown bundle is expected. What was missing is any way for
    # the caller to know it happened. Non-empty orders that land on index 0 are reported here so a
    # training loop can count them, print them, and refuse.
    # Named `w_` so the existing convention keeps it out of the head labels: `dagger_tape.stack`
    # already drops every `w_` key when it builds `batch_data`. This is metadata about the label,
    # not a label.
    w_bundle_miss = np.int32(1 if (orders and shape != MB.bundle_of([])
                                   and int(bundle) == 0) else 0)

    # A quantity is only a decision where the bundle asked for one. Without these weights the
    # 78.9% of turns that send nothing train every quantity head toward class 0 -- the padding
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
            "w_qty_buy_seed": w_buy_seed,
            "w_bundle_miss": w_bundle_miss}


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
