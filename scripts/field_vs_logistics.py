"""Where does a top player's play stop being a tape -- in the FIELD, or in the DELIVERY?

`scripts/farm_vs_market.py` split each turn into farm ops and market orders and found the farm
scripted while the market moved. But "farm ops" is two different jobs sharing one stream:

    field       PLANT WATER HARVEST FEED CARE BUILD DIG FERTILIZE   -- what the schedule commits to
    logistics   MOVE PICKUP DROP PLACE PASS                         -- getting goods to the shed

A tape can fix the field (plant these tiles, water them) and still leave delivery to a live rule,
because which hand walks to the shed with what depends on the board, not on the plan. If that is
where the non-tape behaviour lives, the "adaptive" label on these players is really a delivery
router sitting on top of a fixed field schedule -- and that is a much smaller thing to copy.

    python -u scripts/field_vs_logistics.py Majkel1337 mtmr_s1 "Yusuke Hayashi" SpaTaro
"""
import collections, itertools, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
FIELD = {"PLANT", "WATER", "HARVEST", "FEED", "CARE", "BUILD", "DIG", "FERTILIZE",
         "COLLECT_FERTILIZER"}
#: PASS excluded on purpose. Two idle seasons match trivially, and idleness is not delivery --
#: including it made the logistics stream look far more repeatable than it is.
LOGI = {"MOVE", "PICKUP", "DROP", "PLACE"}


def split(stream):
    """Two parallel streams: the field commitment, and the delivery work."""
    f, l = [], []
    for a in stream:
        if isinstance(a, str):
            a = json.loads(a)
        a = a or {}
        ops = [a.get("farmer")] + list(a.get("hands") or [])
        f.append(json.dumps([o for o in ops if o and o[0] in FIELD]))
        l.append(json.dumps([o for o in ops if o and o[0] in LOGI]))
    return f, l


def agree(a, b):
    k = 0
    for x, y in zip(a, b):
        if x != y:
            break
        k += 1
    return k


def same(a, b):
    return 100.0 * sum(1 for x, y in zip(a, b) if x == y) / max(1, len(a))


def main():
    seen, runs = set(), collections.defaultdict(list)
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen:
                continue
            seen.add(r["episode"])
            for seat, t in enumerate(r["teams"]):
                if t in sys.argv[1:] and seat < len(r["actions"]) and r["actions"][seat]:
                    runs[t].append(r["actions"][seat])
    print(f"{'team':18}{'n':>4}{'FIELD prefix':>16}{'identical':>11}"
          f"{'LOGISTICS prefix':>19}{'identical':>11}")
    for team in sys.argv[1:]:
        v = [split(s) for s in runs.get(team, [])]
        if len(v) < 2:
            continue
        fa, la, fs, ls = [], [], [], []
        for i, j in itertools.combinations(range(len(v)), 2):
            fa.append(agree(v[i][0], v[j][0]))
            la.append(agree(v[i][1], v[j][1]))
            fs.append(same(v[i][0], v[j][0]))
            ls.append(same(v[i][1], v[j][1]))
        m = lambda x: statistics.median(x)
        print(f"{team[:18]:18}{len(v):>4}{f'{min(fa)}-{max(fa)}':>16}{m(fs):>10.0f}%"
              f"{f'{min(la)}-{max(la)}':>19}{m(ls):>10.0f}%")
    print("\nprefix = turns agreeing from turn 0; identical = median % of all 719 turns equal")


if __name__ == "__main__":
    main()
