"""How many teacher labels did the LOCKED masks delete? Counted straight out of the recordings.

Three mask terms were removed on 2026-08-22 (`0f27ae8`, `d23fc85`): movement onto a LOCKED tile,
and the shed ops from a LOCKED shed-access tile. Both were unemittable via `_masked_logits` AND
excluded from the gradient by `bc.py`'s illegal-label rule, so every occurrence in the teacher
stream was a label the student could neither copy nor be taught.

This reads the four kawashigi recordings and counts, per turn and per unit, the labels that the old
masks forbade. It needs no simulator: the recording carries the board and the unit positions, so
the count is a fact about the teacher rather than about our replay of it.

    python -u scripts/probe_locked_tile_labels.py

**Pairing, and it is off by one.** `kaggle-environments` records `steps[i]` as the state AFTER step
`i` was processed, and the `action` on `steps[i][agent]` is what that agent submitted to PRODUCE it.
So the action belongs with the observation at `steps[i - 1]`, which is exactly why `dagger_tape`
reads the opponent stream from `doc["steps"][1:]`.

Pairing them at the same index was tried first and the check caught it: 1077 of 3289 move ops
agreed, so two thirds of the counts were attached to the wrong board. The check runs on every
invocation and the counts are only printed when it passes.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent as SA  # noqa: E402

MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
SHED_OPS = ("PICKUP", "DROP", "PLACE")
TURNS_PER_DAY = 24


def units_of(farm):
    """Farmer first, then hands -- the order `_apply_unit_action` is called in."""
    return [tuple(farm.get("farmer") or (0, 0))] + [tuple(h) for h in (farm.get("hands") or [])]


def actions_of(action):
    return [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])


def shed_access(board):
    h = board // 2
    return {(h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h)}


def _check_pairing(steps, seat, board):
    """Movement is the witness: after a legal move the next observation is one tile along."""
    checked = agreed = 0
    for i in range(len(steps) - 1):
        # `_end_of_day` teleports every unit back to spawn, so the last turn of a day has no
        # readable "one tile along" successor. 3389/3396 agreed before this line and the residue
        # was exactly the day boundaries.
        if i % TURNS_PER_DAY == TURNS_PER_DAY - 1:
            continue
        obs = (steps[i][0] or {}).get("observation") or {}
        nxt = (steps[i + 1][0] or {}).get("observation") or {}
        farms, farms_n = obs.get("farms") or [], nxt.get("farms") or []
        if seat >= len(farms) or seat >= len(farms_n):
            continue
        act = (steps[i + 1][seat] or {}).get("action") or {}
        if not isinstance(act, dict):
            continue
        here, there = units_of(farms[seat]), units_of(farms_n[seat])
        for u, a in enumerate(actions_of(act)):
            if u >= len(here) or u >= len(there) or not isinstance(a, list) or not a:
                continue
            if a[0] not in MOVES:
                continue
            dx, dy = MOVES[a[0]]
            want = (here[u][0] + dx, here[u][1] + dy)
            inside = 0 <= want[0] < board and 0 <= want[1] < board
            checked += 1
            agreed += int(there[u] == (want if inside else here[u]))
    return checked, agreed


def scan(path, team):
    doc = json.loads((REPO / path).read_text())
    seat = doc["info"]["TeamNames"].index(team)
    steps = doc["steps"]
    board = len(((steps[0][0]["observation"]["farms"]) or [{}])[0].get("tiles") or [])
    access = shed_access(board)

    checked, agreed = _check_pairing(steps, seat, board)
    counts = collections.Counter()
    total = 0

    for i in range(len(steps) - 1):
        obs = (steps[i][0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        if seat >= len(farms):
            continue
        act = (steps[i + 1][seat] or {}).get("action") or {}
        if not isinstance(act, dict):
            continue
        farm = farms[seat]
        tiles = farm.get("tiles") or []
        pos = units_of(farm)
        for u, a in enumerate(actions_of(act)):
            if u >= len(pos) or not isinstance(a, list) or not a:
                continue
            total += 1
            x, y = pos[u]
            if not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])):
                continue
            standing_locked = tiles[y][x] == "LOCKED"
            op = a[0]
            if op in MOVES:
                dx, dy = MOVES[op]
                nx, ny = x + dx, y + dy
                if not (0 <= nx < board and 0 <= ny < board):
                    continue
                if tiles[ny][nx] == "LOCKED":
                    counts["MOVE onto LOCKED: " + op] += 1
            elif op in SHED_OPS and (x, y) in access and standing_locked:
                counts["SHED op on LOCKED tile: " + op] += 1

    return dict(seat=seat, board=board, total=total, counts=counts,
                pairing=(checked, agreed))


def main():
    grand = collections.Counter()
    grand_total = 0
    rows = []
    for key, (path, team) in sorted(SA.REPLAY_OPENING_TAPE.items()):
        r = scan(path, team)
        rows.append((pathlib.Path(path).name, r))
        grand.update(r["counts"])
        grand_total += r["total"]

    print("pairing check (move ops whose next observation matches the step):")
    bad = False
    for name, r in rows:
        checked, agreed = r["pairing"]
        ok = checked and agreed == checked
        bad = bad or not ok
        print("  %-16s %6d/%-6d  %s" % (name, agreed, checked, "OK" if ok else "MISMATCH"))
    print()
    if bad:
        print("PAIRING FAILED -- every count below would be attached to the wrong board.")
        print("Not printing them. Fix the pairing first.")
        return

    print("labels the OLD masks made unlearnable, per tape:")
    header = sorted(grand)
    print("  %-16s %8s  %s" % ("tape", "labels", "  ".join("%22s" % h for h in header)))
    for name, r in rows:
        print("  %-16s %8d  %s"
              % (name, r["total"], "  ".join("%22d" % r["counts"].get(h, 0) for h in header)))
    print("  %-16s %8d  %s"
          % ("ALL FOUR", grand_total, "  ".join("%22d" % grand[h] for h in header)))
    print()
    n_bad = sum(grand.values())
    print("total unlearnable teacher labels: %d of %d unit actions (%.3f%%)"
          % (n_bad, grand_total, 100.0 * n_bad / max(1, grand_total)))


if __name__ == "__main__":
    main()
