"""The submission's observation parser is blind to livestock, so the animal economy is unreachable.

**Measured, on the $147,178 seat's own board** (`data/logs/tape_diff_merged.log` and the op census):

    turn 200: RAW animals=7   ->  VIEW animals=0
    turn 400: RAW animals=14  ->  VIEW animals=0
    turn 600: RAW animals=14  ->  VIEW animals=0

    ops the winner uses that we never emit once in 720 turns:
        BUILD_PASTURE, CARE, COLLECT_FERTILIZER, DROP, FEED, FERTILIZE, PICKUP, PLACE

**The cause is an omission, not a wrong index.** `agent.observation_view` builds its `View` without
passing `animal`, `shed_animals`, `shed_wheat`, `carried_wheat` or `carried_animal`, and
`View.__post_init__` then fills them in with, in its own words, "no animals anywhere". So the agent
tells itself it owns no livestock and no feed. Every livestock mask in `executor.py` is gated on
`has_animal`, `carried_wheat > 0`, `carried_animal >= 0` or `fertilizer_available`, which is exactly
the eight ops above.

**Why this matters more than the plan tuning it hides.** CLAUDE.md records that FEED (+0.452) and
CARE (+0.441) are the two ops most correlated with money across 312 leaderboard seats, and that the
top agents draw ~83% of revenue from milk and wool. The whole animal half of `executor.py` -- herd
targets, `stock_day`, `feed_wheat`, the cash-reservation ordering -- is dead code in the *submission*
path regardless of how well it is tuned in the search harness, because `rollout.build_view` passes
these fields and `observation_view` does not.

This is the "verify game obs format" rule in `~/.claude/memory`: inspect the actual observation before
trusting field handling, rather than assuming the two `View` builders agree.

One theory, one test: does the parser see what the replay plainly contains?
"""

import json
import pathlib

import numpy as np
import pytest

from kagg.search import agent as A
from kagg.search import executor as X

EPISODE = pathlib.Path("data/episodes/89873723.json")
TURNS = [200, 400, 600]


def _raw_counts(farm):
    """Animals and pens straight out of the replay's own tile dicts, with no parsing in between."""
    animals = pens = 0
    for row in farm["tiles"]:
        for cell in row:
            if isinstance(cell, dict):
                if cell.get("animal"):
                    animals += 1
                if cell.get("kind") in ("PASTURE", "COOP"):
                    pens += 1
    return animals, pens


def _obs_at(turn, seat=0):
    ep = json.loads(EPISODE.read_text())
    cell = ep["steps"][turn][seat]
    obs = dict(cell["observation"])
    obs.setdefault("player", seat)
    return obs


@pytest.mark.skipif(not EPISODE.exists(), reason="replay not present")
@pytest.mark.parametrize("turn", TURNS)
def test_the_parser_sees_the_animals_the_replay_contains(turn):
    """**The bug.** A board with fourteen animals on it must not parse as an empty farm."""
    obs = _obs_at(turn)
    raw_animals, raw_pens = _raw_counts(obs["farms"][0])
    assert raw_animals > 0, "fixture is wrong: this turn has no animals to find"

    view = A.observation_view(obs)
    seen = int((view.animal[0] >= 0).sum())

    assert seen == raw_animals, (
        f"turn {turn}: the replay shows {raw_animals} animals on {raw_pens} pens and the parser "
        f"reports {seen}. Every livestock mask is gated on `has_animal`, so FEED, CARE, PICKUP and "
        f"PLACE can never fire and the animal economy is unreachable from the submission.")


@pytest.mark.skipif(not EPISODE.exists(), reason="replay not present")
@pytest.mark.parametrize("turn", TURNS)
def test_the_parser_counts_pens_correctly(turn):
    """Pens use `COOP = 4` and `PASTURE = 5` (`kagg/sim/tiles.py:28`).

    Included because my first probe of this asserted a pen over-count using `kind == 2 | 3`, which is
    `WEED | PLANT` -- a bug in the probe, not the parser. Pinning the real constants here so the
    claim is checked rather than remembered.
    """
    obs = _obs_at(turn)
    _, raw_pens = _raw_counts(obs["farms"][0])

    view = A.observation_view(obs)
    seen = int(((view.kind[0] == X.COOP) | (view.kind[0] == X.PASTURE)).sum())

    assert seen == raw_pens, f"turn {turn}: replay has {raw_pens} pens, parser reports {seen}"


@pytest.mark.skipif(not EPISODE.exists(), reason="replay not present")
def test_the_parser_reads_shed_wheat():
    """Feed lives in the shed under `WHEAT`, and `short = want_wheat - held` reads `shed_wheat`.

    Left at 0 by the default, the agent re-orders its entire feed requirement every single turn --
    the leak already pinned by `tests/test_wheat_not_reordered.py`, reachable here through a second
    route that that test cannot see because it hand-builds its `View`.
    """
    ep = json.loads(EPISODE.read_text())
    found = None
    for turn in range(len(ep["steps"])):
        obs = _obs_at(turn)
        held = int(((obs.get("private") or {}).get("shed") or {}).get("WHEAT", 0))
        if held > 0:
            found = (turn, held)
            break
    if found is None:
        pytest.skip("this replay never records shed wheat for the seat")

    turn, held = found
    view = A.observation_view(_obs_at(turn))
    assert int(view.shed_wheat[0]) == held, (
        f"turn {turn}: shed holds {held} wheat, parser reports {int(view.shed_wheat[0])}")
