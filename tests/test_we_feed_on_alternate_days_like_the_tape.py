"""A pen fed yesterday does not need feeding today. The env says so, and the tape does it.

**What a FEED actually buys, read off `_daily_refresh_animals` (`kaggriculture.py:795-820`):**

    if tile["fed_today"]:  tile["consecutive_unfed"] = 0
    else:                  tile["consecutive_unfed"] += 1
    if tile["consecutive_unfed"] >= 2:   ...animal escapes...
    ...
    if days_since_first >= 0 and days_since_first % a["interval"] == 0:
        base = 1
        bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
        tile["yield_units"] = min(a["max_held"], tile["yield_units"] + base + bonus)
    if tile["cared_today"] and tile["fed_today"]:
        tile["pending_care_bonus"] = ... + 1

`base = 1` is added **unconditionally**. Production does not read `fed_today` at all.

**CORRECTED 2026-08-10, and the original claim here was wrong.** This file used to say a feed on a
non-production night "buys nothing whatsoever". It buys the right to CARE, and `pending_care_bonus`
**accumulates** -- one per fed-and-cared night, all the way to the next payout, where it is consumed
in a single `min(max_held, yield + base + bonus)`. Verified against the env itself, COW placed d0
(`first_yield_day 8, interval 2, max_held 6`), units held after d9:

    fed+cared EVERY day          -> 6      (bonus reaches 7 by d6, capped at max_held on payout)
    fed+cared alternate days     -> 2
    fed every day, NEVER cared   -> 2

So the care chain is worth **3x** on a cow, and skipping the feed of a pre-production animal skips
its CARE too, because `router.animal_ops` offers CARE only on a pen that is fed.

**The cadence still ships, on measurement, not on that argument.** Feeding every pen every day to
collect the chain was measured at seed 11 with the crew planner on d0-d3: **$63,600 against
$91,943**, and 21 tiles starved against 18. A wheat and two turns per pen per day costs more than
the milk it banks. The 3x is real and unexploited; capturing it needs to be selective (the pens
close to a payout, not all of them), which is an open question and not this rule.

`router.animal_ops` was built on the opposite belief and says so in its own comment: *"skipping it
forfeits the day's production AND the care bonus"*. Half of that is false, and it is the half that
made every feed MANDATORY.

**The tape feeds on a cycle and it is not subtle.** Ops emitted per day against pens owned:

           d4   d5   d6   d7   d8   d9  d10  d11  d12  d13
    ours    7    7    7    7    7    8    7   15   16   21
    tape    7    4    7    3    7   11   12   17   16   16
    pens    7    7    7   17   17   17   18   21   21   21

Seventeen pens on d7 and he feeds THREE. Nothing starves -- `consecutive_unfed >= 2` leaves a whole
day of slack, and he uses all of it. The animal intervals point the same way: a COW produces every
SECOND day (`first_yield_day 8, interval 2`) and a SHEEP every THIRD (`6, 3`), so a daily feed on a
cow is wasted on at least half the days by construction.

What it costs us is turns and wheat in the same breath: on d7 that is eight extra unit-turns plus
their wheat, on a day the tape spends the difference planting ten to our seventeen and banks $723
against our $217.
"""
import importlib

import pytest

RT = importlib.import_module("kagg.search.router")


def _pen(animal="COW", unfed=0, fed=False, cared=False, placed=0, bonus=0, yield_units=0):
    return {"kind": "PASTURE", "animal": animal, "consecutive_unfed": unfed,
            "fed_today": fed, "cared_today": cared, "placed_day": placed,
            "pending_care_bonus": bonus, "yield_units": yield_units,
            "fertilizer_available": False}


def _ops(cell, day):
    return {o for o, _i, _p in RT.animal_ops(cell, day, have_wheat=True)}


def test_a_pen_that_has_not_started_producing_is_not_fed_unless_it_is_hungry():
    """The rule as it SHIPS, which is not the first rule this file asserted.

    The first cut skipped any pen that does not yield TONIGHT. It measured d16 money
    $9,975 -> $4,814, because `CARE` is offered only on a fed pen and `pending_care_bonus` is banked
    only on a night that is both fed and cared: feed nightly and a production night pays
    `base 1 + bonus 1`; feed only on the payout night and it pays 1. Same turns per unit, half the
    product. So the daily feed of a PRODUCING animal earns its turn.

    What never earns it is the daily feed of one that has not started. A cow placed on d5 first
    yields on d13 (`first_yield_day 8`); until then a feed buys nothing but survival, and
    `consecutive_unfed >= 2` gives that away every second day for free.
    """
    quiet = _pen(unfed=0, placed=5)
    assert "FEED" not in _ops(quiet, day=8), (
        "a cow eight days from its first yield, which ate yesterday, was offered a feed. It cannot "
        "produce and it cannot escape tonight, so the turn and the wheat buy nothing at all."
    )


