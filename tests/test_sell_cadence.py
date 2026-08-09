"""Our sells fragment into 2.4x more fills than Seb's, each worth half as much.

Measured by `scripts/sell_shape.py` on fills -- a positive bank delta, not an order count, because
the agent re-posts each quota on all 24 turns and counting orders counts one sale up to 24 times:

    seed 11   ours 177 fills, 5.9/day, mean $575    SEB 75 fills, 2.7/day, mean $1,118
    seed 12   ours 186 fills, 6.2/day, mean $792    SEB 84 fills, 3.0/day, mean $1,481

Our MAX fill is larger than his ($7,902 vs $7,207) and our late share is the same (42% vs 47%), so
this is not that we cannot sell big and not that we sell at the wrong time. We fragment.

**Why cadence, when a price floor and a volume cap both lost money.** `schedule_agent` already
records the mechanism without connecting it: `market_price` falls monotonically in inventory and a
SELL walks the book one unit at a time, while shops drain inventory **every 4 steps** and the town
centre **every 12** (`kaggriculture.py:706-716`). Offering on every turn therefore sells into a book
that has had one step to recover; offering on the drain cadence lets each fill meet a book that has
fully refilled.

That is a different lever from the two already tried and rejected:

    refuse to sell below 0.5x base   -$16,025   a PRICE floor -- goods never clear
    cap the quota to a day total     -$ 2,653   a VOLUME cap -- misses the book's recovery

Cadence caps neither price nor volume. The same units are offered; they are offered on fewer turns.
The standing-offer argument ("an order is only a request, re-offering is free") is exactly what this
tests: re-offering is free in ACTIONS and not free in PRICE.

Liquidation is exempt. On the last day the shed has no terminal value and the book's recovery is
irrelevant because there is no tomorrow to recover into.
"""

import importlib

import pytest

import kagg.search.schedule_agent as SA


@pytest.fixture(autouse=True)
def _fresh():
    """Flags are module globals and these tests set them, so reload between tests."""
    importlib.reload(SA)
    yield
    importlib.reload(SA)


def test_the_flag_exists_and_ships_off():
    """Every market change in this project ships off until an arena can score it."""
    assert hasattr(SA, "SELL_ON_DRAIN_CADENCE"), "the cadence flag does not exist"
    assert SA.SELL_ON_DRAIN_CADENCE is False, "a market change must not ship on unmeasured"


def test_the_cadence_matches_the_shops_drain_interval():
    """4 is not a tuning choice, it is `kaggriculture.py`'s shop drain interval. A cadence that does
    not divide the drain interval sells into a partially recovered book on some turns and a full one
    on others, which is the fragmentation this is meant to remove."""
    assert SA.SELL_EVERY_N_HOURS == 4


def test_a_non_terminal_offer_only_fires_on_the_cadence():
    """The whole behaviour, at the level of the predicate rather than a whole season."""
    SA.SELL_ON_DRAIN_CADENCE = True
    firing = [h for h in range(24) if SA.sell_hour_is_open(h, liquidating=False)]
    assert firing == [0, 4, 8, 12, 16, 20], f"fired on {firing}"


def test_liquidation_ignores_the_cadence():
    """On the last day the shed has no terminal value and there is no tomorrow for the book to
    recover into, so holding stock back to catch a better price is a pure loss."""
    SA.SELL_ON_DRAIN_CADENCE = True
    assert all(SA.sell_hour_is_open(h, liquidating=True) for h in range(24))


def test_the_flag_off_restores_every_turn_exactly():
    """Off must be the shipped behaviour, not an approximation of it."""
    SA.SELL_ON_DRAIN_CADENCE = False
    assert all(SA.sell_hour_is_open(h, liquidating=False) for h in range(24))


def test_the_cadence_cuts_the_offer_turns_but_not_the_quota():
    """The distinction from the two rejected fixes, stated as an assertion.

    A price floor refuses units; a day-total cap refuses units. Cadence refuses neither -- the same
    quota is still owed and is still re-offered, on a quarter of the turns. If this ever starts
    reducing the quota it has become the fix that already lost $2,653.
    """
    SA.SELL_ON_DRAIN_CADENCE = True
    open_hours = sum(SA.sell_hour_is_open(h, liquidating=False) for h in range(24))
    assert open_hours == 24 // SA.SELL_EVERY_N_HOURS
    assert not hasattr(SA, "SELL_CADENCE_QUOTA_SCALE"), (
        "cadence must not scale the quota; that is the day-total cap that lost $2,653")


def _sell_hours(flag_on, days=6):
    """Hours on which the live agent actually emits a SELL, read off the action stream.

    Offers, not fills -- deliberately, and this is the one place it is correct. The question here is
    "on which turns did the agent SPEAK", which is exactly what the order list records; fills would
    also depend on the book. `feedback_offers_are_not_fills` forbids summing `o[2]` as a volume, and
    nothing is summed here.
    """
    import json
    import pathlib

    from kaggle_environments import make

    sched = {int(k): v for k, v in json.loads(
        pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json").read_text()).items()}
    thin = {d: {k: v for k, v in r.items()
                if k not in ("plant_tiles", "build_tiles", "land_turns", "orders")}
            for d, r in sched.items()}

    SA.SELL_ON_DRAIN_CADENCE = flag_on
    agent = SA.make_agent(thin, 0, router=True)
    env = make("kaggriculture", configuration={"seed": 11}, debug=False)
    env.reset(2)

    hours = set()
    for t in range(24 * days):
        if env.done:
            break
        o0 = env.state[0].observation
        a0 = agent(o0)
        if any(o and o[0] == "SELL" for o in (a0.get("market") or [])):
            hours.add(t % 24)
        n0 = len(o0["farms"][0].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
    return hours


@pytest.mark.slow
def test_the_predicate_is_actually_wired_into_the_emission_site():
    """The hole the revert check found: every test above passes with the emission-site line backed
    out, because they all test `sell_hour_is_open` and none tests that anything CALLS it.

    A green suite after a fix says the fix broke nothing, not that anything checks it -- and this
    project has now been bitten by that three times (CLAUDE.md, 'a gate only tests what it
    exercises'). So this drives the real agent and reads which hours it speaks on.
    """
    off = _sell_hours(False)
    assert off - {0, 4, 8, 12, 16, 20}, (
        "with the flag OFF the agent already sells only on cadence hours, so this test cannot "
        "discriminate and proves nothing")

    on = _sell_hours(True)
    assert on, "with the flag ON the agent never sold at all -- the quota is being destroyed"
    assert on <= {0, 4, 8, 12, 16, 20}, (
        f"the predicate is not wired in: SELLs emitted on hours {sorted(on - {0, 4, 8, 12, 16, 20})}")
