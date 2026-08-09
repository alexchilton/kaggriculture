"""The wheat feed reserve garrisons the shed and lets the harvest die around it.

## The theory under test

`feed_days(day)` returns 4 from day 16, and that one number does two jobs:

* it sizes the BUY (`schedule_agent.py:3017`, `herd = feed_days(day) * alive - fed_today - on_hand`)
* it sizes the SELL guard (`schedule_agent.py:2478`, `have -= feed_days(day) * alive - ...`)

Late season the herd is 14-19 animals, so the reserve is 56-76 units against a `shedCapacity` of
**100 slots shared by all nine products**. The shed never carries that much, which is worse rather
than better: `have` for WHEAT is pinned at 0, so from day 16 we can never sell a single unit of
wheat, and the pile is a one-way ratchet.

`release_order` cannot reach it. The eviction picks wheat first -- it is the cheapest product at $25
-- and is then capped by the same `have`, so the one pile that is causing the crowding is the one
pile the eviction is forbidden to touch.

Measured on two real ladder losses (`data/ladder/losses/`, 2026-08-09), every night that discarded
product:

    day  shedWHEAT  shedTOT  hands  lost
     16     55         61      52     13     <- FEED_DAYS_FROM_DAY = 16, exactly
     17     55         55      72     29
     21     52         52     105     57
     28     52         73      42     15

263 units destroyed in that game against the opponent's 23, and the expensive half of the shed:
STRAWBERRY 72, MILK 69, FERTILIZER 66, WOOL 27. Wheat survived because wheat was in the SHED, and
the shed is what survives the rollover -- hands are what dies.

## What this asserts

The mechanism, not the season total: on a night the shed throws product away, wheat must not be
sitting on more than `SLOT_BUDGET` of the hundred slots. `test_the_shed_does_not_destroy_the_harvest`
already owns the outcome.

The budget is set at 40 because it discriminates: the reserve holds 52-60 today, and one day of feed
for the largest herd this agent runs (19) is 19. It is not a restatement of either arm.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

SEED, DAYS, HANDOVER, CAP = 11, 30, 11, 100

#: Slots of the hundred that the feed reserve may occupy on a night the shed is discarding product.
#: Between the arms: the reserve holds 52-60 now, and one day of feed for a 19-head herd is 19.
SLOT_BUDGET = 40


@pytest.fixture(scope="module")
def nights():
    """Replay Seb d0..d10, hand over at d11, and record the shed on every night that loses product."""
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

    out, dusk = [], None
    for t in range(24 * DAYS - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        priv = o0.get("private") or {}
        shed = collections.Counter(priv.get("shed") or {})
        day, hour = t // 24, t % 24

        if hour == 0 and dusk is not None:
            lost = dusk["held"] - sum(shed.values())
            if lost > 0:
                out.append(dict(day=dusk["day"], wheat=dusk["wheat"], shed=dusk["shed"],
                                hands=dusk["hands"], alive=dusk["alive"], lost=lost))
            dusk = None

        a1 = opp(o1, t)
        if day < HANDOVER:
            a0 = dict(tape_act[t]) if t < len(tape_act) else {"farmer": ["PASS"], "hands": [],
                                                              "market": []}
            ours(o0)                     # keep our agent's per-day state warm for the handover
        else:
            a0 = ours(o0)

        if hour == 23:
            hands = sum(sum(collections.Counter(iv).values())
                        for iv in (priv.get("inventories") or []))
            dusk = dict(day=day, wheat=int(shed.get("WHEAT", 0)), shed=sum(shed.values()),
                        hands=hands, held=sum(shed.values()) + hands,
                        alive=sum(1 for r in o0["farms"][0]["tiles"] for c in r
                                  if isinstance(c, dict) and "animal" in c))

        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return out


def _table(rows):
    head = "    day  shedWHEAT  shedTOT  hands  alive  lost"
    body = ["    %3d  %9d  %7d  %5d  %5d  %4d"
            % (r["day"], r["wheat"], r["shed"], r["hands"], r["alive"], r["lost"]) for r in rows]
    return "\n".join([head] + body)


@pytest.mark.slow
def test_a_night_that_bins_product_is_not_a_night_the_shed_was_full_of_feed(nights):
    """The defect. Wheat may not hold 40+ of the hundred slots while product is being destroyed."""
    assert nights, "no night discarded anything -- the fixture no longer reproduces the defect"
    over = [r for r in nights if r["wheat"] > SLOT_BUDGET]
    assert not over, (
        f"{len(over)} of {len(nights)} discarding nights had more than {SLOT_BUDGET} of the "
        f"{CAP} shed slots held as wheat feed, while "
        f"{sum(r['lost'] for r in over)} units of product were destroyed:\n"
        + _table(over)
        + f"\n    `feed_days(day)` is {SA.FEED_DAYS_LATE} from day {SA.FEED_DAYS_FROM_DAY}, so the "
          "reserve is 4 x herd and `have` for WHEAT is pinned at 0. `release_order` picks wheat "
          "first and is then capped by that same `have`, so the eviction cannot touch the one pile "
          "that is causing the crowding.")


@pytest.mark.slow
def test_the_feed_reserve_is_not_simply_switched_off(nights):
    """The guard on the fix. A herd that starves is worse than a shed that spills.

    `FEED_DAYS_LATE` went 2 -> 4 on 2026-08-08 because escapes went 4 -> 0 over six seasons, and an
    escape is irreversible. Whatever frees the slots must still leave a day of feed standing.

    **Scoped to day >= `FEED_DAYS_FROM_DAY`, and not out of convenience.** Run against the unfixed
    agent this failed on days 12 and 14 -- wheat 14 against a herd of 17 and 20 -- which is the early
    `FEED_DAYS = 2` phase, is nothing to do with the eviction, and left the guard red for a reason
    the fix does not cause and cannot remove. A guard that is already red guards nothing. Those two
    nights are also evidence in their own right: the shed ALREADY runs under a day of feed before
    day 16 and the herd grew 17 -> 20 through it, so `FEED_DAYS_FLOOR = 1` is not a novel risk.
    """
    late = [r for r in nights if r["day"] >= SA.FEED_DAYS_FROM_DAY]
    starved = [r for r in late if r["alive"] and r["wheat"] < r["alive"]]
    assert not starved, (
        "the shed ended a night holding less than one day of feed for the herd, which is how "
        f"`consecutive_unfed >= 2` evicts an animal:\n" + _table(starved))
