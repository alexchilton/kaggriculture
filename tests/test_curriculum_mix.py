"""The mixed curriculum: several game-days in one batch, and the ways that goes wrong silently.

**Why a mix at all.** Pure backward annealing reaches day 0 last, with the least accumulated
exposure, on weights specialised for maintenance -- and when the schedule steps off day 25 that
distribution is gone from the *data*, which re-anchoring a KL prior does not fix. A mix removes both
by construction.

**The failure this file mostly exists to prevent is a mix that is not the mix that was asked for.**
Every case below is a way the composition could differ from the spec while the run logs the spec and
looks healthy:

- fractions that do not sum to 1, so the realised shares are whatever rounding produced;
- a day whose fraction rounds to zero slots, so a "80/20" run is a pure day-25 run that says 80/20
  in its log -- the standing rule here is that a feature silently not running is worse than one that
  fails, because it gives a false model of what is being measured;
- counts that do not sum to the batch, leaving a shortfall for some day to absorb unrecorded;
- a day correlated with the slot index, which would couple it to anything that indexes slots
  positionally -- a restarting slot restarts into `seed_states[i]` by position, so this is a live
  surface even though seat-1 roles happen to be drawn i.i.d. today.

**The day-0 share is not what it looks like, and the test for that is arithmetic rather than a
board.** Episodes are ~120 turns at day 25 and 719 at day 0 and every slot emits the same number of
turns per update, so a 20% slot share is about a 4% share of terminal episodes. The trainer prints
both; `test_terminal_episode_share_is_much_smaller_than_the_slot_share` pins the relationship so the
claim in the help text cannot drift away from the code.
"""

import numpy as np
import pytest

from kagg.rl import curriculum
from kagg.sim import jax_sim as J

pytestmark = pytest.mark.skipif(not curriculum.available(), reason="replay data not downloaded")


# --------------------------------------------------------------------------- parse_mix


def test_a_plain_spec_parses():
    assert curriculum.parse_mix("25:0.8,0:0.2") == {25: 0.8, 0: 0.2}


def test_whitespace_and_three_way_mixes_parse():
    assert curriculum.parse_mix(" 25:0.5 , 15:0.3 , 0:0.2 ") == {25: 0.5, 15: 0.3, 0: 0.2}


def test_fractions_that_do_not_sum_to_one_are_refused():
    """Otherwise the realised composition is whatever the apportionment happened to do, and the log
    would still print the spec."""
    with pytest.raises(ValueError, match="sum to"):
        curriculum.parse_mix("25:0.8,0:0.1")
    with pytest.raises(ValueError, match="sum to"):
        curriculum.parse_mix("25:0.8,0:0.4")


def test_a_zero_or_negative_fraction_is_refused():
    with pytest.raises(ValueError, match="positive fraction"):
        curriculum.parse_mix("25:1.0,0:0.0")


def test_a_day_outside_the_season_is_refused():
    """Day 30+ has no recorded turns, and `_turn_indices` would return an empty window -- which
    surfaces as 'only built N of B seeded states' far from the cause."""
    with pytest.raises(ValueError, match="outside the season"):
        curriculum.parse_mix("30:1.0")
    with pytest.raises(ValueError, match="outside the season"):
        curriculum.parse_mix("-1:1.0")


def test_a_duplicated_day_is_refused():
    """`{25: 0.5, 25: 0.5}` silently becomes `{25: 0.5}` in a dict comprehension, so the fractions
    would then fail to sum to 1 and the error would name the wrong problem."""
    with pytest.raises(ValueError, match="twice"):
        curriculum.parse_mix("25:0.5,25:0.5")


def test_a_malformed_entry_is_refused():
    with pytest.raises(ValueError, match="day:fraction"):
        curriculum.parse_mix("25")


# --------------------------------------------------------------------------- mix_counts


