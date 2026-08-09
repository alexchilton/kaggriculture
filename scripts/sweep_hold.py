"""Run probe_hold across seeds x arms in parallel and print one aggregate table per arm."""

import argparse
import collections
import concurrent.futures as cf
import json
import subprocess
import sys


def one(seed, handover, sets, weeds):
    cmd = [sys.executable, "-u", "scripts/probe_hold.py", "--seed", str(seed),
           "--handover", str(handover), "--weeds", str(weeds), "--json"]
    for s in sets:
        cmd += ["--set", s]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        return seed, {"error": out.stderr[-800:]}
    return seed, json.loads(out.stdout.strip().splitlines()[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="11,12,13,14,15,16,17,18")
    ap.add_argument("--handover", type=int, default=0)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--arm", action="append", default=[],
                    help="NAME:SET=VAL,SET=VAL   (SET=VAL are JSON values)")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    seeds = [int(s) for s in a.seeds.split(",")]
    arms = []
    for spec in a.arm or ["base:"]:
        name, _, body = spec.partition(":")
        arms.append((name, [s for s in body.split(",") if s]))

    print(f"seeds={seeds} handover={a.handover} weeds={a.weeds}")
    print("%-22s %9s %9s %8s %8s %10s %10s %10s"
          % ("arm", "money", "sd", "lost", "escapes", "unfed", "wbuy", "wnet"))
    base = {}
    for name, sets in arms:
        res = {}
        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            for seed, r in ex.map(lambda s: one(s, a.handover, sets, a.weeds), seeds):
                res[seed] = r
        bad = {s: r for s, r in res.items() if "error" in r}
        if bad:
            print(name, "ERRORS", list(bad)[:2], list(bad.values())[0]["error"][:400])
            continue
        agg = collections.Counter()
        for r in res.values():
            for k in ("lost", "escapes", "unfed", "wbuy", "wsell", "wcost", "wrev", "money"):
                agg[k] += r[k]
        n = len(res)
        mean = agg["money"] / n
        sd = (sum((r["money"] - mean) ** 2 for r in res.values()) / max(1, n - 1)) ** 0.5
        wnet = agg["wrev"] - agg["wcost"]
        print("%-22s %9.0f %9.0f %8d %8d %10d %10d %10.0f"
              % (name, mean, sd, agg["lost"], agg["escapes"], agg["unfed"], agg["wbuy"], wnet))
        if not base:
            base = dict(res)
        else:
            d = [res[s]["money"] - base[s]["money"] for s in seeds]
            md = sum(d) / len(d)
            sdd = (sum((x - md) ** 2 for x in d) / max(1, len(d) - 1)) ** 0.5
            se = sdd / len(d) ** 0.5
            won = sum(1 for v in d if v > 0)
            print("%-22s   PAIRED money delta vs first arm: %+.0f +/- %.0f (SE), better on %d/%d"
                  % ("", md, se, won, len(seeds)))


if __name__ == "__main__":
    main()
