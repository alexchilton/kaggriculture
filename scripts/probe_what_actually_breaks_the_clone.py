"""The start board is IDENTICAL on every recording. So what breaks the clone off its tape?

    python -u scripts/probe_what_actually_breaks_the_clone.py

Alex, 2026-08-27: *"dude the boards are identical!!! the only difference is the shops"* -- and
`project_kaggriculture_start_state_is_fixed` records exactly that: all 78 replays start with the same
board, NW only, $3,000 and no shops. Only the OPPONENT, the SHOP UNLOCK TIMING and WEEDS vary.

So "it does not transplant to a foreign board" was never a real explanation for the clone banking $0
on seeds 9000-9007. There is no foreign board. Exactly three things change, and this measures them
ONE AT A TIME against the tape's own configuration:

    base     the tape's own cfg, weeds 0.0, recorded opponent      -> the known-good number
    weeds    the tape's own cfg with weedSpawnChance 0.005
    opp      the tape's own cfg, weeds 0.0, a different opponent
    seed     a foreign seed (so a different SHOP DRAW), weeds 0.0, recorded opponent

Two changes at once produced a confounded verdict on `DEPOT_RING_FIRST` in this repo and it read as a
win until isolated. One delta per arm, and the base is re-run rather than quoted.

The vocabulary is selected by COUNT against `ckpt["vocab_size"]`, never by the stored path: the
checkpoint names `bundle_vocab_teacher.json`, which was topped up from 149 to 151 bundles AFTER the
round-27 pin, and loading it silently shifts every index above the addition.
"""
import argparse
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def load_submission(path):
    ns = {}
    p = pathlib.Path(path)
    exec(compile(p.read_text(), str(p), "exec"), ns)
    return [v for v in ns.values() if callable(v)][-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="data/dagger_tape/season_fast-20260822-235031")
    ap.add_argument("--ckpt", default="pinned_round27.pkl")
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--tapes", type=int, default=2)
    ap.add_argument("--foreign-seed", type=int, default=9000)
    ap.add_argument("--opponent", default=None,
                    help="a generated submission .py to use as the 'opp' arm")
    args = ap.parse_args()

    import pickle

    import dagger_tape as DT
    import jax.numpy as jnp
    from kagg.agents import neural as NEURAL
    from kagg.il import market_bundles as MB
    from kagg.rl import adapter as AD, jax_act as A, jax_obs, jax_policy as P
    from kaggle_environments import make

    run = pathlib.Path(args.run)
    with (run / args.ckpt).open("rb") as fh:
        ckpt = pickle.load(fh)
    params, cargs = ckpt["params"], ckpt.get("args") or {}
    want = ckpt.get("vocab_size")

    vocab_path = None
    for c in (cargs.get("vocab"),
              str(REPO / "data/il/bundle_vocab_teacher_pre_topup.json"),
              str(REPO / "data/il/bundle_vocab_teacher.json"),
              str(REPO / "data/il/bundle_vocab.json")):
        if c and pathlib.Path(c).exists() and len(json.loads(pathlib.Path(c).read_text())) == want:
            vocab_path = c
            break
    if vocab_path is None:
        raise SystemExit(f"no vocabulary on disk holds {want} bundles")
    print(f"{run.name}/{args.ckpt} round {ckpt.get('round')}  vocab {pathlib.Path(vocab_path).name}"
          f" ({want} bundles)")

    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(p) for p in b) for b in json.loads(pathlib.Path(vocab_path).read_text())],
        max_size=P.N_BUNDLES)
    bundle_ok = jnp.asarray(MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    model = P.Policy(d_model=cargs.get("d_model", 128), n_heads=cargs.get("heads", 4),
                     n_layers=cargs.get("layers", 3))

    other = load_submission(args.opponent) if args.opponent else None

    def play(cfg, seat, opponent_stream, opponent_fn):
        env = make("kaggriculture", configuration=cfg, debug=False)
        env.reset(2)
        for turn in range(args.horizon):
            if env.done:
                break
            obs = env.state[seat].observation
            privates = [obs["private"] if p == seat else AD.agent_private_stub()
                        for p in range(2)]
            st = AD.state_from_obs(obs, privates, step=turn)
            tiles, units, glob = jax_obs.encode(st)
            heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
            greedy = DT.greedy_action(heads, masks=A.masks_for(st, bundle_ok))
            n_units = 1 + len(obs["farms"][seat].get("hands") or [])
            act = NEURAL.decode_action(greedy, n_units, vocab, seat=seat)
            if opponent_fn is not None:
                opp = opponent_fn(env.state[1 - seat].observation, None)
            else:
                opp = (opponent_stream[turn] if turn < len(opponent_stream) else {})
            env.step([act if p == seat else opp for p in range(2)])
        return int((env.state[0].observation["farms"][seat] or {}).get("money") or 0)

    print(f"\n{'tape':<16}{'base':>12}{'weeds .005':>13}{'other opp':>12}"
          f"{'seed ' + str(args.foreign_seed):>13}")
    for spec in DT.tape_games()[: args.tapes]:
        seat, opp = spec["seat"], spec["opponent"]
        base_cfg = dict(spec["cfg"])

        b = play(base_cfg, seat, opp, None)

        w = dict(base_cfg)
        w["weedSpawnChance"] = 0.005
        wv = play(w, seat, opp, None)

        ov = play(base_cfg, seat, opp, other) if other else None

        s = dict(base_cfg)
        s["seed"] = args.foreign_seed
        sv = play(s, seat, opp, None)

        print(f"{spec['name'][:15]:<16}{b:>12,}{wv:>13,}"
              f"{('n/a' if ov is None else f'{ov:,}'):>12}{sv:>13,}")


main()
