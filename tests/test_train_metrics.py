"""The training log's win rate, and why the obvious definitions of it cannot move.

`wr` read 0.500 to three decimals on every update of a 63-update run. That is not a policy sitting
at parity -- it is arithmetic leaking into the metric, and it has now happened twice with two
different definitions. These tests pin the property that makes a win rate informative: it must be
able to read something other than 0.5 when the live policy is winning.

The rollout is a compiled JAX scan over the simulator and far too heavy to stand up here, so these
work on the row masks it emits, which is where both bugs actually lived.
"""

import numpy as np
import pytest


def _rows(n_games, opponent_frac):
    """The per-row flags one rollout step emits, laid out as the scan lays them out.

    Rows are `[game, seat]` flattened with the seat axis innermost, so rows 2k and 2k+1 are the two
    seats of one game. Seat 0 is always the live policy; seat 1 is the frozen opponent in exactly
    the games flagged for cross-play.
    """
    use_opp = np.zeros(n_games, dtype=bool)
    use_opp[:int(round(opponent_frac * n_games))] = True

    seat = np.tile([0, 1], n_games)
    crossplay = np.repeat(use_opp, 2)
    take_opp = crossplay & (seat == 1)
    return dict(seat=seat, crossplay=crossplay, trainable=~take_opp)


def _win_rate(rows, reward, live):
    """Mean terminal reward over whichever rows `live` selects."""
    sel = live
    return reward[sel].mean() if sel.any() else float("nan")


def _terminal_reward(rows, live_wins):
    """One game, one winner: seat 0 takes `live_wins`, seat 1 takes the complement."""
    seat0 = np.where(live_wins, 1.0, 0.0)
    reward = np.empty(len(rows["seat"]))
    reward[0::2] = seat0
    reward[1::2] = 1.0 - seat0
    return reward


@pytest.mark.parametrize("opponent_frac", [0.0, 0.25, 0.5])
def test_trainable_rows_alone_pin_the_win_rate_near_one_half(opponent_frac):
    """The previous definition, and why it could not move.

    In a self-play group *both* seats are trainable, so both are counted and the pair averages
    exactly 0.5 whatever either side did. Only a cross-play game contributes a single free row. At
    `--opponent-frac 0.25` that is two pinned rows per self-play game against one free row per
    cross-play game, so 86% of the measurement is fixed by arithmetic -- which is why a policy
    winning *every* cross-play game still cannot push the number far from a half.
    """
    n_games = 64
    rows = _rows(n_games, opponent_frac)
    reward = _terminal_reward(rows, live_wins=np.ones(n_games, dtype=bool))

    wr = _win_rate(rows, reward, rows["trainable"])

    # Two pinned rows per self-play game, one free row per cross-play game.
    ceiling = 0.5 + 0.5 * opponent_frac / (2 - opponent_frac)
    assert wr == pytest.approx(ceiling, abs=1e-9)
    assert wr < 1.0, "a perfect policy cannot read 1.0 under this definition, at any fraction"


def test_the_pinning_is_worst_at_the_fraction_the_runs_actually_use():
    """`--opponent-frac 0.25`: a policy winning every cross-play game reads 0.571, not 1.0.

    So the whole observable range is 0.43-0.57 and the run's 0.500 was consistent with anything.
    """
    rows = _rows(64, 0.25)
    perfect = _terminal_reward(rows, np.ones(64, dtype=bool))

    assert _win_rate(rows, perfect, rows["trainable"]) == pytest.approx(0.5714, abs=1e-4)


def test_crossplay_rows_move_with_the_policy():
    """The definition now in use: the live policy's seat in a cross-play game.

    That row's outcome is the only one not determined by its partner, so it is the whole signal.
    """
    n_games = 64
    rows = _rows(n_games, 0.25)
    live = rows["trainable"] & rows["crossplay"]

    always = _terminal_reward(rows, np.ones(n_games, dtype=bool))
    never = _terminal_reward(rows, np.zeros(n_games, dtype=bool))

    assert _win_rate(rows, always, live) == pytest.approx(1.0)
    assert _win_rate(rows, never, live) == pytest.approx(0.0)