def test_a_producing_pen_is_still_fed_every_day():
    """The other side of it, and the one the measurement insisted on. Red if the rule is written as
    'produces tonight' rather than 'has started producing' -- that variant costs $5,161 a season."""
    working = _pen(unfed=0, placed=0)
    assert "FEED" in _ops(working, day=8), (
        "a cow past its first yield day was skipped. Feeding it is what lets it be CARED, which is "
        "what banks `pending_care_bonus`, which doubles what the next production night pays."
    )


def test_the_cadence_leaves_the_first_week_alone():
    """d0-d6 must stay matched -- Alex's standing rule, and the tape agrees.

    Its feed row over d0-d4 is 4, 5, 5, 6, 7 against 8 pens: everything, every day. The cycling is
    visible at d5 and unmistakable at d7, where he places twelve pens and feeds three. Applied from
    d0 the cadence drags rows that have nothing to do with feeding -- d2 `sell 4/5 -> 2/5`, d3
    `water 14/14 -> 12/14` -- because a rolling half-herd is hungry every morning, every one of
    those feeds prices as CRITICAL, and the routes reorder around them.
    """
    assert RT.FEED_CADENCE_FROM_DAY >= 7, (
        f"FEED_CADENCE_FROM_DAY is {RT.FEED_CADENCE_FROM_DAY}. At 5 it takes d6 off `feed 7/7`, and "
        "at 0 it costs d2 and d3 rows that are exact in the tape."
    )
    fresh = _pen(unfed=0, placed=0)
    assert "FEED" in _ops(fresh, day=2), (
        "a pen was skipped inside the first week. Whatever the cadence is worth later, d0-d6 is "
        "matched and must stay matched."
    )


def test_a_hungry_pen_is_still_fed_and_still_critical():
    """The other half, and the one that must never soften. One more missed day and the animal is gone.

    Red if the rule is written as a blanket cadence rather than as `consecutive_unfed >= 1`.
    """
    hungry = _pen(unfed=1, placed=0)
    ops = RT.animal_ops(hungry, day=8, have_wheat=True)
    assert "FEED" in {o for o, _i, _p in ops}, (
        "a pen that missed yesterday was not offered a feed. `consecutive_unfed >= 2` removes the "
        "animal outright tonight (`kaggriculture.py:804`); this is the one feed that is mandatory."
    )
    prize = next(p for o, _i, p in ops if o == "FEED")
    assert prize >= RT.CRITICAL, (
        f"the hungry feed is priced at {prize}, below CRITICAL ({RT.CRITICAL}). It is the only op on "
        "the board that loses an asset outright if it is skipped."
    )


def test_a_pen_is_fed_on_the_night_it_pays_out_a_care_bonus():
    """`bonus` is released only `if tile["fed_today"]` on a production night. That feed earns.

    Cow placed d0, `day=9`: `days_since_first = 10 - 0 - 8 = 2`, `2 % 2 == 0`, so it produces
    tonight, and it is holding a care bonus to release.
    """
    paying = _pen(unfed=0, placed=0, bonus=1)
    assert "FEED" in _ops(paying, day=9), (
        "a pen that produces tonight and is holding a care bonus was not offered a feed. The bonus "
        "is forfeited unless `fed_today` is set (`kaggriculture.py:813`), and it is the ONLY thing "
        "a non-hungry feed can buy."
    )


@pytest.mark.parametrize("animal,day,produces", [
    ("COW", 9, True),     # 10 - 0 - 8 = 2,  2 % 2 == 0
    ("COW", 8, False),    #  9 - 0 - 8 = 1,  1 % 2 == 1
    ("SHEEP", 8, True),   #  9 - 0 - 6 = 3,  3 % 3 == 0
    ("SHEEP", 7, False),  #  8 - 0 - 6 = 2,  2 % 3 == 2
    ("GOOSE", 5, True),   #  6 - 0 - 4 = 2,  interval 1, always
])
def test_the_production_night_is_read_the_way_the_env_reads_it(animal, day, produces):
    """`next_day - placed_day - first_yield_day`, then modulo the interval. Off by one and the whole
    rule feeds on the wrong nights, which is invisible in a season total and fatal per animal."""
    assert RT.produces_tonight(_pen(animal, placed=0), day) is produces
