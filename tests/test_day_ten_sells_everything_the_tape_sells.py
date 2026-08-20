"""d10 fills every unit the tape fills, so the crew planner must not plan it.

`ACTIVE_EXTRA_DAYS = {10}` sent d10 to `crew.cover` because under `cover.cover` it "stranded TWO
hands for all 24 turns, bought six of a twelve-wheat row, and read `pass 134/78`". That was measured
when d8 planted nine of ten and d9 planted two of one -- d10 opened on a board that was not the
tape's. With `Job.turns` charging the second water on a harvest-and-replant stop, d8 and d9 are
exact and d10 opens where the tape opens.

Re-measured there, seed 11, the exemption now costs:

                       crew planner       cover.cover
    d10  plant            16/23              19/23
    d10  water            35/43              39/43
    d10  sell             46/55              55/55
    d11  harvest           3/4                4/4
    d12  plant             7/8                8/8
    d12  harvest         11/13              13/13
    d12  fertilize         2/3                3/3

d0-d9 are identical under both, so this is a d10-and-after change only.

SELL is the assertion because it is an EXACT per-unit fill (`kagg/analysis/fills.py`), never an
offer, and because d10 is the day the melon crop lands -- 30 units, the largest single settlement of
the first half of the season. Getting 46 of 55 away is nine units of melon left in a hand at dusk.
"""
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

DAY = 10


def _sells(make_me, replay, team, thin, economy, seed=11, tpd=24):
    """Per-day SELL fills for seat 0, up to and including `DAY`."""
    from kaggle_environments import make

    import breakdown as B
    from kagg.analysis.fills import record_fills

    env = make("kaggriculture", configuration=dict(economy, seed=seed, weedSpawnChance=0.0),
               debug=True)
    env.reset(2)
    me, opp = make_me(), B.tape_policy(replay, team, 1)
    per, prev = collections.Counter(), 0
    with record_fills() as f:
        for t in range(tpd * (DAY + 1)):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = me(o0, t), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            now = f.units(0, "SELL")
            per[t // tpd] += now - prev
            prev = now
    return per


def test_day_ten_gets_every_unit_away_that_the_tape_does():
    import breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent")
    CREW = importlib.import_module("kagg.search.crew")
    replay, schedule, team = B.TAPES["victor"]
    raw = json.loads(pathlib.Path(schedule).read_text())
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
            for k, r in raw.items()}
    economy = B.env_config(replay)

    assert DAY not in CREW.ACTIVE_EXTRA_DAYS and DAY >= CREW.ACTIVE_UNTIL_DAY, (
        f"d{DAY} is still routed to the crew planner (ACTIVE_UNTIL_DAY={CREW.ACTIVE_UNTIL_DAY}, "
        f"ACTIVE_EXTRA_DAYS={set(CREW.ACTIVE_EXTRA_DAYS)}). It was exempted on a board where d8 and "
        f"d9 were wrong; on the corrected board it costs nine sell fills on d10.")

    his = _sells(lambda: B.tape_policy(replay, team, 0), replay, team, thin, economy)
    ours = _sells(lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True)),
                  replay, team, thin, economy)

    assert ours[DAY] == his[DAY], (
        f"d{DAY} filled {ours[DAY]} SELL units against the tape's {his[DAY]}. d{DAY} is the day the "
        f"melon crop lands; a shortfall here is produce sitting in a hand when the market closes.")
