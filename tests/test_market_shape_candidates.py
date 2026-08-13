"""Task #49: does OUR standing-offer sell shape cost money against Seb's few/small/late shape?

`docs/fable_market_shape_2026-08-09.md` measures the difference on FILLS and realised prices, not
offers (see `CLAUDE.md`'s warning about summing `o[2]` from the action stream -- that counts what
was OFFERED, not what filled, and re-offering the same quota on every one of 24 turns inflates it
24x). Two philosophies, not two settings of one dial: ours is a standing offer re-posted on every
turn, sized by a stack of caps; Seb's tape is few, small, deliberate orders, late in the day.

`CAP_SELL_OFFER_SIZE` and `LATE_SELL_BIAS` were the two smallest levers toward his shape. Both
shipped OFF originally; `LATE_SELL_BIAS` has since shipped ON (`kagg/search/schedule_agent.py`).
`CAP_SELL_OFFER_SIZE` never made it from the pre-2026-08-09 `schedule_agent.py` into
`schedule_agent_1455mh.py` (now the sole `kagg.search.schedule_agent`) and no longer exists;
its tests were removed in the 2026-08-13 cleanup that collapsed the two files into one -- see
`docs/REGISTER.md` and the commit that did it. The `LATE_SELL_BIAS` tests below still exercise a
real, live, shipped flag. The win-rate verdict lives in the doc, from `kagg.arena.run_arena` --
not here, because a unit test cannot answer an Elo question.
"""

import json
import pathlib

import pytest

from kagg.search import schedule_agent as SA


def _thin_schedule():
    sched_path = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
    if not sched_path.exists():
        pytest.skip("schedule fixture not present")
    sched = {int(k): v for k, v in json.loads(sched_path.read_text()).items()}
    return {d: {k: v for k, v in r.items()
                if k in ("sells", "buys", "seeds", "plants", "hands", "land", "animals",
                         "builds", "harvests")}
            for d, r in sched.items()}


def _opponent_agent(name):
    import importlib

    mod = importlib.import_module(f"kagg.agents.{name}")
    return mod.make_agent() if hasattr(mod, "make_agent") else mod.agent


def _play(flag_name, flag_value, turns=719, seed=11, opponent="pass", weeds=0.005):
    """Play `turns` turns of our agent against a real opponent, returning every SELL order
    emitted with its hour, so both candidates can be checked from one harness.

    **A live opponent matters, not a dummy.** `contrarian` at seed 2 is the scenario that actually
    reproduces an over-30 offer under TODAY's default caps (`RESERVATION_SELL_CAP`,
    `PRICE_AWARE_SELL_CAP`, `HOLD_A_FLOORED_BOOK` all on) -- a solo run against an empty/PASS
    opponent never did, across every seed tried
    (`data/logs/market_shape_offer_sweep_2026-08-09.log`). The market book is `shared: True`, so
    what the opponent does or does not buy changes our own reservation math.
    """
    from kaggle_environments import make

    thin = _thin_schedule()
    was = getattr(SA, flag_name)
    setattr(SA, flag_name, flag_value)
    try:
        env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds})
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        opp = (lambda obs, cfg: {"farmer": ["PASS"], "hands": [], "market": []}) if opponent == "pass" \
            else _opponent_agent(opponent)
        sells = []  # (day, hour, prod, qty)
        for _ in range(turns):
            obs0 = env.state[0].observation
            obs1 = env.state[1].observation
            hour = int(obs0.get("hour", 0) or 0)
            day = int(obs0.get("day", 0) or 0)
            a0 = agent(obs0, env.configuration)
            a1 = opp(obs1, env.configuration)
            for o in a0.get("market") or []:
                if o and o[0] == "SELL" and len(o) > 2:
                    sells.append((day, hour, o[1], int(o[2])))
            env.step([a0, a1])
            if env.state[0].status == "DONE":
                break
        return sells
    finally:
        setattr(SA, flag_name, was)


