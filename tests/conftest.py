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


#: Modules whose module-level globals are snapshotted around every test.
#:
#: **Naming them one at a time did not work.** Seven leaking constants were found by hand, then
#: `cover.PRECOMPUTED_ROUTES` -- the planner's whole route table, rewritten by `MelonBranch.install`
#: and `Q4Branch.install` -- and the suite was still not deterministic: two identical runs disagreed
#: on 20 tests. Run alone the same file is identical 5 times out of 5, so it is shared state and not
#: the environment.
#:
#: So this snapshots EVERY uppercase module-level name in these modules rather than a list someone
#: has to keep current. A list of names goes stale the moment a new global is added; this does not.
#: Private module caches that survive a global restore because they are mutated in place.
_PRIVATE_CACHES = ("_NEAREST", "_REVENUE_CACHE", "_ARMED")

_GUARDED_MODULES = (
    "kagg.search.schedule_agent",
    "kagg.search.cover",
    "kagg.search.router",
    "kagg.search.routines",
    "kagg.search.melon_branch",
    "kagg.search.q4_branch",
    "kagg.search.crew",
    "kagg.search.dayplan",
)


@pytest.fixture(autouse=True)
def _no_test_poisons_the_next_one():
    """Snapshot every module-level CONSTANT in the guarded modules, and put them all back.

    Only names that are already imported are touched -- importing a module here would change what
    a test sees. Values are stored by reference: the leaks REPLACE these objects rather than mutate
    them in place, which is what makes a reference enough and keeps the cost to one dict scan.

    Pollution here does not only turn tests red. In the full suite some of the eight failures in
    `test_the_wheat_row_is_bought_from_the_dawn_bank` PASS, so leaked state was making assertions
    succeed that fail on a clean module. A test that only passes because another test ran first is
    worse than one that fails.
    """
    import sys

    saved = []
    for name in _GUARDED_MODULES:
        mod = sys.modules.get(name)
        if mod is None:
            continue
        for attr, value in vars(mod).items():
            # Private caches count. `cover._NEAREST` memoises nearest-tile lookups and a test
            # clears it; skipping underscore names left exactly that kind of state unguarded.
            if (attr.isupper() and not attr.startswith("__")) or attr in _PRIVATE_CACHES:
                saved.append((mod, attr, value))
    try:
        yield
    finally:
        for mod, attr, value in saved:
            setattr(mod, attr, value)
