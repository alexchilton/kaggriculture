"""Feed the leader's OWN schedule into our emitter and see what comes out.

Alex's test, and it is the cleanest one available: we now have his schedule as ground truth
(`scripts/extract_leader_schedule.py` -> `schedule.json`), so drive `routines.py` at exactly that
schedule and compare. It isolates the emitter from every other layer:

  - if the tape it produces banks near his $141,256, the emitter and simulator are fine and everything
    left to fix is the SEARCH and the SCHEDULER -- they cannot find a plan we can already express.
  - if it banks far less, the emitter cannot express his farm at his schedule, and no search will ever
    close the gap. The bug is upstream of the optimiser.

His schedule, off the tape:

    day  0   4 pens built (COWx3 SHEEPx1), 4 hires, 17 tiles planted, 18 seeds, 49 wheat bought
    day  5   +2 pens        day  7   land parcel 1, 8 hands
    day  6   +1 pen         day 10   land parcel 2, 12 hands
    day  8   +4 pens        day 11   +2 pens -- 14 total
    day  9   +1 pen
    crew ramps 4 -> 12 across days 0-10; plantings continue all season, 131 in total

Two differences from his tape are structural and are reported rather than hidden, because they are the
interesting part:

  - **`ranch()` raises one pen per day per chain.** He builds four pens on day 0 simultaneously, which
    needs four chains, whereas one chain of four raises them on days 0-3. So matching his day-0 herd
    costs four chains where his tape costs four builds; whether that costs us hands depends on the
    packer, which is exactly what this measures.
  - **his crew ramps and ours is implied by the highest unit index in use on that day** (`script.hire`),
    so the ramp is an output here, not an input. If it comes out flat at 12 we are paying his peak crew
    from day 0, which is $376/day for ten days he pays $7-$88.
"""

import argparse
import collections
import json
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import routines as R
import build_script_submission as B

ap = argparse.ArgumentParser()
ap.add_argument("--schedule", default="data/seed_scripts/new_leader/schedule.json")
ap.add_argument("--opponent", default="starter")
ap.add_argument("--games", type=int, default=3)
ap.add_argument("--wheat", action="store_true",
                help="also emit his wheat book: ~35 units bought a day, dumps on days 12 and 29")
args, _unknown = ap.parse_known_args([] if __name__ != "__main__" else None)

SHED = R.shed_access_tiles()
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]
sched = json.load(open(args.schedule))


def cluster(quadrant, n, taken):
    pool = [t for t in [(x, y) for y in range(R.BOARD_SIZE) for x in range(R.BOARD_SIZE)]
            if R.quadrant_of(*t) == quadrant and t not in SHED and t not in taken]
    pool.sort(key=lambda t: abs(t[0] - 4) + abs(t[1] - 4))
    if not pool:
        return []
    out = [pool[0]]
    while len(out) < n:
        nxt = min((t for t in pool if t not in out
                   and any(abs(t[0] - o[0]) + abs(t[1] - o[1]) == 1 for o in out)),
                  key=lambda t: abs(t[0] - 4) + abs(t[1] - 4), default=None)
        if nxt is None:
            break
        out.append(nxt)
    return R.serpentine(out)


# ------------------------------------------------------------------ his schedule, as jobs
land_days = sorted(int(d) for d, r in sched.items() if r["land"])
unlock = {"NW": 0,
          "NE": land_days[0] + 1 if land_days else 99,
          "SW": land_days[1] + 1 if len(land_days) > 1 else 99}

# Pen builds, day by day, with the animal he paid for that day where the tape names one.
pen_events = []
for day in sorted(int(d) for d in sched):
    r = sched[str(day)]
    n = r["builds"]
    if not n:
        continue
    bought = r["animals_bought"] or {}
    animal = max(bought, key=bought.get) if bought else "COW"
    pen_events.append((day, n, animal))

# Plantings, day by day. His 131 tile-plantings include replants of non-ongoing crops, so the schedule
# is read as "this many tiles come online on this day" and blocks are sized to match.
plant_events = []
for day in sorted(int(d) for d in sched):
    n = len(sched[str(day)]["plants"])
    if n:
        crops = collections.Counter(sched[str(day)]["plants"])
        plant_events.append((day, n, crops.most_common(1)[0][0]))
VERBOSE = __name__ == "__main__"


def say(*a):
    if VERBOSE:
        print(*a)


say("=" * 100)
say("HIS SCHEDULE, AS JOBS FOR OUR EMITTER")
say("=" * 100)
say(f"  land parcels on days {land_days}   (NE from day {unlock['NE']}, SW from day {unlock['SW']})")
say(f"  pen builds: {[(d, n, a) for d, n, a in pen_events]}")
say(f"  plant days: {[(d, n) for d, n, _c in plant_events][:12]} ... "
    f"{sum(n for _d, n, _c in plant_events)} tile-plantings total")


