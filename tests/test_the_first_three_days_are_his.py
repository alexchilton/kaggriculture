"""d0, d1 and d2 come from the tape, because all four tapes agree there.

Measured 2026-08-24 against the shipped build: our first action of the season differs from his.
At d0 h0 he does `BUILD_PASTURE` and we `PASS`; a hand sits on `PASS` for most of the opening; and
every turn of d0-d3 differs. The boards happen to converge by d4 and drift apart again at d5.

The reason is that `REPLAY_OPENING_DAYS` started at **d4**, so d0-d3 was played by our own planner
and was never a clone at all.

**Why d0-d2 and not d0-d3.** The tape is selected by `(melon_armed, q4_armed)`, and those latches
decide at `melon_branch.DECIDE_BY_DAY = 3` and `q4_branch.DECIDE_BY_DAY = 6`. Replaying a day
before its latch has decided replays whichever tape the unset key points at. Hashing the four
tapes day by day:

    d0  1 distinct   all four tapes identical
    d1  1 distinct   all four tapes identical
    d2  1 distinct   all four tapes identical
    d3  2 distinct   splits on the melon latch -- which only decides ON d3
    d4  3 distinct

So d0-d2 carry no branch and can be replayed with no latch to read. d3 cannot, and stays ours.

That distinction is not cosmetic: replaying d0-d11 blind measured **mean -$96,897 over 14 games**,
better in only 2, with eight seasons collapsing by $100k-$200k -- the signature of replaying the
wrong arm's opening for three days.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent as SA                                # noqa: E402


def test_the_first_three_days_are_replayed():
    assert 0 in SA.REPLAY_OPENING_DAYS, "d0 is ours, so our first action is not his"
    assert 1 in SA.REPLAY_OPENING_DAYS
    assert 2 in SA.REPLAY_OPENING_DAYS


def test_day_three_is_not_replayed():
    """The melon latch decides ON d3, so d3 has no stable tape to replay."""
    assert 3 not in SA.REPLAY_OPENING_DAYS, (
        "d3 splits on a latch that has not decided yet -- replaying it picks an arm at random")


def test_the_four_tapes_agree_on_every_replayed_day_before_the_latch():
    """The guard that makes this safe. If a future tape edit breaks it, this fails loudly."""
    import hashlib
    import json
    for day in (0, 1, 2):
        sigs = set()
        for tape in SA.REPLAY_OPENING_TAPE.values():
            op = SA._replay_opening((day,), *tape)
            sigs.add(hashlib.sha1(
                json.dumps(op, sort_keys=True, default=str).encode()).hexdigest())
        assert len(sigs) == 1, f"d{day} differs between tapes; it cannot be replayed latch-free"
