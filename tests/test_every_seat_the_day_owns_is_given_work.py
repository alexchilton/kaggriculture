"""Every seat that CAN work is planned for, and none of them stands still while a job is dropped.

This exists because a whole day went into re-cutting lanes, re-ordering the sweep and re-pricing the
shed ferry to make d4's six missing WATERs fit, and none of it could have worked: the work was never
refused for want of turns. Two of the seven hands we hire on d4 emit `PASS` on all 24 of their turns.

Measured off the live agent on seed 11, day 4, hand ops printed by index and hour -- `own=7 emit=7`
on every hour, so this is not a truncation artifact or an index shift from mid-day hiring, and the
hands all land together at h1:

    h1   F=WEST | WEST NORT PASS PICK WEST NORT PASS
    h5   F=CARE | NORT NORT PASS COLL WEST WATE PASS
    h13  F=CARE | SOUT WATE PASS WEST SOUT EAST PASS
    h21  F=EAST | WATE SOUT PASS PASS HARV HARV PASS

**Those two seats are boxed in by the GAME, not lost by the planner**, and the first cut of this file
asserted the opposite. `_spawn_hand` (`kaggriculture.py:520`) rotates hires over the four shed-access
tiles `(4,4) (5,4) (4,5) (5,5)` by occupancy then NWSE index, so with a farmer on `(4,4)` a row of
seven lands `(5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5)`. While only NW is unlocked, all four of
`(5,5)`'s orthogonal neighbours sit in locked quadrants; MOVE onto a locked tile is refused
(`:313`) and every other op no-ops there (`:322`). Hands 2 and 6 can do nothing at all, and
`_mobile` is right to leave them out. Measured, and it self-corrects on the day we buy NE:

    d0-d4  unlocked ['NW']        arrivals ... (5,5)BOX ... (5,5)BOX     2 seats dead
    d5     unlocked ['NW','NE']   arrivals ... (5,5)OK  ... (5,5)OK      0 seats dead

So the invariant is about MOBILE seats. A test that counts hired hands instead measures the board's
quadrant ownership and fails for five days running while the planner is behaving correctly -- which
is what it did, and it would have sent the next session hunting a routing bug that is not there.

The wage is still real and it is still wasted: `_hire_cost` is `mult * fib(n)` with `fib(0)=1`
(`:677`), so on d0-d4 the seventh hire costs 13 and buys a hand that cannot leave its square. That
is a hiring question, not a routing one, and nothing here asserts on it -- the tape hires seven too.

**These are invariants, not scores.** Each is binary and each is a statement about the planner's own
inputs and outputs, so a flag that quietly changes who gets routed breaks a named test instead of
moving a number in the grid. That is the whole point of the file: the flags in `crew.py`,
`cover.py` and `schedule_agent_1455mh.py` are global, they interact, and their effect on *seat
utilisation* is invisible in a per-day op grid until it has already cost the day.

Scope: d0-d10, the days that must match the tape. Nothing here asserts anything about the ops
themselves -- `test_each_day_matches_the_tape` owns that.
"""
import collections
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/91422988.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent_1455mh"
SEED = 11
DAYS = 11
TPD = 24


