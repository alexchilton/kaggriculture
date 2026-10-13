"""How often does our build close day 0 too poor to hire on day 1?

Episode 108326043 lost on four dollars: day 0 closed at exactly $0, the day-1 `HIRE x3` (ladder
1+1+2 = $4) was refused in silence, and the farm ran a whole day with no hands -- 1 FEED against the
opponent's 4, two animals starved, herd capped at 7 against 17.

That is a threshold effect, so it will not show in every game: it needs day 0's spending to land at
or near zero, which depends on the world's shop draw and prices. This measures the frequency and the
margin, so "rare" can be replaced with a number.

    python -u scripts/zero_bank_probe.py submission/v38_ours/main.py --seeds 25
"""
import argparse, json, pathlib, statistics, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHILD = ROOT / "data/logs/_zero_child.py"
CHILD.write_text('''
import importlib.util, json, pathlib, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    old = sys.path[:]; sys.path.insert(0, str(pathlib.Path(path).parent))
    try: spec.loader.exec_module(m)
    finally: sys.path[:] = old
    return m.agent
path, opp, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
a = load(path, "sub_a"); b = load(opp, "sub_b")
from kaggle_environments import make
env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.005}, debug=False)
env.reset(2)
trace = []
def watched(obs, cfg=None):
    f = obs["farms"][obs.get("player", 0)]
    trace.append((obs.get("step", len(trace)), f["money"], len(f.get("hands") or [])))
    return a(obs, cfg)
env.run([watched, b])
farms = env.state[0].observation["farms"]
out = {"bank": farms[0]["money"], "opp": farms[1]["money"]}
for d in (0, 1, 2):
    at = [x for x in trace if x[0] == d * 24 + 23]
    out[f"close_d{d}"] = at[0][1] if at else None
    h = [x for x in trace if x[0] == (d + 1) * 24 + 1]
    out[f"hands_d{d+1}h1"] = h[0][2] if h else None
print(json.dumps(out))
''')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build")
    ap.add_argument("--opp", default="submission/v38/main.py")
    ap.add_argument("--seeds", type=int, default=25)
    args = ap.parse_args()
    rows = []
    print(f"{'seed':>8}{'close d0':>10}{'hands d1h1':>12}{'close d1':>10}"
          f"{'hands d2h1':>12}{'bank':>11}{'opp':>11}")
    for s in range(args.seeds):
        seed = 1000 + s * 7919
        r = subprocess.run([sys.executable, str(CHILD), str(ROOT / args.build),
                            str(ROOT / args.opp), str(seed)],
                           capture_output=True, text=True, cwd=str(ROOT))
        try:
            o = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            print(f"{seed:>8}  FAILED")
            continue
        rows.append(o)
        flag = "  <-- no hands" if (o["hands_d1h1"] or 0) == 0 else ""
        print(f"{seed:>8}{o['close_d0']:>10,.0f}{str(o['hands_d1h1']):>12}"
              f"{o['close_d1']:>10,.0f}{str(o['hands_d2h1']):>12}"
              f"{o['bank']:>11,.0f}{o['opp']:>11,.0f}{flag}", flush=True)
    if rows:
        c0 = [r["close_d0"] for r in rows]
        starved = sum(1 for r in rows if (r["hands_d1h1"] or 0) == 0)
        print(f"\nday-0 close: min {min(c0):,.0f}  median {statistics.median(c0):,.0f}  "
              f"max {max(c0):,.0f}")
        print(f"games with NO hands at day 1 hour 1: {starved}/{len(rows)}")
        print(f"games closing day 0 under $10: {sum(1 for x in c0 if x < 10)}/{len(rows)}")


if __name__ == "__main__":
    main()
