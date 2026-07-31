"""A Gymnasium environment where the policy sets strategy once a day.

## The framing, and why

The natural action space here is brutal: a farmer plus a variable-length list of up to 14 hands,
each choosing one of ~19 ops, plus an ordered 10-slot market queue, every turn for 720 turns. That
is the "genuinely hard modelling problem" the design doc names, and it is exactly the shape that
shattered exploration in Orbit Wars.

So this environment factors the problem. The heuristic agent already routes units competently --
that part is solved and measured. What it cannot do is *decide*: which crops, how much labour,
when to hold produce rather than dump it. Those are the decisions our own experiments show
dominate the score, and there are only thirty of them per game.

One decision per day therefore gives:

- **30 steps per episode, not 720.** Credit assignment over 30 steps is easy, which makes a
  terminal win/loss reward practical rather than hopeless. That matters: the Orbit Wars lesson is
  to keep the reward the true objective, and the true objective here is winning, not money --
  the leaderboard is an Elo rating where margin does not count.
- **A small factored action space.** Six independent heads, no variable-length structure.
- **Fast episodes.** ~24 env turns per RL step, so a full game is 30 policy calls.

The known cost, stated plainly: a policy that only tunes the heuristic's knobs inherits the
heuristic's ceiling. The Orbit Wars post-mortem is emphatic that heuristics-as-policy capped that
project. This is a stepping stone that gets a real learning signal running tonight, not the final
artifact -- the plan for exceeding the ceiling is offline search plus imitation, which needs the
vectorized simulator.
"""

import numpy as np

try:  # gymnasium is the SB3 interface; keep the import soft so the env module stays importable
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:  # pragma: no cover
    gym, spaces = None, None

from kagg.agents import heuristic
from kagg.arena.pool import BASELINE, OPPONENTS

TURNS_PER_DAY = 24
SEASON_DAYS = 30

# Each head picks from a short list. Buckets rather than continuous values because the underlying
# quantities are tile counts and thresholds where fine distinctions are below measurement noise
# (identical parameters vary ~15% across seed sets).
ACTION_BUCKETS = {
    "melon_tiles": (0, 8, 16, 25, 40),
    "strawberry_tiles": (0, 8, 16, 25),
    "cow_tiles": (0, 4, 10),
    "sell_floor_frac": (0.0, 0.4, 0.55, 0.7, 0.9),
    "tiles_per_hand": (4, 7, 10, 14),
    "land_slack": (1.0, 3.0, 6.0),
}
ACTION_KEYS = tuple(ACTION_BUCKETS)

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
BASE_PRICE = heuristic.BASE_PRICE
TRAIN_OPPONENTS = ("mirror", "wheat_only", "melon_heavy", "strawberry", "cow_heavy", "starter")


