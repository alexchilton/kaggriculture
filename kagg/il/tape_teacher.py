"""The shipped agent, wrapped so DAgger can ask it "what would you do HERE?" every turn.

**Why this is not a recorded dataset.** A trajectory recorded from the agent and then fitted is
behaviour cloning on カワシギ's tapes, which was already tried. DAgger needs the labels to land on
states the *student* produced, so the teacher has to be a live call. That is the whole point of
this module: `TapeTeacher.act(obs)` answers from whatever board it is handed.

**What this teacher can and cannot teach.** The tape lookup is time-indexed -- `TAPE[key][step]` --
so on a board the student has damaged it answers "at turn t, on this branch, do X" rather than
re-planning a route around the damage. The branch *selection* is closed-loop and does move with the
board:

    melon_armed   read on day 3   opponent holds >= 9 MELON tiles      melon_branch.py:215
    q4_armed      read on day 5   the yarn store is already unlocked   q4_branch.py:242

plus the COW/SHEEP relabel in `_herd_split`, which reads `unlocked_shops`. With a fixed start state
and weeds off, the student's states stay near the tape, which is the condition that makes a
time-indexed teacher workable. See `docs/dagger_tape_teacher_2026-08-22.md`.

**Call it EVERY turn, in order, even on turns whose answer you discard.** The agent carries latches,
a purchase-intent counter, pen reservations and a sell ledger across turns. Skipping a query does
not skip that state, it corrupts it -- and the corruption is silent.

The agent itself is untouched. Nothing here writes to it.
"""
import collections

from kagg import plan as PLAN
from kagg.search import schedule_agent as SA

#: Turns per day. `obs["step"]` is `day * TURNS_PER_DAY + hour`.
TURNS_PER_DAY = 24


def _closure_state(fn):
    """The agent's per-game `state` dict, read out of its closure. Best effort, never raises.

    `make_agent` does not return its state and this module will not edit the shipped agent to make
    it, so the latches are recovered by name from `__closure__`. Read-only, and used for logging
    only -- if the closure ever changes shape this returns None and nothing else breaks.
    """
    code = getattr(fn, "__code__", None)
    cells = getattr(fn, "__closure__", None)
    if code is None or not cells:
        return None
    names = list(code.co_freevars)
    if "state" not in names:
        # `replayed` closes over `agent`; the state lives one level in.
        if "agent" in names:
            try:
                return _closure_state(cells[names.index("agent")].cell_contents)
            except (ValueError, AttributeError):
                return None
        return None
    try:
        found = cells[names.index("state")].cell_contents
    except (ValueError, AttributeError):
        return None
    return found if isinstance(found, dict) else None


class TapeTeacher:
    """`teacher.act(obs) -> {"farmer": [...], "hands": [...], "market": [...]}`.

    One instance per episode, per seat. It is stateful by construction; reusing one across two
    games replays the first game's latches into the second.
    """

    def __init__(self, seat=0, plan_path=None, router=True):
        self.seat = int(seat)
        #: `kagg.plan.load` is the one loader; the path used to be written out longhand in 27 files.
        self.plan = PLAN.load(plan_path)
        self._agent = SA.make_agent(self.plan, self.seat, router=router)
        self._state = _closure_state(self._agent)
        self.turns = 0
        self.ops = collections.Counter()

    @staticmethod
    def step_of(obs):
        """`obs["step"]`, derived from day/hour when the harness omits it.

        **Seat 1 gets no `step`.** kaggle-environments populates it only for seat 0, so an agent
        seated second reads step 0 every turn and replays turn 0 all season. Tape `(True, True)` is
        a seat-1 recording, so this is not a hypothetical.
        """
        step = obs.get("step")
        if step is not None:
            return int(step)
        return int(obs.get("day", 0) or 0) * TURNS_PER_DAY + int(obs.get("hour", 0) or 0)

    @property
    def latches(self):
        """`(melon_armed, q4_armed)` -- which of the four tapes is being replayed. None if unread."""
        if self._state is None:
            return None
        from kagg.search import melon_branch as MB, q4_branch as Q4

        return (bool(self._state.get(MB.BRANCH.armed_key)),
                bool(self._state.get(Q4.BRANCH.armed_key)))

    def act(self, obs):
        """Ask the teacher. `obs` is the reference environment's dict observation for our seat."""
        if obs.get("step") is None:
            obs = dict(obs)
            obs["step"] = self.step_of(obs)
        action = self._agent(obs)
        self.turns += 1
        self.ops[(action.get("farmer") or ["PASS"])[0]] += 1
        for hand in action.get("hands") or []:
            if hand:
                self.ops[hand[0]] += 1
        return action

    def sendable(self, action, n_units):
        """`action` trimmed to the units that actually exist, ready for `env.step`.

        The agent plans for the crew it expects; the harness accepts one entry per LIVE unit. The
        atomic PLANT rule counts actions *submitted*, so an over-long hand list is not harmless.
        """
        return {"farmer": list(action.get("farmer") or ["PASS"]),
                "hands": [list(h) for h in list(action.get("hands") or [])[:int(n_units)]],
                "market": [list(o) for o in (action.get("market") or [])]}
