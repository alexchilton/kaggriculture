"""Task #55, step 0: is a tape arena faithful at all?

Before a tape can be an opponent, replaying BOTH seats from the recording must reproduce the
recorded banks. If it does not, the arena is measuring something other than the game that was
played, and every number built on it is worthless -- the same failure that made the synthetic pool
useless, one level down.

Reports, per replay: the seed the game was configured with, the recorded final banks, the banks our
env produces from the same two action streams, and the error. Anything above a fraction of a
percent means the tape is not replayable and needs explaining before it becomes a gate.
"""
import argparse
import glob
import json
import pathlib
import sys

sys.path.insert(0, ".")


def _acts(steps, idx):
    out = []
    for step in steps:
        s = (step[idx] or {}) if idx < len(step) else {}
        a = s.get("action") or {}
        out.append({"farmer": a.get("farmer") or ["PASS"],
                    "hands": list(a.get("hands") or []),
                    "market": list(a.get("market") or [])})
    return out


def check(path):
    from kaggle_environments import make

    d = json.loads(pathlib.Path(path).read_text())
    cfg = d.get("configuration") or {}
    seed = cfg.get("seed")
    names = d.get("info", {}).get("TeamNames") or ["?", "?"]
    steps = d["steps"][1:]
    a0, a1 = _acts(steps, 0), _acts(steps, 1)

    final = d["steps"][-1]
    rec = (final[0].get("reward"), final[1].get("reward"))

    conf = {k: v for k, v in cfg.items() if k in
            ("seed", "shedCapacity", "weedSpawnChance", "townCenterSellInterval", "episodeSteps")}
    env = make("kaggriculture", configuration=conf, debug=False)
    env.reset(2)
    for t in range(len(a0)):
        o0 = env.state[0].observation
        if env.done:
            break
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0[t]["farmer"], "hands": a0[t]["hands"][:n0], "market": a0[t]["market"]},
                  {"farmer": a1[t]["farmer"], "hands": a1[t]["hands"][:n1], "market": a1[t]["market"]}])
    got = (env.state[0].observation["farms"][0]["money"],
           env.state[1].observation["farms"][1]["money"])

    def err(r, g):
        if not r:
            return float("nan")
        return abs(g - r) / max(abs(r), 1.0) * 100

    return dict(path=pathlib.Path(path).name, seed=seed, names=names,
                rec=rec, got=got, e0=err(rec[0], got[0]), e1=err(rec[1], got[1]),
                turns=len(a0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="data/seed_scripts/top_guys/*.json")
    ap.add_argument("--limit", type=int, default=6)
    a = ap.parse_args()

    paths = sorted(p for p in glob.glob(a.glob) if pathlib.Path(p).is_file())[:a.limit]
    print(f"{'replay':<18}{'seed':>7}{'turns':>7}{'rec p0':>11}{'got p0':>11}{'err%':>8}"
          f"{'rec p1':>11}{'got p1':>11}{'err%':>8}", flush=True)
    for p in paths:
        try:
            r = check(p)
        except Exception as exc:                                  # noqa: BLE001
            print(f"{pathlib.Path(p).name:<18}  FAILED: {type(exc).__name__}: {exc}", flush=True)
            continue
        print(f"{r['path']:<18}{str(r['seed']):>7}{r['turns']:>7}"
              f"{r['rec'][0] or 0:>11,.0f}{r['got'][0]:>11,.0f}{r['e0']:>8.2f}"
              f"{r['rec'][1] or 0:>11,.0f}{r['got'][1]:>11,.0f}{r['e1']:>8.2f}", flush=True)


if __name__ == "__main__":
    main()
