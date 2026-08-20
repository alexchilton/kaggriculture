"""A bundle index has to become the arrays `jax_sim.Actions` actually carries, and back.

The sim does not take order lists. It takes per-product quantity vectors plus a hire COUNT and a
buy_land flag, and `Game._order_book` compacts those into slots. So the bundle head is only useful
if a bundle round-trips through that representation exactly.

**The hire count is the reason this test exists.** `jax_sim.py:258` documents `hire` as "COUNT of
hands to hire this turn, not a flag", and `:315` warns that "casting to bool here would collapse
'hire twice' to 'hire once'" -- yet `jax_act.to_sim_actions` does exactly that, because the policy's
hire head is `Dense(2)`. The teacher's rank-2 bundle is `HIRE x10` in one turn, 113 times in 5,752
turns. A binary head cannot express it, and that is the d10 failure where units 8 and 9 were never
hired and 20 planned ops died with them.
"""

from kagg.il import market_bundles as MB
from kagg.sim import farm as F
from kagg.sim import market as M


def test_ten_hires_survive_as_ten():
    """The whole point. A count, never a flag."""
    fields = MB.to_sim_fields(MB.bundle_of([["HIRE"]] * 10), None)
    assert fields["hire"] == 10


def test_one_hire_is_not_ten():
    assert MB.to_sim_fields(MB.bundle_of([["HIRE"]]), None)["hire"] == 1


def test_no_hire_is_zero():
    assert MB.to_sim_fields(MB.bundle_of([]), None)["hire"] == 0


def test_sells_land_on_the_right_product_index():
    b = MB.bundle_of([["SELL", "WHEAT", 4], ["SELL", "MILK", 2]])
    fields = MB.to_sim_fields(b, (2, 4))          # quantities follow the bundle's sorted order
    sell = fields["sell"]
    assert len(sell) == M.N_PRODUCTS
    assert sell[M.PRODUCTS.index("MILK")] == 2
    assert sell[M.PRODUCTS.index("WHEAT")] == 4
    assert sum(sell) == 6


def test_seeds_and_products_do_not_bleed_into_each_other():
    b = MB.bundle_of([["BUY_SEED", "WHEAT", 3], ["BUY_PRODUCT", "WHEAT", 5]])
    fields = MB.to_sim_fields(b, None)
    # sorted order is BUY_PRODUCT then BUY_SEED
    assert fields["buy_seed"][F.CROPS.index("WHEAT")] > 0
    assert fields["buy_product"][M.PRODUCTS.index("WHEAT")] > 0
    assert sum(fields["sell"]) == 0


def test_buy_land_is_a_flag_and_survives():
    assert MB.to_sim_fields(MB.bundle_of([["BUY_LAND"]]), None)["buy_land"] is True
    assert MB.to_sim_fields(MB.bundle_of([]), None)["buy_land"] is False


def test_the_sim_fields_round_trip_back_to_the_same_bundle():
    """Labelling reads sim fields; playing writes them. They must agree or the loss trains on a
    different decision than the one the teacher made."""
    for orders in ([["HIRE"]] * 10,
                   [["SELL", "WHEAT", 4], ["SELL", "MILK", 2]],
                   [["BUY_PRODUCT", "WHEAT", 3], ["BUY_SEED", "STRAWBERRY", 1], ["HIRE"], ["HIRE"]],
                   [["BUY_ANIMAL", "COW", 1]],
                   []):
        b = MB.bundle_of(orders)
        fields = MB.to_sim_fields(b, MB.quantities_of(orders) or None)
        assert MB.from_sim_fields(fields) == b


def test_a_missing_quantity_defaults_to_one_not_zero():
    """A zero quantity is a no-op order; the teacher naming no quantity means one unit."""
    fields = MB.to_sim_fields(MB.bundle_of([["SELL", "WHEAT"]]), None)
    assert fields["sell"][M.PRODUCTS.index("WHEAT")] == 1
