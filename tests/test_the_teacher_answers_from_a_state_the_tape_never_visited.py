"""The DAgger property: the teacher must answer at states the tape never reached.

A teacher that only answers on its own trajectory is a dataset, and training on it is behaviour
cloning -- which is the thing already tried and found wanting. The whole reason to keep the shipped
agent in the loop is that it can be *asked* from a board the student damaged.

So this file drives the board somewhere the tape never goes -- the agent passes for a stretch, so
nothing gets planted, watered or sold on those turns -- and then asks the teacher what to do.

It also pins the two traps that have already cost time here:
  * seat 1 gets no `step` from kaggle-environments, so a teacher seated second replays turn 0
  * `configuration.seed` is None; the real seed is `info.seed`

Related: docs/dagger_tape_teacher_2026-08-22.md
"""
import json
import pathlib

import pytest

from kagg.il.tape_teacher import TapeTeacher
from kagg.search import schedule_agent as SA

REPO = pathlib.Path(__file__).resolve().parents[1]
TPD = 24


def _tape(key):
    tape_path, team = SA.REPLAY_OPENING_TAPE[key]
    doc = json.loads((REPO / tape_path).read_text())
    return doc, doc["info"]["TeamNames"].index(team)


def _env(key, steps=None):
    """The env the tape was actually played on: its own economy, its own seed, no weeds."""
    from kaggle_environments import make

    import sys

    sys.path.insert(0, str(REPO / "scripts"))
    import breakdown as B

    tape_path, _ = SA.REPLAY_OPENING_TAPE[key]
    doc, seat = _tape(key)
    cfg = B.env_config(REPO / tape_path)
    cfg.pop("steps", None)
    # **`info.seed`, not `configuration.seed`.** The latter is None on every recording, which leaves
    # env.reset() drawing a fresh town -- two runs of the verifier disagreed by 499 turns on it.
    cfg["seed"] = int(doc["info"]["seed"])
    cfg["weedSpawnChance"] = 0.0
    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    return env, doc, seat


def _pass_action():
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _opponent(doc, seat, t, n_hands):
    act = ((doc["steps"][1 + t][1 - seat] or {}).get("action") or {})
    return {"farmer": act.get("farmer") or ["PASS"],
            "hands": list(act.get("hands") or [])[:n_hands],
            "market": act.get("market") or []}


@pytest.mark.slow
def test_the_teacher_still_answers_after_the_board_has_been_damaged():
    """Pass for a whole day, so no crop is planted or watered, then ask the teacher."""
    key = (True, False)
    env, doc, seat = _env(key)
    teacher = TapeTeacher(seat)

    # Drive 48 turns. For the first 24 the teacher's own action is thrown away and PASS is sent --
    # the board is now one the tape never produced. The teacher is still QUERIED every turn, because
    # its latches and purchase counters are stateful and must track the game it is teaching.
    answers = []
    for t in range(48):
        assert not env.done, "env finished early at turn %d" % t
        obs = env.state[seat].observation
        act = teacher.act(obs)
        answers.append(act)
        hands = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        sent = _pass_action() if t < TPD else {
            "farmer": list(act["farmer"]),
            "hands": [list(h) for h in list(act["hands"])[:hands[seat]]],
            "market": [list(o) for o in (act.get("market") or [])],
        }
        pair = [None, None]
        pair[seat] = sent
        pair[1 - seat] = _opponent(doc, seat, t, hands[1 - seat])
        env.step(pair)

    # The teacher answered every turn, including the 24 where the board was off-trajectory.
    assert len(answers) == 48
    for t, a in enumerate(answers):
        assert isinstance(a, dict) and a.get("farmer"), "turn %d produced no farmer op" % t
        assert isinstance(a.get("hands"), list)
        assert isinstance(a.get("market"), list)

    # And it is not answering PASS-forever after the damage: day 1 still contains real work.
    day_one = answers[TPD:]
    ops = {a["farmer"][0] for a in day_one} | {h[0] for a in day_one for h in a["hands"]}
    assert ops - {"PASS"}, "the teacher had nothing to say for a whole day after the damage"


@pytest.mark.slow
def test_the_teacher_injects_step_when_the_harness_omits_it():
    """Seat 1 gets no `step`. Without injection the teacher replays turn 0 all season."""
    key = (True, False)
    env, doc, seat = _env(key)
    teacher = TapeTeacher(seat)

    obs = dict(env.state[seat].observation)
    obs.pop("step", None)
    obs["day"], obs["hour"] = 2, 7
    assert teacher.step_of(obs) == 2 * TPD + 7


def test_every_tape_key_is_reachable():
    """All four `(melon_armed, q4_armed)` keys must name a distinct recording.

    Three of the four were unreachable by construction once before, because nothing wrote the latch
    keys -- every turn resolved to `(False, False)` and the melon tape played on all four arms.
    """
    keys = set(SA.REPLAY_OPENING_TAPE)
    assert keys == {(False, False), (False, True), (True, False), (True, True)}
    paths = [p for p, _ in SA.REPLAY_OPENING_TAPE.values()]
    assert len(set(paths)) == 4, "two latch keys point at the same recording: %s" % (paths,)
