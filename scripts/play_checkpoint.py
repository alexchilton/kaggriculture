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

from kagg.rl import (commit as CM, jax_act as A, jax_carrot as CARROT,
                     jax_heuristic as HEUR, jax_obs, jax_policy as P, jax_rancher as RANCH)

# **Which opponent the replay is run against, because it only ever ran one.**
#
# The script played the scripted farmer and nothing else, so 'what does the policy actually do'
# was answerable against one opponent out of five -- and that one takes it to $0, which reads as
# a total collapse until you notice `eval_policy` shows it keeping ~$1,100 against another
# policy. Same behaviour, different opponent, opposite conclusion. The informative opponents are
# the ones whose bank is NEAR ours: idle holds $3,000 and carrot banks $3,410, against a policy
# that manages ~$1,100, while the farmer's $30,292 is unreachable and tells us only that it is
# unreachable.
OPPONENTS = {
    'farm': HEUR.actions,      # $23,783-$30,292 -- the ceiling reference
    'carrot': CARROT.actions,  # $3,410 -- just above us, so near maximum outcome variance
    'ranch': RANCH.actions,    # $12,078 -- the animal economy
    'idle': None,              # holds its opening $3,000 by passing every turn
}
from kagg.sim import jax_sim as J
from kagg.sim import ops as O


# The bundle legality mask needs the vocabulary. It is loaded once here rather than threaded through
# every signature: the vocabulary is a global property of a trained model, like a tokenizer, and it
# must be byte-identical across labelling, fitting and play or every bundle index means something
# different. `market_bundles.load_vocab` raises if it is missing rather than inventing one.
#
# **It must NOT default silently, which it did until 2026-08-23.** `load_vocab()` with no argument
# takes `DEFAULT_VOCAB = data/il/bundle_vocab.json` (197 entries), while every run since the DAgger
# teacher work uses `data/il/bundle_vocab_teacher.json` (151). Playing a teacher-vocab checkpoint
# through the 197-entry table decodes every market order into a different order -- and nothing
# raises, because every index is still a valid index. The output looks entirely plausible and is
# meaningless. `--vocab` is required for that reason: an assumed tokenizer is not a default, it is a
# silent corruption, and this script's own docstring above says so one paragraph earlier.
_BUNDLE_SELLS = None
_BUNDLE_TABLES = None
_VOCAB_PATH = None


def _set_vocab(path):
    global _VOCAB_PATH, _BUNDLE_SELLS, _BUNDLE_TABLES
    _VOCAB_PATH, _BUNDLE_SELLS, _BUNDLE_TABLES = path, None, None


def _vocab():
    from kagg.il import market_bundles as _MB
    return _MB.load_vocab(_VOCAB_PATH) if _VOCAB_PATH else _MB.load_vocab()


def _bundle_sells():
    global _BUNDLE_SELLS
    if _BUNDLE_SELLS is None:
        from kagg.rl import jax_policy as _PP
        from kagg.il import market_bundles as _MB
        _BUNDLE_SELLS = _MB.valid_table(_vocab(), pad_to=_PP.N_BUNDLES)
    return _BUNDLE_SELLS


def _bundle_tables():
    """The decode tables `jax_act.to_sim_actions` needs: bundle index -> which orders go out.

    **This script had not been run since the argument was added.** `to_sim_actions` gained its third
    parameter in `f75174e` (2026-08-22) and every call here still passed two, so the first traced
    turn died with `missing 1 required positional argument: 'tables'`. `train_jax_rl.py:99` carries
    the identical note about itself; `eval_policy.py` and `diagnose_policy.py` are still broken the
    same way and are NOT fixed here.

    Padded to the head width for the reason `market_bundles.tables` gives -- JAX clamps an
    out-of-range gather under jit rather than raising, so an unpadded table returns a real,
    confidently-emitted, wrong order.
    """
    global _BUNDLE_TABLES
    if _BUNDLE_TABLES is None:
        import jax.numpy as _jnp
        from kagg.il import market_bundles as _MB
        from kagg.rl import jax_policy as _PP
        _BUNDLE_TABLES = {k: _jnp.asarray(v) for k, v in
                          _MB.tables(_vocab(), pad_to=_PP.N_BUNDLES).items()}
    return _BUNDLE_TABLES


