"""The plan interpreter's mechanics, and the two rules that let it play both simulators.

Both of the interesting tests here exist because of a divergence between `kagg.sim` and the
reference environment that the parity gate could not have caught:

- the gate's random scripts only ever move **one** unit, so the reference's atomic PLANT rule --
  drop *every* plant of a crop when the requests exceed the seeds -- was never exercised against
  the simulator's greedy unit-by-unit seed spending;
- the gate never issues a market order list at all in the shape an agent does, so neither the
  10-order cap nor the reference's slot-paired settlement was ever compared.

Both are silent when broken, which is exactly the failure mode `CLAUDE.md` warns about.
"""

import numpy as np

from kagg.search import agent as A
from kagg.search import executor as X
from kagg.search import library, rollout
from kagg.search import plan as P
from kagg.sim.farm import LAND_PRICES
from kagg.sim.game import Actions, Game

SCHEDULE = {3: 0, 6: 1, 9: 7, 12: 2, 15: 6, 18: 3, 21: 5, 24: 4}


def _drive(genomes, steps, weed_chance=0.0, on_turn=None):
    """Play a batch of plans against each other in the simulator, calling `on_turn` each turn."""
    plans = P.decode(genomes)
    game = Game(plans.size, weed_chance=weed_chance, unlock_schedule=SCHEDULE)
    actions = Actions(plans.size)
    for step in range(steps):
        day, hour = step // 24, step % 24
        for player in (0, 1):
            view = rollout.build_view(game, player, day, hour)
            decision = X.decide(view, plans)
            if on_turn is not None:
                on_turn(view, decision, plans)
            rollout._write(actions, player, decision)
        game.step(actions)
    return game


def test_serpentine_order_is_a_permutation_with_unit_steps():
    assert sorted(X.TILE_OF_ORD.tolist()) == list(range(X.TILES))
    for i in range(X.TILES - 1):
        (x0, y0), (x1, y1) = X.ORDER[i], X.ORDER[i + 1]
        assert abs(x0 - x1) + abs(y0 - y1) == 1


def test_never_requests_more_plants_of_a_crop_than_it_holds_seeds():
    """The reference drops ALL of them if it does; the simulator would plant some. Neither is safe."""
    seen = {"plants": 0}

    def check(view, decision, _plans):
        planting = decision.unit_op == 7            # ops.PLANT_OP
        for crop in range(P.N_CROPS):
            asked = (planting & (decision.unit_crop == crop)).sum(axis=1)
            seen["plants"] += int(asked.sum())
            assert (asked <= view.seeds[:, crop]).all(), (crop, asked, view.seeds[:, crop])

    _drive(np.stack([library.melon_wheat(), library.wheat_only()]), 24 * 12, on_turn=check)
    assert seen["plants"] > 200, "no plants requested at all -- the check proved nothing"


def test_a_fallow_tile_is_never_planted():
    """Proves crop assignment is actually read, not merely stored."""
    genomes = np.stack([library.carrot_small(), library.wheat_only()])
    fallow = set(range(X.TILES)) - set(library.nw_quadrant())
    game = _drive(genomes, 24 * 20)

    kinds = game.tiles[0].kind[0][X.TILE_OF_ORD]
    planted_fallow = [i for i in fallow if kinds[i] == X.PLANT]
    assert planted_fallow == []
    # ...and the tiles it *was* told to farm did get used, so the test is not vacuous.
    assert (kinds[library.nw_quadrant()] == X.PLANT).sum() > 5


def _view_with_stock(prices, day=3):
    """A batch-of-two view whose sheds are full, so only the sell rule can suppress an order."""
    return X.View(
        day=day, hour=0,
        kind=np.full((2, X.TILES), X.EMPTY),
        crop=np.full((2, X.TILES), -1),
        planted_day=np.zeros((2, X.TILES), dtype=np.int64),
        watered=np.zeros((2, X.TILES), dtype=bool),
        yield_units=np.zeros((2, X.TILES), dtype=np.int64),
        unit_ord=np.zeros((2, X.MAX_EXEC_UNITS), dtype=np.int64),
        n_units=np.array([1, 1]),
        money=np.array([3000.0, 3000.0]),
        seeds=np.zeros((2, P.N_CROPS), dtype=np.int64),
        shed=np.full((2, P.N_CROPS), 20),
        prices=np.tile(np.asarray(prices), (2, 1)),
        n_land=np.zeros(2, dtype=np.int64),
    )


def test_a_price_floor_above_the_current_price_stops_the_sale():
    blocked = library.genome([library.WHEAT] * X.TILES, floor=1.1, dump_day=999)
    normal = library.genome([library.WHEAT] * X.TILES, floor=0.5, dump_day=999)
    plans = P.decode(np.stack([blocked, normal]))

    at_base = X.decide(_view_with_stock(P.BASE_PRICE), plans)
    assert at_base.sell[0].sum() == 0, "floor above base must block every sale"
    assert at_base.sell[1].sum() > 0, "floor below base must not"

    # ...and the floor is a floor, not a ban: a scarce market lifts the price through it.
    scarce = X.decide(_view_with_stock(P.BASE_PRICE * 1.5), plans)
    assert scarce.sell[0].sum() > 0


def test_the_dump_day_overrides_the_price_floor():
    blocked = library.genome([library.WHEAT] * X.TILES, floor=1.1, dump_day=999)
    dumping = library.genome([library.WHEAT] * X.TILES, floor=1.1, dump_day=20)
    plans = P.decode(np.stack([blocked, dumping]))
    assert int(P.decode(dumping[None, :]).dump_day[0]) == 20
    decision = X.decide(_view_with_stock(P.BASE_PRICE, day=25), plans)
    assert decision.sell[0].sum() == 0
    assert decision.sell[1].sum() == 20 * P.N_CROPS


