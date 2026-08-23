"""A teacher label the mask forbids must be taught as NOOP, not as the forbidden op.

`kagg/il/replays.py:38` already claims this happens:

    Ops the replay can contain that the simulator folds into NOOP (PASS, and anything illegal)
    map to NOOP, which is what the simulator would have done anyway.

The table underneath maps only `"PASS": O.NOOP`. `"DIG": O.DIG` is unconditional, and
`encode_action` never sees the board, so nothing tests legality. The comment describes an intent
the code does not implement -- the exact failure CLAUDE.md names as "reasoning from a comment
instead of from the code".

The consequence, measured 2026-08-23 over the four tapes, full season:

    104 DIG labels, 97 legal, 7 on an already-empty tile

`reference/kaggriculture.py:484` returns immediately when `tile is None`, so those 7 are no-ops the
reference silently ignores. The mask is right to forbid them. But encoding them as `O.DIG` makes
them unlearnable twice over: `greedy_action` argmaxes over `_masked_logits` so the op carries
`-1e9`, and `bc.py:232` gives an illegal label weight zero. DIG's ceiling is therefore `97/104 =
0.933`, and the converged net sits at exactly `0.933`. No amount of training moves it.

What it costs is not the agreement number, it is what the net emits instead. Round 27, greedy
decode, full season, first pure model error on each tape -- every one of them a DIG:

    tape          on-tape    off-tape       gap   substitute
    92498144      150,316     149,599      -717   PLANT   (in place, hand stays)
    91906088      128,471     126,541    -1,930   SOUTH   (hand walks off)
    91907974       88,882      46,839   -42,043   WEST    (hand walks off)
    92466371      147,036         372  -146,664   PLANT

Teaching NOOP instead reproduces what the reference actually did: nothing, with the hand in place.
"""

import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from kagg.il import market_bundles as MB                          # noqa: E402

# Turn 297 is the first forbidden DIG on tape 92498144; 327 and 331 land on 92466371.
HORIZON = 340


@pytest.mark.slow
def test_no_label_the_trainer_produces_is_forbidden_by_the_mask():
    """RED before the fold: 3 DIG labels inside 340 turns are unemittable and unteachable.

    Goes through `RP.encode_action_legal`, the same call `dagger_tape` makes, so this covers the
    path that actually trains rather than a re-implementation of it.
    """
    import numpy as np
    from kaggle_environments import make

    import dagger_tape as DT
    from kagg.il import replays as RP
    from kagg.il.tape_teacher import TapeTeacher
    from kagg.rl import adapter as AD, jax_act as A

    vocab = MB.load_vocab(str(REPO / "data/il/bundle_vocab_teacher.json"))
    bundle_ok = MB.valid_table(vocab)
    op_name = {v: k for k, v in RP.OP_CODE.items()}

    offenders = []
    for spec in DT.tape_games():
        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        seat = spec["seat"]
        teacher = TapeTeacher(seat)

        for turn in range(HORIZON):
            if env.done:
                break
            obs = env.state[seat].observation
            action = teacher.act(obs)
            privates = [obs["private"] if p == seat else AD.agent_private_stub()
                        for p in range(2)]
            sim_state = AD.state_from_obs(obs, privates, step=turn)
            masks = A.masks_for(sim_state, bundle_ok)
            op_mask = RP.seat_op_mask(masks, seat)

            n_units = 1 + len(obs["farms"][seat].get("hands") or [])
            labels = RP.encode_action_legal(action, n_units, vocab, op_mask)

            for u in range(n_units):
                code = int(np.asarray(labels["op"])[u])
                if not bool(op_mask[u, code]):
                    offenders.append("turn %d day %d unit %d op %s"
                                     % (turn, turn // 24, u, op_name.get(code, code)))

            env.step([action if p == seat else (spec["opponent"][turn]
                                                if turn < len(spec["opponent"]) else {})
                      for p in range(2)])

    assert not offenders, (
        "the trainer is producing labels the mask forbids, so they are zero-weighted in the loss "
        "and carry -1e9 at decode: %s" % offenders[:6])
