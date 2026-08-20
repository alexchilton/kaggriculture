"""The day is planned once, start to end, and the shed trips are stops in it like any other.

**The defect this pins is architectural, not a miscount.** The covering planner modelled a tour as a
list of TILES TO WORK, and paid for its shed trips inside the cost function -- one notional draw at
the front if anything needed drawing, one notional walk home at the back if anything was harvested.
Neither was a stop. Nothing in the route said "be at the shed at this point", so the executor could
not walk to one, and getting produce to market was left to four separate opportunistic mechanisms
firing off whatever the unit happened to be standing on.

That is how day 6 of seed 11 lost a season's worth of tempo. The row says `WOOL: 12` and buys two
cows out of the proceeds. The tape harvests at h0, drops and sells six at h2, harvests again at h2,
drops and sells the last six at h5 -- both cows funded by hour five. We harvested at h4 and h10 and
then CARRIED ten wool through h11 to h18, because no stop ever said "go to the shed", and dropped
four at h19. The bank sat on $20 all day.

The wool was knowable at dawn. Which pens hold sheep, how much each carries, and what today's row
wants are all on the board before the day starts, so `harvest -> shed` is a plan, not a discovery.

So the property, stated as three things a route must be able to say:

    a PICKUP is a stop            the unit walks there because the plan says to, not because a
                                  side-channel `draw` dict was set
    a DROP is a stop              produce today's row wants is delivered by the tour, mid-tour if
                                  the load justifies the trip
    both are costed where they    a shed trip in the middle of a tour is paid for at the point it
    actually happen               happens, so the search can see it and route around it

`test_the_wool_reaches_the_shed_before_the_cows_are_bought` is the one that matters; the two unit
tests above it exist so a failure says WHICH half broke.
"""
import collections
import json
import pathlib

import pytest

from kagg.search import cover as DP
from kagg.search import schedule_agent as SA

SHED = tuple(DP.SHED)


def _work_stops(route):
    return [j for j in route if not getattr(j, "depot", False)]


def _depot_stops(route):
    return [j for j in route if getattr(j, "depot", False)]


def test_a_harvest_the_row_wants_is_followed_by_a_shed_stop():
    """One hand, one ripe pen, and a row that wants the wool. The tour must end at the shed.

    Not "the cost function charges a notional walk home" -- an actual stop, on an actual depot tile,
    that the executor can walk to and DROP on.
    """
    start = SHED[0]
    pen = (start[0] + 3, start[1] + 3)
    job = DP.Job(pen, [("HARVEST", None)], gives={"WOOL": 6})
    out, left = DP.plan([start], [job], [24], SHED, wanted={"WOOL": 12})
    assert not left, "the single job was not covered at all"
    route = out[0]["route"]
    drops = [d for d in _depot_stops(route) if d.drop]
    assert drops, f"no DROP stop planned for six wool the row wants: {route}"
    assert route.index(drops[-1]) > route.index(job), (
        f"the drop is planned BEFORE the harvest that fills the hand: {route}")
    assert tuple(drops[-1].tile) in set(SHED), f"drop stop is not on a depot tile: {drops[-1].tile}"


def test_a_feed_run_draws_its_wheat_at_a_stop_and_not_through_a_side_channel():
    """The pickup half of the same property.

    A unit servicing three pens needs three wheat, and `PICKUP` is unbounded, so that is ONE stop of
    one turn -- but it has to be in the route, at the front, or the executor is guessing.
    """
    start = SHED[0]
    pens = [(start[0] + 1, start[1] + 2), (start[0] + 2, start[1] + 2), (start[0] + 3, start[1] + 2)]
    jobs = [DP.Job(p, [("FEED", "WHEAT")]) for p in pens]
    out, left = DP.plan([start], jobs, [24], SHED, supply={"WHEAT": 10})
    assert not left, "three feeds within reach were not covered"
    route = out[0]["route"]
    picks = [d for d in _depot_stops(route) if d.pick]
    assert len(picks) == 1, f"expected exactly one bulk draw, got {len(picks)}: {route}"
    assert route.index(picks[0]) == 0, f"the draw is not the first stop: {route}"
    assert picks[0].pick["WHEAT"] == 3, f"drew {dict(picks[0].pick)} for three pens"
    # And the cost is the cost of walking THAT route -- no hidden legs either side of it.
    assert out[0]["cost"] == DP.turns(start, route)


