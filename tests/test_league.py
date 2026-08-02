"""The opponent pool's eviction, which killed a 250-update run and would have corrupted the
curriculum silently if it had not.

`pool.pop(len(pool) // 2)` evicted from the params list and left `pool_wr` and `pool_games` a member
longer. Two failures came out of one line:

- **Loud:** `np.random.choice` got `len(pool)` options and `len(pool_wr)` probabilities and raised
  `ValueError: a and p must have same size` on the next update. The run had done 250 updates.
- **Silent, and worse:** every subsequent `pool_wr[opp_idx]` named a different checkpoint than the
  one that had just played, so the priority EMA -- the entire reason for sampling by difficulty
  rather than round-robin -- was attributed to the wrong member with nothing in the log to show it.

These tests are on `kagg.rl.league`, which the training script now uses, rather than on a
reimplementation of it. A test that re-derives the logic it is checking agrees with whatever
misreading produced the bug -- this project lost the no-op HARVEST loop that way.
"""

import numpy as np

from kagg.rl.league import POOL_UNPLAYED_BONUS, Pool


def test_eviction_keeps_the_weights_and_the_members_the_same_length():
    """The crash. Sampling needs one probability per member and not one per member ever added."""
    pool = Pool(max_size=5)
    for i in range(12):
        pool.add(f"ckpt{i}")
        assert len(pool.weights()) == len(pool), (
            f"after {i + 1} adds: {len(pool.weights())} weights for {len(pool)} members")
        pool.select(seed=0, update=i)          # would raise ValueError on a mismatch


def test_eviction_keeps_each_win_rate_attached_to_its_own_checkpoint():
    """The silent half. A surviving member must keep *its* record, not a neighbour's."""
    pool = Pool(max_size=4)
    for i in range(4):
        pool.add(f"ckpt{i}")
    for i, m in enumerate(pool.members):
        m.wr, m.games = 0.1 * (i + 1), i + 1

    before = {m.params: (round(m.wr, 6), m.games) for m in pool.members}
    pool.add("ckpt4")                          # forces one eviction

    for m in pool.members:
        if m.params in before:
            assert (round(m.wr, 6), m.games) == before[m.params], (
                f"{m.params} inherited another member's record")


def test_eviction_keeps_the_anchor_and_the_frontier():
    """Documented intent: the first entry cannot drift, the last is the frontier."""
    pool = Pool(max_size=3)
    for i in range(9):
        pool.add(f"ckpt{i}")
    names = [m.params for m in pool.members]
    assert names[0] == "ckpt0", f"lost the anchor: {names}"
    assert names[-1] == "ckpt8", f"lost the frontier: {names}"


def test_an_unplayed_member_is_favoured_until_it_has_played():
    pool = Pool(max_size=5)
    pool.add("played")
    pool.add("unplayed")
    pool.record(0, opp_wr=0.5, n_done=10)

    w = pool.weights()
    assert w[1] - w[0] == POOL_UNPLAYED_BONUS
    assert pool.members[0].games == 10 and pool.members[1].games == 0


def test_a_checkpoint_that_beats_us_is_sampled_more():
    """`wr` is the *opponent's* rate, so higher means harder, and harder must mean more often."""
    pool = Pool(max_size=5)
    pool.add("weak")
    pool.add("strong")
    pool.record(0, opp_wr=0.1, n_done=50)
    pool.record(1, opp_wr=0.9, n_done=50)

    w = pool.weights()
    assert w[1] > w[0]

    picks = [pool.select(seed=0, update=u) for u in range(400)]
    assert np.mean(picks) > 0.5, "the harder checkpoint is not being played more often"


def test_a_zero_sample_update_does_not_move_the_ema():
    """Terminal rows are ~0.14% of rows, so an update can resolve no games against the opponent.
    Folding that in would drag every member toward 0.5 and flatten the curriculum."""
    pool = Pool(max_size=5)
    pool.add("ckpt")
    pool.record(0, opp_wr=0.9, n_done=20)
    after = pool.members[0].wr

    pool.record(0, opp_wr=0.0, n_done=0)
    assert pool.members[0].wr == after
    assert pool.members[0].games == 20


def test_selection_is_reproducible_for_a_given_update():
    """A resumed run at the same update must draw the same opponent, or a resume changes the
    curriculum silently."""
    pool = Pool(max_size=5)
    for i in range(4):
        pool.add(f"ckpt{i}")
    assert [pool.select(7, u) for u in range(20)] == [pool.select(7, u) for u in range(20)]


def test_a_pool_member_holds_the_seat_for_a_whole_episode():
    """One frozen checkpoint must play a game from start to finish, not 32 turns of it.

    **The bug this pins.** `opp_idx = pool.select(seed, it)` was drawn once per *update*, inside the
    update loop, while an episode is 719 turns and a `--horizon 32` update advances 32 of them. So
    seat 1 was played by ~23 different frozen checkpoints over a single game, swapping every 32
    turns. Sticky *roles* were added so a game keeps its opponent TYPE for the season; the member
    identity was left redrawn, so the fix was half applied.

    The consequence is not a subtle bias. An opponent stitched from 23 checkpoints has no coherent
    plan -- it restarts its strategy 23 times a season -- and plays far worse than any single member
    of the pool. Measured: `wr_pool` read 0.990 while an honest head-to-head between two of those
    same checkpoints on a fair board was nowhere near that, and every member's recorded win rate sat
    at 0.01-0.15 because none of them had ever played a whole game. `pool.record` then attributed
    the result to whichever member happened to hold the seat on the final update.

    `CLAUDE.md` already names this exact failure for the per-opponent win rate -- "the opponent was
    re-drawn every update while a game spans ~22.5 of them" -- so this is the same bug found twice
    in two places, fixed once.
    """
    from kagg.rl import league

    pool = Pool(max_size=8)
    for i in range(6):
        pool.add({"w": i})

    horizon, episode_turns = 32, 719
    hold = league.hold_updates(horizon, episode_turns)
    span = -(-episode_turns // horizon)          # updates one game spans, rounded up

    assert hold >= span, "a member must hold the seat for at least one whole episode"

    worst = 0
    for start in range(0, 300):
        seen = {pool.select(0, u, hold=hold) for u in range(start, start + span)}
        worst = max(worst, len(seen))
    assert worst <= 2, (
        f"a game spanning {span} updates saw up to {worst} distinct opponents; at most 2 is "
        f"possible once a member holds the seat for {hold} updates, and 2 only when the game "
        f"straddles a boundary")

    # The contrast, so the test states what was wrong rather than only what is right.
    unheld = max(len({pool.select(0, u, hold=1) for u in range(s, s + span)}) for s in range(50))
    assert unheld > 2, "with hold=1 a single game faces many opponents -- that was the bug"


def test_holding_the_seat_does_not_freeze_the_choice_forever():
    """Members must still rotate across games, or the pool collapses to one opponent."""
    from kagg.rl import league

    pool = Pool(max_size=8)
    for i in range(6):
        pool.add({"w": i})
    hold = league.hold_updates(32, 719)

    seen = {pool.select(0, u, hold=hold) for u in range(0, hold * 40)}
    assert len(seen) > 1, "the seat must rotate between members across successive episodes"
