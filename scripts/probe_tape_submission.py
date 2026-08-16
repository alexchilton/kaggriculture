"""Does the tape bundle actually PLAY -- does it split where it should, and land the right board?

Not a win rate. This asks four functional questions and nothing else:

  1. does each decision fire when it should, and stay quiet when it should not
  2. does the board that results carry the SHAPE of the tape that was chosen
  3. do the tape's purchases actually FILL on a foreign seed, or get refused
  4. does it reach day 29 without desynchronising into PASS

The two decisions need opposite opponents to exercise, and that is the point of the matrix:

    frozen   `data/sweep/frozen_1186_opponent.py` plays the leader's own schedule and holds 12
             MELON tiles at dawn on d3 on every seed -> the d3 fork ALWAYS fires
    idle     PASS every turn, 0 melon                -> the d3 fork NEVER fires

So the fork is exercised in both directions by choosing the opponent, not by hunting for a seed.
The quadrant branch is exercised by the seed: YARN_STORE unlocks by d6 on 15 of the first 100.

Expected shapes, read off the tapes themselves rather than asserted from memory:

    A3  91919278   MELON 20 / STRAWBERRY 34   COW 10 / SHEEP 4    3 quadrants
    B3  91891131   MELON 12 / STRAWBERRY 42   COW  8 / SHEEP 6    3 quadrants
    Q4  91907974   MELON 20 / STRAWBERRY 34   COW  6 / SHEEP 12   4 quadrants

A tape on a foreign seed plays HANDICAPPED: a shop that has not unlocked refuses its BUY_SEED, and
a purchase is refused when the bank is short, because the market is contested and our fills differ
from the recording's. So the planted counts are an upper bound the tape will not always reach, and
a shortfall is information rather than a bug.

    python -u scripts/probe_tape_submission.py --seeds 3 17 11 7
"""
import argparse
import collections
import importlib.util
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

BUNDLE = "submission/main_tape.py"   # overridden by --bundle
IDLE = {"farmer": ["PASS"], "hands": [], "market": []}


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, str(REPO / path))
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


def board(obs, seat):
    farm = obs["farms"][seat]
    crops, herd, tiles, weeds, pens = collections.Counter(), collections.Counter(), 0, 0, 0
    for row in farm["tiles"]:
        for t in row:
            if t == "LOCKED":
                continue
            tiles += 1
            if isinstance(t, dict):
                if t.get("crop"):
                    crops[t["crop"]] += 1
                elif t.get("kind") == "WEED":
                    weeds += 1
                else:
                    pens += 1
                if t.get("animal"):
                    herd[t["animal"]] += 1
    return crops, herd, tiles, weeds, pens


def one(seed, opponent, weeds, bundle=BUNDLE):
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

    bundle = load(bundle, f"tape_{seed}_{opponent}")
    opp = (lambda o, t: IDLE) if opponent == "idle" else None
    if opp is None:
        mod = load("data/sweep/frozen_1186_opponent.py", f"opp_{seed}")
        opp = lambda o, t: mod.agent(o, None)      # noqa: E731

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=False)
    env.reset(2)
    planted = collections.Counter()
    offered = collections.Counter()
    acted = 0
    with record_fills(env) as fills:
        for t in range(719):
            o0, o1 = env.state[0].observation, env.state[1].observation
            act = bundle.agent(o0, None)
            for op in [act.get("farmer")] + list(act.get("hands") or []):
                if op and op[0] == "PLANT":
                    planted[op[1]] += 1
                if op and op[0] != "PASS":
                    acted += 1
            for order in act.get("market") or []:
                offered[order[0]] += 1
            env.step([act, opp(o1, t)])
            if env.done:
                break
    st = bundle._STATE.get(0, {})
    crops, herd, tiles, weedn, pens = board(env.state[0].observation, 0)
    fin = env.steps[-1]
    return dict(
        seed=seed, opponent=opponent, straw=st.get("straw"), q4=st.get("q4"),
        day=t // 24, tiles=tiles, pens=pens, weeds=weedn,
        planted=dict(planted), crops=dict(crops), herd=dict(herd),
        buy_animal=fills.units(0, "BUY_ANIMAL"), buy_seed=fills.units(0, "BUY_SEED"),
        offered_animal=offered["BUY_ANIMAL"], offered_seed=offered["BUY_SEED"],
        acted=acted, money=fin[0]["reward"], theirs=fin[1]["reward"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[3, 17, 11, 7])
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--bundle", default=BUNDLE)
    a = ap.parse_args()

    print(f"bundle {a.bundle}, weedSpawnChance {a.weeds}\n")
    print(f"{'seed':>5}{'opponent':>9}{'straw':>7}{'q4':>6}{'reach':>7}{'tiles':>7}"
          f"{'planted M/S':>13}{'standing M/S':>14}{'herd C/S':>10}{'seed fills':>11}"
          f"{'ops':>7}{'money':>10}")
    rows = []
    for seed in a.seeds:
        for opponent in ("frozen", "idle"):
            r = one(seed, opponent, a.weeds, a.bundle)
            rows.append(r)
            p, c, h = r["planted"], r["crops"], r["herd"]
            print(f"{r['seed']:>5}{r['opponent']:>9}{str(r['straw']):>7}{str(r['q4']):>6}"
                  f"{'d' + str(r['day']):>7}{r['tiles']:>7}"
                  f"{str(p.get('MELON', 0)) + '/' + str(p.get('STRAWBERRY', 0)):>13}"
                  f"{str(c.get('MELON', 0)) + '/' + str(c.get('STRAWBERRY', 0)):>14}"
                  f"{str(h.get('COW', 0)) + '/' + str(h.get('SHEEP', 0)):>10}"
                  f"{str(r['buy_seed']) + '/' + str(r['offered_seed']):>11}"
                  f"{r['acted']:>7}{r['money']:>10,.0f}", flush=True)

    print("\nplanted M/S is what the tape SUBMITTED; standing M/S is what is alive at the end.")
    print("seed fills is FILLED/OFFERED -- a shop that has not unlocked refuses the buy.\n")
    bad = []
    for r in rows:
        if r["day"] < 29:
            bad.append(f"seed {r['seed']} vs {r['opponent']}: stopped at d{r['day']}, not d29")
        if r["opponent"] == "frozen" and not r["straw"]:
            bad.append(f"seed {r['seed']}: the frozen opponent holds 12 melon at d3 and the fork "
                       f"did NOT fire")
        if r["opponent"] == "idle" and r["straw"]:
            bad.append(f"seed {r['seed']}: an idle opponent holds 0 melon and the fork DID fire")
        if r["q4"] and r["tiles"] < 100:
            bad.append(f"seed {r['seed']} vs {r['opponent']}: armed q4 but ended on {r['tiles']} "
                       f"tiles, not 100")
        if r["acted"] < 2000:
            bad.append(f"seed {r['seed']} vs {r['opponent']}: only {r['acted']} non-PASS ops -- "
                       f"the tape is probably desynchronised")
    for b in bad:
        print("  FAIL " + b)
    print(f"\n{len(bad)} functional problems" if bad else "\nno functional problems")


if __name__ == "__main__":
    main()
