"""DAgger: label the states the policy actually reaches, not the ones the teachers reached.

**Why this and not more epochs.** The cloned policy reproduces its teachers closely on any state a
teacher trajectory contains -- at day 0 hour 2 and day 4 hour 4 alike, including the teacher's own
idle turns. It is not weak and it is not under-trained. What it cannot do is *self-start*: at the
daily spawn every unit stands on the shed tile, and it plays noop with probability 0.9999 under
honest sampling at temperature 1. Nothing gets planted, so no new jobs appear, so every subsequent
morning reproduces the same decision. The agent banks exactly its $3,000 start.

That state is absent from the training data for a simple reason: **competent teachers disperse
immediately**, so "everyone still on the shed tile several turns in" essentially never occurs in
126 replays. It is also the state the policy's own rollouts begin in, every episode. Supervised
learning on the teachers' distribution cannot fix a hole in the *policy's* distribution -- which is
precisely what DAgger is for.

So: roll the current checkpoint out in the real environment, and at every turn ask a competent agent
what it would have done there. Those corrective pairs are exactly the supervision that is missing.

**The labeller is the ES-tuned `converter`, the agent submitted as v8** -- not `contrarian`, which
was v7 and is measurably weaker: converter beats it 87.5% over sixteen seat-swapped fresh seeds at
+$15,010 a game, and scores 0.963 against 0.825 on the ladder. Labelling with the weaker of two
available agents caps the corrective data at the worse teacher for nothing. `CLAUDE.md` blesses the
heuristics as teachers and sparring partners while forbidding them as the final policy, which is
this use exactly.

The labeller is still a worse *ceiling* than the replay teachers, who bank $128k. That is why the
corrective set is deliberately small beside the 90,720 replay pairs: it exists to cover states the
replays cannot contain, not to become the bulk of the signal.

Run:  .venv/bin/python -u scripts/dagger.py 40 2>&1 | tee data/logs/dagger.log
"""

import sys
import time
from pathlib import Path

import numpy as np
from kaggle_environments import make

from kagg.agents import converter, neural
from kagg.il.replays import encode_action
from kagg.rl import adapter, jax_obs

OUT = Path("data/il")


def collect(n_games=40, start_seed=7000, mix_expert=0.0, checkpoint=None):
    """Play the checkpoint, record what the expert would have done at each state it reached.

    `mix_expert` occasionally hands a turn to the expert, so the rollout is not confined entirely to
    the failure state -- the standard DAgger beta. At 0 it is pure on-policy, which is what we want
    first, because the stuck states are the whole point.
    """
    learner = neural.make_agent(checkpoint) if checkpoint else neural.make_agent()
    expert = converter.agent
    tiles_b, units_b, glob_b, labels_b = [], [], [], {}
    rng = np.random.default_rng(0)
    started = time.time()

    for g in range(n_games):
        seed = start_seed + g
        kept_before = len(tiles_b)

        def agent(obs, config=None):
            me = obs["player"]
            expert_action = expert(obs, config)

            # Record the corrective label for the state the *learner* put us in.
            privates = [obs["private"] if p == me else adapter.agent_private_stub()
                        for p in range(2)]
            try:
                state = adapter.state_from_obs(obs, privates)
                t, u, gl = jax_obs.encode(state)
            except Exception:                                    # noqa: BLE001
                return expert_action
            tiles_b.append(np.asarray(t[0, me], dtype=np.float16))
            units_b.append(np.asarray(u[0, me], dtype=np.float16))
            glob_b.append(np.asarray(gl[0, me], dtype=np.float16))
            n_units = 1 + len(obs["farms"][me].get("hands", []))
            for k, v in encode_action(expert_action, n_units=n_units).items():
                labels_b.setdefault(k, []).append(v)

            # The learner drives, so the states we visit are the learner's own.
            if mix_expert and rng.random() < mix_expert:
                return expert_action
            return learner(obs, config)

        env = make("kaggriculture", configuration={"seed": seed}, debug=False)
        env.run([agent, "starter"])
        rate = len(tiles_b) / max(1e-9, time.time() - started)
        print(f"  game {g + 1}/{n_games} seed {seed}: "
              f"learner ${env.steps[-1][0]['reward']:,.0f}, "
              f"{len(tiles_b) - kept_before} corrective pairs "
              f"({len(tiles_b):,} total, {rate:.0f}/s)", flush=True)

    return tiles_b, units_b, glob_b, labels_b


def main():
    n_games = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    mix = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    ckpt = sys.argv[3] if len(sys.argv) > 3 else None
    round_id = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    print(f"round {round_id}: {n_games} games, mix_expert={mix}, checkpoint={ckpt or 'default'}")
    tiles_b, units_b, glob_b, labels_b = collect(n_games, mix_expert=mix, checkpoint=ckpt)
    if not tiles_b:
        raise SystemExit("no data collected")

    OUT.mkdir(parents=True, exist_ok=True)
    # A distinct prefix so a rebuild of the replay shards does not silently drop these, and so the
    # mixture of teacher data to corrective data stays visible on disk.
    path = OUT / f"dagger_{round_id:03d}.npz"
    np.savez_compressed(
        path,
        tiles=np.asarray(tiles_b, dtype=np.float16),
        units=np.asarray(units_b, dtype=np.float16),
        glob=np.asarray(glob_b, dtype=np.float16),
        **{f"y_{k}": np.asarray(v, dtype=np.int16) for k, v in labels_b.items()},
    )
    print(f"\nwrote {path}: {len(tiles_b):,} corrective pairs from {n_games} games")
    print("Retrain with these alongside the replay shards, then re-run the T=1 sampling sweep:")
    print("  P(noop) at spawn must fall well below 0.9999 before the checkpoint is a usable prior.")


if __name__ == "__main__":
    main()
