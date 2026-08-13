"""One day, hour by hour, ours against theirs. Actions and money.

Alex's instruction: make day 0 match -- actions and money -- then day 1. Small steps. So this prints a
single day at full resolution rather than a season summary, because a season summary cannot tell you
which hour to fix.

Teacher-forced: our `decide` reads *their* observation each hour, so a difference here is the plan
disagreeing about what to do on a board it has been handed, never accumulated drift. Their money is
printed as the running context it is; the money question on a teacher-forced run is "would our orders
have cost/earned the same", which the `spend` column answers.

    PYTHONPATH=. python3 -u scripts/day_diff.py --day 0 2>&1 | tee data/logs/day_diff_0.log
"""

import argparse
import collections
import json

from kagg.search import agent as A
from kagg.search import executor as X
from kagg.search import plan as P, replay_plan as RP

TURNS_PER_DAY = 24
SEED_COST = dict(zip(P.CROP_NAMES, [10.0, 20.0, 50.0, 100.0, 80.0]))
ANIMAL_COST = {"GOOSE": 200.0, "COW": 800.0, "SHEEP": 600.0}


def _market(orders):
    """{(op, item): qty}, merging repeats -- the simulator settles the merged total identically."""
    out = collections.Counter()
    for o in orders or []:
        if not isinstance(o, list) or not o:
            continue
        # ORDER quantities, deliberately: this diffs what two agents ASKED FOR, turn by turn,
        # and a difference in the ask is the thing being looked for. It is not a unit count and
        # must not be summed into one.
        if o[0] in ("HIRE", "BUY_LAND"):
            out[(o[0] + " offered", "")] += 1
        elif len(o) >= 3 and int(o[2]) > 0:
            out[(o[0] + " offered", o[1])] += int(o[2])
    return out


def _units(action):
    return collections.Counter(
        tuple(u) for u in [action.get("farmer")] + list(action.get("hands") or []) if u)


def _cash(mkt, prices):
    """Signed cash the order list asks for, at the book the turn opened on."""
    total = 0.0
    for (op, item), q in mkt.items():
        if op == "SELL":
            total += q * prices.get(item, 0)
        elif op == "BUY_PRODUCT":
            total -= q * prices.get(item, 0)
        elif op == "BUY_SEED":
            total -= q * SEED_COST.get(item, 0)
        elif op == "BUY_ANIMAL":
            total -= q * ANIMAL_COST.get(item, 0)
    return total


def _fmt(counter):
    if not counter:
        return "-"
    return " ".join(f"{op}{'/' + item if item else ''}x{q}"
                    for (op, item), q in sorted(counter.items()))


def _ops(counter):
    if not counter:
        return "-"
    return " ".join(f"{k}x{v}" for k, v in sorted(collections.Counter(
        k[0] for k in counter.elements()).items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="data/episodes/89873723.json")
    ap.add_argument("--seat", type=int, default=0)
    ap.add_argument("--day", type=int, default=0)
    a = ap.parse_args()

    layout = RP.layout_from_replay(a.episode, seat=a.seat)
    plan = P.decode(RP.genome_from_layout(layout)[None])

    n_match_m = n_match_u = n = 0
    their_cash = our_cash = 0.0
    print(f"day {a.day} of {a.episode} seat {a.seat}\n")
    lo, hi = a.day * TURNS_PER_DAY, (a.day + 1) * TURNS_PER_DAY
    # `teacher_forced_pairs` supplies the **pre-action** board: a replay records each observation after
    # its own action, so pairing them by index asks a plan to buy seeds a board already holds.
    for t, obs, theirs in RP.teacher_forced_pairs(a.episode, a.seat):
        if not (lo <= t < hi):
            continue
        prices = (obs.get("market") or {}).get("prices") or {}
        view = A.observation_view(obs)
        ours = A.to_action(obs, X.decide(view, plan), int(view.n_units[0]))

        tm, om = _market(theirs.get("market")), _market(ours["market"])
        tu, ou = _units(theirs), _units(ours)
        tc, oc = _cash(tm, prices), _cash(om, prices)
        their_cash += tc
        our_cash += oc
        n += 1
        n_match_m += int(tm == om)
        n_match_u += int(tu == ou)

        hour = t % TURNS_PER_DAY
        flag = "" if (tm == om and tu == ou) else "  <<"
        print(f"h{hour:<2} ${float(obs['farms'][a.seat]['money']):>8,.0f} "
              f"crew {int(view.n_units[0]):>2}{flag}")
        print(f"     mkt  theirs {_fmt(tm)}")
        print(f"          ours   {_fmt(om)}")
        print(f"     cash theirs {tc:>+9,.0f}   ours {oc:>+9,.0f}")
        print(f"     unit theirs {_ops(tu)}")
        print(f"          ours   {_ops(ou)}")

    print(f"\n{'=' * 78}")
    print(f"day {a.day}: market matched {n_match_m}/{n} turns, units matched {n_match_u}/{n}")
    print(f"day {a.day} cash asked: theirs {their_cash:>+,.0f}   ours {our_cash:>+,.0f}   "
          f"gap {our_cash - their_cash:>+,.0f}")


if __name__ == "__main__":
    raise SystemExit(main())
