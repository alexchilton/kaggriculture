"""A recorded fill must be a MOVEMENT OF GOODS, not a call that returned True.

Alex has now rejected the wheat round-trip figure five times, across three different instruments.
Each previous time the instrument was inferring from a proxy and he was right. This time the
instrument claims to read `_commit_unit`'s own return value, which should be ground truth -- so
either the number is real or `_commit_unit` returning True does not mean what `record_fills`
assumes it means.

That is the question, and it is answerable rather than arguable: wrap the commit, read
`private["shed"][item]` immediately before and immediately after the underlying call, and require
the recorded fill to match the observed delta. A SELL must take one unit OUT, a BUY_PRODUCT must put
one unit IN. Anything the instrument counts that did not move goods is an attempt, and this test
names it as one.

This deliberately does NOT trust `ok`. `ok` is what is under suspicion.
"""

import collections
import json
import pathlib

import pytest

SCHED = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
TAPE = pathlib.Path("data/seed_scripts/top_guys/90976060.json")
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")

pytestmark = pytest.mark.skipif(not SCHED.exists(), reason="gitignored data")


def _observed(days=30, seed=11):
    """Play a season, recording for every `_commit_unit` call what actually moved.

    Returns `(claimed, moved, mismatches)`:
      claimed  -- (op, item) -> calls that returned True, i.e. what `record_fills` would count
      moved    -- (op, item) -> calls where the shed genuinely changed by one unit
      mismatch -- list of (op, item, ok, before, after) where the two disagree
    """
    import kaggle_environments.envs.kaggriculture.kaggriculture as kg
    from kaggle_environments import make

    from kagg.arena.tape import build_tape_agent
    from kagg.search import schedule_agent as SA

    sched = {int(k): v for k, v in json.loads(SCHED.read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    claimed = collections.Counter()
    moved = collections.Counter()
    mismatch = []
    original = kg._commit_unit

    def wrapped(op, item, price, farm, private, market, *a, **kw):
        before = dict(private.get("shed") or {}).get(item, 0)
        ok = original(op, item, price, farm, private, market, *a, **kw)
        after = dict(private.get("shed") or {}).get(item, 0)
        delta = after - before
        if ok:
            claimed[(op, item)] += 1
        want = {"SELL": -1, "BUY_PRODUCT": 1}.get(op)
        if want is not None:
            if delta == want:
                moved[(op, item)] += 1
            if bool(ok) != (delta == want):
                mismatch.append((op, item, bool(ok), before, after))
        return ok

    kg._commit_unit = wrapped
    try:
        ours = SA.make_agent(thin, 0, router=True)
        rival = build_tape_agent(str(TAPE), 0)
        env = make("kaggriculture", configuration={"seed": seed}, debug=False)
        env.reset(2)
        for t in range(24 * days):
            if env.done:
                break
            o0 = env.state[0].observation
            a0 = ours(o0)
            a1 = rival(env.state[1].observation)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        kg._commit_unit = original
    return claimed, moved, mismatch


@pytest.mark.slow
def test_a_true_return_always_moved_a_unit_of_goods():
    """If this fails, `record_fills` is counting attempts and every number quoted from it is wrong."""
    claimed, moved, mismatch = _observed()
    assert not mismatch, (
        f"{len(mismatch)} calls where the return value and the shed disagree; "
        f"first five: {mismatch[:5]}")


@pytest.mark.slow
def test_the_wheat_round_trip_is_reported_at_its_true_size():
    """The specific disputed number, stated as goods that moved rather than calls that succeeded."""
    claimed, moved, _m = _observed()
    bought = moved[("BUY_PRODUCT", "WHEAT")]
    sold = moved[("SELL", "WHEAT")]
    print(f"\nWHEAT units that actually moved: bought {bought}, sold {sold}")
    print(f"WHEAT calls that returned True : bought {claimed[('BUY_PRODUCT', 'WHEAT')]}, "
          f"sold {claimed[('SELL', 'WHEAT')]}")
    assert bought == claimed[("BUY_PRODUCT", "WHEAT")]
    assert sold == claimed[("SELL", "WHEAT")]
