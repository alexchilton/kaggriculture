"""d0-d6, per day, per product: what we trade must equal what the plan says to trade.

**The tape cannot be wrong.** `data/seed_scripts/top_guys/90494364/schedule.json` was derived from
Seb's replay and Seb's replay is the thing we are copying, so any disagreement between the two is
ours by construction. That is why `test_the_tape_matches_the_plan_it_was_derived_from` runs first
and must PASS: it proves the target is reachable inside this environment, on this seed, with this
schedule. Once that is green, a failure in the other two tests is a defect in our agent and cannot
be argued into being a property of the game.

Measured 2026-08-09, why this exists:

    SELL           plan                tape              ours
      d0           (no sells row)      -                 WHEAT 7
      d1           FERTILIZER 4        FERTILIZER 4      FERTILIZER 2
      d4           WHEAT 28 FERT 4     WHEAT 28 FERT 4   WHEAT 35 FERT 5

The d0 row is the origin of everything downstream. Seven wheat at $27 is $189 we were never meant
to have, and it is exactly what lets our `BUY_LAND` succeed on d4 where the tape's is refused for
want of cash and does not land until d8. `tiles 50/25` from d4, and the ~$1,000 money gap that
follows it, are that one unasked-for sale leaking forward -- not separate defects.

Fills come from `kagg/analysis/fills.py`, which wraps `_commit_unit`. Never count offers: the agent
re-posts an order every turn until it lands, and `docs/` records three separate occasions where a
proxy for this number produced a confident wrong answer.
"""
import collections
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/90494364.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/90494364/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
SEED = 11
DAYS = 7

#: The agent under test. `1455` is the only artifact that ever scored 1455 and this is that planner
#: plus the market graft plus the shop-adaptive herd. It must be driven by the schedule it was
#: calibrated for -- 90494364, the one loaded above -- or the comparison measures the wrong pairing.
MODULE = "kagg.search.schedule_agent_1455mh"


def _schedule():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): v for k, v in raw.items()}


def _thin(sched):
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def _tape_policy(seat_wanted):
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    src = seat if seat_wanted == 0 else 1 - seat
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[src] or {} for step in d["steps"][1:])]
    return lambda obs, t: acts[t]


