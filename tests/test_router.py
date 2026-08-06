"""Layer 3 tested WITHOUT the game: one farm, a hand-built board, the reference's own op application.

Every previous layer-3 attempt was diagnosed through a 719-turn two-player season against a replay,
which takes ~40 seconds per arm, mixes in the market, the opponent and the schedule, and reports one
number. "FEED landed 29 times against 319" is not a diagnosis, it is a symptom with a dozen possible
causes -- no wheat bought, wheat bought and never drawn, drawn and never delivered, delivered to a pen
that had already starved.

So this file drives `schedule_agent` against a board we wrote by hand, applies its ops with
`kaggriculture._apply_unit_action` and `_daily_refresh_*` -- the reference's own code, so the mechanics
are exact -- and runs no market and no opponent at all. A pen, a unit and some wheat is a five-turn
test that finishes in milliseconds and can only fail for one reason.

`micro()` deliberately does NOT model the market. Anything the farm needs is placed in the shed up
front, which is what makes a failure here unambiguously a routing or execution fault rather than a
purchasing one.
"""

import collections
import importlib.util
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import router as RT
from kagg.search import schedule_agent

REF = pathlib.Path("reference/kaggriculture.py")


@pytest.fixture(scope="module")
def kg():
    spec = importlib.util.spec_from_file_location("_kg_ref", REF)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------------------------
# the micro harness
# ---------------------------------------------------------------------------------------------

def blank_board(unlocked=("NW",)):
    """A 10x10 board with every tile outside `unlocked` set to the string "LOCKED", as the env does."""
    return [["LOCKED" if RT.R.quadrant_of(x, y) not in unlocked else None
             for x in range(10)] for y in range(10)]


def micro(kg, board, sched, days=1, hands=0, shed=None, seeds=None, unlocked=("NW",), trace=None,
          carry=None):
    """Drive our agent on ONE farm for `days` days. No market, no opponent, no purchases.

    Returns `(op_tally, farm, private)`. `trace`, if a list, collects `(day, hour, unit, action)`.
    `carry` presets per-unit inventories, which is how a mid-day replan actually finds the farm.
    """
    farm = {"tiles": board, "money": 100000, "farmer": [4, 4],
            "hands": [list(RT.R.spawn_tile(i + 1)) for i in range(hands)],
            "unlocked_quadrants": list(unlocked)}
    private = {"shed": dict(shed or {}), "seeds": dict(seeds or {}),
               "inventories": [dict((carry or {}).get(i, {})) for i in range(hands + 1)]}
    agent = schedule_agent.make_agent(sched, 0, router=True)
    tally = collections.Counter()
    for day in range(days):
        for hour in range(RT.TPD):
            obs = {"day": day, "hour": hour, "farms": [farm],
                   "private": private, "step": day * RT.TPD + hour}
            act = agent(obs)
            units = [act["farmer"], *act["hands"]]
            for i, a in enumerate(units[:hands + 1]):
                if not (isinstance(a, list) and a):
                    continue
                tally[a[0]] += 1
                if trace is not None:
                    trace.append((day, hour, i, list(a)))
                kg._apply_unit_action(farm, private, i, a, 10, day, RT.TPD, 100)
        kg._daily_refresh_plants(farm, day, RT.TPD)
        kg._daily_refresh_animals(farm, day)
        kg._drop_inventories_to_shed(private, 100)
        farm["hands"] = [list(RT.R.spawn_tile(i + 1)) for i in range(hands)]
    return tally, farm, private


def empty_sched(days=30, **row):
    base = dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                seeds={}, buys={}, sells={}, hands=0)
    return {d: dict(base, **(row if d == 0 else {})) for d in range(days)}


# ---------------------------------------------------------------------------------------------
# the prize model, which is the whole content of the router
# ---------------------------------------------------------------------------------------------

def test_a_melon_water_inside_the_window_is_worth_a_whole_melon():
    """One water inside the window = one unit of yield, so a melon water is the best op in the game."""
    cell = dict(kind="PLANT", crop="MELON", planted_day=0, watered_today=False,
                consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)
    ops = RT.crop_ops(cell, 6, have_fertilizer=False)          # age 6 = (12+1)//2, window opens
    assert [o for o, _i, _p in ops] == ["WATER"]
    assert ops[0][2] == RT.BASE_PRICE["MELON"] == 250


def test_a_melon_water_outside_the_window_is_worth_nothing():
    """Age 5 is one day before the window: watering buys no yield, so it must not be queued."""
    cell = dict(kind="PLANT", crop="MELON", planted_day=0, watered_today=False,
                consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)
    assert RT.crop_ops(cell, 5, have_fertilizer=False) == []


def test_an_ongoing_crop_is_watered_only_to_stop_it_weeding():
    """`_daily_refresh_plants` produces for an ongoing crop regardless of water.

    Water only resets `consecutive_unwatered` and enables the fertilizer bonus, so watering a
    strawberry on a day it is not thirsty is pure walking -- which is the derived reason that watering
    every tile every day measured at -$18,569.
    """
    dry = dict(kind="PLANT", crop="STRAWBERRY", planted_day=0, watered_today=False,
               consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)
    assert RT.crop_ops(dry, 3, have_fertilizer=False) == []
    thirsty = dict(dry, consecutive_unwatered=1)
    assert [o for o, _i, _p in RT.crop_ops(thirsty, 3, have_fertilizer=False)] == ["WATER"]


def test_fertilize_precedes_water_because_water_reads_the_flag():
    """`bonus = 2 if tile["fertilized_until_day"] >= day` is evaluated INSIDE the WATER op.

    So within one visit the order matters, and a router that emits WATER first wastes the fertilizer.
    """
    cell = dict(kind="PLANT", crop="MELON", planted_day=0, watered_today=False,
                consecutive_unwatered=0, yield_units=4, fertilized_until_day=-1)
    ops = [o for o, _i, _p in RT.crop_ops(cell, 12, have_fertilizer=True)]
    assert ops[:2] == ["FERTILIZE", "WATER"], ops


