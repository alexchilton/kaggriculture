"""Do `jax_sim.State` and a reference observation encode to the SAME tensors at turn 0?

    python -u scripts/diff_the_two_ways_a_board_becomes_features.py

THE QUESTION
------------
`pinned_round27.pkl` banks $126k-$150k in the reference environment and spends its entire $3,000 on
TURN 0 in `jax_sim` under greedy decode (`docs/the_clone_dumps_its_bank_on_turn_zero_in_jax_sim_2026-08-28.md`).
The network is the same, the vocabulary is asserted, the commit layer is included. So the difference
is one of the two bridges, and this measures the first one directly.

**No policy is involved.** Every kaggriculture game starts from a byte-identical board -- same
tiles, NW quadrant only, $3,000, no shops (`jax_sim.reset`, and `project_kaggriculture_start_state_is_fixed`).
So `jax_sim`'s turn-0 state and the reference env's turn-0 observation describe the SAME game, and
their encodings must be equal element for element. Any difference is a bug in one of the two paths,
not a modelling question:

    path A   jax_sim.reset_with_shops(1)                      -> jax_obs.encode
    path B   reference env reset -> obs -> adapter.state_from_obs -> jax_obs.encode

**Why this is not covered.** The 300/300 full-length parity gate compares the SIMULATOR against the
reference. It never encodes anything. `CLAUDE.md`: *a gate only tests what it exercises* -- and this
is the fourth time that lesson has been paid for here.

A clean match sends the search to the ACTION bridge (`jax_act.to_sim_actions`, the `qty_*` heads and
`MAX_QTY`). A mismatch names the field.
"""
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

CKPT = REPO / "data/dagger_tape/season_fast-20260822-235031/pinned_round27.pkl"


