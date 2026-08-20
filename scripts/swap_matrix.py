"""Drive `swap_one_crop.py` over a matrix of (src, dst, n, seed), one OS process per cell.

Every cell is a separate `python` invocation on purpose. Measured 2026-08-15: the same config run
four times inside one process gave $134,665 then $94,523 three times -- the FIRST run in a process
differs -- so any in-process loop measures run order rather than the config. That finding is what
this file exists to obey; do not "optimise" it into a loop.

## What the matrix can and cannot ask

The source must be a crop the shipped schedule still plants on the swap day, or there is nothing to
re-crew and the cell is a silent no-op. From d12 onward that is WHEAT (6-14 stops a day) and, thinly,
STRAWBERRY (7 on d12, then 1/day). MELON is planted d0/d6/d7 and is therefore untestable from d12 --
testing it means unsolving the route from d6, which changes the executor as well as the crop and
confounds the cell.

The destination must be able to complete a cycle from the swap day. `swap_one_crop.LATEST_PLANTING`
refuses the cell otherwise:

    CARROT plant by d26   STRAWBERRY plant by d13   MELON plant by d17
    WHEAT  plant by d25   TOMATO     plant by d18

Routes are live from d12 in EVERY cell including the baseline, so the executor handicap is paid
equally and the difference between two cells is the crop.

Each cell reports its substitute's collection rate. A cell whose substitute was collected at 30% is
a routing result wearing a crop's name, and its money figure says nothing about the crop.

    python -u scripts/swap_matrix.py --seeds 3 7 11 15 19 --workers 6
"""
import argparse
import collections
import json
import pathlib
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent

#: Each cell is a `--shifts` spec. **The dose curve first, one tile at a time.** A crop that helps
#: at 8 tiles and not at 1 is a different claim from one that helps linearly, and only the ladder
#: from 1 tells them apart. Then the combinations, because the crops compete for the same crew turns
#: and the same water: one tomato beside one carrot is not the sum of the two cells above it.
DOSES = (1, 2, 3, 4, 8)
SUBS = ("TOMATO", "CARROT", "STRAWBERRY", "MELON")

CELLS = [""]                                            # baseline
for _dst in SUBS:
    for _n in DOSES:
        CELLS.append(f"WHEAT:{_dst}:{_n}")
# pairs, one tile of each, off wheat -- the cheapest possible combination
for _i, _a in enumerate(SUBS):
    for _b in SUBS[_i + 1:]:
        CELLS.append(f"WHEAT:{_a}:1,WHEAT:{_b}:1")
        CELLS.append(f"WHEAT:{_a}:2,WHEAT:{_b}:2")
# the two crops the top players actually fix, taken off strawberry instead of wheat
CELLS += ["STRAWBERRY:TOMATO:2", "STRAWBERRY:CARROT:2", "STRAWBERRY:WHEAT:4",
          "WHEAT:TOMATO:2,STRAWBERRY:TOMATO:2", "WHEAT:TOMATO:1,WHEAT:CARROT:1,WHEAT:MELON:1"]


def label(spec):
    if not spec:
        return "baseline"
    return " + ".join(f"{d.lower()}x{n}<{s[:2].lower()}"
                      for s, d, n in (p.split(":") for p in spec.split(",")))


def one(seed, spec, day, opponent):
    cmd = [sys.executable, "-u", "scripts/swap_one_crop.py", "--seed", str(seed),
           "--day", str(day), "--json", "--opponent", opponent]
    if spec:
        cmd += ["--shifts", spec]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO,
                       env={**__import__("os").environ, "PYTHONPATH": "."})
    out = p.stdout.strip()
    if not out or out.startswith("REFUSED"):
        return dict(seed=seed, label=label(spec), failed=out or p.stderr[-300:])
    r = json.loads(out.splitlines()[-1])
    r["label"] = label(spec)
    r["secs"] = time.time() - t0
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[3, 7, 11, 15, 19])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--day", type=int, default=12)
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    ap.add_argument("--out", default="data/logs/swap_matrix.json")
    a = ap.parse_args()

    jobs = [(s, c) for s in a.seeds for c in CELLS]
    print(f"{len(jobs)} cells = {len(CELLS)} configs x {len(a.seeds)} seeds, "
          f"{a.workers} workers, opponent {a.opponent}", flush=True)

    rows = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(one, s, c, a.day, a.opponent) for s, c in jobs]
        for f in futs:
            r = f.result()
            rows.append(r)
            if r.get("failed"):
                print(f"  seed {r['seed']:>3} {r['label']:<34} FAILED {r['failed'][:120]}",
                      flush=True)
            else:
                got = "  ".join(
                    f"{d[:4].lower()} {r['collected'].get(d,0)}/{r['grown'].get(d,0)}"
                    for d in r["dsts"])
                print(f"  seed {r['seed']:>3} {r['label']:<34} ${r['money']:>10,.0f}  "
                      f"opp ${r['opp_money']:>9,.0f}   {got:<28}[{r['secs']:.0f}s]", flush=True)
            json.dump(rows, open(REPO / a.out, "w"), indent=1)

    # ------------------------------------------------------------------------------- the table
    base = {r["seed"]: r["money"] for r in rows if r.get("label") == "baseline"}
    by = collections.defaultdict(list)
    for r in rows:
        if r.get("failed") or r["label"] == "baseline":
            continue
        by[r["label"]].append(r)

    print(f"\n{'config':<34}" + "".join(f"{s:>10}" for s in a.seeds) +
          f"{'mean d':>10}{'wins':>7}{'collect':>9}")
    print(f"{'baseline $':<34}" + "".join(f"{base.get(s,0):>10,.0f}" for s in a.seeds))
    out = []
    for lab, rs in sorted(by.items()):
        d = {r["seed"]: r["money"] - base.get(r["seed"], r["money"]) for r in rs}
        mean = sum(d.values()) / len(d)
        wins = sum(1 for r in rs if r["money"] > r["opp_money"])
        tg = sum(r["grown"].get(x, 0) for r in rs for x in r["dsts"])
        tc = sum(r["collected"].get(x, 0) for r in rs for x in r["dsts"])
        print(f"{lab:<34}" + "".join(f"{d.get(s, 0):>+10,.0f}" for s in a.seeds) +
              f"{mean:>+10,.0f}{wins:>4}/{len(rs)}"
              f"{(f'{tc/tg:.0%}' if tg else '-'):>9}")
        out.append((lab, mean, wins, len(rs)))

    print("\nbaseline wins: "
          f"{sum(1 for r in rows if r.get('label') == 'baseline' and r['money'] > r['opp_money'])}"
          f"/{len(base)}")
    if out:
        best = max(out, key=lambda x: x[1])
        print(f"best by mean money: {best[0]}  {best[1]:+,.0f}  wins {best[2]}/{best[3]}")
    print("\nThe ladder is Elo. Money here is the SCREEN; anything that survives it has to be "
          "confirmed on win rate against the pool before it ships.")


if __name__ == "__main__":
    main()
