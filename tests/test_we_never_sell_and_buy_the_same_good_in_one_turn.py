"""Selling wheat and buying wheat in the same turn pays the spread twice for nothing.

**Two reserves, one floor, two bases.** Both the sell guard and the dusk top-up protect the same
quantity -- `feed_days(day) * alive`, which is 7 on day 4 -- and they compute the shortfall from
different stock:

    sell guard   `have -= max(0, feed_days(day) * alive - carried_wheat - drawn - will_buy)`
                 (`schedule_agent_1455mh.py:2932`) -- nets off the 28 wheat in hands, so the
                 reserve is 0 and the whole shed is offered
    top-up       `gap = (alive + arriving) - shed["WHEAT"]` (`:3628`) -- shed only, so an empty
                 shed reads as a 7-unit shortfall and buys the cap

So from `DUSK_FEED_HOUR` the day sells the shed bare and immediately buys it back. Day 4, seed 11,
tape 91422988:

    h18                            BUY_PRODUCT WHEAT 6
    h19  SELL WHEAT 6,             BUY_PRODUCT WHEAT 1
    h21                            BUY_PRODUCT WHEAT 6
    h22  SELL WHEAT 6,             BUY_PRODUCT WHEAT 1
    h23  SELL WHEAT 1,             BUY_PRODUCT WHEAT 6

`buy_product 21/1` against a tape that buys ONE wheat all day, and `sell 41/55`. The tape's day is
four clean DROP waves into four sells -- 5, 12, 12, 20 -- and one purchase.

**The rule, not the day.** Stated as an invariant over every turn of d0-d16 and every product,
because it is one whichever side is eventually made to yield: a turn that both sells and buys the
same good has already lost the spread, and no reserve arithmetic can be right and do that at once.

Found by Fable, 2026-08-10; `docs/fable_matching_the_tape_2026-08-10.md` has the full trace.
"""
import importlib
import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/91422988.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
SEED = 11
DAYS = 17
MODULE = "kagg.search.schedule_agent_1455mh"


def _thin():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): {k2: v2 for k2, v2 in r.items() if k2 not in TAPE_ONLY}
            for k, r in raw.items()}


def _opponent():
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    return [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]


def test_no_turn_sells_a_product_it_also_buys():
    from kaggle_environments import make

    SA = importlib.import_module(MODULE)
    opp = _opponent()

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(_thin(), 0, router=True)

    churn = []
    for t in range(24 * DAYS):
        o0 = env.state[0].observation
        a0, a1 = agent(o0), opp[t]
        sold = {o[1] for o in a0["market"] if o and o[0] == "SELL"}
        bought = {o[1] for o in a0["market"] if o and o[0] == "BUY_PRODUCT"}
        both = sold & bought
        if both:
            churn.append(f"    d{t // 24} h{t % 24}  {sorted(both)}  orders {a0['market']}")
        farm = o0["farms"][0]
        n0 = len(farm.get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    assert not churn, (
        f"{len(churn)} turns sold and bought the same good:\n" + "\n".join(churn)
        + "\n  The sell guard nets off wheat carried in hands and the dusk top-up does not, so the "
          "same 7-unit floor is short and satisfied in one turn. Both cannot be right."
    )
