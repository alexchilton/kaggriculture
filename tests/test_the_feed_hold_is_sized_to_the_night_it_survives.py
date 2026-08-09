"""The wheat hold is a constant times the herd; it should be what tonight can spare.

## The theory under test

`feed_days(day)` returns one number that sizes two decisions:

* the BUY  (`schedule_agent.py`, `herd = feed_days(day) * alive - fed_today - on_hand`)
* the SELL (`schedule_agent.py`, `have -= feed_days(day) * alive - carried - drawn - will_buy`)

Neither reads the shed. `FEED_DAYS_LATE` is 4, so a nineteen-head herd asks for 76 units of a shed
that holds **100 slots shared by all nine products**, and the farm keeps buying wheat into a shed
that is about to delete the day's harvest at the rollover.

FEED takes exactly one WHEAT per animal per day (`reference/kaggriculture.py:495`), so the wheat
that has to survive the night is **one meal per animal**, plus whatever buffer the dawn top-up
needs against a book that will not fill. Everything above that is occupying a slot that a $120
strawberry could have used.

## What this asserts

On a night the rollover destroys product, the shed may not be holding more wheat than the herd
will eat before the next dawn buy. It is a statement about the HOLD on the nights the hold costs
something, not about the season total -- `test_the_shed_does_not_destroy_the_harvest` owns the
outcome and `test_the_feed_reserve_yields_a_shed_slot.py` owns the open defect record.

## The discard is read off the env, not off a shed delta

`tests/test_the_feed_reserve_yields_a_shed_slot.py` and
`docs/fable_the_discard_problem_2026-08-09.md` both measure the night's loss as
`held_at_dusk - shed_at_dawn`. That is not the discard: hour 23's SELL and BUY_PRODUCT settle in
the SAME step as the rollover, so a sale counts as a loss and a purchase hides one. On seed 11,
full season, the delta method reports 105-137 units destroyed and the env destroys **7**.

This fixture patches `_drop_inventories_to_shed`, which is the only code path in the game that
deletes product (`PLACE` into a full shed clamps and leaves the remainder in the hand,
`kaggriculture.py:380-396`), so the count here is exact.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

SEED, DAYS, HANDOVER, CAP = 11, 30, 11, 100

#: One WHEAT per animal per day is what FEED takes, so one meal per head is the wheat that has to
#: survive the night. The shipped hold is `FEED_DAYS_LATE * alive` = 4x that.
MEALS_PER_ANIMAL_PER_DAY = 1

_DISCARDS = []


def _install_discard_probe():
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    if getattr(KG, "_hold_test_probe", False):
        return
    orig = KG._drop_inventories_to_shed

    def patched(private, capacity):
        before = collections.Counter()
        for inv in private["inventories"]:
            before.update({k: int(v) for k, v in inv.items() if int(v) > 0})
        before.update({k: int(v) for k, v in private["shed"].items()})
        orig(private, capacity)
        after = collections.Counter({k: int(v) for k, v in private["shed"].items()})
        _DISCARDS.append({k: v for k, v in (before - after).items() if v > 0})

    KG._drop_inventories_to_shed = patched
    KG._hold_test_probe = True


def _season(bounds_the_buy):
    """Replay Seb d0..d10, hand over at d11, and record every night the rollover deletes product."""
    from kaggle_environments import make

    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    _install_discard_probe()
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
    was = SA.FEED_HOLD_BOUNDS_THE_BUY
    SA.FEED_HOLD_BOUNDS_THE_BUY = bounds_the_buy
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    out, dusk = [], None
    for t in range(24 * DAYS - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        priv = o0.get("private") or {}
        shed = collections.Counter({k: int(v) for k, v in (priv.get("shed") or {}).items()})
        day, hour = t // 24, t % 24

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
            animals = [c for r in o0["farms"][0]["tiles"] for c in r
                       if isinstance(c, dict) and "animal" in c]
            dusk = dict(day=day, wheat=int(shed.get("WHEAT", 0)), shed=sum(shed.values()),
                        hands=hands, alive=len(animals),
                        unfed=sum(1 for a in animals if not a.get("fed_today")))

        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        _DISCARDS.clear()
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if hour == 23:
            # `_drop_inventories_to_shed` runs once per farm in seat order, so seat 0 is first.
            lost = _DISCARDS[0] if _DISCARDS else {}
            # The wheat visible at dusk is a floor on what survives: the rollover fills the shed to
            # capacity and wheat is already IN it, so it is never the part that dies.
            dusk["lost"] = sum(lost.values())
            dusk["lost_by"] = lost
            # Escapes are read from the herd count either side of the rollover: an animal that ate
            # nothing two days running is deleted there (`kaggriculture.py:804`).
            after = sum(1 for r in env.state[0].observation["farms"][0]["tiles"] for c in r
                        if isinstance(c, dict) and "animal" in c)
            dusk["escaped"] = max(0, dusk["alive"] - after)
            out.append(dusk)
            dusk = None
    SA.FEED_HOLD_BOUNDS_THE_BUY = was
    return out


@pytest.fixture(scope="module")
def bounded():
    return _season(True)


@pytest.fixture(scope="module")
def unbounded():
    return _season(False)


@pytest.fixture(scope="module")
def nights(bounded):
    return [r for r in bounded if r["lost"] > 0]


def _table(rows):
    head = "    day  shedWHEAT  need  shedTOT  hands  alive  lost  lost_by"
    body = ["    %3d  %9d  %4d  %7d  %5d  %5d  %4d  %s"
            % (r["day"], r["wheat"], r["alive"] * MEALS_PER_ANIMAL_PER_DAY, r["shed"], r["hands"],
               r["alive"], r["lost"],
               ",".join(f"{k}:{v}" for k, v in sorted(r["lost_by"].items(), key=lambda kv: -kv[1])))
           for r in rows]
    return "\n".join([head] + body)


@pytest.mark.slow
def test_bounding_the_buy_by_the_shed_destroys_less_of_the_harvest(bounded, unbounded):
    """The shipped half of the fix. Reverting `FEED_HOLD_BOUNDS_THE_BUY` must turn this red."""
    off = sum(r["lost"] for r in unbounded)
    on = sum(r["lost"] for r in bounded)
    assert off > 0, "the fixture no longer reproduces the defect at all"
    assert on < off, (
        f"the rollover destroyed {on} units with the buy bounded by the shed and {off} without it, "
        "so bounding it is buying nothing. `feed_hold()` is what makes the wheat reserve a "
        "participant in the hundred-slot budget instead of a rule that never reads it; if this "
        "test is green with the flag reverted, the bound is not reaching the BUY_PRODUCT path.")


@pytest.mark.slow
def test_the_herd_is_not_starved_to_free_a_shed_slot(bounded, unbounded):
    """A hold that saves slots by losing animals is not a fix. Escapes may not get worse."""
    off = sum(r["escaped"] for r in unbounded)
    on = sum(r["escaped"] for r in bounded)
    assert on <= off, (
        f"{on} animals escaped with the buy bounded against {off} without it. An escape is an "
        "irreversible $400-$500 write-off plus every remaining day of that animal's production "
        "(`kaggriculture.py:786`), and no number of saved shed slots pays for one. "
        "`FEED_DAYS_FLOOR * alive` is meant to be the floor the bound can never cross.")


@pytest.mark.xfail(reason="OPEN, PARTIALLY CLOSED 2026-08-09. Bounding the BUY (shipped) takes this "
                          "fixture from 123 units destroyed to 69 and from 5 offending nights to 4, "
                          "but it cannot empty a pile that was bought earlier in the day when the "
                          "hands were still empty. Closing it needs the SELL bound as well "
                          "(`FEED_HOLD_BOUNDS_THE_SELL`), which is the direction "
                          "`FEED_RESERVE_YIELDS_TO_OVERFLOW` was rejected on and which measured "
                          "+15% escapes over 32 seeds. See "
                          "docs/feed_hold_and_shed_knapsack_2026-08-09.md.",
                   strict=False)
@pytest.mark.slow
def test_a_night_that_bins_product_holds_no_more_wheat_than_the_herd_will_eat(nights):
    """The hold must be the night's real need, not `FEED_DAYS_LATE` times the herd."""
    assert nights, "no night destroyed anything -- the fixture no longer reproduces the defect"
    over = [r for r in nights if r["wheat"] > r["alive"] * MEALS_PER_ANIMAL_PER_DAY]
    surplus = sum(r["wheat"] - r["alive"] * MEALS_PER_ANIMAL_PER_DAY for r in over)
    assert not over, (
        f"{len(over)} of {len(nights)} nights that DESTROYED product were holding more wheat than "
        f"the herd eats in a day: {surplus} surplus units of the {CAP} shed slots, on nights that "
        f"binned {sum(r['lost'] for r in over)} units of product:\n"
        + _table(over)
        + f"\n    `feed_days(day)` is {SA.FEED_DAYS_LATE} from day {SA.FEED_DAYS_FROM_DAY} and is "
          "multiplied by the live herd at both call sites, so the hold is 4 meals per animal and "
          "no call site has ever read the shed. The hold that gets the herd to the next dawn buy "
          "is one meal per animal plus a fill-risk buffer, and it can never be worth more slots "
          "than the shed has left.")
