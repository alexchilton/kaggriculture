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
