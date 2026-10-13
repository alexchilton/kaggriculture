"""Round-robin between submission builds, one fresh process per game.

The public notebooks mirror each other -- "Dynamic Route Agent" and "Market-Smart Farming" are the
same file, sha256 94c1c2c05ae7cde8 -- so the live field is a handful of distinct builds and playing
them against each other locally is a fair proxy for the ladder.

Win rate, not bank: the ladder is Elo and a $43k win scores like a $4k one. Mean bank is printed
only as a liveness check (a farm on exactly $3,000 never acted).

Fresh process per pairing-seed because these agents build one module-level Chassis at import.

    python -u scripts/arena.py --seeds 6 a=submission/v38_ours/main.py b=submission/v38/main.py ...
"""
import argparse, collections, itertools, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHILD = ROOT / "data/logs/_arena_child.py"
CHILD.write_text('''
import importlib.util, json, pathlib, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    old = sys.path[:]; sys.path.insert(0, str(pathlib.Path(path).parent))
    try: spec.loader.exec_module(mod)
    finally: sys.path[:] = old
    return mod.agent
a, b, seed, weeds, seat = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
fa, fb = load(a, "sub_a"), load(b, "sub_b")
from kaggle_environments import make
env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=False)
env.reset(2)
env.run([fa, fb] if seat == 0 else [fb, fa])
f = env.state[0].observation["farms"]
print(json.dumps({"a": f[seat]["money"], "b": f[1-seat]["money"]}))
''')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("builds", nargs="+", help="name=path")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()
    builds = dict(b.split("=", 1) for b in args.builds)

    wins = collections.Counter()
    played = collections.Counter()
    print(f"{'pairing':34}{'seed':>8}{'seat':>5}{'margin':>12}  win", flush=True)
    for (na, pa), (nb, pb) in itertools.combinations(builds.items(), 2):
        for s in range(args.seeds):
            seed = 1000 + s * 7919
            for seat in (0, 1):
                r = subprocess.run([sys.executable, str(CHILD), str(ROOT / pa), str(ROOT / pb),
                                    str(seed), str(args.weeds), str(seat)],
                                   capture_output=True, text=True, cwd=str(ROOT))
                try:
                    o = json.loads(r.stdout.strip().splitlines()[-1])
                except Exception:
                    print(f"{na+' v '+nb:34}{seed:>8}{seat:>5}  FAILED")
                    continue
                played[(na, nb)] += 1
                w = na if o["a"] > o["b"] else (nb if o["b"] > o["a"] else "tie")
                wins[(na, nb, w)] += 1
                print(f"{na+' v '+nb:34}{seed:>8}{seat:>5}{o['a']-o['b']:>12,.0f}  {w}",
                      flush=True)
    print(f"\n{'pairing':34}{'games':>7}{'result':>18}")
    table = collections.Counter()
    for (na, nb), n in played.items():
        a, b = wins[(na, nb, na)], wins[(na, nb, nb)]
        table[na] += a
        table[nb] += b
        print(f"{na+' v '+nb:34}{n:>7}{f'{a}-{b}':>18}")
    print(f"\n{'build':24}{'total wins':>12}")
    for name, w in table.most_common():
        print(f"{name:24}{w:>12}")


if __name__ == "__main__":
    main()
