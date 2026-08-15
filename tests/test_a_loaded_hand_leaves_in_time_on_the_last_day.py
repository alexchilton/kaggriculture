"""On the last day a loaded hand leaves for the shed at the last hour that still gets it there.

The plan-side fixes (the planned walk, the trimmed tail) close most of the gap and cannot close
the rest: the executor re-derives work at every stop, so a tour runs a turn or two longer than
the plan costed it, and the planned walk home starts too late. The d29 trace after those fixes
shows exactly two hands still stranding -- u8 harvests until h19, walks, and ends the season at
(4,3), ONE tile short of the shed, holding 11 units; u7 works until h22 three tiles out and
strands 12 (`data/logs/fable_d29_trace_after.log`).

The rule pinned here is the runtime mirror of the trimmed tail: a hand holding anything, on the
last day, with `24 - hour <= dist(pos, shed) + 1` turns left (the +1 is the DROP), abandons what
is left of its route and walks. Work it gives up would have made produce the close discards
anyway; leaving later than this bound loses the whole load by construction.

Only the last day. On every other day the overnight sweep banks a carried load for free, so
leaving early costs real work and buys nothing.
"""
import importlib

SA = importlib.import_module("kagg.search.schedule_agent")
R = importlib.import_module("kagg.search.routines")

LAST_DAY = R.SEASON_DAYS - 1
DEPOTS = tuple(sorted(SA.SHED))


def test_the_deadline_is_the_walk_plus_the_drop():
    """(0,0) is 8 steps from the nearest shed tile: leave at h15 (9 turns: 8 walk + 1 drop)."""
    pos, held = (0, 0), {"WHEAT": 3}
    assert SA.must_walk_home_now(LAST_DAY, 15, pos, held, DEPOTS), (
        "h15 at (0,0) holding wheat is the last turn that reaches the shed and drops; the hand "
        "stayed at work")
    assert not SA.must_walk_home_now(LAST_DAY, 14, pos, held, DEPOTS), (
        "h14 still has a turn of work in it; leaving now gives up a job for nothing")


def test_an_empty_hand_never_leaves_early():
    assert not SA.must_walk_home_now(LAST_DAY, 20, (0, 0), {}, DEPOTS)
    assert not SA.must_walk_home_now(LAST_DAY, 20, (0, 0), {"WHEAT": 0}, DEPOTS)


def test_every_other_day_takes_the_sweep():
    """d28's rollover banks the load free; abandoning work there is a pure loss."""
    assert not SA.must_walk_home_now(LAST_DAY - 1, 20, (0, 0), {"WHEAT": 3}, DEPOTS)


def test_it_follows_the_master_switch():
    """One revert restores the whole last-day family."""
    import kagg.search.router as RT
    old = RT.NO_UPKEEP_ON_THE_LAST_DAY
    try:
        RT.NO_UPKEEP_ON_THE_LAST_DAY = False
        assert not SA.must_walk_home_now(LAST_DAY, 20, (0, 0), {"WHEAT": 3}, DEPOTS)
    finally:
        RT.NO_UPKEEP_ON_THE_LAST_DAY = old