# 719, matching `train_jax_rl.py:81` and `eval_policy.py:32`. 720 runs one turn past natural
# termination into a day the 30-day season does not define -- the same species as the already-fixed
# "episode ran into a season that does not exist", reintroduced in one turn of 720.
EPISODE_TURNS = 719
OP_NAMES = ("NOOP", "N", "S", "E", "W", "WATER", "HARV", "PLANT", "DIG",
            "PICKUP", "DROP", "PLACE", "FEED", "CARE", "COLLFERT", "FERTIL",
            "COOP", "PASTURE")
# **Op counts are taken AFTER commitments resolve, so they describe what the units did.**
# A `COMMIT_*` token is a decision, not an action: the turns it produces are ordinary moves and one
# arrival op. Counting the tokens instead would report a policy that "does COMMIT_FEED 5% of the
# time" while the animals starve, which is the same species of lie as counting submitted ops rather
# than ops that took effect.
COMMIT_NAMES = ("cWATER", "cHARV", "cFEED", "cPLANT", "cPICKUP")


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


def play(params, model, batch, key, swap, greedy=False, turns=EPISODE_TURNS,
         opponent_fn=None, frozen_town=False):
    """Policy vs the scripted farmer for a full season.

    Returns `(money [B, 2], money_trace [DAYS, B, 2], op_counts [N_OPS], unit_turns)`.
    The policy holds seat 0 unless `swap`. Op counts cover the policy's seat and its *live* units
    only -- `MAX_UNITS` is 24 against a crew of a few, so counting every slot is the padding
    mistake `train_jax_rl.py` already made twice.
    """
    # Built eagerly, OUTSIDE the scan. Calling `_bundle_tables()` from inside `one_turn` builds the
    # arrays under the trace and leaks a tracer out of the cache -- the same fault that had to be
    # fixed in `train_jax_rl.py:392`.
    tables = _bundle_tables()

    # `reset_with_shops`, not `reset`: a plain reset never opens a shop, so the town drains 140 wheat
    # a season instead of ~700 and end-of-season wheat prices at $37 against the real $51. The
    # money-flow decomposition this script produces is the input to P4's "the farm runs at a loss"
    # finding, and it was pricing the sell side ~30% low at the tail while the buy side is mostly
    # fixed shop prices.
    # `frozen_town=True` reproduces the pre-fix market -- every shop at `NEVER`, season wheat demand
    # 140 units against the real ~700 -- so the A/B for that bug is one flag apart and the only
    # difference between the two runs is the market.
    state = J.reset(batch) if frozen_town else J.reset_with_shops(batch)
    seat = 1 if swap else 0

    def one_turn(carry, _):
        state, key, cmt = carry
        key, ka = jax.random.split(key)

        tiles, units, glob = jax_obs.encode(state)
        masks = A.masks_for(state, _bundle_sells())
        heads, _ = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
        act = _greedy(heads, masks) if greedy else A.sample(ka, heads, masks)[0]

        # Commitments resolve exactly as they do in training, or this replay would measure a
        # different agent than the one that was trained -- which is the whole reason this script
        # exists.
        u32 = lambda k: A._unflat(act[k], batch).astype(jnp.int32)   # noqa: E731
        sim_op, sim_crop, sim_item, sim_qty, cmt, _decided = CM.resolve(
            cmt, state, u32("op"), u32("crop"), u32("item"), u32("qty"))
        sim_actions = A.to_sim_actions(act, batch, tables)._replace(
            unit_op=sim_op.astype(J._I), unit_crop=sim_crop.astype(J._I),
            unit_item=sim_item.astype(J._I),
            unit_qty=P.UNIT_QTY_BUCKETS[sim_qty].astype(J._I))
        # `idle` is all-zeros: NOOP is op 0 and bucket 0 of every market head is quantity zero, so
        # a zeroed Actions IS the do-nothing agent -- no parameters, nothing to keep in sync.
        heur = (jax.tree_util.tree_map(jnp.zeros_like, sim_actions) if opponent_fn is None
                else opponent_fn(state))

        # The opponent takes whichever seat the policy does not.
        #
        # **`tree_map` alone is wrong here, and it raises rather than corrupting -- which is luck.**
        # A scripted opponent may leave a market field as `None` to mean ORDER_NONE, "this seat sends
        # no orders and falls back to the canonical book". `tree_map` then hands `jnp.where` a None
        # and it dies with `where requires ndarray or scalar arguments, got NoneType`. Substituting
        # zeros is the correct reading: bucket 0 of every market head IS quantity zero, so a zeroed
        # field is exactly "no order". `train_jax_rl.py` carries the identical fix as `_blend_seat`.
        seats = jnp.arange(2)[None, :]
        theirs = jnp.broadcast_to(seats != seat, (batch, 2))

        def _blend(mine, other):
            if other is None:
                other = jnp.zeros_like(mine)
            return jnp.where(theirs.reshape(theirs.shape + (1,) * (mine.ndim - 2)), other, mine)

        sim_actions = sim_actions._replace(**{
            f: _blend(getattr(sim_actions, f), getattr(heur, f)) for f in J.Actions._fields})

        # **Accounted, so the bank curve can be read as causes rather than levels.**
        # The per-game-day bank showed the farmer replay falling -21/day to day 10 and -552/day to
        # day 15 -- a cliff, and a policy converged on inaction cannot produce a cliff. A level
        # cannot say what happened; `acct` names every dollar. See `jax_sim.step_accounted`.
        nxt, acct = J.step_accounted(state, sim_actions)

        live = jax_obs.encode(state)[1][..., 0].reshape(batch, 2, -1) > 0.5
        # **The RESOLVED op, not the policy's token.** A `COMMIT_FEED` is a decision; what the unit
        # actually did that turn is a step or an arrival. Counting tokens would report a policy that
        # commits to feeding 5% of the time while every animal starves.
        ops = sim_op
        mine = jnp.zeros((batch, 2), dtype=bool).at[:, seat].set(True)
        counted = live & mine[..., None]
        counts = (jax.nn.one_hot(ops, O.N_OPS, dtype=jnp.float32)
                  * counted[..., None]).sum(axis=(0, 1, 2))
        # How often the policy chose to commit at all, so a replay can tell "never uses the
        # mechanism" from "uses it and it does not help".
        tok = act["op"].reshape(batch, 2, -1)
        commits = (jax.nn.one_hot(tok - O.N_OPS, CM.N_COMMIT, dtype=jnp.float32)
                   * counted[..., None]).sum(axis=(0, 1, 2))
        cmt_next = CM.clear_at_night(cmt, nxt)
        return (nxt, key, cmt_next), (nxt.farm.money, counts, counted.sum(), commits,
                                      acct["hire"], acct["land"], acct["trade"],
                                      acct["sell"], acct["buy"])

    (final, _, _), (money_t, counts_t, unit_t, commit_t,
                    hire_t, land_t, trade_t, sell_t, buy_t) = jax.lax.scan(
        one_turn, (state, key, CM.init(batch)), None, length=turns)
    trace = bank_by_day(money_t)
    acct_trace = {"hire": per_day_flow(hire_t, turns), "land": per_day_flow(land_t, turns),
                  "trade": per_day_flow(trade_t, turns), "sell": per_day_flow(sell_t, turns),
                  "buy": per_day_flow(buy_t, turns)}
    return (final.farm.money, trace, counts_t.sum(axis=0), float(unit_t.sum()),
            commit_t.sum(axis=0), acct_trace)


