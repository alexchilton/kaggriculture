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

**What this test does NOT establish.** The comment also warns that the melon q4 tape sows melon on
squares a strawberry arm wants, and names three q4 STRAWBERRY tapes (`93459936`, `92508348`,
`91906088`) that are not in the registry. Those may be better still. This pins only that
`(True, True)` must not be the q3 strawberry tape, which is measured.
"""

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


def test_both_latches_do_not_replay_the_q3_strawberry_tape():
    """The defect itself: `(True, True)` sharing a file with `(True, False)` discards the q4 read."""
    assert stem((True, True)) != STRAW_Q3, (
        "(True, True) is on the q3 strawberry tape, so a yarn store unlocked by d5 is ignored "
        "whenever the opponent also shows 9 melon. Measured 0/14 wins against 13/14 on the q4 tape."
    )


def test_both_latches_replay_a_four_quadrant_tape():
    """It must be a q4 recording -- the whole content of the second latch."""
    assert stem((True, True)) == Q4


def test_the_other_three_keys_are_untouched():
    """A one-key fix must stay a one-key fix; the other three are measured and exact."""
    assert stem((False, False)) == MELON_Q3
    assert stem((True, False)) == STRAW_Q3
    assert stem((False, True)) == Q4


def test_every_key_points_at_a_file_that_exists():
    """`_replay_opening` degrades to `{}` on a missing path, which is a silent non-replay."""
    for key, (path, _team) in SA.REPLAY_OPENING_TAPE.items():
        assert (REPO / path).exists(), "%s -> %s is not on disk" % (key, path)
