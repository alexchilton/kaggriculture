"""Day 7 buys a sheep, reserves every pen for a cow, and leaves the sheep in the shed all day.

`_refresh_pins` labels a pen with the animal it was sited for and lets that label outlive the pin
(`pen_for`, "Outlive the pin"). The label is read off the schedule by INDEX::

    wanted = [a for d in sorted(sched) if d <= day for a in (sched[d].get("places") or [])]
    have   = structures + pending BUILD pins
    a      = wanted[have] if have < len(wanted) else "COW"

`have` counts PENS and `wanted` lists PLACEMENTS, and the schedule does not align the two day by
day -- d6 builds two pens and places nothing, d7 places three animals and builds two pens. Through
d7 it wants 10 pens and 9 placements, so the index runs off the end of the list and the loop takes
the hardcoded `"COW"` default.

Measured on the kawashigi board, seed 11, at d7 dawn:

    schedule row      places = ['SHEEP', 'COW', 'COW'],  animals_bought = {'COW': 2, 'SHEEP': 1}
    shed              COW 2, SHEEP 1          -- all three BUY_ANIMALs fill, `buy_animal 3/3`
    empty pens        (5,4) (6,4) standing, (6,3) (5,2) pinned to build   -- four slots for three
    pen_for           {(5,4): COW, (6,4): COW, (6,3): COW, (5,2): COW}
    nodes built       four PLACE COW, not one PLACE SHEEP anywhere
    crew.cover        supply COW 2 -> keeps (5,4) (6,4), drops (6,3) (5,2)

So two cows are placed, the sheep is never picked up by anybody, and it sits in the shed until
dusk: `place 2/3`, `animals 8/9`, and then `feed 6/9` because an animal in the shed cannot be fed.

The outstanding placements at that moment are exactly what the shed holds -- cumulative places
SHEEP 3 / COW 6, minus the SHEEP 2 / COW 4 already standing, is SHEEP 1 / COW 2. The information
needed to label the pens correctly is on the board; the index arithmetic throws it away.

The assertion is that the animals the day BUYS are the animals its pens are RESERVED for, which is
the mechanism. It is deliberately not an assertion about which tile gets which species -- the
siting is a separate question and the tape's own geometry differs from ours.
"""
import collections
import importlib

import pytest

import kagg.plan as _PLAN

SEED = 11
DAY = 7


@pytest.fixture(scope="module")
def day_seven():
    """Our seat's d7: animals bought (FILLS), animals placed, and the herd standing at dusk."""
    import scripts.breakdown as B
    from kagg.analysis.fills import record_fills
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)
    shops = B.recorded_shops(replay)

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2)
    ours = SA.make_agent(sched, 0, router=True)
    opp = B.tape_policy(replay, team, 1)

    placed = collections.Counter()
    pens_at_dawn = []
    bought_before = None
    with record_fills(env) as fills:
        for t in range((DAY + 1) * 24):
            o0, o1 = env.state[0].observation, env.state[1].observation
            o0.town["unlocked_shops"] = list(shops(t))
            if t == DAY * 24:
                bought_before = {a: fills.units(0, "BUY_ANIMAL", a) for a in ("COW", "SHEEP")}
                for y, row in enumerate(o0["farms"][0]["tiles"]):
                    for x, c in enumerate(row):
                        if isinstance(c, dict) and c.get("kind") in ("PASTURE", "COOP"):
                            pens_at_dawn.append(((x, y), c.get("animal")))
            a0, a1 = ours(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            if t // 24 == DAY:
                for act in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
                    if act and act[0] == "PLACE" and len(act) > 1:
                        placed[act[1]] += 1
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])

    bought_after = {a: fills.units(0, "BUY_ANIMAL", a) for a in ("COW", "SHEEP")}
    today = collections.Counter({a: bought_after[a] - bought_before[a] for a in bought_after})
    herd = collections.Counter()
    for row in env.state[0].observation["farms"][0]["tiles"]:
        for c in row:
            if isinstance(c, dict) and c.get("animal"):
                herd[c["animal"]] += 1
    return today, placed, herd, pens_at_dawn


def test_the_premise_the_day_buys_the_sheep_it_is_asked_to(day_seven):
    """Guard. If the SHEEP never fills, the placement cannot happen and the defect is in the market,
    not in the pen labelling."""
    today, _placed, _herd, _pens = day_seven
    row = _PLAN.load("data/seed_scripts/kawashigi/schedule.json").get(DAY) or {}
    want = collections.Counter(row.get("animals_bought") or {})
    assert dict(today) == dict(want), (
        f"d{DAY} was asked to buy {dict(want)} and filled {dict(today)} -- the shortage is in the "
        "market, so a pen-labelling assertion would be testing the wrong thing")


def test_the_premise_there_are_more_empty_pens_than_animals_to_put_in_them(day_seven):
    """Guard. With fewer pens than animals the sheep is homeless whatever the labels say."""
    _today, _placed, _herd, pens = day_seven
    row = _PLAN.load("data/seed_scripts/kawashigi/schedule.json").get(DAY) or {}
    empty = [t for t, a in pens if not a]
    slots = len(empty) + int(row.get("builds", 0) or 0)
    need = len(row.get("places") or [])
    assert slots >= need, (
        f"d{DAY} has {len(empty)} empty pens plus {row.get('builds')} to build = {slots} slots for "
        f"{need} placements -- there is no room, so the labels are not what is short")


def test_every_animal_the_day_buys_is_standing_in_a_pen_by_dusk(day_seven):
    today, placed, _herd, pens = day_seven
    missing = {a: n - placed.get(a, 0) for a, n in today.items() if n - placed.get(a, 0) > 0}
    assert not missing, (
        f"d{DAY} bought {dict(today)} and placed {dict(placed)}, leaving {missing} in the shed. "
        f"The empty pens at dawn were {[t for t, a in pens if not a]}. `_refresh_pins` labels a pen "
        "by `wanted[have]`, indexing the cumulative PLACES list by the PEN count -- two quantities "
        "the schedule does not align -- so the index runs off the end and every pen takes the "
        "hardcoded \"COW\" default. Four pens then bid for two cows, the stock cull drops the "
        "surplus, and nothing in the day ever asks for the sheep.")


def test_the_herd_standing_at_dusk_is_everything_that_was_ever_bought(day_seven):
    """The stronger statement of the same thing: an animal bought and never placed is money spent
    on nothing, and it starts no `consecutive_unfed` clock only because it is not on the board."""
    from kagg.analysis.fills import record_fills  # noqa: F401  (documents where `today` comes from)
    _today, _placed, herd, _pens = day_seven
    sched = _PLAN.load("data/seed_scripts/kawashigi/schedule.json")
    want = collections.Counter()
    for d in sorted(sched):
        if int(d) <= DAY:
            want.update(sched[d].get("places") or [])
    assert herd["SHEEP"] >= want["SHEEP"], (
        f"through d{DAY} the schedule places {dict(want)} and the board holds {dict(herd)} -- the "
        "sheep the schedule asked for are not standing in pens")
