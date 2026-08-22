"""`BUY_ANIMAL COW 2` must survive the bundle. Today it becomes one cow, and no policy can say two.

**The defect this pins.** `bundle_of` emits one `(op, item)` pair per ORDER. `HIRE` five times is
five orders, so its multiplicity survives; `BUY_ANIMAL COW 2` is ONE order carrying a quantity, so
it collapses to a single pair and the 2 is lost. `to_sim_fields` would recover it from a quantities
vector, but the head set is `qty_sell`, `qty_buy_product`, `qty_buy_seed` -- there is no
`qty_buy_animal`, so nothing supplies that number and it defaults to 1.

Measured 2026-08-22 over the four tape teachers: 20 turns of 1451 affected, one of them turn 0.
The student then buys one cow and one sheep where the tape buys two of each -- $900 of $2,984
unspent -- and the hand routed to fetch the second cow finds nothing, PASSes, and desynchronises for
the rest of the day. Unit-op agreement with the student driving was 46/163 = 0.2822, and the top
confusions were `PASS->EAST 7`, `PASS->WEST 7`, `NORTH->PASS 5` -- which reads as a movement failure
and is not one.
`docs/the_second_cow_cannot_be_bought_2026-08-22.md`.

The fix repeats the animal pair per unit, exactly as `HIRE` already is. That needs `bundle_of`,
`quantities_of` and `from_sim_fields` to agree, so all three are pinned here.
"""

import pytest

from kagg.il import market_bundles as MB

TWO_COWS = [["BUY_ANIMAL", "COW", 2]]
THE_OPENING = [["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
               ["BUY_ANIMAL", "COW", 2], ["BUY_ANIMAL", "SHEEP", 2],
               ["BUY_SEED", "WHEAT", 7], ["BUY_SEED", "MELON", 12],
               ["BUY_PRODUCT", "WHEAT", 6]]


def test_two_cows_reach_the_sim_as_two():
    fields = MB.to_sim_fields(MB.bundle_of(TWO_COWS))
    assert fields["buy_animal"][MB.M.ANIMALS.index("COW")] == 2, (
        "the second cow is $400 the student cannot spend, and no head can express it")


def test_the_opening_keeps_both_animals():
    fields = MB.to_sim_fields(MB.bundle_of(THE_OPENING))
    assert fields["buy_animal"][MB.M.ANIMALS.index("COW")] == 2
    assert fields["buy_animal"][MB.M.ANIMALS.index("SHEEP")] == 2
    assert fields["hire"] == 5, "hire multiplicity already worked and must not regress"


def test_one_cow_is_still_one():
    fields = MB.to_sim_fields(MB.bundle_of([["BUY_ANIMAL", "COW", 1]]))
    assert fields["buy_animal"][MB.M.ANIMALS.index("COW")] == 1


def test_an_animal_with_no_quantity_named_is_one():
    """A teacher that names no quantity is naming a single unit -- `to_sim_fields` says so."""
    fields = MB.to_sim_fields(MB.bundle_of([["BUY_ANIMAL", "COW"]]))
    assert fields["buy_animal"][MB.M.ANIMALS.index("COW")] == 1


def test_the_bundle_and_its_inverse_still_agree():
    """`from_sim_fields` is the documented inverse. Repeating on one side only would break it."""
    for orders in (TWO_COWS, THE_OPENING, [["BUY_ANIMAL", "SHEEP", 3]]):
        b = MB.bundle_of(orders)
        assert MB.from_sim_fields(MB.to_sim_fields(b)) == b, orders


def test_quantities_stay_aligned_to_the_bundle():
    """`quantities_of` is documented as aligned to `bundle_of`'s ordering. Repeats must match."""
    for orders in (TWO_COWS, THE_OPENING):
        assert len(MB.quantities_of(orders)) == len(MB.bundle_of(orders)), orders


def test_the_quantities_vector_still_drives_the_other_products():
    """Only animals change. SELL keeps its quantity in a head, not in the bundle's multiplicity."""
    orders = [["SELL", "WHEAT", 9]]
    b = MB.bundle_of(orders)
    assert len(b) == 1, "SELL must stay one pair -- its count lives in qty_sell"
    fields = MB.to_sim_fields(b, MB.quantities_of(orders))
    assert fields["sell"][MB.M.PRODUCTS.index("WHEAT")] == 9


@pytest.mark.parametrize("n", [2, 3, 6])
def test_up_to_the_pasture_limit(n):
    """`max_held` is 6, so six is the most the teacher could ever ask for in one order."""
    fields = MB.to_sim_fields(MB.bundle_of([["BUY_ANIMAL", "COW", n]]))
    assert fields["buy_animal"][MB.M.ANIMALS.index("COW")] == n


# --- the decode side: repeats in the bundle must COALESCE back into one order ---------------------
#
# The bundle repeat alone was not enough, and the audit caught the regression it caused. The turn
# carries at most TEN orders and the teacher's opening uses exactly ten. Emitting `COW 1` twice and
# `SHEEP 1` twice instead of `COW 2` and `SHEEP 2` makes twelve, and the last two -- two HIREs --
# are truncated away. That trades the second cow for two hands, which is worse than the defect.

def _decode(orders):
    vocab = MB.Vocabulary.from_bundles([MB.bundle_of([]), MB.bundle_of(orders)])
    n_products = len(MB.M.PRODUCTS)
    return MB.orders_from_heads(
        vocab, vocab.index(MB.bundle_of(orders)),
        qty_sell=[0] * n_products, qty_buy_product=[0] * n_products,
        qty_buy_seed=[0] * len(MB.F.CROPS),
        products=list(MB.M.PRODUCTS), crops=list(MB.F.CROPS), animals=list(MB.M.ANIMALS))


def test_two_cows_decode_as_one_order_of_two():
    got = [o for o in _decode(TWO_COWS) if o[0] == "BUY_ANIMAL"]
    assert got == [["BUY_ANIMAL", "COW", 2]], (
        "two separate one-cow orders spend two of the turn's ten slots instead of one")


def test_the_opening_still_fits_in_ten_orders():
    got = _decode(THE_OPENING)
    assert len(got) <= 10, "the opening uses all ten slots; anything longer loses its tail"
    assert sum(1 for o in got if o[0] == "HIRE") == 5, "all five hires must survive"
    animals = sorted(o for o in got if o[0] == "BUY_ANIMAL")
    assert animals == [["BUY_ANIMAL", "COW", 2], ["BUY_ANIMAL", "SHEEP", 2]]
