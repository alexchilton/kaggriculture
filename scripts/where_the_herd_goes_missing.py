"""The herd, day by day, ours against the tape's, on the same seed.

The season aggregate says we end with thirteen animals and the tape with fourteen, which reads like a
one-animal gap and cannot be worth $35,000. A season total hides WHEN: an animal that arrives on day 4
earns milk for twenty-six days, the same animal bought on day 18 earns for twelve. The two farms can
finish level and be nowhere near level.

So this prints, per day and for both arms:

    alive       animals on the board at dawn, after the overnight refresh has taken escapes
    pens        empty structures waiting for an occupant -- a built pen with no animal is rent paid
                for nothing, and the difference `pens - alive` is capacity we bought and never used
    place       animals put down that day
    escape      alive(d-1) + place(d-1) - alive(d), i.e. animals lost to two unfed days
    animal ops  FEED / CARE / COLLECT emitted that day

`animal-days` at the foot is the number that matters: the integral of `alive` over the season, which
is what actually converts into milk and wool. One animal short for thirty days and fourteen animals
arriving a week late are the same shortfall in a season total and completely different bugs.
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import schedule_agent
import agent_ladder as L

ANIMAL_OPS = ("FEED", "CARE", "COLLECT_PRODUCE")


def _count(tiles, pred):
    return sum(1 for row in tiles for c in row if isinstance(c, dict) and pred(c))


def run(seed, make_us=None, tape=None, theirs=None):
    """One season; returns {day: dict(alive, pens, place, ops)} sampled at dawn."""
    env = L._env(seed, 0.0)
    us = make_us() if make_us else None
    rows, place, ops = {}, collections.Counter(), collections.Counter()
    for t in range(719):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        farm = obs["farms"][0]
        if hour == 0:
            tiles = farm["tiles"]
            rows[day] = dict(
                alive=_count(tiles, lambda c: "animal" in c),
                pens=_count(tiles, lambda c: c.get("kind") in ("PASTURE", "COOP")),
                money=int(farm["money"]),
            )
        if us is not None:
            a = us(obs)
            f0, h0, m0 = a["farmer"], a["hands"], a["market"]
        else:
            f0, h0, m0 = tape[t] if t < len(tape) else (["PASS"], [], [])
        n0 = len(farm.get("hands") or [])
        for act in [f0, *list(h0)[:n0]]:
            if not (isinstance(act, list) and act):
                continue
            if act[0] == "PLACE":
                place[day] += 1
            elif act[0] in ANIMAL_OPS:
                ops[day] += 1
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": f0, "hands": list(h0)[:n0], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    for d, r in rows.items():
        r["place"] = place[d]
        r["ops"] = ops[d]
    # An escape is the only way `alive` can fall, so it is recoverable from the dawn counts alone.
    for d in sorted(rows):
        prev = rows.get(d - 1)
        rows[d]["escape"] = max(0, prev["alive"] + prev["place"] - rows[d]["alive"]) if prev else 0
    return rows, float(env.state[0].observation["farms"][0]["money"])


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    mine, theirs = L.tape_plans()
    sched = {int(k): v for k, v in json.loads(pathlib.Path(L.SCHEDULE).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    tape_rows, tape_money = run(seed, tape=mine, theirs=theirs)
    our_rows, our_money = run(seed, make_us=lambda: schedule_agent.make_agent(sched, 0, router=True),
                              theirs=theirs)

    print(f"seed {seed}   tape ${tape_money:,.0f}   ours ${our_money:,.0f} "
          f"({100 * our_money / tape_money:.0f}%)\n")
    head = (f"{'':>4} {'ALIVE':>11} {'PENS':>11} {'PLACE':>11} {'ESCAPE':>11} "
            f"{'ANIMAL OPS':>13} {'MONEY':>19}")
    print(head)
    print(f"{'day':>4} {'ours':>5}{'tape':>6} {'ours':>5}{'tape':>6} {'ours':>5}{'tape':>6} "
          f"{'ours':>5}{'tape':>6} {'ours':>6}{'tape':>7} {'ours':>9}{'tape':>10}")
    tot = collections.Counter()
    for d in sorted(set(our_rows) | set(tape_rows)):
        o = our_rows.get(d, {})
        t = tape_rows.get(d, {})
        g = lambda r, k: int(r.get(k, 0))
        for k in ("alive", "place", "escape", "ops"):
            tot["o_" + k] += g(o, k)
            tot["t_" + k] += g(t, k)
        tot["o_pens"] += g(o, "pens")
        tot["t_pens"] += g(t, "pens")
        print(f"{d:>4} {g(o,'alive'):>5}{g(t,'alive'):>6} {g(o,'pens'):>5}{g(t,'pens'):>6} "
              f"{g(o,'place'):>5}{g(t,'place'):>6} {g(o,'escape'):>5}{g(t,'escape'):>6} "
              f"{g(o,'ops'):>6}{g(t,'ops'):>7} {g(o,'money'):>9,}{g(t,'money'):>10,}")
    print(f"\n  animal-days (sum of alive)     ours {tot['o_alive']:>6}   tape {tot['t_alive']:>6}"
          f"   {100 * tot['o_alive'] / max(1, tot['t_alive']):>5.0f}%")
    print(f"  pen-days     (sum of pens)     ours {tot['o_pens']:>6}   tape {tot['t_pens']:>6}")
    print(f"  animals placed                 ours {tot['o_place']:>6}   tape {tot['t_place']:>6}")
    print(f"  animals escaped                ours {tot['o_escape']:>6}   tape {tot['t_escape']:>6}")
    print(f"  animal ops                     ours {tot['o_ops']:>6}   tape {tot['t_ops']:>6}")


if __name__ == "__main__":
    main()
