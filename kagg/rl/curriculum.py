"""Seed training episodes from real recorded boards instead of from an empty farm at turn 0.

**The problem this exists for, measured rather than assumed.** The policy's competence is
board-conditional: the BC checkpoint waters on 12.5% of its decisions when handed a real winner's
board and on 2.77% when playing its own. Same weights. It performs maintenance when the board looks
like something in its demonstration distribution and produces almost nothing otherwise -- and its
own board leaves that distribution within one game-day, because it spends $2,915 of its $3,000 in
the first 24 turns and then stands in a weed field no $120k player was ever in.

Every chain in the game then breaks at step two. Over a season it buys 50 seeds and plants 19; plants
19 and waters 39 (a crop needs about ten waterings or it dies in two days); places 58 animals and
feeds 8; builds 35 pastures and digs 27 of them back up.

**Why start states and not a shaped reward.** The reward is unchanged -- still one bit at the end of
the season, still win/lose. What changes is where the episode begins, which changes the *data*, not
the *signal*. That distinction is the whole argument: potential-based shaping is provably equivalent
to initialising the value function (Wiewiora 2003), so hand-authoring an intermediate value is the
banned thing wearing different clothes; changing the initial-state distribution is not, because the
agent still has to win from wherever it lands and is still judged only on whether it did.

It also attacks a second measured problem that nothing else touches. Every opponent currently returns
a *constant* outcome -- 0.000 against the idle seat and the scripted farmer, 0.060 against the
trader, and 89% draws against a frozen self because two bankrupt farms tie exactly. A constant reward
has no gradient regardless of model size or step count. A seeded day-15 board is already worth far
more than the idle opponent's $3,000, so outcomes start varying immediately, which is the first thing
that has to be true before anything else can be learned.

**Both seats come from the same recorded turn, and that is not a convenience.** A replay stores both
players' observations including `private`, so one turn yields a fully consistent two-seat board.
Seeding only the trainee and leaving the opponent on an empty board would reproduce the
virgin-episode bug exactly: `jax_heuristic.py:179` gates planting on `day <= LAST_PLANT_DAY`, so on a
fresh board claiming to be day 15 the scripted farmer declines to plant or hire, both sides stand
still, and the game scores as a tie worth 0.5. That cost this project a session once already.

**What this does not fix, stated so it is not discovered as a surprise.** A crop dies after two
missed waterings and an animal escapes after two missed feedings (`jax_sim.py:974`, `:1057`). A
day-15 board is therefore two turns from beginning the same decay it was seeded to avoid, just inside
a shorter horizon. If that is what happens, this has relocated the failure rather than shortened the
chain, and the tell is the bank curve from the seed day: flat means the position was handed over
rather than earned, a cliff at day 2-3 of the episode means the collapse simply moved.
"""

import jax
import numpy as np

from kagg.il import bc, replays
from kagg.sim import jax_sim as J

# Sampled turns are drawn from a window around the target day rather than from the exact turn, so a
# schedule step does not present one board repeatedly across the batch.
DAY_WINDOW = 1


def available(root="data"):
    return bool(bc.find_replays(root))


def noop_actions(batch):
    """A do-nothing `Actions` for both seats, for tests that only need the state to step."""
    z = lambda *shape: np.zeros(shape, dtype=np.int32)                      # noqa: E731
    return J.Actions(
        unit_op=z(batch, 2, J.MAX_UNITS), unit_crop=z(batch, 2, J.MAX_UNITS),
        unit_item=z(batch, 2, J.MAX_UNITS), unit_qty=z(batch, 2, J.MAX_UNITS) + 1,
        sell=z(batch, 2, J.N_PRODUCTS), buy_seed=z(batch, 2, J.N_CROPS),
        buy_product=z(batch, 2, J.N_PRODUCTS), buy_animal=z(batch, 2, J.N_ANIMALS),
        hire=np.zeros((batch, 2), dtype=bool), buy_land=np.zeros((batch, 2), dtype=bool))


