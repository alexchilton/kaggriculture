"""Melon in the shed is sold now, not at h16, from the day the first flush lands.

`LATE_SELL_BIAS` holds every sale until `LATE_SELL_FROM_HOUR = 16` on the argument in its own
docstring: the price "recovers as the shops restock every 4 steps". That is true of every product a
shop eats and **false of MELON**, which appears in no `SHOPS` entry at all -- its only drain is the
town centre at one unit a day. So the hold waits sixteen hours for a recovery of one unit while the
opponent walks the book down.

`SELL_A_DRAINLESS_PRODUCT_AT_ONCE` already exempts `NO_DRAIN_PRODUCTS` from that hold. It was gated
at `SELL_AT_ONCE_FROM_DAY = 18` on the reasoning that "the first flush already sells well ... and
there is nothing to win before d18". Traced on seed 11 against Kawashigi's tape, that is not what
happens:

    t    d   h | ripe tiles  units on tiles  shed MEL  hands MEL | our SELL
    240  10  0 |         19              67         0          0 | []
    258  10 18 |          7               7         0         67 | []
    263  10 23 |          7               7        24         37 | SELL 24
    264  11  0 |          7               7        37          0 | []
    280  11 16 |          7               7        37          0 | SELL 37

Sixty-seven melons are ripe at d10 h00 -- more than the tape's sixty. They reach the shed at h21-h23,
so only 35 clear that day, and the remaining **37 sit in the shed from d11 h00 to d11 h16** doing
nothing. Melon recovers one unit a day, so every one of those sixteen hours makes the book strictly
worse, and the tape sells his own d11 melon into it meanwhile.

The flush is d10-d11 and the gate is d18, so the exemption cannot reach the days it was written for.

This test pins the behaviour, not the constant: it asserts a melon sale is offered before
`LATE_SELL_FROM_HOUR` on the day the shed is holding melon. `day >= SELL_AT_ONCE_FROM_DAY` means
nothing at or before d9 can move, so d0-d8 is out of reach by construction -- verified separately on
the per-day grid.
"""
import collections
import importlib

import pytest

A = importlib.import_module("kagg.search.schedule_agent")
B = importlib.import_module("scripts.breakdown")
PLAN = importlib.import_module("kagg.plan")


@pytest.fixture(scope="module")
def trace():
    """Play our agent against the tape to d12, recording melon shed level and melon SELLs."""
    from kaggle_environments import make
    B.schedule_agent = A
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = PLAN.load(schedule)
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)
    opp = B.tape_policy(replay, team, 1)
    rows = []
    for t in range(12 * 24):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0 = me(o0, t)
        priv = o0.get("private") or {}
        rows.append(dict(
            day=t // 24, hour=t % 24,
            shed=int((priv.get("shed") or {}).get("MELON", 0) or 0),
            sold=sum(int(o[2]) for o in (a0.get("market") or [])
                     if o and o[0] == "SELL" and o[1] == "MELON" and len(o) > 2),
        ))
        env.step([a0, opp(o1, t)])
        if env.done:
            break
    return rows


def test_melon_is_a_drainless_product(trace):
    """The premise. If a shop ever stocks melon this whole rule is wrong."""
    import reference.kaggriculture as kg
    assert not any("MELON" in prods for prods in kg.SHOPS.values()), kg.SHOPS
    assert "MELON" in A.NO_DRAIN_PRODUCTS


def test_the_shed_does_not_sit_on_melon_all_morning(trace):
    """The defect: melon held in the shed across the whole pre-h16 window on the flush days."""
    worst = None
    for day in (10, 11):
        held = [r for r in trace if r["day"] == day and r["hour"] < A.LATE_SELL_FROM_HOUR
                and r["shed"] > 0]
        if not held:
            continue
        sold = sum(r["sold"] for r in held)
        if sold == 0:
            worst = (day, len(held), max(r["shed"] for r in held))
    assert worst is None, (
        f"day {worst[0]}: melon sat in the shed for {worst[1]} turns before "
        f"h{A.LATE_SELL_FROM_HOUR} with up to {worst[2]} units, and none was offered")


def test_the_gate_can_reach_the_flush(trace):
    """A gate later than the flush is unreachable by construction -- the failure that hid this.

    Scoped deliberately to the flush days alone. The exemption is NOT extended across d12-d17:
    those days keep the `LATE_SELL_FROM_HOUR` hold, because nothing has measured them and the
    original "nothing to win before d18" reasoning still stands everywhere the flush is not.
    """
    flush = sorted({r["day"] for r in trace if r["shed"] >= 20})
    assert flush, "no melon flush found at all -- the fixture is wrong, not the agent"
    exempt = set(getattr(A, "SELL_AT_ONCE_DAYS", ())) | set(range(A.SELL_AT_ONCE_FROM_DAY, 30))
    missed = [d for d in flush if d not in exempt]
    assert not missed, (
        f"melon fills the shed on days {flush} but the exemption covers {sorted(exempt)[:6]}..., "
        f"so it can never fire on {missed}")
