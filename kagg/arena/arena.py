"""Running Kaggriculture matches and reporting results.

Agents are identified by picklable specs -- a built-in name such as ``"starter"``
or a path to a ``.py`` file -- so that matches can be farmed out to worker
processes. Callables are deliberately not supported.
"""

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass


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
    """Play one game and return the final bank of each player."""
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([agent_a, agent_b])
    final = env.steps[-1]
    return MatchResult(seed=seed, money=(final[0]["reward"], final[1]["reward"]))


def _play_job(job):
    """Play one seating of one seed, returning money oriented to agent A.

    Module level so that it survives pickling to a worker process.
    """
    agent_a, agent_b, seed, swapped = job
    seating = (agent_b, agent_a) if swapped else (agent_a, agent_b)
    result = run_match(seating[0], seating[1], seed)
    money = (result.money[1], result.money[0]) if swapped else result.money
    return money


def run_arena(agent_a, agent_b, seeds, workers=1):
    """Play every seed in both seatings and aggregate the outcome.

    Each seed is played twice with the seats exchanged, which removes any
    advantage attached to being player 0 -- market orders settle in seat order,
    so this is not merely theoretical.
    """
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
