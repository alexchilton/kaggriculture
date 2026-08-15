"""The packer must admit work against the tour that actually gets walked.

`cover.cost` is the function the greedy admits on. On `RESERVE_DAYS` it prices the sequence as
`materialise(deliver=True, wanted_only=True)` -- a tour that ends with one closing walk to the shed.
The shipped agent never asks for that tour: `_solve` sets `deliver = max(budget) > DELIVER_CUTOFF_TURNS`
with `DELIVER_CUTOFF_TURNS = 99` against budgets of 23-24, so `deliver` is **always False**, and
`plan` materialises `deliver=False`.

Those two are not the same tour and not the same price. With no closing walk, `materialise` inserts
MID-TOUR shed trips instead, so the load is not stranded past market close. Seed 11, day 10, unit 9,
one work sequence priced both ways:

    ADMIT (deliver=True, wanted_only=True)   21 turns
      SHED pick{WHEAT 4, SHEEP 1} -> (7,4)FEED -> (6,4)FEED -> (6,3)PLACE/FEED -> (5,3)FEED -> SHED drop

    SHIP  (deliver=False)                    29 turns
      SHED pick{WHEAT 4, SHEEP 1} -> (7,4)FEED -> SHED drop+pick -> (6,4)FEED -> SHED drop+pick
      -> (6,3)PLACE/FEED -> (5,3)FEED

The budget is 23. The packer admits 21 turns of work and the day then walks 29, so the last two
stops are never reached. They are `(6,3)` and `(5,3)`, and those are two of the three animals that
end day 10 unfed. `consecutive_unfed >= 2` removes the animal outright
(`reference/kaggriculture.py:817`), so a stop dropped twice running is a $400-$500 asset written off
and a pasture standing empty for the rest of the season -- measured on the ladder in games 93186363,
93237183 and 93239838, all three losing the same tile (6,4) on day 11.

This pins the invariant, not the constant: every tour the planner ships must fit the day it was
planned for. It says nothing about which jobs are chosen, only that the packer may not admit work
the crew cannot perform.

`--tape kawashigi`, seed 11, weeds off, which is the harness every other planner test uses.
"""
import importlib

import pytest

A = importlib.import_module("kagg.search.schedule_agent")
B = importlib.import_module("scripts.breakdown")
COVER = importlib.import_module("kagg.search.cover")
PLAN = importlib.import_module("kagg.plan")

#: The day the defect was found on. Day 10 is the first `RESERVE_DAYS` entry past the matched
#: opening, and the first day the herd is large enough that a dropped FEED is not free.
DAY = 10


@pytest.fixture(scope="module")
def tours():
    """Play to the end of `DAY`, recording every tour the packer shipped and what it really costs.

    Wraps `cover.cover` rather than `cover.plan`, so the sequence is read BEFORE `plan` materialises
    it and the two cost models can be compared on identical input.
    """
    from kaggle_environments import make

    B.schedule_agent = A
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = PLAN.load(schedule)
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)
    opp = B.tape_policy(replay, team, 1)

    seen, unfed, cur = [], [], {"day": -1}
    real = COVER.cover

    def spy(units, jobs, budget, depots=COVER.SHED, carry=None, supply=None, deliver=True,
            wanted=None, day=None, rush=False, due=None):
        work, uncovered = real(units, jobs, budget, depots, carry, supply, deliver, wanted, day,
                               rush, due)
        dep = tuple(depots) or COVER.SHED
        for u, seq in work.items():
            held = (carry or {}).get(u) or {}
            ship = COVER.turns(units[u], COVER.materialise(units[u], seq, held, dep, wanted,
                                                           deliver, rush, due=due))
            seen.append(dict(day=cur["day"], unit=u, budget=budget[u], ships=ship,
                             feeds=[tuple(j.tile) for j in seq
                                    if any(o[0] == "FEED" for o in j.ops)]))
        return work, uncovered

    COVER.cover = spy
    try:
        for t in range((DAY + 1) * 24):
            o0, o1 = env.state[0].observation, env.state[1].observation
            cur["day"] = t // 24
            if t % 24 == 23:
                for y, row in enumerate(o0["farms"][0]["tiles"]):
                    for x, c in enumerate(row):
                        if isinstance(c, dict) and c.get("animal") and not c.get("fed_today"):
                            unfed.append((t // 24, (x, y), c["animal"]))
            env.step([me(o0, t), opp(o1, t)])
            if env.done:
                break
    finally:
        COVER.cover = real
    return seen, unfed


def test_the_shipped_agent_never_asks_for_a_delivering_tour(tours):
    """The premise. If `deliver` is ever True the two cost models can agree and this is not a bug."""
    assert A.DELIVER_CUTOFF_TURNS > 24, (
        "budgets are 23-24 turns; a cutoff at or below that makes `deliver` True and this test moot")


def test_every_tour_fits_the_day_it_was_planned_for(tours):
    """The defect: work admitted at one price and walked at another."""
    seen, _unfed = tours
    over = [r for r in seen if r["ships"] > r["budget"]]
    assert not over, "\n".join(
        f"  d{r['day']} u{r['unit']}: budget {r['budget']}, the tour it ships costs {r['ships']} "
        f"(+{r['ships'] - r['budget']}); FEED stops on it {r['feeds']}" for r in over)


def test_no_animal_goes_unfed_on_the_day_the_packer_overruns(tours):
    """The consequence. Two missed days in a row and the animal is gone, so a miss is not free.

    Scoped to `DAY` alone. Days 0 and 3 also leave animals unfed and are a DIFFERENT defect -- no
    FEED job is built for them at all -- and they sit inside the matched d0-d8 opening, which this
    change must not reach.
    """
    _seen, unfed = tours
    today = [u for u in unfed if u[0] == DAY]
    assert not today, (
        f"day {DAY} ends with {len(today)} unfed animal(s): "
        + ", ".join(f"{t} {kind}" for _d, t, kind in today))