def test_a_hungry_animal_is_mandatory():
    """Two consecutive missed feeds and the animal is gone (`kaggriculture.py:786`)."""
    cell = dict(animal="COW", placed_day=0, fed_today=False, cared_today=False,
                consecutive_unfed=1, fertilizer_available=False, yield_units=0)
    ops = RT.animal_ops(cell, 10, have_wheat=True)
    assert ops[0][0] == "FEED"
    assert ops[0][2] >= RT.MANDATORY
    assert RT.Node((4, 4), ops).mandatory


def test_care_is_only_worth_anything_on_a_fed_day():
    """`pending_care_bonus` accrues only when the animal is cared AND fed."""
    cell = dict(animal="COW", placed_day=0, fed_today=False, cared_today=False,
                consecutive_unfed=0, fertilizer_available=False, yield_units=0)
    assert "CARE" not in [o for o, _i, _p in RT.animal_ops(cell, 10, have_wheat=False)]
    assert "CARE" in [o for o, _i, _p in RT.animal_ops(cell, 10, have_wheat=True)]


def test_fertilizer_threshold_at_the_realised_sale_price_was_measured_null_and_reverted():
    """TRIED: `BASE_PRICE["FERTILIZER"]` (100, nobody pays it) replaced with the mean REALISED sale
    price ($53, `scripts/the_market_ledger.py` on seed 11: 239 units for $12,601) as fertilizing's cost.
    The reasoning holds -- we collect 314 fertilizer-days a season against only 62-67 FERTILIZE ops, so
    almost every unit is headed for a SELL order anyway.

    MEASURED NULL over the 12-seed ladder: identical $109,688, FERTILIZE still 67/season. The only case
    the threshold change touches is an ongoing crop priced between $53 and $100 -- TOMATO at $60 -- and
    this schedule's crop mix is WHEAT/STRAWBERRY/MELON only (`data/seed_scripts/new_leader/schedule.json`
    never plants TOMATO or CARROT). WHEAT's own best one-shot gain is a fixed $50 (2 extra units at
    $25), just under $53, so it is untouched either way. Reverted -- a tie does not beat baseline -- and
    this pins the reverted state so the $53 number is not re-tried against a schedule it cannot move.
    """
    tomato = dict(kind="PLANT", crop="TOMATO", planted_day=0, watered_today=False,
                  consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)
    # age 7: produces tomorrow (first_yield_day=8, interval=1), room=4-0=4 > 1 -- eligible in every way
    # except price, so this isolates the threshold itself.
    ops = RT.crop_ops(tomato, 7, have_fertilizer=True)
    assert "FERTILIZE" not in [o for o, _i, _p in ops], (
        f"tomato fertilized at the un-reverted $53 threshold: {ops}")


def test_a_late_planting_is_worth_nothing_and_must_not_be_pinned():
    """A melon needs to reach age 12, so on day 25 the ground is better left empty than seeded."""
    assert RT.plant_prize("MELON", 5) > 0
    assert RT.plant_prize("MELON", 25) == 0
    assert RT.plant_prize("WHEAT", 25) > 0


# ---------------------------------------------------------------------------------------------
# routing
# ---------------------------------------------------------------------------------------------

def test_a_shared_pasture_was_tried_ranked_by_value_and_measured_a_5676_dollar_loss():
    """TRIED: when COW and SHEEP are both available for one empty `PASTURE`, score each by the same
    `cost + remaining` prize used everywhere else and let the higher one win, instead of always taking
    whichever comes first in `R.ANIMAL_NAMES = ["GOOSE", "COW", "SHEEP"]` (COW, unconditionally).

    The bug this targeted is real: on seed 11, a SHEEP bought day 5 hour 1 was not PLACEd until day 8
    hour 9 -- three days idle in the shed -- because COWs bought later kept winning the single open
    pasture under the fixed order. At day 5 a fresh SHEEP is worth `500 + 6*200 = 1700` against a fresh
    COW's `400 + 8*160 = 1680`, so ranking by value picks SHEEP in exactly that instance.

    MEASURED as a LOSS of **-$5,676** on the 12-seed ladder ($109,688 -> $104,012) once every tied
    pasture across the whole season is decided this way, not just the one example it was diagnosed
    from. The schedule wants 8 COW against 6 SHEEP for the season; a per-turn value tie-break has no
    notion of that mix and reallocates far more pastures than intended. Reverted. This pins the
    reverted (fixed-order) behaviour so the value-ranked version is not re-tried unchanged.
    """
    tiles = blank_board()
    tiles[4][4] = {"kind": "PASTURE"}
    nodes = RT.build_nodes(tiles, day=5, shed={"COW": 1, "SHEEP": 1}, carried={},
                           unlocked={"NW"}, pinned={})
    assert len(nodes) == 1, nodes
    op, item = nodes[0].ops[0]
    assert (op, item) == ("PLACE", "COW"), f"reverted state should still favour COW first: {nodes[0]}"


def test_one_shed_trip_carries_the_whole_days_feed():
    """`PICKUP` is unbounded, so six pens are one draw, not six round trips.

    `n = min(n, available)` then `_inv_add(inv, item, n)` (`kaggriculture.py:340`). Drawing one wheat at
    a time is what made every pen a shed round trip.
    """
    animals = [dict(animal="COW", placed_day=0, fed_today=False, cared_today=False,
                    consecutive_unfed=1, fertilizer_available=False, yield_units=0)
               for _ in range(6)]
    nodes = [RT.Node((x, y), RT.animal_ops(a, 10, have_wheat=True))
             for a, (x, y) in zip(animals, [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)])]
    plan = RT.plan_routes([(4, 4)], nodes, [23])
    assert plan[0]["draw"]["WHEAT"] == 6, plan[0]["draw"]
    assert len(plan[0]["route"]) == 6


def test_the_ratio_beats_both_degenerate_orderings():
    """A cheap near node and an expensive far one: prize/cost takes the near one first, then the far.

    `(rank, distance)` sends every unit at the far node and walks the season away; `(distance, rank)`
    never reaches it. The ratio orders them, which is the whole point of naming this a Team
    Orienteering Problem.
    """
    near = RT.Node((4, 5), [("HARVEST", None, 100.0)])
    far = RT.Node((0, 0), [("HARVEST", None, 900.0)])
    plan = RT.plan_routes([(4, 4)], [near, far], [23])
    assert [n.tile for n in plan[0]["route"]] == [(4, 5), (0, 0)]


