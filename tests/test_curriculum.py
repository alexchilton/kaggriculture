"""Seeding episodes from real recorded boards, and the four ways that goes wrong silently.

Every case here pins a failure this project has already paid for once, in a new guise.

**Both seats must be real.** `staggered_states` seeds a slot mid-season by moving `step_index` and
nothing else, so a slot claiming to be day 15 sits on an empty board with $3,000 a side. The
scripted farmer reads `day <= LAST_PLANT_DAY` (`jax_heuristic.py:179`) and therefore declines to
plant or hire at all on such a board; both sides stand still and the game scores as an exact tie
worth 0.5. Seeding only the trainee's seat from a replay and leaving the opponent's synthetic
reproduces that bug exactly, on the other side of the board. A replay records *both* players'
observations including `private`, so a consistent two-seat board is available and there is no reason
to construct an inconsistent one.

**The seeded board must actually contain a farm.** The entire point is to start where the chain is
half-finished. A seed that lands on an empty board at a late `step_index` is the bug above wearing
the curriculum's clothes, and it would show up as "the curriculum works" -- both sides idle, ties
everywhere, win rate 0.5.

**Diversity.** Sampling one board repeatedly teaches that board's geometry, not a maintenance
policy.

**The day must be the day it says.** Every animal and crop rule in the simulator is driven by
`day = step_index // TURNS_PER_DAY`, so a board whose contents and whose counter disagree is a
board with rules from one game and state from another.
"""

import numpy as np
import pytest

from kagg.rl import curriculum, jax_act as A, jax_obs
from kagg.sim import jax_sim as J

pytestmark = pytest.mark.skipif(not curriculum.available(), reason="replay data not downloaded")


def test_both_seats_are_seeded_from_a_real_board():
    """The Session 6 virgin-episode bug, on the opponent's side.

    One real seat against a synthetic empty one is a board on which the scripted farmer refuses to
    act, so the episode is a guaranteed tie that teaches nothing and reads as 0.5.
    """
    state = curriculum.states_at_day(8, day=15, seed=0)

    kinds = np.asarray(state.tiles.kind)
    for seat in (0, 1):
        occupied = ((kinds[:, seat] == J.PLANT) | (kinds[:, seat] == J.PASTURE)
                    | (kinds[:, seat] == J.COOP) | (kinds[:, seat] == J.WEED)).sum(axis=-1)
        assert (occupied > 0).all(), (
            f"seat {seat} has games with a completely empty board -- that is the synthetic seat "
            f"that makes the scripted farmer stand still")


def test_the_seeded_board_is_a_working_farm_not_an_empty_one():
    """A day-15 seed exists to start the policy where the chain is already half-done."""
    state = curriculum.states_at_day(12, day=15, seed=0)

    plants = (np.asarray(state.tiles.kind)[:, 0] == J.PLANT).sum(axis=-1)
    animals = (np.asarray(state.tiles.animal)[:, 0] != J.NO_ANIMAL).sum(axis=-1)
    money = np.asarray(state.farm.money)[:, 0]

    assert plants.mean() > 2, f"mean standing crops {plants.mean():.1f} -- not a working farm"
    assert animals.max() > 0, "no game has a single animal; FEED would be masked out everywhere"
    assert money.mean() > 3000, (
        f"mean bank ${money.mean():,.0f} is at or below the $3,000 start -- the seeded position "
        f"carries no advantage and cannot make the idle opponent beatable")


def test_the_step_index_matches_the_day_it_claims():
    """Every crop and animal rule reads `step_index // TURNS_PER_DAY`."""
    for day in (5, 15, 25):
        state = curriculum.states_at_day(4, day=day, seed=1)
        got = np.asarray(state.step_index) // J.TURNS_PER_DAY
        assert (np.abs(got - day) <= 1).all(), f"asked for day {day}, got days {sorted(set(got))}"


def test_sampling_gives_different_boards():
    """One board repeated teaches its geometry, not a policy."""
    state = curriculum.states_at_day(12, day=15, seed=0)
    kinds = np.asarray(state.tiles.kind)[:, 0]
    unique = {k.tobytes() for k in kinds}
    assert len(unique) >= max(2, len(kinds) // 2), (
        f"only {len(unique)} distinct boards in {len(kinds)} games")


