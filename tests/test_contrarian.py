"""Tests for the contrarian agent.

The agent exists to make the opponent pool something other than one strategy wearing eight hats,
so the tests here are mostly about the claims in its docstring: that it is self-contained, that it
routes differently, that it reads the opponent's board, and that its sell floors follow the shape
of each market rather than a calendar.

One of them (`test_buying_land_never_abandons_a_growing_tile`) is a regression test for a bug that
cost the first version most of its money, and it is written the way CLAUDE.md demands: the theory
was stated, the test was written, it failed, and only then was the agent changed.
"""

from pathlib import Path

import pytest
from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.agents import contrarian
from kagg.arena import pool

SIZE = 10
P = contrarian.PARAMS


def make_farm(unlocked=("NW",), plants=()):
    """A board with the given quadrants unlocked and `plants` as (x, y, crop, planted_day)."""
    tiles = [["LOCKED"] * SIZE for _ in range(SIZE)]
    for y in range(SIZE):
        for x in range(SIZE):
            if kg._quadrant_of(x, y, SIZE) in unlocked:
                tiles[y][x] = None
    for x, y, crop, planted_day in plants:
        tiles[y][x] = kg._new_plant(crop, planted_day, 24)
    return {"tiles": tiles, "unlocked_quadrants": list(unlocked), "money": 3000.0,
            "farmer": [4, 4], "hands": []}


# --------------------------------------------------------------------------------------------
# Self-containment: the whole point is that this is not the heuristic with new numbers.
# --------------------------------------------------------------------------------------------

def test_module_imports_nothing_at_all():
    """It must load from a bare path in the arena, in kaggle_environments, or as a submission.

    And it must not reach into `kagg.agents.heuristic`: an opponent built from the thing it is
    meant to be different from is the problem this agent was written to fix.
    """
    lines = Path(contrarian.__file__).read_text().splitlines()
    imports = [ln.strip() for ln in lines if ln.startswith(("import ", "from "))]

    assert imports == []


# --------------------------------------------------------------------------------------------
# Routing: the compact disc, and the bug that made the first version lose.
# --------------------------------------------------------------------------------------------

def test_farmed_tiles_are_the_ones_nearest_the_shed():
    """The routing claim. The heuristic scans rows and takes a prefix instead."""
    shed = contrarian._shed_tiles(SIZE)
    tiles = contrarian._farm_tiles(make_farm(("NW", "NE")), SIZE, 20)

    worst = max(contrarian._shed_distance(t, shed) for t in tiles)
    unfarmed = [
        (x, y) for y in range(SIZE) for x in range(SIZE)
        if kg._quadrant_of(x, y, SIZE) in ("NW", "NE") and (x, y) not in tiles
    ]

    assert len(tiles) == 20
    assert all(contrarian._shed_distance(t, shed) >= worst for t in unfarmed)


def test_buying_land_never_abandons_a_growing_tile():
    """Regression test. This bug cost the first version roughly three quarters of its money.

    Unlocking a quadrant makes tiles *closer* to the shed available, so a plain nearest-N set
    silently drops crops that are already in the ground. They then go unwatered and
    `_daily_refresh_plants` turns them into weeds after two days. Measured in a live episode:
    ten planted tiles left the set when NE was bought on day 7, and ten weeds appeared on day 9.
    """
    far_corner = (0, 0)
    before = make_farm(("NW",), plants=[(*far_corner, "MELON", 0)])
    after = make_farm(("NW", "NE"), plants=[(*far_corner, "MELON", 0)])

    # The premise: without the "plus anything already growing" clause the tile would be dropped.
    nearest_only = contrarian._farm_tiles(make_farm(("NW", "NE")), SIZE, P["max_tiles"])

    assert far_corner in contrarian._farm_tiles(before, SIZE, P["max_tiles"])
    assert far_corner not in nearest_only, "premise gone: the corner is inside the cap now"
    assert far_corner in contrarian._farm_tiles(after, SIZE, P["max_tiles"])


