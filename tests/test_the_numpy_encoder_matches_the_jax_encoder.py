"""The numpy observation path must produce what the jax one produces, on real boards.

    python -u -m pytest tests/test_the_numpy_encoder_matches_the_jax_encoder.py -q

WHY THIS IS THE WHOLE POINT
---------------------------
`kagg/rl/numpy_obs.py` exists so a trained net can ship: the competition runtime has never had jax
or flax. But `adapter.py`'s own docstring argues AGAINST a second encoder, and it is right on the
merits -- this project has already paid for exactly this pair. The two encoders that existed
disagreed on 23 dead unit slots, silently, for weeks, and on one board with one set of weights the
LIVE farmer's chosen op came out 1 through `jax_sim` and 17 through the adapter.

The 300/300 fast-sim parity gate does not cover it: that tests the SIMULATOR against the reference,
not the ENCODER. This is the only thing that does.

WHAT IS ASSERTED
----------------
Exact equality of `tiles`, `units` and `glob` at every turn of a real game, both seats -- not
`allclose`. Both paths do the same float32 arithmetic in the same order, so anything other than
equality means an operation differs, and a tolerance would hide the case that differs by a little
today and by a lot on a board this game did not reach.

**THE SHIPPED AGENT DRIVES THE GAME, AND THAT IS THE WHOLE VALUE OF THIS FILE.**

The first version had both seats send `PASS` every turn, on the reasoning that the encoder is a pure
function of the state so any state would do. It passed -- and it passed just as happily with
`pending_care_bonus` scaled by 4.5 instead of 4.0, a real defect introduced deliberately to check.
On an all-PASS board nothing is planted, no animal is placed, no unit leaves spawn and the shed
stays empty, so most tile and unit columns are structurally zero and comparing them compares 0.0 to
0.0. That is this project's standing lesson -- a gate only tests what it exercises -- and 136
component parity tests once passed the same way while the simulator burned seeds.

So seat 0 plays the real agent, in the configuration that ships. That fills the columns an all-PASS
game cannot reach: crops with an age and a yield, animals with a placement day and a feed clock,
units away from spawn carrying items, money moving, and the `_target` geometry pointing at jobs that
exist.

Three tests, and the two supporting ones are not decoration:

    test_the_two_encoders_agree      the claim.
    test_the_board_is_not_empty      that the claim was made about a board with something on it.
                                     The day this goes quiet is the day the claim stops being
                                     evidence, and nothing else would say so.
    test_a_deliberate_defect_is_ca.. that the comparison can fail at all. This is the project's
                                     revert-and-confirm-red step, kept as a test rather than done
                                     once by hand: a green suite after a fix says the fix broke
                                     nothing, not that anything checks it.
"""
import pathlib
import sys
import types

import numpy as np
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

SOURCE = REPO / "kagg/rl/numpy_obs.py"

#: Far enough in that the day-1 and day-3 snapshots have latched, a shop slot has opened (the town
#: opens one at the end of every third day), animals are placed and crops have reached a yield.
TURNS = 24 * 7


def _walk(turns=TURNS, seed=9000):
    """One real game, encoded both ways. `[(turn, jax_out, numpy_out, numpy_state)]`."""
    from kaggle_environments import make

    from kagg import plan as PLAN
    from kagg.rl import adapter as AD, jax_obs, numpy_obs as NO
    from kagg.search import schedule_agent as SA

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

        st = NO.state_from_obs(obs, privates, step=turn, memo=np_memo)
        j = jax_obs.encode(AD.state_from_obs(obs, privates, step=turn, memo=jax_memo))
        out.append((turn,
                    tuple(np.asarray(a) for a in j),
                    tuple(np.asarray(a) for a in NO.encode(st)),
                    st))

        env.step([agent(obs), {"farmer": ["PASS"], "hands": [], "market": []}])
    return out


@pytest.fixture(scope="module")
def walked():
    return _walk()


ARRAYS = [(0, "tiles"), (1, "units"), (2, "glob")]


@pytest.mark.parametrize("which,name", ARRAYS)
def test_the_two_encoders_agree(walked, which, name):
    assert walked, "no turns were played"
    for turn, j, n, _st in walked:
        a, b = j[which], n[which]
        assert a.shape == b.shape, (
            "turn %d, %s: jax %s vs numpy %s" % (turn, name, a.shape, b.shape))
        bad = np.argwhere(a != b)
        assert len(bad) == 0, (
            "turn %d, %s: %d of %d entries differ. First at index %s: jax %r, numpy %r. "
            "A submission built on the numpy path would show the net a different board from the "
            "one its checkpoint was fitted on."
            % (turn, name, len(bad), a.size, tuple(bad[0]),
               float(a[tuple(bad[0])]), float(b[tuple(bad[0])])))


def test_the_board_is_not_empty(walked):
    """The equality above is only evidence if the board it was measured on has something on it."""
    from kagg.rl import numpy_obs as NO

    plants = animals = carried = moved = 0
    money = set()
    for _turn, _j, _n, st in walked:
        t, f = st.tiles, st.farm
        plants += int((t.kind[0, 0] == NO.PLANT).sum())
        animals += int((t.animal[0, 0] != NO.NO_ANIMAL).sum())
        carried += int(f.carried[0, 0].sum())
        moved += int(f.n_units[0, 0] > 1)
        money.add(float(f.money[0, 0]))

    assert plants > 0, "no tile was ever planted; every crop column compared 0.0 against 0.0"
    assert animals > 0, (
        "no animal was ever placed; the placement age, the feed clock and the animal-interval "
        "feature all compared 0.0 against 0.0")
    assert carried > 0, "no unit ever carried anything; the `carried` block was all zeros"
    assert moved > 0, "the crew was never more than the farmer; 23 unit tokens stayed dead"
    assert len(money) > 1, "the bank never moved; every money-derived column was constant"


#: One edit per encoded array, each on a column the agent's own play makes non-zero. If any of these
#: stops being caught, the array it belongs to is no longer being exercised -- which is the failure
#: the all-PASS version of this file had, and which nothing else here would notice.
DEFECTS = [
    ("tiles", "(t.yield_units / 8.0)", "(t.yield_units / 8.5)"),
    ("units", "np.minimum(farm.carried / 10.0, 3.0)", "np.minimum(farm.carried / 10.5, 3.0)"),
    ("glob", "MONEY_SCALE = 50_000.0", "MONEY_SCALE = 50_001.0"),
]


def _mutant(old, new):
    """`numpy_obs` re-exec'd from source with one substitution. The file on disk is not touched."""
    src = SOURCE.read_text()
    assert src.count(old) == 1, (
        "%r appears %d times in %s; the defect test cannot target it unambiguously"
        % (old, src.count(old), SOURCE))
    mod = types.ModuleType("numpy_obs_mutant")
    mod.__file__ = str(SOURCE)
    exec(compile(src.replace(old, new), "numpy_obs_mutant", "exec"), mod.__dict__)
    return mod


@pytest.mark.parametrize("name,old,new", DEFECTS, ids=[d[0] for d in DEFECTS])
def test_a_deliberate_defect_is_caught(walked, name, old, new):
    which = dict((n, i) for i, n in ARRAYS)[name]
    mod = _mutant(old, new)
    for _turn, _j, _n, st in walked:
        if not np.array_equal(np.asarray(mod.encode(st)[which]), _n[which]):
            return
    pytest.fail(
        "%s -> %s changed nothing in `%s` across %d turns. The comparison in this file cannot fail "
        "on that column, so its agreement there is not evidence." % (old, new, name, len(walked)))
