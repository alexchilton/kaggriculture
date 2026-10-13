"""How many of SpaTaro's day-blocks are actually distinct once the jitter is removed?

Counted raw, he has 44 distinct blocks in 44 games on every day, and
`fit_day_classifier` returns +0.0% over the majority baseline on all 30 days. But most
of that difference is measured noise, not plan:

  - 20.5% of his market order slots are malformed `BUY_PRODUCT` of produce the engine
    never sells. They are discarded by the engine and cost nothing.
  - his turn-0 opening has 21 raw variants and 3 once quantities are dropped.

So this strips one layer at a time and counts what survives. The level where the count
collapses to a handful is the level at which a block can be matched and spliced.

  L0  as recorded
  L1  drop malformed BUY_PRODUCT (anything but WHEAT and FERTILIZER)
  L2  L1, and drop market quantities
  L3  L2, and sort the hands within a turn (which hand does a job is not the plan)
  L4  L3, and drop movement (the walk is the planner's job; the ops are the plan)
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOCKS = ROOT / "data/logs/day_rows_spataro.blocks.json"
ROWS = ROOT / "data/logs/day_rows_spataro.json"
BUYABLE = {"WHEAT", "FERTILIZER"}
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


def norm(action, level):
    farmer = list(action.get("farmer") or [])
    hands = [list(h) for h in (action.get("hands") or [])]
    market = [list(o) for o in (action.get("market") or []) if o]
    if level >= 1:
        market = [o for o in market
                  if not (o[0] == "BUY_PRODUCT" and (len(o) < 2 or o[1] not in BUYABLE))]
    if level >= 2:
        market = [o[:2] for o in market]
    if level >= 3:
        hands = sorted(hands, key=lambda h: json.dumps(h))
    if level >= 4:
        farmer = [] if farmer and farmer[0] in MOVES else farmer
        hands = [h for h in hands if not (h and h[0] in MOVES)]
    return json.dumps([farmer, hands, sorted(market)], sort_keys=True, default=str)


def main():
    blocks = json.loads(BLOCKS.read_text())
    rows = json.loads(ROWS.read_text())
    # which block id each game-day played, so a count is per GAME not per unique id
    played = defaultdict(list)
    for r in rows:
        played[str(r["day"])].append(r["block"])

    print(f"{'day':>3} {'games':>5}   " + "  ".join(f"L{l:<5}" for l in range(5)))
    totals = defaultdict(list)
    for day in sorted(blocks, key=int):
        ids = played.get(day, [])
        if not ids:
            continue
        cells = []
        for level in range(5):
            sigs = Counter()
            for bid in ids:
                b = blocks[day].get(bid)
                if b is None:
                    continue
                sigs["".join(norm(a, level) for a in b)] += 1
            cells.append(len(sigs))
            totals[level].append(len(sigs) / max(1, len(ids)))
        print(f"{day:>3} {len(ids):>5}   " + "  ".join(f"{c:<6}" for c in cells))
    print("\nmean distinct blocks as a fraction of games played:")
    for level in range(5):
        import statistics
        print(f"  L{level}: {statistics.mean(totals[level]):.3f}")


if __name__ == "__main__":
    main()
