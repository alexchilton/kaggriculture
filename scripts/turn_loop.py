"""Every turn of every day, ours against his, and WHICH layer differs.

`scripts/breakdown.py --diff` gives day totals. This gives the turn, and splits the difference into
the three layers so the answer is not "something is wrong on d7":

    router     the market queue -- HIRE, BUY_*, SELL. What the day DECIDED to spend.
    planner    which tiles got assigned which ops. What the day INTENDED to do.
    executor   the ops actually issued by units that turn. What the day DID.

The tape drives days 0..handover-1 so the board at the handover is his exactly, and the agent's own
`REPLAY_OPENING_DAYS` is disabled by the caller -- otherwise two replays fight and on his own world
the agent replays all 30 days, so the "planner" is never exercised at all.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TPD = 24


def unit_ops(action):
    c = Counter()
    for a in [action.get("farmer") or []] + list(action.get("hands") or []):
        if a:
            c[a[0]] += 1
    return c


#: The only two products `BUY_PRODUCT` can actually settle. The town centre is built as
#: `[p for p in PRODUCTS if p != "FERTILIZER"]` and stocks nothing else, so every other
#: `BUY_PRODUCT` is discarded by the engine without a trace in the observation.
BUYABLE = ("WHEAT", "FERTILIZER")


def market_ops(action):
    """The orders the engine can actually settle -- never the raw emission.

    **Both columns of this diff have to mean the same thing.** His tape emits `BUY_PRODUCT CARROT 3`,
    `MELON 18`, `MILK 40`, `STRAWBERRY 16`, `TOMATO 20` and so on; none of them are buyable, all are
    discarded, and printing them padded his side of every market row with orders that never happened.
    Our own rows carry no such thing -- they are rebuilt from engine fills
    (`scripts/tape_fills.py`), and 10 schedules over 323 buy entries contain only WHEAT and
    FERTILIZER -- so the diff was comparing our real orders against his intentions and calling the
    difference a fault.

    That is the same defect as reading his `seeds` row as a purchase total, one instrument over:
    an offer is not a fill. Alex, on seeing his decoys in the `his` column: "same bug from the other
    side - just as annoying".

    A quantity is still what was OFFERED -- the engine clamps it by the bank and there is no per-order
    fill in the action stream -- so a repeated unaffordable order still shows, which is deliberate:
    the six consecutive `BUY_SEED STRAWBERRY 6` on d8 h1-h6 is exactly the kind of fault this diff
    exists to surface. Only orders the engine CANNOT settle at all are dropped.
    """
    c = Counter()
    for o in (action.get("market") or []):
        if not o:
            continue
        if o[0] == "BUY_PRODUCT" and len(o) > 1 and o[1] not in BUYABLE:
            continue                      # discarded by the engine; not a difference
        q = o[2] if len(o) > 2 and isinstance(o[2], int) else 1
        c[o[0] if o[0] in ("HIRE", "BUY_LAND") else f"{o[0]} {o[1]}"] += q
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="spataro")
    ap.add_argument("--handover", type=int, default=7)
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument("--first-only", action="store_true",
                    help="stop at the first turn that differs and dump both sides in full")
    args = ap.parse_args()

    import kagg.plan as P
    from kagg.search import schedule_agent as SA
    SA.REPLAY_OPENING_DAYS = ()
    from kaggle_environments import make
    from scripts.breakdown import TAPES, tape_policy

    replay, schedule, team = TAPES[args.tape]
    r = json.loads((ROOT / replay).read_text())
    seat = r["info"]["TeamNames"].index(team)
    sched = {int(k): {kk: vv for kk, vv in row.items() if kk not in P.TAPE_ONLY}
             for k, row in json.loads((ROOT / schedule).read_text()).items()}

    env = make("kaggriculture",
               configuration={"seed": r["info"]["seed"], "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(sched, 0, router=True)
    tape = tape_policy(str(ROOT / replay), team, 0)
    opp = tape_policy(str(ROOT / replay), r["info"]["TeamNames"][1 - seat], 1)

    print(f"tape {args.tape}  seed {r['info']['seed']}  tape drives d0-d{args.handover-1}, "
          f"planner from d{args.handover}\n")
    print(f"{'turn':>6} {'d':>3} {'h':>3}  {'layer':<9} {'ours':<40} {'his'}")
    shown = 0
    for t in range(TPD * args.days):
        if env.done:
            break
        o0, o1 = env.state[0].observation, env.state[1].observation
        day, hour = t // TPD, t % TPD
        a0 = tape(o0, t) if day < args.handover else ours(o0)
        a1 = opp(o1, t)
        his = ((r["steps"][t + 1][seat] or {}) if t + 1 < len(r["steps"]) else {}).get("action") or {}

        if day >= args.handover:
            for layer, f in (("market", market_ops), ("units", unit_ops)):
                mine, theirs = f(a0), f(his)
                if mine != theirs:
                    d_ours = {k: v for k, v in (mine - theirs).items()}
                    d_his = {k: v for k, v in (theirs - mine).items()}
                    print(f"{t:>6} {day:>3} {hour:>3}  {layer:<9} "
                          f"{('+' + str(d_ours)) if d_ours else '-':<40} "
                          f"{('+' + str(d_his)) if d_his else '-'}")
                    shown += 1
                    if args.first_only and shown >= 6:
                        print(f"\nfull turn {t} (d{day} h{hour}):")
                        print(f"  our money ${o0['farms'][0]['money']:,.0f}  "
                              f"row {sched.get(day, {})!r}"[:300])
                        print(f"  OUR market : {a0.get('market')}")
                        print(f"  HIS market : {his.get('market')}")
                        print(f"  OUR farmer : {a0.get('farmer')}  hands {a0.get('hands')}")
                        print(f"  HIS farmer : {his.get('farmer')}  hands {his.get('hands')}")
                        return
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                   "market": a1["market"]}])


if __name__ == "__main__":
    main()
