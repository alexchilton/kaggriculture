"""On a wool-early three-quadrant board the leader buys TWELVE animals, not fourteen.

Fitted directly to カワシギ, as Alex asked: take his three-quadrant seats, work the rule out from
the shop draw, and accept it if it is ~90% exact. Measured 2026-08-15 over **74 distinct** episodes
on disk carrying his seat, deduplicated by episode id and restricted to the 51 seats that own three
quadrants -- the board size we actually play. Seat alignment verified against `92498144`, where
`farms[0]` is カワシギ at $149,998 and matches `rewards[0]`.

He has exactly three answers on three quadrants:

    COW  SHEEP  total   n
      6      6     12    4      every one has its first YARN_STORE in draws 1-3
      8      6     14    5      four of the five have exactly ONE milk shop and no yarn store
     10      4     14   42

Exhaustive search over the two thresholds (`data/logs/kawa_q3_rule_search.log`):

    exact (COW,SHEEP)   yarn_by   milk_lo
       49/51  96.1%           3         1      <- best
       46/51  90.2%           3         0
       45/51  88.2%           2         1

and the two misses are a symmetric pair -- one `nyarn=0, nmilk=3` seat where he ran COW 8 and one
`nyarn=0, nmilk=1` seat where he ran COW 10. Same inputs, opposite choices, so that is irreducible
noise rather than a missing feature.

**The part that matters is the TOTAL, and it goes DOWN.** Our rule copies his 6-cow cap and then
spends the rest of a fixed 14-animal budget on sheep, giving COW 6 / SHEEP 8. He runs COW 6 /
SHEEP 6. Those two extra sheep are ~16 units of wool into a book that reaches `PRICE_FLOOR` at 59
units above `I0` (`docs/the_wool_book_needs_two_shops_2026-08-15.md`), plus $1,000 and two FEED and
two CARE stops every day for the rest of the season. Dropping the total needs no new pens, which is
why this is cheap -- unlike raising it, which he only ever does on FOUR quadrants.

Our current rule scores 42/51 = 82.4% exact against him. This one scores 49/51 = 96.1%.
"""
import pytest

from kagg.search import schedule_agent as S

#: **PARKED 2026-08-15.** The fit is good -- 49/51 = 96.1% against his three-quadrant seats versus
#: 42/51 = 82.4% shipped -- but `HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE` is OFF, because
#: dropping the herd to twelve only pays if the freed turns become crops and our solver is not
#: reactive. See the flag's docstring. `strict=True` so re-enabling it turns these green and says so.
PARKED = pytest.mark.xfail(strict=True, reason=(
    "HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE is off: the total-12 branch surrenders ~16 units "
    "of wool on exactly the boards where wool pays, and we have no logic to spend the freed turns "
    "on planting the way he does."))


NONE_BOUGHT = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
WANT = {"COW": 10, "SHEEP": 4}


def split_for(shops, day=3, bought=None, want=None):
    return S._herd_split(dict(want or WANT), dict(bought or NONE_BOUGHT), day, 0, list(shops), 29)


#: (shops in unlock order, his COW, his SHEEP). The three branches, at every position that
#: discriminates them.
#: The last two match the shipped rule as well, so they must pass with the flag OFF and are not
#: marked parked; the first four are the branches the flag actually changes.
CASES = [
    pytest.param(["YARN_STORE"], 6, 6, marks=PARKED),                    # first yarn at draw #1
    pytest.param(["BAKERY", "YARN_STORE"], 6, 6, marks=PARKED),          # draw #2
    pytest.param(["BAKERY", "BRUNCH_SPOT", "YARN_STORE"], 6, 6, marks=PARKED),   # draw #3
    pytest.param(["PIZZA_SHOP", "BAKERY", "BRUNCH_SPOT"], 8, 6, marks=PARKED),   # no yarn, 1 milk
    (["PIZZA_SHOP", "ICE_CREAM_SHOP", "BAKERY"], 10, 4),             # no yarn, two milk shops
    (["BAKERY", "BRUNCH_SPOT", "FARMERS_MARKET", "YARN_STORE"], 10, 4),   # yarn at draw #4
]


@pytest.mark.parametrize("shops,cow,sheep", CASES)
def test_the_split_matches_the_leader_on_three_quadrants(shops, cow, sheep):
    got = split_for(shops, day=9)
    assert (got["COW"], got["SHEEP"]) == (cow, sheep), (
        f"on {shops!r} he runs COW {cow} / SHEEP {sheep}; we chose {got!r}")


