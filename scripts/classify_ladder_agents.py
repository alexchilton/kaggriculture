"""Read daily ladder replays and say whether a team plays a fixed tape or adapts.

Input is whatever `scripts/fetch_leader_episodes.sh` pulled into a directory: one
kaggle-environments replay JSON per episode, each about 33 MB.

For every seat the replay carries the team name and the 719 actions that seat
actually submitted, so two episodes of the same team can be diffed turn by turn.

    fixed tape   identical actions from turn 0 whatever the opponent and seed
    routing      identical inside one shop draw, different between draws
    adaptive     different inside the same shop draw

The shop draw is the world: the first two shops the town unlocks, in order. A
router cannot vary inside a world, so the within-world comparison is the one that
separates routing from reactivity.

Pass 1 writes a small summary per episode so the 33 MB files are parsed once.

    .venv-sub/bin/python -u scripts/classify_ladder_agents.py data/replays_2026-09-09
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROUTE_STEP = 144


def summarise(path, cache):
    out = cache / (path.stem + ".summary.json")
    if out.exists():
        return json.loads(out.read_text())
    replay = json.loads(path.read_text())
    steps = replay["steps"]
    names = replay["info"]["TeamNames"]
    shops = []
    for step in steps:
        town = step[0]["observation"].get("town") or {}
        unlocked = town.get("unlocked_shops") or []
        for shop in unlocked:
            if shop not in shops:
                shops.append(shop)
        if len(shops) >= 2:
            break
    record = {
        "episode": replay["info"]["EpisodeId"],
        "seed": replay["info"].get("seed"),
        "teams": names,
        "rewards": replay["rewards"],
        "world": shops[:2],
        # steps[t][seat]["action"] is what that seat submitted at turn t-1.
        "actions": [[json.dumps(step[seat].get("action"), sort_keys=True) for step in steps[1:]]
                    for seat in (0, 1)],
    }
    out.write_text(json.dumps(record))
    return record


def first_divergence(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return None


def channel_diffs(a, b):
    plan = market = 0
    for x, y in zip(a, b):
        if x == y:
            continue
        px, py = json.loads(x), json.loads(y)
        if px.get("farmer") != py.get("farmer") or px.get("hands") != py.get("hands"):
            plan += 1
        elif px.get("market") != py.get("market"):
            market += 1
    return plan, market


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--min-episodes", type=int, default=2)
    args = ap.parse_args()

    folder = Path(args.folder)
    cache = folder / "summaries"
    cache.mkdir(exist_ok=True)

    streams = defaultdict(list)
    for path in sorted(folder.glob("*.json")):
        if path.name.endswith(".summary.json"):
            continue
        rec = summarise(path, cache)
        for seat, team in enumerate(rec["teams"]):
            streams[team].append({"episode": rec["episode"], "seed": rec["seed"],
                                  "world": tuple(rec["world"]), "seat": seat,
                                  "reward": rec["rewards"][seat],
                                  "actions": rec["actions"][seat]})
        print(f"read {path.name}  {rec['teams'][0]} vs {rec['teams'][1]}  "
              f"world={'|'.join(rec['world'])}  rewards={rec['rewards']}", flush=True)

    print()
    print(f"{len(streams)} distinct teams across {sum(len(v) for v in streams.values()) // 2} episodes")
    print()
    for team, games in sorted(streams.items(), key=lambda kv: -len(kv[1])):
        if len(games) < args.min_episodes:
            continue
        print(f"=== {team}  {len(games)} episodes")
        for i in range(len(games)):
            for j in range(i + 1, len(games)):
                g, h = games[i], games[j]
                div = first_divergence(g["actions"], h["actions"])
                ndiff = sum(1 for x, y in zip(g["actions"], h["actions"]) if x != y)
                plan, market = channel_diffs(g["actions"], h["actions"])
                same_world = g["world"] == h["world"]
                if div is None:
                    verdict = "IDENTICAL TAPE"
                elif div >= ROUTE_STEP and not same_world:
                    verdict = "routing (diverges at/after the shop pick, different worlds)"
                elif same_world:
                    verdict = "ADAPTIVE IN ONE WORLD"
                else:
                    verdict = "adaptive before the shop pick"
                print(f"  ep {g['episode']} vs {h['episode']}  "
                      f"world {'SAME' if same_world else 'diff'} "
                      f"({'|'.join(g['world'])} / {'|'.join(h['world'])})  "
                      f"first_div={div}  diff={ndiff}/719 (plan {plan}, market-only {market})  -> {verdict}")
        print()


if __name__ == "__main__":
    main()
