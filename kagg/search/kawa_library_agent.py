"""The schedule agent, driven by the row library instead of one recorded season.

Identical executor, different schedule. Everything the agent DOES -- routing, watering, the herd
split, the market block -- is `schedule_agent`; the only difference is which rows it plays. See
`kagg/search/kawa_rows.py` for what those rows are and why the middle has none.

**`make_agent` IGNORES the schedule it is handed.** `scripts/breakdown.py` passes the tape's own
schedule to whatever module `--module` names, and this module builds its own from the library. That
is the whole point of it, and it is also exactly the class of bug this repo keeps paying for -- a
harness measuring an agent that is not the one under discussion -- so the argument is named
`ignored_schedule`, the fact is printed on the returned agent's `.source`, and nothing here accepts
a schedule silently.
"""

from kagg.search import kawa_rows
from kagg.search import schedule_agent as _SA

#: Re-exported so `breakdown.load_agent_module` can check this is a schedule agent it can drive, and
#: so its header line reports the settings that are actually in force. These are the SAME objects
#: `schedule_agent` uses; this module has no dials of its own and must never grow any.
SELLABLE = _SA.SELLABLE
CUMULATIVE_SELLS = _SA.CUMULATIVE_SELLS
SELL_CARRY_DAYS = _SA.SELL_CARRY_DAYS
HIRE_FIRST = _SA.HIRE_FIRST


def make_agent(ignored_schedule=None, me=0, router=True, mid_from=None, opening_from=None):
    """`agent(obs, config) -> action`, playing `kawa_rows.build()`.

    `ignored_schedule` is discarded. It exists only so this module has the signature
    `breakdown.py`, `arena` and the submission builders already call.

    `mid_from` and `opening_from` are passed straight to `kawa_rows.build`; both exist so a
    measurement script can vary one thing from one command. Leave them None everywhere else --
    exactly one boundary ships, and no single season's opening does.
    """
    schedule = kawa_rows.build(mid_from=mid_from, opening_from=opening_from)
    agent = _SA.make_agent(schedule, me, router)
    agent.schedule = schedule
    agent.source = ("kawa_rows.build() from %s -- the schedule passed to make_agent was IGNORED"
                    % kawa_rows.LIBRARY)
    return agent
