"""SpaTaro's seasons as a world-keyed tape library, the same shape as hay_library.

The world -- the first two shops unlocked at step 144 -- is a pure function of the seed
(measured: independent of tape, opponent and seat). He conditions on the town and not on
the opponent (his peak herd against the opponent's herd at day 6 is +0.09). So his
recording for a world is a valid plan for that world, and a tape per world is replayable.

One tape per world, the best-banked season he played there -- ALL of them, not 13. The
chassis asserts exactly 13 tapes (`router.py:207`), which is a statement about the
published set, not a constraint of the replay; `build_spa_router.py` relaxes it to "at
least one complete tape" so every world he has played keeps its own season. Capping at 13
sent seed 11 to a tape from a different town and cost 47k on that seed alone.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09"]
OUT = ROOT / "submission" / "spa_library"


def main():
    by_world = defaultdict(list)
    for d in DIRS:
        for f in sorted((ROOT/d).glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            r = json.loads(f.read_text())
            if "SpaTaro" not in r["info"]["TeamNames"]:
                continue
            seat = r["info"]["TeamNames"].index("SpaTaro")
            st = r["steps"]
            obs = st[144][seat]["observation"]
            world = tuple(((obs.get("town") or {}).get("unlocked_shops") or [])[:2])
            if len(world) < 2:
                continue
            by_world["|".join(world)].append(
                {"bank": r["rewards"][seat], "ep": r["info"]["EpisodeId"],
                 "actions": [s[seat].get("action") for s in st[1:]]})

    print(f"{len(by_world)} worlds over {sum(len(v) for v in by_world.values())} seasons\n")
    print(f"{'world':32} {'n':>3} {'best bank':>11} {'episode':>11}")
    best = {}
    for w, v in sorted(by_world.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        v.sort(key=lambda x: -x["bank"])
        best[w] = v[0]
        print(f"{w:32} {len(v):>3} {v[0]['bank']:>11,.0f} {v[0]['ep']:>11}")

    # slot 0 is the overall best and serves every world he has never played; every world
    # he HAS played keeps its own season.
    overall = max(best.values(), key=lambda x: x["bank"])
    chosen = sorted(by_world)
    OUT.mkdir(parents=True, exist_ok=True)
    tapes = [overall["actions"]] + [best[w]["actions"] for w in chosen]
    assert all(len(t) == 719 for t in tapes), [len(t) for t in tapes]
    (OUT / "actions.json").write_text(json.dumps(tapes, separators=(",", ":")))
    index = {w: i + 1 for i, w in enumerate(chosen)}
    (OUT / "index.json").write_text(json.dumps(index, indent=1, sort_keys=True))
    print(f"\nslot 0 = ep{overall['ep']} bank {overall['bank']:,.0f} (default)")
    print(f"{len(index)} worlds routed, {len(by_world) - len(index)} fall to the default")
    print(f"wrote {OUT}/actions.json and index.json")


if __name__ == "__main__":
    main()