def test_the_placement_order_is_a_contiguous_sweep_from_the_shed():
    """Consecutive tiles must be adjacent, so covering n of them costs n-1 steps and no more."""
    order = RT.field_order({"NW"})
    assert len(order) == 24, len(order)                    # 25 tiles less the shed-access cell (4,4)
    assert order[0] in ((3, 4), (4, 3)), order[:3]         # start hard against the depot
    jumps = [(a, b) for a, b in zip(order, order[1:]) if RT.dist(a, b) != 1]
    assert not jumps, f"sweep breaks contiguity at {jumps[:3]}"


def test_placement_beats_the_adjacency_greedy_on_tour_length():
    """The measurement that justifies replacing `_nearest_empty`, on the metric that costs money.

    Both choosers are asked for the same number of tiles on the same empty board; the tour that visits
    what they picked is the thing paid ~20 times a season.
    """
    from kagg.search import schedule_agent as SA
    n = 12
    board = blank_board()
    swept = RT.field_order({"NW"})[:n]

    greedy, taken = [], set()
    for _ in range(n):
        t = SA._nearest_empty(board, {"NW"}, RT.R.SPAWN, skip=taken)
        greedy.append(t)
        taken.add(t)

    swept_len = RT._path_len((4, 4), RT._two_opt((4, 4), swept))
    greedy_len = RT._path_len((4, 4), RT._two_opt((4, 4), greedy))
    assert swept_len <= greedy_len, f"sweep {swept_len} vs adjacency-greedy {greedy_len}"
    assert swept_len == n, f"a contiguous block of {n} should tour in {n} steps, got {swept_len}"


def test_two_opt_shortens_a_crossed_tour():
    seq = [(0, 0), (3, 3), (0, 1), (3, 4)]
    assert RT._path_len((0, 0), RT._two_opt((0, 0), seq)) < RT._path_len((0, 0), seq)


def test_a_route_never_exceeds_the_turn_budget():
    """23 work turns a day. A tour that overruns is a tour whose tail silently never happens."""
    nodes = [RT.Node((x, y), [("HARVEST", None, 500.0)])
             for x in range(5) for y in range(5) if (x, y) != (4, 4)]
    plan = RT.plan_routes([(4, 4)], nodes, [23])
    cost = RT._path_len((4, 4), [n.tile for n in plan[0]["route"]]) + len(plan[0]["route"])
    assert cost <= 23, f"{cost} turns planned into a 23-turn day"


# ---------------------------------------------------------------------------------------------
# execution: the ops must actually LAND, which is the failure this project keeps having
# ---------------------------------------------------------------------------------------------

def test_a_pen_with_wheat_in_the_shed_gets_fed(kg):
    """The whole of the FEED-29-against-319 symptom, as a one-day test.

    A cow on a shed-access cell, wheat in the shed, one unit standing on it. If this does not FEED
    within a day then no amount of season-length measurement will tell us why.
    """
    board = blank_board()
    board[4][4] = kg._new_animal("COW", 0)
    tally, farm, _priv = micro(kg, board, empty_sched(), days=1, shed={"WHEAT": 4})
    assert tally["FEED"] == 1, dict(tally)
    # `_daily_refresh_animals` clears `fed_today` and zeroes `consecutive_unfed` on a fed day, so the
    # counter -- not the flag -- is what proves the FEED actually landed rather than silently no-oped.
    assert farm["tiles"][4][4]["consecutive_unfed"] == 0


def test_a_herd_survives_thirty_days_on_a_stocked_shed(kg):
    """Four pens, plenty of wheat, four hands. Nothing may escape, and that is the whole test.

    `consecutive_unfed >= 2` removes the animal and leaves the structure, so a surviving herd is proof
    the daily loop closes. A season measured 14 pens standing and 1 animal alive.
    """
    board = blank_board()
    for cell in RT.R.shed_access_tiles():
        if RT.R.quadrant_of(*cell) == "NW":
            board[cell[1]][cell[0]] = kg._new_animal("COW", 0)
    board[3][3] = kg._new_animal("COW", 0)
    board[3][4] = kg._new_animal("SHEEP", 0)
    board[4][3] = kg._new_animal("COW", 0)
    tally, farm, _priv = micro(kg, board, empty_sched(), days=10, hands=3,
                               shed={"WHEAT": 400})
    alive = sum(1 for r in farm["tiles"] for c in r if isinstance(c, dict) and "animal" in c)
    assert alive == 4, f"{alive} of 4 animals survived ten days; ops {dict(tally)}"
    assert tally["FEED"] >= 4 * 10 * 0.9, dict(tally)


def test_a_pinned_planting_does_not_drift_between_turns(kg):
    """`_nearest_empty` re-derived the tile every turn, so a plan went stale the turn after it was made.

    The committed-tour port banked $0 with 211 work ops a season for exactly this. A pin must name one
    tile and keep naming it until the board says otherwise.
    """
    sched = empty_sched(plants=["MELON"], seeds={"MELON": 1})
    state = dict(pins={}, planted=collections.Counter())
    board = blank_board()
    first = None
    for turn in range(6):
        pins = schedule_agent._refresh_pins(state, sched, 0, board, {"NW"})
        got = {t for t, v in pins.items() if v[0] == "PLANT"}
        assert len(got) == 1, pins
        first = first or got
        assert got == first, f"turn {turn}: pin moved from {first} to {got}"


def test_feeding_three_pens_costs_exactly_one_shed_trip(kg):
    """The depot stop must be spent ONCE, not re-entered every time an op consumes what it carried.

    Measured in a season: PICKUP 62 on day 0 and FEED 29 for the year. The executor recomputed the
    shortfall as `wanted - inventory`, so a unit that drew three wheat and fed one pen instantly read
    itself as one short and walked back to the shed -- a round trip per pen, which is the very cost the
    unbounded PICKUP exists to avoid.
    """
    board = blank_board()
    for cell in [(3, 3), (3, 4), (4, 3)]:
        board[cell[1]][cell[0]] = kg._new_animal("COW", 0)
    tally, _farm, _priv = micro(kg, board, empty_sched(), days=1, shed={"WHEAT": 9})
    assert tally["FEED"] == 3, dict(tally)
    assert tally["PICKUP"] == 1, f"{tally['PICKUP']} shed trips for three pens: {dict(tally)}"


