"""Pin the fill instrument against the three proxies that got this wrong.

Each test below corresponds to one historical error, so a regression names the mistake it is
repeating rather than just failing.
"""

import collections
import json
import pathlib

import pytest

from kagg.analysis.fills import record_fills

SCHED = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")

pytestmark = pytest.mark.skipif(not SCHED.exists(), reason="gitignored data")


def _thin():
    sched = {int(k): v for k, v in json.loads(SCHED.read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


TAPE = pathlib.Path("data/seed_scripts/top_guys/90976060.json")


def _play(days):
    """Our agent against **Seb's tape**, with both the fills and the naive proxies recorded.

    The opponent is not a detail. Against a passing opponent the book is uncontested, every offer
    fills, and `offers == fills` to the unit -- so the very error these tests exist to catch cannot
    occur, and they fail declaring themselves unable to discriminate rather than passing vacuously.
    That is CLAUDE.md's "a gate only tests what it exercises": 300 full-length parity episodes once
    passed without both players ever selling the same product.

    `scripts/sell_shape.py` already contests the book this way, which is why its 2.4x fragmentation
    finding is trustworthy and an uncontested measurement of the same thing would not be.
    """
    from kaggle_environments import make

    from kagg.arena.tape import build_tape_agent
    from kagg.search import schedule_agent as SA

    agent = SA.make_agent(_thin(), 0, router=True)
    rival = build_tape_agent(TAPE, 1)
    env = make("kaggriculture", configuration={"seed": 11}, debug=False)
    env.reset(2)

    offered = collections.Counter()
    holdings_drop = collections.Counter()

    def hold(obs):
        p = obs.get("private") or {}
        out = collections.Counter(p.get("shed") or {})
        for inv in (p.get("inventories") or []):
            out.update(inv or {})
        return out

    with record_fills(env) as fills:
        prev = None
        for t in range(24 * days):
            if env.done:
                break
            o0 = env.state[0].observation
            now = hold(o0)
            money = o0["farms"][0]["money"]
            if prev is not None:
                for k in set(now) | set(prev[0]):
                    d = now[k] - prev[0][k]
                    if d < 0 and money > prev[1]:
                        holdings_drop[k] += -d
            prev = (now, money)

            a0 = agent(o0)
            for o in (a0.get("market") or []):
                if o and o[0] == "SELL":
                    offered[o[1]] += int(o[2])
            a1 = rival(env.state[1].observation)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    return fills, offered, holdings_drop


@pytest.mark.slow
def test_offers_are_not_fills():
    """Error 1: summing `o[2]` off the action stream. The quota is re-posted on all 24 turns."""
    fills, offered, _ = _play(days=12)
    sold_units, _rev = fills.sold(player=0)
    total_offered = sum(offered.values())
    assert sold_units > 0, "nothing sold at all; the instrument or the agent is dead"
    assert total_offered > sold_units * 2, (
        f"offers ({total_offered}) barely exceed fills ({sold_units}); this test cannot "
        f"discriminate on this fixture and proves nothing")


@pytest.mark.slow
def test_fed_wheat_is_not_a_wheat_sale():
    """Error 3, the one that invented an $42k wheat round trip.

    FEED consumes wheat from a hand, so "holdings fell while money rose" books every fed unit as a
    sale whenever anything else sold on the same turn. The instrument counts only what
    `_commit_unit` actually traded.
    """
    fills, _offered, holdings_drop = _play(days=12)
    sold_wheat, _rev = fills.sold(player=0, product="WHEAT")
    naive = holdings_drop["WHEAT"]
    assert naive > sold_wheat, (
        f"the naive proxy ({naive}) did not exceed the true fills ({sold_wheat}); either no wheat "
        f"was fed on this fixture or the proxy has been fixed, and this test no longer discriminates")


@pytest.mark.slow
def test_revenue_matches_the_prices_the_units_actually_fetched():
    """A SELL walks the book one unit at a time, so a stack does not clear at the quoted price.
    Summing per-unit prices is the only way to get revenue right."""
    fills, _o, _h = _play(days=12)
    units, revenue = fills.sold(player=0)
    assert units and revenue > 0
    assert revenue / units < 1e6, "implausible mean price; prices are not per unit"


@pytest.mark.slow
def test_every_fill_is_attributed_to_a_seat():
    """The bug that made the first version report zero: `id(farm)` bound once at episode start goes
    stale, because `kaggle_environments` rebuilds `env.state` between steps.

    An unattributed fill is dropped rather than guessed at, so a stale map shows up as a plausible
    small number instead of an error. This asserts the count is exactly zero -- without it, the
    instrument can silently return to being the thing it was written to replace.
    """
    fills, _o, _h = _play(days=12)
    assert fills.unattributed == 0, (
        f"{fills.unattributed} fills could not be attributed to a seat; the farm->seat map is stale")


def test_both_wrappers_are_removed_afterwards():
    """A leaked monkeypatch silently corrupts every later measurement in the same process."""
    import kaggle_environments.envs.kaggriculture.kaggriculture as kg

    commit, market = kg._commit_unit, kg._process_market
    with record_fills():
        assert kg._commit_unit is not commit
        assert kg._process_market is not market
    assert kg._commit_unit is commit, "record_fills leaked its _commit_unit patch"
    assert kg._process_market is market, "record_fills leaked its _process_market patch"


def test_a_failed_commit_is_not_recorded():
    """`_commit_unit` returns False on an empty shed, a short bank or a full shed. Those are
    attempts, not trades -- counting them would reintroduce the offers-are-fills error one level
    down."""
    import kaggle_environments.envs.kaggriculture.kaggriculture as kg

    with record_fills() as fills:
        farm = {"money": 0.0}
        private = {"shed": {"WHEAT": 0}}
        market = {"inventory": {"WHEAT": 100}}
        assert kg._commit_unit("SELL", "WHEAT", 25, farm, private, market) is False
        assert fills.sold(player=0, product="WHEAT") == (0, 0.0)
