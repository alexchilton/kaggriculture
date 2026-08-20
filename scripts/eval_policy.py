"""Score a trained checkpoint against opponents that are not itself.

**Self-play win rate is 0.5 by construction and measures nothing.** Both seats share parameters, so
every game produces one winner and one loser whatever the policy does. A run can therefore look
perfectly healthy while learning nothing, or while both sides quietly converge on a safe mutual
draw -- 0.5 is a fine outcome when your opponent is a mirror, and no gradient pushes against it.
This is the Orbit Wars "measurement before theory" lesson: build the thing that can say *no*.

Two opponents, and they answer different questions:

- **random-legal** -- a floor. Anything that has learned to farm at all should beat it comfortably.
  Failing here means the policy is not playing the game, and no amount of further training helps.
- **frozen checkpoints** -- the honest progress measure. Beating your own past self is the only
  self-play signal that cannot be produced by both sides agreeing to stand still.

Both seats are always played, and every seed is played twice with seats swapped: `_process_market`
quotes both players against the same inventory but commits in seat order, so seat 0 has a real edge
on contested trades. Reporting a one-seated result would flatter or damn the policy for free.
"""

import argparse
import pathlib
import pickle

import jax
import jax.numpy as jnp
import numpy as np

from kagg.rl import jax_act as A, jax_masks, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J


# The bundle legality mask needs the vocabulary. It is loaded once here rather than threaded through
# every signature: the vocabulary is a global property of a trained model, like a tokenizer, and it
# must be byte-identical across labelling, fitting and play or every bundle index means something
# different. `market_bundles.load_vocab` raises if it is missing rather than inventing one.
_BUNDLE_SELLS = None


def _bundle_sells():
    global _BUNDLE_SELLS
    if _BUNDLE_SELLS is None:
        from kagg.il import market_bundles as _MB
        from kagg.rl import jax_policy as _PP
        _BUNDLE_SELLS = _MB.sell_table(_MB.load_vocab(), pad_to=_PP.N_BUNDLES)
    return _BUNDLE_SELLS


EPISODE_TURNS = 719


def load_params(path):
    with pathlib.Path(path).open("rb") as fh:
        ck = pickle.load(fh)
    return ck["params"], ck.get("args", {}), ck.get("update", -1)


def _greedy(heads, masks):
    """Argmax over legal options. Evaluation should not add sampling noise to the score."""
    out = {}
    for k in A.ALL_HEADS:
        logits = P._masked_logits(heads[k], masks[k])
        out[k] = jnp.argmax(logits, axis=-1)
    return out


def random_legal_actions(key, state):
    """Uniform over *legal* options -- the floor a real policy must clear.

    Uniform-over-legal is a much stronger floor than uniform-over-all: it never wastes a turn on an
    illegal op, so it moves, waters and harvests by accident at a reasonable rate.
    """
    masks = A.masks_for(state, _bundle_sells())
    keys = jax.random.split(key, len(A.ALL_HEADS))
    out = {}
    for k, sub in zip(A.ALL_HEADS, keys):
        logits = jnp.zeros(masks[k].shape, dtype=jnp.float32)
        out[k] = P.sample_head(sub, logits, masks[k])[0]
    return out