def test_a_hand_spawned_on_a_locked_shed_cell_walks_to_one_we_own(kg):
    """`_spawn_hand` ignores ownership, so hands wake on `(5,4)`, `(4,5)`, `(5,5)` -- all LOCKED at start.

    `_apply_unit_action` returns on `tile == "LOCKED"` *before* it reaches PICKUP, so a unit that treats
    any shed-access cell as a depot stands there emitting a PICKUP that silently does nothing, forever.
    Observed on day 0 of a real season: 62 PICKUPs, three of five hands dead from hour 2 to hour 23,
    and a herd that then starved because its feed was never drawn.

    Only `(4,4)` is in NW. The other three cost $1,000, $2,000 and $7,000 of land to reach.
    """
    board = blank_board()
    pens = [(0, 0), (0, 4), (4, 0), (2, 2), (1, 3), (3, 1)]
    for x, y in pens:                       # spread, so every unit draws feed rather than one of them
        board[y][x] = kg._new_animal("COW", 0)
    trace = []
    tally, _farm, _priv = micro(kg, board, empty_sched(), days=1, hands=3,
                                shed={"WHEAT": 30}, trace=trace)
    bad = [t for t in trace if t[3][0] == "PICKUP" and t[2] > 0
           and RT.R.quadrant_of(*RT.R.spawn_tile(t[2])) != "NW" and t[1] == 0]
    assert not bad, (f"{len(bad)} PICKUPs emitted from a LOCKED shed cell, "
                     f"first {bad[0]}; a locked tile no-ops before PICKUP is ever reached")
    assert tally["FEED"] == len(pens), dict(tally)


def test_wheat_already_in_a_hand_feeds_the_herd_with_an_EMPTY_shed(kg):
    """A vehicle arrives at the planner with a LOAD, and ignoring it starves the herd.

    Measured on day 3 of a real season: eight wheat carried by the crew, four hungry animals, FEED 0,
    and every one of those animals gone by day 4. The planner costed every pen as needing a shed trip,
    the shed was empty, so the draw was abandoned and the stop dropped -- while another unit stood
    holding the feed. Hands are hired through the morning and each hire forces a replan, so this is not
    an edge case, it is most mornings.
    """
    board = blank_board()
    pens = [(1, 1), (1, 2), (2, 1)]
    for x, y in pens:
        board[y][x] = kg._new_animal("COW", 0)
        board[y][x]["consecutive_unfed"] = 1          # hungry: feed today or they are gone
    tally, farm, _priv = micro(kg, board, empty_sched(), days=1, hands=1,
                               shed={}, carry={1: {"WHEAT": 3}})
    assert tally["FEED"] == 3, dict(tally)
    alive = sum(1 for r in farm["tiles"] for c in r if isinstance(c, dict) and "animal" in c)
    assert alive == 3, f"{alive} of 3 survived with the feed already in hand"


def test_a_purchase_target_is_counted_in_purchases_not_in_livestock():
    """`held` counted `alive` AND `bought`, so every living animal was counted twice.

    The schedule says how many animals to BUY, so the counter has to be how many we have bought. The
    two readings are not close: counting holdings also means "replace anything that escapes", and
    replacing an animal you cannot feed is a deterministic $400-$500 loss that repeats every two days.
    Measured on five seeds, that reading cost **$47,933** and took the greedy arm from 45% of the tape
    to 8%, PLACE going 12 -> 61 a season.

    So the herd shortfall is a FEED problem, and buying more animals is not a fix for it.
    """
    sched = empty_sched(animals_bought={"COW": 3}, places=["COW"] * 3, builds=3)
    agent = schedule_agent.make_agent(sched, 0, router=True)
    board = blank_board()
    farm = {"tiles": board, "money": 100000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {}, "seeds": {}, "inventories": [{}]}
    day0 = agent({"day": 0, "hour": 0, "farms": [farm], "private": priv, "step": 0})
    assert sum(1 for o in day0["market"] if o[0] == "BUY_ANIMAL") == 3, day0["market"]

    # Three bought, three delivered: the target is met and nothing more may be ordered, however the
    # herd fares afterwards.
    priv["shed"] = {"COW": 3}
    again = agent({"day": 1, "hour": 0, "farms": [farm], "private": priv, "step": RT.TPD})
    assert not [o for o in again["market"] if o[0] == "BUY_ANIMAL"], again["market"]

    # One escaped overnight, leaving its pasture. Still no re-order: a beast we cannot feed is a
    # deterministic loss, and the schedule asked for three purchases, not three survivors.
    import importlib.util
    spec = importlib.util.spec_from_file_location("_kg2", REF)
    kg2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kg2)
    priv["shed"] = {}
    board[4][4] = kg2._new_animal("COW", 0)
    board[3][4] = kg2._new_animal("COW", 0)
    board[4][3] = {"kind": "PASTURE"}
    later = agent({"day": 5, "hour": 0, "farms": [farm], "private": priv, "step": 5 * RT.TPD})
    assert not [o for o in later["market"] if o[0] == "BUY_ANIMAL"], later["market"]


def test_the_herds_feed_is_not_sold_out_from_under_it(kg):
    """We bought eleven wheat at hour 0 and sold six of it at hour 1, every day, all season.

    The sell list dumps whatever the shed holds and the schedule asks for `WHEAT: 99`, so the feed
    order and the sell order fought each other one turn apart. Observed on day 13 with eleven animals:

        h0  BUY_PRODUCT WHEAT 11      shed 0 -> 11
        h1  SELL        WHEAT  6      shed 11 -> 0

    which is why `shed WHEAT` read 0 at midday on all thirty days while the bank climbed to $85,000,
    and why the herd decayed from eleven to four. Same shape as the FERTILIZER hold-back already in
    this loop, and missed because wheat is both a crop we grow and the feed we buy.
    """
    board = blank_board()
    for x, y in [(1, 1), (1, 2), (2, 1)]:
        board[y][x] = kg._new_animal("COW", 0)
    sched = empty_sched(sells={"WHEAT": 99})
    agent = schedule_agent.make_agent(sched, 0, router=True)
    farm = {"tiles": board, "money": 5000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {"WHEAT": 5}, "seeds": {}, "inventories": [{}]}
    act = agent({"day": 3, "hour": 0, "farms": [farm], "private": priv, "step": 3 * RT.TPD})
    sold = sum(o[2] for o in act["market"] if o[0] == "SELL" and o[1] == "WHEAT")
    assert sold <= 2, (f"sold {sold} of 5 wheat with three animals to feed; "
                       f"at most the surplus may go: {act['market']}")


