"""What his hands actually DO with their turns -- the op budget our emitter has to hit.

Our emitter spends 22 of 23 work turns on a single 8-tile block, so a hand holds one job and the
crew has to grow with the farm. His hands hold a pen *and* crop tiles. This reads the per-hand,
per-day op histogram off his tape so "what should the emitter emit" is a counted number, not a guess.
"""
import argparse, collections, json, pathlib, sys
sys.path.insert(0, ".")

ap = argparse.ArgumentParser()
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--team", default="somewhere after")
a = ap.parse_args()

TD = 24
d = json.load(open(a.replay))
seat = d["info"]["TeamNames"].index(a.team)

ops = collections.Counter()
per_hand_day = collections.Counter()          # (day, hand_index) -> productive ops
moves_per_hand_day = collections.Counter()
hands_per_day = {}
# which ops each hand does across the whole season, to see if a hand is single-purpose
hand_roles = collections.defaultdict(collections.Counter)

for t, step in enumerate(d["steps"]):
    day, hour = divmod(t, TD)
    s = step[seat] or {}
    obs = s.get("observation") or {}
    farms = obs.get("farms") or []
    if len(farms) > seat:
        hands_per_day[day] = max(hands_per_day.get(day, 0), len(farms[seat].get("hands") or []))
    act = s.get("action") or {}
    crew = [("farmer", act.get("farmer"))] + [(i, h) for i, h in enumerate(act.get("hands") or [])]
    for who, op in crew:
        if not op:
            continue
        name = op[0]
        ops[name] += 1
        if name == "PASS":
            continue
        hand_roles[who][name] += 1
        if name == "MOVE":
            moves_per_hand_day[(day, who)] += 1
        else:
            per_hand_day[(day, who)] += 1

print("=" * 100)
print("HIS OP CENSUS -- every unit op on the tape")
print("=" * 100)
tot = sum(ops.values())
for k, v in ops.most_common():
    print(f"  {k:>22} {v:>6}   {100*v/tot:>5.1f}%")

print()
print("=" * 100)
print("TURNS USED PER HAND PER DAY  (23 work turns available)")
print("=" * 100)
print(f"{'day':>4} {'hands':>6} {'work ops':>9} {'moves':>7} {'total':>7} {'per hand':>9} {'busiest hand':>13}")
for day in sorted(hands_per_day):
    n = hands_per_day[day] + 1                       # + the farmer
    work = sum(v for (dd, _w), v in per_hand_day.items() if dd == day)
    mv = sum(v for (dd, _w), v in moves_per_hand_day.items() if dd == day)
    busiest = max((per_hand_day.get((day, w), 0) + moves_per_hand_day.get((day, w), 0)
                   for w in list(range(20)) + ["farmer"]), default=0)
    print(f"{day:>4} {n:>6} {work:>9} {mv:>7} {work+mv:>7} {(work+mv)/max(n,1):>9.1f} {busiest:>13}")

print()
print("=" * 100)
print("IS A HAND SINGLE-PURPOSE?  ops by hand across the season")
print("=" * 100)
for who in sorted(hand_roles, key=lambda k: str(k)):
    c = hand_roles[who]
    total = sum(c.values())
    kinds = " ".join(f"{k}:{v}" for k, v in c.most_common(8))
    print(f"  hand {str(who):>6} {total:>5} ops   {kinds}")
