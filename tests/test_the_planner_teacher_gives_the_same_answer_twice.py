"""One theory, one test: are the planner teacher's DAgger labels consistent on a fixed seed?

    python -u -m pytest tests/test_the_planner_teacher_gives_the_same_answer_twice.py -q

THE THEORY
----------
`scripts/dagger_tape.py --planner-teacher` empties `REPLAY_OPENING_DAYS`, so the teacher reads the
live board every turn instead of replaying カワシギ's recorded ops off the clock. At round 1 it
scores `greedy op 0.4472` with **0.000 on all four movement directions over ~45,000 samples**, and
the student's playout banks $0 (`/home/alex/kaggriculture/data/logs/dagger_planner.log`, box time
09:56, 2026-08-28).

Alex's question is the right one: the tape clone reproduced its four teachers exactly, so why not
this one? Two explanations, opposite fixes:

  A. **The target is harder.** The tape teacher's action is a function of the CLOCK -- turn index
     alone -- so the student only had to learn a 719-row lookup it could read off `(day, hour)`.
     The planner's action is a function of the BOARD, and the moment the student drives, the board
     is its own. Nothing is wrong; DAgger is doing the job it exists for and needs its rounds.

  B. **The labels contradict each other.** If anything in the episode is re-drawn per run -- the
     shop unlock schedule, weeds -- then the same seed yields a different trajectory, the teacher
     answers a different board, and the student is shown two answers for one state. No capacity or
     round count fixes that, and it would be invisible in the loss.

This test separates them. It replays one seed twice through the same teacher and demands the action
streams be identical. Green means B is ruled out and the round-1 numbers are explanation A. Red
means the DAgger run is training on contradictory labels and should be stopped.

Per-batch shop-unlock randomisation has already invalidated a set of results in this project once,
so this is not a hypothetical.
"""
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

SEED = 91234
TURNS = 240          # ten days: long enough for shops to unlock and for weeds to appear


def _stream(seed, turns):
    """The teacher's action for every turn of one season, as comparable tuples."""
    from kagg.il.tape_teacher import TapeTeacher
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = TapeTeacher(0)
    out = []
    for _t in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        n_units = 1 + len(obs["farms"][0].get("hands") or [])
        act = me.sendable(me.act(obs), n_units)
        out.append((
            tuple(act.get("farmer") or ()),
            tuple(tuple(h) for h in (act.get("hands") or ())),
            tuple(tuple(o) for o in (act.get("market") or ())),
        ))
        env.step([act, {"farmer": ["PASS"], "hands": [], "market": []}])
    return out


@pytest.fixture(autouse=True)
def planner_teacher():
    """Empty `REPLAY_OPENING_DAYS` for this process only -- the arm the box run trains against."""
    from kagg.search import schedule_agent as SA
    shipped = SA.REPLAY_OPENING_DAYS
    SA.REPLAY_OPENING_DAYS = ()
    yield
    SA.REPLAY_OPENING_DAYS = shipped


def test_the_same_seed_produces_the_same_teacher_actions():
    a = _stream(SEED, TURNS)
    b = _stream(SEED, TURNS)
    assert len(a) == len(b), f"seed {SEED} ran {len(a)} turns then {len(b)}"
    first = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
    assert first is None, (
        f"seed {SEED} diverges at turn {first} (day {first // 24} hour {first % 24}):\n"
        f"  run 1  {a[first]}\n  run 2  {b[first]}\n"
        "The teacher answers a different board on the second run, so the DAgger aggregate holds "
        "two labels for one state. Stop the box run before adding rounds to it.")