def test_hire_survives_the_ten_order_market_cap():
    """`maxMarketOrdersPerTurn` is 10 and the list is TRUNCATED before parsing, HIRE appended last.

    Seeding against the pins rather than today's row raises the order count, so a farm with several
    crops outstanding can push HIRE off the end of the list and never grow a crew. In a season that
    shows up as twelve hands' worth of schedule executed by the farmer alone, which is not a routing
    fault at all and would be invisible in any routing measurement.
    """
    sched = empty_sched(plants=["MELON"] * 3 + ["WHEAT"] * 3 + ["STRAWBERRY"] * 3 + ["CARROT"] * 3,
                        seeds={}, hands=6, sells={p: 99 for p in RT.BASE_PRICE},
                        animals_bought={"COW": 2}, places=["COW", "COW"], builds=2)
    agent = schedule_agent.make_agent(sched, 0, router=True)
    farm = {"tiles": blank_board(), "money": 100000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {p: 50 for p in RT.BASE_PRICE}, "seeds": {}, "inventories": [{}]}
    act = agent({"day": 0, "hour": 0, "farms": [farm], "private": priv, "step": 0})
    assert ["HIRE"] in act["market"], act["market"]


def test_a_melon_reaches_full_yield_and_is_harvested(kg):
    """End to end on one tile: six waters inside age 6-12, then a harvest, 6 units of melon.

    `max_yield` 6 is reachable on plain waters over a seven-day window, which is why fertilizer on a
    melon is only worth a water we are going to miss.
    """
    board = blank_board()
    sched = empty_sched(plants=["MELON"], seeds={"MELON": 1})
    tally, _farm, priv = micro(kg, board, sched, days=14, hands=1, seeds={"MELON": 1})
    assert tally["PLANT"] == 1, dict(tally)
    assert priv["shed"].get("MELON", 0) == 6, priv["shed"]


def test_five_units_share_the_field_instead_of_two_carrying_it():
    """Capacity, not distance, is the scarce resource -- so a plan that idles a unit is never optimal.

    Day 0 of seed 11 pins twenty-one jobs (four pens, seventeen plants) on a twenty-four tile field and
    hires four hands. Sequential cheapest-insertion assigned them `10, 9, 2, 0, 0`: two units loaded to
    21 and 20 turns against a budget of 21, and two units given nothing at all. Six jobs were still
    pinned at dusk and three units sat at PASS for twelve hours.

    The cause is that on a serpentine field the cheapest insertion is always "append to the unit already
    standing on the previous tile" -- delta 2 -- against "send an idle unit from the shed" -- delta 6.
    Ranking on `prize / delta` therefore minimises total WALKING, which is the wrong objective when
    every unit is paid for whether it moves or not. An idle unit's turns cost nothing, so its walk is
    free until it saturates.
    """
    units = [(4, 4)] * 5
    field = [t for t in RT.field_order({"NW"})][:21]
    nodes = [RT.Node(t, [("WATER", None, 25)]) for t in field]
    plan = RT.plan_routes(units, nodes, [21] * 5, depots=((4, 4),))
    sizes = sorted(len(plan[u]["route"]) for u in plan)
    assert sum(sizes) == 21, sizes                       # still serves every job
    assert sizes[0] >= 2, f"a unit was left idle beside pending work: {sizes}"
    assert sizes[-1] <= 7, f"one unit was loaded with the whole field: {sizes}"


