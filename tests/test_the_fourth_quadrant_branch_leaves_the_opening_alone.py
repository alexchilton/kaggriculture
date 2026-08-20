"""The q4 variant must be the shipped agent up to d12, and only then diverge.

Three separate theories, one test each.

1. The trigger matches a shop name the environment can actually emit. A predicate keyed on a
   misspelled shop is a predicate that never fires, and it reads exactly like a measured null.
2. Arming the fourth quadrant reaches the agent that plays the game. `schedule_agent.make_agent`
   shallow-copies the OUTER schedule dict and shares every row object with its caller, so a row
   mutated in place is seen -- but that is a property of one line of someone else's module and it
   is the kind of thing that gets "cleaned up" into a deep copy.
3. d0 through d11 is action-for-action identical to what ships. This is the one that matters: the
   whole claim of the variant is that it changes the season from d12 and nothing earlier. Adding a
   `land` row at d12 is NOT obviously inert before d12 -- `_pens_due_before_more_land` scans days
   AFTER today for the next parcel, so a new land day changes what d11 believes about its own pens.
"""
import collections
import sys

import pytest

sys.path.insert(0, ".")

import reference.kaggriculture as KG
from kagg.search import q4_agent as Q4
from kagg.search import schedule_agent as SA
import kagg.plan as PLAN

SCHEDULE = "data/seed_scripts/kawashigi/schedule.json"


def _obs(day, shops):
    return {"day": day, "hour": 0, "town": {"unlocked_shops": list(shops)}}


# --------------------------------------------------------------------------- theory 1
def test_the_trigger_names_a_shop_the_environment_can_draw():
    assert Q4.YARN_STORE in KG.SHOPS, (
        f"{Q4.YARN_STORE!r} is not a shop the town can unlock; "
        f"the trigger would never fire. Real names: {sorted(KG.SHOPS)}")
    assert KG.SHOPS[Q4.YARN_STORE] == ["WOOL"], (
        "the yarn store is the wool shop; if it stopped carrying wool the sheep-heavy "
        "herd has lost its reason")


def test_the_trigger_fires_on_a_yarn_store_and_not_on_anything_else():
    assert Q4.the_town_promised_wool_early(_obs(6, ["YARN_STORE", "BAKERY"]))
    assert Q4.the_town_promised_wool_early(_obs(6, ["BAKERY", "YARN_STORE"]))
    assert not Q4.the_town_promised_wool_early(_obs(6, ["BAKERY", "PIZZA_SHOP"]))
    assert not Q4.the_town_promised_wool_early(_obs(6, []))


def test_the_trigger_only_looks_at_the_draws_that_have_landed_by_its_day():
    """Shops unlock every `townShopUnlockInterval` = 3 days, so d6 has seen exactly two draws.

    A yarn store arriving at d9 or later is a different board -- the leader's own tapes hold cows
    at 10 on those -- and the predicate must not claim it.
    """
    assert Q4.the_town_promised_wool_early(_obs(6, ["BAKERY", "YARN_STORE"]))
    # a third draw is d9 evidence; asked as of d6 it is not on the board yet
    assert not Q4.the_town_promised_wool_early(
        _obs(6, ["BAKERY", "PIZZA_SHOP", "YARN_STORE"]))


# --------------------------------------------------------------------------- theory 2
def test_arming_the_parcel_reaches_the_row_the_inner_agent_reads():
    sched = PLAN.load(SCHEDULE)
    armed = Q4._own_the_schedule(sched)
    inner_view = {int(k): v for k, v in armed.items()}      # what schedule_agent.make_agent does
    Q4._arm_the_fourth_quadrant(armed)
    assert int(inner_view[Q4.Q4_BUY_DAY].get("land", 0)) == 1, (
        "the parcel row did not reach the dict the agent walks")
    assert inner_view[Q4.Q4_BUY_DAY]["animals_bought"].get("SHEEP") == Q4.Q4_EXTRA_SHEEP
    assert int(inner_view[Q4.Q4_BUY_DAY].get("builds", 0)) == Q4.Q4_EXTRA_SHEEP
    assert list(inner_view[Q4.Q4_BUY_DAY].get("places")) == ["SHEEP"] * Q4.Q4_EXTRA_SHEEP


def test_arming_does_not_leak_into_the_callers_schedule():
    """Two agents built from one loaded schedule must not infect each other."""
    sched = PLAN.load(SCHEDULE)
    before = dict(sched[Q4.Q4_BUY_DAY]) if Q4.Q4_BUY_DAY in sched else dict(sched[str(Q4.Q4_BUY_DAY)])
    armed = Q4._own_the_schedule(sched)
    Q4._arm_the_fourth_quadrant(armed)
    row = sched.get(Q4.Q4_BUY_DAY, sched.get(str(Q4.Q4_BUY_DAY)))
    assert int(row.get("land", 0)) == int(before.get("land", 0) or 0) == 0
    assert not (row.get("places") or [])


