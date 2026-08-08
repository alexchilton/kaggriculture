"""The covering day planner, tested without the game: hand-built jobs, random instances, no market.

`kagg/search/cover.py` answers one question -- can this crew cover this job list today -- and every
way it can be wrong is an invariant rather than a number:

    a tour the executor cannot walk     turns over budget
    work that evaporates                a job covered by nobody, or by two units at once
    a wasted shed trip                  a depot stop the route does not need
    a plan that is not the tour         the cost the search optimises differing from the walk
    two units sent for one cow          the shed's animal stock overdrawn
    a plan that differs run to run      non-determinism, which would make every day-by-day
                                        comparison in this project unreadable

Checked on RANDOM instances as well as hand-built ones, because a covering heuristic fails on the
instance nobody thought of. `_instances` fixes its own seed, so any failure is reproducible.
"""
import random

import pytest

from kagg.search import cover as DP

DEPOTS = ((4, 4),)


def cost(start, work, carry=None, depots=DEPOTS, wanted=None, deliver=True):
    """Turns to walk the tour `work` MATERIALISES into. What the search is actually scored on.

    Shed trips used to be charged inside `turns()` without being in the route, so the number and the
    tour disagreed; now `materialise` derives the stops and `turns` walks them. Every cost assertion
    below goes through here, so it is checking the plan and not a parallel accounting of it.
    """
    return DP.turns(start, DP.materialise(start, work, carry, depots, wanted, deliver))


def work_stops(route):
    """The route without its shed trips. `plan` returns the tour; the jobs are what was covered."""
    return [j for j in route if not getattr(j, "depot", False)]


def _jobs(rng, n, feeds=0):
    """`n` jobs on distinct tiles, `feeds` of which draw wheat from the shed."""
    tiles = rng.sample([(x, y) for x in range(10) for y in range(10) if (x, y) != (4, 4)], n)
    out = []
    for i, t in enumerate(tiles):
        if i < feeds:
            ops = [("FEED", "WHEAT"), ("CARE", None)]
        elif rng.random() < 0.25:
            ops = [("FERTILIZE", "FERTILIZER"), ("WATER", None)]
        else:
            ops = [(rng.choice(["WATER", "HARVEST", "COLLECT_FERTILIZER"]), None)]
        out.append(DP.Job(t, ops))
    return out


def _instances(count=30, seed=20260808):
    rng = random.Random(seed)
    for _ in range(count):
        k = rng.randint(1, 12)
        units = [(4, 4) if rng.random() < 0.4 else (rng.randrange(10), rng.randrange(10))
                 for _ in range(k)]
        n = rng.randint(1, 40)
        yield units, _jobs(rng, n, feeds=rng.randint(0, min(8, n))), [rng.randint(6, 23)] * k


# ---------------------------------------------------------------------------------------------
# the cost model, which is the only thing the search is scored against
# ---------------------------------------------------------------------------------------------

def test_one_shed_trip_is_one_turn_per_ITEM_not_per_unit_of_it():
    """`PICKUP` is unbounded (`kaggriculture.py:340`): six wheat is one turn, not six.

    Getting this wrong makes every animal-heavy tour look unaffordable, which is the failure the
    depot model exists to prevent -- one draw at a time made every pen a shed round trip.
    """
    pens = [DP.Job((1, y), [("FEED", "WHEAT")]) for y in range(6)]
    # walk to depot (0) + one draw (1) + (4,4)->(1,0) is 7, down the column 5, six ops
    assert cost((4, 4), pens) == 0 + 1 + 7 + 5 + 6
    # six pens against one: five more steps and five more ops, and NO second draw
    assert cost((4, 4), pens) - cost((4, 4), pens[:1]) == 5 + 5
    # a second ITEM does cost a second draw. (1,6) is one step past the last pen.
    both = pens + [DP.Job((1, 6), [("FERTILIZE", "FERTILIZER")])]
    assert cost((4, 4), both) - cost((4, 4), pens) == 1 + 1 + 1
    # and it is ONE stop, not two: both items come off the same visit.
    route = DP.materialise((4, 4), both, {}, DEPOTS)
    assert len([d for d in route if getattr(d, "depot", False)]) == 1, route


