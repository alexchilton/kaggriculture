"""The schedule's sell row is delivered whatever the bank holds.

Alex, 2026-08-26: *"this was always wrong and never matched kawa either - you built that and i never
agreed"*, and *"i have spent about 3 weeks trying to get you away from it without breaking the rest
of the planner"*.

`FUND_THE_DAY_WHEN_SHORT` gated delivery of the row's `sells` on `_days_bill_now(row) > money`. On a
healthy bank the delivery fell back to opportunistic -- `router.py:234` records it as "free at plan
time", meaning it happens only if a hand wanders past the shed. So the agent sold when it was broke
and warehoused otherwise.

Measured d12 of `clone_open`, seed 123641874, handover d12: the row asks
`{FERTILIZER: 39, WOOL: 11, MILK: 6, STRAWBERRY: 4}`, the shed held wool, fertilizer and strawberry
by dusk, and we offered **none** of the strawberry and DROPped once against his thirteen -- banking
$941 against his $4,178 on that day alone.

This test exists because deleting the flag is not enough: it has been reintroduced before, and
nothing in the suite went red when it was. It asserts the BEHAVIOUR, not the absence of a constant,
so a differently-named gate fails it too.
"""

import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def test_no_flag_gates_the_sell_row_on_the_bank():
    """No module-level constant may re-introduce a bank test around the sell row."""
    src = (REPO / "kagg/search/schedule_agent.py").read_text()
    assert "\nFUND_THE_DAY_WHEN_SHORT = " not in src, (
        "FUND_THE_DAY_WHEN_SHORT is back. The row's sells are delivered always; the bank does not "
        "decide whether the schedule happens.")
    # The gate itself: `short_of_cash` may not consult money.
    line = next((l for l in src.splitlines() if l.strip().startswith("short_of_cash =")), "")
    assert "money" not in line, (
        f"the sell-row gate reads the bank again: {line.strip()!r}")


def test_the_row_s_sells_are_offered_when_the_bank_is_healthy():
    """Drive d12 from the tape's own board and require the row's products to be OFFERED.

    Offers, not fills -- the book may refuse us, and that is a different failure. What this pins is
    that the day ASKS to sell what its row names.
    """
    kaggle_env = pytest.importorskip("kaggle_environments")
    import json

    import scripts.breakdown as B
    from kagg.search import schedule_agent as SA

    rel, sched_rel, team = B.TAPES["clone_open"]
    path = str(REPO / rel)
    economy, shops = B.env_config(path), B.recorded_shops(path)
    tape = B.tape_policy(path, team, 0)
    sched = {int(k): v for k, v in json.loads((REPO / sched_rel).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    ours = SA.make_agent(thin, 0, router=True, start_day=12)

    env = kaggle_env.make("kaggriculture", configuration=dict(economy, seed=123641874), debug=False)
    env.reset(2)
    opp = B.tape_policy(path, team, 1)
    offered, opening_bank = {}, None
    for t in range(313):
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        env.state[1].observation.town["unlocked_shops"] = list(shops(t))
        obs = env.state[0].observation
        act = tape(obs, t) if t < 288 else ours(obs)
        if t == 288:
            opening_bank = float(obs["farms"][0]["money"])
        if t // 24 == 12:
            for o in (act.get("market") or []):
                if o and o[0] == "SELL":
                    offered[o[1]] = offered.get(o[1], 0) + int(o[2])
        env.step([act, opp(env.state[1].observation, t)])

    # The day opens rich -- this is exactly the case the deleted flag suppressed.
    assert opening_bank and opening_bank > 5000, f"d12 opened on ${opening_bank:,.0f}"
    row = sched[12]["sells"]
    missing = [p for p in row if offered.get(p, 0) <= 0]
    assert not missing, (
        f"d12 opened on ${opening_bank:,.0f} and offered nothing for {missing}; "
        f"row {row}, offered {offered}")
