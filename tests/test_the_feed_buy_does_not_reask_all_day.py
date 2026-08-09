"""The feed buy has no cross-turn memory, so it re-asks the herd's WHOLE remaining need every hour.

One theory, one test. The theory: `herd = feed_days(day) * alive - fed_today - on_hand`
(`schedule_agent.py`) is recomputed from scratch on every turn with no credit for what the same day
already ordered, so once the herd outgrows what `FEED_TURN_CAP` and half the bank let through in one
order, the remainder is re-asked on every remaining turn of the day.

Measured on seed 11 against Seb's own schedule, offers read off the action stream:

    day   row   turns ordering   units offered
      0     8                8               8      <- exact, and this is why it hid
      5     3                3               3
     15    20               15              38
     22    20               22             123
     24    20               22             131      <- 6.5x the row
     29     0               10              56      <- the row is ZERO
    ---   407              359           1,468

Early season it is invisible: `alive` is small, one order covers the ration, and the emission matches
the row unit for unit. It only degenerates as the herd grows.

**Two real failure modes sit on this line and the code currently has the second one.** The `ordered`
term was removed deliberately, and the comment above it records why: `ordered` counts what was
OFFERED and never what FILLED, so one unfilled order left `herd <= 0` for the rest of the day and six
animals went unfed while the cows died 7 -> 6 -> 5. Putting the term back reintroduces exactly that.
The comment immediately BELOW the line then claims the subtraction is still there -- it is not, and
the two comments contradicting each other is what let this survive.

So the bound has to credit what ARRIVED rather than what was asked for. `on_hand` already does: it is
recomputed from the live shed, hands and ripe field every turn, so a filled order is visible there
and an unfilled one is not. What is missing is that a day's cumulative purchases are never compared
against the day's genuine ration.

This test asserts the property, not the implementation -- any fix that stops the re-ask without
starving the herd passes it.
"""

import collections
import json
import pathlib

import pytest

SCHED = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
TAPE = pathlib.Path("data/seed_scripts/top_guys/90976060.json")
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")

pytestmark = pytest.mark.skipif(not SCHED.exists(), reason="gitignored data")


def _season(seed=11, days=30):
    """Play our agent against Seb's tape, returning per-day wheat offers and true fills.

    Fills come from `kagg.analysis.fills`, which resolves the seat inside `_process_market` where the
    live farm list is in scope. Do NOT re-derive attribution from `id(...)` on an observation object:
    `kaggle_environments` rebuilds `env.state` between steps, so such a check silently records zero.
    That mistake has now been made twice in this repository.
    """
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.arena.tape import build_tape_agent
    from kagg.search import schedule_agent as SA

    sched = {int(k): v for k, v in json.loads(SCHED.read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    ours = SA.make_agent(thin, 0, router=True)
    rival = build_tape_agent(str(TAPE), 0)
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)

    turns = collections.Counter()
    offered = collections.Counter()
    with record_fills() as fills:
        for t in range(24 * days):
            if env.done:
                break
            o0 = env.state[0].observation
            a0 = ours(o0)
            a1 = rival(env.state[1].observation)
            for o in (a0.get("market") or []):
                if o and o[0] == "BUY_PRODUCT" and o[1] == "WHEAT":
                    turns[t // 24] += 1
                    offered[t // 24] += int(o[2])
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    rows = {d: int(((sched.get(d, {}) or {}).get("buys") or {}).get("WHEAT", 0) or 0)
            for d in range(days)}
    return turns, offered, rows, fills


@pytest.mark.slow
def test_the_feed_buy_does_not_fire_on_almost_every_turn_of_a_day():
    """The direct statement of the defect: a metered drip does not speak on 23 turns out of 24.

    `BUY_DRIP` exists to SPREAD one day's purchase across the hours, so several turns per day is
    intended and is not what this catches. Firing on most of the day is the re-ask.
    """
    turns, offered, rows, _f = _season()
    worst = max(turns.values()) if turns else 0
    busy = sorted(d for d, n in turns.items() if n > 12)
    assert worst <= 12, (
        f"the feed buy fired on {worst} turns of one day; days over 12 turns: {busy}\n"
        f"per-day turns: {dict(sorted(turns.items()))}")


@pytest.mark.slow
def test_a_day_does_not_offer_several_times_its_own_row():
    """A day's offers should stay near its row. The row is the plan we chose to follow; drifting to
    6x it means the executor, not the plan, is deciding how much wheat the farm buys."""
    _t, offered, rows, _f = _season()
    bad = {d: (offered[d], rows[d]) for d in range(30)
           if offered[d] > max(4, rows[d] * 2)}
    assert not bad, ("days offering more than twice their row (offered, row): "
                     f"{dict(sorted(bad.items()))}")


@pytest.mark.slow
def test_the_last_day_buys_no_feed_at_all():
    """Day 29's row is 0 and nothing bought then can ever be eaten -- the season ends that night."""
    _t, offered, _r, _f = _season()
    assert offered[29] == 0, f"bought {offered[29]} units of feed on the final day"


@pytest.mark.slow
def test_the_season_does_not_buy_several_times_the_plans_wheat():
    """The money statement. Seb's own tape buys 395 against this row of 407; we bought 1,830 at
    ~$53/unit, which is the whole bank gap on this seed."""
    _t, _o, rows, fills = _season()
    bought, cost = fills.bought(player=0, product="WHEAT")
    plan = sum(rows.values())
    assert bought <= plan * 1.5, (
        f"bought {bought} wheat (${cost:,.0f}) against a season row of {plan}; "
        f"Seb's tape buys 395 on the same row")