def test_the_cost_of_a_route_is_the_route_and_nothing_else():
    """A revert tripwire for the cost model.

    The old `turns()` bolted a depot leg on the front and a homeward leg on the back of a route that
    did not contain either. Any route the planner emits must now cost exactly what walking it costs,
    or the search is optimising a number that is not the plan.
    """
    start = SHED[0]
    jobs = [DP.Job((start[0] + 1, start[1] + 1), [("FEED", "WHEAT")]),
            DP.Job((start[0] + 2, start[1] + 4), [("HARVEST", None)], gives={"MILK": 4})]
    out, _left = DP.plan([start], jobs, [24], SHED, supply={"WHEAT": 5}, wanted={"MILK": 4})
    route = out[0]["route"]
    walked, pos = 0, start
    for stop in route:
        walked += DP.dist(pos, stop.tile) + stop.turns
        pos = tuple(stop.tile)
    assert out[0]["cost"] == walked, f"cost {out[0]['cost']} != walking the route {walked}: {route}"


def test_the_feed_a_tour_still_needs_is_not_deliverable_however_much_the_row_wants_it():
    """Day 4 of seed 11, stated as a unit test. It cost every feed on the day.

    The row reads `sells: {WHEAT: 28}` and `money_dawn: 28.0` against a bill of about $1,400 -- a
    COW, a land parcel and eight hires -- so the day is short of cash and its produce is wanted
    early. But the produce the row wants is WHEAT, and WHEAT is also what the herd eats. A hand
    walking to three pens with three wheat in its pocket then reads as a hand carrying $75 of goods
    the market is waiting for, so it turns round and banks the herd's dinner.

    Measured on the full season: `feed 7 -> 0`, `care 7 -> 0`, `drop 5 -> 13` and moves 80 -> 124 on
    day 4 alone. Not one animal was fed. `collect_fertilizer` stayed at 6/6, which is the tell -- the
    hands DID reach the pens, they just arrived empty, because `_live_ops` cannot emit a FEED for a
    unit holding no wheat and falls through to the next op at the tile.

    So deliverable is the SURPLUS, never the load: what the hand holds beyond what the rest of its
    own tour will consume. This is the `own_route_needs_it` gate the executor used to apply after the
    fact, moved into the plan where the route is actually known.
    """
    start = SHED[0]
    pens = [DP.Job((start[0] + 1, start[1] + 2), [("FEED", "WHEAT")]),
            DP.Job((start[0] + 2, start[1] + 2), [("FEED", "WHEAT")]),
            DP.Job((start[0] + 3, start[1] + 2), [("FEED", "WHEAT")])]
    route = DP.materialise(start, pens, {"WHEAT": 3}, SHED, wanted={"WHEAT": 28}, rush=True)
    assert not [d for d in _depot_stops(route) if d.drop], (
        f"the herd's feed was banked as sellable goods: {route}")
    # And the surplus IS deliverable: one wheat more than the tour needs is a real delivery.
    #
    # Asked as "does the milk REACH THE SHED", not "is there a DROP". Since `BANK_THE_SURPLUS_NOT_THE
    # _HAND` the planner has a second way to bank it -- `PLACE MILK 8`, one turn, hand keeps its three
    # wheat -- and `_bank` takes it here because it is cheaper than DROP-plus-redraw. That is this
    # test's own point carried further, not a way round it: the whole complaint above is that DROP
    # cannot separate the herd's dinner from the market's goods, and PLACE can.
    spare = DP.materialise(start, pens, {"WHEAT": 3, "MILK": 8}, SHED,
                           wanted={"WHEAT": 28, "MILK": 8}, rush=True)
    banked = [d for d in _depot_stops(spare) if d.drop or d.place]
    assert banked, f"eight milk the row wants was carried past the shed: {spare}"
    assert not [d for d in banked if d.place and d.place.get("WHEAT")], (
        f"the herd's feed was banked as sellable goods, one item at a time: {spare}")


