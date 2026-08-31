"""How many times must the teacher step in, if every divergence is corrected the moment it happens?

    python -u scripts/probe_how_many_corrections_a_season_needs.py

Alex, 2026-08-27: *"the student drives but then gets kicked if it says something the teacher
disagrees with"*, and *"it is almost certainly a single or 2 errors and cascade, similar to the 72"*.

THE QUESTION THIS SETTLES, and why it comes before a retrain
------------------------------------------------------------
Off-tape op agreement is 99.97 / 99.68 / 87.20 / 51.25 across the four tapes, and the money follows
it steeply -- 98.5%, 99.6%, 52.7%, 0.3% of the teacher. But an agreement figure cannot distinguish

    (a) ninety independent mistakes            -> the net is undertrained, resume the run
    (b) one mistake and 700 turns of cascade   -> find the root, fix it, no training needed

and those want opposite work. The `SELL WHEAT 72` cap was case (b): ONE unrepresentable label per
tape, costing $1,930 on a tape whose market was otherwise perfect for 719 turns.

So: play the student, and whenever its action differs from the teacher's, EXECUTE THE TEACHER'S and
count it. The trajectory is therefore pinned to the tape and every correction is an independent
error rather than a consequence of an earlier one. Corrections per season is the number that
separates (a) from (b).

This is a diagnostic, not a training mode and not a submission. There is no teacher on the ladder.
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


def _norm(action, n_units):
    """A comparable form: the unit ops in order, plus the market as a sorted multiset."""
    units = [action.get("farmer")] + list(action.get("hands") or [])
    units = [tuple(str(z) for z in (u or ["PASS"])) for u in units[:n_units]]
    market = tuple(sorted(tuple(str(z) for z in o) for o in (action.get("market") or []) if o))
    return tuple(units), market


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="data/dagger_tape/season_fast-20260822-235031")
    ap.add_argument("--ckpt", default="pinned_round27.pkl")
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--tapes", type=int, default=4)
    ap.add_argument("--show", type=int, default=10)
    ap.add_argument("--correct", default="all", choices=("all", "market", "units", "none"),
                    help="which half of the action the teacher is allowed to repair")
    args = ap.parse_args()

    import pickle

    import dagger_tape as DT
    import jax.numpy as jnp
    from kagg.agents import neural as NEURAL
    from kagg.il import market_bundles as MB
    from kagg.il.tape_teacher import TapeTeacher
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
    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(p) for p in b) for b in json.loads(pathlib.Path(vocab_path).read_text())],
        max_size=P.N_BUNDLES)
    bundle_ok = jnp.asarray(MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    model = P.Policy(d_model=cargs.get("d_model", 128), n_heads=cargs.get("heads", 4),
                     n_layers=cargs.get("layers", 3))
    print(f"{run.name}/{args.ckpt} round {ckpt.get('round')}  vocab "
          f"{pathlib.Path(vocab_path).name} ({want} bundles)")
    print("student drives; every divergence is CORRECTED to the teacher, so each one is "
          "independent\n")

    print(f"{'tape':<15}{'corrections':>12}{'unit-only':>11}{'mkt-only':>10}{'both':>7}"
          f"{'bank':>12}{'teacher':>12}")
    details = []
    for spec in DT.tape_games()[: args.tapes]:
        seat = spec["seat"]
        env = make("kaggriculture", configuration=spec["cfg"], debug=False)
        env.reset(2)
        teacher = TapeTeacher(seat)
        n_corr = unit_only = mkt_only = both = 0
        first = []
        by_day = collections.Counter()

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
            greedy = DT.greedy_action(heads, masks=A.masks_for(st, bundle_ok))
            n_units = 1 + len(obs["farms"][seat].get("hands") or [])
            s_act = NEURAL.decode_action(greedy, n_units, vocab, seat=seat,
                                         shed=(obs.get("private") or {}).get("shed"))

            tu, tm = _norm(t_act, n_units)
            su, sm = _norm(s_act, n_units)
            if tu != su or tm != sm:
                n_corr += 1
                by_day[turn // TPD] += 1
                if tu != su and tm != sm:
                    both += 1
                elif tu != su:
                    unit_only += 1
                else:
                    mkt_only += 1
                if len(first) < args.show:
                    if tu != su:
                        bad = [(i, a, b) for i, (a, b) in enumerate(zip(tu, su)) if a != b]
                        i, a, b = bad[0]
                        first.append(f"    turn {turn:>3} d{turn // TPD:>2} h{turn % TPD:>2} "
                                     f"unit {i}: teacher {' '.join(a):<22} net {' '.join(b)}")
                    else:
                        first.append(f"    turn {turn:>3} d{turn // TPD:>2} h{turn % TPD:>2} "
                                     f"MARKET: teacher {list(tm)}  net {list(sm)}")

            # THE KICK. `--correct all` pins the trajectory to the tape, so every divergence counted
            # above is independent rather than an earlier one's shadow.
            #
            # `--correct market` is the decisive arm for Alex's reading -- *"a missed buy and then
            # ops are screwed because they cant"*. Unit ops and market orders are coupled through
            # the shed: a BUY that never lands leaves seeds short, and then PLANT is illegal however
            # right the unit head is. So repair ONLY the orders and let the unit head run free. If
            # the season comes back, the market head is the single root and the unit head was never
            # the problem. The ordering already points this way: on 92466371 the market diverges at
            # turn 312 and the first op error is at 327.
            if args.correct == "all":
                mine = t_act
            elif args.correct == "market":
                mine = dict(s_act)
                mine["market"] = t_act.get("market") or []
            elif args.correct == "units":
                mine = dict(t_act)
                mine["market"] = s_act.get("market") or []
            else:
                mine = s_act
            opp = spec["opponent"][turn] if turn < len(spec["opponent"]) else {}
            env.step([mine if p == seat else opp for p in range(2)])

        bank = int((env.state[0].observation["farms"][seat] or {}).get("money") or 0)
        doc = json.loads((REPO / spec["tape_path"]).read_text())
        tb = int((doc.get("rewards") or [0, 0])[seat])
        print(f"{spec['name'][:14]:<15}{n_corr:>12}{unit_only:>11}{mkt_only:>10}{both:>7}"
              f"{bank:>12,}{tb:>12,}")
        details.append((spec["name"], first, by_day))

    for name, first, by_day in details:
        if not first:
            continue
        print(f"\n{name}   corrections by day: "
              + ", ".join(f"d{d}:{n}" for d, n in sorted(by_day.items())))
        for line in first:
            print(line)


main()
