"""Behaviour cloning from the winners' replays: seat selection, feature building, and the loss.

Kept out of `scripts/bc_replay.py` so the loss can be tested. Every property in
`tests/test_bc_replay.py` is a mistake this project has already paid for once.

**Why the replays and not a live in-sim teacher.** `scripts/bc_dagger.py` works and solves covariate
shift properly, but its only teacher that ever emits FEED is `jax_rancher` at $12,078, and that agent
spends 37-52% of its actions on a PICKUP thrash it would teach along with the good behaviour. The
replays on disk contain seats banking $112k-$132k. For a *warm start* the teacher's quality matters
more than the state distribution: the checkpoint does not have to play well, it has to move the
weights somewhere PPO's own exploration can reach the animal economy, and PPO generates on-policy
data from the first update -- which is the correction a fixed replay set cannot provide.

**Three things here differ from `bc_dagger.py`, deliberately.**

1. **Conditioned heads are cloned under every trade mode, not just mode 0.** `bc_dagger` labels
   `trade` as 0 and excludes it from the loss, which also means only the mode-0 slice of `sell` and
   `buy_product` is ever trained. At play time the mode is *sampled*, so two turns in three the
   market behaviour of a warm-started policy would be untrained noise -- and the offline loss could
   not see it, because it only measured the slice it trained. The mode axis is a coordinating latent
   with no counterpart in a replay, so the honest label is "this order, whichever mode you draw".
2. **Only the unit heads the chosen op actually reads are scored** (`jax_act.active_unit_heads`).
   A `crop` label on a PICKUP slot is not the teacher's opinion about crops, it is a zero from the
   encoder. Scoring it trains every non-PLANT slot toward crop index 0, which is WHEAT.
3. **Label smoothing is on by default.** The parked BC track's op head learned a 9.7-nat gap at the
   daily spawn state -- P(move) = 6e-5 per unit-turn, so across a thirteen-unit crew and a thirty-day
   season you would expect about one unit to ever leave the shed. That is the absorbing state that
   made the checkpoint bank exactly its $3,000 start. Smoothing bounds the achievable logit gap.

Features come from `adapter.state_from_obs` and the *same* `jax_obs.encode` that PPO trains on, for
the reason `adapter.py` gives at length: a second encoder is a thing that must agree forever and
will not.
"""

import json
import time
from dataclasses import dataclass
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np

from kagg.il import replays
from kagg.rl import adapter, jax_act as A, jax_obs, jax_policy as P
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
        _BUNDLE_SELLS = _MB.valid_table(_MB.load_vocab(), pad_to=_PP.N_BUNDLES)
    return _BUNDLE_SELLS


# `trade` is the one head with no counterpart in a replay -- agents name quantities, not a mode -- so
# it is not scored. See point 1 in the module docstring for what that must *not* also mean.
SCORED_HEADS = A.ALL_HEADS

INDEX = Path("data/replay_index.json")

# **Two naming conventions are on disk and matching only one silently drops 30 replays.**
# `fetch_replays.py` has written both `89197802.json` and `episode-89182349-replay.json`, and a
# `[0-9]*.json` glob finds 126 of the 156. It fails quietly -- fewer teachers, a different top-25 --
# so the pattern list lives here and both the script and the tests use `find_replays`.
# `plan_*.json`, `search_history.json` and this module's own index cache share the directory.
REPLAY_PATTERNS = ("[0-9]*.json", "episode-*-replay.json")


# ---------------------------------------------------------------------------- seat selection

def find_replays(root="data"):
    """Every downloaded episode replay under `root`, deduplicated and sorted."""
    root = Path(root)
    out = set()
    for pattern in REPLAY_PATTERNS:
        out.update(root.glob(pattern))
    return sorted(out)

@dataclass(frozen=True)
class SeatRef:
    """One seat of one replay, and the money it finished with."""

    path: str
    seat: int
    bank: float