def play(params_a, params_b, model, batch, key, greedy=True, swap=False):
    """Play `batch` games. Returns per-game final money `[B, 2]`.

    A takes seat 0 and B seat 1, unless `swap`, which puts A in seat 1. `params_b = None` means the
    random-legal opponent.

    `swap` exists because the seating is worth real money: `_process_market` quotes both players
    against the same inventory but commits in seat order, so seat 0 wins every contested trade tie.
    Reporting one seating flatters or damns a policy for free. The first version of this script had
    a `swap` that only applied when the opponent was another checkpoint, so every random-legal
    evaluation silently measured seat 0 twice and printed the same number under two labels.
    """
    # `reset_with_shops`: a plain reset freezes every shop, cutting the town's season wheat demand
    # from ~700 units to 140 and every tail sale price by 27-38%. An evaluation in that market is
    # not an evaluation of the game the submission plays.
    state = J.reset_with_shops(batch)

    def one_turn(carry, _):
        state, key = carry
        key, ka, kb = jax.random.split(key, 3)

        tiles, units, glob = jax_obs.encode(state)
        masks = A.masks_for(state, _bundle_sells())

        heads_a, _ = model.apply(params_a, A._flat(tiles), A._flat(units), A._flat(glob))
        act_a = _greedy(heads_a, masks) if greedy else A.sample(ka, heads_a, masks)[0]

        if params_b is None:
            act_b = random_legal_actions(kb, state)
        else:
            heads_b, _ = model.apply(params_b, A._flat(tiles), A._flat(units), A._flat(glob))
            act_b = _greedy(heads_b, masks) if greedy else A.sample(kb, heads_b, masks)[0]

        # Each player supplies the column of the seat it occupies. Both sets were computed over the
        # full [B, P] batch, so this is a column select, not a re-run.
        merged = {}
        for k in A.ALL_HEADS:
            a = act_a[k].reshape(batch, 2, *act_a[k].shape[1:])
            b = act_b[k].reshape(batch, 2, *act_b[k].shape[1:])
            first, second = (b, a) if swap else (a, b)
            merged[k] = jnp.concatenate([first[:, :1], second[:, 1:]], axis=1).reshape(
                batch * 2, *act_a[k].shape[1:])

        sim_actions = A.to_sim_actions(merged, batch)
        return (J.step(state, sim_actions), key), None

    (final, _key), _ = jax.lax.scan(one_turn, (state, key), None, length=EPISODE_TURNS)
    return final.farm.money


def score(money):
    """Win rate for seat 0, counting a tie as half."""
    a, b = np.asarray(money)[:, 0], np.asarray(money)[:, 1]
    return float(((a > b).sum() + 0.5 * (a == b).sum()) / len(a))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checkpoint")
    ap.add_argument("--vs", default=None, help="another checkpoint; omit to play random-legal")
    ap.add_argument("--games", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sample", action="store_true", help="sample instead of argmax")
    args = ap.parse_args()

    params, cfg, update = load_params(args.checkpoint)
    model = P.Policy(d_model=cfg.get("d_model", 128), n_heads=cfg.get("heads", 4),
                     n_layers=cfg.get("layers", 3))
    other = load_params(args.vs)[0] if args.vs else None

    print(f"checkpoint: {args.checkpoint} (update {update})")
    print(f"opponent:   {args.vs or 'random-legal'}")
    print(f"games:      {args.games} per seating, {2 * args.games} total")

    key = jax.random.PRNGKey(args.seed)
    k1, k2 = jax.random.split(key)

    # Both seatings, always -- including against random-legal, where `swap` is what actually moves
    # the policy into seat 1 rather than replaying seat 0 under a different key.
    m1 = play(params, other, model, args.games, k1, greedy=not args.sample, swap=False)
    wr_seat0 = score(m1)

    m2 = play(params, other, model, args.games, k2, greedy=not args.sample, swap=True)
    # With `swap`, the policy is in seat 1, so its win rate is the complement of seat 0's score.
    wr_seat1 = 1.0 - score(m2)

    own = np.concatenate([np.asarray(m1)[:, 0], np.asarray(m2)[:, 1]])
    opp = np.concatenate([np.asarray(m1)[:, 1], np.asarray(m2)[:, 0]])
    print(f"\nwin rate as seat 0: {wr_seat0:.3f}")
    print(f"win rate as seat 1: {wr_seat1:.3f}")
    print(f"overall:            {(wr_seat0 + wr_seat1) / 2:.3f}")
    print(f"policy bank:        mean ${own.mean():,.0f}  max ${own.max():,.0f}")
    print(f"opponent bank:      mean ${opp.mean():,.0f}  max ${opp.max():,.0f}")
    print(f"starting money was $3,000 -- a policy below that is destroying value, and a win over an "
          f"opponent who destroys more is not evidence of skill.")


if __name__ == "__main__":
    main()