def _play(who):
    """Play DAYS days in seat 0 and return {(day, op, item): units} of ACTUAL fills."""
    import importlib

    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

    sched = _schedule()
    thin = _thin(sched)
    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    if who == "ours":
        SA = importlib.import_module(MODULE)
        p0 = SA.make_agent(thin, 0, router=True)
        act0 = lambda o, t: p0(o)          # noqa: E731
    else:
        act0 = _tape_policy(0)
    opp = _tape_policy(1)

    out = collections.Counter()
    with record_fills(env) as fills:
        # `_rows` is append-only per (seat, op, item), so the units added since the previous turn
        # are the tail of each list. Counting lengths per turn attributes each unit to its own day.
        seen = collections.Counter()
        for t in range(24 * DAYS):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = act0(o0, t), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            for (seat, op, item), prices in fills._rows.items():
                if seat != 0:
                    continue
                new = len(prices) - seen[(op, item)]
                if new:
                    out[(t // 24, op, item)] += new
                    seen[(op, item)] = len(prices)
    assert fills.unattributed == 0, "a fill could not be attributed to a seat; the map is broken"
    return out


@pytest.fixture(scope="module")
def tape_fills():
    return _play("tape")


@pytest.fixture(scope="module")
def our_fills():
    return _play("ours")


def _wanted(sched, day, row):
    return {k: int(v) for k, v in (sched.get(day, {}).get(row) or {}).items() if int(v)}


def _got(fills, day, op):
    return {item: n for (d, o, item), n in fills.items() if d == day and o == op and n}


def _report(label, sched, fills, row, op):
    """Every day's plan against every day's fills, as one readable block."""
    bad = []
    for day in range(DAYS):
        want, got = _wanted(sched, day, row), _got(fills, day, op)
        if want != got:
            bad.append(f"    d{day}  plan {want or '{}'}   actual {got or '{}'}")
    return "" if not bad else f"{label} does not match the plan:\n" + "\n".join(bad)


def test_the_tape_matches_the_plan_it_was_derived_from(tape_fills):
    """The control. If this fails, the schedule or the harness is wrong and NOTHING else here means
    anything -- do not touch the agent until it passes."""
    sched = _schedule()
    problems = [_report("tape SELL", sched, tape_fills, "sells", "SELL"),
                _report("tape BUY_PRODUCT", sched, tape_fills, "buys", "BUY_PRODUCT")]
    problems = [p for p in problems if p]
    assert not problems, "\n".join(problems)


def test_our_sells_match_the_plan_every_day(our_fills):
    """Selling anything the plan does not name, on a day it does not name, is a defect.

    It is not a free extra: the d0 wheat funds a d4 land parcel the tape cannot afford, so an
    unasked-for sale on day zero changes the board for the rest of the season.
    """
    problem = _report("our SELL", _schedule(), our_fills, "sells", "SELL")
    assert not problem, problem


def test_our_buys_match_the_plan_every_day(our_fills):
    problem = _report("our BUY_PRODUCT", _schedule(), our_fills, "buys", "BUY_PRODUCT")
    assert not problem, problem


def _play_day_zero():
    """Ops and end-of-day board for d0, ours and the tape, from the same seed and opponent."""
    import importlib

    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

    sched = _schedule()
    thin = _thin(sched)
    out = {}
    for who in ("ours", "tape"):
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        if who == "ours":
            SA = importlib.import_module(MODULE)
            p0 = SA.make_agent(thin, 0, router=True)
            act0 = lambda o, t: p0(o)          # noqa: E731
        else:
            act0 = _tape_policy(0)
        opp = _tape_policy(1)
        ops = collections.Counter()
        with record_fills(env) as fills:
            for t in range(24):
                o0, o1 = env.state[0].observation, env.state[1].observation
                a0, a1 = act0(o0, t), opp(o1, t)
                n0 = len(o0["farms"][0].get("hands") or [])
                n1 = len(o0["farms"][1].get("hands") or [])
                for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
                    if a:
                        ops[a[0]] += 1
                        ops["_turns"] += 1
                env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                           "market": a0["market"]},
                          {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                           "market": a1["market"]}])
            for op in ("SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL"):
                ops[op] = fills.units(0, op)
        farm = env.state[0].observation["farms"][0]
        board = collections.Counter(money=int(farm["money"]))
        for row in farm["tiles"]:
            for c in row:
                if c == "LOCKED":
                    continue
                board["tiles"] += 1
                if isinstance(c, dict):
                    if c.get("kind") == "PLANT":
                        board["crop_" + str(c.get("crop"))] += 1
                    else:
                        board["pens"] += 1
                    if c.get("animal"):
                        board["an_" + str(c["animal"])] += 1
        out[who] = (ops, board)
    return out


#: d0 rows that MATCH the tape as of 2026-08-09, after `allow` was made to bind on both sell paths.
#: This list is the regression guard and nothing may be removed from it to make a run pass -- if a
#: change takes a row off this list, the change is wrong.
#:
#: PICKUP and DROP are deliberately absent: tour shape, and Alex ruled them out of scope. The turn
#: budget is absent because it does NOT match yet -- see the xfail below, which is the honest record
#: of that rather than a silent omission.
D0_MATCHING_OPS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "DIG",
                   "BUILD_PASTURE", "BUILD_COOP", "PLACE", "FERTILIZE",
                   "SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL")


