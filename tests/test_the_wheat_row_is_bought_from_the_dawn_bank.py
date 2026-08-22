"""The wheat row is offered at the hour the recording we are replaying offers it.

**This file used to assert `first == 0` on every day, and that assertion is dead.** It was written
when the day chose its own market order, before `REPLAY_OPENING_DAYS` became `tuple(range(30))`.
The agent now replays a カワシギ recording on every day of the season, so the hour is his, not ours,
and the old rule demanded we deviate from the tape we deliberately replay.

Measured 2026-08-22, seed 11, our first BUY_PRODUCT WHEAT hour against the armed recording's:

     day   ours h   tape h   armed recording
       0        0        0   92498144
       1       18       18   92498144
       2        2        2   92498144
       4        0        0   92498144
       5       15       15   91907974      <- q4 latch arms here
       6        5        5   91907974
       7        4        4   91907974
       8        0        0   91907974
       9        3        3   91907974
      10        3        3   91907974
      11        6        6   91907974

Eight of those were red. Every one of them matched the tape exactly. The old failure message --
"d10 row wants 33 wheat; first order is at h03, after the day has already spent its dawn bank on
hires" -- was describing カワシギ's own choice and calling it our defect. He does not buy at h0 on
every day; he buys at h18, h2, h15, h5, h4, h3, h3 and h6.

**What is kept, and why this is repointed rather than deleted.** The money gate
(`test_the_money_lands_on_his_turn.py`) covers BUY_LAND, HIRE, BUY_ANIMAL and BUY_SEED. It does NOT
cover BUY_PRODUCT, and the wheat row is the largest BUY_PRODUCT the season makes. So this file now
gates the same property for the op nothing else watches: a day that replays a recording must place
that recording's wheat order, at that recording's hour. A replay that silently drops or delays the
wheat row shows here and nowhere else.

The original economics still hold for any day the replay does not cover -- the whole $3,000 goes on
hires and animals before wheat is considered, and `feed 4/5` and `care 4/5` are the same defect one
step downstream. `REPLAY_OPENING_DAYS` covers all 30 today, so there is no such day, and a rule that
can never run is not a gate. If the replay is ever narrowed, restore the `first == 0` assertion for
the days it gives back.
"""
import collections
import kagg.plan as _PLAN
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top2/91854176.json"
SCHEDULE = _PLAN.SHIPPED_PLAN
TEAM = "Victor @ Tufa Labs"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAYS = 12
TPD = 24


class _WhichTape(dict):
    """An opening that records which recording governed each day. See the money gate."""

    def __init__(self, opening, tape, log):
        super().__init__(opening)
        self._tape, self._log = tape, log

    def __contains__(self, step):
        self._log[int(step) // 24] = self._tape
        return super().__contains__(step)


def _tape_wheat_hours(path, team):
    """`{day: [hours]}` of every BUY_PRODUCT WHEAT in a recording, from that team's seat."""
    d = json.loads(pathlib.Path(path).read_text())
    seat = d["info"]["TeamNames"].index(team)
    out = collections.defaultdict(list)
    for step, frame in enumerate(d["steps"][1:]):
        a = (frame[seat] or {}).get("action") or {}
        for o in (a.get("market") or []):
            if len(o) >= 3 and o[0] == "BUY_PRODUCT" and o[1] == "WHEAT":
                out[step // TPD].append(step % TPD)
    return out


@pytest.fixture(scope="module")
def emitted():
    """`({day: [(hour, qty), ...]}, {day: recording})` for every BUY_PRODUCT WHEAT emitted."""
    SA = importlib.import_module(MODULE)
    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    out = collections.defaultdict(list)
    armed = {}
    plain = SA._replay_opening
    SA._replay_opening = lambda days, tape=None, team=None: _WhichTape(
        plain(days, tape, team), tape, armed)
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            o0 = env.state[0].observation
            a0, a1 = agent(o0), opp[t]
            for o in (a0.get("market") or []):
                if o and o[0] == "BUY_PRODUCT" and o[1] == "WHEAT":
                    out[t // TPD].append((t % TPD, int(o[2])))
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        SA._replay_opening = plain

    opening = SA.REPLAY_OPENING_TAPE[(False, False)][0]
    by_day = {d: armed.get(d, opening) for d in range(DAYS)}
    return dict(out), by_day


def _rows():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): int((v.get("buys") or {}).get("WHEAT", 0)) for k, v in raw.items()}


def test_the_premise_some_day_buys_wheat(emitted):
    """Guard. With no wheat row in range the assertion below is vacuous."""
    rows = _rows()
    assert [d for d in range(DAYS) if rows.get(d, 0) > 0], f"no wheat row in d0-d{DAYS - 1}"


def test_the_premise_the_agent_actually_replays(emitted):
    """Guard on the gate itself.

    Every assertion below compares us to the recording we replay. If no opening were consulted --
    a missing tape file makes `_replay_opening` return `{}` by design -- each comparison would be
    against a recording that never governed anything, and would pass or fail for reasons that have
    nothing to do with the agent. That silent degradation cost 80 minutes and 2,800 seasons of a
    box sweep on 2026-08-22.
    """
    _got, by_day = emitted
    SA = importlib.import_module(MODULE)
    assert SA.REPLAY_OPENING_DAYS, "REPLAY_OPENING_DAYS is empty; nothing is replayed"
    for day in range(DAYS):
        assert pathlib.Path(by_day[day]).exists(), (
            f"d{day} names recording {by_day[day]}, which is not on disk. `_replay_opening` "
            f"returns {{}} for a missing file and the day degrades to the planner in silence.")


@pytest.mark.parametrize("day", range(DAYS))
def test_the_wheat_row_lands_on_the_recordings_hour(emitted, day):
    """A replayed day places that recording's wheat order, at that recording's hour.

    Not `first == 0`. See the module docstring: the hour is カワシギ's, and on eight of these twelve
    days it is not zero. What this catches is a replay that drops the row or slides it.
    """
    rows = _rows()
    want = rows.get(day, 0)
    if want <= 0:
        pytest.skip(f"d{day} buys no wheat")

    got, by_day = emitted
    recording = by_day[day]
    team = next(t for p, t in _replay_tape_values() if p == recording)
    theirs = _tape_wheat_hours(REPO / recording, team).get(day, [])
    if not theirs:
        pytest.skip(f"d{day}: {pathlib.Path(recording).stem} places no wheat order")

    ours = got.get(day, [])
    assert ours, (
        f"d{day} row wants {want} wheat and we emitted no order at all, while "
        f"{pathlib.Path(recording).stem} orders at h{min(theirs):02d}. The replay dropped the row.")
    assert min(h for h, _q in ours) == min(theirs), (
        f"d{day} wheat: ours h{min(h for h, _q in ours):02d} / "
        f"{pathlib.Path(recording).stem} h{min(theirs):02d}. We are replaying that recording on "
        f"this day, so the hour is its choice, not ours. Orders: {ours}")


def _replay_tape_values():
    """`(path, team)` for every entry in `REPLAY_OPENING_TAPE`, deduplicated."""
    SA = importlib.import_module(MODULE)
    return list(dict.fromkeys(SA.REPLAY_OPENING_TAPE.values()))