def _ranch(target, ground, unit, kw):
    R.ranch(target, animal=kw["animal"], tile=list(ground), start_day=kw["start_day"], unit=unit,
            buy_land=False, feed_every=2, collect_fertilizer=True, sell_fertilizer=True)


def _grow(target, ground, unit, kw):
    R.grow(target, kw["crop"], list(ground), plant_day=kw["start_day"], unit=unit,
           buy_land=False, water_every=2)


def emit(wheat=False):
    """His schedule through our routines. Returns (script, used, refused)."""
    script = R.Script()
    taken, used, refused, busy = set(), [], [], set()
    for day in land_days:
        t = day * R.TURNS_PER_DAY
        if 0 <= t < script.T:
            script.buy_land[t] += 1

    def place(fn, ground, **kw):
        """Lowest unit that accepts the job, units already carrying work tried first."""
        import copy
        for unit in sorted(busy) + [u for u in range(20) if u not in busy]:
            probe = copy.deepcopy(script)
            try:
                fn(probe, ground, unit, kw)
            except ValueError:
                continue
            fn(script, ground, unit, kw)
            busy.add(unit)
            return unit
        return None

    # **Pens first and in NW.** NW is the only quadrant open on day 0 and the herd is the working
    # capital: it sells fertilizer from day 1 while milk does not arrive until day 8. Measured -- a
    # plan that puts crops in NW instead ends with one pen and banks $2.
    for day, n, animal in pen_events:
        for _ in range(n):
            group = cluster("NW", 1, taken)
            if not group:
                refused.append(f"day {day}: no NW tile left for a pen")
                break
            u = place(_ranch, group, animal=animal, start_day=day)
            if u is None:
                refused.append(f"day {day}: no unit takes a pen ({animal})")
                break
            taken.update(group)
            used.append(("ranch", animal, len(group), u, day))

    # **Crops behind the parcels.** A PLANT on LOCKED ground is a silent no-op, so a block cannot
    # start before its quadrant unlocks whatever his tape does on that day.
    for day, n, crop in plant_events:
        remaining = n
        while remaining > 0:
            placed = False
            for quadrant in ("NE", "SW", "NW"):
                if unlock[quadrant] > day:
                    continue
                for size in range(min(8, remaining), 0, -1):
                    block = cluster(quadrant, size, taken)
                    if len(block) < size:
                        continue
                    u = place(_grow, block, crop=crop, start_day=day)
                    if u is None:
                        continue
                    taken.update(block)
                    used.append(("grow", crop, len(block), u, day))
                    remaining -= len(block)
                    placed = True
                    break
                if placed:
                    break
            if not placed:
                refused.append(f"day {day}: {remaining} of {n} {crop} tiles unplaced")
                break

    if wheat:
        w = R.PRODUCTS.index("WHEAT")
        for day in sorted(int(d) for d in sched):
            n = sched[str(day)]["buys"].get("WHEAT", 0)
            for k in range(n):
                t = day * R.TURNS_PER_DAY + (k % (R.TURNS_PER_DAY - 1)) + 1
                if t < script.T:
                    script.buy_product[t, w] += 1
        for day, qty in ((12, 204), (29, 176)):
            t = day * R.TURNS_PER_DAY
            if t < script.T:
                script.sell[t, w] += qty
    return script, used, refused


def census(unit_op):
    """Op histogram and per-hand-per-day turn use for OUR tape, in his units.

    His numbers off the same census: 56% of ops are MOVE, 1.44 walk turns per productive turn, and
    every hand runs at 21-22 of 23 work turns from day 0. Ours has to be read the same way or the
    comparison is not a comparison.
    """
    import numpy as _np
    names = {v: k for k, v in R.OP.items()}
    MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
    hist = collections.Counter()
    per_day_work = collections.Counter()
    per_day_move = collections.Counter()
    busiest = collections.Counter()
    hands_used = collections.defaultdict(set)
    T, U = unit_op.shape
    for t in range(T):
        day = t // R.TURNS_PER_DAY
        for u in range(U):
            nm = names.get(int(unit_op[t, u]), "PASS")
            hist[nm] += 1
            if nm == "PASS":
                continue
            hands_used[day].add(u)
            if nm in MOVES:
                per_day_move[day] += 1
            else:
                per_day_work[day] += 1
            busiest[(day, u)] += 1
    return dict(hist=hist, work=per_day_work, move=per_day_move,
                busiest=busiest, hands=hands_used)


