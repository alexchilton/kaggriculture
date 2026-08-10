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

#: Every tape the grid can be pointed at.  A new download with a different economy has to be
#: caught here, not discovered three false leads later.
#:
#: `seb2988` is xfail STRICT, not skipped: it was recorded at `townCenterSellInterval` 24, the same
#: economy that is installed, and still does not reproduce -- money is out by $52 at d4 growing to
#: $362 by d6, with one melon missing at d5 and d6.  Neither the sell interval nor the weed rate
#: explains it (replayed at 0.005 as recorded, the same days fail identically), so the cause is
#: still open and is NOT the bug this file fixed.  Strict, so that whatever closes it fails here
#: and gets the marker removed rather than leaving a passing test marked broken.
TAPES = (
    "seb",
    pytest.param("seb2988", marks=pytest.mark.xfail(
        strict=True, reason="open: money drifts $52 -> $362 over d4-d6 and one melon is missing; "
                            "not the sell interval (24, as installed) and not the weed rate")),
)


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

    bad = []
    for t in range(TPD * DAYS):
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
