"""A/B the d13-d18 tree clamp against the unclamped control on identical seeds.

Copies the harness pattern out of `scripts/breakdown.py` (`run`, `tape_policy`, `recorded_shops`,
`env_config`) rather than reinventing it: same env economy keys, same recorded shop draw injected
into BOTH seats, same fills-based market counting, same tape opponent.

For each seed it plays two full seasons of our agent against the kawashigi tape opponent:

    control   TREE_CLAMP off
    clamped   TREE_CLAMP on

and reports, per arm: the bank at the close of d12-d18 (so each window day's BANKED money reads
as a difference), PLANT ops offered per window day, standing crop tiles at dusk of d18 and d29,
and -- clamped arm only -- which tree leaf fired each dawn. Identical seeds, identical shop draw;
the only difference between arms is the clamp.

    python -u scripts/tree_clamp_ab.py --seeds 11,12,13,14,15,16
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

import breakdown as B                       # noqa: E402  -- the shared harness
from kagg.search import schedule_agent as SA   # noqa: E402
from kagg.search import tree_clamp as TC    # noqa: E402

WINDOW = tuple(range(TC.CLAMP_FROM_DAY, TC.CLAMP_TO_DAY + 1))


def play(seed, weeds, clamp):
    """One full season. Returns a row dict for one arm of one seed."""
    replay, schedule, team = B.TAPES[B.DEFAULT_TAPE]
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in json.loads(pathlib.Path(schedule).read_text()).items()}

    # Which leaf fired at each dawn. `schedule_agent` holds the same module object, so wrapping
    # `apply` here intercepts the agent's own calls.
    leaves = {}
    if clamp:
        _inner = TC.apply

        def apply(sched_, day, obs, me=0):
            farms = obs.get("farms") or []
            ok = len(farms) > me and sched_.get(day)
            if ok:
                priv = obs.get("private") or {}
                leaves[day] = TC.regime(
                    TC.dawn_features(farms[me]["tiles"], priv.get("shed") or {}))
            return _inner(sched_, day, obs, me)

        TC.apply = apply

    TC.TREE_CLAMP = clamp
    try:
        a = SA.make_agent(sched, 0, router=True)
        # `B.run` drives every policy as `policy(obs, turn)`, and takes a FACTORY for each seat.
        agent = lambda o, t=None, _a=a: _a(o)
        opp = lambda: B.tape_policy(str(REPO / replay), team, 1)
        days, ops, _cash, _dawn = B.run(lambda: agent, opp, seed, weeds,
                                        economy=B.env_config(replay),
                                        shops=B.recorded_shops(replay))
    finally:
        TC.TREE_CLAMP = True
        if clamp:
            TC.apply = _inner

    # `days[d]` is the board at the END of day d; crop_* keys live flat in the snapshot.
    snap = days[18]
    crops18 = {c: snap["crop_" + c] for c in ("WHEAT", "STRAWBERRY", "MELON")}
    snap29 = days[-1]
    crops29 = {c: snap29["crop_" + c] for c in ("WHEAT", "STRAWBERRY", "MELON")}
    return {
        "seed": seed,
        "money": [d["money"] for d in days],
        "plants": {d: ops[d]["PLANT"] for d in WINDOW},
        "crops_d18": crops18,
        "crops_d29": crops29,
        "leaves": dict(leaves),
        "final": days[-1]["money"],
    }


def fmt(row):
    banks = "".join(f"{row['money'][d]:>9}" for d in range(12, 19))
    plants = "".join(f"{row['plants'][d]:>5}" for d in WINDOW)
    c18 = ",".join(f"{k[:3]}{v}" for k, v in sorted(row["crops_d18"].items()))
    return f"  banks d12..d18{banks}   PLANT{plants}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="11,12,13,14,15,16")
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]

    ctrl, clam = [], []
    for seed in seeds:
        ctrl.append(play(seed, args.weeds, clamp=False))
        clam.append(play(seed, args.weeds, clamp=True))
        print(f"seed {seed} done", flush=True)

    for name, rows in (("CONTROL", ctrl), ("CLAMPED", clam)):
        print(f"\n{name}")
        for r in rows:
            # NOT truncated to 5 chars: 'straw' is a prefix of 'straw+wheat' and once cost an
            # entire misreading of which leaf fired.
            leaf = " ".join(f"d{d}:{r['leaves'].get(d, '-')}" for d in WINDOW) if r["leaves"] \
                else "(no leaf log)"
            print(f"  seed {r['seed']:>3}{fmt(r)}")
            print(f"        {leaf}")

    print("\n  PAIRS  (clamped - control, same seed)")
    tot_window = tot_final = 0
    for c, k in zip(ctrl, clam):
        banked = sum(k["money"][d] - c["money"][d] for d in WINDOW)
        planted = sum(k["plants"][d] - c["plants"][d] for d in WINDOW)
        tot_window += banked
        tot_final += k["final"] - c["final"]
        w18 = sum(k["crops_d18"].values()) - sum(c["crops_d18"].values())
        w29 = sum(k["crops_d29"].values()) - sum(c["crops_d29"].values())
        print(f"  seed {k['seed']:>3}  banked d13-18 {banked:+8.0f}   plants {planted:+4d}   "
              f"crops@d18 {w18:+4d}   crops@season {w29:+4d}   final {k['final'] - c['final']:+10.0f}")
    n = len(seeds)
    print(f"\n  mean banked d13-18 {tot_window / n:+8.0f}   mean final {tot_final / n:+10.0f}"
          f"   over {n} seeds")


if __name__ == "__main__":
    main()
