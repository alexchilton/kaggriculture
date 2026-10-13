"""Two submission builds, one FRESH PROCESS per game.

These agents keep state at module level: v38 builds a single `Chassis` when `main.py` is imported
(`_IMPL = make_agent(...)`) and every later call runs through that same object. Importing once and
looping games therefore carries one game's state into the next, and the author's own notebook says
they use a fresh process per game for exactly this reason.

An earlier in-process loop here read 16/20 for the hybrid; that number is not trustworthy and this
script exists to replace it.

    python -u scripts/h2h_isolated.py submission/v38_ours/main.py submission/v38/main.py --seeds 10
"""
import argparse, json, pathlib, statistics, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

CHILD = '''
import importlib.util, json, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    old = sys.path[:]
    sys.path.insert(0, str(__import__("pathlib").Path(path).parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path[:] = old
    return mod.agent
a, b, seed, weeds, seat = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
fa, fb = load(a, "sub_a"), load(b, "sub_b")
from kaggle_environments import make
env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=False)
env.reset(2)
env.run([fa, fb] if seat == 0 else [fb, fa])
farms = env.state[0].observation["farms"]
print(json.dumps({"a": farms[seat]["money"], "b": farms[1 - seat]["money"]}))
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()

    child = ROOT / "data/logs/_h2h_child.py"
    child.write_text(CHILD)
    wins = {"a": 0, "b": 0, "tie": 0}
    banks = {"a": [], "b": []}
    print(f"{'seed':>7} {'seat':>5} {'A bank':>12} {'B bank':>12} {'margin':>11}  win")
    for s in range(args.seeds):
        seed = 1000 + s * 7919
        for seat in (0, 1):
            r = subprocess.run([sys.executable, str(child), str(ROOT / args.a), str(ROOT / args.b),
                                str(seed), str(args.weeds), str(seat)],
                               capture_output=True, text=True, cwd=str(ROOT))
            try:
                out = json.loads(r.stdout.strip().splitlines()[-1])
            except Exception:
                print(f"{seed:>7} {seat:>5}  FAILED {r.stderr.strip().splitlines()[-1][:70] if r.stderr.strip() else '?'}")
                continue
            ba, bb = out["a"], out["b"]
            banks["a"].append(ba)
            banks["b"].append(bb)
            w = "A" if ba > bb else ("B" if bb > ba else "tie")
            wins["a" if w == "A" else ("b" if w == "B" else "tie")] += 1
            print(f"{seed:>7} {seat:>5} {ba:>12,.0f} {bb:>12,.0f} {ba-bb:>11,.0f}  {w}", flush=True)
    n = sum(wins.values())
    print(f"\nA = {args.a}\nB = {args.b}")
    print(f"games {n}   A {wins['a']}  B {wins['b']}  ties {wins['tie']}"
          f"   A win rate {100*wins['a']/max(1,n):.1f}%")
    for k in ("a", "b"):
        if banks[k]:
            print(f"   {k.upper()} mean bank {statistics.mean(banks[k]):>12,.0f}")


if __name__ == "__main__":
    main()
