"""`--module` defaulted to an agent four days out of date, and nothing said so.

`kagg/search/schedule_agent.py` was last touched on 2026-08-09 (`ea72a1e`). `schedule_agent_1455mh.py`
carries every commit since, including `c99a8a5`, "Three of the nine products could never be sold":

    schedule_agent          SELLABLE = MELON WOOL MILK STRAWBERRY FERTILIZER WHEAT
    schedule_agent_1455mh   SELLABLE = ... + CARROT TOMATO EGG

CARROT, TOMATO and EGG were absent from the list the agent is allowed to sell, so no carrot it grew
could ever be turned into money. Four of the five `schedule_agent*` files in the tree are still on
the wrong side of that fix, and `--module` defaulted to one of them. Every grid run without an
explicit `--module` measured it -- which produced a "missing cow since d6" finding that evaporated
the moment the right module was used.

Two things follow, and the second is the one that lasts:

1. The default has to be the module the work is actually going into.
2. **The grid has to refuse a module it cannot vouch for.** A default is a guess about what someone
   meant; a marker check is a fact about what was loaded. The marker is deliberately a CAPABILITY
   the agent must have -- can it sell a carrot -- not a version string, because a version string
   goes stale exactly as quietly as the module did.
"""

import sys
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import breakdown as B

#: Products the agent must be ABLE to sell. `_commit_unit` accepts any of the nine, and these three
#: are the ones a bug silently removed. Choosing not to sell one is a decision the schedule makes
#: per day; not being able to is a defect, and it lasted long enough to invalidate four carrot arms
#: and the whole goose verdict.
MUST_BE_SELLABLE = ("CARROT", "TOMATO", "EGG")


def test_the_default_module_can_sell_the_three_products_the_bug_blocked():
    import importlib

    module = importlib.import_module("kagg.search." + B.DEFAULT_MODULE)
    for product in MUST_BE_SELLABLE:
        assert product in module.SELLABLE, (
            f"{B.DEFAULT_MODULE} cannot sell {product}; it predates c99a8a5")


def test_loading_a_stale_module_raises_instead_of_measuring_it():
    with pytest.raises(SystemExit) as caught:
        B.load_agent_module("schedule_agent")
    assert "SELLABLE" in str(caught.value)
    assert "CARROT" in str(caught.value)


def test_loading_the_current_module_works_and_returns_it():
    module = B.load_agent_module(B.DEFAULT_MODULE)
    assert hasattr(module, "make_agent")
    for attribute in ("CUMULATIVE_SELLS", "SELL_CARRY_DAYS", "HIRE_FIRST"):
        assert hasattr(module, attribute), attribute


def test_the_check_names_every_module_in_the_tree_that_would_fail_it():
    """Not a test of the check so much as a record of the blast radius: four of five variants are
    on the wrong side of the fix, so the odds of picking a stale one by hand were 4 in 5."""
    import importlib

    stale = []
    for path in sorted((REPO / "kagg/search").glob("schedule_agent*.py")):
        module = importlib.import_module("kagg.search." + path.stem)
        if any(p not in getattr(module, "SELLABLE", ()) for p in MUST_BE_SELLABLE):
            stale.append(path.stem)
    assert B.DEFAULT_MODULE not in stale
    assert stale, ("every variant now carries the fix -- if they were collapsed into one file, "
                   "this test has done its job and can go")
