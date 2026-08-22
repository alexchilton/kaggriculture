"""Reduce every archived game to the actions and the town draw, once, so analysis stops re-parsing.

A recording is ~30 MB and 99.6% of it is observations. Almost every opponent question -- who plants
tomato, whose herd leans which way, where two seasons first disagree -- needs only the 720 actions
per seat, the two team names and the town's shop draw.

Without a cache each script re-parses the whole archive per player. The first-divergence sweep over
eleven players was doing 858 games x 30 MB x 11 = about 280 GB of JSON and had to be killed. With
the cache it is one pass, then milliseconds.

One line per game in a JSONL file:

    {"id": ..., "path": ..., "names": [a, b], "draw": [shop, ...],
     "actions": [[per-turn for seat 0], [per-turn for seat 1]]}

**De-duplicated on EpisodeId**, because 48 of 858 games sit in two directories at once and comparing
a game with its own copy reads as perfect determinism.

    python -u scripts/build_action_cache.py
    python -u scripts/build_action_cache.py --dirs ryo downloads_2026-08-20
"""

import argparse
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

ROOT = REPO / "data/seed_scripts"
OUT = REPO / "data/action_cache.jsonl"

#: Everything recorded on the current economy. `downloads_2026-08-14to16` predates the 2026-08-15
#: balance change and is a different game (`CLAUDE.md`).
DIRS = ("ryo", "downloads_2026-08-20", "downloads_2026-08-19", "leaders_2026-08-19",
        "top_guys", "ladder_2026-08-17b", "field_leaders", "kawashigi", "kawashigi_b3",
        "kawashigi_q4c", "downloads_2026-08-13", "top2", "new_leader", "tetsuya_93866112")


def draw_of(game):
    for frame in reversed(game.get("steps") or []):
        if isinstance(frame, list) and frame and isinstance(frame[0], dict):
            t = (frame[0].get("observation") or {}).get("town") or {}
            if t.get("unlocked_shops"):
                return list(t["unlocked_shops"])
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+", default=list(DIRS))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    seen, n, bad, t0 = set(), 0, 0, time.time()
    with open(args.out, "w") as fh:
        for dn in args.dirs:
            d = ROOT / dn
            if not d.is_dir():
                continue
            for p in sorted(d.glob("*.json")):
                try:
                    g = json.loads(p.read_text())
                except Exception:
                    bad += 1
                    continue
                if not isinstance(g, dict) or not g.get("steps"):
                    bad += 1
                    continue
                info = g.get("info") or {}
                names = info.get("TeamNames") or []
                eid = info.get("EpisodeId")
                if len(names) < 2 or eid is None or eid in seen:
                    bad += 1
                    continue
                seen.add(eid)
                acts = [[], []]
                for frame in g["steps"][1:]:
                    for s in (0, 1):
                        a = (frame[s] or {}).get("action") or {} if len(frame) > s else {}
                        acts[s].append([a.get("farmer") or ["PASS"],
                                        list(a.get("hands") or []),
                                        list(a.get("market") or [])])
                fh.write(json.dumps({"id": eid, "path": str(p.relative_to(REPO)),
                                     "names": names[:2], "draw": draw_of(g),
                                     "actions": acts}, ensure_ascii=False) + "\n")
                n += 1
                if n % 100 == 0:
                    print("  %5d games  %5.0fs" % (n, time.time() - t0), flush=True)
    size = pathlib.Path(args.out).stat().st_size
    print("\n%d games cached, %d skipped (unreadable or duplicate) -> %s  (%.0f MB, %.0fs)"
          % (n, bad, args.out, size / 1e6, time.time() - t0))


if __name__ == "__main__":
    main()
