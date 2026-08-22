"""When both latches fire we must not silently discard the yarn-store one.

`REPLAY_OPENING_TAPE` is keyed on `(melon_armed, q4_armed)` and there are four keys over three
recordings, so one key has to share. It was `(True, True)`, pointed at the q3 strawberry tape --
the same file as `(True, False)` -- which throws the q4 trigger away.

**The reasoning for that was sound and then expired.** The comment on the entry said, correctly:

    It does not matter, because over `REPLAY_OPENING_DAYS` -- d4 to d11 -- the q3 strawberry tape
    and all three of the good q4 strawberry tapes are INDISTINGUISHABLE ... They part company at
    d12, which is PAST the handover.

`REPLAY_OPENING_DAYS` became `tuple(range(30))` on 2026-08-21. The tapes part company at d12 and we
now replay eighteen days beyond it, so the premise is gone. This is the
"a decision to skip a fix can expire when the problem changes" lesson in `CLAUDE.md`, and the entry
was never revisited.

Measured 2026-08-22 on the fourteen `(town, opponent)` pairs that arm `(True, True)`, same town,
same opponent, same seed, only the tape moved:

    control  wins  0/14        retaped wins 13/14
    town 0, Ryo Hasegawa        99,309 / 122,771   ->  129,383 / 119,298
    town 1, MIRROR              60,560 /  61,147   ->   86,999 /  60,120
    town 1, peikopon            61,982 /  68,926   ->   86,819 /  67,040

Roughly +$20k a game, and every game flips from a loss to a win.

**Settled 2026-08-22.** The paragraph that used to sit here said the melon q4 tape sows melon on
squares a strawberry arm wants, named `93459936`, `92508348` and `91906088` as unregistered
candidates that "may be better still", and pinned only that `(True, True)` must not be the q3
strawberry tape. The shootout ran two of the three, 6,048 seasons -- 48 stratified towns x 9 ladder
opponents x 3 seeds x 6 arms. Restricted to the 420 seasons each arm actually changed:

    arm                     n diff  arm win%  incumbent win%   swing  mean delta $
    91906088                   420     90.0%           62.1%   +27.9          -822
    93459936                   420     73.8%           62.1%   +11.7        -1,653
    92488785                   420     64.8%           62.1%    +2.6        -3,564
    92466371  (q3 straw)       420      6.0%           62.1%   -56.2       -21,835

`(True, True)` is `91906088` as of 2026-08-22. It banks LESS and wins MORE; win rate is the
selection criterion on an Elo ladder. The q3 strawberry tape at 6.0% is the same defect this file
was written for, now measured on 420 seasons rather than 14 configurations.

Full write-up: `docs/tape_shootout_2026-08-22.md`.
"""

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent as SA                                  # noqa: E402

MELON_Q3 = "92498144"
STRAW_Q3 = "92466371"
Q4 = "91907974"


def stem(key):
    return pathlib.Path(SA.REPLAY_OPENING_TAPE[key][0]).stem


def quadrants(key):
    """How many quadrants the recording behind `key` ends the season owning.

    Read off the tape rather than inferred from its filename. `unlocked_quadrants` is on the farm
    in every observation, so the last step gives the season's final holding:

        91906088  4  ['NW','NE','SW','SE']  bank 128,408
        91907974  4  ['NW','NE','SW','SE']  bank  88,763
        92466371  3  ['NW','NE','SW']       bank 147,059
        92498144  3  ['NW','NE','SW']       bank 149,998

    Note the banks: the two three-quadrant seasons are the RICHEST. "Four quadrants" is a statement
    about the shape of the plan we are replaying, not about how much it made, and the shootout
    below found the same thing -- 128k beats 136k beats 81k as a tape to replay.
    """
    path, team = SA.REPLAY_OPENING_TAPE[key]
    d = json.loads((REPO / path).read_text())
    seat = d["info"]["TeamNames"].index(team)
    return len(d["steps"][-1][0]["observation"]["farms"][seat]["unlocked_quadrants"])


def test_both_latches_do_not_replay_the_q3_strawberry_tape():
    """The defect itself: `(True, True)` sharing a file with `(True, False)` discards the q4 read."""
    assert stem((True, True)) != STRAW_Q3, (
        "(True, True) is on the q3 strawberry tape, so a yarn store unlocked by d5 is ignored "
        "whenever the opponent also shows 9 melon. Measured 0/14 wins against 13/14 on the q4 tape."
    )


def test_both_latches_replay_a_four_quadrant_tape():
    """It must be a q4 recording -- the whole content of the second latch.

    **Asserts the PROPERTY, not a filename.** This read `stem((True, True)) == "91907974"` until
    2026-08-22, which pinned the incumbent rather than the requirement, and went red the moment the
    shootout replaced it with a recording that is equally four-quadrant and wins 27.9 points more.
    The docstring said "a q4 recording" the whole time; the assertion said "this file".

    A filename pin also cannot tell a q4 tape from a q3 one -- it only knows the name it was
    written with. Reading `unlocked_quadrants` off the tape does, and it keeps working through any
    future re-tape that satisfies the actual requirement.
    """
    n = quadrants((True, True))
    assert n == 4, (
        f"(True, True) replays {stem((True, True))}, which ends the season owning {n} quadrants. "
        f"The key means 'opponent shows 9+ melon AND a yarn store by d5' -- the whole content of "
        f"the second latch is that we go to four quadrants. A q3 recording throws it away.")


def test_the_other_three_keys_are_untouched():
    """A one-key fix must stay a one-key fix; the other three are measured and exact.

    These stay pinned by name deliberately. Unlike `(True, True)`, each is the exact recording its
    own measurement was taken on, so "some other file with the same shape" is not good enough.
    """
    assert stem((False, False)) == MELON_Q3
    assert stem((True, False)) == STRAW_Q3
    assert stem((False, True)) == Q4


def test_every_key_points_at_a_file_that_exists():
    """`_replay_opening` degrades to `{}` on a missing path, which is a silent non-replay."""
    for key, (path, _team) in SA.REPLAY_OPENING_TAPE.items():
        assert (REPO / path).exists(), "%s -> %s is not on disk" % (key, path)