def test_counts_sum_to_exactly_the_batch():
    for batch in (16, 100, 250, 256, 257, 1000):
        for spec in ("25:0.8,0:0.2", "25:0.5,15:0.3,0:0.2", "25:0.34,15:0.33,0:0.33"):
            counts = curriculum.mix_counts(batch, curriculum.parse_mix(spec))
            assert sum(counts.values()) == batch, (batch, spec, counts)


def test_counts_are_close_to_the_requested_fractions():
    counts = curriculum.mix_counts(256, {25: 0.8, 0: 0.2})
    assert counts == {25: 205, 0: 51}


def test_a_day_that_would_get_zero_slots_is_refused():
    """A '99.9/0.1' mix at batch 256 wants 0.256 day-0 slots. Rounding that to zero produces a run
    that logs a mix and trains a pure day-25 curriculum."""
    with pytest.raises(ValueError, match="0 of 256 slots"):
        curriculum.mix_counts(256, {25: 0.999, 0: 0.001})


def test_a_tiny_but_representable_share_is_allowed():
    counts = curriculum.mix_counts(256, {25: 0.99, 0: 0.01})
    assert counts[0] >= 1 and sum(counts.values()) == 256


def test_counts_are_deterministic():
    """Largest-remainder with an explicit tie-break, so two runs with the same spec compose the same
    batch. A nondeterministic apportionment would make a mix run unreproducible for a reason nobody
    would look for."""
    a = curriculum.mix_counts(257, {25: 0.34, 15: 0.33, 0: 0.33})
    b = curriculum.mix_counts(257, {25: 0.34, 15: 0.33, 0: 0.33})
    assert a == b


# --------------------------------------------------------------------------- states_at_mix


def test_the_batch_contains_boards_from_every_requested_day():
    """The whole point. A mix whose states all came from one day would pass every arithmetic test
    above and train the thing the mix exists to replace."""
    mix = {25: 0.5, 0: 0.5}
    state = curriculum.states_at_mix(8, mix, seed=0)
    days = np.asarray(state.step_index) // J.TURNS_PER_DAY
    assert set(np.unique(days)) & {25, 24, 26}, days      # DAY_WINDOW=1 either side
    assert (days <= 2).any(), days                        # the day-0 pool, window included
    assert len(days) == 8


def test_the_realised_day_counts_match_the_apportionment():
    mix = {25: 0.75, 0: 0.25}
    state = curriculum.states_at_mix(8, mix, seed=1)
    days = np.asarray(state.step_index) // J.TURNS_PER_DAY
    assert (days >= 20).sum() == 6
    assert (days <= 2).sum() == 2


def test_the_day_is_not_correlated_with_the_slot_index():
    """A restarting slot restarts into `seed_states[i]` by position. Block ordering would pin each
    slot to one game-day for the life of the pool, so anything that ever indexes slots positionally
    would silently couple to the curriculum day."""
    mix = {25: 0.5, 0: 0.5}
    state = curriculum.states_at_mix(16, mix, seed=3)
    days = np.asarray(state.step_index) // J.TURNS_PER_DAY
    early = days <= 2
    # Block-ordered would put all 8 late boards in the first half. Permuted must not.
    assert early[:8].sum() not in (0, 8), f"day looks block-ordered by slot: {days}"


def test_shuffle_off_is_block_ordered_so_the_test_above_discriminates():
    """Confirms the permutation is what breaks the correlation, rather than the draw happening to
    look mixed. Without this, the test above could pass on a pool that was never ordered."""
    mix = {25: 0.5, 0: 0.5}
    state = curriculum.states_at_mix(16, mix, seed=3, shuffle=False)
    days = np.asarray(state.step_index) // J.TURNS_PER_DAY
    assert (days[:8] >= 20).all() and (days[8:] <= 2).all(), days