def _turn_indices(n_steps, day, window=DAY_WINDOW):
    """Recorded step indices whose game-day is within `window` of `day`."""
    lo = max(1, (day - window) * J.TURNS_PER_DAY)
    hi = min(n_steps - 1, (day + window + 1) * J.TURNS_PER_DAY)
    return lo, hi


def _with_step_index(state, step):
    """Force `step_index`, because `obs["step"]` is `None` in some replays.

    `adapter.state_from_obs` defaults a missing step to 0, which would hand the simulator a
    mid-season board carrying a day-0 counter -- and every crop and animal rule is driven by
    `step_index // TURNS_PER_DAY`, so the board would be run under the wrong rules silently.
    Safe to overwrite after construction: `_tile_arrays` takes `day` but never reads it, so no
    reconstructed field depends on the value being right at build time.
    """
    import jax.numpy as jnp

    return state._replace(step_index=jnp.full_like(state.step_index, int(step)))


def _swap_seats(state):
    """Exchange the two players' farms and tiles, leaving the shared market alone.

    `ref.seat` is the seat the replay index ranked, and `adapter.state_from_obs` places each farm at
    its own index, so the ranked seat is not always seat 0. Swapping is how the trainee is put in the
    poorer position without rebuilding anything.
    """
    import jax.numpy as jnp

    flip = lambda x: jnp.flip(x, axis=1)                                     # noqa: E731
    return state._replace(
        tiles=jax.tree_util.tree_map(flip, state.tiles),
        farm=jax.tree_util.tree_map(flip, state.farm),
    )


def _stack(states):
    """Concatenate a list of batch-of-one `State`s along the batch axis.

    `key` is taken from the first rather than concatenated: it is a PRNG key, not a per-game field,
    and the simulator splits it itself.
    """
    import jax.numpy as jnp

    def cat(field):
        return jnp.concatenate([getattr(s, field) for s in states], axis=0)

    return J.State(
        step_index=cat("step_index"),
        tiles=J.Tiles(**{f: jnp.concatenate([getattr(s.tiles, f) for s in states], axis=0)
                         for f in states[0].tiles._fields}),
        farm=J.Farm(**{f: jnp.concatenate([getattr(s.farm, f) for s in states], axis=0)
                       for f in states[0].farm._fields}),
        inventory=cat("inventory"),
        unlock_day=cat("unlock_day"),
        key=states[0].key,
    )


