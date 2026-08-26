"""Which named players finish COW 6 / SHEEP 6, and what land and crops they run alongside it.

**Do NOT use `replay_fills.seat_of` for this.** It returns 0 when the name is absent
(`kagg/analysis/replay_fills.py:79-86`), so a scan built on it silently reads seat 0 of every game
it cannot match. That is exactly what happened on 2026-08-25: a scan reported "1291 kawa seats" from
a download pile, and the resulting 10/4-is-his-mode table was withdrawn in full. Here a game where
the name is missing is SKIPPED and counted, so the denominator is honest.

The question this answers, from Alex: the players who ran 6/6 well bought an extra parcel and put
effective crops on it. So a herd count alone is not the finding -- the herd has to be reported next
to tiles owned and what was grown.

    python -u scripts/who_plays_six_six.py --top 30
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

SCAN_DIRS = ("downloads_2026-08-13", "downloads_2026-08-14to16", "downloads_2026-08-19",
             "downloads_2026-08-20", "downloads_2026-08-21", "top_guys", "leaders_2026-08-24",
             "leaders_2026-08-19", "field_leaders", "tetsuya", "ryo", "tetsuya_93866112",
             "victor", "kawashigi", "new_leader", "top2")


def _last_obs(replay, seat):
    """The last step's observation for `seat`. Seat 0 carries the full board in most recordings."""
    for step in reversed(replay.get("steps") or []):
        if seat < len(step):
            obs = (step[seat] or {}).get("observation") or {}
            if obs.get("farms"):
                return obs
        obs = (step[0] or {}).get("observation") or {}
        if obs.get("farms"):
            return obs
    return {}


def _herd_and_land(replay, seat):
    """`(cows, sheep, tiles_owned, crop_counter, money)` for `seat` at the end of the game."""
    obs = _last_obs(replay, seat)
    farms = obs.get("farms") or []
    if seat >= len(farms):
        return None
    farm = farms[seat]
    # **A farm has no `animals` key.** Its keys are farmer, hands, hires_today, money, tiles and
    # unlocked_quadrants. Livestock stands ON A TILE as `tile["animal"]`, which is what
    # `replay_fills.animals_alive` reads. Counting `farm["animals"]` returns None for every game and
    # reports zero 6/6 seats out of 3,224 -- measured, and wrong, on 2026-08-25.
    animals, owned, crops = collections.Counter(), 0, collections.Counter()
    for row in (farm.get("tiles") or []):
        for t in row:
            if t == "LOCKED":
                continue
            owned += 1
            if not isinstance(t, dict):
                continue
            if t.get("animal"):
                animals[t["animal"]] += 1
            if t.get("crop"):
                crops[t["crop"]] += 1
    return (animals.get("COW", 0), animals.get("SHEEP", 0), owned, crops,
            float(farm.get("money", 0.0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=30, help="how many 6/6 rows to print")
    args = ap.parse_args()

    rows = []
    seen_games = 0
    per_name = collections.Counter()
    six_six = collections.Counter()
    files = []
    for d in SCAN_DIRS:
        p = REPO / "data/seed_scripts" / d
        if p.exists():
            files.extend(sorted(p.glob("*.json")))

    for f in files:
        try:
            r = json.loads(f.read_text())
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(r, dict):
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        if len(names) < 2:
            continue
        seen_games += 1
        for seat, name in enumerate(names[:2]):
            got = _herd_and_land(r, seat)
            if got is None:
                continue
            cow, sheep, owned, crops, money = got
            per_name[name] += 1
            if cow == 6 and sheep == 6:
                six_six[name] += 1
                rows.append((money, name, f.stem, owned, crops))

    print(f"games read {seen_games}   seats with a herd read {sum(per_name.values())}")
    print(f"seats at COW 6 / SHEEP 6: {sum(six_six.values())}")
    print()
    print("6/6 BY PLAYER (seats):")
    for n, c in six_six.most_common(20):
        print(f"  {c:>4}/{per_name[n]:<5}  {n}")
    print()
    print(f"TOP {args.top} 6/6 SEATS BY FINAL BANK -- herd, tiles owned, crops on the board:")
    print(f"  {'bank':>10}  {'tiles':>5}  {'player':<20} {'game':<12} crops")
    for money, name, game, owned, crops in sorted(rows, reverse=True)[:args.top]:
        mix = " ".join(f"{k}:{v}" for k, v in crops.most_common(5)) or "-"
        print(f"  {money:>10,.0f}  {owned:>5}  {name[:20]:<20} {game:<12} {mix}")


if __name__ == "__main__":
    main()
