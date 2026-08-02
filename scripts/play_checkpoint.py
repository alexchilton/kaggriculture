"""Play a trained checkpoint against the in-sim scripted farmer and show what it actually does.

**Why this exists, when `eval_policy.py` already scores checkpoints.** `eval_policy.py` reports a
single win rate against random-legal or another checkpoint, and a win rate counts a tie as half.
That is exactly the ambiguity that matters right now: the training log showed `farm:0.445/91x`,
which reads as "wins nearly half its games against the farmer" and is equally consistent with
"draws almost everything". A rate cannot separate those two; a win/draw/loss decomposition can, and
a money curve shows *why*.

So this prints three things a rate cannot:

- **W/D/L counts, not a rate.** A draw in this game means `money == money` exactly, which is what
  two passive players sitting on their $3,000 start produce. If the draws dominate, the policy has
  found the mutual-standstill equilibrium rather than learned to farm.
- **The money curve, per game-day.** A farmer that plants, waters and harvests has a rising bank; a
  policy that banks its opening $3,000 and stops has a flat line. These are indistinguishable in
  any end-of-episode scalar and obvious in five numbers.
- **An op census over a whole season**, on the policy's own seat only, for the same reason
  `train_jax_rl.py` counts `live_units` rather than every slot.

Both seatings are always played. `_process_market` quotes both players against the same inventory
but commits in seat order, so seat 0 wins every contested tie -- reporting one seating flatters or
damns a policy for free, which `eval_policy.py`'s docstring already records as a bug it once had.

    .venv/bin/python scripts/play_checkpoint.py data/.../latest.pkl --games 32
"""

import argparse
import pathlib
import pickle

import jax
import jax.numpy as jnp
import numpy as np

from kagg.rl import jax_act as A, jax_heuristic as HEUR, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

# 719, matching `train_jax_rl.py:81` and `eval_policy.py:32`. 720 runs one turn past natural
# termination into a day the 30-day season does not define -- the same species as the already-fixed
# "episode ran into a season that does not exist", reintroduced in one turn of 720.
EPISODE_TURNS = 719
OP_NAMES = ("NOOP", "N", "S", "E", "W", "WATER", "HARV", "PLANT", "DIG",
            "PICKUP", "DROP", "PLACE", "FEED", "CARE", "COLLFERT", "FERTIL",
            "COOP", "PASTURE")


def _greedy(heads, masks):
    """Argmax over legal options, **conditioning on `trade` and `op` first**.

    `sell` and `buy_product` carry a `[.., N_PRODUCTS, N_TRADE_MODES, K]` axis and
    `crop`/`item`/`qty` a `[.., MAX_UNITS, N_OPS, K]` one, so neither can be masked or argmaxed
    until its conditioning variable has been chosen -- `A.condition_all` is what collapses those
    axes. `eval_policy.py:41` still argmaxes the raw heads and therefore cannot run at all; that
    predates this change and is still open.

    Note the greedy decode is exactly what `CLAUDE.md` records as emitting **zero** market orders,
    because nine independent "probably not sell" marginals compose into "never sell". Conditioning
    fixes the joint, not that per-product argmax bias, so read the market rows of a greedy
    playthrough with that in mind. Sampling is the default for exactly this reason.
    """
    cond = {k: jnp.argmax(P._masked_logits(heads[k], masks[k]), axis=-1)
            for k in A.CONDITION_HEADS}
    conditioned = A.condition_all(heads, cond)
    out = {k: jnp.argmax(P._masked_logits(conditioned[k], masks[k]), axis=-1)
           for k in A.ALL_HEADS}
    out["trade"] = cond["trade"]
    return out


def play(params, model, batch, key, swap, greedy=False, turns=EPISODE_TURNS):
    """Policy vs the scripted farmer for a full season.

    Returns `(money [B, 2], money_trace [DAYS, B, 2], op_counts [N_OPS], unit_turns)`.
    The policy holds seat 0 unless `swap`. Op counts cover the policy's seat and its *live* units
    only -- `MAX_UNITS` is 24 against a crew of a few, so counting every slot is the padding
    mistake `train_jax_rl.py` already made twice.
    """
    state = J.reset(batch)
    seat = 1 if swap else 0

    def one_turn(carry, _):
        state, key = carry
        key, ka = jax.random.split(key)

        tiles, units, glob = jax_obs.encode(state)
        masks = A.masks_for(state)
        heads, _ = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
        act = _greedy(heads, masks) if greedy else A.sample(ka, heads, masks)[0]

        sim_actions = A.to_sim_actions(act, batch)
        heur = HEUR.actions(state)

        # The farmer takes whichever seat the policy does not.
        seats = jnp.arange(2)[None, :]
        theirs = jnp.broadcast_to(seats != seat, (batch, 2))
        sim_actions = jax.tree_util.tree_map(
            lambda mine, other: jnp.where(
                theirs.reshape(theirs.shape + (1,) * (mine.ndim - 2)), other, mine),
            sim_actions, heur)

        nxt = J.step(state, sim_actions)

        live = jax_obs.encode(state)[1][..., 0].reshape(batch, 2, -1) > 0.5
        ops = act["op"].reshape(batch, 2, -1)
        mine = jnp.zeros((batch, 2), dtype=bool).at[:, seat].set(True)
        counted = live & mine[..., None]
        counts = (jax.nn.one_hot(ops, O.N_OPS, dtype=jnp.float32)
                  * counted[..., None]).sum(axis=(0, 1, 2))
        return (nxt, key), (nxt.farm.money, counts, counted.sum())

    (final, _), (money_t, counts_t, unit_t) = jax.lax.scan(
        one_turn, (state, key), None, length=turns)
    # One sample per game-day rather than per turn, which is the unit a human reads.
    trace = money_t[::J.TURNS_PER_DAY]
    return final.farm.money, trace, counts_t.sum(axis=0), float(unit_t.sum())


