"""An opponent pool, and evaluation against it.

Why this exists: the first submitted agent scored $43.6k against the built-in `starter` and
$21.2k against a copy of itself. Every parameter had been chosen against `starter`, which sells
almost nothing, so the market never got contested and every number was roughly twice reality.
The agent then lost its ranked matches.

So: **never tune against `starter` alone.** Tune against opponents that actually compete for
prices, and select on **win rate**, because the leaderboard is an Elo-style rating where margin
does not count.

Pool members are `(name, spec)` where a spec is either a built-in agent name or a dict of
parameter overrides for the heuristic agent. Dicts rather than closures so jobs stay picklable
for worker processes.
"""

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

# Fixed reference strategy the named opponents are built from. Frozen on purpose: if opponents
# inherited the candidate's parameters, changing the candidate would change the opposition too and
# no two measurements would be comparable. Only "mirror" follows the candidate.
BASELINE = {
    "tiles_per_hand": 14,
    "max_hands": 14,
    "carry_before_drop": 25,
    "seed_buffer": 0,
    "land_slack": 3.0,
    "productive_gate": 0.8,
    "phase_mod": 5,
    "cow_tiles": 0,
    "strawberry_tiles": 0,
    "melon_tiles": 12,
    "sell_floor_frac": 0.55,
    "plant_floor_frac": 0.45,
    "endgame_day": 28,
}

# Strategy profiles rather than near-duplicates, so a candidate cannot win by exploiting one
# opponent's specific blind spot. Fable's review flagged single-opponent overfitting explicitly.
MIRROR = "__mirror__"
OPPONENTS = {
    "mirror": MIRROR,                                       # follows the candidate's own params
    "wheat_only": {"strawberry_tiles": 0, "melon_tiles": 0, "cow_tiles": 0},
    "melon_heavy": {"strawberry_tiles": 0, "melon_tiles": 25, "cow_tiles": 0},
    "strawberry": {"strawberry_tiles": 25, "melon_tiles": 0, "cow_tiles": 0},
    "cow_heavy": {"cow_tiles": 20, "melon_tiles": 8, "strawberry_tiles": 0},
    "starter": "starter",
    "pass": "pass",
}

# The pool worth optimising against: everything that actually competes for market prices.
COMPETITIVE = ("mirror", "wheat_only", "melon_heavy", "strawberry", "cow_heavy")


@dataclass(frozen=True)
class PoolResult:
    """Aggregate over every opponent, oriented to the candidate."""

    win_rate: float
    draw_rate: float
    mean_money: float
    per_opponent: dict  # name -> (win_rate, mean_money)

    def __str__(self):
        rows = "  ".join(
            f"{name}:{wr:.0%}/${money:.0f}" for name, (wr, money) in sorted(self.per_opponent.items())
        )
        return f"win {self.win_rate:.1%} (draw {self.draw_rate:.1%}) mean ${self.mean_money:.0f} | {rows}"


def _build(spec, candidate_params):
    """Turn a pool spec into something `env.run` accepts.

    Named strategies are built from the frozen BASELINE so they do not drift when the candidate
    changes; only MIRROR follows the candidate.
    """
    from kagg.agents import heuristic

    if spec == MIRROR:
        return heuristic.make_agent(candidate_params)
    if isinstance(spec, str):
        return spec
    return heuristic.make_agent({**BASELINE, **spec})


def _play(job):
    """One seating of one seed against one opponent. Returns (own_money, opponent_money)."""
    candidate_params, spec, seed, swapped = job
    from kaggle_environments import make

    from kagg.agents import heuristic

    me = heuristic.make_agent(candidate_params)
    them = _build(spec, candidate_params)
    pair = (them, me) if swapped else (me, them)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(list(pair))
    final = env.steps[-1]
    money = (final[0]["reward"], final[1]["reward"])
    return (money[1], money[0]) if swapped else money


def evaluate(candidate_params, seeds, opponents=COMPETITIVE, workers=10):
    """Play `candidate_params` against every named opponent, both seatings, every seed."""
    jobs, owners = [], []
    for name in opponents:
        for seed in seeds:
            for swapped in (False, True):
                jobs.append((candidate_params, OPPONENTS[name], seed, swapped))
                owners.append(name)

    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(_play, jobs))
    else:
        results = [_play(j) for j in jobs]

    per = {}
    for name, (mine, theirs) in zip(owners, results):
        wins, draws, total, money = per.get(name, (0, 0, 0, 0.0))
        per[name] = (
            wins + (mine > theirs),
            draws + (mine == theirs),
            total + 1,
            money + mine,
        )

    per_opponent = {n: (w / t, m / t) for n, (w, d, t, m) in per.items()}
    games = sum(t for _, _, t, _ in per.values())
    return PoolResult(
        win_rate=sum(w for w, _, _, _ in per.values()) / games,
        draw_rate=sum(d for _, d, _, _ in per.values()) / games,
        mean_money=sum(m for _, _, _, m in per.values()) / games,
        per_opponent=per_opponent,
    )
