"""An animal that goes two days unfed escapes. Ours lose three; the tape loses none.

`reference/kaggriculture.py:786` removes the animal and leaves the structure once
`consecutive_unfed` reaches 2. That is a correctness floor, not a metric: a herd that starves is
wrong however good the money looks, and this repo has a standing rule that floors are never traded
away.

Measured on Seb's tape, seed 11, weeds off, before any fix:

    (8, 0) escapes at the day-16 rollover
    (6, 5) escapes at the day-17 rollover
    (9, 0) escapes at the day-18 rollover

and in each case the pen was left unfed on the PREVIOUS day too. The tape leaves one to three pens
unfed on most days as well -- it simply never leaves the SAME pen unfed twice running.

Three explanations were tested and killed before this test was written, so do not re-derive them:

  * not the prize -- `router.animal_ops` already adds `cost + _animal_remaining` on top of MANDATORY
    once `consecutive_unfed >= 1`, so an at-risk pen is already the dearest FEED on the board;
  * not the stock -- at day 16 hour 20 we hold ten wheat (7 shed + 3 carried) with a pen at risk;
  * not the `have_wheat` guard -- our wheat never reaches zero across days 15 to 18.

What remains is assignment: at day 16 hour 20 a FEED *is* emitted and it goes to a pen that is not
the one about to lose its animal.
"""
import json
import pathlib

import pytest

from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy, DEFAULT_TAPE

pytestmark = pytest.mark.slow


def _escapes(days=20, seed=11):
    """Every (day, tile) where an animal vanished from a pen that survives, i.e. starved out."""
    from kaggle_environments import make

    replay, schedule, team = TAPES[DEFAULT_TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    def penned(obs):
        return {(x, y): c["animal"]
                for y, row in enumerate(obs["farms"][0]["tiles"])
                for x, c in enumerate(row)
                if isinstance(c, dict) and c.get("animal")}

    lost, prev = [], penned(env.state[0].observation)
    for t in range(24 * days - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
        now = penned(env.state[0].observation)
        # An animal only ever leaves a pen through the unfed rule -- there is no SELL_ANIMAL and no
        # op that removes one -- so a tile that held an animal and no longer does is an escape.
        for tile in sorted(set(prev) - set(now)):
            lost.append((t // 24, tile))
        prev = now
    return lost


def test_no_animal_ever_starves_out_of_its_pen():
    """The floor. Three sheep escape on days 16, 17 and 18; the tape loses none."""
    lost = _escapes()
    assert lost == [], (
        f"{len(lost)} animal(s) starved out of their pens: {lost}. "
        "An animal is only removed by `consecutive_unfed >= 2`, so each of these is a pen that was "
        "left unfed two days running while the tape never leaves the same pen unfed twice."
    )
