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
from kagg.search.schedule_agent import FEED_DAYS

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


def test_a_melon_water_outside_the_window_is_offered_only_on_the_brink():
    """Age 5 is one day before the window: the water buys no YIELD, only survival.

    So it is offered on the day the tile would otherwise weed and on no other day. A tile at
    `consecutive_unwatered = 0` cannot die tonight, and water does nothing else for it.

    **This test previously asserted the opposite** -- a half-price offer every day -- on the strength
    of a table showing "the tape" watering ~1.06 per live tile daily, 18 times on day 1 against our 1.
    That table is the OLD LEADER's tape. Seb's, which is the stronger of the two and the one we match,
    waters on alternate days: d0 17, **d1 0**, d2 17, d3 14, reaching dawn on day 2 with all 17 tiles
    sitting at 1 and taking zero weeds through day 7. `router.py`'s own header had said so all along
    ("water every tile every day" measured at -$18,569); only this branch had drifted.
    """
    cell = dict(kind="PLANT", crop="MELON", planted_day=0, watered_today=False,
                consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)
    slack = RT.crop_ops(cell, 5, have_fertilizer=False)
    assert slack == [], f"a tile watered yesterday must not be offered water: {slack}"

    thirsty = RT.crop_ops(dict(cell, consecutive_unwatered=1), 5, have_fertilizer=False)
    assert thirsty == [("WATER", None, 1500.0)], thirsty


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


def test_a_days_wheat_reserve_was_measured_at_two_days_and_one_day_lost_money():
    """TRIED: `FEED_DAYS = 1`, on the theory that the two-day hold-back blocks the day-4 wheat sale.

    The chain is real -- on Seb's day 4 he sells 49 wheat and we sell 38, and the 11-unit difference
    is exactly our `FEED_DAYS * alive` reserve of 12. That leaves us on $532 against his $1,143, so at
    dawn on day 5 the seed order half-fills (5 strawberry of 10) and five tiles never get planted.

    But halving the reserve is not the fix. Twelve seeds at weedSpawnChance 0.005:

        FEED_DAYS   our schedule   Seb's schedule
            2         $118,761        $92,773
            1         $112,525        $88,817

    -$6,236 and -$3,956. The reserve is not idle capital: it is the slack in shed -> PICKUP -> walk ->
    FEED, and our tours need more of it than his tape does. Reverted; this pins the two.
    """
    assert schedule_agent.FEED_DAYS == 2


def test_counting_field_wheat_as_feed_stock_was_measured_a_31358_dollar_loss():
    """TRIED: count `yield_units` on our own WHEAT tiles towards `on_hand` in the feed order.

    The waste is real. On Seb's day 4 we buy five wheat while `HARVEST 14` is identical in both
    columns -- ~$300 spent on feed already growing in the field, on the day the day-6 parcel has to
    be funded, and he buys one.

    MEASURED over twelve seeds at weedSpawnChance 0.005:

        our schedule   $118,761 -> $87,403     -$31,358
        Seb's schedule $ 92,773 -> $54,419     -$38,354

    Owned is not AVAILABLE. Standing wheat needs a HARVEST, a DROP and a walk, and most of the
    season's wheat is still growing, so counting it silences the feed order and the herd starves --
    the same shape as the $47,933 replace-what-escapes mistake. The feed chain needs stock that can be
    picked up THIS turn: the shed and the crew, nothing else. This pins the reverted state.
    """
    board = blank_board()
    for x in range(4):
        board[1][x] = dict(kind="PLANT", crop="WHEAT", planted_day=0, watered_today=True,
                           consecutive_unwatered=0, yield_units=4, fertilized_until_day=-1)
    board[3][3] = dict(kind="PASTURE", animal="COW", fed_today=False, cared_today=False,
                       last_fed_day=0, produce_ready=False)
    agent = schedule_agent.make_agent(empty_sched(), 0, router=True)
    farm = {"tiles": board, "money": 5000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {}, "seeds": {}, "inventories": [{}]}
    ordered = 0
    for hour in range(RT.TPD):
        act = agent({"day": 6, "hour": hour, "farms": [farm], "private": priv,
                     "step": 6 * RT.TPD + hour})
        ordered += sum(o[2] for o in act["market"] if o[:2] == ["BUY_PRODUCT", "WHEAT"])
    assert ordered > 0, (f"the feed order went silent with sixteen units of our own wheat standing "
                         f"in the field -- that arm measured -$31,358 and must stay reverted")


