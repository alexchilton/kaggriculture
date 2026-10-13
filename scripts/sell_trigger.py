"""What happens on the turns he sells? Not the price -- the EVENTS.

Every rule tested so far was a function of price, and all of them lost. The alternative is that the
sell is not a market decision at all: it is triggered by SUPPLY. A HARVEST or a COLLECT puts goods
in the shed, the shed caps at 100, and the sale is simply what clears the space.

For each SELL, this looks at what the farm did in the surrounding turns -- and at the shed level --
to see what the sale follows.

    python -u scripts/sell_trigger.py 107642213 107041112 107399673
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    agg = collections.defaultdict(collections.Counter)
    shedlv = collections.defaultdict(list)
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        steps = rep["steps"]
        for seat, team in enumerate(teams):
            ops = []          # per turn: set of op names
            sells = []        # per turn: set of products sold
            sheds = []        # per turn: total shed units
            for step in steps[1:]:
                cell = (step[seat] if seat < len(step) else None) or {}
                a = cell.get("action") or {}
                ops.append({op[0] for op in [a.get("farmer")] + list(a.get("hands") or []) if op})
                sells.append({o[1] for o in (a.get("market") or []) if o and o[0] == "SELL"})
                shed = ((cell.get("observation") or {}).get("private") or {}).get("shed") or {}
                sheds.append(sum(int(v or 0) for v in shed.values()))
            for t, s in enumerate(sells):
                if not s:
                    continue
                agg[team]["sell_turns"] += 1
                win = set()
                for k in range(max(0, t - 2), t + 1):
                    win |= ops[k]
                if "HARVEST" in win:
                    agg[team]["after_harvest"] += 1
                if "COLLECT_FERTILIZER" in win:
                    agg[team]["after_collect"] += 1
                if "DROP" in win:
                    agg[team]["after_drop"] += 1
                if t < len(sheds):
                    shedlv[team].append(sheds[t])
            for t, o in enumerate(ops):
                if "HARVEST" in o:
                    agg[team]["harvest_turns"] += 1
                    if any(sells[k] for k in range(t, min(len(sells), t + 3))):
                        agg[team]["harvest_then_sell"] += 1
    print(f"{'team':20}{'sell turns':>11}{'≤2 after HARVEST':>18}{'after COLLECT':>14}"
          f"{'after DROP':>12}{'median shed':>13}")
    for team, c in sorted(agg.items(), key=lambda kv: -kv[1]["sell_turns"]):
        n = c["sell_turns"]
        lv = sorted(shedlv[team])
        print(f"{team[:20]:20}{n:>11,}{100*c['after_harvest']/max(1,n):>17.1f}%"
              f"{100*c['after_collect']/max(1,n):>13.1f}%{100*c['after_drop']/max(1,n):>11.1f}%"
              f"{(lv[len(lv)//2] if lv else 0):>13}")
    print()
    print(f"{'team':20}{'harvest turns':>14}{'followed by a sell ≤2':>22}")
    for team, c in sorted(agg.items(), key=lambda kv: -kv[1]["sell_turns"]):
        h = c["harvest_turns"]
        print(f"{team[:20]:20}{h:>14,}{100*c['harvest_then_sell']/max(1,h):>21.1f}%")


if __name__ == "__main__":
    main()
