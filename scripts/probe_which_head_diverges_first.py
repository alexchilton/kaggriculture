"""Which head breaks the playout first -- the unit ops, or the market?

    python -u scripts/probe_which_head_diverges_first.py --run data/dagger_tape/season_fast-... \
        --ckpt pinned_round27.pkl --horizon 719

WHY THIS EXISTS
---------------
`probe_where_the_replay_goes_wrong.py` compares `labels["op"][u]` and nothing else (its lines
117-120). Its `wrong` columns therefore count UNIT OPS only: not the market bundle, and not the op
arguments. Read as "the action was right", they say more than they measure -- and they were read that
way here on 2026-08-27, producing the conclusion "the collapse is entirely movement".

That conclusion cannot stand on that counter. `OFF-TAPE wrong 0` for days 0-2 is consistent with the
market head being wrong on all 72 of those turns. And the duel says something is: the net banks
exactly $0 (seat 0) or $50 (seat 1) on eight different seeds, which is not what a policy with sound
unit ops does -- it would farm and sell something.

So this probe plays the student ALONE and records, per turn, three things independently:

    op        did every unit's op code match the teacher's
    args      did the op arguments match (crop / item / quantity)
    market    did the emitted market orders match the teacher's, as a set

and prints the FIRST turn each of them diverges. Whichever is earliest is the one that steers the
season; the others are downstream of it.

The market comparison is on the DECODED orders rather than the bundle index, because that is what the
environment executes and it is invariant to a vocabulary reshuffle -- the exact failure that made the
first run of `duel_net_vs_tape.py` look like a broken policy.
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


def _orders(action):
    """A market action as a comparable multiset of tuples."""
    out = collections.Counter()
    for o in (action or {}).get("market") or []:
        if o:
            out[tuple(str(z) for z in o)] += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--ckpt", default="latest.pkl", help="file INSIDE --run")
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--tapes", type=int, default=4)
    ap.add_argument("--show", type=int, default=6)
    args = ap.parse_args()

    import pickle

    import dagger_tape as DT
    import jax.numpy as jnp
    from kagg.agents import neural as NEURAL
    from kagg.il import market_bundles as MB
    from kagg.il import replays as RP
    from kagg.il.tape_teacher import TapeTeacher
    from kagg.rl import adapter as AD, jax_act as A, jax_obs, jax_policy as P
    from kaggle_environments import make

    run = pathlib.Path(args.run)
    with (run / args.ckpt).open("rb") as fh:
        ckpt = pickle.load(fh)
    params, rnd = ckpt["params"], ckpt.get("round")
    cargs = ckpt.get("args") or {}

    # **The checkpoint's own vocabulary, verified by COUNT.** `vocab_path` names a file that may have
    # been rebuilt since; `vocab_size` is what the weights were actually fitted against. A mismatch
    # shifts every index above the difference and is silent at play time.
    want = ckpt.get("vocab_size")
    cand = [cargs.get("vocab"), str(REPO / "data/il/bundle_vocab_teacher_pre_topup.json"),
            str(REPO / "data/il/bundle_vocab_teacher.json"),
            str(REPO / "data/il/bundle_vocab.json")]
    vocab_path = None
    for c in cand:
        if c and pathlib.Path(c).exists() and len(json.loads(pathlib.Path(c).read_text())) == want:
            vocab_path = c
            break
    if vocab_path is None:
        raise SystemExit(f"no vocabulary file on disk holds {want} bundles; tried {cand}")
    print(f"checkpoint {run.name}/{args.ckpt} round {rnd}   vocab {vocab_path} ({want} bundles)")

    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(p) for p in b) for b in json.loads(pathlib.Path(vocab_path).read_text())],
        max_size=P.N_BUNDLES)
    bundle_ok = jnp.asarray(MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    model = P.Policy(d_model=cargs.get("d_model", 128), n_heads=cargs.get("heads", 4),
                     n_layers=cargs.get("layers", 3))

    print(f"\n{'tape':<14}{'op agree':>10}{'first op':>10}{'first args':>12}"
          f"{'first mkt':>11}{'mkt turns':>11}{'bank':>12}")
    for spec in DT.tape_games()[: args.tapes]:
        seat = spec["seat"]
        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        teacher = TapeTeacher(seat)

        first = {"op": None, "args": None, "market": None}
        mkt_bad = 0
        examples = []
        # **Op agreement is the objective, not the bank.** Alex, 2026-08-27: "that is what the net is
        # supposed to do -- memorise the tape and play it back ... we do not care about the opponent
        # ... just follow the ops". The bank moves with the opponent through the shared order book, so
        # a money delta measures the opposition, not the imitation. Count matched unit slots instead.
        op_ok = op_n = 0
        for turn in range(args.horizon):
            obs = env.state[seat].observation
            t_act = teacher.act(obs)

            privates = [obs["private"] if p == seat else AD.agent_private_stub()
                        for p in range(2)]
            st = AD.state_from_obs(obs, privates, step=turn)
            tiles, units, glob = jax_obs.encode(st)
            heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
            greedy = DT.greedy_action(heads, masks=A.masks_for(st, bundle_ok))
            n_units = 1 + len(obs["farms"][seat].get("hands") or [])
            s_act = NEURAL.decode_action(greedy, n_units, vocab, seat=seat)

            labels = RP.encode_action(t_act, n_units, vocab=vocab)
            g_op = np.asarray(greedy["op"])[seat]
            for u in range(n_units):
                op_n += 1
                op_ok += int(int(labels["op"][u]) == int(g_op[u]))
            if first["op"] is None and any(
                    int(labels["op"][u]) != int(g_op[u]) for u in range(n_units)):
                first["op"] = turn

            t_ops = [t_act.get("farmer")] + list(t_act.get("hands") or [])
            s_ops = [s_act.get("farmer")] + list(s_act.get("hands") or [])
            if first["args"] is None:
                for a, b in zip(t_ops, s_ops):
                    if a and b and a[0] == b[0] and list(a[1:]) != list(b[1:]):
                        first["args"] = turn
                        break

            to, so = _orders(t_act), _orders(s_act)
            if to != so:
                mkt_bad += 1
                if first["market"] is None:
                    first["market"] = turn
                if len(examples) < args.show:
                    examples.append(f"    turn {turn:>3} day {turn // TPD:>2} h{turn % TPD:>2}  "
                                    f"teacher {sorted(to.elements()) or '-'}  "
                                    f"net {sorted(so.elements()) or '-'}")

            opp = spec["opponent"][turn] if turn < len(spec["opponent"]) else {}
            env.step([s_act if p == seat else opp for p in range(2)])

        bank = int((env.state[0].observation["farms"][seat] or {}).get("money") or 0)
        print(f"{spec['name'][:13]:<14}{100.0 * op_ok / max(1, op_n):>9.2f}%"
              f"{str(first['op']):>10}{str(first['args']):>12}"
              f"{str(first['market']):>11}{mkt_bad:>11}{bank:>12,}")
        for e in examples:
            print(e)


main()
