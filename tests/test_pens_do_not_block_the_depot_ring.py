"""Does a PASTURE/COOP sitting on a shed-access tile block DROP or PICKUP there?

Rendering the board at the end of day 11 showed all four shed-access tiles -- (4,4), (5,4), (4,5),
(5,5), `kg._shed_access_tiles(10)` -- carrying PASTURE, in two different pen-siting configurations.
That raised the question directly: if a structure on the depot ring blocks delivery, it would sit
upstream of a great deal of recent work, including a delivery investigation where seven separate
fixes all regressed, and the finding that the day-10 melon harvest never reaches the shed.

Read off `reference/kaggriculture.py` (`_apply_unit_action`), the answer is NO, and it is a
positional accident why the intuition is tempting: DROP and PICKUP gate on `_is_shed_adjacent`,
which is a pure `(x, y)` set-membership check (`kaggriculture.py:123-124`). The shared prefix
above both branches only rejects `tile == "LOCKED"` (`kaggriculture.py:322-323`); a PASTURE or COOP
dict is not `"LOCKED"`, so it does not trip that gate either. Movement is gated the same way
(`kaggriculture.py:308-316`, blocks only `"LOCKED"`), so a unit can walk onto and stand on an
occupied shed-access tile in the first place -- there is no unit-collision or structure-occupancy
check anywhere in `_apply_unit_action`.

So: a structure on the depot ring does NOT block delivery, and the tile is shed-adjacent regardless
of what is built on it. This is a clean negative -- it rules the mechanism out, it does not explain
the day-10 melon-never-reaches-shed finding, and that finding needs a different cause.
"""

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

BOARD_SIZE = 10


def _farm_with_structure(tile, kind):
    farm = {"tiles": [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)],
            "farmer": list(tile), "hands": [], "money": 3000.0}
    farm["tiles"][tile[1]][tile[0]] = {"kind": kind}
    return farm


def test_the_depot_ring_is_exactly_the_four_tiles_the_investigation_named():
    assert set(kg._shed_access_tiles(BOARD_SIZE)) == {(4, 4), (5, 4), (4, 5), (5, 5)}


def test_a_pasture_on_a_shed_access_tile_does_not_block_drop():
    tile = (4, 4)
    farm = _farm_with_structure(tile, "PASTURE")
    private = {"shed": {}, "seeds": {}, "inventories": [{"WHEAT": 5}]}

    kg._apply_unit_action(farm, private, 0, ["DROP"], BOARD_SIZE, 0, 24)

    assert private["shed"].get("WHEAT", 0) == 5, (
        "DROP was silently blocked by the PASTURE occupying the shed-access tile")
    assert private["inventories"][0] == {}, "DROP should have emptied the unit's inventory"


def test_a_pasture_on_a_shed_access_tile_does_not_block_pickup():
    tile = (5, 5)
    farm = _farm_with_structure(tile, "PASTURE")
    private = {"shed": {"WHEAT": 5}, "seeds": {}, "inventories": [{}]}

    kg._apply_unit_action(farm, private, 0, ["PICKUP", "WHEAT", 3], BOARD_SIZE, 0, 24)

    assert private["inventories"][0].get("WHEAT", 0) == 3, (
        "PICKUP was silently blocked by the PASTURE occupying the shed-access tile")
    assert private["shed"]["WHEAT"] == 2


def test_a_coop_on_a_shed_access_tile_does_not_block_drop():
    """Same claim, the other pen-siting structure the day-11 render showed."""
    tile = (4, 5)
    farm = _farm_with_structure(tile, "COOP")
    private = {"shed": {}, "seeds": {}, "inventories": [{"EGG": 2}]}

    kg._apply_unit_action(farm, private, 0, ["DROP"], BOARD_SIZE, 0, 24)

    assert private["shed"].get("EGG", 0) == 2, (
        "DROP was silently blocked by the COOP occupying the shed-access tile")


