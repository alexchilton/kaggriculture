"""`_hires_this_turn` must apply the same wall check the market block applies before it orders.

`_hires_this_turn`'s own docstring states the contract: it predicts "how many hands the market
block below is about to buy" so the DAWN PLAN can route them, and "must not diverge from what that
block actually orders." The market block, at the HIRE_PINNED_DAYS branch, computes
`want = row["hands"]` and then -- on a day that buys land -- caps it with
`_unwalled_landing_slots(tiles, units, want)` before appending any HIRE orders
(`HOLD_A_HIRE_FOR_THE_GROUND_IT_NEEDS`). `_hires_this_turn` never calls `_unwalled_landing_slots` at
all, so on a day where the wall check actually reduces `want`, the forecast and the order diverge --
exactly the failure the docstring warns about.

**Where this actually bites, measured seed 11 against the `victor` tape (`--tape victor`).**
`_unwalled_landing_slots` was instrumented across d0-d12. It is called on exactly the two days with
`land > 0` in the schedule (d6 and d10), and it only REDUCES `want` on one of them:

    d 6   land=1  row hands=4   _unwalled_landing_slots(tiles, units, 4)  -> 2   _hires_this_turn -> 4
    d10   land=1  row hands=14  _unwalled_landing_slots(tiles, units, 14) -> 14  _hires_this_turn -> 14

So d6 is the clean demonstration of THIS bug: the market block's own `want` is 2 (it will not order a
walled hire), but the forecast the dawn plan and `_clear_the_spawn_ring` route against is 4.

**d10 is not evidence for this bug**, despite matching the `land=1, hands=14` description an earlier
pass flagged it under. On d10 the wall check is a no-op (the quadrants already owned before this day
leave no walled shed-access tile at hour 0), so `_hires_this_turn`'s prediction of 14 already equals
the market block's own `want` of 14. d10's real predicted-vs-landed gap (14 predicted, only 7 HIRE
orders actually emitted) is `ORDER_SLOTS = 10` truncating the turn's order queue (2 SELL + 7 HIRE +
1 BUY_LAND = 10 slots, exactly full) -- a different, pre-existing throttle this test does not touch
and this fix does not address.

This test therefore compares `_hires_this_turn`'s prediction against the market block's own
pre-slot-truncation `want` (what it "actually orders," per the docstring, before `ORDER_SLOTS` cuts
the queue -- a cap applied uniformly to every order type, not specific to hiring) -- not against the
final emitted HIRE count, which would also fail on d10 for the unrelated ORDER_SLOTS reason and could
never be made to pass by this fix.

**Why the assertion is `<=`, not `==`, across all days.** `_hires_this_turn` also runs its own fib
affordability simulation, deliberately more conservative than the market block's raw `want` -- the
market block emits `want` HIRE orders unconditionally and lets `_do_hire` fail SILENTLY on a thin
bank, while `_hires_this_turn` predicts only the ones that will actually SETTLE. That is a second,
correct, pre-existing mechanism, not the bug this file is about, and it legitimately makes
`predicted < market_want` on some days (this run: d11) -- especially once the fix changes d6's
hiring and that ripples the bank forward through the rest of the replay, since this is a full env
season, not an isolated call. Requiring strict equality there would fail the test on a correct
forecast for a reason that has nothing to do with the wall check. What must NEVER happen, on any
day, is the reverse: `_hires_this_turn` predicting MORE hires than the wall check would let the
market block order -- that over-count is what orphans a route onto a unit that will not exist, and
it is exactly what d6 demonstrates pre-fix.
"""
import importlib
import inspect
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top2/91854176.json"
SCHEDULE = REPO / "data/seed_scripts/victor/schedule.json"
TEAM = "Victor @ Tufa Labs"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent_1455mh"
SEED = 11
DAYS = 13
TPD = 24


