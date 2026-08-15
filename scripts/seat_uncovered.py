"""Can the uncovered jobs be seated at all? Search TOURS, not pool order.

`solve_day_offline.py` permutes the job pool and re-runs `cover`'s greedy. That searches almost
nothing: it cannot change how `materialise` builds a tour, where the turns go, or which unit ends
its day early. 401 shuffled restarts on d12 all returned the same 45/47, which says the search space
was wrong, not that the day was full -- the tape covers its own far corners on that day while
idling 39 turns to our 20, and its last plantings are at h20 where ours stop at h18.

This searches the thing that actually decides it, using `cover.py`'s own cost model:

    materialise(start, work, carry, depots, wanted, deliver, rush, due) -> tour
    turns(start, tour)                                                  -> cost

so a seating this reports as feasible is feasible under the real model, not a second one.

    step 1  INSERT   try each uncovered job at every position in every unit's sequence
    step 2  EJECT    if nothing fits, take one job out of a unit, insert the uncovered job,
                     and re-home the ejected one anywhere it fits (a depth-1 ejection chain)

Both steps accept only when the rebuilt tour costs <= that unit's budget, so nothing here can
invent turns. If both fail, the jobs genuinely do not fit the current crew and budgets, and the
answer is upstream -- in what the day chose to plant, or in how many hands it hired.
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from kagg.search import cover as C                                        # noqa: E402


def load(path):
    d = json.loads(pathlib.Path(path).read_text())
    jobs = []
    for j in d["jobs"]:
        job = C.Job(tile=j["tile"], ops=[(o[0], o[1]) for o in j["ops"]],
                    needs=j.get("needs") or None, gives=j.get("gives") or None,
                    at_risk=j.get("at_risk", False), products=j.get("products") or ())
        job.funds = bool(j.get("funds", False))
        jobs.append(job)
    kw = dict(units=[tuple(u) for u in d["units"]], budget=list(d["budget"]),
              depots=tuple(tuple(x) for x in d["depots"]),
              carry={int(k): v for k, v in (d.get("carry") or {}).items()},
              supply=d.get("supply"), deliver=d.get("deliver", True), wanted=d.get("wanted"),
              rush=d.get("rush", False), day=d.get("day"), due=d.get("due"))
    return jobs, kw


def cost(u, seq, kw):
    """Turns for unit `u` to run `seq`, or None if the tour cannot be built."""
    tour = C.materialise(kw["units"][u], seq, kw["carry"].get(u), kw["depots"],
                         kw["wanted"], kw["deliver"], kw["rush"], due=kw["due"])
    if tour is None:
        return None
    return C.turns(kw["units"][u], tour)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture")
    args = ap.parse_args()
    jobs, kw = load(args.fixture)
    routes, left = C.cover(jobs=list(jobs), **kw)
    print(f"{args.fixture}\n  day {kw['day']}  {len(jobs)} jobs  "
          f"{sum(len(v) for v in routes.values())} seated  {len(left)} uncovered\n")

    print(f"  {'unit':>5} {'start':>8} {'jobs':>5} {'cost':>5} {'budget':>7} {'SLACK':>6}")
    slack = {}
    for u, seq in sorted(routes.items()):
        c = cost(u, seq, kw) if seq else 0
        slack[u] = kw["budget"][u] - (c or 0)
        print(f"  u{u:<4} {str(kw['units'][u]):>8} {len(seq):>5} {str(c):>5} "
              f"{kw['budget'][u]:>7} {slack[u]:>6}")
    print(f"  total slack across the crew: {sum(slack.values())} turns\n")

    for j in left:
        print(f"  --- trying to seat {tuple(j.tile)} {[o[0] for o in j.ops]}")
        best = None
        for u, seq in routes.items():
            for pos in range(len(seq) + 1):
                trial = seq[:pos] + [j] + seq[pos:]
                c = cost(u, trial, kw)
                if c is not None and c <= kw["budget"][u]:
                    if best is None or c < best[2]:
                        best = (u, pos, c)
        if best:
            u, pos, c = best
            print(f"      INSERT fits: u{u} at position {pos}, tour {c}/{kw['budget'][u]}")
            routes[u] = routes[u][:pos] + [j] + routes[u][pos:]
            continue
        print("      no plain insertion fits; trying depth-1 ejection")
        done = False
        for u, seq in routes.items():
            for out_i in range(len(seq)):
                ejected = seq[out_i]
                rest = seq[:out_i] + seq[out_i + 1:]
                for pos in range(len(rest) + 1):
                    trial = rest[:pos] + [j] + rest[pos:]
                    c = cost(u, trial, kw)
                    if c is None or c > kw["budget"][u]:
                        continue
                    for v, seq2 in routes.items():
                        if v == u:
                            continue
                        for p2 in range(len(seq2) + 1):
                            t2 = seq2[:p2] + [ejected] + seq2[p2:]
                            c2 = cost(v, t2, kw)
                            if c2 is not None and c2 <= kw["budget"][v]:
                                print(f"      EJECT fits: u{u} takes {tuple(j.tile)} "
                                      f"({c}/{kw['budget'][u]}), {tuple(ejected.tile)} moves to "
                                      f"u{v} ({c2}/{kw['budget'][v]})")
                                routes[u] = trial
                                routes[v] = t2
                                done = True
                                break
                        if done:
                            break
                    if done:
                        break
                if done:
                    break
            if done:
                break
        if not done:
            print("      NO SEATING EXISTS under these budgets -- not an assignment problem.")


if __name__ == "__main__":
    main()
