"""Destroyed vs merely late, measured exactly -- not guessed, not differenced across the rollover.

## Why this exists

`docs/fable_the_delivery_problem_2026-08-09.md` was commissioned to answer "high-value produce is
made and never reaches a sellable place" -- 443 units of MILK/WOOL/MELON/STRAWBERRY were observed
sitting in HANDS at dusk on one seed, and the open question was how much of that is a permanent
write-off (`_drop_inventories_to_shed`, `kaggriculture.py:830`, discards whatever will not fit) versus
merely sold a day late (fits, banks overnight, sells after the book has moved).

**Differencing the shed across the rollover overstates this by up to 15x**
(`docs/fable_the_discard_problem_2026-08-09.md`) because a SELL and a BUY_PRODUCT at hour 23 settle in
the same `env.step` as the rollover, so a sale reads as a loss. This test instead monkeypatches
`_drop_inventories_to_shed` itself -- the exact function that performs the sweep -- so `destroyed_p`
and `landed_p` are read off the real call, per product, every day, with zero inference:

    held_p         units of product p across every hand's inventory, going INTO the real call
    shed_before_p  what the shed already held of p (drops made earlier in the day)
    shed_after_p   what the shed holds of p, coming OUT of the real call
    landed_p       shed_after_p - shed_before_p        (<= held_p always, by construction)
    destroyed_p    held_p - landed_p                   (exact, not inferred)

## The measurement (2026-08-09, shipped `schedule_agent`, seb1326 tape opponent, seat 0)

Two different denominators, both reported so neither is mistaken for the other:

| seed | destroyed | landed late | destroyed % of ROLLOVER-SWEPT hi-value | destroyed % of SEASON hi-value produced |
|-----:|----------:|------------:|----------------------------------------:|------------------------------------------:|
|   13 |        22 |         410 |                                    5.1% |                                       2.7% |
|   17 |        36 |         442 |                                    7.5% |                                       4.2% |
|   19 |         2 |         315 |                                    0.6% |                                       0.3% |
|   23 |        15 |         321 |                                    4.5% |                                       2.0% |

"Rollover-swept" is `destroyed / (destroyed + landed)`: of the produce that actually went through
`_drop_inventories_to_shed` (i.e. was still in a hand at dusk), what fraction was lost. "Season" is
`destroyed / (destroyed + sold + unsold-shed-at-end)`, via `kagg.analysis.fills.record_fills` for the
`sold` term -- most hi-value production never rides to dusk at all, so this denominator is larger and
the percentage smaller. This test asserts the first (larger, stricter) one.

**Destruction is small either way: well under 10% of hi-value production, a few thousand dollars a
game at base price.** The 443-unit figure this investigation started from is real but is mostly the
LATE bucket -- produce that reaches the shed a day later than it could have and sells at whatever the
book is doing by then, not a write-off. Do not add the two buckets together; they are different losses
(`docs/fable_the_delivery_problem_2026-08-09.md` has the full reasoning and the seed-by-seed table).

## What this test asserts

A regression guard, not a target to chase: destruction stays a SMALL fraction of production. If a
future change to `cover.py`'s delivery batching (`DELIVER_MIN`, `DROP_WHERE_THE_TOUR_ALREADY_STANDS`,
the closing-trip cutoff) pushes it materially higher, this goes red and says so — the threshold sits
above the worst seed measured (4.2%) with headroom for seed variance, not tight against it.
"""
import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.arena.tape import build_tape_agent
from kagg.search import router as RT
from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY

HI = ("MILK", "WOOL", "MELON", "STRAWBERRY")
REPLAY, SCHEDULE, _TEAM = TAPES["seb1326"]

#: Worst seed measured is 4.2% (seed 17). Set with headroom above that, not tight against it -- this
#: is a regression guard on the ROLLOVER mechanism, not a target for a future delivery change to chase.
MAX_DESTROYED_PCT = 10.0


def _play_and_split(seed):
    """One season, shipped agent vs the seb1326 tape, exact destroyed/landed split for player 0."""
    import kaggle_environments.envs.kaggriculture.kaggriculture as kg
    from kaggle_environments import make

    destroyed = collections.Counter()
    landed = collections.Counter()
    calls = [0]
    orig_drop = kg._drop_inventories_to_shed

    def patched(private, capacity):
        # `_end_of_day` (kaggriculture.py:865) calls this once per player, in `enumerate(obs0.farms)`
        # order -- player 0 first, then player 1. That parity is the only way to attribute a call
        # without a player id in the signature; there is nowhere else this function is invoked from
        # (grep `reference/kaggriculture.py` -- one definition, one call site).
        is_us = (calls[0] % 2 == 0)
        calls[0] += 1
        held = collections.Counter()
        for inv in private["inventories"]:
            held.update(inv)
        shed_before = collections.Counter(private["shed"])
        orig_drop(private, capacity)
        if not is_us:
            return
        shed_after = collections.Counter(private["shed"])
        for item, n in held.items():
            if n <= 0:
                continue
            gained = shed_after.get(item, 0) - shed_before.get(item, 0)
            lost = n - gained
            if lost > 0:
                destroyed[item] += lost
            if gained > 0:
                landed[item] += gained

    kg._drop_inventories_to_shed = patched
    try:
        sched = {int(k): v for k, v in json.loads(pathlib.Path(SCHEDULE).read_text()).items()}
        thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
        ours = SA.make_agent(thin, 0, router=True)
        rival = build_tape_agent(REPLAY, 0)
        env = make("kaggriculture", configuration={"seed": seed}, debug=False)
        env.reset(2)
        for t in range(24 * 30):
            if env.done:
                break
            o0 = env.state[0].observation
            a0 = ours(o0)
            a1 = rival(env.state[1].observation)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        kg._drop_inventories_to_shed = orig_drop

    d_hi = sum(destroyed[p] for p in HI)
    l_hi = sum(landed[p] for p in HI)
    return d_hi, l_hi


@pytest.mark.slow
@pytest.mark.parametrize("seed", [13, 17, 19, 23])
def test_destroyed_is_a_small_fraction_of_hi_value_production(seed):
    destroyed_hi, landed_hi = _play_and_split(seed)
    produced = destroyed_hi + landed_hi   # `landed` undercounts same-day sells (never held at dusk),
    # so this ratio is against what WENT THROUGH THE ROLLOVER, not all season production -- exactly
    # the population `_drop_inventories_to_shed` can destroy. See the module docstring's full-season
    # `hi_produced` figures (destroyed + sold + unsold-shed) for the season-wide percentage.
    pct = 100.0 * destroyed_hi / max(1, produced)
    assert pct <= MAX_DESTROYED_PCT, (
        f"seed {seed}: {destroyed_hi} of {produced} rollover-swept hi-value units destroyed "
        f"({pct:.1f}%), above the {MAX_DESTROYED_PCT:.0f}% regression guard. "
        f"landed late: {landed_hi}.")
