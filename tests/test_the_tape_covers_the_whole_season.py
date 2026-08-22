"""The replay must cover every day it claims to, on every latch key, or the planner plays instead.

**This is the one guard the archive cannot do without.** `tests/archive/` holds 35 files and 183
tests covering `crew.cover`, `router.plan_routes` and the per-tile pricing under them. They are
switched off because the shipped agent replays a 720-step tape on 719 of 720 turns, so that whole
layer runs and has its answer discarded. Measured 2026-08-22,
`data/logs/planner_coverage_2026-08-22.log`:

    latch key             steps     of 720    planner decides
    (False, False)          719      99.9%          1
    (False, True)           719      99.9%          1
    (True, False)           719      99.9%          1
    (True, True)            719      99.9%          1

That is only safe while it stays true. `_replay_opening` returns `{}` for a path it cannot read --
**by design**, because a submission bundle has no `data/` tree and must degrade rather than raise
(`schedule_agent.py:5747`). So the failure mode is silent: the artifact keeps running, plays a whole
season out of the planner, and every line of that path is now untested by construction.

`replayed()` falls through with `if step not in opening: return live`, so a short tape does the same
thing for the days it does not reach. A tape truncated at d20 hands d20-d29 to the planner without
any error at all.

There is no assertion anywhere else that the openings are non-empty. `test_every_key_points_at_a_
file_that_exists` in `test_the_yarn_latch_is_not_thrown_away_when_the_melon_latch_fires.py` checks
the paths resolve, which is a different question -- a file can exist, be read, and still yield an
opening that stops at d11.

Written 2026-08-22 when the archive was created, for exactly that reason.
"""
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent as SA                                  # noqa: E402

TPD = 24


def _openings():
    """Every registered tape, resolved the same way `make_agent` resolves it."""
    return {key: SA._replay_opening(SA.REPLAY_OPENING_DAYS, *tape)
            for key, tape in SA.REPLAY_OPENING_TAPE.items()}


def test_every_registered_tape_yields_a_non_empty_opening():
    """`{}` means the file was unreadable and the agent silently plays the archived planner."""
    empty = [str(key) for key, op in _openings().items() if not op]
    assert not empty, (
        "these latch keys resolve to an EMPTY opening, so the agent plays the day planner for the "
        "whole season: " + ", ".join(empty)
        + "\n  `_replay_opening` returns {} for a path it cannot read and does not raise. The "
          "planner test surface is in tests/archive/ and is not collected, so nothing else would "
          "have caught this."
    )


@pytest.mark.parametrize("key", sorted(SA.REPLAY_OPENING_TAPE))
def test_the_opening_reaches_the_last_day_of_the_season(key):
    """A tape that stops early hands the remaining days to the planner, silently.

    Asserted on the highest step present rather than on the count, because a recording with a gap
    in the middle is a different defect from one that is simply short, and this test is about the
    end of the season.
    """
    op = _openings()[key]
    assert op, f"{key} resolves to an empty opening"
    last_day = max(op) // TPD
    want = max(SA.REPLAY_OPENING_DAYS)
    assert last_day >= want, (
        f"{key} replays up to d{last_day}, but REPLAY_OPENING_DAYS asks for d{want}. "
        f"`replayed()` falls through with `if step not in opening: return live`, so d{last_day + 1} "
        f"to d{want} are played by the day planner -- whose tests are in tests/archive/ and are not "
        f"collected."
    )


@pytest.mark.parametrize("key", sorted(SA.REPLAY_OPENING_TAPE))
def test_the_opening_has_no_hole_in_it(key):
    """Every step from 0 to the last one present, so no day is quietly handed back mid-season."""
    op = _openings()[key]
    assert op, f"{key} resolves to an empty opening"
    missing = [s for s in range(max(op) + 1) if s not in op]
    assert not missing, (
        f"{key} is missing {len(missing)} steps inside its own range, first at step {missing[0]} "
        f"(d{missing[0] // TPD} h{missing[0] % TPD}). Each one is a turn the planner decides."
    )


def test_the_bundler_embeds_an_opening_for_every_key_it_ships():
    """A bundle reads `EMBEDDED_OPENINGS`, never the disk. One missing key is a planner season.

    `build_planner_submission.py:431` writes `_EMBEDDED_OPENINGS_JSON` and line 255 loads it back
    onto the module. `make_agent` prefers it and falls back to disk only when it is empty
    (`schedule_agent.py:5754`), so in a submission -- which has no `data/` tree -- a key absent from
    the embed is a key that resolves to `{}`.

    Checked against the builder's own `_embedded_openings()` rather than by building a bundle, so it
    stays a fast test. It goes red if a fifth latch key is registered and the builder is not taught
    about it.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "_bps", REPO / "scripts/build_planner_submission.py")
    bps = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bps)

    # Keys round-trip through JSON, so they arrive as `"[false, false]"` -- read them back the same
    # way `build_planner_submission.py:255` does. Parsing them any other way makes this test fail
    # on all four keys and read exactly like the defect it is looking for.
    embedded = {tuple(json.loads(k)) for k in bps._embedded_openings()}
    registered = {tuple(k) for k in SA.REPLAY_OPENING_TAPE}
    missing = sorted(str(k) for k in registered - embedded)
    assert not missing, (
        "the builder embeds no opening for " + ", ".join(missing)
        + ".\n  A submission has no data/ tree, so that key falls back to `{}` and plays the "
          "archived day planner for a whole season, without raising."
    )
