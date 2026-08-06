"""Where the winner puts things and how far it walks, against where we put things and how far we walk.

Both halves of layer 3 have been argued about on synthetic boards, which is the wrong reference. The
replay contains the winner's actual choices -- `plant_tiles`, `build_tiles`, and, by replaying it, the
exact position of every unit on every turn -- so the comparison can be made directly and per day.

    placement   how many tiles worked, how far they sit from the shed, and what one tour over the
                worked set costs. A farm is its tile SET; the set is walked ~20 times a season.
    movement    move ops per day and per work op. The tape's ratio is the number to beat, and beating
                it while doing a THIRD of the work is not a win -- which is why both are printed.

Same seed, same opponent, both seats driven.

## What it measured, seed 11, tape $129,371 against our $85,247

    tiles worked                ours 43.7   tape 46.6
    mean distance to shed       ours  3.8   tape  3.9
    tour over the worked set    ours 51.2   tape 54.9
    moves per work op           ours 1.27   tape 1.44
    TOTAL WORK OPS              ours 1613   tape 2857

**Placement and movement are done.** Our tile set is the same size, the same distance from the shed and
marginally cheaper to tour than the winner's, and we walk less per unit of work than it does. An arm
that forced the tape's own coordinates into our agent was planned here and is not worth writing: the
sets already match, so it could only measure noise.

The whole gap is **work volume** -- 56% of the winner's ops from an equivalent farm -- and it is
concentrated in the herd. Animal ops: tape 945 a season, ours 505. Crop ops are close. So the next
question is not where the tiles are, it is why the animals keep starving.
"""

import collections
import json
import pathlib
import statistics
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import router as RT
from kagg.search import schedule_agent
import agent_ladder as L

MOVES = ("NORTH", "SOUTH", "EAST", "WEST")
SHED = RT.SHED


def worked_tiles(tiles):
    """Tiles the farm is actually maintaining: crops, pens and animals. Weeds are not work, they are debt."""
    return {(x, y) for y, r in enumerate(tiles) for x, c in enumerate(r)
            if isinstance(c, dict) and c.get("kind") != "WEED"}


def shape(tileset):
    """(count, mean distance to the nearest shed cell, 2-opt tour length over the set)."""
    if not tileset:
        return 0, 0.0, 0
    near = statistics.mean(min(RT.dist(t, s) for s in SHED) for t in tileset)
    seq = RT._two_opt((4, 4), sorted(tileset))
    return len(tileset), near, RT._path_len((4, 4), seq)


def run(seed, weeds, make_us=None, tape=None, theirs=None):
    """Play one season; return per-day (worked-set shape, moves, work ops)."""
    env = L._env(seed, weeds)
    us = make_us() if make_us else None
    rows, moves, work, snap = {}, collections.Counter(), collections.Counter(), {}
    for t in range(719):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        farm = obs["farms"][0]
        if hour == 12:
            snap[day] = shape(worked_tiles(farm["tiles"]))
        if us is not None:
            a = us(obs)
            f0, h0, m0 = a["farmer"], a["hands"], a["market"]
        else:
            f0, h0, m0 = tape[t] if t < len(tape) else (["PASS"], [], [])
        n0 = len(farm.get("hands") or [])
        for act in [f0, *list(h0)[:n0]]:
            if isinstance(act, list) and act:
                (moves if act[0] in MOVES else work)[day] += 1 if act[0] != "PASS" else 0
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": f0, "hands": list(h0)[:n0], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    for d, s in snap.items():
        rows[d] = (s, moves[d], work[d])
    return rows, float(env.state[0].observation["farms"][0]["money"])


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    mine, theirs = L.tape_plans()
    full = {int(k): v for k, v in json.loads(pathlib.Path(L.SCHEDULE).read_text()).items()}
    thin = json.loads(json.dumps({str(k): v for k, v in full.items()}))
    thin = {int(k): v for k, v in thin.items()}
    for r in thin.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    tape_rows, tape_money = run(seed, 0.0, tape=mine, theirs=theirs)
    our_rows, our_money = run(seed, 0.0,
                              make_us=lambda: schedule_agent.make_agent(thin, 0, router=True),
                              theirs=theirs)

    print(f"seed {seed}   tape ${tape_money:,.0f}   ours ${our_money:,.0f} "
          f"({100 * our_money / tape_money:.0f}%)\n")
    print(f"{'':>5} {'TILES WORKED':>15} {'MEAN DIST TO SHED':>20} {'TOUR OVER SET':>16}"
          f" {'MOVES/DAY':>13} {'WORK OPS/DAY':>15}")
    print(f"{'day':>5} {'ours':>7}{'tape':>8} {'ours':>10}{'tape':>10} {'ours':>8}{'tape':>8}"
          f" {'ours':>6}{'tape':>7} {'ours':>7}{'tape':>8}")
    agg = collections.defaultdict(list)
    for d in sorted(set(our_rows) | set(tape_rows)):
        (on, od, ot), om, ow = our_rows.get(d, ((0, 0, 0), 0, 0))
        (tn, td, tt), tm, tw = tape_rows.get(d, ((0, 0, 0), 0, 0))
        agg["tiles"].append((on, tn)); agg["dist"].append((od, td))
        agg["tour"].append((ot, tt)); agg["moves"].append((om, tm)); agg["work"].append((ow, tw))
        print(f"{d:>5} {on:>7}{tn:>8} {od:>10.1f}{td:>10.1f} {ot:>8}{tt:>8}"
              f" {om:>6}{tm:>7} {ow:>7}{tw:>8}")
    print()
    for k, label in (("tiles", "tiles worked"), ("dist", "mean distance to shed"),
                     ("tour", "tour over the worked set"), ("moves", "moves"),
                     ("work", "work ops")):
        o = statistics.mean(a for a, _b in agg[k])
        t = statistics.mean(b for _a, b in agg[k])
        print(f"  season mean {label:<26} ours {o:>8.1f}   tape {t:>8.1f}   "
              f"{'ours ' + ('better' if (o < t) == (k in ('dist', 'tour', 'moves')) else 'worse')}")
    om = sum(m for _s, m, _w in our_rows.values()); ow = sum(w for _s, _m, w in our_rows.values())
    tm = sum(m for _s, m, _w in tape_rows.values()); tw = sum(w for _s, _m, w in tape_rows.values())
    print(f"\n  moves per work op            ours {om / max(1, ow):>8.2f}   tape {tm / max(1, tw):>8.2f}")
    print(f"  total work ops               ours {ow:>8}   tape {tw:>8}")


if __name__ == "__main__":
    main()
