"""One small summary per replay: teams, seed, world, banks, and each seat's action stream.

A replay is ~32 MB and the questions asked of it here are small -- who played, in which world, what
did they do on turn 0, did two seasons of the same team diverge. `scripts/classify_top30.py` and
the other classifiers all read `<dir>/summaries/<episode>.summary.json`, and nothing in the repo
wrote them, so they were being made by hand and the format lived only in the files themselves.

    python -u scripts/summarise_replays.py data/replays_2026-09-11

Skips a summary that already exists, so it is resumable and safe to re-run while a fetch is still
filling the directory.
"""
import json, pathlib, sys


def world_of(rep, seat):
    """This seat's FIRST unlocked shop -- what makes two seasons comparable.

    Not readable at step 0: the town opens its first shop `townShopUnlockInterval` days in, so
    `unlocked_shops` is `[]` on the opening observation and taking `[0]` there returns None for
    every episode. Scanned forward to the first step that names one.
    """
    for step in (rep.get("steps") or []):
        if seat >= len(step):
            continue
        obs = (step[seat] or {}).get("observation") or {}
        shops = (obs.get("town") or {}).get("unlocked_shops") or []
        if shops:
            return shops[0]
    return None


def summarise(path):
    rep = json.loads(path.read_text())
    info = rep.get("info") or {}
    teams = info.get("TeamNames") or []
    steps = rep.get("steps") or []
    actions = []
    for seat in range(len(teams)):
        actions.append([json.dumps((s[seat] or {}).get("action"))
                        for s in steps[1:] if seat < len(s)])
    return {"episode": int(path.stem),
            "seed": info.get("seed", info.get("Seed")),
            "teams": teams,
            "rewards": rep.get("rewards") or [],
            "world": [world_of(rep, i) for i in range(len(teams))],
            "actions": actions}


def main():
    d = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "data/replays_2026-09-11")
    out = d / "summaries"
    out.mkdir(parents=True, exist_ok=True)
    made = skipped = bad = 0
    for p in sorted(d.glob("*.json")):
        q = out / f"{p.stem}.summary.json"
        if q.exists():
            skipped += 1
            continue
        try:
            q.write_text(json.dumps(summarise(p)))
            made += 1
        except Exception as e:
            bad += 1
            print(f"  {p.name}: {type(e).__name__} {e}", flush=True)
    print(f"{d}: {made} written, {skipped} already there, {bad} unreadable")


if __name__ == "__main__":
    main()