@pytest.fixture(scope="module")
def played():
    """One playthrough of d0-d6, returning what the planner was handed and what the farm emitted.

    Three things are collected, and they are deliberately at different levels:

      - `plans[day]`  every `crew.cover` call that day, as `(n_units, budget, work, uncovered)`.
        The DAWN call is `plans[day][0]`, and it is the one that matters: the day is planned once
        (see `test_the_day_is_solved_once`), so a seat missing there is a seat missing all day.
      - `emitted[day][seat]`  the ops each seat actually sent, `"F"` for the farmer and `uN` for
        hand N. Truncated to the hands the farm owns at that turn, exactly as `make_agent`'s caller
        does, so a phantom seat routed for an arriving hire cannot inflate the count.
      - `mobile[day]`  the seat names that were able to act at ANY hour of the day, by `_mobile`:
        owned ground, or orthogonally adjacent to some. A hand that spawns on `(5,5)` with only NW
        unlocked is in none of those and is excluded, because the game will refuse everything it
        sends. Read per turn rather than once, since buying a quadrant mid-day frees a boxed hand.

    `STRICT_FEASIBILITY` is forced off for the run. The raise is a development instrument; these
    tests need to see the dropped jobs as data, and a day that aborts mid-plan emits nothing to
    inspect.
    """
    SA = importlib.import_module(MODULE)
    CREW = importlib.import_module("kagg.search.crew")

    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    plans = collections.defaultdict(list)
    emitted = collections.defaultdict(lambda: collections.defaultdict(list))
    mobile = collections.defaultdict(set)
    owned_at_h1 = collections.defaultdict(int)
    owned_by_dusk = collections.defaultdict(int)
    walled_at_h1 = collections.defaultdict(list)
    now = {"day": 0}

    real_cover, real_strict = CREW.cover, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, *a, **kw):
        work, left = real_cover(units, jobs, budget, *a, **kw)
        plans[now["day"]].append(
            (len(units), list(budget),
             {u: len(seq) for u, seq in work.items()},
             [(j.tile, [o for o, _i in j.ops]) for j in left]))
        return work, left

    CREW.cover, CREW.STRICT_FEASIBILITY = spy, False
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            day, now["day"] = t // TPD, t // TPD
            o0 = env.state[0].observation
            a0, a1 = agent(o0), opp[t]
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            unlocked = o0["farms"][0].get("unlocked_quadrants")
            owned_by_dusk[day] = max(owned_by_dusk[day], n0)
            if t % TPD == 1:
                owned_at_h1[day] = n0
                walled_at_h1[day] = [(f"u{i}", tuple(p))
                                     for i, p in enumerate(o0["farms"][0].get("hands") or [])
                                     if not SA._mobile(tuple(p), unlocked)]
            if SA._mobile(tuple(o0["farms"][0]["farmer"]), unlocked):
                mobile[day].add("F")
            for i, pos in enumerate((o0["farms"][0].get("hands") or [])):
                if SA._mobile(tuple(pos), unlocked):
                    mobile[day].add(f"u{i}")
            emitted[day]["F"].append((a0["farmer"] or ["PASS"])[0])
            for i, op in enumerate(list(a0["hands"])[:n0]):
                emitted[day][f"u{i}"].append((op or ["PASS"])[0])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        CREW.cover, CREW.STRICT_FEASIBILITY = real_cover, real_strict

    return {"plans": dict(plans), "emitted": {k: dict(v) for k, v in emitted.items()},
            "mobile": {k: set(v) for k, v in mobile.items()},
            "owned_at_h1": dict(owned_at_h1), "owned_by_dusk": dict(owned_by_dusk), "walled_at_h1": dict(walled_at_h1)}


@pytest.mark.parametrize("day", range(DAYS))
def test_the_dawn_plan_is_built_for_every_seat_the_day_will_own(played, day):
    """The dawn plan routes as many units as the farm will hold, not as many as it holds at h0.

    At hour 0 the farm owns ZERO hands -- the whole crew is bought in that turn's market phase and
    appears at h1 -- so the seat count in the dawn plan is entirely a prediction, made by
    `_arrivals` off `_hires_this_turn`. If that prediction is short, the missing seats are never
    given a lane and no downstream routing rule can reach them, because they are not in `units`.
    `crew.cover` then reports the leftover work as jobs that will not FIT, against a budget list
    that does not mention the hands it was never told about.

    Counted against MOBILE seats, not hired ones. A hand the game has boxed in is not a seat the
    planner failed to use -- see the module docstring for why that distinction was worth measuring.

    Asserted `>=`, not `==`: routing a seat that turns out to be unusable costs a wasted lane and is
    caught by `test_no_op_is_handed_to_a_unit_we_do_not_own`, whereas routing one seat too few
    silently deletes a working hand's entire day.
    """
    plans = played["plans"].get(day)
    assert plans, f"day {day} never called crew.cover -- the planner did not run"
    n_units, budget, _work, _left = plans[0]
    seats = len(played["mobile"][day])
    assert n_units >= seats, (
        f"day {day}: the dawn plan was built for {n_units} seats (budgets {budget}) but "
        f"{seats} seats could act that day ({sorted(played['mobile'][day])}), so "
        f"{seats - n_units} of them were never handed to the planner and cannot be routed by "
        f"anything downstream.")


