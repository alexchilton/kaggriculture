"""The dawn plan routes each hand from a predicted spawn tile. The hand must actually be there.

`_end_of_day` discharges the whole crew -- `farm["hands"] = []` (`kaggriculture.py:867`) -- so every
hand is a fresh `_spawn_hand` every morning and the plan can only *predict* where they land.
`_arrivals` is that prediction: least-occupied shed-access tile, ties in NWSE ring order
`[(4,4), (5,4), (4,5), (5,5)]`, counting `[farmer] + hands` **at the moment the HIRE settles**.

The hires settle in the MARKET phase, which runs AFTER the unit phase (`kaggriculture.py:922` then
`:928`). So the ring the hires see is the ring as it stands *after* the farmer has taken its hour-0
action. `_clear_the_spawn_ring` knows this and handles the case where the farmer is stepped off
DELIBERATELY -- but it only does that when the step saves a hand from the dead `(5,5)` corner, and
once the whole board is unlocked nothing is dead, so it returns `step_off=None` and predicts the ring
with the farmer still on `(4,4)`.

The farmer's own routed tour then walks it off `(4,4)` anyway, `(4,4)` reads empty when hire 1
settles, and **every hand lands one slot early**:

    day 11, seed 11, 11 units
      predicted  (5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5)
      actual     (4,4) (5,4) (4,5) (5,5) (4,4) (5,4) (4,5) (5,5) (4,4) (5,4)

Every tour is then priced from the wrong tile. It cost a strawberry: u10's tour was priced at exactly
23 turns against a budget of 23 and ended `WATER (1,2)`; starting two turns away it finished at (3,2),
two tiles short, and `(1,2)` weeded that night at `consecutive_unwatered >= 2` (`:770`) -- worth
`strawb 35/36` for the rest of the season plus a `dig` on d13.

Day 9 is the control: 8 units, the farmer stays home, and all eight predictions are exact.

**The obvious fix was tried and is a LOSS.** Pinning the farmer on a hire turn (`hold_farmer`, which
already exists for the deliberate spawn-ring step) makes the prediction true by force, and the force
is a turn of the 24-turn unit on nearly every hire day. On the 17-day grid, seed 11:

    money@d16   17,459/15,759 -> 16,044/15,759
    strawb      35/36 -> 33/36
    weeds       2 -> 4          `(1,2)` lived; `(0,2)`, `(1,4)` and `(2,1)` died instead

d11 went fully green and d10 from 14 wrong to 7 -- the residual is a SECOND cause, hands that arrive
in a later wave at h2, by which time the h0 wave has walked off the ring and the h0-computed
prediction is stale for them.

So this is left XFAIL: the defect is real and proven, the price of forcing it is known, and the
untried direction is to fix the PREDICTION rather than reality -- re-plan once after the farmer's
hour-0 move is known, which costs a solve and no game turn.
"""

import importlib
import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

DAYS = 12
SEED = 11
TPD = 24


@pytest.fixture(scope="module")
def sightings():
    """`{day: [(unit, predicted, actual_or_None), ...]}` for every unit of every day up to `DAYS`."""
    import breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    DP = SA.DP

    real_plan = DP.plan
    assumed = []

    def spy(units, jobs, budget, *a, **kw):
        assumed.append([tuple(u) for u in units])
        return real_plan(units, jobs, budget, *a, **kw)

    DP.plan = spy
    try:
        replay, schedule, team = B.TAPES["victor"]
        sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
        thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

        env = make("kaggriculture",
                   configuration=dict(B.env_config(replay) or {}, seed=SEED, weedSpawnChance=0.0),
                   debug=True)
        env.reset(2)
        me = SA.make_agent(thin, 0, router=True)
        them = B.tape_policy(replay, team, 1)

        out, first = {}, {}
        for t in range(TPD * DAYS):
            day = t // TPD
            if t % TPD == 0:
                assumed.clear()
                first = {}
            obs = env.state[0].observation
            farm = obs["farms"][0]
            here = [tuple(farm.get("farmer") or (4, 4))]
            for h in (farm.get("hands") or []):
                here.append(tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4))))
            a0 = me(obs, t)
            for u, p in enumerate(here):
                first.setdefault(u, p)
            env.step([a0, them(env.state[1].observation, t)])
            if t % TPD == TPD - 1 and assumed:
                out[day] = [(u, s, first.get(u)) for u, s in enumerate(assumed[0])]
        return out
    finally:
        DP.plan = real_plan


def _wrong(rows):
    return [(u, s, a) for u, s, a in rows if a is not None and a != s]


def test_day_nine_is_the_control_and_every_prediction_is_exact(sightings):
    """Eight units, farmer parked: the predictor is right, so the mechanism below is not a harness bug."""
    rows = sightings[9]
    assert not _wrong(rows), "\n".join(
        f"u{u}: routed from {s}, woke on {a}" for u, s, a in _wrong(rows))


@pytest.mark.xfail(reason="open defect; the forcing fix is a measured loss -- see banner", strict=False)
def test_a_hand_starts_the_day_on_the_tile_it_was_routed_from(sightings):
    """Every hand, every day. A hand routed from the wrong tile has every op after it mispriced."""
    bad = {d: _wrong(rows) for d, rows in sightings.items() if _wrong(rows)}
    assert not bad, "hands routed from a tile they did not wake on:\n" + "\n".join(
        f"  day {d}: " + ", ".join(f"u{u} routed {s} woke {a}" for u, s, a in rows)
        for d, rows in sorted(bad.items()))