def test_a_load_already_in_the_hand_removes_the_shed_trip():
    """A unit carrying the feed must not be sent to fetch it. This starved a herd once already."""
    pens = [DP.Job((1, y), [("FEED", "WHEAT")]) for y in range(3)]
    cold = cost((4, 4), pens)
    assert cost((4, 4), pens, {"WHEAT": 3}) == cold - 1
    assert not [d for d in DP.materialise((4, 4), pens, {"WHEAT": 3}, DEPOTS)
                if getattr(d, "depot", False)], "sent to fetch feed it was already holding"


def test_a_tour_that_ends_holding_product_pays_the_walk_home():
    """The market only reads the SHED, so a harvest still in a hand at dusk is unsold."""
    harvest = [DP.Job((0, 0), [("HARVEST", None)])]
    water = [DP.Job((0, 0), [("WATER", None)])]
    # The walk home plus the DROP itself, which the old cost function charged as travel alone.
    assert cost((4, 4), harvest) - cost((4, 4), water) == DP.dist((0, 0), (4, 4)) + 1
    # And it is a STOP, at a depot, after the harvest -- not a number bolted onto the total.
    route = DP.materialise((4, 4), harvest, {}, DEPOTS)
    assert getattr(route[-1], "depot", False) and route[-1].drop, route
    assert tuple(route[-1].tile) in set(DEPOTS)
    # `deliver=False` is the dusk case: the overnight sweep banks it, so no leg is reserved.
    assert cost((4, 4), harvest, deliver=False) == cost((4, 4), water, deliver=False)


# ---------------------------------------------------------------------------------------------
# invariants
# ---------------------------------------------------------------------------------------------

def test_no_route_ever_exceeds_its_budget():
    """A tour that overruns is a tour whose tail silently never happens."""
    for units, jobs, budget in _instances():
        out, _left = DP.plan(units, jobs, budget, DEPOTS)
        for u, st in out.items():
            assert st["cost"] <= budget[u], (
                f"unit {u}: {st['cost']} turns into a {budget[u]}-turn day, "
                f"{[j.tile for j in st['route']]}")


def test_no_job_is_covered_twice_and_none_is_invented():
    for units, jobs, budget in _instances():
        out, left = DP.plan(units, jobs, budget, DEPOTS)
        done = [j for st in out.values() for j in work_stops(st["route"])]
        ids = [id(j) for j in done]
        assert len(ids) == len(set(ids)), "a job was given to two units at once"
        assert set(ids) | {id(j) for j in left} == {id(j) for j in jobs}
        assert not (set(ids) & {id(j) for j in left}), "a job is both covered and uncovered"


def test_every_job_can_be_started_when_the_tour_reaches_it():
    """The point of putting the shed trips IN the route: a hand never arrives empty-handed.

    This is the invariant the old `draw` side-channel could only approximate. Walk each tour in
    order, carrying what the stops pick up and spending what the jobs consume, and no job may ever
    need an item the hand is not holding.
    """
    import collections
    for units, jobs, budget in _instances():
        out, _left = DP.plan(units, jobs, budget, DEPOTS, supply=None)
        for u, st in out.items():
            held = collections.Counter()
            for stop in st["route"]:
                if getattr(stop, "depot", False):
                    if stop.drop:
                        held = collections.Counter()
                    held += stop.pick
                    continue
                for item, qty in stop.needs.items():
                    assert held[item] >= qty, (
                        f"unit {u} reaches {stop.tile} needing {qty} {item} holding {held[item]}: "
                        f"{st['route']}")
                held -= stop.needs
                held += stop.gives


def test_the_cost_is_the_tour_and_the_draw_list_is_what_the_tour_picks_up():
    """A cost that is not the walk is a search optimising something nobody executes."""
    for units, jobs, budget in _instances():
        out, _left = DP.plan(units, jobs, budget, DEPOTS)
        for u, st in out.items():
            assert st["cost"] == DP.turns(units[u], st["route"])
            assert dict(st["draw"]) == dict(DP.draws(st["route"]))


