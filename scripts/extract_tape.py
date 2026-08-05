"""The tape at full resolution: every op resolved to the tile it acted on, per turn, per unit.

`extract_leader_schedule.py` keeps a bag of crops per day -- `plants: ['MELON','MELON','WHEAT',...]`
-- and throws away which tile, which unit and which turn. That is why the round trip degrades: a tape
cell is `["PLANT","MELON"]` with no coordinate, the op acts on whatever tile the unit is standing on,
and an emitter handed only a bag has to re-invent the placement. An invention cannot round-trip.

It does not have to be inferred. The observation carries every unit's position each turn
(`farm["farmer"]` and `farm["hands"]`), so the tile every op acted on is recoverable exactly.

    tape[turn][unit] = (op, arg, tile)

which makes extract and emit inverses: emit at these tiles, in this order, and the tape comes back.
"""
import argparse, collections, json, pathlib, sys
sys.path.insert(0, ".")

ap = argparse.ArgumentParser()
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--team", default="somewhere after")
ap.add_argument("--out", default="data/seed_scripts/new_leader/tape.json")
a = ap.parse_args()
TD = 24

d = json.load(open(a.replay))
seat = d["info"]["TeamNames"].index(a.team)

def positions_at(idx):
    """Unit positions recorded in `steps[idx]`."""
    if idx < 0 or idx >= len(d["steps"]):
        return []
    st = d["steps"][idx][seat] or {}
    farms = (st.get("observation") or {}).get("farms") or []
    farm = farms[seat] if len(farms) > seat else {}
    out = [tuple(farm.get("farmer") or (4, 4))]
    for h in (farm.get("hands") or []):
        out.append(tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4))))
    return out


tape = []
for t, step in enumerate(d["steps"]):
    s = step[seat] or {}
    # **The position stored in `steps[t]` is where the unit ended up AFTER that turn's action, not
    # where it stood before it.** Proven by the router diff: a WEST move at turn t was recorded with
    # identical source and destination tiles, and a two-step walk (4,4)->(4,2) came out as
    # (4,3)->(4,2). Pairing an op with its own step's position shifted every tile one move forward,
    # and those shifted tiles were being fed back in as ground truth -- so the error compounded into
    # every placement, every day, for the whole season.
    # **At dawn the units have been teleported home, so the previous turn's position is not where
    # this turn's op acts.** `_end_of_day` resets `farm["farmer"]` to spawn and empties `farm["hands"]`
    # (`reference/kaggriculture.py:848-849`), so reading `t - 1` across a day boundary hands back the
    # END of yesterday. Measured: paths that were the first of their day matched 161/334 while every
    # later path in the same tape matched 1437/1579 -- the boundary, not the router.
    # Turn 0 is the market phase and moves nobody, so its own record is already the dawn position.
    pos = positions_at(t) if t % TD == 0 else (positions_at(t - 1) or positions_at(t))
    # A hand hired THIS turn has no row in the previous turn's list, so its ops came out with no
    # tile at all -- 5 of the 131 plantings were being dropped on the floor. It spawns at the shed,
    # so fall back per unit rather than losing the op.
    later = positions_at(t)
    while len(pos) < len(later):
        pos.append(later[len(pos)])
    act = s.get("action") or {}
    ops = [act.get("farmer")] + list(act.get("hands") or [])
    row = []
    for u, op in enumerate(ops):
        if not op:
            row.append(None)
            continue
        row.append(dict(op=op[0], arg=(op[1] if len(op) > 1 else None),
                        qty=(op[2] if len(op) > 2 else None),
                        tile=list(pos[u]) if u < len(pos) else None))
    tape.append(dict(turn=t, day=t // TD, units=row, market=act.get("market") or []))

pathlib.Path(a.out).write_text(json.dumps(tape))

# ---- what the full-resolution tape says that the bag-of-crops schedule could not
placed = collections.defaultdict(list)
for r in tape:
    for u, c in enumerate(r["units"]):
        if c and c["op"] in ("PLANT", "BUILD_PASTURE", "BUILD_COOP", "PLACE"):
            placed[r["day"]].append((c["op"], c["arg"], tuple(c["tile"] or ())))

print("=" * 100)
print(f"FULL-RESOLUTION TAPE -- {len(tape)} turns, written to {a.out}")
print("=" * 100)
for day in sorted(placed)[:6]:
    print(f"\nday {day}:")
    for op, arg, tile in placed[day]:
        print(f"    {op:>14} {str(arg):>12} at {tile}")

tiles = {t for v in placed.values() for _o, _a, t in v if t}
print(f"\ndistinct tiles ever planted or built on: {len(tiles)}")
print(f"total placements: {sum(len(v) for v in placed.values())}")