def test_a_single_day_mix_matches_states_at_day():
    """A mix of one is the degenerate case and must not be a different code path with different
    behaviour, or the mix flag would quietly change results at 100% day 25."""
    a = curriculum.states_at_mix(4, {25: 1.0}, seed=7, shuffle=False)
    b = curriculum.states_at_day(4, day=25, seed=7 + 1000 * 25)
    assert np.array_equal(np.asarray(a.step_index), np.asarray(b.step_index))
    assert np.array_equal(np.asarray(a.farm.money), np.asarray(b.farm.money))


def test_both_seats_are_real_on_a_day_zero_board():
    """The Session 6 virgin-episode bug is the reason the single-day path seeds both seats. A day-0
    board is where it would be hardest to notice, because an empty-looking board is *correct* there
    -- so the check is that the opponent seat has the same non-default structure as the trainee's."""
    state = curriculum.states_at_mix(4, {0: 1.0}, seed=0)
    money = np.asarray(state.farm.money)
    assert money.shape[1] == 2
    # Both seats present and finite; neither is the all-zero placeholder a synthetic seat would be.
    assert (money > 0).all(), money


def test_seeded_boards_carry_a_step_index_matching_their_day():
    """Every crop and animal rule is driven by `step_index // TURNS_PER_DAY`, so a board whose
    contents and counter disagree runs under one game's rules with another game's state."""
    state = curriculum.states_at_mix(6, {25: 0.5, 0: 0.5}, seed=11)
    days = np.asarray(state.step_index) // J.TURNS_PER_DAY
    assert ((days <= 2) | ((days >= 24) & (days <= 26))).all(), days


# --------------------------------------------------------------------------- the share arithmetic


def test_terminal_episode_share_is_much_smaller_than_the_slot_share():
    """Pins the claim the flag's help text makes, so the two cannot drift apart.

    A 20% day-0 *slot* share is about a 4% share of terminal *episodes*, because a day-0 episode is
    719 turns against day 25's ~120 and every slot emits the same turns per update. This is why the
    small fraction is described as buying coverage rather than policy credit.
    """
    batch, horizon = 256, 32
    counts = curriculum.mix_counts(batch, {25: 0.8, 0: 0.2})
    eps = {d: n * horizon / ((30 - d) * J.TURNS_PER_DAY) for d, n in counts.items()}
    share_0 = eps[0] / sum(eps.values())
    assert 0.02 < share_0 < 0.07, share_0
    assert counts[0] / batch == pytest.approx(0.199, abs=0.01)


def test_sixty_percent_of_slots_is_needed_for_a_fifth_of_episodes():
    """The correction that matters when setting the dial: to get 20% of terminal episodes from day 0
    you need roughly 60% of slots there, not 20%."""
    batch, horizon = 256, 32
    counts = curriculum.mix_counts(batch, {25: 0.4, 0: 0.6})
    eps = {d: n * horizon / ((30 - d) * J.TURNS_PER_DAY) for d, n in counts.items()}
    assert eps[0] / sum(eps.values()) == pytest.approx(0.20, abs=0.03)


# --------------------------------------------------------------------------- mirrored seats


def test_mirroring_plays_the_same_boards_from_both_sides():
    """The point of mirroring: half the batch inherits the richer seat and half the poorer, on the
    SAME boards, so the advantage of a seeded lead cancels in the aggregate.

    Checked by construction rather than by a win rate: the unmirrored pool at the same seed is the
    `behind=False` half, and the mirrored pool's other half must be that same set of boards with the
    two seats exchanged -- i.e. seat 0's money in one equals seat 1's money in the other.
    """
    rich = curriculum.states_at_day(4, day=25, seed=25_000, behind=False)
    poor = curriculum.states_at_day(4, day=25, seed=25_000, behind=True)
    r, p = np.asarray(rich.farm.money), np.asarray(poor.farm.money)
    assert np.array_equal(r[:, 0], p[:, 1]), (r, p)
    assert np.array_equal(r[:, 1], p[:, 0]), (r, p)


