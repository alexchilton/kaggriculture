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


@pytest.fixture(scope="session")
def season():
    """`(ours, tape)` for all `DAYS`, played ONCE for the whole session.

    Session-scoped deliberately: every assertion below is arithmetic on a table already computed,
    and paying for two 720-turn seasons per test id would make the gate too slow to keep, which is
    how a gate stops being run.
    """
    import breakdown as B

    replay, schedule, team = B.TAPES[TAPE]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA = importlib.import_module(MODULE)

    # `run` needs one day beyond the last compared: column d is the board at the END of day d.
    horizon = DAYS + 1
    opp = lambda: B.tape_policy(str(REPO / replay), team, 1)      # noqa: E731

    def ours():
        a = SA.make_agent(sched, 0)
        return lambda o, t: a(o)

    # `run` returns FOUR things -- `days[1:], ops, cash, days[0]`. The cash ledger and the dawn
    # snapshot are not read here; unpacking only two is a ValueError, which is how this arrived.
    a_days, a_ops, _a_cash, _a_dawn = B.run(ours, opp, SEED, WEEDS, stop_day=horizon)
    b_days, b_ops, _b_cash, _b_dawn = B.run(lambda: B.tape_policy(str(REPO / replay), team, 0), opp,
                                            SEED, WEEDS, stop_day=horizon)
    return (a_days, a_ops), (b_days, b_ops)


def _cell(measured, day, row):
    """`(ours, tape)` for one cell. Ops live in the op counters, board rows in the day snapshots."""
    (a_days, a_ops), (b_days, b_ops) = measured
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


@pytest.mark.xfail(strict=False,
                   reason="ours-dependent by construction: the tape is replayed against US and both "
                          "seats drain one shared market book. Reported so a change stays visible, "
                          "never gating. See the module docstring.")
@pytest.mark.parametrize("day", range(DAYS))
@pytest.mark.parametrize("row", CONTAMINATED)
def test_the_contaminated_row_is_reported(season, day, row):
    ours, tape = _cell(season, day, row)
    assert ours == tape, f"d{day} {row}: ours {ours} / tape {tape}"
