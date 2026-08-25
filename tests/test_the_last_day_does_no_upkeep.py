"""FEED and CARE on the last day buy nothing. The turns belong to harvest and delivery.

Both ops pay out through `_daily_refresh_animals`, which runs inside `_end_of_day`:

    if days_since_first >= 0 and days_since_first % a["interval"] == 0:
        base = 1
        bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
        tile["yield_units"] = min(a["max_held"], tile["yield_units"] + base + bonus)

On day 29 that fires at the rollover into day **30**, and there is no day 30. The units land on the
pen and no turn ever exists to harvest them, so neither the base yield nor the care bonus can reach
the shed, let alone the market.

The other thing a FEED buys is survival -- `consecutive_unfed >= 2` removes the animal. That is also
worthless on the last day: the score is banked money, and an animal that escapes after the final
turn costs nothing.

The tape agrees, and the grid says so plainly (ours/tape):

    row              d27       d28       d29
    feed           14/14     14/10     14/0
    care           14/12     14/9      14/0
    collect_fert   14/12     14/9      14/0
    harvest        31/35     29/32     26/19
    drop            0/0       2/0       2/9

**Zero feeds, zero cares and zero fertilizer collections on its last day**, against our 42
unit-turns, and it spends the day harvesting and walking produce in -- nine DROPs to our two.

What those turns are worth: the season currently ends with 51 sellable units still in the crew's
hands, about $1,192 at the closing book, because there are no turns left to walk them to the shed
(`tests/test_the_last_day_puts_its_load_in_the_shed.py`). Twenty-eight turns of upkeep against the
~36 needed to send six loaded hands home is most of the gap.

This pins the ops, not the routing: nothing here says which hand goes where.
"""
import importlib

import pytest

import reference.kaggriculture as KG

RT = importlib.import_module("kagg.search.router")
R = importlib.import_module("kagg.search.routines")

LAST_DAY = R.SEASON_DAYS - 1


def _pen(animal="COW", placed_day=0, fed=False, cared=False, unfed=0):
    return {"animal": animal, "placed_day": placed_day, "fed_today": fed,
            "cared_today": cared, "consecutive_unfed": unfed, "yield_units": 0}


def test_the_last_day_is_twenty_nine():
    """The premise. If the season length moves this test is aimed at the wrong day."""
    assert LAST_DAY == 29, f"SEASON_DAYS says the last day is {LAST_DAY}"


def test_upkeep_pays_out_only_at_the_rollover():
    """Read off the reference: production happens in `_end_of_day`, never during the day.

    If a FEED could add a unit the same turn, skipping it on the last day would cost real produce.
    """
    src = KG._daily_refresh_animals.__doc__ or ""
    assert "_daily_refresh_animals" in KG._end_of_day.__code__.co_names, (
        "animal production moved out of _end_of_day; re-read it before trusting this test")
    assert "FEED" not in [n for n in KG._apply_unit_action.__code__.co_names if n == "yield_units"], (
        "sanity: FEED must not add yield_units during the turn")


def test_no_feed_is_offered_on_the_last_day():
    ops = RT.animal_ops(_pen(), LAST_DAY, have_wheat=True)
    assert not [o for o in ops if o[0] == "FEED"], (
        f"a FEED was offered on d{LAST_DAY}; it pays out at the rollover into d30, which does not "
        f"exist, and a starved animal costs nothing once the season is scored: {ops}")


def test_no_care_is_offered_on_the_last_day():
    ops = RT.animal_ops(_pen(fed=True), LAST_DAY, have_wheat=True)
    assert not [o for o in ops if o[0] == "CARE"], (
        f"a CARE was offered on d{LAST_DAY}; its bonus is released by the next production night, "
        f"which never comes: {ops}")


def test_the_underfoot_feed_also_stops_on_the_last_day():
    """The 2026-08-15 relapse. Dropping FEED from `animal_ops` measured d29 feed 14 -> 14.

    The route is a visit order and the EXECUTOR re-derives work at every stop and crossing:
    `underfoot()` (`schedule_agent:2458`) feeds any pen it stands on if `will_be_fed` agrees, so
    the ration the planner declined went in anyway the moment a loaded hand crossed the pen. The
    predicate is the one place all the feed paths ask, so it is the one place the last day says no.
    """
    assert not RT.will_be_fed(_pen(), LAST_DAY), (
        "will_be_fed still says yes on the last day, so underfoot() re-adds every FEED the "
        "planner dropped -- measured as d29 feed 14/0 with NO_UPKEEP_ON_THE_LAST_DAY on")


def test_the_underfoot_feed_still_runs_on_d28():
    """The other side: d28's feed pays out at the d29 rollover and must stay."""
    assert RT.will_be_fed(_pen(), LAST_DAY - 1), (
        "will_be_fed stopped feeding a d28 pen; only the last day buys nothing")


def test_the_last_day_gate_is_one_predicate():
    """`underfoot()`'s CARE branch cannot ask `animal_ops`, so it needs the same gate the FEED
    paths use. Pin the helper both will call."""
    assert RT.upkeep_buys_nothing(LAST_DAY)
    assert not RT.upkeep_buys_nothing(LAST_DAY - 1)
    assert not RT.upkeep_buys_nothing(None)


def test_a_ripe_pen_is_still_harvested_on_the_last_day():
    """The other side. Dropping upkeep must not stop us collecting what is already there."""
    pen = _pen(fed=True, cared=True)
    pen["yield_units"] = 4
    ops = RT.animal_ops(pen, LAST_DAY, have_wheat=True)
    assert [o for o in ops if o[0] == "HARVEST"], (
        f"the last day refused to harvest a pen holding 4 units: {ops}")


@pytest.mark.parametrize("day", [20, 25, 28])
def test_every_other_day_is_untouched(day):
    """This must be the LAST day only -- d28's feed still pays out at the d29 rollover.

    **d28 is no longer unconditional, knowingly, 2026-08-25.** `SHEEP_GO_HUNGRY_FROM_DAY = 27` lets
    a pen that can no longer earn its ration go hungry on d27 and d28, which is what makes it escape
    at the d28 rollover -- カワシギ's own timing, and worth `+$480 a game, sem 128, t=3.75` over 60
    paired tapes (`docs/kawa_herd_and_the_tape_gate_2026-08-25.md`). Exempting d28 would make the
    whole rule a no-op, because an escape needs two consecutive misses.

    Alex, told this test stood in the way: *"well that test is not relevant if we break it
    knowingly"*.

    So the claim is narrowed rather than dropped: on d20, d25 and d28 a pen that **still has product
    coming** is fed. That is what the docstring above always meant -- the original fixture happened
    to be a COW whose d29 rollover is `(29-0-8) = 21`, odd, so at `interval` 2 it produced nothing
    and the feed it asserted bought nothing.
    """
    pen = _pen(unfed=1)
    # A pen with a yield still to come, which is the case the rule is protecting.
    pen["yield_units"] = 2
    ops = RT.animal_ops(pen, day, have_wheat=True)
    assert [o for o in ops if o[0] == "FEED"], (
        f"d{day} stopped offering FEED to a hungry pen that still has product: {ops}")
