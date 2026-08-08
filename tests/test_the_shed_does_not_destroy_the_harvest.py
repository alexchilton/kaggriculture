"""Product that will not fit in the shed at midnight is deleted, and we delete a lot of it.

## The fixture

Seb's own actions are replayed for days 0..10, which reproduces his board EXACTLY -- `owned`,
`plant`, `pen` and `animal` match him day for day, and all three land parcels land on his days
(4, 6, 10). Our agent then takes over at day 11 from a board it did not build.

That isolates the question. There is no early-game deficit left to blame: at the handover we hold
$3,950 against his $3,864 and the same 100 tiles. Everything measured after it is our selling.

## The defect

`_drop_inventories_to_shed` (`kaggriculture.py:813`) banks every hand into the shed at the rollover
up to `shedCapacity` 100 and **discards the overflow**. A HARVEST into a full shed loses the
difference too (`kaggriculture.py:470`). Measured on the fixture:

    day    11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28
    shed   14  33  35  35  45  86 100 100 100 100 100 100 100 100 100 100  90 100
    lost    0   1   2   1   0  21  13  27  23  18  42  36  28  11  41   7  10  24

**331 units destroyed over the season**, and from day 17 the shed never comes off its cap. Seb sits
between 18 and 36 all season because he never stops selling.

## The cause, and why it is not a capacity problem

`schedule_agent.py:2088`:

    allow = max(today + carry, have - still_owed[prod])
    n     = min(have, allow, rate[prod])

Both caps are transcribed from HIS schedule and neither can see our shed. `still_owed` is everything
the remaining season's rows will ever ask for, so `have - still_owed` stays negative until roughly
day 25 and `allow` collapses to today's row. Meanwhile we plant 77 tiles to his 45, so the surplus we
produce has no row anywhere in the schedule to release it.

`SELL_TO_MAKE_ROOM` is already on and does not fix it -- it reserves room for tonight's drop, which
is a different and smaller question than "this product has no buyer in the plan".

## What this asserts

An outcome, not a mechanism: a season must not destroy a large fraction of what it grows. The
threshold is set between the two measured arms (331 with `PRICE_AWARE_SELL_CAP` off, 82 with it on),
so it discriminates them and is not a restatement of either number.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

SEED, DAYS, HANDOVER, CAP = 11, 30, 11, 100

#: Between the two measured arms. Off destroys 331, on destroys 82.
MAX_DESTROYED = 150


@pytest.fixture(scope="module")
def season():
    """Replay Seb d0..d10, hand over at d11, and count what the shed throws away."""
    from kaggle_environments import make

    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    replay, schedule, team = TAPES["seb1326"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    raw = json.loads(pathlib.Path(replay).read_text())
    tseat = raw["info"]["TeamNames"].index(team)
    tape_act = [dict(farmer=((s[tseat] or {}).get("action") or {}).get("farmer") or ["PASS"],
                     hands=list(((s[tseat] or {}).get("action") or {}).get("hands") or []),
                     market=list(((s[tseat] or {}).get("action") or {}).get("market") or []))
                for s in raw["steps"][1:]]

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    out = {"destroyed": 0, "at_cap": 0, "shed": {}, "owned": {}, "dusk": None}
    for t in range(24 * DAYS - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        priv = o0.get("private") or {}
        total = sum(collections.Counter(priv.get("shed") or {}).values())
        day, hour = t // 24, t % 24

        if hour == 0:
            if out["dusk"] is not None and out["dusk"] - total > 0:
                out["destroyed"] += out["dusk"] - total
            out["shed"][day] = total
            out["owned"][day] = sum(1 for r in o0["farms"][0]["tiles"] for c in r if c != "LOCKED")
        if total >= CAP:
            out["at_cap"] += 1

        a1 = opp(o1, t)
        if day < HANDOVER:
            a0 = dict(tape_act[t]) if t < len(tape_act) else {"farmer": ["PASS"], "hands": [],
                                                              "market": []}
            ours(o0)                     # keep our agent's per-day state warm for the handover
        else:
            a0 = ours(o0)

        out["dusk"] = total + sum(sum(collections.Counter(iv).values())
                                  for iv in (priv.get("inventories") or []))
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return out


@pytest.mark.slow
def test_the_replay_really_does_reproduce_his_board(season):
    """The premise. If the splice stops matching him, everything after it measures something else."""
    got = [season["owned"][d] for d in (4, 5, 6, 7, 10, 11)]
    assert got == [25, 50, 50, 75, 75, 100], (
        "replaying his days 0-10 no longer reproduces his land ladder "
        f"(parcels on days 4, 6 and 10): owned at d4,5,6,7,10,11 = {got}")


@pytest.mark.slow
def test_the_season_does_not_destroy_its_own_harvest(season):
    """The whole thing. A unit deleted at midnight was grown, watered, walked home -- and binned."""
    assert season["destroyed"] <= MAX_DESTROYED, (
        f"{season['destroyed']} units were discarded at the midnight rollover, and the shed sat at "
        f"capacity for {season['at_cap']} turns.\n    "
        + "  ".join(f"d{d}:{season['shed'][d]}" for d in sorted(season["shed"]) if d >= HANDOVER)
        + "\n    `allow` and `rate` are both transcribed from HIS schedule and neither can see our "
          "shed; we plant 77 tiles to his 45, so the surplus has no row to release it.")
