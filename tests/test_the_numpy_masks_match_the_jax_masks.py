"""The numpy action path must produce what the jax one produces, on real boards.

    python -u -m pytest tests/test_the_numpy_masks_match_the_jax_masks.py -q

Third of the three ports that let a trained net ship, after the forward pass
(`test_the_numpy_net_matches_the_flax_net.py`) and the encoder
(`test_the_numpy_encoder_matches_the_jax_encoder.py`). Same standing as both: unrun, `numpy_act.py`
is a liability rather than an asset.

**A mask defect is the quietest kind this project has.** It emits no error and no NaN. A masked-out
op is simply never chosen, and the loss is zeroed on it too, so it never reaches a gradient either
-- the hand stranded at (5,5) read as `WEST 24/25 = 0.960` on the checkpoint while dragging
whole-season op agreement to ~0.78 once the net drove. The 300/300 parity gate cannot see any of
this: it tests the simulators against the reference, and the masks are RL-side only.

So the comparison is exact, per head, on every turn of a game the shipped agent drives -- and
`test_the_masks_are_not_all_true` exists because a mask that says "everything is legal" would match
trivially on a board with nothing on it, which is exactly how the encoder test passed while checking
nothing.

`test_the_constants_still_agree` pins the four numbers `numpy_act` restates rather than imports.
They are restated because importing `jax_policy` pulls flax into the submission; a silent drift
there would resize a head and mis-decode every action above the changed index.
"""
import pathlib
import sys

import numpy as np
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

TURNS = 24 * 5


def _walk(turns=TURNS, seed=9000):
    """One real game with the shipped agent driving; masks built both ways at every turn."""
    from kaggle_environments import make

    from kagg import plan as PLAN
    from kagg.il import market_bundles as MB
    from kagg.rl import adapter as AD, jax_act as A, jax_policy as P, numpy_act as NA, \
        numpy_obs as NO
    from kagg.search import schedule_agent as SA

    bundle_ok = MB.valid_table(MB.load_vocab(), pad_to=P.N_BUNDLES)
    agent = SA.make_agent(PLAN.load(), 0)
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    jax_memo, np_memo = AD.GameMemo(), NO.GameMemo()
    out = []
    for turn in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        jax_memo.observe(obs, step=turn)
        np_memo.observe(obs, step=turn)
        privates = [obs["private"] if p == 0 else AD.agent_private_stub() for p in range(2)]

        j = A.masks_for(AD.state_from_obs(obs, privates, step=turn, memo=jax_memo), bundle_ok)
        n = NA.masks_for(NO.state_from_obs(obs, privates, step=turn, memo=np_memo), bundle_ok)
        out.append((turn, {k: np.asarray(v) for k, v in j.items()}, n))

        env.step([agent(obs), {"farmer": ["PASS"], "hands": [], "market": []}])
    return out


@pytest.fixture(scope="module")
def walked():
    return _walk()


HEADS = ["op", "crop", "item", "qty", "bundle", "qty_sell", "qty_buy_product", "qty_buy_seed"]


def test_the_constants_still_agree():
    """`numpy_act` restates four numbers rather than importing flax. Pin them to the originals."""
    from kagg.rl import jax_act as A, jax_policy as P, numpy_act as NA

    assert NA.N_BUNDLES == int(P.N_BUNDLES)
    assert NA.MAX_QTY == int(P.MAX_QTY)
    assert list(NA.UNIT_QTY_BUCKETS) == [int(v) for v in P.UNIT_QTY_BUCKETS]
    assert NA.ALL_HEADS == A.ALL_HEADS
    assert NA.OP_CONDITIONED_HEADS == A.OP_CONDITIONED_HEADS
    assert NA.CONDITION_HEADS == A.CONDITION_HEADS


@pytest.mark.parametrize("head", HEADS)
def test_the_two_mask_builders_agree(walked, head):
    assert walked, "no turns were played"
    for turn, j, n in walked:
        a, b = j[head], n[head]
        assert a.shape == b.shape, (
            "turn %d, %s: jax %s vs numpy %s" % (turn, head, a.shape, b.shape))
        bad = np.argwhere(a != b)
        assert len(bad) == 0, (
            "turn %d, %s: %d of %d entries differ, first at %s (jax %s, numpy %s). A mask "
            "disagreement is silent -- the op is simply never chosen and never learned."
            % (turn, head, len(bad), a.size, tuple(bad[0]),
               bool(a[tuple(bad[0])]), bool(b[tuple(bad[0])])))


def test_the_masks_are_not_all_true(walked):
    """An all-permissive mask would match trivially and check nothing.

    `op` is the one that carries real structure; the market heads are all-ones by design and the
    bundle head is fixed padding, so they are excluded rather than asserted about.
    """
    from kagg.rl import numpy_act as NA

    seen_false = np.zeros(NA.N_POLICY_OPS, dtype=bool)
    seen_true = np.zeros(NA.N_POLICY_OPS, dtype=bool)
    for _turn, _j, n in walked:
        op = n["op"]
        seen_false |= (~op).any(axis=(0, 1))
        seen_true |= op.any(axis=(0, 1))

    both = seen_false & seen_true
    assert both.sum() >= 8, (
        "only %d of %d ops were ever both legal and illegal across the walk; the op mask is close "
        "to constant, so agreeing about it is not evidence. Legal-somewhere: %d, "
        "illegal-somewhere: %d." % (int(both.sum()), NA.N_POLICY_OPS,
                                    int(seen_true.sum()), int(seen_false.sum())))
