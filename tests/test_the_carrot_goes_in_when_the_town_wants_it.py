"""d25-d27 sow CARROT instead of WHEAT, but only where the town will absorb it.

**Why a condition and not a swap.** Unconditionally the same edit is **-$237** over 48 towns: the
towns that cannot take the carrot cancel the towns that can. Cut by the town's carrot drain -- the
units its unlocked shops pull per tick -- the picture is monotone and large. Measured 2026-08-22,
12,096 paired seasons, `control` against `cond_carrot_d4`
(`docs/carrot_refine_2026-08-22.md`):

    drain   n     control   cond    delta
        0   126     73.0    73.0    +0.0     rule never fires
        3   105     61.0    61.0    +0.0     rule never fires
        4    84     42.9    44.0    +1.2     fires, and is a WASH
        5   231     42.0    51.1    +9.1
        6   147     57.8    71.4   +13.6
        7    63     46.0    66.7   +20.6

Hence `CARROT_DRAIN_MIN = 5`, not the 4 that `tape_edit.carrot_when_it_pays` defaults to: drain 4
buys nothing and exposes 84 seasons of variance for +1.2 points.

**The mechanism is our own book, not the opponent's.** We already grow and sell carrot, so this is
incremental supply. Adding it where the town cannot drain it floods our own market -- the failure
already recorded for milk, where 159 units cleared at $1-$5 because cow COUNT was causal. `drain` is
precisely the town's absorption rate, which is why it is the condition that matters.

`CARROT_OPP_MAX` is kept as cheap insurance on a thin tail. Measured over 85 downloaded games and
170 player-seats, 94% hold zero carrot at day 25 and 85% never plant one all season, so it almost
never binds -- which is exactly what the sweep saw when `o3`, `o7` and `o99` came out byte-identical.
But `carrot_when_it_pays`'s own prior measured the `opp CA 15+` bucket at -$510 / 28% improved, and
1-2% of seats reach it. A guard that costs nothing and covers a real tail stays.

**Decided ONCE, on the first turn of day 25**, not re-evaluated per turn. By d25 the town has drawn
all eight shops and the opponent's carrot is long since standing, so nothing is being guessed at,
and a decision that can flip mid-window would sow half a field of each.
"""

import pytest

from kagg.search import schedule_agent as SA


def obs_with(shops, day=25, hour=0, opp_carrot=0, me=0):
    """Minimal observation: unlocked shops, and the opponent's standing carrot."""
    tiles = [[None] * 10 for _ in range(10)]
    placed = 0
    for r in range(10):
        for c in range(10):
            if placed < opp_carrot:
                tiles[r][c] = {"crop": "CARROT"}
                placed += 1
    farms = [{"tiles": [[None] * 10 for _ in range(10)]}, {"tiles": [[None] * 10 for _ in range(10)]}]
    farms[1 - me] = {"tiles": tiles}
    return {"day": day, "hour": hour, "player": me, "farms": farms,
            "town": {"unlocked_shops": list(shops)}}


def drain_of(shops):
    return SA._carrot_town_drain(obs_with(shops))


#: Shop names that buy CARROT, read from the environment rather than hard-coded.
def carrot_shops():
    kg = SA._KG
    if kg is None:
        pytest.skip("the kaggriculture module is not importable")
    return [n for n, prods in kg.SHOPS.items() if "CARROT" in (prods or [])]


def shops_reaching(target):
    """Fewest unlock SLOTS whose carrot drain totals at least `target`.

    **Slots repeat, and that is the whole reason drain can exceed 3.** Only two of the eight shops
    buy carrot -- `PET_CAFE` (carrot only, so it counts double) and `FARMERS_MARKET` (four products,
    counts once) -- so the distinct-name maximum is 3. The town draws its eight unlocks WITH
    REPLACEMENT, one per unlock day, so a town can hold `PET_CAFE` three times and reach drain 7.
    That is what the measured 0-7 distribution across 48 towns is made of, and an earlier version of
    this helper tried each name once, could never pass 3, and skipped the two tests that matter.
    """
    names, got = [], 0
    while got < target:
        if len(names) > 16:                       # more slots than a season has unlock days
            pytest.skip("no draw of shops reaches drain %d" % target)
        names.append(carrot_shops()[0])
        got = drain_of(names)
    return names


def test_the_drain_counts_a_carrot_only_shop_double():
    """Mirrors `_town_consume`: a shop pulls 1 per product, or 2 if it sells only one."""
    kg = SA._KG
    if kg is None:
        pytest.skip("the kaggriculture module is not importable")
    solo = [n for n in carrot_shops() if len(kg.SHOPS[n]) == 1]
    multi = [n for n in carrot_shops() if len(kg.SHOPS[n]) > 1]
    if not solo or not multi:
        pytest.skip("need one carrot-only shop and one multi-product carrot shop")
    assert drain_of(solo[:1]) == 2
    assert drain_of(multi[:1]) == 1