def build(games=None, opponent=None, wheat=None):
    """Play his schedule through our emitter. The dict the schedule tests read."""
    import numpy as _np
    from kaggle_environments import make

    script, used, refused = emit(wheat=args.wheat if wheat is None else wheat)
    hire = _np.asarray(script.hire)
    crew = {d: int(hire[d * R.TURNS_PER_DAY]) for d in range(R.SEASON_DAYS)
            if d * R.TURNS_PER_DAY < len(hire)}
    plan = B.build_plan(script.arrays())

    def agent(obs, config=None):
        step = int(obs.get("step", 0) or 0)
        if step >= len(plan):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farmer, hands_, market = plan[step]
        farms = obs.get("farms") or []
        me = int(obs.get("player", 0) or 0)
        n = len(farms[me].get("hands", []) or []) if me < len(farms) else 0
        return {"farmer": farmer, "hands": hands_[:n], "market": market}

    finals, curve = [], {}
    for g in range(args.games if games is None else games):
        env = make("kaggriculture", debug=False)
        res = env.run([agent, args.opponent if opponent is None else opponent])
        obs = (res[-1][0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        finals.append(float(farms[0]["money"]) if len(farms) == 2 else 0.0)
        if not curve:
            for t, step in enumerate(res):
                o = (step[0] or {}).get("observation") or {}
                f = o.get("farms") or []
                if len(f) == 2 and t % R.TURNS_PER_DAY == 0:
                    curve[t // R.TURNS_PER_DAY] = float(f[0]["money"])
    return dict(script=script, used=used, refused=refused, crew=crew, bank=curve,
                final=float(_np.mean(finals)), finals=finals,
                pens=sum(u[2] for u in used if u[0] == "ranch"),
                tiles=sum(u[2] for u in used if u[0] == "grow"),
                census=census(script.unit_op))


if __name__ == "__main__":
    out = build()
    script, used, refused = out["script"], out["used"], out["refused"]
    hire = np.asarray(script.hire)
    print()
    print("=" * 100)
    print("WHAT OUR EMITTER PRODUCED")
    print("=" * 100)
    print(f"  {len(used)} chains, {out['pens']} pens, {out['tiles']} crop tiles, "
          f"peak crew {int(hire.max())} hands")
    print(f"  his: 14 pens, 131 tile-plantings, peak crew 12 hands")
    for r in refused[:12]:
        print(f"  REFUSED {r}")
    if len(refused) > 12:
        print(f"  ... and {len(refused) - 12} more refusals")

    # ---------------------------------------------------------------- the op budget, side by side
    c = out["census"]
    MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
    tot = sum(v for k, v in c["hist"].items() if k != "PASS")
    mv = sum(v for k, v in c["hist"].items() if k in MOVES)
    print()
    print("=" * 100)
    print("OUR OP CENSUS  (his: 4,120 moves / 2,857 work = 1.44 walk per work, 56% moves)")
    print("=" * 100)
    for k, v in c["hist"].most_common():
        if k == "PASS":
            continue
        print(f"  {k:>22} {v:>6}   {100 * v / max(tot, 1):>5.1f}%")
    print(f"\n  moves {mv}, work {tot - mv}, ratio {mv / max(tot - mv, 1):.2f} walk turns per work turn")

    print()
    print(f"{'day':>4} {'OUR hands':>10} {'HIS hands':>10} {'OUR turns':>10} {'HIS turns':>10} "
          f"{'OUR /hand':>10} {'HIS /hand':>10}")
    HIS_TURNS = {0: 101, 1: 92, 2: 112, 3: 106, 4: 143, 5: 130, 6: 136, 7: 175, 8: 228,
                 9: 256, 10: 268, 11: 276, 12: 266, 13: 274}
    for day in range(0, 14):
        ours_h = len(c["hands"].get(day, ()))
        his_h = sched[str(day)]["hands"] + 1
        ours_t = c["work"].get(day, 0) + c["move"].get(day, 0)
        his_t = HIS_TURNS[day]
        print(f"{day:>4} {ours_h:>10} {his_h:>10} {ours_t:>10} {his_t:>10} "
              f"{ours_t / max(ours_h, 1):>10.1f} {his_t / max(his_h, 1):>10.1f}")

    print()
    print("=" * 100)
    print(f"BANK -- his schedule through our emitter.  mean of {args.games} games")
    print("=" * 100)
    print(f"  ours  ${out['final']:>12,.0f}   (min ${min(out['finals']):,.0f}  "
          f"max ${max(out['finals']):,.0f})")
    print(f"  his   ${141_256:>12,}")
    print()
    print(f"{'day':>4} {'OURS':>12} {'HIS':>12}")
    for day in range(0, 30):
        his = sched[str(day)]["money_dawn"]
        print(f"{day:>4} {out['bank'].get(day, float('nan')):>12,.0f} {(his or 0):>12,.0f}")
