"""Day 0 has two FEEDs for four animals, and it spends both on the two that cap anyway.

An animal's yield on its production day is `min(max_held, 1 + pending_care_bonus)`
(`kaggriculture.py:814`), and the bonus is one per day the pen was **fed and cared** together,
banked at each rollover and consumed by the production day. So a FEED is worth a unit of product
only while the animal's remaining bonus days are FEWER than its cap. Count them for an animal
placed on day 0:

    SHEEP   first yield d6, cap 6   ->  d0..d4 bank the bonus: FIVE days for a cap of six.
                                        Every one is load-bearing. Miss d0 and the yield is 1+4 = 5.
    COW     first yield d8, cap 6   ->  d0..d7 bank the bonus: EIGHT days for the same six.
                                        It needs five of them and the schedule feeds it on
                                        d1-d6 (4/4, 4/4, 4/4, 5/5, 6/6, 6/6). The d0 feed is spare.

Measured on the kawashigi board, seed 11. Both sides place four animals on d0 and both manage
exactly `FEED 2 / CARE 2` -- the counts are identical, the species are opposite:

    ours    h07 PLACE/COW    h08 FEED  h09 CARE
            h12 PLACE/COW    h13 FEED  h14 CARE
            h17 PLACE/SHEEP  -- never fed, never cared
            h20 PLACE/SHEEP  -- never fed, never cared
    tape    h05 PLACE/SHEEP  h06 PLACE/SHEEP     both fed and cared
            h05 PLACE/COW    h12 PLACE/COW

Two sheep at 1+4 is ten wool. The day-6 row sells `FERTILIZER 5` and `WOOL 12`; we ship the
fertilizer and ten of the wool, and `sell 15/17` is that subtraction and nothing else.

The assertion is on WHICH animals the day services, not on how many, and not on the placement
order -- the order is downstream, since an animal placed at h17 has nothing left to be fed with.
A day that placed the sheep first and still fed the cows would be the same defect.
"""
import collections
import importlib

import pytest

import kagg.plan as _PLAN

SEED = 11
DAY = 0


@pytest.fixture(scope="module")
def serviced():
    """Which species our seat FEEDs and CAREs on day 0, read off the tile each unit stands on."""
    import scripts.breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)
    shops = B.recorded_shops(replay)

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2)
    ours = SA.make_agent(sched, 0, router=True)
    opp = B.tape_policy(replay, team, 1)

    fed, placed = collections.Counter(), []
    for t in range((DAY + 1) * 24):
        o0, o1 = env.state[0].observation, env.state[1].observation
        o0.town["unlocked_shops"] = list(shops(t))
        farm = o0["farms"][0]
        tiles = farm["tiles"]
        at = [tuple(farm.get("farmer") or (4, 4))]
        for h in (farm.get("hands") or []):
            at.append(tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4))))

        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if t // 24 == DAY:
            for u, act in enumerate([a0["farmer"]] + list(a0["hands"] or [])[:n0]):
                if not act or u >= len(at):
                    continue
                x, y = at[u]
                cell = tiles[y][x]
                if act[0] in ("FEED", "CARE") and isinstance(cell, dict) and "animal" in cell:
                    fed[(act[0], cell["animal"])] += 1
                if act[0] == "PLACE" and len(act) > 1:
                    placed.append((t % 24, act[1]))

        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return fed, placed


def test_the_premise_day_zero_cannot_service_everything_it_places(serviced):
    """Guard. With a FEED for every animal placed there is nothing to choose between and the rule
    below is vacuous."""
    row = _PLAN.load("data/seed_scripts/kawashigi/schedule.json").get(DAY) or {}
    places = list(row.get("places") or [])
    fed, _ = serviced
    served = sum(n for (op, _a), n in fed.items() if op == "FEED")
    assert 0 < served < len(places), (
        f"d{DAY} places {len(places)} animals and FEEDs {served} -- there is no shortage to "
        "allocate, so this test is measuring nothing")


def test_the_premise_the_day_places_both_species(serviced):
    """Guard. The choice only exists if day 0 puts down a sheep and a cow."""
    row = _PLAN.load("data/seed_scripts/kawashigi/schedule.json").get(DAY) or {}
    places = collections.Counter(row.get("places") or [])
    assert places["SHEEP"] and places["COW"], (
        f"d{DAY} places {dict(places)} -- one species only, so there is nothing to prefer")


def test_the_scarce_feed_goes_to_the_sheep(serviced):
    fed, placed = serviced
    sheep = fed[("FEED", "SHEEP")]
    cow = fed[("FEED", "COW")]
    assert sheep >= cow, (
        f"d{DAY} fed COW x{cow} and SHEEP x{sheep}, placing {placed}. A cow placed today banks its "
        "care bonus over d0-d7 -- eight days for a cap of six -- and is fed on every one of d1-d6, "
        "so today's feed changes nothing about its d8 milk. A sheep has only d0-d4, five days for "
        "the same cap of six, so every one is worth a unit of wool. Missing d0 takes both sheep "
        "from 6 to 5 and the d6 row from WOOL 12 to WOOL 10, which is `sell 15/17`.")


def test_the_sheep_is_on_the_board_early_enough_to_be_fed(serviced):
    """The feed rule cannot fire on an animal that is not standing in a pen yet, so the placement
    order carries it. `places` already reads SHEEP, COW, SHEEP, COW -- the schedule's own order."""
    _, placed = serviced
    first_sheep = next((h for h, a in placed if a == "SHEEP"), None)
    first_cow = next((h for h, a in placed if a == "COW"), None)
    assert first_sheep is not None, f"d{DAY} placed no SHEEP at all: {placed}"
    assert first_cow is None or first_sheep <= first_cow, (
        f"d{DAY} placed its first COW at h{first_cow:02d} and its first SHEEP at h{first_sheep:02d} "
        f"({placed}). The schedule's `places` row is SHEEP, COW, SHEEP, COW and the tape places both "
        "sheep at h05 and h06. A sheep that arrives at dusk cannot be fed, and its d6 wool is one "
        "unit short for the rest of its life.")
