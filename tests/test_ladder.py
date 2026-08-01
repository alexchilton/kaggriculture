"""The graded fitness, and the waste detector that would have caught the converter bug on day one.

Two claims are worth testing here rather than trusting:

- the ladder produces a score that *moves*, where a single strong opponent produced 0.000 for every
  candidate and could not rank anything;
- `census` finds no-op actions without being told what makes any particular op a no-op. It is
  validated against the exact bug it failed to catch last time -- harvesting a crop before
  `first_yield_day` -- by reintroducing that bug deliberately and checking the detector reports it.
"""

import pytest

from kagg.agents import converter
from kagg.arena import ladder


def test_the_ladder_spans_weak_and_strong_opponents():
    """A fitness needs somewhere to be partially right. One opponent gave 0.000 to everything."""
    assert ladder.RUNGS[0] == "pass"
    assert ladder.RUNGS[-1] == "contrarian"
    assert len(ladder.RUNGS) >= 4


def test_every_rung_builds_into_something_playable():
    """A spec that cannot be built fails inside a worker process, where the traceback is lost."""
    for name in ladder.RUNGS:
        built = ladder.build(dict(ladder.LADDER)[name])
        assert isinstance(built, str) or callable(built), name


def test_a_parameterised_candidate_is_picklable_and_buildable():
    """Closures cannot be sent to a worker, so the candidate travels as (module_name, params)."""
    built = ladder.build(("converter", {"melon_tiles": 6}))

    assert callable(built)


@pytest.mark.slow
def test_the_score_moves_between_a_broken_and_a_working_agent():
    """The property the whole design rests on: different agents get different numbers.

    `contrarian` alone scored 0.000 for `converter` before and after two real fixes. Across the
    ladder the two agents must separate.
    """
    seeds = (4000,)
    weak = ladder.evaluate(("converter", {"melon_tiles": 0, "target_herd": 0}), seeds, workers=2)
    strong = ladder.evaluate(("module", "kagg.agents.contrarian"), seeds, workers=2)

    assert strong.score > weak.score, f"ladder cannot separate them: {weak} vs {strong}"


@pytest.mark.slow
def test_the_waste_detector_finds_a_deliberately_reintroduced_no_op():
    """The bug that cost the season: HARVEST on a crop before `first_yield_day`.

    The environment accepts the action and silently returns, so it costs a turn and leaves the
    board identical -- and because it never clears its own precondition the unit re-picks it every
    turn. Backing the maturity check out must make the waste count jump; if it does not, the
    detector is not measuring what it claims and the next such bug goes unseen too.

    This is the "revert the fix and confirm the test goes red" discipline from CLAUDE.md, applied
    to a detector rather than to a fix.
    """
    clean = ladder.census(("converter", {}))

    original = converter._ripe
    try:
        converter._ripe = lambda cell, day: cell.get("yield_units", 0) > 0
        broken = ladder.census(("converter", {}))
    finally:
        converter._ripe = original

    assert broken["wasted"] > clean["wasted"], (
        f"detector blind to the known bug: clean {clean['wasted']} vs broken {broken['wasted']}")
