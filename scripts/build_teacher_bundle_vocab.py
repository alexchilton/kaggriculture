"""Write the market bundle vocabulary from what the TAPE TEACHERS actually emit.

`scripts/build_bundle_vocab.py` builds it from label shards -- 640 recorded leaderboard games. That
is the right source for cloning the ladder and the wrong source for cloning one teacher. Measured
2026-08-22 on the four tapes:

    shipped vocabulary                197 entries
      never used by the teacher       139        <- other agents' behaviour, occupying the head
      used by the teacher, missing     90
    distinct bundles the teacher uses 148        <- fits P.N_BUNDLES = 256 with room to spare

Those 90 missing bundles were labelled EMPTY by `Vocabulary.index`'s silent fallback, on 179 of 1451
traded turns (12.3%), containing 512 HIRE and 444 SELL orders -- including the entire opening. The
student learned to emit nothing on exactly the turns that commit money.
See `docs/the_vocabulary_labels_the_opening_as_nothing_2026-08-22.md`.

This writes to a NEW path by default. It does not overwrite the shipped artifact, because other
label paths still read it and re-indexing them silently is the same class of failure this fixes.

    python -u scripts/build_teacher_bundle_vocab.py --out data/il/bundle_vocab_teacher.json
"""

import argparse
import collections
import importlib.util
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from kagg.il import market_bundles as MB                    # noqa: E402
from kagg.il.tape_teacher import TapeTeacher                # noqa: E402
from kagg.rl import jax_policy as P                         # noqa: E402
from kagg.search import schedule_agent as SA                # noqa: E402


def _dagger():
    """`scripts/` is not a package; the episode plumbing lives in `dagger_tape.py`."""
    spec = importlib.util.spec_from_file_location("dagger_tape", REPO / "scripts/dagger_tape.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def collect(turns, seeds=0, planner=False, rng_seed=0):
    """Every bundle the teachers emit, with its count, over a full season each.

    **`seeds` and `planner` must match the DAgger run this vocabulary is for.** A vocabulary is a
    sample of one teacher's market behaviour on one distribution of towns; sample the wrong one and
    `Vocabulary.index` silently returns EMPTY for anything it did not see. Measured 2026-08-28 on
    the box: the 149-entry vocabulary built here from the four RECORDED towns with the tape teacher
    could not express **361 turns** of the PLANNER teacher on fresh towns, the opening among them --
    `turn0 bundle 0/4`. That is the same failure as
    `docs/the_vocabulary_labels_the_opening_as_nothing_2026-08-22.md`, which cost a whole run.
    """
    from kaggle_environments import make

    if planner:
        SA.REPLAY_OPENING_DAYS = ()
        print("teacher: PLANNER (REPLAY_OPENING_DAYS emptied for this process)", flush=True)

    DT = _dagger()
    specs = DT.episode_specs(DT.tape_games(), DT.opponent_pool(0), seeds,
                             np.random.default_rng(rng_seed))
    seen = collections.Counter()
    for game in specs:
        env = make("kaggriculture", configuration=game["cfg"], debug=False)
        env.reset(2)
        seat = game["seat"]
        teacher = TapeTeacher(seat)
        for turn in range(turns):
            if env.done:
                break
            obs = env.state[seat].observation
            action = teacher.act(obs)
            # **Read the LIVE action, not the recorded JSON.** They are not the same object: the
            # teacher builds its market list per turn and the hires are in the live one only. The
            # earlier "coverage 100%" figure came from measuring the recording, and it was wrong.
            seen[tuple(MB.bundle_of(action.get("market") or []))] += 1
            hands = [len((env.state[0].observation["farms"][i] or {}).get("hands") or [])
                     for i in (0, 1)]
            pair = [None, None]
            pair[seat] = teacher.sendable(action, hands[seat])
            pair[1 - seat] = DT.opponent_action(game, turn, hands[1 - seat])
            env.step(pair)
        print("  %-16s seat %d  done" % (game["name"], seat), flush=True)
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "data/il/bundle_vocab_teacher.json"))
    ap.add_argument("--turns", type=int, default=719)
    ap.add_argument("--max-size", type=int, default=None,
                    help="defaults to jax_policy.N_BUNDLES -- the head cannot express more")
    ap.add_argument("--seeds", type=int, default=0,
                    help="extra town draws per game, as in dagger_tape.py. MUST match the run this "
                         "vocabulary is built for: a bundle the teacher only plays on a fresh town "
                         "is invisible to a vocabulary sampled from the recorded four.")
    ap.add_argument("--planner-teacher", action="store_true",
                    help="sample the PLANNER rather than the tape replay, to match "
                         "`dagger_tape.py --planner-teacher`. Measured 2026-08-28: mixing the two "
                         "left 361 planner turns inexpressible, including every opening.")
    args = ap.parse_args()

    max_size = args.max_size or P.N_BUNDLES
    print("collecting from the tape teachers, %d turns each, %d extra seeds, planner=%s"
          % (args.turns, args.seeds, args.planner_teacher), flush=True)
    seen = collect(args.turns, seeds=args.seeds, planner=args.planner_teacher)

    # Most frequent first, so a truncation drops the rarest -- but a truncation here is a defect,
    # not a trade-off, and the check below refuses rather than reporting a percentage.
    ordered = [b for b, _n in seen.most_common()]
    print("\nturns seen                %d" % sum(seen.values()))
    print("distinct bundles          %d" % len(ordered))
    print("head width                %d" % max_size)
    if len(ordered) > max_size:
        raise SystemExit(
            "%d distinct bundles against a %d-wide head. Truncating would make the dropped ones "
            "unemittable and label them EMPTY -- the exact defect this script exists to fix. Widen "
            "jax_policy.N_BUNDLES instead." % (len(ordered), max_size))

    # EMPTY must be index 0. `decode_action` and every mask treat 0 as "place no orders", and the
    # counter above puts it first anyway; this makes that a guarantee rather than a coincidence.
    empty = MB.bundle_of([])
    ordered = [empty] + [b for b in ordered if b != empty]

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([[list(pair) for pair in b] for b in ordered], indent=0))
    print("\nwrote %d entries to %s" % (len(ordered), out))

    # Round-trip through the real loader, so a format mistake fails here and not mid-run.
    check = MB.load_vocab(str(out))
    assert check.index(empty) == 0, "EMPTY must be index 0"
    missing = [b for b in seen if tuple(b) not in check._index]
    print("coverage check: %d/%d distinct bundles, %d missing"
          % (len(seen) - len(missing), len(seen), len(missing)))
    if missing:
        raise SystemExit("the file just written cannot express %d of its own bundles" % len(missing))


if __name__ == "__main__":
    main()
