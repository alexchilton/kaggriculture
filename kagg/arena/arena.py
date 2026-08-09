"""Running Kaggriculture matches and reporting results.

Agents are identified by picklable specs -- a built-in name such as ``"starter"``
or a path to a ``.py`` file -- so that matches can be farmed out to worker
processes. Callables are deliberately not supported.

**A live callable is one object, and :func:`run_arena` plays many matches.** That combination cost
this project a 17.8x error: `kagg.search.schedule_agent.make_agent` builds its `state` dict once in
the closure (`day=-1`, `hired`, `bought`, `pins`, `planted`, `pen_for`) and resets only the per-day
part on a day change, so a finished season walked into the next match and killed the agent outright.
Measured 2026-08-09 (`docs/arena_state_leak_2026-08-09.md`): seed 40 against `pass`, one copy of the
seed means $115,237 and the same seed listed twice means $57,618, because matches three and four
bank $0. Over seeds 20-27 against `heuristic`/`rancher`/`contrarian`, one shared agent scores
$5,774 / 6.2% where one agent per match scores $102,886 / 100%. A path or a built-in name never had
this problem -- `kaggle_environments` re-`exec`s the file for each `Agent`, so those get a fresh
namespace per match.

So :func:`run_arena` takes a *factory*, not an agent. Wrap the builder in :class:`AgentFactory` and
it is invoked once per match, inside the worker. :func:`run_match` plays exactly one match and
therefore still accepts a bare callable; nothing can leak out of a single game.
"""

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass


class AgentFactory:
    """A picklable "build me a fresh agent" instruction, invoked once per match.

    ``AgentFactory(build, *args, **kwargs)`` calls ``build(*args, **kwargs)`` and returns whatever
    the environment should drive. Keep `build` a module-level function and the arguments picklable
    and the factory survives the trip to a ``ProcessPoolExecutor`` worker -- which a `make_agent`
    closure never did, and which is why `scripts/arena_gate.py` documents `workers=1` as a
    constraint. The build runs in the worker, so the closure is created there rather than shipped.
    """

    __slots__ = ("build", "args", "kwargs")

    def __init__(self, build, *args, **kwargs):
        if not callable(build):
            raise TypeError(f"AgentFactory needs a callable, got {type(build).__name__}")
        self.build = build
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.build(*self.args, **self.kwargs)

    def __reduce__(self):
        # `__slots__` and no `__dict__`, so spell the reconstruction out rather than relying on the
        # default protocol. Keeps the class usable under `workers > 1`, which is the point of it.
        return (_rebuild_factory, (self.build, self.args, self.kwargs))


def _rebuild_factory(build, args, kwargs):
    return AgentFactory(build, *args, **kwargs)


def _resolve(spec):
    """A factory becomes a brand new agent; every other spec is passed through untouched."""
    return spec() if isinstance(spec, AgentFactory) else spec


@dataclass(frozen=True)
class MatchResult:
    """Outcome of a single game.

    ``money`` is the final bank of each player, which is also the environment's
    reward and the competition's score.
    """

    seed: int
    money: tuple[float, float]


@dataclass(frozen=True)
class ArenaReport:
    """Aggregate of many games, seat-swapped.

    All fields are oriented to the *first* agent passed to :func:`run_arena`,
    regardless of which seat it occupied in any given game.
    """

    games: int
    mean_money: tuple[float, float]
    win_rate: float
    draw_rate: float
    mean_delta: float

    def __str__(self):
        return (
            f"{self.games} games | "
            f"money {self.mean_money[0]:.0f} vs {self.mean_money[1]:.0f} "
            f"(delta {self.mean_delta:+.0f}) | "
            f"win rate {self.win_rate:.1%} (draws {self.draw_rate:.1%})"
        )


def run_match(agent_a, agent_b, seed):
    """Play one game and return the final bank of each player.

    A bare callable is fine here and is how `scripts/confirm_late_sell_bias.py` drives its
    fresh-agent-per-match sweep: one match cannot leak into a next one that does not exist.
    An :class:`AgentFactory` is honoured too, so the same spec works through either entry point.
    """
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([_resolve(agent_a), _resolve(agent_b)])
    final = env.steps[-1]
    return MatchResult(seed=seed, money=(final[0]["reward"], final[1]["reward"]))


def _play_job(job):
    """Play one seating of one seed, returning money oriented to agent A.

    Module level so that it survives pickling to a worker process. `run_match` resolves each
    factory, so the agent is built here -- once per match, in whichever process plays it.
    """
    agent_a, agent_b, seed, swapped = job
    seating = (agent_b, agent_a) if swapped else (agent_a, agent_b)
    result = run_match(seating[0], seating[1], seed)
    money = (result.money[1], result.money[0]) if swapped else result.money
    return money


def _check_spec(spec, label):
    """Refuse a live agent object, because `run_arena` would drive it through every match.

    Raising rather than quietly wrapping it: there is no way to rebuild an agent from an instance of
    one, and a stateless-looking callable is indistinguishable from a stateful one from out here.
    The 2x error in the module docstring is what silence buys.
    """
    if callable(spec) and not isinstance(spec, AgentFactory):
        raise TypeError(
            f"run_arena({label}=...) got a live callable, which it would drive through every match "
            f"and every seating. Pass a name (\"starter\"), a path to a .py file, or "
            f"AgentFactory(build, *args) so each match gets its own agent."
        )


def run_arena(agent_a, agent_b, seeds, workers=1):
    """Play every seed in both seatings and aggregate the outcome.

    Each seed is played twice with the seats exchanged, which removes any
    advantage attached to being player 0 -- market orders settle in seat order,
    so this is not merely theoretical.

    Each of those matches gets its own agent. Pass an :class:`AgentFactory` for anything built in
    process; a bare callable is refused rather than reused.
    """
    _check_spec(agent_a, "agent_a")
    _check_spec(agent_b, "agent_b")

    jobs = [
        (agent_a, agent_b, seed, swapped)
        for seed in seeds
        for swapped in (False, True)
    ]

    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            monies = list(pool.map(_play_job, jobs))
    else:
        monies = [_play_job(job) for job in jobs]

    games = len(monies)
    total_a = sum(m[0] for m in monies)
    total_b = sum(m[1] for m in monies)
    wins = sum(1 for m in monies if m[0] > m[1])
    draws = sum(1 for m in monies if m[0] == m[1])

    return ArenaReport(
        games=games,
        mean_money=(total_a / games, total_b / games),
        win_rate=wins / games,
        draw_rate=draws / games,
        mean_delta=(total_a - total_b) / games,
    )