def test_the_sell_quota_is_re_offered_every_turn(kg):
    """Pins a standing offer, because BOTH attempts to make selling cleverer lost money on twelve seeds.

    The dump looks obviously wrong -- one season's wool went 123 units sold to 138 while wool REVENUE
    fell $29,041 to $21,811, a mean price of $234 down to $158, so fifteen extra units cost $7,230 --
    and `market_price` really does fall monotonically in inventory (`kaggriculture.py:177`).

        refuse to sell below 0.5 x base price      -$16,025   a floor cancels sales, it does not
                                                              space them; the season ends holding
        cap the quota to a day total, not a turn    -$ 2,653   a standing offer collects the book's
                                                              recovery, a one-shot order does not

    Shops drain inventory every 4 steps and the town centre every 12, at 4x from day 20, so the book
    refills all day. An order is a request that fills one unit at a time and stops when the shed
    empties, so re-offering costs nothing and catches every refill. Leave it alone.
    """
    board = blank_board()
    agent = schedule_agent.make_agent(empty_sched(sells={"WOOL": 4}), 0, router=True)
    farm = {"tiles": board, "money": 3000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    offers = 0
    for hour in range(RT.TPD):
        act = agent({"day": 0, "hour": hour, "farms": [farm], "step": hour,
                     "private": {"shed": {"WOOL": 40}, "seeds": {}, "inventories": [{}]}})
        offers += sum(1 for o in act["market"] if o[:2] == ["SELL", "WOOL"])
    assert offers == RT.TPD, f"the offer stood on {offers} of {RT.TPD} turns"
    """Tried mandatory, measured -$2,804 over twelve seeds, reverted. This pins the reverted state.

    Two dry days and the tile is a WEED, which really is the crop equivalent of an animal walking off,
    and making every FEED mandatory really had cost the field: crops lost to weeds went 7 a season to
    20 against the tape's 17, watering 773 to 704, harvests 322 to 283. Promoting the survival water
    into the mandatory pass fixed exactly that -- harvests back to 318 -- and undid the feeding gain,
    321 down to 301, for a net loss. A pass holding fourteen pens AND every thirsty tile cannot triage;
    the ratio rule has to be allowed to do that job on one side of the line.

    The prize is still the tile's entire remaining value, which is the honest figure. It competes.
    """
    thirsty = dict(kind="PLANT", crop="STRAWBERRY", planted_day=0, watered_today=False,
                   consecutive_unwatered=1, yield_units=0, fertilized_until_day=-1)
    ops = RT.crop_ops(thirsty, 3, have_fertilizer=False)
    assert [o for o, _i, _p in ops] == ["WATER"], ops
    assert 0 < ops[0][2] < RT.MANDATORY, f"survival water at ${ops[0][2]}"
    # A tile that is NOT thirsty must stay silent, or we are back to watering everything every day
    # -- measured at -$18,569.
    assert RT.crop_ops(dict(thirsty, consecutive_unwatered=0), 3, have_fertilizer=False) == []


def test_the_fertilizer_reserve_is_not_held_against_a_field_that_cannot_use_it():
    """A flat hold-back of four blocks the WHOLE sale on any day the shed holds four or fewer.

    Measured on Seb's day 1 (`scripts/first_two_days_all_params.py 11 --days 2`), where his plan and
    ours are otherwise near-identical -- same 17 plants, same 8 pastures, same 7 hires:

        SELL FERTILIZER      ours 0    his 4
        money at dusk      ours $189   his $356

    The gap is $167 and four fertilizer at the realised ~$42 is $168. That is the entire day, and it
    is the day the bank has to start compounding from if the day-4 parcel is ever going to clear.

    The reserve itself is right -- fertilizer applied to a producing tile doubles the yield, and
    dumping the shed every turn is why FERTILIZE never fired at all. What is wrong is that it is
    held unconditionally, against a field with nothing to apply it to. Reserve what the FIELD can
    actually use today, not a constant.
    """
    board = blank_board()
    # Two pens and nothing growing: there is no tile FERTILIZE could be worth anything on.
    board[1][1] = {"kind": "PASTURE"}
    board[1][2] = {"kind": "PASTURE"}
    # `empty_sched` only decorates day 0, and this is a day-1 measurement, so put the quota on
    # every day -- otherwise the assertion passes on an empty row and measures nothing.
    sched = empty_sched()
    for r in sched.values():
        r["sells"] = {"FERTILIZER": 4}
    agent = schedule_agent.make_agent(sched, 0, router=True)
    farm = {"tiles": board, "money": 200, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {"FERTILIZER": 4}, "seeds": {}, "inventories": [{}]}
    act = agent({"day": 1, "hour": 0, "farms": [farm], "private": priv, "step": RT.TPD})
    sold = sum(o[2] for o in act["market"] if o[:2] == ["SELL", "FERTILIZER"])
    assert sold == 4, f"four fertilizer held back from a field with no crop at all: {act['market']}"


def test_the_fertilizer_reserve_still_stands_where_the_field_can_use_it():
    """The other half of the rule: a producing tile keeps its fertilizer off the sell list.

    Dumping the whole shed every turn is what stopped FERTILIZE ever firing, so relaxing the reserve
    must not relax it on the case it was written for.
    """
    board = blank_board()
    for x in range(4):
        board[1][x] = dict(kind="PLANT", crop="STRAWBERRY", planted_day=0, watered_today=False,
                           consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)
    # Ask the prize model which day it actually wants to fertilize on rather than guessing one --
    # picking a day the model is silent about would pass this test while measuring nothing.
    day = next(d for d in range(1, 20)
               if "FERTILIZE" in [o for o, _i, _p in RT.crop_ops(board[1][0], d, True)])
    sched = empty_sched()
    for r in sched.values():
        r["sells"] = {"FERTILIZER": 4}
    agent = schedule_agent.make_agent(sched, 0, router=True)
    farm = {"tiles": board, "money": 200, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {"FERTILIZER": 4}, "seeds": {}, "inventories": [{}]}
    act = agent({"day": day, "hour": 0, "farms": [farm], "private": priv, "step": day * RT.TPD})
    sold = sum(o[2] for o in act["market"] if o[:2] == ["SELL", "FERTILIZER"])
    assert sold == 0, f"sold the fertilizer four producing strawberries want: {act['market']}"


def test_feeding_a_healthy_animal_outranks_a_melon():
    """An unfed animal produces nothing that day, so the feed is not worth one unit of milk.

    Priced at `BASE_PRICE[product]` a cow's FEED is $160 for one turn while a melon water is $250 for
    one turn, so on a tight day the melon wins and the pen is skipped -- and skipping it forfeits the
    day's milk AND the care bonus, because `pending_care_bonus` is only paid out on a day the animal is
    also fed. Across 312 real leaderboard seats FEED correlates +0.452 with final money and WATER
    correlates -0.276; the ratio rule was ranking them the other way round.

    Measured after the feed buffer landed: `FED 285 against 319`, `CARE 285 against 308`.
    """
    pen = dict(animal="COW", fed_today=False, cared_today=False, consecutive_unfed=0,
               yield_units=0, fertilizer_available=False)
    ops = RT.animal_ops(pen, day=5, have_wheat=True)
    assert [o for o, _i, _p in ops] == ["FEED", "CARE"], ops
    assert ops[0][2] >= RT.MANDATORY, f"a healthy animal's feed is optional at ${ops[0][2]}"
    # Without wheat there is nothing to offer, and CARE alone banks nothing on an unfed day.
    assert RT.animal_ops(pen, day=5, have_wheat=False) == []


def test_the_feed_is_bought_with_a_day_of_slack(kg):
    """One wheat per animal per day is the consumption, not the order size -- it leaves no slack.

    Measured over thirty days of seed 11: `FED 291 against 319`, `CARE 290 against 308`, and the herd
    running 315 animal-days against 325. Wool sells at an identical price in both runs ($236 against
    $234) and we still bank $10,575 less of it, so that line is pure volume: animal-days we did not
    work. The shed held 227 wheat-unit-days across the season against the tape's 990.

    A pen is only fed if a unit is CARRYING wheat when it arrives, so every link in shed -> PICKUP ->
    walk -> FEED has to hold on the same turn. Ordering exactly `alive` means any one of them slipping
    is a missed feed, and a missed feed is a lost production day plus a step towards an escape.
    """
    board = blank_board()
    for cell in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1)]:
        board[cell[1]][cell[0]] = kg._new_animal("COW", 0)
    agent = schedule_agent.make_agent(empty_sched(), 0, router=True)
    farm = {"tiles": board, "money": 100000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {"WHEAT": 5}, "seeds": {}, "inventories": [{}]}
    # Sum the WHOLE day. A single turn says nothing: the PICKUP the router emits drains this copy of
    # the shed before the market half reads it, so hour 0 always looks short by exactly the draw.
    ordered = 0
    for hour in range(RT.TPD):
        act = agent({"day": 0, "hour": hour, "farms": [farm], "private": priv,
                     "step": hour})
        ordered += sum(o[2] for o in act["market"] if o[:2] == ["BUY_PRODUCT", "WHEAT"])
    assert ordered >= 10, f"five animals bought {ordered} wheat for the day -- no slack at all"


