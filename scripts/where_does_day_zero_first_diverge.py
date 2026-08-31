"""Day 0, op for op, unit by unit. Name the FIRST divergence.

    python -u scripts/where_does_day_zero_first_diverge.py --ckpt <path>

WHY DAY 0 AND NOT A SEASON
--------------------------
A season total cannot say where a clone broke, and a 30-day playout costs minutes to tell you
something d0 tells you in seconds: **any op or market divergence on day 0 poisons everything after
it.** The board is deterministic and the teacher is a fixed schedule, so a unit that does the wrong
thing at hour 3 is standing somewhere else at hour 4, and every later comparison is against a board
the teacher never saw. Agreement measured with the teacher driving hides this completely -- it puts
the student back on the rails every turn.

This project's own rule is d0-d6 op for op, not money, and this is the first day of it.

WHAT IS PRINTED
---------------
The teacher drives (so the boards stay identical and a divergence is the student's, not drift), and
at every turn the student's greedy decode is compared slot by slot:

    turn, hour, unit slot, teacher op, student op, and the market baskets when they differ.

Then the first divergence, called out on its own, because that is the one to fix -- everything after
it is downstream.

`PICKUP`, `DROP` and `PASS` are reported like any other op here. The tape-matching skill exempts
them as tour shape when comparing OUR planner to a recording; this is a net against the teacher it
was fitted to, where any difference is a fitting gap.
"""
import argparse
import collections
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
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--episodes", type=int, default=1)
    ap.add_argument("--rng", type=int, default=0,
                    help="town-draw seed. The training run used 0, so any other "
                         "value gives towns the net has never seen -- which is the "
                         "only way to tell a learned latch from a memorised season.")
    args = ap.parse_args()

    from kaggle_environments import make

    from kagg.agents.neural import decode_action
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

    rng = np.random.default_rng(args.rng)
    specs = DT.episode_specs(DT.tape_games(), DT.opponent_pool(0), 4, rng)

    print("ckpt  %s   round %s" % (args.ckpt, ck.get("round")), flush=True)
    print("teacher drives; the student is scored on the SAME board every turn\n", flush=True)

    for spec in specs[: args.episodes]:
        seat = spec["seat"]
        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        teacher = TapeTeacher(seat)
        memo = AD.GameMemo()
        first = None
        counts = collections.Counter()

        print("=== %s seat %d" % (spec.get("name"), seat), flush=True)
        for turn in range(24 * args.days):
            if env.done:
                break
            obs = env.state[seat].observation
            memo.observe(obs, step=turn)
            privates = [obs["private"] if p == seat else AD.agent_private_stub() for p in range(2)]
            st = AD.state_from_obs(obs, privates, step=turn, memo=memo)
            t_, u_, g_ = jax_obs.encode(st)
            heads, _v = model.apply(params, A._flat(t_), A._flat(u_), A._flat(g_))
            picks = {k: np.asarray(v) for k, v in
                     DT.greedy_action(heads, A.masks_for(st, bundle_ok)).items()}

            t_act = teacher.act(obs)
            n_units = 1 + len(obs["farms"][seat].get("hands") or [])
            s_act = decode_action(picks, n_units, vocab, seat=seat,
                                  shed=(obs.get("private") or {}).get("shed"))

            t_ops = [t_act.get("farmer") or ["PASS"]] + list(t_act.get("hands") or [])
            s_ops = [s_act.get("farmer") or ["PASS"]] + list(s_act.get("hands") or [])
            for slot in range(min(len(t_ops), len(s_ops))):
                t_o = list(t_ops[slot] or ["PASS"])
                s_o = list(s_ops[slot] or ["PASS"])
                if t_o != s_o:
                    counts["op"] += 1
                    if first is None:
                        first = ("op", turn, slot, t_o, s_o)
                    if counts["op"] <= 12:
                        print("  t%-3d h%-2d unit %-2d  teacher %-24s student %s"
                              % (turn, turn % 24, slot, str(t_o), str(s_o)), flush=True)

            t_m = [list(o) for o in (t_act.get("market") or [])]
            s_m = [list(o) for o in (s_act.get("market") or [])]
            if sorted(map(str, t_m)) != sorted(map(str, s_m)):
                counts["market"] += 1
                if first is None:
                    first = ("market", turn, -1, t_m, s_m)
                if counts["market"] <= 6:
                    print("  t%-3d h%-2d MARKET" % (turn, turn % 24), flush=True)
                    print("        teacher %s" % (t_m,), flush=True)
                    print("        student %s" % (s_m,), flush=True)

            pair = [None, None]
            pair[seat] = teacher.sendable(t_act, len(obs["farms"][seat].get("hands") or []))
            pair[1 - seat] = DT.opponent_action(
                spec, turn, len(obs["farms"][1 - seat].get("hands") or []))
            env.step(pair)

        print("\n  op divergences %d   market divergences %d over %d turns"
              % (counts["op"], counts["market"], 24 * args.days), flush=True)
        if first:
            kind, turn, slot, t_o, s_o = first
            print("  FIRST DIVERGENCE  %s at turn %d (hour %d)%s"
                  % (kind, turn, turn % 24, "" if slot < 0 else ", unit %d" % slot), flush=True)
            print("    teacher %s" % (t_o,), flush=True)
            print("    student %s" % (s_o,), flush=True)
        else:
            print("  NO DIVERGENCE over %d turns" % (24 * args.days), flush=True)
        print(flush=True)


if __name__ == "__main__":
    main()
