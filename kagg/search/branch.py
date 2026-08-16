"""One shape for every schedule branch: read a trigger off the board, decide once, install rows.

## Why this exists, and it is not code reuse

The shared code is about twenty lines. What is shared and worth pinning is the CONTRACT, because
both ways of getting it wrong are silent:

**Decide once, then hold the answer.** The leader's melon purchase spans two days -- d5 buys 3
seeds, d6 buys 5 -- so a trigger re-read between them can answer differently and buy half a row of
each. `arm` latches into `state` on the first day at or after `decide_by_day` and never looks again.

**Clear and refill each row IN PLACE.** `schedule_agent.make_agent` shallow-copies the outer dict
but shares every row object with its caller, and reads them live every turn. Rebinding
`schedule[day] = new_row` therefore does nothing at all, while looking exactly like a working
branch -- the failure this project calls a byte-identical null. `install` does
`target.clear(); target.update(row)`.

## What a branch is

Three things, and nothing else:

    trigger(observation)   a predicate read off the board, true when the branch should be taken
    rows()                 {day: row} for the days it replaces
    split_day              the first day it replaces

`decide_by_day` is when the trigger is read, and it is normally EARLIER than `split_day`: the
decision has to be settled before the first row that spends money on it.

Subclasses are data plus a predicate. `melon_branch` and `q4_branch` are each about twenty lines of
code around an embedded season.
"""


class Branch:
    """A schedule branch. Subclass, set the four attributes, implement `trigger` and `rows`."""

    #: The day the trigger is READ. Normally earlier than `split_day`.
    decide_by_day = 0

    #: The first day whose row this branch replaces.
    split_day = 0

    #: Keys under which the decision is latched in the agent's per-game `state`.
    decided_key = "branch_decided"
    armed_key = "branch_armed"

    def trigger(self, observation):
        """True when the branch should be taken. Read off the board, never off our own plan."""
        raise NotImplementedError

    def rows(self):
        """`{day: row}` for `split_day` onwards. A fresh dict each call, so callers cannot mutate."""
        raise NotImplementedError

    def install(self, schedule):
        """Replace rows from `split_day` on, in place. True if anything moved.

        In place because the caller shares the row objects; see the module docstring.
        """
        moved = False
        for day, row in self.rows().items():
            if day < self.split_day:
                continue
            target = schedule.get(day) if hasattr(schedule, "get") else None
            if target is None:
                continue
            target.clear()
            target.update(row)
            moved = True
        return moved

    def arm(self, schedule, state, observation, day):
        """Decide once, on or after `decide_by_day`; install if the trigger fired. Returns the latch."""
        if state.get(self.decided_key):
            return state.get(self.armed_key, False)
        if day < self.decide_by_day:
            return False
        state[self.decided_key] = True
        state[self.armed_key] = bool(self.trigger(observation))
        if state[self.armed_key]:
            self.install(schedule)
        return state[self.armed_key]


def count_tiles(observation, seat, **match):
    """How many of `seat`'s tiles match every key/value given. `count_tiles(obs, 1, crop="MELON")`.

    Both branches ask a question of this shape and both wrote the nested loop out by hand.
    """
    farms = observation.get("farms") or []
    if not 0 <= seat < len(farms):
        return 0
    return sum(1 for row in (farms[seat].get("tiles") or []) for cell in row
               if isinstance(cell, dict) and all(cell.get(k) == v for k, v in match.items()))


def opponent_seat(observation):
    """The seat that is not ours. `player` is absent in some harnesses and defaults to seat 0."""
    return 1 - int(observation.get("player", 0) or 0)
