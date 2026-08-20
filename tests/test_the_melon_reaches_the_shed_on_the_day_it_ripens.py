"""Melon harvested on day 10 must reach the shed on day 10, not on the overnight sweep.

The harvest itself is not the defect. All thirteen ripe melon tiles get a `HARVEST` job on d10 and
all thirteen are seated -- 65 of the 67 units on the board. What no tour has is a **shed stop**:

    u0   16/24  (3,2)W (3,1)WH (2,1)WH (1,1)WH (1,0)WH        ends at (1,0)
    u8   23/23  (2,4)FCC (0,3)WH (0,2)WH (0,1)WH (0,0)WHPW    ends at (0,0)
    u10  23/23  (4,3)FCCH (4,2)FCC (4,1)PW (4,0)WH (3,0)WH (2,0)WH
    u3    0/23  (idle)
    u6    0/23  (idle)

Three hands carry sixty-five melons to dusk while two hands sit on 46 unused turns. The melon is
banked by `_drop_inventories_to_shed` (`reference/kaggriculture.py:812`) at the day rollover, which
is **after the market has closed for day 10**. Traced on seed 11 against the kawashigi tape:

    d10 h00-h23   shed 0 all day, hands 0 -> 66, book 272 -> 246, no SELL offered
    d11 h00       shed 72, SELL 60 at 246, then SELL 12 at 189

`DELIVER_CUTOFF_TURNS = 99` is what makes the closing walk unreachable: `_solve` sets
`deliver = max(budget) > DELIVER_CUTOFF_TURNS` against budgets of 23-24, so `plan` never even tries
to append it. That constant was measured on the **victor** grid and its stated reason is that "the
overnight sweep banks the produce anyway, which is free". That is true of money at season end and
false of melon on d10: no shop stocks melon, the town takes one unit a day, and the opponent is
selling his own flush into the same book. A day's delay is the whole prize.

This pins the behaviour, not the constant: melon that our own hands harvested on the flush day must
be offerable that day. It is scoped to d10-d11 and says nothing about any other day, so the matched
d0-d8 opening is out of reach by construction.
"""
import importlib

import pytest

A = importlib.import_module("kagg.search.schedule_agent")
B = importlib.import_module("scripts.breakdown")
PLAN = importlib.import_module("kagg.plan")

#: The melon flush. `first_yield_day` puts the crop on the board at d10 and the tail lands d11.
FLUSH = (10, 11)


@pytest.fixture(scope="module")
def melon():
    """Hour by hour over the flush: our shed, our hands, and the MELON SELL we offered."""
    from kaggle_environments import make

    B.schedule_agent = A
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = PLAN.load(schedule)
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)
    opp = B.tape_policy(replay, team, 1)

    rows = []
    for t in range((max(FLUSH) + 1) * 24):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0 = me(o0, t)
        priv = o0.get("private") or {}
        rows.append(dict(
            day=t // 24, hour=t % 24,
            shed=int((priv.get("shed") or {}).get("MELON", 0) or 0),
            hands=sum(int((i or {}).get("MELON", 0) or 0)
                      for i in (priv.get("inventories") or [])),
            sold=sum(int(o[2]) for o in (a0.get("market") or [])
                     if o and len(o) > 2 and o[0] == "SELL" and o[1] == "MELON"),
        ))
        env.step([a0, opp(o1, t)])
        if env.done:
            break
    return rows


def test_the_hands_do_fill_with_melon_on_the_flush_day(melon):
    """The premise. If the melon never reaches a hand, this is a harvest defect and not a delivery
    one, and the fix below would be aimed at the wrong half."""
    peak = max((r["hands"] for r in melon if r["day"] == 10), default=0)
    assert peak >= 40, f"only {peak} melon ever reached our hands on d10; this is not a delivery bug"


def test_most_of_the_days_harvest_clears_the_same_day(melon):
    """The defect: a whole day's harvest banked by the overnight sweep, after the market shut.

    **Measured as a FLOW, not as a shed level.** The first version of this assertion required the
    shed to rise above 0 during the day and stayed red after the fix, because a hand deposits and
    the market sells inside the SAME turn -- the unit phase runs before `_process_market`
    (`kaggriculture.py:922` then `:928`) -- so the shed observation never samples it. That is the
    trap `breakdown.py`'s own header states: a shed level is one sample of a flow and lies about it.
    Read what was offered.
    """
    for day in FLUSH:
        hands = max((r["hands"] for r in melon if r["day"] == day), default=0)
        if hands < 20:
            continue                      # nothing worth delivering that day
        sold = sum(r["sold"] for r in melon if r["day"] == day)
        assert sold >= hands // 2, (
            f"day {day}: up to {hands} melon passed through our hands and only {sold} were offered "
            f"that day -- the rest waited for the overnight sweep, after the market closed")


def test_a_melon_is_offered_on_the_day_it_is_harvested(melon):
    """The consequence. Melon has no shop and the town takes one a day, so the book does not
    recover; a day late is a day of the opponent's flush walking the price down ahead of us."""
    sold = {d: sum(r["sold"] for r in melon if r["day"] == d) for d in FLUSH}
    assert sold[10] > 0, (
        f"nothing was offered on d10 at all; the whole flush waited for d11 (offered {sold[11]})")
