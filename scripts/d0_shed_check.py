"""Is d0's `BUY_PRODUCT 5/8` + `SELL 0/3` the same NET wheat, or a real shortfall?

The grid scores OPS. `kawa_rows.net_the_round_trip` removed a SELL the tape emits, so the op counts
must differ by construction. What must NOT differ is the shed the day ends on -- if it does, netting
changed the plan rather than simplifying it.
"""
import sys
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import scripts.breakdown as BD                                              # noqa: E402
from kagg.search import kawa_library_agent                                  # noqa: E402


def main():
    BD.schedule_agent = BD.load_agent_module("schedule_agent")
    replay, _s, team = BD.TAPES["kawashigi"]
    economy, shops = BD.env_config(replay), BD.recorded_shops(replay)
    opp = lambda: BD.tape_policy(replay, team, 1)                           # noqa: E731

    def mine():
        a = kawa_library_agent.make_agent(None, 0, router=True, opening_from="92498144")
        return lambda o, t: a(o)

    ours, oo, _c, _d = BD.run(mine, opp, 11, 0.0, stop_day=2, economy=economy, shops=shops)
    his, ho, _c2, _d2 = BD.run(lambda: BD.tape_policy(replay, team, 0), opp, 11, 0.0,
                               stop_day=2, economy=economy, shops=shops)

    for day in (0, 1):
        print("end of d%d, ours/tape" % day)
        for k in ("shed_WHEAT", "shed_MILK", "shed_WOOL", "shed_FERTILIZER", "money"):
            print("  %-18s %s/%s" % (k, ours[day][k], his[day][k]))
        print("  BUY_PRODUCT        %d/%d" % (oo[day]["BUY_PRODUCT"], ho[day]["BUY_PRODUCT"]))
        print("  SELL               %d/%d" % (oo[day]["SELL"], ho[day]["SELL"]))
        print("  net wheat traded   ours %+d   tape %+d"
              % (oo[day]["BUY_PRODUCT"] - oo[day]["SELL"],
                 ho[day]["BUY_PRODUCT"] - ho[day]["SELL"]))
        print()


if __name__ == "__main__":
    main()
