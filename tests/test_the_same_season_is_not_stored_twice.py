"""A teacher-driven season is deterministic, so re-rolling it must not grow the training pool.

**The measurement that forced this.** `data/dagger_tape/d4fix2-.../aggregate.pkl` at round 24 held
**477 unique rows in a pool of 12,000 -- each distinct row stored 25.2 times.** d0-d4 is 4 tapes x
120 turns = 480 turns, so the entire dataset was 477 rows and the run had appended 25 copies of it.

It has to be that way at beta=1: fixed start state, `weedSpawnChance = 0.0`, a deterministic teacher
(`TAPE[key][step]`), and an opponent that is a fixed recording. Nothing in the rollout can differ
between rounds.

**What it cost.** Not the rollout -- that was measured at 41.1 s for a 719-turn episode, ~205 s of
an 868 s box round. The other ~660 s was the fit, doing roughly 20x the gradient steps an epoch
needs because 20 copies of every row were in it.

**What is NOT deduplicated, and why.** Student rows. Once beta anneals they come from a moving
policy, so two visits to the same turn are genuinely different states and the reservoir below is
what keeps the sample unbiased. Only `by_teacher` rows are filtered.

**And rows from an aggregate written before episode identity existed.** They carry no `ep` key, so
`(None, turn)` would make one tape's turn 300 shadow another's. `_expert_marks` skips them: a
resumed run keeps whatever duplicates it already had and only filters fresh rows.
"""

import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

DT = pytest.importorskip("dagger_tape")

EP_A = ("92498144.json", 0, 1240813987, "recorded")
EP_B = ("91907974.json", 0, 244615642, "recorded")


def teacher_row(ep, turn):
    return {"ep": ep, "turn": turn, "by_teacher": True}


def student_row(ep, turn):
    return {"ep": ep, "turn": turn, "by_teacher": False}


def aggregate(rows, expert, student, expert_seen):
    """The pool-filling loop from `dagger_tape`, with the caps out of the way.

    Kept deliberately small: this pins the DEDUP rule, not the reservoir. `test_dagger_tape.py`
    covers capping.
    """
    for row in rows:
        row = dict(row)
        by_teacher = row.pop("by_teacher")
        if by_teacher:
            mark = (row.get("ep"), row.get("turn"))
            if mark in expert_seen:
                continue
            expert_seen.add(mark)
        (expert if by_teacher else student).append(row)
    return expert, student


def test_re_rolling_the_same_season_adds_nothing():
    """The defect, at its own scale: two identical rounds must leave one round's worth of rows."""
    season = [teacher_row(EP_A, t) for t in range(120)]
    expert, student, seen = [], [], set()
    aggregate(season, expert, student, seen)
    after_one = len(expert)
    aggregate(season, expert, student, seen)
    assert after_one == 120
    assert len(expert) == 120, (
        "re-rolling an identical teacher season grew the pool from %d to %d. At beta=1 the rollout "
        "is deterministic, so those rows are byte-identical copies and every one of them multiplies "
        "the gradient steps an epoch costs." % (after_one, len(expert)))


def test_twenty_five_rounds_still_hold_one_copy():
    """The measured case: 25 rounds produced 25.2 copies of each row."""
    season = [teacher_row(EP_A, t) for t in range(120)]
    expert, student, seen = [], [], set()
    for _ in range(25):
        aggregate(season, expert, student, seen)
    assert len(expert) == 120, "expected 120 rows after 25 identical rounds, got %d" % len(expert)


def test_the_same_turn_of_a_different_season_is_kept():
    """Dedup is keyed on `(episode, turn)`, never on the turn alone.

    Four tapes all have a turn 300 and they are different states. Keying on `turn` would throw away
    three quarters of the dataset -- a far worse bug than the one being fixed.
    """
    expert, student, seen = [], [], set()
    aggregate([teacher_row(EP_A, 300), teacher_row(EP_B, 300)], expert, student, seen)
    assert len(expert) == 2, (
        "turn 300 of two different tapes collapsed to one row; dedup must key on the episode too")


def test_a_different_seed_is_a_different_episode():
    """`episode_specs` varies the town seed, which changes the shop draw and the q4 latch."""
    other_seed = (EP_A[0], EP_A[1], 999, EP_A[3])
    expert, student, seen = [], [], set()
    aggregate([teacher_row(EP_A, 50), teacher_row(other_seed, 50)], expert, student, seen)
    assert len(expert) == 2


def test_a_different_opponent_is_a_different_episode():
    other_opp = (EP_A[0], EP_A[1], EP_A[2], "tetsuya")
    expert, student, seen = [], [], set()
    aggregate([teacher_row(EP_A, 50), teacher_row(other_opp, 50)], expert, student, seen)
    assert len(expert) == 2


def test_student_rows_are_never_deduplicated():
    """Once beta anneals, two visits to the same turn are different states. Keep both."""
    expert, student, seen = [], [], set()
    aggregate([student_row(EP_A, 7), student_row(EP_A, 7)], expert, student, seen)
    assert len(student) == 2, (
        "a student row was discarded as a duplicate. Student states come from a moving policy and "
        "the reservoir needs every one of them to stay unbiased.")
    assert expert == []


def test_a_legacy_pool_without_episode_tags_is_left_alone():
    """`_expert_marks` must not turn untagged rows into `(None, turn)` and collapse the tapes."""
    legacy = [{"turn": t} for t in range(5)] + [{"turn": t} for t in range(5)]
    marks = DT._expert_marks(legacy)
    assert marks == set(), (
        "rows predating the `ep` tag were given dedup marks; on resume that would make one tape's "
        "turn shadow another's. Got %r" % (marks,))


def test_marks_are_rebuilt_from_a_tagged_pool_on_resume():
    """A resumed run must not re-append rows the pool already holds."""
    pool = [{"ep": EP_A, "turn": t} for t in range(10)]
    marks = DT._expert_marks(pool)
    assert marks == {(EP_A, t) for t in range(10)}

    expert, student = list(pool), []
    aggregate([teacher_row(EP_A, t) for t in range(10)], expert, student, marks)
    assert len(expert) == 10, "resume re-appended rows already in the pool"
