"""A PLANT on the last turn of a day is a WEED by dawn. It must not be emitted.

The reference makes this unconditional, in three lines that are far apart:

    `:222`  a new plant starts at  "consecutive_unwatered": 1   -- the planting day counts as dry
    `:781`  the dusk rollover does  consecutive_unwatered += 1   -- taking it to 2
    `:783`  and at >= 2             farm["tiles"][y][x] = {"kind": "WEED"}

WATER is a separate turn from PLANT, so a plant emitted at `turns_per_day - 1` cannot be watered by
anyone, on any route, ever. It is not a risk or a trade-off: the tile is a weed by dawn with
certainty, the seed is spent, and the ground is then blocked for the rest of the season because
PLANT needs EMPTY and WATER needs `kind == "PLANT"`.

Measured on seed 11, melon arm, d6: `u4 PLANT/MELON` at h23 standing on (8,4), tile empty, 8 melon
seeds in store, NE unlocked -- every gate in `reference:417` passes, the plant lands, and the day
ends `crop_MELON 12` with `weed 2` against the tape's `14` and `1`. One action, two wrong cells.

`routines.py` already states the rule for the tape builder -- "WATER on the planting day, not from
the next one" -- and emits `["PLANT", "WATER"]` as one job. What is missing is the turn budget: the
pair needs two turns and the last turn of the day has one.
"""
import importlib
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
REPLAY = "data/seed_scripts/kawashigi/92498144.json"
TEAM = "カワシギ"


def plants_by_hour(day, seed=11, weeds=0.005):
    """`[(hour, unit, crop)]` -- every PLANT seat 0 submits on `day`."""
    from kaggle_environments import make

    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / REPLAY)
    env = make("kaggriculture", configuration=dict(B.env_config(replay), seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, 0)
    opp = B.tape_policy(replay, TEAM, 1)
    out = []
    for t in range((day + 1) * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = agent(o0), opp(o1, t)
        d, h = divmod(t, TPD)
        if d == day:
            n0 = len(o0["farms"][0].get("hands") or [])
            for u, a in enumerate([a0["farmer"]] + list(a0["hands"] or [])[:n0]):
                if a and a[0] == "PLANT":
                    out.append((h, u, a[1] if len(a) > 1 else None))
        env.step([a0, a1])
        if env.done:
            break
    return out


def test_the_premise_a_fresh_plant_starts_one_night_from_weeding():
    """Read straight out of the reference, so the rule cannot drift under us."""
    src = (REPO / "reference/kaggriculture.py").read_text()
    assert '"consecutive_unwatered": 1,  # planting day counts as unwatered' in src
    assert 'if tile["consecutive_unwatered"] >= 2:' in src


@pytest.mark.parametrize("day", [6])
def test_no_plant_is_emitted_on_the_last_turn_of_the_day(day):
    late = [p for p in plants_by_hour(day) if p[0] == TPD - 1]
    assert late == [], (
        f"day {day}: PLANT emitted at h{TPD - 1} {late}. There is no turn left to water it, so "
        f"`_daily_refresh_plants` weeds the tile at the rollover -- the seed is spent, the melon "
        f"never exists, and the ground is blocked for the season.")
