"""ONE TEST PER CELL: every gated row, every day, ours against the tape.

This replaced a version that ran d0-d6 against Seb's tape with one test per DAY. Two things were
wrong with that, and both cost real time.

**It stopped at d6.** The agent plays all 30 days off the schedule, and the days actually losing are
d6-d13 -- `water 17/33` on d8, melon short on every day from d6, `plant 6/9` on d8. A gate that stops
at d6 cannot see any of it.

**One test per day names the day, not the defect.** A day failed as
`test_the_day_matches_the_tape[8]` with twelve rows inside the assertion message, so the report said
"d8 is broken" and the broken cell had to be read out of a string. One test per (day, row) fails as
`test_the_row_matches_the_tape[water-8]` -- the name of the actual defect -- and a fresh regression
on one row cannot hide inside a day that was already red.

## What gates, and what cannot

The tape column is NOT the tape's own game. `breakdown.run` replays the recorded actions against
**us**, and both seats sell into one shared market inventory, so four quantities are ours-dependent
by construction and cannot be held to equality however good the agent gets:

    money              the replayed tape's bank parts from its real one at d4: it buys a parcel on
                       $718 in its own game and is REFUSED at $683 against us
    SELL, BUY_PRODUCT  one book, drained per unit in lockstep between the seats
                       (`_process_market`), so any day we both sell the same product has
                       ours-dependent fills on BOTH sides
    owned              inherits the money problem the day a land purchase is refused

Those four are `xfail(strict=False)`: they run, they are reported, they never gate. Everything else
is exact, with no tolerance -- not even a dollar, and never a threshold added to make this pass.

`PICKUP`, `DROP` and `PASS` are absent because they are tour SHAPE: one hand carrying four wheat and
another carrying one is the same four feeds. `PASS` is the residual of everything else and would fail
a second time for a cause already counted.

`BUY_SEED`, `BUY_ANIMAL`, `BUY_LAND` and `HIRE` DO gate. They are spent from our own bank on a turn
we choose, so a mismatch is ours.

    python -u -m pytest tests/test_each_day_matches_the_tape.py -q
"""
import importlib
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

SEED = 11
#: **The ladder value, not zero.** `_spawn_weeds` fires on empty ground at 0.005 in a real game, so
#: a grid run at 0.0 is a different board and hides every DIG the tape has to make.
WEEDS = 0.005
DAYS = 30
TAPE = "kawashigi"
MODULE = "kagg.search.schedule_agent"

#: Ops the day emits. Tour shape is deliberately absent -- see the module docstring.
GATED_OPS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "DIG",
             "BUILD_PASTURE", "BUILD_COOP", "PLACE", "FERTILIZE",
             "BUY_SEED", "BUY_ANIMAL", "BUY_LAND", "HIRE")

#: Dusk board rows that are ours alone.
GATED_BOARD = ("pen", "weed", "hands",
               "crop_WHEAT", "crop_MELON", "crop_STRAWBERRY", "crop_TOMATO", "crop_CARROT",
               "an_COW", "an_SHEEP", "an_GOOSE")

#: Reported, never gating. The reason for each is in the module docstring, and none of them is
#: "it was inconvenient".
CONTAMINATED = ("money", "owned", "SELL", "BUY_PRODUCT")


