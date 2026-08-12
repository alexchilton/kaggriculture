"""Solve a whole day offline: assign every job to a hand and order each tour, exactly, no time limit.

The shipped planner has one second a turn, so `cover()` is a greedy: cheapest insertion under a
fair-share cap, one pass, never revisited. Offline that constraint does not exist -- the board has
no random terrain (`_initial_tile` is a pure function of coordinates; the only RNG in
`kaggriculture.py` drives the shop draw and weed spawns), so geometry and distances are identical in
every game and a day solved once is worth solving properly. See
`docs/the_route_is_precomputable_2026-08-12.md`.

**Why this is not `solve_day_offline.py`.** That script permuted the job POOL and re-ran the same
greedy, which cannot change how a tour is built or where a unit's turns go. On d12 it returned
45/47 on all 401 restarts and I read that as "the day is full". It was not: u7 was using 15 turns of
23 and u8 16 of 23, and both uncovered jobs fit by plain insertion. The search space was wrong.
This one searches the assignment AND the order.

**The cost model is `cover.py`'s own.** A candidate is legal only when

    turns(start_u, materialise(start_u, seq_u, carry_u, depots, wanted, deliver, rush, due)) <= budget_u

for every unit, so nothing here can invent turns or shortcut a walk. `materialise` also inserts the
depot trips a sequence needs, which is why cost is NOT a sum of arc lengths and why this is a local
search against an oracle rather than a MIP.

**Objective**, in strict order:
  1. jobs covered, weighted -- a job that prevents an irreversible loss counts far above ordinary
     work, mirroring the tiers `cover`'s own passes already run in. An at-risk REQUIRED job is an
     animal one missed FEED from being removed (`kaggriculture.py:804`); an at-risk job is a tile
     one dry day from becoming a WEED (`:771`).
  2. total turns spent, minimised, as a pure tie-break between plans covering the same work.

**The search** is ruin-and-recreate: remove k jobs from the current plan, re-insert everything
unassigned by cheapest feasible insertion in random order, keep the result if the objective improves.
Restarts from the greedy each time the search stalls. `--seconds 0` runs until every job is covered
or the iteration cap is hit.

    python -u scripts/solve_day.py tests/fixtures/day_12_seed11_victor.json --seconds 60
    python -u scripts/solve_day.py FIXTURE --seconds 300 --dump-route route.json
"""
import argparse
import json
import pathlib
import random
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from kagg.search import cover as C                                        # noqa: E402

#: Weights for the coverage term. Ordering matches `cover`'s own pass order
#: (at_risk and required -> funds -> required -> at_risk -> everything else); the magnitudes only
#: have to keep each tier above any number of the tier below, and a day has under a hundred jobs.
W_DEATH = 1_000_000      # at_risk AND required: an animal is removed if this is missed
W_RISK = 10_000          # at_risk: a tile becomes a WEED
W_FUNDS = 1_000          # the day's shopping list, unpaid
W_REQUIRED = 100
W_ORDINARY = 1


def weight(j):
    if j.at_risk and j.required:
        return W_DEATH
    if j.at_risk:
        return W_RISK
    if j.funds:
        return W_FUNDS
    if j.required:
        return W_REQUIRED
    return W_ORDINARY


