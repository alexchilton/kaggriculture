"""A recorded opponent may only be given moves the board actually allows.

`ROLE_TAPE` pastes a downloaded player's recorded action into seat 1 by turn index. The tape is
TIME-indexed, not state-conditioned, so on a board that has drifted from the one it was recorded on
the recorded move is frequently illegal -- measured at **126 of 576 unit-ops, 22%**, on the
trainer's own staggered start states.

The simulator shrugs those off. The PPO update does not: it re-scores the stored action's
log-probability against the same legality mask the policy was sampled under, and an action the mask
forbids has probability exactly zero. `log(0)` is `-inf`, and the entropy term then evaluates
`0 * -inf`, which is `nan`. That killed run `bc40` on its first update:

    [0] ret +0.1076  ent 0.0 (op nan)  clip 0.000  kl +nan  seatL nan

The comment shipped alongside the role said an illegal recorded action "degrades toward a weaker
player rather than an illegal one", which is true of the SIMULATOR and false of the LOSS.

So the splice has to be masked per unit: where the tape's op is not legal for this unit on this
board, that unit keeps the policy's own action -- and its dependent heads (`crop`, `item`, `qty`)
have to come along with it, or the unit plays the policy's op with the tape's crop.
"""
import pathlib
import sys

import jax
import jax.numpy as jnp
import numpy as np
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

TAPES = REPO / "data/il/opponent_tape_actions.npz"
VOCAB = REPO / "data/il/bundle_vocab_teacher.json"

pytestmark = pytest.mark.skipif(
    not TAPES.exists() or not VOCAB.exists(),
    reason="needs data/il/opponent_tape_actions.npz and bundle_vocab_teacher.json")

BATCH = 24
UNIT_HEADS = ("op", "crop", "item", "qty")


