"""What do we bank if we sell on KAWA'S cadence instead of our own?

Every sell rule tried today was ours with a knob turned. This one throws our sell logic away for
the solver zone and replays HIS market orders verbatim -- same turns, same products, same lot
sizes -- keeping our own unit actions. It is the direct test of the thing that has been true all
along and that no arm has addressed:

    kawa d12-d23   75 turns carried a fill, 797 units, mean lot 10.6, shed peak 97
    ours d12-d23   737 units, in a handful of huge lots, shed pinned at 95-100 all morning

**Clamping.** His shed is not our shed, so a verbatim `SELL WHEAT 60` may ask for more than we
hold. Each order is clamped to our shed at that turn. That makes this an approximation of his
cadence rather than a copy of his season, and the clamp is reported so the size of that gap is
visible rather than assumed.

**The market is contested.** We and the tape sell into the SAME book, so replaying his orders on
our side does not reproduce his prices -- both sides are now hitting the same curve. That is a
real effect, not an artefact to correct away: it is what would happen if we actually played this.

`--zone` picks which days get his cadence. Outside it our own market logic runs untouched.
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
TAPES = {
    "kawashigi": ("data/seed_scripts/kawa_2026-08-24/97466318.json",
                  "data/seed_scripts/kawashigi/schedule.json", 1240813987),
    "kawa_straw": ("data/seed_scripts/kawa_2026-08-24/97466318.json",
                   "data/seed_scripts/kawa_straw/schedule.json", 468411728),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="kawa_straw")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--zone", default="12-23")
    ap.add_argument("--ours", action="store_true", help="baseline: use our own market logic")
    args = ap.parse_args()
    lo, hi = (int(x) for x in args.zone.split("-"))
    global FILLS
    FILLS = json.loads((REPO / "data/logs/kawa_fill_schedule.json").read_text())

    import breakdown as B
    from kaggle_environments import make

    tape_path, sched_path, seed = TAPES[args.tape]
    SA = importlib.import_module(f"kagg.search.{args.module}")
    B.schedule_agent = SA
    raw = json.loads((REPO / sched_path).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    rec = json.loads((REPO / tape_path).read_text())
    steps = rec["steps"]
    names = (rec.get("info") or {}).get("TeamNames") or []
    his = names.index("カワシギ") if "カワシギ" in names else 0
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)

    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, 0)

    asked = filled_turns = 0
    clamped_units = asked_units = 0
    sold_units = collections.Counter()
    prev_shed = prev_money = None

    for t in range(30 * TPD):
        o = env.state[0].observation
        priv = o.get("private") or {}
        shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
        money = float(o["farms"][0]["money"])
        if prev_shed is not None and money > prev_money:
            d = sum(max(0, prev_shed.get(k, 0) - shed.get(k, 0))
                    for k in set(prev_shed) | set(shed))
            if d > 0:
                filled_turns += 1
                sold_units["total"] += d
        prev_shed, prev_money = shed, money

        day = t // TPD
        n = len(o["farms"][0].get("hands") or [])
        a = agent(o)
        at = steps[t + 1][his].get("action") if t + 1 < len(steps) else None
        at = at if isinstance(at, dict) else {}

        market = a["market"]
        if not args.ours and lo <= day <= hi:
            # **Only the SELLs are his.** Corrected 2026-08-25. `_process_market` carries HIRE,
            # BUY_LAND, BUY_SEED, BUY_PRODUCT and BUY_ANIMAL on this same channel, so the earlier
            # version -- which replaced the whole list -- switched our hiring and purchasing OFF for
            # the twelve days of the zone. It reported $19,701 and $22,186 against a $95k control
            # and those numbers measured a farm with no crew growth and no seed, not a cadence.
            # `scripts/his_cadence_across_seeds.py` is the version to use; this one is kept for the
            # two tape seeds only.
            # **His FILLS, not his offers.** The action stream re-posts the same quota every turn,
            # so replaying it verbatim asks for the day's whole allowance 24 times: the first
            # attempt at this clamped away 2,589 of 2,649 units (98%) and measured a harness
            # artefact, not a cadence. `data/logs/kawa_fill_schedule.json` is built from his shed
            # deltas on turns where his money rose -- 137 turns and 1,397 units over the season,
            # 75 turns and 797 units in d12-d23.
            his_sells = []
            for prod, q in (FILLS.get(str(t)) or {}).items():
                if prod not in SA.SELLABLE:
                    continue
                asked += 1
                asked_units += int(q)
                take = min(int(q), shed.get(prod, 0))
                clamped_units += int(q) - take
                if take > 0:
                    his_sells.append(["SELL", prod, take])
            market, placed = [], False
            for o in (a["market"] or []):
                if isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL":
                    if not placed:
                        market.extend(his_sells)
                        placed = True
                    continue
                market.append(o)
            if not placed:
                market.extend(his_sells)
            market = market[:10]                      # maxMarketOrdersPerTurn

        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n], "market": market}
        n2 = len(o["farms"][1].get("hands") or [])
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n2],
                 "market": at.get("market") or []}
        env.step([mine, yours])
        if env.done:
            break

    final = float(env.state[0].observation["farms"][0]["money"])
    theirs = float(env.state[0].observation["farms"][1]["money"])
    mode = "OUR cadence" if args.ours else f"KAWA cadence d{lo}-d{hi}"
    print(f"\n=== {args.tape}  {args.module}  {mode} ===")
    print(f"  final bank        {final:>12,.0f}   tape {theirs:>12,.0f}   "
          f"margin {final - theirs:>+12,.0f}")
    print(f"  turns with a fill {filled_turns:>12,}")
    print(f"  units sold        {sold_units['total']:>12,}")
    if not args.ours:
        print(f"  his orders replayed {asked:>10,}  units asked {asked_units:>8,}  "
              f"units clamped away {clamped_units:>8,}")


if __name__ == "__main__":
    main()
