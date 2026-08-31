"""The round-27 DAgger net against a verbatim tape replay, on foreign seeds.

    python -u scripts/duel_net_vs_tape.py --seeds 24 \
        --b /path/to/submission/main_dusta_clone_land.py

WHAT THIS ARM CHANGES, and what would have to be true for it to win
------------------------------------------------------------------
The tape side replays one recorded action stream verbatim. The net side is
`data/dagger_tape/season_fast-20260822-235031/pinned_round27.pkl`, a policy cloned from the tape
TEACHER at `greedy op 0.9997 / bundle 1.0000` (`docs/the_clone_only_misses_the_unlearnable_digs_2026-08-23.md`).

A tape does not transplant: measured -$13,896 over these same 24 seeds when Dusta's tape met
Diment's. The net can only beat that if it is reading the BOARD. If it memorised the 54-wide clock
one-hot that `jax_obs` hands it -- which the probe's own docstring says 1.0000 on-tape is consistent
with -- then it emits the teacher's turn-t action whatever the state is, which is a tape replay with
extra steps, and it should score like one or worse.

So: net >= tape means the clone generalises. net << tape means it is a clock lookup.

Both nets were trained with `weedSpawnChance` 0.0 on four fixed seeds. 0.005 and seeds 9000+ are
deliberately out of distribution -- that is the question, not a flaw in the harness.

Seats swap on odd seeds: seat 0 commits first when both players' orders land in the same slot
(`reference/kaggriculture.py:614`). Rows flush as they finish.

THE VOCABULARY IS NOT OPTIONAL, and the default is wrong for this checkpoint
---------------------------------------------------------------------------
`pinned_round27.pkl` embeds no bundle list, so `neural.make_agent` falls back to
`data/il/bundle_vocab.json` and says so loudly. That file holds 197 bundles; the checkpoint records
`vocab_size = 149`, and its `vocab_path` names `bundle_vocab_teacher.json`, which now holds 151
because it was topped up at 12:56 on 2026-08-23 -- after the round-27 pin was written at 10:02.
`Vocabulary.from_bundles` sorts, so adding two bundles moves every index above them.

The only 149-bundle file on disk is `bundle_vocab_teacher_pre_topup.json`, and that is the default
here. Run with the wrong one and the net emits six SELL orders into an empty shed on turn 0 and
banks $0 -- measured, and it reads exactly like a policy that cannot play.
"""
import argparse
import csv
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

CKPT = "data/dagger_tape/season_fast-20260822-235031/pinned_round27.pkl"


def load_file(path):
    p = pathlib.Path(path)
    ns = {}
    exec(compile(p.read_text(), str(p), "exec"), ns)
    return [v for v in ns.values() if callable(v)][-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--base", type=int, default=9000)
    ap.add_argument("--ckpt", default=CKPT)
    ap.add_argument("--b", required=True, help="path to a generated submission .py")
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--csv", default="data/logs/net_vs_tape.csv")
    ap.add_argument("--vocab", default="data/il/bundle_vocab_teacher_pre_topup.json")
    args = ap.parse_args()

    from kaggle_environments import make

    from kagg.agents import neural
    from kagg.il import market_bundles as MB
    from kagg.rl import jax_policy as P

    # Force the checkpoint's own vocabulary. `make_agent` has no argument for it and falls back to
    # the wrong file for this checkpoint -- see the module docstring. Patched rather than edited so
    # nothing that ships changes.
    import pickle
    with open(args.ckpt, "rb") as fh:
        want = pickle.load(fh).get("vocab_size")
    bundles = json.loads(pathlib.Path(args.vocab).read_text())
    assert len(bundles) == want, (
        f"{args.vocab} holds {len(bundles)} bundles, the checkpoint was fitted against {want}. "
        f"Every index above the difference would decode as a different order.")
    _v = MB.Vocabulary.from_bundles([tuple(tuple(p) for p in b) for b in bundles],
                                    max_size=P.N_BUNDLES)
    MB.load_vocab = lambda *a, **k: _v
    print(f"vocab {args.vocab}  {len(bundles)} bundles, matches the checkpoint")

    A = neural.make_agent(args.ckpt)
    B = load_file(args.b)
    na = "round27_net"
    nb = pathlib.Path(args.b).stem.replace("main_", "")

    out = REPO / args.csv
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w", newline="")
    w = csv.writer(fh)
    w.writerow(["seed", "a_seat", na, nb, "delta", "winner", "worst_ms"])
    fh.flush()

    print(f"{na} vs {nb}, {args.seeds} seeds, weeds {args.weeds}, seats swapped")
    print(f"ckpt {args.ckpt}")
    print(f"    {'seed':>6}{na[:11]:>13}{nb[:11]:>13}{'delta':>11}  {'ms':>5}  winner")
    wins = {na: 0, nb: 0, "draw": 0}
    tot = 0.0
    for i in range(args.seeds):
        seed = args.base + i
        sa = i % 2
        env = make("kaggriculture",
                   configuration={"seed": seed, "weedSpawnChance": args.weeds}, debug=False)
        env.reset(2)
        worst = 0.0
        for _ in range(719):
            act = [None, None]
            t0 = time.time()
            act[sa] = A(env.state[sa].observation, None)
            worst = max(worst, (time.time() - t0) * 1000.0)
            act[1 - sa] = B(env.state[1 - sa].observation, None)
            env.step(act)
        o = env.state[0].observation
        ma = float(o["farms"][sa]["money"])
        mb = float(o["farms"][1 - sa]["money"])
        d = ma - mb
        who = na if d > 0 else nb if d < 0 else "draw"
        wins[who] += 1
        tot += d
        print(f"    {seed:>6}{ma:>13,.0f}{mb:>13,.0f}{d:>+11,.0f}  {worst:>5.0f}  {who}")
        w.writerow([seed, sa, f"{ma:.0f}", f"{mb:.0f}", f"{d:.0f}", who, f"{worst:.0f}"])
        fh.flush()

    fh.close()
    print(f"\n  {na} {wins[na]}, {nb} {wins[nb]}, draws {wins['draw']} of {args.seeds}")
    print(f"  mean delta {tot / max(1, args.seeds):+,.0f}")


main()
