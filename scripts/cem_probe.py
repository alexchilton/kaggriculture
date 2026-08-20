"""Does the objective discriminate at all? Two questions, both gating the CEM design.

1. **Time**, which sizes population x generations x seeds.
2. **Discrimination.** Measured 2026-08-15: the shipped agent wins **100%** of its games against
   every member of `pool.OPPONENTS` except `mirror`, which it draws 100% of the time because it is
   the same file playing itself in a deterministic environment. So the pool's win rate is a constant
   and cannot rank anything. An Elo objective needs an opponent that can actually beat us, and the
   strongest one available is a FROZEN copy of the shipped agent itself.

`--mode discriminate` scores a handful of hand-picked dial vectors against a frozen shipped agent
and against two pool guards, and prints them side by side. If the frozen column is also constant,
there is no objective here and the CEM should not be run.
"""
import argparse
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

sys.path.insert(0, str(REPO / "scripts"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="discriminate", choices=["time", "discriminate"])
    ap.add_argument("--seeds", type=int, nargs="+", default=[301, 302, 303, 304])
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args()

    from cem_allocation import BASELINE, label, write_candidate
    from kagg.arena import pool

    if a.mode == "time":
        cand = write_candidate(BASELINE)
        for i in range(2):
            t0 = time.time()
            r = pool.evaluate(cand, a.seeds[:2], opponents=("mirror", "carrot_25"), workers=a.workers)
            n = 2 * 2 * 2
            print(f"call {i}: {n} games in {time.time() - t0:.1f}s  win {r.win_rate:.4f} "
                  f"draw {r.draw_rate:.4f} mean ${r.mean_money:,.1f}", flush=True)
            print(f"   per_opponent {sorted(r.per_opponent.items())}", flush=True)
        return

    # The frozen bar: the shipped dials, in the same unsolved routing regime as every candidate.
    pool.OPPONENTS["shipped"] = write_candidate(BASELINE)
    field = ("shipped", "carrot_25", "melon_heavy")

    probes = [
        BASELINE,               # must draw itself exactly, or the harness is not deterministic
        (0, 0, 0, 0, 0, 0),     # fork off: MELON 20 / STRAWBERRY 34, Kawashigi's own allocation
        (1, 0, 0, 0, 4, 0),     # today's prior: strawberry down 4
        (1, 4, 0, 0, 0, 0),     # today's prior: melon up 4
        (1, 0, 0, 8, 0, 0),     # carrot, the crop the balance change repriced hardest
        (1, 0, 0, 0, 0, 2),     # geese
    ]
    print(f"field {field}   seeds {a.seeds}   "
          f"{len(a.seeds) * len(field) * 2} games per row\n", flush=True)
    print(f"  {'config':<26}{'elo':>7}{'win':>7}{'money':>12}   per-opponent elo", flush=True)
    for v in probes:
        t0 = time.time()
        r = pool.evaluate(write_candidate(v), a.seeds, opponents=field, workers=a.workers)
        elo = r.win_rate + 0.5 * r.draw_rate
        per = "  ".join(f"{k}:{w:.2f}/${m:,.0f}" for k, (w, m) in sorted(r.per_opponent.items()))
        print(f"  {label(v):<26}{elo:>7.3f}{r.win_rate:>7.3f}{r.mean_money:>12,.0f}   {per}"
              f"   [{time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
