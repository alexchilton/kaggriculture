"""The agent's own carrot gate must agree with the deficit reading, on the real boards.

`tests/test_the_book_is_cornered_only_when_it_is_deep.py` tests `corner_the_book.plan` directly.
This tests the WIRING: that `schedule_agent._carrot_pays`, the function the arm actually calls,
now reaches the same verdicts. A decision function nothing calls is a decision function that has
never run, and this repo has shipped that shape before.

The discriminating case is 98495047: `CARROT_OPP_MAX = 7` stood us down there because the opponent
held 10 carrot tiles, and we lost by $29,384 to someone who cleared 76 units at $498.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent as SA                               # noqa: E402

TPD = 24
US = "alex chilton"

GAMES = [
    ("98495047", True),    # drain 11, opponent on 10 carrot tiles -- the game the old gate lost
    ("98460892", True),    # drain 6
    ("98494953", False),   # drain 2
    ("98499540", False),   # drain 2
    ("98501831", False),   # drain 2
    ("98428765", False),   # drain 3
]


def _obs(episode, day=25):
    hits = list((REPO / "data/seed_scripts").rglob(f"{episode}.json"))
    if not hits:
        pytest.skip(f"{episode}.json not downloaded")
    rec = json.loads(hits[0].read_text())
    names = rec["info"]["TeamNames"]
    if US not in names:
        pytest.skip(f"{episode} is not one of ours")
    seat = names.index(US)
    return rec["steps"][day * TPD][seat]["observation"], seat


@pytest.mark.parametrize("episode,should_fire", GAMES)
def test_the_wired_gate_matches_the_deficit_reading(episode, should_fire):
    obs, seat = _obs(episode)
    assert SA._carrot_pays(obs, seat) is should_fire, (
        f"{episode}: the arm's own gate disagrees with the book's depth")


def test_the_old_constants_no_longer_decide_anything():
    """Setting either constant to an absurd value must not change the verdict.

    This is the check that the replacement is real rather than additive. If `_carrot_pays` still
    consulted them, moving them would move the answer -- and a rule that still reads an unmeasured
    constant is the rule we are removing.
    """
    obs, seat = _obs("98495047")
    before = SA._carrot_pays(obs, seat)
    old_drain, old_opp = SA.CARROT_DRAIN_MIN, SA.CARROT_OPP_MAX
    try:
        SA.CARROT_DRAIN_MIN, SA.CARROT_OPP_MAX = 10_000, 0
        assert SA._carrot_pays(obs, seat) is before, (
            "the gate still reads CARROT_DRAIN_MIN / CARROT_OPP_MAX")
    finally:
        SA.CARROT_DRAIN_MIN, SA.CARROT_OPP_MAX = old_drain, old_opp