def test_land_is_bought_for_shed_access_not_for_area():
    """One extra quadrant only. A second adds no shed-access tile the farm can reach."""
    assert P["max_extra_quadrants"] == 1
    # Two quadrants already offer more tiles than the farm will ever work.
    assert P["max_tiles"] < 2 * (SIZE // 2) ** 2


# --------------------------------------------------------------------------------------------
# The opponent-reactive branch, which is the thing no dial on the heuristic can express.
# --------------------------------------------------------------------------------------------

def test_melon_is_winner_take_all_which_is_why_the_branch_exists():
    """The measurement the branch is built on, pinned against the live market model."""
    i0 = kg.MARKET_PARAMS["MELON"]["I0"]
    headroom = next(n for n in range(1, 5000) if kg.market_price("MELON", i0 + n) <= 1)

    # A committed player produces ~300 units, so two of them cannot both be paid.
    assert headroom < 200
    # And holding melon earns almost nothing, because its scarcity curve is `log`.
    assert kg.market_price("MELON", i0 - 400) < 1.25 * kg.MARKET_PARAMS["MELON"]["base"]


def test_premium_crop_is_melon_against_an_opponent_who_ignores_it():
    assert contrarian._premium_crop({"WHEAT": 40}, P) == "MELON"


def test_premium_crop_switches_to_strawberry_against_a_melon_opponent():
    """The whole point of reading the opponent's board."""
    melon_farmer = {"MELON": P["melon_opp_tiles"], "WHEAT": 20}

    assert contrarian._premium_crop(melon_farmer, P) == "STRAWBERRY"


def test_the_opening_is_mixed_because_the_opponents_board_starts_empty():
    """Melon goes in on day 0 and the plan moves to strawberry as their commitment appears.

    Measured to matter: a variant hard-wired to strawberry from turn 0 scores 74.5% against the
    eight-member pool where reading the board scores 92.2%, because the early melon cycle is what
    funds the season.
    """
    assert contrarian._premium_crop({}, P) == "MELON"


def test_market_inventory_is_deliberately_not_used_to_detect_a_melon_rival():
    """Regression guard for a rule that made the agent quit melon for having sold melon.

    Melon's `max_yield_day` is 12, so neither player can put one on the market before day 12,
    while the last melon planting that can still ripen goes in around day 17. Any above-I0 melon
    inventory inside the decision window is therefore our own sales. Measured cost of the rule:
    mean bank $39,885 against $45,769, at an identical 92.2% win rate.
    """
    import inspect

    assert "melon_glut_units" not in P
    assert "inventory" not in inspect.signature(contrarian._premium_crop).parameters
    # The premise: melon really cannot be sold before day 12.
    assert kg.CROPS["MELON"]["max_yield_day"] == 12


def test_opponent_incoming_reads_their_board_to_time_a_sale():
    """Front-running needs to know when their crop lands, which the observation makes visible."""
    opp = make_farm(("NW",), plants=[(0, 0, "MELON", 0), (1, 0, "MELON", 0), (2, 0, "WHEAT", 0)])
    ripe_day = kg.CROPS["MELON"]["max_yield_day"]

    early = contrarian._opponent_incoming(opp, day=0, lead=2)
    late = contrarian._opponent_incoming(opp, day=ripe_day - 2, lead=2)

    assert early.get("MELON", 0) == 0
    assert late["MELON"] == 12


# --------------------------------------------------------------------------------------------
# Job priority: water before harvest inside the watering window.
# --------------------------------------------------------------------------------------------

def test_watering_on_the_last_day_of_the_window_still_grants_a_unit():
    """The environment fact the priority is built on.

    `_apply_unit_action` grants the watering bonus while `window_start <= age <= max_yield_day`,
    and HARVEST on a non-ongoing crop clears the tile. So harvesting first on `max_yield_day`
    throws that day's unit away.
    """
    day = kg.CROPS["WHEAT"]["max_yield_day"]
    farm = make_farm(("NW",), plants=[(4, 4, "WHEAT", 0)])
    private = kg._new_private()

    kg._apply_unit_action(farm, private, 0, ["WATER"], SIZE, day, 24)

    assert farm["tiles"][4][4]["yield_units"] > kg._new_plant("WHEAT", 0, 24)["yield_units"]


def test_tile_job_waters_before_harvesting_on_the_last_day_of_the_window():
    tile = kg._new_plant("WHEAT", 0, 24)
    tile["yield_units"] = 3
    ripe_day = kg.CROPS["WHEAT"]["max_yield_day"]

    assert contrarian._tile_job(tile, ripe_day, watered_first=True) == "WATER"
    # Once watered, the same tile is harvested.
    tile["watered_today"] = True
    assert contrarian._tile_job(tile, ripe_day, watered_first=True) == "HARVEST"


def test_tile_job_harvests_first_when_the_watering_window_has_closed():
    tile = kg._new_plant("WHEAT", 0, 24)
    tile["yield_units"] = 4
    past_window = kg.CROPS["WHEAT"]["max_yield_day"] + 1

    assert contrarian._tile_job(tile, past_window, watered_first=True) == "HARVEST"


# --------------------------------------------------------------------------------------------
# Sell floors follow the market curve, not the calendar.
# --------------------------------------------------------------------------------------------

def test_strawberry_is_held_above_base_and_melon_is_dumped_below_it():
    """Opposite behaviour from one code path, chosen from the measured curve shapes."""
    assert P["sell_floor_frac"]["STRAWBERRY"] > 1.0
    assert P["sell_floor_frac"]["MELON"] < 1.0

    i0 = kg.MARKET_PARAMS["STRAWBERRY"]["I0"]
    base = kg.MARKET_PARAMS["STRAWBERRY"]["base"]
    headroom = next(n for n in range(1, 5000) if kg.market_price("STRAWBERRY", i0 + n) <= 1)

    # Strawberry has to be sold into the deficit: there is almost no room above I0, and the
    # scarcity premium there is large. That is what makes holding it correct.
    assert headroom < 100
    assert kg.market_price("STRAWBERRY", i0 - 400) > 2 * base


def test_strawberry_is_held_at_base_price_but_sold_once_drain_has_lifted_it():
    shed = {"STRAWBERRY": 20}
    base = contrarian.BASE_PRICE["STRAWBERRY"]

    at_base = contrarian._sell_orders(shed, {"STRAWBERRY": base}, {}, day=12, p=P)
    lifted = contrarian._sell_orders(shed, {"STRAWBERRY": 3 * base}, {}, day=12, p=P)

    assert at_base == []
    assert lifted == [["SELL", "STRAWBERRY", 20]]


def test_a_full_shed_beats_the_floor_because_the_overflow_is_destroyed():
    """`_drop_inventories_to_shed` discards anything past `shedCapacity`."""
    packed = {"STRAWBERRY": int(contrarian.SHED_CAP * P["shed_panic"]) + 1}

    orders = contrarian._sell_orders(packed, {"STRAWBERRY": 1}, {}, day=12, p=P)

    assert orders and orders[0][0] == "SELL"


def test_a_held_good_is_sold_early_when_the_opponent_is_about_to_glut_it():
    """Front-running: price is a ladder over cumulative inventory, so the first seller wins."""
    shed = {"STRAWBERRY": 20}
    base = contrarian.BASE_PRICE["STRAWBERRY"]
    flood = {"STRAWBERRY": P["front_run_units"]}

    assert contrarian._sell_orders(shed, {"STRAWBERRY": base}, {}, day=12, p=P) == []
    assert contrarian._sell_orders(shed, {"STRAWBERRY": base}, flood, day=12, p=P) != []


def test_everything_is_sold_in_the_endgame_because_stock_scores_nothing():
    orders = contrarian._sell_orders({"STRAWBERRY": 5}, {"STRAWBERRY": 1}, {},
                                     day=P["endgame_day"], p=P)

    assert orders == [["SELL", "STRAWBERRY", 5]]


# --------------------------------------------------------------------------------------------
# Legality, and the pool wiring.
# --------------------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def episode():
    """One full episode, with each action paired to the observation it was chosen from.

    `env.steps[i]["action"]` is the action that produced `env.steps[i]["observation"]`, so it was
    decided from step `i-1`. Pairing them naively makes both tests below fail against a correct
    agent, which is how the off-by-one was found.
    """
    env = make("kaggriculture", configuration={"seed": 5}, debug=True)
    env.run([contrarian.agent, "starter"])
    pairs = [(env.steps[i - 1][0]["observation"], env.steps[i][0]["action"])
             for i in range(1, len(env.steps))]
    return env, pairs


def test_agent_plays_a_full_legal_episode(episode):
    """Invalid actions are silent no-ops in this environment, so illegality hides. Check shape."""
    env, pairs = episode

    for obs, action in pairs:
        assert set(action) == {"farmer", "hands", "market"}
        assert isinstance(action["farmer"], list) and action["farmer"]
        assert len(action["hands"]) == len(obs["farms"][0]["hands"])
        assert len(action["market"]) <= 10
    assert env.steps[-1][0]["reward"] > 3000


def test_never_asks_to_plant_more_seeds_than_it_holds(episode):
    """`interpreter` drops *every* PLANT for a crop when the requests exceed the seeds held."""
    _, pairs = episode

    for obs, action in pairs:
        seeds = obs["private"]["seeds"]
        demand = {}
        for unit in [action["farmer"], *action["hands"]]:
            if len(unit) >= 2 and unit[0] == "PLANT":
                demand[unit[1]] = demand.get(unit[1], 0) + 1
        for crop, n in demand.items():
            assert n <= seeds.get(crop, 0), f"{crop}: asked {n}, held {seeds.get(crop, 0)}"


def test_no_unit_is_ever_left_idle_while_a_tile_needs_work(episode):
    """A cheap check that the compact-routing claim is not costing throughput."""
    _, pairs = episode
    midgame = [(o, a) for o, a in pairs if 5 <= o.get("day", 0) <= 25]
    passes = sum(
        1 for _, a in midgame for unit in [a["farmer"], *a["hands"]] if unit == ["PASS"]
    )
    total = sum(1 + len(a["hands"]) for _, a in midgame)

    assert passes / total < 0.5, f"{passes}/{total} unit-turns idle"


def test_pool_can_build_a_module_spec():
    """Module paths rather than closures, so jobs survive the trip to a worker process."""
    built = pool._build(("module", "kagg.agents.contrarian"), pool.BASELINE)

    assert built is contrarian.agent


def test_module_specs_are_picklable_so_evaluate_can_use_workers():
    import pickle

    spec = pool.OPPONENTS["contrarian"]

    assert pickle.loads(pickle.dumps(spec)) == spec


def test_the_competitive_pool_is_no_longer_one_strategy_in_eight_hats():
    """The reason this agent was written. Every other member is a heuristic override dict."""
    specs = [pool.OPPONENTS[name] for name in pool.COMPETITIVE]
    non_heuristic = [s for s in specs if isinstance(s, tuple) and s[0] == "module"]

    assert "contrarian" in pool.COMPETITIVE
    assert non_heuristic, "pool is still entirely heuristic parameter dicts"


@pytest.mark.parametrize("candidate", [pool.BASELINE, ("module", "kagg.agents.contrarian")])
def test_mirror_follows_whichever_candidate_is_under_test(candidate):
    """`evaluate` has to be able to run a module agent as the candidate, not only as an opponent."""
    assert pool._build(pool.MIRROR, candidate) is not None
