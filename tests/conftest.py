"""Applies the `slow` marker at module granularity.

The default `pytest` run must stay a few-seconds inner-loop check. Everything below pays for a JAX
trace-and-compile, a real CEM search, a scan of the replay archive, or a full 719-turn season, and
none of that belongs in the loop that runs on every edit.

Marking happens here rather than on individual tests so the list stays in one place, greppable, and
trivially revertible -- delete a line and the module rejoins the default run.

Classification (decided by reading each module's imports and assertions, not its filename):

- JAX fast-sim parity -- asserts the JAX simulator matches the numpy one, the numpy one matches the
  reference, or the fast sim's own per-turn invariants hold.
- RL training -- exercises `kagg.rl` policy/critic/curriculum/observation machinery.
- Integration -- runs the CEM search, plays a full episode through the reference or arena/ladder, or
  scans the replay archive on disk.

Left OUT deliberately, however slow, because each is a unit test of live game rules or of the
search's primitive building blocks (`kagg/search/routines.py`, `kagg/search/chains.py`), not of
search, training, or parity machinery: `test_grow_routine`, `test_production`, `test_routines`,
`test_seeded_genome`.
"""

import pytest

SLOW_MODULES = {
    # -- JAX fast-sim parity --
    "test_jax_ordered_order_book",
    "test_jax_sim",
    "test_money_accounting",
    "test_sim_parity",
    # -- RL training --
    "test_commit",
    "test_curriculum",
    "test_curriculum_mix",
    "test_jax_act",
    "test_jax_carrot",
    "test_param_migration",
    "test_rehire_cost_feature",
    "test_shaping_wiring",
    "test_train_metrics",
    "test_value_head_range",
    # -- Integration: CEM search / ladder / arena / replay-archive --
    "test_arena",
    "test_arena_state_leak",
    "test_bc_replay",
    "test_converter",
    "test_ladder",
    "test_search_executor",
    "test_search_plan",
    "test_search_transfer",
    "test_selection_boards_are_shared",
    "test_tape_parity",
}


def pytest_collection_modifyitems(config, items):
    import pytest

    slow = pytest.mark.slow
    for item in items:
        if item.module.__name__ in SLOW_MODULES:
            item.add_marker(slow)


#: Module globals that a test can change and that nothing puts back.
#:
#: `cover.PRECOMPUTED_ROUTES` is the big one. `MelonBranch.install` and `Q4Branch.install` both
#: overwrite it -- the whole route table -- and `Q4Branch` also clears `cover.UNSOLVE_DAYS`. That is
#: correct in production, where the branch installs once mid-season and the process ends with the
#: game. In a test process it means the first test that arms a latch re-points the planner's route
#: table for every test after it on that worker.
#:
#: Measured 2026-08-22: 16 tests changed verdict between two identical runs, including
#: `test_the_melon_latch_reaches_the_strawberry_tape` -- a latch test flipping on latch state left
#: behind by an earlier latch test. Fixing the leaks file by file found the constants and missed
#: this, because it is not a constant.
_GUARDED = (
    ("kagg.search.cover", "PRECOMPUTED_ROUTES"),
    ("kagg.search.cover", "UNSOLVE_DAYS"),
    ("kagg.search.schedule_agent", "REPLAY_OPENING_DAYS"),
    ("kagg.search.schedule_agent", "EMBEDDED_OPENINGS"),
    ("kagg.search.melon_branch", "OPPONENT_MELON"),
    ("kagg.search.melon_branch", "DECIDE_BY_DAY"),
    ("kagg.search.q4_branch", "DECIDE_BY_DAY"),
)


@pytest.fixture(autouse=True)
def _no_test_poisons_the_next_one():
    """Snapshot every guarded global before each test and put it back after.

    Autouse and function-scoped, so it costs one dict copy per test and removes the whole class of
    failure rather than the instances of it found by hand. A shallow copy is enough: the tests that
    leak REPLACE these objects, they do not mutate them in place.
    """
    import importlib

    saved = []
    for mod_name, attr in _GUARDED:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:                                      # noqa: BLE001
            continue                                           # optional module, nothing to guard
        if hasattr(mod, attr):
            saved.append((mod, attr, getattr(mod, attr)))
    try:
        yield
    finally:
        for mod, attr, value in saved:
            setattr(mod, attr, value)
