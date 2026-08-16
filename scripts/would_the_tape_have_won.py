"""On the seed of a game we LOST, replay the winner's tape against ours and against the leader's.

## The question

We lost five ladder games on 2026-08-16 by $2,264 to $19,432, all with the same signature: ahead at
d18, behind by d22. Our agent plays カワシギ's schedule. So the question that separates "the plan is
wrong" from "our executor is worse than the plan" is whether **his own recorded actions** would have
beaten the same opponent on the same board.

Three arms per seed, all against the winner's recorded actions on the other seat:

    ours    our live agent on the shipped schedule   -- reproduces the ladder game
    kawa    カワシギ's recorded actions from his own game
    idle    PASS every turn                          -- the floor, so a "win" can be read

## What a tape can and cannot do on a foreign seed

The board geometry is identical in every game: `_initial_tile(x, y, board_size)` is a pure function
of coordinates, so tiles, distances and the shed sit where the tape expects them. Only two things
are drawn from `random.Random` -- the weed spawn and the shop unlock order -- so a foreign tape
plays a correct board with a different shop draw and different weeds.

That makes the comparison legitimate but ASYMMETRIC in one direction worth stating: the tape is
open-loop and cannot react, so it is handicapped relative to a live agent, and any purchase it makes
can be refused if its bank is short on this seed. A tape that WINS here has therefore won despite a
handicap. A tape that loses has not proven much.

**`weedSpawnChance` is 0.005 on the ladder, not 0.** `scripts/vs_tapes.py` defaults it to 0 and that
is wrong for reproducing a ladder game -- random weeds spawn on EMPTY tiles only
(`_spawn_weeds`, `reference/kaggriculture.py:836`), so a crop tile that weeds is still our own missed
watering, but the empty-ground spawns are real and the tape has to dig them too.

    python -u scripts/would_the_tape_have_won.py --replays 93531871 93525585 93531863 93530978
"""
import argparse
import collections
import importlib
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
DOWNLOADS = pathlib.Path.home() / "Downloads"
KAWA_REPLAY = "data/seed_scripts/kawashigi/92498144.json"
KAWA_TEAM = "カワシギ"


def find_replay(eid):
    for p in (DOWNLOADS / f"{eid}.json",
              REPO / f"data/seed_scripts/ladder_2026-08-16/episode-{eid}-replay.json",
              REPO / f"data/seed_scripts/ladder_1943/episode-{eid}-replay.json"):
        if p.exists():
            return str(p)
    return None


def one(eid, arm, weeds):
    """One season in its own process -- the first run in a process differs from later ones."""
    from kaggle_environments import make

    B = importlib.import_module("scripts.breakdown")
    A = importlib.import_module("kagg.search.schedule_agent")
    PLAN = importlib.import_module("kagg.plan")

    path = find_replay(eid)
    d = json.loads(pathlib.Path(path).read_text())
    names = d["info"]["TeamNames"]
    seed = d["info"].get("seed", 0)
    us = next((i for i, n in enumerate(names) if "alex" in (n or "").lower()), 0)
    winner = names[1 - us]

    # the winner's own recorded actions, on seat 1
    opp = B.tape_policy(path, winner, 0)

    if arm == "ours":
        me = A.make_agent(PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json")), me=0)
    elif arm == "kawa":
        me = B.tape_policy(str(REPO / KAWA_REPLAY), KAWA_TEAM, 0)
    else:
        me = lambda obs, t: {"farmer": ["PASS"], "hands": [], "market": []}

    env = make("kaggriculture",
               configuration={"seed": seed, "weedSpawnChance": weeds}, debug=False)
    env.reset(2)
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        env.step([me(o0, t), opp(o1, t)])
        if env.done:
            break
    fin = env.steps[-1]
    o = env.state[0].observation
    weedn = sum(1 for row in o["farms"][0]["tiles"] for c in row
                if c == "WEED" or (isinstance(c, dict) and c.get("kind") == "WEED"))
    return dict(eid=eid, arm=arm, seed=seed, winner=winner,
                mine=fin[0]["reward"], theirs=fin[1]["reward"], weeds=weedn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replays", nargs="+", required=True)
    ap.add_argument("--arms", nargs="+", default=["ours", "kawa"])
    ap.add_argument("--weeds", type=float, default=0.005,
                    help="the LADDER value; vs_tapes.py defaults to 0 and that is not the ladder")
    ap.add_argument("--child", nargs=2, default=None)
    a = ap.parse_args()

    if a.child:
        print(json.dumps(one(a.child[0], a.child[1], a.weeds)))
        return

    print(f"weedSpawnChance {a.weeds} (the ladder value). The winner's recorded actions hold "
          f"seat 1 in every row.\n")
    print(f"{'episode':>10}{'seed':>13}  {'winner':<22}{'arm':>6}{'ours $':>11}{'theirs $':>11}"
          f"{'margin':>11}{'weeds':>7}")
    out = collections.defaultdict(dict)
    for eid in a.replays:
        for arm in a.arms:
            p = subprocess.run([sys.executable, "-u", __file__, "--child", eid, arm,
                                "--replays", eid, "--weeds", str(a.weeds)],
                               capture_output=True, text=True, cwd=REPO,
                               env={**__import__("os").environ, "PYTHONPATH": "."})
            try:
                r = json.loads(p.stdout.strip().splitlines()[-1])
            except Exception:
                print(f"{eid:>10}  {arm} FAILED {(p.stderr or p.stdout)[-160:]}")
                continue
            out[eid][arm] = r
            print(f"{r['eid']:>10}{r['seed']:>13}  {r['winner'][:21]:<22}{arm:>6}"
                  f"{r['mine']:>11,.0f}{r['theirs']:>11,.0f}"
                  f"{r['mine'] - r['theirs']:>+11,.0f}{r['weeds']:>7}", flush=True)
    print()
    for eid, arms in out.items():
        if "ours" in arms and "kawa" in arms:
            o, k = arms["ours"], arms["kawa"]
            print(f"{eid}: ours {o['mine'] - o['theirs']:+,.0f}   kawa {k['mine'] - k['theirs']:+,.0f}"
                  f"   -> the tape is {k['mine'] - o['mine']:+,.0f} on our seat")
    print("\nThe tape is open-loop and cannot react, so it plays handicapped. A tape WIN where we "
          "lost says our executor is behind the plan it copies; a tape loss says less.")


if __name__ == "__main__":
    main()
