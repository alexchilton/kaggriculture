"""A day's idle turns are moved to the hand that can reach the work, not left where they fell.

`cover.cover`'s fair-share cap is justified on this principle, stated in the file itself:

    Units are hired for the whole day whether they move or not, so an idle unit's turns are free
    and the scarce resource is per-unit TIME, not total walking.

`COMPACT` then ranks relocations the other way. It accepts a move only when TOTAL turns fall:

    gain = ((used[u] - got[0]) if v == u
            else (used[u] + used[v]) - (without + got[0]))
    if gain > 0 and (best is None or gain > best[0]):

So a relocation that takes work off a saturated hand and gives it to an idle one -- raising total
walking, lowering the maximum -- is refused, and the saturated hand never gets the headroom to take
the job only it can reach.

Measured on Victor's d12, seed 11. Four ripe tiles sit uncovered in the north-east corner:

    (8,0) (9,0) (8,1) (9,1)     each WATER,HARVEST,PLANT = 4 turns of work

u7 walks to the (9,2) pen and back every day, six squares each way, and those four tiles lie on the
path. Inserting them into u7 costs +1, 0, 0 and -1 turns of TRAVEL -- they are free to reach. The
only cost is the 16 turns of work, and u7 has none spare:

    slack   u0:-3  u1:11  u2:4  u3:2  u4:7  u5:7  u6:2  u7:-3  u8:-5  u9:0  u10:3
    total spare 36, largest single pool 11

Thirty-six idle turns exist and the sixteen needed cannot be assembled on one hand. u1 starts on the
shed ring with eleven of them; u7's three shed stops would cost it almost nothing to take.

The premise test guards the measurement: if the day ever stops having more spare turns than the
dropped work needs, this file is asserting something it never measured and must be re-derived.
"""
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
FOCUS_DAY = 12
CORNER = {(8, 0), (9, 0), (8, 1), (9, 1)}

_cache = {}


def _dawn_plan(day):
    """The day's FIRST `cover.plan` call: (units, jobs, budget, routes, uncovered, cost fn)."""
    if day in _cache:
        return _cache[day]
    from kaggle_environments import make

    import breakdown as B
    from kagg.search import cover as DP
    from kagg.search import crew as CREW

    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    replay, schedule, team = B.TAPES["victor"]
    raw = json.loads(pathlib.Path(schedule).read_text())
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
            for k, r in raw.items()}

    got = {}
    real, strict = DP.plan, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, depots=DP.SHED, carry=None, supply=None, deliver=True,
            wanted=None, rush=False, day_=None, due=None, **kw):
        d = kw.pop("day", day_)
        out, unc = real(units, jobs, budget, depots, carry, supply, deliver, wanted, rush, d, due)
        if d == day and not got:
            got.update(units=list(units), jobs=list(jobs), budget=list(budget),
                       depots=tuple(depots) or DP.SHED, carry=dict(carry or {}),
                       wanted=wanted, rush=rush, due=due,
                       routes={u: list(st.get("route") or ()) for u, st in out.items()},
                       unc=list(unc or []))
        return out, unc

    DP.plan, CREW.STRICT_FEASIBILITY = spy, False
    try:
        env = make("kaggriculture",
                   configuration=dict(B.env_config(replay), seed=11, weedSpawnChance=0.0),
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        opp = B.tape_policy(replay, team, 1)
        for t in range(TPD * day + 1):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        DP.plan, CREW.STRICT_FEASIBILITY = real, strict

    assert got, f"day {day} never called cover.plan -- the planner did not run"
    _cache[day] = got
    return got


def _slack(got):
    """`{unit: budget - turns its route actually costs}`, using the planner's own cost model."""
    from kagg.search import cover as DP

    by_tile = {tuple(j.tile): j for j in got["jobs"]}
    out = {}
    for u in range(len(got["units"])):
        seq = [by_tile[tuple(n.tile)] for n in got["routes"].get(u, []) if tuple(n.tile) in by_tile]
        cost = DP.turns(got["units"][u],
                        DP.materialise(got["units"][u], seq, got["carry"].get(u) or {},
                                       got["depots"], got["wanted"], False, got["rush"],
                                       due=got["due"]))
        out[u] = got["budget"][u] - cost
    return out


def test_the_premise_the_day_has_more_spare_turns_than_it_drops():
    """If the day stops having spare turns, the defect is capacity and this file measures nothing."""
    got = _dawn_plan(FOCUS_DAY)
    spare = sum(max(0, s) for s in _slack(got).values())
    owed = sum(j.turns for j in got["unc"])
    assert got["unc"], (
        f"d{FOCUS_DAY} now covers everything; this file's premise is stale and the corner it was "
        f"written for is gone.")
    assert spare > owed, (
        f"d{FOCUS_DAY} has {spare} spare unit-turns against {owed} turns of dropped work. The day "
        f"is genuinely short of capacity, so relocating turns cannot fix it and this test is "
        f"asserting the wrong thing.")


def test_the_ripe_corner_is_worked_by_the_hand_that_walks_past_it():
    got = _dawn_plan(FOCUS_DAY)
    dropped = {tuple(j.tile) for j in got["unc"]}
    slack = _slack(got)
    assert not (dropped & CORNER), (
        f"d{FOCUS_DAY} leaves {sorted(dropped & CORNER)} unworked while {sum(max(0, s) for s in slack.values())} "
        f"unit-turns sit idle ({ {u: s for u, s in slack.items() if s > 0} }). u7 walks to the (9,2) "
        f"pen and back past every one of them; the turns to do the work exist, on other hands, and "
        f"`COMPACT` will not move them because relocating raises TOTAL turns while lowering the max.")