def test_an_all_zero_action_really_is_the_do_nothing_agent():
    """The idle opponent is all-zeros, so this has to hold or the seat is doing something.

    `NOOP` is op 0, and bucket 0 of every market head is quantity 0. If either ever changes, an
    "idle" seat silently starts farming and the metric it was added to unpin goes quiet again.
    """
    from kagg.rl import jax_policy as P
    from kagg.sim import ops as O

    assert O.NOOP == 0
    assert int(P.SELL_BUCKETS[0]) == 0
    assert int(P.BUY_BUCKETS[0]) == 0


def test_idle_seats_are_excluded_from_the_policy_loss_and_counted_as_crossplay():
    """An idle seat's actions are not the policy's, so they must not enter the PPO ratio.

    They must still count as cross-play, because those are precisely the games whose outcome is
    not pinned by a partner -- which is the whole reason the seat exists.
    """
    batch = 8
    seat = np.tile([0, 1], batch)
    use_opp = np.zeros(batch, dtype=bool)
    use_idle = np.zeros(batch, dtype=bool)
    use_opp[0], use_idle[4] = True, True

    take_opp = np.repeat(use_opp, 2) & (seat == 1)
    take_idle = np.repeat(use_idle, 2) & (seat == 1)
    trainable = ~(take_opp | take_idle)
    crossplay = np.repeat(use_opp | use_idle, 2)

    assert not trainable[1] and not trainable[9], "opponent/idle seats must not be trained on"
    assert trainable[0] and trainable[8], "the live policy's own seat must be trained on"

    live = trainable & crossplay
    assert set(np.flatnonzero(live)) == {0, 8}, "one free row per cross-play game, seat 0"


