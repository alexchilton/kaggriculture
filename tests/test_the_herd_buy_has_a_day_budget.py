"""The wheat round trip is a BUY-side defect, not a sell-side one.

`docs/fable_the_wheat_churn_2026-08-09.md` has the full write-up. Short version: 66 of our own
1.32.6 ladder replays show the whole field buying 266-392 wheat a season while we buy 1,099 --
selling is downstream of having bought too much, not the anomaly itself. Syed sells 649 and banks
$101k; Seb sells 84 and banks $74k. The field disagrees on how much to SELL and agrees closely on
how much to BUY.

The mechanism is `kagg/search/schedule_agent.py`'s feed-buy emission, ~line 3208:

    short = min(max(herd, min(max(0, owed), BUY_DRIP)), FEED_TURN_CAP)

`owed` (the schedule row) is credited every turn via `state["ordered"][("buys", "WHEAT")]`, so it
self-limits to the day's row and goes quiet once asked. `herd` (`feed_days(day) * alive - fed_today
- on_hand`) chases a 2-4 DAY stock buffer with no day-level ceiling at all -- only the per-turn
`FEED_TURN_CAP` (6) bounds it, giving a theoretical 6 x 24 = 144/day, and the diagnostic trace in
`data/logs/herd_diag_seed11.log` shows it hitting that ceiling on 20+ of 24 turns on the worst days
(17 through 29), for 1,668-1,800 herd-path units asked across the season on seed 11 alone (measured
two ways -- see the doc for why the two numbers differ and which one is ground truth).

The fix adds `herd_ceiling`/`herd_floor` right after `herd` is computed: a day-level ceiling on the
HERD path's own asks, credited against `state["ordered"][("feed", "WHEAT")]` (the SAME counter the
row already uses) and sized at `max(wanted, FEED_BUY_CEILING_DAYS * alive)`, plus a floor
(`alive - fed_today - on_hand`, an ARRIVAL signal) that always wins via `max()` so a genuine
shortfall is never silenced by the budget. `FEED_BUY_CEILING_DAYS = 2`, not 1: a tighter one-day
ceiling passed THIS test and then starved six animals on a fresh run, because the shed can hold idle
wheat that no hand has time to carry to a tile -- a routing/labor limit the old code's gross
over-buying happened to mask with sheer surplus. Two days of ceiling is the smallest headroom this
investigation found that keeps the herd from shrinking at all across the season (see
`test_the_herd_never_shrinks_across_the_season` below).

This test measures the GROUND TRUTH via `kagg.analysis.fills.record_fills` -- never `o[2]` off the
action stream (an offer, re-posted up to 24x) and never a holdings delta (FEED consumes wheat,
HARVEST adds it, both already produced fictitious findings here, see `fills.py`'s own docstring).
"""

import json
import pathlib

import pytest

from kagg.analysis.fills import record_fills

SCHED = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
TAPE = pathlib.Path("data/seed_scripts/top_guys/90976060.json")
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")

pytestmark = pytest.mark.skipif(not SCHED.exists(), reason="gitignored data")


def _thin():
    sched = {int(k): v for k, v in json.loads(SCHED.read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def _play_season(seed=11, days=30, track_herd=False):
    """Our agent (router) against Seb's tape. `track_herd` also returns the herd size (tiles with
    an `"animal"` key) at the end of each in-game day, to check the anti-starvation constraint
    without trusting a holdings-delta proxy for it either."""
    from kaggle_environments import make

    from kagg.arena.tape import build_tape_agent
    from kagg.search import schedule_agent as SA

    ours = SA.make_agent(_thin(), 0, router=True)
    rival = build_tape_agent(TAPE, 1)
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)

    herd_by_day = {}
    with record_fills(env) as fills:
        for t in range(24 * days):
            if env.done:
                break
            o0 = env.state[0].observation
            if track_herd:
                tiles = o0["farms"][0]["tiles"]
                herd_by_day[t // 24] = sum(
                    1 for r in tiles for c in r if isinstance(c, dict) and "animal" in c)
            a0 = ours(o0)
            a1 = rival(env.state[1].observation)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    if track_herd:
        return fills, herd_by_day
    return fills


#: Seb's own tape buys 395 wheat all season on this fixture. Across 66 real 1.32.6 ladder replays
#: the field buys 266-392. Our own `FEED_BUY_CEILING_DAYS = 2` fix measures 797 bought on seed 11 --
#: well above the field, because our herd is a different size to Seb's and the ceiling deliberately
#: keeps two days of buffer headroom (see the module docstring for why one day starved the herd).
#: 1,100 gives seed-to-seed margin (CLAUDE.md: ~15% variance) while still discriminating hard against
#: the unfixed 1,668-1,800.
WHEAT_BOUGHT_CEILING = 1100


@pytest.mark.slow
def test_wheat_bought_stays_within_a_days_budget_of_the_herds_need():
    """RED before the day-budget fix: this measured 1,800 bought on seed 11 (ground truth via
    `record_fills`; see the module docstring's diagnostic for why an offer-count proxy read lower).
    GREEN after: the herd path may no longer chase a 2-4 day stock buffer on every one of the day's
    24 turns."""
    fills = _play_season()
    bought, _cost = fills.bought(player=0, product="WHEAT")
    assert bought > 0, "nothing bought at all; the fixture or the instrument is dead"
    assert bought <= WHEAT_BOUGHT_CEILING, (
        f"{bought} WHEAT units bought against a ceiling of {WHEAT_BOUGHT_CEILING} -- "
        f"the herd path is not day-budgeted")


@pytest.mark.slow
def test_the_herd_never_shrinks_across_the_season():
    """The constraint that made the FIRST version of this fix wrong. `FEED_BUY_CEILING_DAYS = 1`
    (sized at exactly `alive`, one day's consumption) passed the budget test above at 393 bought and
    then this test caught it: seed 11, day 15, the shed held 16-19 idle WHEAT the whole day while
    only 7 of 20 animals got fed, and six of them starved by day 17's rollover
    (`consecutive_unfed >= 2`, `reference/kaggriculture.py:786`). `FEED_BUY_CEILING_DAYS = 2` fixes
    it -- zero drops across the season on this fixture -- and this test is what must stay green if
    that constant, or anything else on this path, moves again."""
    _fills, herd_by_day = _play_season(track_herd=True)
    days = sorted(herd_by_day)
    assert len(days) > 20, "season ended too early to be a meaningful check"
    drops = [(days[i - 1], days[i], herd_by_day[days[i - 1]], herd_by_day[days[i]])
             for i in range(1, len(days)) if herd_by_day[days[i]] < herd_by_day[days[i - 1]]]
    assert not drops, (
        f"herd shrank on {len(drops)} day transition(s) -- (day, day, before, after): {drops}; "
        f"an animal was starved (consecutive_unfed >= 2) or otherwise lost")
