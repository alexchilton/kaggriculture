"""Alex's experiment: give OUR planner Seb's day-16 board, and then our own. Which one is broken?

Three failures all look the same from the outside -- a hungry pen unfed, a dry crop unwatered, hands
standing idle -- and they have been confounded all day. This separates them by holding the ALGORITHM
fixed and swapping the BOARD:

    our planner on SEB's board    works -> the algorithm is fine, our board is the problem
    our planner on OUR board      fails
    fails on both                 -> the algorithm is the problem
    fails only on ours            -> the geometry is the problem
    high-prize work unserved with spare turns on BOTH -> the algorithm, regardless of board

Day 16 is the isolation point: it is the day the first sheep starves out, and by then both sides hold
nineteen pens, so the boards are comparable in size.

The planner is driven exactly as `schedule_agent._router_acts` drives it -- same `build_nodes`
arguments, same `plan_routes` arguments, same budget rule `TPD - hour - 1`, same depot rule -- because
a harness that calls it differently measures its own calling convention. That mistake has already
cost this project twice, and it cost it again earlier today when an in-process flag toggle silently
reset on import and made a revert check pass that should have failed.

`pins` is empty for BOTH boards. Pins carry the schedule's PLANT demand, which is not what is being
tested here and would differ between the two seats for reasons that have nothing to do with routing.
Everything measured below is work the BOARD ITSELF offers: feeds, waters, harvests, collections.
"""
import collections
import json
import pathlib

import pytest

from kagg.search import router as RT
from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy, DEFAULT_TAPE

pytestmark = pytest.mark.slow

#: Mid-morning, not dawn. Hands are HIRED THROUGH THE MORNING, so at hour 0 a farm owns exactly one
#: unit -- the farmer -- and the crew this experiment is about does not exist yet. A first version of
#: this test ran at hour 0, measured `units=1, nodes=0`, and PASSED all three assertions on both
#: boards while testing nothing whatsoever. That is the "a gate only tests what it exercises" lesson
#: arriving for the fourth time; the guard below is what makes it fail loudly instead.
DAY, HOUR = 16, 8


def _boards(seed=11):
    """Seat-0 observations at DAY dawn: ours, and the tape's, each against the same opponent."""
    from kaggle_environments import make

    replay, schedule, team = TAPES[DEFAULT_TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    out = {}
    for label, make_seat0 in (
        ("OURS", lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True))),
        ("SEB", lambda: tape_policy(replay, team, 0)),
    ):
        env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
        env.reset(2)
        p0, opp = make_seat0(), tape_policy(replay, team, 1)
        for t in range(24 * DAY + HOUR):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = p0(o0, t), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
        out[label] = env.state[0].observation
    return out


def _plan(obs):
    """Run OUR planner on this board, exactly as `_router_acts` would. Returns a report dict."""
    farm = obs["farms"][0]
    priv = obs.get("private") or {}
    tiles = farm["tiles"]
    # The key is `unlocked_quadrants`, and getting it wrong is silent: `build_nodes` filters every
    # tile through `R.quadrant_of(...) in unlocked`, so an empty set yields ZERO nodes and a planner
    # with nothing to do trivially satisfies every assertion below. See `schedule_agent.py:1247`.
    unlocked = set(farm.get("unlocked_quadrants") or ["NW"])
    units = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
    invs = priv.get("inventories") or []
    shed = collections.Counter({k: int(v) for k, v in (priv.get("shed") or {}).items()})

    carried = collections.Counter()
    for iv in invs:
        carried.update(iv or {})
    budget = [max(0, SA.TPD - HOUR - 1)] * len(units)
    depots = tuple(c for c in RT.R.shed_access_tiles() if SA._owned(c, unlocked)) or (SA.SPAWN,)
    load = {u: collections.Counter(invs[u] if u < len(invs) else {}) for u in range(len(units))}

    nodes = RT.build_nodes(tiles, DAY, shed, carried, unlocked, {}, HOUR)
    routes = RT.plan_routes(units, nodes, budget, depots, load, supply=shed)

    served = {n.tile for st in routes.values() for n in st["route"]}
    unserved = [n for n in nodes if n.tile not in served]
    # Per unit, not just the total. 35 spare turns spread as 2.7 each across 13 units is NOT the same
    # defect as 35 sitting on two units: the first cannot fit a six-turn feed run anywhere and needs
    # rebalancing, the second is work simply never offered to a free hand. Reporting only the sum
    # cannot tell them apart, and the fix differs completely.
    per_unit = [max(0, budget[u] - st["cost"]) for u, st in sorted(routes.items())]
    spare = sum(per_unit)

    def wants(n, op):
        return any(o == op for o, _i in n.ops)

    return dict(
        units=len(units), pens=sum(1 for r in tiles for c in r
                                   if isinstance(c, dict) and c.get("animal")),
        nodes=len(nodes), served=len(nodes) - len(unserved), spare_turns=spare,
        spare_per_unit=per_unit, biggest_spare=max(per_unit, default=0),
        units_fully_idle=sum(1 for s in per_unit if s == budget[0]),
        # The cheapest unserved node, in turns, from the unit with the most room. If this is <= the
        # biggest single spare, the work FITS somewhere and was simply never assigned.
        cheapest_unserved_reach=min(
            (min(abs(n.tile[0] - units[u][0]) + abs(n.tile[1] - units[u][1]) + n.service
                 for u in range(len(units)))
             for n in unserved), default=0),
        feeds_offered=sum(1 for n in nodes if wants(n, "FEED")),
        feeds_unserved=sum(1 for n in unserved if wants(n, "FEED")),
        waters_offered=sum(1 for n in nodes if wants(n, "WATER")),
        waters_unserved=sum(1 for n in unserved if wants(n, "WATER")),
        top_unserved=sorted((round(n.prize), n.tile, [o for o, _i in n.ops])
                            for n in unserved)[-3:],
        mandatory_unserved=sum(1 for n in unserved if n.mandatory),
    )


