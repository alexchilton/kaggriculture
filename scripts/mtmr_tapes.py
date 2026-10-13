"""How many distinct FARM tapes does mtmr_s1 run, and does the choice follow the world?

mtmr_s1 sits at 2907.5, ~240 above every public notebook, and its play is tape-like where it counts:
seasons pair up with byte-identical 719-turn FARM streams (PLANT/WATER/HARVEST/FEED/CARE and the
MOVE/PICKUP/DROP that deliver), while the market moves. If the farm is a small set of fixed tapes
selected by the shop draw -- the way yhay81's 13 routes are -- it is extractable the same way.

Clusters on the FARM stream alone (market excluded, PASS kept, since an idle turn is part of the
route) and prints the worlds each cluster was seen in.

    python -u scripts/mtmr_tapes.py mtmr_s1
"""
import collections, itertools, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def farm(stream):
    out = []
    for a in stream:
        if isinstance(a, str):
            a = json.loads(a)
        a = a or {}
        out.append(json.dumps([a.get("farmer"), a.get("hands")]))
    return out


def main():
    team = sys.argv[1] if len(sys.argv) > 1 else "mtmr_s1"
    seen, runs = set(), []
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen:
                continue
            seen.add(r["episode"])
            for seat, t in enumerate(r["teams"]):
                if t == team and seat < len(r["actions"]) and r["actions"][seat]:
                    runs.append((r["episode"], r["world"][seat], farm(r["actions"][seat]),
                                 r["rewards"][seat] if seat < len(r["rewards"]) else None))
    n = len(runs)
    print(f"{team}: {n} seasons\n")

    def pref(a, b):
        k = 0
        for x, y in zip(a, b):
            if x != y:
                break
            k += 1
        return k

    for thr in (719, 600, 400, 200):
        par = list(range(n))

        def find(i):
            while par[i] != i:
                par[i] = par[par[i]]
                i = par[i]
            return i
        for i, j in itertools.combinations(range(n), 2):
            if pref(runs[i][2], runs[j][2]) >= thr:
                a, b = find(i), find(j)
                if a != b:
                    par[a] = b
        g = collections.defaultdict(list)
        for i in range(n):
            g[find(i)].append(i)
        sizes = sorted((len(v) for v in g.values()), reverse=True)
        print(f"farm-tape clusters at >= {thr:>3} identical turns: {len(g):>2} groups  sizes {sizes}")

    # the 719 clustering, with worlds -- is a tape tied to a shop?
    par = list(range(n))

    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for i, j in itertools.combinations(range(n), 2):
        if runs[i][2] == runs[j][2]:
            a, b = find(i), find(j)
            if a != b:
                par[a] = b
    g = collections.defaultdict(list)
    for i in range(n):
        g[find(i)].append(i)
    print(f"\nidentical-farm groups and the worlds they ran in:")
    print(f"{'group':>6}{'seasons':>9}  worlds")
    for k, v in sorted(g.items(), key=lambda kv: -len(kv[1])):
        w = collections.Counter(runs[i][1] for i in v)
        eps = [runs[i][0] for i in v]
        print(f"{k:>6}{len(v):>9}  {dict(w)}")
        if len(v) > 1:
            print(f"{'':15}  episodes {eps}")
    worlds = collections.Counter(r[1] for r in runs)
    print(f"\nworlds seen: {dict(worlds)}")
    print(f"distinct worlds {len(worlds)}, distinct farm tapes {len(g)}")


if __name__ == "__main__":
    main()
