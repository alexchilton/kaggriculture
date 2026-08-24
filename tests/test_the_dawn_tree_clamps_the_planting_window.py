"""The middle window plants what a measured decision tree says the board supports, and no more.

Written RED before the clamp existed, per the project rule: one theory, one failing pytest.

Source: docs/history/the_opening_is_a_tape_the_middle_is_two_regimes_2026-08-21.md. The season
grid measured us at -$11,544 against the tape with -89 standing wheat and +171 idle unit-turns,
and d13-d18 -- the over-planting window -- is exactly where a dawn-board depth-3 tree predicts
the count (+45 to +23 points over baseline per day, dead from d19). So:

    13 <= day <= 18 ONLY, at dawn, cap today's `plants` row at what the tree's leaf supports.

**Measured verdict 2026-08-24: the window banks +$5,832 mean but the SEASON closes -$4,496 mean,
negative on all six seeds. `TREE_CLAMP` ships OFF** (see `tree_clamp.TREE_CLAMP`); these tests pin
the mechanism with the switch armed, so an arm that changes nothing still fails here.

The budgets are カワシギ's own d13-d18 rows (`data/seed_scripts/kawashigi/schedule.json`,
`plant_tiles`), filtered to each leaf's crop family:

                 d13 d14 d15 d16 d17 d18   total
    straw+wheat   8   4   3   2   1   0      18
    wheat         0   1   1   2   1   0       5
    straw         8   3   2   0   0   0      13

The tree itself, board-only, as fitted (my_seed_* features dropped deliberately -- they read a
decision already paid for on d12):

    my_empty <= 5.5
       my_shed_WHEAT <= 29.5          -> straw+wheat
       my_shed_WHEAT 29.5-34.5        -> wheat
       my_shed_WHEAT > 34.5           -> straw
    my_empty > 5.5
       my_crop_STRAWBERRY <= 41.5
          my_shed_FERTILIZER <= 24.5  -> straw+wheat
          my_shed_FERTILIZER > 24.5   -> straw
       my_crop_STRAWBERRY > 41.5      -> wheat

A CAP, not a rewrite: crops already in the ground are never touched, and a row already under its
budget passes through unchanged.
"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA                     # noqa: E402
from kagg.search import tree_clamp as TC                         # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent
N = 10

#: Read at IMPORT time, before the fixture arms the switch -- this is the shipped default.
SHIPPED_DEFAULT = TC.TREE_CLAMP


@pytest.fixture(autouse=True)
def clamp_on():
    """The switch ships OFF after the measured negative (see `tree_clamp.TREE_CLAMP`).
    These tests pin the MECHANISM, so each runs with it armed, and restores."""
    was = TC.TREE_CLAMP
    TC.TREE_CLAMP = True
    yield
    TC.TREE_CLAMP = was


def the_schedule():
    """The shipped plan as `make_agent` holds it: int keys, live row objects, tape columns stripped."""
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    return {int(k): {kk: vv for kk, vv in r.items()
                     if kk not in ("plant_tiles", "build_tiles", "land_turns", "orders")}
            for k, r in raw.items()}


def a_board(empty, strawberry=0):
    """An owned 10x10 board with exactly `empty` bare tiles and `strawberry` standing strawberry."""
    board = [[None] * N for _ in range(N)]
    cells = [(x, y) for y in range(N) for x in range(N)]
    for x, y in cells[:strawberry]:
        board[y][x] = {"kind": "PLANT", "crop": "STRAWBERRY"}
    for x, y in cells[strawberry:len(cells) - empty]:
        board[y][x] = {"kind": "PASTURE"}          # occupied ground that is neither crop nor bare
    return board


def an_obs(board, shed_wheat=0, shed_fertilizer=0):
    return {
        "day": 13, "hour": 0,
        "town": {"unlocked_shops": ["BAKERY"]},
        "farms": [
            {"tiles": board, "farmer": [4, 4], "hands": [], "money": 40000.0,
             "unlocked_quadrants": ["NW", "NE", "SW", "SE"]},
            {"tiles": a_board(100), "farmer": [5, 5], "hands": [], "money": 30000.0,
             "unlocked_quadrants": ["NW", "NE", "SW", "SE"]},
        ],
        "private": {"shed": {"WHEAT": shed_wheat, "FERTILIZER": shed_fertilizer},
                    "seeds": {}, "inventories": [{}]},
    }


# ---------------------------------------------------------------- the fitted tree, read back


@pytest.mark.parametrize("empty,wheat,fert,straw,expected", [
    # upper branch: a nearly full board is decided by the shed's wheat
    (3, 10, 0, 0, "straw+wheat"),
    (3, 32, 0, 0, "wheat"),           # 29.5 < 32 <= 34.5
    (3, 35, 0, 0, "straw"),
    (5, 30, 0, 0, "wheat"),           # 5.5 is the boundary: still the upper branch
    # lower branch: room to sow, decided by strawberries then fertilizer
    (20, 0, 10, 30, "straw+wheat"),
    (20, 0, 30, 30, "straw"),
    (20, 0, 0, 50, "wheat"),          # strawberry-rich boards go wheat whatever the shed holds
])
def test_the_regime_read_is_the_fitted_tree(empty, wheat, fert, straw, expected):
    feats = TC.dawn_features(a_board(empty, strawberry=straw),
                             {"WHEAT": wheat, "FERTILIZER": fert})
    assert TC.regime(feats) == expected


# ---------------------------------------------------------------- the cap, on the live plan


def test_a_wheat_leaf_caps_each_row_to_his_wheat_budget():
    """29.5 < shed WHEAT <= 34.5 on a full board: wheat only, at his own per-day counts."""
    sched = the_schedule()
    obs = an_obs(a_board(3), shed_wheat=32)
    for day, want in [(13, []), (14, ["WHEAT"]), (15, ["WHEAT"]),
                      (16, ["WHEAT", "WHEAT"]), (17, ["WHEAT"]), (18, [])]:
        assert TC.apply(sched, day, obs) is True
        assert sched[day]["plants"] == want, f"d{day}"
        obs["day"] = day + 1


def test_a_straw_leaf_takes_the_wheat_out_of_the_window():
    """shed WHEAT > 34.5 on a full board: the board cannot support wheat plantings this window."""
    sched = the_schedule()
    # The shipped rows d13-d18 are pure wheat; give one a mixed row so the FILTER is visible,
    # not just the emptying.
    sched[14]["plants"] = ["WHEAT", "STRAWBERRY", "MELON", "WHEAT"]
    obs = an_obs(a_board(3), shed_wheat=40)
    for day in range(13, 19):
        assert TC.apply(sched, day, obs) is True
        assert "WHEAT" not in sched[day]["plants"], f"d{day} still sows wheat"
        obs["day"] = day + 1
    assert sched[14]["plants"] == ["STRAWBERRY", "MELON"]      # his d14 mix, wheat removed
    assert sched[13]["plants"] == []                           # his row was wheat-only
    assert sched[16]["plants"] == []                           # his d16 was wheat-only too


def test_a_straw_wheat_leaf_caps_the_count_but_keeps_the_mix():
    """Room to sow, few strawberries, fertilizer short: his own count caps the row, mix untouched."""
    sched = the_schedule()
    sched[15]["plants"] = ["WHEAT"] * 6 + ["STRAWBERRY"]     # over his d15 budget of 3
    obs = an_obs(a_board(60, strawberry=10), shed_fertilizer=10)
    for day in range(13, 19):
        TC.apply(sched, day, obs)          # rows already under budget legitimately pass through
        obs["day"] = day + 1
    assert sched[15]["plants"] == ["WHEAT", "WHEAT", "WHEAT"]   # cut to his count, order kept


def test_a_row_already_under_its_budget_passes_through():
    """A CAP: never stretch a row up, never reorder it, only cut down."""
    sched = the_schedule()
    sched[13]["plants"] = ["WHEAT"]                        # already under every budget
    before = list(sched[13]["plants"])
    obs = an_obs(a_board(60, strawberry=10), shed_fertilizer=10)
    assert TC.apply(sched, 13, obs) is False               # nothing changed
    assert sched[13]["plants"] == before


def test_nothing_outside_d13_d18_moves():
    """The signal is dead after d19 and the tape owns the opening: gate hard on the window."""
    sched = the_schedule()
    before = json.dumps(sched, sort_keys=True)
    obs = an_obs(a_board(3), shed_wheat=40)                # maximally clamping leaf
    for day in [11, 12, 19, 20, 25]:
        assert TC.apply(sched, day, obs) is False, f"d{day} moved"
    assert json.dumps(sched, sort_keys=True) == before


# ---------------------------------------------------------------- wired into the agent


def test_the_switch_ships_off_after_the_measured_negative():
    """The season verdict is negative on every seed measured; the default must say so."""
    assert SHIPPED_DEFAULT is False


def test_with_the_switch_off_nothing_moves_anywhere():
    sched = the_schedule()
    before = json.dumps(sched, sort_keys=True)
    obs = an_obs(a_board(3), shed_wheat=40)
    TC.TREE_CLAMP = False
    try:
        for day in range(13, 19):
            assert TC.apply(sched, day, obs) is False
            obs["day"] = day + 1
    finally:
        TC.TREE_CLAMP = True
    assert json.dumps(sched, sort_keys=True) == before


def _drive(day, board=None, shed=None):
    """`agent(obs)` once, at dawn of `day`, on the shipped plan. Returns the mutated schedule."""
    sched = the_schedule()
    agent = SA.make_agent(sched, 0, router=True)
    obs = an_obs(board if board is not None else a_board(3),
                 shed_wheat=(shed or {}).get("WHEAT", 0),
                 shed_fertilizer=(shed or {}).get("FERTILIZER", 0))
    obs["day"] = day
    agent(obs)
    return sched, obs


def test_the_agent_clamps_at_dawn_of_d13():
    """End to end: one dawn call in the wheat leaf, the row comes back at his budget."""
    sched, _obs = _drive(13, a_board(3), {"WHEAT": 32})
    assert sched[13]["plants"] == []


def test_the_agent_clamps_late_in_the_window_too():
    sched, _obs = _drive(17, a_board(3), {"WHEAT": 33})
    assert sched[17]["plants"] == ["WHEAT"]
    sched, _obs = _drive(18, a_board(3), {"WHEAT": 33})
    assert sched[18]["plants"] == []


def test_the_opening_stays_byte_identical_through_the_clamp():
    """d0-d12 belong to the tape. One clamped dawn at d13 must not have touched any of them."""
    sched, _obs = _drive(13, a_board(3), {"WHEAT": 40})
    fresh = the_schedule()
    for d in range(13):
        assert json.dumps(sched[d], sort_keys=True) == json.dumps(fresh[d], sort_keys=True), \
            f"d{d} changed"
