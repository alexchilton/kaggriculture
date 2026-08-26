"""Play a built submission against the lineage that is actually beating us.

**The opponent pool cannot decide anything about this agent any more.** Measured 2026-08-26,
`data/logs/gate_both.log`: the shipped build wins **100% of 160 games against nine of the ten pool
opponents**, and the tenth is `mirror`, which sits at 50% by construction. Win rate has no room to
move, so the only column that can differ between two arms is money -- and money is the wrong
selection criterion on an Elo ladder, which is this project's oldest recorded lesson.

Meanwhile the real field banks $130-150k. `docs/the_clones_beat_kawa_and_us_2026-08-26.md`: one
published script under ~30 names, five openings covering 58% of 240 seats, and カワシギ -- the tape we
imitate -- down in 12th.

So this gates against THEM. `tape_policy` replays a recorded seat verbatim, which is exactly what
these agents are: fixed 720-turn scripts whose only board-dependence is the yarn draw. Three
opponents, one per branch:

    clone_yarn3   98889302  WeAreFarmers    $127,080   yarn unlocks d3
    clone_yarn6   98857364  Bharath Varma   $134,682   yarn unlocks d6
    clone_late    98898511  G!vIOne         $147,576   yarn late or never

**Two things this cannot tell you, and they matter.**

1. A replayed tape is NOT the agent that recorded it. It cannot respond to us, so it will sell into
   a book we are also selling into and bank less than it did in its own game -- the same effect
   already documented for the カワシギ column in `scripts/breakdown.py` ("Seb's REAL bank at d4 h22
   $718 ... replayed against us $683"). Read the WIN, not their money.
2. Each tape is one recorded season. Playing it on other seeds changes the board it was recorded
   on, so its own play degrades. `--own-seed` plays each tape only on the seed it was recorded on,
   which is the honest single-game comparison; the multi-seed sweep is a robustness check on us,
   not a fair fight for them.

    PYTHONPATH=. python -u scripts/gate_against_the_clones.py --agent submission/main_base.py
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

#: name -> (replay, team, the seed it was recorded on)
CLONES = {
    "clone_yarn3": ("data/seed_scripts/clone_yarn3/98889302.json", "WeAreFarmers", 1290360884),
    "clone_yarn6": ("data/seed_scripts/clone_yarn6/98857364.json", "Bharath Varma", 205177061),
    "clone_late": ("data/seed_scripts/clone_late/98898511.json", "G!vIOne", 1598723111),
}


def load_agent(path):
    """The built bundle's entry point, as a fresh callable.

    **A fresh one per game.** The bundle keeps per-day state on the closure `make_agent` builds, so
    reusing one across two seatings would carry day 29 of the last game into day 0 of the next. The
    builder guarantees the last callable in the file is `agent()`.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        f"_gate_sub_{abs(hash(path))}_{load_agent.n}", path)
    load_agent.n += 1
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, "agent")
    # The bundle's `agent` may be `(obs)` or `(obs, config)`; call it with what it accepts.
    import inspect
    takes = len(inspect.signature(fn).parameters)
    return fn if takes == 1 else (lambda obs: fn(obs, None))


load_agent.n = 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="submission/main.py")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--first-seed", type=int, default=700)
    ap.add_argument("--own-seed", action="store_true",
                    help="play each tape only on the seed it was recorded on")
    args = ap.parse_args()

    from kaggle_environments import make
    import scripts.breakdown as B

    rows = []
    for name, (path, team, own) in CLONES.items():
        # **A PATH, not a loaded dict.** `env_config`, `recorded_shops` and `tape_policy` all read
        # the file themselves (`breakdown.py:254`), so handing them parsed JSON dies on
        # `pathlib.Path(dict)`.
        replay = str(REPO / path)
        economy = B.env_config(replay)
        shops = B.recorded_shops(replay)
        seeds = [own] if args.own_seed else [args.first_seed + i for i in range(args.seeds)]
        for seed in seeds:
            # BOTH seatings. Seat 0 is the only one kaggle-environments gives a `step` to, and a
            # harness that only ever seats us second replays turn 0 all season
            # (`project_kaggriculture_seat1_has_no_step`); playing both is also what the pool gate
            # does, so the two numbers are comparable.
            for our_seat in (0, 1):
                env = make("kaggriculture",
                           configuration=dict(economy, seed=seed), debug=False)
                env.reset(2)
                # `tape_policy(replay, team, 0)` returns THAT player's own actions, indexed by turn.
                tape = B.tape_policy(replay, team, 0)
                ours = load_agent(args.agent)
                for t in range(719):
                    # The shop draw is half the economy and must come from the recording, exactly as
                    # `breakdown.run` does it -- a tape replayed against a different town is fiction.
                    env.state[0].observation.town["unlocked_shops"] = list(shops(t))
                    acts = [None, None]
                    acts[our_seat] = ours(env.state[our_seat].observation)
                    acts[1 - our_seat] = tape(env.state[1 - our_seat].observation, t)
                    env.step(acts)
                farms = env.state[0].observation["farms"]
                ours = float(farms[our_seat]["money"])
                theirs = float(farms[1 - our_seat]["money"])
                rows.append((name, seed, our_seat, ours, theirs))
                print(f"   {name:<12} seed {seed:<11} seat {our_seat}  "
                      f"ours ${ours:>9,.0f}  theirs ${theirs:>9,.0f}  "
                      f"{'WIN' if ours > theirs else 'LOSS' if ours < theirs else 'DRAW'}",
                      flush=True)

    print()
    by = collections.defaultdict(list)
    for name, _s, _seat, ours, theirs in rows:
        by[name].append(ours > theirs)
    for name, wins in by.items():
        print(f"   {name:<12}{100*sum(wins)/len(wins):>6.0f}%  ({sum(wins)}/{len(wins)})")
    allw = [w for v in by.values() for w in v]
    print(f"   {'OVERALL':<12}{100*sum(allw)/max(1,len(allw)):>6.0f}%  "
          f"({sum(allw)}/{len(allw)})")


if __name__ == "__main__":
    main()
