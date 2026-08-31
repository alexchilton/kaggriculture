"""Does the opponent block tell the network which tape it is in, before it learns anything?

    python -u scripts/is_the_opponent_block_a_game_id.py

ALEX'S POINT
------------
*"but the only thing of the opponent which is important is that 1 value"* -- the opponent's MELON
tile count at day 3, which is the sole input to `melon_branch.trigger` (`melon_branch.py:215`).
`jax_obs` gives the net **14**: `_OPPONENT_WIDTH = N_KINDS + N_CROPS + N_ANIMAL_KINDS`, the trailing
block of the 122-wide global token.

THE MECHANISM THIS TESTS
------------------------
Each of the four tapes was played against a DIFFERENT opponent. If those 13 unused features are
distinctive enough, the opponent block is a **game fingerprint**: the network can read which tape it
is in and index the recorded action, instead of learning any board-to-action rule at all. That would
explain, with no appeal to capacity, why the clone reproduces its four teachers to within $63 and
banks $300 on seed 9000 -- a fresh seed means a fresh opponent, the fingerprint misses, and there is
nothing underneath it.

It is a claim about separability, so it is measured by separability: a 1-nearest-neighbour classifier
on the 14 numbers alone, asked which of the four tapes a turn came from.

**Held out by TIME, not by tape.** The first version of this held out by tape, which is unanswerable
by construction -- the held-out tape's label is not in the training set, so the correct answer is
unreachable and every arm scored exactly 0.0%. Splitting on the day keeps all four labels present
and still stops a turn being answered by its own neighbour one hour later.

Read it as:
    near 100%   the block is a game ID. Cutting it to the one value the teacher uses removes the
                shortcut, and is a change to what the net SEES rather than to its size.
    near 25%    chance. The block carries no game identity and the memorisation is elsewhere.
"""
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

TAPES = {
    "92498144": "data/seed_scripts/kawashigi/92498144.json",
    "92466371": "data/seed_scripts/kawashigi/92466371.json",
    "91906088": "data/seed_scripts/downloads_2026-08-13/91906088.json",
    "91907974": "data/seed_scripts/downloads_2026-08-13/91907974.json",
}
TURNS = 719


def seat_of(doc, team="カワシギ"):
    names = [str(t or "") for t in ((doc.get("info") or {}).get("TeamNames") or [])]
    return next(i for i, n in enumerate(names) if team.lower() in n.lower())


def blocks(path):
    """The trailing `_OPPONENT_WIDTH` features of `glob`, for our seat, every turn."""
    from kagg.rl import adapter as AD, jax_obs

    doc = json.loads(pathlib.Path(path).read_text())
    seat = seat_of(doc)
    width = jax_obs._OPPONENT_WIDTH
    out = []
    for i, step in enumerate(doc["steps"][:TURNS]):
        obs = (step[seat] or {}).get("observation") or {}
        if not obs.get("farms"):
            continue
        raw = [(step[p] or {}).get("observation", {}).get("private") for p in range(2)]
        privates = [raw[p] if (p == seat and raw[p]) else AD.agent_private_stub()
                    for p in range(2)]
        state = AD.state_from_obs(obs, privates, step=i)
        _t, _u, glob = jax_obs.encode(state)
        out.append(np.asarray(glob)[0, seat, -width:])
    return np.asarray(out, dtype=np.float32)


def _knn_hits(tr_X, tr_y, te_X, label):
    """1-NN hits, chunked so the [n_test, n_train] distance matrix stays small."""
    hit = 0
    for s in range(0, len(te_X), 256):
        d = ((te_X[s:s + 256, None, :] - tr_X[None, :, :]) ** 2).sum(-1)
        hit += int((tr_y[d.argmin(1)] == label).sum())
    return hit


def main():
    from kagg.rl import jax_obs

    print(f"_OPPONENT_WIDTH = {jax_obs._OPPONENT_WIDTH} features, the trailing block of `glob`\n")

    X, y, names = [], [], list(TAPES)
    for k, path in TAPES.items():
        b = blocks(path)
        print(f"  {k}  {len(b)} turns", flush=True)
        X.append(b)
        y.append(np.full(len(b), names.index(k)))
    day = np.concatenate([np.arange(len(b)) // 24 for b in X])
    X, y = np.concatenate(X), np.concatenate(y)

    # The most direct measure, and it needs no classifier at all: at a given turn, are the four
    # tapes' opponent blocks even different from each other? If they are identical the net has
    # nothing to key on; if they are all distinct it can tell the games apart at that instant.
    per_turn = np.stack([X[y == i] for i in range(len(names))])          # [4, T, 14]
    distinct = np.array([len({tuple(np.round(per_turn[i, t], 4)) for i in range(len(names))})
                         for t in range(per_turn.shape[1])])
    print("\ndistinct opponent blocks across the four tapes, at the same turn index:")
    for k in range(1, len(names) + 1):
        n = int((distinct == k).sum())
        print(f"  {k} distinct   {n:>5,} turns  {n / len(distinct):>6.1%}")
    first_split = int(np.argmax(distinct > 1)) if (distinct > 1).any() else -1
    print(f"  first turn the blocks differ at all: {first_split} "
          f"(day {first_split // 24}, hour {first_split % 24})")

    train = day < 15
    print(f"\n1-NN on the {X.shape[1]} opponent features -- train days 0-14, test days 15-29")
    print(f"  {'tape':>16}{'turns':>9}{'named correctly':>18}")
    tot_hit = tot_n = 0
    for i, k in enumerate(names):
        te = (~train) & (y == i)
        hit = _knn_hits(X[train], y[train], X[te], i)
        tot_hit += hit
        tot_n += int(te.sum())
        print(f"  {k:>16}{int(te.sum()):>9,}{hit / max(1, int(te.sum())):>17.1%}")
    print(f"  {'ALL':>16}{tot_n:>9,}{tot_hit / max(1, tot_n):>17.1%}   (chance = 25.0%)")

    # How EARLY is the tell. Train on the first half of each window, test on the second, so a
    # fingerprint present from the opening is distinguishable from one that only appears once the
    # seasons have diverged.
    print("\nseparability by day window (train first half of the window, test second):")
    print(f"  {'days':>10}{'turns':>9}{'named correctly':>18}")
    for lo, hi in ((0, 3), (3, 6), (6, 12), (12, 30)):
        mid = (lo + hi) / 2
        tr = (day >= lo) & (day < mid)
        hit = n_sel = 0
        for i, _k in enumerate(names):
            te = (day >= mid) & (day < hi) & (y == i)
            if not te.any() or not tr.any():
                continue
            hit += _knn_hits(X[tr], y[tr], X[te], i)
            n_sel += int(te.sum())
        print(f"  {f'{lo}-{hi}':>10}{n_sel:>9,}{hit / max(1, n_sel):>17.1%}")

    # Which of the 14 carry it. The teacher uses ONE -- the opponent's melon tile count -- so any
    # feature above chance on its own is a shortcut the net is free to key on and the teacher never
    # consults.
    print("\nper-feature 1-NN (each of the 14 alone), same time split:")
    per = []
    for f in range(X.shape[1]):
        hit = n = 0
        for i, _k in enumerate(names):
            te = (~train) & (y == i)
            hit += _knn_hits(X[train][:, f:f + 1], y[train], X[te][:, f:f + 1], i)
            n += int(te.sum())
        per.append((hit / max(1, n), f))
    for r, f in sorted(per, reverse=True)[:6]:
        print(f"    feature {f:>3}   {r:>6.1%}")
    print(f"    ... {sum(1 for r, _f in per if r > 0.35)} of {X.shape[1]} features beat 35%")


main()
