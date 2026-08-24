"""A day whose row asks for no wheat must not buy wheat.

Measured 2026-08-24 across all 35 kawashigi replays, each on its own seed against its own recorded
opponent. At d3 h0 our bank and shed match his EXACTLY in all 35. By d4 h0 they do not, and d3's
order tally is identical in every game:

    d3 orders          his   ours
      BUY_ANIMAL COW     1     1
      HIRE               5     5
      BUY_SEED CARROT    1     1
      SELL FERTILIZER    4     7
      BUY_PRODUCT WHEAT  0     4     <-- the row asks for none

    d4 dawn FERTILIZER gap ours-his:  -3 in all 35
    d4 dawn bank gap ours-his:        +$161 to +$188

The schedule row for d3 is `buys {}`. `schedule_agent.py:5320` bounds the dusk top-up to the row
only when the row has one:

    row_buys = int((row.get("buys") or {}).get("WHEAT", 0) or 0)
    if row_buys > 0:
        gap = min(gap, row_buys - int(state["ordered"][("buys", "WHEAT")]))

and its own comment states the consequence -- *"A day with no `buys` row keeps the top-up unbounded:
there the formula is the only rule there is."* d0, d1, d2 and d4 all carry a row (WHEAT 6, 5, 4, 6),
which is why only d3 leaks inside the opening.

He buys no wheat at any hour of d3 and sells FERTILIZER 4 the next day, so the stock is meant to be
held overnight. Five days in the schedule have no `buys.WHEAT` row: d3, d15, d16, d20, d29.
"""

import collections
import glob
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
WHO = "カワシギ"
TPD = 24
DAY = 3


def _game():
    for d in ("kawashigi", "kawa_2026-08-24", "kawashigi_b3", "top_guys"):
        for p in sorted(glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json"))):
            try:
                rec = json.loads(pathlib.Path(p).read_text())
            except Exception:                                                 # noqa: BLE001
                continue
            if not isinstance(rec, dict) or "steps" not in rec:
                continue
            names = (rec.get("info") or {}).get("TeamNames") or []
            if WHO in names and (rec.get("info") or {}).get("seed") is not None:
                return rec, names.index(WHO), rec["info"]["seed"], pathlib.Path(p).stem
    return None, None, None, None


def _day_three_orders():
    sys.path.insert(0, str(REPO))
    sys.path.insert(0, str(REPO / "scripts"))
    from kaggle_environments import make
    import breakdown as B
    import us_in_his_seat as U
    from kagg.search import schedule_agent as SA

    rec, seat, seed, ep = _game()
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    steps = rec["steps"]
    them = 1 - seat
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, seat)

    ours = collections.Counter()
    for t in range((DAY + 1) * TPD):
        o = env.state[seat].observation
        n_us = len(o["farms"][seat].get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])
        a = agent(o)
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                "market": a["market"]}
        if t // TPD == DAY:
            for order in (mine["market"] or []):
                if order and order[0] == "BUY_PRODUCT" and len(order) >= 3:
                    ours[order[1]] += int(order[2])
        at = U._recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        env.step([mine, yours] if seat == 0 else [yours, mine])
        if env.done:
            break
    return ours, sched, ep


@pytest.mark.skipif(_game()[0] is None, reason="no kawashigi replay on disk")
def test_a_day_with_no_buys_row_buys_nothing():
    """d3's row is `buys {}`. The day must not buy wheat."""
    ours, sched, ep = _day_three_orders()
    row_buys = int((sched[DAY].get("buys") or {}).get("WHEAT", 0) or 0)
    assert row_buys == 0, "this test assumes d3's row asks for no wheat"
    assert ours["WHEAT"] == 0, (
        f"{ep}: d3's row is `buys {{}}` and he buys no wheat all day, but we ordered "
        f"BUY_PRODUCT WHEAT {ours['WHEAT']} -- the dusk top-up is unbounded on a day with no row "
        f"(schedule_agent.py:5320)"
    )
