"""The opening replay must play the tape the LATCHES pick, not always the melon one.

`REPLAY_OPENING_TAPE` holds four tapes keyed on `(melon_armed, q4_armed)`, and `_replay_opening`
reads that key off `state` every turn. Nothing sets either key unless `_MB.arm` and `_Q4.arm` are
called -- and both calls were deleted from this module on 2026-08-20, when the agent was pointed at
tetsuya and カワシギ's rows were overwriting his. The key was therefore `(False, False)` on every
turn of every seed, so all four entries resolved to `92498144` and three of the four tapes were
unreachable by construction.

Measured 2026-08-21 with the calls absent, `scripts/seed_tape_grid.py`, five seeds each, weeds 0.0:

    --tape kawashigi        d0-d20 exact, 0 differing cells        the melon tape, and the one played
    --tape kawashigi_b3     first bad day d3, 148 cells            the day the melon and berry tapes part
    --tape kawashigi_q4c    first bad day d5, 216 cells            the day the q3 and q4 tapes part

Both bad days land exactly where the tapes first disagree, which is what a wrong-tape replay looks
like: the ops are sent faithfully, into a board the plan does not describe.

These tests each play four to six days, so they are slow by this suite's standards and cheap
against the thing they protect -- a silent reversion here reads as a planner regression fifteen days
later.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import breakdown as B                                              # noqa: E402


def cells(tape, days, seed=11):
    """Independent differing cells per day, ours minus the tape, over `days` days."""
    B.schedule_agent = B.load_agent_module(B.DEFAULT_MODULE)
    replay, schedule, team = B.TAPES[tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    economy = B.env_config(replay)
    shops = B.recorded_shops(replay)

    def opp():
        return B.tape_policy(replay, team, 1)

    his, his_ops, _, _ = B.run(lambda: B.tape_policy(replay, team, 0), opp, seed, 0.0,
                               stop_day=days + 1, economy=economy, shops=shops)

    def mine():
        a = B.schedule_agent.make_agent(thin, 0, router=True)
        return lambda o, t: a(o)

    ours, our_ops, _, _ = B.run(mine, opp, seed, 0.0, stop_day=days + 1, economy=economy,
                                shops=shops)

    state_fields = (["money", "hands", "owned", "pen", "weed"]
                    + ["crop_" + c for c in B.CROPS] + ["animals"])
    compass = {"NORTH", "SOUTH", "EAST", "WEST"}
    ops = [o for o in sorted(set(B.OPS) | {"OTHER"} | set(B.MARKET_FILL_OPS)) if o not in compass]
    return [sum(1 for k in state_fields if ours[d][k] != his[d][k])
            + sum(1 for o in ops if our_ops[d][o] != his_ops[d][o])
            for d in range(days)]


def test_the_melon_latch_reaches_the_strawberry_tape():
    """d3 is the first day the two three-quadrant tapes disagree, and `melon_branch` decides on d3.

    The opponent in `92466371` holds 9 MELON tiles at d3 -- exactly `melon_branch.OPPONENT_MELON` --
    so this game arms, and an armed game must replay `92466371`'s own d3.
    """
    per = cells("kawashigi_b3", days=4)
    assert per[3] == 0, "d3 differs by %d cells; per-day %s" % (per[3], per)


def test_the_yarn_latch_fires_before_the_tapes_diverge():
    """`91907974` unlocks YARN_STORE at **d3**, and the q3/q4 tapes part company at **d5**.

    So the latch must have decided by d5, not d6. `DECIDE_BY_DAY` was 6, one day too late, and d5
    was played from the unarmed tape by construction -- the ops were sent faithfully, into a board
    the plan does not describe, and the board never recovered.

    Measured 2026-08-21, `scripts/seed_tape_grid.py --vs-all --live-shops`, 16 seed-drawn towns,
    differing cells over d0-d23 on the tape the latches actually chose:

        yarn store up by d3   6 seeds    23-29 cells
        yarn store up at d6   3 seeds       63 cells
        no yarn store         7 seeds       21 cells

    Same tape, same latch; the only difference is whether the decision was available before d5.
    """
    per = cells("kawashigi_q4c", days=7)
    assert per[5] == 0, "d5 differs by %d cells; per-day %s" % (per[5], per)
    assert per[6] == 0, "d6 differs by %d cells; per-day %s" % (per[6], per)


def test_the_melon_tape_still_matches_when_neither_latch_fires():
    """The regression guard. `92498144`'s opponent shows 5 MELON at d3 and its town has no yarn
    store at d6, so this game arms NEITHER latch and must keep replaying the melon tape exactly."""
    per = cells("kawashigi", days=7)
    assert per == [0] * 7, "per-day %s" % per


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