def late_hands(budget, n):
    """Charge the LAST `n` hands one more turn: their HIRE spilled, so they start an hour later.

    The fixture records the budget the shipped planner used, and that budget is optimistic. The env
    accepts ten market orders a turn (`schedule_agent.ORDER_SLOTS`), and `_fit_order_slots` defers
    the surplus HIREs to the next turn -- correctly, since `hires_today` is a per-DAY fibonacci
    counter, so deferring a hire inside a day is free. But `_router_acts` charges EVERY arriving hand
    a flat one turn, so a hand whose HIRE spilled is budgeted 23 and actually gets 22.

    Day 18, seed 11, measured -- the bank holds $22,809 at hour 0 and nothing is refused:

        h0  hands=0   HIRE offers this turn=9      nine fit, one slot went to another order
        h1  hands=9   HIRE offers this turn=2
        h2  hands=11

    Unit 10 drew eleven waters in a line from (4,7) round to (2,7), priced at exactly 23 of 23. It
    walked ten of them and left (2,7) dry -- the `water 53/54` cell.

    **This belongs here and not in the agent.** Correcting the budget inside `_router_acts` changes
    every day, and measured it broke d10 and d11, which were exact: `ORDER_SLOTS - 1` over-charges on
    a fourteen-hire day and five lost turns cost more than the one they saved. Here it changes one
    solved day and nothing else, and the solver has somewhere to put the displaced work -- on d18
    two hands sit completely idle with 23 turns each.

    `_fit_order_slots` drops surplus HIREs from the LAST one backwards and `_arrivals` returns hands
    in append order, so the late hands are always the last `n` units.

    **MEASURED AND WORSE on d18, 2026-08-12. Default 0; do not turn it on without re-measuring.**
    With `--late-hands 2` the solver still seats 69/69 in 191 turns and moves a stop off u10
    (11 jobs at 23/23 becomes 10 at 20/22), but the day it produces is worse than the route solved
    on the optimistic budget:

        d18            old route      --late-hands 2
        weeds            0/0             1/0            a tile died
        strawb          36/36           35/36
        harvest         11/14           10/14
        sell            35/61           23/61
        water           53/54           53/54           UNCHANGED

    So the honest reading is that the budget was not what kept `(2,7)` dry, or the work displaced off
    the late hands costs more elsewhere than it saves. The diagnosis of the late arrival is solid --
    the crew really does go 0 -> 9 -> 11 and those hands really do have 22 turns -- but acting on it
    here does not pay. `data/logs/route_d18_bd.json`, solved WITHOUT this, is the one to use.
    """
    out = list(budget)
    for k in range(max(0, len(out) - n), len(out)):
        out[k] = max(0, out[k] - 1)
    return out


def load(path, late=0):
    d = json.loads(pathlib.Path(path).read_text())
    jobs = []
    for j in d["jobs"]:
        job = C.Job(tile=j["tile"], ops=[(o[0], o[1]) for o in j["ops"]],
                    needs=j.get("needs") or None, gives=j.get("gives") or None,
                    at_risk=j.get("at_risk", False), products=j.get("products") or ())
        job.funds = bool(j.get("funds", False))
        jobs.append(job)
    kw = dict(units=[tuple(u) for u in d["units"]], budget=late_hands(d["budget"], late),
              depots=tuple(tuple(x) for x in d["depots"]),
              carry={int(k): v for k, v in (d.get("carry") or {}).items()},
              supply=d.get("supply"), deliver=d.get("deliver", True), wanted=d.get("wanted"),
              rush=d.get("rush", False), day=d.get("day"), due=d.get("due"))
    return jobs, kw


class Oracle:
    """`cover.py`'s own cost model, memoised. Returns None when the tour cannot be built."""

    def __init__(self, kw):
        self.kw = kw
        self.cache = {}
        self.calls = 0

    def cost(self, u, seq):
        key = (u, tuple(id(j) for j in seq))
        hit = self.cache.get(key)
        if hit is not None:
            return hit[0]
        self.calls += 1
        kw = self.kw
        tour = C.materialise(kw["units"][u], list(seq), kw["carry"].get(u), kw["depots"],
                             kw["wanted"], kw["deliver"], kw["rush"], due=kw["due"])
        c = None if tour is None else C.turns(kw["units"][u], tour)
        self.cache[key] = (c,)
        return c

    def fits(self, u, seq):
        c = self.cost(u, seq)
        return c is not None and c <= self.kw["budget"][u]


def score(routes, oracle):
    """(covered weight, -total turns). Higher is better, compared as a tuple."""
    w = sum(weight(j) for seq in routes.values() for j in seq)
    t = sum(oracle.cost(u, seq) or 0 for u, seq in routes.items() if seq)
    return (w, -t)


def best_insertion(routes, j, oracle, rng):
    """Cheapest feasible (unit, position) for `j`, or None."""
    best = None
    units = list(routes)
    rng.shuffle(units)
    for u in units:
        seq = routes[u]
        base = oracle.cost(u, seq) or 0
        for pos in range(len(seq) + 1):
            trial = seq[:pos] + [j] + seq[pos:]
            c = oracle.cost(u, trial)
            if c is None or c > oracle.kw["budget"][u]:
                continue
            delta = c - base
            if best is None or delta < best[0]:
                best = (delta, u, pos)
    return best


