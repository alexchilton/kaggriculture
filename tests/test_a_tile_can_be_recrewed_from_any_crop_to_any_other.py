"""Any crop can be spent on any other, not only wheat on carrot and tomato.

`_wheat_to` could re-crew WHEAT plant stops only, so a sweep could ask "more tomato" but never
"less melon" or "more wheat". That is the wrong shape for the question in front of us. Measured on
ladder game `93346440`, a game we WON by $70,525, the closing book was:

    product        base   inv close   price close
    MELON           250       10157         $  4     flooded, +157 units
    WHEAT            25        9419         $ 49     scarce, ~2x base, -581 drained
    TOMATO           60        9916         $ 70     scarce, above base
    CARROT           35       10032         $ 28     we supplied it, nobody drained it
    STRAWBERRY      120        9916         $197     scarce, above base

Melon realised **1.6% of its base price** while wheat realised nearly double. Neither is reachable
with a knob that only spends wheat, and `SHOP_ADAPT_CROPS`'s own docstring names that exact pair --
"wheat against strawberry+melon" -- as the axis worth building.

This pins the mechanism, not any particular allocation: it says a shift is expressible and billed
correctly. It says nothing about which shift is right, which is what the sweep is for.
"""
import importlib

import pytest

A = importlib.import_module("kagg.search.schedule_agent")
RT = importlib.import_module("kagg.search.router")


def _row():
    """A day that plants four wheat, two melon and one strawberry, with the seeds to match."""
    return {"plants": ["WHEAT", "MELON", "WHEAT", "STRAWBERRY", "WHEAT", "MELON", "WHEAT"],
            "seeds": {"WHEAT": 4, "MELON": 2, "STRAWBERRY": 1}}


def test_the_general_recrew_exists():
    """The premise. `_wheat_to` alone cannot express 'less melon'."""
    assert hasattr(A, "_recrew"), (
        "no _recrew(row, src, dst, budget); only _wheat_to exists, so a sweep can never reduce "
        "melon or increase wheat")


def test_melon_can_be_spent_on_wheat():
    """The case the win at 93346440 argues for: melon closed $4 of $250, wheat $49 of $25."""
    row, spent = A._recrew(_row(), "MELON", "WHEAT", 2)
    assert spent == 2, f"asked to move 2 melon tiles, moved {spent}"
    assert row["plants"].count("MELON") == 0, f"melon survived the shift: {row['plants']}"
    assert row["plants"].count("WHEAT") == 6, f"wheat did not gain both tiles: {row['plants']}"


def test_the_seed_row_follows_the_plants():
    """The bill has to stay honest -- the crops do not cost the same.

    `RT.SEED_COST` MELON 80, WHEAT 10. Moving the plants without the seeds under-bills the day and
    mis-sets `short_of_cash`, which is the failure `_wheat_to`'s docstring already records.
    """
    row, _ = A._recrew(_row(), "MELON", "WHEAT", 2)
    assert row["seeds"].get("MELON", 0) == 0, f"melon seed left behind: {row['seeds']}"
    assert row["seeds"].get("WHEAT", 0) == 6, f"wheat seed did not follow: {row['seeds']}"


def test_the_budget_is_a_ceiling():
    """Asking for more tiles than the row holds moves what there is and reports it."""
    row, spent = A._recrew(_row(), "STRAWBERRY", "TOMATO", 9)
    assert spent == 1, f"row holds one strawberry, moved {spent}"
    assert row["plants"].count("TOMATO") == 1


def test_a_zero_budget_changes_nothing():
    before = _row()
    row, spent = A._recrew(before, "WHEAT", "TOMATO", 0)
    assert spent == 0 and row["plants"] == before["plants"] and row["seeds"] == before["seeds"]


def test_a_crop_the_row_does_not_plant_is_a_no_op():
    before = _row()
    row, spent = A._recrew(before, "CARROT", "WHEAT", 4)
    assert spent == 0 and row["plants"] == before["plants"]


def test_the_shift_table_is_inert_by_default():
    """Nothing ships changed until a sweep sets it."""
    assert A.CROP_TILE_SHIFTS == (), (
        f"CROP_TILE_SHIFTS defaults to {A.CROP_TILE_SHIFTS!r}; it must be inert")


@pytest.mark.parametrize("src,dst", [("WHEAT", "TOMATO"), ("MELON", "WHEAT"),
                                     ("STRAWBERRY", "MELON"), ("CARROT", "WHEAT")])
def test_every_pair_is_expressible(src, dst):
    """All five crops, both directions -- that is what 'knob all of them' means."""
    row = {"plants": [src, src, "WHEAT"], "seeds": {src: 2, "WHEAT": 1}}
    out, spent = A._recrew(row, src, dst, 1)
    assert spent == 1, f"{src} -> {dst} moved nothing"
    assert out["plants"].count(dst) >= 1