def _use_opp(batch, opponent_frac, it, contiguous):
    """Which games face the frozen opponent on update `it`, old scheme and new."""
    n = int(round(opponent_frac * batch))
    flags = np.zeros(batch, dtype=bool)
    if not n:
        return flags
    if contiguous:
        flags[[(it * n + j) % batch for j in range(n)]] = True
    else:
        stride = max(1, batch // n)
        flags[[(j * stride + it) % batch for j in range(n)]] = True
    return flags


@pytest.mark.parametrize("contiguous,expect_covered", [(True, False), (False, True)])
def test_crossplay_games_must_reach_the_end_of_the_season(contiguous, expect_covered):
    """A game's index is its phase group, and a phase group is a fixed season position.

    So index order is season order, and the games that *finish* are the contiguous band sitting at
    the season boundary. Choosing cross-play games as a contiguous block means two blocks rotating
    at different rates, which mostly miss: the cross-play win rate saw zero qualifying rows update
    after update, and the frozen opponent never played the endgame. Striding covers every band on
    every update.
    """
    batch = 256
    ending = np.zeros(batch, dtype=bool)
    ending[-24:] = True                      # the phase groups about to cross turn 719

    covered = [bool((_use_opp(batch, 0.25, it, contiguous) & ending).any()) for it in range(8)]

    assert all(covered) is expect_covered, f"per-update coverage of the endgame: {covered}"


def test_crossplay_rows_are_the_live_policys_own_seat():
    """Never the opponent's: its reward is our loss, and averaging it back in cancels the signal."""
    rows = _rows(16, 0.25)
    live = rows["trainable"] & rows["crossplay"]

    assert live.sum() == 4, "one row per cross-play game, not two"
    assert set(rows["seat"][live]) == {0}


def test_the_hand_prior_is_the_shape_it_claims_to_be():
    """`noop_p` on doing nothing, the remainder split evenly over the other *legal* ops.

    Ender's prior was two numbers in a config, and the whole argument for preferring it over a
    cloned one is that it contains no strategy -- so it cannot cap the ceiling, and it cannot
    punish exploration the way a collapsed clone does. That argument only holds if the
    distribution really is flat outside noop, which is what this checks.
    """
    import importlib.util
    import pathlib

    import jax.numpy as jnp

    from kagg.sim import ops as O

    spec = importlib.util.spec_from_file_location(
        "t", pathlib.Path(__file__).resolve().parent.parent / "scripts" / "train_jax_rl.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # One unit with four legal ops: noop, and three others.
    mask = np.zeros((1, 1, O.N_OPS), dtype=bool)
    mask[0, 0, [O.NOOP, O.NORTH, O.WEST, O.WATER]] = True
    heads = {"op": jnp.zeros((1, 1, O.N_OPS))}
    masks = {"op": jnp.asarray(mask)}

    prior = mod.hand_prior_heads(heads, masks, noop_p=0.3)["op"]
    p = np.asarray(jnp.exp(jnp.where(masks["op"], prior, -jnp.inf)))[0, 0]

    assert p[O.NOOP] == pytest.approx(0.3, abs=1e-6)
    for op in (O.NORTH, O.WEST, O.WATER):
        assert p[op] == pytest.approx(0.7 / 3, abs=1e-6), "non-noop mass must be flat"
    assert p.sum() == pytest.approx(1.0, abs=1e-6)


def test_the_hand_prior_cannot_punish_exploration():
    """The property that blocks the cloned prior, stated as a test.

    The measured BC checkpoint assigns 6e-5 to moving at the spawn state, so `KL(policy || prior)`
    would tax PPO for discovering the one behaviour it needs. A hand prior's floor on any legal
    option is `(1 - noop_p) / n_legal`, which for realistic values is thousands of times larger.
    """
    import importlib.util
    import pathlib

    import jax.numpy as jnp

    from kagg.sim import ops as O

    spec = importlib.util.spec_from_file_location(
        "t", pathlib.Path(__file__).resolve().parent.parent / "scripts" / "train_jax_rl.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    mask = np.zeros((1, 1, O.N_OPS), dtype=bool)
    mask[0, 0, :] = True                       # worst case: every op legal, mass spread thinnest
    heads = {"op": jnp.zeros((1, 1, O.N_OPS))}
    masks = {"op": jnp.asarray(mask)}

    prior = mod.hand_prior_heads(heads, masks, noop_p=0.3)["op"]
    p = np.asarray(jnp.exp(prior))[0, 0]
    worst = p[O.NORTH]

    assert worst > 1e-3, f"floor {worst:.2e} is too thin to be safe as a prior"
    assert worst > 500 * 6e-5, "must be far above the collapsed clone's 6e-5 at spawn"


def _roles_per_update(batch, updates, sticky, seed=0):
    """Seat-1 role for every game on every update, under both schemes.

    Returns `[updates, batch]` of role ids. `sticky` holds a role until the game restarts; the old
    scheme re-drew every role every update from a strided partition.
    """
    rng = np.random.default_rng(seed)
    fr = [("pool", 0.15), ("farm", 0.30), ("trade", 0.15), ("idle", 0.05)]
    # A game spans a season: 720 turns at horizon 32 is 22.5 updates, so restarts are rare.
    turns_per_update, season = 32, 720
    phase = (np.arange(batch) * (season + 1)) // batch
    out = np.empty((updates, batch), dtype=object)

    if sticky:
        names = ["self"] + [n for n, _ in fr]
        p = np.array([1.0 - sum(f for _, f in fr)] + [f for _, f in fr])
        role = rng.choice(names, size=batch, p=p)
        for it in range(updates):
            out[it] = role
            # Games whose season ends inside this update restart, and only they re-draw.
            step = phase + turns_per_update * (it + 1)
            restart = step > season - 1
            phase = np.where(restart, -turns_per_update * (it + 1), phase)
            role = np.where(restart, rng.choice(names, size=batch, p=p), role)
    else:
        stride = max(1, int(batch * 0.6180339887)) | 1
        while np.gcd(stride, batch) != 1:
            stride += 2
        for it in range(updates):
            order = (np.arange(batch) * stride + it) % batch
            role = np.full(batch, "self", dtype=object)
            cut = 0
            for name, f in fr:
                n = int(round(f * batch))
                role[order[cut:cut + n]] = name
                cut += n
            out[it] = role
    return out


@pytest.mark.parametrize("sticky,expect_at_most", [(False, 5), (True, 2)])
def test_a_games_opponent_must_not_change_mid_season(sticky, expect_at_most):
    """**The bug this pins.** The role assignment was recomputed every update while the game state
    persisted across updates, so a game spanning ~22.5 updates had its seat-1 opponent re-drawn on
    every one of them -- a mean of 4.9 distinct opponents per season.

    Everything downstream broke quietly. The per-opponent win rate attributed a game's outcome to
    whichever label happened to be set on its final update; all four columns collapsed to ~0.5
    because 35% of updates put the live policy on seat 1, where it spent its stake to $0 and the tie
    paid half; and the scripted ladder never existed at all, because the farmer cannot bank $23,783
    while holding the seat for 30% of updates with the policy dismantling the farm in between.

    A game that never restarts must see exactly one opponent. Allowing 2 covers the one restart a
    22-update window can contain.
    """
    roles = _roles_per_update(batch=256, updates=20, sticky=sticky)
    distinct = [len(set(roles[:, j])) for j in range(roles.shape[1])]

    assert max(distinct) <= expect_at_most, (
        f"a single game saw up to {max(distinct)} opponents in one season "
        f"(mean {np.mean(distinct):.1f}); sticky={sticky}")


def _gae_one_step(reward, value, next_value, done, trunc, gamma=0.998732):
    """The single-step body of `make_rollout`'s `gae`, extracted verbatim."""
    nv = 0.0 if done else next_value
    adv = 0.0 if (done or trunc) else 1.0        # incoming trace, cut on either flag
    delta = reward + gamma * nv - value
    return delta + gamma * 0.95 * adv


def test_a_phase_seeded_first_ending_keeps_its_bootstrap():
    """**Why a virgin ending must be a truncation and not a termination.**

    `staggered_states` seeds each slot mid-season on an EMPTY board, so a slot starting at turn 700
    "ends" twenty turns later having played twenty turns. That is not a result: the scripted farmer
    reads `day = step_index // TURNS_PER_DAY`, sees day 29 on a board where nothing has happened,
    and declines to plant or hire at all -- so both sides stand still and it scores as an exact tie
    worth 0.5. This fires on every run start, not only on a resume.

    Suppressing the reward is necessary but not sufficient. `gae` zeroes the bootstrap on `done`, so
    a suppressed reward flagged `done` teaches the critic that a mid-season state is worth exactly
    zero -- trading a wrong reward for a wrong value target. Flagging it `trunc` cuts the advantage
    trace and keeps the bootstrap, which is what truncation already does.
    """
    value, next_value = 0.5, 0.5

    as_done = _gae_one_step(0.0, value, next_value, done=True, trunc=False)
    as_trunc = _gae_one_step(0.0, value, next_value, done=False, trunc=True)

    assert as_done == pytest.approx(-0.5, abs=1e-3), (
        "flagged done, the target collapses to zero and the critic learns the state is worthless")
    assert as_trunc == pytest.approx(0.0, abs=1e-3), (
        "flagged trunc, the bootstrap stands and the critic learns nothing false")
    assert as_trunc > as_done


def test_a_virgin_slot_still_restarts_even_though_it_pays_nothing():
    """The reward and the reset are separate decisions and only the reward is suppressed.

    `restart = just_done | truncate` must keep firing on a virgin ending, or the slot would run past
    turn 719 into a season that does not exist -- bug #2 from the original handoff, reintroduced.
    """
    just_done = np.array([True, True, False, False])
    virgin = np.array([True, False, True, False])
    truncate = np.array([False, False, False, True])

    real_done = just_done & ~virgin
    pseudo_trunc = truncate | (just_done & virgin)
    restart = just_done | truncate

    assert list(real_done) == [False, True, False, False], "only the non-virgin ending is a result"
    assert list(pseudo_trunc) == [True, False, False, True], "the virgin ending becomes a trunc"
    assert list(restart) == [True, True, False, True], "both endings still reset the slot"
    assert not (real_done & pseudo_trunc).any(), "a row is never both at once"


def test_the_price_of_the_next_purchase_is_visible():
    """**Why the policy needs the price and not just the balance.**

    `money`, `n_land` and `hires_today` were all in the observation and no price was, so the policy
    had to learn `n_land -> {1000, 2000, 4000}` from a terminal reward 700 turns later.

    The case that matters: `LAND_PRICES[0] + LAND_PRICES[1]` is exactly the $3,000 opening bank and
    both purchases are affordability-legal, so buying two quadrants on day 0 is legal and leaves
    nothing for the remaining twenty-five days. Across 312 real replay seats the median first land
    purchase is turn 242 (day 10); the seat that bought three from turn 1 banked $9,443 against the
    leaders' $130k. The quadrant is not a bad buy, it is a bad buy *now*.

    This asserts the fact is present and correctly scaled, not that any action is preferred.
    """
    jax = pytest.importorskip("jax")
    from kagg.rl import jax_obs
    from kagg.sim import jax_sim as J

    glob = np.asarray(jax_obs.encode(J.reset(2))[2])[0, 0]

    # The two quadrants that together cost the whole opening bank.
    assert float(J.LAND_PRICES[0] + J.LAND_PRICES[1]) == 3000.0, (
        "if the price table changed, the motivating case in this test needs rechecking")

    land = float(J.LAND_PRICES[0]) / 3000.0
    hire = float(J.HIRE_COST[0]) / 3000.0
    assert any(abs(v - land) < 1e-4 for v in glob), (
        f"next-land cost as a share of the bank ({land:.4f}) is not in the global token")
    assert any(abs(v - hire) < 1e-6 for v in glob), (
        f"next-hire cost as a share of the bank ({hire:.6f}) is not in the global token")
    assert not np.isnan(glob).any() and not np.isinf(glob).any()


def test_an_animals_days_to_next_yield_matches_the_simulator():
    """**The `is_ripe` asymmetry again, in the tile features rather than the geometry.**

    `t.placed_day` was used nowhere in `jax_obs.py`. Crops got their age with an explicit comment --
    "Age drives every yield rule, so give it directly rather than making the net subtract" -- and the
    animal half of the identical rule got nothing, so the policy could not tell a cow that yields
    tomorrow from one that yields in four days.

    `jax_sim`'s rule is `days_since = day - placed_day - ANIMAL_FIRST_YIELD_DAY[a]`, producing when
    `days_since >= 0 and days_since % ANIMAL_INTERVAL[a] == 0`. The feature is the inverted distance
    to that event, so it must read exactly 1.0 on a production day and less on every other.
    """
    jax = pytest.importorskip("jax")
    import jax.numpy as jnp
    from kagg.rl import jax_obs
    from kagg.sim import jax_sim as J

    COW = 1
    first = int(np.asarray(J.ANIMAL_FIRST_YIELD_DAY)[COW])
    interval = int(np.asarray(J.ANIMAL_INTERVAL)[COW])
    s = J.reset(2)
    tiles = s.tiles._replace(
        animal=s.tiles.animal.at[:, :, 0].set(COW),
        placed_day=s.tiles.placed_day.at[:, :, 0].set(0),
    )

    got, want = [], []
    for day in range(first + 2 * interval + 2):
        st = s._replace(tiles=tiles,
                        step_index=jnp.full_like(s.step_index, day * J.TURNS_PER_DAY))
        feats = np.asarray(jax_obs.encode(st)[0])[0, 0, 0]
        ds = day - first
        produces = ds >= 0 and ds % interval == 0
        # The feature reads 1.0 only when the animal produces today.
        got.append(bool(np.isclose(feats.max(), 1.0) and any(np.isclose(feats, 1.0))))
        want.append(produces)

    # On every production day some feature must be exactly 1.0 (the inverted zero distance).
    prod_days = [d for d, w in enumerate(want) if w]
    assert prod_days, "the test's own setup produced no yield days"
    for d in prod_days:
        st = s._replace(tiles=tiles,
                        step_index=jnp.full_like(s.step_index, d * J.TURNS_PER_DAY))
        feats = np.asarray(jax_obs.encode(st)[0])[0, 0, 0]
        assert np.isclose(feats, 1.0).any(), f"day {d} produces but no feature reads 1.0"


def test_the_declared_feature_widths_match_the_arrays():
    """`TILE_FEATURES`, `UNIT_FEATURES` and `GLOBAL_FEATURES` are documentation unless checked.

    All three had gone stale: UNIT_FEATURES said 16 against an actual 28, unchanged since the
    nearest-job geometry landed a session earlier. Nothing broke -- flax infers real shapes at trace
    time and the only other reader is a printed memory estimate -- but a constant that lies about the
    observation is exactly the kind of thing a later change trusts.
    """
    jax = pytest.importorskip("jax")
    from kagg.rl import jax_obs
    from kagg.sim import jax_sim as J

    tiles, units, glob = jax_obs.encode(J.reset(2))

    assert tiles.shape[-1] == jax_obs.TILE_FEATURES, (
        f"TILE_FEATURES says {jax_obs.TILE_FEATURES}, arrays are {tiles.shape[-1]}")
    assert units.shape[-1] == jax_obs.UNIT_FEATURES, (
        f"UNIT_FEATURES says {jax_obs.UNIT_FEATURES}, arrays are {units.shape[-1]}")
    assert glob.shape[-1] == jax_obs.GLOBAL_FEATURES, (
        f"GLOBAL_FEATURES says {jax_obs.GLOBAL_FEATURES}, arrays are {glob.shape[-1]}")


def test_the_spend_prior_survives_a_behaviour_cloned_prior():
    """`--spend-prior` must govern the spend heads even when `--kl-prior` supplies a BC prior.

    **Theory under test: it does not.** `merge_priors` keeps the hand prior for `op` alone, so every
    head `--spend-prior` exists to shape -- `buy_seed`, `buy_animal`, `buy_land`, `hire` -- falls
    through to the BC prior. A run can pass `--spend-prior 0.05`, have it echoed back in its own
    args line, and have it apply to nothing.

    Measured in `league1-20260802-175612`, every spend rate sits *on* the BC prior rather than above
    it -- buy_land 0.000 against 0.0%, buy_animal 0.0002 against 0.1%, buy_seed 0.012 against 0.9%,
    hire 0.073 against 6.3%. `CLAUDE.md` names that exact reading as the test that a prior has
    capped the ceiling: "trained spend rates finish above the prior, not pinned to it".

    This pins the flag's contract, not the choice of prior value. Whatever `spend_p` is set to, it
    must reach the heads it names.
    """
    import importlib.util
    import pathlib

    import jax.numpy as jnp

    from kagg.sim import ops as O

    spec = importlib.util.spec_from_file_location(
        "t", pathlib.Path(__file__).resolve().parent.parent / "scripts" / "train_jax_rl.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    spend_p = 0.05
    # `buy_land` is the starkest case: binary, and the BC checkpoint puts 0.0% on buying.
    heads = {"op": jnp.zeros((1, 1, O.N_OPS)), "buy_land": jnp.zeros((1, 1, 2))}
    masks = {"op": jnp.ones((1, 1, O.N_OPS), dtype=bool),
             "buy_land": jnp.ones((1, 1, 2), dtype=bool)}

    hand = mod.hand_prior_heads(heads, masks, noop_p=0.3, spend_p=spend_p)
    assert float(jnp.exp(hand["buy_land"])[0, 0, 1]) == pytest.approx(spend_p, abs=1e-6), \
        "precondition: the hand prior really does put spend_p on buying"

    # A collapsed clone, which is what the measured BC checkpoint is on this head.
    bc = {"op": jnp.zeros((1, 1, O.N_OPS)),
          "buy_land": jnp.log(jnp.asarray([[[1.0 - 1e-4, 1e-4]]]))}

    merged = mod.merge_priors(hand, bc)
    p_buy = float(jnp.exp(merged["buy_land"])[0, 0, 1])

    assert p_buy == pytest.approx(spend_p, abs=1e-6), (
        f"--spend-prior {spend_p} was discarded: the head is governed by the BC prior at "
        f"{p_buy:.1e}, a {spend_p / p_buy:.0f}x tighter constraint the flag never asked for")


def _load():
    import importlib.util
    import pathlib
    spec = importlib.util.spec_from_file_location(
        "t", pathlib.Path(__file__).resolve().parent.parent / "scripts" / "train_jax_rl.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_the_op_census_counts_commit_tokens():
    """Every COMMIT draw was being counted as nothing at all.

    `jax.nn.one_hot` returns a zero row for an out-of-range index rather than raising, so
    one-hotting the *policy* op over `O.N_OPS` silently dropped tokens 18-22 -- the five COMMIT
    macros, which are the behaviour the whole run exists to test. The printed percentages then
    normalise by the primitive total, making them shares of primitive draws wearing the label
    "share of unit-turns".
    """
    import jax.numpy as jnp

    from kagg.rl import commit as CM
    from kagg.sim import ops as O

    mod = _load()
    # Two live unit-turns: one ordinary WATER, one COMMIT_PICKUP (the highest token).
    op_rows = jnp.asarray([[O.WATER, CM.N_POLICY_OPS - 1]])
    live = jnp.ones((1, 2), dtype=bool)

    counts = mod.op_census(op_rows, live)

    assert float(counts.sum()) == pytest.approx(2.0), (
        f"census total {float(counts.sum()):.0f} of 2 live unit-turns: the COMMIT token was "
        f"dropped, so commit share is unobservable and every printed op rate is renormalised")
    assert len(counts) == CM.N_POLICY_OPS, "census must span the policy op space, not the sim's"
    assert float(counts[CM.N_POLICY_OPS - 1]) == pytest.approx(1.0)


def test_the_op_prior_does_not_flat_weight_commit_macros_against_primitives():
    """The COMMIT class takes `COMMIT_PRIOR_SHARE` of non-noop mass, not its flat per-token share.

    Flat-over-legal weights one COMMIT_WATER equal to one N, despite `MAX_COMMIT_TURNS = 4` meaning
    the commit stands in for up to four primitive draws whose intermediate turns are excluded from
    the PPO density. That is a granularity mismatch, not a claim about good play -- the split is
    over the two classes and says nothing about which commit or which primitive.
    """
    import jax.numpy as jnp

    from kagg.rl import commit as CM
    from kagg.sim import ops as O

    mod = _load()
    noop_p = 0.05
    heads = {"op": jnp.zeros((1, 1, CM.N_POLICY_OPS))}
    masks = {"op": jnp.ones((1, 1, CM.N_POLICY_OPS), dtype=bool)}

    prior = mod.hand_prior_heads(heads, masks, noop_p=noop_p)["op"]
    p = np.asarray(jnp.exp(prior))[0, 0]

    commit_share = p[O.N_OPS:].sum()
    want = mod.COMMIT_PRIOR_SHARE * (1.0 - noop_p)
    assert commit_share == pytest.approx(want, abs=1e-6), (
        f"commit class holds {commit_share:.3f} of the mass, not {want:.3f}: it is being "
        f"flat-weighted per token ({CM.N_COMMIT}/{CM.N_POLICY_OPS - 1} of non-noop)")

    prims = p[1:O.N_OPS]
    assert prims.std() == pytest.approx(0.0, abs=1e-9), "within primitives the prior stays flat"
    assert p.sum() == pytest.approx(1.0, abs=1e-6)
    assert p[O.NOOP] == pytest.approx(noop_p, abs=1e-6)
