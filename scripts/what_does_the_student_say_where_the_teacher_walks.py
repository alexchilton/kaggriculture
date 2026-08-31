"""Movement agreement is exactly 0.000 over 45,485 labels. What IS the student emitting there?

    python -u scripts/what_does_the_student_say_where_the_teacher_walks.py --ckpt <path>

THE MEASUREMENT THIS REPLACES
-----------------------------
Two DAgger runs reported, identically:

    per-op (greedy)  WEST 0.000/12844  NORTH 0.000/12960  SOUTH 0.000/9668  EAST 0.000/10013
                     PICKUP 0.000/3236  DIG 0.000/516  PLACE 0.000/351  BUILD_PASTURE 0.000/232

Exactly 0.000 over tens of thousands of labels is not "fitted badly" -- a poorly fitted class still
fires sometimes. It means the student never emits those codes at all, and a rate cannot say what it
emits instead. Three explanations have already been ruled out by measurement rather than argument:

    the label space      `replays.OP_CODE` matches `kagg.sim.ops` on all 18 codes.
    the encoder widening the same 0.000 appears warm-starting from the pre-latch 122-wide
                         checkpoint, so it is not the 122 -> 183 change.
    the dead-slot columns the same 0.000 appears after parking unhired slots at spawn.

**The hypothesis this tests.** The policy's op head is 23 wide: `O.N_OPS` (18) primitives plus five
COMMIT tokens from `kagg.rl.commit`, which mean "walk to the nearest tile needing X and do it on
arrival". The teacher is the planner, which emits primitive moves. If the student has learned to
answer with a commit token where the teacher walks, then:

    - every movement label is scored a miss, which is what the table shows;
    - the student is nonetheless doing something coherent;
    - op agreement survives on NOOP and the stationary ops, which is what 0.4648 looks like.

That is a metric problem wearing the clothes of a learning problem, and the two want opposite fixes.

WHAT IS PRINTED
---------------
The joint histogram: for each teacher op, what the student's greedy decode said instead. Plus the
student's overall op distribution, because "it says NOOP to everything" and "it says COMMIT_WATER to
everything" are both consistent with the per-op table and are different diagnoses.

Greedy, masked, exactly as `dagger_tape.greedy_action` decodes it -- a distribution over what the
student *would* play, not over what it samples.
"""
import argparse
import collections
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

DEFAULT_CKPT = REPO / "data/backup_weights/planner-20260828-014128_latest.pkl"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=str(DEFAULT_CKPT))
    ap.add_argument("--turns", type=int, default=480)
    ap.add_argument("--seed", type=int, default=9000)
    args = ap.parse_args()

    import pickle

    import jax
    import jax.numpy as jnp
    from kaggle_environments import make

    from kagg import plan as PLAN
    from kagg.il import market_bundles as MB, replays as RP
    from kagg.rl import adapter as AD, commit as C, jax_act as A, jax_obs, jax_policy as P
    from kagg.search import schedule_agent as SA

    OP_NAME = {v: k for k, v in RP.OP_CODE.items()}
    for i in range(C.N_COMMIT):
        OP_NAME[RP.OP_CODE and (len(RP.OP_CODE) + i)] = "COMMIT_%d" % i
    # Named off `commit.ARRIVAL_OP` so the label says which job the token walks to.
    arrival = [int(v) for v in np.asarray(C.ARRIVAL_OP)]
    for i, a in enumerate(arrival):
        OP_NAME[18 + i] = "COMMIT_" + {v: k for k, v in RP.OP_CODE.items()}.get(a, str(a))

    ck = pickle.load(open(args.ckpt, "rb"))
    a = ck.get("args") or {}
    n_layers = int(a.get("layers", 3))
    model = P.Policy(d_model=int(a.get("d_model", 128)), n_heads=int(a.get("heads", 4)),
                     n_layers=n_layers)
    _t, _u, _g = jax_obs.encode(__import__("kagg.sim.jax_sim", fromlist=["x"]).reset(1))
    template = model.init(jax.random.PRNGKey(0), A._flat(_t), A._flat(_u), A._flat(_g))
    params = P.load_or_migrate(ck["params"], template)

    stored = ck.get("vocab")
    vocab = (MB.Vocabulary.from_bundles([tuple(tuple(p) for p in b) for b in stored],
                                        max_size=P.N_BUNDLES)
             if stored else MB.load_vocab())
    bundle_ok = MB.valid_table(vocab, pad_to=P.N_BUNDLES)

    # The planner IS the teacher for this run, so it drives and labels.
    SA.REPLAY_OPENING_DAYS = ()
    teacher = SA.make_agent(PLAN.load(), 0)

    env = make("kaggriculture", configuration={"seed": args.seed, "weedSpawnChance": 0.0},
               debug=False)
    env.reset(2)
    memo = AD.GameMemo()

    joint = collections.Counter()          # (teacher_op_name, student_op_name) -> n
    student_all = collections.Counter()

    for turn in range(args.turns):
        if env.done:
            break
        obs = env.state[0].observation
        memo.observe(obs, step=turn)
        privates = [obs["private"] if p == 0 else AD.agent_private_stub() for p in range(2)]
        state = AD.state_from_obs(obs, privates, step=turn, memo=memo)

        tiles, units, glob = jax_obs.encode(state)
        heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
        masks = A.masks_for(state, bundle_ok)
        op_logits = jnp.where(masks["op"], heads["op"], -jnp.inf)
        student_op = np.asarray(jnp.argmax(op_logits, axis=-1))[0]      # seat 0

        act = teacher(obs)
        t_ops = [act.get("farmer") or ["PASS"]] + list(act.get("hands") or [])
        n_live = len(t_ops)
        for slot in range(n_live):
            t_name = str(t_ops[slot][0]) if t_ops[slot] else "PASS"
            s_name = OP_NAME.get(int(student_op[slot]), str(int(student_op[slot])))
            joint[(t_name, s_name)] += 1
            student_all[s_name] += 1

        env.step([act, {"farmer": ["PASS"], "hands": [], "market": []}])

    print("ckpt   %s" % args.ckpt, flush=True)
    print("turns  %d, seed %d, teacher = planner\n" % (args.turns, args.seed), flush=True)

    print("WHAT THE STUDENT SAYS, OVERALL", flush=True)
    tot = sum(student_all.values()) or 1
    for name, n in student_all.most_common(12):
        print("  %-22s %6d  %5.1f%%" % (name, n, 100.0 * n / tot), flush=True)

    print("\nWHERE THE TEACHER MOVES, WHAT THE STUDENT SAYS INSTEAD", flush=True)
    for t_name in ("WEST", "NORTH", "SOUTH", "EAST", "PICKUP", "DIG"):
        rows = [(n, s) for (t, s), n in joint.items() if t == t_name]
        if not rows:
            continue
        seen = sum(n for n, _ in rows)
        top = "  ".join("%s %d (%.0f%%)" % (s, n, 100.0 * n / seen)
                        for n, s in sorted(rows, reverse=True)[:4])
        print("  %-8s seen %5d ->  %s" % (t_name, seen, top), flush=True)

    print("\nREAD IT", flush=True)
    print("  mass on COMMIT_*   the student answers a walk with a commitment. The 0.000 is the", flush=True)
    print("                     METRIC counting a different-but-coherent answer as a miss.", flush=True)
    print("  mass on PASS       the student has collapsed to the majority class; a real fit", flush=True)
    print("                     failure, and per-op agreement is honest.", flush=True)


if __name__ == "__main__":
    main()