def test_the_feed_budget_uses_the_live_quote_not_a_hardcoded_sixty(kg):
    """WHEAT's `I0` is 10,000, so its price runs from $25 at the season's open toward $125 as the book
    drains (`kaggriculture.py:177`), and the observation carries the live quote in
    `obs["market"]["prices"]`. Budgeting the feed order at a hardcoded $60 is therefore wrong in both
    directions at once: it under-buys by 2.4x on an open book and over-orders by 2x on a drained one.

    Six animals want twelve wheat. At the opening quote of $25 that is $300, and at most half the bank
    goes on feed, so $600 buys all twelve -- not the five that $600 // 60 // 2 allows.

    The half-bank cap is deliberate and measured. Feed is a recurring daily cost and seed, pens and
    land are the one-offs that compound, so committing the whole bank to feed on a cheap book starves
    them. The hardcoded $60 was doing this by accident on an open book; twelve seeds at
    weedSpawnChance 0.005 say to keep the throttle and fix the price:

        $60 flat                 our $118,761   Seb $92,773
        live quote, no cap       our $112,913   Seb $96,328
        live quote + half bank   our $119,281   Seb $96,064
    """
    board = blank_board()
    for x, y in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)]:
        board[y][x] = kg._new_animal("COW", 0)
    agent = schedule_agent.make_agent(empty_sched(), 0, router=True)
    # **$150, not $600, and that is forced by `FEED_ORDER_CAP`.** This test needs the BUDGET to be
    # what limits the first order, and at $600 the live quote allows twelve while the cap allows four,
    # so the order reads 4 whichever price is used and discriminates nothing. Summing the day instead
    # is vacuous for the reason this test was tightened once already: a hand-built obs never debits
    # the bank, so `money * 0.5 // quote` is recomputed intact every turn and the `ordered` retry
    # reaches twelve over three turns under $60 as well.
    #
    # Half of $150 is $75, which buys THREE wheat at the live $25 and ONE at the hardcoded $60. Both
    # sit under the cap, so the first order still separates the two budgets.
    farm = {"tiles": board, "money": 150, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {}, "seeds": {}, "inventories": [{}]}
    market = {"prices": {"WHEAT": 25}, "inventory": {"WHEAT": 10000}}
    act = agent({"day": 1, "hour": 0, "farms": [farm], "private": priv,
                 "market": market, "step": RT.TPD})
    ordered = sum(o[2] for o in act["market"] if o[:2] == ["BUY_PRODUCT", "WHEAT"])
    assert ordered == 3, (f"half of $150 buys three wheat at the live quote of $25, but the turn "
                          f"ordered {ordered} -- the budget is still the hardcoded $60")


