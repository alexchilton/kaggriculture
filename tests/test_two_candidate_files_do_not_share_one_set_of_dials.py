"""Two agent files in one process must not overwrite each other's dials.

The failure this pins, measured 2026-08-15: `scripts/cem_collection.py` reported **byte-identical**
tiles, bank and collection rates for `m8`, `c8`, `s4` and the zero vector -- MELON 12, WHEAT 132,
STRAWBERRY 41, CARROT 8, $132,959 -- on all four. The dials were not reaching the game.

The cause is that a candidate file sets its dials as attributes on the shared
`kagg.search.schedule_agent` module:

    import kagg.search.schedule_agent as A
    A.CROP_TILE_SHIFTS = (("WHEAT", "MELON", 8),)

`import` returns the module already in `sys.modules`, so the second file to load wins and BOTH
agents then play its dials. This matters far beyond the one script: the CEM's objective plays a
candidate against a frozen `shipped` agent inside a single `env.run`, and both files are exec'd in
that one process. A collision there does not fail loudly -- it silently turns every duel into a
mirror match, which is exactly the "print the name the code actually reads before any A/B" trap in
`CLAUDE.md`.

`scripts/cem_allocation.py` therefore gives each candidate file a PRIVATE copy of the module, loaded
from source under a unique name. These tests are what keep it that way.
"""
import importlib.util
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
SCHEDULE = REPO / "data" / "seed_scripts" / "kawashigi" / "schedule.json"

pytestmark = pytest.mark.skipif(not SCHEDULE.exists(), reason="schedule.json is gitignored data")

sys.path.insert(0, str(REPO / "scripts"))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_a_naive_shared_import_lets_the_second_file_win(tmp_path):
    """The bug itself, reproduced on purpose, so the fix below is measured against something.

    If this ever stops failing to isolate, the shared-module hazard has gone away and
    `write_candidate`'s private-copy machinery can be simplified.
    """
    import kagg.search.schedule_agent as A

    before = A.CROP_TILE_SHIFTS
    try:
        for i, shifts in enumerate([(("WHEAT", "MELON", 8),), ()]):
            p = tmp_path / f"naive_{i}.py"
            p.write_text("import kagg.search.schedule_agent as A\n"
                         f"A.CROP_TILE_SHIFTS = {shifts!r}\n")
            load(p, f"naive_{i}")
        assert A.CROP_TILE_SHIFTS == (), "expected the second file to have overwritten the first"
    finally:
        A.CROP_TILE_SHIFTS = before


def test_two_candidate_files_keep_their_own_dials(tmp_path):
    from cem_allocation import write_candidate

    a = load(write_candidate((1, 8, 0, 0, 0, 0)), "cand_a")
    b = load(write_candidate((1, 0, 0, 0, 0, 0)), "cand_b")

    assert a.A is not b.A, "the two candidates share one schedule_agent module"
    assert a.A.CROP_TILE_SHIFTS == (("WHEAT", "MELON", 8),), a.A.CROP_TILE_SHIFTS
    assert b.A.CROP_TILE_SHIFTS == (), b.A.CROP_TILE_SHIFTS


def test_the_fork_and_geese_dials_survive_a_second_file_too(tmp_path):
    from cem_allocation import write_candidate

    a = load(write_candidate((0, 0, 0, 0, 0, 3)), "cand_c")
    b = load(write_candidate((1, 0, 0, 0, 0, 0)), "cand_d")

    assert (a.A.MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT, a.A.HERD_GEESE) == (False, 3)
    assert (b.A.MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT, b.A.HERD_GEESE) == (True, 0)


def test_a_private_copy_does_not_leak_into_the_shared_module(tmp_path):
    """The shared `kagg.search.schedule_agent` must come out of this untouched.

    Anything else in the process -- `pool`, the guards, a later import -- reads that one.
    """
    import kagg.search.schedule_agent as SHARED
    from cem_allocation import write_candidate

    before = (SHARED.CROP_TILE_SHIFTS, SHARED.HERD_GEESE,
              SHARED.MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT)
    load(write_candidate((0, 12, 4, 4, 7, 3)), "cand_e")
    after = (SHARED.CROP_TILE_SHIFTS, SHARED.HERD_GEESE,
             SHARED.MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT)
    assert before == after, (before, after)