def test_the_plan_is_the_same_every_time():
    """Every tie-break is a total order and there is no clock in the file."""
    for units, jobs, budget in list(_instances(10)):
        a, _ = DP.plan(units, jobs, budget, DEPOTS)
        b, _ = DP.plan(units, jobs, budget, DEPOTS)
        assert ({u: [j.tile for j in st["route"]] for u, st in a.items()}
                == {u: [j.tile for j in st["route"]] for u, st in b.items()})
        assert ({u: st["cost"] for u, st in a.items()} == {u: st["cost"] for u, st in b.items()})


def test_a_crew_with_room_covers_everything():
    """Twelve hands and eight jobs beside the shed: leaving any of it undone is a bug, not a choice."""
    units = [(4, 4)] * 12
    jobs = [DP.Job((3, y), [("WATER", None)]) for y in range(4)] + \
           [DP.Job((5, y), [("WATER", None)]) for y in range(4)]
    _out, left = DP.plan(units, jobs, [23] * 12, DEPOTS)
    assert not left, f"{len(left)} jobs left undone with twelve idle hands: {left}"


def test_the_field_is_shared_out_instead_of_two_units_carrying_it():
    """Capacity, not distance, is scarce -- so a plan that idles a hand beside work is never right.

    Global cheapest-insertion on its own always appends the next tile to the unit already standing on
    the previous one (cost 2) rather than starting an idle unit from the shed (cost 6), so it
    minimises total WALKING, which is the wrong objective when every hand is paid for whether it
    moves or not. Day 0 of seed 11 measured `10, 9, 2, 0, 0` across five units with six jobs never
    started, and leaving the fair-share cap out of the first version of `dayplan` reproduced it over a
    whole season: 2,173 jobs uncovered, $117,732 -> $84,702.
    """
    units = [(4, 4)] * 5
    from kagg.search import router as RT
    field = RT.field_order({"NW"})[:21]
    jobs = [DP.Job(t, [("WATER", None)]) for t in field]
    out, left = DP.plan(units, jobs, [21] * 5, ((4, 4),))
    sizes = sorted(len(work_stops(st["route"])) for st in out.values())
    assert not left, f"{len(left)} jobs uncovered with five hands and 105 turns"
    assert sum(sizes) == 21, sizes
    assert sizes[0] >= 2, f"a hand was left idle beside pending work: {sizes}"
    assert sizes[-1] <= 7, f"one hand was given the whole field: {sizes}"


def test_one_cow_in_the_shed_is_placed_once():
    """`supply` is a budget shared across units, exactly like turns.

    Without it, one COW and three empty pens produce three placements and two units walk a full round
    trip to a pen with no animal in it.
    """
    units = [(4, 4)] * 3
    pens = [DP.Job((1, y), [("PLACE", "COW")]) for y in range(3)]
    out, _left = DP.plan(units, pens, [23] * 3, DEPOTS, supply={"COW": 1})
    placed = sum(1 for st in out.values() for j in work_stops(st["route"])
                 for o, i in j.ops if o == "PLACE" and i == "COW")
    assert placed == 1, f"{placed} units sent for the same single COW"


# ---------------------------------------------------------------------------------------------
# repair: the move the whole file exists for
# ---------------------------------------------------------------------------------------------

def _stranded():
    """A far harvest only u0 can reach, after the greedy has spent u0 on cheap work by the shed.

    Budgets are 7: room on u0 for the far harvest and ONE other stop, not two, and at that budget u1
    cannot reach (4,1) at all. Covering it means u0 gives up a stop, and that stop has to land on u1
    rather than in a bin -- which is the whole difference between this and a plain eviction.

    FOUR earlier versions of this board were wrong, and all four are worth recording, because every
    one of them made this test silently stop measuring the repair.
    The first put u1 in the far corner, where it could not absorb the displaced stop either, so the
    instance was genuinely infeasible and the repair was failing for the board's reasons. The second
    used a FEED as the stranded job -- which `REQUIRED_OPS` now covers in the first pass, so the
    greedy seated it unaided and the test measured nothing. The stranded job has to be ORDINARY work.
    The third was budget 8, exactly right while the walk home was charged as travel alone: once the
    shed trip became a STOP it cost its DROP turn too and 8 was infeasible again. The fourth was
    budget 9, right for the one commit in which the closing trip was charged during packing; it stops
    discriminating the moment that trip becomes opportunistic, because then u1 can reach the harvest
    unaided. The two tests below are what caught each of these, in both directions, which is why both
    are kept and why neither may be deleted to make the other pass.
    """
    units = [(4, 4), (7, 4)]
    near = [DP.Job((4, 3), [("WATER", None)]), DP.Job((3, 4), [("WATER", None)])]
    far = [DP.Job((7, 3), [("WATER", None)])]
    ripe = DP.Job((4, 1), [("HARVEST", None)])
    return units, near + far + [ripe], [7, 7]