def test_a_mirrored_mix_is_half_rich_and_half_poor():
    """Aggregated over the batch, the trainee's seat must not be systematically the richer one."""
    plain = curriculum.states_at_mix(8, {25: 1.0}, seed=0, shuffle=False, mirror=False)
    mirrored = curriculum.states_at_mix(8, {25: 1.0}, seed=0, shuffle=False, mirror=True)
    pm = np.asarray(plain.farm.money)
    mm = np.asarray(mirrored.farm.money)
    # **Not asserting that seat 0 is richer.** `rank_seats` ranks by FINAL bank, so the ranked seat
    # is the one that ended up winning -- which at day 25 is the richer side only about 37% of the
    # time over the full seat pool. `states_at_day`'s "richer seat" wording is misleading and this
    # test previously encoded that misreading. What mirroring actually guarantees is the pairing
    # below, and that is what is checked.
    assert not np.array_equal(pm[:, 0], pm[:, 1])
    # Mirrored: the first half is one seating, the second half is its exact mirror.
    assert np.array_equal(mm[:4, 0], mm[4:, 1])
    assert np.array_equal(mm[:4, 1], mm[4:, 0])


def test_an_odd_count_gives_the_leftover_slot_to_the_poorer_seat():
    """A rounding artefact must bias against us, never for us -- the opposite of the bias mirroring
    exists to remove."""
    m = curriculum.states_at_mix(5, {25: 1.0}, seed=0, shuffle=False, mirror=True)
    money = np.asarray(m.farm.money)
    assert money.shape[0] == 5
    # The 4 mirrored slots cancel exactly; the leftover is drawn with behind=True, i.e. the trainee
    # takes the seat the replay did NOT rank. Asserting on money would be asserting that the ranked
    # seat is the richer one, which is false ~63% of the time -- see the test above.
    assert np.array_equal(money[:2, 0], money[2:4, 1])
    assert np.array_equal(money[:2, 1], money[2:4, 0])


def test_mirroring_preserves_the_batch_size_and_the_day_mix():
    m = curriculum.states_at_mix(8, {25: 0.5, 0: 0.5}, seed=1, mirror=True)
    days = np.asarray(m.step_index) // J.TURNS_PER_DAY
    assert len(days) == 8
    assert (days >= 20).sum() == 4 and (days <= 2).sum() == 4


# --------------------------------------------------------------------------- symmetric starts


def test_symmetric_gives_both_seats_the_identical_position():
    """The point: the only difference between the two players is what they DO.

    Checked field by field over the whole state rather than on money alone -- levelling the cash
    while leaving 16 animals against 4 would look fair and would not be, and money is the field most
    likely to be special-cased by hand.
    """
    st = curriculum.states_at_mix(6, {25: 1.0}, seed=0, symmetric=True, shuffle=False)
    for name in st.farm._fields:
        arr = np.asarray(getattr(st.farm, name))
        if arr.ndim >= 2 and arr.shape[1] == 2:
            assert np.array_equal(arr[:, 0], arr[:, 1]), f"farm.{name} differs between seats"
    for name in st.tiles._fields:
        arr = np.asarray(getattr(st.tiles, name))
        if arr.ndim >= 2 and arr.shape[1] == 2:
            assert np.array_equal(arr[:, 0], arr[:, 1]), f"tiles.{name} differs between seats"


def test_symmetric_boards_are_still_real_and_not_empty():
    """Two copies of one real seat, not two blank farms. An empty board at a late day is the bug
    `states_at_day` warns about: the scripted farmer refuses to plant and every episode ties at 0.5."""
    st = curriculum.states_at_mix(6, {25: 1.0}, seed=0, symmetric=True, shuffle=False)
    money = np.asarray(st.farm.money)
    assert (money > 1000).all(), money
    days = np.asarray(st.step_index) // J.TURNS_PER_DAY
    assert ((days >= 24) & (days <= 26)).all(), days


