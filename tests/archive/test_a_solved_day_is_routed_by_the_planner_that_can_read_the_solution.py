"""A day with a precomputed route must be routed by the planner that knows how to read it.

`cover.plan` picks its router per day (`cover.py:1661`):

    assign = (CREW.cover if day is not None and day < CREW.ACTIVE_UNTIL_DAY else cover)

`crew.ACTIVE_UNTIL_DAY` is 8, so d0-d7 go to `crew.cover`. `PRECOMPUTED_ROUTES` is read only inside
`cover.cover` -- `crew.py` does not contain the name at all. So a route solved for d6 today is
written into `solved_days.py`, loaded into `PRECOMPUTED_ROUTES`, and then never consulted, because
the planner that runs on d6 has no code to consult it.

That is a byte-identical null waiting to happen, and this repo has shipped three of them
(`CHAIN_OPS` under `COVER_PLANNER`, `SOLVED_DAYS` vs `PRECOMPUTED_ROUTES`, `RESERVATION_SLIP`).
The rule this pins is the general one, not d6: **whichever days are solved, those days route
through the planner that can read the solution.**

Inert until a day below `ACTIVE_UNTIL_DAY` is actually solved -- every current entry is d12+.
"""
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import cover as C      # noqa: E402
from kagg.search import crew as CREW    # noqa: E402


@pytest.fixture
def which_router(monkeypatch):
    """Record which of the two routers `cover.plan` chose, without running either."""
    called = []

    def fake(name):
        def f(units, jobs, budget, depots=None, carry=None, supply=None, deliver=True,
              wanted=None, day=None, rush=False, due=None):
            called.append(name)
            return {}, []
        return f

    monkeypatch.setattr(C, "cover", fake("cover"))
    monkeypatch.setattr(CREW, "cover", fake("crew"))
    return called


def test_the_premise_crew_owns_the_early_days(which_router):
    """Unsolved early days keep going to the crew planner. This must not change."""
    assert CREW.ACTIVE_UNTIL_DAY == 8
    C.plan([], [], [], day=6)
    assert which_router == ["crew"]


def test_the_premise_cover_owns_the_later_days(which_router):
    C.plan([], [], [], day=12)
    assert which_router == ["cover"]


def test_a_solved_early_day_routes_through_cover(monkeypatch, which_router):
    """The point. A solved d6 must reach the planner that reads `PRECOMPUTED_ROUTES`."""
    monkeypatch.setitem(C.PRECOMPUTED_ROUTES, 6, {})
    C.plan([], [], [], day=6)
    assert which_router == ["cover"], (
        "d6 has a precomputed route and was still routed by `crew.cover`, which cannot read one. "
        "Solving the day would produce a byte-identical null.")


def test_an_unsolved_early_day_is_untouched_by_the_change(monkeypatch, which_router):
    """Solving d6 must not drag d5 off the crew planner with it."""
    monkeypatch.setitem(C.PRECOMPUTED_ROUTES, 6, {})
    C.plan([], [], [], day=5)
    assert which_router == ["crew"]


def test_todays_solved_days_are_all_already_on_cover():
    """So the change is inert until a day below `ACTIVE_UNTIL_DAY` is solved."""
    early = [d for d in C.PRECOMPUTED_ROUTES if d < CREW.ACTIVE_UNTIL_DAY]
    assert early == [], f"days {early} are solved AND below the crew cutoff; this is no longer inert"
