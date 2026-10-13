"""The offline day solver, run inline against the day the agent is actually playing.

`scripts/solve_day.py` searches the assignment AND the order of a day's jobs against `cover.py`'s
own cost model, and it wins: on the fixtures it seats work the shipped greedy leaves uncovered. Its
output was frozen into `solved_days.SOLVED_DAYS`, and that is the form that cannot survive a change
of plan -- the fixture names tiles and ops, so when the schedule or the matrix moves the day's job
set, the stops stop matching. `solved_days.py`'s own docstring measures it: of the previous
generation's 571 stops only 143 still matched a job our board had, the rest silently skipped.

So the search is not frozen here. It runs at dawn on whatever jobs the day has, which is what makes
it independent of the schedule and of the matrix: those change WHICH tiles carry work, and this
searches over the work it is given.

**Nothing about the constraints is re-invented.** Feasibility is `cover.materialise` plus
`cover.turns` under each unit's own budget, so a candidate is legal only if the tour can really be
walked; `materialise` inserts the shed trips a sequence needs, honours `due` -- the turn by which
the row's produce has to be STANDING IN THE SHED -- and `deliver=False` is the case where a hand may
simply carry its load to the bell, because `_drop_inventories_to_shed` banks every hand into the
shed at the rollover for free. The objective is coverage weighted by what a miss costs, turns only
as a tie-break, mirroring the tiers `cover`'s own passes run in.

**Why a one-second budget is enough.** Quality saturates early: measured at 157 iterations/sec,
3 seconds reaches 106 turns where 300 seconds reaches 100. The day is planned ONCE, at dawn, so the
cost is one solve a day and not one a turn.
"""
import collections
import random
import time

#: Coverage weights, same tiers and magnitudes as `scripts/solve_day.py`. Each tier only has to
#: outrank any number of the tier below it, and a day holds under a hundred jobs.
W_DEATH = 1_000_000      # at_risk AND required: the animal is removed
W_RISK = 10_000          # at_risk: the tile becomes a WEED
W_FUNDS = 1_000          # the day's shopping list, unpaid
W_REQUIRED = 100
W_ORDINARY = 1

#: Wall clock a dawn solve may spend, and the ruin size. Both parameters, not switches.
SECONDS = 1.0
RUIN = 6
SEED = 20260911


#: Row field for each op the row states a count of. `plants` and `places` are LISTS in the row, so
#: their length is the count; the rest are already integers.
ROW_OPS = {"WATER": "waters", "FEED": "feeds", "CARE": "cares", "HARVEST": "harvests",
           "PLANT": "plants", "BUILD": "builds", "PLACE": "places"}


def violations(routes, row):
    """How far this plan's op counts sit from the row. 0 means every stated count is met.

    **The constraints are the gate, and turns are only a tie-break below them.** Coverage as a
    weighted SUM lets the search trade a FEED against turns and still score better, which is how a
    plan that spends fewer turns lands a different board: measured, spataro d7 6 -> 12 and d7 91
    against 71 over the eight worlds that finished. Alex: "i have no issue with it spending fewer
    turns - AS LONG AS ALL CONSTRAINTS ARE ALSO SATISFIED".

    Absolute difference, not shortfall, because the gate counts a field that differs in either
    direction -- bakery d7 is `water 27/21`, an overshoot, and it costs the same cell as a miss.

    Read off the row, so it is per-world and per-matrix with nothing to configure: the matrix moves
    the counts and this moves with it.
    """
    if not row:
        return 0
    got = collections.Counter()
    for seq in routes.values():
        for j in seq:
            for o, _i in getattr(j, "ops", ()):
                got[o] += 1
    out = 0
    for op, field in ROW_OPS.items():
        want = row.get(field)
        if want is None:
            continue
        want = len(want) if isinstance(want, (list, tuple)) else int(want)
        out += abs(got[op] - want)
    return out


def weight(j):
    if getattr(j, "at_risk", False) and getattr(j, "required", False):
        return W_DEATH
    if getattr(j, "at_risk", False):
        return W_RISK
    if getattr(j, "funds", False):
        return W_FUNDS
    if getattr(j, "required", False):
        return W_REQUIRED
    return W_ORDINARY