def _farm_features(farm, tiles_side=10):
    """Tile composition and holdings for one farm, as a fixed-length vector."""
    counts = {"empty": 0, "locked": 0, "weed": 0, "animal": 0}
    crops = {c: 0 for c in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")}
    for row in farm["tiles"]:
        for cell in row:
            if cell == "LOCKED":
                counts["locked"] += 1
            elif cell is None:
                counts["empty"] += 1
            elif isinstance(cell, dict):
                if "animal" in cell:
                    counts["animal"] += 1
                elif cell.get("kind") == "WEED":
                    counts["weed"] += 1
                elif cell.get("kind") == "PLANT":
                    crops[cell["crop"]] = crops.get(cell["crop"], 0) + 1
    total = tiles_side * tiles_side
    out = [counts[k] / total for k in ("empty", "locked", "weed", "animal")]
    out += [crops[c] / total for c in sorted(crops)]
    return out


class StrategyEnv(gym.Env if gym else object):
    """Set strategy each morning; the heuristic executes the day.

    Reward is **terminal only**: +1 for a win, -1 for a loss, 0 for a draw. That is the actual
    competition objective. Money is reported in `info` for diagnostics but never rewarded, so the
    policy cannot learn to bank dollars at the expense of winning.
    """

    metadata = {"render_modes": []}

    def __init__(self, seed_pool=range(10_000), opponents=TRAIN_OPPONENTS, reward="win"):
        self.seed_pool = list(seed_pool)
        self.opponents = list(opponents)
        self.reward_kind = reward
        self._rng = np.random.default_rng()

        self.action_space = spaces.MultiDiscrete([len(ACTION_BUCKETS[k]) for k in ACTION_KEYS])
        # money(2) + day + prices(9) + shed(9) + own farm(9) + opponent farm(9) + hands + quadrants
        self.observation_space = spaces.Box(-5.0, 5.0, shape=(41,), dtype=np.float32)

        self._env = None
        self._params = dict(BASELINE)

    # ---- internals -----------------------------------------------------------------------

    def _observe(self):
        obs = self._env.state[self._me].observation
        farm, other = obs["farms"][self._me], obs["farms"][1 - self._me]
        prices = obs["market"]["prices"]
        shed = obs["private"]["shed"]

        vec = [
            farm["money"] / 50_000.0,
            other["money"] / 50_000.0,
            obs.get("day", 0) / SEASON_DAYS,
        ]
        vec += [prices.get(p, 0) / max(1, BASE_PRICE.get(p, 1)) for p in PRODUCTS]
        vec += [min(shed.get(p, 0), 100) / 100.0 for p in PRODUCTS]
        vec += _farm_features(farm)
        vec += _farm_features(other)
        vec += [
            len(farm.get("hands", [])) / 14.0,
            len(farm.get("unlocked_quadrants", ["NW"])) / 4.0,
        ]
        return np.clip(np.asarray(vec, dtype=np.float32), -5.0, 5.0)

    def _apply(self, action):
        for key, choice in zip(ACTION_KEYS, np.asarray(action).ravel()):
            options = ACTION_BUCKETS[key]
            self._params[key] = options[int(choice) % len(options)]

    def _run_one_day(self):
        """Advance the underlying env by a day, both agents acting each turn."""
        me = heuristic.make_agent(self._params)
        for _ in range(TURNS_PER_DAY):
            if self._env.done:
                break
            actions = []
            for idx, agent in enumerate((me, self._opponent) if self._me == 0 else (self._opponent, me)):
                obs = self._env.state[idx].observation
                actions.append(agent(obs, self._env.configuration) if callable(agent) else None)
            self._env.step(actions)

    # ---- gym API -------------------------------------------------------------------------

    def reset(self, *, seed=None, options=None):
        from kaggle_environments import make

        if seed is not None:
            self._rng = np.random.default_rng(seed)
        episode_seed = int(self._rng.choice(self.seed_pool))
        self._me = int(self._rng.integers(2))  # alternate seats so neither is learned

        name = self.opponents[int(self._rng.integers(len(self.opponents)))]
        spec = OPPONENTS[name]
        self._opponent_name = name
        self._params = dict(BASELINE)
        if isinstance(spec, str) and spec != "__mirror__":
            from kaggle_environments import agent as _kagg_agents  # noqa: F401
            self._opponent = spec
        else:
            base = self._params if spec == "__mirror__" else {**BASELINE, **spec}
            self._opponent = heuristic.make_agent(dict(base))

        self._env = make("kaggriculture", configuration={"seed": episode_seed}, debug=False)
        self._env.reset(num_agents=2)
        return self._observe(), {"opponent": name, "seed": episode_seed}

    def step(self, action):
        self._apply(action)
        self._run_one_day()

        obs = self._env.state[self._me].observation
        day = obs.get("day", 0)
        done = bool(self._env.done) or day >= SEASON_DAYS

        reward = 0.0
        info = {}
        if done:
            mine = obs["farms"][self._me]["money"]
            theirs = obs["farms"][1 - self._me]["money"]
            info = {"money": mine, "opponent_money": theirs, "opponent": self._opponent_name}
            if self.reward_kind == "win":
                reward = float(np.sign(mine - theirs))
            else:  # "money" -- diagnostic only; the ladder does not reward margin
                reward = (mine - theirs) / 50_000.0
            info["win"] = float(mine > theirs)

        return self._observe(), reward, done, False, info