def _index(paths, cache=INDEX):
    """Final banks per replay, cached by (size, mtime).

    163 replays are 3.1 GB of JSON and `json.loads` is the slow part of this whole script, so the
    ranking pass is cached. Keyed on size and mtime rather than content: `fetch_replays.py` only ever
    appends new files, and a rewritten file changes both.
    """
    known = {}
    if cache and Path(cache).exists():
        known = json.loads(Path(cache).read_text())

    out, fresh = {}, 0
    for p in paths:
        p = Path(p)
        st = p.stat()
        key = str(p)
        hit = known.get(key)
        if hit and hit.get("size") == st.st_size and hit.get("mtime") == int(st.st_mtime):
            out[key] = hit
            continue
        try:
            rewards = replays.replay_summary(p)["rewards"]
        except (KeyError, IndexError, ValueError) as exc:
            # A partially-written download rather than a replay. Say which file and carry on: the
            # alternative is one bad file aborting a twenty-minute build.
            print(f"  skipping {p.name}: not a replay ({type(exc).__name__})")
            continue
        out[key] = {"size": st.st_size, "mtime": int(st.st_mtime),
                    "rewards": [float(r or 0.0) for r in rewards]}
        fresh += 1

    if cache and fresh:
        Path(cache).parent.mkdir(parents=True, exist_ok=True)
        Path(cache).write_text(json.dumps(out))
    return out, fresh


def rank_seats(paths, min_bank=None, cache=INDEX, max_bank=None):
    """Every seat in `paths`, richest first.

    **Seats, not replays.** In 89197802 the *losing* seat still banked $106,091; discarding it
    because of who it happened to be drawn against throws away a teacher. Filtering by final bank is
    the right criterion and `winners_only` is not.

    **`max_bank` exists because the best teacher is not always the most useful one.** The 312 seats
    on disk are heavily skewed strong -- 207 of them clear $70k, median $83,802 -- and a $130k
    player's actions are conditioned on a $130k player's board, which a student banking $0 cannot
    produce. Measured symptom: the cloned checkpoint waters on 12.5% of decisions when handed a real
    winner's board and 2.77% on its own, because its own board leaves the demonstration distribution
    within one game-day. A mid-tier band ($15k-$35k, 41 seats, median $24,066) sits nearer the
    scripted farmer's $30,292 and is a target the student could plausibly reach.

    The trade is reachability against ceiling, and it is only safe because `--init` is params-only
    with no KL anchor -- PPO can walk away from a mediocre clone. Anchoring to one would be the
    thing `CLAUDE.md` forbids: a heuristic that becomes the policy.
    """
    index, _fresh = _index(paths, cache)
    out = [SeatRef(path, seat, bank)
           for path, entry in index.items()
           for seat, bank in enumerate(entry["rewards"])
           if (min_bank is None or bank >= min_bank)
           and (max_bank is None or bank <= max_bank)]
    out.sort(key=lambda r: -r.bank)
    return out


# ---------------------------------------------------------------------------- feature building

@jax.jit
def _features(state):
    """Observation tensors and every legality mask for a batch-of-one state, network-flat."""
    tiles, units, glob = jax_obs.encode(state)
    return A._flat(tiles), A._flat(units), A._flat(glob), A.masks_for(state, _bundle_sells())


