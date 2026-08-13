"""The day works out WHEN its SELL row is due before it routes anything, and is never late.

This is goal 1 of the ferry work, and it is deliberately separate from whether any tile then gets
watered. `cover.materialise` cannot price a shed trip correctly until something tells it the hour
the goods are needed; this asserts that the hour is derived, is derived at dawn, and agrees with a
player who wins the day.

**The ground truth is the tape, and it is unusually clean.** Seb's first DROP and his first SELL
land on the SAME HOUR every day of d0-d6 -- nothing ever sits in his shed waiting for a buyer -- so
the hour he delivers is exactly the hour his cadence needed the goods. Measured off replay
91422988 by `_tape_deadline` below rather than pasted in, so it cannot rot:

    day        d0    d1    d2    d3    d4    d5    d6
    delivers    2     4    15    15    18    17     9
    sells       -     4    15    15    18    17     9

The assertion is ONE-SIDED, and that is the point. Being earlier than Seb is legal and merely
expensive -- it buys a shed trip some hand pays for in turns. Being LATER than Seb is a missed
sale: the market reads the shed and nothing else, and produce that arrives after the row could have
cleared is produce sold at whatever the last unit fetches, or swept into the shed overnight with
the market already shut. So the requirement is `ours <= tape`, per day, and not equality.

Why not assert equality: our farm is not his farm by d4 -- we own a parcel he does not, our bank
differs, and `breakdown.py`'s own tape column is contaminated from d4 on for exactly this reason.
A deadline that tracked his hour exactly would be fitting to a trajectory we do not share.
"""
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
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAYS = 7


def _replay():
    d = json.loads(REPLAY.read_text())
    return d, d["info"]["TeamNames"].index(TEAM)


@pytest.fixture(scope="module")
def tape_due():
    """`{day: hour Seb first has produce in the shed}`, or absent when he delivers nothing.

    Read off DROP, not off SELL: the DROP is the delivery, and it is the thing our planner is being
    asked to schedule. That they coincide on every one of these days is what makes the tape usable
    as a deadline at all, and `test_the_tape_never_banks_before_it_sells` pins it -- if a future day
    breaks the coincidence this fixture stops meaning "deadline" and the test should be re-derived.
    """
    d, seat = _replay()
    steps = d["steps"][1:]
    out = {}
    for day in range(DAYS):
        for h in range(24):
            t = day * 24 + h
            if t >= len(steps):
                break
            a = (steps[t][seat] or {}).get("action") or {}
            ops = [a.get("farmer") or []] + list(a.get("hands") or [])
            if any(o and o[0] == "DROP" for o in ops):
                out[day] = h
                break
    return out


@pytest.fixture(scope="module")
def tape_sold():
    """`{day: hour of Seb's first SELL order}`. Offers, not fills, and that is fine here: the claim
    is only that he is not ASKING to sell before he has delivered, which is a statement about his
    intent and reads correctly off the order stream."""
    d, seat = _replay()
    steps = d["steps"][1:]
    out = {}
    for day in range(DAYS):
        for h in range(24):
            t = day * 24 + h
            if t >= len(steps):
                break
            for m in ((steps[t][seat] or {}).get("action") or {}).get("market") or []:
                if m and m[0] == "SELL" and len(m) > 2 and int(m[2] or 0) > 0:
                    out[day] = h
                    break
            if day in out:
                break
    return out


@pytest.fixture(scope="module")
def ours():
    """`{day: the deadline hour our own dawn plan derived}`, from the real agent on the real board.

    `sell_deadline` is wrapped rather than called with hand-built arguments because the input that
    matters is `short_of_cash`, which is the live bank against the live schedule row. A fixture that
    supplied that by hand would be asserting against my arithmetic instead of the agent's.
    """
    SA = importlib.import_module(MODULE)

    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d, seat = _replay()
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    seen, real = [], SA.sell_deadline

    def spy(hour, selling, short_of_cash):
        got = real(hour, selling, short_of_cash)
        seen.append((hour, selling, short_of_cash, got))
        return got

    SA.sell_deadline = spy
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        out = {}
        for t in range(24 * DAYS):
            o0 = env.state[0].observation
            before = len(seen)
            a0, a1 = agent(o0), opp[t]
            # The FIRST call of each day is the dawn one, and the dawn one is the whole claim:
            # the deadline is an input to the routing, so a value derived after the tours are cut
            # would be a different -- and useless -- number.
            if t % 24 == 0 and len(seen) > before:
                out[t // 24] = seen[before][3]
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        SA.sell_deadline = real
    return out


def test_the_premise_the_deadline_is_computed_at_dawn(ours):
    """Runs first. If `sell_deadline` is never called at hour 0 the two tests below compare empty
    dictionaries and pass while measuring nothing -- the same shape as the `crew.ACTIVE_UNTIL_DAY`
    guard in `test_a_lane_is_cut_to_what_its_hand_can_walk`."""
    assert set(ours) == set(range(DAYS)), (
        f"no dawn deadline was recorded for days {sorted(set(range(DAYS)) - set(ours))}.")


def test_the_tape_never_banks_before_it_sells(tape_due, tape_sold):
    """The property that lets a DROP hour stand in for a deadline at all: Seb does not deliver early
    and sit on it. If this ever fails, `tape_due` is measuring storage, not cadence."""
    off = {d: (tape_due.get(d), h) for d, h in tape_sold.items() if tape_due.get(d) != h}
    assert not off, "\n".join(
        f"day {d}: first DROP h{drop}, first SELL h{sell} -- he banked {sell - (drop or 0)}h early"
        for d, (drop, sell) in sorted(off.items()))


def test_every_day_that_sells_has_a_deadline(ours):
    """A day whose row asks for produce must name an hour by which it is owed. `None` means the
    routing falls back to pricing every unit as due immediately, which is the defect."""
    raw = json.loads(SCHEDULE.read_text())
    sells = {int(k): (v.get("sells") or {}) for k, v in raw.items()}
    missing = [d for d in sorted(ours)
               if any(int(q) > 0 for q in sells.get(d, {}).values()) and ours[d] is None]
    assert not missing, (
        f"days {missing} sell produce and derived no delivery deadline.")


def test_no_day_plans_to_deliver_later_than_the_tape(ours, tape_due):
    """The one that matters. Earlier than Seb is allowed and merely costs turns; later than Seb is a
    sale we cannot make, because the market reads the shed and the row is a day total."""
    late = {d: (ours[d], tape_due[d]) for d in sorted(ours)
            if d in tape_due and ours[d] is not None and ours[d] > tape_due[d]}
    assert not late, "\n".join(
        f"day {d}: we plan the row into the shed by h{got}, the tape has it there at h{want} "
        f"-- {got - want}h late"
        for d, (got, want) in sorted(late.items()))