def test_day_zero_still_matches_the_tape_on_every_row_it_reached():
    """**The regression guard for everything fixed on d0 today, and the reason it is separate.**

    `test_our_sells_match_the_plan_every_day` asserts over d0-d6 in one message and is RED for
    d1-d5, so a d0 regression would appear as one more line in an already-failing test and be
    invisible. A guard has to be able to go from green to red on its own.

    What d0 looked like before, and after making `allow` bind on the `price_ok` sell path:

        feed        1/4  ->  4/4
        care        1/4  ->  4/4
        sell        7/0  ->  0/0     (the wheat wash trade: buy 8 at $27, sell 7 back at $27)
        money   760/566  ->  566/566
    """
    got = _play_day_zero()
    (ours, our_board), (tape, tape_board) = got["ours"], got["tape"]
    bad = [f"    {op:<20} ours {ours[op]}  tape {tape[op]}"
           for op in D0_MATCHING_OPS if ours[op] != tape[op]]
    bad += [f"    board {k:<14} ours {v}  tape {tape_board[k]}"
            for k, v in sorted(our_board.items()) if v != tape_board[k]]
    bad += [f"    board {k:<14} ours {our_board[k]}  tape {v}"
            for k, v in sorted(tape_board.items()) if k not in our_board and v]
    assert not bad, "d0 has REGRESSED -- these matched the tape and no longer do:\n" + "\n".join(bad)


@pytest.mark.xfail(strict=True, reason="d0 turn budget: we spend 182 unit-turns to the tape's 185, "
                                       "and idle 78 against 64. Not pickup/drop noise -- three "
                                       "units simply never act. Unfixed, recorded rather than "
                                       "quietly left out of the guard above.")
def test_day_zero_spends_the_same_unit_turns_as_the_tape():
    got = _play_day_zero()
    assert got["ours"][0]["_turns"] == got["tape"][0]["_turns"]
    assert got["ours"][0]["PASS"] == got["tape"][0]["PASS"]


def test_nothing_the_row_asked_to_sell_ends_the_day_in_a_hand():
    """The mechanism behind d1 selling 2 FERTILIZER against a row of 4.

    **A wrong theory first, recorded so it is not tried again.** The fertilizer reserve
    (`have = max(0, have - want)`, holding back stock a watered tile could still use) looked like
    the cause and is not: flooring that reserve at the row changes the d0-d6 table by nothing.

    Traced per turn instead, d1, seed 11, weeds off -- `shed[FERTILIZER]` is **0 on all 24 turns**:

        h3  COLLECT   carried 0->1
        h4  DROP      SELL FERTILIZER 1     carried 1->0
        h7  COLLECT   carried 1
        h8  COLLECT   carried 2
        h11 DROP      SELL FERTILIZER 1     carried 2->1
        h12 COLLECT   carried 2
        h13..h23      carried 2, shed 0, no DROP, no SELL

    `_commit_unit` sells out of `private["shed"]`, so a unit holding fertilizer cannot sell it. We
    collect 4 -- exactly what he collects -- and deliver 2. The only two sales happen on the turns
    straight after a DROP. The tape DROPs 6 times on d1; we DROP 3.

    So this is not a market rule at all. It is the same defect as d0's `feed 1/4`: the tour is
    committed early and has no delivery leg for goods that appear during the day. Asserted here on
    the state rather than on the sell count, so that a sell-rule change cannot make it pass without
    the goods actually arriving.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    thin = _thin(sched)
    SA = importlib.import_module(MODULE)
    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    opp = _tape_policy(1)

    stranded = {}
    for t in range(24 * DAYS):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        if t % 24 == 23:                      # dusk, before the rollover deletes what will not fit
            day = t // 24
            wanted = set((sched.get(day, {}).get("sells") or {}))
            held = collections.Counter()
            for iv in ((o0.get("private") or {}).get("inventories") or []):
                for k, v in (iv or {}).items():
                    if k in wanted and int(v) > 0:
                        held[k] += int(v)
            if held:
                stranded[day] = dict(held)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert not stranded, (
        "product the day's own `sells` row asked for was still in a hand at dusk, so it was never "
        "sellable that day:\n"
        + "\n".join(f"    d{d}  {h}" for d, h in sorted(stranded.items()))
        + "\n  The sell rule cannot reach this -- the market sells from the SHED. It is a routing "
          "defect: nothing schedules the trip home."
    )


def test_the_day_is_planned_once_and_only_at_dawn():
    """**One plan per day, built at hour 0, covering all 24 hours.**

    The day is fully deterministic: `hires`, `animals_bought`, `builds`, `places`, `plants`, `buys`
    and `sells` are all written in the schedule before it starts, and the board evolves from them by
    rules we simulate exactly. There is nothing for a mid-day replan to discover.

    The trigger this pins is the crew one. `interpreter` applies unit actions BEFORE
    `_process_market` (`kaggriculture.py:922` then `:928`), so a hand hired at hour 0 does not exist
    when hour 0 is planned and appears at hour 1. `state["crew"] != len(live)` then fires and throws
    the dawn plan away -- so what actually covers the day is an hour-1 plan for 23 hours, and hour 0
    is planned for the pre-hire crew alone.

    The fix is not to stop hiring at dawn; the tape hires at dawn too. It is for the dawn plan to
    ROUTE the hands it knows are coming, from the square `_spawn_hand` will land them on and from
    the turn they can first act.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    SA = importlib.import_module(MODULE)
    solves = collections.Counter()

    real_solve = SA._solve
    box = {"hour": 0, "day": 0}

    def counting_solve(*a, **k):
        solves[(box["day"], box["hour"])] += 1
        return real_solve(*a, **k)

    SA._solve = counting_solve
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
        env.reset(2)
        agent = SA.make_agent(_thin(sched), 0, router=True)
        opp = _tape_policy(1)
        for t in range(24 * DAYS):
            box["day"], box["hour"] = t // 24, t % 24
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        SA._solve = real_solve

    per_day = collections.Counter()
    for (day, _hour), n in solves.items():
        per_day[day] += n
    late = sorted((d, h, n) for (d, h), n in solves.items() if h != 0)

    assert not late and all(per_day[d] == 1 for d in range(DAYS)), (
        "the day was not planned once at dawn:\n"
        + "\n".join(f"    d{d}  {per_day[d]} plan(s)" for d in range(DAYS))
        + ("\n  replans away from hour 0:\n"
           + "\n".join(f"    d{d} h{h}  x{n}" for d, h, n in late) if late else "")
    )


