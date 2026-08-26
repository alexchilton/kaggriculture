"""Which board features decide WHICH opening the shared script plays? Fit a tree and read it.

Alex, 2026-08-26: *"ok can you use the decision tree to work it out?"*

`data/logs/tape_coverage.log`: the shared script emits five openings over 139 seats, and 121 of them
sit on a shop draw that maps to exactly ONE opening -- so the selector is close to deterministic and
should be recoverable. Two branches are already readable by eye:

    356835aca0   every one of its 17 draws BEGINS with YARN_STORE   -> yarn unlocks d3
    d198b9f673   every one of its 8 draws has YARN in slot 2        -> yarn unlocks d6

What is not readable by eye is the split between `d1f515b59d` (49 seats) and `62d81623f9` (40), which
between them are 89 of the 139. Their draw sets overlap, so the shops alone do not choose.

カワシギ's selector is two bits -- the yarn store at d5 AND the opponent's melon count >= 9 at d3
(`project_kaggriculture_only_two_bits_vary`). So the opponent's board is a candidate feature here and
is included.

Features, all readable at d3 or earlier by an agent that must decide at d3:

    shop_1..shop_4        which shop unlocked in each slot, as categories
    yarn_slot             the unlock slot YARN_STORE landed in, 9 if never (by d12)
    opp_melon_d3          the opponent's melon tiles at dawn d3   <- kawa's second bit
    opp_straw_d3          the opponent's strawberry tiles at dawn d3
    opp_wheat_d3          likewise wheat
    opp_tiles_d3          how much ground the opponent holds at d3

Target is the opening hash. A shallow tree is fitted and printed as rules; accuracy is reported on
the training set deliberately -- the question is "is this rule RECOVERABLE", not "does it
generalise", and a deterministic selector should be fittable to near 100% by a small tree.
"""

import collections
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
NEW = "data/seed_scripts/daily_2026-08-26"
OPEN_TO = 11
SCRIPT = {"d1f515b59d", "62d81623f9", "356835aca0", "123c42fb5d", "d198b9f673"}


def stream_hash(replay, seat, last_day=OPEN_TO):
    parts = []
    for t, step in enumerate(replay.get("steps") or []):
        if t // TPD > last_day or seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        parts.append("|".join("-".join(str(x) for x in o) if o else "." for o in ops))
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()[:10]


def shop_order(replay, upto_day=12):
    order = []
    for t in range(0, len(replay.get("steps") or []), TPD):
        if t // TPD > upto_day:
            break
        cur = list((((replay["steps"][t][0] or {}).get("observation") or {}).get("town")
                    or {}).get("unlocked_shops") or [])
        while len(order) < len(cur):
            order.append(cur[len(order)])
    return order


def board_at(replay, seat, day):
    t = day * TPD
    steps = replay.get("steps") or []
    if t >= len(steps):
        return collections.Counter(), 0
    farms = ((steps[t][0] or {}).get("observation") or {}).get("farms") or []
    if seat >= len(farms):
        return collections.Counter(), 0
    crops = collections.Counter()
    tiles = 0
    for row in (farms[seat].get("tiles") or []):
        for c in row:
            if isinstance(c, dict):
                if c.get("owned", True):
                    tiles += 1
                if c.get("crop"):
                    crops[c["crop"]] += 1
    return crops, tiles


def main():
    rows = []
    for f in sorted(pathlib.Path(NEW).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        order = shop_order(r)
        yarn_slot = order.index("YARN_STORE") if "YARN_STORE" in order else 9
        for seat in range(min(2, len(names))):
            h = stream_hash(r, seat)
            if h not in SCRIPT:
                continue
            opp = 1 - seat
            crops, tiles = board_at(r, opp, 3)
            rows.append(dict(
                y=h, yarn_slot=yarn_slot,
                shop_1=order[0] if len(order) > 0 else "-",
                shop_2=order[1] if len(order) > 1 else "-",
                shop_3=order[2] if len(order) > 2 else "-",
                shop_4=order[3] if len(order) > 3 else "-",
                opp_melon_d3=crops.get("MELON", 0),
                opp_straw_d3=crops.get("STRAWBERRY", 0),
                opp_wheat_d3=crops.get("WHEAT", 0),
                opp_tiles_d3=tiles,
            ))
    print(f"{len(rows)} seats on the shared script")
    print("   target distribution: "
          + "  ".join(f"{h} {c}" for h, c in collections.Counter(r["y"] for r in rows).most_common()))
    print()

    try:
        from sklearn.tree import DecisionTreeClassifier, export_text
    except ImportError:
        print("sklearn not available"); return

    shops = sorted({r[k] for r in rows for k in ("shop_1", "shop_2", "shop_3", "shop_4")})
    feats, names_ = [], []
    for slot in ("shop_1", "shop_2", "shop_3", "shop_4"):
        for s in shops:
            names_.append(f"{slot}=={s}")
    names_ += ["yarn_slot", "opp_melon_d3", "opp_straw_d3", "opp_wheat_d3", "opp_tiles_d3"]
    for r in rows:
        v = []
        for slot in ("shop_1", "shop_2", "shop_3", "shop_4"):
            v += [1 if r[slot] == s else 0 for s in shops]
        v += [r["yarn_slot"], r["opp_melon_d3"], r["opp_straw_d3"], r["opp_wheat_d3"],
              r["opp_tiles_d3"]]
        feats.append(v)
    y = [r["y"] for r in rows]

    for depth in (2, 3, 4, 6):
        clf = DecisionTreeClassifier(max_depth=depth, random_state=0)
        clf.fit(feats, y)
        acc = clf.score(feats, y)
        print(f"--- depth {depth}: fits {100*acc:.1f}% of seats")
        if depth in (3, 6):
            print(export_text(clf, feature_names=names_, max_depth=depth))
    clf = DecisionTreeClassifier(max_depth=6, random_state=0).fit(feats, y)
    imp = sorted(zip(names_, clf.feature_importances_), key=lambda kv: -kv[1])
    print("--- what the tree actually uses")
    for n, v in imp[:10]:
        if v > 0:
            print(f"   {n:<28}{v:>7.3f}")


if __name__ == "__main__":
    main()
