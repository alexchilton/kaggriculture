"""Which animals the tape bundle loses, on which day, and what it failed to feed them.

The functional probe showed the four-quadrant arm BUYS `COW 6 / SHEEP 12` and stands `3/11` at d29
-- four to five head lost. This says which day each one went and what the board looked like that day.

An animal is removed when it goes unfed for long enough (`consecutive_unfed` in
`_daily_refresh_animals`), so a loss on day D is a FEED that did not happen on D-1 or earlier, not a
mistake made on D. The columns are therefore printed with the feed count of the days BEFORE the loss.

Read against the tape's own game, which is the point: the tape fed these animals successfully on the
board it was recorded on. Anything it loses here it loses because the FOREIGN seed moved something
-- a refused purchase, a shop that had not unlocked, a contested fill -- and the recorded feed
schedule no longer matches the herd that actually exists.

    python -u scripts/where_the_animals_die.py --seeds 3 17
"""
import argparse
import collections
import importlib.util
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

IDLE = {"farmer": ["PASS"], "hands": [], "market": []}


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, str(REPO / path))
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


def herd_of(obs, seat):
    """`(x, y) -> species` for every animal standing in a pen, plus its hunger counter."""
    out = {}
    for y, row in enumerate(obs["farms"][seat]["tiles"]):
        for x, t in enumerate(row):
            if isinstance(t, dict) and t.get("animal"):
                out[(x, y)] = (t["animal"], int(t.get("consecutive_unfed", 0) or 0))
    return out


def one(seed, opponent, weeds, days):
    from kaggle_environments import make

    bundle = load("submission/main_tape.py", f"tape_{seed}_{opponent}")
    if opponent == "idle":
        opp = lambda o, t: IDLE                                    # noqa: E731
    else:
        mod = load("data/sweep/frozen_1186_opponent.py", f"opp_{seed}")
        opp = lambda o, t: mod.agent(o, None)                      # noqa: E731

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=False)
    env.reset(2)
    feeds = collections.Counter()          # day -> FEED ops we submitted
    bought = collections.Counter()         # day -> animals that arrived
    losses = []                            # (day, species, tile, unfed at last sight)
    prev = {}
    for t in range(719):
        o0 = env.state[0].observation
        day = t // 24
        cur = herd_of(o0, 0)
        if t % 24 == 0:
            for tile, (sp, unfed) in prev.items():
                if tile not in cur:
                    losses.append((day, sp, tile, unfed))
            prev = cur
        else:
            prev = cur
        act = bundle.agent(o0, None)
        for op in [act.get("farmer")] + list(act.get("hands") or []):
            if op and op[0] == "FEED":
                feeds[day] += 1
        for order in act.get("market") or []:
            if order[0] == "BUY_ANIMAL":
                bought[day] += order[2]
        env.step([act, opp(env.state[1].observation, t)])
        if env.done:
            break

    st = bundle._STATE.get(0, {})
    return dict(seed=seed, opponent=opponent, straw=st.get("straw"), q4=st.get("q4"),
                feeds=feeds, bought=bought, losses=losses, standing=len(prev), days=days)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[3, 17])
    ap.add_argument("--opponents", nargs="+", default=["frozen"])
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()

    for seed in a.seeds:
        for opponent in a.opponents:
            r = one(seed, opponent, a.weeds, a.days)
            head = sum(r["bought"].values())
            print(f"\n=== seed {r['seed']} vs {opponent}   straw={r['straw']} q4={r['q4']}   "
                  f"bought {head}, standing at the end {r['standing']}, lost {len(r['losses'])}")
            if not r["losses"]:
                print("    nothing lost")
                continue
            print(f"    {'day':>5}{'species':>9}{'tile':>9}{'unfed':>7}   "
                  f"feeds on the three days before")
            for day, sp, tile, unfed in r["losses"]:
                before = " ".join(f"d{d}:{r['feeds'].get(d, 0)}" for d in range(max(0, day - 3), day))
                print(f"    {day:>5}{sp:>9}{str(tile):>9}{unfed:>7}   {before}")
            print(f"\n    herd size by day, and the feeds it got:")
            live, line1, line2 = 0, [], []
            for d in range(a.days):
                live += r["bought"].get(d, 0)
                live -= sum(1 for (dd, *_rest) in r["losses"] if dd == d)
                line1.append(f"{live:>3}")
                line2.append(f"{r['feeds'].get(d, 0):>3}")
            print("      day   " + "".join(f"{d:>3}" for d in range(a.days)))
            print("      herd  " + "".join(line1))
            print("      feeds " + "".join(line2))
            print("    A pen needs one FEED per animal per day; feeds below herd is the shortfall.")


if __name__ == "__main__":
    main()
