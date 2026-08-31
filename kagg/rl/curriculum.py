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
from kagg.sim import tiles as T

# Sampled turns are drawn from a window around the target day rather than from the exact turn, so a
# schedule step does not present one board repeatedly across the batch.
DAY_WINDOW = 1

# The day `chain_states` builds its half-farm at. Named rather than repeated, because the length
# weighting below and the function's own default must not be able to drift apart -- a mismatch is
# invisible and mis-allocates the rung's slots by the ratio of the two numbers.
CHAIN_START_DAY = 25

# Mix keys that are not recorded game days, mapped to the game day whose episode LENGTH they have.
# -1 is `chain_states`: a half-built farm at day 25, so the last link of the production chain is
# learnable inside a ~120-turn episode.
#
# **This mapping is what `length_weighted_mix` was missing.** It weighted `-1` by
# `season_days - (-1)` = 31 days when the rung produces a ~5-day episode, so the rung received 6.2x
# the slots its requested episode share called for. Rung `-1` and rung `25` are the same length and
# cannot correctly get different allocations for the same requested share.
SYNTHETIC_START_DAY = {-1: CHAIN_START_DAY}
SYNTHETIC_RUNGS = frozenset(SYNTHETIC_START_DAY)


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
    """Recorded step indices whose game-day is within `window` of `day`.

    **`day` stays the centre of the window even when the clip bites.** The old spelling was
    `lo = max(1, (day - window) * TURNS_PER_DAY)`, which had two defects in one line:

    - **turn 0 was unreachable for every day**, and turn 0 is the only true game start on disk;
    - **at day 0 the window was not centred on day 0.** Clipping the low side to turn 1 while
      leaving the high side at `(0 + 1 + 1) * 24` gave `(1, 48)`, a window spanning game-days 0-2
      with its median at turn 24 -- game-day *1*. Measured, `states_at_day(0)` returned boards on
      $476 holding 7 units, a full game-day of play already spent.

    Shrinking the far side by however much the near side was clipped keeps the requested day at the
    median at every day, which is what the docstring always claimed.

    A recording shorter than the requested day still returns `hi <= lo`. That is the caller's
    signal to skip the replay, and clamping it away would silently answer a day-29 request with
    day-25 turns.
    """
    lo_day, hi_day = day - window, day + window
    if lo_day < 0:
        hi_day += lo_day          # same amount off the top, so `day` stays the centre
        lo_day = 0
    lo = max(0, lo_day * J.TURNS_PER_DAY)
    hi = min(n_steps - 1, (hi_day + 1) * J.TURNS_PER_DAY)
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
        # **The snapshot is seat-indexed too, so it swaps with them.** It holds each seat's view of
        # the OTHER, so leaving it behind would hand the trainee the position it used to be in and
        # call it the opponent's -- a wrong number that reads as a plausible one.
        opp_snapshot=flip(state.opp_snapshot),
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
        # The shop each unlock slot names, concatenated alongside its day -- they are one schedule
        # split over two arrays and must never be stacked independently of each other.
        unlock_shop=cat("unlock_shop"),
        key=states[0].key,
        opp_snapshot=cat("opp_snapshot"),
    )


