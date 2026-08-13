"""The grid must reconcile on its own terms, without a reader knowing which caveats to apply.

Alex's complaint, in his words: the columns match "if you ignore x, y, z". Two of them could not
be added up at all.

**The turn budget.** `work`, `idle` and `unit-turns` were printed and `move` was hidden behind
`--moves`, so three of the four terms of an identity were on the page and the fourth was not.
`--moves` exists to hide the four COMPASS rows, which are tour shape rather than a defect; hiding
the budget's `move` term is a different thing and left a block that does not sum.

**The cash.** Nothing tied the market rows to the money row. Every dollar a farm gains or loses
passes through `_commit_unit`, `_do_hire` or `_do_buy_land` -- there is no other path -- so with
fills carrying the price each unit actually fetched, `open + sold - product - seed - animal - hire
- land` IS the closing money, exactly. If it does not tie, a path is unwrapped and the grid is
lying about something; `breakdown.run` raises rather than printing a plausible number.

Both identities are checked here on a real pair of games rather than on the tape, because the tape
comparison needs downloaded recordings and these identities hold for any two agents.
"""

import sys

import pytest

sys.path.insert(0, ".")

pytest.importorskip("kaggle_environments")

DAYS = 3


def played():
    import importlib

    import scripts.breakdown as breakdown
    from kagg.agents import heuristic, rancher

    breakdown.schedule_agent = importlib.import_module("kagg.search.schedule_agent")
    return breakdown.run(heuristic.make_agent, lambda: (lambda o, t: rancher.agent(o)),
                         seed=11, weeds=0.0, stop_day=DAYS + 1)


def test_work_plus_move_plus_idle_is_every_unit_turn():
    """A unit that acted spent its turn walking, working or doing nothing. There is no fourth
    place for it to go, so the three add to `unit-turns` -- and an op the vocabulary does not know
    would break this rather than quietly inflating whichever row it fell into."""
    _days, ops, _cash, _dawn = played()
    for day in range(DAYS):
        counts = ops[day]
        assert counts["_work"] + counts["_move"] + counts["_pass"] == counts["_turns"], day
    assert sum(ops[d]["_turns"] for d in range(DAYS)), "nothing acted; this proved nothing"


def test_every_term_of_the_budget_identity_is_actually_printed():
    """The identity holding in the data is not the point -- it holds by construction. The defect
    was that `move` was hidden behind `--moves` while `work`, `idle` and `unit-turns` were shown,
    so the block on the page had three of four terms and could not be added up."""
    import scripts.breakdown as breakdown

    printed = {key for key, _label in breakdown.BUDGET_ROWS}
    assert printed == {"_turns", "_work", "_move", "_pass"}, (
        f"the budget block prints {sorted(printed)}; a reader cannot add that up")


def test_the_op_vocabulary_covers_every_op_the_env_can_execute():
    """`OTHER` is where an op the `OPS` tuple has not heard of lands, and a row nothing reaches is
    the wrong way to check that. `OPS` listed `"BUILD"`, which matches nothing -- the real ops are
    `BUILD_COOP` and `BUILD_PASTURE` -- so every build fell into the catch-all and was reported as
    a MOVE, and the routing argument rested on that row.

    So this reads the vocabulary off the env's own unit phase rather than off a game that happens
    to exercise it. A game only covers the ops its two agents chose to emit.
    """
    import pathlib
    import re

    import scripts.breakdown as breakdown

    source = pathlib.Path("reference/kaggriculture.py").read_text()
    body = source[source.index("def _apply_unit_action"):source.index("def _spawn_hand")]
    executable = set(re.findall(r'op == "([A-Z_]+)"', body))
    from reference.kaggriculture import FARMER_MOVES
    executable |= set(FARMER_MOVES)

    assert not executable - set(breakdown.OPS), (
        f"the env can execute {sorted(executable - set(breakdown.OPS))} and the grid would file "
        f"them under OTHER")


def test_no_op_falls_into_the_catch_all():
    """The same thing on a live game, which is the only place a malformed action can show up."""
    _days, ops, _cash, _dawn = played()
    assert not any(ops[d]["OTHER"] for d in range(DAYS))


def test_the_cash_column_closes_to_the_dollar():
    """open + sold - the five costs == close, per day, exactly."""
    import scripts.breakdown as breakdown

    days, _ops, cash, dawn = played()
    for day in range(DAYS):
        opened = dawn["money"] if day == 0 else days[day - 1]["money"]
        flow = cash.get(day, {}).get("SELL", 0) - sum(
            cash.get(day, {}).get(op, 0)
            for op in breakdown.MARKET_FILL_OPS if op != "SELL")
        assert round(opened + flow) == days[day]["money"], day


def test_hire_and_buy_land_are_in_the_fill_list_not_the_offer_list():
    """They are refused silently when the bank is short, so an emitted one is an offer. They were
    printed in the same table as the fills under a heading that called everything in it emitted."""
    import scripts.breakdown as breakdown

    assert "HIRE" in breakdown.MARKET_FILL_OPS
    assert "BUY_LAND" in breakdown.MARKET_FILL_OPS
    assert not set(breakdown.MARKET_FILL_OPS) & set(breakdown.OPS), (
        "an op cannot be both a unit op and a market fill; it would print in both blocks")
