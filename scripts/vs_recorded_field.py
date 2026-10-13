"""Both builds against RECORDED ladder opponents, on their own seeds.

The local arena was four relatives of one chassis on 8 seeds, and the two live games examined were
the two that were flagged as losses -- a sample selected on the outcome being explained. Neither can
say whether a change helps against the field.

This replays each recorded episode with the opponent's ACTUAL action stream and our build in its
seat, on that episode's own seed and configuration, so the opponent is a real ladder agent playing
its real game and only our side changes.

    python -u scripts/vs_recorded_field.py submission/v38_ours/main.py submission/noflip/main.py
"""
import collections, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-11", "data/replays_2026-09-09", "data/replays_live"]
CHILD = ROOT / "data/logs/_field_child.py"
CHILD.write_text('''
import importlib.util, json, pathlib, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    old = sys.path[:]; sys.path.insert(0, str(pathlib.Path(path).parent))
    try: spec.loader.exec_module(m)
    finally: sys.path[:] = old
    return m.agent
build, rep_path, myseat = sys.argv[1], sys.argv[2], int(sys.argv[3])
a = load(build, "sub_a")
rep = json.loads(pathlib.Path(rep_path).read_text())
steps = rep["steps"]
acts = [((s[1-myseat] or {}).get("action") or {}) for s in steps[1:]]
idle = {"farmer": ["PASS"], "hands": [], "market": []}
box = {"t": 0}
def opp(obs, cfg=None):
    i = box["t"]; box["t"] += 1
    if i >= len(acts): return idle
    x = acts[i]
    return {"farmer": x.get("farmer", ["PASS"]) or ["PASS"],
            "hands": list(x.get("hands") or []), "market": list(x.get("market") or [])}
from kaggle_environments import make
cfg = dict(rep.get("configuration") or {}); cfg.pop("seed", None)
env = make("kaggriculture", configuration=dict(cfg, seed=rep["info"]["seed"]), debug=False)
env.reset(2)
env.run([a, opp] if myseat == 0 else [opp, a])
f = env.state[0].observation["farms"]
print(json.dumps({"me": f[myseat]["money"], "opp": f[1-myseat]["money"],
                  "opp_name": rep["info"]["TeamNames"][1-myseat]}))
''')


def main():
    builds = sys.argv[1:3]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    eps = []
    for d in DIRS:
        for p in sorted((ROOT / d).glob("*.json")):
            eps.append(p)
            if len(eps) >= limit:
                break
        if len(eps) >= limit:
            break
    res = collections.defaultdict(list)
    print(f"{'episode':>10} {'opponent':18}" + "".join(f"{pathlib.Path(b).parent.name:>14}"
                                                       for b in builds) + f"{'delta':>12}")
    for p in eps:
        row, banks = f"{p.stem:>10} ", {}
        name = ""
        for b in builds:
            r = subprocess.run([sys.executable, str(CHILD), str(ROOT / b), str(p), "0"],
                               capture_output=True, text=True, cwd=str(ROOT))
            try:
                o = json.loads(r.stdout.strip().splitlines()[-1])
            except Exception:
                banks[b] = None
                continue
            banks[b] = o["me"] - o["opp"]
            name = o["opp_name"]
            res[b].append(banks[b])
        row += f"{name[:18]:18}"
        for b in builds:
            row += f"{(banks.get(b) if banks.get(b) is not None else 0):>14,.0f}"
        if all(banks.get(b) is not None for b in builds):
            row += f"{banks[builds[1]] - banks[builds[0]]:>12,.0f}"
        print(row, flush=True)
    print()
    for b in builds:
        v = res[b]
        if v:
            print(f"{b:34} n={len(v):>3}  wins {sum(1 for x in v if x > 0):>3}  "
                  f"mean margin {sum(v)/len(v):>+12,.0f}")


if __name__ == "__main__":
    main()