def states_at_day(batch, day, seed=0, min_bank=None, top=200, root="data", behind=False,
                  max_bank=None):
    """A batched `jax_sim.State` of `batch` real boards from around game-day `day`.

    Boards are drawn from the richest seats and from as many *distinct* replays as possible, because
    one board repeated across the batch teaches that board's geometry rather than a policy.

    **`hide_opponent=False` is deliberate and is the opposite of what behaviour cloning wants.** BC
    blanks the other seat because a submission never sees it; here the pair *is* the environment,
    and a simulator handed a blank opponent shed would run a different game from the one recorded.

    **`behind` is the difficulty dial, and it costs nothing.** Both seats come from one recorded
    turn, so the pair is always a real strong player against their real opponent -- the only choice
    is which of the two the trainee inherits. `behind=False` puts it in the richer seat, which is
    what makes the position beatable on the seed alone and is the fastest route to a non-constant
    outcome. That is also its failure mode: winning by inheriting a lead looks identical, in a win
    rate, to winning by playing well, and the tell is a bank curve that is flat from the seed day
    rather than rising. `behind=True` puts it in the poorer seat, where a win cannot be inherited
    and has to be earned. Mixing the two is what stops the schedule confirming itself.
    """
    from kagg.rl import adapter

    # **`max_bank` is the answer to "are we handing it one strategy?"** Ranking by final bank and
    # taking the top puts almost only animal-heavy boards in the pool -- of 64 boards at day 25,
    # 62 carry five or more animals and the median is 17. But the seats are not strategically
    # uniform: one banked $86,206 with FEED **zero** (163 plantings, 1,256 waterings, no animals at
    # all), and 30 of 124 seats above $60k sit in the bottom quartile for feeding. Bank correlates
    # with feed count at only 0.227. So there are at least two viable strategies on disk and the
    # default pool contains essentially one of them.
    refs = bc.rank_seats(bc.find_replays(root), min_bank=min_bank, max_bank=max_bank)[:top]
    if not refs:
        raise SystemExit("no replays to seed from")

    rng = np.random.default_rng(seed)
    # One board per replay first, cycling only if more games are wanted than replays exist.
    order = rng.permutation(len(refs))
    states, used, misses = [], 0, 0
    # **Bail on consecutive failures, not on total attempts.** Capping attempts at a multiple of the
    # reference count also caps the number of states that can be built, so a batch larger than that
    # multiple can never be filled -- which is exactly how a 256-game run died having built 240.
    # Consecutive misses is the condition actually worth detecting: it means no replay can supply
    # the requested day at all.
    while len(states) < batch and misses <= len(order):
        ref = refs[order[used % len(order)]]
        used += 1
        turns = list(replays.iter_turns(ref.path, winners_only=False, seats={ref.seat},
                                        hide_opponent=False, with_index=True))
        if not turns:
            misses += 1
            continue
        lo, hi = _turn_indices(len(turns), day)
        if hi <= lo:
            # This replay is shorter than the requested day -- a real condition near day 29.
            misses += 1
            continue
        misses = 0
        obs, privates, _action, seat, step = turns[int(rng.integers(lo, hi))]
        st = _with_step_index(adapter.state_from_obs(obs, privates), step)
        # `adapter` places each farm at its own replay index, so the ranked seat is not always
        # index 0. Swap only when the seat we want the trainee to occupy is not already there --
        # an unconditional swap flips whatever happens to be present and the dial does nothing.
        want_ranked_at = 1 if behind else 0
        if seat != want_ranked_at:
            st = _swap_seats(st)
        states.append(st)

    if len(states) < batch:
        raise SystemExit(f"only built {len(states)} of {batch} seeded states")
    return _stack(states[:batch])


def _duplicate_seat(state, seat=0):
    """Copy one real seat's whole position onto BOTH sides, so the start is exactly symmetric.

    **Why this and not equalising the cash.** Both seats come from the same recorded turn, so a
    seeded game is a real strong player against their real opponent -- and at day 25 the gap between
    them is mostly *assets*, not cash: one side carries 16 animals and 20 crops against the other's 4
    and 8, while the banks differ by about 13% ($69k against the scripted farmer's $61,440). Levelling
    the cash alone would look fair and would not be, because the farm is worth far more than the
    difference in the bank.

    **Why it is safe where a hand-built board is not.** Every field is copied from one seat that
    really existed at that turn, so both sides are internally consistent and the day counter matches
    the contents. That is the property `states_at_day` protects: the bug it warns about is a *real*
    seat facing a *synthetic empty* one, which makes `jax_heuristic` refuse to plant (it gates on
    `day <= LAST_PLANT_DAY`) and scores every episode a 0.5 tie. Two copies of one real board cannot
    trigger that -- neither side is empty and both are legal.

    The market and the PRNG key are left alone: they are per-game, not per-seat.
    """
    import jax.numpy as jnp

    def dup(x):
        # Per-seat arrays are [batch, 2, ...]; anything else (per-game) is returned untouched.
        if getattr(x, "ndim", 0) >= 2 and x.shape[1] == 2:
            return jnp.repeat(x[:, seat:seat + 1], 2, axis=1)
        return x

    return state._replace(
        tiles=jax.tree_util.tree_map(dup, state.tiles),
        farm=jax.tree_util.tree_map(dup, state.farm),
        inventory=dup(state.inventory),
    )


