"""Task #54: `run_arena` must not drive one agent object through more than one match.

The theory under test, stated so it can fail: `run_arena` takes an agent *value* and passes that
same object into every job -- every seed, both seatings -- while `kagg.search.schedule_agent`'s
`make_agent` builds its `state` dict once in the closure (`day=-1`, `hired`, `bought`, `pins`,
`planted`, `pen_for`) and resets only the per-day part on a day change. A finished season therefore
walks into the next match.

Tests deliberately different in kind:

* `test_run_arena_gives_each_match_its_own_agent` is structural and needs no fixture. It counts how
  many games one agent object was driven through. That is the defect itself, with no economics in
  the way.
* `test_run_arena_does_not_carry_a_season_into_the_next_match` is the money. It plays the real
  schedule agent, and the same seed listed twice must not move the mean.
* `test_a_path_spec_was_never_contaminated` is the control: the shipped artifact travels as a path,
  which `kaggle_environments` re-`exec`s per match, so it was never on the broken path at all.

Measured before the fix, seed 40 against `pass`: `seeds=[40]` means $115,237 and `seeds=[40, 40]`
means $57,618, because matches three and four bank $0 -- below the $3,000 opening stake, so the
agent is being invalidated rather than playing badly. See `docs/arena_state_leak_2026-08-09.md`.

`tests/conftest.py` marks whole modules slow by name; this one is in `SLOW_MODULES` beside
`test_arena`, so it runs under `pytest -m slow`.
"""

import json
import pathlib

import pytest

from kagg.arena import AgentFactory, run_arena

SEED = 40
SCHEDULE = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
SUBMISSION = pathlib.Path("submission/main.py")
#: Rows that describe the recorded tape rather than a decision the agent makes.
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


class _GameCounter:
    """Banks nothing; records how many distinct games it was driven through.

    A fresh instance per match sees exactly one `day 0, hour 0`. An instance reused across matches
    sees one per match, which is the whole of the defect.
    """

    def __init__(self):
        self.games = 0

    def __call__(self, obs, config=None):
        if int(obs.get("day", 0) or 0) == 0 and int(obs.get("hour", 0) or 0) == 0:
            self.games += 1
        return {"farmer": ["PASS"], "hands": [], "market": []}


def _thin_schedule():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    return {d: {k: v for k, v in row.items() if k not in TAPE_ONLY} for d, row in sched.items()}


def _schedule_agent():
    """The shipped agent's shape *without* its day-0 rebuild -- one lazy instance per seat.

    `submission/main.py` already rebuilds at `day == 0 and hour == 0`; this is what it looked like
    before that line, and what every in-process caller of `make_agent` still looks like.
    """
    import kagg.search.schedule_agent as SA

    thin = _thin_schedule()
    seats = {}

    def agent(obs, config=None):
        me = int(obs.get("player", 0) or 0)
        if me not in seats:
            seats[me] = SA.make_agent(thin, me, router=True)
        return seats[me](obs)

    return agent


def test_run_arena_gives_each_match_its_own_agent():
    """One `run_arena` call over one seed is two matches, and must be two agents.

    The factory records what it built, so the assertion is on the objects themselves rather than on
    a number the aggregate might launder.
    """
    built = []

    def build():
        counter = _GameCounter()
        built.append(counter)
        return counter

    run_arena(AgentFactory(build), "pass", seeds=[SEED], workers=1)

    assert len(built) == 2, f"{len(built)} agents built for 2 matches"
    for counter in built:
        assert counter.games == 1, (
            f"one agent object was driven through {counter.games} games; every match after the "
            f"first inherits the previous season's state"
        )


def _build_counter():
    """Module level on purpose -- a factory is only picklable if what it holds is."""
    return _GameCounter()


def test_a_factory_survives_the_worker_pool():
    """`workers > 1` was unusable for anything built in process; the factory is what unlocks it.

    `scripts/arena_gate.py` pins `--workers 1` and documents why: "Can't pickle local object
    'make_agent.<locals>.agent'" silently dropped two of six opponents. An `AgentFactory` ships the
    *recipe* -- a module-level function and picklable arguments -- and builds inside the worker.
    """
    report = run_arena(AgentFactory(_build_counter), "pass", seeds=[0, 1], workers=2)

    assert report.games == 4
    assert report.mean_money[0] == 3000.0     # PASS every turn, so the opening stake, untouched


def test_run_arena_refuses_a_live_agent():
    """A bare callable is the trap, so it has to be loud rather than merely discouraged."""
    with pytest.raises(TypeError, match="AgentFactory"):
        run_arena(_GameCounter(), "pass", seeds=[SEED], workers=1)


@pytest.mark.skipif(not SCHEDULE.exists(), reason=f"missing fixture {SCHEDULE}")
def test_run_arena_does_not_carry_a_season_into_the_next_match():
    """The same seed listed twice must not change the mean.

    Comparing `[SEED]` against `[SEED, SEED]` rather than against a single `run_match` is
    deliberate: seat 0 commits first on a contested trade, so a one-seating comparison would be
    measuring the seat as well as the leak. Both calls here play the identical pair of seatings,
    the second one twice, so seat effects cancel exactly and only carried state can move the number.
    """
    once = run_arena(AgentFactory(_schedule_agent), "pass", seeds=[SEED], workers=1)
    twice = run_arena(AgentFactory(_schedule_agent), "pass", seeds=[SEED, SEED], workers=1)

    # **Check the agent farmed before comparing two numbers.** $3,000 is the opening stake and $0 is
    # a crashed agent; either would make the equality below true and meaningless -- and backing the
    # fix out is one of the ways to reach exactly that, since an unresolved factory is called with
    # `(observation, configuration)` and dies. CLAUDE.md's "verify built artifacts actually run".
    assert once.mean_money[0] > 3000.0, (
        f"the agent banked ${once.mean_money[0]:,.0f}; it did not play a season, so the comparison "
        f"below would be vacuous"
    )
    assert twice.mean_money[0] == pytest.approx(once.mean_money[0]), (
        f"the same seed played twice means ${twice.mean_money[0]:,.0f} against "
        f"${once.mean_money[0]:,.0f} for one copy of it"
    )


@pytest.mark.skipif(not SUBMISSION.exists(), reason=f"missing {SUBMISSION} -- build it first")
def test_a_path_spec_was_never_contaminated():
    """The SHIPPED artifact was never affected, and this is the check that says so.

    `scripts/gate_pool.py` passes `submission/main.py` as a path, and `kagg.arena.pool.evaluate`
    passes that path straight through to `kaggle_environments`. `build_agent` there re-`exec`s the
    file into a fresh namespace for each `Agent`, and an `Agent` is constructed per `env.run`, so a
    path gets a fresh module -- and therefore a fresh `_AGENTS` dict -- every match, in every worker.
    The artifact also rebuilds its own agent at `day == 0 and hour == 0` on top of that.

    Same shape as the test above, so a regression in either mechanism shows up the same way.
    """
    once = run_arena(str(SUBMISSION), "pass", seeds=[SEED], workers=1)
    twice = run_arena(str(SUBMISSION), "pass", seeds=[SEED, SEED], workers=1)

    assert once.mean_money[0] > 3000.0, f"the artifact banked ${once.mean_money[0]:,.0f}"
    assert twice.mean_money[0] == pytest.approx(once.mean_money[0])
