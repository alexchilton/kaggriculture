"""The gate a BC checkpoint must pass before it is trusted as a KL prior or a PPO init.

**Why a gate rather than a look at the loss.** A checkpoint that scores well on held-out accuracy
can still be useless -- or worse than useless -- for the two jobs it is being trained for. The
measured example: a checkpoint at 52% ACTED accuracy assigned `P(noop) = 0.9999` at the daily spawn
state, so it emitted PASS on all 719 turns of a real game and banked exactly its $3,000 start. The
loss curve showed none of that.

Two things are checked, and the second is the one that matters:

1. **Does it play?** Final bank against `starter`, and the op census. Banking exactly $3,000 is the
   signature of a policy that never acted.
2. **Can it be used as a prior without harm?** `KL(policy || prior)` taxes the policy for putting
   mass where the prior has none. A prior assigning 6e-5 to moving at spawn would fine PPO roughly
   0.044 per turn for the one behaviour it needs to discover -- at the state it visits most, with
   `--ent-coef 0` recommended alongside so nothing pushes back. That is the 95%-NOOP collapse
   rebuilt through a new mechanism, so it is a blocking check rather than a warning.

`P(noop)` is measured under **honest sampling**, not argmax, because argmax is a decoder choice and
the prior is used on the raw distribution. Measured at temperature 1 the old checkpoint still gave
PASS on every turn, which is what ruled out "just decode it differently" as a fix.

Run:  .venv/bin/python -u scripts/gate_bc.py [checkpoint]
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

# What "usable as a prior" means, decided before looking at any result so it cannot be moved
# afterwards. The floor a hand-specified prior would give any legal op is (1 - 0.3) / 18 = 0.039,
# so requiring a tenth of that is a modest bar and still ~65x the collapsed checkpoint's 6e-5.
MAX_SPAWN_NOOP = 0.98
MIN_SPAWN_MOVE = 4e-3


def spawn_distribution(checkpoint):
    """P(noop) and the best non-noop probability at the state every episode begins in."""
    import jax
    import jax.numpy as jnp
    import pickle

    from kaggle_environments import make
    from kagg.rl import adapter, jax_act as A, jax_obs, jax_policy as P
    from kagg.sim import ops as O

    with Path(checkpoint).open("rb") as fh:
        params = pickle.load(fh)["params"]
    model = P.Policy()

    env = make("kaggriculture", configuration={"seed": 4000}, debug=False)
    env.reset(2)
    obs = json.loads(json.dumps(env.steps[0][0]["observation"]))
    obs["player"] = 0
    state = adapter.state_from_obs(
        obs, [obs["private"], adapter.agent_private_stub()])

    heads, _v = model.apply(params, *[A._flat(x) for x in jax_obs.encode(state)])
    masks = A.masks_for(state)
    probs = np.asarray(jax.nn.softmax(
        jnp.where(masks["op"], heads["op"], -jnp.inf), axis=-1))[0, 0]

    legal = np.asarray(masks["op"])[0, 0]
    non_noop = probs.copy()
    non_noop[O.NOOP] = 0.0
    return float(probs[O.NOOP]), float(non_noop.max()), int(legal.sum())


def plays(checkpoint):
    """Final bank against `starter`, plus the op census."""
    from kaggle_environments import make
    from kagg.agents import neural

    agent = neural.make_agent(checkpoint)
    ops = Counter()

    def spy(obs, config=None):
        act = agent(obs, config)
        for u in [act["farmer"]] + list(act["hands"]):
            ops[u[0]] += 1
        return act

    env = make("kaggriculture", configuration={"seed": 4000}, debug=False)
    env.run([spy, "starter"])
    return env.steps[-1][0]["reward"], ops


def main():
    ckpt = sys.argv[1] if len(sys.argv) > 1 else "data/bc/bc.pkl"
    p_noop, p_move, n_legal = spawn_distribution(ckpt)
    bank, ops = plays(ckpt)

    print(f"checkpoint {ckpt}")
    print(f"  spawn state: {n_legal} legal ops, P(noop) {p_noop:.6f}, "
          f"best non-noop {p_move:.6f}")
    print(f"  plays: ${bank:,.0f} vs starter   ops {dict(ops.most_common(6))}")
    print()

    prior_ok = p_noop <= MAX_SPAWN_NOOP and p_move >= MIN_SPAWN_MOVE
    plays_ok = bank > 3000.0

    print(f"  [{'PASS' if prior_ok else 'FAIL'}] usable as KL prior / init "
          f"(needs P(noop) <= {MAX_SPAWN_NOOP}, P(best move) >= {MIN_SPAWN_MOVE})")
    print(f"  [{'PASS' if plays_ok else 'FAIL'}] plays at all "
          f"(banking exactly $3,000 means it never acted)")

    if not prior_ok:
        print("\n  Do NOT wire this into --kl-prior or --init. As a prior it would tax PPO for "
              "moving at the state it visits most.")
    return 0 if prior_ok else 1


if __name__ == "__main__":
    sys.exit(main())
