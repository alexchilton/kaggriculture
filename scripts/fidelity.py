"""Where does our run stop matching the tape? One seed, day by day, ours minus his.

**A final bank is not a fidelity measurement.** Two seasons can land on similar money having taken
completely different routes, and one end-of-season figure cannot say WHERE they parted -- which is
how this project ended up with 120 one-off day-diff scripts instead of one harness. The measurement
is the state trajectory: replay his tape and run our agent on the schedule extracted from that same
tape, at the SAME seed, snapshot both farms at dawn every day, and print the difference.

Eight scalars, because each one fails for a different reason and the pattern names the mechanism:

    money     the only one that is a consequence rather than a cause
    hands     crew size. Diverges when a HIRE was skipped or could not be paid for
    owned     unlocked tiles. Diverges the day a BUY_LAND lands late -- and never converges after,
              because every later plant and pen is competing for less ground
    plant     live crop tiles
    weed      `consecutive_unwatered >= 2`. Ground that refuses PLANT for the rest of the season
    pen       COOP + PASTURE built
    animal    animals actually standing in a pen, which is PLACE, not BUY_ANIMAL
    shed      units held. Rises when we produce and cannot sell, falls when we sell into a dead book

The first day a field parts is the day to open a trace on. Everything after it is downstream and
must not be read as an independent fault -- one late parcel shows up as a plant deficit, a weed
surplus and a harvest deficit for the next twenty days.

Seat 1 is the tape's own opponent in both runs, so the shared order book is contested identically
and any price difference is caused by our seat alone.

    python -u scripts/fidelity.py --seed 11
"""

import argparse
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent

REPLAY = "data/seed_scripts/new_leader/90016067.json"
SCHEDULE = "data/seed_scripts/new_leader/schedule.json"
TEAM = "somewhere after"

#: Read by `dayplan.emit` and by NOTHING in the shipping executor -- `kagg/search/schedule_agent.py`
#: reads none of them. Dropping them is not a safeguard, it is a statement that the live agent
#: chooses every tile itself, which is the whole reason a tile-level plan cannot be handed to it.
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")

SNAP = ("money", "hands", "owned", "plant", "weed", "pen", "animal", "shed")

#: `shed` alone cannot say why the shed is short -- it totals nine products whose production paths do
#: not overlap. MILK short means the herd (pens, feed, CARE cadence); STRAWBERRY short means crop
#: yield (waters inside the window, fertilize); FERTILIZER short means COLLECT_FERTILIZER never ran.
#: The per-product split is what turns "we hold 50 fewer units" into a named mechanism.
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")


def _snapshot(obs, seat):
    farm = obs["farms"][seat]
    n = dict.fromkeys(SNAP, 0)
    for row in farm["tiles"]:
        for t in row:
            if t == "LOCKED":
                continue
            n["owned"] += 1
            if not isinstance(t, dict):
                continue
            kind = t.get("kind")
            if kind == "PLANT":
                n["plant"] += 1
            elif kind == "WEED":
                n["weed"] += 1
            else:
                n["pen"] += 1
            if t.get("animal"):
                n["animal"] += 1
    shed = (obs.get("private") or {}).get("shed") or {}
    n["money"] = float(farm["money"])
    n["hands"] = len(farm.get("hands") or [])
    n["shed"] = sum(shed.values())
    for p in PRODUCTS:
        n[p] = int(shed.get(p, 0) or 0)
    return n


def tape_policy(replay, team, seat_wanted):
    """Seat `seat_wanted`'s recorded actions, from `steps[1:]`.

    `steps[0].action` is the placeholder recorded at reset and is never applied. Replaying from
    index 0 shifts every turn by one: on this episode offset 0 gives $45,387 and offset 1 gives
    $149,662 against a recorded $141,256.
    """
    d = json.loads(pathlib.Path(replay).read_text())
    seat = d["info"]["TeamNames"].index(team)
    src = seat if seat_wanted == 0 else 1 - seat
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[src] or {} for step in d["steps"][1:])]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    return lambda obs, t: acts[t] if t < len(acts) else idle


def agent_policy(sched, seat):
    a = schedule_agent.make_agent(sched, seat, router=True)
    return lambda obs, t: a(obs)


