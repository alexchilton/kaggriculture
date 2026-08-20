"""Generate (observation, action) pairs by playing the ead81e2 teacher against itself.

Round 0 of the DAgger plan: plain behaviour cloning data, teacher states labelled by the teacher.
Later rounds roll the STUDENT and call `label_state` on the states it actually reached -- that is
the on-policy correction the recorded tape can never give us, and the reason the planner is worth
using as a teacher at all.

The teacher is a self-contained Kaggle submission exposing `agent(observation, configuration)`, so
we drive the environment ourselves rather than using `env.run`. That is what makes the pairs exact:
we capture the observation the agent was handed and the action it returned, with nothing in between.

    python -u label_games.py --games 20 --worker 0 --out /home/alex/labels

One shard per worker, JSONL, one line per player-turn.
"""

import argparse
import json
import pathlib
import random
import time

AGENT = "/home/alex/kagg-teacher/submission/main.py"


def load_agent(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("teacher_%d" % random.randrange(1 << 30), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def obs_snapshot(ob, seat):
    """Exactly what `adapter.state_from_obs` consumes. Nothing hand-picked.

    **The first version of this function hand-picked fields and dropped three the encoder needs.**
    `private["inventories"]` -- what each unit is CARRYING -- would have encoded as all zeros, and
    "am I holding wheat" is the entire precondition for FEED, PLACE and DROP. `market` carries the
    prices every sell decision turns on. And `farms` was stored for the acting seat only, while
    `state_from_obs` reads both. None of that fails loudly; it trains a net on zeroed carry state.

    So this stores what the bridge reads, verbatim, rather than a summary of it. Storage is cheap;
    a silently mis-encoded 900k-row dataset is not.

    The opponent's private is NOT stored, deliberately. A submission never sees it, and
    `adapter.agent_private_stub()` is what play substitutes -- so training on the real thing would
    fit features that vanish at deployment.
    """
    return {
        "step": int(ob.get("step", 0) or 0),
        "day": int(ob.get("day", 0) or 0),
        "hour": int(ob.get("hour", 0) or 0),
        "seat": seat,
        # Both seats: `state_from_obs` builds tiles for farms[0] and farms[1].
        "farms": ob.get("farms"),
        # `market["inventory"]` is read per product for the price features.
        "market": ob.get("market"),
        # Own private only -- seeds, shed, and the inventories the first version dropped.
        "private": ob.get("private"),
        "shops": sorted(str(v) for v in ((ob.get("town") or {}).get("unlocked_shops") or [])),
    }


def play(seed, out_fh, agent_a, agent_b):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    agents = [agent_a, agent_b]
    turns = 0
    while not env.done:
        actions = []
        snaps = []
        for seat in (0, 1):
            ob = env.state[seat].observation
            cfg = env.configuration
            snaps.append(obs_snapshot(ob, seat))
            actions.append(agents[seat](ob, cfg))
        for seat in (0, 1):
            out_fh.write(json.dumps({"seed": seed, "seat": seat,
                                     "obs": snaps[seat], "act": actions[seat]}) + "\n")
        env.step(actions)
        turns += 1
    banks = [(s.get("reward") or 0.0) for s in env.steps[-1]]
    return turns, banks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=10)
    ap.add_argument("--worker", type=int, default=0)
    ap.add_argument("--out", default="/home/alex/labels")
    ap.add_argument("--agent", default=AGENT)
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    shard = out / ("shard_%03d.jsonl" % args.worker)

    a = load_agent(args.agent)
    b = load_agent(args.agent)

    t0 = time.time()
    with shard.open("w") as fh:
        for g in range(args.games):
            seed = args.worker * 100000 + g
            t1 = time.time()
            turns, banks = play(seed, fh, a, b)
            print("w%02d game %3d seed %-8d turns %3d banks %s  %.1fs"
                  % (args.worker, g, seed, turns,
                     ["%.0f" % x for x in banks], time.time() - t1), flush=True)
    print("w%02d DONE %d games in %.1fs -> %s"
          % (args.worker, args.games, time.time() - t0, shard), flush=True)


if __name__ == "__main__":
    main()
