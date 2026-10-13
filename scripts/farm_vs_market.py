"""Is the FARM scripted and the MARKET live? Measured by splitting the stream in two.

A season's action is two independent things: the unit ops (farmer + hands) and the market orders.
Comparing the whole action treats one live market order as a divergence of the entire turn, so a
scripted farm with a reactive market reads as "adaptive" and its tape is never seen.

Split them and the question answers itself:

    unit ops agree deep, market shallow  ->  fixed farm, live market   (clone the farm, not the book)
    both agree deep                      ->  fixed tape
    both shallow                         ->  reads the board

    python -u scripts/farm_vs_market.py mtmr_s1 Majkel1337
"""
import collections, itertools, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
TAPES = ROOT / "submission/hay_router2/actions.json"


def split(stream):
    farm, mkt = [], []
    for a in stream:
        if isinstance(a, str):
            a = json.loads(a)
        a = a or {}
        farm.append(json.dumps([a.get("farmer"), a.get("hands")]))
        mkt.append(json.dumps(a.get("market")))
    return farm, mkt


def agree(a, b):
    k = 0
    for x, y in zip(a, b):
        if x != y:
            break
        k += 1
    return k


def same(a, b):
    return sum(1 for x, y in zip(a, b) if x == y)


def load(team):
    seen, out = set(), []
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen:
                continue
            seen.add(r["episode"])
            for seat, t in enumerate(r["teams"]):
                if t == team and seat < len(r["actions"]) and r["actions"][seat]:
                    out.append((r["episode"], r["world"][seat], r["actions"][seat]))
    return out


def report(name, seasons):
    sp = [split(s) for s in seasons]
    n = len(sp)
    if n < 2:
        print(f"{name}: {n} season, nothing to compare")
        return
    fa, ma, fs, ms = [], [], [], []
    for i, j in itertools.combinations(range(n), 2):
        fa.append(agree(sp[i][0], sp[j][0]))
        ma.append(agree(sp[i][1], sp[j][1]))
        fs.append(same(sp[i][0], sp[j][0]) / len(sp[i][0]) * 100)
        ms.append(same(sp[i][1], sp[j][1]) / len(sp[i][1]) * 100)
    f = lambda v: f"{min(v):>4}-{max(v):<4} med {sorted(v)[len(v)//2]:>4}"
    g = lambda v: f"{min(v):>5.1f}-{max(v):<5.1f} med {sorted(v)[len(v)//2]:>5.1f}"
    print(f"\n{name}: {n} seasons, {len(fa)} pairs")
    print(f"   FARM  ops  prefix {f(fa)}   turns identical {g(fs)}%")
    print(f"   MARKET     prefix {f(ma)}   turns identical {g(ms)}%")


def main():
    for team in sys.argv[1:] or ["mtmr_s1"]:
        v = load(team)
        report(team, [a for _e, _w, a in v])
    report("OURS (13 tapes)", json.loads(TAPES.read_text()))


if __name__ == "__main__":
    main()