def build_rows(refs, max_turns=None, log_every=0):
    """`SeatRef`s -> the supervised arrays the loss consumes, one row per teacher turn.

    Rows are built one turn at a time because `adapter.state_from_obs` walks a nested 10x10 tile dict
    in Python; the jitted part is `_features`, which compiles once and is not the cost.

    **The opponent's private state is blanked** (`replays.iter_turns(hide_opponent=True)`). A replay
    records both sheds; a real agent is handed `adapter.agent_private_stub()` for the other seat.
    Training on what the policy will not be able to see flatters every offline number and shows up
    only on the ladder.
    """
    cols = {k: [] for k in ("tiles", "units", "glob", "live")}
    started, n = time.time(), 0

    for ref in refs:
        turns = 0
        for obs, privates, action, seat in replays.iter_turns(
                ref.path, winners_only=False, seats={ref.seat}):
            if max_turns is not None and turns >= max_turns:
                break
            state = adapter.state_from_obs(obs, privates)
            tiles, units, glob, masks = _features(state)

            cols["tiles"].append(np.asarray(tiles[seat], dtype=np.float32))
            cols["units"].append(np.asarray(units[seat], dtype=np.float32))
            cols["glob"].append(np.asarray(glob[seat], dtype=np.float32))
            # Column 0 of the unit features is `live`: a slot the farm actually owns.
            cols["live"].append(np.asarray(units[seat][:, 0] > 0.5, dtype=np.float32))

            for h in SCORED_HEADS:
                cols.setdefault(f"m_{h}", []).append(np.asarray(masks[h][seat], dtype=bool))

            labels = replays.encode_action(action, J.MAX_UNITS)
            for h in SCORED_HEADS:
                cols.setdefault(f"y_{h}", []).append(np.asarray(labels[h], dtype=np.int32))
            # **The quantity weights, or 78.9% of turns train the qty heads on nothing.** A quantity
            # is a decision only where the teacher's bundle asked for one; without these the loss
            # pulls every unselected product toward bucket 0 and the head collapses, after which the
            # floor-at-1 decode turns every sell and buy into quantity 1.
            for h in ("qty_sell", "qty_buy_product", "qty_buy_seed"):
                cols.setdefault(f"w_{h}", []).append(np.asarray(labels[f"w_{h}"],
                                                                dtype=np.float32))

            turns += 1
            n += 1
            if log_every and n % log_every == 0:
                rate = n / max(1e-9, time.time() - started)
                print(f"  built {n:,} rows  ({rate:.0f}/s)", flush=True)

    if not n:
        raise SystemExit("no rows built -- check the replay paths")
    return {k: np.stack(v) for k, v in cols.items()}


# ---------------------------------------------------------------------------- the loss

def head_term(logits, mask, label, live=None, smooth=0.0):
    """Masked log-probability of a teacher label, and the weight that label should carry.

    **A label the mask calls illegal carries weight zero.** A masked-illegal option sits at
    `NEG_INF = -1e9`, so asking for its log-probability puts 1e9 in the objective and one such row
    swamps every real one -- this is the 5.3e7 loss that would not move in the first version of
    `bc_dagger.py`. The teacher names an item and a quantity on every unit slot, including slots
    where nothing is legal, so these rows are common rather than exotic. You cannot clone an action
    the student has no way to take.
    """
    logits = jnp.asarray(logits)
    mask = jnp.broadcast_to(jnp.asarray(mask), logits.shape)
    label = jnp.asarray(label, dtype=jnp.int32)

    logp = jax.nn.log_softmax(P._masked_logits(logits, mask), axis=-1)
    chosen = jnp.take_along_axis(logp, label[..., None], axis=-1)[..., 0]
    legal = jnp.take_along_axis(mask, label[..., None], axis=-1)[..., 0]

    if smooth:
        # Mean log-probability over the **legal** options only. Averaging over all of them would
        # average in `-1e9` entries and the smoothing term would dominate the objective it is meant
        # to soften.
        n_legal = mask.sum(axis=-1)
        legal_mean = jnp.where(mask, logp, 0.0).sum(axis=-1) / jnp.maximum(n_legal, 1)
        chosen = (1.0 - smooth) * chosen + smooth * legal_mean

    # Zeroed rather than left at -1e9 so the tensor stays finite even where the weight is zero.
    chosen = jnp.where(legal, chosen, 0.0)
    weight = legal.astype(jnp.float32)
    if live is not None:
        weight = weight * jnp.asarray(live, dtype=jnp.float32)
    return chosen, weight


def conditioned_term(logits, mask, label, smooth=0.0):
    """`sell` / `buy_product`: clone the teacher's order under **every** trade mode.

    The head is `[.., N_PRODUCTS, N_TRADE_MODES, K]` and the mode is a coordinating latent the
    replay does not record. Training only the mode-0 slice leaves the other two at initialisation,
    and `jax_act.sample` draws the mode before the products -- so two turns in three a warm-started
    policy would trade at random while the offline loss reported success on the slice it trained.
    """
    logits = jnp.asarray(logits)
    mask = jnp.broadcast_to(jnp.asarray(mask)[..., None, :], logits.shape)
    label = jnp.broadcast_to(jnp.asarray(label, dtype=jnp.int32)[..., None], logits.shape[:-1])
    return head_term(logits, mask, label, smooth=smooth)