class _Oracle:
    """`cover.py`'s own cost model, memoised. None when the tour cannot be built."""

    def __init__(self, C, units, budget, depots, carry, wanted, deliver, rush, due):
        self.C, self.units, self.budget = C, units, budget
        self.depots, self.carry, self.wanted = depots, carry, wanted
        self.deliver, self.rush, self.due = deliver, rush, due
        self.cache = {}

    def cost(self, u, seq):
        return self._both(u, seq)[0]

    def banked_by(self, u, seq):
        """Turn by which this tour has made its LAST shed drop, or 0 if it never banks.

        **This is "get the harvest in early", as a number the search can minimise.** Matching a
        count is not enough: a tour that harvests at h20 still reports `harvest 8/8` and sells
        nothing, because the market reads the SHED and the produce is in a hand. His d8 takes the
        harvest at h0 and the milk sells at h1.

        Total turns -- what this replaced -- is actively wrong for the gate. A plan that does the
        same work in fewer turns scores better and leaves a different board: measured on the
        nine-world gate, spataro d7 went 6 -> 11 and the eight finished worlds read d7 91 against
        the keeper's 71 on the same eight.
        """
        return self._both(u, seq)[1]

    def _both(self, u, seq):
        key = (u, tuple(id(j) for j in seq))
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        tour = self.C.materialise(self.units[u], list(seq), (self.carry or {}).get(u),
                                  self.depots, self.wanted, self.deliver, self.rush, due=self.due)
        if tour is None:
            self.cache[key] = (None, 0)
            return self.cache[key]
        c = self.C.turns(self.units[u], tour)
        last = None
        for i, st in enumerate(tour):
            if getattr(st, "depot", False) and getattr(st, "drop", False):
                last = i
        banked = 0 if last is None else self.C.turns(self.units[u], tour[:last + 1])
        self.cache[key] = (c, banked)
        return self.cache[key]


def _best_insertion(routes, j, oracle, rng):
    best = None
    us = list(routes)
    rng.shuffle(us)
    for u in us:
        seq = routes[u]
        base = oracle.cost(u, seq) or 0
        for pos in range(len(seq) + 1):
            c = oracle.cost(u, seq[:pos] + [j] + seq[pos:])
            if c is None or c > oracle.budget[u]:
                continue
            if best is None or c - base < best[0]:
                best = (c - base, u, pos)
    return best


def _recreate(routes, pool, oracle, rng):
    leftover = []
    for j in sorted(pool, key=lambda j: (-weight(j), -getattr(j, "turns", 0))):
        got = _best_insertion(routes, j, oracle, rng)
        if got is None:
            leftover.append(j)
            continue
        _d, u, pos = got
        routes[u] = routes[u][:pos] + [j] + routes[u][pos:]
    return leftover


def _score(routes, oracle, row=None):
    """(-row violations, covered weight, -turns). Higher is better, compared as a tuple.

    Lexicographic, and the order is the whole point. A plan that misses a count the row states can
    never win on turns, however few it spends; among plans that satisfy the row, fewer turns is
    free. `weight` sits between them so that while violations are equal the irreversible losses --
    an animal removed, a tile weeded -- still outrank ordinary work.
    """
    v = violations(routes, row)
    w = sum(weight(j) for seq in routes.values() for j in seq)
    t = sum(oracle.cost(u, seq) or 0 for u, seq in routes.items() if seq)
    return (-v, w, -t)


def solve(units, jobs, budget, depots=None, carry=None, supply=None, deliver=True, wanted=None,
          day=None, rush=False, due=None, start=None, row=None):
    """Same signature and return shape as `cover.cover`: `(work, uncovered)`.

    `start` is the assignment the search opens from -- the planner that is live today. The loop only
    ever accepts a STRICTLY better score, so this can match that planner or beat it and cannot come
    back worse than the plan it was handed.
    """
    from . import cover as C

    routes, left = (start or C.cover)(units, list(jobs), budget, depots, carry, supply, deliver,
                                     wanted, day, rush, due)
    routes = {u: list(v) for u, v in routes.items()}
    oracle = _Oracle(C, units, budget, depots, carry, wanted, deliver, rush, due)
    rng = random.Random(SEED)

    # The greedy's leftovers first: on the d12 fixture both fitted by plain insertion.
    left = _recreate(routes, list(left), oracle, rng)
    best, best_left = {u: list(v) for u, v in routes.items()}, list(left)
    best_score = _score(best, oracle, row)

    start = time.monotonic()
    # **No early exit on full coverage.** The objective's second term is total turns, and a plan
    # that seats every job can still be walked in fewer -- which is budget the next pass can spend.
    # `solve_day.py` only stops early under `--seconds 0`, where coverage IS the stopping condition.
    while time.monotonic() - start < SECONDS:
        trial = {u: list(v) for u, v in best.items()}
        pool = list(best_left)
        seated = [(u, j) for u, seq in trial.items() for j in seq]
        if seated:
            for u, j in rng.sample(seated, min(RUIN, len(seated))):
                if j in trial[u]:
                    trial[u].remove(j)
                    pool.append(j)
        leftover = _recreate(trial, pool, oracle, rng)
        sc = _score(trial, oracle, row)
        if sc > best_score:
            best, best_left, best_score = trial, leftover, sc

    return best, best_left
