"""Task #55: the tape arena has to be an opponent, not a corpse.

Every failure mode this project has hit with a new harness is a variant of "it ran and measured
nothing": the $3,000 stake read as a score, a saturated pool read as a win, offers read as fills. So
these check liveness and independence before anything checks a number.
"""

import pathlib

import pytest

from kagg.arena import AgentFactory, run_match
from kagg.arena.tape import build_tape_agent, load_tape

TAPE = pathlib.Path("data/seed_scripts/top_guys/90976060.json")
TCSI_1326 = 24
STAKE = 3000.0

pytestmark = pytest.mark.skipif(not TAPE.exists(), reason=f"{TAPE} is gitignored data")


def test_the_tape_is_the_economy_we_are_measuring_in():
    """`townCenterSellInterval` is the one line separating 1.32.2 from 1.32.6, and reading it
    wrong cost a full day of tuning. A tape from the other economy is a different game."""
    _stream, name, tcsi = load_tape(TAPE, 0)
    assert tcsi == TCSI_1326, (
        f"{TAPE.name} is a 1.32.{'2' if tcsi == 12 else '?'} recording (tcsi={tcsi}); the ladder "
        f"runs 1.32.6 (tcsi=24) and this tape prices a market that no longer exists")
    assert name, "no team name recorded"


def test_a_tape_actually_plays_a_season():
    """The liveness guard. A farm holding exactly the $3,000 stake did nothing at all -- that is
    how 'verify built artifacts actually run' was learned, twice."""
    res = run_match(AgentFactory(build_tape_agent, str(TAPE), 0), "pass", seed=11)
    assert res.money[0] > STAKE * 5, (
        f"the tape banked ${res.money[0]:,.0f} against a ${STAKE:,.0f} stake -- it is passing, not "
        f"playing. Check the action dict shape and the hand truncation.")


def test_two_tape_agents_from_one_factory_are_independent():
    """The #54 defect, in the new code. `build_tape_agent` holds a turn counter, so one shared
    object driven through two matches replays the second season from wherever the first stopped."""
    factory = AgentFactory(build_tape_agent, str(TAPE), 0)
    a, b = factory(), factory()
    for _ in range(50):
        a({"player": 0, "farms": [{"hands": []}, {"hands": []}]})
    first = b({"player": 0, "farms": [{"hands": []}, {"hands": []}]})
    fresh = factory()({"player": 0, "farms": [{"hands": []}, {"hands": []}]})
    assert first == fresh, "a second agent from the same factory inherited the first one's turn"


def test_a_tape_must_be_passed_as_a_factory_not_a_prebuilt_agent():
    """Tapes run in `run_arena` -- as `AgentFactory(build_tape_agent, path, seat)`, which is built
    once per match inside the worker. What is refused is a *pre-built* agent object, because it
    holds a turn counter and one object driven through 32 matches would replay match two from
    wherever match one stopped. That is #54's defect, and before the fix this call would have run
    and quietly returned garbage rather than raising."""
    from kagg.arena import run_arena

    with pytest.raises(TypeError, match="live callable"):
        run_arena(build_tape_agent(str(TAPE), 0), "pass", seeds=[0])


def test_market_jitter_moves_the_orders_and_nothing_else():
    """`farmer` and `hands` are board-dependent: a walk is a sequence to a specific tile and a PLANT
    is legal only on tilled ground, so perturbing either measures us against a cripple. Only the
    market may move."""
    plain = build_tape_agent(str(TAPE), 0)
    noisy = build_tape_agent(str(TAPE), 0, jitter_seed=7, drop=0.5, scale=0.5)
    obs = {"player": 0, "farms": [{"hands": [{}] * 12}, {"hands": []}]}

    moved = 0
    for _ in range(24 * 12):
        p, n = plain(obs), noisy(obs)
        assert p["farmer"] == n["farmer"], "jitter moved the farmer"
        assert p["hands"] == n["hands"], "jitter moved a hand"
        moved += p["market"] != n["market"]
    assert moved > 0, "jitter changed no market order in twelve days; the knobs are inert"
