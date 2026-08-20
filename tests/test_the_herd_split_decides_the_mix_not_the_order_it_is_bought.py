"""`_herd_split` re-labels the SPECIES of the herd. It must not re-order the days it is bought on.

The schedule already contains Kawashigi's animal-buy algorithm exactly -- `animals_bought` reads
`d0 COW2 SHEEP2, d3 COW1, d5 COW1, d7 COW2 SHEEP1, d8 SHEEP1, d9 COW2, d11 COW2`, which is his
recorded order stream op for op, COW 10 / SHEEP 4. Then `_place_animals` overwrites it:

    if SHOP_ADAPT_HERD and day >= SHOP_ADAPT_FROM_DAY:
        _s = _herd_split(want_total, state["bought"], ...)
        want_total["COW"], want_total["SHEEP"] = _s["COW"], _s["SHEEP"]

`want_total` at that point is the schedule accumulated through **today**, not over the season, so
`_herd_split` is asked to divide a partial herd. Its greedy fills the species with the most headroom
first, and on a board with no early YARN_STORE `WOOL_SHOP_SETS_THE_HERD` pins COW to
`WOOL_SHOP_NO_YARN_COW = 10` and gives sheep only the remainder -- so every cow of the season is
bought before the first floating sheep. A schedule that interleaves the two species cannot survive
that, and this one does.

Measured on the kawashigi board, seed 11, FILLS not offers. Cumulative bought at each day's dusk:

           ours          his tape
    d5     C4 / S2       C4 / S2      identical to here
    d7     C6 / S2       C6 / S3      his d7 row is COW 2 + SHEEP 1; we buy the cows only
    d8     C8 / S2       C6 / S4      his d8 row is SHEEP 1; we buy two more cows
    d9     C10 / S2      C8 / S4
    d11    C10 / S4      C10 / S4     the totals reconcile, four days late

The season MIX is not in dispute -- the split picks COW 10 / SHEEP 4 on this board, which is his
mix. Only the order is wrong, and the order is what the sells depend on: two sheep that arrive on
d11 instead of d7 and d8 are two sheep that shear nothing into the d8-d10 wool rows.

The assertion is on the mix bought by the end of d8, because that is where his schedule has asked
for both extra sheep and the greedy has spent the budget on cows instead. It is deliberately NOT an
assertion that `SHOP_ADAPT_HERD` is off: on a board whose shops say all-cow the split should still
say all-cow. It must say it about the season, once, and then let the schedule's rows say when.
"""
import collections
import importlib

import pytest

import kagg.plan as _PLAN

SEED = 11
DAY = 8


@pytest.fixture(scope="module")
def herd():
    """Cumulative BUY_ANIMAL FILLS for our seat at each day's dusk, plus the board's season split."""
    import scripts.breakdown as B
    from kagg.analysis.fills import record_fills
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)
    shops = B.recorded_shops(replay)

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2)
    ours = SA.make_agent(sched, 0, router=True)
    opp = B.tape_policy(replay, team, 1)

    dusk, unlocked = {}, ()
    with record_fills(env) as fills:
        for t in range((DAY + 1) * 24):
            o0, o1 = env.state[0].observation, env.state[1].observation
            unlocked = list(shops(t))
            o0.town["unlocked_shops"] = unlocked
            a0, a1 = ours(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if t % 24 == 23:
                dusk[t // 24] = {a: fills.units(0, "BUY_ANIMAL", a) for a in ("COW", "SHEEP")}

    season = collections.Counter()
    for dd in sched:
        for a, q in (sched[dd].get("animals_bought") or {}).items():
            season[a] += int(q)
    split = SA._herd_split(season, collections.Counter(), DAY, 0, unlocked, 29)
    return dusk, season, split


def _scheduled_through(day):
    sched = _PLAN.load("data/seed_scripts/kawashigi/schedule.json")
    want = collections.Counter()
    for dd in sched:
        if int(dd) <= day:
            for a, q in (sched[dd].get("animals_bought") or {}).items():
                want[a] += int(q)
    return want


def test_the_premise_the_schedule_interleaves_the_two_species(herd):
    """Guard. The override can only reorder a sheep it can reach: one rowed on or after
    `SHOP_ADAPT_FROM_DAY`, with a cow rowed after it. Both hold here -- d7 `COW2 SHEEP1` and d8
    `SHEEP1` sit in front of d9 `COW2` and d11 `COW2`."""
    SA = importlib.import_module("kagg.search.schedule_agent")
    sched = _PLAN.load("data/seed_scripts/kawashigi/schedule.json")
    rows = {int(dd): (sched[dd].get("animals_bought") or {}) for dd in sched}
    sheep = [d for d, r in rows.items() if int(r.get("SHEEP", 0) or 0) > 0]
    cows = [d for d, r in rows.items() if int(r.get("COW", 0) or 0) > 0]
    assert [d for d in sheep if SA.SHOP_ADAPT_FROM_DAY <= d <= DAY], (
        f"no SHEEP is rowed between d{SA.SHOP_ADAPT_FROM_DAY} and d{DAY} (sheep on {sorted(sheep)}) "
        "-- the override cannot reach one, and this test is measuring nothing")
    assert [d for d in cows if d > max(sheep)], (
        f"every COW row (on {sorted(cows)}) precedes the last SHEEP row -- the greedy's cows-first "
        "fill would agree with the schedule and this test is measuring nothing")


def test_the_premise_the_board_does_not_itself_ask_for_a_different_mix(herd):
    """Guard. If the shops genuinely say all-cow, re-labelling the sheep away is correct.

    It does not. YARN_STORE lands on this board at d12 -- the fourth draw, outside
    `WOOL_SHOP_DRAW_LIMIT` -- and the split still returns the schedule's own COW 10 / SHEEP 4,
    because `WOOL_SHOP_NO_YARN_COW` is 10 and the herd is 14. So the season mix is not what moved.
    """
    _, season, split = herd
    assert (split["COW"], split["SHEEP"]) == (season["COW"], season["SHEEP"]), (
        f"the board's season split is {dict(split)} against a schedule of {dict(season)} -- the mix "
        "itself is in dispute here, so a day-8 ordering assertion would be testing the wrong thing")


def test_the_days_the_schedule_buys_a_sheep_on_buy_a_sheep(herd):
    dusk, _, _ = herd
    want = _scheduled_through(DAY)
    got = dusk[DAY]
    assert got["SHEEP"] >= want["SHEEP"], (
        f"through d{DAY} the schedule asks for COW {want['COW']} / SHEEP {want['SHEEP']} -- his own "
        f"recorded rows -- and we bought COW {got['COW']} / SHEEP {got['SHEEP']}. `_herd_split` was "
        "handed the herd accumulated through TODAY instead of over the season, so its greedy spent "
        "the day's budget filling cows to the no-yarn cap and deferred every floating sheep to the "
        "end of the herd. The season mix it picks is right; the order it imposes is not the "
        "schedule's.")
