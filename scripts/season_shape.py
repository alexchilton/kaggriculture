"""What a season actually DOES: crew, herd, ground, water, market -- counted off the action stream.

Byte-level tape diffs answer "is it our file". They do not answer "is their farm run differently",
which is the only question that decides whether their play is worth adopting. Every number here is
counted the same way for a recorded replay and for one of our shipped tapes, so the two columns are
comparable.

    python -u scripts/season_shape.py mtmr_s1 Majkel1337 "Yusuke Hayashi" SpaTaro

`--ours` adds our release's 13 tapes as a pseudo-team.
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
TAPES = ROOT / "submission/hay_router2/actions.json"
UNIT_OPS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "BUILD", "DIG", "PICKUP", "DROP",
            "PLACE", "COLLECT_FERTILIZER", "FERTILIZE", "MOVE", "PASS")


def shape(stream):
    """One season's ops. `stream` is a list of 719 action dicts (or their json strings)."""
    c = collections.Counter()
    first_hire = None
    for t, a in enumerate(stream):
        if isinstance(a, str):
            a = json.loads(a)
        if not a:
            continue
        for op in [a.get("farmer")] + list(a.get("hands") or []):
            if op:
                c["op:" + str(op[0])] += 1
        for o in a.get("market") or []:
            if not o:
                continue
            n = int(o[2]) if len(o) > 2 and isinstance(o[2], int) else 1
            if o[0] == "HIRE":
                c["HIRE"] += 1
                if first_hire is None:
                    first_hire = t
            elif o[0] == "BUY_LAND":
                c["LAND"] += 1
            elif o[0] == "BUY_ANIMAL":
                c["animal:" + o[1]] += n
            elif o[0] == "BUY_SEED":
                c["seed:" + o[1]] += n
            elif o[0] == "BUY_PRODUCT":
                c["buy:" + o[1]] += n
            elif o[0] == "SELL":
                c["sell:" + o[1]] += n
    c["first_hire_turn"] = -1 if first_hire is None else first_hire
    return c


def main():
    teams = [t for t in sys.argv[1:] if not t.startswith("--")]
    seen = set()
    runs = collections.defaultdict(list)
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen:
                continue
            seen.add(r["episode"])
            for seat, team in enumerate(r["teams"]):
                if team in teams and seat < len(r["actions"]):
                    runs[team].append((shape(r["actions"][seat]),
                                       r["rewards"][seat] if seat < len(r["rewards"]) else 0))
    runs["OURS (13 tapes)"] = [(shape(t), None) for t in json.loads(TAPES.read_text())]
    order = ["OURS (13 tapes)"] + teams

    keys = ["HIRE", "LAND", "animal:COW", "animal:SHEEP", "animal:GOOSE",
            "seed:WHEAT", "seed:MELON", "seed:STRAWBERRY", "seed:CARROT", "seed:TOMATO",
            "buy:WHEAT", "sell:WHEAT", "sell:MELON", "sell:MILK", "sell:WOOL", "sell:EGG",
            "sell:FERTILIZER", "sell:STRAWBERRY", "sell:CARROT",
            "op:PLANT", "op:WATER", "op:HARVEST", "op:FEED", "op:CARE", "op:BUILD",
            "op:PLACE", "op:DIG", "op:PICKUP", "op:DROP", "op:MOVE", "op:PASS",
            "first_hire_turn"]
    print(f"{'metric':20}" + "".join(f"{t[:15]:>16}" for t in order))
    print(f"{'seasons':20}" + "".join(f"{len(runs[t]):>16}" for t in order))
    for k in keys:
        row = f"{k:20}"
        for t in order:
            v = [s[k] for s, _b in runs[t]]
            row += f"{(sum(v)/len(v) if v else 0):>16,.1f}"
        print(row)
    row = f"{'mean bank':20}"
    for t in order:
        b = [x for _s, x in runs[t] if x]
        row += f"{(sum(b)/len(b) if b else 0):>16,.0f}"
    print(row)


if __name__ == "__main__":
    main()
