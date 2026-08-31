"""The numpy net agent must emit what the jax net agent emits, turn for turn.

    python -u -m pytest tests/test_the_numpy_agent_plays_the_same_game.py -q

WHY THIS IS SEPARATE FROM THE THREE COMPONENT TESTS
---------------------------------------------------
`numpy_policy`, `numpy_obs` and `numpy_act` each have their own parity test and all three pass. That
is not enough, and this project holds the receipt: **136 component parity tests passed and a 200-step
end-to-end check passed while the simulator silently burned seeds on failed plants**, and the
719-step gate then failed 40/40. Components verify components; only composition verifies
composition.

The specific things only this test can catch: the seat row picked out of the flattened batch, the
conditioning applied before or after masking, the argmax taken over the wrong axis, `n_units`
counted off the wrong farm, the vocabulary resolved from a different file than the mask table, and
`_uncap_sells` reading a shed that is not ours. Every one of those leaves all three component tests
green.

WHAT IS ASSERTED
----------------
The action dict itself -- `farmer`, `hands`, `market` -- compared exactly at every turn of a real
game, because the action dict is the only thing the environment ever sees. Not the logits, not the
argmaxes: those are means, and a difference in them that never reaches an action does not matter,
while a difference that does is visible here.

The net drives BOTH seats' decisions in the sense that matters -- it is asked for an action every
turn -- but the game is stepped with the same actions for both paths, so the two walk an identical
board and any divergence is the agent's, not the board's.

`test_the_agent_does_something` is the anti-vacuity guard, and it is not decoration: this net's
measured failure mode is emitting nothing at all -- a previous checkpoint banked exactly its $3,000
start because greedy argmax over per-head marginals picked "do nothing" on every product on every
turn. Two agents that both emit `PASS` and no orders agree perfectly and prove nothing.
"""
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

CKPT = REPO / "data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl"
TURNS = 24 * 4


def _norm(action):
    """The action dict in a form two implementations can be compared on."""
    return {
        "farmer": [str(x) for x in (action.get("farmer") or [])],
        "hands": [[str(x) for x in (h or [])] for h in (action.get("hands") or [])],
        "market": [[str(x) for x in (o or [])] for o in (action.get("market") or [])],
    }


def _walk(turns=TURNS, seed=9000):
    from kaggle_environments import make

    if not CKPT.exists():
        pytest.skip("%s not on disk" % CKPT)

    from kagg.agents import neural as JN, numpy_neural as NN

    jax_agent = JN.make_agent(str(CKPT))
    np_agent = NN.make_agent(str(CKPT))

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    out = []
    for turn in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        j_raw = jax_agent(obs)
        out.append((turn, _norm(j_raw), _norm(np_agent(obs))))
        # **Stepped with the jax action itself, not a rebuilt copy of it.** Both agents are asked
        # for the same board, so any divergence below is theirs rather than an accumulated
        # difference in the game -- and reconstructing an action from `_norm`'s stringified form
        # is a third representation with its own bugs. The first version did that and died on
        # `["HIRE"]`, a one-element order, while both agents were behaving correctly.
        env.step([j_raw, {"farmer": ["PASS"], "hands": [], "market": []}])
    return out


@pytest.fixture(scope="module")
def walked():
    return _walk()


def test_the_two_agents_emit_the_same_action(walked):
    assert walked, "no turns were played"
    for turn, j, n in walked:
        for key in ("farmer", "hands", "market"):
            assert j[key] == n[key], (
                "turn %d, %r differs.\n  jax   %r\n  numpy %r\n"
                "Three component parity tests can be green while the composition is wrong -- the "
                "seat row, the conditioning order, the argmax axis, `n_units`, or the vocabulary."
                % (turn, key, j[key], n[key]))


def test_the_agent_does_something(walked):
    """Two agents that both do nothing agree perfectly and prove nothing.

    This net's measured failure mode is exactly that: a checkpoint that banked its $3,000 start
    because greedy argmax picked "do nothing" on every product on every turn.
    """
    ops = {tuple(a) for _t, _j, n in walked
           for a in [n["farmer"]] + n["hands"]}
    orders = sum(len(n["market"]) for _t, _j, n in walked)
    non_pass = {o for o in ops if o and o[0] != "PASS"}

    assert non_pass, (
        "every unit action across %d turns was PASS. The comparison above is between two agents "
        "that do nothing." % len(walked))
    assert orders > 0, (
        "no market order was emitted across %d turns, so the whole market half of the decode -- "
        "bundle, the three quantity heads, `_uncap_sells` -- is untested here." % len(walked))
