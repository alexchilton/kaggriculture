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
