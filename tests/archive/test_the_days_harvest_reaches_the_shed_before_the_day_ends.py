"""Produce picked during a day is in the shed before that day's last market phase.

The market reads `private["shed"]` and nothing else (`_commit_unit`, `kaggriculture.py:639-670`).
A unit sitting in a hand is not sellable, however valuable it is and however long the crew has been
carrying it. At the rollover `_drop_inventories_to_shed(private, shed_cap)` (`:864`) empties every
hand into the shed **subject to `shedCapacity`**, and `farm["hands"] = []` on the next line throws
away whatever did not fit.

So a tour that harvests all day and never walks to the shed loses twice: the day's produce cannot be
sold on the day it was picked, and any overflow past 100 units is destroyed outright.

Measured on ladder game 91989194 (our shipped agent, seat 1, against Ahmet Abdullah Gultekin), the
game we lost by $14,810. Day 21, the melon flush:

    turn      vine   shed  hands   hands detail
    d21 h07     57      0      6   u2:6
    d21 h13     31      0     36   u2:6, u4:12, u6:6, u8:6, u11:6
    d21 h17     15      0     54   u2:6, u4:12, u6:12, u8:12, u11:6, u12:6
    d21 h23      5      3    146   FERTILIZER 10, MELON 66, STRAWBERRY 34, WOOL 16, WHEAT 8, MILK 12
    d22 h00      5    100      0

Six hands carried 146 units past a shed holding 3, with 97 slots free, for the whole day. At the
rollover 49 units were binned -- MELON 66 -> 36, STRAWBERRY 34 -> 24, WOOL 16 -> 12, MILK 12 -> 9,
FERTILIZER 11 -> 9 -- roughly $6,000 at that day's prices.

The 36 melons that survived went to market on d22, by which time the opponent had walked the book
from $238 to $133 selling his own flush across d20 and d21. Our 36 units realised **$54**. His 114
units realised $21,743. That single product is $13,522 of the $14,810 game.

Note what this is NOT. It is not a decision to hold stock for a better price: `HOLD_A_FLOORED_BOOK`
(`schedule_agent.py:2576`) already refuses to do that for melon, and its docstring records the
measurement -- the town drains melon at 1/day, so `d_rem >= supply` is false and the guard correctly
does not fire. The stock was never in the shed for any sell rule to see.

Two assertions, both about the same mechanism and both on OUR seat:

  1. Nothing is destroyed at a rollover. Pure loss, no tradeoff, no judgement call.
  2. Produce picked on a day is sellable on that day -- the shed is not empty at the day's last
     market phase while the hands are loaded.

The second says nothing about whether the day SHOULD sell, only that it must be able to. A day whose
crew picks nothing is skipped by both.
"""
import collections
import kagg.plan as _PLAN
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

#: The ladder game we lost. `weedSpawnChance` is the ladder's own 0.005, not the 0.0 the local
#: tape work uses -- this test is about the board that was actually played.
REPLAY = REPO / "data/seed_scripts/ladder/91989194.json"
OPPONENT = "Ahmet Abdullah Gultekin"
OUR_SEAT = 1
TPD = 24
DAYS = 30
CAP = 100


