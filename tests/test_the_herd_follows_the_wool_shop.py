"""The wool shop is what moves the herd, and it moves it on the day it lands.

Measured over 16 downloaded games of カワシギ, the #1 player, 15-1
(`docs/kawashigi_one_board_2026-08-13.md`). His cow/sheep split separates on one variable only --
whether a YARN_STORE is among the first three unlocks -- and separates cleanly:

    0 wool shops in the first 3 draws : SHEEP 4,4,4,4,4,4,4,4,4,6   COW 10
    1 wool shop                       : SHEEP 8,8,12,12            COW 6
    2 wool shops                      : SHEEP 12,12                COW 6

Milk-shop count gives no signal at all: COW 6 occurs at both one and two milk shops. Ours ties to
COW on equal headroom and reasons that "MILK is carried by three shops against WOOL's one", which is
true of the shop table and false of the outcome -- three shops sharing milk is what floors the milk
price, and wool is the product that held $160-$181 late (`docs/the_market_is_the_late_season...`).

The other half is cadence. The first draw lands on d3 (`townShopUnlockInterval` 3) and he acts on it
that hour; `SHOP_ADAPT_FROM_DAY` was 6, so three days of evidence were being ignored.
"""
import pytest

from kagg.search import schedule_agent_1455mh as S


WANT = {"COW": 10, "SHEEP": 4}
NONE_BOUGHT = {"COW": 0, "SHEEP": 0, "GOOSE": 0}


def split_for(shops, day=3, bought=None):
    return S._herd_split(dict(WANT), dict(bought or NONE_BOUGHT), day, 0, list(shops), 29)


def test_the_split_is_decided_from_day_3_not_day_6():
    """His first response lands the hour the first shop unlocks."""
    assert S.SHOP_ADAPT_FROM_DAY == 3, "the first draw is d3; adapting from d6 discards it"


def test_a_yarn_store_in_the_first_draws_makes_the_herd_sheep_heavy():
    """**Assert his number, not a bound.**

    This test first read `SHEEP >= 8 and COW <= 6`, and passed with the rule switched OFF -- the
    existing headroom greedy answers a wool shop by falling to the COW FLOOR of 4 and putting 10
    into sheep, which satisfies both bounds while being two cows past what the leader does. A loose
    bound around the target cannot tell "already correct" from "overshooting in the same direction".
    """
    got = split_for(["YARN_STORE"])
    assert (got["COW"], got["SHEEP"]) == (6, 8), (
        "every one of his six yarn-store games ran exactly 6 cows; we chose %r" % (got,))


def test_two_yarn_stores_do_not_go_backwards():
    one = split_for(["YARN_STORE", "BAKERY"])
    two = split_for(["YARN_STORE", "YARN_STORE"])
    assert two["SHEEP"] >= one["SHEEP"], "more wool demand must not mean fewer sheep"


def test_no_wool_shop_keeps_the_herd_cow_heavy():
    """The other side of the rule: this must not become "always sheep"."""
    got = split_for(["PIZZA_SHOP", "BAKERY", "ICE_CREAM_SHOP"])
    assert got["COW"] >= 9, "no wool shop, so the leader runs 10 cows; we chose %r" % (got,)
    assert got["SHEEP"] <= 5


def test_the_total_is_never_exceeded():
    """`want_total` is the schedule's count and the split may only redistribute it."""
    for shops in ([], ["YARN_STORE"], ["YARN_STORE", "YARN_STORE"], ["PIZZA_SHOP"]):
        got = split_for(shops)
        assert got["COW"] + got["SHEEP"] == WANT["COW"] + WANT["SHEEP"], shops


def test_animals_already_bought_are_never_unbought():
    got = split_for(["YARN_STORE"], bought={"COW": 8, "SHEEP": 0, "GOOSE": 0})
    assert got["COW"] >= 8, "the split anchors on what is bought; it cannot fall"
