"""At d11 h0 on an unseen town, is the teacher's bundle MASKED, or just ranked second?

    python -u scripts/why_is_buy_land_dropped_at_turn_264.py --ckpt <path> --rng 777

THE TWO ANSWERS AND WHY THEY NEED DIFFERENT FIXES
-------------------------------------------------
The held-out replay drops exactly one order from one basket at turn 264:

    teacher  SELL MELON 12, SELL MILK 6, BUY_ANIMAL COW, BUY_ANIMAL SHEEP, BUY_LAND,
             HIRE x5, BUY_SEED STRAWBERRY 23
    student  the same basket with BUY_LAND missing

Both baskets are in the 164-entry vocabulary, so "the net cannot say it" is already ruled out.
That leaves two causes, and they are not the same problem:

    MASKED    `masks_for` marked the teacher's bundle illegal, so the argmax never considered it.
              Then this is not a learning failure at all -- the net is picking the best LEGAL
              bundle, and the bug is in the mask (or the bank really is short and the teacher's
              own recorded action is the thing that would have failed). Training does not touch it.

    RANKED    the bundle was legal and the net scored the no-land one higher. Then it IS a fitting
              gap, on a decision that is 1.0000 on all 64 trained towns -- a generalisation gap,
              which more epochs on the same towns cannot close and more towns (or RL) can.

Printed for the diverging turn: the mask bit and the logit for BOTH bundles, plus the top 5. The
teacher drives, so the board and the bank are the teacher's own -- any difference is the student's.
"""
import argparse
import importlib.util
import json
import pathlib
import pickle
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--rng", type=int, default=777)
    ap.add_argument("--turn", type=int, default=264)
    ap.add_argument("--episodes", type=int, default=6)
    args = ap.parse_args()

    from kaggle_environments import make

    from kagg.il import market_bundles as MB
    from kagg.il.tape_teacher import TapeTeacher
    from kagg.rl import adapter as AD, jax_act as A, jax_obs, jax_policy as P

    DT = _load("dagger_tape", REPO / "scripts/dagger_tape.py")

    ck = pickle.load(open(args.ckpt, "rb"))
    a = ck.get("args") or {}
    model = P.Policy(d_model=int(a.get("d_model", 128)), n_heads=int(a.get("heads", 4)),
                     n_layers=int(a.get("layers", 3)))
    params = ck["params"]
    vocab = MB.load_vocab(str(ck.get("vocab_path") or a.get("vocab")))
    bundle_ok = MB.valid_table(vocab, pad_to=P.N_BUNDLES)

    def key(entry):
        return json.dumps(sorted([list(o) for o in entry]))

    entries = list(vocab)
    by_key = {key(e): i for i, e in enumerate(entries)}

    rng = np.random.default_rng(args.rng)
    specs = DT.episode_specs(DT.tape_games(), DT.opponent_pool(0), 4, rng)

    print("ckpt %s   turn %d\n" % (args.ckpt, args.turn), flush=True)

    for spec in specs[: args.episodes]:
        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        seat = spec["seat"]
        teacher = TapeTeacher(seat)
        memo = AD.GameMemo()
        for turn in range(args.turn + 1):
            if env.done:
                break
            obs = env.state[seat].observation
            memo.observe(obs, step=turn)
            t_act = teacher.act(obs)
            if turn == args.turn:
                privates = [obs["private"] if p == seat else AD.agent_private_stub()
                            for p in range(2)]
                st = AD.state_from_obs(obs, privates, step=turn, memo=memo)
                t_, u_, g_ = jax_obs.encode(st)
                heads, _v = model.apply(params, A._flat(t_), A._flat(u_), A._flat(g_))
                logits = np.asarray(heads["bundle"]).reshape(-1)
                mask = np.asarray(A.masks_for(st, bundle_ok)["bundle"]).reshape(-1)

                t_basket = [[o[0], o[1] if len(o) > 1 else ""]
                            for o in (t_act.get("market") or [])]
                t_idx = by_key.get(key(t_basket))
                s_idx = int(np.argmax(np.where(mask, logits, -np.inf)))

                farm = (obs.get("farms") or [None, None])[seat] or {}
                print("=== %s seat %d   money $%s   tiles %s"
                      % (spec.get("name"), seat, format(int(farm.get("money") or 0), ","),
                         len(farm.get("tiles") or [])), flush=True)
                if t_idx is None:
                    print("  teacher basket is NOT IN THE VOCABULARY -- %s" % t_basket, flush=True)
                else:
                    print("  teacher bundle idx %-4d mask %-5s logit %+8.3f"
                          % (t_idx, bool(mask[t_idx]), logits[t_idx]), flush=True)
                print("  student bundle idx %-4d mask %-5s logit %+8.3f"
                      % (s_idx, bool(mask[s_idx]), logits[s_idx]), flush=True)
                if t_idx is not None:
                    verdict = ("MASKED -- the argmax never saw it; this is a mask question, "
                               "not a training one" if not mask[t_idx] else
                               "LEGAL but RANKED %+.3f BELOW the student's pick -- a fitting gap"
                               % (logits[t_idx] - logits[s_idx]))
                    print("  VERDICT  %s" % verdict, flush=True)
                order = np.argsort(np.where(mask, logits, -np.inf))[::-1][:5]
                print("  top 5 legal bundles:", flush=True)
                for i in order:
                    print("    %-4d %+8.3f  %s"
                          % (i, logits[i],
                             json.dumps([list(o) for o in entries[i]])[:150]
                             if i < len(entries) else "<pad>"), flush=True)
                print(flush=True)
                break
            pair = [None, None]
            pair[seat] = teacher.sendable(t_act, len(obs["farms"][seat].get("hands") or []))
            pair[1 - seat] = DT.opponent_action(
                spec, turn, len(obs["farms"][1 - seat].get("hands") or []))
            env.step(pair)


if __name__ == "__main__":
    main()
