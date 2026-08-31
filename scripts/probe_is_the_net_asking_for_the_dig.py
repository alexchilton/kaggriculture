"""At the turns the teacher DIGs an empty tile, what does the net actually want?

    python -u scripts/probe_is_the_net_asking_for_the_dig.py

THE PREMISE THIS TESTS
----------------------
`jax_masks.py:125` allows DIG only on a weed, a plant or an empty structure:

    masks[O.DIG] = (kind == J.WEED) | is_plant | empty_structure

The reference ACCEPTS a DIG on an empty tile -- `reference/kaggriculture.py:484`, `if tile is None:
return` -- as a legal no-op that costs the unit its turn. So we forbid something the game permits.

Measured 2026-08-27 (`data/logs/corrections_all.log`, `corrections_market.log`): the teacher's DIG is
the FIRST divergence on three of four tapes, and what follows is not a mistake but a PHASE SHIFT --

    turn 297 teacher DIG               net PLANT STRAWBERRY
    turn 298 teacher PLANT STRAWBERRY  net WATER
    turn 299 teacher WATER             net SOUTH

the net emitting the teacher's NEXT action, one turn late, for the rest of the season. A tape with a
dropped frame. On `92466371` it never re-syncs: 23-24 corrections a day, every day, d14 to d29, and
the season ends at $372 against the teacher's $147,059.

The proposed fix -- emit PASS when DIG is the unmasked argmax but masked out -- is behaviourally
identical to the teacher's no-op and keeps the sequence aligned, with no retrain and no change to
`jax_masks.py` (which is RL-side and uncovered by the 300-episode parity gate).

**It only works if the net's unmasked first choice at those turns IS DIG.** If the mask is not what
displaces it, the fix is a null. So: at every turn the teacher DIGs, print the net's top-3 UNMASKED
classes and its top-3 masked ones. That is the whole question.
"""
import argparse
import collections
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="data/dagger_tape/season_fast-20260822-235031")
    ap.add_argument("--ckpt", default="pinned_round27.pkl")
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--tapes", type=int, default=4)
    args = ap.parse_args()

    import pickle

    import dagger_tape as DT
    import jax.numpy as jnp
    from kagg.il import market_bundles as MB
    from kagg.il import replays as RP
    from kagg.il.tape_teacher import TapeTeacher
    from kagg.rl import adapter as AD, jax_act as A, jax_obs, jax_policy as P
    from kaggle_environments import make

    run = pathlib.Path(args.run)
    with (run / args.ckpt).open("rb") as fh:
        ckpt = pickle.load(fh)
    params, cargs = ckpt["params"], ckpt.get("args") or {}
    want = ckpt.get("vocab_size")
    vpath = next(c for c in (cargs.get("vocab"),
                             str(REPO / "data/il/bundle_vocab_teacher_pre_topup.json"),
                             str(REPO / "data/il/bundle_vocab_teacher.json"))
                 if c and pathlib.Path(c).exists()
                 and len(json.loads(pathlib.Path(c).read_text())) == want)
    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(p) for p in b) for b in json.loads(pathlib.Path(vpath).read_text())],
        max_size=P.N_BUNDLES)
    bundle_ok = jnp.asarray(MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    model = P.Policy(d_model=cargs.get("d_model", 128), n_heads=cargs.get("heads", 4),
                     n_layers=cargs.get("layers", 3))
    name_of = {v: k for k, v in RP.OP_CODE.items()}
    dig_code = RP.OP_CODE["DIG"]

    print(f"{run.name}/{args.ckpt} round {ckpt.get('round')}   DIG op code {dig_code}")
    verdict = collections.Counter()
    for spec in DT.tape_games()[: args.tapes]:
        seat = spec["seat"]
        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        teacher = TapeTeacher(seat)
        print(f"\n{spec['name']}  seat {seat}")
        for turn in range(args.horizon):
            if env.done:
                break
            obs = env.state[seat].observation
            t_act = teacher.act(obs)
            privates = [obs["private"] if p == seat else AD.agent_private_stub()
                        for p in range(2)]
            st = AD.state_from_obs(obs, privates, step=turn)
            tiles, units, glob = jax_obs.encode(st)
            heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
            masks = A.masks_for(st, bundle_ok)
            n_units = 1 + len(obs["farms"][seat].get("hands") or [])
            labels = RP.encode_action(t_act, n_units, vocab=vocab)

            raw = np.asarray(heads["op"])[seat]
            msk = np.asarray(masks["op"])[seat]
            for u in range(n_units):
                if int(labels["op"][u]) != dig_code:
                    continue
                allowed = bool(msk[u][dig_code])
                free = np.argsort(-raw[u])[:3]
                mvals = np.where(msk[u], raw[u], -np.inf)
                held = np.argsort(-mvals)[:3]
                farm = obs["farms"][seat]
                pos = ([tuple(farm.get("farmer") or (0, 0))]
                       + [tuple(h) for h in (farm.get("hands") or [])])
                x, y = pos[u] if u < len(pos) else (-1, -1)
                tile = (farm.get("tiles") or [[]])[y][x] if 0 <= y < len(farm["tiles"]) else None
                key = ("DIG allowed" if allowed else
                       ("MASKED, net wants DIG" if int(free[0]) == dig_code
                        else "MASKED, net wants something else"))
                verdict[key] += 1
                print(f"  turn {turn:>3} d{turn // 24:>2} u{u:<2} at ({x},{y}) "
                      f"tile={'None' if tile is None else tile.get('kind')}  "
                      f"mask={'ok' if allowed else 'BLOCKED'}  "
                      f"unmasked top3 {[name_of.get(int(c), int(c)) for c in free]}  "
                      f"-> plays {name_of.get(int(held[0]), int(held[0]))}")
            env.step([t_act if p == seat else
                      (spec["opponent"][turn] if turn < len(spec["opponent"]) else {})
                      for p in range(2)])

    print("\nverdict")
    for k, v in verdict.most_common():
        print(f"  {k:<34} {v}")


main()
