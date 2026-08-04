"""Action-by-action, dollar-for-dollar: where does our plan first disagree with the winner?

Alex's standard, and it is the correct one: if day 0 cash differs at all, the error is already there,
so the comparison has to be turn by turn and dollar to dollar, not a per-day cash summary.

**Teacher-forced on purpose.** Our `decide` is fed the replay's *own* observation at every turn, not
our own simulated state, so nothing compounds: turn 137 is judged against the exact board the winner
faced on turn 137. A divergence here is the plan disagreeing with the winner's play, never accumulated
drift. That is what makes "the first differing turn" a meaningful answer.

The comparison is on the emitted action, because that is what the plan produces and what the money
follows from. `kagg/sim` already reproduces a real season to 0.2% given the actions, so identical
actions imply identical dollars and there is nothing further to check.

    PYTHONPATH=. python3 -u scripts/tape_diff.py 2>&1 | tee data/logs/tape_diff.log
"""

import argparse
import collections
import json

import numpy as np

from kagg.search import agent as A
from kagg.search import executor as X
from kagg.search import plan as P, replay_plan as RP

TURNS_PER_DAY = 24


def _norm_market(orders):
    """A market list as {(op, item): total_qty}, **merging repeats of the same (op, item)**.

    The merge is the whole point, and getting it wrong is what made the first version of this script
    report a false impossibility. The winner's turn 1 emits `SELL WHEAT 1`, `SELL WHEAT 3`,
    `SELL WHEAT 5`, and comparing those as three separate (op, item, qty) entries scored four
    disagreements against our single `SELL WHEAT 5` -- when the correct answer is none.

    `tests/test_split_sell_orders.py` measures it against the reference directly: any partition of a
    quantity banks **identically**, because `_refresh_prices` is a pure function of inventory (ref
    194-197) and the per-unit quote recomputes `market_price` off live inventory rather than reading
    the cached prices (ref 571). So the extra refreshes that splitting inserts change only what
    agents *observe*, never what a unit transacts at.

    One exception, and it is small: with both seats selling the same product the lockstep pairs them
    by slot index, so granularity shifts a couple of dollars between them ($2 on 5 wheat, zero-sum).
    That is a real effect and it is why the raw-order entry point is still worth having -- but it is
    a rounding error against a $147k season, not a reason a plan cannot express a turn.
    """
    out = collections.Counter()
    for o in orders or []:
        if not isinstance(o, list) or not o:
            continue
        op = o[0]
        if op in ("HIRE", "BUY_LAND"):
            out[(op, None)] += 1
        elif op in ("SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
            try:
                n = int(o[2])
            except (TypeError, ValueError):
                continue
            if n > 0:
                out[(op, o[1])] += n
    return out


def _norm_units(action):
    """Unit ops as a multiset, since which *hand* does a job is not part of the plan."""
    units = [action.get("farmer")] + list(action.get("hands") or [])
    return collections.Counter(tuple(u) for u in units if u)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="data/episodes/89873723.json")
    ap.add_argument("--seat", type=int, default=0)
    ap.add_argument("--show", type=int, default=12, help="how many differing turns to print")
    a = ap.parse_args()

    ep = json.load(open(a.episode))
    steps = ep["steps"]
    layout = RP.layout_from_replay(a.episode, seat=a.seat)
    plan = P.decode(RP.genome_from_layout(layout)[None])
    print(f"{a.episode} seat {a.seat}: ${layout.money:,.0f} over {len(steps)} turns")
    print("teacher-forced: our `decide` reads THEIR observation each turn, so nothing compounds\n")

    first = None
    n_same = n_diff = 0
    market_only = units_only = 0
    shown = 0
    op_delta = collections.Counter()

    for t, step in enumerate(steps):
        cell = step[a.seat]
        obs, theirs = cell.get("observation"), cell.get("action")
        if not isinstance(theirs, dict) or not obs or "farms" not in obs:
            continue
        obs = dict(obs)
        obs.setdefault("player", a.seat)

        view = A.observation_view(obs)
        ours = A.to_action(obs, X.decide(view, plan), int(view.n_units[0]))

        tm, om = _norm_market(theirs.get("market")), _norm_market(ours["market"])
        tu, ou = _norm_units(theirs), _norm_units(ours)
        same_m, same_u = tm == om, tu == ou
        if same_m and same_u:
            n_same += 1
            continue

        n_diff += 1
        market_only += int(not same_m and same_u)
        units_only += int(same_m and not same_u)
        for k in set(om) | set(tm):
            op_delta[k[0]] += abs(om[k] - tm[k])

        if first is None:
            first = t
        if shown < a.show:
            shown += 1
            day, hour = t // TURNS_PER_DAY, t % TURNS_PER_DAY
            money = float(obs["farms"][a.seat]["money"])
            print(f"--- turn {t} (day {day} hour {hour}), their bank ${money:,.0f}")
            if not same_m:
                miss, extra = tm - om, om - tm
                if miss:
                    print(f"    they ordered more : "
                          f"{', '.join(f'{o} {i or ''} x{q}' for (o, i), q in miss.items())}")
                if extra:
                    print(f"    we ordered more   : "
                          f"{', '.join(f'{o} {i or ''} x{q}' for (o, i), q in extra.items())}")
            if not same_u:
                miss, extra = tu - ou, ou - tu
                print(f"    their units {dict(collections.Counter(k[0] for k in tu.elements()))}")
                print(f"    our units   {dict(collections.Counter(k[0] for k in ou.elements()))}")

    total = n_same + n_diff
    print(f"\n{'=' * 78}")
    print(f"turns compared        : {total}")
    print(f"identical             : {n_same}  ({n_same / max(total, 1):.1%})")
    print(f"first divergence      : turn {first}"
          + (f" = day {first // TURNS_PER_DAY} hour {first % TURNS_PER_DAY}" if first is not None
             else " (none)"))
    print(f"differ in market only : {market_only}")
    print(f"differ in units only  : {units_only}")
    print(f"differ in both        : {n_diff - market_only - units_only}")
    print(f"\nmarket order-count disagreement, by op:")
    for op, n in op_delta.most_common():
        print(f"    {op:<14} {n:>6}")


if __name__ == "__main__":
    raise SystemExit(main())
