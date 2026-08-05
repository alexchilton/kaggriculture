"""WHICH day makes a chain refuse -- the measurement that decides the emitter's design.

Our tape leaves 6-11 of 23 work turns idle per hand per day and still refuses 12 of his plantings.
Those two facts can only both be true if the refusal comes from a day other than the one the job
starts on: `grow()` claims turns on EVERY day of the season, so a unit is rejected for a day-4 job
because its day-20 is full. This prints the day named in each ValueError, and the free turns on the
day the job actually wanted, so the theory is confirmed or dead before any code changes.
"""
import collections
import copy
import re
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

import emit_leader_schedule as E
from kagg.search import routines as R

script = R.Script()
taken, busy = set(), set()
for day in E.land_days:
    t = day * R.TURNS_PER_DAY
    if 0 <= t < script.T:
        script.buy_land[t] += 1

DAY_RE = re.compile(r"day (\d+) unit (\d+)")
refusal_days = collections.Counter()
detail = []


def place(fn, ground, want_day, **kw):
    reasons = []
    for unit in sorted(busy) + [u for u in range(20) if u not in busy]:
        probe = copy.deepcopy(script)
        try:
            fn(probe, ground, unit, kw)
        except ValueError as e:
            m = DAY_RE.search(str(e))
            if m:
                reasons.append((unit, int(m.group(1)), int(m.group(2))))
            continue
        fn(script, ground, unit, kw)
        busy.add(unit)
        return unit, reasons
    return None, reasons


def free_turns(day):
    return {u: script.turns_left(day, u) for u in range(20)}


for day, n, animal in E.pen_events:
    for _ in range(n):
        group = E.cluster("NW", 1, taken)
        if not group:
            break
        u, _r = place(E._ranch, group, day, animal=animal, start_day=day)
        if u is None:
            break
        taken.update(group)

for day, n, crop in E.plant_events:
    remaining = n
    while remaining > 0:
        placed = False
        for quadrant in ("NE", "SW", "NW"):
            if E.unlock[quadrant] > day:
                continue
            for size in range(min(8, remaining), 0, -1):
                block = E.cluster(quadrant, size, taken)
                if len(block) < size:
                    continue
                u, reasons = place(E._grow, block, day, crop=crop, start_day=day)
                if u is None:
                    if reasons:
                        detail.append((day, size, crop, reasons))
                        for _un, blocked_day, _bu in reasons:
                            refusal_days[blocked_day] += 1
                    continue
                taken.update(block)
                remaining -= len(block)
                placed = True
                break
            if placed:
                break
        if not placed:
            break

print("=" * 100)
print("WHICH DAY THE REFUSAL COMES FROM")
print("=" * 100)
print(f"{'job wants':>10} {'size':>5} {'crop':>11}   blocked-on days (unit -> day claim() failed)")
for day, size, crop, reasons in detail[:20]:
    by_day = collections.Counter(bd for _u, bd, _bu in reasons)
    print(f"{day:>10} {size:>5} {crop:>11}   {dict(sorted(by_day.items()))}")

print()
print("blocked-on day histogram across every refusal:")
for d, c in sorted(refusal_days.items()):
    print(f"   day {d:>3}: {c:>4} refusals")

print()
print("=" * 100)
print("FREE TURNS ON THE DAYS WE REFUSED  (23 work turns per hand per day)")
print("=" * 100)
for day in sorted({d for d, _s, _c, _r in detail}):
    f = free_turns(day)
    active = {u: v for u, v in f.items() if v < R.TURNS_PER_DAY - 1}
    print(f"  day {day:>3}: {sum(f.values()):>4} free turns across 20 units; "
          f"in-use units {active}")
