"""Print the d0-d8 grid with the melon fork forced ON and forced OFF, on several seeds.

The fork is `melon_branch.arm`, gated on the opponent holding
`melon_branch.OPPONENT_MELON` (9) melon tiles at `DECIDE_BY_DAY` (3). The tape opponent
holds 12, so it fires by default; forcing it off means raising the threshold out of reach.

Only the threshold moves between the two arms. Nothing else.

    python -u scripts/fork_grid.py --seeds 11 3 7 --days 8
"""
import argparse
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from kagg.search import melon_branch as _MB

ROWS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "DIG",
        "BUILD_PASTURE", "PLACE", "FERTILIZE", "BUY_SEED", "BUY_ANIMAL", "BUY_LAND", "HIRE",
        "SELL", "crop_MELON", "crop_STRAWBERRY", "crop_WHEAT", "weed", "pen", "money")


def one(seed, days, threshold):
    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    _MB.OPPONENT_MELON = threshold
    B.schedule_agent = SA
    replay, schedule, team = B.TAPES["kawashigi"]
    raw = json.loads((REPO / schedule).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    opp = lambda: B.tape_policy(str(REPO / replay), team, 1)          # noqa: E731

    def ours():
        a = SA.make_agent(sched, 0)
        return lambda o, t: a(o)

    d, ops, _c, _dawn = B.run(ours, opp, seed, 0.005, stop_day=days + 1)
    return d, ops


def child(seed, days, threshold):
    """One OS process per arm: the first run in a process differs from later ones."""
    import subprocess
    out = subprocess.run([sys.executable, "-u", __file__, "--child",
                          str(seed), str(days), str(threshold)],
                         capture_output=True, text=True, cwd=str(REPO))
    if out.returncode:
        raise SystemExit(out.stderr[-2000:])
    return json.loads(out.stdout)


def main():
    if "--child" in sys.argv:
        i = sys.argv.index("--child")
        seed, days, threshold = (int(x) for x in sys.argv[i + 1:i + 4])
        d, ops = one(seed, days, threshold)
        print(json.dumps([[dict(x) for x in d], [dict(ops[k]) for k in sorted(ops)]]))
        return

    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[11, 3, 7])
    ap.add_argument("--days", type=int, default=8)
    a = ap.parse_args()

    for seed in a.seeds:
        on_d, on_o = child(seed, a.days, 0)          # threshold 0 -> always fires
        off_d, off_o = child(seed, a.days, 99)       # threshold 99 -> never fires
        print(f"\n===== seed {seed}, weeds 0.005, d0-d{a.days}      melon+ = fork ON "
              f"(strawberry), melon- = fork OFF")
        head = "".join(f"{'d' + str(d):>11}" for d in range(a.days + 1))
        print(f"{'row':>20}{head}")
        for r in ROWS:
            def val(dd, oo, day):
                return (oo[day] if r.isupper() else dd[day]).get(r, 0)
            hi = [val(on_d, on_o, d) for d in range(a.days + 1)]
            lo = [val(off_d, off_o, d) for d in range(a.days + 1)]
            cells = "".join(f"{str(x) + '/' + str(y):>11}" for x, y in zip(hi, lo))
            mark = "   <-- differs" if hi != lo else ""
            print(f"{r:>20}{cells}{mark}")
        print("   cells are melon+/melon-  (fork ON / fork OFF)")


if __name__ == "__main__":
    main()
