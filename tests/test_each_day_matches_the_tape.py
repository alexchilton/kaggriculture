"""One test per day: d0 through d6, ours against Seb's tape, op for op.

**Why per day and not one test for the week.** A week total hides a trade: day 0 gaining two feeds
while day 6 loses two sells nets to zero and reads as "no change". Days also compound -- a pen not
built on day 0 is an animal not producing for the rest of the season -- so the rule is that days
match IN ORDER, and a regression on d0 must not be payable out of d6. Separate test ids make that
visible in the report instead of in a total.

Driven by `scripts/breakdown.run`, the same function behind
`scripts/breakdown.py --module schedule_agent_1455mh --days 7`, so this file and that table cannot
disagree about what was measured. Market rows there are EXACT FILLS read per unit from
`_commit_unit` via `kagg/analysis/fills.py` -- never offers, which the agent re-posts every turn.

Exempt rows, and why each is exempt rather than merely inconvenient:

    PICKUP / DROP   tour SHAPE. One hand carrying four wheat and another carrying one is the same
                    four feeds. The ops those trips serve are not exempt and are checked here.
    PASS            the residual of everything else, so it fails twice for one cause.
    the compass     we work the board westward and the tape southward. Not a defect, and nothing
                    downstream reads it.

Every other op the day emits is checked, plus the board at dusk: money, tiles owned, pens, standing
crops and the herd.
"""
import collections
import importlib
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

SEED = 11
WEEDS = 0.0
DAYS = 7
MODULE = "kagg.search.schedule_agent_1455mh"
PLAN = "90494364"

#: Tour shape, not work. See the module docstring.
EXEMPT = ("PICKUP", "DROP", "PASS")

#: Ops the day emits, in the order the table prints them.
CHECKED = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "DIG",
           "BUILD_PASTURE", "BUILD_COOP", "PLACE", "FERTILIZE",
           "SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "BUY_LAND", "HIRE")

#: Dusk board rows. `money` is the one every later day inherits.
BOARD = ("money", "owned", "pen", "weed",
         "crop_WHEAT", "crop_MELON", "crop_STRAWBERRY", "crop_TOMATO", "crop_CARROT",
         "an_COW", "an_SHEEP", "an_GOOSE")


@pytest.fixture(scope="module")
def measured():
    """`(ours, tape)` -- each a list of `(board, ops)` per day, straight from `breakdown.run`."""
    import json

    import breakdown as B

    replay, schedule, team = B.TAPES["seb"]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA = importlib.import_module(MODULE)

    # `run` needs one day beyond the last day compared: column d is the board at the END of day d.
    horizon = DAYS + 1
    opp = lambda: B.tape_policy(str(REPO / replay), team, 1)      # noqa: E731

    def ours():
        a = SA.make_agent(sched, 0, router=True)
        return lambda o, t: a(o)

    a_days, a_ops, _a_cash, _a_dawn = B.run(ours, opp, SEED, WEEDS, stop_day=horizon)
    b_days, b_ops, _b_cash, _b_dawn = B.run(
        lambda: B.tape_policy(str(REPO / replay), team, 0), opp, SEED, WEEDS, stop_day=horizon)
    return (a_days, a_ops), (b_days, b_ops)


@pytest.mark.parametrize("day", range(DAYS))
def test_the_day_matches_the_tape(measured, day):
    (a_days, a_ops), (b_days, b_ops) = measured
    bad = []

    for op in CHECKED:
        if op in EXEMPT:
            continue
        got, want = a_ops[day][op], b_ops[day][op]
        if got != want:
            bad.append(f"    {op.lower():22s} {got:>5} / {want:<5}")

    for row in BOARD:
        got, want = a_days[day].get(row, 0), b_days[day].get(row, 0)
        # **Exact, and no tolerance -- not even a dollar.** d2 reading 657 against 659 is a
        # difference, and a rule that calls it identical would also swallow the $295 fertilizer
        # shortfall that produced it before the delivery fix. A bank gap is never local either: it
        # decides whether the next day's land, animal or seed clears at all.
        if got != want:
            bad.append(f"    {row:22s} {got:>5} / {want:<5}")

    assert not bad, (
        f"day {day} does not match the tape (ours / tape):\n" + "\n".join(bad)
        + f"\n\n  Reproduce: python -u scripts/breakdown.py --module {MODULE.rsplit('.', 1)[-1]}"
          f" --days {DAYS}\n"
          "  Days match IN ORDER: an earlier day's failure is the one to fix, because every later\n"
          "  day inherits its board and its bank."
    )