def test_an_animal_drawn_from_the_shed_is_placed_the_same_day(kg):
    """The cow rode around in a pocket all day and was dropped back home unplaced.

    Seed 11, day 4 on Seb's plan, per turn:

        h1   shed{COW: 1}       bought and settled
        h3   carry{COW: 1}      a unit DREW it for a PLACE
        h12  carry{COW: 1}      still carried, through fifteen other jobs
        h19  shed{COW: 1}       dropped back home, never placed

    Two empty pastures stood free the whole day, and the tape places its cow the same day: `PLACE 0
    against 1`, `tile:animal 6 against 7`. An animal in a pocket produces nothing, eats nothing and
    cannot be cared for, so a whole animal-day is lost -- and FEED/CARE are the two ops that correlate
    hardest with money on the leaderboard.

    **This test does NOT reproduce it.** Written three ways -- cow in the shed at dawn, cow arriving at
    hour 1 after the routes were planned, and the same on an eight-unit farm with six mandatory feeds
    and a field of ripe melons -- the executor places it every time. So the season failure needs some
    condition this board does not have, and the "carried all day" reading of the per-turn dump is not
    yet a diagnosis: the COW leaves the carry around h13 and is back in the shed by h19, which is also
    consistent with the return leg walking it home and DROPping it unplaced.

    Kept as a guard on the path that does work, so a future change to the draw-and-place handoff cannot
    silently break the case that is currently correct.
    """
    board = blank_board()
    board[1][1] = {"kind": "PASTURE"}
    board[1][2] = {"kind": "PASTURE"}
    # Match day 4: six animals already on the board, every one of them a MANDATORY feed, plus a field
    # of ripe melons. The PLACE has to compete with all of it rather than being the only job going.
    for x, y in [(4, 4), (5, 4), (4, 5), (3, 4), (4, 3), (3, 3)]:
        board[y][x] = kg._new_animal("COW", 0)
    for x in range(0, 4):
        board[0][x] = dict(kind="PLANT", crop="MELON", planted_day=0, watered_today=False,
                           consecutive_unwatered=0, yield_units=0, fertilized_until_day=-1)
    # The cow arrives at hour 1, NOT at dawn -- BUY_ANIMAL settles during the turn, so the day's
    # routes were planned on a shed that had no cow in it. Handing it over at dawn passes already;
    # the whole failure is that the plan is a day old by the time the animal exists.
    farm = {"tiles": board, "money": 100000, "farmer": [4, 4],
            "hands": [list(RT.R.spawn_tile(i + 1)) for i in range(7)],
            "unlocked_quadrants": ["NW"]}
    private = {"shed": {"WHEAT": 20}, "seeds": {}, "inventories": [{} for _ in range(8)]}
    agent = schedule_agent.make_agent(empty_sched(), 0, router=True)
    tally = collections.Counter()
    for hour in range(RT.TPD):
        if hour == 1:
            private["shed"]["COW"] = 1
        act = agent({"day": 0, "hour": hour, "farms": [farm], "private": private, "step": hour})
        for i, a in enumerate([act["farmer"], *act["hands"]][:8]):
            if isinstance(a, list) and a:
                tally[a[0]] += 1
                kg._apply_unit_action(farm, private, i, a, 10, 0, RT.TPD, 100)
    placed = sum(1 for r in farm["tiles"] for c in r if isinstance(c, dict) and "animal" in c)
    assert placed == 7, (f"a cow that arrived at hour 1 was never placed -- ops: {dict(tally)}, "
                         f"carried at dusk: {[iv for iv in private['inventories'] if iv]}")


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

    **FIVE waters, not four, and the fifth one is waste.** Wheat's window is ages 2-4, so the day-1
    water added by the every-day survival offer buys no yield whatever -- the tile is watered on 2, 3
    and 4 regardless and could never have reached `consecutive_unwatered >= 2`. The yield is
    unchanged at 4 units, so the cost is one turn on a short-window crop.

    That is a real and accepted cost of matching the tape's watering cadence, priced here rather than
    hidden: on a one-tile board with an idle hand the offer is always taken, while in a season it
    competes for the tour. The refinement that would remove it -- offer the early water only when the
    tile could actually weed before its next in-window water is due -- is NOT implemented.
    """
    board = blank_board()
    sched = empty_sched(plants=["WHEAT"], seeds={"WHEAT": 1})
    tally, _farm, priv = micro(kg, board, sched, days=6, hands=1, seeds={"WHEAT": 1})
    assert tally["PLANT"] == 1, dict(tally)
    assert tally["HARVEST"] == 1, dict(tally)
    assert tally["WATER"] == 5, dict(tally)   # day 0 survival, day 1 waste, days 2-4 the yield
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


def test_the_feed_order_is_never_capped_below_the_herds_daily_need(kg):
    """PINNED NEGATIVE. Capping one BUY_PRODUCT to meter the day's buying STARVES a large herd.

    The motivating measurement is real and still unfixed: on day 0 the leader places sixteen
    BUY_PRODUCT WHEAT of 1-6 across h1-h22 interleaved with ten SELLs -- 41 orders over 18 of the 24
    hours -- against our 12 orders over 4 hours, and `market_price` moves with every unit so a block
    order walks itself up the curve (`kaggriculture.py:177`).

    But `FEED_ORDER_CAP = 4` is the wrong instrument. It shrinks the ONE order rather than adding
    orders, and a ceiling below the herd's daily need can never fund it. Seb runs 19 animals = 38
    wheat a day at `FEED_DAYS = 2`. Animals in pens, seed 11, Seb's schedule:

        day        14   15   16   17   20   25   29
        cap = 4    14   12    7    8    8    8    8
        no cap     15   17   17   17   17   17   17

    The herd starved from day 15 and never came back, and because `COLLECT_FERTILIZER` is one op per
    animal per day it took the fertilizer chain with it -- 233 collected against the tape's 379.

    Fixing the cadence means MORE orders at full size, never a smaller order.
    """
    board = blank_board()
    for i in range(11):
        board[i // 5][i % 5] = kg._new_animal("COW", 0)
    agent = schedule_agent.make_agent(empty_sched(), 0, router=True)
    farm = {"tiles": board, "money": 100000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    priv = {"shed": {}, "seeds": {}, "inventories": [{}]}
    act = agent({"day": 13, "hour": 0, "farms": [farm], "private": priv,
                 "step": 13 * RT.TPD})
    ordered = sum(o[2] for o in act["market"] if o[:2] == ["BUY_PRODUCT", "WHEAT"])
    assert ordered == FEED_DAYS * 11, (
        f"eleven animals need {FEED_DAYS * 11} wheat and the order asked for {ordered}; "
        f"a cap here starves the herd: {act['market']}")


def test_a_sell_row_that_landed_on_an_empty_shed_is_recovered_later(kg):
    """`sells` was the last per-day target in this file; every other one is already cumulative.

    `plants`, `builds` and `animals_bought` were each converted to "what the schedule has asked for
    through today, minus what I have actually done", every time for the same reason: a row that
    could not be filled on the day it appeared was silently forfeited and never retried.

    Measured on Seb's tape, seed 11, and it is the largest single divergence left. He sells
    `MELON: 18` on day 10 and asks for no melon again until day 16. Our melons ripen one day later,
    so the day-10 row fires against an EMPTY shed and days 11-15 ask for zero -- we hold exactly
    those 18 melons from day 11 to day 15 with **$2 in the bank**, cannot afford the $4,000 third
    parcel until day 16, and farm 25 fewer tiles for six days. The plant deficit tracks it almost
    unit for unit (-26 plants against -25 tiles on day 12), and that is where the harvest gap and
    everything downstream of it comes from.
    """
    board = blank_board()
    agent = schedule_agent.make_agent(empty_sched(sells={"MELON": 18}), 0, router=True)
    farm = {"tiles": board, "money": 3000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    act = agent({"day": 3, "hour": 0, "farms": [farm], "step": 3 * RT.TPD,
                 "private": {"shed": {"MELON": 18}, "seeds": {}, "inventories": [{}]}})
    offered = [o for o in act["market"] if o[:2] == ["SELL", "MELON"]]
    assert offered == [["SELL", "MELON", 18]], (
        f"day 0 asked for 18 melons against an empty shed; by day 3 the shed holds them and the "
        f"offer must still stand: {act['market']}")


def test_a_carried_sell_row_never_offers_more_than_the_biggest_day_ever_asked(kg):
    """The carry recovers a MISSED row; it must not become a licence to dump the shed.

    `market_price` falls monotonically in inventory and a SELL walks n units down that curve one at
    a time, so a bigger offer clears at a worse mean price -- measured as wool 123 units -> 138 for
    REVENUE $29,041 -> $21,811. The per-offer rate is the thing
    `test_the_sell_quota_is_re_offered_every_turn` protects, so the carry is capped at the largest
    single day the schedule ever asks for. Two missed rows of 5 may be recovered, but only 5 at a
    time, over as many turns as it takes.
    """
    sched = empty_sched()
    sched[0]["sells"] = {"MELON": 5}
    sched[1]["sells"] = {"MELON": 5}
    agent = schedule_agent.make_agent(sched, 0, router=True)
    farm = {"tiles": blank_board(), "money": 3000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    act = agent({"day": 3, "hour": 0, "farms": [farm], "step": 3 * RT.TPD,
                 "private": {"shed": {"MELON": 20}, "seeds": {}, "inventories": [{}]}})
    offered = [o for o in act["market"] if o[:2] == ["SELL", "MELON"]]
    assert offered == [["SELL", "MELON", 5]], (
        f"two rows of 5 went unfilled, but the offer rate stays 5: {act['market']}")


def test_the_crew_is_bought_before_the_goods_when_the_bank_can_only_cover_one():
    """HIRE is appended LAST, after SELL/LAND/ANIMAL/SEED/FEED have already debited `money`.

    Measured on Seb's tape, seed 11. `scripts/when_the_crew_arrives.py` prints the hour each HIRE was
    sent and the bank at that moment. Day 6 we open on $711 against his $869, want 8 hands, and go:

        ours  (0,$711) (0,$711) (1,$10) (1,$10) (2,$5) (2,$5) (3,$0) (3,$0)
        tape  (0,$869) x8

    The bank is gone by hour 1 -- not spent on hands, spent on seed and feed between our first pair of
    hires and our third -- so six of the eight HIREs fail outright and the day is worked by five hands
    instead of eight. 135 unit-turns against his 208. `_hire_cost` is `mult * fib(hires_today)` and
    `hires_today` is a per-DAY counter, so the crew costs exactly the same whenever it is bought: there
    is no saving in dribbling, only a bank that a later order can empty first.

    A hand hired at hour 0 works 23 turns. Nothing downstream recovers a turn that was never available,
    which is why this sits ahead of every routing question.
    """
    sched = empty_sched(hands=4, seeds={"MELON": 6}, plants=["MELON"] * 6)
    agent = schedule_agent.make_agent(sched, 0, router=True)
    farm = {"tiles": blank_board(unlocked=("NW", "NE")), "money": 400, "farmer": [4, 4],
            "hands": [], "unlocked_quadrants": ["NW", "NE"]}
    priv = {"shed": {}, "seeds": {}, "inventories": [{}]}
    act = agent({"day": 0, "hour": 0, "farms": [farm], "private": priv, "step": 0})
    hires = [o for o in act["market"] if o[0] == "HIRE"]
    seeds = [o for o in act["market"] if o[0] == "BUY_SEED"]
    assert len(hires) == 4, f"wanted the whole crew first, got {len(hires)}: {act['market']}"
    assert act["market"].index(hires[0]) < (act["market"].index(seeds[0]) if seeds else 99), \
        f"HIRE must precede BUY_SEED in the list: {act['market']}"


def test_a_claim_is_released_when_an_idle_unit_would_arrive_far_sooner():
    """A claimed tile was off limits for the rest of the day, however far off its claimant was.

    Measured on Seb's tape, seed 11, day 0. A PLACE node is available from hour 9, and replans DO run
    -- at hours 9, 14, 15, 16, 17 and 18. The work was visible and the planner was running the whole
    time. The pen was simply claimed at hour 6 by a unit with a long tour, and

        busy = {n.tile for u, st in routes.items() if u not in idle for n in st["route"]}

    subtracts every claimed tile from what an idle unit is allowed to take. So the animal waited for
    its claimant and was placed at **hour 18**, by which point it cannot be fed: the shed is four moves
    off and the budget at hour 20 is `24 - 20 - 1 = 3`. That is `feed -2` and `care -2` on day 0.

    Same shape as the `sells` bug: a decision taken when the board looked one way outliving the board.
    A claim is only worth honouring while the claimant is the one who arrives first.
    """
    class N:
        def __init__(self, tile, service=1):
            self.tile, self.service = tile, service

    #   unit 0 (committed) starts at the shed (4,4) and tours (4,3) -> (0,0) -> (0,4).
    #   walking its own tour in order:  (4,3) at turn 2,  (0,0) at turn 10,  (0,4) at turn 15.
    #   unit 1 (idle) stands at (0,3): 4 from (4,3), 3 from (0,0), 1 from the pen at (0,4).
    units = [(4, 4), (0, 3)]
    routes = {0: {"route": [N((4, 3)), N((0, 0)), N((0, 4))]}}
    idle = [1]
    busy = schedule_agent._claimed_tiles(units, routes, idle, margin=4)

    assert (0, 4) not in busy, \
        "unit 1 is one step from the pen and unit 0 is 15 turns off -- the claim must be released"
    assert (4, 3) in busy, \
        "unit 0 reaches (4,3) on turn 2 and unit 1 is 4 away, so that claim stands"
    assert (0, 4) in schedule_agent._claimed_tiles(units, routes, idle, margin=None), \
        "margin=None must restore the old all-claims-are-permanent rule exactly"

    # A head start inside the margin is not enough to break up a tour: claimant arrives on turn 2,
    # the idle unit is 2 away, so it wins by nothing once the margin is applied.
    near = schedule_agent._claimed_tiles([(2, 0), (3, 0)], {0: {"route": [N((1, 0))]}}, [1], margin=4)
    assert (1, 0) in near, "a 2-turn head start is inside the margin; the claim should stand"


def test_seb_day_zero_places_every_animal_early_enough_to_feed_it():
    """Replans fire on a CREW change or an idle unit -- never on new work appearing.

    Pinned against the real tape rather than a hand-built board, because three synthetic versions of
    this all passed: `micro` gives every unit a short tour, so a unit falls idle almost at once and the
    idle top-up covers the bug. It only bites when the crew is fully committed for hours at a stretch.

    Measured on Seb's tape, seed 11, day 0, by spying on every `plan_routes` call:

        hr  9  1 unit,  1 node,  PLACE offered=[]          <- the one free pen was excluded as claimed
        hr 10-13   NO CALL AT ALL                          <- pens 3,4,5 become placeable in here
        hr 14  2 units, 5 nodes, PLACE offered=[5] assigned=[4]
        hr 16  3 units, 3 nodes, PLACE offered=[3] assigned=[]   budget 7, a shed trip costs more

    The crew is stable at 8 from hour 6 and every unit has crop work, so nothing goes idle and nothing
    replans while four pens sit empty and four animals ride around in unit inventories. By the time a
    unit does fall idle the budget is `24 - hour - 1` and a PLACE needs a shed trip, so the node is
    offered and cannot be afforded. The last two animals land at hour 18 and are never fed:

        ours   PLACE [3, 6, 18, 18]   FEED [6, 11]         CARE [7, 12]
        tape   PLACE [4, 6, 11, 13]   FEED [9, 11, 17, 19] CARE [12, 17, 20, 20]

    which is `feed -2` / `care -2` on day 0 against the tape.

    Two theories were measured and rejected on the way here, recorded so they are not retried: tour
    ORDERING is not the constraint, because the node is not in any tour to be ordered; and claim
    exclusion is not sufficient -- `STEAL_MARGIN` moved one placement 18 -> 16 and left feed and care
    untouched. The trigger has to include the work, not just the workers.
    """
    import json
    import pathlib as _pl
    from kaggle_environments import make

    replay = "data/seed_scripts/top_guys/90494364.json"
    schedule = "data/seed_scripts/top_guys/90494364/schedule.json"
    team = "Seb (allegedly)"
    tape_only = ("plant_tiles", "build_tiles", "land_turns", "orders")

    d = json.loads(_pl.Path(replay).read_text())
    seat = d["info"]["TeamNames"].index(team)
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]
    sched = {int(k): v for k, v in json.loads(_pl.Path(schedule).read_text()).items()}
    thin = {k: {a: b for a, b in v.items() if a not in tape_only} for k, v in sched.items()}

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = schedule_agent.make_agent(thin, 0, router=True)
    placed, fed = [], []
    for t in range(24):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0 = agent(o0)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        for x in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if x and x[0] == "PLACE":
                placed.append(t)
            if x and x[0] == "FEED":
                fed.append(t)
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": acts[t]["farmer"], "hands": list(acts[t]["hands"])[:n1],
                   "market": acts[t]["market"]}])

    assert len(placed) == 4, f"the schedule places four animals on day 0; got {placed}"
    assert max(placed) <= 13, (
        f"last PLACE at hour {max(placed)} (tape: 13). A shed round trip is ~8 turns against a budget "
        f"of 24-hour-1, so an animal placed this late can never be fed. PLACE {placed}, FEED {fed}")
    assert len(fed) >= 4, f"every animal placed should be fed the same day; PLACE {placed}, FEED {fed}"


def test_a_placement_late_in_the_day_is_worth_less_than_one_at_dawn():
    """`PLACE` is priced at `cost + remaining` whatever the hour, and that flat price is the real bug.

    An animal placed at hour 6 is fed, cared for and starts its production clock the same day. One
    placed at hour 18 gets none of that: a FEED needs a shed round trip of about eight turns against a
    budget of `24 - hour - 1`, so it stands unfed and uncared until tomorrow. Measured on Seb's tape,
    seed 11, day 0, where our last two animals land at hour 18 -- `feed -2` and `care -2`.

    Because the price does not move, the planner has no reason to serve the node early. Forcing it to
    (an `URGENT_OPS` replan trigger) simply made it outbid something else: PLANT fell 17 -> 16 and
    `test_the_whole_day_zero_schedule_is_executed` went red. That is the coupling -- work, route and a
    bank that all draw on the same turns -- and it cannot be resolved by forcing an op whose stated
    value is a lie.

    Pricing the hour in resolves both directions at once: an early placement wins on merit, and a late
    one correctly loses to a plant instead of being forced through.
    """
    pen = [[{"kind": "PASTURE"}]]
    shed = {"COW": 1}

    early = RT.build_nodes(pen, day=0, shed=shed, carried={}, unlocked=("NW",), pinned={}, hour=2)
    late = RT.build_nodes(pen, day=0, shed=shed, carried={}, unlocked=("NW",), pinned={}, hour=20)
    assert early and late, "the pen is placeable at both hours; only the price should move"
    assert early[0].prize > late[0].prize, (
        f"a dawn placement must outprice a dusk one: {early[0].prize} vs {late[0].prize}")

    # And the default must be unchanged, so every existing caller and every pinned number still holds.
    same = RT.build_nodes(pen, day=0, shed=shed, carried={}, unlocked=("NW",), pinned={})
    assert same[0].prize == early[0].prize, "omitting `hour` must price as the start of the day"


def test_only_the_one_genuinely_walled_spawn_slot_is_skipped_and_hiring_continues():
    """The spawn guard stopped hiring at the first walled slot, throwing away four good hands with it.

    Of the four shed-access tiles, only `(5,5)` is genuinely walled while we own NW alone:

        (4,4) NW  escapes to (3,4), (4,3)
        (5,4) NE  escapes to (4,4)          <- fine
        (4,5) SW  escapes to (4,4)          <- fine
        (5,5) SE  neighbours (4,5) and (5,4) are both LOCKED   <- the only trap

    `_spawn_hand` fills them least-occupied-first, ties NWSE, so seven hires land
    `(5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5)` -- only the 3rd and 7th are stuck. `break` discarded
    hires 3 to 7, four of which were perfectly good, and that is what forced the old two-a-turn dribble:

        break at walled     0,2,2,4,4,6,7 = 144 hand-turns (-17 vs tape)   50/112 cells differ
        hire all anyway     0,7,7,7,7,7,7 = 161 (+0)  but two hands idle    50/112
        skip the slot       0,5,6,7,7,7,7 = 158 (-3)  and all seven work    42/108

    Measured on Seb's tape, seed 11, days 0-3. Skipping the slot and carrying on is best on both counts:
    nearly the tape's hand-turns, with no hand wasted.
    """
    priv = {"shed": {}, "seeds": {}, "inventories": [{}]}

    def hires(unlocked, onto_locked):
        old = schedule_agent.HIRE_ONTO_LOCKED
        schedule_agent.HIRE_ONTO_LOCKED = onto_locked
        try:
            agent = schedule_agent.make_agent(empty_sched(hands=6), 0, router=True)
            farm = {"tiles": blank_board(unlocked=unlocked), "money": 100000, "farmer": [4, 4],
                    "hands": [], "unlocked_quadrants": list(unlocked)}
            act = agent({"day": 0, "hour": 0, "farms": [farm], "private": priv, "step": 0})
            return len([o for o in act["market"] if o[0] == "HIRE"])
        finally:
            schedule_agent.HIRE_ONTO_LOCKED = old

    # Six wanted, one slot walled: five go out now and the sixth follows next turn, once a hand has
    # stepped off its spawn tile and freed a good slot. Never two.
    assert hires(("NW",), onto_locked=False) == 5
    # NE unlocks (5,5)'s escape square, so nothing is walled and the whole row goes at once.
    assert hires(("NW", "NE"), onto_locked=False) == 6
    # The flag takes the walled slot too, which is only worth doing once a stuck hand can be given
    # depot work -- it is a loader, not a vehicle. Measured worse until then: 50 cells against 42.
    assert hires(("NW",), onto_locked=True) == 6


def test_day_zero_matches_seb_op_for_op():
    """**The day-0 gate. Every number, ours against the tape, and exact means identical.**

    Seb's tape, seed 11, weeds off. Day 0 is the whole of the pre-land-buy window's first day and the
    agreed definition of the executor working: if day 0 matches op for op, the schedule is being played
    faithfully and the hire/spawn questions downstream resolve themselves.

    What already matches, and must not regress:

        plant 17   water 17   build_pasture 8   place 4   pickup 5
        buy_seed 17   buy_product 8   buy_animal 4   hire 7
        dawn: money 3000, tiles 25, pens 0, every crop 0, every animal 0, shed 0

    What does not, as of this commit:

        feed        3/4     one animal placed at hour 20 is never fed
        care        3/4     and so never cared
        drop        0/1     the tape banks a load at hour 2; we never DROP on day 0
        north      21/24    same tiles, different tour shape --
        south       2/13    we work the board WESTWARD, the tape SOUTHWARD
        east        6/4
        west       30/20
        pass       66/64
        unit-turns 182/185  three hand-turns, from the one walled spawn slot we skip

    The open question behind feed/care/drop: FEED is priced `MANDATORY`, its wheat is in the shed from
    hour 4, and no unit serves it until hour 15. Eight hours in which the highest-priced node on the
    board goes untouched.
    """
    import json
    import pathlib as _pl
    from kaggle_environments import make

    d = json.loads(_pl.Path("data/seed_scripts/top_guys/90494364.json").read_text())
    seat = d["info"]["TeamNames"].index("Seb (allegedly)")
    tape = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]
    mine = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[seat] or {} for step in d["steps"][1:])]
    sched = {int(k): v for k, v in json.loads(
        _pl.Path("data/seed_scripts/top_guys/90494364/schedule.json").read_text()).items()}
    thin = {k: {a: b for a, b in v.items()
                if a not in ("plant_tiles", "build_tiles", "land_turns", "orders")}
            for k, v in sched.items()}

    def day_zero(policy):
        env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
        env.reset(2)
        tally = collections.Counter()
        for t in range(24):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0 = policy(o0, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            for x in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
                if x:
                    tally[x[0]] += 1
            for o in (a0["market"] or []):
                if o:
                    tally[o[0]] += int(o[2]) if len(o) > 2 else 1
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": tape[t]["farmer"], "hands": list(tape[t]["hands"])[:n1],
                       "market": tape[t]["market"]}])
        return tally

    agent = schedule_agent.make_agent(thin, 0, router=True)
    ours = day_zero(lambda o, t: agent(o))
    his = day_zero(lambda o, t: mine[t])

    fields = sorted(set(ours) | set(his))
    diff = {k: f"{ours[k]}/{his[k]}" for k in fields if ours[k] != his[k]}
    assert not diff, (
        f"day 0 is not exact -- {len(diff)} of {len(fields)} ops differ (ours/tape):\n"
        + "\n".join(f"    {k:<20} {v}" for k, v in sorted(diff.items())))


def _seb_tape():
    """Seb's replay, our seat's actions, his seat's actions, and the schedule stripped to shipping keys."""
    import json
    import pathlib as _pl
    d = json.loads(_pl.Path("data/seed_scripts/top_guys/90494364.json").read_text())
    seat = d["info"]["TeamNames"].index("Seb (allegedly)")

    def acts(idx):
        return [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
                 "hands": list((s.get("action") or {}).get("hands") or []),
                 "market": list((s.get("action") or {}).get("market") or [])}
                for s in (step[idx] or {} for step in d["steps"][1:])]

    sched = {int(k): v for k, v in json.loads(
        _pl.Path("data/seed_scripts/top_guys/90494364/schedule.json").read_text()).items()}
    thin = {k: {a: b for a, b in v.items()
                if a not in ("plant_tiles", "build_tiles", "land_turns", "orders")}
            for k, v in sched.items()}
    return acts(seat), acts(1 - seat), thin


