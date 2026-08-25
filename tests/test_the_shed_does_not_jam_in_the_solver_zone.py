"""The shed must not sit at its cap in d12-d23 while sellable stock is standing in it.

`shedCapacity` is 100 (`reference/kaggriculture.py:553`) and it is a hard ceiling on everything the
farm holds. `_drop_inventories_to_shed` (`:878`, defined `:843`) runs at every dawn and its own
docstring says what happens when the ceiling is reached:

    Drop every per-farmer inventory into the shed up to `capacity`; overflow is discarded.

So a full shed does two things at once: it destroys whatever the crew is still carrying at dawn, and
it leaves every further HARVEST with nowhere to go, because HARVEST puts yield in the unit's own
inventory (`:466`) and a SELL is refused unless the goods are already in the shed.

Measured 2026-08-25 over 35 of our own ladder games:

    turns OUR shed at 100/100    :   306   (9 a game)
    turns THEIR shed at 100/100  :    91   (3 a game)
    turns ours   >= 90           : 2,505
    turns theirs >= 90           :   488

and on the strawberry arm's own seed, over d12-d23, we harvest 211 times against the tape's 201 and
sell 737 units against its 914. Ten more harvests, 177 fewer units banked.

**Why the solver zone only.** `SELL_SURPLUS_HORIZON`'s release already exists but only binds from
d25, and the `shed_dusk` arm that would reach d12-d24 is deliberately unwired because it regressed
d4 and d5 -- the two days that currently match the tape -- for a cause its author could not find.
d0-d11 is therefore off limits here. The jam we measured is entirely inside d12-d23, so that is the
only window this touches.

This test is about HEADROOM, not about revenue. A shed at the cap is a shed that is destroying
goods, whatever the price column says.
"""

import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
CAP = 100
#: The strawberry tape and its OWN seed. The replay is exact only on this one.
STRAW_SEED = 468411728
STRAW_TAPE = "data/seed_scripts/kawa_2026-08-24/97466318.json"
SOLVER = range(12, 24)


def play_the_solver_zone(seed=STRAW_SEED, tape=STRAW_TAPE):
    """Our agent against the tape's recorded actions. Returns per-turn shed totals for our seat."""
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

    per_turn = []
    for t in range(30 * TPD):
        o = env.state[0].observation
        shed = (o.get("private") or {}).get("shed") or {}
        per_turn.append((t // TPD, sum(int(v or 0) for v in shed.values()), dict(shed)))
        n = len(o["farms"][0].get("hands") or [])
        a = agent(o)
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
    return per_turn


def test_the_shed_keeps_headroom_through_the_solver_zone():
    """No turn in d12-d23 may find the shed at its 100-unit cap."""
    per_turn = play_the_solver_zone()
    at_cap = [(d, tot, shed) for d, tot, shed in
              ((d, tot, shed) for d, tot, shed in per_turn) if d in SOLVER and tot >= CAP]
    by_day = collections.Counter(d for d, _t, _s in at_cap)
    worst = max((s for _d, _t, s in at_cap), key=lambda s: sum(s.values()), default={})
    assert not at_cap, (
        f"{len(at_cap)} turns in d12-d23 have the shed at {CAP}/{CAP}; every dawn in that state "
        f"destroys what the crew is carrying and every harvest after it has nowhere to go. "
        f"Turns at cap by day: {dict(sorted(by_day.items()))}. "
        f"A shed at the cap held: { {k: v for k, v in worst.items() if v} }")
