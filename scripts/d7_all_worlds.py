"""d7 on EVERY world, with that world's own schedule. The gate: d7 must match on all of them.

Each arm is one recorded season: its replay plays d0-d6, our planner takes over at d7, and the rows
are that same season's LANDED rows (`seeds` from `plants`, `buys`/`sells` from engine fills). Pairing
the replay with a DIFFERENT season's rows would compare a board against rows it was not built for,
so the pairing is one-to-one by construction.

Writes one CSV per world and prints d7's differing fields per world, so a fault common to all eight
is separable from one that is world-specific.
"""
import argparse, csv, json, multiprocessing, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

RUNNER = '''import sys
sys.path.insert(0, {root!r})
sys.argv = ["breakdown.py", "--tape", {tape!r}, "--handover", "7", "--days", {days!r},
            "--diff", "--seed", {seed!r}, "--csv", {csv!r}]
from kagg.search import schedule_agent as SA
SA.REPLAY_OPENING_DAYS = ()          # the pure planner from the handover on
import runpy
runpy.run_path({bd!r}, run_name="__main__")
'''


def one(args):
    tape, days, seed = args
    out = ROOT / f"data/logs/w_{tape}.csv"
    log = ROOT / f"data/logs/w_{tape}.log"
    script = ROOT / f"data/logs/w_{tape}_run.py"
    script.write_text(RUNNER.format(root=str(ROOT), tape=tape, days=str(days), seed=str(seed),
                                    csv=str(out), bd=str(ROOT / "scripts/breakdown.py")))
    with open(log, "w") as fh:
        r = subprocess.run([str(ROOT / ".venv-sub/bin/python"), "-u", str(script)],
                           stdout=fh, stderr=subprocess.STDOUT, cwd=str(ROOT))
    return tape, r.returncode, str(out), str(log)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tapes", nargs="+", default=None)
    ap.add_argument("--days", type=int, default=8)
    ap.add_argument("--seed", type=int, default=666671489)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()

    sys.path.insert(0, str(ROOT))
    import scripts.breakdown as B
    tapes = a.tapes or sorted(k for k in B.TAPES if k.startswith("spa"))

    with multiprocessing.Pool(a.jobs) as pool:
        done = pool.map(one, [(t, a.days, a.seed) for t in tapes])

    print(f"\n{'world':14s} {'exit':>4s} {'d0-d6':>6s} {'d7 cells':>9s}   d7 fields that differ")
    for tape, rc, out, log in done:
        verdict = ""
        for line in pathlib.Path(log).read_text().splitlines():
            if "per-day differing cells" in line:
                verdict = line.strip()
        early = d7 = "?"
        if verdict:
            bits = dict(x.split("=") for x in verdict.split(":")[1].split())
            early = "exact" if all(int(bits.get(f"d{i}", 1)) == 0 for i in range(7)) else "DIFFERS"
            d7 = bits.get("d7", "?")
        fields = []
        p = pathlib.Path(out)
        if p.exists():
            rows = list(csv.DictReader(open(p)))
            r = next((x for x in rows if x.get("day") == "7"), None)
            if r:
                for b in sorted(set(k.rsplit(".", 1)[0] for k in r if "." in k)):
                    if r.get(b + ".ours") != r.get(b + ".tape"):
                        fields.append(f"{b.split('.')[-1]} {r[b+'.ours']}/{r[b+'.tape']}")
        print(f"{tape:14s} {rc:>4d} {early:>6s} {d7:>9s}   " + "  ".join(fields[:6]))
        if len(fields) > 6:
            print(f"{'':38s}   " + "  ".join(fields[6:]))


if __name__ == "__main__":
    main()