def chain_states(n, wheat=12, plots=6, herd=3, crop=0, start_day=CHAIN_START_DAY):
    """A pristine board with the production chain already half-built, late in the season.

    **The problem, measured.** The policy will not buy animals or land, and over a full night those
    rates *fell* -- animals 0.0048 -> 0.0012, land 0.0014 -> 0.0006. That is not stubbornness, it is
    correct. Buying an animal is a certain loss unless PLACE, PICKUP and FEED all follow: an animal
    escapes after two unfed nights and first yield is 4-8 days out. Every prefix of the chain is
    punished, so PPO cannot discover a five-step sequence whose every initial segment loses money.
    What it learnt instead was frugality -- a full season against `jax_carrot` went 3,000 -> 2,988,
    dead flat, FEED firing zero times. It preserves capital and produces nothing, which beats an
    idle seat and can never beat the farmer's $23,783.

    **The fix is what `commit.py` already did, applied to the economic chain instead of the spatial
    one.** Commitment did not teach the policy to walk better; it shortened the credit horizon so a
    walk could pay off inside it. This does the same for production: animals already placed, wheat
    already in the shed, crops already planted and watered and carrying yield. FEED then pays off in
    ONE step rather than five, and HARVEST is legal immediately rather than after surviving
    plant -> water -> wait.

    **`start_day` is the other half, and arguably the more important one.** A half-built farm at
    turn 0 still asks the policy to hold the chain together for thirty days. At day 25 there are ~5
    game-days left, so the episode is ~120 turns against day 0's 719 -- six times shorter -- and the
    only thing that fits in the window is the last link: feed what you have, harvest what is in the
    ground, sell before the bell. Nothing else is learnable there, which is the point. It also makes
    terminals ~6x cheaper per slot, which this run is separately short of.

    **This is a shortened horizon, not a demonstration.** It says nothing about which animal, which
    crop, when to buy, or how big a herd -- all readable off the replays, all strategy the policy
    would inherit rather than discover. It asserts only that a half-built farm is a state worth
    being able to value, which is a claim about credit assignment. Money is left at the full $3,000
    deliberately: the assets are the gift, so if the policy still cannot convert them into a win,
    the problem was never capital.
    """
    import jax.numpy as jnp

    # `reset_with_shops`, not `reset`: a plain reset freezes every shop at `NEVER`, so the town
    # buys 140 wheat a season instead of ~700 and end-of-season wheat sits at $37 against the real
    # $51. This rung exists to make the last link of the chain -- sell before the bell -- learnable,
    # and it was pricing that sale 27% low.
    st = J.reset_with_shops(n, phase=np.full(n, int(start_day) * J.TURNS_PER_DAY, dtype=np.int64))
    tiles, farm = st.tiles, st.farm

    # Only tiles that start unlocked and empty; the locked quadrants stay locked.
    free = np.flatnonzero(np.asarray(tiles.kind[0, 0]) == T.EMPTY)
    plot_ix, herd_ix = free[:plots], free[plots:plots + herd]

    kind = np.asarray(tiles.kind).copy()
    crop_a = np.asarray(tiles.crop).copy()
    watered = np.asarray(tiles.watered_today).copy()
    yield_u = np.asarray(tiles.yield_units).copy()
    animal = np.asarray(tiles.animal).copy()

    # Crops in the ground, watered today, already carrying yield -- HARVEST is legal on turn one.
    kind[:, :, plot_ix] = T.PLANT
    crop_a[:, :, plot_ix] = crop
    watered[:, :, plot_ix] = 1
    yield_u[:, :, plot_ix] = 1
    # A placed herd, fed today, so the two-night escape window is open rather than already lost.
    kind[:, :, herd_ix] = T.PASTURE
    animal[:, :, herd_ix] = 1                      # COW

    shed = np.asarray(farm.shed).copy()
    shed[:, :, 0] += wheat                         # WHEAT is item 0 -- what FEED consumes

    return st._replace(
        tiles=tiles._replace(
            kind=jnp.asarray(kind), crop=jnp.asarray(crop_a),
            watered_today=jnp.asarray(watered), yield_units=jnp.asarray(yield_u),
            animal=jnp.asarray(animal)),
        farm=farm._replace(shed=jnp.asarray(shed)))


