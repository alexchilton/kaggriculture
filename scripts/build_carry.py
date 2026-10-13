"""carry% of OUR build, measured the same way as the ladder players'.

Goods in a hand's inventory cannot be sold; only DROP moves them to the shed. Measured over recorded
seasons: Majkel1337 carries 38-43% of its stock, mtmr_s1 48-60%, binghua 91%. The low-carry farms
bank more, and the gap is the delivery policy, not the market layer.

This runs our own submission build and reads the same quantity, so the comparison is like for like.

    python -u scripts/build_carry.py submission/v38_ours/main.py
"""
import collections, importlib.util, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def load(path, name):
    p = pathlib.Path(path).resolve()
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    old = sys.path[:]
    sys.path.insert(0, str(p.parent))
    try:
        spec.loader.exec_module(m)
    finally:
        sys.path[:] = old
    return m.agent


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "submission/v38_ours/main.py"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    a = load(path, "sub")
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.005}, debug=False)
    env.reset(2)
    carry, shed = collections.Counter(), collections.Counter()
    ops = collections.Counter()

    def watched(obs, cfg=None):
        priv = obs.get("private") or {}
        for iv in priv.get("inventories") or []:
            for k, v in (iv or {}).items():
                carry[k] += int(v or 0)
        for k, v in (priv.get("shed") or {}).items():
            shed[k] += int(v or 0)
        act = a(obs, cfg)
        for op in [act.get("farmer")] + list(act.get("hands") or []):
            if op:
                ops[op[0]] += 1
        return act

    env.run([watched, a])
    tot_c, tot_s = sum(carry.values()), sum(shed.values())
    print(f"build: {path}   seed {seed}")
    print(f"bank {env.state[0].observation['farms'][0]['money']:,.0f}")
    print(f"\ncarry%  {100*tot_c/max(1,tot_c+tot_s):.1f}   "
          f"(carried {tot_c:,} turn-units, shed {tot_s:,})")
    print(f"   reference: Majkel1337 38-43%, mtmr_s1 48-60%, binghua 91%")
    print(f"\nDROP {ops['DROP']}   PASS {ops['PASS']}   HARVEST {ops['HARVEST']}   "
          f"PICKUP {ops['PICKUP']}")
    print(f"   reference PASS: Majkel1337 61-91, mtmr_s1 403-504, binghua 1,109")
    print(f"\n{'product':12}{'carry%':>8}{'shed':>10}")
    for p in sorted(set(carry) | set(shed)):
        t = carry[p] + shed[p]
        if t > 200:
            print(f"{p:12}{100*carry[p]/t:>8.0f}{shed[p]:>10,}")


if __name__ == "__main__":
    main()
