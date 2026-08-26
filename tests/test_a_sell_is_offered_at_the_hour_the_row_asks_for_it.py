"""A sell the row asks for at hour h is offered at hour h, not held to dusk.

Alex, 2026-08-26: *"sometimes the board is the truth sometimes the schedule"*. The sell row is the
schedule's side of that line -- what to sell, how much, and **when**.

`LATE_SELL_BIAS` / `LATE_SELL_FROM_HOUR` held every offer to h16 from a module constant, so the
hour tag on every row order was dead data. Measured across the three clone arms, every day of the
season carries sell orders and they are spread over all 24 hours; for `clone_open`, **260 of 591
sell orders fall before h16** -- 44% of the teacher's timing, discarded.

Measured d12 of `clone_open`, seed 123641874, handover d12. The shed at dawn is HIS shed exactly,
15 FERTILIZER and 2 WOOL, because d0-d11 is his tape replayed verbatim:

    hour    our shed FERT    his shed FERT    row asks
      0          15               15
      1          15               15          SELL FERTILIZER 8
      2          15                6          SELL FERTILIZER 8, SELL FERTILIZER 1
      3          14                0          SELL FERTILIZER 3
     16          20                0          (our first offer of the day)

He clears the shed by h3 from stock that was already sitting there. We offered nothing until h16.
This is not a delivery problem -- nothing had to be fetched, carried or dropped. The goods were in
the shed at dawn and the day declined to sell them.

**The prior measurement that defends holding to h16 is a different arm.** The comment at the gate
records "letting the whole day's quota through instead measured -$7,617 on melon", and that arm
offered the entire day's quota in one turn at h2. The row is not a dump: d12 meters 8, 9, 3 and 1
over four hours and then posts nothing until h18. The same comment argues metering is the correct
shape. So that null says nothing about following the row's own hours.

This test asserts the BEHAVIOUR, so a differently-named constant fails it too.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

ARM, SEED, HANDOVER, DAY = "clone_open", 123641874, 12, 12
TPD = 24


def _offers_by_hour():
    """`{hour: {product: qty}}` for every SELL we post on `DAY`, plus the dawn shed."""
    kaggle_env = pytest.importorskip("kaggle_environments")
    import kagg.plan as _PLAN
    import scripts.breakdown as B
    from kagg.search import schedule_agent as SA

    rel, sched_rel, team = B.TAPES[ARM]
    path = str(REPO / rel)
    economy, shops = B.env_config(path), B.recorded_shops(path)
    tape = B.tape_policy(path, team, 0)
    sched = {int(k): v for k, v in json.loads((REPO / sched_rel).read_text()).items()}
    thin = {d: _PLAN.thin(r) for d, r in sched.items()}
    ours = SA.make_agent(thin, 0, router=True, start_day=HANDOVER)

    env = kaggle_env.make("kaggriculture", configuration=dict(economy, seed=SEED), debug=False)
    env.reset(2)
    opp = B.tape_policy(path, team, 1)
    offers, dawn_shed = {}, None
    for t in range((DAY + 1) * TPD + 1):
        for s in (0, 1):
            env.state[s].observation.town["unlocked_shops"] = list(shops(t))
        obs = env.state[0].observation
        act = tape(obs, t) if t < HANDOVER * TPD else ours(obs)
        if t == DAY * TPD:
            dawn_shed = dict((obs.get("private") or {}).get("shed") or {})
        if t // TPD == DAY:
            got = offers.setdefault(t % TPD, {})
            for o in (act.get("market") or []):
                if o and o[0] == "SELL" and len(o) > 2:
                    got[o[1]] = got.get(o[1], 0) + int(o[2])
        env.step([act, opp(env.state[1].observation, t)])
    return offers, dawn_shed, sched[DAY]


def test_no_constant_holds_every_sell_to_a_fixed_hour():
    """The sell hour comes from the row, not from a module-level number."""
    src = (REPO / "kagg/search/schedule_agent.py").read_text()
    for name in ("LATE_SELL_BIAS", "LATE_SELL_FROM_HOUR"):
        assert f"\n{name} = " not in src, (
            f"{name} is back. The row carries an hour on every order and it is the driver; "
            "a fixed hour makes 44% of the teacher's sell timing unreachable.")


def test_the_row_reaches_the_agent_carrying_its_sell_hours():
    """The gate is unreachable if `orders` is stripped, and that is exactly what happened once.

    The first version of the release read `row["orders"]` while `kagg.plan.TAPE_ONLY` still stripped
    it, so the gate never fired on any turn of any day and the change measured as the h16 deletion
    alone. This pins the plumbing, not the policy.
    """
    import kagg.plan as P

    assert "orders" not in P.TAPE_ONLY, (
        "TAPE_ONLY strips `orders` again -- the sell hour cannot reach the agent and the release "
        "gate silently does nothing.")
    row = P.thin(json.loads((REPO / f"data/seed_scripts/{ARM}/schedule.json").read_text())[str(DAY)])
    assert row.get("orders"), f"d{DAY} of {ARM} reached the agent with no orders: {sorted(row)}"


def test_the_agent_reads_only_the_sell_entries_of_the_order_stream():
    """`orders` travels with the row, so the tape restriction has to live in the agent.

    `_sell_by_hour` is the sanctioned view. Nothing else in the module may touch `orders`, or the
    schedule stops being a target sheet and starts being a replay of someone's HIREs and land buys.
    """
    src = (REPO / "kagg/search/schedule_agent.py").read_text()
    readers = [l.strip() for l in src.splitlines()
               if ('row["orders"]' in l or 'row.get("orders")' in l) and not l.strip().startswith("#")]
    assert len(readers) == 2, (
        "`orders` is read outside `_sell_by_hour`. The agent may take (product, hour, qty) off SELL "
        f"rows and nothing else. Readers found: {readers}")


def test_the_row_s_early_sell_is_offered_early():
    """d12 asks for FERTILIZER at h1 with 15 in the shed. It must be offered at h1."""
    offers, dawn_shed, row = _offers_by_hour()

    early = [o for o in (row.get("orders") or [])
             if len(o) > 3 and o[1] == "SELL" and int(o[0]) <= 4]
    assert early, "d12 of clone_open is the fixture because its row sells before h4"

    held = int((dawn_shed or {}).get("FERTILIZER", 0))
    assert held >= 8, f"fixture broken: dawn shed holds {held} FERTILIZER, expected his 15"

    late = []
    for hour, _side, prod, qty in ((o[0], o[1], o[2], o[3]) for o in early):
        got = sum(v for h, got in offers.items() if h <= int(hour)
                  for k, v in got.items() if k == prod)
        if got <= 0:
            late.append((int(hour), prod, int(qty)))
    first = min((h for h, got in offers.items() if got), default=None)
    assert not late, (
        f"the row asks {late} and nothing was offered by those hours; "
        f"dawn shed {dawn_shed}, our first offer of the day is h{first}")
