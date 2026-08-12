"""The dawn bank is compared against what the day owes AT DAWN, not against its whole bill.

`_days_bill` sums everything the row buys -- animals, hires, seeds, products, land -- into one
number, and `short_of_cash` compares that to the bank. Day 4 is what that gets wrong:

    cow    400   bought at h0    covered by the $480 dawn bank on its own
    hires   33   h0
    wheat  ~28   h0
    land  1000   bought late     the only thing the day's produce has to fund
    ----------
          ~1461  > $480  ->  short_of_cash  ->  sell_deadline returns `hour` -> due=0, rush=True

Two purchases with different due dates added together, so a parcel nobody needs until the evening
drags the delivery deadline to hour 0 and rushes the whole day to the shed.

The tape does not play it that way. Seb buys his cow at h0 on a $45 bank, then sits on $12 from h2
to h18 with nothing due, sells 5 wheat at h18, and at h21 sells 5 fertilizer and 12 wheat and buys
the parcel in the SAME turn -- funded by its own turn's sells, which settle in earlier order slots.
Then he keeps selling: 12 more at h22, 20 plus a fertilizer at h23, finishing on $1115 against our
$115.

So the dawn question is only "can I cover what I spend at dawn". Land is a dusk obligation because
the agent buys it the first turn it can afford it, and `land_turns` is in `TAPE_ONLY` -- the agent is
never told the hour, so it cannot be treated as an early one.

This is one slice of the ledger in `docs/the_day_is_a_cash_ledger.md`, not the whole of it: the real
model is a list of dated obligations against a running balance, with the sells spread into waves.
This test pins the slice that is provably wrong today.
"""
import importlib
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
MODULE = "kagg.search.schedule_agent_1455mh"


@pytest.fixture(scope="module")
def row():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): v for k, v in raw.items()}


def test_day_four_can_cover_its_dawn_spend_without_selling_anything(row):
    """d4 buys a $400 cow on a $480 bank. That needs no sale, so nothing is due at hour 0."""
    SA = importlib.import_module(MODULE)
    bill_now = SA._days_bill_now(row[4])
    assert bill_now <= 480.0, (
        f"day 4 opens on $480 and its dawn spend is priced at ${bill_now:.0f}. The cow ($400), the "
        f"seven hires ($33) and one wheat fit inside the bank; only the $1000 parcel does not, and "
        f"the parcel is not bought at dawn.")


def test_the_parcel_is_not_counted_as_a_dawn_obligation(row):
    """The land price is the whole gap between the dawn spend and the day's total bill."""
    SA = importlib.import_module(MODULE)
    total, now = SA._days_bill(row[4]), SA._days_bill_now(row[4])
    assert total - now >= 1000.0, (
        f"day 4's total bill is ${total:.0f} and its dawn spend ${now:.0f}. The difference should be "
        f"the parcel; it is ${total - now:.0f}.")


def test_day_four_does_not_rush_its_delivery_to_hour_zero(row):
    """`sell_deadline` must not put d4's row at hour 0 -- the tape delivers it at h18."""
    SA = importlib.import_module(MODULE)
    short = SA._days_bill_now(row[4]) > 480.0
    due = SA.sell_deadline(0, True, short)
    assert due != 0, (
        "day 4 planned to have its whole SELL row in the shed by hour 0. Seb's first DROP that day "
        "is h18 and his first SELL is h18. A deadline of 0 makes every crop tile carry a shed trip "
        "it does not need.")
