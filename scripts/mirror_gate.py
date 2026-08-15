"""Score a market change where a market change is actually visible: against ourselves.

**Why this exists, and why the tape gate cannot replace it.** `scripts/tape_gate.py` returned
100.0%, 100.0% and 99.4% for the three agents it was asked to separate
(`data/logs/tape_gate_three.log`). A gate that cannot lose cannot rank, and that is the same
failure its own docstring records for the synthetic pool it replaced. Tapes are open-loop: they
cannot contest a book they did not expect to be contested, so a rule about *how much to sell into
a contested book* is invisible to them by construction.

A mirror is the opposite. `market["inventory"]` is one shared object, so both seats sell into the
same book on the same turns -- which is exactly the condition that floors a price (WOOL floors 59
units above I0, MILK 76; see `docs/the_book_is_shallow_2026-08-09.md`). It is also what Kaggle
validation runs.

The baseline is the module's own shipped defaults and the candidate is the same module with flags
overridden, so the two differ in precisely the thing under test and nothing else.

**Read the win rate, not the bank.** The ladder is an Elo rating: a $43k win and a $4k win score
the same. Both seats are played on every seed so a seat advantage cannot masquerade as skill, and
a mirror with no change is a coin flip by construction -- if an unchanged arm does not land near
50%, the harness is broken, which is what `--selftest` checks.

    PYTHONPATH=. python3 -u scripts/mirror_gate.py --selftest
    PYTHONPATH=. python3 -u scripts/mirror_gate.py --set HOLD_A_FLOORED_BOOK=False
"""

import argparse
import collections
import concurrent.futures as cf
import json
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
#: The plan the CURRENT `schedule_agent` is calibrated for. It is not a property of the harness --
#: see `--plan` below.
PLAN = REPO / "data/seed_scripts/top_guys/90976060/schedule.json"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
HI = ("MILK", "WOOL", "MELON", "STRAWBERRY")