def main():
    import jax.numpy as jnp
    from kagg.rl import adapter as AD, jax_obs
    from kagg.sim import jax_sim as J
    from kaggle_environments import make

    # ---- path A: native jax_sim ------------------------------------------------------
    sim = J.reset_with_shops(1, seed=0)
    a_tiles, a_units, a_glob = (np.asarray(x) for x in jax_obs.encode(sim))

    # ---- path B: reference env, through the adapter -----------------------------------
    env = make("kaggriculture", debug=False)
    env.reset(2)
    obs = env.state[0].observation
    privates = [obs["private"], AD.agent_private_stub()]
    st = AD.state_from_obs(obs, privates, step=0)
    b_tiles, b_units, b_glob = (np.asarray(x) for x in jax_obs.encode(st))

    print(f"{'tensor':<10}{'A shape':>18}{'B shape':>18}{'equal':>8}{'max |diff|':>14}")
    bad = []
    for name, a, b in (("tiles", a_tiles, b_tiles), ("units", a_units, b_units),
                       ("glob", a_glob, b_glob)):
        if a.shape != b.shape:
            print(f"{name:<10}{str(a.shape):>18}{str(b.shape):>18}{'SHAPE':>8}{'':>14}")
            bad.append(name)
            continue
        same = np.allclose(a, b, atol=1e-5)
        d = float(np.max(np.abs(a - b))) if a.size else 0.0
        print(f"{name:<10}{str(a.shape):>18}{str(b.shape):>18}{str(same):>8}{d:>14.4f}")
        if not same:
            bad.append(name)

    for name, a, b in (("tiles", a_tiles, b_tiles), ("units", a_units, b_units),
                       ("glob", a_glob, b_glob)):
        if name not in bad or a.shape != b.shape:
            continue
        diff = np.abs(a - b)
        print(f"\n  {name}: {int((diff > 1e-5).sum())} differing elements of {diff.size}")
        # **Report WHERE, not just how much.** An earlier version printed element [0] of the
        # flattened tensor next to the max |diff| taken over the whole thing, so it showed two
        # IDENTICAL values beside a difference of 1.0 -- unreadable, and it invites a verdict the
        # data does not support. `units` is [B, P, SLOT, FEAT] and only slot 0 is alive at turn 0,
        # so which SLOT differs is the whole question: padding the network masks is harmless, the
        # live slot is not.
        idx = np.argwhere(diff > 1e-5)
        if idx.size:
            axes = "BPSF" if a.ndim == 4 else "BPF"
            print(f"  {'index':<22}{'A':>12}{'B':>12}")
            for loc in idx[:20]:
                t = tuple(int(v) for v in loc)
                where = " ".join(f"{ax}{v}" for ax, v in zip(axes, t))
                print(f"  {where:<22}{a[t]:>12.4f}{b[t]:>12.4f}")
            if a.ndim == 4:
                slots = sorted({int(v[2]) for v in idx})
                print(f"  slots differing: {slots}")
                print(f"  feats differing: {sorted({int(v[3]) for v in idx})}")

    # ---- does the difference reach the ACTION? ----------------------------------------
    # A tensor difference in padding is only a bug if the network reads it. `live` (feature 0)
    # agrees between the two paths, so a policy that masks dead slots would be unaffected -- and
    # calling this the cause without checking is the mistake this file already made once tonight.
    if bad and CKPT.exists():
        import pickle

        from kagg.il import market_bundles as MB
        from kagg.rl import jax_act as A, jax_policy as P

        with CKPT.open("rb") as fh:
            ckpt = pickle.load(fh)
        vpath = REPO / "data/il/bundle_vocab_teacher_pre_topup.json"
        import json as _json
        vocab = MB.Vocabulary.from_bundles(
            [tuple(tuple(p) for p in b) for b in _json.loads(vpath.read_text())], max_size=None)
        bundle_ok = jnp.asarray(MB.valid_table(vocab, pad_to=P.N_BUNDLES))
        ca = ckpt.get("args") or {}
        model = P.Policy(d_model=ca.get("d_model", 128), n_heads=ca.get("heads", 4),
                         n_layers=ca.get("layers", 3))

        def act_of(tiles, units, glob, state):
            heads, _v = model.apply(ckpt["params"], A._flat(jnp.asarray(tiles)),
                                    A._flat(jnp.asarray(units)), A._flat(jnp.asarray(glob)))
            masks = A.masks_for(state, bundle_ok)
            cond = {k: jnp.argmax(P._masked_logits(heads[k], masks[k]), axis=-1)
                    for k in A.CONDITION_HEADS}
            cnd = A.condition_all(heads, cond)
            return {k: np.asarray(jnp.argmax(P._masked_logits(cnd[k], masks[k]), axis=-1))
                    for k in A.ALL_HEADS}

        # Same masks (built from the jax_sim state) both times, so ONLY the input tensors vary.
        ga = act_of(a_tiles, a_units, a_glob, sim)
        gb = act_of(b_tiles, b_units, b_glob, sim)
        print(f"\n  turn-0 action from each encoding (same weights, same masks)")
        print(f"  {'head':<18}{'from jax_sim':>16}{'from adapter':>16}{'same':>8}")
        for k in A.ALL_HEADS:
            va, vb = ga[k].ravel(), gb[k].ravel()
            print(f"  {k:<18}{str(va[:4]):>16}{str(vb[:4]):>16}"
                  f"{str(bool(np.array_equal(va, vb))):>8}")
        if all(np.array_equal(ga[k], gb[k]) for k in A.ALL_HEADS):
            print("  -> the padding difference does NOT change the turn-0 action. Look elsewhere.")
        else:
            print("  -> the padding difference DOES change the turn-0 action.")

    print("\nVERDICT")
    if not bad:
        print("  OBSERVATION BRIDGE IS CLEAN at turn 0. The turn-0 spend is the ACTION bridge:")
        print("  jax_act.to_sim_actions, the qty_* heads, MAX_QTY, or the bundle tables.")
    else:
        print(f"  OBSERVATION BRIDGE DIFFERS in {bad}. The clone is looking at a different game in")
        print("  jax_sim than the one it was trained on, and no RL setting repairs that.")


main()
