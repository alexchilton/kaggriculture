"""Two questions in one pass: does our release actually fill, and what shape is kawa's selling?

**Q1 -- is the room-making release working?** `schedule_agent` computes, unconditionally,

    room_needed = max(0, sum(shed.values()) + carried_home - SHED_CAPACITY)

and releases from the LARGEST holding when the shed cannot take tonight's drop. It is live -- the
`SELL_TO_MAKE_ROOM` name in the comment no longer exists as a constant, so nothing gates it. Yet the
shed still reaches 100/100 for 306 turns across 35 of our ladder games. Either the rule is not
emitting, or it emits and the market will not take it. Those need different fixes, so separate them:
at every turn where our shed is at or near the cap, count SELL orders EMITTED and units actually
FILLED (a shed drop paired with money rising -- never the offer stream, which re-posts every turn).

**Q2 -- what does kawa's selling look like?** Not how much, which we know (914 units to our 737 over
d12-d23), but the SHAPE: how many turns of the day carry a sell, how big each one is, and how evenly
they are spread. That is the thing to copy in concept.

Reads recorded replays only. No agent is driven, so nothing here depends on the unit-to-inventory
index mapping that produced two contradictory answers earlier today.
"""

import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

US = "alex chilton"
TPD = 24
CAP = 100
KAWA_TAPE = "data/seed_scripts/kawa_2026-08-24/97466318.json"


def fills_and_orders(steps, seat):
    """Per turn: (shed_total, sell_orders_emitted, units_filled, money_delta)."""
    out = []
    prev_shed, prev_money = None, None
    for t, st in enumerate(steps):
        o = st[seat].get("observation") or {}
        priv = o.get("private") or {}
        shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
        farms = (st[0].get("observation") or {}).get("farms") or []
        money = float(farms[seat]["money"]) if len(farms) > seat else 0.0
        a = st[seat].get("action")
        sells = 0
        if isinstance(a, dict):
            sells = sum(1 for od in (a.get("market") or []) if od and od[0] == "SELL")
        filled = 0
        if prev_shed is not None and money > prev_money:
            filled = sum(max(0, prev_shed.get(k, 0) - shed.get(k, 0)) for k in set(prev_shed) | set(shed))
        out.append((sum(shed.values()), sells, filled, (money - prev_money) if prev_money is not None else 0.0))
        prev_shed, prev_money = shed, money
    return out


def main():
    # ---- Q1: our own ladder games -------------------------------------------------------
    agg = collections.Counter()
    near_rows = []
    games = 0
    for f in sorted(glob.glob(str(pathlib.Path.home() / "Downloads" / "*.json"))):
        rec = json.loads(pathlib.Path(f).read_text())
        names = (rec.get("info") or {}).get("TeamNames") or []
        if US not in names:
            continue
        me = names.index(US)
        rows = fills_and_orders(rec["steps"], me)
        games += 1
        for t, (tot, sells, filled, dmoney) in enumerate(rows):
            if not (12 <= t // TPD <= 23):
                continue
            if tot >= CAP:
                agg["cap_turns"] += 1
                agg["cap_with_sell_order"] += 1 if sells else 0
                agg["cap_units_filled"] += filled
                if len(near_rows) < 12:
                    near_rows.append((pathlib.Path(f).stem, t // TPD, t % TPD, tot, sells, filled))
            elif tot >= 90:
                agg["near_turns"] += 1
                agg["near_with_sell_order"] += 1 if sells else 0
                agg["near_units_filled"] += filled

    print(f"=== Q1: our {games} ladder games, solver zone d12-d23 ===")
    print(f"  turns with shed AT cap (100)      : {agg['cap_turns']:,}")
    print(f"     of those, a SELL was emitted   : {agg['cap_with_sell_order']:,}")
    print(f"     units that actually FILLED     : {agg['cap_units_filled']:,}")
    print(f"  turns with shed 90-99             : {agg['near_turns']:,}")
    print(f"     of those, a SELL was emitted   : {agg['near_with_sell_order']:,}")
    print(f"     units that actually FILLED     : {agg['near_units_filled']:,}")
    print("\n  sample cap turns (episode, day, hour, shed, sell orders, units filled):")
    for r in near_rows:
        print("    ", r)

    # ---- Q2: kawa's own recorded game ---------------------------------------------------
    rec = json.loads((REPO / KAWA_TAPE).read_text())
    names = (rec.get("info") or {}).get("TeamNames") or []
    his = names.index("カワシギ") if "カワシギ" in names else 0
    rows = fills_and_orders(rec["steps"], his)

    print(f"\n=== Q2: kawa's own game {pathlib.Path(KAWA_TAPE).stem}, seat {his} ===")
    print(f"  {'day':>4} {'shed peak':>10} {'turns w/ fill':>14} {'units sold':>11} "
          f"{'mean lot':>9} {'busiest lot':>12}")
    for d in range(30):
        chunk = rows[d * TPD:(d + 1) * TPD]
        if not chunk:
            break
        fills = [c[2] for c in chunk if c[2] > 0]
        peak = max(c[0] for c in chunk)
        print(f"  {d:>4} {peak:>10} {len(fills):>14} {sum(fills):>11} "
              f"{(sum(fills)/len(fills) if fills else 0):>9.1f} {(max(fills) if fills else 0):>12}")
    solver = [c for i, c in enumerate(rows) if 12 <= i // TPD <= 23]
    f = [c[2] for c in solver if c[2] > 0]
    print(f"\n  kawa d12-d23: {len(f)} turns carried a fill, {sum(f)} units, "
          f"mean lot {sum(f)/max(1,len(f)):.1f}, largest {max(f) if f else 0}, "
          f"shed peak {max(c[0] for c in solver)}")


if __name__ == "__main__":
    main()