def _thin(plan):
    sched = {int(k): v for k, v in json.loads(pathlib.Path(plan).read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def _coerce(text):
    """`--set NAME=VALUE` values are typed: bools, ints, floats, else the string."""
    if text in ("True", "False"):
        return text == "True"
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


def one(job):
    """One mirror season. Returns (candidate_bank, baseline_bank, per-product $/unit for both)."""
    module, overrides, seed, cand_seat, base_module, cand_plan, base_plan = job
    sys.path.insert(0, str(REPO))
    import importlib

    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

    SA = importlib.import_module("kagg.search." + module)
    # **The baseline may be a DIFFERENT module.** Comparing two agents is not the same question as
    # comparing two flag settings of one agent: the shipped `schedule_agent` sits on a base that
    # scored 1232.8 while `schedule_agent` sits on one that scored 1455, so "is this change
    # good" and "is this the right base" have to be asked separately.
    SB = importlib.import_module("kagg.search." + base_module) if base_module else SA
    # **And an agent must carry the plan it was calibrated for.** This harness fed one hardcoded plan
    # to both seats, which void ed the first HEAD-vs-1455mh run: 1455 is `daf7c97`'s planner and the
    # only artifact that ever scored 1455, and it scored it paired with 90494364, not 90976060. Run
    # on HEAD's plan it lost 84.4% -- a result that says HEAD's code reads HEAD's schedule better
    # than a stranger's code does, which is close to a tautology and is not the question. A mirror
    # requires one shared BOARD, not one shared plan; the plans are part of what is being compared.
    thin_c = _thin(cand_plan)
    thin_b = _thin(base_plan) if base_plan != cand_plan else thin_c

    # The two agents differ ONLY by the overrides, and the flags are module-level globals, so the
    # candidate's factory is called while they are set and the baseline's while they are not.
    # `make_agent` closes over the values it needs at build time for the flags that are read once;
    # for the rest the module global is shared, so a single process cannot host both arms at once.
    # That is why each job restores the originals immediately after building.
    saved = {k: getattr(SA, k) for k in overrides}
    for k, v in overrides.items():
        setattr(SA, k, v)
    cand = SA.make_agent(thin_c, cand_seat, router=True)
    for k, v in saved.items():
        setattr(SA, k, v)
    base = SB.make_agent(thin_b, 1 - cand_seat, router=True)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    # The overrides are re-applied per turn to the CANDIDATE's module only. When the two seats are
    # different modules that is trivially safe; when they are the same module it is what stops the
    # baseline seeing the candidate's flags, since both share one set of globals.
    agents = {cand_seat: (cand, SA, overrides), 1 - cand_seat: (base, SB, {})}

    with record_fills(env) as fills:
        for _t in range(24 * 30):
            if env.done:
                break
            acts = []
            for p in (0, 1):
                o = env.state[p].observation
                agent, mod, ov = agents[p]
                saved2 = {k: getattr(mod, k) for k in ov}
                for k, v in ov.items():
                    setattr(mod, k, v)
                a = agent(o)
                for k, v in saved2.items():
                    setattr(mod, k, v)
                n = len(o["farms"][p].get("hands") or [])
                acts.append({"farmer": a["farmer"], "hands": list(a["hands"])[:n],
                             "market": a["market"]})
            env.step(acts)

    farms = env.state[0].observation["farms"]
    out = {"seed": seed, "cand_seat": cand_seat,
           "cand": float(farms[cand_seat]["money"]),
           "base": float(farms[1 - cand_seat]["money"])}
    for p in HI:
        u, r = fills.sold(player=cand_seat, product=p)
        out["cand_" + p] = (r / u) if u else 0.0
        out["cand_" + p + "_u"] = u
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", default="schedule_agent",
                    help="the CANDIDATE seat's agent module")
    ap.add_argument("--base-module", default=None,
                    help="the BASELINE seat's module, if comparing two agents rather than two "
                         "flag settings of one (e.g. schedule_agent)")
    ap.add_argument("--set", action="append", default=[],
                    help="NAME=VALUE flag override applied to the CANDIDATE seat only")
    ap.add_argument("--plan", default=str(PLAN),
                    help="the CANDIDATE's schedule. An agent must be paired with the plan it was "
                         "calibrated for: 1455 scored 1455 on 90494364, not on 90976060")
    ap.add_argument("--base-plan", default=None,
                    help="the BASELINE's schedule; defaults to --plan")
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--seed0", type=int, default=4001)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--selftest", action="store_true",
                    help="run with NO overrides; the result must land near 50%% or the gate lies")
    args = ap.parse_args()

    overrides = {}
    for item in args.set:
        k, _, v = item.partition("=")
        overrides[k] = _coerce(v)
    if args.selftest:
        overrides = {}

    base_plan = args.base_plan or args.plan
    seeds = [args.seed0 + i for i in range(args.seeds)]
    jobs = [(args.module, overrides, s, seat, args.base_module, args.plan, base_plan)
            for s in seeds for seat in (0, 1)]
    label = "SELFTEST (no change)" if args.selftest else (overrides or "no overrides")
    vs = args.base_module or args.module
    print(f"mirror gate: candidate {args.module} vs baseline {vs}  {len(jobs)} seasons  "
          f"candidate = {label}", flush=True)
    print(f"  candidate plan {pathlib.Path(args.plan).parent.name}   "
          f"baseline plan {pathlib.Path(base_plan).parent.name}", flush=True)

    rows = []
    with cf.ProcessPoolExecutor(max_workers=args.workers) as ex:
        for i, r in enumerate(ex.map(one, jobs), 1):
            rows.append(r)
            if i % 6 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)

    w = sum(1 for r in rows if r["cand"] > r["base"])
    d = sum(1 for r in rows if r["cand"] == r["base"])
    ln = len(rows) - w - d
    n = max(1, len(rows))
    print(f"\ncandidate  W{w} D{d} L{ln}   win rate {100.0 * (w + 0.5 * d) / n:.1f}%")
    print(f"  candidate mean bank ${statistics.mean(r['cand'] for r in rows):,.0f}"
          f"   baseline mean bank ${statistics.mean(r['base'] for r in rows):,.0f}")

    # **Score on the paired margin, not the win rate.** A win/loss threshold throws away the size of
    # the difference and inherits the full seed variance, which here spans $17k-$163k: detecting a
    # 5pp shift at 95% needs roughly 400 paired games. Pairing on the seed removes that variance --
    # both arms played the same board -- and summing the two seatings removes any seat effect, so
    # each seed contributes one number whose expectation is zero under the null.
    by_seed = collections.defaultdict(float)
    for r in rows:
        by_seed[r["seed"]] += r["cand"] - r["base"]
    margins = list(by_seed.values())
    mean = statistics.mean(margins)
    if len(margins) > 1:
        se = statistics.stdev(margins) / (len(margins) ** 0.5)
        t = mean / se if se else float("inf")
        verdict = ("SIGNIFICANT" if abs(t) >= 2.0 else
                   "not significant -- inside noise, do not act on it")
        print(f"\n  paired margin per seed (both seatings summed):")
        print(f"    mean ${mean:+,.0f}   SE ${se:,.0f}   t = {t:+.2f}   -> {verdict}")
        print(f"    seeds better for candidate: "
              f"{sum(1 for m in margins if m > 0)}/{len(margins)}")

    print("\n  candidate realised price, $/unit (units sold):")
    for p in HI:
        vals = [r["cand_" + p] for r in rows if r["cand_" + p] > 0]
        us = [r["cand_" + p + "_u"] for r in rows]
        floored = sum(1 for v in vals if v < 20)
        print(f"    {p:<12} ${statistics.mean(vals) if vals else 0:>7.2f}   "
              f"{statistics.mean(us):>6.0f} units   floored in {floored}/{len(rows)} seasons")

    if args.selftest:
        lo, hi = 35.0, 65.0
        rate = 100.0 * (w + 0.5 * d) / n
        verdict = "OK" if lo <= rate <= hi else "BROKEN -- an unchanged mirror must be a coin flip"
        print(f"\nselftest: {rate:.1f}% -> {verdict}")


if __name__ == "__main__":
    sys.exit(main())
