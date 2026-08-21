"""Which `(melon, q4)` key does each tape's own game arm, and therefore which opening gets replayed?

The seed sweep in `scripts/seed_tape_grid.py` came back identical on all five seeds for every tape,
which is the prediction that motivated it: neither latch reads the seed.

  `melon_branch.trigger` counts the OPPONENT's MELON tiles at d3, and in `breakdown.py` the opponent
  is `tape_policy(replay, team, 1)` -- the tape game's own other seat, fixed by the file.

  `q4_branch.trigger` asks whether `YARN_STORE` is in `town.unlocked_shops` at d6, and
  `breakdown.recorded_shops` injects the tape's own town draw into both columns.

So both are properties of the FILE. This reads them straight out of the recordings, with no
simulation, and pairs them with the tape `REPLAY_OPENING_TAPE` would then play back. Where those
two disagree, the grid is comparing our replay of one tape against a different tape's actions --
which is the honest reading of a "first bad day" that lands exactly on a latch day.

    python -u scripts/which_branch_does_each_tape_arm.py
"""

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import breakdown as B                                              # noqa: E402
from kagg.search import melon_branch as MB                         # noqa: E402
from kagg.search import q4_branch as Q4                            # noqa: E402
from kagg.search.schedule_agent import REPLAY_OPENING_TAPE         # noqa: E402


def read(path, team):
    d = json.loads(pathlib.Path(path).read_text())
    seat = d["info"]["TeamNames"].index(team)
    return d, seat


def melon_tiles(obs, seat):
    farm = (obs.get("farms") or [])[seat]
    return sum(1 for row in farm["tiles"] for t in row
               if isinstance(t, dict) and t.get("crop") == "MELON")


def main():
    print("both latches are properties of the TAPE FILE, not of --seed\n")
    print("%-16s %-34s %6s %5s | %9s %6s | %-34s"
          % ("--tape", "file", "d3 opp", "melon", "yarn@d6", "q4", "opening it then replays"))
    print("-" * 132)
    for name in ("kawashigi", "kawashigi_b3", "kawashigi_q4c"):
        path, _, team = B.TAPES[name]
        d, seat = read(path, team)
        opp_seat = 1 - seat

        # d3 dawn is step 3*24. The observation carried on a step is the state the actors saw.
        step = d["steps"][3 * 24]
        obs = step[seat].get("observation") or {}
        n_melon = melon_tiles(obs, opp_seat)
        melon = n_melon >= MB.OPPONENT_MELON

        obs6 = (d["steps"][6 * 24][seat].get("observation") or {})
        shops = ((obs6.get("town") or {}).get("unlocked_shops") or [])
        yarn = Q4.TRIGGER_SHOP in shops
        q4 = yarn and Q4.BRANCH_ON_THE_YARN_STORE

        played, _ = REPLAY_OPENING_TAPE[(melon, q4)]
        print("%-16s %-34s %6d %5s | %9s %6s | %-34s%s"
              % (name, pathlib.Path(path).name, n_melon, melon, yarn, q4,
                 pathlib.Path(played).name,
                 "" if pathlib.Path(played).name == pathlib.Path(path).name else "   <- MISMATCH"))
    print("\nMISMATCH means the grid compares our replay of one tape against another tape's actions.")


if __name__ == "__main__":
    main()
