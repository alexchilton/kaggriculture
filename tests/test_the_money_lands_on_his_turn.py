"""The second acceptance gate: every purchase lands on the TURN the tape makes it, not just the day.

`test_each_day_matches_the_tape.py` counts what a day did. This counts WHEN. They are different
measurements and only the second one can see the defect that actually costs us the opening.

## Why the hour is its own gate

d8, ours against the tape, from the per-day grid:

    hands   9 / 11        unit-turns  231 / 267        idle  100 / 36

Both sides hire. He hires ten hands at h1-h2 off a five dollar bank; we reach nine, later, and open
the day on $4. The day-count gate sees `HIRE 9 / 11` and calls it one missing pair of hands. What
actually happened is a cadence failure with two mechanisms behind it, neither visible in a count:

  * `HIRE` costs `mult * fib(hires_today)` on a per-DAY counter (`_do_hire`), so ten hires bought in
    one turn cost what ten hires cost -- his eleven cost $232 against our nine at $88 -- and the
    price does not depend on the hour.
  * `_do_hire` fails SILENTLY on a thin bank. The bank is what gates it, and the SELL that funds the
    hire settles in the same `_process_market` call, in ORDER SLOT sequence. So a SELL queued in an
    earlier slot of the same turn pays for the HIRE behind it. That is how a $5 bank hires ten hands.

A gate that only counts per day cannot distinguish "we could not afford it" from "we asked eight
hours too late", and those need opposite fixes.

## What gates and what does not

    BUY_LAND, HIRE, BUY_ANIMAL, BUY_SEED    gate on the turn. Spent from OUR bank on a turn WE
                                            choose, so a mismatch is ours.
    SELL                                    reported, never gating on the fill turn. One shared
                                            market book, drained per unit in lockstep between the
                                            seats, so WHEN a sell fills is partly the opponent's
                                            doing. What is ours is the hour we OFFER, which is a
                                            different measurement and is not read from fills.

Read off `fills.events`, which records `(seat, op, item, price, day, hour)` per unit at the moment
`_commit_unit` succeeds. **Never off the action stream** -- the agent re-posts every order on all 24
turns of a day, so an emitted order counted as an event inflates by up to 24x. That mistake has been
made three separate ways in this project; see the docstring of `kagg/analysis/fills.py`.

    python -u -m pytest tests/test_the_money_lands_on_his_turn.py -q
"""
import collections
import importlib
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

SEED = 11
WEEDS = 0.005
DAYS = 30
TAPE = "kawashigi"
MODULE = "kagg.search.schedule_agent"

#: Spent from our own bank on a turn we choose. These gate.
OURS_TO_TIME = ("BUY_LAND", "HIRE", "BUY_ANIMAL", "BUY_SEED")

#: Reported, never gating -- the fill turn is partly the opponent's doing. See the docstring.
CONTESTED = ("SELL",)


def _cadence(events, seat):
    """`day -> op -> sorted list of hours`, one entry per unit that actually traded."""
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for e in events:
        if e["seat"] != seat:
            continue
        out[e["day"]][e["op"]].append(e["hour"])
    for day in out:
        for op in out[day]:
            out[day][op].sort()
    return out


@pytest.fixture(scope="session")
def cadence():
    """`(ours, tape)` cadence tables, each `day -> op -> [hours]`.

    Two separate seasons, as in the day gate: ours against the tape's recorded actions, then the
    tape against the same, so both columns are measured in the same contested market rather than
    one being read out of the original replay where the opponent was somebody else.
    """
    import breakdown as B

    replay, schedule, team = B.TAPES[TAPE]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA = importlib.import_module(MODULE)
    horizon = DAYS + 1
    opp = lambda: B.tape_policy(str(REPO / replay), team, 1)      # noqa: E731

    def ours():
        a = SA.make_agent(sched, 0)
        return lambda o, t: a(o)

    B.run(ours, opp, SEED, WEEDS, stop_day=horizon)
    mine = _cadence(B.LAST_FILLS.events, 0)

    B.run(lambda: B.tape_policy(str(REPO / replay), team, 0), opp, SEED, WEEDS, stop_day=horizon)
    theirs = _cadence(B.LAST_FILLS.events, 0)
    return mine, theirs


@pytest.mark.parametrize("day", range(DAYS))
@pytest.mark.parametrize("op", OURS_TO_TIME)
def test_the_purchase_lands_on_his_turn(cadence, day, op):
    """Same count AND same hours. A day that buys the same things later is a different day."""
    mine, theirs = cadence
    ours = mine[day][op]
    tape = theirs[day][op]
    assert ours == tape, (
        f"d{day} {op}: ours h{ours} / tape h{tape}"
        + (f"  -- {len(ours)} vs {len(tape)} units" if len(ours) != len(tape) else "")
        + "\n    HIRE is mult*fib(hires_today) on a per-DAY counter and fails silently on a thin "
          "bank; the SELL that funds it settles in the same turn, in order-slot sequence.")


@pytest.mark.xfail(strict=False,
                   reason="one shared market book drained in lockstep between the seats, so the "
                          "turn a SELL FILLS is partly the opponent's doing. Reported so a change "
                          "stays visible, never gating.")
@pytest.mark.parametrize("day", range(DAYS))
@pytest.mark.parametrize("op", CONTESTED)
def test_the_contested_fill_turn_is_reported(cadence, day, op):
    mine, theirs = cadence
    assert mine[day][op] == theirs[day][op], (
        f"d{day} {op}: ours h{mine[day][op]} / tape h{theirs[day][op]}")


def test_the_events_are_fills_and_not_offers(cadence):
    """A guard on the instrument itself.

    The agent re-posts every order on all 24 turns of a day. If `events` were ever fed from the
    action stream instead of `_commit_unit`, counts would inflate toward a multiple of 24 and every
    assertion above would fail for a reason that has nothing to do with the agent. A day cannot buy
    more land than there are quadrants, and that is cheap to assert.
    """
    mine, _theirs = cadence
    for day in range(DAYS):
        assert len(mine[day]["BUY_LAND"]) <= 3, (
            f"d{day} recorded {len(mine[day]['BUY_LAND'])} BUY_LAND fills; there are only three "
            f"quadrants to buy. events is counting offers, not fills.")