def weighted_mean(logp, weight):
    """Mean log-probability over the weighted rows. Higher is a better fit; the loss negates it."""
    return (logp * weight).sum() / jnp.maximum(weight.sum(), 1.0)


def loss_terms(heads, batch, smooth=0.0):
    """Per-head `(log_prob, weight)`, with the padding and irrelevance rules applied.

    Unit heads are weighted by live slots **and** by whether the teacher's op actually reads them.
    `MAX_UNITS` is 24 against a crew of about twelve, and a `crop` label on a FEED slot is a zero
    from the encoder rather than a decision -- scoring either makes the loss mostly constant.

    **`crop`/`item`/`qty` are cloned on the slice the teacher's own op selects.** The op is recorded
    in the replay, so the right target is the conditional the policy will actually act from, fitted
    on the turns the teacher used that op.

    The market side no longer needs an equivalent. It used to condition on a `trade` latent the
    replay does not record, which forced every slice of every product head to be trained. The bundle
    is recorded -- it is just the teacher's order list -- so the coordination is a label now rather
    than a hidden variable, and the quantity heads are weighted by which products that label named.

    **What this does and does not buy, stated precisely.** It matters only where two ops share a
    head. `crop` is read by PLANT alone and the `active` weighting below already restricted it to
    PLANT slots, so that head was already conditional and the op axis changes nothing for it. The
    gain is `item` and `qty`, which PICKUP and PLACE both read: their teacher distributions differ
    at total variation 0.900, and a single head had to average them into something that suited
    neither. Note PLACE is ~8x rarer than PICKUP, so it is both the case that pooling hurt most and
    the case where a split slice has least data to learn from.
    """
    live = jnp.asarray(batch["live"], dtype=jnp.float32)
    y_op = jnp.asarray(batch["y_op"])
    active = A.active_unit_heads(y_op)
    # Same call `jax_act.evaluate` makes, so the offline objective and the online density are the
    # same object. Slots where the op ignores the argument are weighted out by `active` below, so
    # the slice chosen there is irrelevant rather than wrong.
    heads = A.condition_on_op(heads, y_op)

    parts = {}
    for h in SCORED_HEADS:
        label, mask = batch[f"y_{h}"], batch[f"m_{h}"]
        if h in A.UNIT_HEADS:
            w = live * active[h].astype(jnp.float32) if h != "op" else live
            parts[h] = head_term(heads[h], mask, label, live=w, smooth=smooth)
        else:
            # **A quantity is only a decision for a product the teacher's bundle selected.**
            #
            # `qty_sell` carries one entry per product against a bundle that names one or two, so
            # scoring every entry trains the rest toward "bucket 0" on turns where the teacher
            # expressed no opinion at all -- and 78.7% of turns select nothing whatsoever. That is
            # the padding mistake this file already warns about for the unit heads, arriving on the
            # market side: most of the objective becomes a constant, and the part that carries the
            # signal is swamped.
            #
            # The dataset builder supplies `w_qty_*`, one weight per product, set from the teacher's
            # own bundle. `bundle` itself has no weight -- every turn is a real decision about which
            # orders to send, including the decision to send none.
            w = batch.get(f"w_{h}")
            parts[h] = head_term(heads[h], mask, label,
                                 live=None if w is None else jnp.asarray(w, dtype=jnp.float32),
                                 smooth=smooth)
    return parts


def loss(heads, batch, smooth=0.0):
    """Mean negative log-likelihood, averaged **per head** and then across heads.

    Per head rather than per element: `op` has 24 slots against one scalar for `hire`, so summing raw
    per-element losses lets slot count decide which decisions matter.
    """
    parts = loss_terms(heads, batch, smooth=smooth)
    per_head = {h: -weighted_mean(*v) for h, v in parts.items()}
    total = sum(per_head.values()) / len(per_head)
    return total, per_head
