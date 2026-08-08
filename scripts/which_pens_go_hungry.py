"""Two sheep escape on day 16. Is the feed short, or is it just aimed at the wrong pens?

`reference/kaggriculture.py:786` -- an animal whose `consecutive_unfed` reaches 2 escapes and leaves
its structure behind. So two of ours missed two days running, ending d16.

The season diff says `feed -4` and `pens` identical from d7 on, i.e. we emit nearly the same number
of FEED ops as the tape across the same nineteen pens. If that holds, "the cadence cannot carry 19
pens" is the wrong diagnosis and the real fault is DISTRIBUTION -- some pens fed twice while two are
missed.

Prints, for every day, how many pens exist, how many were fed, and the `consecutive_unfed` of every
pen that is carrying a hungry day. A pen at 1 is one day from escaping.
"""
import json
import pathlib
import sys

sys.path.insert(0, "/Users/alexchilton/DataspellProjects/kaggriculture")

from kaggle_environments import make

from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

DAYS = 20
replay, schedule, team = TAPES["seb"]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def pens(obs):
    """(x, y) -> (animal, consecutive_unfed, fed_today) for every occupied pen."""
    out = {}
    for y, row in enumerate(obs["farms"][0]["tiles"]):
        for x, cell in enumerate(row):
            if isinstance(cell, dict) and cell.get("animal"):
                out[(x, y)] = (cell["animal"], int(cell.get("consecutive_unfed", 0)),
                               bool(cell.get("fed_today")))
    return out


def run(make_seat0, label):
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    p0 = make_seat0()
    opp = tape_policy(replay, team, 1)
    print(f"\n===== {label} =====")
    print("  day  pens  FEED_ops  fed_today  hungry (pen -> consecutive_unfed)")
    feeds = 0
    for t in range(24 * DAYS - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        for act in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if act and act[0] == "FEED":
                feeds += 1
        # Read the pens at the LAST turn of the day, before the rollover clears `fed_today`
        # and before an unfed animal is removed.
        last = (t % 24 == 23)
        snap = pens(env.state[0].observation) if last else None
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
        if last:
            fed = sum(1 for _, (_, _, f) in snap.items() if f)
            hungry = {p: c for p, (_, c, f) in snap.items() if not f}
            after = pens(env.state[0].observation)
            lost = sorted(set(snap) - set(after))
            print(f"  d{t // 24:<3} {len(snap):>4}  {feeds:>8}  {fed:>9}  "
                  f"{sorted(hungry.items()) if hungry else ''}"
                  f"{'   ESCAPED: ' + str(lost) if lost else ''}")
            feeds = 0


run(lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True)), "OURS")
run(lambda: tape_policy(replay, team, 0), "SEB (the tape)")