@pytest.fixture(scope="module")
def played():
    """Play d0-d12 of the Victor schedule, recording per day:

      - `predicted[day]`   `_hires_this_turn`'s own return value at hour 0.
      - `row_hands[day]`   the schedule row's raw `hands` value -- independent of the fix, so it can
        anchor the guard test without circularity.
      - `market_want[day]` the market block's `want` for HIRE at hour 0, AFTER the wall check and
        BEFORE `ORDER_SLOTS` truncation -- reconstructed from the schedule row and, on a land day,
        from `_unwalled_landing_slots` called with the exact live `tiles`/`units` the market block
        itself uses (captured via a spy, not recomputed independently, so this cannot silently drift
        from what the real code path does).
    """
    SA = importlib.import_module(MODULE)

    raw = json.loads(SCHEDULE.read_text())
    sched = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    predicted, row_hands, market_want = {}, {}, {}
    real_hires_this_turn = SA._hires_this_turn
    real_unwalled = SA._unwalled_landing_slots
    now = {"day": 0}
    # `tiles`/`units` are only passed if the target still accepts them, so this file demonstrates a
    # clean assertion failure -- not a TypeError -- against the pre-fix signature too (see "revert
    # and confirm red" in the project's testing discipline).
    accepts_tiles = "tiles" in inspect.signature(real_hires_this_turn).parameters

    def spy_hires(state, row, day, hour, money, tiles=None, units=None):
        if accepts_tiles:
            n = real_hires_this_turn(state, row, day, hour, money, tiles=tiles, units=units)
        else:
            n = real_hires_this_turn(state, row, day, hour, money)
        if hour == 0:
            predicted[day] = n
            row_hands[day] = int(row.get("hands", 0) or 0)
            # Default: no land day (or the flag is off) means the market block's `want` is the raw
            # row value, unreduced. `spy_unwalled` below overwrites this for a day it actually runs
            # -- whether that call comes from inside the (now fixed) `_hires_this_turn` or from the
            # market block later in the same turn, both read the same live `tiles`/`units` and so
            # agree by construction.
            market_want[day] = row_hands[day]
        return n

    def spy_unwalled(tiles, units, want):
        n = real_unwalled(tiles, units, want)
        market_want[now["day"]] = n
        return n

    SA._hires_this_turn = spy_hires
    SA._unwalled_landing_slots = spy_unwalled
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(sched, 0, router=True)
        for t in range(TPD * DAYS):
            day = t // TPD
            now["day"] = day
            o0 = env.state[0].observation
            a0, a1 = agent(o0), opp[t]
            env.step([a0, a1])
    finally:
        SA._hires_this_turn = real_hires_this_turn
        SA._unwalled_landing_slots = real_unwalled

    return predicted, row_hands, market_want


def test_a_land_day_reduces_the_market_blocks_want_via_the_wall_check(played):
    """Guard the fixture against seed/tape drift: at least one day must actually exercise the wall
    check with a REDUCTION below the raw schedule row, or the assertion below passes vacuously and
    proves nothing. Anchored on `row_hands`, not `predicted`, so it holds regardless of the fix.
    """
    _predicted, row_hands, market_want = played
    reduced = [d for d in row_hands if market_want[d] < row_hands[d]]
    assert reduced, (
        f"no day in d0-{DAYS - 1} had the wall check reduce `want` below the raw hands row -- "
        f"row_hands={row_hands} market_want={market_want}")


@pytest.mark.parametrize("day", range(DAYS))
def test_the_forecast_never_exceeds_the_market_blocks_own_want(played, day):
    """`_hires_this_turn` must never predict MORE hires than the market block's own `want` after the
    wall check -- an over-count is what orphans a route onto a unit that will not exist this turn.

    Not `==`: `_hires_this_turn` also runs a fib affordability check the market block's raw `want`
    does not (see module docstring), which can legitimately push the prediction BELOW `want` on a
    thin bank. That is a different, correct mechanism and not this bug -- only the `>` direction is
    the wall-check failure.
    """
    predicted, _row_hands, market_want = played
    if day not in predicted:
        pytest.skip(f"d{day} was not reached")
    assert predicted[day] <= market_want[day], (
        f"d{day}: dawn forecast predicted {predicted[day]} hires, more than the market block's own "
        f"`want` of {market_want[day]} after the wall check -- this orphans a route onto a hire the "
        f"market block was never going to order.")


def test_the_known_wall_bound_day_predicts_the_reduced_count(played):
    """The sharpest check: on Victor d6 (`land=1, hands=4`), the wall check caps the market block's
    own `want` to 2 and the bank comfortably affords all 4 (pre-fix `_hires_this_turn` returned the
    full, un-reduced 4 -- affordability was never what limited it). So post-fix the forecast must be
    exactly 2, not merely `<= 4`. Hardcoded rather than parametrized: this is the one day in the
    replay where the wall check is confirmed to bind AND affordability is confirmed not to, so it is
    the one place a strict number is a meaningful assertion rather than a coincidence.
    """
    predicted, _row_hands, market_want = played
    assert market_want[6] == 2, f"fixture/tape drift: expected d6 market_want == 2, got {market_want[6]}"
    assert predicted[6] == 2, (
        f"d6: dawn forecast predicted {predicted[6]} hires; the market block's own want after the "
        f"wall check is 2, and the bank affords all 4 unreduced, so the forecast should read 2.")
