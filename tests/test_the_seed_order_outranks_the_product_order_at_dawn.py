"""d0 h0: the whole `buys` row fires in one turn and strands the bank for the rest of the day.

Found 2026-08-21 by handing the executor Kawashigi's OWN d0-d12 rows from game 92498144 and grading
the result op for op (`scripts/can_the_executor_play_his_own_row.py`). It is BRANCH B: the executor
does not reproduce a row it was handed, and it misses from the very first day.

The hour-by-hour trace (`scripts/what_the_day_did_hour_by_hour.py --day 0`):

    h0   ours  $3000 -> BUY_PRODUCT WHEAT x9 + five HIREs
         tape  $3000 -> five HIREs + all nineteen seeds
    h1   ours  $7    -> SELL WHEAT x3, BUY_SEED MELON x1, BUY_SEED WHEAT x1
         tape  $13   -> SELL WHEAT x3
    h2   ours  $6                        tape  $100
    ...
    h23  ours  $6                        tape  $16

    From h2 to h23 -- TWENTY-TWO CONSECUTIVE TURNS -- we emit `BUY_SEED WHEAT x1` and it never
    fills, because a WHEAT seed costs $10 and the bank holds $6.

The row's `buys` is a DAY TOTAL with no cadence in it. A target row has no hours, so the executor
picks the turn, and it picks the first one -- putting a $9-unit product order in front of the seed
the ground is waiting for. Kawashigi buys his seed at h0 and spreads the product over h6 and h12.

The day ends one plant short (18 against 19) and the bank never recovers: d6 $16 against $957, d8
crew 3 against 11, d10 crew 5 against 11 with `water 3/32`, and thirteen weeds by d11 against his
zero.

**This is the same failure family `schedule_agent.py:4860` already documents**, where BUY_ANIMAL
outranked BUY_SEED and `SEED_BEFORE_LIVESTOCK` was the answer: "A BUY_SEED fills only what the bank
covers ... it says the seed is due first on the day the ground is waiting for it." Same argument,
different competitor for the same dollars -- BUY_PRODUCT this time.

FIXED 2026-08-21 in `schedule_agent._wheat_row_first`: the wheat product order is still moved ahead
of HIRE and BUY_ANIMAL, but never ahead of a BUY_SEED in the same turn. Days with no seed order that
turn are untouched, so the Victor measurement in that function's own docstring still holds.
"""

import pathlib

import pytest

from kagg.search import kawa_rows

GAME = "92498144"
WHEAT_SEED_COST = 10


@pytest.fixture(scope="module")
def his_d0():
    if not kawa_rows.LIBRARY.exists():
        pytest.skip("row library %s is not on disk (data/ is gitignored)" % kawa_rows.LIBRARY)
    return kawa_rows.build(opening_from=GAME)[0]


def test_the_row_we_are_handed_asks_for_nineteen_plants(his_d0):
    """Not the defect -- the premise. If this changes, the numbers below describe another day."""
    assert len(his_d0.get("plants") or []) == 19
    assert (his_d0.get("seeds") or {}) == {"MELON": 12, "WHEAT": 7}
    assert (his_d0.get("buys") or {}) == {"WHEAT": 9}


def test_the_day_can_afford_the_seed_the_row_asks_for(his_d0):
    """The theory, as an arithmetic claim about one turn.

    A day that spends its opening bank on the product order cannot pay for its own seed row. The
    executor has $3,000, the row's seeds cost $1,030 and its product order takes the rest; whichever
    of the two goes first is the one that fills.
    """
    import scripts.breakdown as BD
    from kagg.search import kawa_library_agent

    BD.schedule_agent = BD.load_agent_module("schedule_agent")
    replay, _s, team = BD.TAPES["kawashigi"]
    economy, shops = BD.env_config(replay), BD.recorded_shops(replay)

    def mine():
        agent = kawa_library_agent.make_agent(None, 0, router=True, opening_from=GAME)
        return lambda o, t: agent(o)

    ours, our_ops, _c, _d = BD.run(mine, lambda: BD.tape_policy(replay, team, 1), 11, 0.0,
                                   stop_day=1, economy=economy, shops=shops)
    # Every seed the row orders must land. `buy_seed` here is a FILL, from `kagg/analysis/fills.py`,
    # not the count of orders emitted -- the agent re-posts an unfilled order every turn.
    wanted = sum((his_d0.get("seeds") or {}).values())
    assert our_ops[0]["BUY_SEED"] == wanted, (
        "the row orders %d seeds and only %d filled; the day ends holding $%d"
        % (wanted, our_ops[0]["BUY_SEED"], ours[0]["money"]))