@pytest.fixture(scope="module")
def reports():
    b = _boards()
    r = {k: _plan(v) for k, v in b.items()}
    print("\n\n  OUR PLANNER, TWO BOARDS, day 16 dawn")
    print(f"  {'':<20}{'OURS':>12}{'SEB':>12}")
    for k in ("units", "pens", "nodes", "served", "spare_turns", "feeds_offered",
              "feeds_unserved", "waters_offered", "waters_unserved", "mandatory_unserved"):
        print(f"  {k:<20}{r['OURS'][k]:>12}{r['SEB'][k]:>12}")
    for lab in ("OURS", "SEB"):
        print(f"  dearest unserved on {lab}: {r[lab]['top_unserved']}")
    return r


def test_the_experiment_is_actually_exercising_something(reports):
    """Runs FIRST. A planner handed no crew and no work passes everything below while testing nothing.

    The first version of this file did exactly that -- `units=1, nodes=0` on both boards, three green
    assertions, zero information -- because hands are hired through the morning and because the
    quadrant key is `unlocked_quadrants`, not `unlocked`. Both mistakes are silent. This is the
    tripwire.
    """
    for lab, r in reports.items():
        assert r["units"] > 1, f"{lab}: only {r['units']} unit -- the crew has not been hired yet"
        assert r["nodes"] > 0, f"{lab}: build_nodes offered NOTHING -- check `unlocked_quadrants`"
        assert r["pens"] > 0, f"{lab}: no pens on the board at day {DAY}"


def test_the_planner_leaves_no_mandatory_work_unserved_on_our_own_board(reports):
    """If this fails, the algorithm cannot drain its own queue -- board notwithstanding."""
    r = reports["OURS"]
    assert r["mandatory_unserved"] == 0, (
        f"{r['mandatory_unserved']} mandatory node(s) unserved on OUR board with "
        f"{r['spare_turns']} spare unit-turns. Dearest unserved: {r['top_unserved']}"
    )


def test_the_planner_leaves_no_mandatory_work_unserved_on_sebs_board(reports):
    """The control. Failing HERE too means the algorithm, not the geometry, is at fault."""
    r = reports["SEB"]
    assert r["mandatory_unserved"] == 0, (
        f"{r['mandatory_unserved']} mandatory node(s) unserved on SEB's board with "
        f"{r['spare_turns']} spare unit-turns. Dearest unserved: {r['top_unserved']}"
    )


def test_spare_turns_and_unserved_work_do_not_coexist_on_either_board(reports):
    """The real defect, stated directly: idle hands beside work nobody took."""
    bad = {k: (r["spare_turns"], r["nodes"] - r["served"])
           for k, r in reports.items() if r["spare_turns"] > 0 and r["nodes"] > r["served"]}
    assert not bad, f"idle capacity beside unserved work (spare_turns, unserved): {bad}"
