"""The two decoders must emit the same order SEQUENCE, not just the same order SET.

**The defect this pins.** `orders_from_heads` builds an explicit list and sorts it by `SLOT_ORDER`.
`jax_act.to_sim_actions` builds per-product quantity VECTORS, and `_order_book` then lays those out
in its own fixed sequence -- sells, seeds, products, animals, HIRE, BUY_LAND. The two sequences were
different, and a bundle is a sorted multiset, so nothing that compares contents could see it.

It matters because the environment settles slots in sequence: slot i takes its money and its shed
space before slot i+1 is quoted. Measured 2026-08-22 on the teacher's turn 0, same ten orders:

    HIRE before the wheat product   bank 3000 -> 13    hands 5   shed {WHEAT 5, COW 2, SHEEP 2}
    the wheat product before it     bank 3000 -> 484   hands 5   shed {WHEAT 6, COW 2, SHEEP 1}

So the student rolls out in the real environment through `orders_from_heads` and is EVALUATED in a
simulator that gives it a different farm from the same decision. Every sim-side number would be
measuring a game the ladder will not play.

`Actions` already carries `order_op` / `order_item` / `order_qty`, and both `Game._order_book` and
`jax_sim._order_book` prefer an explicit list over the canonical layout, per seat. This pins that
`to_sim_actions` fills them, and fills them with exactly what `orders_from_heads` emits.

The division of labour between this test and its neighbours:

- this one -- the two decoders AGREE on the sequence.
- `test_the_opening_orders_leave_the_shed_the_tape_has.py` -- the agreed sequence is the RIGHT one,
  pinned by outcome on the real environment.
- `test_the_orders_go_out_in_the_order_the_bank_needs.py` -- `orders_from_heads` never emits out of
  slot rank.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.il import market_bundles as MB
from kagg.rl import jax_act as A
from kagg.rl import jax_policy as P
from kagg.sim import game as G
from kagg.sim import jax_sim as J
from kagg.sim.market import ANIMALS, PRODUCTS
from kagg.sim.tiles import CROP_INDEX

CROPS = [c for c, _ in sorted(CROP_INDEX.items(), key=lambda kv: kv[1])]

#: Both live vocabulary artifacts. `bundle_vocab.json` was built from leaderboard games;
#: `bundle_vocab_teacher.json` from the tape teacher's own output, and it is the one DAgger runs on.
#: The agreement property must hold for whichever file a run loads.
VOCAB_FILES = ["data/il/bundle_vocab.json", "data/il/bundle_vocab_teacher.json"]

#: Op name -> the simulator's `ORDER_*` value. Both sims share this enum.
OP_CODE = {MB.SELL: G.ORDER_SELL, MB.BUY_SEED: G.ORDER_BUY_SEED,
           MB.BUY_PRODUCT: G.ORDER_BUY_PRODUCT, MB.BUY_ANIMAL: G.ORDER_BUY_ANIMAL,
           MB.HIRE: G.ORDER_HIRE, MB.BUY_LAND: G.ORDER_BUY_LAND}

#: Which index space each op's `item` field lives in.
ITEM_SPACE = {MB.SELL: PRODUCTS, MB.BUY_PRODUCT: PRODUCTS, MB.BUY_SEED: CROPS,
              MB.BUY_ANIMAL: ANIMALS}


def as_slots(orders):
    """`orders_from_heads` output -> the `(op, item, qty)` triples a slot list should hold."""
    out = []
    for o in orders:
        op = o[0]
        item = ITEM_SPACE[op].index(o[1]) if op in ITEM_SPACE else 0
        out.append((OP_CODE[op], item, int(o[2]) if len(o) > 2 else 1))
    return out


def drawn_quantities(seed=0):
    """Quantity heads with distinct, non-trivial values, so a mis-gathered item index shows up."""
    rng = np.random.default_rng(seed)
    hi = P.MAX_QTY - 1
    return (rng.integers(1, hi, len(PRODUCTS)),
            rng.integers(1, hi, len(PRODUCTS)),
            rng.integers(1, hi, len(CROPS)))


def sim_slots(vocab, tables, index, qty_sell, qty_bp, qty_bs):
    """Run one bundle through `to_sim_actions` and read its explicit order list back."""
    def head(vec, width):
        return jnp.asarray(np.broadcast_to(np.asarray(vec)[None, :], (2, width)), dtype=jnp.int32)

    actions = {
        "op": jnp.zeros((2, J.MAX_UNITS), dtype=jnp.int32),
        "crop": jnp.zeros((2, J.MAX_UNITS), dtype=jnp.int32),
        "item": jnp.zeros((2, J.MAX_UNITS), dtype=jnp.int32),
        "qty": jnp.zeros((2, J.MAX_UNITS), dtype=jnp.int32),
        "bundle": jnp.full((2,), index, dtype=jnp.int32),
        "qty_sell": head(qty_sell, len(PRODUCTS)),
        "qty_buy_product": head(qty_bp, len(PRODUCTS)),
        "qty_buy_seed": head(qty_bs, len(CROPS)),
    }
    sim = A.to_sim_actions(actions, 1, tables)
    assert sim.order_op is not None, (
        "to_sim_actions left order_op unset, so `_order_book` falls back to the canonical layout "
        "and the sim plays a different sequence from the one the agent sends the environment")
    op = np.asarray(sim.order_op)[0, 0]
    item = np.asarray(sim.order_item)[0, 0]
    qty = np.asarray(sim.order_qty)[0, 0]
    return [(int(a), int(b), int(c)) for a, b, c in zip(op, item, qty) if int(a) != G.ORDER_NONE]


@pytest.fixture(scope="module", params=VOCAB_FILES)
def live(request):
    import pathlib
    if not pathlib.Path(request.param).exists():
        pytest.skip("no vocabulary at %s" % request.param)
    vocab = MB.load_vocab(request.param)
    tables = {k: jnp.asarray(v) for k, v in MB.tables(vocab, pad_to=P.N_BUNDLES).items()}
    return vocab, tables


def test_the_opening_goes_out_hires_first(live):
    """The one turn we know the answer to by measurement. HIRE must precede BUY_PRODUCT."""
    vocab, tables = live
    opening = MB.bundle_of([["HIRE"]] * 5 + [["BUY_ANIMAL", "COW", 2], ["BUY_ANIMAL", "SHEEP", 2],
                                             ["BUY_SEED", "WHEAT", 7], ["BUY_SEED", "MELON", 12],
                                             ["BUY_PRODUCT", "WHEAT", 6]])
    index = vocab.index(opening)
    if index == 0:
        pytest.skip("this vocabulary does not contain the teacher's opening")

    ops = [op for op, _, _ in sim_slots(vocab, tables, index, *drawn_quantities())]
    assert G.ORDER_HIRE in ops and G.ORDER_BUY_PRODUCT in ops
    assert ops.index(G.ORDER_HIRE) < ops.index(G.ORDER_BUY_PRODUCT), (
        "buying the wheat product before the hires fills the last shed slot with wheat and costs a "
        "whole sheep -- measured on the real environment, bank 484 against the tape's 13")


def test_every_live_bundle_decodes_to_the_same_sequence_in_both_paths(live):
    """The property test. `to_sim_actions` and `orders_from_heads` must agree for every bundle."""
    vocab, tables = live
    qty_sell, qty_bp, qty_bs = drawn_quantities()

    bad = []
    for i in range(vocab.size):
        want = as_slots(MB.orders_from_heads(vocab, i, qty_sell, qty_bp, qty_bs,
                                             PRODUCTS, CROPS, ANIMALS))[:G.MAX_ORDERS]
        got = sim_slots(vocab, tables, i, qty_sell, qty_bp, qty_bs)
        if got != want:
            bad.append((i, vocab.bundle(i), got, want))
    assert not bad, "%d of %d bundles disagree, e.g.\n  bundle %r\n  sim %r\n  env %r" % (
        len(bad), vocab.size, bad[0][1], bad[0][2], bad[0][3])


def test_a_padding_index_sends_nothing(live):
    """Padding rows must decode to an empty list, not to the highest real bundle.

    JAX clamps an out-of-range gather under jit rather than raising, so this is the difference
    between "no orders" and "somebody else's orders, emitted confidently".
    """
    vocab, tables = live
    assert vocab.size < P.N_BUNDLES, "no padding rows to test"
    assert sim_slots(vocab, tables, P.N_BUNDLES - 1, *drawn_quantities()) == []


def test_the_empty_bundle_sends_nothing(live):
    vocab, tables = live
    assert sim_slots(vocab, tables, 0, *drawn_quantities()) == []


def test_both_simulators_lay_an_explicit_list_out_the_same_way(live):
    """The composition check: `game._order_book` and `jax_sim._order_book` must agree.

    They are separate implementations of the same compaction -- one numpy with `nonzero`, one
    branchless under jit with a scatter into a scratch column. The 300-episode parity gate cannot
    reach either explicit branch, because `parity.random_script` has no way to express an order
    SEQUENCE: it emits per-kind dicts and lets `_order_book` choose the layout. So this is the only
    thing standing between the two.
    """
    from kagg.sim import jax_sim as JS
    from kagg.sim.game import Actions as NpActions

    vocab, tables = live
    qtys = drawn_quantities()

    bad = []
    for i in range(0, vocab.size, max(1, vocab.size // 40)):
        slots = sim_slots(vocab, tables, i, *qtys)
        np_act = NpActions(1, 2)
        for k, (op, item, qty) in enumerate(slots):
            np_act.order_op[0, 0, k] = op
            np_act.order_item[0, 0, k] = item
            np_act.order_qty[0, 0, k] = qty
        got_np = [tuple(int(v) for v in col) for col in np.stack(
            [np.asarray(x)[0, 0] for x in _np_order_book(np_act)], axis=-1)]

        jx = JS.Actions(**{f: jnp.zeros((1, 2, JS.MAX_UNITS), dtype=jnp.int32)
                           for f in ("unit_op", "unit_crop", "unit_item", "unit_qty")},
                        sell=jnp.zeros((1, 2, len(PRODUCTS)), dtype=jnp.int32),
                        buy_seed=jnp.zeros((1, 2, len(CROPS)), dtype=jnp.int32),
                        buy_product=jnp.zeros((1, 2, len(PRODUCTS)), dtype=jnp.int32),
                        buy_animal=jnp.zeros((1, 2, len(ANIMALS)), dtype=jnp.int32),
                        hire=jnp.zeros((1, 2), dtype=jnp.int32),
                        buy_land=jnp.zeros((1, 2), dtype=bool),
                        order_op=jnp.asarray(np_act.order_op, dtype=jnp.int32),
                        order_item=jnp.asarray(np_act.order_item, dtype=jnp.int32),
                        order_qty=jnp.asarray(np_act.order_qty, dtype=jnp.int32))
        got_jx = [tuple(int(v) for v in col) for col in np.stack(
            [np.asarray(x)[0, 0] for x in JS._order_book(jx)], axis=-1)]

        if got_np != got_jx:
            bad.append((i, got_np, got_jx))
    assert not bad, "%d bundles lay out differently in the two sims, e.g.\n  numpy %r\n  jax   %r" % (
        len(bad), bad[0][1], bad[0][2])


def _np_order_book(actions):
    from kagg.sim.game import Game
    return Game._order_book(Game(1, weed_chance=0.0), actions)
