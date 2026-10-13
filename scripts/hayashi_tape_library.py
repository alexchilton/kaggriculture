"""Cluster Hayashi's live seasons into his actual tape library.

He replays with ~26 of 719 turns of repair noise inside one world, while distinct
tapes differ on 129-341 turns. So single-linkage at a threshold between the two
recovers the library, and the world each cluster appears in recovers his routing
key.

The published set is 13: one default for every non-yarn draw, eleven keyed on
which shop pairs with YARN_STORE, and one shared ending forced at step 648. The
question is whether his current library keeps that shape.
"""
import json, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THRESHOLD = 80          # between his 26-turn repair noise and the 129-turn tape gap


def load(folder):
    out = []
    for p in sorted((Path(folder) / "summaries").glob("*.summary.json")):
        rec = json.loads(p.read_text())
        for seat, team in enumerate(rec["teams"]):
            if team.startswith("Yusuke"):
                out.append({"episode": rec["episode"], "world": "|".join(rec["world"]),
                            "bank": rec["rewards"][seat],
                            "actions": rec["actions"][seat]})
    return out


def main(folder="data/replays_hayashi"):
    seasons = load(folder)
    print(f"{len(seasons)} Hayashi seasons")
    if not seasons:
        return
    parent = list(range(len(seasons)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(seasons)):
        for j in range(i + 1, len(seasons)):
            d = sum(1 for x, y in zip(seasons[i]["actions"], seasons[j]["actions"]) if x != y)
            if d < THRESHOLD:
                parent[find(i)] = find(j)
    clusters = defaultdict(list)
    for i, s in enumerate(seasons):
        clusters[find(i)].append(s)

    print(f"\n{len(clusters)} distinct tapes at a {THRESHOLD}-turn threshold\n")
    print(f"{'tape':>5} {'seasons':>8} {'median bank':>12}  worlds")
    yarn_tapes = non_yarn = 0
    for k, members in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
        worlds = sorted({m["world"] for m in members})
        banks = sorted(m["bank"] for m in members)
        has_yarn = any("YARN_STORE" in w for w in worlds)
        yarn_tapes += has_yarn
        non_yarn += (not has_yarn)
        print(f"{k:>5} {len(members):>8} {banks[len(banks)//2]:>12,.0f}  "
              f"{'YARN ' if has_yarn else '     '}{', '.join(w for w in worlds[:4])}"
              f"{' ...' if len(worlds) > 4 else ''}")
    print(f"\ntapes seen in yarn worlds: {yarn_tapes}   non-yarn only: {non_yarn}")
    print("published structure for comparison: 1 non-yarn default + 11 yarn variants + 1 ending")

    out = ROOT / "submission" / "hay_library"
    out.mkdir(exist_ok=True)
    index = {}
    for k, members in clusters.items():
        best = max(members, key=lambda m: m["bank"])
        name = f"tape_{k}.json"
        (out / name).write_text(json.dumps([json.loads(a) for a in best["actions"]]))
        for w in {m["world"] for m in members}:
            index.setdefault(w, name)
    (out / "index.json").write_text(json.dumps(index, indent=2, sort_keys=True))
    print(f"\nwrote {len(clusters)} tapes + index.json to {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/replays_hayashi")
