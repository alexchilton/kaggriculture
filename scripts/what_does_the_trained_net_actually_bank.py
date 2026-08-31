"""Play a checkpoint over the training episodes and print the bank. The number agreement proxies.

    python -u scripts/what_does_the_trained_net_actually_bank.py --ckpt <path>

WHY NOT `play_checkpoint.py`
---------------------------
It is stale: `_greedy` reads `cond["trade"]` (`play_checkpoint.py:151`) and the `trade` head was
deleted when the market became one bundle categorical -- `jax_act.py` records it, "`trade` used to
sit here too. It is gone". It dies with `KeyError: 'trade'` before playing a turn. Left alone rather
than repaired, because this needs the CURRENT decode and that lives in `dagger_tape.run_episode`.

WHY THIS NUMBER AND NOT MORE AGREEMENT
--------------------------------------
Offline, 50 epochs on the frozen aggregate took unit-op agreement 0.470 -> 0.662 and movement
0.000 -> 0.320. Neither says whether it can play. This project's standing rule is to prefer a replay
to an aggregate, and the specific trap here is that **a route two-thirds wrong does not arrive**:
agreement is per-turn and forgiving, while reaching a tile is a conjunction over every step of the
walk. 0.32 movement can be worth $0.

`beta=0.0` means the STUDENT drives every turn and the teacher only labels -- which is what
`run_episode` already does for the `PLAYOUT` line in the training log, so this number is directly
comparable to the `student 0 opponent 185507` that log has been printing.
"""
import argparse
import importlib.util
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
    ap.add_argument("--episodes", type=int, default=4)
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--seeds", type=int, default=4)
    args = ap.parse_args()

    import jax

    from kagg.il import market_bundles as MB
    from kagg.rl import jax_policy as P
    from kagg.search import schedule_agent as SA

    DT = _load("dagger_tape", REPO / "scripts/dagger_tape.py")

    # The planner arm, matching how the teacher was built for this data.
    SA.REPLAY_OPENING_DAYS = ()

    ck = pickle.load(open(args.ckpt, "rb"))
    a = ck.get("args") or {}
    model = P.Policy(d_model=int(a.get("d_model", 128)), n_heads=int(a.get("heads", 4)),
                     n_layers=int(a.get("layers", 3)))
    params = ck["params"]

    vocab = MB.load_vocab(str(ck.get("vocab_path") or a.get("vocab")))
    bundle_ok = MB.valid_table(vocab, pad_to=P.N_BUNDLES)

    rng = np.random.default_rng(0)
    specs = DT.episode_specs(DT.tape_games(), DT.opponent_pool(0), args.seeds, rng)
    key = jax.random.PRNGKey(0)

    print("ckpt      %s" % args.ckpt, flush=True)
    print("offline epochs %s   round %s" % (ck.get("offline_epochs"), ck.get("round")), flush=True)
    print("beta 0.0 -- the STUDENT drives every turn\n", flush=True)
    print("  %-24s %10s %10s   %s" % ("episode", "student", "opponent", "result"), flush=True)

    # **`run_episode`'s own `marks` stop at d6, and that is a six-day window being read as a
    # season.** The teacher runs on $1-$171 through the first week too -- kawa's money arrives from
    # d12 (`money_dawn` 15,389) -- so an early curve near zero is not evidence of anything. The day
    # the student diverges is later, and invisible without this.
    #
    # Recorded by wrapping the env rather than by changing `run_episode`, so the training loop keeps
    # using the code path it has always used.
    def _full_curve(spec):
        """One season, STUDENT driving, bank recorded at every dawn. `{day: (mine, opp, hands)}`.

        Decoded exactly as `run_episode` decodes at beta=0 -- `greedy_action` then `decode_action`,
        with the shed passed so a SELL at the head's top class is read back as the amount actually
        in the barn. A second decode here that differed from the training one would measure a policy
        we never trained.

        The TEACHER is still queried every turn and its answer discarded: its latches, purchase
        counter and sell ledger are carried across turns, and skipping the query does not skip that
        state, it corrupts it.
        """
        from kaggle_environments import make

        from kagg.agents.neural import decode_action
        from kagg.il.tape_teacher import TapeTeacher
        from kagg.rl import adapter as AD, jax_act as A, jax_obs

        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        seat = spec["seat"]
        teacher = TapeTeacher(seat)
        memo = AD.GameMemo()
        out = {}
        for turn in range(args.horizon):
            if env.done:
                break
            obs = env.state[seat].observation
            if turn % 24 == 0:
                farm = (obs.get("farms") or [None, None])[seat] or {}
                opp = (obs.get("farms") or [None, None])[1 - seat] or {}
                out[turn // 24] = (int(farm.get("money") or 0), int(opp.get("money") or 0),
                                   len(farm.get("hands") or []))
            teacher.act(obs)
            memo.observe(obs, step=turn)
            privates = [obs["private"] if p == seat else AD.agent_private_stub() for p in range(2)]
            st = AD.state_from_obs(obs, privates, step=turn, memo=memo)
            t_, u_, g_ = jax_obs.encode(st)
            heads, _v = model.apply(params, A._flat(t_), A._flat(u_), A._flat(g_))
            picks = {k: np.asarray(v) for k, v in
                     DT.greedy_action(heads, A.masks_for(st, bundle_ok)).items()}
            n_units = 1 + len(obs["farms"][seat].get("hands") or [])
            student = decode_action(picks, n_units, vocab, seat=seat,
                                    shed=(obs.get("private") or {}).get("shed"))
            pair = [None, None]
            pair[seat] = teacher.sendable(student, len(obs["farms"][seat].get("hands") or []))
            pair[1 - seat] = DT.opponent_action(
                spec, turn, len(obs["farms"][1 - seat].get("hands") or []))
            env.step(pair)
        return out

    banks = []
    for spec in specs[: args.episodes]:
        _rows, pstats, key = DT.run_episode(spec, params, model, vocab, bundle_ok, key,
                                            0.0, args.horizon, rng)
        me = float(pstats.get("bank", 0.0))
        opp = float(pstats.get("opponent_bank", 0.0))
        banks.append((me, opp))
        print("  %-24s %10s %10s   %s"
              % (str(spec.get("name"))[:24], format(me, ",.0f"), format(opp, ",.0f"),
                 "win" if me > opp else ("draw" if me == opp else "loss")), flush=True)
        # `marks` is `{day: (money, owned_tiles, hands)}` for d0-d6, recorded at dawn. A flat bank
        # with zero hands is the "banked its opening and stopped" signature, and an end-of-season
        # scalar cannot show it.
        # The WHOLE season at dawn, not the six days `run_episode.marks` records. The teacher runs
        # on $1-$171 through the first week itself, so a six-day window cannot distinguish "on
        # track" from "dead".
        curve = _full_curve(spec)
        days = sorted(curve)
        for label, i in (("mine", 0), ("opp ", 1)):
            print("      %s " % label
                  + " ".join("%6d" % curve[d][i] for d in days), flush=True)
        print("      day  " + " ".join("%6d" % d for d in days), flush=True)

    if banks:
        mine = [b for b, _o in banks]
        print("\n  median student bank %s   wins %d/%d"
              % (format(float(np.median(mine)), ",.0f"),
                 sum(1 for m, o in banks if m > o), len(banks)), flush=True)
    print("\nREAD IT", flush=True)
    print("  bank near $3,000    it banks its opening and stops -- the failure this project has", flush=True)
    print("                      shipped before. Agreement was measuring nothing playable.", flush=True)
    print("  bank rising         the clone is worth continuing; compare against the planner's", flush=True)
    print("                      own ~$150k on the same arm.", flush=True)


if __name__ == "__main__":
    main()
