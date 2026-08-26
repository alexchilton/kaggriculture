"""`LATE_SELL_BIAS` must not hold the offer back when the shed has no room left.

`schedule_agent.py:4626` zeroes the offer for every product on every turn before
`LATE_SELL_FROM_HOUR = 16`:

    if (LATE_SELL_BIAS and hour < LATE_SELL_FROM_HOUR and not last_day_liquidating
            and not unfunded
            and not (prod in NO_DRAIN_PRODUCTS and ...)):
        n = 0

It has two escapes and neither one is about storage. `last_day_liquidating` is day 29.
`unfunded` is `(money + pending) < _days_bill(row)` (`:4295`) -- the bank cannot pay today's
wages -- and in the solver zone the bank is six figures, so it never fires.

The reason the gate exists is sound: shops drain inventory every 4 steps and the town centre
every 12 (`reference/kaggriculture.py:706-716`), so a price that collapsed this morning has
recovered by evening, and selling late fetches more per unit. That reasoning is about PRICE.
It assumes the goods are still there to sell at h16.

They are not always. `shedCapacity` is 100 (`:553`) and it is a hard ceiling.
`_drop_inventories_to_shed` runs at every dawn (`:878`) and its own docstring says
"overflow is discarded", and HARVEST puts yield in the unit's own inventory (`:466`) where a
SELL cannot reach it. So a shed sitting at the cap from dawn to h16 is not holding for a better
price; it is destroying the crew's carry every dawn and blocking every harvest in between.

Measured on the strawberry arm's own seed, d12-d23, before this test existed:

    d   h  shed  WHEAT  price   SELL orders emitted
   19   2   100     47     46   []
   19   3    97     46     46   []
    ... fourteen consecutive hours, shed 96-100, nothing offered ...
   19  16    96     45     47   [['SELL','STRAWBERRY',26], ['SELL','WOOL',12], ...]

Wheat quoted $44-47 the whole morning, so no price floor was binding, and the feed reserve is
`feed_days(day) * animals` = ~14 units against 59 held. The gate is the whole of it.

The rule this pins: **when the shed is at or above `SHED_TARGET`, the hour gate does not apply.**
Holding is free only while there is somewhere to hold.
"""

import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
#: The strawberry tape and its OWN seed. The replay is exact only on this one.
STRAW_SEED = 468411728
STRAW_TAPE = "data/seed_scripts/kawa_2026-08-24/97466318.json"
SOLVER = range(12, 24)


def play_and_record_the_offers(seed=STRAW_SEED, tape=STRAW_TAPE):
    """Our agent against the tape's actions. Returns (day, hour, shed_total, n_sell_orders)."""
    import breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawa_straw/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    rec = json.loads((REPO / tape).read_text())
    steps = rec["steps"]
    names = (rec.get("info") or {}).get("TeamNames") or []
    his = names.index("カワシギ") if "カワシギ" in names else 0

    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, 0)

    rows = []
    for t in range(30 * TPD):
        o = env.state[0].observation
        shed = (o.get("private") or {}).get("shed") or {}
        total = sum(int(v or 0) for v in shed.values())
        n = len(o["farms"][0].get("hands") or [])
        a = agent(o)
        sells = [od for od in (a.get("market") or []) if od and od[0] == "SELL"]
        rows.append((t // TPD, t % TPD, total, len(sells)))
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n], "market": a["market"]}
        at = steps[t + 1][his].get("action") if t + 1 < len(steps) else None
        at = at if isinstance(at, dict) else {}
        n2 = len(o["farms"][1].get("hands") or [])
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n2],
                 "market": at.get("market") or []}
        env.step([mine, yours])
        if env.done:
            break
    return rows


def test_a_pressed_shed_offers_before_the_late_sell_hour():
    """Every solver-zone turn with the shed at SHED_TARGET or above must offer something."""
    SA = importlib.import_module("kagg.search.schedule_agent")
    rows = play_and_record_the_offers()

    mute = [(d, h, tot) for d, h, tot, sells in rows
            if d in SOLVER and h < SA.LATE_SELL_FROM_HOUR
            and tot >= SA.SHED_TARGET and sells == 0]

    by_day = {}
    for d, _h, _t in mute:
        by_day[d] = by_day.get(d, 0) + 1

    assert not mute, (
        f"{len(mute)} turns in d12-d23 hold the shed at {SA.SHED_TARGET}+ of "
        f"{SA.SHED_CAPACITY} before hour {SA.LATE_SELL_FROM_HOUR} and offer NOTHING. "
        f"Every dawn in that state discards what the crew carries and every harvest after it "
        f"has nowhere to land, so the better evening price the gate is waiting for is bought "
        f"with goods that no longer exist. Mute turns by day: {dict(sorted(by_day.items()))}. "
        f"First ten (day, hour, shed): {mute[:10]}")