def test_a_shop_that_does_not_buy_carrot_adds_nothing():
    kg = SA._KG
    if kg is None:
        pytest.skip("the kaggriculture module is not importable")
    other = [n for n, p in kg.SHOPS.items() if "CARROT" not in (p or [])]
    if not other:
        pytest.skip("every shop buys carrot")
    assert drain_of(other) == 0


def test_the_rule_fires_at_the_measured_threshold_and_not_below():
    """drain 4 measured +1.2 and drain 5 measured +9.1. The line goes between them."""
    assert SA.CARROT_DRAIN_MIN == 5, (
        "the threshold is 5 by measurement, not the 4 that tape_edit defaults to; "
        "see docs/carrot_refine_2026-08-22.md")
    low = obs_with(shops_reaching(SA.CARROT_DRAIN_MIN - 1))
    assert SA._carrot_town_drain(low) < SA.CARROT_DRAIN_MIN
    assert not SA._carrot_pays(low), "fired on a town below the measured threshold"

    high = obs_with(shops_reaching(SA.CARROT_DRAIN_MIN))
    assert SA._carrot_town_drain(high) >= SA.CARROT_DRAIN_MIN
    assert SA._carrot_pays(high), "did not fire on a town at the measured threshold"


def test_a_carrot_heavy_opponent_calls_it_off():
    """The thin tail: `opp CA 15+` measured -$510. Rare, and still worth refusing."""
    shops = shops_reaching(SA.CARROT_DRAIN_MIN)
    assert SA._carrot_pays(obs_with(shops, opp_carrot=SA.CARROT_OPP_MAX))
    assert not SA._carrot_pays(obs_with(shops, opp_carrot=SA.CARROT_OPP_MAX + 1))


def test_the_opponent_is_read_from_the_other_seat():
    """Our own carrot must not veto our own rule. Seat 1 reads seat 0, and vice versa."""
    shops = shops_reaching(SA.CARROT_DRAIN_MIN)
    many = SA.CARROT_OPP_MAX + 5
    for me in (0, 1):
        o = obs_with(shops, opp_carrot=many, me=me)
        assert not SA._carrot_pays(o), "seat %d failed to see the opponent's carrot" % me
        ours = dict(o)
        ours["farms"] = list(o["farms"])
        ours["farms"][me], ours["farms"][1 - me] = o["farms"][1 - me], o["farms"][me]
        assert SA._carrot_pays(ours), (
            "seat %d counted its OWN carrot as the opponent's and vetoed itself" % me)


def test_the_swap_rewrites_the_plants_and_the_seed_row_together():
    """Both halves, or the day buys wheat it will never sow."""
    acts = [["PLANT", "WHEAT"], ["WATER"], ["PLANT", "MELON"], ["PLANT", "WHEAT"]]
    orders = [["BUY_SEED", "WHEAT", 6], ["SELL", "MILK", 3], ["BUY_SEED", "MELON", 2]]
    acts, orders = SA._sow_carrot_instead(acts, orders)
    assert [a[1] for a in acts if a[0] == "PLANT"] == ["CARROT", "MELON", "CARROT"]
    assert ["BUY_SEED", "CARROT", 6] in orders
    assert ["BUY_SEED", "MELON", 2] in orders, "an unrelated seed row must not move"
    assert ["SELL", "MILK", 3] in orders, "an unrelated order must not move"


def test_the_seed_row_is_repointed_even_on_a_turn_that_plants_nothing():
    """He buys seed on turns with no planting. Gating the rewrite on a plant leaves wheat bought."""
    acts = [["WATER"], ["HARVEST"]]
    _acts, orders = SA._sow_carrot_instead(acts, orders=[["BUY_SEED", "WHEAT", 11]])
    assert orders == [["BUY_SEED", "CARROT", 11]]


def test_the_window_is_the_three_days_that_were_measured():
    assert tuple(sorted(SA.CARROT_SWAP_DAYS)) == (25, 26, 27)


# ---- the call site ---------------------------------------------------------------------------
#
# Everything above tests the FUNCTIONS. The agent could define all of them, never call one, and
# every assertion above would still pass -- "a gate only tests what it exercises", which this
# project's CLAUDE.md records as having cost time three times. These two run the real agent for a
# real season and read what it emits, with the DECISION stubbed so the wiring is isolated from
# whether a particular town draw happens to qualify.

import json                                                                    # noqa: E402
import pathlib                                                                 # noqa: E402
import sys                                                                     # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

SEED = 11


def plants_in_the_window(decision):
    """Run one season to the end of the window; return every PLANT crop emitted inside it."""
    B = pytest.importorskip("breakdown")

    replay, schedule, team = B.TAPES["kawashigi"]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA

    seen = []
    plain = SA._carrot_pays
    SA._carrot_pays = lambda obs, me=0: decision
    try:
        def ours():
            a = SA.make_agent(sched, 0)

            def wrapped(o, _t=None):
                act = a(o)
                if int(o.get("day", 0) or 0) in SA.CARROT_SWAP_DAYS:
                    for u in [act.get("farmer")] + list(act.get("hands") or []):
                        if u and u[0] == "PLANT" and len(u) > 1:
                            seen.append(u[1])
                return act
            return wrapped

        opp = lambda: B.tape_policy(str(REPO / replay), team, 1)          # noqa: E731
        B.run(ours, opp, SEED, 0.0, stop_day=max(SA.CARROT_SWAP_DAYS) + 1)
    finally:
        SA._carrot_pays = plain
    return seen