@pytest.mark.parametrize("day", range(DAYS))
def test_the_dawn_plan_routes_no_more_hires_than_the_turn_can_order(played, day):
    """`_hires_this_turn` predicts exactly the hands the market block below it will actually buy.

    This is that function's own stated contract -- "it must not diverge from what that block actually
    orders" -- and it checks affordability but not ORDER SLOTS. The env keeps `orders[:10]`
    (`kaggriculture.py:535`) and `_fit_slots` spills surplus HIREs to stay inside that, deliberately:
    a deferred hire is free because `hires_today` is a per-DAY fibonacci counter, while a deferred
    PLACE loses the day's feed and care with it. So the spill is right and the prediction is wrong.

    Measured, d0 h0, seed 11 -- seven hires wanted, four animals bought, eleven orders for ten slots:

        market(10): HIRE x6, BUY_ANIMAL COW 1, BUY_ANIMAL COW 1, BUY_ANIMAL SHEEP 1, ...SHEEP 1

    The dawn plan routed seven arrivals at their h0 spawn tiles. Six landed. The seventh was re-sent
    by the drip path at h2, and by then the dawn pair had walked off the shed ring, so `_spawn_hand`
    read a different occupancy and put it somewhere else entirely -- a working hand at a tile no
    route mentions.

    Asserted against the hands the day ENDS UP owning, not the ones standing at h1. Once
    `_arrival_plan` spreads a row across h0-h2 to keep anyone off `(5,5)`, a dawn plan routing seven
    hands while two stand at h1 is correct, not over-committed -- the rest are on their way. What
    stays wrong is routing a hand that never appears at all.
    """
    plans = played["plans"].get(day)
    assert plans, f"day {day} never called crew.cover -- the planner did not run"
    n_units, budget, _work, _left = plans[0]
    landed = played["owned_by_dusk"][day]
    assert n_units - 1 <= landed, (
        f"day {day}: the dawn plan routed {n_units - 1} hands (budgets {budget}) but only {landed} "
        f"ever arrived, so {n_units - 1 - landed} route(s) were built for a hand that never existed.")


@pytest.mark.parametrize("day", range(DAYS))
def test_no_hand_is_bought_onto_a_square_it_cannot_leave(played, day):
    """We do not pay a wage for a hand that lands walled in.

    The landing square is not luck and it is not fixed -- `_spawn_hand` reads occupancy at the moment
    each HIRE settles, so it is a function of WHEN the hire is sent. Sending all seven in the hour-0
    block fills the ring in one go and the 3rd and 7th land on `(5,5)`, the one shed-access tile with
    no unlocked orthogonal neighbour while we own NW alone. Sending the same seven an hour apart lands
    them on tiles the earlier hands have already walked off.

    The drip path in the market block implements exactly that -- it skips a walled slot and lets the
    hire come back next turn -- and `HIRE_PINNED_DAYS` covering all 30 days means the hour-0 branch
    always wins and the skip never runs.

    The counter-argument in that block is that a walled hand is "stuck, not useless", because PICKUP
    and DROP test shed-adjacency only, so it can load and unload all day. That is true of the rule and
    false of this agent: `test_no_hand_that_can_move_passes_the_whole_day` measures those same seats
    emitting PASS 24 times. We are not using them as shed loaders, so they are a wage for nothing.
    """
    SA = importlib.import_module(MODULE)
    walled = played["walled_at_h1"][day]
    assert not walled, (
        f"day {day}: hand(s) {sorted(n for n, _p in walled)} were hired onto "
        f"{sorted({p for _n, p in walled})}, which has no unlocked neighbour to step out to, so "
        f"they cannot move, cannot work, and cost a wage. Send them an hour later instead.")


