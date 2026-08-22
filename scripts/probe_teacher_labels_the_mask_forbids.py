"""Which teacher labels can the student never emit and never be taught? Per op, whole season.

**This is the check that would have caught all three LOCKED bugs at once, and it did not exist.**
`0f27ae8` and `d23fc85` were found by chasing a single stuck op backwards from an agreement table.
That works, slowly, and only for an op the training happens to sample often enough to notice.

A label the mask calls illegal is blocked twice over:

  - `greedy_action` argmaxes over `_masked_logits`, so the op carries -1e9 and is unemittable at
    any parameter setting;
  - `bc.py:232` gives an illegal label weight zero, so it never reaches the gradient either.

The two together mean a masking mistake is invisible in the loss, invisible in the sampled
agreement, and shows up only as one op sitting at a value that never moves. So check the labels
directly instead.

    python -u scripts/probe_teacher_labels_the_mask_forbids.py            # all four tapes, d0-d30
    python -u scripts/probe_teacher_labels_the_mask_forbids.py --horizon 120

The teacher drives every turn, so the states are exactly the ones behaviour cloning trains on. No
checkpoint is loaded and no network is run: this is a property of the mask and the tape, not of any
particular set of weights.

**A nonzero count is not automatically a bug.** The mask is allowed to forbid what the reference
would silently no-op. Read the offenders it prints: if the reference would have executed the action,
the mask is wrong; if the reference would have ignored it, the teacher wasted a turn and the mask is
right to say so.
"""

import argparse
import collections
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from kagg.il import market_bundles as MB, replays as RP           # noqa: E402
from kagg.il.tape_teacher import TapeTeacher                      # noqa: E402
from kagg.rl import adapter as AD, jax_act as A                   # noqa: E402
from kagg.sim import ops as O                                     # noqa: E402

TPD = 24
OP_NAME = {v: k for k, v in RP.OP_CODE.items()}


def op_label(code):
    return OP_NAME.get(int(code), "op%d" % int(code))


def scan(spec, vocab, bundle_ok, horizon):
    """Step one tape with the teacher driving; count labels the mask forbids, per op."""
    from kaggle_environments import make

    env = make("kaggriculture", configuration=spec["cfg"], debug=False)
    env.reset(2)
    seat = spec["seat"]
    teacher = TapeTeacher(seat)

    seen = collections.Counter()
    blocked = collections.Counter()
    examples = collections.defaultdict(list)

    for turn in range(horizon):
        if env.done:
            break
        obs = env.state[seat].observation
        teacher_action = teacher.act(obs)

        privates = [obs["private"] if p == seat else AD.agent_private_stub()
                    for p in range(2)]
        # `step=turn`: seat 1 gets no `step` in its observation, and a day-0 clock forbids HARVEST
        # everywhere. That was this probe's own first finding -- see the test named in the fix.
        sim_state = AD.state_from_obs(obs, privates, step=turn)
        masks = A.masks_for(sim_state, bundle_ok)

        n_units = 1 + len(obs["farms"][seat].get("hands") or [])
        labels = RP.encode_action(teacher_action, n_units, vocab=vocab)
        op_mask = np.asarray(masks["op"]).reshape(2, -1, np.asarray(masks["op"]).shape[-1])[seat]

        for u in range(n_units):
            code = int(labels["op"][u])
            name = op_label(code)
            seen[name] += 1
            if not bool(op_mask[u, code]):
                blocked[name] += 1
                if len(examples[name]) < 4:
                    farm = obs["farms"][seat]
                    pos = ([tuple(farm.get("farmer") or (0, 0))]
                           + [tuple(h) for h in (farm.get("hands") or [])])
                    tiles = farm.get("tiles") or []
                    x, y = pos[u] if u < len(pos) else (-1, -1)
                    cell = tiles[y][x] if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]) else "?"
                    kind = cell if isinstance(cell, str) else (
                        cell.get("kind") if isinstance(cell, dict) else "EMPTY")
                    examples[name].append(
                        "turn %3d day %2d unit %d at (%d,%d) on %s" % (
                            turn, turn // TPD, u, x, y, kind))

        env.step([teacher_action if p == seat else (spec["opponent"][turn]
                                                    if turn < len(spec["opponent"]) else {})
                  for p in range(2)])

    return seen, blocked, examples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizon", type=int, default=719)
    ap.add_argument("--vocab", default=str(REPO / "data/il/bundle_vocab_teacher.json"))
    args = ap.parse_args()

    import dagger_tape as DT

    vocab = MB.load_vocab(args.vocab)
    bundle_ok = MB.valid_table(vocab)
    games = DT.tape_games()

    total_seen = collections.Counter()
    total_blocked = collections.Counter()
    all_examples = collections.defaultdict(list)

    for spec in games:
        seen, blocked, examples = scan(spec, vocab, bundle_ok, args.horizon)
        total_seen.update(seen)
        total_blocked.update(blocked)
        for k, v in examples.items():
            all_examples[k].extend(v[:2])
        print("  %-16s %6d labels, %4d forbidden" % (spec["name"], sum(seen.values()),
                                                     sum(blocked.values())), flush=True)

    print()
    print("teacher labels the mask forbids, over %d turns x %d tapes:" % (args.horizon, len(games)))
    print("  %-22s %8s %10s %8s" % ("op", "seen", "forbidden", "rate"))
    for name in sorted(total_seen, key=lambda n: -total_blocked[n]):
        n_bad = total_blocked[name]
        print("  %-22s %8d %10d %7.3f%%"
              % (name, total_seen[name], n_bad, 100.0 * n_bad / max(1, total_seen[name])))

    n_bad = sum(total_blocked.values())
    n_all = sum(total_seen.values())
    print()
    print("TOTAL %d of %d unit labels forbidden (%.3f%%)" % (n_bad, n_all, 100.0 * n_bad / max(1, n_all)))
    if n_bad:
        print()
        print("first offenders per op -- check each against reference/kaggriculture.py:")
        for name in sorted(all_examples):
            for line in all_examples[name][:4]:
                print("  %-22s %s" % (name, line))


if __name__ == "__main__":
    main()
