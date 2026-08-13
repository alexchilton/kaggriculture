"""The comparison harness has to be able to reproduce a real game before it can compare anything.

`scripts/breakdown.py` had no way of knowing whether it was right, and three faults sat in it
undetected. The JAX simulator has a 300-episode parity gate; this had nothing.

The test that settles it: drive **both seats** of a downloaded ladder game from the recording and
require the harness to land on the banks Kaggle recorded. Both players are fully determined by the
file, so the harness has no freedom at all -- if it cannot reproduce a real game's ending, nothing
it prints about a comparison means anything.

## What this found

Run as the harness stood, on its fixed `seed=11`, it did not reproduce a single one of four games:

    92588301   recorded 92,884 / 93,254   replayed 93,236 /  84,442
    92550780   recorded 69,881 / 77,275   replayed 41,899 / 128,253
    92562037   recorded 129,161 / 133,724 replayed 85,979 /  88,297
    92498144   recorded 149,998 / 143,436 replayed 68,080 /  69,880

First divergence on 92550780 is turn 75, day 3 hour 3, one dollar. Day 3 is when the first shop
unlocks. The cause is the SHOP DRAW: `run` built the env from a fixed seed, so the tape's actions
were replayed into a town that wanted different things -- which moves prices, which moves what his
sells fetch, which moves his bank, which moves what he can afford next. A narrow $7k loss replayed
as an $86k rout.

This is the same fault as the `townCenterSellInterval` bug of 2026-08-08, which
`tests/test_the_tape_column_reproduces_the_tape.py` was written for: **the economy a tape was played
on has to come from the recording.** The shop draw is part of that economy and was left out. It
cannot be derived from the seed either -- `_end_of_day` spends the same generator on `_spawn_weeds`
first, once per empty tile per player -- but it does not need to be, because every observation in
the recording carries `town.unlocked_shops`.

## What still does not reproduce, and why it is acceptable

With the recorded shops injected, all four games reproduce **the bank, the market inventory and both
sheds exactly, on every one of 719 turns**. The only field that still diverges is WEED tiles, on the
turn `_end_of_day` runs: recordings carry `weedSpawnChance = 0.005` and the weed RNG is keyed off a
seed the recording does not store. In these four games it never reached money, the market or the
shed. The `weeds` row of any grid replayed from a tape is therefore the one row that is not
trustworthy, and `run` is honest about it rather than quiet.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

pytest.importorskip("kaggle_environments")

TPD = 24

#: Four real ladder games, spanning both a narrow loss and the biggest bank downloaded. 92498144 is
#: the current #1's, at $149,998 -- the hardest of the four to reproduce and the most convincing.
GAMES = (
    "data/seed_scripts/ours_ladder_new/92588301.json",
    "data/seed_scripts/ours_ladder_new/92550780.json",
    "data/seed_scripts/ours_ladder_new/92562037.json",
    "data/seed_scripts/kawashigi/92498144.json",
)


def recorded_policy(raw, seat):
    """Every action the recording holds for one seat, indexed by turn."""
    actions = [{"farmer": (s[seat].get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
                "hands": list((s[seat].get("action") or {}).get("hands") or []),
                "market": list((s[seat].get("action") or {}).get("market") or [])}
               for s in raw["steps"][1:]]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    return lambda _obs, t: actions[t] if t < len(actions) else idle


@pytest.mark.parametrize("game", GAMES)
def test_both_seats_from_the_recording_land_on_the_recorded_banks(game):
    import breakdown as B

    path = REPO / game
    if not path.exists():
        pytest.skip(f"{game} not downloaded")
    raw = json.loads(path.read_text())
    want = [float(r) for r in raw["rewards"]]

    days, _ops, _cash, _dawn = B.run(
        lambda: recorded_policy(raw, 0), lambda: recorded_policy(raw, 1),
        seed=11, weeds=0.0, economy=B.env_config(str(path)),
        shops=B.recorded_shops(str(path)))
    got = days[-1]["money"]

    assert got == want[0], (
        f"{pathlib.Path(game).name}: the harness replayed seat 0 to ${got:,.0f} where Kaggle "
        f"recorded ${want[0]:,.0f}. Both seats came from the recording, so the harness had no "
        f"freedom -- this is the harness, not the agent.")


@pytest.mark.parametrize("game", GAMES[:2])
def test_the_market_and_both_sheds_match_on_every_single_turn(game):
    """A final bank can be right by cancellation. This is the per-turn version, and it is the one
    that says the economy engine is sound rather than merely lucky."""
    from kaggle_environments import make

    import breakdown as B

    path = REPO / game
    if not path.exists():
        pytest.skip(f"{game} not downloaded")
    raw = json.loads(path.read_text())
    shops = B.recorded_shops(str(path))

    env = make("kaggriculture",
               configuration=dict(B.env_config(str(path)), seed=11, weedSpawnChance=0.0),
               debug=True)
    env.reset(2)
    policies = [recorded_policy(raw, 0), recorded_policy(raw, 1)]
    bad = []
    for t in range(len(raw["steps"]) - 1):
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        obs = env.state[0].observation
        a0, a1 = policies[0](obs, t), policies[1](obs, t)
        n0 = len(obs["farms"][0].get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                   "market": a1["market"]}])
        expected = raw["steps"][t + 1][0]["observation"]
        actual = env.state[0].observation
        if actual["market"]["inventory"] != expected["market"]["inventory"]:
            bad.append(f"market inventory at turn {t} (d{t // TPD} h{t % TPD})")
        for seat in (0, 1):
            mine = {k: v for k, v in
                    ((env.state[seat].observation.private or {}).get("shed") or {}).items() if v}
            theirs = {k: v for k, v in
                      (((raw["steps"][t + 1][seat].get("observation") or {}).get("private")
                        or {}).get("shed") or {}).items() if v}
            if mine != theirs:
                bad.append(f"seat {seat} shed at turn {t} (d{t // TPD} h{t % TPD})")
        for seat in (0, 1):
            if (actual["farms"][seat]["money"]
                    != expected["farms"][seat]["money"]):
                bad.append(f"seat {seat} money at turn {t} (d{t // TPD} h{t % TPD})")
        if bad:
            break
        if env.state[0].status == "DONE":
            break
    assert not bad, bad[:5]


@pytest.mark.parametrize("game", GAMES[:2])
def test_without_the_recorded_shops_it_does_not_reproduce(game):
    """The discriminator. A self-test that passes with the fix backed out proves nothing, and this
    one is worth pinning permanently: it is the reason the fix exists, and the size of the error is
    the reason it mattered -- a $7k loss replayed as an $86k rout."""
    import breakdown as B

    path = REPO / game
    if not path.exists():
        pytest.skip(f"{game} not downloaded")
    raw = json.loads(path.read_text())

    days, _ops, _cash, _dawn = B.run(
        lambda: recorded_policy(raw, 0), lambda: recorded_policy(raw, 1),
        seed=11, weeds=0.0, economy=B.env_config(str(path)), shops=None)
    assert days[-1]["money"] != float(raw["rewards"][0]), (
        "the fixed-seed shop draw now reproduces this game, so either the draw stopped mattering "
        "or the injection is no longer doing anything. Find out which before deleting this test.")


def test_recorded_shops_returns_the_list_as_it_stood_at_that_turn():
    """Not the closing list. A shop unlocks every third day, so applying the final draw to the
    whole season gives the first weeks demand that did not exist yet."""
    import breakdown as B

    path = REPO / GAMES[0]
    if not path.exists():
        pytest.skip("not downloaded")
    shops = B.recorded_shops(str(path))
    assert shops(0) == []
    assert len(shops(len(json.loads(path.read_text())["steps"]) - 2)) == 8
    assert len(shops(100)) <= len(shops(500))