def trace(make0, make1, seed, weeds):
    """One season at an EXPLICIT seed. Returns 30 dawn snapshots of seat 0.

    `env.state[s].status` goes to ERROR or INVALID on a malformed action and the season simply stops;
    the bank at that moment is still a float and reads as a result. Raises instead.
    """
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": int(seed), "weedSpawnChance": float(weeds)},
               debug=True)
    env.reset(2)
    p0, p1 = make0(), make1()
    days, orders = [], {}
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t % 24 == 0:
            days.append(_snapshot(o0, 0))
        a0, a1 = p0(o0, t), p1(o1, t)
        # Every market order seat 0 actually EMITTED, kept per day with the hour it went in. A shed
        # delta says what we ended up holding; only the order list says whether we asked for it and
        # were refused, or never asked.
        for o in (a0["market"] or []):
            if o:
                orders.setdefault(t // 24, []).append((t % 24, list(o)))
        # Hands truncated to the crew that seat actually has THIS turn; an over-long list is a
        # malformed action and takes the seat to INVALID for the rest of the season.
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    bad = [(s, env.state[s].status) for s in (0, 1) if env.state[s].status != "DONE"]
    if bad:
        raise RuntimeError(f"seed {seed}: seat status {bad}\n" +
                           "\n".join(str(x) for x in (env.logs or [])[-6:]))
    days.append(_snapshot(env.state[0].observation, 0))
    return days, orders


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--days", type=int, default=2, help="how many days of market orders to print")
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--replay", default=REPLAY)
    ap.add_argument("--team", default=TEAM)
    ap.add_argument("--schedule", default=SCHEDULE)
    args = ap.parse_args()

    # A run whose provenance is not printed beside it is an anecdote: a 20-minute ladder was once run
    # while a subagent held +75 uncommitted lines in `schedule_agent.py`, and the number it printed
    # was reported as the baseline when it was that subagent's losing variant.
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                         text=True).stdout.strip()
    dirty = [l for l in subprocess.run(["git", "status", "--porcelain"], capture_output=True,
                                       text=True).stdout.splitlines() if l[3:].startswith("kagg/")]

    sched = {int(k): v for k, v in json.loads(pathlib.Path(args.schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(args.replay, args.team, 1)

    his, his_ord = trace(lambda: tape_policy(args.replay, args.team, 0), opp, args.seed, args.weeds)
    ours, our_ord = trace(lambda: agent_policy(thin, 0), opp, args.seed, args.weeds)

    # **A shed delta says what we ended up holding; only the order list says whether we asked.** An
    # order that is placed and refused, and one that is never placed at all, produce the identical
    # shed row and need completely different fixes.
    # **How many orders, spread over how many HOURS.** `market_price` moves with every unit and
    # `BUY_PRODUCT` quotes at `market_price(inventory - 1)`, so one 8-unit block walks itself up the
    # curve while eight 1-unit orders spread across the day quote against a book the shops have been
    # restocking every 4 steps. Two agents can buy the same total and pay very different money.
    print("  order cadence -- orders placed, and how many distinct hours of the 24 were used\n")
    print(f"  {'day':>5}{'tape orders':>13}{'hours':>7}{'ours orders':>14}{'hours':>7}")
    for d in range(31):
        t, o = his_ord.get(d, []), our_ord.get(d, [])
        if not (t or o):
            continue
        print(f"  {d:>5}{len(t):>13}{len({h for h, _ in t}):>7}"
              f"{len(o):>14}{len({h for h, _ in o}):>7}")
    print()

    for d in range(int(args.days)):
        print(f"  day {d} market orders")
        for who, src in (("tape", his_ord), ("ours", our_ord)):
            for h, o in sorted(src.get(d, [])):
                print(f"    {who}  h{h:<3} {o}")
        print()

    print(f"HEAD {sha}" + ("   UNCOMMITTED kagg/ CODE:" if dirty else ""))
    for l in dirty:
        print(f"    {l}")
    print(f"seed {args.seed}   weedSpawnChance {args.weeds}   "
          f"ours minus tape, seat 0, at dawn each day\n")
    print("  day " + "".join(f"{f:>9}" for f in SNAP))
    first = {}
    for d, (a, b) in enumerate(zip(ours, his)):
        cells = ""
        for f in SNAP:
            delta = a[f] - b[f]
            if delta and f not in first:
                first[f] = d
            cells += f"{'':>9}" if not delta else (
                f"{delta:>+9,.0f}" if f == "money" else f"{delta:>+9d}")
        print(f"  {d:>3} {cells}")

    # **"First day it parts" is the wrong thing to chase on its own.** A field can part on day 1 by a
    # trivial or FAVOURABLE amount and re-converge for a fortnight; the day that matters is the one
    # after which it never comes back. Both are printed, and it is the sustained column to open a
    # trace on.
    print(f"\n  shed by product, ours minus tape -- WHICH product is short names the mechanism\n")
    print("  day " + "".join(f"{p[:6]:>8}" for p in PRODUCTS))
    for d, (a, b) in enumerate(zip(ours, his)):
        cells = "".join(f"{'':>8}" if a[p] == b[p] else f"{a[p] - b[p]:>+8d}" for p in PRODUCTS)
        print(f"  {d:>3} {cells}")

    print("\n  {:<8}{:>14}{:>14}{:>12}".format("field", "first parts", "never returns", "final"))
    for f in SNAP:
        deltas = [a[f] - b[f] for a, b in zip(ours, his)]
        sust = next((d for d in range(len(deltas)) if all(deltas[e] for e in range(d, len(deltas)))),
                    None)
        print("    {:<8}{:>12}{:>14}{:>12,.0f}".format(
            f, f"day {first[f]}" if f in first else "never",
            f"day {sust}" if sust is not None else "re-converges", deltas[-1]))


if __name__ == "__main__":
    main()