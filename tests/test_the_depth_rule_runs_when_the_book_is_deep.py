"""The depth rule is deliberately unreachable below base price. Do not "fix" it.

`schedule_agent`'s sell block sizes an offer like this:

    price_ok = PRICE_AWARE_SELL_CAP and prices[prod] >= BASE_PRICE[prod]
    if price_ok:
        n = min(have, rate[prod])
        if RESERVATION_SELL_CAP:
            n = min(have, reservation_units(prod, inventory, step, unlocked_shops, q_rem))
    else:
        n = min(have, allow, rate[prod])          # day totals from the reference replay
        ...
        if DEPTH_RULE_BELOW_BASE and RESERVATION_SELL_CAP:
            n = min(n, reservation_units(...))    # OFF -- see below

`reservation_units` is the only code in the file that reads `town.unlocked_shops` to decide HOW
MUCH to sell. `market_price` is monotone decreasing in inventory and equals base exactly at `I0`,
so `price >= base` means the book is at or below its neutral level. The rule is therefore live only
while the book has room, and silent once we are flooding it.

**That looks exactly like a bug, and it is not.** It was implemented, measured, and reverted.

32 mirror seasons, 16 seeds x both seatings (`scripts/mirror_gate.py`,
`data/logs/mirror_depth_rule.log`), candidate = rule OFF below base, baseline = rule ON:

    OFF   W26 D0 L6   81.2%   mean bank $69,633
    ON                        mean bank $61,833
    paired margin per seed  $+15,599   SE $5,386   t = +2.90   SIGNIFICANT, 13/16 seeds

The mechanism does what it says: with the rule on, seed 29's sub-base MILK selling falls from 211
units to 90. Suppressing those sales is what costs the money. The town's drain is a **common pool**
-- every unit it removes is one re-sale at a good price and whoever sold first has it -- so holding
stock back to protect a price in a contested book hands the absorption to the opponent.

This could not be seen on the tape gate, which scores 100.0% (`data/logs/tape_gate_three.log`):
a tape is open-loop and cannot race us for the drain. Only a mirror can.

These tests pin the behaviour in BOTH directions so the branch is not re-"fixed" by inspection, and
so that a future change which silently stops the flag working is caught.
"""

import collections
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
PLAN = REPO / "data/seed_scripts/top_guys/90976060/schedule.json"
TAPE = REPO / "data/seed_scripts/top_guys/90976060.json"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
HI = ("MILK", "WOOL", "MELON", "STRAWBERRY")


def _thin():
    sched = {int(k): v for k, v in json.loads(PLAN.read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def _run(seed):
    """One season. Returns (units sold below base per product, turns the depth rule was asked).

    Both counters only ever move on a turn where the agent actually emitted a SELL for that product
    while its quoted price was under base -- the exact turns the `else` branch governs.
    """
    import kagg.search.schedule_agent as SA
    from kaggle_environments import make

    from kagg.arena.tape import build_tape_agent
    from kagg.search import router as RT      # `RT` is `router` in schedule_agent, not `routines`

    asked = collections.Counter()
    real = SA.reservation_units

    def spy(prod, *a, **kw):
        asked[prod] += 1
        return real(prod, *a, **kw)

    SA.reservation_units = spy
    try:
        ours = SA.make_agent(_thin(), 0, router=True)
        rival = build_tape_agent(str(TAPE), 0)
        env = make("kaggriculture", configuration={"seed": seed}, debug=False)
        env.reset(2)

        sub_base_sells = collections.Counter()
        asked_while_sub_base = collections.Counter()

        for _t in range(24 * 30):
            if env.done:
                break
            o0 = env.state[0].observation
            prices = (o0.get("market") or {}).get("prices") or {}
            before = collections.Counter(asked)

            a0 = ours(o0)

            for order in (a0.get("market") or []):
                if not isinstance(order, list) or len(order) < 3 or order[0] != "SELL":
                    continue
                prod = order[1]
                if prod not in HI:
                    continue
                base = RT.BASE_PRICE.get(prod, 0)
                if float(prices.get(prod, base)) < base:
                    sub_base_sells[prod] += int(order[2])
                    if asked[prod] > before[prod]:
                        asked_while_sub_base[prod] += 1

            n0 = len(o0["farms"][0].get("hands") or [])
            a1 = rival(env.state[1].observation)
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
        return sub_base_sells, asked_while_sub_base
    finally:
        SA.reservation_units = real


@pytest.mark.slow
def test_the_shipped_agent_does_not_consult_the_depth_rule_below_base(monkeypatch):
    """The shipped default. Deliberate, and worth $15,599 a seed -- see the module docstring."""
    import kagg.search.schedule_agent as SA
    assert SA.DEPTH_RULE_BELOW_BASE is False, (
        "DEPTH_RULE_BELOW_BASE ships OFF. Turning it on was measured at -$15,599 per seed over 32 "
        "mirror seasons (t = +2.90 for OFF). Read this file's docstring before changing it."
    )
    monkeypatch.setattr(SA, "DEPTH_RULE_BELOW_BASE", False)
    sub_base, asked = _run(29)

    assert sum(sub_base.values()) > 0, (
        "seed 29 emitted no sub-base SELL at all, so this fixture can no longer see the behaviour "
        "it exists to pin -- a silent pass here would be indistinguishable from the branch changing"
    )
    assert not asked, (
        f"the depth rule was consulted below base with the flag OFF: {dict(asked)} -- the branch "
        f"has moved, and the mirror measurement behind the OFF default no longer describes the code"
    )


@pytest.mark.slow
def test_the_flag_really_does_reach_the_depth_rule_when_enabled(monkeypatch):
    """The flag must remain live, so the OFF default stays a choice rather than dead code."""
    import kagg.search.schedule_agent as SA
    monkeypatch.setattr(SA, "DEPTH_RULE_BELOW_BASE", True)
    sub_base, asked = _run(29)

    assert asked, (
        "with DEPTH_RULE_BELOW_BASE on, the depth rule was still never consulted below base -- the "
        "flag is dead code, so the measured OFF-vs-ON comparison is meaningless"
    )
    # Measured 211 -> 90 on this seed. Assert only the direction, not the number: the point is that
    # the flag bites, and pinning 90 would make an unrelated routing change fail this test.
    assert sub_base["MILK"] < 211, (
        f"the flag no longer restrains sub-base MILK selling (got {sub_base['MILK']}, the OFF arm "
        f"measured 211) -- either the branch or `reservation_units` has changed"
    )
