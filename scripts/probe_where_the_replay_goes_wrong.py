"""Where does the replay diverge, and is it the net or the drift? Two columns, same checkpoint.

**The question this answers.** `greedy op 1.0000` is measured on states the TEACHER produced. The
playout is the student driving alone. Between those two numbers sit two different failures, and
they want different fixes:

  ON-TAPE   the teacher drives; the student is only scored. Any disagreement is the net being
            wrong about a state it was trained on. Pure model error.
  OFF-TAPE  the student drives. Disagreement is model error PLUS every consequence of an earlier
            slip -- a unit on the wrong tile, a shed one item short, a bank that could not afford
            the purchase the tape makes next.

If OFF-TAPE breaks at the same turn ON-TAPE does, the net is wrong. If ON-TAPE is clean and
OFF-TAPE falls apart after turn N, the net is right and the trajectory is unstable -- which is a
statement about compounding, not about capacity.

    python -u scripts/probe_where_the_replay_goes_wrong.py --run data/dagger_tape/d4fix2-...

**The GREEDY decode, because that is what ships.** `neural.py:255`, inside `make_agent`, is
`jnp.argmax`. `dagger_tape`'s playout reuses `run_episode`, which samples because the rollout
COLLECTOR needs stochasticity -- so every playout bank in the training log measures a policy the
submission does not use.

**What this cannot tell you.** Nothing here is held out. The four tapes, the fixed start state and
weeds off mean the board at turn t is near-identical every episode, and `jax_obs` hands the net an
explicit 54-wide clock one-hot. A 957,903-parameter model can memorise 480 turns, so ON-TAPE 1.0000
is consistent with a lookup table keyed on the clock. Use `--holdout` on a training run to test
that; this probe deliberately does not claim to.
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

TPD = 24


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="a dagger_tape run directory")
    ap.add_argument("--horizon", type=int, default=120)
    ap.add_argument("--tapes", type=int, default=4)
    ap.add_argument("--show", type=int, default=8, help="divergences to print per tape")
    args = ap.parse_args()

    import pickle

    import jax
    import jax.numpy as jnp

    import dagger_tape as DT
    from kagg.agents import neural as NEURAL
    from kagg.il import market_bundles as MB
    from kagg.il import replays as RP
    from kagg.il.tape_teacher import TapeTeacher
    from kagg.rl import adapter as AD, jax_act as A, jax_obs, jax_policy as P
    from kaggle_environments import make

    run = pathlib.Path(args.run)
    with (run / "latest.pkl").open("rb") as fh:
        ckpt = pickle.load(fh)
    params, rnd = ckpt["params"], ckpt["round"]
    cargs = ckpt["args"]

    vocab_path = cargs.get("vocab") or str(REPO / "data/il/bundle_vocab_teacher.json")
    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(pair) for pair in b) for b in json.loads(pathlib.Path(vocab_path).read_text())],
        max_size=P.N_BUNDLES)
    bundle_ok = jnp.asarray(MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    model = P.Policy(d_model=cargs.get("d_model", 128), n_heads=cargs.get("heads", 4),
                     n_layers=cargs.get("layers", 3))

    print("checkpoint %s round %d  horizon %d  GREEDY decode (the one make_agent uses)"
          % (run.name, rnd, args.horizon), flush=True)
    print()

    op_name = {v: k for k, v in RP.OP_CODE.items()}

    def play(spec, student_drives):
        """Step one tape. Returns (per-day divergences, first offenders, bank)."""
        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        seat = spec["seat"]
        teacher = TapeTeacher(seat)
        per_day = collections.Counter()
        seen_day = collections.Counter()
        first = []

        for turn in range(args.horizon):
            if env.done:
                break
            obs = env.state[seat].observation
            teacher_action = teacher.act(obs)

            privates = [obs["private"] if p == seat else AD.agent_private_stub()
                        for p in range(2)]
            st = AD.state_from_obs(obs, privates, step=turn)
            tiles, units, glob = jax_obs.encode(st)
            heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
            masks = A.masks_for(st, bundle_ok)
            greedy = DT.greedy_action(heads, masks)

            n_units = 1 + len(obs["farms"][seat].get("hands") or [])
            labels = RP.encode_action(teacher_action, n_units, vocab=vocab)
            g_op = np.asarray(greedy["op"])[seat]

            day = turn // TPD
            for u in range(n_units):
                seen_day[day] += 1
                t_code, s_code = int(labels["op"][u]), int(g_op[u])
                if t_code != s_code:
                    per_day[day] += 1
                    if len(first) < args.show:
                        farm = obs["farms"][seat]
                        pos = ([tuple(farm.get("farmer") or (0, 0))]
                               + [tuple(h) for h in (farm.get("hands") or [])])
                        x, y = pos[u] if u < len(pos) else (-1, -1)
                        first.append(
                            "turn %3d day %2d h%2d unit %d at (%d,%d): teacher %-18s net %s"
                            % (turn, day, turn % TPD, u, x, y,
                               op_name.get(t_code, t_code), op_name.get(s_code, s_code)))

            action = (NEURAL.decode_action(greedy, n_units, vocab, seat=seat)
                      if student_drives else teacher_action)
            opp = spec["opponent"][turn] if turn < len(spec["opponent"]) else {}
            env.step([action if p == seat else opp for p in range(2)])

        bank = int((env.state[0].observation["farms"][seat] or {}).get("money") or 0)
        return per_day, seen_day, first, bank

    for spec in DT.tape_games()[: args.tapes]:
        on_day, on_seen, on_first, on_bank = play(spec, student_drives=False)
        off_day, off_seen, off_first, off_bank = play(spec, student_drives=True)

        days = sorted(set(on_seen) | set(off_seen))
        print("%s  seat %d" % (spec["name"], spec["seat"]))
        print("  day            " + "".join("%8d" % d for d in days))
        print("  slots          " + "".join("%8d" % on_seen.get(d, 0) for d in days))
        print("  ON-TAPE  wrong " + "".join("%8d" % on_day.get(d, 0) for d in days))
        print("  OFF-TAPE wrong " + "".join("%8d" % off_day.get(d, 0) for d in days))
        print("  bank: on-tape %d, off-tape %d" % (on_bank, off_bank))
        if off_first:
            print("  first divergences when the student drives:")
            for line in off_first:
                print("    " + line)
        else:
            print("  NO divergence at all with the student driving -- it replays the tape exactly")
        if on_first:
            print("  first divergences with the TEACHER driving (pure model error):")
            for line in on_first:
                print("    " + line)
        print(flush=True)


if __name__ == "__main__":
    main()