def test_a_unit_can_stand_on_an_occupied_shed_access_tile_at_all():
    """DROP/PICKUP presuppose the unit got there. Confirm movement onto the tile is not blocked
    either -- there is no structure-occupancy or unit-collision check in `_apply_unit_action`."""
    tile = (5, 4)
    farm = _farm_with_structure(tile, "PASTURE")
    farm["farmer"] = [tile[0] - 1, tile[1]]  # one step west of the tile
    private = {"shed": {}, "seeds": {}, "inventories": [{}]}

    kg._apply_unit_action(farm, private, 0, ["EAST"], BOARD_SIZE, 0, 24)

    assert tuple(farm["farmer"]) == tile, "movement onto an occupied shed-access tile was blocked"


def test_an_empty_shed_access_tile_behaves_identically_control():
    """Control: the same DROP on the same tile with no structure on it, to show the structure
    itself changes nothing -- both paths reach the same shed state."""
    tile = (4, 4)
    farm = {"tiles": [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)],
            "farmer": list(tile), "hands": [], "money": 3000.0}
    private = {"shed": {}, "seeds": {}, "inventories": [{"WHEAT": 5}]}

    kg._apply_unit_action(farm, private, 0, ["DROP"], BOARD_SIZE, 0, 24)

    assert private["shed"].get("WHEAT", 0) == 5


def test_not_even_locked_blocks_a_shed_operation():
    """**REVERSED BY kaggle-environments 1.32.6.** LOCKED no longer stops DROP either.

    This was the contrast case: it asserted that LOCKED DOES block DROP, to show the gate was a
    real check rather than a no-op that merely happened not to fire for a structure. That contrast
    no longer exists. `_apply_unit_action` now says so in its own comments:

        Movement onto LOCKED tiles is allowed: a hand can spawn on a locked [tile]
        Tile operations (PLANT, WATER, etc.) still no-op on LOCKED tiles.
        Shed operations resolve before the LOCKED guard. They use the tile only as
        [a position, and] the four shed-access tiles start LOCKED, so guarding them
        first would make the [shed unreachable on day 0].

    So the ordering is deliberate and the reason is the depot ring itself: those four tiles begin
    the game LOCKED, and a shed you cannot reach until you buy the middle quadrant would be a very
    different game.

    The module's conclusion is unchanged and now holds a fortiori -- NOTHING blocks a shed
    operation on the depot ring. Tile ops (PLANT, WATER) do still no-op on LOCKED, so the guard is
    not gone, it simply sits after the shed branch.
    """
    tile = (4, 4)
    farm = {"tiles": [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)],
            "farmer": list(tile), "hands": [], "money": 3000.0}
    farm["tiles"][tile[1]][tile[0]] = "LOCKED"
    private = {"shed": {}, "seeds": {}, "inventories": [{"WHEAT": 5}]}

    kg._apply_unit_action(farm, private, 0, ["DROP"], BOARD_SIZE, 0, 24)

    assert private["shed"].get("WHEAT", 0) == 5, (
        "a shed operation resolves before the LOCKED guard, so DROP on a locked depot tile lands")


def test_the_locked_guard_still_fires_for_a_tile_operation():
    """The guard is reordered, not removed -- pinned so the reversal above cannot be over-read.

    Without this, `test_not_even_locked_blocks_a_shed_operation` alone would read as "LOCKED means
    nothing now", and a future session could reasonably conclude the whole check had been deleted.
    """
    tile = (3, 3)
    farm = {"tiles": [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)],
            "farmer": list(tile), "hands": [], "money": 3000.0}
    farm["tiles"][tile[1]][tile[0]] = "LOCKED"
    private = {"shed": {}, "seeds": {"WHEAT": 5}, "inventories": [{}]}

    kg._apply_unit_action(farm, private, 0, ["PLANT", "WHEAT"], BOARD_SIZE, 0, 24)

    assert farm["tiles"][tile[1]][tile[0]] == "LOCKED", "PLANT must still no-op on a LOCKED tile"
    assert private["seeds"]["WHEAT"] == 5, "a blocked PLANT must not consume the seed"