@pytest.fixture(scope="module")
def window():
    return {"on": plants_in_the_window(True), "off": plants_in_the_window(False)}


def test_the_agent_actually_sows_the_carrot(window):
    """The wiring. Without the call at the boundary every unit test above still passes.

    **Asserted as a DIFFERENCE, not as presence.** An earlier version of this test asserted
    `"CARROT" in window["on"]` and stayed green with the wrapper unhooked, because the agent already
    grows carrot of its own accord -- so the assertion was true whatever the rule did. A test that
    passes when the feature is absent is worse than no test.
    """
    assert window["off"], (
        "the agent planted nothing at all in d25-27, so this test cannot see the swap "
        "and would be green by construction")
    assert "WHEAT" in window["off"], (
        "no wheat is planned in the window on this seed, so there is nothing for the rule to "
        "swap and the comparison is vacuous")
    assert window["on"].count("CARROT") > window["off"].count("CARROT"), (
        "the decision said yes and the carrot count did not move: %d with the rule on against %d "
        "with it off. `_sow_carrot_instead` is defined but is not reached -- note `replayed` "
        "discards `agent`'s answer for any step the tape covers."
        % (window["on"].count("CARROT"), window["off"].count("CARROT")))


def test_the_inlined_rule_plays_exactly_what_the_measured_wrapper_plays():
    """Equivalence with `tape_edit.carrot_when_it_pays`, which is what the 12,096 seasons measured.

    **This is the only claim the shipped code can make.** The sweep measured a WRAPPER applied from
    outside the agent. Inlining it changes where the rule lives, not what it does -- so the thing to
    verify is that the two emit the same actions, not that the inlined one banks well on a handful
    of fresh seeds. A bank comparison over a few seasons is inside seed variance (~15%) and could
    not distinguish "equivalent" from "subtly different" anyway.

    Turn-for-turn, whole window, one season. Anything less is a shorter test, not a weaker one.
    """
    B = pytest.importorskip("breakdown")
    E = pytest.importorskip("kagg.search.tape_edit")

    replay, schedule, team = B.TAPES["kawashigi"]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    B.schedule_agent = SA

    def season(inlined):
        seen = []
        days = SA.CARROT_SWAP_DAYS
        # Disabling the inlined rule by emptying its day window is the honest way to get a
        # "wrapper only" arm: it leaves every other code path identical.
        SA.CARROT_SWAP_DAYS = days if inlined else ()
        try:
            def ours():
                a = SA.make_agent(sched, 0)
                if not inlined:
                    a = E.carrot_when_it_pays(a, SA.CARROT_DRAIN_MIN, SA.CARROT_OPP_MAX,
                                              days=days)

                def wrapped(o, _t=None):
                    act = a(o)
                    if int(o.get("day", 0) or 0) in days:
                        seen.append((int(o.get("step", 0) or 0),
                                     [list(u) for u in [act.get("farmer")] + list(act.get("hands") or [])],
                                     [list(m) for m in (act.get("market") or [])]))
                    return act
                return wrapped

            opp = lambda: B.tape_policy(str(REPO / replay), team, 1)       # noqa: E731
            B.run(ours, opp, SEED, 0.0, stop_day=max(days) + 1)
        finally:
            SA.CARROT_SWAP_DAYS = days
        return seen

    mine, theirs = season(True), season(False)
    assert mine and theirs, "neither arm reached the window"
    assert len(mine) == len(theirs), "the two arms played a different number of turns"
    bad = [(s, a, b) for (s, a, _), (_, b, _) in zip(mine, theirs) if a != b]
    assert not bad, "%d of %d turns differ in unit actions, first at step %d:\n  inlined %r\n  wrapper %r" % (
        len(bad), len(mine), bad[0][0], bad[0][1][:4], bad[0][2][:4])
    bad_m = [(s, a, b) for (s, _, a), (_, _, b) in zip(mine, theirs) if a != b]
    assert not bad_m, "%d of %d turns differ in MARKET orders, first at step %d:\n  inlined %r\n  wrapper %r" % (
        len(bad_m), len(mine), bad_m[0][0], bad_m[0][1], bad_m[0][2])


def test_the_wheat_that_was_planned_is_what_became_carrot(window):
    """Conservation. The swap must move wheat to carrot, not invent or destroy plantings."""
    on, off = window["on"], window["off"]
    assert len(on) == len(off), "the swap changed how MANY tiles are planted, not just what"
    assert on.count("WHEAT") == 0, "wheat left in the window while the rule was on"
    assert on.count("CARROT") == off.count("CARROT") + off.count("WHEAT")
    for crop in set(off) - {"WHEAT", "CARROT"}:
        assert on.count(crop) == off.count(crop), "%s was disturbed by the carrot swap" % crop
