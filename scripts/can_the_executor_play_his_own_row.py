"""Hand the executor Kawashigi's OWN d0-d12 rows. Does it reproduce his days?

Alex, 2026-08-21: "strange that it cant match the d3 -12..."

He is right to be suspicious, and the modal-row run cannot answer him. That run played the MODAL
row on every day, so "d3-d12 does not match" currently means "we chose a different plan" -- game
92498144 is only the modal season on d0, d1, d2 and d4. Nobody has tested whether the executor could
have played his plan if it had been handed it.

This is that test, and it is a FORK:

  A  it matches d0-d12. The executor is sound, the whole gap is SELECTION, and a d7-d13 selector is
     justified -- the 17-25% modal coverage is then the entire problem.
  B  it does not match. The executor cannot reproduce a row it was handed, no selector can fix that,
     and the first divergent day is the defect to name.

**This is NOT the op replay, and the two must not be confused.** It is already established that
replaying his ACTIONS reproduces his board exactly to d11. An action is a 24-turn op tape with
hours, coordinates, movement and WATER in it. A target row has none of those -- our router
regenerates every one of them. The op replay passing says nothing about whether the ROW round-trips.

`kawa_rows.build(opening_from=...)` runs his rows through `only_animals_get_placed` exactly as the
modal rows are, so a failure here cannot be the `places` extractor defect.

Grading is `breakdown.py`'s own: same `run`, same `snap`, same fills, same economy and injected shop
draw. PICKUP, DROP and PASS are tour shape and are exempt; the four compass rows likewise.

    python -u scripts/can_the_executor_play_his_own_row.py --seed 11 --days 13
"""

import argparse
import collections
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import scripts.breakdown as BD                                              # noqa: E402
from kagg.search import kawa_library_agent                                  # noqa: E402

TAPE = "kawashigi"
GAME = "92498144"
WEEDS = 0.0

#: Tour shape, not a defect. `PICKUP`/`DROP` are how goods reach the shed and the two sides route
#: differently by design; `PASS` is idle. The compass rows are the same argument -- we work the board
#: westward and the tape works it southward.
EXEMPT = frozenset(("PICKUP", "DROP", "PASS", "NORTH", "SOUTH", "EAST", "WEST"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--days", type=int, default=13)
    ap.add_argument("--detail", type=int, default=4,
                    help="print every differing field for this many leading days")
    a = ap.parse_args()

    BD.schedule_agent = BD.load_agent_module("schedule_agent")
    replay, _sched, team = BD.TAPES[TAPE]
    economy = BD.env_config(replay)
    shops = BD.recorded_shops(replay)
    opp = lambda: BD.tape_policy(replay, team, 1)                           # noqa: E731

    def mine():
        agent = kawa_library_agent.make_agent(None, 0, router=True, opening_from=GAME,
                                              mid_from=None)
        return lambda o, t: agent(o)

    ours, our_ops, _c, _d = BD.run(mine, opp, a.seed, WEEDS, stop_day=a.days + 1,
                                   economy=economy, shops=shops)
    his, his_ops, _c2, _d2 = BD.run(lambda: BD.tape_policy(replay, team, 0), opp, a.seed, WEEDS,
                                    stop_day=a.days + 1, economy=economy, shops=shops)

    n = a.days
    print("tape %s   game %s   seed %d   weeds %.3f   %s"
          % (TAPE, GAME, a.seed, WEEDS,
             "  ".join("%s %s" % kv for kv in economy.items())))
    print("  d0-d%d play %s's OWN target rows. Every cell is ours/tape.\n" % (n - 1, GAME))

    state_fields = ([("money", "money"), ("hands", "hands"), ("owned", "tiles"), ("pen", "pens"),
                     ("weed", "weeds")]
                    + [("crop_" + c, c.lower()[:6]) for c in BD.CROPS]
                    + [("animals", "animals")])

    def grid(title, rows, get_ours, get_his):
        print("  %s\n" % title)
        print("  %-13s" % "" + "".join("%13s" % ("d%d" % d) for d in range(n)))
        for key, lab in rows:
            cells = "".join("%13s" % ("%s/%s" % (get_ours(d, key), get_his(d, key)))
                            for d in range(n))
            print("  %-13s%s" % (lab, cells))
        print()

    live_state = [(k, lab) for k, lab in state_fields
                  if any(ours[d][k] or his[d][k] for d in range(n))]
    grid("board and herd at END of day", live_state,
         lambda d, k: ours[d][k], lambda d, k: his[d][k])

    unit_ops = [o for o in BD.OPS + ("OTHER",)
                if o not in ("NORTH", "SOUTH", "EAST", "WEST")
                and any(our_ops[d][o] or his_ops[d][o] for d in range(n))]
    grid("unit ops OFFERED that day", [(o, o.lower()[:12]) for o in unit_ops],
         lambda d, k: our_ops[d][k], lambda d, k: his_ops[d][k])

    fill_ops = [o for o in BD.MARKET_FILL_OPS
                if any(our_ops[d][o] or his_ops[d][o] for d in range(n))]
    grid("market FILLS that day, UNITS that committed", [(o, o.lower()[:12]) for o in fill_ops],
         lambda d, k: our_ops[d][k], lambda d, k: his_ops[d][k])

    grid("turn budget -- work + move + idle == unit-turns", list(BD.BUDGET_ROWS),
         lambda d, k: our_ops[d][k], lambda d, k: his_ops[d][k])

    # ---- the grade -----------------------------------------------------------------------------
    # **A day counts only if EVERY non-exempt tracked field matches.** There is no "essentially
    # exact"; `breakdown.py`'s own verdict block exists because a 67-cell gap got called near-exact
    # twice. Fields that are zero on both sides all week are excluded from the base -- they are not
    # evidence of agreement.
    tracked = ([("state", k, [(ours[d][k], his[d][k]) for d in range(n)]) for k, _ in state_fields]
               + [("op", o, [(our_ops[d][o], his_ops[d][o]) for d in range(n)])
                  for o in BD.OPS + ("OTHER",) if o not in EXEMPT]
               + [("fill", o, [(our_ops[d][o], his_ops[d][o]) for d in range(n)])
                  for o in BD.MARKET_FILL_OPS])
    base = [t for t in tracked if any(o or h for o, h in t[2])]

    per_day = [sum(1 for _k, _f, c in base if c[d][0] != c[d][1]) for d in range(n)]
    exact = [d for d, k in enumerate(per_day) if k == 0]
    print("  per-day differing cells (exempt: %s)" % ", ".join(sorted(EXEMPT)))
    print("    " + "  ".join("d%d=%d" % (d, k) for d, k in enumerate(per_day)))
    print("  %d/%d days exact: %s" % (len(exact), n, exact or "none"))

    # Every differing field for the first `--detail` days, not just the first divergent one. Days
    # grade in order, but a day whose miss is one cell is the cheapest diagnostic on the board and
    # printing only d0's fields hides it.
    for day in range(min(a.detail, n)):
        print("\n  d%d -- %s" % (day, "EXACT" if per_day[day] == 0
                                 else "%d differing cells" % per_day[day]))
        for kind, field, cells in base:
            o, h = cells[day]
            if o != h:
                print("    %-6s %-18s ours %8s   tape %8s   %+d" % (kind, field, o, h, o - h))


if __name__ == "__main__":
    main()