def n_game_days(turns):
    """Game-days spanned by `turns`, rounding **up**.

    `719 // 24` is 29 and the season is 30 days: the last one is a 23-turn tail. Flooring it is what
    made the last 23 turns of every game invisible in the flow table, while the bank kept moving --
    against `ranch` the trace read $388 at turn 696 and the true final was $6.
    """
    return -(-turns // J.TURNS_PER_DAY)


def per_day_flow(x, turns):
    """`[days, ...]` -- sum a per-turn *flow* into game-days, including the partial last day.

    Money movements are flows and must be summed over the day, not sampled at its boundary the way a
    bank level is; sampling a flow reports one turn's spend as a day's. The tail is zero-padded to a
    whole day so every turn lands in exactly one bucket -- `test_every_turn_lands_in_exactly_one_day_bucket`
    is the guard, because a reporting tool that silently drops turns prints numbers that are each
    true and a picture that is wrong.
    """
    n_days = n_game_days(turns)
    pad = n_days * J.TURNS_PER_DAY - x.shape[0]
    if pad:
        x = jnp.concatenate([x, jnp.zeros((pad,) + x.shape[1:], x.dtype)], axis=0)
    return x.reshape(n_days, J.TURNS_PER_DAY, *x.shape[1:]).sum(axis=1)


def bank_by_day(money_t):
    """`[days, ...]` -- the bank at the **end** of each game-day, final turn always included.

    Sampling `money_t[::TURNS_PER_DAY]` took day *starts*, so the last sample was turn 696 while the
    headline "policy $" is `final.farm.money` at turn 718. Two timestamps, presented side by side as
    though they were one, and the gap was $382 against `ranch` seat 0 and $3,216 against seat 1.
    """
    ends = jnp.arange(J.TURNS_PER_DAY - 1, money_t.shape[0], J.TURNS_PER_DAY)
    # The final turn closes the season whether or not it falls on a day boundary.
    last = money_t.shape[0] - 1
    idx = ends if int(ends[-1]) == last else jnp.concatenate([ends, jnp.asarray([last])])
    return money_t[idx]


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
    ap.add_argument("--opponent", default="farm", choices=sorted(OPPONENTS),
                    help="which seat-1 agent to replay against. The farmer alone is a "
                         "misleading picture -- see OPPONENTS.")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--frozen-town", action="store_true",
                    help="reproduce the pre-2026-08-03 market in which no shop ever unlocked, so "
                         "the town bought 140 wheat a season instead of ~700 and end-of-season "
                         "wheat priced at $37 against $51. For the A/B only -- it is not a "
                         "reachable configuration of the real game.")
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
    ap.add_argument("--vocab", default=None,
                    help="bundle vocabulary this checkpoint was TRAINED with. Defaults to the path "
                         "recorded in the checkpoint's own args, and falls back to "
                         "market_bundles.DEFAULT_VOCAB only if the checkpoint predates that field. "
                         "Getting this wrong decodes every market order into a different order and "
                         "raises nothing -- see the note by `_bundle_sells`.")
    args = ap.parse_args()

    with pathlib.Path(args.checkpoint).open("rb") as fh:
        ck = pickle.load(fh)
    saved = ck.get("args", {})

    # The vocabulary travels with the model, so the checkpoint is the authority and the flag is an
    # override. Printed either way: a tokenizer chosen by default is exactly the kind of thing that
    # is never noticed until the numbers have already been believed.
    vocab_path = args.vocab or saved.get("vocab")
    _set_vocab(vocab_path)
    if vocab_path:
        src = "--vocab" if args.vocab else "checkpoint"
        print(f"vocab: {vocab_path}  (from {src})")
    else:
        from kagg.il import market_bundles as _MBv
        print(f"vocab: {_MBv.DEFAULT_VOCAB}  (DEFAULT -- checkpoint records none; "
              f"if this model was trained on another vocabulary every order below is wrong)")
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
        money, trace, counts, unit_turns, commits, acct = play(
            params, model, args.games, sub, swap, greedy=args.greedy,
            opponent_fn=OPPONENTS[args.opponent], frozen_town=args.frozen_town)
        w, d, ll, me, them = report(money, swap)
        seat = 1 if swap else 0
        print(f"--- policy in seat {seat} vs {args.opponent} ---")
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

        # **Where the money went, per game-day, as causes rather than a level.**
        #
        # The bank curve showed the farmer replay falling -21/day to day 10 and then -552/day to
        # day 15. A cliff is not something a policy converged on inaction can produce, because its
        # own inaction is the dominant driver of its own cash and inaction is smooth. These three
        # columns say which line moved. They sum to the day's change exactly -- pinned by
        # `tests/test_money_accounting.py`.
        #
        # `hire` is the one to watch and the reason this is per-day rather than cumulative: the
        # crew resets to a single unit every night, so a crew of N is re-bought every morning at
        # `sum(HIRE_COST[:N])`, and HIRE_COST is Fibonacci. Eight units is $54/day, twelve is $376,
        # fourteen is $986. That is a recurring bill booked as a one-off purchase, and it is
        # invisible in any bank level.
        med = lambda k: np.median(np.asarray(acct[k])[:, :, seat], axis=1)   # noqa: E731
        hire_d, land_d, sell_d, buy_d = med("hire"), med("land"), med("sell"), med("buy")
        print("  money flow per day (median over games), + is income")
        print(f"    {'day':>5} {'sell':>10} {'buy':>10} {'hire':>10} {'land':>10} {'net':>10}")
        for d_ in range(len(hire_d)):
            net = sell_d[d_] - buy_d[d_] - hire_d[d_] - land_d[d_]
            if d_ in (0, 1, 2, 3, 5, 8, 10, 11, 12, 13, 14, 15, 17, 20, 25, 29) or abs(net) > 100:
                print(f"    {d_:>5} {sell_d[d_]:>10,.0f} {-buy_d[d_]:>10,.0f} "
                      f"{-hire_d[d_]:>10,.0f} {-land_d[d_]:>10,.0f} {net:>10,.0f}")
        tot = lambda a: np.asarray(a)[:, :, seat].sum(axis=0)      # noqa: E731
        # **Gross sales for the season is the number that says whether the chain ever pays.**
        # A net of -$648 is produced equally by a farm that sells nothing and one that sells $600
        # while spending $1,248. Only the gross tells those apart, and they imply opposite fixes.
        print(f"    season totals   SELL {np.median(tot(acct['sell'])):>+10,.0f}   "
              f"buy {-np.median(tot(acct['buy'])):>+10,.0f}   "
              f"hire {-np.median(tot(acct['hire'])):>+10,.0f}   "
              f"land {-np.median(tot(acct['land'])):>+10,.0f}")
        gross = np.asarray(acct["sell"])[:, :, seat].sum(axis=0)
        print(f"    games that sold ANYTHING all season: "
              f"{int((gross > 0).sum())}/{len(gross)}   "
              f"gross sales median ${np.median(gross):,.0f} max ${gross.max():,.0f}")

        cm = np.asarray(commits)
        print("  commits chosen  " + "  ".join(
            f"{CM_NAME}:{cm[i] / max(1.0, unit_turns):.2%}"
            for i, CM_NAME in enumerate(COMMIT_NAMES)))

        c = np.asarray(counts)
        total = max(1.0, unit_turns)
        top = np.argsort(-c)[:9]
        print("  ops (share of the policy's own live-unit actions)")
        print("    " + "  ".join(f"{OP_NAMES[i]}:{c[i] / total:.2%}" for i in top))
        # FERTILIZE is printed explicitly for the same reason FEED is: it sits outside the top-N
        # slice above, so "not in the list" was being read as "zero". The policy buys FERTILIZER on
        # 19.3% of turns and sells on 24.5%, and whether any of it reaches a plant -- FERTILIZE
        # doubles a watered plant's yield for three days -- decides whether that is sound melon play
        # or a wash trade paying the spread twice.
        print(f"    FEED:{c[O.FEED] / total:.4%}  CARE:{c[O.CARE] / total:.4%}  "
              f"HARV:{c[O.HARVEST] / total:.4%}  raw FEED count {c[O.FEED]:,.0f}")
        print(f"    FERTILIZE:{c[O.FERTILIZE] / total:.4%} (raw {c[O.FERTILIZE]:,.0f})  "
              f"COLLECT_FERT:{c[O.COLLECT_FERT] / total:.4%} (raw {c[O.COLLECT_FERT]:,.0f})\n")


if __name__ == "__main__":
    main()
