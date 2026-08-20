"""A hand that has run out of work walks its load to the shed. It never stands still holding it.

**What the tape does.** Day 4 of 91422988, hours 15-23, is Seb's whole crew turning round and
marching home:

    h17  u7@(4,4){WHEAT 11}        h18 DROP     SELL WHEAT 5
    h20  u2,u3,u6 @(4,4)           h21 DROP     SELL WHEAT 12, FERTILIZER 5, BUY_LAND
    h21  u5@(4,4){WHEAT 12}        h22 DROP     SELL WHEAT 12
    h22  u0,u1@(4,4){WHEAT 12/8}   h23 DROP     SELL WHEAT 20, FERTILIZER 1

49 wheat and 6 fertilizer, which is the schedule row for the day to the unit. u0 spends eight
consecutive turns, h15 to h22, walking (0,0) -> (4,4) carrying twelve wheat and doing nothing else.
The return leg is not something his day finds room for; it is most of the back half of it. His shed
holds 7 -- his pen count -- from h18 to dusk, and he buys ONE wheat all day.

**What we do on the same hours.** u1 and u5 stand still at (1,1) and (2,0) from h19 to h23 holding
eight wheat each, while the market orders buy 6 wheat at h18, 6 at h21 and 6 at h23 against a shed
the goods never reached. d4 closed `shed 1, pens 7, carried 28` where the tape closed `shed 7,
carried 0`.

**Why the planned stop does not cover this.** `cover.plan` appends the closing shed trip only when
it fits in the turns the tour did not spend, and the dawn plan for d4 declines it on five of six
units:

    u0 cost=23/24 closes_at_shed=False    ends (1,2)
    u1 cost=18/23 closes_at_shed=False    ends (1,1)   5 turns unspent, trip costs 7
    u2 cost=22/23 closes_at_shed=False    ends (0,2)
    u3 cost=23/23 closes_at_shed=False    ends (4,0)
    u4 cost=18/23 closes_at_shed=False    ends (2,0)   5 turns unspent, trip costs 7
    u5 cost=21/23 closes_at_shed=True

That is correct as a *plan* -- the trip is genuinely not worth a job, and `_drop_inventories_to_shed`
(`kaggriculture.py:812`) empties every hand at the rollover anyway, so the goods are not lost. They
are merely late, and late is the whole difference: the market reads the shed, so wheat that arrives
at the rollover is wheat the day could not sell and wheat the day then buys a second copy of.

So this is deliberately NOT a planning change and costs no job. It spends turns the unit is already
passing on. `WALK_THE_LOAD_HOME` is the executor's answer to the one question the plan does not
ask: the tour is over, the hand is full, and there are hours left.

`PASS`, `DROP` and `PICKUP` are tour shape and are exempt from the tape match, so a turn moving from
PASS to a walk cannot regress a matched day by construction. What it can change is money, which is
the point.
"""
import importlib
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/91422988.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
SEED = 11
DAYS = 7
MODULE = "kagg.search.schedule_agent"


def _thin():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): {k2: v2 for k2, v2 in r.items() if k2 not in TAPE_ONLY}
            for k, r in raw.items()}


def _opponent():
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    return [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]


def test_no_hand_stands_still_holding_a_load():
    """The rule itself. A carried item and a PASS in the same turn is the defect, wherever it is.

    Stated per TURN and not as a dusk total, because the dusk total is the symptom: by h23 the
    stranding has already cost the day its sells. Red at 40 turns when this was written, all of them
    d3-d6 evenings.
    """
    from kaggle_environments import make

    SA = importlib.import_module(MODULE)
    opp = _opponent()

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(_thin(), 0, router=True)

    stalled = []
    for t in range(24 * DAYS):
        o0 = env.state[0].observation
        a0, a1 = agent(o0), opp[t]
        farm, priv = o0["farms"][0], o0["private"]
        invs = priv.get("inventories") or []
        pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
        acts = [a0["farmer"], *a0["hands"]]
        for u, p in enumerate(pos):
            ac = acts[u] if u < len(acts) else None
            if not ac or ac[0] != "PASS":
                continue
            load = {i: q for i, q in ((invs[u] or {}) if u < len(invs) else {}).items() if q > 0}
            if load:
                stalled.append(f"    d{t // 24} h{t % 24}  u{u}@{p} holding {load}")
        n0 = len(farm.get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert not stalled, (
        f"{len(stalled)} turns spent standing still with a full hand:\n" + "\n".join(stalled)
        + "\n  The tape walks these home. The market reads the shed, so produce that arrives at the "
          "rollover is produce the day could not sell -- and then bought a second copy of."
    )


def test_day_four_closes_with_its_wheat_in_the_shed_not_in_hands():
    """The day the defect was traced on, stated as the tape states it: `shed 7, carried 0`.

    Kept separate from the rule above because it can fail for a second reason -- the crew walks home
    and arrives too late -- and a single test would report that as the same defect.
    """
    from kaggle_environments import make

    SA = importlib.import_module(MODULE)
    opp = _opponent()

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(_thin(), 0, router=True)

    carried = shed = None
    for t in range(24 * 5):
        o0 = env.state[0].observation
        a0, a1 = agent(o0), opp[t]
        farm, priv = o0["farms"][0], o0["private"]
        if t == 24 * 4 + 23:
            carried = sum(sum(q for q in (iv or {}).values())
                          for iv in (priv.get("inventories") or []))
            shed = int((priv.get("shed") or {}).get("WHEAT", 0))
        n0 = len(farm.get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert carried <= 4, (
        f"d4 closed with {carried} items still in hands and {shed} WHEAT in the shed. The tape "
        "closed the same day carrying nothing, with 7 in the shed -- its pen count -- having sold "
        "49 wheat and 6 fertilizer. It was 28 carried against 1 in the shed when this was written."
    )
