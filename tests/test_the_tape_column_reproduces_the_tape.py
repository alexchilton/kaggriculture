"""The tape column has to BE the tape.

Every board row in `scripts/breakdown.py`'s right-hand column is produced by replaying the tape's
own actions.  If that replay does not land on the board the tape recorded, the column is fiction
and every comparison drawn against it is fiction too.

It went fiction on 2026-08-08, when the environment moved to 1.32.6 and `townCenterSellInterval`
changed from 12 to 24.  `run` builds the env from `seed` and `weedSpawnChance` only, so it picked
up the new default and replayed a pre-rebalance game on a post-rebalance market.  Seb's sells
filled differently, his d4 parcel was refused, and the column reported him holding 25 tiles, 8
pens and 6 melon at d6 where his own file records 50, 9 and 13.  Three separate false leads came
off those cells in one session -- "we over-buy pens", "we plant too much melon", "we buy an extra
cow" -- and all three were the harness, not the agent.

The recorded configuration is right there in the replay file, so this is checkable rather than
arguable, which is what this test makes permanent.
"""
import collections
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
SEED, WEEDS, TPD, DAYS = 11, 0.0, 24, 7

#: Every tape the grid can be pointed at. A new download with a different economy has to be caught
#: here, not discovered three false leads later.
#:
#: `seb` and `seb2988` were the two entries here until 2026-08-13 and are gone with the rest of the
#: Seb tapes -- selecting one also selected HIS schedule for our own agent, so it was never a
#: comparison. `seb2988`'s xfail is gone with it: it never reproduced its own board (money out by
#: $52 at d4 growing to $362 by d6, one melon missing at d5-d6) and the cause was open at removal.
#: The shop-draw fix landed the same day and is the first thing to try if it is ever restored --
#: that is exactly the shape of failure an unreplayed shop draw produces.
TAPES = tuple(sorted(__import__("breakdown").TAPES))


def _board(farm):
    """Money, owned tiles, pens and the standing crop, from one farm observation."""
    crops, pens, owned = collections.Counter(), 0, 0
    for row in farm["tiles"]:
        for cell in row:
            if cell == "LOCKED":
                continue
            owned += 1
            if isinstance(cell, dict):
                if cell.get("kind") == "PLANT":
                    crops[cell["crop"]] += 1
                elif cell.get("kind") != "WEED":
                    pens += 1
    return farm["money"], owned, pens, dict(crops)


@pytest.mark.parametrize("tape", TAPES)
def test_replaying_the_tape_lands_on_the_board_the_tape_recorded(tape):
    import breakdown as B
    from kaggle_environments import make

    replay, _schedule, team = B.TAPES[tape]
    raw = json.loads((REPO / replay).read_text())
    seat = raw["info"]["TeamNames"].index(team)
    recorded = {d: _board(raw["steps"][d * TPD + TPD][seat]["observation"]["farms"][seat])
                for d in range(DAYS)}

    # The seed stays FIXED rather than taken from the recording -- the recordings carry
    # `seed: None`, and an unpinned seed makes every number downstream noise.  What must come from
    # the recording is the economy it was played on.
    cfg = dict(B.env_config(str(REPO / replay)), seed=SEED, weedSpawnChance=WEEDS)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    p0 = B.tape_policy(str(REPO / replay), team, 0)
    p1 = B.tape_policy(str(REPO / replay), team, 1)
    # The other half of "replay it on the economy it was played on": WHICH SHOPS unlocked. Built
    # from a fixed seed, the tape's actions meet a town that wants different things, and the first
    # divergence lands on day 3 -- the day the first shop opens. See `recorded_shops`.
    shops = B.recorded_shops(str(REPO / replay))

    bad = []
    for t in range(TPD * DAYS):
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if t % TPD == TPD - 1:
            day = t // TPD
            got = _board(env.state[0].observation["farms"][0])
            if got != recorded[day]:
                bad.append(f"    d{day}  replay {got}\n          tape   {recorded[day]}")

    assert not bad, (
        f"tape {tape!r}: replaying the tape does not reproduce its own board.\n"
        + "\n".join(bad)
        + f"\n\n  env config used: {cfg}\n"
          "  The recording carries the economy it was played on; replay it on that economy."
    )