def test_a_thin_bank_buys_the_feed_it_can_afford_instead_of_none(kg):
    """`money >= 60 * short` is ALL-OR-NOTHING: it cancels the whole order, so the herd eats nothing.

    Measured on Seb's day 1 with four animals and an empty shed. The order is eight wheat (two days'
    slack) at ~$60, so it needs $480 and the bank held $189 -- the guard fired, we bought zero feed,
    and FEED ran 3 against his 5. His shed carried WHEAT 3 all afternoon; ours carried none.

    Starving four animals to protect $189 is the wrong trade in both directions: an escape is a
    deterministic $400-$500 write-off (`kaggriculture.py:786`) and a fed animal produces the same day.
    Buy what the bank covers.
    """
    board = blank_board()
    for x, y in [(1, 1), (1, 2), (2, 1), (2, 2)]:
        board[y][x] = kg._new_animal("COW", 0)
    agent = schedule_agent.make_agent(empty_sched(), 0, router=True)
    farm = {"tiles": board, "money": 189, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {}, "seeds": {}, "inventories": [{}]}
    ordered = 0
    for hour in range(RT.TPD):
        act = agent({"day": 1, "hour": hour, "farms": [farm], "private": priv,
                     "step": RT.TPD + hour})
        ordered += sum(o[2] for o in act["market"] if o[:2] == ["BUY_PRODUCT", "WHEAT"])
    assert ordered >= 3, (f"$189 covers three wheat and four animals are hungry, "
                          f"but the day ordered {ordered}")


def test_a_unit_that_has_finished_carries_the_harvest_home(kg):
    """A tour with no return leg cannot sell anything it picks up until the following dawn.

    Measured against the tape on days 1, 2 and 3 of seed 11: `EAST 0/10, 0/17, 0/15` and
    `SOUTH 0/13, 0/14, 0/14`. Our crew never once walked back towards the shed on three consecutive
    days, while the tape spent 25-30 turns a day doing it and emitted `DROP` 1-2 times daily. Produce
    therefore sat in unit inventories until `_drop_inventories_to_shed` ran overnight, so the day's
    harvest could not be sold on the day it was taken -- and the turns that should have carried it home
    were being spent on PASS anyway.

    DROP moves the WHOLE inventory and must be emitted on a shed-access tile (`kaggriculture.py:325`).
    """
    board = blank_board()
    # Age 5 is past `max_yield_day` 4, so the window is shut and the four units are all it will ever
    # hold: the tile is ready to harvest on turn one and nothing about the day is about watering.
    board[2][2] = dict(kg._new_plant("WHEAT", -5, RT.TPD), yield_units=4)
    tally, _farm, priv = micro(kg, board, empty_sched(), days=1, hands=1)
    assert tally["HARVEST"] == 1, dict(tally)
    assert tally["DROP"] >= 1, f"the harvest was carried around all day: {dict(tally)}"
    # `micro` runs `_drop_inventories_to_shed` after the day, so prove it arrived DURING the day by
    # checking no unit is still holding it at dusk is not enough -- the DROP op above is the evidence.
    assert priv["shed"].get("WHEAT", 0) == 4, priv["shed"]


def test_a_boxed_in_hand_is_not_counted_as_a_vehicle():
    """The third hand of every four wakes on (5,5) and cannot move until a second quadrant is bought.

    Its four orthogonal neighbours are all in locked quadrants, MOVE onto LOCKED is refused, and every
    other op no-ops on the LOCKED tile it stands on. Planning work onto it does not make it slow, it
    deletes the work: the executor drops the stops as unreachable, the unit reads as idle, and the
    top-up hands it the same stops back every turn until dusk.
    """
    assert schedule_agent._mobile((4, 4), {"NW"})            # the farmer, on owned ground
    assert schedule_agent._mobile((5, 4), {"NW"})            # NE shed cell, but (4,4) is one step west
    assert schedule_agent._mobile((4, 5), {"NW"})            # SW shed cell, (4,4) is one step north
    assert not schedule_agent._mobile((5, 5), {"NW"})        # boxed in
    assert schedule_agent._mobile((5, 5), {"NW", "NE"})      # NE bought: (5,4) is now a legal step


def test_the_whole_day_zero_schedule_is_executed(kg):
    """Seventeen plants and four pens are pinned at dawn; all twenty-one must be done by dusk.

    Measured against the tape on day 0: `PLANT 14 of 17`, `BUILD_PASTURE 2 of 4`, `PLACE 2 of 4`, and
    one tile planted but never watered so it weeded overnight. None of that was a schedule, seed or
    money shortfall -- every job was pinned by dawn. It was the crew standing still.
    """
    board = blank_board()
    sched = empty_sched(plants=["WHEAT"] * 10 + ["MELON"] * 7, seeds={}, builds=4,
                        places=["COW", "COW", "SHEEP", "COW"],
                        animals_bought={"COW": 3, "SHEEP": 1})
    tally, farm, _priv = micro(kg, board, sched, days=1, hands=4,
                               shed={"COW": 3, "SHEEP": 1, "WHEAT": 8},
                               seeds={"WHEAT": 10, "MELON": 7})
    assert tally["PLANT"] == 17, dict(tally)
    assert tally["BUILD_PASTURE"] + tally["BUILD_COOP"] == 4, dict(tally)
    assert tally["PLACE"] == 4, dict(tally)
    # Every plant must be watered the day it goes in: a tile is created at `consecutive_unwatered = 1`
    # and weeds at 2, so an unwatered planting is a seed and two turns thrown away.
    assert not any(isinstance(c, dict) and c.get("kind") == "WEED" for r in farm["tiles"] for c in r), \
        "a tile was planted and left unwatered"


