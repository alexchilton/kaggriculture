"""Play the built submission under whatever `kaggle-environments` is installed, and report.

Run it twice, from two venvs, to price the 1.32.6 "town rebalance" against the 1.32.2 economy the
ladder was still running on 2026-08-07:

    .venv/bin/python -u scripts/version_sensitivity.py
    /path/to/v1326/bin/python -u scripts/version_sensitivity.py

The comparison is only meaningful because it changes exactly one thing. Both runs use the same
seed, the same tape, the same weeds-off configuration and the same `submission/main.py` -- and
the bundle is self-contained, so the second venv needs nothing but `numpy` and the environment.
That self-containment is the property `scripts/build_planner_submission.py` exists to guarantee,
and this is the first thing that actually depends on it.

What changed in 1.32.6:

    townCenterSellInterval        12 -> 24      the centre buys once a day, not twice
    TOWN_CENTER_DEMAND_SCHEDULE   [(20,4),(10,2),(0,1)] -> DELETED, flat 1 all season
    MAX_SHOP_INSTANCES = 8        each unlocked shop gets its own town slot
    movement onto LOCKED          blocked -> ALLOWED

Late-season town drawdown falls roughly 8x, so a plan that banks stock and dumps it late is
priced against a ramp that no longer exists. Our schedule was read off a 1.32.2 tape, so the
question this answers is not "which is better" but "how much of our season is version-specific".

Deliberately NOT a gate. It reports; the decision about which version to target is a judgement
about what the ladder is running, which no local measurement can settle.
"""

import argparse
import importlib.metadata
import importlib.util
import json
import pathlib
import sys

REPLAY = "data/seed_scripts/top_guys/90494364.json"
TEAM = "Seb (allegedly)"
TARGET = "submission/main.py"


def tape_policy(replay, team, seat_wanted):
    """Replay one side of a downloaded episode, verbatim. Copied from `scripts/breakdown.py`.

    Inlined rather than imported because this script has to run inside a venv that has no
    repository on its path -- importing `scripts.breakdown` would drag in `kagg` and defeat the
    point of the exercise.
    """
    d = json.loads(pathlib.Path(replay).read_text())
    seat = d["info"]["TeamNames"].index(team)
    src = seat if seat_wanted == 0 else 1 - seat
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[src] or {} for step in d["steps"][1:])]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    return lambda obs, t: acts[t] if t < len(acts) else idle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    args = ap.parse_args()

    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as kg

    version = importlib.metadata.version("kaggle-environments")
    spec = importlib.util.spec_from_file_location("_bundle", pathlib.Path(TARGET).resolve())
    bundle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bundle)

    env = make("kaggriculture",
               configuration={"seed": args.seed, "weedSpawnChance": args.weeds})
    interval = env.configuration.get("townCenterSellInterval")
    schedule = getattr(kg, "TOWN_CENTER_DEMAND_SCHEDULE", "DELETED")
    env.reset(2)
    opp = tape_policy(REPLAY, TEAM, 1)

    for t in range(24 * 30):
        if env.done:
            break
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = bundle.agent(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    farms = env.state[0].observation["farms"]
    ours, tape = float(farms[0]["money"]), float(farms[1]["money"])
    print(f"kaggle-environments {version} | townCenterSellInterval {interval} | "
          f"demand schedule {schedule}")
    print(f"  seed {args.seed}, weeds {args.weeds}: ours ${ours:,.0f} vs tape ${tape:,.0f} "
          f"({'WIN' if ours > tape else 'LOSS'} {ours - tape:+,.0f})")


if __name__ == "__main__":
    main()
