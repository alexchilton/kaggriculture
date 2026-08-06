"""Which unit holds the animal, what is in its route, and whether it ever stands on an empty pen.

Seed 11 day 4 on Seb's plan places no animal while the tape places one -- `PLACE 0 against 1`,
`tile:animal 6 against 7`, on every seed. The per-turn dump showed the cow drawn from the shed at h3
and back in the shed by h19, which was read as "carried all day and never placed". That reading does
not survive a unit test: written three ways, including a mid-day arrival on an eight-unit farm with
six mandatory feeds, the executor places the animal every time.

So the symptom is real and the cause is not known. This prints the one thing the season dump cannot:
per unit, per turn, the animal it carries, the tiles left in its route and the ops each of those
tiles is expected to yield, beside the list of empty pens standing free. If the PLACE is in a route,
the failure is delivery; if it is in nobody's route, the failure is node generation; if it is in the
route of a unit that is not carrying the animal, the failure is the draw-and-place handoff.

Run: python -u scripts/where_the_cow_goes.py 11 --day 4
"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import router as RT
from kagg.search import schedule_agent
import agent_ladder as L

ANIMALS = ("COW", "SHEEP", "GOOSE")


def _state_of(agent):
    """`make_agent` returns a closure; the per-day book-keeping dict is one of its free variables."""
    for cell in agent.__closure__ or ():
        v = cell.cell_contents
        if isinstance(v, dict) and "pins" in v and "routes" in v:
            return v
    raise SystemExit("could not reach the agent's state through its closure")


def _pens(tiles):
    return [(x, y) for y, r in enumerate(tiles) for x, c in enumerate(r)
            if isinstance(c, dict) and c.get("kind") in ("PASTURE", "COOP") and "animal" not in c]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", nargs="?", type=int, default=11)
    ap.add_argument("--day", type=int, default=4)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--replay", default="data/seed_scripts/top_guys/90497592.json")
    ap.add_argument("--team", default="Seb (allegedly)")
    ap.add_argument("--schedule", default="data/seed_scripts/top_guys/90497592/schedule.json")
    args = ap.parse_args()

    sched = {int(k): v for k, v in json.loads(pathlib.Path(args.schedule).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []
    _mine, theirs = L.tape_plans(pathlib.Path(args.replay), args.team)

    env = L._env(args.seed, args.weeds)
    us = schedule_agent.make_agent(sched, 0, router=True)
    state = _state_of(us)

    for t in range(719):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        if day > args.day:
            break
        farm, priv = obs["farms"][0], obs["private"]
        act = us(obs)

        if day == args.day:
            tiles = farm["tiles"]
            pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
            acts = [act["farmer"], *act["hands"]][:len(pos)]
            invs = priv.get("inventories") or []
            shed_animals = {a: int((priv.get("shed") or {}).get(a, 0)) for a in ANIMALS
                            if (priv.get("shed") or {}).get(a, 0)}
            free = _pens(tiles)
            print(f"h{hour:>2}  shed{shed_animals or '{}'}  empty pens {free}")
            for u, p in enumerate(pos):
                iv = invs[u] if u < len(invs) else {}
                held = {a: iv[a] for a in ANIMALS if iv.get(a)}
                st = state["routes"].get(u) or {}
                route = [(n.tile, [o for o, _i in n.ops], dict(n.needs)) for n in st.get("route", [])]
                assigned = state["assigned"].get(u)
                flag = "  <== HOLDS ANIMAL" if held else ""
                print(f"      u{u} at {p} {str(acts[u]):<22} carry{held or '{}'} "
                      f"assigned={assigned}{flag}")
                if route:
                    print(f"          route {route}")
            if act["market"]:
                print(f"      market {act['market']}")
            print()

        n0 = len(farm.get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": act["farmer"], "hands": list(act["hands"])[:n0], "market": act["market"]},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break


if __name__ == "__main__":
    main()
