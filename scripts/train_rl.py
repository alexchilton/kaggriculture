"""Train a strategy policy with PPO. Built to be left running overnight.

Reward is **terminal win/loss only** (+1/-1/0). That is the competition's actual objective -- the
leaderboard is an Elo-style rating, so margin does not count -- and it is affordable here because
`StrategyEnv` makes one decision per day, giving 30-step episodes rather than 720. The Orbit Wars
lesson holds: keep the reward the true objective. Money is logged but never rewarded.

Watch these, per `CLAUDE.md`:

- `train/explained_variance` must pass **0.5** early. If it does not, the frame is wrong, not the
  hyperparameters. That is a committed kill criterion.
- `rollout/ep_rew_mean` is win rate mapped to [-1, 1]. 0.0 means breaking even against the pool.
- **`ret=0.00 +/- 0.00` is a stop-everything signal**: it means reward is not reaching the
  algorithm at all.

Run:
    .venv/bin/python scripts/train_rl.py --steps 3000000 --envs 10
"""

import argparse
import pathlib
import time

RUN_DIR = pathlib.Path("data/rl_runs")


def build_env(n_envs, seed_pool):
    from stable_baselines3.common.monitor import Monitor
    from stable_baselines3.common.vec_env import SubprocVecEnv

    from kagg.rl.env import StrategyEnv

    def factory(rank):
        def _make():
            return Monitor(StrategyEnv(seed_pool=seed_pool))
        return _make

    return SubprocVecEnv([factory(i) for i in range(n_envs)], start_method="spawn")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=3_000_000)
    ap.add_argument("--envs", type=int, default=10)
    ap.add_argument("--n-steps", type=int, default=64, help="rollout length per env (episodes are 30)")
    ap.add_argument("--ent-coef", type=float, default=0.005,
                    help="0.02 was too high for the large MultiDiscrete in Orbit Wars; this space "
                         "is small, so start low and raise only if entropy collapses")
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--tag", default="ppo")
    args = ap.parse_args()

    from stable_baselines3 import PPO
    from stable_baselines3.common.callbacks import CheckpointCallback

    run = RUN_DIR / f"{args.tag}-{int(time.time())}"
    run.mkdir(parents=True, exist_ok=True)
    print(f"run dir: {run}")

    env = build_env(args.envs, seed_pool=range(50_000))

    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=args.lr,
        n_steps=args.n_steps,
        batch_size=args.envs * args.n_steps // 2,
        n_epochs=4,
        # Terminal reward over a 30-step episode: no discounting, so the policy is optimising the
        # actual objective rather than a nearer-term proxy. 0.999 over 720 steps would have been a
        # 0.48 implicit discount, which is why the per-turn framing was rejected.
        gamma=1.0,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=args.ent_coef,
        vf_coef=0.5,
        policy_kwargs={"net_arch": [128, 128]},
        tensorboard_log=str(run),
        verbose=1,
    )

    # A plain CSV alongside tensorboard, so an overnight run can be checked with `tail`.
    from stable_baselines3.common.logger import configure
    model.set_logger(configure(str(run), ["stdout", "csv", "tensorboard"]))

    model.learn(
        total_timesteps=args.steps,
        callback=CheckpointCallback(save_freq=50_000, save_path=str(run), name_prefix="ckpt"),
        progress_bar=False,
    )
    model.save(str(run / "final"))
    print(f"saved {run / 'final'}")


if __name__ == "__main__":
    main()
