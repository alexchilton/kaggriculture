"""Play the imported public agents against each other on the official engine.

Two artifacts, both Apache-2.0 and both carrying yhay81's 13 route tapes:
  submission/shop0909/main.py  -- Yusuke Hayashi's Shop Router 0909, unmodified
  submission/e182/main.py      -- Dmitrii Gluzdov's 7-turn terminal rescue on top of it

Seats are swapped on every seed, so a win here is not a seat artifact.
"""
import argparse
import json
import sys
import time
from pathlib import Path

from kaggle_environments import make

ROOT = Path(__file__).resolve().parent.parent


def play(seed, left, right):
    env = make("kaggriculture", configuration={"seed": seed}, debug=True)
    env.run([str(left), str(right)])
    return [s["reward"] for s in env.steps[-1]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[11, 4242, 70683142, 244615642])
    ap.add_argument("--left", default="submission/e182/main.py")
    ap.add_argument("--right", default="submission/shop0909/main.py")
    ap.add_argument("--out", default="data/logs/smoke_shop0909.csv")
    args = ap.parse_args()

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as fh:
        fh.write("seed,left_seat,left_reward,right_reward,margin,winner\n")
        fh.flush()
        wins = 0
        games = 0
        for seed in args.seeds:
            for left_seat in (0, 1):
                a, b = ROOT / args.left, ROOT / args.right
                pair = [a, b] if left_seat == 0 else [b, a]
                t0 = time.time()
                rewards = play(seed, *pair)
                lr = rewards[left_seat]
                rr = rewards[1 - left_seat]
                games += 1
                wins += lr > rr
                fh.write(f"{seed},{left_seat},{lr},{rr},{lr - rr},{'left' if lr > rr else 'right'}\n")
                fh.flush()
                print(f"seed={seed} left_seat={left_seat} left={lr} right={rr} "
                      f"margin={lr - rr:+} {time.time() - t0:.0f}s", flush=True)
        print(f"left wins {wins}/{games}", flush=True)


if __name__ == "__main__":
    main()