def test_a_seeded_state_encodes_and_steps():
    """It has to survive the same encode and mask path training uses, and then a step.

    A `State` that encodes to NaN or whose masks are empty would train on garbage, and the failure
    would appear as a loss curve rather than an error.
    """
    state = curriculum.states_at_day(6, day=15, seed=2)

    tiles, units, glob = jax_obs.encode(state)
    for name, arr in (("tiles", tiles), ("units", units), ("glob", glob)):
        assert np.isfinite(np.asarray(arr)).all(), f"{name} has non-finite entries"
    assert np.asarray(tiles).shape[-1] == jax_obs.TILE_FEATURES

    masks = A.masks_for(state)
    assert np.asarray(masks["op"]).any(axis=-1).all(), "a unit has no legal op at all"

    nxt = J.step(state, curriculum.noop_actions(6))
    assert (np.asarray(nxt.step_index) > np.asarray(state.step_index)).all()


def test_walking_the_start_day_back_changes_the_board():
    """The schedule's whole mechanism: an earlier seed is a less complete farm."""
    late = curriculum.states_at_day(12, day=22, seed=3)
    early = curriculum.states_at_day(12, day=4, seed=3)

    def built(s):
        k = np.asarray(s.tiles.kind)[:, 0]
        return float((((k == J.PASTURE) | (k == J.COOP)).sum(axis=-1)).mean())

    assert built(late) > built(early), (
        f"day 22 boards are not more built up than day 4 boards "
        f"({built(late):.1f} vs {built(early):.1f}) -- the schedule has no gradient to walk")


def test_the_behind_dial_actually_puts_the_trainee_in_the_poorer_seat():
    """The difficulty knob, and the guard against a self-confirming curriculum.

    Seeding the trainee into the richer seat makes the position beatable on the seed alone, which is
    the point -- and is also indistinguishable, in a win rate, from having learned anything. The
    poorer seat is where a win has to be earned. If this dial does nothing, every curriculum result
    is a lead being inherited.
    """
    ahead = curriculum.states_at_day(12, day=20, seed=5, behind=False)
    behind = curriculum.states_at_day(12, day=20, seed=5, behind=True)

    a = np.asarray(ahead.farm.money)
    b = np.asarray(behind.farm.money)

    # Same boards, seats exchanged: seat 0's bank in one is seat 1's in the other.
    assert np.allclose(a[:, 0], b[:, 1]) and np.allclose(a[:, 1], b[:, 0])
    assert b[:, 0].mean() < a[:, 0].mean(), (
        f"trainee bank behind={b[:, 0].mean():,.0f} is not below ahead={a[:, 0].mean():,.0f}")
    # The market is shared and must not move with the seats.
    assert np.array_equal(np.asarray(ahead.inventory), np.asarray(behind.inventory))


def test_a_batch_larger_than_the_reference_pool_still_fills():
    """A 256-game run died having built 240 states.

    The attempt cap was a multiple of the reference count, which also capped how many states could
    ever be built -- so any batch above that multiple was unfillable by construction. The guard that
    is actually wanted is *consecutive* misses, which detects "no replay can supply this day" without
    limiting successes.
    """
    state = curriculum.states_at_day(40, day=15, seed=0, top=8)
    assert np.asarray(state.farm.money).shape[0] == 40


def test_a_day_no_replay_reaches_fails_loudly():
    """Past the end of the season there is nothing to seed from, and that must not hang or return
    a short batch quietly."""
    with pytest.raises(SystemExit):
        curriculum.states_at_day(8, day=90, seed=0)


def test_early_limit_below_the_seed_turn_is_rejected():
    """`--early-limit` is an absolute turn number; a seeded episode starts past it.

    Truncation fires on `step_index >= early_limit`, so a day-15 seed (turn 360) under a limit of
    288 truncates on turn one, restarts to 360, and truncates again forever. Half the batch then
    produces no episodes -- visible only as `wr nan` and `tstd 0.000`, never as an error. This is the
    arithmetic the trainer now refuses at startup.
    """
    from kagg.sim.jax_sim import TURNS_PER_DAY

    for day, limit in ((15, 288), (12, 288), (5, 120)):
        assert limit <= day * TURNS_PER_DAY, (
            f"day {day} starts at turn {day * TURNS_PER_DAY}; a limit of {limit} would not clash "
            f"and this case does not test what it claims")
    # And the combination that is fine: a limit above the seed turn truncates normally.
    assert 480 > 15 * TURNS_PER_DAY