def report(money, swap):
    """W/D/L from the policy's side, plus the banks. A tie is `money == money` exactly."""
    m = np.asarray(money)
    me = m[:, 1] if swap else m[:, 0]
    them = m[:, 0] if swap else m[:, 1]
    w = int((me > them).sum())
    d = int((me == them).sum())
    ll = int((me < them).sum())
    return w, d, ll, me, them


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checkpoint")
    ap.add_argument("--games", type=int, default=32)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--greedy", action="store_true",
                    help="decode with per-head argmax instead of sampling. NOT the default any "
                         "more, and the reason is measured: on the same checkpoint, greedy emitted "
                         "WATER 0%%, PLANT 0%%, HARVEST 0%%, raw FEED 0 and a bank of exactly $2,998 "
                         "in all 32 games (zero variance), while sampling gave WATER 5.62%%, PLANT "
                         "2.50%%, HARVEST 0.76%% and raw FEED 18. The marginals contain the "
                         "behaviour; argmax over independent per-head marginals destroys it, which "
                         "is the same mechanism CLAUDE.md records for market orders -- nine "
                         "independent 'probably not' decisions compose into 'never'. So argmax is "
                         "not a cleaner score, it is a score of a different and much worse policy. "
                         "Kept only for reproducing that comparison.")
    ap.add_argument("--sample", action="store_true",
                    help="deprecated no-op; sampling is now the default")
    args = ap.parse_args()

    with pathlib.Path(args.checkpoint).open("rb") as fh:
        ck = pickle.load(fh)
    saved = ck.get("args", {})
    # The checkpoint stores `args`, whose names are the CLI's (`heads`, `layers`), while the module
    # fields are `n_heads`/`n_layers`. `eval_policy.py:128` does the same translation.
    model = P.Policy(d_model=saved.get("d_model", 128),
                     n_heads=saved.get("heads", 4),
                     n_layers=saved.get("layers", 3))
    # Pre-op-axis checkpoints are tiled onto the current argument heads rather than refused --
    # replaying the old ones is the whole point of this script, and refusing them would make every
    # result before the op axis unreproducible. See `jax_policy.migrate_params`.
    _s = J.reset(1)
    _t, _u, _g = jax_obs.encode(_s)
    _template = model.init(jax.random.PRNGKey(0), A._flat(_t), A._flat(_u), A._flat(_g))
    params = jax.device_put(P.load_or_migrate(ck["params"], _template))
    print(f"checkpoint {args.checkpoint}")
    print(f"  saved at update {ck.get('update')}   games {args.games} per seating\n")

    key = jax.random.PRNGKey(args.seed)
    for swap in (False, True):
        key, sub = jax.random.split(key)
        money, trace, counts, unit_turns = play(
            params, model, args.games, sub, swap, greedy=args.greedy)
        w, d, ll, me, them = report(money, swap)
        seat = 1 if swap else 0
        print(f"--- policy in seat {seat} vs scripted farmer ---")
        print(f"  W/D/L      {w} / {d} / {ll}      "
              f"(win rate counting a tie as half: {(w + 0.5 * d) / len(me):.3f})")
        print(f"  policy $   median {np.median(me):>10,.0f}   mean {me.mean():>10,.0f}   "
              f"min {me.min():>8,.0f}   max {me.max():>9,.0f}")
        print(f"  farmer $   median {np.median(them):>10,.0f}   mean {them.mean():>10,.0f}")

        t = np.asarray(trace)[:, :, seat]
        days = [0, 5, 10, 15, 20, 25, 29]
        print("  policy bank by day  "
              + "  ".join(f"d{d_}:{np.median(t[d_]):,.0f}" for d_ in days if d_ < len(t)))
        tf = np.asarray(trace)[:, :, 1 - seat]
        print("  farmer bank by day  "
              + "  ".join(f"d{d_}:{np.median(tf[d_]):,.0f}" for d_ in days if d_ < len(tf)))

        c = np.asarray(counts)
        total = max(1.0, unit_turns)
        top = np.argsort(-c)[:9]
        print("  ops (share of the policy's own live-unit actions)")
        print("    " + "  ".join(f"{OP_NAMES[i]}:{c[i] / total:.2%}" for i in top))
        print(f"    FEED:{c[O.FEED] / total:.4%}  CARE:{c[O.CARE] / total:.4%}  "
              f"HARV:{c[O.HARVEST] / total:.4%}  raw FEED count {c[O.FEED]:,.0f}\n")


if __name__ == "__main__":
    main()