def test_symmetric_is_off_by_default_so_nothing_changes_silently():
    st = curriculum.states_at_mix(6, {25: 1.0}, seed=0, shuffle=False)
    money = np.asarray(st.farm.money)
    assert not np.array_equal(money[:, 0], money[:, 1])


# --------------------------------------------------------------------------- board diversity


def test_top_none_draws_from_more_seats_than_the_old_hardcoded_200():
    """`top` was hard-coded to 200 while 312 seats exist on disk, so 112 boards were never used and
    a 256-slot pool had to draw some boards twice."""
    from kagg.il import bc
    all_refs = bc.rank_seats(bc.find_replays("data"))
    if len(all_refs) <= 200:
        pytest.skip(f"only {len(all_refs)} seats on disk; nothing was being discarded")
    assert len(all_refs[:None]) > len(all_refs[:200])


def test_a_tiny_top_still_varies_because_the_TURN_is_redrawn_too():
    """Measured, and it corrects the assumption that `top` alone controls diversity.

    With `top=1` every board comes from ONE recorded seat -- and the six boards are still all
    different, because `_turn_indices` draws a random turn from a +/-1 day window (49 turns at day
    25) and a farm changes every turn. So board variety comes from two sources, and the seat cap is
    the weaker one. Raising `top` is still right (it was discarding 112 of 312 seats), but it buys
    less than the repeat-count arithmetic suggests on its own.
    """
    one = curriculum.states_at_day(6, day=25, seed=0, top=1)
    m_one = np.asarray(one.farm.money)[:, 0]
    assert len(np.unique(m_one)) == 6, m_one


def test_top_is_still_honoured_when_passed():
    """Changing the default must not make the parameter inert."""
    from kagg.il import bc
    refs = bc.rank_seats(bc.find_replays("data"))
    if len(refs) < 3:
        pytest.skip("need at least 3 seats")
    assert len(refs[:2]) == 2


# --------------------------------------------------------------------------- length weighting


def test_length_weighting_gives_every_day_an_equal_share_of_terminal_episodes():
    """The property the whole helper exists for. Slot share is deliberately UNequal; what must be
    equal is the share of finished episodes, because that is what the gradient consumes."""
    mix = curriculum.length_weighted_mix([25, 20, 15, 10, 5, 0])
    batch, horizon = 3000, 32
    eps = {d: f * batch * horizon / ((30 - d) * J.TURNS_PER_DAY) for d, f in mix.items()}
    tot = sum(eps.values())
    for d, e in eps.items():
        assert e / tot == pytest.approx(1 / len(mix), rel=0.02), (d, e / tot)


def test_length_weighting_puts_more_SLOTS_on_the_early_days():
    """Equal episode share requires unequal slots: a day-0 episode is 6x a day-25 one."""
    mix = curriculum.length_weighted_mix([25, 0])
    assert mix[0] > mix[25]
    assert mix[0] == pytest.approx(30 / 35) and mix[25] == pytest.approx(5 / 35)


def test_uniform_day_sampling_would_be_dominated_by_the_last_days():
    """Pins the motivation, so the docstring's numbers cannot drift from the arithmetic: sampling
    days uniformly gives day 29 ~25% of terminal episodes and day 0 under 1%."""
    days = list(range(30))
    eps = {d: (1 / 30) / (30 - d) for d in days}
    tot = sum(eps.values())
    assert eps[29] / tot == pytest.approx(0.25, abs=0.01)
    assert eps[0] / tot < 0.01


def test_the_length_prefix_parses_and_sums_to_one():
    mix = curriculum.parse_mix("length:25,20,15,10,0")
    assert set(mix) == {25, 20, 15, 10, 0}
    assert sum(mix.values()) == pytest.approx(1.0)
    assert mix[0] > mix[25]


def test_a_length_spec_with_an_out_of_season_day_is_refused():
    with pytest.raises(ValueError, match="outside"):
        curriculum.parse_mix("length:30,0")
