"""A saving made on a replayed day buys things the tape could not afford.

The `BUY_SEED` trim inside `_replay_opening` caps his order at what our season can still plant --
his counts are sized for his season and the surplus sits dead in the shed. Sound on its own terms,
and NOT free on a replayed day: the bank is shared state, and the reference hires on it.

`_do_hire` fails **silently** on a thin bank (`reference/kaggriculture.py:691`) and the cost is
`mult * fib(hires_today)`. So $60 saved at d6 buys a hand at d8 that HE COULD NOT AFFORD, and one
extra hand for the rest of the season is not a rounding error.

Measured 2026-08-21, seed 7 against `kawashigi_b3`'s seat 1, field by field:

    d6   money +60  buy_seed -3                                    the trim
    d7   money +60
    d8   money -29  hands +1  hire +1  plant +2  water +1  ...      9 cells
         our hands 11, tape 10 -- his 11th hire refused, ours cleared
    d9+  weed, WHEAT and STRAWBERRY diverge for the rest of the season

Seed 899's town is richer, its 11th hire clears, and that season stays exact. That is the entire
130-vs-60 split the strawberry arm showed across 16 towns -- not the herd, not tape coverage, just
whether his d8 hire happened to be affordable on that draw.

**Three wrong theories died before this one, and each was disproved by a measurement rather than by
argument.** The herd re-label was the loudest: `animals x16` appeared in all ten bad seeds and none
of the five good ones, d8 is the day the tape places a SHEEP, and removing the re-label came back
**byte-identical** -- because d8 buys no animal at all. `PLACE` on d8 is a head bought on d7. A
byte-identical grid means the change was not on the path.

`scripts/seed_tape_grid.py --vs-all --live-shops --opponent kawashigi_b3`, 16 towns, d0-d29:

    trim on all arms      10 seeds 130-132,  5 seeds 60-62,  1 seed 40
    trim off strawberry    5 seeds  0,      10 seeds    25,  1 seed 40

The trim STAYS on the melon arm, where it is the whole margin: seed 11 at `--replay-days 30` ends
**+$240** on the leader with it and level at 0 cells without it. He wastes that seed; copying the
waste is not fidelity worth having.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import breakdown as B                                              # noqa: E402

#: A town on which the tape's d8 hire is refused. Seed 7 scored 131 cells with `d8 = 9`.
POOR_TOWN_SEED = 7
#: A town on which it clears, so the trim never mattered. Scored 60 with `d8 = 1`.
RICH_TOWN_SEED = 899


def cells(seed, days, opponent="kawashigi_b3", tape="kawashigi_b3"):
    """Differing cells per day, ours minus `tape`, with the seed drawing its own town.

    The opponent is `kawashigi_b3`'s seat 1, which holds 9 MELON tiles at d3 -- exactly
    `melon_branch.OPPONENT_MELON` -- so the melon latch arms and the strawberry tape is replayed.
    With the default opponent it never arms and this file measures nothing.

    **No `shops=`, deliberately.** `recorded_shops` injects the tape's own town into both columns,
    and on the tape's own town his hire always clears -- so with it on, this test cannot fail.
    """
    B.schedule_agent = B.load_agent_module(B.DEFAULT_MODULE)
    replay, schedule, team = B.TAPES[tape]
    opp_replay, _, opp_team = B.TAPES[opponent]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    economy = B.env_config(replay)

    def opp():
        return B.tape_policy(opp_replay, opp_team, 1)

    his, his_ops, _, _ = B.run(lambda: B.tape_policy(replay, team, 0), opp, seed, 0.0,
                               stop_day=days + 1, economy=economy)

    def mine():
        a = B.schedule_agent.make_agent(thin, 0, router=True)
        return lambda o, t: a(o)

    ours, our_ops, _, _ = B.run(mine, opp, seed, 0.0, stop_day=days + 1, economy=economy)

    state_fields = (["money", "hands", "owned", "pen", "weed"]
                    + ["crop_" + c for c in B.CROPS] + ["animals"])
    compass = {"NORTH", "SOUTH", "EAST", "WEST"}
    ops = [o for o in sorted(set(B.OPS) | {"OTHER"} | set(B.MARKET_FILL_OPS)) if o not in compass]
    return [sum(1 for k in state_fields if ours[d][k] != his[d][k])
            + sum(1 for o in ops if our_ops[d][o] != his_ops[d][o])
            for d in range(days)]


def test_a_poor_town_does_not_give_us_a_hand_the_tape_could_not_hire():
    """d0-d8 exact on the town where his 11th hire is refused.

    d8 is asserted because it is the day the extra hand appears; d0-d7 because a fix that repairs d8
    by moving the divergence earlier has not repaired anything.
    """
    per = cells(POOR_TOWN_SEED, days=9)
    assert per[:9] == [0] * 9, "per-day %s" % per


def test_the_town_that_never_had_the_problem_is_not_made_worse():
    """The control. Seed 899's hire already cleared, so it was exact here before the fix too.

    A change that repairs seed 7 by breaking seed 899 has moved the problem, not solved it.
    """
    per = cells(RICH_TOWN_SEED, days=9)
    assert per[:9] == [0] * 9, "per-day %s" % per


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