def recreate(routes, pool, oracle, rng):
    """Insert everything in `pool` by cheapest feasible insertion. Returns what would not fit."""
    leftover = []
    order = sorted(pool, key=lambda j: (-weight(j), -j.turns))
    for j in order:
        got = best_insertion(routes, j, oracle, rng)
        if got is None:
            leftover.append(j)
            continue
        _d, u, pos = got
        routes[u] = routes[u][:pos] + [j] + routes[u][pos:]
    return leftover


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture")
    ap.add_argument("--seconds", type=float, default=60.0,
                    help="0 = run until everything is covered or --max-iters is reached")
    ap.add_argument("--max-iters", type=int, default=1_000_000)
    ap.add_argument("--ruin", type=int, default=6, help="jobs removed per iteration")
    ap.add_argument("--seed", type=int, default=20260812)
    ap.add_argument("--dump-route", default=None)
    ap.add_argument("--late-hands", type=int, default=0,
                    help="how many of the day's hands arrive an hour late because their HIRE "
                         "spilled out of this turn's ten order slots; their budget is one turn "
                         "shorter than the fixture claims. See `late_hands`. Get the number by "
                         "counting the crew at h0/h1/h2 -- d18 seed 11 goes 0 -> 9 -> 11, so 2.")
    args = ap.parse_args()

    jobs, kw = load(args.fixture, late=args.late_hands)
    oracle = Oracle(kw)
    rng = random.Random(args.seed)
    total_w = sum(weight(j) for j in jobs)

    routes, left = C.cover(jobs=list(jobs), **kw)
    routes = {u: list(v) for u, v in routes.items()}
    print(f"{args.fixture}")
    print(f"  day {kw['day']}   {len(kw['units'])} units   {len(jobs)} jobs   "
          f"budgets {kw['budget'][:3]}...")
    if args.late_hands:
        print(f"  the last {args.late_hands} hand(s) arrive late: budgets now {kw['budget']}")
    print(f"  shipped greedy: {sum(len(v) for v in routes.values())}/{len(jobs)} seated, "
          f"{len(left)} uncovered")

    # The greedy's leftovers are the first thing to try -- on d12 both fit by plain insertion.
    left = recreate(routes, list(left), oracle, rng)
    best = {u: list(v) for u, v in routes.items()}
    best_left = list(left)
    best_score = score(best, oracle)
    seated = sum(len(v) for v in best.values())
    print(f"  after direct insertion: {seated}/{len(jobs)} seated, {len(best_left)} uncovered")

    start = time.monotonic()
    it = 0
    while it < args.max_iters:
        if args.seconds and time.monotonic() - start > args.seconds:
            break
        if not best_left and args.seconds == 0:
            break
        it += 1
        routes = {u: list(v) for u, v in best.items()}
        pool = list(best_left)
        seated_jobs = [(u, j) for u, seq in routes.items() for j in seq]
        if seated_jobs:
            for u, j in rng.sample(seated_jobs, min(args.ruin, len(seated_jobs))):
                if j in routes[u]:
                    routes[u].remove(j)
                    pool.append(j)
        leftover = recreate(routes, pool, oracle, rng)
        sc = score(routes, oracle)
        if sc > best_score:
            best, best_left, best_score = ({u: list(v) for u, v in routes.items()},
                                           list(leftover), sc)
            print(f"    iter {it}: {sum(len(v) for v in best.values())}/{len(jobs)} seated, "
                  f"{-best_score[1]} turns, {len(best_left)} uncovered")

    seated = sum(len(v) for v in best.values())
    print(f"\n  {it} iterations, {oracle.calls} tour evaluations, "
          f"{time.monotonic() - start:.1f}s")
    print(f"  BEST {seated}/{len(jobs)} seated, {-best_score[1]} turns, "
          f"{best_score[0]}/{total_w} of the weighted work")
    print(f"\n  {'unit':>5} {'start':>8} {'jobs':>5} {'cost':>5} {'budget':>7} {'slack':>6}")
    for u, seq in sorted(best.items()):
        c = oracle.cost(u, seq) if seq else 0
        print(f"  u{u:<4} {str(kw['units'][u]):>8} {len(seq):>5} {str(c):>5} "
              f"{kw['budget'][u]:>7} {kw['budget'][u] - (c or 0):>6}")
    for j in best_left:
        print(f"      UNCOVERED {tuple(j.tile)} {[o[0] for o in j.ops]} w={weight(j)}")

    if args.dump_route:
        out = {str(u): [{"tile": list(j.tile), "ops": [list(o) for o in j.ops]} for j in seq]
               for u, seq in best.items()}
        pathlib.Path(args.dump_route).write_text(json.dumps(out, indent=2))
        print(f"\n  route written to {args.dump_route}")


if __name__ == "__main__":
    main()
