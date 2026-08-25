"""カワシギ lets 42% of his sheep go at the end. We feed every pen to the bell and lose none.

Alex, 2026-08-25: *"match his animals then add something late game - look when they start dying then
if wool = crushed go for the strawberry"*, and then: *"only let the sheep die when the wool has gone
in the shop - if not keep them alive"*.

**The placements already match.** Measured over the 76 post-balance-change tapes that contain him,
our shipped agent against his recorded stream (`data/logs/kawa_arm_old.log`,
`data/logs/kawa_placed.log`):

    his PLACED                    ours (shipped)
      10/4 = 14   41   53.9%        10/4 = 14   44   57.9%
      6/12 = 18   17   22.4%        6/12 = 18   16   21.1%
       6/8 = 14   12   15.8%         6/8 = 14   11   14.5%

What differs is the endgame. He stops feeding sheep and lets them escape
(`kaggriculture.py:817` -- `consecutive_unfed >= 2` replaces the tile with its bare structure).
There is no selling animals in this environment, so an animal leaves the board exactly one way, and
this is therefore deliberate (Alex).

    SHEEP LET GO PER SEAT              BY HOW MANY HE PLACED
       lost  seats   share               placed  seats  mean lost  mean kept
          0      6     7.9%                    4     41       1.71       2.29
          2     44    57.9%                    8     12       3.50       4.50
          4     14    18.4%                   12     17       5.12       6.88
          6     10    13.2%
      mean 2.82                         he keeps 58.1% of the sheep he places

    COWS LET GO PER SEAT:  0 in 76 of 76 seats.

Not a fixed count -- a fixed fraction, ~42%, whatever the herd size. And never a cow.

**Why a sheep and not a cow, without hardcoding the species.** A FEED costs one WHEAT. A SHEEP
produces every 3 days (`interval`), a COW every 2, so a sheep eats half again as much wheat per unit
of product. What decides it is the live book: we flood our own wool -- ladder game 99114898 took
WOOL $239 -> $11 on 57 units -- while milk holds. An animal is worth its ration only while its
product outsells the wheat it eats, and that test names no species.

These tests pin that rule. `_animal_remaining` is deliberately included on the value side because
escape replaces the whole tile dict, destroying `yield_units` along with the animal.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from kagg.search import router as RT                                     # noqa: E402

#: **d27 is his measured stop, not a chosen number.** `scripts/his_last_feed_day.py` over the same
#: 76 seats: his last day with any FEED is d28 in 100% of them, and the pens standing hold flat at
#: 15.01 from d19 all the way to d28 before falling to 12.20 at d29. An escape needs two unfed days
#: (`kaggriculture.py:817`), so the sheep he loses are the ones he stops feeding at d27 -- they miss
#: d27 and d28 and are gone at that rollover. He starves nothing mid-season.
#:
#:     day   feeds   pens   share fed
#:      26   13.45  15.01     89.6%
#:      27    8.47  15.01     56.4%
#:      28    8.72  15.01     58.1%
#:      29    0.00  12.20      0.0%
LATE = 27

#: The book at the close of a season where we flooded our own wool, ladder game 99114898.
WOOL_CRUSHED = 11.0
#: The book where wool held -- game 98428765, seed 1236821574.
WOOL_HEALTHY = 144.0
#: Milk in that same game. Cows are the control: he never starves one.
MILK_HEALTHY = 270.0


def a_sheep(units=0, unfed=1, placed_day=8):
    """A hungry sheep -- one missed feed, so the next miss escapes it."""
    return {"animal": "SHEEP", "yield_units": units, "fed_today": False,
            "consecutive_unfed": unfed, "placed_day": placed_day,
            "fertilizer_available": False, "cared_today": True}


def a_cow(units=0, unfed=1, placed_day=8):
    return {"animal": "COW", "yield_units": units, "fed_today": False,
            "consecutive_unfed": unfed, "placed_day": placed_day,
            "fertilizer_available": False, "cared_today": True}


def feed_prize(ops):
    for op, _item, prize in ops:
        if op == "FEED":
            return prize
    return None


def test_a_sheep_whose_wool_is_crushed_is_not_worth_its_wheat():
    """$11 wool against $25 wheat, three wheat per unit of wool. Let it go.

    This is the whole of Alex's rule: *"only let the sheep die when the wool has gone in the shop"*.
    """
    prize = feed_prize(RT.animal_ops(a_sheep(), LATE, have_wheat=True,
                                     product_price=WOOL_CRUSHED))
    assert prize is None, (
        f"a sheep making $11 wool is still offered a FEED at prize {prize}. It eats three wheat "
        f"per unit of wool, so the ration costs more than the wool it buys.")


def test_a_sheep_whose_wool_still_sells_is_kept_alive():
    """$144 wool pays for its wheat many times over. Feed it. This is the 'if not keep them alive'
    half, and it is the half that makes the rule safe: forcing sheep down cost 27.6 points."""
    prize = feed_prize(RT.animal_ops(a_sheep(), LATE, have_wheat=True,
                                     product_price=WOOL_HEALTHY))
    assert prize is not None and prize >= RT.CRITICAL, (
        f"a sheep making $144 wool was dropped or demoted (prize {prize}). Escape is irreversible "
        f"and this animal still pays for its ration.")


def test_a_cow_is_never_starved():
    """Zero cows lost in 76 of 76 of his seats."""
    prize = feed_prize(RT.animal_ops(a_cow(), LATE, have_wheat=True,
                                     product_price=MILK_HEALTHY))
    assert prize is not None and prize >= RT.CRITICAL, (
        f"a cow was not fed (prize {prize}). He never starves one -- 76 of 76 seats.")


def test_a_cow_whose_milk_is_worthless_is_let_go_like_any_other_pen():
    """**A cow guard was added here and then deleted, and this test records why.**

    カワシギ loses 0 cows in 76 of 76 seats, so a `!= "SHEEP"` guard was added to match him. On the
    13 games available at the time the money read as a null (+228, sem 287). The full 60 paired
    games said otherwise, and the guard was not free:

        what died    games    mean $     sem  richer    cows sheep
        cows only       16      +775     172  14/16      5.3   0.0
        sheep only      16      +715     259  12/16      0.0   3.7
        neither         14      -148     260   6/14      0.0   0.0

    Cow and sheep pay the same per game; the guard deletes the `cows only` bucket outright. Alex,
    shown that table: *"i mean try it - nothing says we cant"*. Matching him is a heuristic for
    winning and not the objective.

    $1 milk is a real board -- game 98335212 closed there while we held three cows.
    """
    prize = feed_prize(RT.animal_ops(a_cow(), LATE, have_wheat=True, product_price=1.0))
    assert prize is None, (
        f"a cow making $1 milk was still fed at prize {prize}. The rule reads the book and names no "
        f"species; a cow that cannot pay for its wheat goes the same way a sheep does.")


#: **The shop gate is NOT implemented and has no test here on purpose.** Alex asked for *"only
#: starve them if the shop is gone"* -- a veto keeping any pen whose product the town can still
#: absorb. It was written as an `absorbable` parameter, never wired to a caller, and deleted unbuilt
#: the same day rather than left as an unreachable branch that reads as done. See
#: `router.pays_for_its_ration` for what building it would take. A test asserting behaviour no code
#: implements is worse than no test: it goes green on the default and pins nothing.


def test_a_sheep_still_holding_crushed_wool_is_kept_until_it_is_shorn():
    """Escape replaces the whole tile dict (`kaggriculture.py:819`), so the standing wool dies with
    the animal. Six units even at $11 is $66 against three wheat, and it must not be thrown away."""
    prize = feed_prize(RT.animal_ops(a_sheep(units=6), LATE, have_wheat=True,
                                     product_price=WOOL_CRUSHED))
    assert prize is not None, (
        "a sheep holding 6 units of wool was dropped; escaping it destroys the wool as well as "
        "the animal, and that wool is still sellable today.")


def test_the_wheat_purchase_stops_too():
    """`will_be_fed` sizes the market's wheat buy off the same predicate (`schedule_agent:4364`).
    A sheep we have decided not to feed must not still have wheat bought for it -- Alex, on the
    seed cap: *"if you dont plant extra you also wouldnt buy the seed for it"*."""
    assert not RT.will_be_fed(a_sheep(), LATE, product_price=WOOL_CRUSHED), (
        "will_be_fed still says yes, so the wheat is bought and underfoot() feeds the pen anyway")
    assert RT.will_be_fed(a_sheep(), LATE, product_price=WOOL_HEALTHY), (
        "will_be_fed refused a sheep whose wool still sells")
