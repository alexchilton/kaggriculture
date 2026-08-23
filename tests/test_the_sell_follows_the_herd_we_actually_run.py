"""The SELL of animal produce must follow the herd, and wool must not sit in the shed.

`replayed()` re-points two of the tape's three order kinds and left the third alone:

    BUY_ANIMAL   re-split head by head against `state["herd_split"]`   schedule_agent.py:6035
    BUY_SEED     trimmed to what the season can still plant            schedule_agent.py:6017
    SELL         fell through to `orders.append(o)` verbatim           <- this

The seed trim's own comment says why it exists -- "his seed COUNT is sized for his season, not
ours, and the surplus is never sown" -- which is exactly as true of wool and milk.

Measured on two ladder games, both losses, 2026-08-23:

    97495667  straw_q3  seat 1    tape COW 10 SHEEP 4   ours COW 8 SHEEP 6   sells 29/23 both
    97486506  melon_q3  seat 0    tape COW 10 SHEEP 4   ours COW 9 SHEEP 5   sells 25/25 both

**Wool and milk are not the same problem, and the price series proves it.** Game 97495667:

    day  WOOLprc  shed  MILKprc  wool offered
     13     227      8     112       8
     19     231     21       1      20      <- 20 offered, price 231 -> 227
     23     230     32       1      12
     28     227     44       1       8
     29     229     40       3       8

WOOL holds 227-234 all season whatever we offer; MILK falls 185 -> 1 over the same days. So the
yarn book is drain-limited, not price-limited: an unfilled wool offer costs nothing, and holding 40
units at 229 to the final bell realises zero. Milk is the book we flood ourselves, and there the
right move is to offer LESS.

Hence two different rules, which is why an earlier version of this file asserted a 1.5x ratio for
wool. That was measured to be too timid and the assertion is deliberately changed here -- the shed
goes out, not a multiple of the tape's count.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent as SA                       # noqa: E402

TAPE_HERD = {"COW": 10, "SHEEP": 4}
OURS = {"COW": 8, "SHEEP": 6}
MID = 15


def sell(order, shed, day=MID, ours=None, tape=None):
    return SA.scale_the_sell_to_the_herd(order, ours or OURS, tape or TAPE_HERD, shed, day)


def test_wool_offers_the_whole_shed():
    """CHANGED from a 1.5x ratio. The book holds 227-234 whatever we send, so send it all."""
    assert sell(["SELL", "WOOL", 4], {"WOOL": 38}) == ["SELL", "WOOL", 38], \
        "38 in the shed and a book that does not move -- offer all of it"


def test_wool_offer_is_never_less_than_the_tape_asked():
    """A thin shed must not silently shrink the tape's own cadence below what it holds."""
    assert sell(["SELL", "WOOL", 4], {"WOOL": 2}) == ["SELL", "WOOL", 2], \
        "the shed holds 2, so 2 is the most that can be offered"


def test_milk_is_offered_LESS_when_we_run_fewer_cows():
    """MILK collapses 185 -> 1 because we flood it. 8 cows against 10 means 0.8x, not the shed."""
    assert sell(["SELL", "MILK", 10], {"MILK": 50}) == ["SELL", "MILK", 8], \
        "10 * 8/10 = 8; dumping the shed here is what floors the price"


def test_milk_does_not_dump_the_shed():
    """The explicit contrast with wool. A big milk shed must NOT become a big milk offer."""
    out = sell(["SELL", "MILK", 4], {"MILK": 60})
    assert out == ["SELL", "MILK", 3], "4 * 8/10 = 3.2 -> 3, not 60. got %r" % (out,)


def test_the_last_days_flush_everything_including_milk():
    """Unsold produce is worth zero at the bell, so the final days sell whatever is left."""
    assert sell(["SELL", "MILK", 4], {"MILK": 60}, day=28) == ["SELL", "MILK", 60], \
        "at d28 there is no future price to protect"
    assert sell(["SELL", "WOOL", 4], {"WOOL": 40}, day=28) == ["SELL", "WOOL", 40]


def test_a_crop_sell_is_left_alone():
    """Only animal produce follows the herd. WHEAT has nothing to do with cows or sheep."""
    order = ["SELL", "WHEAT", 12]
    assert sell(order, {"WHEAT": 99}) == ["SELL", "WHEAT", 12]
    assert sell(order, {"WHEAT": 99}, day=28) == ["SELL", "WHEAT", 12], \
        "the flush is animal produce only -- crop cadence is the tape's"


def test_an_empty_shed_drops_the_order():
    """An offer of stock we do not hold is not a sale."""
    assert sell(["SELL", "WOOL", 4], {"WOOL": 0}) is None
    assert sell(["SELL", "MILK", 3], {"MILK": 0}) is None


def test_a_tape_with_no_animals_of_that_species_is_not_divided_by_zero():
    """The melon arm could carry a tape that buys no sheep at all."""
    out = sell(["SELL", "WOOL", 4], {"WOOL": 38}, tape={"COW": 14, "SHEEP": 0})
    assert out == ["SELL", "WOOL", 38], "wool still clears the shed, got %r" % (out,)
    out = sell(["SELL", "MILK", 4], {"MILK": 9}, tape={"COW": 0, "SHEEP": 4})
    assert out == ["SELL", "MILK", 4], "no baseline to scale against -- keep the tape's own number"


def test_an_unchanged_milk_cadence_returns_the_same_object():
    """**Regression guard.** My weed fix broke clean boards by rebuilding untouched objects."""
    order = ["SELL", "MILK", 10]
    out = sell(order, {"MILK": 50}, ours=dict(TAPE_HERD))
    assert out is order, "same herd, mid-season: the tape's own order object must pass through"