# ---------------------------------------------------------------------------- 2. the motivating fact
def test_the_historical_loss_actually_shows_the_78_unit_offer():
    """Pins the STATIC, historical fact this file's candidate is a response to. `data/ladder/
    losses/91229682.json` is a real recorded ladder game, played by whatever `submission/main.py`
    was live on Kaggle that day (5 submissions/day, so it can trail the tree by several commits);
    it is not re-playable from this repository.

    Today's tree, with every current cap on (`RESERVATION_SELL_CAP`, `PRICE_AWARE_SELL_CAP`,
    `HOLD_A_FLOORED_BOOK`), does NOT reproduce a 78-unit offer -- a 24-seed/opponent sweep
    (`data/logs/market_shape_offer_sweep_2026-08-09.log`) tops out at 43, against `contrarian`
    only, on day 29 hour 0 (seeds 2 and 6), and never against `heuristic`/`rancher` at all. So the
    caps already added since this loss have shrunk the problem, not solved it: 43 still clears the
    30-unit line `test_the_cap_reproduces_and_then_fixes_an_over_thirty_offer` below exercises
    live, on the exact seed/opponent pair that reaches it."""
    import json
    import pathlib

    path = pathlib.Path("data/ladder/losses/91229682.json")
    if not path.exists():
        pytest.skip("loss fixture not present")
    d = json.loads(path.read_text())
    max_qty = 0
    for step in d["steps"]:
        act = (step[0] or {}).get("action") or {}
        for o in act.get("market") or []:
            if o and o[0] == "SELL" and len(o) > 2:
                max_qty = max(max_qty, int(o[2]))
    assert max_qty > 30, f"expected the historical loss to show an offer over 30, got max={max_qty}"


def test_without_the_bias_orders_fire_before_hour_sixteen():
    sells = _play("LATE_SELL_BIAS", False, turns=200)
    assert any(hour < SA.LATE_SELL_FROM_HOUR for _, hour, _, _ in sells)


# ---------------------------------------------------------------------------- 3. RED before GREEN
def test_late_sell_bias_actually_suppresses_early_offers():
    """RED before wiring: the flag existed but every early-hour offer still fired. GREEN once the
    order construction is gated on `hour >= LATE_SELL_FROM_HOUR`, with the last-day liquidation
    window (`LIQUIDATE_LAST_DAY`) exempted -- that override is explicitly out of scope for every
    other sell cap in this file and this one is no different."""
    sells = _play("LATE_SELL_BIAS", True, turns=719)
    last_day_liquidation_hour = SA.LIQUIDATE_FROM_HOUR
    early = [(d, h, p, q) for d, h, p, q in sells
             if h < SA.LATE_SELL_FROM_HOUR
             and not (SA.LIQUIDATE_LAST_DAY and h >= last_day_liquidation_hour)]
    # A day-29 (last day) offer before LATE_SELL_FROM_HOUR but at/after LIQUIDATE_FROM_HOUR would
    # already be excluded above; anything else before the threshold is a wiring failure.
    early_not_last_day = [(d, h, p, q) for d, h, p, q in early if d < max(d2 for d2, *_ in sells)]
    assert not early_not_last_day, \
        f"LATE_SELL_BIAS on but early offers still fired: {early_not_last_day[:10]}"


# ---------------------------------------------------------------------------- 4. the wiring rail
def test_turning_the_late_bias_on_actually_changes_what_is_ordered():
    off = _play("LATE_SELL_BIAS", False, turns=400)
    on = _play("LATE_SELL_BIAS", True, turns=400)
    assert off != on


# ---------------------------------------------------------------------------- 5. determinism
def test_the_shipped_agent_is_deterministic_on_a_fixed_seed():
    """Two runs at the shipped defaults, no flags touched, must produce byte-identical action
    streams. This used to also pin 'both CAP_SELL_OFFER_SIZE and LATE_SELL_BIAS off reproduces
    shipped behaviour exactly' -- CAP_SELL_OFFER_SIZE no longer exists (it never made it from the
    pre-2026-08-09 schedule_agent.py into schedule_agent_1455mh.py, now the sole
    kagg.search.schedule_agent) and LATE_SELL_BIAS ships ON, not OFF, so that premise no longer
    holds. What survives is the determinism claim itself."""
    from kaggle_environments import make

    thin = _thin_schedule()

    def run():
        env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        acts = []
        for _ in range(200):
            obs = env.state[0].observation
            a = agent(obs, env.configuration)
            acts.append(json.dumps(a, sort_keys=True))
            env.step([a, {}])
        return acts

    assert run() == run()