@pytest.mark.slow
def test_day_four_feeds_the_herd_even_though_the_row_is_selling_wheat():
    """The same defect as the test above, but in the EXECUTOR, which kept its own copy of the census.

    Day 4 of seed 11 plans correctly -- traced at every replan, six or seven FEED jobs offered, four
    or five covered, eight wheat on the draw list at h1 with seven in the shed at dawn. And the day
    emits `FEED` zero times, `CARE` zero times, `PICKUP` twice and `DROP` thirteen times.

    The wheat is drawn and then immediately put back. `DELIVER_THE_SELL_ROW` fires on any depot cell
    when the load contains something today's row still owes, and its census is deliberately blind to
    what the unit's own route needs -- the comment there says so, and the reason given was that DROP
    is all-or-nothing so a mixed load cannot shed its wool without its wheat. That reasoning holds
    only while WHEAT is not itself the thing being sold. On day 4 it is: `sells: {WHEAT: 28}`. So a
    hand that has just drawn eight wheat for eight pens reads as $200 of goods the market is waiting
    for, drops all eight, and walks to the pens empty.

    A decision to skip a gate can expire when the problem changes. That is why this is a test and not
    a comment.
    """
    from kaggle_environments import make
    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    replay, schedule, team = TAPES["seb"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    assert sched[4]["sells"].get("WHEAT"), "day 4 no longer sells wheat; this test needs a new day"

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)
    ops = collections.Counter()
    for t in range(24 * 5 - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if t // 24 == 4:
            for act in [a0["farmer"], *list(a0["hands"])[:n0]]:
                if isinstance(act, list) and act:
                    ops[act[0]] += 1
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert ops["FEED"] >= 6, (
        f"day 4 fed {ops['FEED']} animals of eight pens. The tape feeds 7. "
        f"PICKUP={ops['PICKUP']} DROP={ops['DROP']} CARE={ops['CARE']} "
        f"COLLECT_FERTILIZER={ops['COLLECT_FERTILIZER']} -- the fertilizer count is normal (6) "
        "beside zero feeds, so the pens were being visited; what did not arrive is the wheat.")


@pytest.mark.slow
def test_the_wool_reaches_the_shed_before_the_cows_are_bought():
    """Seed 11, day 6. The row is `WOOL: 12` and two COWs are bought out of it.

    The tape banks all twelve by hour five. We carried ten of them to hour nineteen. The hours below
    are not a fidelity target -- they are the constraint the day-6 purchases sit behind, and every
    day after 6 inherits the herd this one buys.
    """
    from kaggle_environments import make
    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    replay, schedule, team = TAPES["seb"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    cut, sold = None, None
    for t in range(24 * 7 - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if t // 24 == 6:
            for act in [a0["farmer"], *list(a0["hands"])[:n0]]:
                if isinstance(act, list) and act and act[0] == "HARVEST" and cut is None:
                    cut = t % 24
            for order in (a0["market"] or []):
                if order and order[0] == "SELL" and order[1] == "WOOL" and sold is None:
                    sold = t % 24
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert cut is not None, "nothing was harvested on day 6 at all"
    assert sold is not None, (
        f"day 6 harvested at h{cut} and never offered the wool for sale. `sells: {{WOOL: 12}}` and "
        "two COWs are bought out of it. Carrying it is not banking it -- the market reads the SHED, "
        "and `_drop_inventories_to_shed` (`kaggriculture.py:812`) only sweeps hands at the ROLLOVER.")
    # **The delivery, not the harvest.** The tape cuts at h0 because its sheep stand ON the shed; ours
    # stand at (1,4) and (3,4) and are cut later, which is a geometry and ordering question and is not
    # what this file is about. What IS: once the wool is in a hand, the tour must already have a shed
    # stop scheduled for it. Before the rebuild the crew carried ten wool from h11 to h18 and delivered
    # four at h19; the gap below was NINE turns and is now one.
    assert sold - cut <= 2, (
        f"harvested at h{cut}, first wool sale at h{sold} -- {sold - cut} turns of carrying. The "
        "delivery is meant to be a stop in the tour, planned at dawn off the pens' own yield_units, "
        "not something a hand stumbles into later.")
