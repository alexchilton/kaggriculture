"""Two submission builds, played against each other on fresh seeds, both seats, weeds on.

The ladder is Elo, so WIN RATE is the metric and a $43k win scores like a $4k one. Mean bank is
printed beside it only as a liveness check: a farm that ends on exactly $3,000 never acted, which is
how a broken entry point masquerades as a legitimate loss.

Both seats every seed, because seat 0 and seat 1 do not see the same board.

    python -u scripts/head_to_head.py submission/v38/main.py submission/twocoins_h1/main.py --seeds 8
"""
import argparse, importlib.util, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(path, name):
    """Import a submission's main.py and return its per-turn callable."""
    path = pathlib.Path(path).resolve()
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    old = sys.path[:]
    sys.path.insert(0, str(path.parent))     # its siblings (policy.py, actions.json) must resolve
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path[:] = old
    for attr in ("agent", "act", "main"):
        f = getattr(mod, attr, None)
        if callable(f):
            return f, mod
    raise SystemExit(f"{path}: no agent entry point found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()

    fa, _ma = load(args.a, "sub_a")
    fb, _mb = load(args.b, "sub_b")
    from kaggle_environments import make

    wins = {"a": 0, "b": 0, "tie": 0}
    banks = {"a": [], "b": []}
    print(f"{'seed':>6} {'seat':>5} {'A bank':>12} {'B bank':>12} {'margin':>12}  winner")
    for s in range(args.seeds):
        seed = 1000 + s * 7919
        for seat in (0, 1):
            env = make("kaggriculture",
                       configuration={"seed": seed, "weedSpawnChance": args.weeds}, debug=False)
            env.reset(2)
            agents = [fa, fb] if seat == 0 else [fb, fa]
            try:
                env.run(agents)
            except Exception as e:
                print(f"{seed:>6} {seat:>5}  RUN FAILED {type(e).__name__}: {e}")
                continue
            farms = env.state[0].observation["farms"]
            ba = farms[seat]["money"]
            bb = farms[1 - seat]["money"]
            banks["a"].append(ba)
            banks["b"].append(bb)
            w = "A" if ba > bb else ("B" if bb > ba else "tie")
            wins["a" if w == "A" else ("b" if w == "B" else "tie")] += 1
            print(f"{seed:>6} {seat:>5} {ba:>12,.0f} {bb:>12,.0f} {ba-bb:>12,.0f}  {w}",
                  flush=True)
    n = sum(wins.values())
    print(f"\nA = {args.a}")
    print(f"B = {args.b}")
    print(f"games {n}   A wins {wins['a']}  B wins {wins['b']}  ties {wins['tie']}"
          f"   A win rate {100*wins['a']/max(1,n):.1f}%")
    for k in ("a", "b"):
        v = banks[k]
        if v:
            print(f"   {k.upper()} mean bank {statistics.mean(v):>12,.0f}   "
                  f"median {statistics.median(v):>12,.0f}")


if __name__ == "__main__":
    main()
