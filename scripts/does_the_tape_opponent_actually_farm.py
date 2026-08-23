"""Does a replayed tape opponent farm, or does it stall into no-ops?

`ROLE_TAPE` pastes a downloaded player's recorded action into a seat by TURN INDEX. The board it
lands on is not the board that action was recorded on, and every refused action pushes the two
further apart -- so the replay can spiral into a seat that does nothing.

**What would have to be true for the role to be worth having.** Its whole justification is that the
heuristic opponents cap at $30,292 while the ladder is decided at $130k-$180k. So a replayed seat
has to bank real money. If it ends a season near its $3,000 opening bank it is a WEAKER opponent
than the heuristics it was meant to replace, and the role is worthless however well the splice is
masked.

The seat plays alone -- the other seat passes -- so this measures the replay itself with no
opponent interference. That makes it the friendliest possible case: on a contested market it can
only do worse.

    python -u scripts/does_the_tape_opponent_actually_farm.py --n 8
"""
import argparse
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

BANDS = ((0, 10), (10, 20), (20, 30))       # day ranges reported separately


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tapes", default=str(REPO / "data/il/opponent_tape_actions.npz"))
    ap.add_argument("--vocab", default=str(REPO / "data/il/bundle_vocab_teacher.json"))
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--turns", type=int, default=719)
    args = ap.parse_args()

    import jax.numpy as jnp
    from kagg.il import market_bundles as MB
    from kagg.rl import jax_act as A, jax_policy as P
    from kagg.sim import jax_sim as J
    from kagg.sim import ops as O

    npz = np.load(args.tapes)
    names = [str(x) for x in npz["names"]]
    tape = {k: jnp.asarray(npz[k]) for k in npz.files
            if k != "names" and not k.startswith("w_")}
    batch = min(args.n, tape["op"].shape[0])

    vocab = MB.load_vocab(args.vocab)
    sells = MB.valid_table(vocab, pad_to=P.N_BUNDLES)
    tables = {k: jnp.asarray(v) for k, v in MB.tables(vocab, pad_to=P.N_BUNDLES).items()}

    state = J.reset(batch)
    ids = jnp.arange(batch)
    n_units = tape["op"].shape[2]

    refused = np.zeros((batch, len(BANDS)))
    attempted = np.zeros((batch, len(BANDS)))
    noops = np.zeros(batch)
    slots = np.zeros(batch)

    print("tapes: %d of %d, %d turns, seat 1 passes every turn"
          % (batch, tape["op"].shape[0], args.turns), flush=True)

    for t in range(args.turns):
        picked = {h: v[ids, min(t, v.shape[1] - 1)] for h, v in tape.items()}

        # Seat 0 replays the tape; seat 1 is all-zeros, which is NOOP everywhere and the empty
        # bundle -- the "idle" opponent the trainer already documents.
        flat = {}
        for head, v in picked.items():
            pad = jnp.zeros_like(v)
            flat[head] = jnp.stack([v, pad], axis=1).reshape((batch * 2,) + v.shape[1:])

        masks = A.masks_for(state, sells)
        m_op = A._unflat(masks["op"], batch)[:, 0]                       # [B, units, ops]
        legal = np.asarray(
            jnp.take_along_axis(m_op, picked["op"][..., None], axis=-1)[..., 0])
        op = np.asarray(picked["op"])
        tried = op != O.NOOP
        day = t // J.TURNS_PER_DAY
        band = next(i for i, (lo, hi) in enumerate(BANDS) if lo <= day < hi)
        refused[:, band] += (tried & ~legal).sum(axis=1)
        attempted[:, band] += tried.sum(axis=1)
        noops += (~tried).sum(axis=1)
        slots += n_units

        state = J.step(state, A.to_sim_actions(flat, batch, tables))

    money = np.asarray(J.money(state))[:, 0]
    print()
    print("%-22s %10s %10s %10s %10s %10s %8s"
          % ("tape", "bank", "profit", "refused d0-9", "d10-19", "d20-29", "noop%"))
    pct = lambda a, b: ("%.1f%%" % (100.0 * a / b)) if b else "   -  "    # noqa: E731
    for i in range(batch):
        print("%-22s %10.0f %10.0f %10s %10s %10s %8s"
              % (names[i][:22], money[i], money[i] - 3000.0,
                 pct(refused[i, 0], attempted[i, 0]),
                 pct(refused[i, 1], attempted[i, 1]),
                 pct(refused[i, 2], attempted[i, 2]),
                 pct(noops[i], slots[i])))
    print()
    print("median bank %.0f, median profit %.0f over %d tapes"
          % (np.median(money), np.median(money) - 3000.0, batch))
    print("A heuristic `farm` opponent banks $30,292 and a real recorded season banks $130k-$180k.")


if __name__ == "__main__":
    main()