def test_the_dawn_plan_can_see_the_goods_the_day_is_about_to_buy():
    """**The dawn plan is built before the day's shopping settles, and must be told about it.**

    `interpreter` applies unit actions and only THEN calls `_process_market`
    (`kaggriculture.py:922` then `:928`), so day 0's `buys: {WHEAT: 8}` reaches the shed at the end
    of hour 0. `_router_acts` runs at the top of hour 0 and hands `_solve` the shed as it stands --
    empty of that wheat. FEED needs WHEAT, so the plan correctly concludes there is nothing to feed
    with and routes no feeds at all.

    That, not the crew, is why a single dawn plan lost to a plan rebuilt at hour 1: the hour-1 plan
    was simply the first one that could see the goods. Measured on d0 with the crew planned ahead:

        feed 0/4    pickup 1/5    drop 0/1     (dawn plan, blind to the buys)
        feed 2/4    pickup 5/5    drop 1/1     (rebuilt at hour 1, wheat now in the shed)

    The fix is the same shape as `_arrivals`: the row already says what will be bought, so credit it
    at plan time instead of discovering it an hour later.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    SA = importlib.import_module(MODULE)
    seen = {}

    real_solve = SA._solve
    box = {"day": 0, "hour": 0}

    def spying_solve(*a, **k):
        if box["hour"] == 0 and box["day"] not in seen:
            seen[box["day"]] = collections.Counter(k.get("supply") or {})
        return real_solve(*a, **k)

    SA._solve = spying_solve
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
        env.reset(2)
        agent = SA.make_agent(_thin(sched), 0, router=True)
        opp = _tape_policy(1)
        for t in range(24 * DAYS):
            box["day"], box["hour"] = t // 24, t % 24
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        SA._solve = real_solve

    short = []
    for day in range(DAYS):
        buys = {p: int(q) for p, q in (sched.get(day, {}).get("buys") or {}).items() if int(q) > 0}
        if not buys:
            continue
        supply = seen.get(day, collections.Counter())
        for product, qty in buys.items():
            if supply.get(product, 0) < qty:
                short.append(f"    d{day}  {product}: plan sees {supply.get(product, 0)}, "
                             f"the row buys {qty} this morning")

    assert not short, (
        "the dawn plan was built blind to goods the same turn's market phase buys:\n"
        + "\n".join(short)
        + "\n  Nothing downstream recovers this -- a FEED that was never routed is not a FEED that "
          "happens late, it is a turn spent PASSing."
    )


def test_the_dawn_plan_offers_a_place_for_every_animal_the_day_buys():
    """**A pen that does not exist yet offers no PLACE, so a one-plan day places nothing.**

    `build_nodes` reaches the PLACE branch through `elif kind in ("PASTURE", "COOP")` -- a tile that
    is ALREADY a pen. On day 0 the pens are built during the day, so at dawn the whole node set is
    `{BUILD: 8, PLANT: 17}` and there is no placement in it to route. The four placements that do
    happen today exist only because the crew-change replan at hour 1 and hour 3 rebuilds the plan
    against a board where some pens have since appeared.

    Everything hanging off a PLACE goes with it. `SERVE_THE_ANIMAL_IT_PLACES` attaches the FEED and
    the CARE to the placement node, so `feed 0/4` and `care 0/4` on a planned-once day 0 are not a
    feeding defect at all -- they are two placements that were never in the plan.

    The pin already knows the answer: `_refresh_pins` writes `pins[spot] = ("BUILD", animal, cost)`,
    so the ground and the beast are chosen together at dawn. The node has to carry the whole chain.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    SA = importlib.import_module(MODULE)
    offered = {}

    real_solve = SA._solve
    box = {"day": 0, "hour": 0}

    def spying_solve(units, nodes, *a, **k):
        if box["hour"] == 0 and box["day"] not in offered:
            seen = collections.Counter()
            for n in nodes:
                for op, *_rest in n.ops:
                    seen[op] += 1
            offered[box["day"]] = seen
        return real_solve(units, nodes, *a, **k)

    SA._solve = spying_solve
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
        env.reset(2)
        agent = SA.make_agent(_thin(sched), 0, router=True)
        opp = _tape_policy(1)
        for t in range(24 * DAYS):
            box["day"], box["hour"] = t // 24, t % 24
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        SA._solve = real_solve

    short = []
    for day in range(DAYS):
        want = sum(int(q) for q in (sched.get(day, {}).get("animals_bought") or {}).values())
        if not want:
            continue
        got = offered.get(day, collections.Counter()).get("PLACE", 0)
        if got < want:
            short.append(f"    d{day}  dawn plan offers {got} PLACE, the row buys {want} animals "
                         f"(nodes offer {dict(offered.get(day, {}))})")

    assert not short, (
        "the dawn plan had no placement to route for animals the day buys:\n" + "\n".join(short)
        + "\n  The pen is BUILT and PLACEd on the same square by the same plan. If the BUILD node "
          "does not carry the PLACE, only a replan can ever find it."
    )


