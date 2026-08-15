"""Sell late, unless today's shopping list costs more than the bank holds.

**Read off Seb's own tape, and it is not a constant hour.** His sell hour tracks his cash need:

    d2   SELL FERTILIZER  h15x3 h19x2          nothing to fund that day
    d3   SELL FERTILIZER  h15x4 h18x1          nothing to fund that day
    d6   SELL WOOL        h09x6 h13x6          BUY_LAND at h13, bank $5 -> $1,349

On d6 he sells in the MORNING, and it is the one day in that window whose row buys a parcel. On the
days with nothing to fund he sells after the town has drained the book. So "sell late" is the
default and "sell now" is what a purchase buys you out of.

Ours does neither. Exact fills, seed 11, crew planner on d0-d6 (`data/logs/cadence_all.log`):

    d2   SELL FERTILIZER  h07x1 h08x1 h12x1 h13x2      early, funding nothing
    d3   SELL FERTILIZER  h07x1 h12x1 h13x2 h14x1      early, funding nothing
    d6   SELL WOOL        h07x1 h19x5                  1 unit early, 5 too late to buy land

Twelve wool either way on d6. We hold $47 at h13 and do not reach $1,400 until h23, so the parcel
slips and d6 ends on 50 tiles against his 75.

**Why the hour matters at all.** `townCenterSellInterval = 24` on this economy, so the town drains
the book once a day; `market_price` falls monotonically in inventory (`kaggriculture.py:177`) and
recovers as the shops restock every 4 steps. Selling before the drain is selling into the bottom of
the curve. But a better price is worthless if the cash arrives after the purchase it was for, which
is Alex's framing and the reason this is a gate and not a constant: once the bank covers the day,
the timing is free money; while it does not, the timing IS the purchase.

`LATE_SELL_BIAS` has existed and shipped OFF this whole time. Switched on flat it delays the d6
wool past h13 and makes the parcel strictly worse -- which is presumably why it was measured as a
loss and left off. The demand gate is the missing half.
"""
import collections
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

from kagg.analysis.fills import record_fills

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/91422988.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAYS = 7


def _sched():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): v for k, v in raw.items()}


def _opponent():
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    return [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]


@pytest.fixture(scope="module")
def season():
    """Per-hour EXACT fills, plus tiles owned at each dusk.

    Fills are diffed out of `record_fills` after every step rather than counted off the action
    stream: the agent re-posts a standing order every turn, so an offer count is up to 24x the
    truth. See `kagg/analysis/fills.py`.
    """
    full = _sched()
    thin = {d: {a: b for a, b in r.items() if a not in TAPE_ONLY} for d, r in full.items()}
    opp = _opponent()
    SA = importlib.import_module(MODULE)
    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    fills_at = collections.defaultdict(list)     # (day, op, item) -> [(hour, units)]
    bank = {}                                    # (day, hour) -> money at the START of that turn
    with record_fills(env) as fills:
        prev = collections.Counter()
        for t in range(24 * DAYS):
            o0 = env.state[0].observation
            a0, a1 = agent(o0), opp[t]
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            now = collections.Counter({k: len(v) for k, v in fills._rows.items()})
            for (seat, op, item), n in (now - prev).items():
                if seat == 0:
                    fills_at[(t // 24, op, item)].append((t % 24, n))
            prev = now
            bank[(t // 24, t % 24)] = float(o0["farms"][0]["money"])
    return {"fills": dict(fills_at), "sched": full, "bank": bank, "bill": SA._days_bill}


def _hours(season, day, op, item):
    return [h for h, _n in season["fills"].get((day, op, item), [])]


def test_the_premise_day_six_is_the_only_funded_day_in_the_window(season):
    """Runs first. d6 buys a parcel and d2/d3 buy nothing large, which is what makes them a clean
    pair -- same product, same week, opposite cash position."""
    sched = season["sched"]
    assert int(sched[6].get("land") or 0) == 1, (
        "day 6's row no longer buys land, so it cannot be the funded day. Wrong tape, or the "
        "schedule was rederived."
    )
    for day in (2, 3):
        assert not int(sched[day].get("land") or 0), (
            f"day {day}'s row buys land, so it is not an unfunded-day control."
        )


def test_nothing_clears_early_on_a_turn_the_bank_could_already_pay_for(season):
    """The mechanism, asserted per turn rather than on a hand-picked day.

    The first cut of this test named d2 and d3 as "nothing to fund" controls because neither buys
    land. d2 holds; **d3 sells at h07/h12/h13/h14 and is right to** -- its row places a COW on top
    of seven wheat and seven hires, and our bank at that point does not cover it. Picking control
    days by eye asserted the wrong thing; the rule is about the bank against the bill, so that is
    what is checked.

    `pending` (this turn's sale proceeds, banked before BUY_LAND settles) is not visible here, but
    it is never negative, so `money + pending < bill` implies `money < bill`. Checking the weaker
    form cannot produce a false failure.
    """
    SA = importlib.import_module(MODULE)
    offenders = []
    for (day, op, item), rows in season["fills"].items():
        if op != "SELL":
            continue
        bill = season["bill"](season["sched"].get(day) or {})
        for hour, units in rows:
            if hour >= SA.LATE_SELL_FROM_HOUR:
                continue
            money = season["bank"].get((day, hour), 0.0)
            if money >= bill:
                offenders.append((day, hour, item, units, round(money), round(bill)))
    assert not offenders, (
        "sold before hour {} on turns whose bank already covered the whole day's bill "
        "(day, hour, item, units, money, bill):\n  {}".format(
            SA.LATE_SELL_FROM_HOUR,
            "\n  ".join(str(o) for o in sorted(offenders))))


def test_a_day_that_must_buy_land_sells_early_enough_to_pay_for_it(season):
    """The other half, and the one a flat `LATE_SELL_BIAS` gets wrong. Red today for the opposite
    reason to the test above: five of our twelve wool clear at h19, six hours after the parcel
    needed paying for."""
    wool = _hours(season, 6, "SELL", "WOOL")
    assert wool, "day 6 sold no wool at all; the row asks for twelve."
    assert min(wool) <= 13, (
        f"day 6's wool cleared at {wool}. He sells six at h09 and six at h13 and takes the parcel "
        f"at h13 on the proceeds. A sale after h13 cannot fund it."
    )
    assert sum(n for h, n in season["fills"].get((6, "SELL", "WOOL"), []) if h <= 13) >= 6, (
        f"day 6 cleared only {[(h, n) for h, n in season['fills'].get((6, 'SELL', 'WOOL'), [])]} "
        "by h13. One unit is not a parcel; he banks $1,344 off six."
    )
