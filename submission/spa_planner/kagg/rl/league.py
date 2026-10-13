"""The self-play opponent pool and its priority sampling.

**Why this is a module and not three lists in the training script.** It was `pool`, `pool_wr` and
`pool_games`, kept in step by hand at four separate call sites, and eviction updated exactly one of
them:

    pool.pop(len(pool) // 2)        # pool_wr and pool_games keep the evicted member's entry

The run died 250 updates in with `ValueError: a and p must have same size` -- `np.random.choice` was
handed `len(pool)` options and `len(pool_wr)` probabilities. The crash is the lucky half. The silent
half is that after an eviction every `pool_wr[opp_idx]` refers to a **different checkpoint than the
one that played**, so the priority EMA -- the whole curriculum -- is attributed to the wrong member
from that point on, and nothing about that reads as wrong in a log.

Three lists indexed in parallel is the bug. One list of records cannot desynchronise, so eviction
becomes a single `pop` that is correct by construction.

Priority sampling is ported from Ender's `_select_league_opponent`: pick opponents by how well they
do against us rather than round-robin, because `pool[it % len(pool)]` plays the random initialisation
exactly as often as the best checkpoint in the pool -- a lottery rather than a curriculum.
"""

from dataclasses import dataclass, field
from typing import Any

import numpy as np

# Ender's weights: `floor + winrate ** temperature`, plus a bonus while a member is unplayed.
POOL_PRIORITY_FLOOR = 0.1
POOL_PRIORITY_TEMP = 1.0
POOL_PRIORITY_ALPHA = 0.2
POOL_UNPLAYED_BONUS = 0.25


def hold_updates(horizon, episode_turns):
    """Updates one pool member must hold the seat to cover a whole episode.

    `ceil(episode_turns / horizon)`, floored at 1. A game that starts mid-window still straddles at
    most one boundary, so it faces at most two opponents rather than the ~23 it faced before -- and
    the common case is one. Making it exact would mean per-slot opponent parameters, which is a
    different and far more expensive design: the rollout applies **one** parameter set to the whole
    batch, so per-slot members would need either a forward pass per member or a batch-sized copy of
    the parameters. Two-at-worst for free is the right trade; the residual is stated rather than
    hidden.
    """
    return max(1, -(-int(episode_turns) // max(1, int(horizon))))


@dataclass
class Member:
    """One frozen checkpoint, and an EMA of the win rate it achieves *against the live policy*.

    `wr` is the **opponent's** rate, so a checkpoint that beats us has a high value and gets picked
    more often. It starts at 0.5 because an unplayed member has no evidence either way.
    """

    params: Any
    wr: float = 0.5
    games: int = 0


@dataclass
class Pool:
    """Frozen past selves, sampled by difficulty."""

    max_size: int = 5
    members: list = field(default_factory=list)

    def __len__(self):
        return len(self.members)

    def add(self, params):
        """Append a snapshot, evicting from the middle if the pool is full."""
        self.members.append(Member(params=params))
        # **Drop from the middle, never the ends.** Evicting the oldest would leave a pool of
        # near-identical recent snapshots, which is how self-play starts cycling: the policy forgets
        # strategies it used to beat, rediscovers a counter to its recent self, loses to something
        # from ten thousand updates ago, and every local win rate looks healthy throughout. The first
        # entry is an anchor that cannot drift; the last is the frontier.
        while len(self.members) > max(1, self.max_size):
            self.members.pop(len(self.members) // 2)

    def weights(self):
        """Sampling weight per member, in member order."""
        return np.array(
            [POOL_PRIORITY_FLOOR + max(m.wr, 1e-6) ** POOL_PRIORITY_TEMP
             + (POOL_UNPLAYED_BONUS if m.games <= 0 else 0.0)
             for m in self.members], dtype=np.float64)

    def select(self, seed, update, hold=1):
        """Index of the opponent for this update. Seeded by `(seed, window)`, so a resumed run at
        the same update draws the same opponent.

        **`hold` is the number of consecutive updates one member keeps the seat, and it is the fix
        for a bug that made `wr_pool` meaningless.** This was drawn per *update*, inside the update
        loop, while an episode is `EPISODE_TURNS` long and one update advances `--horizon` turns of
        it. At horizon 32 that is ~23 updates per game, so seat 1 was played by ~23 different frozen
        checkpoints over a single season, swapping every 32 turns.

        An opponent stitched from 23 checkpoints has no plan -- it restarts its strategy 23 times a
        season -- and plays far worse than any single member. That is how `wr_pool` reached 0.990
        against snapshots that are near-peers on a fair board, and why every member's recorded rate
        sat at 0.01-0.15: none of them had ever played a whole game, and `record` credited whichever
        one held the seat on the final update.

        `CLAUDE.md` already names this failure for the per-opponent win rate -- "the opponent was
        re-drawn every update while a game spans ~22.5 of them". Sticky *roles* fixed it for the
        opponent TYPE and left the member identity redrawn, so the same bug survived in the same
        file. `hold=1` reproduces the old behaviour exactly and exists only so that is expressible.
        """
        w = self.weights()
        window = update // max(1, int(hold))
        return int(np.random.default_rng((seed, window)).choice(len(self.members), p=w / w.sum()))

    def params(self, index):
        return self.members[index].params

    def record(self, index, opp_wr, n_done):
        """Fold this update's result into one member's EMA.

        **Only when games actually finished against it.** Terminal rows are ~0.14% of all rows, so an
        update can legitimately resolve none, and folding a zero-sample estimate in would drag every
        member toward 0.5 and flatten the curriculum back into the round-robin this replaces.
        """
        if n_done <= 0:
            return
        m = self.members[index]
        a = POOL_PRIORITY_ALPHA
        m.wr = (1 - a) * m.wr + a * opp_wr
        m.games += int(n_done)

    def summary(self):
        """`wr/games` per member, for the log."""
        return "  ".join(f"{m.wr:.2f}/{m.games}" for m in self.members)