@pytest.fixture(scope="module")
def season():
    """`{day: (shed_at_h23, hands_at_h23, shed_at_next_dawn)}` for our seat."""
    import breakdown as B
    from kaggle_environments import make

    import kagg.search.schedule_agent as sa

    raw = json.loads(REPLAY.read_text())
    names = raw["info"]["TeamNames"]
    assert names[OUR_SEAT].lower().startswith("alex"), f"seat {OUR_SEAT} is {names}"
    team = names[1 - OUR_SEAT]

    sched = {int(k): v for k, v in json.loads(
        (_PLAN.SHIPPED_PLAN).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    #: The board that was ACTUALLY played, not `env_config`'s economy subset. `ECONOMY_KEYS` is
    #: `("townCenterSellInterval",)` only, so it drops `weedSpawnChance` (0.005 on the ladder, 0.0
    #: in all local tape work) and cannot carry a seed at all -- the replay's `configuration.seed`
    #: is null and the real one is in `info.seed`. Replayed without it this game lands on a random
    #: board and finishes 108,794 vs 109,225 instead of the 67,479 vs 82,289 that was played.
    cfg = {k: v for k, v in (raw.get("configuration") or {}).items() if v is not None}
    cfg["seed"] = raw["info"]["seed"]
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, OUR_SEAT, router=True)
    opp = B.tape_policy(REPLAY, team, 1 - OUR_SEAT)

    out = {}
    for t in range(TPD * DAYS):
        if env.done:                    # the env allows 719 steps, not 720
            break
        obs = [env.state[i].observation for i in range(2)]
        ours = agent(obs[OUR_SEAT])
        theirs = opp(obs[1 - OUR_SEAT], t)
        acts = [None, None]
        for seat, a in ((OUR_SEAT, ours), (1 - OUR_SEAT, theirs)):
            n = len(obs[0]["farms"][seat].get("hands") or [])
            acts[seat] = {"farmer": a["farmer"], "hands": list(a["hands"])[:n],
                          "market": a["market"]}
        if t % TPD == TPD - 1:
            p = env.state[OUR_SEAT].observation["private"]
            hands = collections.Counter()
            for inv in p.get("inventories") or []:
                for k, v in inv.items():
                    hands[k] += int(v)
            out[t // TPD] = [dict(p["shed"]), dict(hands), None]
        env.step(acts)
        if t % TPD == TPD - 1 and t // TPD in out:
            out[t // TPD][2] = dict(env.state[OUR_SEAT].observation["private"]["shed"])
    return out


def test_the_premise_the_crew_picks_something(season):
    """Guard. If nothing is ever harvested both assertions below are vacuous."""
    assert any(sum(h.values()) for _s, h, _n in season.values()), \
        "our seat never carried a single unit in a hand; wrong fixture"


@pytest.mark.parametrize("day", range(DAYS - 1))
def test_no_produce_is_destroyed_at_the_rollover(season, day):
    """`_drop_inventories_to_shed` obeys shedCapacity and `hands = []` bins the rest."""
    shed, hands, nxt = season[day]
    if not sum(hands.values()):
        pytest.skip(f"d{day} ends with empty hands")
    before = sum(shed.values()) + sum(hands.values())
    after = sum((nxt or {}).values())
    lost = {k: (int(shed.get(k, 0)) + int(hands.get(k, 0))) - int((nxt or {}).get(k, 0))
            for k in set(list(shed) + list(hands))
            if (int(shed.get(k, 0)) + int(hands.get(k, 0))) > int((nxt or {}).get(k, 0))}
    assert before == after, (
        f"d{day} ends holding {before} units ({sum(shed.values())} shed + {sum(hands.values())} "
        f"hands) and {after} survive the rollover. Destroyed: {lost}. shedCapacity is {CAP} and "
        f"`_drop_inventories_to_shed` bins the overflow -- the crew carried produce past a shed "
        f"with {CAP - sum(shed.values())} free slots all day.")


@pytest.mark.parametrize("day", range(DAYS - 1))
def test_the_days_produce_is_sellable_on_the_day_it_is_picked(season, day):
    """The market reads the shed only. A loaded hand at dusk is a day's sales that cannot happen."""
    shed, hands, _nxt = season[day]
    carried = sum(hands.values())
    if not carried:
        pytest.skip(f"d{day} ends with empty hands")
    room = CAP - sum(shed.values())
    assert carried <= room or room <= 0, (
        f"d{day} h23: the crew is carrying {carried} units ({dict(hands)}) while the shed holds "
        f"{sum(shed.values())}/{CAP} with {room} slots free. None of it was sellable today, and "
        f"{carried - room} units will be destroyed tonight. The tour never walked to the shed.")
