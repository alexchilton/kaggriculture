"""Task #19/#11: score a chain genome in the REAL environment, on fresh seeds, with weeds.

Every number the chain search produces -- $64,146, 16/16 -- comes from `jax_sim` against four
*recorded* opponent tapes on one seed with `weed_chance=0.0`, and every run prints its own disclaimer
to that effect. This is the gate that disclaimer points at:

* `kaggle_environments` rather than our simulator, so a parity gap shows up as a score gap;
* the pool agents playing *live*, not a tape of one seat of one seed;
* fresh seeds, both seatings, weeds on -- the ladder's own defaults;
* **win rate**, because the ladder is Elo and a $43k win scores the same as a $4k win.

**Read the mean bank before believing any win rate.** A farm that banks exactly $3,000 did nothing at
all: that is the opening stake, and it is how CLAUDE.md's "verify built artifacts actually run" lesson
was learned the first time. This script hit it too -- the first version returned a list where the env
wants `{"farmer": ..., "hands": ..., "market": ...}` and read `obs["players"]` for a field that is
called `farms`, so it scored 0.000 against `starter` while the genome itself was fine.

    PYTHONPATH=. .venv/bin/python -u scripts/arena_gate.py --seeds 20
"""

import argparse
import sys

import numpy as np


# Module level, and rebuilt from `_GENOME` on first use in each worker, because `run_arena` fans out
# over processes and a closure cannot be pickled.
_GENOME = None
_PLAN = None


def _get(obs, key, default=None):
    if isinstance(obs, dict):
        return obs.get(key, default)
    return getattr(obs, key, default)


def _plan():
    """Resolve the genome into the same per-turn plan `build_script_submission.py` would ship.

    Anything else would be testing an artifact we would not submit.
    """
    global _PLAN
    if _PLAN is None:
        from kagg.search import chains as C

        sys.path.insert(0, "scripts")
        import build_script_submission as B

        path, n_slots = _GENOME
        genome = np.asarray(np.load(path)["genome"], dtype=np.int64)
        script, _used, _skipped = C.decode(genome, n_slots)
        _PLAN = B.build_plan(script.arrays())
    return _PLAN


def agent(obs, config=None):
    plan = _plan()
    step = int(_get(obs, "step", 0) or 0)
    if step >= len(plan):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    farmer, hands, market = plan[step]
    # Truncate to the hands the farm actually owns: the reference's atomic PLANT rule counts the
    # actions *submitted*, so a padded list can block plants no real agent could block.
    n_hands = 0
    farms = _get(obs, "farms")
    if farms:
        me = int(_get(obs, "player", 0) or 0)
        if me < len(farms):
            n_hands = len(farms[me].get("hands", []) or [])
    return {"farmer": farmer, "hands": hands[:n_hands], "market": market}


def _opponent(name):
    """`kaggle_environments` resolves its own built-ins by name; ours live in `kagg.agents`."""
    import importlib

    try:
        return getattr(importlib.import_module(f"kagg.agents.{name}"), "agent")
    except ModuleNotFoundError:
        return name          # a built-in like `starter` or `pass`


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--genome", default="data/chain_search_s8/best_beam_genome.npz")
    ap.add_argument("--slots", type=int, default=8)
    ap.add_argument("--seeds", type=int, default=20)
    # **1, not 12, and this is not a performance choice.** `ProcessPoolExecutor` on macOS spawns
    # rather than forks, so each worker re-imports this module with `_GENOME` unset. `_plan()` then
    # cannot build the tape, `agent()` falls back to `{"farmer": ["PASS"]}` every turn, and the gate
    # reports our bank as exactly $3,000 with a 0.000 win rate against every opponent -- while the same
    # tape banks $41,041 against `starter` when played in-process.
    #
    # It also silently dropped two of six opponents: `make_agent` returns a closure, and
    # "Can't pickle local object 'make_agent.<locals>.agent'" removed `homestead` and `shepherd` from
    # the pool entirely. Sequential play has neither problem, and a gate that measures its own plumbing
    # is worse than no gate -- it reads as "the agent does nothing" when the agent is fine.
    ap.add_argument("--workers", type=int, default=1)
    # `starter` is included only as a floor check, never as the verdict: CLAUDE.md records that it
    # sells almost nothing, so the market is never contested and its numbers run ~2x reality. v4
    # scored $43.6k against `starter` and then lost its ranked matches at a rating of 429.9.
    ap.add_argument("--opponents",
                    default="starter,heuristic,rancher,homestead,contrarian,shepherd")
    args = ap.parse_args()

    from kagg.arena import run_arena
    from kagg.search import chains as C

    global _GENOME
    _GENOME = (args.genome, args.slots)
    genome = np.asarray(np.load(args.genome)["genome"], dtype=np.int64)
    _script, used, skipped = C.decode(genome, args.slots)
    print(f"genome {args.genome}  slots={args.slots}  chains skipped={skipped}")
    for u in used:
        print(f"    {u}")
    print()

    print(f"{'opponent':>12} {'games':>7} {'win rate':>9} {'draws':>7} {'our mean $':>12} "
          f"{'their mean $':>13} {'delta':>11}")
    rows = []
    for name in args.opponents.split(","):
        name = name.strip()
        try:
            rep = run_arena(agent, _opponent(name), seeds=range(args.seeds),
                            workers=args.workers)
        except Exception as exc:                  # noqa: BLE001 - report, do not abort the sweep
            print(f"{name:>12}  FAILED: {type(exc).__name__}: {exc}", flush=True)
            continue
        flag = "   <-- DID NOTHING" if abs(rep.mean_money[0] - 3000) < 1 else ""
        print(f"{name:>12} {rep.games:>7} {rep.win_rate:>9.3f} {rep.draw_rate:>7.3f} "
              f"{rep.mean_money[0]:>12,.0f} {rep.mean_money[1]:>13,.0f} "
              f"{rep.mean_delta:>+11,.0f}{flag}", flush=True)
        rows.append((name, rep))

    if rows:
        wr = float(np.mean([r[1].win_rate for r in rows]))
        print(f"\npool mean win rate: {wr:.3f} across {len(rows)} opponents, {args.seeds} seeds, "
              f"both seatings, weeds ON (real kaggle_environments)")
        print("Selection criterion is win rate, not money (CLAUDE.md): the ladder is Elo.")
        worst = min(rows, key=lambda r: r[1].win_rate)
        print(f"worst matchup: {worst[0]} at {worst[1].win_rate:.3f}")


if __name__ == "__main__":
    main()
