"""The numpy forward pass must produce what flax produces, on real boards.

    python -u -m pytest tests/test_the_numpy_net_matches_the_flax_net.py -q

WHY THIS IS THE WHOLE POINT
---------------------------
`kagg/rl/numpy_policy.py` exists so a trained net can ship: the competition runtime has never had
jax or flax, and every artifact shipped so far imports only the standard library, numpy and
`kaggle_environments`. But a second implementation of a network is a thing that must agree with the
first one forever, and this project has already paid for that exact mistake once -- the two
observation encoders disagreed on 23 dead unit slots, silently, for weeks, and it changed the live
farmer's chosen op.

So the equality is pinned here, on boards from a real game rather than on random arrays: random
inputs would not exercise the feature scales the net was fitted on, and a disagreement that only
appears at realistic magnitudes is exactly the kind that survives a synthetic test.

WHAT IS ASSERTED, and why both
------------------------------
    argmax identical      what actually gets played. A logit difference that never changes an
                          argmax cannot change a game.
    logits close          the early-warning. Argmaxes can agree while the representation drifts,
                          and the drift is what eventually flips one.

`gelu` is the likeliest place for this to go wrong: `nn.gelu` defaults to the tanh approximation and
the erf form differs by up to ~1e-3 per unit, which three residual layers will amplify.
"""
import pathlib
import pickle
import sys

import numpy as np
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

CKPT = REPO / "data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl"


def _real_boards(n_turns=8):
    """Encoded features from a real game, so the magnitudes are the ones the net was fitted on."""
    from kaggle_environments import make

    from kagg.rl import adapter as AD, jax_act as A, jax_obs

    env = make("kaggriculture", configuration={"seed": 9000, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    ts, us, gs = [], [], []
    memo = AD.GameMemo()
    for turn in range(n_turns):
        if env.done:
            break
        obs = env.state[0].observation
        memo.observe(obs, step=turn)
        privates = [obs["private"] if p == 0 else AD.agent_private_stub() for p in range(2)]
        state = AD.state_from_obs(obs, privates, step=turn, memo=memo)
        t, u, g = jax_obs.encode(state)
        ts.append(np.asarray(A._flat(t))[0])
        us.append(np.asarray(A._flat(u))[0])
        gs.append(np.asarray(A._flat(g))[0])
        env.step([{"farmer": ["PASS"], "hands": [], "market": []}] * 2)
    return np.stack(ts), np.stack(us), np.stack(gs)


def _both():
    import jax
    import jax.numpy as jnp

    from kagg.rl import jax_obs, jax_policy as P, numpy_policy as NP

    if not CKPT.exists():
        pytest.skip(f"{CKPT} not on disk")
    ck = pickle.load(open(CKPT, "rb"))
    a = ck.get("args") or {}
    n_layers = a.get("layers", 3)
    model = P.Policy(d_model=a.get("d_model", 128), n_heads=a.get("heads", 4), n_layers=n_layers)

    tiles, units, glob = _real_boards()
    # The checkpoint predates the latch/shop features, so migrate it into the current width the same
    # way play does -- zero-padded rows, which contribute nothing.
    template = model.init(jax.random.PRNGKey(0),
                          jnp.zeros((1, tiles.shape[1], jax_obs.TILE_FEATURES), jnp.float32),
                          jnp.zeros((1, units.shape[1], jax_obs.UNIT_FEATURES), jnp.float32),
                          jnp.zeros((1, jax_obs.GLOBAL_FEATURES), jnp.float32))
    params = P.load_or_migrate(ck["params"], template)

    flax_heads, flax_v = model.apply(params, jnp.asarray(tiles), jnp.asarray(units),
                                     jnp.asarray(glob))
    np_heads, np_v = NP.apply(NP.pack(params), tiles, units, glob, n_layers=n_layers)
    return flax_heads, np.asarray(flax_v), np_heads, np_v


def test_every_head_picks_the_same_action():
    """The one that decides games."""
    flax_heads, _fv, np_heads, _nv = _both()
    assert set(flax_heads) == set(np_heads), (
        "head names differ: flax %s, numpy %s" % (sorted(flax_heads), sorted(np_heads)))
    for name in sorted(flax_heads):
        a = np.asarray(flax_heads[name])
        b = np.asarray(np_heads[name])
        assert a.shape == b.shape, f"{name}: flax {a.shape} vs numpy {b.shape}"
        same = a.argmax(-1) == b.argmax(-1)
        assert same.all(), (
            "%s: %d of %d argmaxes differ. A submission built on this numpy pass would play a "
            "different game from the checkpoint it was trained as."
            % (name, int((~same).sum()), same.size))


def test_the_logits_match_closely():
    """The early warning: argmaxes can agree while the representation drifts."""
    flax_heads, _fv, np_heads, _nv = _both()
    worst, where = 0.0, None
    for name in sorted(flax_heads):
        a = np.asarray(flax_heads[name], dtype=np.float64)
        b = np.asarray(np_heads[name], dtype=np.float64)
        d = float(np.abs(a - b).max())
        if d > worst:
            worst, where = d, name
    assert worst < 2e-3, (
        "largest logit difference %.3g, on head %r. Check `gelu` (tanh vs erf), the LayerNorm "
        "epsilon, and whether the attention scale is applied to the query or to the logits."
        % (worst, where))


def test_the_value_head_matches():
    _fh, flax_v, _nh, np_v = _both()
    assert flax_v.shape == np_v.shape, f"flax {flax_v.shape} vs numpy {np_v.shape}"
    assert np.abs(flax_v - np_v).max() < 1e-4, (
        "value differs by %.3g; the sigmoid or the margin rescale is wrong"
        % float(np.abs(flax_v - np_v).max()))