def test_the_parcel_the_env_hands_over_is_the_south_east_one():
    """`_do_buy_land` takes `LAND_ORDER[len(unlocked) - 1]`, so the third parcel is not a choice."""
    assert KG.LAND_ORDER == ["NE", "SW", "SE"]
    assert KG.LAND_PRICES[2] == 4000
    assert Q4.Q4_QUADRANT == "SE"


def test_the_herd_split_answers_the_armed_row_with_six_cows_and_twelve_sheep():
    """The split reads the schedule's COUNT and the shop draw decides the mix."""
    sched = PLAN.load(SCHEDULE)
    armed = Q4._own_the_schedule(sched)
    Q4._arm_the_fourth_quadrant(armed)
    inner = {int(k): v for k, v in armed.items()}
    want = collections.Counter()
    for d in sorted(inner):
        if d <= 12:
            for a, q in (inner[d].get("animals_bought") or {}).items():
                want[a] += int(q)
    assert want["COW"] + want["SHEEP"] == Q4.Q4_COW + Q4.Q4_SHEEP, (
        f"armed schedule asks for {dict(want)}, which cannot reach "
        f"COW {Q4.Q4_COW} / SHEEP {Q4.Q4_SHEEP}")
    split = SA._herd_split(want, bought={"COW": 6, "SHEEP": 8}, day=12, hour=0,
                           unlocked_shops=["YARN_STORE", "BAKERY"])
    assert split == {"COW": Q4.Q4_COW, "SHEEP": Q4.Q4_SHEEP}, split


# --------------------------------------------------------------------------- theory 3
#: Seeds whose town draws a YARN_STORE in its first two draws, measured by playing the shipped
#: agent in both seats and reading `town.unlocked_shops` at d6h0 (`data/logs/q4_shopscan.log`).
#:
#: **These cannot be found by stepping a PASS-only game, and the first version of this test did
#: exactly that and was vacuous.** The shop draw comes off the environment's own `rng`, which the
#: weed spawn and everything else also consume, so a game where nobody plants anything draws a
#: DIFFERENT shop stream from the game the agents actually play. The pre-scan said seed 0 had an
#: early yarn store; the real game shows `['BAKERY', 'PET_CAFE']`. The identity assertions all
#: passed and tested nothing, because the branch under test never armed.
#:
#: 11 of seeds 0-69, a base rate of 15.7% against a theoretical 1 - (7/8)**2 = 23.4%. The gap is a
#: 20-seed run with none in it, not a bias worth modelling.
EARLY_YARN_SEEDS = (3, 10, 17, 18, 22, 45, 47, 53, 60, 65, 66)


@pytest.mark.slow
@pytest.mark.parametrize("seed", EARLY_YARN_SEEDS)
def test_the_opening_is_action_for_action_what_ships(seed):
    """Play both agents against the SAME environment and compare every action through d11.

    Only one agent can drive the seat, so the shipped agent plays the game and the q4 agent is
    handed the identical observation each turn and asked what it would do. That is the strict test:
    any divergence in the opening shows up as a differing action on the turn it happens.

    Routes are NOT unsolved before d12. The q4 branch turns them live from d12, which is after the
    window this test covers, so the solved routes are still in force for every turn compared.

    **The `armed` assertion at the end is the one that keeps this from being vacuous.** The branch
    only edits the schedule when the trigger fires, so on a board with no early yarn store the two
    agents are the same object graph and the comparison proves nothing at all.
    """
    from kaggle_environments import make

    sched = PLAN.load(SCHEDULE)
    shipped = SA.make_agent(PLAN.load(SCHEDULE), me=0)
    q4 = Q4.make_agent(sched, me=0)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    opp = SA.make_agent(PLAN.load(SCHEDULE), me=1)

    last_compared = -1
    for t in range(719):
        o = env.state[0].observation
        day = int(o.get("day", 0) or 0)
        a_ship = shipped(o, t)
        a_q4 = q4(o, t)
        if day < Q4.Q4_BUY_DAY:
            assert a_q4 == a_ship, (
                f"seed {seed} d{day} h{int(o.get('hour', 0) or 0)} (turn {t}): the q4 variant "
                f"diverged before d{Q4.Q4_BUY_DAY}\n  shipped {a_ship}\n  q4      {a_q4}")
            last_compared = day
        env.step([a_ship, opp(env.state[1].observation, t)])
        if env.done or day > Q4.Q4_BUY_DAY:
            break

    assert last_compared == Q4.Q4_BUY_DAY - 1, (
        f"the comparison never reached d{Q4.Q4_BUY_DAY - 1}; it stopped at d{last_compared}")
    assert q4.q4_report["armed"], (
        f"seed {seed} is in EARLY_YARN_SEEDS but the trigger did not fire; its d6 draws were "
        f"{q4.q4_report['shops_at_d6']}. The comparison above therefore tested nothing.")