@PARKED
def test_an_early_wool_board_buys_twelve_animals_not_fourteen():
    """The defect, isolated from the ratio.

    This is the whole change: the ratio 6:8 and the ratio 6:6 both cap cows at six, so a test that
    only asserted the cow count would pass with the bug in place.
    """
    got = split_for(["YARN_STORE"], day=9)
    assert got["COW"] + got["SHEEP"] == 12, (
        f"an early yarn store should take the herd DOWN to 12 -- he never runs 14 there -- "
        f"we chose a total of {got['COW'] + got['SHEEP']}: {got!r}")


@PARKED
def test_a_milk_poor_board_moves_one_cow_into_a_sheep():
    """The 8/6 branch, which our rule has never expressed.

    Five of his 51 three-quadrant seats run COW 8 / SHEEP 6 and four of those five have exactly one
    milk shop and no yarn store. MILK is carried by three shop types of eight, so a single milk shop
    is a genuinely thin book.
    """
    got = split_for(["PIZZA_SHOP", "BAKERY", "BRUNCH_SPOT"], day=9)
    assert (got["COW"], got["SHEEP"]) == (8, 6), got


def test_the_common_board_is_untouched():
    """42 of 51 seats. This rule must not disturb the branch that was already right."""
    got = split_for(["PIZZA_SHOP", "ICE_CREAM_SHOP", "BAKERY"], day=9)
    assert (got["COW"], got["SHEEP"]) == (10, 4), got


def test_animals_already_bought_are_never_unbought():
    """The total may only fall for animals not yet purchased.

    Dropping to twelve must never mean selling or abandoning a cow that exists, and `_herd_split`
    is anchored on `bought` precisely so it cannot.
    """
    got = split_for(["YARN_STORE"], day=9, bought={"COW": 8, "SHEEP": 2, "GOOSE": 0})
    assert got["COW"] >= 8 and got["SHEEP"] >= 2, got
    assert got["COW"] + got["SHEEP"] >= 10, got


@PARKED
def test_the_rule_beats_the_old_one_on_his_own_seats():
    """The 90% bar, asserted rather than described.

    Encodes the measured distribution of his 51 three-quadrant seats and requires the live rule to
    reproduce it. `data/logs/kawa_q3_rule_search.log` holds the search this came from.
    """
    # (first-yarn draw or None, milk-shop count) -> (his COW, his SHEEP), with the seat count
    seats = [((3, 4), (6, 6), 1), ((3, 5), (6, 6), 1), ((3, 3), (6, 6), 2),
             ((None, 1), (8, 6), 4), ((None, 3), (8, 6), 1),
             ((None, 1), (10, 4), 1), ((None, 2), (10, 4), 4), ((None, 3), (10, 4), 6),
             ((None, 4), (10, 4), 6), ((None, 5), (10, 4), 3), ((None, 6), (10, 4), 4),
             ((4, 3), (10, 4), 2), ((4, 5), (10, 4), 2), ((4, 6), (10, 4), 1),
             ((6, 2), (10, 4), 1), ((6, 3), (10, 4), 1), ((6, 5), (10, 4), 1),
             ((7, 3), (10, 4), 2), ((8, 3), (10, 4), 1), ((8, 4), (10, 4), 3),
             ((4, 4), (10, 4), 1), ((6, 4), (10, 4), 2), ((4, 1), (10, 4), 1)]
    milk_shop = {1: ["PIZZA_SHOP"], 2: ["PIZZA_SHOP", "ICE_CREAM_SHOP"],
                 3: ["PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP"]}
    ok = total = 0
    misses = []
    for (fy, nmilk), his, n in seats:
        shops = []
        milks = milk_shop.get(min(3, nmilk), ["PIZZA_SHOP"]) * max(1, nmilk // 3)
        for i in range(1, 9):
            if fy is not None and i == fy:
                shops.append("YARN_STORE")
            elif milks:
                shops.append(milks.pop(0))
            else:
                shops.append("BAKERY")
        got = split_for(shops, day=9)
        total += n
        if (got["COW"], got["SHEEP"]) == his:
            ok += n
        else:
            misses.append((fy, nmilk, his, (got["COW"], got["SHEEP"]), n))
    assert ok / total >= 0.90, (
        f"reproduced {ok}/{total} = {ok / total:.1%} of his three-quadrant seats, below the 90% "
        f"bar; misses (first-yarn, milk shops, his, ours, n): {misses}")