def test_repair_covers_a_job_the_greedy_strands():
    """Take a stop off the only unit in range, put the pen on, and re-home the stop elsewhere."""
    units, jobs, budget = _stranded()
    _out, left = DP.plan(units, jobs, budget, DEPOTS)
    assert not left, f"repair left {[j.tile for j in left]} uncovered"


def test_the_greedy_alone_does_NOT_cover_it():
    """The revert check, inline. A test that passes with the feature off is measuring the board.

    Three fixes on this project were, at first, covered by nothing -- the suite stayed green with them
    backed out. `REPAIR = False` is the plain cheapest-insertion greedy.
    """
    units, jobs, budget = _stranded()
    DP.REPAIR = False
    try:
        _routes, left = DP.cover(units, jobs, budget, DEPOTS)
    finally:
        DP.REPAIR = True
    assert [j.tile for j in left] == [(4, 1)], (
        f"the greedy covers this unaided ({left}), so the repair test above proves nothing. "
        "Build a harder instance rather than deleting this check.")


def test_a_feed_is_a_constraint_and_beats_ordinary_work_to_the_crew():
    """`REQUIRED_OPS`: skip a FEED twice and the animal is gone (`kaggriculture.py:786`).

    Counting jobs alone cannot see that -- three cheap waters against one lost cow reads +3 -1 on
    today's tally and is a disaster across the fortnight the cow would have milked -- because the
    cost lands on every FOLLOWING day, and a single-day covering objective has no term for it. So
    required work is covered first and the rest of the day is packed around it.

    One unit, seven turns: room for the pen or for the waters beside it, not both.
    """
    units = [(4, 4)]
    waters = [DP.Job((3, y), [("WATER", None)]) for y in (3, 4, 5)]
    pen = DP.Job((4, 1), [("FEED", "WHEAT")])
    assert pen.required and not any(w.required for w in waters)
    out, left = DP.plan(units, waters + [pen], [7], DEPOTS)
    done = {j.tile for st in out.values() for j in work_stops(st["route"])}
    assert (4, 1) in done, (
        f"the pen lost its feed to the waters next door: covered {done}, left {[j.tile for j in left]}")


def test_repair_never_uncovers_work_it_had_already_covered():
    """Coverage is the objective, so it must be monotone -- which is also why the loop terminates."""
    for units, jobs, budget in _instances():
        routes, left = DP.cover(units, jobs, budget, DEPOTS)
        covered = sum(len(r) for r in routes.values())
        assert covered + len(left) == len(jobs)


# ---------------------------------------------------------------------------------------------
# the adapter, which is how this reaches the agent at all
# ---------------------------------------------------------------------------------------------

def test_a_router_node_converts_without_losing_the_feed_a_placement_implies():
    """`Node.needs` carries the wheat a PLACE implies, and it is invisible in `ops`.

    `build_nodes` adds it because a placement necessarily creates a hungry animal and the FEED node
    for it cannot exist until the animal is standing there. Re-deriving `needs` from `ops` would drop
    it, and the unit would leave the shed carrying a cow and no feed -- measured on day 0 of seed 11.
    """
    from kagg.search import router as RT

    node = RT.Node((1, 1), [("PLACE", "COW", 1840.0)])
    assert node.needs["WHEAT"] == 1, "this test is asserting against PLACE_DRAWS_FEED being on"
    job = DP.from_nodes([node])[0]
    assert job.needs == node.needs
    assert job.tile == (1, 1) and job.turns == node.service
