"""The strawberry/melon split answers the OPPONENT's melon, not the shop draw.

Measured across all sixteen downloaded カワシギ games, 2026-08-15. His split has exactly two states
and the total is always 54:

    STRAW 34 / MELON 20   10 games        STRAW 42 / MELON 12    6 games

Every game buys `MELON 12` on d0; the entire decision is one binary +8 executed `d5:+3 d6:+5`, paid
for with eight fewer strawberry. It separates 16/16 on the opponent:

    researchstudio.site   6 games   d5 board: MELON 9, WHEAT 7                -> MELON 12
    Yusuke Hayashi        6 games   d5 board: MELON 5, STRAWBERRY 3, WHEAT 6  -> MELON 20
    Filip Strzalka        3 games   same                                      -> MELON 20
    Arda Ceylan           1 game    same                                      -> MELON 20

The first shop unlocks at d2h23 in all sixteen and does NOT separate them -- `PIZZA_SHOP` and
`SMOOTHIE_SHOP` each appear on both sides. Melon is the one crop no shop buys at all
(`kaggriculture.py:91-98`), so its price is set by nothing but how much the two farms dump into the
town book, while strawberry has four shops bidding. An opponent on nine melon tiles is going to
flood that book.

This corrects C-23 in `docs/REGISTER.md`, which closed the `STRAWBERRY<->MELON` swap as unable to
adapt "because no shop carries melon". True of `SHOP_ADAPT_CROPS`, and the wrong reason: the signal
was never the shop.

See `MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`.
"""
import importlib

import pytest

SA = importlib.import_module("kagg.search.schedule_agent_1455mh")


def _row():
    return {"seeds": {"MELON": 3, "WHEAT": 4}, "plants": {"MELON": 3, "WHEAT": 4},
            "sells": {"MILK": 6}, "hires": 2}


def test_the_melon_count_becomes_a_strawberry_count():
    out = SA._melon_to_strawberry(_row())
    assert out["seeds"] == {"WHEAT": 4, "STRAWBERRY": 3}, out["seeds"]
    assert out["plants"] == {"WHEAT": 4, "STRAWBERRY": 3}, out["plants"]


def test_the_count_is_kept_exactly():
    """54 either way -- only the crop is re-decided, never the number of stops."""
    row = {"seeds": {"MELON": 5, "STRAWBERRY": 4}, "plants": {"MELON": 5, "STRAWBERRY": 4}}
    out = SA._melon_to_strawberry(row)
    for key in ("seeds", "plants"):
        before = sum(row[key].get(c, 0) for c in ("MELON", "STRAWBERRY"))
        after = sum(out[key].get(c, 0) for c in ("MELON", "STRAWBERRY"))
        assert before == after == 9, f"{key}: {before} -> {after}"
        assert "MELON" not in out[key], out[key]


def test_the_rest_of_the_row_is_untouched():
    out = SA._melon_to_strawberry(_row())
    assert out["sells"] == {"MILK": 6} and out["hires"] == 2, out


def test_the_input_row_is_not_mutated():
    """`make_agent` shares every row with the caller, so a swap in place leaks into the next game."""
    row = _row()
    SA._melon_to_strawberry(row)
    assert row["seeds"] == {"MELON": 3, "WHEAT": 4}, (
        f"the caller's schedule was rewritten in place: {row['seeds']}")


def test_a_row_with_no_melon_is_returned_unchanged():
    row = {"seeds": {"WHEAT": 4}, "plants": {"WHEAT": 4}}
    assert SA._melon_to_strawberry(row) is row


def test_the_threshold_sits_between_the_two_observed_boards():
    """5 melon tiles must not fire and 9 must. Those are the only values the sixteen games hold."""
    assert 5 < SA.MELON_YIELD_OPPONENT_MELON <= 9, SA.MELON_YIELD_OPPONENT_MELON
    assert SA.MELON_YIELD_FROM_DAY == 5, SA.MELON_YIELD_FROM_DAY