def _trainer():
    """Import `scripts/train_jax_rl.py` as a module without running `main`."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("_train", REPO / "scripts/train_jax_rl.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_train"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def fixture():
    from kagg.rl import jax_act as A
    T = _trainer()
    T._set_vocab(str(VOCAB))
    state = T.staggered_states(BATCH, 12, seed=0)
    masks = A.masks_for(state, T._bundle_sells())
    npz = np.load(TAPES)
    tape = {k: jnp.asarray(npz[k]) for k in npz.files
            if k != "names" and not k.startswith("w_")}
    return T, A, state, masks, tape


def _picked(T, state, tape):
    """The recorded action each game would be handed this turn."""
    ids = jnp.arange(BATCH) % tape["op"].shape[0]
    idx = jnp.clip(state.step_index, 0, tape["op"].shape[1] - 1)
    return {h: t[ids, idx] for h, t in tape.items()}


def _mine(masks, n_units, marker=0):
    """A stand-in for the policy's own action: the first LEGAL op for every unit.

    Legal for every row by construction, so any illegal op in a spliced result came from the tape
    and nowhere else. `marker` fills the dependent heads so a test can see which side supplied them.
    """
    return {
        "op": jnp.argmax(masks["op"], axis=-1).astype(jnp.int32),
        "crop": jnp.full((BATCH * 2, n_units), marker, jnp.int32),
        "item": jnp.full((BATCH * 2, n_units), marker, jnp.int32),
        "qty": jnp.full((BATCH * 2, n_units), marker, jnp.int32),
        "bundle": jnp.zeros((BATCH * 2,), jnp.int32),
        "qty_sell": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_product": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_seed": jnp.zeros((BATCH * 2, 5), jnp.int32),
    }


def test_the_recorded_move_is_often_illegal_which_is_why_this_matters(fixture):
    """The premise. If this ever reads 0, the masking below is untested by construction."""
    T, A, state, masks, tape = fixture
    picked = _picked(T, state, tape)
    m_op = A._unflat(masks["op"], BATCH)[:, 1]                 # [B, units, ops], seat 1
    legal = jnp.take_along_axis(m_op, picked["op"][..., None], axis=-1)[..., 0]
    illegal = int((~legal).sum())
    assert illegal > 0, "no illegal recorded ops on this draw; the fix cannot be exercised"


def test_no_illegal_op_survives_the_splice(fixture):
    """After splicing, every seat-1 unit-op must be legal on its own board."""
    T, A, state, masks, tape = fixture
    picked = _picked(T, state, tape)

    n_units = masks["op"].shape[1]
    # Stand-in for the policy: the first legal op for each unit. Legal for every row by
    # construction, so any illegal op in the result came from the tape.
    mine = {
        "op": jnp.argmax(masks["op"], axis=-1).astype(jnp.int32),
        "crop": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "item": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "qty": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "bundle": jnp.zeros((BATCH * 2,), jnp.int32),
        "qty_sell": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_product": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_seed": jnp.zeros((BATCH * 2, 5), jnp.int32),
    }
    use_tape = jnp.ones((BATCH,), bool)                        # every game faces a tape

    out = T.splice_tape_actions(mine, picked, masks, BATCH, use_tape)

    m_op = A._unflat(masks["op"], BATCH)
    chosen = A._unflat(out["op"], BATCH)
    legal = jnp.take_along_axis(m_op, chosen[..., None], axis=-1)[..., 0]
    bad = int((~legal).sum())
    assert bad == 0, f"{bad} spliced unit-ops are illegal on their board"


def test_a_unit_that_keeps_its_own_op_keeps_its_own_crop(fixture):
    """`crop`, `item` and `qty` are read only for the op that was chosen.

    Splicing them independently of `op` would have a unit play the policy's PLANT with the tape's
    crop -- a combination neither side chose.
    """
    T, A, state, masks, tape = fixture
    picked = _picked(T, state, tape)
    n_units = masks["op"].shape[1]

    marker = 7
    mine = {
        "op": jnp.argmax(masks["op"], axis=-1).astype(jnp.int32),
        "crop": jnp.full((BATCH * 2, n_units), marker, jnp.int32),
        "item": jnp.full((BATCH * 2, n_units), marker, jnp.int32),
        "qty": jnp.full((BATCH * 2, n_units), marker, jnp.int32),
        "bundle": jnp.zeros((BATCH * 2,), jnp.int32),
        "qty_sell": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_product": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_seed": jnp.zeros((BATCH * 2, 5), jnp.int32),
    }
    use_tape = jnp.ones((BATCH,), bool)
    out = T.splice_tape_actions(mine, picked, masks, BATCH, use_tape)

    m_op = A._unflat(masks["op"], BATCH)[:, 1]
    kept = ~jnp.take_along_axis(m_op, picked["op"][..., None], axis=-1)[..., 0]   # tape refused
    if int(kept.sum()) == 0:
        pytest.skip("no refused units on this draw")
    crop = A._unflat(out["crop"], BATCH)[:, 1]
    assert int((crop[kept] != marker).sum()) == 0, \
        "a unit that kept the policy's op was given the tape's crop"


def test_seat_zero_is_never_touched(fixture):
    """The tape plays seat 1. Seat 0 is the policy under training and must be untouched."""
    T, A, state, masks, tape = fixture
    picked = _picked(T, state, tape)
    n_units = masks["op"].shape[1]
    mine = {
        "op": jnp.argmax(masks["op"], axis=-1).astype(jnp.int32),
        "crop": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "item": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "qty": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "bundle": jnp.zeros((BATCH * 2,), jnp.int32),
        "qty_sell": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_product": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_seed": jnp.zeros((BATCH * 2, 5), jnp.int32),
    }
    use_tape = jnp.ones((BATCH,), bool)
    out = T.splice_tape_actions(mine, picked, masks, BATCH, use_tape)
    for head in mine:
        before = A._unflat(mine[head], BATCH)[:, 0]
        after = A._unflat(out[head], BATCH)[:, 0]
        assert bool(jnp.all(before == after)), f"seat 0's {head} was modified"


def test_a_game_with_no_tape_opponent_is_untouched(fixture):
    """`use_tape` False means self-play or a heuristic holds the seat; nothing may be spliced."""
    T, A, state, masks, tape = fixture
    picked = _picked(T, state, tape)
    n_units = masks["op"].shape[1]
    mine = {
        "op": jnp.argmax(masks["op"], axis=-1).astype(jnp.int32),
        "crop": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "item": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "qty": jnp.zeros((BATCH * 2, n_units), jnp.int32),
        "bundle": jnp.zeros((BATCH * 2,), jnp.int32),
        "qty_sell": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_product": jnp.zeros((BATCH * 2, 9), jnp.int32),
        "qty_buy_seed": jnp.zeros((BATCH * 2, 5), jnp.int32),
    }
    out = T.splice_tape_actions(mine, picked, masks, BATCH, jnp.zeros((BATCH,), bool))
    for head in mine:
        assert bool(jnp.all(out[head] == mine[head])), f"{head} changed with no tape seat"
