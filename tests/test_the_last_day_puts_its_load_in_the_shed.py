"""On the last day the automatic drop is too late. Anything still in a hand is thrown away.

`_end_of_day` calls `_drop_inventories_to_shed`, so on every ordinary day a unit's carried load
reaches the shed for free and no DROP op is needed -- which is why カワシギ emits **five** DROPs in
the whole of `92498144` against 389 harvests.

Day 29 is different, and only day 29. The drop still happens, but it happens after the last turn,
and `_commit_unit` will only sell what is already in `private["shed"]`:

    if op == "SELL":
        if private["shed"].get(item, 0) <= 0:
            return False

So produce that ends the season in a hand is never sellable. It is not carried over, it is not
banked, it is simply gone.

Measured on the kawashigi grid, seed 11, at the final step of d29:

    US    carried and LOST   58 units  ~$1,430   {WHEAT: 34, MILK: 12, FERTILIZER: 12}
    US    shed at close       0 units
    TAPE  carried and LOST    7 units    ~$245   {WHEAT: 7}
    TAPE  shed at close       2 units

The tape spends **9 DROPs on d29** against our 2, which is the whole of the difference: it walks its
load in, we finish the season holding it.

This pins the outcome, not the mechanism. It does not say which hand delivers, or when, only that
the season must not end with the crew holding sellable goods.
"""
import collections
import importlib

import pytest

import reference.kaggriculture as KG

A = importlib.import_module("kagg.search.schedule_agent")
B = importlib.import_module("scripts.breakdown")
PLAN = importlib.import_module("kagg.plan")

#: What we are willing to leave in hands at the close. The tape leaves 7, so demanding zero would
#: be stricter than the player we are chasing and would fail on a rounding of the last tour.
TOLERATED_UNITS = 12


@pytest.fixture(scope="module")
def final_state():
    """Carried inventories and shed for both seats at the last step of the season."""
    from kaggle_environments import make

    B.schedule_agent = A
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = PLAN.load(schedule)
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)
    opp = B.tape_policy(replay, team, 1)

    last = None
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t // 24 == 29:
            carried = []
            for i in (0, 1):
                c = collections.Counter()
                for inv in (env.state[i].observation["private"].get("inventories") or []):
                    for k, v in (inv or {}).items():
                        c[k] += v
                carried.append(c)
            last = (carried, env.state[0].observation["market"]["inventory"])
        env.step([me(o0, t), opp(o1, t)])
        if env.done:
            break
    return last


def test_the_automatic_drop_cannot_rescue_the_last_day():
    """The premise, read off the reference rather than assumed.

    If a SELL could draw from a unit's inventory this whole test is aimed at nothing.
    """
    priv = {"shed": {"WHEAT": 0}}
    farm = {"money": 0.0}
    market = {"inventory": {"WHEAT": 10000}}
    assert KG._commit_unit("SELL", "WHEAT", 50, farm, priv, market) is False, (
        "a SELL committed against an empty shed; then carrying stock would be harmless")
    priv["shed"]["WHEAT"] = 1
    assert KG._commit_unit("SELL", "WHEAT", 50, farm, priv, market) is True
    assert "_drop_inventories_to_shed" in KG._end_of_day.__code__.co_names, (
        "the automatic drop moved out of _end_of_day; re-read where it runs before trusting this")


@pytest.mark.xfail(strict=True, reason=(
    "KNOWN GAP, UNFIXED. 51 sellable units (~$1,192) end the season in the crew's hands. Two "
    "attempts failed and are recorded so they are not re-tried blind: adding d29 to "
    "WALK_THE_LOAD_HOME_DAYS recovered only 7 units, because a solved route stores work stops and "
    "materialise appends the shed trip from slack that d29 does not have; and freeing 28 turns by "
    "dropping FEED/CARE regressed harvest 396->389 and sell 1489->1474, because _apply_precomputed "
    "keys on the exact op tuple. The fix has to come from the route storing its delivery, or from "
    "_apply_precomputed not matching on ops. strict=True so it reports the day either lands."))
def test_the_season_does_not_end_with_the_crew_holding_sellable_goods(final_state):
    """The defect. Every unit here is produce the board grew and we threw away."""
    carried, inv = final_state
    ours = carried[0]
    sellable = {k: n for k, n in ours.items() if k in inv and n > 0}
    lost = sum(sellable.values())
    value = sum(n * KG.market_price(k, inv[k]) for k, n in sellable.items())
    theirs = sum(v for k, v in carried[1].items() if k in inv)
    assert lost <= TOLERATED_UNITS, (
        f"the season ended with {lost} sellable units in our hands, worth about ${value:,.0f} at "
        f"the closing book: {sellable}. The tape ends holding {theirs}. `_end_of_day` drops these "
        f"into the shed after the last turn, and `_commit_unit` will not sell from a hand, so they "
        f"are simply discarded.")