def _tally_day(policy, opp, day):
    """Every unit op and market order our seat emits during `day`, playing `opp` in the other seat."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    tally = collections.Counter()
    for t in range(24 * (day + 1)):
        o0 = env.state[0].observation
        a0 = policy(o0, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if t // 24 == day:
            for x in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
                if x:
                    tally[x[0]] += 1
            for o in (a0["market"] or []):
                if o:
                    tally[o[0]] += int(o[2]) if len(o) > 2 else 1
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": opp[t]["farmer"], "hands": list(opp[t]["hands"])[:n1],
                   "market": opp[t]["market"]}])
    return tally


def test_day_one_matches_seb_op_for_op():
    """**The day-1 gate**, the same contract as day 0: exact means no op differs.

    Day 1's whole character is that the tape does almost nothing. It waters **nothing** -- 17 live
    tiles, every one of them left at `consecutive_unwatered = 1` overnight, watered again on day 2 --
    and spends the day feeding, caring, collecting fertilizer and placing the one cow the row asks for.
    25 work turns against our 40, and it idles 131 turns to our 82.

    Watering on alternate days is not a risk the tape is running; it is the rule. `consecutive_unwatered`
    starts at 1 on the planting day and only weeds the tile at 2, so a tile watered on day 0 is safe
    through day 1 and must be watered again on day 2. Water buys nothing else for an ongoing crop --
    `_daily_refresh_tiles` accrues yield regardless -- and outside its window it buys nothing for a
    one-shot either. The tape ends day 7 with zero weeds doing this.
    """
    mine, his, thin = _seb_tape()
    agent = schedule_agent.make_agent(thin, 0, router=True)
    ours = _tally_day(lambda o, t: agent(o), his, 1)
    theirs = _tally_day(lambda o, t: mine[t], his, 1)

    fields = sorted(set(ours) | set(theirs))
    diff = {k: f"{ours[k]}/{theirs[k]}" for k in fields if ours[k] != theirs[k]}
    assert not diff, (
        f"day 1 is not exact -- {len(diff)} of {len(fields)} ops differ (ours/tape):\n"
        + "\n".join(f"    {k:<20} {v}" for k, v in sorted(diff.items())))


def test_a_crop_watered_yesterday_is_not_watered_again_today():
    """The every-second-day rule, at the prize level, for both crop kinds.

    A tile with `consecutive_unwatered = 0` cannot weed tonight, and water does not make an ongoing
    crop produce. Offering it anyway is what put 17 dead WATER turns on our day 1. A tile at 1 is on
    the brink and must be offered.
    """
    day = 8
    for crop, ongoing in (("TOMATO", True), ("MELON", False)):
        for debt, wanted in ((0, False), (1, True)):
            cell = {"kind": "PLANT", "crop": crop, "planted_day": day - 1, "yield_units": 0,
                    "watered_today": False, "consecutive_unwatered": debt, "fertilized_until_day": -1}
            ops = RT.crop_ops(cell, day, have_fertilizer=False)
            got = any(o == "WATER" for o, _i, _p in ops)
            assert got is wanted, (
                f"{crop} (ongoing={ongoing}) at consecutive_unwatered={debt}: "
                f"WATER offered={got}, expected {wanted} -- ops {ops}")
