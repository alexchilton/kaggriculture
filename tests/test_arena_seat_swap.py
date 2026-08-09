"""Task #58: `run_arena` swaps seats, and an agent with its seat baked in never finds out.

`run_arena` plays every seed twice with the seats exchanged, because market orders settle in seat
order and seat 0 has a real edge on a contested trade. That cancels the seat advantage only if both
agents actually *play* the seat they are given.

`kagg.search.schedule_agent.make_agent(schedule, me)` takes its seat as a construction argument and
reads `obs["farms"][me]` forever after. Placed in seat 1 by the swap, it reads the opponent's farm:
it waters their tiles, feeds their animals, and sells stock it does not hold. Half of every
`run_arena` sweep over a schedule agent was that.

`submission/main.py` is immune -- it reads `obs["player"]` per turn -- which is why this never
showed up in a gate and only shows up in sweeps. `scripts/confirm_late_sell_bias.py` works around it
by building its own agent per seating; `run_arena` could not, because it only held a callable.

Now that #54 made the factory the unit of construction, the seat can be handed to it. A factory
with `seat_kwarg` set is built once per *seating*, told which seat it is about to occupy.
"""

import pytest

from kagg.arena import AgentFactory, run_arena
from kagg.arena.arena import _play_job, _resolve


def _seat_reporter(*, me=None):
    """A builder whose agent reports the seat it was CONSTRUCTED with, not the one it is in."""
    def agent(obs, config=None):
        return me
    return agent


def _plain():
    def agent(obs, config=None):
        return "no-seat"
    return agent


def test_a_seat_aware_factory_is_built_for_the_seat_it_will_occupy():
    """The core of the fix. Same factory object, two seats, two differently-built agents."""
    f = AgentFactory(_seat_reporter, seat_kwarg="me")
    assert _resolve(f, 0)(None) == 0
    assert _resolve(f, 1)(None) == 1, (
        "the factory was not told which seat it is playing; an agent that bakes in its seat will "
        "read the opponent's farm for the whole swapped half of the sweep")


def test_a_factory_without_seat_kwarg_is_untouched():
    """Opt-in. `build_tape_agent` and every existing caller take their seat positionally and must
    not suddenly receive a keyword they do not accept."""
    f = AgentFactory(_plain)
    assert _resolve(f, 0)(None) == "no-seat"
    assert _resolve(f, 1)(None) == "no-seat"


def test_a_name_or_path_still_passes_straight_through():
    """A built-in name and a file path are what the env resolves itself; seat-awareness must not
    turn them into calls."""
    assert _resolve("starter", 0) == "starter"
    assert _resolve("submission/main.py", 1) == "submission/main.py"


@pytest.mark.slow
def test_the_swapped_seating_builds_agent_a_for_seat_one():
    """`_play_job` is where the swap happens, so it is where the seat has to arrive.

    Marked slow because it plays a real game: the stub agent returns `None`, which the environment
    accepts as "no action" rather than rejecting, so there is no way to observe the construction
    without letting the season run. The money is irrelevant; `seen` is the assertion.
    """
    seen = []

    def _spy(*, me=None):
        seen.append(me)
        return lambda obs, config=None: None

    f = AgentFactory(_spy, seat_kwarg="me")
    _play_job((f, "pass", 0, True))
    assert seen and seen[0] == 1, (
        f"under the swap, agent_a takes seat 1 but was built with me={seen[0] if seen else None}")


def test_run_arena_still_refuses_a_live_callable():
    """The #54 guard must survive the change -- a bare callable is still one object for every
    match, seat-aware or not."""
    with pytest.raises(TypeError, match="live callable"):
        run_arena(_plain(), "pass", seeds=[0])
