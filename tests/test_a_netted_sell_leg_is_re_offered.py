"""A sell the netting cancels is a sell the day still owes.

`NET_THE_TWO_LEGS` deletes the round trip when a turn both sells and buys the same product. It was
written for Seb's day 4, where the two legs were an accident -- the sell guard nets wheat carried in
hands, the dusk top-up counts the shed alone, so the sell emptied the shed and the top-up refilled
it in the same turn, nine times over d0-d16.

Victor's day 5 is not that. His row is `sells {WHEAT: 17, FERTILIZER: 5}` against `buys {WHEAT: 7}`,
and his own orders show the shape: `[0, SELL, WHEAT, 17]` in one lump at dawn, then `BUY_PRODUCT
WHEAT 1` at h1, h4, h5, h9, h11, h14 and h18. He dumps the harvest while the book is deep and buys
the herd's ration back a unit at a time. Both legs are deliberate.

We queue the whole day's buying at h0 beside the bulk sell, so the netting sees a 17/7 overlap and
cancels 7 of each. That alone would be survivable -- `CUMULATIVE_SELLS` re-offers a row that did not
fill. It is not survivable because the counter is asymmetric: `state["ordered"][("sold", prod)]` is
credited with the full 17 when the order is queued, and the netting below shrinks the order to 10
without giving any of it back. The buy side gives its counter back explicitly, two lines later. So
the day has offered 10, banked 10, and believes it has met a row of 17, and no later hour re-offers:
`sell 15/22` on d5, and every wheat sale for the rest of the day is suppressed.

The assertion is on FILLS, per product, for the day: the row asks for 17 wheat and the shed holds 23
at dawn, so 17 must actually trade. It says nothing about which hour they trade in -- bunching is
tour shape, and the netting itself is free to keep cancelling.
"""
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

SEED = 11
DAY = 5
TPD = 24


def _sold_on_day(day):
    """`(Counter of units SOLD that day, Counter of stock held at that dawn)` for our seat."""
    import breakdown as B
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    import kagg.search.schedule_agent_1455mh as sa

    replay, schedule, team = B.TAPES["victor"]
    sched = {int(k): v for k, v in json.loads((REPO / schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    cfg = dict(B.env_config(REPO / replay), seed=SEED, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    at_dawn, before, after = None, collections.Counter(), collections.Counter()
    with record_fills(env) as fills:
        for t in range(TPD * (day + 1)):
            o0, o1 = env.state[0].observation, env.state[1].observation
            if t == TPD * day:
                at_dawn = collections.Counter(o0["private"].get("shed") or {})
                before = collections.Counter(
                    {p: fills.units(0, "SELL", p) for p in fills.products()})
            a0, a1 = agent(o0), tape(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
        after = collections.Counter({p: fills.units(0, "SELL", p) for p in fills.products()})
    return after - before, at_dawn


def test_the_premise_day_5_sells_and_buys_the_same_product():
    """Guard. Without an overlap on the day the netting never fires and this proves nothing."""
    raw = json.loads((REPO / "data/seed_scripts/victor/schedule.json").read_text())
    row = raw[str(DAY)]
    overlap = set(row.get("sells") or {}) & set(row.get("buys") or {})
    assert overlap, f"d{DAY} row sells {row.get('sells')} and buys {row.get('buys')}; no overlap"


def test_the_days_wheat_row_is_sold_in_full():
    sold, at_dawn = _sold_on_day(DAY)
    raw = json.loads((REPO / "data/seed_scripts/victor/schedule.json").read_text())
    want = int((raw[str(DAY)].get("sells") or {}).get("WHEAT", 0))
    held = int(at_dawn.get("WHEAT", 0))
    assert held >= want, (
        f"premise broken: d{DAY} dawn shed holds WHEAT {held} against a row of {want}; "
        f"this is a stock problem, not a netting one")
    assert int(sold.get("WHEAT", 0)) == want, (
        f"d{DAY} row sells WHEAT {want} off a dawn shed of {held}, "
        f"but only {int(sold.get('WHEAT', 0))} traded")
