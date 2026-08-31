"""Per-day, ours against theirs, in one recorded game. Where does the gap actually open?

Two claims are in the air and this settles both from the tape alone -- no simulation, so nothing
here depends on our agent reproducing anything.

  * Mr Stealth, 2026-08-24: *"it goes wrong already at d12"*.
  * Alex, 2026-08-24: *"is our planner fundamentally screwing up and planting too much, or why do
    we not manage to empty the board in the same way as kawa does?"*

For each day it prints, for both seats, at DUSK:

    bank        money at the last turn of the day
    gap         theirs - ours. The day the gap starts growing is the day to look at.
    tiles       owned tiles
    planted     tiles carrying a crop
    standing    units of yield sitting on the board, uncollected
    hands       crew size
    sold        units that LEFT the shed+hands that day -- fills, never offers. The agent
                re-posts every order each turn, so summing the action stream over-counts ~24x.

`standing` is the "empty the board" question directly: a player who ends every day near zero is
converting the field, and one who carries 30 units is farming into a bin. `planted` against
`standing` is the "planting too much" question -- planting more than the crew can collect shows up
as `planted` high and `standing` high together.

    python -u scripts/where_the_game_is_lost.py 98499540
    python -u scripts/where_the_game_is_lost.py 98499540 --from-day 8 --to-day 20
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TPD = 24
US = "alex chilton"


def _find(episode):
    hits = list((REPO / "data/seed_scripts").rglob(f"{episode}.json"))
    if not hits:
        sys.exit(f"no replay named {episode}.json under data/seed_scripts/")
    return hits[0]


def _held(step, seat):
    """`{product: units}` across shed and every hand, from that seat's OWN observation.

    Read the seat's own observation. `steps[i][0][...]["farms"][1]` is the opponent as seat 0 sees
    it and is not the same object -- indexing the wrong one has cost time here before.
    """
    priv = step[seat]["observation"]["private"]
    out = collections.Counter(priv.get("shed") or {})
    for inv in priv.get("inventories") or []:
        out.update(inv)
    return out


def _board(step, seat):
    """`(tiles, planted, standing_units)` for `seat` at this step."""
    grid = step[seat]["observation"]["farms"][seat]["tiles"]
    tiles = planted = standing = 0
    for row in grid:
        for t in row:
            if not isinstance(t, dict):
                continue
            tiles += 1
            if t.get("crop"):
                planted += 1
            standing += t.get("yield_units") or 0
    return tiles, planted, standing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--from-day", type=int, default=0)
    ap.add_argument("--to-day", type=int, default=29)
    a = ap.parse_args()

    rec = json.loads(_find(a.episode).read_text())
    names = rec["info"]["TeamNames"]
    seat = names.index(US)
    them = 1 - seat
    steps = rec["steps"]
    rw = rec.get("rewards") or [0, 0]

    print(f"game {a.episode}  seed {rec['info'].get('seed')}  "
          f"we are seat {seat}\n  ours   {names[seat]}  ${rw[seat]:,.0f}"
          f"\n  theirs {names[them]}  ${rw[them]:,.0f}"
          f"\n  margin ${rw[seat] - rw[them]:,.0f}\n")

    print(f"{'day':>4} | {'our bank':>10} {'their bank':>11} {'gap':>9} {'dgap':>8} "
          f"| {'tile':>4} {'plnt':>4} {'stand':>5} {'hand':>4} {'sold':>5} "
          f"| {'tile':>4} {'plnt':>4} {'stand':>5} {'hand':>4} {'sold':>5}")
    print(f"{'':>4} | {'':>10} {'':>11} {'':>9} {'':>8} "
          f"| {'------ ours ------':^30} | {'----- theirs -----':^30}")

    prev_gap = 0.0
    prev_held = {seat: _held(steps[0], seat), them: _held(steps[0], them)}
    for day in range(a.from_day, min(a.to_day, 29) + 1):
        i = min(day * TPD + TPD - 1, len(steps) - 1)
        step = steps[i]
        farms = step[seat]["observation"]["farms"]
        ours_bank = farms[seat]["money"]
        theirs_bank = step[them]["observation"]["farms"][them]["money"]
        gap = theirs_bank - ours_bank

        # Units that LEFT inventory across the day, per seat: fills, not offers.
        sold = {}
        for s in (seat, them):
            now = _held(step, s)
            gone = sum(max(0, prev_held[s].get(k, 0) - now.get(k, 0)) for k in set(prev_held[s]) | set(now))
            sold[s] = gone
            prev_held[s] = now

        ot, op, ost = _board(step, seat)
        tt, tp, tst = _board(step, them)
        oh = 1 + len(farms[seat].get("hands") or [])
        th = 1 + len(step[them]["observation"]["farms"][them].get("hands") or [])

        mark = "  <<" if gap - prev_gap > 3000 else ""
        print(f"{day:>4} | {ours_bank:>10,.0f} {theirs_bank:>11,.0f} {gap:>9,.0f} "
              f"{gap - prev_gap:>+8,.0f} "
              f"| {ot:>4} {op:>4} {ost:>5} {oh:>4} {sold[seat]:>5} "
              f"| {tt:>4} {tp:>4} {tst:>5} {th:>4} {sold[them]:>5}{mark}")
        prev_gap = gap

    print("\n  gap = theirs - ours, so a POSITIVE dgap is a day we lost ground.")
    print("  '<<' marks a day the gap opened by more than $3,000.")
    print("  stand = uncollected yield units sitting on the board at dusk.")


if __name__ == "__main__":
    main()
