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

    def select(self, seed, update):
        """Index of the opponent for this update. Seeded by `(seed, update)`, so a resumed run at
        the same update draws the same opponent."""
        w = self.weights()
        return int(np.random.default_rng((seed, update)).choice(len(self.members), p=w / w.sum()))

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
