"""The bundle head picks the opening correctly and the season still hires nobody. Print the action.

    python -u scripts/print_the_students_opening_turn.py --ckpt <path>

WHERE THIS SITS
---------------
Established, in order:

    the vocabulary       turn-0 label is index 31, legal under its own mask.
    the head             the student ranks 31 FIRST on all 16 turn-0 rows and picks it.
    bundle 31            BUY_ANIMAL COW x2, SHEEP x2, BUY_PRODUCT WHEAT, BUY_SEED MELON,
                         BUY_SEED WHEAT, HIRE x5 -- ten orders after the animal coalesce.
    the playout          `hands 0` on every day of every season, bank $0.

Those cannot all be true of a working decode, so the loss is between the chosen index and the
submitted action. Rather than reason about which of `greedy_action`, `orders_from_heads`,
`_uncap_sells` or the ten-slot cut is responsible, this prints every stage of turn 0 side by side:

    the raw head picks, the bundle index, the order list as decoded, what `sendable` passes on,
    and what the environment reports one step later.

The teacher's own turn 0 is printed beneath it as the reference. If the two order lists match and
the crew is still zero afterwards, the defect is in the environment's acceptance and not in us --
which is a different investigation, and worth separating cleanly.
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
    args = ap.parse_args()

    import jax
    import jax.numpy as jnp
    from kaggle_environments import make

    from kagg.il import market_bundles as MB
    from kagg.il.tape_teacher import TapeTeacher
    from kagg.rl import adapter as AD, jax_act as A, jax_obs, jax_policy as P
    from kagg.search import schedule_agent as SA

    DT = _load("dagger_tape", REPO / "scripts/dagger_tape.py")
    SA.REPLAY_OPENING_DAYS = ()

    ck = pickle.load(open(args.ckpt, "rb"))
    a = ck.get("args") or {}
    model = P.Policy(d_model=int(a.get("d_model", 128)), n_heads=int(a.get("heads", 4)),
                     n_layers=int(a.get("layers", 3)))
    params = ck["params"]
    vocab = MB.load_vocab(str(ck.get("vocab_path") or a.get("vocab")))
    bundle_ok = MB.valid_table(vocab, pad_to=P.N_BUNDLES)

    rng = np.random.default_rng(0)
    spec = DT.episode_specs(DT.tape_games(), DT.opponent_pool(0), 4, rng)[0]
    seat = spec["seat"]

    env = make("kaggriculture", configuration=spec["cfg"], debug=False)
    env.reset(2)
    obs = env.state[seat].observation
    memo = AD.GameMemo().observe(obs, step=0)
    privates = [obs["private"] if p == seat else AD.agent_private_stub() for p in range(2)]
    state = AD.state_from_obs(obs, privates, step=0, memo=memo)
    tiles, units, glob = jax_obs.encode(state)
    heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
    masks = A.masks_for(state, bundle_ok)

    act = DT.greedy_action(heads, masks)
    picks = {k: np.asarray(v) for k, v in act.items()}
    b_idx = int(picks["bundle"].reshape(-1)[seat])

    print("episode  %s  seat %d" % (spec.get("name"), seat), flush=True)
    print("bank at turn 0: %s" % (obs["farms"][seat] or {}).get("money"), flush=True)
    print("\nbundle index picked: %d" % b_idx, flush=True)
    print("bundle decodes to:   %s" % (list(vocab.bundle(b_idx)),), flush=True)
    for h in ("qty_sell", "qty_buy_product", "qty_buy_seed"):
        print("  %-16s %s" % (h, picks[h].reshape(picks[h].shape[0], -1)[seat][:12]), flush=True)

    n_units = 1 + len(obs["farms"][seat].get("hands") or [])
    from kagg.agents.neural import decode_action
    student = decode_action(picks, n_units, vocab, seat=seat,
                            shed=(obs.get("private") or {}).get("shed"))
    print("\nSTUDENT action", flush=True)
    print("  farmer %s" % student.get("farmer"), flush=True)
    print("  hands  %s" % student.get("hands"), flush=True)
    print("  market (%d orders)" % len(student.get("market") or []), flush=True)
    for o in student.get("market") or []:
        print("     %s" % (o,), flush=True)

    teacher = TapeTeacher(seat)
    t_act = teacher.act(obs)
    print("\nTEACHER action", flush=True)
    print("  farmer %s" % t_act.get("farmer"), flush=True)
    print("  market (%d orders)" % len(t_act.get("market") or []), flush=True)
    for o in t_act.get("market") or []:
        print("     %s" % (o,), flush=True)

    hands_now = len(obs["farms"][seat].get("hands") or [])
    pair = [None, None]
    pair[seat] = teacher.sendable(student, hands_now)
    pair[1 - seat] = DT.opponent_action(spec, 0, len(obs["farms"][1 - seat].get("hands") or []))
    print("\nSENT to env: market (%d orders) %s"
          % (len(pair[seat]["market"]), pair[seat]["market"]), flush=True)
    env.step(pair)

    after = env.state[0].observation["farms"][seat] or {}
    print("\nAFTER ONE STEP", flush=True)
    print("  money %s   hands %d   shed %s"
          % (after.get("money"), len(after.get("hands") or []),
             dict((env.state[seat].observation.get("private") or {}).get("shed") or {})), flush=True)
    print("\n  if hands == 0 here with the orders above sent, the environment refused them;", flush=True)
    print("  if the order list above is short or empty, the decode dropped them.", flush=True)


if __name__ == "__main__":
    main()