def test_a_placement_is_planned_onto_the_hand_that_builds_its_pen():
    """**PLACE on a pen someone else builds is a walk to an empty square.**

    The route is a visit ORDER; `_live_ops` re-derives the work from the live board at each stop
    (`schedule_agent:1201`). So a hand that arrives at a tile whose pen has not been built yet reads
    a bare square, gets no ops back, and the stop is dropped -- the animal goes home in its hand and
    the walk is spent for nothing. Between two DIFFERENT hands there is no ordering at all, so
    whether the placement works is down to which one happens to arrive first.

    Traced on the day-0 dawn plan, seed 11, with the day planned once:

        u3  ... (3,4)['BUILD'] (3,4)['PLACE','FEED','CARE'] (2,4)['PLACE','FEED','CARE']
        u4  ... (2,4)['BUILD'] (1,4)['BUILD'] ...

    u3 is sent to fill (2,4) and u4 is the hand that builds it. `place` measured 2/4, and the wasted
    walks are where `build_pasture` 6/8 and `plant` 16/17 went.

    `Job.only` already exists for exactly this -- `cover.slot` refuses any unit but the named one --
    so the fix is to name it once the build is placed, not to invent a mechanism.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    SA = importlib.import_module(MODULE)
    CV = importlib.import_module("kagg.search.cover")
    split = {}

    real_plan = CV.plan
    box = {"day": 0, "hour": 0}

    def spying_plan(units, jobs, budget, *a, **k):
        out = real_plan(units, jobs, budget, *a, **k)
        if box["hour"] == 0 and box["day"] not in split:
            who = {}
            # `cover.plan` returns `(routes, uncovered)`.
            for u, st in (out[0] if isinstance(out, tuple) else out).items():
                for n in st["route"]:
                    for op, _item in n.ops:
                        who.setdefault((tuple(n.tile), op), u)
            bad = [(t, who[(t, "BUILD")], who[(t, "PLACE")])
                   for t in {tt for tt, o in who if o == "BUILD"}
                   if (t, "PLACE") in who and who[(t, "PLACE")] != who[(t, "BUILD")]]
            split[box["day"]] = bad
        return out

    CV.plan = spying_plan
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
        env.reset(2)
        agent = SA.make_agent(_thin(sched), 0, router=True)
        opp = _tape_policy(1)
        for t in range(24 * DAYS):
            box["day"], box["hour"] = t // 24, t % 24
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        CV.plan = real_plan

    bad = [f"    d{d}  tile {t}: BUILD on u{b}, PLACE on u{p}"
           for d, rows in sorted(split.items()) for t, b, p in rows]
    assert not bad, (
        "a placement was planned onto a hand that does not build that pen:\n" + "\n".join(bad)
        + "\n  The placing hand arrives at a bare square, `_live_ops` returns nothing and the stop "
          "is dropped. The animal never leaves the shed and the walk is spent."
    )


def test_no_pen_stands_empty_at_dusk_beside_a_shed_holding_its_animal():
    """**A depot stop spent on an empty shed is spent for good.**

    `interpreter` runs the unit phase before `_process_market` (`kaggriculture.py:922` then `:928`),
    so the animals the day buys are not in the shed while hour 0 is being worked. A tour whose draw
    is scheduled at hour 0 therefore picks up nothing, the stop is consumed anyway, and the hand
    walks its whole route unable to do the one thing it was routed for.

    Traced on day 0, seed 11, hands watched from the dawn plan:

        h 0  shed={}                      u0@(4,4) -> BUILD_PASTURE
        h 2  shed={WHEAT:1, SHEEP:2}      u0@(3,4) -> BUILD_PASTURE
        h 3..h23                          u0@(3,4) -> PASS   x21

    Two pens built by that hand, two PLACE stops still in its route, four animals in the shed, and
    twenty-one turns of nothing. `place 2/4`, `feed 0/4` and `sheep 0/2` are all downstream of it.

    Asserted on the BOARD rather than on the route, because that is the thing that must be true: if
    a pen is empty at dusk and the shed still holds an animal that fits it, the day was mis-sequenced
    whatever the plan said.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    SA = importlib.import_module(MODULE)
    R = importlib.import_module("kagg.search.routines")

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(_thin(sched), 0, router=True)
    opp = _tape_policy(1)

    stranded = {}
    for t in range(24 * DAYS):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        if t % 24 == 23:
            farm, priv = o0["farms"][0], o0["private"]
            shed = collections.Counter({k: int(v) for k, v in (priv.get("shed") or {}).items()})
            empty = collections.Counter()
            for row in farm["tiles"]:
                for cell in row:
                    if isinstance(cell, dict) and cell.get("kind") in ("PASTURE", "COOP") \
                            and "animal" not in cell:
                        empty[cell["kind"]] += 1
            waste = {a: shed[a] for a in R.ANIMAL_NAMES
                     if shed[a] > 0 and empty[R.ANIMALS[a]["structure"]] > 0}
            if waste:
                stranded[t // 24] = (waste, dict(empty))
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert not stranded, (
        "an animal sat in the shed at dusk with an empty pen of its own kind standing:\n"
        + "\n".join(f"    d{d}  shed {w}   empty pens {e}" for d, (w, e) in sorted(stranded.items()))
        + "\n  The pen was built and the animal was bought. Only the sequencing failed."
    )


def test_an_animal_placed_today_is_fed_today():
    """**A hand that carries the cow out can walk back for the wheat.**

    `SERVE_THE_ANIMAL_IT_PLACES` puts the FEED and CARE on the placement node, and after the PLACE
    lands `_live_ops` re-derives the tile: `animal_ops(cell, day, inv["WHEAT"] > 0)`. A hand holding
    no wheat gets an empty list back, so the stop is dropped and that pen is never visited again --
    the placement's own feed is lost even though the hand has most of the day left.

    Traced on day 0, seed 11: u0 draws SHEEP 2 and WHEAT 4 and serves both its pens; u4 draws COW 2
    and no wheat, places at h4 and h7, and feeds neither. `feed 2/4`, `care 2/4`.

    It is not a timing problem. The tape's wheat arrives LATER than ours -- hours 5, 7, 9, 11, 12,
    14, 17, 19 against our 1 through 8 -- and it still feeds all four, because its hand goes back.

    An animal placed and not fed also starts its `consecutive_unfed` count on the day it arrives
    (`kaggriculture.py:786`), so this is a survival question and not only a production one.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    SA = importlib.import_module(MODULE)

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(_thin(sched), 0, router=True)
    opp = _tape_policy(1)

    unfed = {}
    for t in range(24 * DAYS):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        if t % 24 == 23:
            farm, priv = o0["farms"][0], o0["private"]
            hungry = [(x, y) for y, row in enumerate(farm["tiles"])
                      for x, cell in enumerate(row)
                      if isinstance(cell, dict) and "animal" in cell and not cell.get("fed_today")]
            wheat = int((priv.get("shed") or {}).get("WHEAT", 0))
            carried = sum(int((iv or {}).get("WHEAT", 0))
                          for iv in (priv.get("inventories") or []))
            if hungry and (wheat or carried):
                unfed[t // 24] = (hungry, wheat, carried)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert not unfed, (
        "an animal went unfed at dusk while wheat was on the farm:\n"
        + "\n".join(f"    d{d}  hungry {h}   shed WHEAT {w}, carried {c}"
                    for d, (h, w, c) in sorted(unfed.items()))
        + "\n  The wheat existed and the hand had turns. Only the trip back was never planned."
    )


def test_no_hand_walks_over_a_hungry_animal_with_the_feed_in_its_hand():
    """**The route is a visit ORDER, so a tile merely passed through is never looked at.**

    `_live_ops` is consulted at route STOPS. A hand walking from one stop to the next crosses tiles
    it is not booked to work, and nothing asks whether the ground under it needs something it is
    already carrying.

    Traced on day 4, seed 11, at the pen (1,4) which ends the day unfed:

        h13   u6@(1,4){WHEAT: 8}  -> EAST
        h15   u5@(1,4){WHEAT: 8}  -> EAST

    Two hands, eight wheat each, standing ON the hungry animal, walking over it. `feed 6/7` and
    `care 6/7` on day 4 and `feed 7/8` on day 6 are this.

    A FEED is not an optimisation: `consecutive_unfed >= 2` removes the animal outright
    (`kaggriculture.py:786`), so the animal this costs is a $400-500 asset plus every remaining day
    of its production. `REQUIRED_OPS = ("FEED",)` already says as much in the planner; the executor
    just never gets the chance to act on it.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    SA = importlib.import_module(MODULE)
    MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(_thin(sched), 0, router=True)
    opp = _tape_policy(1)

    walked = []
    for t in range(24 * DAYS):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        farm, priv = o0["farms"][0], o0["private"]
        invs = priv.get("inventories") or []
        pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
        acts = [a0["farmer"], *a0["hands"]]
        for u, p in enumerate(pos):
            if u >= len(acts) or not acts[u] or acts[u][0] not in MOVES:
                continue
            # **Surplus only, which is the rule and not a softened threshold.** The wheat a hand
            # carries is drawn for the pens still on its OWN route; spending it on the tile
            # underfoot would move the hunger rather than remove it. Three cases in d0-d6 carry
            # exactly one wheat with a feed of their own still to serve, and walking on is correct
            # for all three. Only wheat held ABOVE that count is free to spend here.
            held = int((invs[u] or {}).get("WHEAT", 0) if u < len(invs) else 0)
            owed = sum(1 for r in farm["tiles"] for c in r
                       if isinstance(c, dict) and "animal" in c and not c.get("fed_today"))
            if held <= 1 and owed > 1:
                continue
            if held <= 0:
                continue
            cell = farm["tiles"][p[1]][p[0]]
            if isinstance(cell, dict) and "animal" in cell and not cell.get("fed_today"):
                walked.append(f"    d{t // 24} h{t % 24}  u{u}@{p} carrying "
                              f"{int((invs[u] or {}).get('WHEAT', 0))} WHEAT -> {acts[u][0]}, "
                              f"leaving a hungry {cell['animal']}")
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert not walked, (
        "a hand walked off a tile holding a hungry animal while carrying its feed:\n"
        + "\n".join(walked)
        + "\n  One turn to FEED. `consecutive_unfed >= 2` removes the animal outright."
    )


@pytest.mark.xfail(strict=True, reason=(
    "CARE_WHAT_YOU_STAND_ON is OFF by measurement, not by omission. The rule fires on every hand "
    "crossing the pen on the shed tile, so care overshoots the tape on five days (d0 5/4, d2 8/5, "
    "d4 10/7, d5 9/7) and BREAKS day 0, which is exact without it. Day 6 pays hardest: feed 7/8 -> "
    "4/8, buy_product 7/9 -> 1/9. One extra unit of product tomorrow is not worth a feed today. "
    "Left strict so that if a future change makes the care free, this goes green and says so."))
def test_no_hand_walks_over_a_fed_but_uncared_animal():
    """**The CARE is the same walk-past as the FEED, one step later.**

    `pending_care_bonus` is consumed only on a day the animal is ALSO fed (`router.animal_ops`), so
    a CARE is worth exactly one extra unit of product on the next production day -- and it is worth
    that ONLY on a pen already fed today. It costs one turn and no item at all: `_apply_unit_action`
    just sets `cared_today` (`kaggriculture.py:511-517`).

    So a hand standing on a pen it has just fed, about to walk away, is one turn from banking that
    unit. Day 4 measures `feed 7/7` and `care 6/7` for exactly this reason: the feed now happens
    under the hand's feet and then it moves on.

    Restricted to pens ALREADY FED, so this can never spend a turn on a care that banks nothing.
    """
    import importlib

    from kaggle_environments import make

    sched = _schedule()
    SA = importlib.import_module(MODULE)
    MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(_thin(sched), 0, router=True)
    opp = _tape_policy(1)

    walked = []
    for t in range(24 * DAYS):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        farm = o0["farms"][0]
        pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
        acts = [a0["farmer"], *a0["hands"]]
        for u, p in enumerate(pos):
            if u >= len(acts) or not acts[u] or acts[u][0] not in MOVES:
                continue
            cell = farm["tiles"][p[1]][p[0]]
            if (isinstance(cell, dict) and "animal" in cell
                    and cell.get("fed_today") and not cell.get("cared_today")):
                walked.append(f"    d{t // 24} h{t % 24}  u{u}@{p} -> {acts[u][0]}, "
                              f"leaving a fed but uncared {cell['animal']}")
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert not walked, (
        "a hand walked off a pen it had fed, leaving the care undone:\n" + "\n".join(walked)
        + "\n  One turn, no item, one extra unit of product on the next production day."
    )
