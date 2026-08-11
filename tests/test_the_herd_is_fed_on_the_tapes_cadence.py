"""The feed cadence is read off the tape being matched, not inherited from a different one.

`FEED_ONLY_WHEN_IT_BUYS_SOMETHING` withholds a FEED from a pen that is neither hungry nor about to
produce, on the argument -- correct, and sourced from `kaggriculture.py:795-820` -- that production
never reads `fed_today`, so on a non-payout night a feed buys only the animal's survival, which one
feed in two also buys.

`FEED_CADENCE_FROM_DAY = 7` is where that starts, and its docstring says why: *"The tape feeds
everything, every day, until d5 ... the cycling starts at d5 (4 of 7) and is unmistakable by d7
(3 of 17)."* That is **Seb's** tape. Seventeen pens on d7 is nobody's herd here -- Victor has ten.

Victor does not cycle. His feed row against his own herd:

    d0  5/5    d3  5/5    d6   7/7     d9  12/12
    d1  0/0    d4  5/5    d7  10/10    d10 12/12
    d2  5/5    d5  6/6    d8  12/12    d11 12/12

Every animal, every day, from d0 to the end of the window -- d1 is a two-unit day with 47 unit-turns
and feeds nothing on either side. Ours tracks him exactly to d6 and then breaks at d7, which is the
constant, not a coincidence: `feed 8/10` on d7 and `7/12`, `9/12`, `8/12`, `9/12` after it. The dawn
plan generates the shortfall itself -- d7 plans `FEED 8, CARE 8` and reports `uncovered: []`, with
`(0,4)` and `(5,4)` given COLLECT_FERTILIZER and no FEED.

CARE follows FEED and inherits the whole loss, because `kaggriculture.py:816` banks the bonus only
on a night that is both fed and cared, and `animal_ops` offers CARE only on a pen it is feeding. So
`care` mirrors `feed` cell for cell in the grid, and both rows are one defect.

The assertion is that a pen alive at dawn is fed, from `FEED_CADENCE_FROM_DAY` on. It says nothing
about pens placed later in the day -- those are the placement's business -- and nothing about d1,
which is below the cadence day anyway.
"""
import collections
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

SEED = 11
DAYS = 12
TPD = 24


@pytest.fixture(scope="module")
def played():
    """`{day: (feeds_emitted, pens_alive_at_dawn)}` for our seat."""
    import breakdown as B
    from kaggle_environments import make
    import kagg.search.schedule_agent_1455mh as sa

    replay, schedule, team = B.TAPES["victor"]
    sched = {int(k): v for k, v in json.loads((REPO / schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    cfg = dict(B.env_config(REPO / replay), seed=SEED, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    feeds = collections.Counter()
    dawn_pens = {}
    for t in range(TPD * DAYS):
        day = t // TPD
        o0, o1 = env.state[0].observation, env.state[1].observation
        farm = o0["farms"][0]
        if t % TPD == 0:
            dawn_pens[day] = sum(1 for r in farm["tiles"] for c in r
                                 if isinstance(c, dict) and "animal" in c)
        a0, a1 = agent(o0), tape(o1, t)
        n0 = len(farm.get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if a and a[0] == "FEED":
                feeds[day] += 1
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return {d: (feeds[d], dawn_pens[d]) for d in dawn_pens}


def test_the_premise_the_cadence_day_is_inside_the_window(played):
    """Guard. If the cadence never switches on in range, nothing below is testing it."""
    from kagg.search import router as R

    assert R.FEED_CADENCE_FROM_DAY < DAYS, (
        f"FEED_CADENCE_FROM_DAY={R.FEED_CADENCE_FROM_DAY} is outside d0-d{DAYS - 1}; "
        "this file asserts what happens once it applies")


@pytest.mark.parametrize("day", range(DAYS))
def test_every_pen_alive_at_dawn_is_fed(played, day):
    from kagg.search import router as R

    if day < R.FEED_CADENCE_FROM_DAY:
        pytest.skip(f"d{day} is below the cadence day")
    fed, pens = played[day]
    if not pens:
        pytest.skip(f"d{day} owns no animals at dawn")
    assert fed >= pens, (
        f"d{day} woke with {pens} animals and emitted {fed} FEEDs. The tape feeds its whole herd "
        "every day; the cadence that withholds one was measured on Seb's, whose d7 has 17 pens.")