@pytest.mark.parametrize("day", range(DAYS))
def test_no_seat_stands_idle_while_the_planner_drops_a_job(played, day):
    """If any job is left uncovered, every seat the planner was given is carrying work.

    This is the claim `InfeasibleDay` makes and the one worth testing: a job reported as not fitting
    is a claim about turns, and it is only credible once the turns are actually spent. A seat with an
    empty lane has its whole budget unspent, so the same call is asserting both "there is no room"
    and "here are 23 unused turns".

    The failure it was written for is `pool.remove(pick)` in `run_crew` with no re-add -- each hand
    got exactly one lane per pass, and the sweep ran out of hands before it ran out of tiles.
    """
    plans = played["plans"].get(day)
    assert plans, f"day {day} never called crew.cover -- the planner did not run"
    n_units, budget, work, left = plans[0]
    if not left:
        return
    idle = sorted(u for u in range(n_units) if not work.get(u))
    assert not idle, (
        f"day {day}: {len(left)} job(s) reported as not fitting -- {left} -- while seat(s) {idle} "
        f"were given no work at all, out of budgets {budget}. The drop is priced wrong, not tight.")


@pytest.mark.parametrize("day", range(DAYS))
def test_no_hand_passes_the_whole_day(played, day):
    """No seat the farm pays for spends all 24 turns on PASS.

    The emitted-op counterpart to the two above, and the one that cannot be fooled by a planner that
    hands out an empty lane and calls it covered: whatever the plan says it covered, an all-PASS
    seat did nothing.

    **Counts every hired hand, mobile or not, and that is deliberate.** An earlier cut of this test
    exempted seats the board had boxed in, on the grounds that `_mobile` was right to skip them. That
    exemption made the test agree with the defect: a hand bought onto `(5,5)` costs the same wage as
    any other and returns nothing, so "the game did it" is an explanation, not a defence. Where a
    hire LANDS is a function of the hour it is sent, which is ours to choose -- see `_arrival_plan`.

    An idle hand is a wasted wage on any day, and on these days it is worse than that, because a
    WATER that goes untoured turns the tile into a weed two days later (`kaggriculture.py:771`: two
    consecutive unwatered days destroy it).
    """
    seats = played["emitted"][day]
    dead = sorted(name for name, ops in seats.items()
                  if name != "F" and ops and set(ops) <= {"PASS"})
    assert not dead, (
        f"day {day}: seat(s) {dead} emitted PASS on all {len(next(iter(seats.values())))} turns "
        f"while the farm paid their wage.")


@pytest.mark.parametrize("bank,want", [(0, 7), (1, 7), (3, 7), (12, 7), (32, 7), (33, 7), (561, 7),
                                       (85, 6), (3000, 8)])
def test_the_hire_ladder_agrees_with_the_environment(bank, want):
    """`_hires_this_turn` charges what `_do_hire` charges, so it predicts a crew that actually lands.

    Its own docstring is the requirement -- "it must not diverge from what that block actually
    orders" -- and the failure is silent in both directions. `_do_hire` returns without hiring when
    `farm["money"] < cost` (`kaggriculture.py:691`), so an over-prediction leaves a routed hand that
    never appears and its whole lane is deleted rather than deferred.

    The ladder is `mult * _fib(hires_today)` with `_fib(0) = 1` (`:677`), a per-DAY counter, so seven
    hires cost `1 1 2 3 5 8 13` = 33. Ours ran `a, b = 0, 1` and charged `0 1 1 2 3 5 8` = 20 -- one
    position off, which is affordable exactly when the bank sits between the two totals. Compared
    against the reference implementation rather than a pasted table so it cannot drift.
    """
    kg = importlib.import_module("reference.kaggriculture")
    SA = importlib.import_module(MODULE)

    left, expect = float(bank), 0
    for k in range(want):
        cost = kg._hire_cost(k)
        if left < cost:
            break
        left -= cost
        expect += 1

    state = {"hired": 0}
    row = {"hands": want}
    got = SA._hires_this_turn(state, row, 0, 0, float(bank))
    assert got == expect, (
        f"bank ${bank} wanting {want} hands: predicted {got}, the env will actually hire {expect} "
        f"(ladder {[kg._hire_cost(k) for k in range(want)]}).")
