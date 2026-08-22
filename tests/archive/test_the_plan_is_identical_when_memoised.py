"""Memoising `slot` must not change one job, one position, one turn.

## Why this exists

Submission 55352401 was disqualified on time, not on play. Episode 91023699, seat 0: 482 turns of
719, then TIMEOUT with the 60s overage bank at -1.7s. Every second of it came from 22 turns at
hours 1 and 2 -- the day solve -- and a profile of days 12-16 puts **99.7%** of all agent time
inside `_solve`, essentially all of it in `cover`:

    slot() called from     cover() [the COMPACT loop]   30,290 calls   20.19s
                           greedy()                     51,470 calls   11.96s

Both loops re-evaluate `slot(v, j, routes[v])` for units whose route has not changed since the
last sweep. `slot` walks every insertion position and re-materialises the whole tour at each one,
so that is 354,811 full tour rebuilds across 55 solves.

## Why this test is the right test

The agent it is optimising is a MEASURED, WINNING agent -- $127,846 against Seb's tape and 94.4%
against the opponent pool. The only defect is the clock. So the requirement is not "still good",
it is **identical**: same work sequences, same uncovered set, same everything, on every input.

`slot` depends on exactly four things -- the unit's position, the job, that unit's current route,
and the turn limit -- all of which are constant between mutations of `routes`. That is the
argument for why a version-keyed memo is exactly equivalent. This test is the evidence, because
the argument has to survive `COMPACT` moving jobs between units and `greedy` running five times
over four different job classes, and an argument is not a measurement.

Randomised and differential, in the style `Game._order_book` was verified with: many boards, both
settings, compared field by field. A single hand-built case would not reach the interaction that
matters.
"""

import random
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import cover as DP

OPS = ("WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER", "DIG")


def _random_jobs(rng, n, size=10):
    """A plausible day's work: a mix of ordinary tiles, herd jobs that draw wheat, and produce."""
    jobs = []
    for _ in range(n):
        tile = (rng.randrange(size), rng.randrange(size))
        op = rng.choice(OPS)
        needs = {"WHEAT": 1} if op == "FEED" else None
        gives = {rng.choice(("MILK", "WOOL", "EGG")): rng.randrange(1, 9)} if op == "HARVEST" else None
        j = DP.Job(tile, [(op, "WHEAT" if op == "FEED" else None)], needs=needs, gives=gives,
                   at_risk=rng.random() < 0.2)
        j.funds = rng.random() < 0.1
        jobs.append(j)
    return jobs


def _plan(rng_seed, memoise):
    """One full `cover` under a fixed seed, with the memo on or off."""
    rng = random.Random(rng_seed)
    n_units = rng.randrange(1, 9)
    units = [(rng.randrange(10), rng.randrange(10)) for _ in range(n_units)]
    jobs = _random_jobs(rng, rng.randrange(4, 26))
    budget = [rng.randrange(6, 24) for _ in range(n_units)]
    carry = {u: {"WHEAT": rng.randrange(0, 4)} for u in range(n_units)}
    supply = {"WHEAT": rng.randrange(0, 20), "COW": rng.randrange(0, 3)}
    wanted = {"MILK": rng.randrange(0, 12)} if rng.random() < 0.5 else None

    old = DP.MEMOISE_SLOT
    DP.MEMOISE_SLOT = memoise
    try:
        work, uncovered = DP.cover(units, jobs, budget, carry=carry, supply=supply, wanted=wanted)
    finally:
        DP.MEMOISE_SLOT = old

    # Compare by identity-free content: tile plus op list plus position, per unit.
    shape = {u: [(j.tile, tuple(o for o, _i in j.ops)) for j in seq] for u, seq in work.items()}
    left = sorted((j.tile, tuple(o for o, _i in j.ops)) for j in uncovered)
    return shape, left


@pytest.mark.parametrize("seed", range(40))
def test_the_memo_changes_nothing_about_the_plan(seed):
    """The whole point, forty times over."""
    assert _plan(seed, memoise=False) == _plan(seed, memoise=True), (
        f"seed {seed}: memoising slot() changed the plan")


def test_the_memo_is_actually_doing_something():
    """A test that passes with the optimisation switched off proves nothing.

    Guards against the memo silently never hitting -- a version key that changes every call would
    keep every assertion above green while saving nothing at all, and the timeout would come back.
    """
    rng = random.Random(7)
    units = [(0, 0), (9, 9), (4, 4)]
    jobs = _random_jobs(rng, 20)
    budget = [22, 22, 22]

    calls = {"n": 0}
    real = DP.materialise

    def spy(*a, **kw):
        calls["n"] += 1
        return real(*a, **kw)

    DP.materialise = spy
    try:
        for memo in (False, True):
            DP.MEMOISE_SLOT = memo
            calls["n"] = 0
            DP.cover(units, list(jobs), budget)
            if memo:
                after = calls["n"]
            else:
                before = calls["n"]
    finally:
        DP.materialise = real
        DP.MEMOISE_SLOT = True

    assert after < before * 0.75, (
        f"the memo saved almost nothing: {before} tour rebuilds without it, {after} with "
        f"({after / max(before, 1):.0%}). A memo that never hits is not an optimisation.")
