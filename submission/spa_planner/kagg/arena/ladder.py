"""A graded fitness: how far up a ladder of opponents a candidate gets.

**Why a ladder rather than one opponent.** `converter` scores 0 wins in 16 seed-paired games
against `contrarian`, both before and after two real bug fixes that measurably repaired its crop.
A fitness that reads 0 for every candidate carries no information, and no evolutionary method --
plain ES, CMA-ES, memetic, island -- can select among candidates that all score the same. The
eight hand-tunings that "did not converge" were sampling exactly that flat surface.

So the opponents are ordered by strength and the score is the mean win rate across all of them.
A candidate that cannot yet touch `contrarian` is still ranked by how it does against `starter`
and `rancher`, and the score moves continuously as it improves. The ladder spans a wide enough
range that something in the middle is always contested.

**Census invariants are the second signal, and they have no seed variance at all.** Final money
has ~15% seed variance and needs many seeds to resolve; "this agent issued 447 no-op actions" is
exact from a single episode and points at one branch. They are reported alongside the win rate,
and used only to break ties -- never as the objective, because they measure waste rather than
winning and an agent can be tidy and still lose.

Specs are the same picklable forms `pool.py` accepts, plus ``("converter", {...})`` and
``("heuristic", {...})`` for a parameterised candidate, because closures cannot be sent to a
worker process.
"""

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field

# Ordered weakest to strongest, by measured head-to-head. `pass` and `starter` barely contest the
# market, so they are a floor rather than a test -- kept because a broken candidate needs somewhere
# to register at all, and a score against them is the difference between "losing" and "not playing".
# `contrarian` beats `heuristic` and `rancher` 100%.
LADDER = (
    ("pass", "pass"),
    ("starter", "starter"),
    ("rancher", ("module", "kagg.agents.rancher")),
    ("heuristic", ("module", "kagg.agents.heuristic")),
    ("contrarian", ("module", "kagg.agents.contrarian")),
)

RUNGS = tuple(name for name, _ in LADDER)
_SPECS = dict(LADDER)

# Ops that change nothing when they are issued against an unsatisfied precondition. The environment
# accepts them and silently returns, so they cost a turn and leave the board identical -- which is
# how a unit can pick the same one every turn for ten days. Counting them needs no knowledge of why
# any particular one failed.
_WASTEFUL = ("HARVEST", "WATER", "FEED", "PICKUP", "PLACE", "CARE", "COLLECT_FERTILIZER", "PLANT")


def build(spec):
    """Turn a picklable spec into a callable agent. Only ever called inside a worker."""
    from importlib import import_module

    if isinstance(spec, tuple) and spec and spec[0] == "module":
        return import_module(spec[1]).agent
    if isinstance(spec, tuple) and len(spec) == 2 and isinstance(spec[1], dict):
        module = import_module(f"kagg.agents.{spec[0]}")
        return module.make_agent(spec[1])
    if isinstance(spec, str):
        return spec
    raise ValueError(f"unrecognised agent spec: {spec!r}")


@dataclass(frozen=True)
class LadderResult:
    """Per-rung outcome, oriented to the candidate."""

    score: float                     # mean win rate over every rung -- the fitness
    per_rung: dict = field(default_factory=dict)     # name -> (win_rate, mean_money)
    games: int = 0

    # Waste deliberately does not live here. It is measured by `census`, which plays its own
    # episode, and a field that `evaluate` never fills would print 0.0% forever -- the same shape
    # of always-blank metric that let `wr 0.500` and `ev_signal n/a` go unread for a whole run.

    def __str__(self):
        rows = "  ".join(f"{n}:{wr:.0%}" for n, (wr, _m) in
                         sorted(self.per_rung.items(), key=lambda kv: RUNGS.index(kv[0])))
        return f"score {self.score:.3f}  | {rows}"


def _play(job):
    """One seating of one seed against one rung."""
    candidate, spec, seed, swapped = job
    from kaggle_environments import make

    me, them = build(candidate), build(spec)
    pair = (them, me) if swapped else (me, them)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(list(pair))
    final = env.steps[-1]
    money = (final[0]["reward"], final[1]["reward"])
    return (money[1], money[0]) if swapped else money


def evaluate(candidate, seeds, rungs=RUNGS, workers=1):
    """Play `candidate` against every rung, both seatings, every seed.

    The score is the **mean win rate across rungs**, each rung weighted equally regardless of how
    many seeds it drew, so adding a seed to one rung cannot shift the balance between them.
    """
    jobs, owners = [], []
    for name in rungs:
        for seed in seeds:
            for swapped in (False, True):
                jobs.append((candidate, _SPECS[name], seed, swapped))
                owners.append(name)

    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(_play, jobs))
    else:
        results = [_play(j) for j in jobs]

    per = {}
    for name, (mine, theirs) in zip(owners, results):
        wins, total, money = per.get(name, (0, 0, 0.0))
        per[name] = (wins + (mine > theirs), total + 1, money + mine)

    per_rung = {n: (w / t, m / t) for n, (w, t, m) in per.items()}
    return LadderResult(
        score=sum(wr for wr, _m in per_rung.values()) / max(1, len(per_rung)),
        per_rung=per_rung,
        games=len(jobs),
    )


def census(candidate, opponent="contrarian", seed=4000):
    """Waste and op mix over one episode. Zero seed variance, one branch to blame.

    An action is counted as waste when applying it leaves the farm byte-identical. That is measured
    by running the environment's own `_apply_unit_action` against a copy of the farm rather than
    re-deriving eighteen preconditions here, which is how the ten-day no-op HARVEST loop was missed
    in the first place -- the agent's idea of "harvestable" and the environment's disagreed, and any
    check written from the same misreading would have agreed with the agent.
    """
    import copy

    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as kg

    ops, wasted, total = Counter(), 0, 0
    play = build(candidate)

    def spy(obs, config=None):
        nonlocal wasted, total
        action = play(obs, config)
        me = obs["player"]
        farm, private = obs["farms"][me], obs["private"]
        day = obs.get("day", 0)
        units = [action["farmer"]] + list(action["hands"])
        for idx, act in enumerate(units):
            ops[act[0]] += 1
            if act[0] == "PASS":
                continue
            total += 1
            if act[0] not in _WASTEFUL:
                continue
            f2, p2 = copy.deepcopy(farm), copy.deepcopy(private)
            try:
                kg._apply_unit_action(f2, p2, idx, act, len(farm["tiles"]), day, 24)
            except Exception:
                continue
            if f2 == farm and p2 == private:
                wasted += 1
        return action

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([spy, build(_SPECS[opponent])])
    return dict(ops=dict(ops), waste=wasted / max(1, total), wasted=wasted, actions=total)