def test_units_reach_their_tiles_rather_than_deadlocking_against_locked_land():
    """A greedy longer-axis-first route can wedge against a locked quadrant; it must fall back.

    **The profit check is on net worth, not cash.** `money > 3000` was the assertion until 2026-08-04,
    and it is not a stable proxy for "the farm made money" -- buying land converts cash into an asset,
    so a *better* season can end with less in the bank. Measured when hiring became a per-turn count
    (`executor.HIRES_PER_TURN`):

        cap  final cash   peak cash   parcels   plants
          1      $3,550      $3,791         2       50
          3        $205      $3,738         3       63

    Identical earning power; the cap-3 farm simply spent $4,000 on the third parcel that the cap-1 farm
    could never afford, and then owned 63 planted tiles instead of 50. Reading the cash column alone
    reports that as a 94% collapse. This is CLAUDE.md's own warning about a metric that is correct per
    row while its label moves under the thing it describes, so the assertion now counts what the stake
    actually became.
    """
    game = _drive(np.stack([library.wheat_only(), library.wheat_only()]), 24 * 22)
    kinds = game.tiles[0].kind[0]
    assert (kinds == X.PLANT).sum() > 20, "farm is idle -- units are not reaching their tiles"

    cash = float(game.farms[0].money[0])
    parcels = int(game.farms[0].n_land[0])
    spent_on_land = float(np.asarray(LAND_PRICES)[:parcels].sum())
    assert cash + spent_on_land > 3000.0, (
        f"started on $3,000 and finished holding ${cash:,.0f} cash plus {parcels} land parcels "
        f"(${spent_on_land:,.0f}) -- the farm did not turn a profit in any form")


def _recorded(genome, seed):
    """Play a real episode, snapshotting each observation *as the agent saw it*.

    Reading `env.steps[i]["observation"]` afterwards is not the same thing and quietly lies: the
    interpreter mutates the very dicts the recorder holds, so seed counts read back post-planting
    and the hand list read back post-hiring.
    """
    from kaggle_environments import make

    inner = A.make_agent(genome)
    log = []

    def spy(obs, config=None):
        before = {
            "seeds": dict(obs["private"]["seeds"]),
            "hands": len(obs["farms"][obs.get("player", 0)]["hands"]),
        }
        action = inner(obs, config)
        log.append((before, action))
        return action

    env = make("kaggriculture", configuration={"seed": seed}, debug=True)
    env.run([spy, "starter"])
    return log


def test_the_real_environment_agent_emits_a_legal_action_every_turn():
    widest = 0
    for before, action in _recorded(library.melon_wheat(), 77):
        assert set(action) == {"farmer", "hands", "market"}
        assert isinstance(action["farmer"], list) and action["farmer"]
        assert len(action["hands"]) == before["hands"]
        widest = max(widest, len(action["market"]))
        assert len(action["market"]) <= 10, "maxMarketOrdersPerTurn would silently drop orders"

        # **This asserted a fixed slot layout until 2026-08-04** -- sells for all five crops at
        # indices 0..4, zero-quantity ones padded -- on the reasoning that padding keeps the
        # reference's slot-paired settlement aligned with the simulator's. That reasoning was wrong
        # in a way only the end-to-end gate could show: `game._order_book` keeps only positive
        # quantities (`present = c_qty > 0`) and compacts, so a padded list and the simulator
        # disagree the moment anything is truncated. Widening sells from five products to nine took
        # the list to twelve, `reference/kaggriculture.py:534` truncated positionally *before*
        # parsing, HIRE and BUY_LAND fell off every turn, and
        # `tests/test_search_transfer.py` measured sim $29,447 against real $18,953.
        #
        # It is replaced by the invariant that actually has to hold: the list is compacted, in the
        # canonical order, and every entry is a real order. `CLAUDE.md` -- "only end-to-end parity
        # verifies composition"; the transfer test is the authority here, and it fails on padding.
        seen_non_sell = False
        for entry in action["market"]:
            op = entry[0]
            if op in ("SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL"):
                assert int(entry[2]) > 0, f"{entry} is a wasted slot -- `_parse_order` rejects it"
            if op == "SELL":
                assert not seen_non_sell, f"sells must lead the list, found {op} after a non-sell"
            else:
                seen_non_sell = True
        sells = [e[1] for e in action["market"] if e[0] == "SELL"]
        order = [P.CROP_NAMES + P.ANIMAL_PRODUCT_NAMES][0]
        assert sells == sorted(sells, key=order.index), f"sells out of product order: {sells}"
    assert widest <= 10


def test_the_saved_plan_loads_and_plays_a_full_episode():
    """`kagg/search/best_plan.json` is what the arena and any submission would actually run."""
    from kaggle_environments import make

    genome = A.load_best(A.DEFAULT_PLAN)
    assert genome.shape == (P.N_GENES,)
    assert (genome < P.N_CATS).all() and (genome >= 0).all()

    env = make("kaggriculture", configuration={"seed": 91}, debug=True)
    env.run([A.agent, "starter"])
    final = env.steps[-1]
    assert final[0]["status"] == "DONE"
    assert final[0]["reward"] > 3000.0, "the saved plan should at least out-earn doing nothing"


def test_the_real_environment_agent_never_over_requests_plants():
    asked_any = 0
    for before, action in _recorded(library.melon_wheat(), 78):
        demand = {}
        for unit in [action["farmer"], *action["hands"]]:
            if len(unit) >= 2 and unit[0] == "PLANT":
                demand[unit[1]] = demand.get(unit[1], 0) + 1
        for crop, n in demand.items():
            asked_any += n
            assert n <= before["seeds"].get(crop, 0), f"{crop}: asked {n}"
    assert asked_any > 100
