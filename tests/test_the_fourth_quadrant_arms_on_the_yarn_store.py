"""The four-quadrant branch arms on the yarn store, once, and only after the opening is safe.

Written RED before the branch was wired into `schedule_agent`, per the project rule.

Each test names the mechanism it protects, not the symptom. The two that matter most:

- `test_installing_mutates_the_rows_in_place` -- `make_agent` rebuilds the outer dict with int keys
  but SHARES the row objects, and reads them live each turn. A branch that rebinds rows instead of
  mutating them produces a byte-identical null that looks exactly like a working branch.
- `test_the_opening_is_untouched` -- the two tapes are the same plan through d8. If a swap ever
  reaches d0-d8 the standing "do not regress the opening" rule is broken silently, because the
  branch only fires on 15% of seeds and would not show up in an average.
"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

import reference.kaggriculture as KG
from kagg.search import q4_branch as Q

REPO = pathlib.Path(__file__).resolve().parent.parent


def a_schedule():
    """The shipped three-quadrant plan, as `make_agent` holds it: int keys, live row objects."""
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    return {int(k): v for k, v in raw.items()}


def an_observation(shops):
    return {"town": {"unlocked_shops": list(shops)}}


def test_the_trigger_shop_is_a_real_shop_in_the_environment():
    """A trigger naming a shop the env does not have would never fire, and never say so."""
    assert Q.TRIGGER_SHOP in KG.SHOPS
    assert KG.SHOPS[Q.TRIGGER_SHOP] == ["WOOL"]


def test_the_town_promise_is_read_from_the_town_not_a_top_level_shops_key():
    """`observation["shops"]` does not exist; reading it produced all-zero drains over 5,376 games."""
    assert Q.the_town_promised_wool_early(an_observation(["YARN_STORE", "BAKERY"])) is True
    assert Q.the_town_promised_wool_early(an_observation(["BAKERY"])) is False
    assert Q.the_town_promised_wool_early({"shops": ["YARN_STORE"]}) is False
    assert Q.the_town_promised_wool_early({}) is False


def test_it_does_not_decide_before_the_deciding_day():
    sched, state = a_schedule(), {}
    for day in range(Q.DECIDE_BY_DAY):
        assert Q.arm(sched, state, an_observation(["YARN_STORE"]), day) is False
    assert "q4_decided" not in state


def test_it_arms_on_the_deciding_day_when_the_yarn_store_is_up():
    sched, state = a_schedule(), {}
    assert Q.arm(sched, state, an_observation(["YARN_STORE"]), Q.DECIDE_BY_DAY) is True
    assert state["q4_armed"] is True


def test_it_stays_disarmed_without_the_yarn_store():
    sched, state = a_schedule(), {}
    before = json.dumps(sched[12], sort_keys=True)
    assert Q.arm(sched, state, an_observation(["BAKERY", "PET_CAFE"]), Q.DECIDE_BY_DAY) is False
    assert json.dumps(sched[12], sort_keys=True) == before


def test_it_decides_exactly_once_even_if_the_shop_appears_later():
    """A shop unlocking on d10 must not re-arm a plan whose split day has already passed."""
    sched, state = a_schedule(), {}
    assert Q.arm(sched, state, an_observation(["BAKERY"]), Q.DECIDE_BY_DAY) is False
    for day in range(Q.DECIDE_BY_DAY + 1, 20):
        assert Q.arm(sched, state, an_observation(["YARN_STORE"]), day) is False
    assert json.dumps(sched[12].get("land")) == "0"


def test_the_opening_is_untouched():
    """d0-d8 are the same plan in both tapes, so arming must change nothing there."""
    sched = a_schedule()
    before = {d: json.dumps(sched[d], sort_keys=True) for d in range(Q.SPLIT_DAY)}
    Q.arm(sched, {}, an_observation(["YARN_STORE"]), Q.DECIDE_BY_DAY)
    for d in range(Q.SPLIT_DAY):
        assert json.dumps(sched[d], sort_keys=True) == before[d], f"d{d} changed"


def test_installing_mutates_the_rows_in_place():
    """The row OBJECT must survive; `make_agent` shares it and reads it live every turn."""
    sched = a_schedule()
    keep = {d: sched[d] for d in range(30)}
    Q.install_the_fourth_quadrant(sched)
    for d in range(30):
        assert sched[d] is keep[d], f"d{d} row was rebound, not mutated -- this is a silent null"


def test_arming_buys_the_fourth_parcel_and_the_sheep_heavy_herd():
    """The branch's whole content: a third land purchase on d12, and SHEEP where q3 takes COW."""
    sched = a_schedule()
    assert sched[12].get("land", 0) == 0
    Q.arm(sched, {}, an_observation(["YARN_STORE"]), Q.DECIDE_BY_DAY)
    assert sched[12].get("land", 0) == 1, "the fourth parcel is the branch"

    herd = {}
    for d in range(30):
        for k, v in (sched[d].get("animals_bought") or {}).items():
            herd[k] = herd.get(k, 0) + v
    assert herd == {"COW": 6, "SHEEP": 12}, f"expected the leader's four-quadrant herd, got {herd}"


def test_the_split_day_is_the_first_day_the_two_tapes_disagree():
    """If they ever diverge earlier, the opening is no longer safe by construction."""
    q3 = a_schedule()
    q4 = {int(k): v for k, v in
          json.loads((REPO / Q.Q4_SCHEDULE).read_text()).items()}
    for d in range(Q.SPLIT_DAY):
        assert q3[d].get("animals_bought") == q4[d].get("animals_bought"), f"d{d} herd differs"
        assert q3[d].get("land", 0) == q4[d].get("land", 0), f"d{d} land differs"
    assert q3[Q.SPLIT_DAY].get("animals_bought") != q4[Q.SPLIT_DAY].get("animals_bought")


def test_the_q4_routes_cover_every_day_from_the_split():
    """Routes solved for 75 tiles DROP on a 100-tile board; the branch needs its own table."""
    q4 = __import__("kagg.search.solved_days_q4", fromlist=["SOLVED_DAYS"])
    assert set(q4.SOLVED_DAYS) >= set(range(Q.SPLIT_DAY, 30))


def test_switching_the_branch_off_changes_nothing():
    sched, state = a_schedule(), {}
    before = json.dumps(sched, sort_keys=True)
    Q.BRANCH_ON_THE_YARN_STORE = False
    try:
        assert Q.arm(sched, state, an_observation(["YARN_STORE"]), Q.DECIDE_BY_DAY) is False
        assert json.dumps(sched, sort_keys=True) == before
    finally:
        Q.BRANCH_ON_THE_YARN_STORE = True