def states_at_day(batch, day, seed=0, min_bank=None, top=None, root="data", behind=False,
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
    # **`top=None` means every seat on disk, and the old default of 200 was leaving boards unused.**
    # There are 312 seats recorded (`rank_seats`: "The 312 seats on disk are heavily skewed strong --
    # 207 of them clear $70k"), so `top=200` discarded 112 of them while `--batch 256` was drawing
    # from a 200-board pool -- which means some boards appeared twice in the same batch. Combined with
    # a restarting slot going back into `seed_states[i]` by index, the effective diversity was ~200
    # distinct boards each replayed ~7 times per resample window, and the handoff calls the unbounded
    # version of exactly that "an overfitting surface rather than a curriculum".
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
        # **Swap on the money actually in the drawn board, not on `ref.seat`.**
        #
        # `adapter` places each farm at its own replay index, so the richer seat is not always index
        # 0, and swapping only when needed is what stops the dial cancelling itself out.
        #
        # It used to key off `ref.seat` -- the seat `bc.rank_seats` ranked, which ranks by **final**
        # bank. That is not the same seat as the one that is ahead *at the seed turn*, and the gap is
        # not small: measured over 24 boards per rung, the ranked seat led at the seed in 62% of
        # day-10 boards, 50% at day 15, 58% at day 20 and 50% at day 25. So the flag delivered a
        # coin flip, and at days 20 and 25 it **inverted** -- `behind=True` handed the trainee the
        # richer seat ($58,391 against $54,052 at day 25).
        #
        # That silently voided the guard the flag exists to provide. Its docstring's claim is that
        # `behind=True` is where "a win cannot be inherited and has to be earned"; on the late rungs
        # it was where a win was *most* inheritable. Comparing the two banks in the state itself
        # makes the dial exact rather than 50-62% accurate, and it is the flag's documented contract
        # rather than a new behaviour.
        #
        # `mirror` still works: two calls with the same seed draw the same boards, and the richer
        # seat lands at index 0 in one and index 1 in the other, which is the exact exchange it wants.
        money = np.asarray(st.farm.money)[0]
        richer = int(np.argmax(money))
        want_richer_at = 1 if behind else 0
        if richer != want_richer_at:
            st = _swap_seats(st)
        states.append(st)

    if len(states) < batch:
        raise SystemExit(f"only built {len(states)} of {batch} seeded states")
    stacked = _stack(states[:batch])

    # **Stamp a plausible shop schedule over the adapter's `NEVER`.**
    #
    # `adapter.state_from_obs` sets `unlock_day = NEVER` for a correct reason -- the schedule is a
    # per-episode RNG artifact and an observation does not record it. But `NEVER` is not a neutral
    # unknown: it is the assertion that no shop ever opens, which drops the town's shop drain to
    # zero and holds end-of-season wheat at $37 against the real $51. A sampled schedule is
    # unknowably wrong in its *order* and right about the cadence; `NEVER` is wrong about both.
    #
    # The recorded board is mid-season, so a day-15 seed correctly finds five of eight shops
    # already open -- the sampled days run 3..24 regardless of where the episode resumes.
    #
    # `unlock_shop` must move with it. `random_unlock_days` is shop-indexed -- slot `i` is shop `i`
    # -- and the stacked state inherited the adapter's all-zero companion, which would read as
    # eight instances of shop 0 and drain one shop's products eightfold.
    return stacked._replace(
        unlock_day=J.random_unlock_days(batch, seed=seed),
        unlock_shop=J.shop_ids_for_days(batch),
    )


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


def length_weighted_mix(days, season_days=30):
    """`{day: fraction}` weighted so each day contributes the requested share of terminal episodes.

    Pass an iterable of days for an EQUAL share each, or a `{day: episode_fraction}` mapping to ask
    for a specific split -- `{0: 0.6, 25: 0.1, ...}` means "60% of finished episodes should start at
    day 0", which is not expressible as a slot fraction and is the thing actually worth setting.

    **The problem it fixes.** A day-`d` episode is `(season_days - d)` game-days long, and every slot
    emits the same `--horizon` turns per update, so terminal episodes from day `d` arrive in
    proportion to `1 / (season_days - d)`. Sampling days uniformly therefore hands the last few days
    almost all of the gradient: over `d = 0..29` the share is `1/(30-d)` normalised by
    `sum(1/k, k=1..30) ~= 3.995`, which gives **day 29 about 25% of all terminal outcomes and day 0
    about 0.8%** -- and a day-29 episode is one game-day, essentially already decided.

    **The fix is one line: weight the day by remaining season length.** With `P(d) ~ (season_days - d)`
    the two biases cancel exactly, because episodes ~ `P(d) / (season_days - d)` = constant. So each
    requested day supplies an equal share of terminal episodes, which is the unit the gradient
    actually consumes.

    Measured motivation from the run this replaced: at `25:0.6,20:0.1,15:0.1,10:0.1,0:0.1` the day-25
    slots had 748 finished games by update 16 while day 20 had 36 and days 15, 10 and 0 had **zero** --
    a day-0 episode needs ~22 updates to finish even one. The middle and early rungs were not
    contributing weakly; they were contributing nothing.
    """
    # A mapping asks for specific episode shares; a bare iterable asks for an equal split. Both end
    # up in `want`, so there is exactly one weighting expression below rather than two that could
    # drift apart.
    if isinstance(days, dict):
        want = {int(d): float(f) for d, f in days.items()}
        if any(f <= 0 for f in want.values()):
            raise ValueError("episode fractions must be positive; drop the day instead of asking "
                             "for a zero share, or it silently will not run")
        total_want = sum(want.values())
        if abs(total_want - 1.0) > 1e-6:
            raise ValueError(f"episode fractions sum to {total_want:.6f}, not 1.0")
    else:
        keys = sorted({int(d) for d in days}, reverse=True)
        want = {d: 1.0 / len(keys) for d in keys} if keys else {}

    if not want:
        raise ValueError("no days given")
    for d in want:
        # Negative keys are SYNTHETIC rungs, not recorded game days -- currently only -1, the
        # half-built chain at day 25. Validated against the known set rather than a range, so a
        # typo still fails loudly instead of silently seeding something nobody asked for.
        if d in SYNTHETIC_RUNGS:
            continue
        if d < 0 or d >= season_days:
            raise ValueError(f"day {d} is outside 0..{season_days - 1} "
                             f"(synthetic rungs: {sorted(SYNTHETIC_RUNGS)})")

    # **Slots ~ episode_share x remaining length.** Episodes arrive in proportion to
    # `slots / (season_days - d)`, so multiplying the target by the length cancels the bias exactly
    # and each day lands on the share that was asked for. The equal-share case reduces to the
    # original `season_days - d`, which is why the old spelling keeps working unchanged.
    # A synthetic rung's key is not its length. `-1` is a half-built farm at day 25, so it must be
    # weighted as a 5-day episode; weighting it by `season_days - (-1)` = 31 gave it 6.2x the slots
    # its requested share called for, which is a confound sitting directly under P7.
    weights = {d: want[d] * float(season_days - SYNTHETIC_START_DAY.get(d, d))
               for d in sorted(want, reverse=True)}
    total = sum(weights.values())
    return {d: w / total for d, w in weights.items()}


def parse_mix(spec):
    """`"25:0.8,0:0.2"` -> `{25: 0.8, 0: 0.2}`, validated.

    Raises rather than normalising a bad spec. Fractions that do not sum to 1 would produce a batch
    whose composition is not the one asked for, and this project's standing rule is that a feature
    which silently runs as something other than what was requested is worse than one that fails.
    """
    # `length:25,20,15,10,0` asks for equal TERMINAL-EPISODE share per day rather than equal slots.
    # Spelled as a prefix rather than a separate flag so the two cannot both be set and disagree.
    text = str(spec).strip()
    if text.lower().startswith("length:"):
        body = [x.strip() for x in text.split(":", 1)[1].split(",") if x.strip()]
        # Both spellings behind the one prefix: `length:25,20,0` is an equal episode split, and
        # `length:0:0.6,25:0.1` names the episode share per day. Deciding on the presence of a
        # colon keeps them from being two flags that can disagree.
        if any(":" in p for p in body):
            if not all(":" in p for p in body):
                raise ValueError(
                    "mixed 'length:' forms: give every day a fraction (length:0:0.6,25:0.4) or "
                    "none of them (length:0,25), not a mixture -- the missing ones would silently "
                    "take a share nobody wrote down")
            return length_weighted_mix({int(p.split(":", 1)[0]): float(p.split(":", 1)[1])
                                        for p in body})
        return length_weighted_mix(int(x) for x in body)

    mix = {}
    for part in str(spec).split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise ValueError(f"mix entry {part!r} is not day:fraction (e.g. '25:0.8,0:0.2')")
        day_s, frac_s = part.split(":", 1)
        day, frac = int(day_s), float(frac_s)
        # **Synthetic rungs are deliberately NOT accepted in the plain form**, and that is pinned by
        # `test_a_day_outside_the_season_is_refused`. The reason holds on inspection: a synthetic
        # rung's whole problem is that its key is not its episode length, so it is only meaningful
        # once length weighting is applied -- which is exactly what the `length:` prefix turns on.
        # Allowing `-1:0.1` in the plain form would hand it a raw *slot* share and reintroduce the
        # 6.2x mis-allocation from the other direction.
        #
        # The message says so, rather than leaving the caller to guess why one spelling works.
        if day < 0 or day > 29:
            hint = (f" -- synthetic rungs {sorted(SYNTHETIC_RUNGS)} need the 'length:' form, which "
                    f"applies the episode-length weighting they require"
                    if day in SYNTHETIC_RUNGS else "")
            raise ValueError(f"mix day {day} is outside the season (0-29){hint}")
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


def states_at_mix(batch, mix, seed=0, min_bank=None, top=None, root="data", behind=False,
                  max_bank=None, shuffle=True, mirror=False, symmetric=False, with_days=False):
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
    # Per-slot seed day, built in the SAME order the pools are concatenated and permuted with the
    # same permutation. Returned rather than re-derived, because a second copy of this ordering
    # logic could drift from the first and the symptom would be per-day win rates attributed to the
    # wrong day -- correct-looking numbers measuring nothing, which is the failure mode this project
    # has hit repeatedly.
    day_labels = []
    pools = []
    for day, n in sorted(counts.items(), reverse=True):
        if not n:
            continue
        day_seed = seed + 1000 * day
        day_labels.extend([day] * n)
        if day < 0:
            # Negative keys are SYNTHETIC rungs, not recorded ones: -1 is the half-built chain at
            # day 25. Kept out of the positive-day space so a mix string still reads as game days.
            pools.append(chain_states(n))
            continue
        if day == 0:
            # **Day 0 is the actual start of a game, not a snapshot of somebody else's.**
            #
            # `states_at_day(.., day=0)` draws from `_turn_indices(.., 0)` = turns 1..48, median
            # ~turn 24 -- a full game-day in -- and `lo = max(1, (0 - DAY_WINDOW) * 24)` means turn
            # 0 is never drawn at all. Measured at startup, that rung began on **$623**, because by
            # turn ~24 the recorded player had converted ~$2,400 of its $3,000 into seed and
            # planted it.
            #
            # Symmetric seats made that *fair* -- both sides get the same position, richer ends the
            # winner -- and it was never a fairness problem. It was coverage. The competition starts
            # at turn 0 with $3,000 and bare tiles, 78% of slots were this rung, and the policy was
            # therefore trained to CONTINUE an elite opening and deployed to MAKE one. Both
            # measurements were right and disagreed: the rung read wr 0.59-0.72 while the same
            # checkpoint from `J.reset` ended on $1,104 of a $3,000 stake.
            #
            # `mirror`, `behind` and `symmetric` are all no-ops here by construction: a pristine
            # board is already identical on both seats, so there is no richer seat to inherit and
            # nothing to mirror.
            #
            # `reset_with_shops` rather than `reset`, for the reason recorded on `chain_states`: a
            # plain reset never opens a shop, so this rung -- 60% of the live run's slots -- was a
            # full 719-turn season in a market that bought a fifth of the wheat it should.
            pools.append(J.reset_with_shops(n, seed=day_seed))
            continue
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
    days = np.asarray(day_labels, dtype=np.int32)
    if symmetric:
        # Both sides get seat 0's position, so the ONLY difference between the players is what they
        # do. This makes the win rate directly interpretable, which it is not by default: the trainee
        # inherits the richer seat and a win can therefore be inherited rather than earned.
        stacked = _duplicate_seat(stacked, seat=0)
    if not shuffle:
        return (stacked, days) if with_days else stacked

    import jax.numpy as jnp

    np_order = np.random.default_rng(seed).permutation(batch)
    days = days[np_order]
    order = jnp.asarray(np_order)
    take = lambda x: jnp.take(x, order, axis=0)                              # noqa: E731
    out = stacked._replace(
        step_index=take(stacked.step_index),
        tiles=jax.tree_util.tree_map(take, stacked.tiles),
        farm=jax.tree_util.tree_map(take, stacked.farm),
        inventory=take(stacked.inventory),
        # Both halves of the unlock schedule take the same permutation, or a game ends up with one
        # row's unlock days against another row's shops.
        unlock_day=take(stacked.unlock_day),
        unlock_shop=take(stacked.unlock_shop),
    )
    return (out, days) if with_days else out


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