def parse_mix(spec):
    """`"25:0.8,0:0.2"` -> `{25: 0.8, 0: 0.2}`, validated.

    Raises rather than normalising a bad spec. Fractions that do not sum to 1 would produce a batch
    whose composition is not the one asked for, and this project's standing rule is that a feature
    which silently runs as something other than what was requested is worse than one that fails.
    """
    mix = {}
    for part in str(spec).split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise ValueError(f"mix entry {part!r} is not day:fraction (e.g. '25:0.8,0:0.2')")
        day_s, frac_s = part.split(":", 1)
        day, frac = int(day_s), float(frac_s)
        if day < 0 or day > 29:
            raise ValueError(f"mix day {day} is outside the season (0-29)")
        if frac <= 0:
            raise ValueError(f"mix fraction for day {day} is {frac}; use a positive fraction or "
                             f"drop the entry rather than asking for a zero share")
        if day in mix:
            raise ValueError(f"day {day} appears twice in the mix")
        mix[day] = frac
    if not mix:
        raise ValueError("empty curriculum mix")
    total = sum(mix.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"mix fractions sum to {total:.6f}, not 1.0")
    return mix


def mix_counts(batch, mix):
    """Slots per day, summing to exactly `batch`, by largest remainder.

    **Exactly**, because a naive `int(batch * frac)` per day leaves a shortfall that `states_at_mix`
    would then have to pad from somewhere, and whichever day absorbed the padding would be over-
    represented by an amount nobody wrote down.

    **A requested day that would get zero slots raises.** `{25: 0.999, 0: 0.001}` at batch 256 wants
    0.256 day-0 slots, and rounding that to zero produces a run which reports a mix in its log and
    trains a pure day-25 curriculum. That is the exact failure mode this project has a standing rule
    against: a feature that is silently not running gives a false model of what is being measured.
    """
    days = sorted(mix, reverse=True)
    exact = {d: batch * mix[d] for d in days}
    counts = {d: int(exact[d]) for d in days}
    remainder = batch - sum(counts.values())
    # Largest fractional part first; ties broken by the day order above so this is deterministic.
    for d in sorted(days, key=lambda d: (-(exact[d] - int(exact[d])), days.index(d)))[:remainder]:
        counts[d] += 1

    zero = [d for d in days if counts[d] == 0]
    if zero:
        raise ValueError(
            f"day(s) {zero} would get 0 of {batch} slots at these fractions, so the mix would "
            f"silently run without them. Raise the fraction or the batch.")
    return counts