def test_a_one_shot_crop_is_not_harvested_while_the_window_is_still_open():
    """HARVEST on a one-shot crop DESTROYS the tile (`kaggriculture.py:409`), forfeiting the rest.

    A wheat's yield window is ages 2-4 and every in-window water is a unit, so the tile is worth three
    waters. The prize model offered HARVEST at `held * price` the moment `held > 0`, which on day 3
    reads as $25 for the harvest against $25 for another water -- and because both sit on the SAME
    node they were both emitted in one visit: water to two units, then harvest and delete the tile.
    Measured on the board, the crop count fell 16 -> 11 on day 3 of seed 11.

    An early harvest is not worth `held * price`, it is worth `held * price` MINUS everything the
    window could still add. Until the window shuts or the tile is full, that number is negative.
    """
    cell = dict(kind="PLANT", crop="WHEAT", planted_day=0, watered_today=False,
                consecutive_unwatered=0, yield_units=1, fertilized_until_day=-1)
    ops = RT.crop_ops(cell, 3, have_fertilizer=False)             # age 3, window is 2-4
    assert [o for o, _i, _p in ops] == ["WATER"], ops
    # Age 4 shuts the window: nothing more can be added, so the harvest is finally free money.
    shut = RT.crop_ops(dict(cell, yield_units=2), 4, have_fertilizer=False)
    assert [o for o, _i, _p in shut] == ["WATER", "HARVEST"], shut


def test_forcing_a_late_one_shot_harvest_on_the_last_day_was_measured_a_92_dollar_loss():
    """TRIED: `_one_shot_is_finished` only checked `age >= max_day`, so a tile planted too late in the
    season for its window to ever CLOSE was never offered HARVEST at all -- WHEAT's window is ages 2-4,
    and a tile planted on day `SEASON_DAYS - 3` reaches only age 2 by the season's last day, so
    `max_day` (age 4) needs a day 30 that does not exist. `plant_prize` already discounts the truncated
    window and correctly still plants it -- a partial wheat still pays -- but the harvest gate carried
    no such discount and simply never fired.

    Diagnosed as real on seed 11 (a tile-lifecycle scan, no monkeypatching, just reading `farm["tiles"]`
    every turn): 32 of 66 wheat plantings (48%) were STILL STANDING, unharvested, at season end, almost
    all of them from day 26-27. The tape's equivalent count is 1 of 66.

    Adding `day >= R.SEASON_DAYS - 1` to `_one_shot_is_finished` MEASURED as a LOSS of **-$92** on the
    12-seed ladder despite HARVEST rising exactly as predicted (296 -> 323 a season) -- a two-day-early
    variant (`- 2`), tested stacked with the PASTURE fix below, lost far more. A forced late-season
    harvest still has to reach the shed (DROP) and clear a SELL order before the game ends to bank
    anything; it does not reliably get there, so the fix mostly converts "still growing, banks $0" into
    "harvested but unsold, banks $0" at the cost of a turn that would have gone to something that
    clears. Reverted. The bug is real; this fix for it is not a net win here.
    """
    cell = dict(kind="PLANT", crop="WHEAT", planted_day=RT.R.SEASON_DAYS - 3, watered_today=True,
                consecutive_unwatered=0, yield_units=2, fertilized_until_day=-1)
    last_day = RT.R.SEASON_DAYS - 1
    age = last_day - cell["planted_day"]
    assert age < RT.CROP["WHEAT"]["max_day"], "the window must still read as OPEN, not naturally shut"
    ops = RT.crop_ops(cell, last_day, have_fertilizer=False)
    assert "HARVEST" not in [o for o, _i, _p in ops], (
        f"reverted state should still leave a still-growing late planting standing: {ops}")


def test_a_wheat_reaches_its_plain_yield_and_is_harvested_once(kg):
    """End to end on one tile: a survival water on the planting day, then ages 2, 3, 4, then a harvest.

    Four is the plain-water ceiling and it is worth being exact about, because two of the four units
    are free: a one-shot crop is created holding `yield_units = 1` (`kaggriculture.py:206`) and the
    window then offers three waters. `max_yield` 6 is reachable only with fertilizer on all three --
    +2 units for a $100 input against $25 wheat, which is why the model declines it.

    Anything under four means the tile was demolished mid-window; the measured value before the fix
    was two.
    """
    board = blank_board()
    sched = empty_sched(plants=["WHEAT"], seeds={"WHEAT": 1})
    tally, _farm, priv = micro(kg, board, sched, days=6, hands=1, seeds={"WHEAT": 1})
    assert tally["PLANT"] == 1, dict(tally)
    assert tally["HARVEST"] == 1, dict(tally)
    assert tally["WATER"] == 4, dict(tally)          # day 0 keeps it alive, days 2-4 are the yield
    assert priv["shed"].get("WHEAT", 0) == 4, priv["shed"]


def test_a_one_shot_crop_is_not_planted_if_its_window_cannot_finish():
    """`plant_prize` gates on `first_yield_day`, which is the wrong end of the crop's life.

    A one-shot crop only banks anything through a HARVEST, and HARVEST is only offered once the yield
    window has shut (`_one_shot_is_finished`). So a wheat needs to reach age `max_yield_day` = 4 with
    a turn left to harvest it, not merely age 2. Gating on `first` planted wheat that could never be
    collected: 32 of 66 wheat plantings sat unharvested at season end against the tape's 1 of 66.

    Each one costs a $10 seed, a PLANT turn and a WATER turn for nothing, and occupies ground.
    """
    last = RT.R.SEASON_DAYS - 1
    assert RT.plant_prize("WHEAT", last - 5) > 0          # sown day 24, age 4 on day 28, a day spare
    # Sown day 26: age 4 lands on day 30 and the season ends on 29, so it can NEVER be harvested --
    # yet `days_left` 2 clears `first_yield_day` 2 and the old rule priced it at $25.
    assert RT.plant_prize("WHEAT", last - 3) == 0
    assert RT.plant_prize("MELON", last - 5) == 0         # melon needs age 12; hopeless this late
    # An ongoing crop is unaffected: it pays from `first_yield_day` onwards and needs no window.
    assert RT.plant_prize("STRAWBERRY", last - 11) > 0
