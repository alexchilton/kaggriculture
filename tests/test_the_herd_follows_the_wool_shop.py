"""The wool shop is what moves the herd -- but only if it lands EARLY, and it moves the total too.

Measured over **66** downloaded games of カワシギ, the #1 player, 61-0-5
(`docs/kawashigi_one_board_2026-08-13.md`). Shops unlock every third day, so draw #N lands on day 3N
(verified 66/66). Against the position of the FIRST yarn store the herd is a step function:

    yarn first at draw #1 (d3)    : COW  6, SHEEP 12, total 18    n=10
    yarn first at draw #2 (d6)    : COW  6, SHEEP 12, total 18    n=11
    yarn first at draw #3 (d9)    : COW  6, SHEEP  8, total 14    n= 3
    yarn first at draw #4+ (d12+) : COW 10, SHEEP  4, total 14    n=16
    no yarn store at all          : COW 10, SHEEP  4, total 14    n=22  (+4 at COW 8/SHEEP 6)

`COW == 6` iff a yarn store is among the first three draws: **24/24 yes, 0/42 no**. Milk-shop count
predicts nothing yarn does not already explain -- at zero milk shops the mean cow count is still
6.57 -- and the PET_CAFE/carrot hypothesis for the four COW-8 outliers is dead: 4 of the 42 no-yarn
games have a carrot shop early, but so do 21 of the games that ran 10 cows.

This file previously rested on 6 games and asserted `(6, 8)` -- which the larger sample shows is the
RARE branch, 3 of 24. The common one is `(6, 12)` at a herd of 18, and we cannot reach it: the
extra four sheep need four more pens and `_herd_split` may only redistribute the schedule's own
count. That gap is asserted explicitly below rather than left implicit, so it cannot be mistaken for
a passing rule.
"""
import pytest

from kagg.search import schedule_agent as S


WANT = {"COW": 10, "SHEEP": 4}
NONE_BOUGHT = {"COW": 0, "SHEEP": 0, "GOOSE": 0}


def split_for(shops, day=3, bought=None):
    return S._herd_split(dict(WANT), dict(bought or NONE_BOUGHT), day, 0, list(shops), 29)


def test_the_split_is_decided_from_day_3_not_day_6():
    """His first response lands the hour the first shop unlocks."""
    assert S.SHOP_ADAPT_FROM_DAY == 3, "the first draw is d3; adapting from d6 discards it"


@pytest.mark.parametrize("shops", [
    ["YARN_STORE"],                                 # draw #1, d3
    ["BAKERY", "YARN_STORE"],                       # draw #2, d6
    ["BAKERY", "PIZZA_SHOP", "YARN_STORE"],         # draw #3, d9
])
def test_a_yarn_store_in_the_first_three_draws_holds_the_herd_at_six_cows(shops):
    """**Assert his number, not a bound.**

    This test first read `SHEEP >= 8 and COW <= 6`, and passed with the rule switched OFF -- the
    existing headroom greedy answers a wool shop by falling to the COW FLOOR of 4 and putting 10
    into sheep, which satisfies both bounds while being two cows past what the leader does. A loose
    bound around the target cannot tell "already correct" from "overshooting in the same direction".

    Six cows is the whole of what 24 of 24 yarn games agree on, at every one of the three early
    positions. The SHEEP number is not asserted here because it depends on the herd total, which we
    do not control -- see the total test below.
    """
    got = split_for(shops)
    assert got["COW"] == 6, (
        "all 24 of his early-yarn games ran exactly 6 cows; on %r we chose %r" % (shops, got))


def test_a_yarn_store_that_arrives_late_does_not_trigger_the_rule():
    """The half the first version of this rule got wrong, and the reason for the draw limit.

    Sixteen games unlock their first yarn store at draw #4 or later -- d12 onward -- and every one
    runs COW 10, exactly as if there were no wool shop at all. Wool landing at d12 has six
    production cycles left. The unsliced membership test cut those herds to six cows, so this pins
    that the RULE stays out of it.
    """
    late = ["BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "YARN_STORE"]
    got = split_for(late, day=12)
    assert got["COW"] != 6 or got["SHEEP"] != 8, (
        "the wool rule fired on a draw-#4 yarn store, which the leader ignores; got %r" % (got,))


@pytest.mark.xfail(reason="the headroom greedy, not the wool rule: it swings to the COW FLOOR of 4 "
                          "on any yarn store, early or late. Pre-existing, and changing it means "
                          "changing the greedy rather than adding a rule -- flagged, not fixed",
                   strict=True)
def test_a_late_yarn_store_still_leaves_the_herd_cow_heavy():
    """What he actually does once the rule correctly declines to fire, and what we do instead.

    With the yarn store at draw #4 the rule is out of the way and the headroom greedy decides. It
    answers a wool shop -- at ANY position -- by falling to `HERD_FLOOR_COW` and putting the rest
    into sheep, giving COW 4 / SHEEP 10 where all sixteen of his late-yarn games run COW 10 /
    SHEEP 4. So the greedy is not merely un-tuned here, it is inverted.
    """
    got = split_for(["BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "YARN_STORE"], day=12)
    assert got["COW"] >= 9, (
        "a yarn store first drawn at #4 (d12) is one he ignores -- 16 games, all COW 10; "
        "we chose %r" % (got,))


def test_two_yarn_stores_do_not_go_backwards():
    one = split_for(["YARN_STORE", "BAKERY"])
    two = split_for(["YARN_STORE", "YARN_STORE"])
    assert two["SHEEP"] >= one["SHEEP"], "more wool demand must not mean fewer sheep"


@pytest.mark.xfail(reason="the extra four sheep need four more pens; `_herd_split` may only "
                          "redistribute the schedule's count, it cannot raise it", strict=True)
def test_an_early_yarn_store_also_raises_the_herd_total():
    """The dominant branch, 21 of his 24 yarn games, and the one we cannot currently express.

    A yarn store by d6 takes him to EIGHTEEN animals -- COW 6, SHEEP 12 -- not to fourteen split
    differently. `xfail(strict=True)` so this fails loudly the day the schedule grows the pens for
    it, rather than sitting here as a comment nobody re-reads.
    """
    got = split_for(["YARN_STORE"])
    assert (got["COW"], got["SHEEP"]) == (6, 12)


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