class _WhichTape(dict):
    """An opening that records the day it was consulted on.

    `replayed` picks its opening per turn off the two latches and then asks `step not in opening`,
    so `__contains__` fires exactly once per turn on exactly the tape that governs that turn. That
    is the only place the choice is observable from outside, and reading it needs no change to the
    agent.
    """

    def __init__(self, opening, tape, log):
        super().__init__(opening)
        self._tape, self._log = tape, log

    def __contains__(self, step):
        self._log[int(step) // 24] = self._tape
        return super().__contains__(step)


@pytest.fixture(scope="session")
def season():
    """`(ours, tape-per-day)` for all `DAYS`, played ONCE for the whole session.

    **The tape column is per DAY, because the agent changes recording mid-season.** It opens on
    `REPLAY_OPENING_TAPE[(False, False)]`, and `melon_branch` at d3 and `q4_branch` at d5 each swap
    it for a different カワシギ game. Held to one recording for all 30 days this gate was 285 cells
    red from `BUY_SEED-5` on -- red by construction, against an agent whose job is to leave that
    recording. It measured nothing and nobody read it.

    So the tape side is played once per recording the agent actually armed, against the SAME
    opponent, and each day is compared to the one that governed it. What that gates is the thing
    that ships: is the replay faithful to the recording it chose.

    Session-scoped deliberately: every assertion below is arithmetic on a table already computed,
    and paying for a 720-turn season per test id would make the gate too slow to keep, which is how
    a gate stops being run.
    """
    import breakdown as B

    replay, schedule, team = B.TAPES[TAPE]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA = importlib.import_module(MODULE)

    # `run` needs one day beyond the last compared: column d is the board at the END of day d.
    horizon = DAYS + 1
    # **One opponent for every run.** The tape side varies only in which カワシギ recording sits in
    # seat 0; seat 1 stays the opponent our own run faced, or the comparison moves two things.
    opp = lambda: B.tape_policy(str(REPO / replay), team, 1)      # noqa: E731

    armed = {}
    plain = SA._replay_opening
    SA._replay_opening = lambda days, tape=None, team=None: _WhichTape(
        plain(days, tape, team), tape, armed)
    try:
        def ours():
            a = SA.make_agent(sched, 0)
            return lambda o, t: a(o)

        # `run` returns FOUR things -- `days[1:], ops, cash, days[0]`. The cash ledger and the dawn
        # snapshot are not read here; unpacking only two is a ValueError, which is how this arrived.
        a_days, a_ops, _a_cash, _a_dawn = B.run(ours, opp, SEED, WEEDS, stop_day=horizon)
    finally:
        SA._replay_opening = plain

    assert armed, ("no opening was consulted: the agent never replayed, so this gate is comparing "
                   "a planner against a tape and would be red by construction")

    columns = {}
    for tape in dict.fromkeys(armed.values()):
        seat0 = lambda t=tape: B.tape_policy(str(REPO / t), team, 0)   # noqa: E731
        b_days, b_ops, _b_cash, _b_dawn = B.run(seat0, opp, SEED, WEEDS, stop_day=horizon)
        columns[tape] = (b_days, b_ops)

    # A day with no recorded arming is one the replay did not cover; fall back to the opening tape
    # so the cell still gates rather than disappearing.
    opening_tape = SA.REPLAY_OPENING_TAPE[(False, False)][0]
    per_day = {d: armed.get(d, opening_tape) for d in range(DAYS)}
    return (a_days, a_ops), columns, per_day


def _cell(measured, day, row):
    """`(ours, tape)` for one cell, against the recording that governed THAT day.

    Ops live in the op counters, board rows in the day snapshots.
    """
    (a_days, a_ops), columns, per_day = measured
    b_days, b_ops = columns[per_day[day]]
    if row.isupper():
        return a_ops[day][row], b_ops[day][row]
    return a_days[day].get(row, 0), b_days[day].get(row, 0)


@pytest.mark.parametrize("day", range(DAYS))
@pytest.mark.parametrize("row", GATED_OPS + GATED_BOARD)
def test_the_row_matches_the_tape(season, day, row):
    """Exact, no tolerance.

    Days match IN ORDER -- every later day inherits this one's board and bank -- so fix the lowest
    failing day first and ignore the rest until it is green. A change that fixes d8 and breaks d4 is
    a regression however good the week looks.
    """
    ours, tape = _cell(season, day, row)
    assert ours == tape, f"d{day} {row}: ours {ours} / tape {tape}"


@pytest.mark.parametrize("day", range(DAYS))
@pytest.mark.parametrize("row", CONTAMINATED)
def test_the_contested_row_matches_too(season, day, row):
    """**These four gate now.** They were `xfail(strict=False)` for a reason that expired.

    The reason was real while the tape column was one fixed recording: two different seats drained
    one shared market book, so money, `owned`, SELL and BUY_PRODUCT were ours-dependent and could
    not be held to equality. Comparing a replay against the recording it is replaying, both seats
    post the same orders in the same slots on the same turns, so the book drains identically and
    the four are exact -- all 120 cells xpassed the moment the fixture was repointed.

    A marker that says "expected to fail" on a test that always passes is worth nothing. If the
    replay ever stops being faithful these are the first rows to show it, because a dropped order
    moves money before it moves an op count.
    """
    ours, tape = _cell(season, day, row)
    assert ours == tape, f"d{day} {row}: ours {ours} / tape {tape}"