def states_at_mix(batch, mix, seed=0, min_bank=None, top=200, root="data", behind=False,
                  max_bank=None, shuffle=True, mirror=False, symmetric=False):
    """A batched `State` drawn from several game-days at once, in the proportions `mix` asks for.

    **Why a mix rather than walking the day back.** Pure backward annealing arrives at day 0 last,
    with the least accumulated exposure, on weights specialised for maintenance -- that objection is
    recorded in `HANDOFF_2026-08-02.md` against the anneal it also proposes. A mix removes it by
    construction: the opening is in the state distribution from the first update. It also removes a
    failure the anneal cannot avoid, which is that when the schedule steps from day 25 to day 20 the
    day-25 distribution is *gone from the data*. Re-anchoring a KL prior preserves the behaviour
    partially; nothing preserves the data. In a mix nothing is ever removed.

    **What the small fraction actually buys, stated because it is easy to over-claim.** Episode
    length differs about six-fold between day 25 (~120 turns) and day 0 (719), and every slot emits
    the same `--horizon` turns per update, so a 20% day-0 *slot* share is roughly a 4% share of
    *terminal episodes* -- and each of those episodes carries its reward across ~22 horizon segments
    instead of ~4. So a small day-0 fraction is not buying policy credit on the opening. It buys
    **coverage**: opening states stay in the distribution, so the critic can learn to value them and
    they never become out-of-distribution. That ordering is the point, since policy gradient on
    opening states is worth nothing until the critic can separate a good opening from a bad one.

    **`shuffle` exists to keep the day out of the slot index.** Seat-1 roles are drawn i.i.d. per
    slot (`jax.random.categorical(..., shape=(batch,))`), so block ordering does not currently
    correlate day with opponent -- but a restarting slot restarts into `seed_states[i]` by position,
    so any future per-slot assignment would inherit the block structure and the confound would be
    invisible. Permuting costs one gather and makes the class of bug unreachable.
    """
    counts = mix_counts(batch, mix)
    pools = []
    for day, n in sorted(counts.items(), reverse=True):
        if not n:
            continue
        day_seed = seed + 1000 * day
        if not mirror:
            pools.append(states_at_day(n, day=day, seed=day_seed, min_bank=min_bank, top=top,
                                       root=root, behind=behind, max_bank=max_bank))
            continue
        # **Mirrored pairs: the same boards played from both sides.** `states_at_day` draws its
        # replay order and its turn index from `np.random.default_rng(seed)`, and `behind` only
        # decides which seat the trainee ends up in -- so two calls with the SAME seed and the same
        # count return the same boards with the seats exchanged. The advantage of inheriting the
        # richer seat therefore cancels in the aggregate, without editing a single field.
        #
        # This is the alternative to equalising the two seats' money, which would fabricate a
        # position no recorded game produced -- and `states_at_day`'s own docstring records that an
        # inconsistent two-seat board is what made the scripted farmer decline to act, scoring every
        # episode as a 0.5 tie and costing a session.
        half = n // 2
        if half:
            pools.append(states_at_day(half, day=day, seed=day_seed, min_bank=min_bank, top=top,
                                       root=root, behind=False, max_bank=max_bank))
            pools.append(states_at_day(half, day=day, seed=day_seed, min_bank=min_bank, top=top,
                                       root=root, behind=True, max_bank=max_bank))
        # An odd count cannot be mirrored exactly. The leftover slot goes to the POORER seat, so a
        # rounding artefact can only ever understate the win rate -- the opposite bias to the one
        # this flag exists to remove.
        if n % 2:
            pools.append(states_at_day(1, day=day, seed=day_seed + 7, min_bank=min_bank, top=top,
                                       root=root, behind=True, max_bank=max_bank))
    stacked = _stack(pools) if len(pools) > 1 else pools[0]
    if symmetric:
        # Both sides get seat 0's position, so the ONLY difference between the players is what they
        # do. This makes the win rate directly interpretable, which it is not by default: the trainee
        # inherits the richer seat and a win can therefore be inherited rather than earned.
        stacked = _duplicate_seat(stacked, seat=0)
    if not shuffle:
        return stacked

    import jax.numpy as jnp

    order = jnp.asarray(np.random.default_rng(seed).permutation(batch))
    take = lambda x: jnp.take(x, order, axis=0)                              # noqa: E731
    return stacked._replace(
        step_index=take(stacked.step_index),
        tiles=jax.tree_util.tree_map(take, stacked.tiles),
        farm=jax.tree_util.tree_map(take, stacked.farm),
        inventory=take(stacked.inventory),
        unlock_day=take(stacked.unlock_day),
    )


def schedule(update, updates_per_step, start_day, end_day=0):
    """Start day for a given update: walks `start_day` down to `end_day` in even steps.

    Deliberately a function of the update counter rather than of the win rate. A win-rate-driven
    schedule is the more principled design and is also self-confirming: the metric that advances the
    curriculum is the metric that judges it, so a curriculum that advances because outcomes became
    degenerate looks identical to one that advanced because the policy improved. Drive it on the
    clock, and read the win rate as an independent measurement.
    """
    if updates_per_step <= 0:
        return start_day
    steps = update // updates_per_step
    return int(max(end_day, start_day - steps))
